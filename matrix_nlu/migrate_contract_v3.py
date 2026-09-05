"""Fail-closed V2 -> V3 migration classification.

This module accepts rows supplied explicitly by a caller.  It never discovers or
opens canonical TRAIN/DEV/Frozen paths and does not invent missing V3 semantics.
"""

from __future__ import annotations

from collections import Counter
from typing import Mapping, Sequence


MIGRATION_CLASSES = ("DIRECT_REUSE", "DETERMINISTIC_MIGRATION", "NEEDS_REANNOTATION", "UNUSABLE")


def classify_v2_claim(claim: Mapping) -> dict:
    labels = claim.get("labels", {})
    spans = claim.get("spans", {})
    fields = {
        "boundary/object/subject/temporal/entity spans": "DIRECT_REUSE",
        "speaker/observer context IDs": "DETERMINISTIC_MIGRATION",
        "sourceReferent": "NEEDS_REANNOTATION",
        "field status/confidence": "NEEDS_REANNOTATION",
    }
    negation = spans.get("negation")
    fields["negationCueSpans"] = "NEEDS_REANNOTATION" if negation is not None else "DETERMINISTIC_MIGRATION"
    for role in ("subjectReferent", "targetReferent", "ownerReferent", "perspectiveReferent"):
        value = labels.get(role)
        if value in {"SPEAKER", "OBSERVER"}:
            fields[role] = "DETERMINISTIC_MIGRATION"
        elif value in {"KNOWN_ENTITY", "RECENT_ENTITY", "SELF", "SUBJECT"}:
            fields[role] = "NEEDS_REANNOTATION"
        else:
            fields[role] = "NEEDS_REANNOTATION"
    kind = labels.get("claimKind")
    fields["claimKind"] = "DETERMINISTIC_MIGRATION" if kind == "HYPOTHESIS" else "NEEDS_REANNOTATION"
    act = labels.get("dialogueAct")
    fields["dialogueAct"] = "NEEDS_REANNOTATION" if act == "HYPOTHESIS" else "DIRECT_REUSE"
    temporal = labels.get("temporalRelation")
    fields["temporalRelation"] = "DIRECT_REUSE" if temporal in {
        "ATEMPORAL", "CURRENT", "PAST", "FUTURE", "UNKNOWN"
    } else "NEEDS_REANNOTATION"
    severity = max((MIGRATION_CLASSES.index(value) for value in fields.values()), default=0)
    return {"classification": MIGRATION_CLASSES[severity], "fields": fields}


def classify_v2_rows(rows: Sequence[Mapping]) -> dict:
    results = []
    counts = Counter()
    for row in rows:
        claims = [classify_v2_claim(claim) for claim in row.get("claims", [])]
        severity = max((MIGRATION_CLASSES.index(item["classification"]) for item in claims), default=3)
        classification = MIGRATION_CLASSES[severity]
        counts[classification] += 1
        results.append({"rowId": row.get("id"), "classification": classification, "claims": claims})
    return {
        "provenance": "CALLER_SUPPLIED_ROWS_ONLY",
        "canonicalPartitionsOpened": False,
        "counts": {name: counts[name] for name in MIGRATION_CLASSES},
        "rows": results,
    }
