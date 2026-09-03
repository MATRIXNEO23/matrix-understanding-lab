import json
import pathlib
import tempfile
import unittest

import audit_dataset_v2
import build_dataset_v2


ROOT = pathlib.Path(__file__).resolve().parents[1]


class DatasetV2Test(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.output = tempfile.TemporaryDirectory()
        cls.data_dir = pathlib.Path(cls.output.name)
        records, mapping = build_dataset_v2.build(ROOT / "gold/p05-gold-v1.json")
        manifests = {source: build_dataset_v2.write_dataset(
            records[source], cls.data_dir, f"{source}-v2",
            build_dataset_v2.V1_HASHES[source]) for source in ("matrix", "p05")}
        mapping["v2Files"] = {source: manifest["files"]
                              for source, manifest in manifests.items()}
        (cls.data_dir / "v1-to-v2-corrections.json").write_text(
            json.dumps(mapping, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")
        cls.records = records
        cls.mapping = mapping
        cls.audit = audit_dataset_v2.audit(cls.data_dir)

    @classmethod
    def tearDownClass(cls):
        cls.output.cleanup()

    def test_v1_hashes_are_reconstructed_without_writing_v1_files(self):
        self.assertEqual(build_dataset_v2.V1_HASHES,
                         self.mapping["immutableV1HashesVerified"])
        self.assertFalse(any(self.data_dir.glob("matrix-train.jsonl")))
        self.assertFalse(any(self.data_dir.glob("p05-test.jsonl")))

    def test_v2_audit_is_fully_green(self):
        self.assertEqual("PASS", self.audit["status"], self.audit["failures"])
        self.assertEqual({
            "contradictoryExactInputCount": 0,
            "crossSplitExactSurfaceCount": 0,
            "crossSplitSemanticTemplateCount": 0,
            "failureCount": 0,
        }, self.audit["invariants"])
        self.assertFalse(self.audit["frozenPredictionsRead"])
        self.assertFalse(self.audit["frozenDataUsedForTuning"])

    def test_negation_and_implicit_subject_are_canonical(self):
        for rows in self.records.values():
            for row in rows:
                for claim in row["claims"]:
                    labels, spans = claim["labels"], claim["spans"]
                    self.assertEqual(spans["source"] if labels["polarity"] == "NEGATIVE"
                                     else None, spans["negation"])
                    if labels["subjectReferent"] == "SPEAKER":
                        self.assertIsNone(spans["subject"])

    def test_explicit_generated_temporal_phrases_are_spanned(self):
        observed = set()
        for rows in self.records.values():
            for row in rows:
                for claim in row["claims"]:
                    if claim["annotationPolicy"]["temporalSurface"] == "EXPLICIT":
                        span = claim["spans"]["temporal"]
                        observed.add(row["text"][span[0]:span[1]].casefold())
        for expressions in build_dataset_v2.EXPLICIT_TEMPORAL_EXPRESSIONS.values():
            self.assertTrue(set(expressions) & observed)

    def test_migration_records_corrections_and_partition_drops(self):
        self.assertGreater(self.mapping["counts"]["claimCorrections"], 0)
        self.assertGreater(self.mapping["counts"]["partitionDrops"], 0)
        self.assertEqual(24, self.mapping["counts"]["trainAdditions"])
        reasons = {item["reason"] for item in self.mapping["partitionDrops"]}
        self.assertEqual({"DEV_TOO_CLOSE_TO_FROZEN_TEST",
                          "TRAIN_TOO_CLOSE_TO_HELD_OUT"}, reasons)

    def test_target_languages_remain_present_and_balanced(self):
        for rows in self.records.values():
            for split in ("train", "dev", "test"):
                counts = {language: sum(row["split"] == split and
                                        row["language"] == language for row in rows)
                          for language in ("it", "en", "es")}
                self.assertTrue(all(counts.values()), (split, counts))
                self.assertLessEqual(max(counts.values()) - min(counts.values()), 2,
                                     (split, counts))


if __name__ == "__main__":
    unittest.main()
