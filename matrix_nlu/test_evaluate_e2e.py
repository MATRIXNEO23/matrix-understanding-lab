import unittest

from evaluate_e2e import score_rows


def row():
    return {"id": "r1", "split": "dev", "language": "it", "text": "amo il blu",
            "context": {"speaker": "PLAYER", "observer": "luna",
                        "knownEntities": {}, "recentEntityRefs": []},
            "claims": [{"sourceId": "gold:1", "labels": {
                "dialogueAct": "ASSERT", "predicate": "preference.like",
                "subjectReferent": "SPEAKER", "targetReferent": "NONE",
                "ownerReferent": "SUBJECT", "perspectiveReferent": "SPEAKER",
                "polarity": "POSITIVE", "temporalRelation": "ATEMPORAL",
                "claimKind": "EXPLICIT"}, "spans": {
                "source": [0, 10], "object": [4, 10], "subject": None,
                "negation": None, "temporal": None, "entities": []}}]}


def prediction():
    return {"claims": [{"status": "VALID", "speaker": "PLAYER", "subject": "PLAYER",
        "target": None, "owner": "PLAYER", "perspective": "PLAYER",
        "dialogueAct": "ASSERT", "predicate": "preference.like", "objectSpan": [4, 10],
        "polarity": "POSITIVE", "negationSpan": None, "temporalRelation": "ATEMPORAL",
        "temporalSpan": None, "entities": [], "claimKind": "EXPLICIT", "confidence": .9,
        "sourceSpans": [[0, 10]], "sourceIds": ["benchmark:r1"], "worldTruth": False,
        "memoryAdmission": "MEMORY_CANDIDATE", "diagnostics": []}]}


class EndToEndScoringTest(unittest.TestCase):
    def test_perfect_prediction_scores_one_and_zero_authority_violations(self):
        result, errors = score_rows([row()], [prediction()])
        self.assertEqual(1.0, result["overall"]["claimCountExact"])
        self.assertEqual(1.0, result["overall"]["claimExact"])
        self.assertEqual(1.0, result["overall"]["exactClaimSet"])
        self.assertEqual(1.0, result["overall"]["fieldExact"])
        self.assertEqual(1.0, result["overall"]["predicateAccuracy"])
        self.assertEqual(1.0, result["overall"]["temporalAccuracy"])
        self.assertEqual(0, result["overall"]["ownershipCorruption"])
        self.assertEqual(0, result["overall"]["worldTruthUpdates"])
        self.assertAlmostEqual(0.9, result["overall"]["calibration"]["meanConfidence"])
        self.assertAlmostEqual(0.01, result["overall"]["calibration"]["brier"])
        self.assertEqual([], errors)

    def test_wrong_owner_is_a_critical_error(self):
        observed = prediction()
        observed["claims"][0]["owner"] = "luna"
        result, errors = score_rows([row()], [observed])
        self.assertEqual(1, result["overall"]["ownershipCorruption"])
        self.assertEqual(1, result["byLanguage"]["it"]["ownershipCorruption"])
        self.assertLess(result["overall"]["fieldExact"], 1.0)
        self.assertEqual("owner", errors[0]["errors"][0]["field"])

    def test_extra_claim_fails_count_without_distorting_paired_field_denominator(self):
        observed = prediction()
        observed["claims"].append(dict(observed["claims"][0]))
        result, errors = score_rows([row()], [observed])
        self.assertEqual(0.0, result["overall"]["claimCountExact"])
        self.assertEqual(0.0, result["overall"]["exactClaimSet"])
        self.assertEqual(1.0, result["overall"]["fieldExact"])
        self.assertTrue(any(item["kind"] == "CLAIM_COUNT" for item in errors[0]["errors"]))


if __name__ == "__main__":
    unittest.main()
