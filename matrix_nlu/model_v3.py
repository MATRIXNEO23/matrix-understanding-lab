"""Student-5-compatible encoder adapter and compact Matrix-NLU V3 heads.

Torch/Transformers are imported lazily so registry and structural tests remain
data-independent.  No optimizer or training operation exists in this module.
"""

from __future__ import annotations

from typing import Any

from contract_v3 import FIXED_SEQUENCE_LABELS, ROLE_HEADS, TOKEN_LABELS


def encoder_hidden_size(encoder: Any) -> int:
    config = encoder.config
    for name in ("hidden_size", "dim", "d_model"):
        value = getattr(config, name, None)
        if value is not None:
            return int(value)
    raise ValueError("unsupported encoder config: no hidden size")


def encoder_layer_container(encoder: Any):
    """Return (parent, attribute, layers) for BERT or DistilBERT-style models."""
    bert_parent = getattr(encoder, "encoder", None)
    if bert_parent is not None and hasattr(bert_parent, "layer"):
        return bert_parent, "layer", bert_parent.layer
    distil_parent = getattr(encoder, "transformer", None)
    if distil_parent is not None and hasattr(distil_parent, "layer"):
        return distil_parent, "layer", distil_parent.layer
    raise ValueError("unsupported encoder: expected encoder.layer or transformer.layer")


def encoder_layer_count(encoder: Any) -> int:
    return len(encoder_layer_container(encoder)[2])


def head_parameter_estimate(hidden_size: int) -> dict:
    """Exact parameter count for the V3 head implementation below."""
    token_outputs = sum(len(values) for values in TOKEN_LABELS.values())
    sequence_outputs = sum(len(values) for values in FIXED_SEQUENCE_LABELS.values())
    token = hidden_size * token_outputs + token_outputs
    fixed_sequence = hidden_size * sequence_outputs + sequence_outputs
    shared_pointer_projection = hidden_size * hidden_size
    role_queries = len(ROLE_HEADS) * hidden_size
    pointer_specials = 2 * hidden_size
    total = token + fixed_sequence + shared_pointer_projection + role_queries + pointer_specials
    return {
        "tokenHeads": token,
        "fixedSequenceHeads": fixed_sequence,
        "sharedPointerProjection": shared_pointer_projection,
        "roleQueries": role_queries,
        "pointerSpecialEmbeddings": pointer_specials,
        "totalV3Heads": total,
        "estimatedFp32Bytes": total * 4,
        "estimatedInt8BytesWhereEligible": total,
    }


def build_model_v3(
    model_name_or_path: str | None = None,
    revision: str | None = None,
    *,
    encoder=None,
    local_files_only: bool = False,
):
    """Attach the frozen V3 heads to an injected or pristine HF encoder."""
    import torch
    import torch.nn as nn

    if encoder is None:
        if not model_name_or_path:
            raise ValueError("model_name_or_path is required when encoder is not injected")
        from transformers import AutoModel
        encoder = AutoModel.from_pretrained(
            model_name_or_path,
            revision=revision,
            trust_remote_code=False,
            local_files_only=local_files_only,
        )
    hidden_size = encoder_hidden_size(encoder)

    class MatrixNluV3Model(nn.Module):
        def __init__(self, backbone):
            super().__init__()
            self.encoder = backbone
            self.hidden_size = hidden_size
            self.dropout = nn.Dropout(0.1)
            self.token_heads = nn.ModuleDict({
                name: nn.Linear(hidden_size, len(labels))
                for name, labels in TOKEN_LABELS.items()
            })
            self.fixed_sequence_heads = nn.ModuleDict({
                name: nn.Linear(hidden_size, len(labels))
                for name, labels in FIXED_SEQUENCE_LABELS.items()
            })
            self.candidate_projection = nn.Linear(hidden_size, hidden_size, bias=False)
            self.role_queries = nn.ParameterDict({
                name: nn.Parameter(torch.empty(hidden_size)) for name in ROLE_HEADS
            })
            self.pointer_special_embeddings = nn.Parameter(torch.empty(2, hidden_size))
            nn.init.normal_(self.pointer_special_embeddings, mean=0.0, std=0.02)
            for query in self.role_queries.values():
                nn.init.normal_(query, mean=0.0, std=0.02)

        def forward(self, input_ids, attention_mask, candidate_embeddings, candidate_mask):
            hidden = self.encoder(
                input_ids=input_ids,
                attention_mask=attention_mask,
            ).last_hidden_state
            token_hidden = self.dropout(hidden)
            pooled = self.dropout(hidden[:, 0])
            if candidate_embeddings.shape[-1] != self.hidden_size:
                raise ValueError("candidate embedding hidden size mismatch")
            projected = self.candidate_projection(candidate_embeddings)
            batch = projected.shape[0]
            specials = self.pointer_special_embeddings.unsqueeze(0).expand(batch, -1, -1)
            all_candidates = torch.cat((projected, specials), dim=1)
            special_mask = torch.ones((batch, 2), dtype=candidate_mask.dtype, device=candidate_mask.device)
            all_mask = torch.cat((candidate_mask, special_mask), dim=1)
            pointer_logits = {}
            scale = float(self.hidden_size) ** -0.5
            for name in ROLE_HEADS:
                query = pooled + self.role_queries[name]
                logits = torch.bmm(all_candidates, query.unsqueeze(-1)).squeeze(-1) * scale
                pointer_logits[name] = logits.masked_fill(all_mask == 0, -1e4)
            return {
                "tokens": {name: head(token_hidden) for name, head in self.token_heads.items()},
                "sequence": {
                    **{name: head(pooled) for name, head in self.fixed_sequence_heads.items()},
                    **pointer_logits,
                },
            }

    return MatrixNluV3Model(encoder)


def parameter_summary_v3(model) -> dict:
    total = sum(parameter.numel() for parameter in model.parameters())
    encoder = sum(parameter.numel() for parameter in model.encoder.parameters())
    return {
        "total": total,
        "encoder": encoder,
        "heads": total - encoder,
        "encoderLayers": encoder_layer_count(model.encoder),
        "hiddenSize": encoder_hidden_size(model.encoder),
    }
