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
DATA_V2_DIR = BUILD / "data-v2"
MASSIVE_DIR = BUILD / "massive"
DEFAULT_TRAINING_DIR = BUILD / "training"
AUTOMATION_DIR = BUILD / "automation"
DEFAULT_LAST_GOOD_DIR = BUILD / "last-good-training"


def validate_training_artifact(training_dir: pathlib.Path, require_frozen: bool = True) -> dict:
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
    if require_frozen:
        for key in ("matrixTest", "p05Test", "massiveTest"):
            if key not in frozen:
                raise RuntimeError(f"training result is missing frozen evaluation '{key}'")
    elif frozen.get("status") != "DEFERRED_UNTIL_DEV_THRESHOLD_GATE":
        raise RuntimeError("v2 training must defer frozen evaluation until the dev gate")
    if not require_frozen and (result.get("frozenDataRead") is not False or
                               result.get("trainingSplitsRead") != ["train", "dev"]):
        raise RuntimeError("v2 training provenance does not prove train/dev-only access")

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
    is_v2 = getattr(args, "dataset_version", "v1") == "v2"
    data_dir = DATA_V2_DIR if is_v2 else DATA_DIR
    config = "matrix_nlu/train_config_v2.json" if is_v2 else "matrix_nlu/train_config.json"
    steps = [
        Step(
            "Software regression tests",
            [python, "-m", "unittest", "discover", "-s", "matrix_nlu", "-p", "test_*.py", "-v"],
        ),
        Step("Build Matrix datasets", [python, "matrix_nlu/build_dataset_v2.py"] if is_v2
             else [python, "matrix_nlu/build_dataset.py"]),
    ]
    if is_v2:
        steps.append(Step(
            "Audit complete v2 dataset before training",
            [python, "matrix_nlu/audit_dataset_v2.py", "--data-dir",
             str(data_dir.relative_to(ROOT)), "--output",
             str((AUTOMATION_DIR / "dataset-v2-audit.json").relative_to(ROOT)),
             "--fail-on-error"],
        ))
    else:
        steps.append(Step(
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
        ))
    steps.extend([
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
                config,
                "--data-dir",
                str(data_dir.relative_to(ROOT)),
                "--massive-dir",
                str(MASSIVE_DIR.relative_to(ROOT)),
                "--output-dir",
                str(training_dir.relative_to(ROOT)),
            ],
        ),
    ])
    if args.student_layers is not None:
        steps[-1].command.extend(["--student-layers", str(args.student_layers)])
    if is_v2:
        steps[-1].command.append("--defer-frozen")
        resume_evidence = getattr(args, "resume_evidence", None)
        if resume_evidence is not None:
            steps[-1].command.extend(["--resume-evidence", str(resume_evidence)])
    return steps


def main() -> int:
    parser = argparse.ArgumentParser(description="Automatic Matrix-NLU training pipeline")
    parser.add_argument("--seed", type=int, default=810923)
    parser.add_argument("--massive-train-per-language", type=int, default=3000)
    parser.add_argument("--massive-dev-per-language", type=int, default=600)
    parser.add_argument("--massive-test-per-language", type=int, default=1000)
    parser.add_argument("--student-layers", type=int)
    parser.add_argument("--dataset-version", choices=("v1", "v2"), default="v1")
    parser.add_argument("--variant", help="explicit isolated variant name")
    parser.add_argument("--resume-evidence", type=pathlib.Path,
                        help="verified provenance for an explicitly restored v2 checkpoint")
    parser.add_argument("--output-dir", type=pathlib.Path,
                        help="variant-specific output; default is training or training-student-N")
    args = parser.parse_args()

    config_path = ROOT / "matrix_nlu" / ("train_config_v2.json" if args.dataset_version == "v2"
                                         else "train_config.json")
    configured_seed = json.loads(config_path.read_text())["seed"]
    if args.seed != configured_seed:
        parser.error(f"--seed {args.seed} differs from immutable train_config seed {configured_seed}")

    variant = (args.variant or ("teacher-6-layer" if args.student_layers is None
                                else f"student-{args.student_layers}-layer"))
    if args.dataset_version == "v2" and variant != "student-4-v2":
        parser.error("dataset v2 is authorized only for the fresh student-4-v2 variant")
    if args.dataset_version == "v2" and args.student_layers != 4:
        parser.error("student-4-v2 requires --student-layers 4")
    if args.resume_evidence is not None and args.dataset_version != "v2":
        parser.error("--resume-evidence is valid only for dataset v2")
    training_dir = (args.output_dir or
                    (BUILD / "training-student-4-v2" if args.dataset_version == "v2" else
                    (BUILD / f"training-student-{args.student_layers}"
                     if args.student_layers is not None else DEFAULT_TRAINING_DIR))).resolve()
    try:
        training_dir.relative_to(ROOT)
    except ValueError:
        parser.error("--output-dir must be inside the repository for auditable manifests")
    last_good_dir = (BUILD / "last-good-training-student-4-v2"
                     if args.dataset_version == "v2" else
                     BUILD / f"last-good-training-student-{args.student_layers}"
                     if args.student_layers is not None else DEFAULT_LAST_GOOD_DIR)
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
        "datasetVersion": args.dataset_version,
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

        metadata = validate_training_artifact(training_dir, require_frozen=args.dataset_version != "v2")
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
