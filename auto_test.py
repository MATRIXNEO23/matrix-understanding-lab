#!/usr/bin/env python3
"""One-command Matrix-NLU validation, frozen benchmark, export and packaging."""

from __future__ import annotations

import argparse
import json
import pathlib
import shutil
import sys
import time

from matrix_nlu.pipeline_support import Step, atomic_json, atomic_promote, file_manifest, run_step, sha256


ROOT = pathlib.Path(__file__).resolve().parent
BUILD = ROOT / "build" / "matrix-nlu"
DATA = BUILD / "data"
DATA_V2 = BUILD / "data-v2"
DEFAULT_BUNDLE = BUILD / "training"
STATUS = BUILD / "automation" / "auto-test-status.json"
LAST_GOOD_PACKAGE = BUILD / "last-good-package"

MINIMUMS = {
    "claimCountExact": 0.99,
    "exactClaimSet": 0.98,
    "fieldExact": 0.99,
    "validSelectiveAccuracy": 0.99,
    "validCoverage": 0.98,
}


def verify_training_inputs(bundle: pathlib.Path) -> dict:
    result_path = bundle / "training-result.json"
    result = json.loads(result_path.read_text(encoding="utf-8"))
    expected_model = result.get("modelStateSha256")
    actual_model = sha256(bundle / "model-state.pt")
    if expected_model != actual_model:
        raise RuntimeError(f"model checksum mismatch: expected={expected_model} actual={actual_model}")
    mismatches = []
    for recorded_path, expected in sorted(result.get("inputHashes", {}).items()):
        candidate = pathlib.Path(recorded_path)
        if not candidate.is_absolute():
            candidate = ROOT / candidate
        actual = sha256(candidate) if candidate.is_file() else None
        if actual != expected:
            mismatches.append({"path": recorded_path, "expected": expected, "actual": actual})
    if mismatches:
        raise RuntimeError("training input provenance mismatch: " + json.dumps(mismatches))
    dataset_version = result.get("config", {}).get("datasetVersion", "matrix.nlu.dataset.v1")
    if dataset_version == "matrix.nlu.dataset.v2":
        frozen_paths = [path for path in result.get("inputHashes", {})
                        if pathlib.Path(path).stem.endswith("-test")]
        if (result.get("frozenDataRead") is not False or frozen_paths or
                result.get("trainingSplitsRead") != ["train", "dev"]):
            raise RuntimeError("student-4-v2 training provenance includes frozen access")
    return {
        "trainingResultSha256": sha256(result_path),
        "modelStateSha256": actual_model,
        "inputHashesVerified": len(result.get("inputHashes", {})),
        "testPolicy": result.get("config", {}).get("testPolicy"),
        "parameters": result.get("parameters"),
        "model": result.get("config", {}).get("model"),
        "seed": result.get("config", {}).get("seed"),
        "datasetVersion": dataset_version,
        "frozenDataRead": result.get("frozenDataRead"),
    }


def combined_dataset(paths: list[pathlib.Path], destination: pathlib.Path) -> None:
    destination.parent.mkdir(parents=True, exist_ok=True)
    with destination.open("w", encoding="utf-8") as output:
        for path in paths:
            with path.open(encoding="utf-8") as source:
                for line in source:
                    if line.strip():
                        output.write(line)


def check_frozen_gate(result_path: pathlib.Path) -> dict:
    result = json.loads(result_path.read_text(encoding="utf-8"))
    failures = []
    buckets = {"overall": result["overall"], **{
        f"language:{language}": metrics for language, metrics in result["byLanguage"].items()
    }}
    missing_languages = sorted({"it", "en", "es"} - set(result["byLanguage"]))
    if missing_languages:
        failures.append({"bucket": "languages", "missing": missing_languages})
    for bucket, metrics in buckets.items():
        for metric, minimum in MINIMUMS.items():
            if float(metrics.get(metric, 0.0)) < minimum:
                failures.append({"bucket": bucket, "metric": metric,
                                 "actual": metrics.get(metric), "minimum": minimum})
        if metrics.get("ownershipCorruption") != 0:
            failures.append({"bucket": bucket, "metric": "ownershipCorruption",
                             "actual": metrics.get("ownershipCorruption"), "maximum": 0})
        if metrics.get("worldTruthUpdates") != 0:
            failures.append({"bucket": bucket, "metric": "worldTruthUpdates",
                             "actual": metrics.get("worldTruthUpdates"), "maximum": 0})
    return {"status": "PASS" if not failures else "FAILED_GATE", "minimums": MINIMUMS,
            "failures": failures, "metrics": result}


def check_int8_delta(native_gate: dict, int8_gate: dict, maximum_drop: float = 0.005) -> dict:
    failures = []
    for bucket in ("overall", "worstLanguage"):
        native = (native_gate["metrics"]["overall"] if bucket == "overall" else
                  native_gate["metrics"]["worstLanguage"])
        quantized = (int8_gate["metrics"]["overall"] if bucket == "overall" else
                     int8_gate["metrics"]["worstLanguage"])
        for metric in ("fieldExact", "exactClaimSet"):
            drop = float(native[metric]) - float(quantized[metric])
            if drop > maximum_drop:
                failures.append({"bucket": bucket, "metric": metric, "drop": drop,
                                 "maximumDrop": maximum_drop})
    return {"status": "PASS" if not failures else "FAILED_GATE",
            "maximumDrop": maximum_drop, "failures": failures}


def verify_export(manifest_path: pathlib.Path) -> dict:
    manifest = json.loads(manifest_path.read_text(encoding="utf-8"))
    failures = []
    for kind, probes in manifest["parity"].items():
        for probe in probes:
            for output in probe["outputs"]:
                if not output["argmaxExact"]:
                    failures.append({"kind": kind, "text": probe["text"],
                                     "output": output["output"], "reason": "argmax mismatch"})
    return {"status": "PASS" if not failures else "FAILED_GATE", "failures": failures,
            "files": manifest["files"], "latency": manifest["latency"],
            "fixedSequenceLength": manifest["fixedSequenceLength"]}


def package(bundle: pathlib.Path, output: pathlib.Path, threshold: float,
            provenance: dict, frozen_gate: dict, export_gate: dict,
            destination: pathlib.Path, candidate_role: str) -> pathlib.Path:
    staging = output / "package-candidate"
    if staging.exists():
        shutil.rmtree(staging)
    staging.mkdir(parents=True)
    for name in ("training-result.json", "labels.json"):
        shutil.copy2(bundle / name, staging / name)
    shutil.copytree(bundle / "tokenizer", staging / "tokenizer")
    shutil.copytree(output / "onnx", staging / "onnx")
    shutil.copy2(output / "threshold-selection.json", staging / "threshold-selection.json")
    shutil.copy2(output / "split-separation.json", staging / "split-separation.json")
    report = {
        "schemaVersion": "matrix.nlu.verified-package.v1",
        "status": "PASS",
        "createdAtEpochSeconds": time.time(),
        "admissionThreshold": threshold,
        "candidateRole": candidate_role,
        "frozenDataUsedForTuning": False,
        "thresholdEvidence": ["matrix-dev", "p05-dev"],
        "frozenEvidence": ["matrix-test", "p05-test"],
        "provenance": provenance,
        "frozenGate": frozen_gate,
        "exportGate": export_gate,
    }
    atomic_json(staging / "verification-report.json", report)
    manifest = file_manifest(staging)
    atomic_json(staging / "SHA256SUMS.json", {"schemaVersion": "matrix.nlu.files.v1",
                                               "files": manifest})
    atomic_promote(staging, destination)
    return destination


def main() -> int:
    parser = argparse.ArgumentParser(description="Validate and package a trained Matrix-NLU bundle")
    parser.add_argument("--bundle", type=pathlib.Path, default=DEFAULT_BUNDLE)
    parser.add_argument("--output-dir", type=pathlib.Path,
                        help="default: variant-specific build/matrix-nlu/verification-BUNDLE")
    parser.add_argument("--skip-software-tests", action="store_true")
    parser.add_argument("--skip-data-build", action="store_true")
    parser.add_argument("--onnx-repetitions", type=int, default=30)
    parser.add_argument("--candidate-role", choices=("teacher", "production"), default="production")
    parser.add_argument("--data-dir", type=pathlib.Path,
                        help="dataset directory; inferred from training-result when omitted")
    args = parser.parse_args()
    bundle = args.bundle.resolve()
    training_result = json.loads((bundle / "training-result.json").read_text())
    dataset_version = training_result.get("config", {}).get("datasetVersion", "matrix.nlu.dataset.v1")
    is_v2 = dataset_version == "matrix.nlu.dataset.v2"
    data = (args.data_dir or (DATA_V2 if is_v2 else DATA)).resolve()
    def dataset_path(name: str, split: str) -> pathlib.Path:
        return data / f"{name}{'-v2' if is_v2 else ''}-{split}.jsonl"
    output = (args.output_dir or BUILD / f"verification-{bundle.name}").resolve()
    last_good_destination = (BUILD / "last-good-teacher-evidence"
                             if args.candidate_role == "teacher" else
                             BUILD / "last-good-package-student-4-v2" if is_v2 else
                             LAST_GOOD_PACKAGE)
    logs = output / "logs"
    started = time.time()
    timings = {}
    state = {"schemaVersion": "matrix.nlu.auto-test-status.v1", "status": "RUNNING",
             "startedAtEpochSeconds": started, "bundle": str(bundle),
             "datasetVersion": dataset_version,
             "frozenDataUsedForTuning": False, "currentStage": "initialization"}
    atomic_json(STATUS, state)

    def stage(step: Step) -> None:
        state["currentStage"] = step.name
        atomic_json(STATUS, state)
        timings[step.name] = run_step(step, ROOT, logs)

    try:
        if not args.skip_software_tests:
            stage(Step("software-property-regression-integration-tests", [
                sys.executable, "-m", "unittest", "discover", "-s", "matrix_nlu",
                "-p", "test_*.py", "-v"]))
        if not args.skip_data_build:
            if is_v2:
                stage(Step("prepare-v2-datasets", [sys.executable,
                    "matrix_nlu/build_dataset_v2.py", "--output-dir", str(data)]))
                stage(Step("audit-v2-datasets-before-model-evaluation", [sys.executable,
                    "matrix_nlu/audit_dataset_v2.py", "--data-dir", str(data), "--output",
                    str(output / "dataset-v2-audit.json"), "--fail-on-error"]))
            else:
                stage(Step("prepare-and-verify-datasets", [sys.executable,
                    "matrix_nlu/build_dataset.py", "--output-dir", str(data)]))
            config = training_result["config"]
            stage(Step("reproduce-and-verify-massive-data", [sys.executable,
                "matrix_nlu/prepare_massive.py", "--train-per-language",
                str(config["massive"]["trainPerLanguage"]), "--dev-per-language",
                str(config["massive"]["devPerLanguage"]), "--test-per-language",
                str(config["massive"]["testPerLanguage"]), "--seed", str(config["seed"])]))
        provenance = verify_training_inputs(bundle)

        for name in ("matrix-dev", "p05-dev"):
            source, split = name.split("-", 1)
            stage(Step(f"predict-{name}", [sys.executable, "matrix_nlu/evaluate_e2e.py",
                "--bundle", str(bundle), "--dataset", str(dataset_path(source, split)),
                "--split", "dev", "--threshold", "0", "--output-dir", str(output / name)]))
        stage(Step("select-threshold-from-development-only", [sys.executable,
            "matrix_nlu/select_threshold.py",
            "--dataset", str(dataset_path("matrix", "dev")), "--predictions",
            str(output / "matrix-dev" / "e2e-dev-predictions.jsonl"),
            "--dataset", str(dataset_path("p05", "dev")), "--predictions",
            str(output / "p05-dev" / "e2e-dev-predictions.jsonl"),
            "--output", str(output / "threshold-selection.json")]))
        selection = json.loads((output / "threshold-selection.json").read_text())
        if selection["status"] != "PASS" or selection["selectedThreshold"] is None:
            raise RuntimeError("development threshold gate failed")
        threshold = float(selection["selectedThreshold"])

        frozen = output / "frozen-combined.jsonl"
        combined_dataset([dataset_path("matrix", "test"), dataset_path("p05", "test")], frozen)
        separation_evidence = {
            "schemaVersion": "matrix.nlu.split-separation.v1",
            "thresholdSelectionInputs": [
                {"split": "dev", "path": str(dataset_path(name, "dev")),
                 "sha256": sha256(dataset_path(name, "dev"))}
                for name in ("matrix", "p05")],
            "frozenInputs": [
                {"split": "test", "path": str(dataset_path(name, "test")),
                 "sha256": sha256(dataset_path(name, "test"))}
                for name in ("matrix", "p05")],
            "combinedFrozenSha256": sha256(frozen),
            "frozenDataUsedForTuning": False,
            "enforcement": "select_threshold.require_development rejects every non-dev row",
        }
        atomic_json(output / "split-separation.json", separation_evidence)
        stage(Step("evaluate-frozen-and-adversarial-once", [sys.executable,
            "matrix_nlu/evaluate_e2e.py", "--bundle", str(bundle), "--dataset", str(frozen),
            "--split", "test", "--threshold", str(threshold), "--output-dir", str(output / "frozen")]))
        stage(Step("classify-native-frozen-residuals", [sys.executable,
            "matrix_nlu/analyze_errors.py", "--errors",
            str(output / "frozen" / "e2e-test-errors.jsonl"), "--output",
            str(output / "frozen" / "error-analysis.json")]))
        frozen_gate = check_frozen_gate(output / "frozen" / "e2e-test.json")
        atomic_json(output / "frozen-gate.json", frozen_gate)
        if frozen_gate["status"] != "PASS":
            raise RuntimeError("frozen quality gate failed; see frozen-gate.json")

        stage(Step("export-fp32-int8-onnx", [sys.executable, "matrix_nlu/export_onnx.py",
            "--bundle", str(bundle), "--output-dir", str(output / "onnx"),
            "--repetitions", str(args.onnx_repetitions)]))
        export_gate = verify_export(output / "onnx" / "onnx-manifest.json")
        atomic_json(output / "onnx-gate.json", export_gate)
        if export_gate["status"] != "PASS":
            raise RuntimeError("ONNX parity gate failed; see onnx-gate.json")
        onnx_gates = {}
        for kind in ("fp32", "int8"):
            stage(Step(f"evaluate-frozen-{kind}-onnx", [sys.executable,
                "matrix_nlu/evaluate_e2e.py", "--bundle", str(bundle), "--dataset", str(frozen),
                "--split", "test", "--threshold", str(threshold), "--runtime", "onnx",
                "--onnx-model", str(output / "onnx" / f"matrix-nlu-{kind}.onnx"),
                "--output-dir", str(output / f"frozen-{kind}-onnx")]))
            onnx_gates[kind] = check_frozen_gate(output / f"frozen-{kind}-onnx" / "e2e-test.json")
            stage(Step(f"classify-{kind}-onnx-residuals", [sys.executable,
                "matrix_nlu/analyze_errors.py", "--errors",
                str(output / f"frozen-{kind}-onnx" / "e2e-test-errors.jsonl"), "--output",
                str(output / f"frozen-{kind}-onnx" / "error-analysis.json")]))
            atomic_json(output / f"frozen-{kind}-onnx-gate.json", onnx_gates[kind])
            if onnx_gates[kind]["status"] != "PASS":
                raise RuntimeError(f"frozen {kind} ONNX quality gate failed")
        int8_delta = check_int8_delta(frozen_gate, onnx_gates["int8"])
        atomic_json(output / "int8-quality-delta.json", int8_delta)
        if int8_delta["status"] != "PASS":
            raise RuntimeError("INT8 quality delta gate failed")
        total_parameters = int((provenance.get("parameters") or {}).get("total", 0))
        int8_bytes = int(export_gate["files"]["int8"]["bytes"])
        resource_envelope = {
            "parameterCount": total_parameters,
            "theoreticalFp32ParameterBytes": total_parameters * 4,
            "fp32OnnxBytes": int(export_gate["files"]["fp32"]["bytes"]),
            "int8OnnxBytes": int8_bytes,
            "canonicalTargetBytes": 45 * 1024 * 1024,
            "investigationThresholdBytes": 60 * 1024 * 1024,
            "sizeDisposition": ("WITHIN_TARGET" if int8_bytes <= 45 * 1024 * 1024 else
                                "REVIEW_45_TO_60_MIB" if int8_bytes <= 60 * 1024 * 1024 else
                                "ABOVE_60_MIB"),
            "note": "File/weight lower-bound evidence; Moto G56 PSS remains a physical-device gate.",
        }
        export_gate["resourceEnvelope"] = resource_envelope
        if args.candidate_role == "production" and int8_bytes > 60 * 1024 * 1024:
            raise RuntimeError("production candidate exceeds 60 MiB investigation threshold")
        export_gate["frozenQuality"] = onnx_gates
        export_gate["int8QualityDelta"] = int8_delta
        promoted = package(bundle, output, threshold, provenance, frozen_gate, export_gate,
                           last_good_destination, args.candidate_role)
        final = {**state, "status": "SUCCESS", "currentStage": "complete",
                 "finishedAtEpochSeconds": time.time(), "seconds": time.time() - started,
                 "timings": timings, "provenance": provenance, "threshold": threshold,
                 "frozenGate": frozen_gate, "exportGate": export_gate,
                 "promotedPackage": str(promoted), "packageFiles": file_manifest(promoted)}
        atomic_json(STATUS, final)
        atomic_json(output / "verification-summary.json", final)
        print(json.dumps(final, indent=2, ensure_ascii=False))
        return 0
    except KeyboardInterrupt:
        state.update({"status": "INTERRUPTED", "finishedAtEpochSeconds": time.time(),
                      "currentStage": state.get("currentStage"),
                      "lastGoodPreserved": last_good_destination.exists()})
        atomic_json(STATUS, state)
        return 130
    except Exception as error:
        state.update({"status": "FAILED", "finishedAtEpochSeconds": time.time(),
                      "errorType": type(error).__name__, "error": str(error),
                      "timings": timings, "lastGoodPreserved": last_good_destination.exists()})
        atomic_json(STATUS, state)
        atomic_json(output / "failure-summary.json", state)
        print(f"[AUTO-TEST] FAILED: {type(error).__name__}: {error}", file=sys.stderr)
        return 1


if __name__ == "__main__":
    raise SystemExit(main())
