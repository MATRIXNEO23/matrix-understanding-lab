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


def passing_result(languages=("it", "en", "es")):
    return {"overall": passing_metrics(),
            "byLanguage": {language: passing_metrics() for language in languages},
            "byCriticalFamily": {family: {"observations": 3, "failedObservations": 0,
                                           "exactClaimSet": 1.0,
                                           "byLanguage": {language: {
                                               "observations": 1,
                                               "failedObservations": 0,
                                               "exactClaimSet": 1.0}
                                               for language in ("it", "en", "es")}}
                                 for family in auto_test.CRITICAL_FAMILIES}}


class PipelineAutomationTest(unittest.TestCase):
    def test_training_runs_contract_audit_before_external_data_and_training(self):
        args = type("Args", (), {
            "massive_train_per_language": 3,
            "massive_dev_per_language": 3,
            "massive_test_per_language": 3,
            "seed": 810923,
            "student_layers": 4,
            "dataset_version": "v1",
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

    def test_v2_ci_is_isolated_from_v1_workflow_and_artifacts(self):
        root = pathlib.Path(__file__).resolve().parents[1]
        v1 = (root / ".github/workflows/matrix-nlu-train.yml").read_text(encoding="utf-8")
        v2 = (root / ".github/workflows/matrix-nlu-student-4-v2.yml").read_text(
            encoding="utf-8")
        self.assertIn("pipeline/student-4.trigger", v1)
        self.assertNotIn("student-4-v2", v1)
        self.assertIn("pipeline/student-4-v2-resume.trigger", v2)
        self.assertIn("--dataset-version v2 --student-layers 4", v2)
        self.assertIn("matrix-nlu-student-4-v2-resume-${{ github.run_id }}", v2)
        self.assertIn("--resume-evidence", v2)

    def test_v2_hardened_post_gate_reuses_bundle_without_retraining(self):
        root = pathlib.Path(__file__).resolve().parents[1]
        workflow = (root / ".github/workflows/matrix-nlu-student-4-v2-post.yml").read_text(
            encoding="utf-8")
        self.assertIn("pipeline/student-4-v2-post.trigger", workflow)
        self.assertIn("matrix-nlu-bundle-$SOURCE_RUN", workflow)
        self.assertIn("python auto_test.py", workflow)
        self.assertNotIn("python auto_train.py", workflow)
        self.assertIn("--candidate-role counter-review", workflow)

    def test_v2_pipeline_audits_before_training_and_defers_frozen(self):
        args = type("Args", (), {
            "massive_train_per_language": 3, "massive_dev_per_language": 3,
            "massive_test_per_language": 3, "seed": 810923,
            "student_layers": 4, "dataset_version": "v2",
        })()
        steps = auto_train.build_steps(
            args, auto_train.ROOT / "build/matrix-nlu/training-student-4-v2")
        self.assertEqual("Audit complete v2 dataset before training", steps[2].name)
        self.assertLess([step.name for step in steps].index(
            "Audit complete v2 dataset before training"),
            [step.name for step in steps].index("Train/resume Matrix-NLU"))
        self.assertIn("--defer-frozen", steps[-1].command)
        self.assertTrue(any(value.endswith("train_config_v2.json")
                            for value in steps[-1].command))
        self.assertFalse(any(value.endswith("-test.jsonl")
                             for value in steps[-1].command))

    def test_v2_pipeline_is_counter_review_not_production(self):
        args = type("Args", (), {"skip_train": False, "bundle": None,
            "student_layers": 4, "seed": 810923, "onnx_repetitions": 2,
            "dataset_version": "v2", "candidate_role": "production"})()
        testing = run_pipeline.commands(args)[-1].command
        role = testing[testing.index("--candidate-role") + 1]
        self.assertEqual("counter-review", role)

    def test_frozen_gate_is_zero_tolerance_and_per_language(self):
        with tempfile.TemporaryDirectory() as temporary:
            path = pathlib.Path(temporary) / "result.json"
            result = passing_result()
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
            path.write_text(json.dumps(passing_result(("it", "en"))), encoding="utf-8")
            result = auto_test.check_frozen_gate(path)
            self.assertEqual("FAILED_GATE", result["status"])
            self.assertIn("es", result["failures"][0]["missing"])

    def test_frozen_gate_rejects_systematic_critical_family_error(self):
        with tempfile.TemporaryDirectory() as temporary:
            path = pathlib.Path(temporary) / "result.json"
            result = passing_result()
            result["byCriticalFamily"]["negation"]["exactClaimSet"] = 0.90
            path.write_text(json.dumps(result), encoding="utf-8")
            gate = auto_test.check_frozen_gate(path)
            self.assertEqual("FAILED_GATE", gate["status"])
            self.assertTrue(any(item["bucket"] == "critical:negation"
                                for item in gate["failures"]))

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
            "student_layers": None, "seed": 810923, "onnx_repetitions": 2,
            "dataset_version": "v1"})()
        self.assertEqual(["prepare-verify-train-or-resume", "validate-frozen-adversarial-package"],
                         [step.name for step in run_pipeline.commands(train_args)])
        bundle_args = type("Args", (), {"skip_train": True, "bundle": pathlib.Path("candidate"),
            "student_layers": None, "seed": 810923, "onnx_repetitions": 2,
            "dataset_version": "v1"})()
        steps = run_pipeline.commands(bundle_args)
        self.assertEqual(1, len(steps))
        self.assertIn("candidate", steps[0].command)


if __name__ == "__main__":
    unittest.main()
