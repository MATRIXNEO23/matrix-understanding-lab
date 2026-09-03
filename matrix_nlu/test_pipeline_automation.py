import json
import pathlib
import tempfile
import unittest

import auto_test
import auto_train
import run_pipeline
from pipeline_support import atomic_json, atomic_promote, file_manifest, sha256


def passing_metrics():
    return {
        "claimCountExact": 1.0, "exactClaimSet": 1.0, "fieldExact": 1.0,
        "validSelectiveAccuracy": 1.0, "validCoverage": 1.0,
        "ownershipCorruption": 0, "worldTruthUpdates": 0,
    }


class PipelineAutomationTest(unittest.TestCase):
    def test_training_runs_contract_audit_before_external_data_and_training(self):
        args = type("Args", (), {
            "massive_train_per_language": 3,
            "massive_dev_per_language": 3,
            "massive_test_per_language": 3,
            "seed": 810923,
            "student_layers": 4,
        })()
        names = [step.name for step in auto_train.build_steps(
            args, auto_train.ROOT / "build/matrix-nlu/training-student-4")]
        self.assertEqual([
            "Software regression tests",
            "Build Matrix datasets",
            "Audit train-dev annotation contracts",
            "Prepare verified MASSIVE auxiliary data",
            "Train/resume Matrix-NLU",
        ], names)

    def test_one_click_ci_uses_separate_report_bundle_and_resume_artifacts(self):
        workflow = (pathlib.Path(__file__).resolve().parents[1] / ".github" /
                    "workflows" / "matrix-nlu-train.yml").read_text(encoding="utf-8")
        self.assertIn("matrix-nlu-report-${{ github.run_id }}", workflow)
        self.assertIn("matrix-nlu-bundle-${{ github.run_id }}", workflow)
        self.assertIn("matrix-nlu-resume-${{ github.run_id }}", workflow)
        self.assertNotIn("name: matrix-nlu-one-click-${{ github.run_id }}", workflow)

    def test_frozen_gate_is_zero_tolerance_and_per_language(self):
        with tempfile.TemporaryDirectory() as temporary:
            path = pathlib.Path(temporary) / "result.json"
            result = {"overall": passing_metrics(), "byLanguage": {
                language: passing_metrics() for language in ("it", "en", "es")}}
            path.write_text(json.dumps(result), encoding="utf-8")
            self.assertEqual("PASS", auto_test.check_frozen_gate(path)["status"])
            result["byLanguage"]["es"]["ownershipCorruption"] = 1
            path.write_text(json.dumps(result), encoding="utf-8")
            failed = auto_test.check_frozen_gate(path)
            self.assertEqual("FAILED_GATE", failed["status"])
            self.assertTrue(any(item.get("bucket") == "language:es" for item in failed["failures"]))

    def test_frozen_gate_requires_all_target_languages(self):
        with tempfile.TemporaryDirectory() as temporary:
            path = pathlib.Path(temporary) / "result.json"
            path.write_text(json.dumps({"overall": passing_metrics(), "byLanguage": {
                "it": passing_metrics(), "en": passing_metrics()}}), encoding="utf-8")
            result = auto_test.check_frozen_gate(path)
            self.assertEqual("FAILED_GATE", result["status"])
            self.assertIn("es", result["failures"][0]["missing"])

    def test_export_gate_rejects_any_head_argmax_delta(self):
        with tempfile.TemporaryDirectory() as temporary:
            path = pathlib.Path(temporary) / "onnx-manifest.json"
            manifest = {"parity": {"fp32": [{"text": "x", "outputs": [
                {"output": "sequence.owner", "argmaxExact": True}]}],
                "int8": [{"text": "x", "outputs": [
                    {"output": "sequence.owner", "argmaxExact": False}]}]},
                "files": {}, "latency": {}, "fixedSequenceLength": 64}
            path.write_text(json.dumps(manifest), encoding="utf-8")
            result = auto_test.verify_export(path)
            self.assertEqual("FAILED_GATE", result["status"])
            self.assertEqual("int8", result["failures"][0]["kind"])

    def test_atomic_promotion_preserves_complete_manifested_copy(self):
        with tempfile.TemporaryDirectory() as temporary:
            root = pathlib.Path(temporary)
            source, destination = root / "candidate", root / "last-good"
            source.mkdir()
            (source / "model.bin").write_bytes(b"verified")
            atomic_promote(source, destination)
            self.assertEqual("verified", (destination / "model.bin").read_text())
            self.assertEqual(sha256(destination / "model.bin"), file_manifest(destination)[0]["sha256"])

    def test_status_json_write_is_complete(self):
        with tempfile.TemporaryDirectory() as temporary:
            path = pathlib.Path(temporary) / "status.json"
            atomic_json(path, {"status": "RUNNING"})
            self.assertEqual({"status": "RUNNING"}, json.loads(path.read_text()))

    def test_one_click_order_and_existing_bundle_mode(self):
        train_args = type("Args", (), {"skip_train": False, "bundle": None,
            "student_layers": None, "seed": 810923, "onnx_repetitions": 2})()
        self.assertEqual(["prepare-verify-train-or-resume", "validate-frozen-adversarial-package"],
                         [step.name for step in run_pipeline.commands(train_args)])
        bundle_args = type("Args", (), {"skip_train": True, "bundle": pathlib.Path("candidate"),
            "student_layers": None, "seed": 810923, "onnx_repetitions": 2})()
        steps = run_pipeline.commands(bundle_args)
        self.assertEqual(1, len(steps))
        self.assertIn("candidate", steps[0].command)


if __name__ == "__main__":
    unittest.main()
