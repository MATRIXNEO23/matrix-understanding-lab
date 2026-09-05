import copy
import pathlib
import tempfile
import unittest

import contract_v3
import train_v3_migration as migration


def v2_row(text="Anna non vuole Luca domani"):
    def span(value):
        start = text.index(value)
        return [start, start + len(value)]
    return {
        "schemaVersion": "matrix.nlu.dataset.v2",
        "id": "train:multi-entity",
        "split": "train",
        "language": "it",
        "text": text,
        "context": {
            "speaker": "PLAYER", "observer": "luna",
            "knownEntities": {"Anna": {"type": "PERSON"}, "Luca": {"type": "PERSON"}},
            "recentEntityRefs": [],
        },
        "adultOnly": False,
        "provenance": {"kind": "TEST_ONLY"},
        "claims": [{
            "family": "synthetic",
            "labels": {
                "dialogueAct": "ASSERT", "predicate": "goal.object",
                "subjectReferent": "KNOWN_ENTITY", "targetReferent": "KNOWN_ENTITY",
                "ownerReferent": "SUBJECT", "perspectiveReferent": "SPEAKER",
                "polarity": "NEGATIVE", "temporalRelation": "FUTURE",
                "claimKind": "EXPLICIT", "worldTruth": False,
            },
            "spans": {
                "source": [0, len(text)], "subject": span("Anna"),
                "object": span("Luca"), "negation": [0, len(text)],
                "temporal": span("domani"),
                "entities": [
                    {"span": span("Anna"), "type": "PERSON", "referent": "PERSON"},
                    {"span": span("Luca"), "type": "PERSON", "referent": "PERSON"},
                ],
            },
        }],
    }


class TrainV3MigrationTest(unittest.TestCase):
    def test_multi_entity_roles_are_independent_and_source_is_explicit(self):
        row, record = migration.migrate_row(v2_row(), "test-train")
        labels = row["claims"][0]["labels"]
        self.assertEqual("mention:m0", labels["subjectReferent"])
        self.assertEqual("mention:m1", labels["targetReferent"])
        self.assertEqual("mention:m0", labels["ownerReferent"])
        self.assertEqual("ctx:speaker", labels["perspectiveReferent"])
        self.assertEqual("ctx:speaker", labels["sourceReferent"])
        self.assertEqual("REANNOTATED", record["finalDisposition"])

    def test_negation_cue_reannotation_does_not_reuse_full_scope(self):
        row, _ = migration.migrate_row(v2_row(), "test-train")
        text = row["text"]
        spans = row["claims"][0]["negationCueSpans"]
        self.assertEqual(["non"], [text[start:end] for start, end in spans])
        self.assertNotEqual([[0, len(text)]], spans)
        self.assertEqual("NEGATIVE", row["claims"][0]["labels"]["polarity"])

    def test_multiple_negation_cues_are_preserved(self):
        text = "Anna non dice che Luca non parte domani"
        row = v2_row(text)
        row["claims"][0]["spans"].update({
            "subject": [0, 4], "object": [18, 22], "negation": [0, len(text)],
            "temporal": [34, 40],
            "entities": [
                {"span": [0, 4], "type": "PERSON", "referent": "PERSON"},
                {"span": [18, 22], "type": "PERSON", "referent": "PERSON"},
            ],
        })
        migrated, _ = migration.migrate_row(row, "test-train")
        self.assertEqual(2, len(migrated["claims"][0]["negationCueSpans"]))

    def test_unknown_and_none_remain_distinct(self):
        row = v2_row()
        row["claims"][0]["labels"]["targetReferent"] = "NONE"
        migrated, _ = migration.migrate_row(row, "test-train")
        labels = migrated["claims"][0]["labels"]
        statuses = migrated["claims"][0]["fieldStatusByField"]
        self.assertEqual("NONE", labels["targetReferent"])
        self.assertEqual("NOT_APPLICABLE", statuses["targetReferent"])

        row["claims"][0]["labels"]["targetReferent"] = "UNKNOWN"
        migrated, _ = migration.migrate_row(row, "test-train")
        self.assertEqual("UNKNOWN", migrated["claims"][0]["labels"]["targetReferent"])
        self.assertEqual("UNKNOWN", migrated["claims"][0]["fieldStatusByField"]["targetReferent"])

    def test_forbidden_v2_sentinel_never_survives(self):
        migrated, _ = migration.migrate_row(v2_row(), "test-train")
        values = [migrated["claims"][0]["labels"][head] for head in contract_v3.ROLE_HEADS]
        self.assertFalse(any(value in contract_v3.FORBIDDEN_ROLE_VALUES for value in values))

    def test_temporal_evidence_and_speech_time_anchor_are_materialized(self):
        migrated, _ = migration.migrate_row(v2_row(), "test-train")
        claim = migrated["claims"][0]
        self.assertEqual("domani", migrated["text"][slice(*claim["temporalEvidence"][0]["span"])])
        self.assertEqual("speech-time", claim["labels"]["temporalRelation"]["anchorRef"])

    def test_multi_claim_spans_and_ids_are_preserved(self):
        row = v2_row()
        text = "Anna non vuole Luca domani e Anna vuole Luca ora"
        first = copy.deepcopy(row["claims"][0])
        second = copy.deepcopy(row["claims"][0])
        first["spans"]["source"] = [0, 28]
        second["spans"] = {
            "source": [31, len(text)], "subject": [31, 35], "object": [42, 46],
            "negation": None, "temporal": [47, 50],
            "entities": [
                {"span": [31, 35], "type": "PERSON", "referent": "PERSON"},
                {"span": [42, 46], "type": "PERSON", "referent": "PERSON"},
            ],
        }
        second["labels"]["polarity"] = "POSITIVE"
        row.update({"text": text, "claims": [first, second]})
        first["spans"]["entities"] = [
            {"span": [0, 4], "type": "PERSON", "referent": "PERSON"},
            {"span": [16, 20], "type": "PERSON", "referent": "PERSON"},
        ]
        migrated, _ = migration.migrate_row(row, "test-train")
        self.assertEqual(["c0", "c1"], [claim["claimId"] for claim in migrated["claims"]])
        self.assertEqual([[0, 28], [31, len(text)]], [claim["sourceSpan"] for claim in migrated["claims"]])

    def test_code_switch_adult_family_is_not_moderated(self):
        row = v2_row()
        row["text"] = "Voglio fare sexting con Luca domani"
        row["id"] = "adult-code-switch"
        row["adultOnly"] = True
        row["claims"][0]["family"] = "v22a_adult_it_english_term"
        row["claims"][0]["labels"].update({
            "subjectReferent": "SPEAKER", "targetReferent": "KNOWN_ENTITY",
            "ownerReferent": "SUBJECT", "polarity": "POSITIVE",
        })
        row["claims"][0]["spans"].update({
            "subject": None, "object": [12, 29], "negation": None,
            "temporal": [30, 36],
            "entities": [{"span": [24, 28], "type": "PERSON", "referent": "PERSON"}],
        })
        migrated, _ = migration.migrate_row(row, "test-train")
        self.assertEqual("code-switch", migrated["language"])
        self.assertFalse(set(migrated) & contract_v3.FORBIDDEN_OUTPUT_FIELDS)

    def test_validator_and_target_builder_accept_migrated_row(self):
        migrated, _ = migration.migrate_row(v2_row(), "test-train")
        self.assertEqual([], migration.validate_v3_row(migrated))
        gate = migration.target_builder_gate([migrated])
        self.assertEqual(1, gate["rowsBuildable"])
        self.assertEqual([], gate["errors"])

    def test_source_loader_refuses_non_train_names(self):
        with tempfile.TemporaryDirectory() as directory:
            path = pathlib.Path(directory) / "matrix-dev.jsonl"
            path.write_text("", encoding="utf-8")
            with self.assertRaises(ValueError):
                migration.load_train_jsonl(path, migration.sha256(path))

    def test_unique_implicit_known_role_is_not_first_mention_guessing(self):
        row = v2_row()
        row["claims"][0]["spans"]["subject"] = None
        row["claims"][0]["spans"]["entities"] = [
            {"span": [0, 4], "type": "PERSON", "referent": "PERSON"}
        ]
        row["claims"][0]["labels"]["targetReferent"] = "NONE"
        migrated, _ = migration.migrate_row(row, "test-train")
        self.assertEqual("mention:m0", migrated["claims"][0]["labels"]["subjectReferent"])

        row["claims"][0]["spans"]["entities"].append(
            {"span": [16, 20], "type": "PERSON", "referent": "PERSON"}
        )
        with self.assertRaises(migration.UnusableRow):
            migration.migrate_row(row, "test-train")

    def test_cross_language_duplicate_role_repair_is_explicit(self):
        row = v2_row()
        row["text"] = "No me gusta Marco ahora"
        row.update({"id": "mx-v22a-cross-001", "language": "es"})
        row["claims"][0]["labels"].update({
            "subjectReferent": "SPEAKER", "targetReferent": "NONE",
            "ownerReferent": "SUBJECT", "polarity": "POSITIVE",
            "predicate": "preference.like",
        })
        row["claims"][0]["spans"].update({
            "source": [0, len(row["text"])],
            "subject": None, "object": [12, 17], "negation": [0, len(row["text"])],
            "temporal": None, "entities": [],
        })
        migrated, record = migration.migrate_row(row, "test-train")
        labels = migrated["claims"][0]["labels"]
        self.assertEqual("NEGATIVE", labels["polarity"])
        self.assertEqual("mention:m0", labels["targetReferent"])
        self.assertIn("CONTROLLED_CROSS_LINGUAL_ROLE_REANNOTATION", record["reasonCodes"])

    def test_explicit_third_party_report_gets_independent_source(self):
        row = v2_row()
        row.update({"id": "mx-v22a-it-core-113", "text": "Giulia dice che non vuole venire a casa"})
        row["claims"][0]["labels"]["targetReferent"] = "NONE"
        row["claims"][0]["spans"].update({
            "source": [0, len(row["text"])], "subject": [0, 6],
            "object": [26, len(row["text"])], "negation": [0, len(row["text"])],
            "temporal": None,
            "entities": [{"span": [0, 6], "type": "PERSON", "referent": "PERSON"}],
        })
        migrated, record = migration.migrate_row(row, "test-train")
        labels = migrated["claims"][0]["labels"]
        self.assertEqual("REPORT", labels["claimKind"])
        self.assertEqual("mention:m0", labels["sourceReferent"])
        self.assertEqual("ctx:speaker", labels["perspectiveReferent"])
        self.assertNotEqual(labels["sourceReferent"], labels["perspectiveReferent"])
        self.assertIn("EXPLICIT_THIRD_PARTY_REPORT_REANNOTATION", record["reasonCodes"])


if __name__ == "__main__":
    unittest.main()
