#!/usr/bin/env python3
"""Evaluate Student-4-v2.2A on development only and stop before frozen access."""

from __future__ import annotations

import argparse
import json
import pathlib
import subprocess
import sys
import time

from matrix_nlu.pipeline_support import Step, atomic_json, run_step, sha256

ROOT = pathlib.Path(__file__).resolve().parent.parent
VARIANT = "student-4-v2.2a"
REQUIRED_BUNDLE_FILES = ("training-result.json", "model-state.pt", "labels.json")


def validate_bundle(bundle: pathlib.Path) -> tuple[dict, str]:
    missing = [name for name in REQUIRED_BUNDLE_FILES if not (bundle / name).is_file()]
    if missing:
        raise SystemExit("incomplete Student-4-v2.2A bundle: " + ", ".join(missing))
    result = json.loads((bundle / "training-result.json").read_text(encoding="utf-8"))
    config = result.get("config", {})
    if config.get("model", {}).get("variant") != VARIANT:
        raise SystemExit(f"refusing non-{VARIANT} bundle")
    if config.get("studentLayers") != 4 or result.get("studentLayers") != 4:
        raise SystemExit("refusing bundle without studentLayers == 4 provenance")
    if result.get("frozenDataRead") is not False or result.get("trainingSplitsRead") != ["train", "dev"]:
        raise SystemExit("training provenance does not prove train/dev-only access")
    if result.get("frozenEvaluationDeferred") is not True:
        raise SystemExit("training result does not explicitly defer frozen evaluation")
    expected = result.get("modelStateSha256")
    actual = sha256(bundle / "model-state.pt")
    if expected != actual:
        raise SystemExit(f"model checksum mismatch: expected={expected} actual={actual}")
    return result, actual


def combine(sources: list[pathlib.Path], destination: pathlib.Path) -> None:
    destination.parent.mkdir(parents=True, exist_ok=True)
    with destination.open("w", encoding="utf-8") as output:
        for source in sources:
            with source.open(encoding="utf-8") as handle:
                for line in handle:
                    if line.strip():
                        output.write(line)


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--bundle", type=pathlib.Path, required=True)
    parser.add_argument("--data-dir", type=pathlib.Path, required=True)
    parser.add_argument("--output-dir", type=pathlib.Path, required=True)
    args = parser.parse_args()
    bundle, data, output = (path.resolve() for path in (args.bundle, args.data_dir, args.output_dir))
    output.mkdir(parents=True, exist_ok=True)
    logs = output / "logs"
    result, actual = validate_bundle(bundle)

    timings = {}
    for name in ("matrix", "p05"):
        dataset = data / f"{name}-v2-dev.jsonl"
        step = Step(f"predict-{name}-dev", [sys.executable, "matrix_nlu/evaluate_e2e.py",
            "--bundle", str(bundle), "--dataset", str(dataset), "--split", "dev",
            "--threshold", "0", "--output-dir", str(output / f"{name}-dev")])
        timings[step.name] = run_step(step, ROOT, logs)

    errors = output / "dev-combined-errors.jsonl"
    combine([output / "matrix-dev" / "e2e-dev-errors.jsonl",
             output / "p05-dev" / "e2e-dev-errors.jsonl"], errors)
    step = Step("classify-development-residuals", [sys.executable,
        "matrix_nlu/analyze_errors.py", "--errors", str(errors), "--output",
        str(output / "dev-error-analysis.json")])
    timings[step.name] = run_step(step, ROOT, logs)

    threshold_path = output / "threshold-selection.json"
    command = [sys.executable, "matrix_nlu/select_threshold.py",
        "--dataset", str(data / "matrix-v2-dev.jsonl"), "--predictions",
        str(output / "matrix-dev" / "e2e-dev-predictions.jsonl"),
        "--dataset", str(data / "p05-v2-dev.jsonl"), "--predictions",
        str(output / "p05-dev" / "e2e-dev-predictions.jsonl"),
        "--output", str(threshold_path)]
    started = time.monotonic()
    completed = subprocess.run(command, cwd=ROOT, text=True, capture_output=True, check=False)
    timings["select-threshold-from-development-only"] = time.monotonic() - started
    (logs / "select-threshold-from-development-only.log").parent.mkdir(parents=True, exist_ok=True)
    (logs / "select-threshold-from-development-only.log").write_text(
        completed.stdout + completed.stderr, encoding="utf-8")
    if completed.returncode not in (0, 2) or not threshold_path.is_file():
        raise SystemExit(f"threshold process failed unexpectedly: exit={completed.returncode}")

    selection = json.loads(threshold_path.read_text(encoding="utf-8"))
    passed = selection.get("status") == "PASS" and selection.get("selectedThreshold") is not None
    decision = ("DEV_GATE_PASSED_AWAITING_FROZEN_AUTHORIZATION" if passed
                else "STOPPED_FOR_REVIEW")
    summary = {
        "schemaVersion": "matrix.nlu.student-4-v2.2a-controlled-stop.v1",
        "decision": decision,
        "datasetVersion": "matrix.nlu.dataset.v2",
        "variant": VARIANT,
        "baseline": "student-4-v2.1 STOPPED_FOR_REVIEW",
        "studentLayers": 4,
        "trainingSplitsRead": ["train", "dev"],
        "frozenDataRead": False,
        "frozenEvaluationExecuted": False,
        "onnxExported": False,
        "quantizationExecuted": False,
        "modelStateSha256": actual,
        "trainingResultSha256": sha256(bundle / "training-result.json"),
        "labelsSha256": sha256(bundle / "labels.json"),
        "thresholdProcessExitCode": completed.returncode,
        "selectionStatus": selection.get("status"),
        "selectedThreshold": selection.get("selectedThreshold"),
        "targetedRepair": result.get("config", {}).get("repairPolicy"),
        "timings": timings,
    }
    atomic_json(output / "controlled-stop-summary.json", summary)
    print(json.dumps(summary, indent=2, ensure_ascii=False))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
