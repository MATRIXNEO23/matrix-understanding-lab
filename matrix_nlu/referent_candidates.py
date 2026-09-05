"""Deterministic V3 mention and referent candidate construction."""

from __future__ import annotations

from typing import Iterable, Mapping, Sequence

from contract_v3 import DEFAULT_MAX_REFERENT_CANDIDATES


def _span(value) -> tuple[int, int]:
    if not isinstance(value, (list, tuple)) or len(value) != 2:
        raise ValueError(f"invalid span: {value!r}")
    start, end = int(value[0]), int(value[1])
    if start < 0 or end <= start:
        raise ValueError(f"invalid span: {value!r}")
    return start, end


def _overlaps(left: Sequence[int], right: Sequence[int]) -> bool:
    return left[0] < right[1] and right[0] < left[1]


def build_mentions(entity_spans: Iterable[Mapping], text_length: int) -> list[dict]:
    """Assign stable IDs by start, end and type; do not infer entity identity."""
    normalized = []
    for item in entity_spans:
        start, end = _span(item["span"])
        if end > text_length:
            raise ValueError("entity span is outside the observation")
        entity_type = str(item["type"])
        if entity_type not in {"PERSON", "LOCATION"}:
            raise ValueError(f"unsupported V3 entity type: {entity_type}")
        normalized.append((start, end, entity_type))
    if len(normalized) != len(set(normalized)):
        raise ValueError("duplicate entity mention")
    return [
        {"mentionId": f"m{index}", "span": [start, end], "entityType": entity_type}
        for index, (start, end, entity_type) in enumerate(sorted(normalized))
    ]


def _context_entities(context: Mapping) -> list[dict]:
    raw = context.get("contextEntities", [])
    if isinstance(raw, Mapping):
        raw = [{"entityRef": ref, "surfaceForms": surfaces} for ref, surfaces in raw.items()]
    output = []
    for item in raw:
        ref = str(item["entityRef"])
        output.append({
            "candidateId": f"entity:{ref}",
            "kind": "CONTEXT_ENTITY",
            "resolvedEntityRef": ref,
            "surfaceForms": sorted(str(value) for value in item.get("surfaceForms", [])),
            "resolutionStatus": "RESOLVED",
        })
    return sorted(output, key=lambda item: item["candidateId"])


def build_candidate_table(
    text: str,
    mentions: Sequence[Mapping],
    context: Mapping,
    critical_spans: Sequence[Sequence[int]] = (),
    max_candidates: int = DEFAULT_MAX_REFERENT_CANDIDATES,
) -> dict:
    """Build a bounded stable table and report rather than hide any overflow."""
    if max_candidates < 4:
        raise ValueError("max_candidates must be at least 4")
    required = [
        {
            "candidateId": "ctx:speaker",
            "kind": "CONTEXT_SPEAKER",
            "resolvedEntityRef": context.get("speaker"),
            "resolutionStatus": "RESOLVED" if context.get("speaker") is not None else "UNRESOLVED",
        },
        {
            "candidateId": "ctx:observer",
            "kind": "CONTEXT_OBSERVER",
            "resolvedEntityRef": context.get("observer"),
            "resolutionStatus": "RESOLVED" if context.get("observer") is not None else "UNRESOLVED",
        },
    ]
    critical = [_span(value) for value in critical_spans]
    context_by_surface = {}
    for candidate in _context_entities(context):
        for surface in candidate.get("surfaceForms", []):
            context_by_surface.setdefault(surface.casefold(), []).append(candidate["resolvedEntityRef"])

    mention_candidates = []
    for mention in mentions:
        start, end = _span(mention["span"])
        surface = text[start:end]
        exact = context_by_surface.get(surface.casefold(), [])
        resolved = exact[0] if len(exact) == 1 else None
        mention_candidates.append({
            "candidateId": f"mention:{mention['mentionId']}",
            "kind": "MENTION",
            "mentionId": str(mention["mentionId"]),
            "span": [start, end],
            "entityType": str(mention["entityType"]),
            "resolvedEntityRef": resolved,
            "resolutionStatus": "RESOLVED" if resolved is not None else (
                "AMBIGUOUS" if len(exact) > 1 else "UNRESOLVED"
            ),
            "critical": any(_overlaps((start, end), span) for span in critical),
        })
    critical_mentions = [item for item in mention_candidates if item["critical"]]
    other_mentions = [item for item in mention_candidates if not item["critical"]]
    ordered = required + critical_mentions + other_mentions + _context_entities(context)
    kept = ordered[:max_candidates]
    lost = ordered[max_candidates:]
    lost_critical = [item["candidateId"] for item in lost if item.get("critical")]
    return {
        "candidates": kept,
        "candidateMask": [1] * len(kept) + [0] * (max_candidates - len(kept)),
        "overflow": bool(lost),
        "droppedCandidateIds": [item["candidateId"] for item in lost],
        "lostCriticalCandidateIds": lost_critical,
        "requiredCandidateLost": bool(lost_critical),
        "maxReferentCandidates": max_candidates,
    }


def pointer_values(table: Mapping) -> list[str]:
    return [item["candidateId"] for item in table["candidates"]] + ["NONE", "UNKNOWN"]
