import json
import pathlib
import tempfile
import unittest

import build_dataset


class MatrixDatasetTest(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.rows = build_dataset.build_records()
        build_dataset.validate(cls.rows)

    def test_is_deterministic(self):
        again = build_dataset.build_records()
        self.assertEqual(
            json.dumps(self.rows, ensure_ascii=False, sort_keys=True),
            json.dumps(again, ensure_ascii=False, sort_keys=True),
        )

    def test_large_frozen_test_is_balanced(self):
        test = [x for x in self.rows if x["split"] == "test"]
        self.assertGreaterEqual(len(test), 1400)
        self.assertEqual({"it", "en", "es"}, {x["language"] for x in test})
        counts = {lang: sum(x["language"] == lang for x in test) for lang in ("it", "en", "es")}
        self.assertEqual(1, len(set(counts.values())))

    def test_contains_two_and_three_claim_inputs(self):
        widths = {len(x["claims"]) for x in self.rows}
        self.assertTrue({1, 2, 3} <= widths)

    def test_zero_world_truth_and_critical_coverage(self):
        labels = [c["labels"] for row in self.rows for c in row["claims"]]
        self.assertFalse(any(x["worldTruth"] for x in labels))
        predicates = {x["predicate"] for x in labels}
        self.assertTrue({"consent.grant", "consent.refuse", "residence.place",
                         "preference.like", "goal.object"} <= predicates)
        self.assertTrue(any(x["polarity"] == "NEGATIVE" for x in labels))
        self.assertTrue(any(x["dialogueAct"] == "HYPOTHESIS" for x in labels))

    def test_source_and_entity_spans_round_trip(self):
        for row in self.rows:
            for claim in row["claims"]:
                start, end = claim["spans"]["source"]
                self.assertTrue(row["text"][start:end].strip())
                for entity in claim["spans"]["entities"]:
                    a, b = entity["span"]
                    self.assertTrue(row["text"][a:b])

    def test_manifest_hashes_are_reproducible(self):
        with tempfile.TemporaryDirectory() as first, tempfile.TemporaryDirectory() as second:
            one = build_dataset.write(self.rows, pathlib.Path(first))
            two = build_dataset.write(self.rows, pathlib.Path(second))
            self.assertEqual(
                {k: v["sha256"] for k, v in one["files"].items()},
                {k: v["sha256"] for k, v in two["files"].items()},
            )


if __name__ == "__main__":
    unittest.main()
