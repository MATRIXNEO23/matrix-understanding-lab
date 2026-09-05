"""Frozen Matrix-NLU V3 registry, schema constants and fail-closed metadata checks."""

from __future__ import annotations

import hashlib
import json
from typing import Any, Mapping


CONTRACT_VERSION = "MATRIX_NLU_CONTRACT_V3"
SCHEMA_VERSION = "3.0"
DEFAULT_MAX_REFERENT_CANDIDATES = 16

TOKEN_LABELS = {
    "boundary": ["O", "B-CLAIM", "I-CLAIM"],
    "object": ["O", "B-OBJECT", "I-OBJECT"],
    "subject": ["O", "B-SUBJECT", "I-SUBJECT"],
    "negation": ["O", "B-NEGATION_CUE", "I-NEGATION_CUE"],
    "temporal": ["O", "B-TEMPORAL", "I-TEMPORAL"],
    "entity": ["O", "B-PERSON", "I-PERSON", "B-LOCATION", "I-LOCATION"],
}

FIXED_SEQUENCE_LABELS = {
    "dialogueAct": ["ASSERT", "QUESTION", "REQUEST", "COMMAND", "CORRECT", "UNKNOWN"],
    "predicate": [
        "identity.name", "identity.age", "residence.place", "presence.reported",
        "preference.like", "work.role", "possession.has", "goal.object",
        "attribute.is", "consent.grant", "consent.refuse", "speech.unresolved",
    ],
    "polarity": ["POSITIVE", "NEGATIVE", "UNKNOWN"],
    "temporalRelation": [
        "ATEMPORAL", "CURRENT", "PAST", "FUTURE", "BEFORE", "AFTER",
        "DURING", "RECURRENT", "AT_REFERENCE", "UNKNOWN",
    ],
    "claimKind": ["DIRECT", "REPORT", "BELIEF", "HYPOTHESIS", "UNKNOWN"],
}

ROLE_HEADS = (
    "subjectReferent",
    "targetReferent",
    "ownerReferent",
    "perspectiveReferent",
    "sourceReferent",
)

TOKEN_HEADS = tuple(TOKEN_LABELS)
SEQUENCE_HEADS = (
    "dialogueAct",
    "predicate",
    "subjectReferent",
    "targetReferent",
    "ownerReferent",
    "perspectiveReferent",
    "sourceReferent",
    "polarity",
    "temporalRelation",
    "claimKind",
)

POINTER_SPECIAL_VALUES = ("NONE", "UNKNOWN")
CANDIDATE_KINDS = (
    "CONTEXT_SPEAKER",
    "CONTEXT_OBSERVER",
    "MENTION",
    "CONTEXT_ENTITY",
)
FIELD_STATUSES = ("RESOLVED", "UNKNOWN", "AMBIGUOUS", "NOT_APPLICABLE")
STRUCTURAL_STATUSES = ("VALID", "INVALID")
INTERPRETATION_STATUSES = ("RESOLVED", "AMBIGUOUS", "ABSTAINED")
ANCHOR_REQUIRED_RELATIONS = frozenset({"BEFORE", "AFTER", "DURING", "AT_REFERENCE"})
ANCHOR_KINDS = ("SPEECH_TIME", "CONTEXT_REFERENCE", "TEMPORAL_EVIDENCE", "CLAIM")

FORBIDDEN_ROLE_VALUES = frozenset({"SELF", "SUBJECT", "KNOWN_ENTITY", "RECENT_ENTITY"})
FORBIDDEN_OUTPUT_FIELDS = frozenset({
    "worldTruth", "memoryAdmission", "authority", "beliefConfidence",
    "persistentConsent", "persistentGoal", "relationshipState",
    "affectiveState", "behaviorDecision",
})


class ContractMismatchError(ValueError):
    """Raised before decoding when bundle metadata does not exactly match V3."""


def ids(vocabularies: Mapping[str, list[str]]) -> dict[str, dict[str, int]]:
    return {
        head: {label: index for index, label in enumerate(values)}
        for head, values in vocabularies.items()
    }


TOKEN_IDS = ids(TOKEN_LABELS)
FIXED_SEQUENCE_IDS = ids(FIXED_SEQUENCE_LABELS)


def contract_descriptor(max_referent_candidates: int = DEFAULT_MAX_REFERENT_CANDIDATES) -> dict:
    """Return the complete ordered, JSON-serializable fingerprint input."""
    if max_referent_candidates < 4:
        raise ValueError("maxReferentCandidates must leave room for reserved and mention candidates")
    return {
        "contractVersion": CONTRACT_VERSION,
        "schemaVersion": SCHEMA_VERSION,
        "maxReferentCandidates": int(max_referent_candidates),
        "tokenHeads": list(TOKEN_HEADS),
        "sequenceHeads": list(SEQUENCE_HEADS),
        "headTypes": {
            **{head: "TOKEN_BIO" for head in TOKEN_HEADS},
            **{head: "SEQUENCE_POINTER" for head in ROLE_HEADS},
            "dialogueAct": "SEQUENCE_CATEGORICAL",
            "predicate": "SEQUENCE_CATEGORICAL",
            "polarity": "SEQUENCE_CATEGORICAL",
            "temporalRelation": "SEQUENCE_RELATION_WITH_ANCHOR",
            "claimKind": "SEQUENCE_CATEGORICAL",
        },
        "tokenLabels": TOKEN_LABELS,
        "fixedSequenceLabels": FIXED_SEQUENCE_LABELS,
        "roleHeads": list(ROLE_HEADS),
        "pointerSpecialValues": list(POINTER_SPECIAL_VALUES),
        "candidateKinds": list(CANDIDATE_KINDS),
        "fieldStatuses": list(FIELD_STATUSES),
        "structuralStatuses": list(STRUCTURAL_STATUSES),
        "interpretationStatuses": list(INTERPRETATION_STATUSES),
        "temporalAnchorKinds": list(ANCHOR_KINDS),
    }


def contract_fingerprint(max_referent_candidates: int = DEFAULT_MAX_REFERENT_CANDIDATES) -> str:
    payload = json.dumps(
        contract_descriptor(max_referent_candidates),
        ensure_ascii=False,
        separators=(",", ":"),
        sort_keys=True,
    ).encode("utf-8")
    return hashlib.sha256(payload).hexdigest()


def bundle_contract_metadata(
    max_referent_candidates: int = DEFAULT_MAX_REFERENT_CANDIDATES,
) -> dict:
    descriptor = contract_descriptor(max_referent_candidates)
    return {**descriptor, "contractFingerprintSha256": contract_fingerprint(max_referent_candidates)}


def validate_bundle_contract(
    observed: Mapping[str, Any],
    max_referent_candidates: int | None = None,
) -> dict:
    """Fail closed on any contract, order, type, schema or fingerprint mismatch."""
    limit = int(observed.get("maxReferentCandidates", -1)) if max_referent_candidates is None else int(max_referent_candidates)
    expected = bundle_contract_metadata(limit)
    differences = [key for key, value in expected.items() if observed.get(key) != value]
    unexpected = sorted(set(observed) - set(expected))
    if differences or unexpected:
        details = ", ".join(differences + [f"unexpected:{key}" for key in unexpected])
        raise ContractMismatchError(f"V3 bundle contract mismatch: {details}")
    return expected


def assert_registry() -> None:
    if len(TOKEN_HEADS) != 6 or len(SEQUENCE_HEADS) != 10:
        raise AssertionError("V3 must contain exactly 6 token and 10 sequence heads")
    if len(set(TOKEN_HEADS + SEQUENCE_HEADS)) != 16:
        raise AssertionError("V3 head names must be unique")
    if "sourceReferent" not in ROLE_HEADS:
        raise AssertionError("sourceReferent must be an independent role head")
    for forbidden in FORBIDDEN_ROLE_VALUES:
        if forbidden in POINTER_SPECIAL_VALUES:
            raise AssertionError(f"obsolete role value retained: {forbidden}")
    if "HYPOTHESIS" in FIXED_SEQUENCE_LABELS["dialogueAct"]:
        raise AssertionError("HYPOTHESIS belongs only to claimKind")
    if "CORRECTION" in FIXED_SEQUENCE_LABELS["dialogueAct"]:
        raise AssertionError("the canonical dialogue act is CORRECT")


assert_registry()
