import unittest

import student5_deep_pruning as pruning


class Student5DeepPruningContractTest(unittest.TestCase):
    def test_required_targets_are_present(self):
        self.assertEqual((40000, 60000, 80000, 100000), pruning.TARGETS)

    def test_phase_a_gate_is_stricter_than_student4_size(self):
        self.assertLess(pruning.GATE["maxEstimatedInt8Bytes"],
                        pruning.STUDENT4_MIXED_BYTES)

    def test_mapping_keeps_special_ids_and_mask(self):
        selected = list(range(4, 39999))
        mapping = pruning.new_to_old_mapping(40000, selected)
        self.assertEqual([0, 1, 2, 3], mapping[:4])
        self.assertEqual(250001, mapping[-1])
        self.assertEqual(40000, len(mapping))

    def test_probe_has_all_required_slices(self):
        rows = pruning.probes()
        self.assertTrue({"it", "en", "es", "code_switch"} <=
                        {row["language"] for row in rows})
        self.assertTrue(any(row["domain"] == "adult_intimacy" for row in rows))
        categories = {row["category"] for row in rows}
        self.assertTrue({"negation", "request", "correction", "temporal",
                         "ownership", "third_party", "names_locations",
                         "consent_boundary", "anatomy", "slang"} <= categories)

    def test_contrasts_cover_adult_and_general_semantics(self):
        identifiers = {pair["id"] for pair in pruning.contrast_pairs()}
        self.assertTrue(any(name.startswith("adult-consent-refusal") for name in identifiers))
        self.assertTrue(any(name.startswith("negation-") for name in identifiers))
        self.assertTrue(any(name.startswith("third-party-") for name in identifiers))

    def test_status_does_not_authorize_teaching_or_quantization(self):
        source = pruning.__doc__
        self.assertIn("No Matrix head", source)
        self.assertIn("No quantization", source)


if __name__ == "__main__":
    unittest.main()
