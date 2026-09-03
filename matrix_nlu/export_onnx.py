#!/usr/bin/env python3
"""Export the trained Matrix-NLU teacher/student to offline ONNX and INT8."""

from __future__ import annotations

import argparse
import hashlib
import json
import math
import pathlib
import statistics
import time

from inference import MatrixNluRuntime
from labels import SEQUENCE_LABELS, TOKEN_LABELS


TOKEN_HEADS = tuple(TOKEN_LABELS)
SEQUENCE_HEADS = tuple(SEQUENCE_LABELS)
OUTPUT_NAMES = tuple([f"token.{name}" for name in TOKEN_HEADS] +
                     [f"sequence.{name}" for name in SEQUENCE_HEADS] +
                     ["massive.intent", "massive.slot"])


def sha256(path):
    return hashlib.sha256(path.read_bytes()).hexdigest()


def percentile(values, fraction):
    ordered = sorted(values)
    return ordered[min(len(ordered) - 1, max(0, math.ceil(len(ordered) * fraction) - 1))]


def flatten(output):
    return tuple([output["tokens"][name] for name in TOKEN_HEADS] +
                 [output["sequence"][name] for name in SEQUENCE_HEADS] +
                 [output["massive_intent"], output["massive_slot"]])


def parity(native, observed):
    import numpy as np
    entries = []
    for name, expected, actual in zip(OUTPUT_NAMES, native, observed):
        expected = expected.detach().cpu().numpy()
        difference = np.abs(expected - actual)
        entries.append({"output": name, "maxAbsLogitDelta": float(difference.max()),
                        "argmaxExact": bool(np.array_equal(expected.argmax(-1),
                                                             actual.argmax(-1)))})
    return entries


def latency(session, inputs, repetitions):
    for _ in range(3):
        session.run(list(OUTPUT_NAMES), inputs)
    values = []
    for _ in range(repetitions):
        started = time.perf_counter()
        session.run(list(OUTPUT_NAMES), inputs)
        values.append((time.perf_counter() - started) * 1000)
    return {"repetitions": repetitions, "medianMs": statistics.median(values),
            "p95Ms": percentile(values, 0.95), "maxMs": max(values)}


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--bundle", type=pathlib.Path, required=True)
    parser.add_argument("--output-dir", type=pathlib.Path, required=True)
    parser.add_argument("--repetitions", type=int, default=30)
    args = parser.parse_args()
    import numpy as np
    import onnxruntime as ort
    import torch
    from onnxruntime.quantization import QuantType, quantize_dynamic

    runtime = MatrixNluRuntime(args.bundle)
    args.output_dir.mkdir(parents=True, exist_ok=True)
    fp32_path = args.output_dir / "matrix-nlu-fp32.onnx"
    int8_path = args.output_dir / "matrix-nlu-int8.onnx"

    class Wrapper(torch.nn.Module):
        def __init__(self, model):
            super().__init__()
            self.model = model

        def forward(self, input_ids, attention_mask):
            return flatten(self.model(input_ids, attention_mask))

    encoded = runtime.tokenizer("mi chiamo Alberto", max_length=runtime.max_length, padding="max_length",
                                truncation=True, return_tensors="pt")
    wrapper = Wrapper(runtime.model).eval()
    torch.onnx.export(wrapper, (encoded["input_ids"], encoded["attention_mask"]), fp32_path,
                      input_names=["input_ids", "attention_mask"],
                      output_names=list(OUTPUT_NAMES), opset_version=17,
                      do_constant_folding=True)
    quantize_dynamic(fp32_path, int8_path, per_channel=True, reduce_range=False,
                     weight_type=QuantType.QInt8)

    sessions = {"fp32": ort.InferenceSession(str(fp32_path), providers=["CPUExecutionProvider"]),
                "int8": ort.InferenceSession(str(int8_path), providers=["CPUExecutionProvider"])}
    probes = ("mi chiamo Alberto e vivo a San Vendemiano",
              "my name is Albert and I live in New York",
              "me llamo Alberto y vivo en San Sebastián")
    parity_results = {"fp32": [], "int8": []}
    for text in probes:
        tokens = runtime.tokenizer(text, max_length=runtime.max_length, padding="max_length", truncation=True,
                                   return_tensors="pt")
        with torch.no_grad():
            native = flatten(runtime.model(tokens["input_ids"], tokens["attention_mask"]))
        ort_inputs = {"input_ids": tokens["input_ids"].numpy().astype(np.int64),
                      "attention_mask": tokens["attention_mask"].numpy().astype(np.int64)}
        for kind, session in sessions.items():
            parity_results[kind].append({"text": text,
                "outputs": parity(native, session.run(list(OUTPUT_NAMES), ort_inputs))})

    timing_inputs = {"input_ids": encoded["input_ids"].numpy().astype(np.int64),
                     "attention_mask": encoded["attention_mask"].numpy().astype(np.int64)}
    files = {"fp32": fp32_path, "int8": int8_path}
    manifest = {"schemaVersion": "matrix.nlu.onnx-export.v1", "opset": 17,
                "fixedSequenceLength": runtime.max_length, "outputs": list(OUTPUT_NAMES),
                "source": {"trainingResultSha256": sha256(args.bundle / "training-result.json"),
                           "modelStateSha256": sha256(args.bundle / "model-state.pt"),
                           "labelsSha256": sha256(args.bundle / "labels.json")},
                "files": {kind: {"path": path.name, "bytes": path.stat().st_size,
                                  "sha256": sha256(path)} for kind, path in files.items()},
                "parity": parity_results,
                "latency": {kind: latency(session, timing_inputs, args.repetitions)
                            for kind, session in sessions.items()}}
    (args.output_dir / "onnx-manifest.json").write_text(json.dumps(manifest, indent=2) + "\n")
    print(json.dumps(manifest, indent=2))


if __name__ == "__main__":
    main()
