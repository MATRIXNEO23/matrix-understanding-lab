import copy
import unittest

import contract_v3
import export_onnx_v3
import model_v3
import referent_candidates


class _Config:
    hidden_size = 384


class _LayerParent:
    def __init__(self):
        self.layer = [object() for _ in range(12)]


class _FakeBert:
    def __init__(self):
        self.config = _Config()
        self.encoder = _LayerParent()


class ContractV3CoreTest(unittest.TestCase):
    def test_frozen_registry_is_exactly_six_plus_ten(self):
        self.assertEqual(6, len(contract_v3.TOKEN_HEADS))
        self.assertEqual(10, len(contract_v3.SEQUENCE_HEADS))
        self.assertEqual(16, len(set(contract_v3.TOKEN_HEADS + contract_v3.SEQUENCE_HEADS)))
        self.assertIn("sourceReferent", contract_v3.SEQUENCE_HEADS)
        self.assertNotIn("HYPOTHESIS", contract_v3.FIXED_SEQUENCE_LABELS["dialogueAct"])
        self.assertEqual(
            ["DIRECT", "REPORT", "BELIEF", "HYPOTHESIS", "UNKNOWN"],
            contract_v3.FIXED_SEQUENCE_LABELS["claimKind"],
        )

    def test_negation_and_temporal_registries_match_freeze(self):
        self.assertEqual(
            ["O", "B-NEGATION_CUE", "I-NEGATION_CUE"],
            contract_v3.TOKEN_LABELS["negation"],
        )
        self.assertEqual(
            ["ATEMPORAL", "CURRENT", "PAST", "FUTURE", "BEFORE", "AFTER",
             "DURING", "RECURRENT", "AT_REFERENCE", "UNKNOWN"],
            contract_v3.FIXED_SEQUENCE_LABELS["temporalRelation"],
        )

    def test_contract_fingerprint_is_deterministic_and_sensitive(self):
        first = contract_v3.bundle_contract_metadata()
        second = contract_v3.bundle_contract_metadata()
        self.assertEqual(first, second)
        self.assertEqual(64, len(first["contractFingerprintSha256"]))
        changed = copy.deepcopy(first)
        changed["tokenHeads"] = list(reversed(changed["tokenHeads"]))
        with self.assertRaises(contract_v3.ContractMismatchError):
            contract_v3.validate_bundle_contract(changed)

    def test_bundle_validation_rejects_unknown_or_obsolete_registry(self):
        metadata = contract_v3.bundle_contract_metadata()
        metadata["pointerSpecialValues"] = ["NONE", "SELF", "UNKNOWN"]
        with self.assertRaises(contract_v3.ContractMismatchError):
            contract_v3.validate_bundle_contract(metadata)

    def test_student5_bert_adapter_reads_bert_structure(self):
        encoder = _FakeBert()
        self.assertEqual(384, model_v3.encoder_hidden_size(encoder))
        self.assertEqual(12, model_v3.encoder_layer_count(encoder))
        parent, attribute, layers = model_v3.encoder_layer_container(encoder)
        self.assertIs(parent, encoder.encoder)
        self.assertEqual("layer", attribute)
        self.assertEqual(12, len(layers))

    def test_v3_head_parameter_estimate_is_exact_and_small(self):
        summary = model_v3.head_parameter_estimate(384)
        self.assertEqual(171704, summary["totalV3Heads"])
        self.assertEqual(686816, summary["estimatedFp32Bytes"])
        self.assertLess(summary["estimatedFp32Bytes"], 1024 * 1024)

    def test_mentions_and_candidate_order_are_deterministic(self):
        text = "Marco told me that Anna loves Luca."
        spans = [
            {"span": [text.index("Luca"), text.index("Luca") + 4], "type": "PERSON"},
            {"span": [0, 5], "type": "PERSON"},
            {"span": [text.index("Anna"), text.index("Anna") + 4], "type": "PERSON"},
        ]
        mentions = referent_candidates.build_mentions(spans, len(text))
        self.assertEqual(["m0", "m1", "m2"], [item["mentionId"] for item in mentions])
        table = referent_candidates.build_candidate_table(
            text, mentions, {"speaker": "player", "observer": "npc"},
            critical_spans=[item["span"] for item in mentions],
        )
        self.assertEqual(
            ["ctx:speaker", "ctx:observer", "mention:m0", "mention:m1", "mention:m2"],
            [item["candidateId"] for item in table["candidates"]],
        )
        self.assertFalse(table["requiredCandidateLost"])
        self.assertEqual("UNKNOWN", referent_candidates.pointer_values(table)[-1])

    def test_candidate_overflow_reports_lost_critical_instead_of_hiding_it(self):
        text = "A B C D E"
        spans = [{"span": [i, i + 1], "type": "PERSON"} for i in (0, 2, 4, 6, 8)]
        mentions = referent_candidates.build_mentions(spans, len(text))
        table = referent_candidates.build_candidate_table(
            text, mentions, {"speaker": "s", "observer": "o"},
            critical_spans=[item["span"] for item in mentions], max_candidates=4,
        )
        self.assertTrue(table["overflow"])
        self.assertTrue(table["requiredCandidateLost"])
        self.assertGreater(len(table["lostCriticalCandidateIds"]), 0)

    def test_onnx_structural_contract_has_all_sixteen_outputs(self):
        spec = export_onnx_v3.structural_export_spec()
        self.assertEqual(16, len(spec["outputs"]))
        self.assertIn("sequence.sourceReferent", spec["outputs"])
        self.assertEqual([], spec["customOperators"])


if __name__ == "__main__":
    unittest.main()
