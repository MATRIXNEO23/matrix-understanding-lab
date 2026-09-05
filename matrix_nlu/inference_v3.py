"""Deterministic Matrix-NLU V3 decoding and invariant validation.

This module validates learned linguistic outputs.  It does not infer linguistic
meaning with regexes and it never makes authority, truth or persistence choices.
"""

from __future__ import annotations

import math
from typing import Iterable, Mapping, Sequence

from contract_v3 import (
    ANCHOR_REQUIRED_RELATIONS,
    CONTRACT_VERSION,
    FIELD_STATUSES,
    FIXED_SEQUENCE_LABELS,
    FORBIDDEN_OUTPUT_FIELDS,
    FORBIDDEN_ROLE_VALUES,
    POINTER_SPECIAL_VALUES,
    ROLE_HEADS,
)


def groups_from_tags(
    offsets: Sequence[Sequence[int]],
    tags: Sequence[int],
    begin_ids: Iterable[int] = (1,),
    inside_ids: Iterable[int] = (2,),
) -> list[list[int]]:
    """Return every valid BIO group; never silently select only the first."""
    begins, insides = set(begin_ids), set(inside_ids)
    groups: list[list[Sequence[int]]] = []
    current: list[Sequence[int]] = []
    for offset, tag in zip(offsets, tags):
        if len(offset) != 2 or offset[1] <= offset[0]:
            continue
        if tag in begins:
            if current:
                groups.append(current)
            current = [offset]
        elif tag in insides:
            if not current:
                current = [offset]
            else:
                current.append(offset)
        elif current:
            groups.append(current)
            current = []
    if current:
        groups.append(current)
    return [[int(group[0][0]), int(group[-1][1])] for group in groups]


def entity_spans(offsets: Sequence[Sequence[int]], tags: Sequence[int]) -> list[dict]:
    output = []
    for entity_type, begin, inside in (("PERSON", 1, 2), ("LOCATION", 3, 4)):
        for span in groups_from_tags(offsets, tags, (begin,), (inside,)):
            output.append({"span": span, "type": entity_type})
    return sorted(output, key=lambda item: (item["span"][0], item["span"][1], item["type"]))


def field(value, confidence: float, status: str | None = None, alternatives=None) -> dict:
    confidence = float(confidence)
    if not math.isfinite(confidence) or not 0.0 <= confidence <= 1.0:
        raise ValueError("field confidence must be finite and in [0, 1]")
    if status is None:
        status = "UNKNOWN" if value == "UNKNOWN" else (
            "NOT_APPLICABLE" if value == "NONE" else "RESOLVED"
        )
    if status not in FIELD_STATUSES:
        raise ValueError(f"invalid field status: {status}")
    output = {"value": value, "confidence": confidence, "fieldStatus": status}
    if alternatives:
        output["alternatives"] = list(alternatives)
    return output


def decode_pointer(
    probabilities: Sequence[float],
    pointer_values: Sequence[str],
    *,
    ambiguity_margin: float | None = None,
) -> dict:
    """Decode one role independently; optional margin is versioned caller config."""
    if len(probabilities) != len(pointer_values) or not probabilities:
        raise ValueError("pointer probabilities and values must have equal non-zero length")
    scored = sorted(
        [(float(score), str(value)) for score, value in zip(probabilities, pointer_values)],
        key=lambda item: (-item[0], item[1]),
    )
    if any(not math.isfinite(score) or score < 0.0 for score, _ in scored):
        raise ValueError("pointer probabilities must be finite and non-negative")
    best_score, best_value = scored[0]
    if best_value in FORBIDDEN_ROLE_VALUES:
        raise ValueError(f"forbidden V3 role value: {best_value}")
    if ambiguity_margin is not None and len(scored) > 1:
        second_score, second_value = scored[1]
        if best_value not in POINTER_SPECIAL_VALUES and second_value not in POINTER_SPECIAL_VALUES and best_score - second_score <= ambiguity_margin:
            return field(
                "UNKNOWN", best_score, "AMBIGUOUS",
                alternatives=[
                    {"value": best_value, "confidence": best_score},
                    {"value": second_value, "confidence": second_score},
                ],
            )
    return field(best_value, best_score)


def categorical_field(head: str, value: str, confidence: float) -> dict:
    labels = FIXED_SEQUENCE_LABELS[head]
    if value not in labels:
        raise ValueError(f"invalid {head} label: {value}")
    return field(value, confidence)


def _valid_span(span, text_length: int, source_span: Sequence[int] | None = None) -> bool:
    if not isinstance(span, (list, tuple)) or len(span) != 2:
        return False
    start, end = span
    if not isinstance(start, int) or not isinstance(end, int) or not (0 <= start < end <= text_length):
        return False
    return source_span is None or source_span[0] <= start < end <= source_span[1]


def _validate_non_overlapping_spans(spans, text_length: int, source_span) -> bool:
    if not isinstance(spans, list) or any(not _valid_span(span, text_length, source_span) for span in spans):
        return False
    ordered = sorted((span[0], span[1]) for span in spans)
    return all(left[1] <= right[0] for left, right in zip(ordered, ordered[1:]))


def _anchor_valid(value: Mapping, temporal_ids: set[str], claim_ids: set[str]) -> bool:
    relation = value.get("relation")
    anchor = value.get("anchorRef")
    if relation in ANCHOR_REQUIRED_RELATIONS:
        if not isinstance(anchor, str):
            return False
        if anchor in {"speech-time", "context-reference"}:
            return True
        if anchor.startswith("temporal:"):
            return anchor.split(":", 1)[1] in temporal_ids
        if anchor.startswith("claim:"):
            return anchor.split(":", 1)[1] in claim_ids
        return False
    return anchor is None or anchor in {"speech-time", "context-reference"}


def required_critical_fields(claim: Mapping) -> list[str]:
    names = [
        "boundary", "subjectSpans", "negationCueSpans", "entityMentionIds",
        "dialogueAct", "predicate", "subjectReferent", "ownerReferent",
        "perspectiveReferent", "sourceReferent", "polarity",
        "temporalRelation", "claimKind",
    ]
    target = claim.get("targetReferent", {}).get("value")
    if target != "NONE":
        names.append("targetReferent")
    if claim.get("objectSpans"):
        names.append("objectSpans")
    if claim.get("temporalEvidence"):
        names.append("temporalEvidence")
    return names


def validate_claim_v3(
    raw: Mapping,
    *,
    text_length: int,
    candidate_ids: Iterable[str],
    claim_ids: Iterable[str],
    confidence_thresholds: Mapping[str, float] | None = None,
) -> dict:
    """Validate one already-decoded claim and apply structural/confidence gates."""
    claim = dict(raw)
    diagnostics: list[str] = []
    source_span = claim.get("sourceSpan")
    if not _valid_span(source_span, text_length):
        diagnostics.append("invalid sourceSpan")
    for name in ("subjectSpans", "objectSpans", "negationCueSpans"):
        if not _validate_non_overlapping_spans(claim.get(name), text_length, source_span):
            diagnostics.append(f"invalid or overlapping {name}")
    temporal_evidence = claim.get("temporalEvidence")
    if not isinstance(temporal_evidence, list):
        diagnostics.append("temporalEvidence must be a list")
        temporal_evidence = []
    temporal_ids = set()
    for item in temporal_evidence:
        if not isinstance(item, Mapping) or not _valid_span(item.get("span"), text_length, source_span):
            diagnostics.append("invalid temporalEvidence span")
            continue
        temporal_id = str(item.get("temporalId", ""))
        if not temporal_id or temporal_id in temporal_ids:
            diagnostics.append("missing or duplicate temporalId")
        temporal_ids.add(temporal_id)

    candidate_set = set(candidate_ids)
    for role in ROLE_HEADS:
        role_field = claim.get(role)
        if not isinstance(role_field, Mapping):
            diagnostics.append(f"missing {role} field")
            continue
        value = role_field.get("value")
        if value in FORBIDDEN_ROLE_VALUES or value not in candidate_set | set(POINTER_SPECIAL_VALUES):
            diagnostics.append(f"invalid {role} pointer")

    for head in ("dialogueAct", "predicate", "polarity", "claimKind"):
        item = claim.get(head)
        if not isinstance(item, Mapping) or item.get("value") not in FIXED_SEQUENCE_LABELS[head]:
            diagnostics.append(f"invalid {head} field")
    temporal = claim.get("temporalRelation")
    if not isinstance(temporal, Mapping) or not isinstance(temporal.get("value"), Mapping):
        diagnostics.append("invalid temporalRelation field")
    else:
        temporal_value = temporal["value"]
        if temporal_value.get("relation") not in FIXED_SEQUENCE_LABELS["temporalRelation"]:
            diagnostics.append("invalid temporal relation label")
        elif not _anchor_valid(temporal_value, temporal_ids, set(claim_ids)):
            diagnostics.append("missing or invalid temporal anchor")

    confidence_by_field = claim.get("confidenceByField")
    if not isinstance(confidence_by_field, Mapping):
        diagnostics.append("missing confidenceByField")
        confidence_by_field = {}
    required = required_critical_fields(claim)
    required_confidences = []
    ambiguous = False
    low = []
    status_by_field = dict(claim.get("fieldStatusByField", {}))
    for name in ("boundary", "subjectSpans", "objectSpans", "negationCueSpans", "temporalEvidence", "entityMentionIds"):
        status_by_field.setdefault(name, "RESOLVED")
    for name in ("dialogueAct", "predicate", *ROLE_HEADS, "polarity", "temporalRelation", "claimKind"):
        item = claim.get(name)
        if isinstance(item, Mapping):
            status_by_field[name] = item.get("fieldStatus", "UNKNOWN")
    for name in required:
        item = claim.get(name)
        status = status_by_field.get(name)
        if status == "AMBIGUOUS":
            ambiguous = True
        raw_confidence = confidence_by_field.get(name)
        if raw_confidence is None and isinstance(item, Mapping):
            raw_confidence = item.get("confidence")
        if raw_confidence is None:
            diagnostics.append(f"missing confidence for critical field {name}")
            continue
        value = float(raw_confidence)
        if not math.isfinite(value) or not 0.0 <= value <= 1.0:
            diagnostics.append(f"invalid confidence for critical field {name}")
            continue
        required_confidences.append(value)
        threshold = (confidence_thresholds or {}).get(name)
        if threshold is not None and value < float(threshold):
            low.append(name)
    if low:
        diagnostics.append("critical field below configured threshold: " + ",".join(sorted(low)))
    overall = min(required_confidences) if required_confidences else 0.0
    structural = "INVALID" if diagnostics and any(
        message.startswith(("invalid", "missing confidence", "missing ", "temporalEvidence"))
        and "below configured" not in message
        for message in diagnostics
    ) else "VALID"
    interpretation = "ABSTAINED" if structural == "INVALID" or low else (
        "AMBIGUOUS" if ambiguous else "RESOLVED"
    )
    claim.update({
        "overallInterpretationConfidence": overall,
        "fieldStatusByField": status_by_field,
        "structuralStatus": structural,
        "interpretationStatus": interpretation,
        "diagnostics": diagnostics,
    })
    return claim


def _assert_no_forbidden_fields(value, path="output"):
    if isinstance(value, Mapping):
        forbidden = FORBIDDEN_OUTPUT_FIELDS & set(value)
        if forbidden:
            raise ValueError(f"forbidden V3 ownership fields at {path}: {sorted(forbidden)}")
        for key, child in value.items():
            _assert_no_forbidden_fields(child, f"{path}.{key}")
    elif isinstance(value, list):
        for index, child in enumerate(value):
            _assert_no_forbidden_fields(child, f"{path}[{index}]")


def build_matrix_output_v3(
    *,
    text: str,
    observation_source_id: str,
    context: Mapping,
    mentions: Sequence[Mapping],
    candidate_table: Mapping,
    raw_claims: Sequence[Mapping],
    confidence_thresholds: Mapping[str, float] | None = None,
) -> dict:
    candidate_ids = [item["candidateId"] for item in candidate_table["candidates"]]
    claim_ids = [str(item["claimId"]) for item in raw_claims]
    claims = [
        validate_claim_v3(
            item,
            text_length=len(text),
            candidate_ids=candidate_ids,
            claim_ids=claim_ids,
            confidence_thresholds=confidence_thresholds,
        )
        for item in raw_claims
    ]
    if candidate_table.get("requiredCandidateLost"):
        for claim in claims:
            claim["interpretationStatus"] = "ABSTAINED"
            claim["diagnostics"].append("required referent candidate lost to bounded overflow")
    output = {
        "contractVersion": CONTRACT_VERSION,
        "input": text,
        "observationSourceId": observation_source_id,
        "speakerRef": context.get("speaker"),
        "observerRef": context.get("observer"),
        "mentions": list(mentions),
        "referentCandidates": list(candidate_table["candidates"]),
        "claims": claims,
    }
    _assert_no_forbidden_fields(output)
    return output
