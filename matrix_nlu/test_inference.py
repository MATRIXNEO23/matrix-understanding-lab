import unittest

import inference


class InferenceInvariantTest(unittest.TestCase):
    def test_groups_recover_two_claims_without_joiner(self):
        offsets = [(0, 2), (3, 5), (6, 7), (8, 12), (13, 17)]
        self.assertEqual([[0, 5], [8, 17]], inference.groups_from_tags(offsets, [1, 2, 0, 1, 2]))

    def test_known_entity_binds_only_from_supplied_context(self):
        context = {"speaker": "PLAYER", "observer": "luna",
                   "knownEntities": {"Marco": "npc:marco"}, "recentEntityRefs": []}
        raw = {"labels": {"subjectReferent": "KNOWN_ENTITY", "ownerReferent": "SUBJECT",
                "perspectiveReferent": "SPEAKER", "targetReferent": "NONE",
                "dialogueAct": "ASSERT", "predicate": "residence.place",
                "polarity": "POSITIVE", "temporalRelation": "CURRENT", "claimKind": "EXPLICIT"},
               "spans": {"source": [0, 19], "subject": [0, 5], "object": [13, 19],
                         "negation": None, "temporal": None, "entities": []}, "confidence": 0.95}
        claim = inference.validate_claim(raw, "Marco vive a Madrid", context, "obs:1", 0.7)
        self.assertEqual("npc:marco", claim["subject"])
        self.assertEqual("npc:marco", claim["owner"])
        self.assertFalse(claim["worldTruth"])

    def test_unknown_third_party_is_rejected_not_invented(self):
        context = {"speaker": "PLAYER", "observer": "luna",
                   "knownEntities": {}, "recentEntityRefs": []}
        raw = {"labels": {"subjectReferent": "KNOWN_ENTITY", "ownerReferent": "SUBJECT",
                "perspectiveReferent": "SPEAKER", "targetReferent": "NONE",
                "dialogueAct": "ASSERT", "predicate": "residence.place",
                "polarity": "POSITIVE", "temporalRelation": "CURRENT", "claimKind": "EXPLICIT"},
               "spans": {"source": [0, 19], "subject": [0, 5], "object": [13, 19],
                         "negation": None, "temporal": None, "entities": []}, "confidence": 0.95}
        claim = inference.validate_claim(raw, "Marco vive a Madrid", context, "obs:2", 0.7)
        self.assertEqual("REJECTED_INVARIANT", claim["status"])
        self.assertEqual("REJECT", claim["memoryAdmission"])
        self.assertFalse(claim["worldTruth"])

    def test_low_confidence_abstains_without_losing_provenance(self):
        context = {"speaker": "PLAYER", "observer": "luna",
                   "knownEntities": {}, "recentEntityRefs": []}
        raw = {"labels": {"subjectReferent": "SPEAKER", "ownerReferent": "SUBJECT",
                "perspectiveReferent": "SPEAKER", "targetReferent": "NONE",
                "dialogueAct": "ASSERT", "predicate": "preference.like",
                "polarity": "NEGATIVE", "temporalRelation": "ATEMPORAL", "claimKind": "EXPLICIT"},
               "spans": {"source": [0, 12], "subject": None, "object": [8, 12],
                         "negation": [0, 3], "temporal": None, "entities": []}, "confidence": 0.4}
        claim = inference.validate_claim(raw, "non amo caos", context, "obs:3", 0.7)
        self.assertEqual("speech.unresolved", claim["predicate"])
        self.assertEqual(["obs:3"], claim["sourceIds"])
        self.assertEqual("NO_ADMISSION", claim["memoryAdmission"])


if __name__ == "__main__":
    unittest.main()
