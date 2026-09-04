#!/usr/bin/env python3
"""Export Matrix-NLU to ONNX with mixed/head-protected INT8 quantization.

This path is intentionally experimental.  It may be used for practical runtime
experiments after a dev-gate failure, but it must not promote the model, read
frozen data, or produce a production-approved artifact.

Policy:
- export an FP32 ONNX reference;
- quantize encoder/body MatMul/Gemm weights dynamically to INT8;
- exclude all Matrix semantic heads from quantization:
  - token heads: boundary, object, subject, negation, temporal, entity;
  - sequence heads: dialogueAct, predicate, subjectReferent, targetReferent,
    ownerReferent, perspectiveReferent, polarity, temporalRelation, claimKind;
- leave MASSIVE auxiliary heads unprotected because they are not the runtime
  authority/memory surface for Matrix Engine.
"""

from __future__ import annotations

import argparse
import json
import pathlib
import time

from export_onnx import OUTPUT_NAMES, flatten, latency, parity, sha256
from labels import SEQUENCE_LABELS, TOKEN_LABELS
from inference import MatrixNluRuntime


TOKEN_HEADS = tuple(TOKEN_LABELS)
SEQUENCE_HEADS = tuple(SEQUENCE_LABELS)
PROTECTED_TOKEN_HEADS = TOKEN_HEADS
PROTECTED_SEQUENCE_HEADS = SEQUENCE_HEADS
PROTECTED_HEAD_MARKERS = tuple(
    [f"token_heads.{name}" for name in PROTECTED_TOKEN_HEADS]
    + [f"sequence_heads.{name}" for name in PROTECTED_SEQUENCE_HEADS]
)
PROTECTED_OUTPUTS = tuple(
    [f"token.{name}" for name in PROTECTED_TOKEN_HEADS]
    + [f"sequence.{name}" for name in PROTECTED_SEQUENCE_HEADS]
)
EXPERIMENTAL_STATUS = "EXPERIMENTAL_TEST_CANDIDATE_NOT_PRODUCTION_APPROVED"
LINEAR_OPS = frozenset({"MatMul", "Gemm"})
QUANTIZED_LINEAR_OPS = frozenset({"MatMulInteger", "QLinearMatMul", "QGemm"})


def _blob(items) -> str:
    return "\n".join(item for item in items if item)


def _node_text(node) -> str:
    return _blob([node.name, node.op_type, *node.input, *node.output])


def protected_nodes(model_path: pathlib.Path, outputs=PROTECTED_OUTPUTS) -> dict:
    """Return each protected output's linear producer.

    PyTorch may export a head as ``Add(MatMul(...), bias)`` and ONNX Runtime
    rewrites ``Gemm`` to ``MatMul`` before dynamic quantization.  Following the
    output edge is therefore safer than relying on initializer-name markers.
    """
    import onnx

    model = onnx.load(str(model_path))
    producers = {output: node for node in model.graph.node for output in node.output}
    grouped = {output: [] for output in outputs}
    terminal_ops = LINEAR_OPS | QUANTIZED_LINEAR_OPS
    for output in outputs:
        pending = [output]
        visited = set()
        while pending:
            value = pending.pop()
            node = producers.get(value)
            if node is None or id(node) in visited:
                continue
            visited.add(id(node))
            if node.op_type in terminal_ops:
                name = node.name or next(iter(node.output), "")
                if name:
                    grouped[output].append(name)
                continue
            pending.extend(node.input)
    return grouped


def encoder_quantizable_nodes(model_path: pathlib.Path) -> list[str]:
    """Select only encoder/backbone linear nodes for INT8 conversion."""
    import onnx

    model = onnx.load(str(model_path))
    return [
        node.name
        for node in model.graph.node
        if node.name and node.op_type in LINEAR_OPS and "/encoder/" in _node_text(node)
    ]


def quantizer_exclusion_names(model_path: pathlib.Path, grouped: dict) -> list[str]:
    """Include Gemm names after ONNX Runtime's internal Gemm-to-MatMul rewrite."""
    import onnx

    model = onnx.load(str(model_path))
    op_by_name = {node.name: node.op_type for node in model.graph.node}
    names = flatten_grouped_nodes(grouped)
    rewritten = [name + "_MatMul" for name in names if op_by_name.get(name) == "Gemm"]
    return flatten_grouped_nodes({"original": names, "rewritten": rewritten})


def flatten_grouped_nodes(grouped: dict) -> list[str]:
    seen = set()
    ordered = []
    for names in grouped.values():
        for name in names:
            if name not in seen:
                seen.add(name)
                ordered.append(name)
    return ordered


def missing_markers(grouped: dict) -> list[str]:
    return [marker for marker, names in grouped.items() if not names]


def protected_weight_names(model_path: pathlib.Path, grouped: dict) -> dict:
    """Resolve protected head weights from their FP32 compute nodes."""
    import onnx

    model = onnx.load(str(model_path))
    initializers = {initializer.name for initializer in model.graph.initializer}
    nodes = {node.name: node for node in model.graph.node}
    return {
        output: [
            value
            for name in names
            for value in nodes[name].input
            if value in initializers
        ]
        for output, names in grouped.items()
    }


def verify_protected_initializers_remain_float(fp32_path: pathlib.Path,
                                               mixed_path: pathlib.Path,
                                               fp32_grouped: dict) -> dict:
    import onnx
    from onnx import TensorProto

    model = onnx.load(str(mixed_path))
    initializers = {initializer.name: initializer for initializer in model.graph.initializer}
    weights = protected_weight_names(fp32_path, fp32_grouped)
    protected = []
    violations = []
    for output, names in weights.items():
        for name in names:
            initializer = initializers.get(name)
            entry = {
                "output": output,
                "name": name,
                "present": initializer is not None,
                "dataType": int(initializer.data_type) if initializer is not None else None,
                "isFloat": bool(initializer is not None and
                                initializer.data_type == TensorProto.FLOAT),
            }
            protected.append(entry)
            if not entry["isFloat"]:
                violations.append(entry)

    mixed_grouped = protected_nodes(mixed_path)
    mixed_nodes = {node.name: node for node in model.graph.node}
    compute = []
    missing_outputs = []
    for output, names in mixed_grouped.items():
        if not names:
            missing_outputs.append(output)
        for name in names:
            node = mixed_nodes[name]
            entry = {"output": output, "name": name, "opType": node.op_type}
            compute.append(entry)
            if node.op_type in QUANTIZED_LINEAR_OPS:
                violations.append(entry)
    return {
        "protectedInitializers": protected,
        "protectedComputeNodes": compute,
        "missingProtectedOutputs": missing_outputs,
        "violations": violations,
    }


def quantized_ops(model_path: pathlib.Path) -> dict:
    import onnx

    model = onnx.load(str(model_path))
    counts = {}
    for node in model.graph.node:
        counts[node.op_type] = counts.get(node.op_type, 0) + 1
    return counts


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--bundle", type=pathlib.Path, required=True)
    parser.add_argument("--output-dir", type=pathlib.Path, required=True)
    parser.add_argument("--repetitions", type=int, default=30)
    parser.add_argument(
        "--allow-missing-protected-node-marker",
        action="store_true",
        help="Do not fail if ONNX export names do not expose a protected head marker.",
    )
    args = parser.parse_args()

    import numpy as np
    import onnxruntime as ort
    import torch
    from onnxruntime.quantization import QuantType, quantize_dynamic

    started = time.perf_counter()
    runtime = MatrixNluRuntime(args.bundle)
    args.output_dir.mkdir(parents=True, exist_ok=True)
    fp32_path = args.output_dir / "matrix-nlu-fp32.onnx"
    mixed_path = args.output_dir / "matrix-nlu-mixed-head-protected-int8.onnx"

    class Wrapper(torch.nn.Module):
        def __init__(self, model):
            super().__init__()
            self.model = model

        def forward(self, input_ids, attention_mask):
            return flatten(self.model(input_ids, attention_mask))

    encoded = runtime.tokenizer(
        "mi chiamo Alberto",
        max_length=runtime.max_length,
        padding="max_length",
        truncation=True,
        return_tensors="pt",
    )
    wrapper = Wrapper(runtime.model).eval()
    torch.onnx.export(
        wrapper,
        (encoded["input_ids"], encoded["attention_mask"]),
        fp32_path,
        input_names=["input_ids", "attention_mask"],
        output_names=list(OUTPUT_NAMES),
        opset_version=17,
        do_constant_folding=True,
    )

    grouped = protected_nodes(fp32_path)
    missing = missing_markers(grouped)
    if missing and not args.allow_missing_protected_node_marker:
        raise RuntimeError(
            "ONNX export did not expose protected head markers: " + ", ".join(missing)
        )
    excluded = quantizer_exclusion_names(fp32_path, grouped)
    if not excluded:
        raise RuntimeError("No protected ONNX nodes detected; refusing unsafe mixed quantization")
    encoder_nodes = encoder_quantizable_nodes(fp32_path)
    if not encoder_nodes:
        raise RuntimeError("No encoder/backbone ONNX nodes detected; refusing empty quantization")

    quantize_dynamic(
        fp32_path,
        mixed_path,
        op_types_to_quantize=["MatMul", "Gemm"],
        per_channel=True,
        reduce_range=False,
        weight_type=QuantType.QInt8,
        nodes_to_quantize=encoder_nodes,
        nodes_to_exclude=excluded,
    )

    initializer_check = verify_protected_initializers_remain_float(
        fp32_path, mixed_path, grouped
    )
    if initializer_check["missingProtectedOutputs"] or initializer_check["violations"]:
        raise RuntimeError(
            "Protected head verification failed: "
            + json.dumps(initializer_check, indent=2)
        )

    sessions = {
        "fp32": ort.InferenceSession(str(fp32_path), providers=["CPUExecutionProvider"]),
        "mixedHeadProtectedInt8": ort.InferenceSession(
            str(mixed_path), providers=["CPUExecutionProvider"]
        ),
    }
    probes = (
        "non voglio uscire con Marco",
        "detesto le code lunghe",
        "Marco dice che Sara non mi crede",
        "no, non vivo a Roma, vivo a Padova",
        "puede que Marco no viva en Madrid",
        "I prefer that you do not touch me",
    )
    parity_results = {"fp32": [], "mixedHeadProtectedInt8": []}
    for text in probes:
        tokens = runtime.tokenizer(
            text,
            max_length=runtime.max_length,
            padding="max_length",
            truncation=True,
            return_tensors="pt",
        )
        with torch.no_grad():
            native = flatten(runtime.model(tokens["input_ids"], tokens["attention_mask"]))
        ort_inputs = {
            "input_ids": tokens["input_ids"].numpy().astype(np.int64),
            "attention_mask": tokens["attention_mask"].numpy().astype(np.int64),
        }
        for kind, session in sessions.items():
            parity_results[kind].append(
                {"text": text, "outputs": parity(native, session.run(list(OUTPUT_NAMES), ort_inputs))}
            )

    timing_inputs = {
        "input_ids": encoded["input_ids"].numpy().astype(np.int64),
        "attention_mask": encoded["attention_mask"].numpy().astype(np.int64),
    }
    files = {"fp32": fp32_path, "mixedHeadProtectedInt8": mixed_path}
    manifest = {
        "schemaVersion": "matrix.nlu.onnx-mixed-head-protected-export.v1",
        "variant": "student-4-v2.2a",
        "productionStatus": EXPERIMENTAL_STATUS,
        "decisionCarryOver": "STOPPED_FOR_REVIEW_FAILED_DEV_GATE",
        "frozen": {
            "frozenDataRead": False,
            "frozenEvaluationExecuted": False,
            "frozenPredictionsRead": False,
        },
        "quantization": {
            "mode": "dynamic-int8-encoder-with-matrix-heads-fp32",
            "weightType": "QInt8",
            "perChannel": True,
            "opTypesToQuantize": ["MatMul", "Gemm"],
            "protectedTokenHeads": list(PROTECTED_TOKEN_HEADS),
            "protectedSequenceHeads": list(PROTECTED_SEQUENCE_HEADS),
            "protectedOutputs": list(PROTECTED_OUTPUTS),
            "excludedOnnxNodes": excluded,
            "excludedNodeCount": len(excluded),
            "encoderNodesSelectedForQuantization": encoder_nodes,
            "encoderNodeCount": len(encoder_nodes),
            "missingProtectedMarkers": missing,
            "massiveAuxiliaryHeadsProtected": False,
        },
        "opset": 17,
        "fixedSequenceLength": runtime.max_length,
        "outputs": list(OUTPUT_NAMES),
        "source": {
            "trainingResultSha256": sha256(args.bundle / "training-result.json"),
            "modelStateSha256": sha256(args.bundle / "model-state.pt"),
            "labelsSha256": sha256(args.bundle / "labels.json"),
        },
        "files": {
            kind: {"path": path.name, "bytes": path.stat().st_size, "sha256": sha256(path)}
            for kind, path in files.items()
        },
        "protectedInitializerCheck": initializer_check,
        "operatorCounts": {
            "fp32": quantized_ops(fp32_path),
            "mixedHeadProtectedInt8": quantized_ops(mixed_path),
        },
        "parity": parity_results,
        "latency": {
            kind: latency(session, timing_inputs, args.repetitions)
            for kind, session in sessions.items()
        },
        "elapsedSeconds": time.perf_counter() - started,
    }
    (args.output_dir / "onnx-mixed-head-protected-manifest.json").write_text(
        json.dumps(manifest, indent=2) + "\n"
    )
    (args.output_dir / "FROZEN_GUARD.txt").write_text(
        "variant=student-4-v2.2a\n"
        "productionStatus=EXPERIMENTAL_TEST_CANDIDATE_NOT_PRODUCTION_APPROVED\n"
        "decisionCarryOver=STOPPED_FOR_REVIEW_FAILED_DEV_GATE\n"
        "frozenDataRead=false\n"
        "frozenEvaluationExecuted=false\n"
        "frozenPredictionsRead=false\n"
        "quantizationExecuted=mixed_head_protected_experimental\n"
        "onnxExported=true\n"
    )
    print(json.dumps(manifest, indent=2))


if __name__ == "__main__":
    main()
