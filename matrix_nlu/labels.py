"""Stable label vocabularies for the Matrix-NLU multi-task heads."""

SEQUENCE_LABELS = {
    "dialogueAct": ["ASSERT", "CORRECT", "QUESTION", "REQUEST", "HYPOTHESIS", "UNKNOWN"],
    "predicate": [
        "identity.name", "identity.age", "residence.place", "presence.reported",
        "preference.like", "work.role", "possession.has", "goal.object",
        "attribute.is", "consent.grant", "consent.refuse", "speech.unresolved",
    ],
    "subjectReferent": ["SPEAKER", "OBSERVER", "KNOWN_ENTITY", "RECENT_ENTITY", "UNKNOWN"],
    "targetReferent": ["NONE", "SELF", "SPEAKER", "OBSERVER", "KNOWN_ENTITY", "RECENT_ENTITY", "UNKNOWN"],
    "ownerReferent": ["SUBJECT", "SPEAKER", "OBSERVER", "KNOWN_ENTITY", "RECENT_ENTITY", "UNKNOWN"],
    "perspectiveReferent": ["SPEAKER", "SUBJECT", "OBSERVER", "KNOWN_ENTITY", "RECENT_ENTITY", "UNKNOWN"],
    "polarity": ["POSITIVE", "NEGATIVE", "UNKNOWN"],
    "temporalRelation": ["ATEMPORAL", "CURRENT", "PAST", "FUTURE", "UNKNOWN"],
    "claimKind": ["EXPLICIT", "HYPOTHESIS"],
}

TOKEN_LABELS = {
    "boundary": ["O", "B-CLAIM", "I-CLAIM"],
    "object": ["O", "B-OBJECT", "I-OBJECT"],
    "subject": ["O", "B-SUBJECT", "I-SUBJECT"],
    "negation": ["O", "B-NEGATION", "I-NEGATION"],
    "temporal": ["O", "B-TEMPORAL", "I-TEMPORAL"],
    "entity": ["O", "B-PERSON", "I-PERSON", "B-LOCATION", "I-LOCATION"],
}


def ids(vocabularies):
    return {head: {label: index for index, label in enumerate(values)}
            for head, values in vocabularies.items()}


SEQUENCE_IDS = ids(SEQUENCE_LABELS)
TOKEN_IDS = ids(TOKEN_LABELS)
