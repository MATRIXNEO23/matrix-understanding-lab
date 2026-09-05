import inspect
import unittest

import evaluate_v3
import inference_v3
import referent_candidates
from synthetic_v3_fixtures import SYNTHETIC_CASES
from test_inference_v3 import marco_fixture


def gold_and_prediction(language="en", domain="general"):
    text, mentions, table, raw = marco_fixture()
    prediction = inference_v3.build_matrix_output_v3(
        text=text, observation_source_id="synthetic", context={"speaker": "player", "observer": "matrix"},
        mentions=mentions, candidate_table=table, raw_claims=[raw],
    )
    gold_claim = {
        "claimId": "c0", "sourceSpan": raw["sourceSpan"],
        "subjectSpans": raw["subjectSpans"], "objectSpans": [],
        "negationCueSpans": [], "temporalEvidence": [],
        "entityMentionIds": ["m0", "m1", "m2"],
        "dialogueAct": "ASSERT", "predicate": "preference.like",
        "subjectReferent": "mention:m1", "targetReferent": "mention:m2",
        "ownerReferent": "mention:m1", "perspectiveReferent": "mention:m0",
        "sourceReferent": "mention:m0", "polarity": "POSITIVE",
        "temporalRelation": {"relation": "CURRENT", "anchorRef": "speech-time"},
        "claimKind": "REPORT", "interpretationStatus": "RESOLVED",
    }
    gold = {
        "contractVersion": "MATRIX_NLU_CONTRACT_V3", "id": "g0",
        "language": language, "domain": domain, "text": text,
        "referentCandidates": table["candidates"], "claims": [gold_claim],
    }
    return gold, prediction


class EvaluateV3Test(unittest.TestCase):
    def test_gold_normalizer_is_independent_from_production_validator(self):
        source = inspect.getsource(evaluate_v3)
        self.assertNotIn("import inference_v3", source)
        self.assertNotIn("validate_claim_v3", source)

    def test_perfect_structure_scores_one(self):
        gold, prediction = gold_and_prediction()
        result = evaluate_v3.score_v3_rows([gold], [prediction])
        self.assertEqual(1.0, result["claimExact"])
        self.assertEqual(1.0, result["rolePointerExact"])
        self.assertEqual(0, result["ownershipCorruptions"])
        self.assertEqual(0, result["sourceCorruptions"])

    def test_wrong_role_is_detected_not_mirrored_into_gold(self):
        gold, prediction = gold_and_prediction()
        prediction["claims"][0]["ownerReferent"]["value"] = "mention:m0"
        prediction["claims"][0]["sourceReferent"]["value"] = "mention:m1"
        result = evaluate_v3.score_v3_rows([gold], [prediction])
        self.assertLess(result["rolePointerExact"], 1.0)
        self.assertEqual(1, result["ownershipCorruptions"])
        self.assertEqual(1, result["sourceCorruptions"])

    def test_field_status_and_abstention_are_scored(self):
        gold, prediction = gold_and_prediction()
        prediction["claims"][0]["sourceReferent"]["fieldStatus"] = "AMBIGUOUS"
        prediction["claims"][0]["fieldStatusByField"]["sourceReferent"] = "AMBIGUOUS"
        prediction["claims"][0]["interpretationStatus"] = "AMBIGUOUS"
        result = evaluate_v3.score_v3_rows([gold], [prediction])
        self.assertLess(result["fieldStatusExact"], 1.0)
        self.assertLess(result["claimExact"], 1.0)

    def test_negation_polarity_temporal_anchor_and_status_are_scored(self):
        gold, prediction = gold_and_prediction()
        gold["claims"][0]["negationCueSpans"] = [[0, 5], [6, 10]]
        prediction["claims"][0]["negationCueSpans"] = [[0, 5]]
        prediction["claims"][0]["polarity"]["value"] = "NEGATIVE"
        prediction["claims"][0]["temporalRelation"]["value"]["anchorRef"] = None
        prediction["claims"][0]["interpretationStatus"] = "ABSTAINED"
        result = evaluate_v3.score_v3_rows([gold], [prediction])
        self.assertLess(result["claimExact"], 1.0)
        self.assertLess(result["spanGroupExact"], 1.0)
        self.assertLess(result["temporalExact"], 1.0)

    def test_language_and_adult_slices_remain_ordinary(self):
        rows, predictions = [], []
        for language, domain in (("it", "general"), ("en", "adult-intimacy"), ("es", "general")):
            gold, prediction = gold_and_prediction(language, domain)
            rows.append(gold); predictions.append(prediction)
        result = evaluate_v3.score_v3_rows(rows, predictions)
        self.assertEqual({"en:adult-intimacy", "es:general", "it:general"}, set(result["slices"]))
        self.assertTrue(all(value["rolePointerExact"] == 1.0 for value in result["slices"].values()))

    def test_synthetic_inventory_covers_required_families_and_languages(self):
        families = {item["family"] for item in SYNTHETIC_CASES}
        languages = {item["language"] for item in SYNTHETIC_CASES}
        domains = {item.get("domain", "general") for item in SYNTHETIC_CASES}
        for family in ("referent", "report", "belief", "hypothesis", "command", "request", "negation", "temporal", "multi-claim", "adult-consent", "adult-refusal", "adult-withdrawal-report"):
            self.assertIn(family, families)
        self.assertTrue({"it", "en", "es", "code-switch"} <= languages)
        self.assertIn("adult-intimacy", domains)
        self.assertFalse(any("unsafe" in item["text"].casefold() or "censor" in item["text"].casefold() for item in SYNTHETIC_CASES))


if __name__ == "__main__":
    unittest.main()
