#!/usr/bin/env python3
"""Robust one-command, resumable and failure-safe Matrix-NLU training orchestrator."""

from __future__ import annotations

import argparse
import json
import pathlib
import shutil
import sys
import time

from matrix_nlu.pipeline_support import Step, atomic_json, run_step as run_pipeline_step, sha256

ROOT = pathlib.Path(__file__).resolve().parent
BUILD = ROOT / "build" / "matrix-nlu"
DATA_DIR = BUILD / "data"
MASSIVE_DIR = BUILD / "massive"
DEFAULT_TRAINING_DIR = BUILD / "training"
AUTOMATION_DIR = BUILD / "automation"
DEFAULT_LAST_GOOD_DIR = BUILD / "last-good-training"


def validate_training_artifact(training_dir: pathlib.Path) -> dict:
    result_path = training_dir / "training-result.json"
    model_path = training_dir / "model-state.pt"
    labels_path = training_dir / "labels.json"
    tokenizer_dir = training_dir / "tokenizer"
    required = (result_path, model_path, labels_path, tokenizer_dir)
    missing = [str(path.relative_to(ROOT)) for path in required if not path.exists()]
    if missing:
        raise RuntimeError("missing required training artifacts: " + ", ".join(missing))

    result = json.loads(result_path.read_text(encoding="utf-8"))
    actual_model_hash = sha256(model_path)
    expected_model_hash = result.get("modelStateSha256")
    if expected_model_hash != actual_model_hash:
        raise RuntimeError(
            "model checksum mismatch: "
            f"expected={expected_model_hash} actual={actual_model_hash}"
        )

    frozen = result.get("frozen")
    if not isinstance(frozen, dict):
        raise RuntimeError("training-result.json is missing frozen evaluation results")
    for key in ("matrixTest", "p05Test", "massiveTest"):
        if key not in frozen:
            raise RuntimeError(f"training result is missing frozen evaluation '{key}'")

    return {
        "trainingResult": str(result_path.relative_to(ROOT)),
        "modelState": str(model_path.relative_to(ROOT)),
        "modelStateSha256": actual_model_hash,
        "bestDevScore": result.get("bestDevScore"),
        "parameters": result.get("parameters"),
        "frozen": frozen,
    }


def promote_last_good(training_dir: pathlib.Path, destination: pathlib.Path, metadata: dict) -> None:
    staging = BUILD / f".{destination.name}-staging"
    if staging.exists():
        shutil.rmtree(staging)
    staging.mkdir(parents=True, exist_ok=True)

    for name in ("training-result.json", "model-state.pt", "labels.json"):
        shutil.copy2(training_dir / name, staging / name)
    shutil.copytree(training_dir / "tokenizer", staging / "tokenizer")

    old = BUILD / f".{destination.name}-old"
    if old.exists():
        shutil.rmtree(old)
    if destination.exists():
        destination.replace(old)
    staging.replace(destination)
    if old.exists():
        shutil.rmtree(old)

    atomic_json(
        AUTOMATION_DIR / f"{destination.name}.json",
        {
            "schemaVersion": "matrix.nlu.last-good.v1",
            "promotedAtEpochSeconds": time.time(),
            **metadata,
        },
    )


def build_steps(args: argparse.Namespace, training_dir: pathlib.Path) -> list[Step]:
    python = sys.executable
    steps = [
        Step(
            "Software regression tests",
            [python, "-m", "unittest", "discover", "-s", "matrix_nlu", "-p", "test_*.py", "-v"],
        ),
        Step("Build Matrix datasets", [python, "matrix_nlu/build_dataset.py"]),
        Step(
            "Audit train-dev annotation contracts",
            [
                python,
                "matrix_nlu/audit_dataset_contract.py",
                "--dataset", f"matrix-train={DATA_DIR.relative_to(ROOT) / 'matrix-train.jsonl'}",
                "--dataset", f"matrix-dev={DATA_DIR.relative_to(ROOT) / 'matrix-dev.jsonl'}",
                "--dataset", f"p05-train={DATA_DIR.relative_to(ROOT) / 'p05-train.jsonl'}",
                "--dataset", f"p05-dev={DATA_DIR.relative_to(ROOT) / 'p05-dev.jsonl'}",
                "--output", str((AUTOMATION_DIR / "dataset-contract-audit.json").relative_to(ROOT)),
                "--fail-on-conflict",
            ],
        ),
        Step(
            "Prepare verified MASSIVE auxiliary data",
            [
                python,
                "matrix_nlu/prepare_massive.py",
                "--train-per-language",
                str(args.massive_train_per_language),
                "--dev-per-language",
                str(args.massive_dev_per_language),
                "--test-per-language",
                str(args.massive_test_per_language),
                "--seed",
                str(args.seed),
            ],
        ),
        Step(
            "Train/resume Matrix-NLU",
            [
                python,
                "matrix_nlu/train.py",
                "--config",
                "matrix_nlu/train_config.json",
                "--data-dir",
                str(DATA_DIR.relative_to(ROOT)),
                "--massive-dir",
                str(MASSIVE_DIR.relative_to(ROOT)),
                "--output-dir",
                str(training_dir.relative_to(ROOT)),
            ],
        ),
    ]
    if args.student_layers is not None:
        steps[-1].command.extend(["--student-layers", str(args.student_layers)])
    return steps


def main() -> int:
    parser = argparse.ArgumentParser(description="Automatic Matrix-NLU training pipeline")
    parser.add_argument("--seed", type=int, default=810923)
    parser.add_argument("--massive-train-per-language", type=int, default=3000)
    parser.add_argument("--massive-dev-per-language", type=int, default=600)
    parser.add_argument("--massive-test-per-language", type=int, default=1000)
    parser.add_argument("--student-layers", type=int)
    parser.add_argument("--output-dir", type=pathlib.Path,
                        help="variant-specific output; default is training or training-student-N")
    args = parser.parse_args()

    configured_seed = json.loads((ROOT / "matrix_nlu/train_config.json").read_text())["seed"]
    if args.seed != configured_seed:
        parser.error(f"--seed {args.seed} differs from immutable train_config seed {configured_seed}")

    training_dir = (args.output_dir or
                    (BUILD / f"training-student-{args.student_layers}"
                     if args.student_layers is not None else DEFAULT_TRAINING_DIR)).resolve()
    try:
        training_dir.relative_to(ROOT)
    except ValueError:
        parser.error("--output-dir must be inside the repository for auditable manifests")
    last_good_dir = (BUILD / f"last-good-training-student-{args.student_layers}"
                     if args.student_layers is not None else DEFAULT_LAST_GOOD_DIR)
    variant = "teacher-6-layer" if args.student_layers is None else f"student-{args.student_layers}-layer"
    status_file = AUTOMATION_DIR / f"auto-train-{variant}-status.json"
    log_dir = AUTOMATION_DIR / "logs" / variant

    AUTOMATION_DIR.mkdir(parents=True, exist_ok=True)
    started_wall = time.time()
    started_mono = time.monotonic()
    timings: dict[str, float] = {}
    base_state = {
        "schemaVersion": "matrix.nlu.auto-train-status.v1",
        "startedAtEpochSeconds": started_wall,
        "command": sys.argv,
        "trainingDir": str(training_dir.relative_to(ROOT)),
        "variant": variant,
    }

    atomic_json(
        status_file,
        {
            **base_state,
            "status": "RUNNING",
        },
    )

    try:
        steps = build_steps(args, training_dir)
        for index, step in enumerate(steps, 1):
            print(f"[AUTO-TRAIN] step {index}/{len(steps)}")
            timings[step.name] = run_pipeline_step(step, ROOT, log_dir)

        metadata = validate_training_artifact(training_dir)
        promote_last_good(training_dir, last_good_dir, metadata)
        elapsed = time.monotonic() - started_mono
        final = {
            **base_state,
            "status": "SUCCESS",
            "finishedAtEpochSeconds": time.time(),
            "seconds": elapsed,
            "timings": timings,
            **metadata,
        }
        atomic_json(status_file, final)
        print("\n[AUTO-TRAIN] SUCCESS")
        print(json.dumps(final, indent=2, ensure_ascii=False))
        return 0
    except KeyboardInterrupt:
        failure = {
            **base_state,
            "status": "INTERRUPTED",
            "finishedAtEpochSeconds": time.time(),
            "seconds": time.monotonic() - started_mono,
            "timings": timings,
            "error": "KeyboardInterrupt",
            "lastGoodPreserved": last_good_dir.exists(),
            "resumeCheckpointPreserved": (training_dir / "checkpoints" / "latest.pt").exists(),
        }
        atomic_json(status_file, failure)
        print("\n[AUTO-TRAIN] INTERRUPTED: resumable checkpoint and last-good artifacts preserved.")
        return 130
    except Exception as exc:
        failure = {
            **base_state,
            "status": "FAILED",
            "finishedAtEpochSeconds": time.time(),
            "seconds": time.monotonic() - started_mono,
            "timings": timings,
            "errorType": type(exc).__name__,
            "error": str(exc),
            "lastGoodPreserved": last_good_dir.exists(),
            "resumeCheckpointPreserved": (training_dir / "checkpoints" / "latest.pt").exists(),
        }
        atomic_json(status_file, failure)
        print(f"\n[AUTO-TRAIN] FAILED: {type(exc).__name__}: {exc}", file=sys.stderr)
        print("Previous last-good artifacts were not overwritten.", file=sys.stderr)
        return 1


if __name__ == "__main__":
    raise SystemExit(main())
