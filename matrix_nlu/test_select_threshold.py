import unittest

from test_evaluate_e2e import prediction, row
from select_threshold import apply_threshold, choose_threshold, require_development


def evidence(confidence=.9):
    observed = prediction()
    labels = {"dialogueAct": "ASSERT", "predicate": "preference.like",
              "subjectReferent": "SPEAKER", "targetReferent": "NONE",
              "ownerReferent": "SUBJECT", "perspectiveReferent": "SPEAKER",
              "polarity": "POSITIVE", "temporalRelation": "ATEMPORAL",
              "claimKind": "EXPLICIT"}
    observed["rawClaims"] = [{"labels": labels, "confidence": confidence, "spans": {
        "source": [0, 10], "object": [4, 10], "subject": None,
        "negation": None, "temporal": None, "entities": []}}]
    return [{"id": "r1", "language": "it", "prediction": observed}]


class ThresholdSelectionTest(unittest.TestCase):
    def test_revalidation_abstains_above_confidence(self):
        observed = apply_threshold([row()], evidence(.7), .8)
        self.assertEqual("ABSTAINED_LOW_CONFIDENCE", observed[0]["claims"][0]["status"])

    def test_selects_maximum_coverage_passing_dev_accuracy(self):
        result = choose_threshold([row()], evidence(.9), .99)
        self.assertEqual("PASS", result["status"])
        self.assertEqual(0.0, result["selectedThreshold"])
        self.assertEqual(1.0, result["selectedMetrics"]["validCoverage"])

    def test_no_false_pass_from_zero_coverage(self):
        bad = evidence(.3)
        bad[0]["prediction"]["rawClaims"][0]["labels"]["predicate"] = "identity.age"
        result = choose_threshold([row()], bad, .99)
        self.assertEqual("FAILED_GATE", result["status"])
        self.assertIsNone(result["selectedThreshold"])

    def test_extra_claim_cannot_pass_selective_accuracy_gate(self):
        extra = evidence(.9)
        extra[0]["prediction"]["rawClaims"].append(
            dict(extra[0]["prediction"]["rawClaims"][0]))
        result = choose_threshold([row()], extra, .99)
        self.assertEqual("FAILED_GATE", result["status"])

    def test_frozen_row_is_rejected_as_threshold_input(self):
        frozen = row()
        frozen["split"] = "test"
        with self.assertRaisesRegex(ValueError, "development partitions only"):
            require_development([frozen])


if __name__ == "__main__":
    unittest.main()
