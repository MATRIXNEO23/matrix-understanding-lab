import unittest
import itertools

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

    def test_entity_referents_use_roles_and_context_without_surface_guessing(self):
        context = {"speaker": "PLAYER", "observer": "luna",
                   "knownEntities": {"Marco": "npc:marco"},
                   "recentEntityRefs": ["npc:recent"]}
        raw = {"labels": {"subjectReferent": "SPEAKER", "ownerReferent": "SUBJECT",
                "perspectiveReferent": "SPEAKER", "targetReferent": "NONE",
                "dialogueAct": "ASSERT", "predicate": "identity.name",
                "polarity": "POSITIVE", "temporalRelation": "ATEMPORAL",
                "claimKind": "EXPLICIT"},
               "spans": {"source": [0, 31], "subject": None, "object": [11, 17],
                         "negation": None, "temporal": None,
                         "entities": [{"span": [11, 17], "type": "PERSON"},
                                      {"span": [25, 31], "type": "LOCATION"}]},
               "confidence": 0.95}
        claim = inference.validate_claim(raw, "mi chiamo Andrea e vivo a Madrid",
                                         context, "obs:entities", 0.7)
        self.assertEqual([
            {"span": [11, 17], "type": "PERSON", "referent": "SPEAKER"},
            {"span": [25, 31], "type": "LOCATION", "referent": "LOCATION"},
        ], claim["entities"])

        raw["labels"]["predicate"] = "work.role"
        raw["spans"]["source"] = [0, 24]
        raw["spans"]["object"] = [18, 24]
        raw["spans"]["entities"] = [{"span": [0, 5], "type": "PERSON"}]
        known = inference.validate_claim(raw, "Marco lavora come medico", context,
                                         "obs:known", 0.7)
        self.assertEqual("KNOWN_ENTITY", known["entities"][0]["referent"])

    def test_unbound_person_entity_is_explicitly_unknown(self):
        context = {"speaker": "PLAYER", "observer": "luna",
                   "knownEntities": {}, "recentEntityRefs": []}
        raw = {"labels": {"subjectReferent": "SPEAKER", "ownerReferent": "SUBJECT",
                "perspectiveReferent": "SPEAKER", "targetReferent": "NONE",
                "dialogueAct": "ASSERT", "predicate": "attribute.is",
                "polarity": "POSITIVE", "temporalRelation": "CURRENT",
                "claimKind": "EXPLICIT"},
               "spans": {"source": [0, 15], "subject": None, "object": [10, 15],
                         "negation": None, "temporal": None,
                         "entities": [{"span": [0, 5], "type": "PERSON"}]},
               "confidence": 0.95}
        claim = inference.validate_claim(raw, "Paolo sembra calmo", context,
                                         "obs:unknown", 0.7)
        self.assertEqual("UNKNOWN", claim["entities"][0]["referent"])

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
        self.assertEqual("ABSTAINED_LOW_CONFIDENCE", claim["status"])
        self.assertEqual("speech.unresolved", claim["predicate"])
        self.assertEqual(["obs:3"], claim["sourceIds"])
        self.assertEqual("NO_ADMISSION", claim["memoryAdmission"])

    def test_low_confidence_property_never_admits_or_promotes_world_truth(self):
        context = {"speaker": "PLAYER", "observer": "luna",
                   "knownEntities": {"Marco": "npc:marco"},
                   "recentEntityRefs": ["npc:recent"]}
        subject_values = ("SPEAKER", "OBSERVER", "KNOWN_ENTITY", "RECENT_ENTITY", "UNKNOWN")
        owner_values = ("SUBJECT", "SPEAKER", "OBSERVER", "KNOWN_ENTITY",
                        "RECENT_ENTITY", "UNKNOWN")
        perspective_values = ("SPEAKER", "SUBJECT", "OBSERVER", "KNOWN_ENTITY",
                              "RECENT_ENTITY", "UNKNOWN")
        for subject, owner, perspective in itertools.product(
                subject_values, owner_values, perspective_values):
            raw = {"labels": {"subjectReferent": subject, "ownerReferent": owner,
                    "perspectiveReferent": perspective, "targetReferent": "NONE",
                    "dialogueAct": "ASSERT", "predicate": "residence.place",
                    "polarity": "POSITIVE", "temporalRelation": "CURRENT",
                    "claimKind": "EXPLICIT"},
                   "spans": {"source": [0, 19], "subject": [0, 5], "object": [13, 19],
                             "negation": None, "temporal": None, "entities": []},
                   "confidence": 0.1}
            claim = inference.validate_claim(raw, "Marco vive a Madrid", context,
                                             "obs:property", 0.7)
            self.assertFalse(claim["worldTruth"])
            self.assertNotEqual("VALID", claim["status"])
            self.assertIn(claim["memoryAdmission"], {"NO_ADMISSION", "REJECT"})

    def test_invalid_source_spans_are_always_rejected(self):
        context = {"speaker": "PLAYER", "observer": "luna",
                   "knownEntities": {}, "recentEntityRefs": []}
        for span in ([-1, 3], [0, 0], [0, 99], [8, 4]):
            raw = {"labels": {}, "spans": {"source": span}, "confidence": 1.0}
            claim = inference.validate_claim(raw, "testo", context, "obs:bad", 0.7)
            self.assertEqual("REJECTED_INVARIANT", claim["status"])
            self.assertEqual("REJECT", claim["memoryAdmission"])
            self.assertFalse(claim["worldTruth"])


if __name__ == "__main__":
    unittest.main()
