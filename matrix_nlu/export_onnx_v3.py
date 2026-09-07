"""Structural ONNX contract for an untrained Matrix-NLU V3 model."""

from __future__ import annotations

from contract_v3 import ROLE_HEADS, SEQUENCE_HEADS, TOKEN_HEADS


INPUT_NAMES = (
    "input_ids",
    "attention_mask",
    "candidate_embeddings",
    "candidate_mask",
    "temporal_anchor_embeddings",
    "temporal_anchor_mask",
)
OUTPUT_NAMES = tuple(
    [f"token.{name}" for name in TOKEN_HEADS]
    + [f"sequence.{name}" for name in SEQUENCE_HEADS if name != "temporalRelation"]
    + ["sequence.temporalRelation.relation", "sequence.temporalRelation.anchor"]
)


def structural_export_spec() -> dict:
    return {
        "opset": 17,
        "inputs": list(INPUT_NAMES),
        "outputs": list(OUTPUT_NAMES),
        "dynamicAxes": {
            "input_ids": {0: "batch", 1: "sequence"},
            "attention_mask": {0: "batch", 1: "sequence"},
            "candidate_embeddings": {0: "batch", 1: "candidates"},
            "candidate_mask": {0: "batch", 1: "candidates"},
            "temporal_anchor_embeddings": {0: "batch", 1: "temporal_anchors"},
            "temporal_anchor_mask": {0: "batch", 1: "temporal_anchors"},
            **{f"token.{name}": {0: "batch", 1: "sequence"} for name in TOKEN_HEADS},
            **{f"sequence.{name}": {0: "batch"} for name in SEQUENCE_HEADS if name != "temporalRelation"},
            "sequence.temporalRelation.relation": {0: "batch"},
            "sequence.temporalRelation.anchor": {0: "batch", 1: "temporal_anchors"},
        },
        "pointerCandidateDimension": "dynamic candidates + NONE + UNKNOWN",
        "temporalAnchorDimension": "dynamic speech/context/evidence/claim anchors",
        "expectedStandardOperators": [
            "Gather", "MatMul", "Add", "Concat", "Equal", "Where", "Softmax",
        ],
        "customOperators": [],
        "roleHeads": list(ROLE_HEADS),
        "qualityMeaning": "NONE_UNTRAINED_STRUCTURAL_PROBE_ONLY",
    }


def export_model_v3(model, sample_inputs, output_path):
    """Execute the canonical V3 export spec on a real, caller-owned model.

    The wrapper only flattens named model outputs into the frozen tensor order.
    It does not change weights, labels, masks or candidate semantics.
    """
    import torch

    class FlatOutputs(torch.nn.Module):
        def __init__(self, wrapped):
            super().__init__()
            self.wrapped = wrapped

        def forward(self, *inputs):
            result = self.wrapped(*inputs)
            tensors = []
            for name in OUTPUT_NAMES:
                parts = name.split(".")
                value = result["tokens" if parts[0] == "token" else "sequence"][parts[1]]
                if len(parts) == 3:
                    value = value[parts[2]]
                tensors.append(value)
            return tuple(tensors)

    spec = structural_export_spec()
    torch.onnx.export(
        FlatOutputs(model).eval(), tuple(sample_inputs), str(output_path),
        input_names=spec["inputs"], output_names=spec["outputs"],
        dynamic_axes=spec["dynamicAxes"], opset_version=spec["opset"],
        do_constant_folding=True,
    )
    return spec
