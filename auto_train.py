#!/usr/bin/env python3
"""Robust one-command, resumable and failure-safe Matrix-NLU training orchestrator."""

from __future__ import annotations

import argparse
import hashlib
import json
import os
import pathlib
import shutil
import subprocess
import sys
import tempfile
import time
from dataclasses import dataclass

from tqdm import tqdm

ROOT = pathlib.Path(__file__).resolve().parent
BUILD = ROOT / "build" / "matrix-nlu"
DATA_DIR = BUILD / "data"
MASSIVE_DIR = BUILD / "massive"
DEFAULT_TRAINING_DIR = BUILD / "training"
AUTOMATION_DIR = BUILD / "automation"
STATUS_FILE = AUTOMATION_DIR / "auto-train-status.json"
DEFAULT_LAST_GOOD_DIR = BUILD / "last-good-training"


@dataclass(frozen=True)
class Step:
    name: str
    command: list[str]


def atomic_json(path: pathlib.Path, payload: dict) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    fd, tmp_name = tempfile.mkstemp(prefix=f".{path.name}.", suffix=".tmp", dir=path.parent)
    try:
        with os.fdopen(fd, "w", encoding="utf-8") as handle:
            json.dump(payload, handle, indent=2, ensure_ascii=False)
            handle.write("\n")
            handle.flush()
            os.fsync(handle.fileno())
        os.replace(tmp_name, path)
    except Exception:
        try:
            os.unlink(tmp_name)
        except FileNotFoundError:
            pass
        raise


def sha256(path: pathlib.Path) -> str:
    digest = hashlib.sha256()
    with path.open("rb") as handle:
        for chunk in iter(lambda: handle.read(1024 * 1024), b""):
            digest.update(chunk)
    return digest.hexdigest()


def run_step(step: Step) -> float:
    started = time.monotonic()
    print(f"\n[AUTO-TRAIN] {step.name}")
    print("$ " + " ".join(step.command))
    process = subprocess.Popen(
        step.command,
        cwd=ROOT,
        stdout=subprocess.PIPE,
        stderr=subprocess.STDOUT,
        text=True,
        encoding="utf-8",
        errors="replace",
        bufsize=1,
    )
    assert process.stdout is not None
    with tqdm(desc=step.name, unit="line", dynamic_ncols=True) as progress:
        for line in process.stdout:
            print(line, end="")
            progress.update(1)
    return_code = process.wait()
    elapsed = time.monotonic() - started
    if return_code != 0:
        raise RuntimeError(f"step '{step.name}' failed with exit code {return_code}")
    return elapsed


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

    training_dir = (args.output_dir or
                    (BUILD / f"training-student-{args.student_layers}"
                     if args.student_layers is not None else DEFAULT_TRAINING_DIR)).resolve()
    try:
        training_dir.relative_to(ROOT)
    except ValueError:
        parser.error("--output-dir must be inside the repository for auditable manifests")
    last_good_dir = (BUILD / f"last-good-training-student-{args.student_layers}"
                     if args.student_layers is not None else DEFAULT_LAST_GOOD_DIR)

    AUTOMATION_DIR.mkdir(parents=True, exist_ok=True)
    started_wall = time.time()
    started_mono = time.monotonic()
    timings: dict[str, float] = {}

    atomic_json(
        STATUS_FILE,
        {
            "schemaVersion": "matrix.nlu.auto-train-status.v1",
            "status": "RUNNING",
            "startedAtEpochSeconds": started_wall,
            "command": sys.argv,
            "trainingDir": str(training_dir.relative_to(ROOT)),
            "variant": "teacher-6-layer" if args.student_layers is None else f"student-{args.student_layers}-layer",
        },
    )

    try:
        steps = build_steps(args, training_dir)
        with tqdm(total=len(steps), desc="Matrix-NLU pipeline", unit="step", dynamic_ncols=True) as overall:
            for step in steps:
                timings[step.name] = run_step(step)
                overall.update(1)

        metadata = validate_training_artifact(training_dir)
        promote_last_good(training_dir, last_good_dir, metadata)
        elapsed = time.monotonic() - started_mono
        final = {
            "schemaVersion": "matrix.nlu.auto-train-status.v1",
            "status": "SUCCESS",
            "startedAtEpochSeconds": started_wall,
            "finishedAtEpochSeconds": time.time(),
            "seconds": elapsed,
            "timings": timings,
            **metadata,
        }
        atomic_json(STATUS_FILE, final)
        print("\n[AUTO-TRAIN] SUCCESS")
        print(json.dumps(final, indent=2, ensure_ascii=False))
        return 0
    except KeyboardInterrupt:
        failure = {
            "schemaVersion": "matrix.nlu.auto-train-status.v1",
            "status": "INTERRUPTED",
            "startedAtEpochSeconds": started_wall,
            "finishedAtEpochSeconds": time.time(),
            "seconds": time.monotonic() - started_mono,
            "timings": timings,
            "error": "KeyboardInterrupt",
            "lastGoodPreserved": last_good_dir.exists(),
            "resumeCheckpointPreserved": (training_dir / "checkpoints" / "latest.pt").exists(),
        }
        atomic_json(STATUS_FILE, failure)
        print("\n[AUTO-TRAIN] INTERRUPTED: resumable checkpoint and last-good artifacts preserved.")
        return 130
    except Exception as exc:
        failure = {
            "schemaVersion": "matrix.nlu.auto-train-status.v1",
            "status": "FAILED",
            "startedAtEpochSeconds": started_wall,
            "finishedAtEpochSeconds": time.time(),
            "seconds": time.monotonic() - started_mono,
            "timings": timings,
            "errorType": type(exc).__name__,
            "error": str(exc),
            "lastGoodPreserved": last_good_dir.exists(),
            "resumeCheckpointPreserved": (training_dir / "checkpoints" / "latest.pt").exists(),
        }
        atomic_json(STATUS_FILE, failure)
        print(f"\n[AUTO-TRAIN] FAILED: {type(exc).__name__}: {exc}", file=sys.stderr)
        print("Previous last-good artifacts were not overwritten.", file=sys.stderr)
        return 1


if __name__ == "__main__":
    raise SystemExit(main())
