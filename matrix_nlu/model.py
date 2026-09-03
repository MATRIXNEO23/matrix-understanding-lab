"""Shared compact encoder and learned Matrix/MASSIVE multi-task heads."""

from __future__ import annotations

import json
import pathlib

from labels import SEQUENCE_LABELS, TOKEN_LABELS


def build_model(model_name: str, revision: str, massive_intents: int,
                massive_slots: int, student_layers: int | None = None):
    import torch.nn as nn
    from transformers import AutoModel

    class MatrixMultiTaskModel(nn.Module):
        def __init__(self):
            super().__init__()
            self.encoder = AutoModel.from_pretrained(model_name, revision=revision,
                                                     trust_remote_code=False)
            if student_layers is not None:
                layers = self.encoder.transformer.layer
                if student_layers >= len(layers) or student_layers < 2:
                    raise ValueError("student layer count must be between 2 and teacher_layers-1")
                # Evenly retain pretrained layers including the final layer.
                indices = [round(i * (len(layers) - 1) / (student_layers - 1))
                           for i in range(student_layers)]
                self.encoder.transformer.layer = nn.ModuleList([layers[i] for i in indices])
                self.encoder.config.n_layers = student_layers
            hidden = self.encoder.config.dim
            self.dropout = nn.Dropout(0.1)
            self.token_heads = nn.ModuleDict({
                head: nn.Linear(hidden, len(values)) for head, values in TOKEN_LABELS.items()
            })
            self.sequence_heads = nn.ModuleDict({
                head: nn.Linear(hidden, len(values)) for head, values in SEQUENCE_LABELS.items()
            })
            self.massive_intent = nn.Linear(hidden, massive_intents)
            self.massive_slot = nn.Linear(hidden, massive_slots)

        def forward(self, input_ids, attention_mask):
            hidden = self.encoder(input_ids=input_ids, attention_mask=attention_mask).last_hidden_state
            token_hidden = self.dropout(hidden)
            pooled = self.dropout(hidden[:, 0])
            return {
                "tokens": {name: head(token_hidden) for name, head in self.token_heads.items()},
                "sequence": {name: head(pooled) for name, head in self.sequence_heads.items()},
                "massive_intent": self.massive_intent(pooled),
                "massive_slot": self.massive_slot(token_hidden),
            }

    return MatrixMultiTaskModel()


def parameter_summary(model) -> dict:
    total = sum(parameter.numel() for parameter in model.parameters())
    trainable = sum(parameter.numel() for parameter in model.parameters() if parameter.requires_grad)
    encoder = sum(parameter.numel() for parameter in model.encoder.parameters())
    return {"total": total, "trainable": trainable, "encoder": encoder,
            "heads": total - encoder, "encoderLayers": model.encoder.config.n_layers}
