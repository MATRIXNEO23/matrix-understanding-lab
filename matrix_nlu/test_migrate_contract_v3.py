import unittest

import migrate_contract_v3


class MigrateContractV3Test(unittest.TestCase):
    def test_migration_is_fail_closed_for_unprovable_fields(self):
        row = {"id": "v2:1", "claims": [{
            "spans": {"negation": [0, 10]},
            "labels": {
                "dialogueAct": "HYPOTHESIS", "claimKind": "EXPLICIT",
                "subjectReferent": "KNOWN_ENTITY", "targetReferent": "SELF",
                "ownerReferent": "SUBJECT", "perspectiveReferent": "RECENT_ENTITY",
                "temporalRelation": "CURRENT",
            },
        }]}
        result = migrate_contract_v3.classify_v2_rows([row])
        self.assertEqual("NEEDS_REANNOTATION", result["rows"][0]["classification"])
        fields = result["rows"][0]["claims"][0]["fields"]
        self.assertEqual("NEEDS_REANNOTATION", fields["negationCueSpans"])
        self.assertEqual("NEEDS_REANNOTATION", fields["sourceReferent"])
        self.assertEqual("NEEDS_REANNOTATION", fields["subjectReferent"])
        self.assertFalse(result["canonicalPartitionsOpened"])

    def test_speaker_observer_can_migrate_but_source_cannot_be_invented(self):
        claim = {"spans": {"negation": None}, "labels": {
            "dialogueAct": "ASSERT", "claimKind": "HYPOTHESIS",
            "subjectReferent": "SPEAKER", "targetReferent": "OBSERVER",
            "ownerReferent": "SPEAKER", "perspectiveReferent": "OBSERVER",
            "temporalRelation": "PAST",
        }}
        result = migrate_contract_v3.classify_v2_claim(claim)
        self.assertEqual("DETERMINISTIC_MIGRATION", result["fields"]["subjectReferent"])
        self.assertEqual("NEEDS_REANNOTATION", result["fields"]["sourceReferent"])
        self.assertEqual("NEEDS_REANNOTATION", result["classification"])


if __name__ == "__main__":
    unittest.main()
