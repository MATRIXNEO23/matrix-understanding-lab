import json
import pathlib
import tempfile
import unittest

from audit_dataset_contract import audit, has_critical_findings, negation_shape


def row(row_id, split, source_kind, negation, *, language="it"):
    text = "non amo la pioggia"
    return {
        "id": row_id, "split": split, "language": language, "text": text,
        "provenance": {"kind": source_kind},
        "claims": [{
            "labels": {"predicate": "preference.like", "polarity": "NEGATIVE",
                       "temporalRelation": "ATEMPORAL"},
            "spans": {"source": [0, len(text)], "object": [9, len(text)],
                      "subject": None, "negation": negation, "temporal": None,
                      "entities": []},
        }],
    }


def write_rows(path, rows):
    path.write_text("".join(json.dumps(value) + "\n" for value in rows),
                    encoding="utf-8")


class DatasetContractAuditTest(unittest.TestCase):
    def test_classifies_full_and_cue_scope_without_language_rules(self):
        full = row("full", "dev", "GOLD", [0, len("non amo la pioggia")])["claims"][0]
        cue = row("cue", "train", "GENERATED", [0, 3])["claims"][0]
        self.assertEqual("FULL_SOURCE", negation_shape(full))
        self.assertEqual("DISJOINT_FROM_OBJECT", negation_shape(cue))

    def test_reports_cross_source_negation_contract_conflict(self):
        with tempfile.TemporaryDirectory() as directory:
            root = pathlib.Path(directory)
            train = root / "train.jsonl"
            dev = root / "dev.jsonl"
            write_rows(train, [row("cue", "train", "GENERATED", [0, 3])])
            write_rows(dev, [row("full", "dev", "GOLD", [0, len("non amo la pioggia")])])
            result = audit([("generated-train", train), ("gold-dev", dev)])
        self.assertTrue(result["decisionRequired"])
        self.assertIn("NEGATION_SCOPE_CONVENTION_CONFLICT",
                      {item["kind"] for item in result["contractConflicts"]})
        self.assertFalse(result["scope"]["frozenTestRead"])
        self.assertEqual(0, result["semanticSpanContainment"]["failureCount"])
        self.assertTrue(has_critical_findings(result))
        self.assertEqual(1, result["exactInputAnnotationConflicts"]["count"])

    def test_rejects_frozen_test_rows(self):
        with tempfile.TemporaryDirectory() as directory:
            path = pathlib.Path(directory) / "forbidden.jsonl"
            write_rows(path, [row("test", "test", "FROZEN", [0, len("non amo la pioggia")])])
            with self.assertRaisesRegex(ValueError, "forbidden split"):
                audit([("must-not-read", path)])

    def test_output_is_deterministic(self):
        with tempfile.TemporaryDirectory() as directory:
            path = pathlib.Path(directory) / "dev.jsonl"
            write_rows(path, [row("full", "dev", "GOLD", [0, len("non amo la pioggia")])])
            first = audit([("dev", path)])
            second = audit([("dev", path)])
        self.assertEqual(first, second)
        self.assertFalse(has_critical_findings(first))

    def test_context_distinguishes_otherwise_identical_inputs(self):
        with tempfile.TemporaryDirectory() as directory:
            root = pathlib.Path(directory)
            first_path, second_path = root / "first.jsonl", root / "second.jsonl"
            first = row("first", "train", "A", [0, 3])
            second = row("second", "dev", "B", [0, len("non amo la pioggia")])
            first["context"] = {"speaker": "PLAYER"}
            second["context"] = {"speaker": "NPC"}
            write_rows(first_path, [first])
            write_rows(second_path, [second])
            result = audit([("first", first_path), ("second", second_path)])
        self.assertEqual(0, result["exactInputAnnotationConflicts"]["count"])


if __name__ == "__main__":
    unittest.main()
