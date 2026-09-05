import unittest

import contract_v3
import inference_v3
import referent_candidates


def semantic_field(value, confidence=0.99, status=None):
    return inference_v3.field(value, confidence, status)


def marco_fixture():
    text = "Marco told me that Anna loves Luca."
    spans = [
        {"span": [0, 5], "type": "PERSON"},
        {"span": [text.index("Anna"), text.index("Anna") + 4], "type": "PERSON"},
        {"span": [text.index("Luca"), text.index("Luca") + 4], "type": "PERSON"},
    ]
    mentions = referent_candidates.build_mentions(spans, len(text))
    table = referent_candidates.build_candidate_table(
        text, mentions, {"speaker": "player", "observer": "matrix"},
        critical_spans=[item["span"] for item in mentions],
    )
    confidence = {
        name: 0.99 for name in (
            "boundary", "subjectSpans", "objectSpans", "negationCueSpans",
            "temporalEvidence", "entityMentionIds", "dialogueAct", "predicate",
            *contract_v3.ROLE_HEADS, "polarity", "temporalRelation", "claimKind",
        )
    }
    claim = {
        "claimId": "c0",
        "sourceSpan": [0, len(text)],
        "subjectSpans": [[text.index("Anna"), text.index("Anna") + 4]],
        "objectSpans": [],
        "negationCueSpans": [],
        "temporalEvidence": [],
        "entityMentionIds": ["m0", "m1", "m2"],
        "dialogueAct": semantic_field("ASSERT"),
        "predicate": semantic_field("preference.like"),
        "subjectReferent": semantic_field("mention:m1"),
        "targetReferent": semantic_field("mention:m2"),
        "ownerReferent": semantic_field("mention:m1"),
        "perspectiveReferent": semantic_field("mention:m0"),
        "sourceReferent": semantic_field("mention:m0"),
        "polarity": semantic_field("POSITIVE"),
        "temporalRelation": semantic_field({"relation": "CURRENT", "anchorRef": "speech-time"}),
        "claimKind": semantic_field("REPORT"),
        "confidenceByField": confidence,
    }
    return text, mentions, table, claim


class InferenceV3Test(unittest.TestCase):
    def test_all_bio_groups_are_preserved(self):
        offsets = [[0, 1], [2, 3], [4, 5], [6, 7], [8, 9]]
        self.assertEqual([[0, 3], [6, 9]], inference_v3.groups_from_tags(offsets, [1, 2, 0, 1, 2]))

    def test_pointer_heads_select_roles_independently(self):
        values = ["ctx:speaker", "ctx:observer", "mention:m0", "mention:m1", "mention:m2", "NONE", "UNKNOWN"]
        selected = {
            "source": inference_v3.decode_pointer([0, 0, 1, 0, 0, 0, 0], values)["value"],
            "subject": inference_v3.decode_pointer([0, 0, 0, 1, 0, 0, 0], values)["value"],
            "target": inference_v3.decode_pointer([0, 0, 0, 0, 1, 0, 0], values)["value"],
            "owner": inference_v3.decode_pointer([0, 0, 0, 1, 0, 0, 0], values)["value"],
            "perspective": inference_v3.decode_pointer([0, 0, 1, 0, 0, 0, 0], values)["value"],
        }
        self.assertEqual(
            {"source": "mention:m0", "subject": "mention:m1", "target": "mention:m2",
             "owner": "mention:m1", "perspective": "mention:m0"},
            selected,
        )

    def test_pointer_ambiguity_abstains_from_guessing(self):
        decoded = inference_v3.decode_pointer(
            [0.49, 0.48, 0.02, 0.01], ["mention:m0", "mention:m1", "NONE", "UNKNOWN"],
            ambiguity_margin=0.02,
        )
        self.assertEqual("UNKNOWN", decoded["value"])
        self.assertEqual("AMBIGUOUS", decoded["fieldStatus"])
        self.assertEqual(2, len(decoded["alternatives"]))

    def test_obsolete_role_values_are_rejected(self):
        with self.assertRaises(ValueError):
            inference_v3.decode_pointer([1.0], ["KNOWN_ENTITY"])

    def test_multi_entity_fixture_preserves_six_distinct_semantic_roles(self):
        text, mentions, table, claim = marco_fixture()
        output = inference_v3.build_matrix_output_v3(
            text=text,
            observation_source_id="synthetic:marco",
            context={"speaker": "player", "observer": "matrix"},
            mentions=mentions,
            candidate_table=table,
            raw_claims=[claim],
        )
        observed = output["claims"][0]
        self.assertEqual("mention:m0", observed["sourceReferent"]["value"])
        self.assertEqual("mention:m1", observed["subjectReferent"]["value"])
        self.assertEqual("mention:m2", observed["targetReferent"]["value"])
        self.assertEqual("mention:m1", observed["ownerReferent"]["value"])
        self.assertEqual("mention:m0", observed["perspectiveReferent"]["value"])
        self.assertEqual("RESOLVED", observed["interpretationStatus"])

    def test_negation_cues_do_not_determine_polarity(self):
        _, _, table, claim = marco_fixture()
        claim["negationCueSpans"] = [[0, 5], [6, 10]]
        claim["polarity"] = semantic_field("POSITIVE")
        validated = inference_v3.validate_claim_v3(
            claim, text_length=38,
            candidate_ids=[item["candidateId"] for item in table["candidates"]],
            claim_ids=["c0"],
        )
        self.assertEqual(2, len(validated["negationCueSpans"]))
        self.assertEqual("POSITIVE", validated["polarity"]["value"])

    def test_relative_temporal_relation_requires_anchor(self):
        text, _, table, claim = marco_fixture()
        claim["temporalRelation"] = semantic_field({"relation": "AFTER", "anchorRef": None})
        invalid = inference_v3.validate_claim_v3(
            claim, text_length=len(text),
            candidate_ids=[item["candidateId"] for item in table["candidates"]], claim_ids=["c0"],
        )
        self.assertEqual("INVALID", invalid["structuralStatus"])
        self.assertEqual("ABSTAINED", invalid["interpretationStatus"])

        claim["temporalEvidence"] = [{"temporalId": "t0", "span": [6, 10]}]
        claim["temporalRelation"] = semantic_field({"relation": "AFTER", "anchorRef": "temporal:t0"})
        valid = inference_v3.validate_claim_v3(
            claim, text_length=len(text),
            candidate_ids=[item["candidateId"] for item in table["candidates"]], claim_ids=["c0"],
        )
        self.assertEqual("VALID", valid["structuralStatus"])

    def test_low_critical_token_confidence_can_abstain(self):
        text, _, table, claim = marco_fixture()
        claim["confidenceByField"]["negationCueSpans"] = 0.2
        validated = inference_v3.validate_claim_v3(
            claim, text_length=len(text),
            candidate_ids=[item["candidateId"] for item in table["candidates"]], claim_ids=["c0"],
            confidence_thresholds={"negationCueSpans": 0.5},
        )
        self.assertEqual("VALID", validated["structuralStatus"])
        self.assertEqual("ABSTAINED", validated["interpretationStatus"])
        self.assertLessEqual(validated["overallInterpretationConfidence"], 0.2)

    def test_v3_output_contains_no_downstream_ownership(self):
        text, mentions, table, claim = marco_fixture()
        output = inference_v3.build_matrix_output_v3(
            text=text, observation_source_id="synthetic", context={"speaker": "s", "observer": "o"},
            mentions=mentions, candidate_table=table, raw_claims=[claim],
        )
        serialized_keys = set()
        def collect(value):
            if isinstance(value, dict):
                serialized_keys.update(value)
                for child in value.values(): collect(child)
            elif isinstance(value, list):
                for child in value: collect(child)
        collect(output)
        self.assertFalse(serialized_keys & contract_v3.FORBIDDEN_OUTPUT_FIELDS)

    def test_flat_multi_claim_output_preserves_both_claims(self):
        text = "I lived in Venice, now I live in Milan."
        venice = [text.index("Venice"), text.index("Venice") + len("Venice")]
        milan = [text.index("Milan"), text.index("Milan") + len("Milan")]
        mentions = referent_candidates.build_mentions(
            [{"span": venice, "type": "LOCATION"}, {"span": milan, "type": "LOCATION"}],
            len(text),
        )
        table = referent_candidates.build_candidate_table(
            text,
            mentions,
            {"speaker": "player", "observer": "matrix"},
            critical_spans=[venice, milan],
        )
        confidence = {
            name: 0.99 for name in (
                "boundary", "subjectSpans", "objectSpans", "negationCueSpans",
                "temporalEvidence", "entityMentionIds", "dialogueAct", "predicate",
                *contract_v3.ROLE_HEADS, "polarity", "temporalRelation", "claimKind",
            )
        }

        def claim(claim_id, source_span, object_span, mention_id, relation):
            return {
                "claimId": claim_id,
                "sourceSpan": source_span,
                "subjectSpans": [],
                "objectSpans": [object_span],
                "negationCueSpans": [],
                "temporalEvidence": [],
                "entityMentionIds": [mention_id],
                "dialogueAct": semantic_field("ASSERT"),
                "predicate": semantic_field("residence.place"),
                "subjectReferent": semantic_field("ctx:speaker"),
                "targetReferent": semantic_field("NONE"),
                "ownerReferent": semantic_field("ctx:speaker"),
                "perspectiveReferent": semantic_field("ctx:speaker"),
                "sourceReferent": semantic_field("ctx:speaker"),
                "polarity": semantic_field("POSITIVE"),
                "temporalRelation": semantic_field({"relation": relation, "anchorRef": "speech-time"}),
                "claimKind": semantic_field("DIRECT"),
                "confidenceByField": dict(confidence),
            }

        split = text.index("now")
        output = inference_v3.build_matrix_output_v3(
            text=text,
            observation_source_id="synthetic:multi-claim",
            context={"speaker": "player", "observer": "matrix"},
            mentions=mentions,
            candidate_table=table,
            raw_claims=[
                claim("c0", [0, split], venice, "m0", "PAST"),
                claim("c1", [split, len(text)], milan, "m1", "CURRENT"),
            ],
        )
        self.assertEqual(["c0", "c1"], [item["claimId"] for item in output["claims"]])
        self.assertEqual([[venice], [milan]], [item["objectSpans"] for item in output["claims"]])
        self.assertTrue(all(item["structuralStatus"] == "VALID" for item in output["claims"]))


if __name__ == "__main__":
    unittest.main()
