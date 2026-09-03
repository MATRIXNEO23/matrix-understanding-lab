#!/usr/bin/env python3
"""Strict one-click prepare/train/resume/validate/frozen/package pipeline."""

from __future__ import annotations

import argparse
import json
import pathlib
import sys
import time

from matrix_nlu.pipeline_support import Step, atomic_json, run_step


ROOT = pathlib.Path(__file__).resolve().parent
BUILD = ROOT / "build" / "matrix-nlu"
STATUS = BUILD / "automation" / "pipeline-status.json"


def commands(args: argparse.Namespace) -> list[Step]:
    steps = []
    bundle = args.bundle or (BUILD / f"training-student-{args.student_layers}"
                             if args.student_layers is not None else BUILD / "training")
    if not args.skip_train:
        training = [sys.executable, "auto_train.py", "--seed", str(args.seed)]
        if args.student_layers is not None:
            training.extend(["--student-layers", str(args.student_layers)])
        steps.append(Step("prepare-verify-train-or-resume", training))
    testing = [sys.executable, "auto_test.py", "--bundle", str(bundle),
               "--onnx-repetitions", str(args.onnx_repetitions), "--candidate-role",
               "production" if args.student_layers is not None or getattr(args, "candidate_role", "teacher") == "production"
               else "teacher"]
    if not args.skip_train:
        testing.extend(["--skip-software-tests", "--skip-data-build"])
    steps.append(Step("validate-frozen-adversarial-package", testing))
    return steps


def main() -> int:
    parser = argparse.ArgumentParser(description="Matrix-NLU strict one-click pipeline")
    parser.add_argument("--skip-train", action="store_true",
                        help="validate an already completed immutable training bundle")
    parser.add_argument("--bundle", type=pathlib.Path,
                        help="bundle to validate; defaults to build/matrix-nlu/training")
    parser.add_argument("--student-layers", type=int)
    parser.add_argument("--seed", type=int, default=810923)
    parser.add_argument("--onnx-repetitions", type=int, default=30)
    parser.add_argument("--candidate-role", choices=("teacher", "production"), default="teacher",
                        help="teacher preserves evidence; production enforces deployable size")
    parser.add_argument("--dry-run", action="store_true")
    args = parser.parse_args()
    if args.bundle is not None and not args.skip_train:
        parser.error("--bundle requires --skip-train; training owns its output bundle")
    planned = commands(args)
    if args.dry_run:
        print(json.dumps({"steps": [{"name": step.name, "command": step.command}
                                     for step in planned]}, indent=2))
        return 0
    started = time.time()
    state = {"schemaVersion": "matrix.nlu.pipeline-status.v1", "status": "RUNNING",
             "startedAtEpochSeconds": started, "currentStage": None,
             "steps": [step.name for step in planned], "timings": {}}
    atomic_json(STATUS, state)
    try:
        for step in planned:
            state["currentStage"] = step.name
            atomic_json(STATUS, state)
            state["timings"][step.name] = run_step(step, ROOT, BUILD / "automation" / "logs")
        state.update({"status": "SUCCESS", "currentStage": "complete",
                      "finishedAtEpochSeconds": time.time(), "seconds": time.time() - started,
                      "verifiedPackage": str(BUILD / "last-good-package")})
        atomic_json(STATUS, state)
        print(json.dumps(state, indent=2))
        return 0
    except KeyboardInterrupt:
        state.update({"status": "INTERRUPTED", "finishedAtEpochSeconds": time.time(),
                      "resumeCheckpointPreserved": (BUILD / "training/checkpoints/latest.pt").exists(),
                      "lastGoodPackagePreserved": (BUILD / "last-good-package").exists()})
        atomic_json(STATUS, state)
        return 130
    except Exception as error:
        state.update({"status": "FAILED", "finishedAtEpochSeconds": time.time(),
                      "errorType": type(error).__name__, "error": str(error),
                      "resumeCheckpointPreserved": (BUILD / "training/checkpoints/latest.pt").exists(),
                      "lastGoodPackagePreserved": (BUILD / "last-good-package").exists()})
        atomic_json(STATUS, state)
        print(f"[PIPELINE] FAILED: {type(error).__name__}: {error}", file=sys.stderr)
        return 1


if __name__ == "__main__":
    raise SystemExit(main())
