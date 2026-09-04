import hashlib
import json
import pathlib
import tempfile
import unittest

from labels import SEQUENCE_LABELS, TOKEN_LABELS
from train import class_weight_values, stage_complete, validate_resume_evidence


class TrainResumePolicyTest(unittest.TestCase):
    def test_completed_epoch_range_is_not_replayed(self):
        checkpoint = {"stage": "matrix", "nextEpoch": 4, "epochsWithoutImprovement": 0}
        self.assertTrue(stage_complete(checkpoint, "matrix", 4, 2))
        self.assertFalse(stage_complete(checkpoint, "massive-aux", 1, 2))

    def test_early_stopped_stage_is_complete(self):
        checkpoint = {"stage": "matrix", "nextEpoch": 3, "epochsWithoutImprovement": 2}
        self.assertTrue(stage_complete(checkpoint, "matrix", 5, 2))

    def test_incomplete_stage_remains_resumable(self):
        checkpoint = {"stage": "matrix", "nextEpoch": 2, "epochsWithoutImprovement": 1}
        self.assertFalse(stage_complete(checkpoint, "matrix", 4, 2))

    def test_pre_identity_resume_requires_matching_external_evidence(self):
        identity = {"datasetVersion": "matrix.nlu.dataset.v2",
                    "variant": "student-4-v2", "studentLayers": 4,
                    "configSha256": "current"}
        with tempfile.TemporaryDirectory() as temporary:
            root = pathlib.Path(temporary)
            checkpoint = root / "latest.pt"
            checkpoint.write_bytes(b"isolated-v2-checkpoint")
            evidence = {"schemaVersion": "matrix.nlu.resume-evidence.v1",
                        "sourceRunId": 33818777290,
                        "checkpointSha256": hashlib.sha256(checkpoint.read_bytes()).hexdigest(),
                        "datasetVersion": identity["datasetVersion"],
                        "variant": identity["variant"], "studentLayers": 4}
            path = root / "resume-evidence.json"
            path.write_text(json.dumps(evidence), encoding="utf-8")
            self.assertEqual(evidence, validate_resume_evidence(path, checkpoint, identity))
            evidence["variant"] = "student-4-layer"
            path.write_text(json.dumps(evidence), encoding="utf-8")
            with self.assertRaisesRegex(RuntimeError, "invalid v2 resume evidence"):
                validate_resume_evidence(path, checkpoint, identity)

    def test_inverse_sqrt_weights_raise_rare_sequence_and_token_classes(self):
        examples = []
        for index in range(10):
            sequence = {head: 0 for head in SEQUENCE_LABELS}
            tokens = {head: [0, 0, 0] for head in TOKEN_LABELS}
            if index == 9:
                sequence["polarity"] = 1
                tokens["negation"] = [1, 2, 2]
            examples.append({"sequence_labels": sequence, "token_labels": tokens})
        weights = class_weight_values(examples, {
            "classWeighting": {"method": "inverse-frequency-sqrt",
                               "groups": ["tokens", "sequence"], "maximum": 8.0}})
        self.assertGreater(weights["sequence"]["polarity"][1],
                           weights["sequence"]["polarity"][0])
        self.assertGreater(weights["tokens"]["negation"][1],
                           weights["tokens"]["negation"][0])


if __name__ == "__main__":
    unittest.main()
