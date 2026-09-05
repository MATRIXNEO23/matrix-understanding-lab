"""Independent Matrix-NLU V3 gold normalization and structural scoring.

This module intentionally does not import or call the production V3 decoder or
validator.  Gold defects therefore cannot be mirrored automatically in predictions.
"""

from __future__ import annotations

from collections import Counter, defaultdict
from copy import deepcopy
from typing import Mapping, Sequence

from contract_v3 import (
    CONTRACT_VERSION,
    FIXED_SEQUENCE_LABELS,
    FORBIDDEN_ROLE_VALUES,
    POINTER_SPECIAL_VALUES,
    ROLE_HEADS,
)


SPAN_FIELDS = ("subjectSpans", "objectSpans", "negationCueSpans", "temporalEvidence", "entityMentionIds")
CATEGORICAL_FIELDS = ("dialogueAct", "predicate", "polarity", "claimKind")
STATUS_FIELDS = ("boundary",) + SPAN_FIELDS + CATEGORICAL_FIELDS + ROLE_HEADS + ("temporalRelation",)


def normalize_gold_v3(row: Mapping) -> dict:
    """Normalize authored V3 gold without using production decoding code."""
    if row.get("contractVersion") != CONTRACT_VERSION:
        raise ValueError("gold row is not MATRIX_NLU_CONTRACT_V3")
    text = row.get("text")
    if not isinstance(text, str):
        raise ValueError("gold text must be a string")
    candidates = {item["candidateId"] for item in row.get("referentCandidates", [])}
    claims = []
    for original in row.get("claims", []):
        claim = deepcopy(original)
        span = claim.get("sourceSpan")
        if not isinstance(span, list) or len(span) != 2 or not (0 <= span[0] < span[1] <= len(text)):
            raise ValueError("invalid gold sourceSpan")
        for head in CATEGORICAL_FIELDS:
            value = claim.get(head)
            if value not in FIXED_SEQUENCE_LABELS[head]:
                raise ValueError(f"invalid gold {head}: {value}")
        temporal = claim.get("temporalRelation")
        if not isinstance(temporal, Mapping) or temporal.get("relation") not in FIXED_SEQUENCE_LABELS["temporalRelation"]:
            raise ValueError("invalid gold temporalRelation")
        for role in ROLE_HEADS:
            value = claim.get(role)
            if value in FORBIDDEN_ROLE_VALUES or value not in candidates | set(POINTER_SPECIAL_VALUES):
                raise ValueError(f"invalid gold {role}: {value}")
        status_by_field = dict(claim.get("fieldStatusByField", {}))
        for name in ("boundary",) + SPAN_FIELDS:
            status_by_field.setdefault(name, "RESOLVED")
        for name in CATEGORICAL_FIELDS:
            status_by_field.setdefault(name, "UNKNOWN" if claim[name] == "UNKNOWN" else "RESOLVED")
        for role in ROLE_HEADS:
            status_by_field.setdefault(role, "UNKNOWN" if claim[role] == "UNKNOWN" else (
                "NOT_APPLICABLE" if claim[role] == "NONE" else "RESOLVED"
            ))
        status_by_field.setdefault(
            "temporalRelation",
            "UNKNOWN" if temporal["relation"] == "UNKNOWN" else "RESOLVED",
        )
        claim["fieldStatusByField"] = status_by_field
        claims.append(claim)
    return {
        "id": row.get("id"),
        "language": row.get("language"),
        "domain": row.get("domain", "general"),
        "claims": claims,
    }


def _prediction_value(claim: Mapping, name: str):
    value = claim.get(name)
    if isinstance(value, Mapping) and "value" in value:
        return value["value"]
    return value


def _temporal_prediction(claim: Mapping):
    value = _prediction_value(claim, "temporalRelation")
    return value if isinstance(value, Mapping) else {}


def score_v3_rows(gold_rows: Sequence[Mapping], predicted_outputs: Sequence[Mapping]) -> dict:
    if len(gold_rows) != len(predicted_outputs):
        raise ValueError("gold/prediction row count mismatch")
    counts = Counter()
    slice_counts = defaultdict(Counter)
    for raw_gold, prediction in zip(gold_rows, predicted_outputs):
        gold = normalize_gold_v3(raw_gold)
        if prediction.get("contractVersion") != CONTRACT_VERSION:
            raise ValueError("prediction contract mismatch")
        predicted_claims = prediction.get("claims", [])
        counts["rows"] += 1
        counts["goldClaims"] += len(gold["claims"])
        counts["predictedClaims"] += len(predicted_claims)
        if len(gold["claims"]) == len(predicted_claims):
            counts["claimCountExact"] += 1
        row_exact = len(gold["claims"]) == len(predicted_claims)
        key = f"{gold['language']}:{gold['domain']}"
        for expected, observed in zip(gold["claims"], predicted_claims):
            claim_exact = True
            for name in CATEGORICAL_FIELDS:
                counts["fields"] += 1
                slice_counts[key]["fields"] += 1
                if expected[name] == _prediction_value(observed, name):
                    counts["fieldExact"] += 1
                    slice_counts[key]["fieldExact"] += 1
                else:
                    claim_exact = False
            for role in ROLE_HEADS:
                counts["roleFields"] += 1
                slice_counts[key]["roleFields"] += 1
                actual = _prediction_value(observed, role)
                if expected[role] == actual:
                    counts["roleExact"] += 1
                    slice_counts[key]["roleExact"] += 1
                else:
                    claim_exact = False
                    if role == "ownerReferent":
                        counts["ownershipCorruptions"] += 1
                    if role == "sourceReferent":
                        counts["sourceCorruptions"] += 1
            for name in SPAN_FIELDS:
                counts["spanFields"] += 1
                if expected.get(name, []) == observed.get(name, []):
                    counts["spanExact"] += 1
                else:
                    claim_exact = False
            expected_temporal = expected["temporalRelation"]
            actual_temporal = _temporal_prediction(observed)
            counts["temporalFields"] += 2
            counts["temporalExact"] += int(expected_temporal.get("relation") == actual_temporal.get("relation"))
            counts["temporalExact"] += int(expected_temporal.get("anchorRef") == actual_temporal.get("anchorRef"))
            if expected_temporal != actual_temporal:
                claim_exact = False
            expected_status = expected.get("interpretationStatus", "RESOLVED")
            if expected_status == observed.get("interpretationStatus"):
                counts["statusExact"] += 1
            else:
                claim_exact = False
            observed_statuses = observed.get("fieldStatusByField", {})
            for name in STATUS_FIELDS:
                counts["fieldStatuses"] += 1
                if expected["fieldStatusByField"].get(name) == observed_statuses.get(name):
                    counts["fieldStatusExact"] += 1
                else:
                    claim_exact = False
            counts["claimsPaired"] += 1
            counts["claimExact"] += int(claim_exact)
            row_exact = row_exact and claim_exact
        counts["rowExact"] += int(row_exact)

    def ratio(numerator, denominator):
        return counts[numerator] / counts[denominator] if counts[denominator] else 0.0

    return {
        "rows": counts["rows"],
        "claimCountExact": ratio("claimCountExact", "rows"),
        "claimExact": ratio("claimExact", "claimsPaired"),
        "fieldExact": ratio("fieldExact", "fields"),
        "rolePointerExact": ratio("roleExact", "roleFields"),
        "spanGroupExact": ratio("spanExact", "spanFields"),
        "temporalExact": ratio("temporalExact", "temporalFields"),
        "fieldStatusExact": ratio("fieldStatusExact", "fieldStatuses"),
        "ownershipCorruptions": counts["ownershipCorruptions"],
        "sourceCorruptions": counts["sourceCorruptions"],
        "slices": {
            key: {
                "fieldExact": value["fieldExact"] / value["fields"] if value["fields"] else 0.0,
                "rolePointerExact": value["roleExact"] / value["roleFields"] if value["roleFields"] else 0.0,
            }
            for key, value in sorted(slice_counts.items())
        },
    }
