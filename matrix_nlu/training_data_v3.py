"""Pure V3 target construction for caller-supplied rows.

No path discovery or dataset reading is provided intentionally.  TASK 2.2 may
build targets for synthetic rows, but canonical migration belongs to TASK 2.3.
"""

from __future__ import annotations

from typing import Mapping, Sequence

from contract_v3 import (
    CONTRACT_VERSION,
    FIXED_SEQUENCE_IDS,
    POINTER_SPECIAL_VALUES,
    ROLE_HEADS,
    TOKEN_IDS,
)
from referent_candidates import build_candidate_table, pointer_values


IGNORE = -100


def overlapping_token_indices(offsets, span):
    if span is None:
        return []
    start, end = span
    return [
        index for index, (left, right) in enumerate(offsets)
        if right > left and left < end and right > start
    ]


def bio(offsets, spans, begin=1, inside=2):
    labels = [IGNORE if right <= left else 0 for left, right in offsets]
    occupied = set()
    for span in spans:
        indices = overlapping_token_indices(offsets, span)
        if occupied.intersection(indices):
            raise ValueError("overlapping groups are not valid for one V3 BIO head")
        for position, index in enumerate(indices):
            labels[index] = begin if position == 0 else inside
            occupied.add(index)
    return labels


def entity_bio(offsets, mentions):
    labels = [IGNORE if right <= left else 0 for left, right in offsets]
    for mention in mentions:
        entity_type = mention["entityType"]
        if entity_type == "PERSON":
            begin, inside = TOKEN_IDS["entity"]["B-PERSON"], TOKEN_IDS["entity"]["I-PERSON"]
        elif entity_type == "LOCATION":
            begin, inside = TOKEN_IDS["entity"]["B-LOCATION"], TOKEN_IDS["entity"]["I-LOCATION"]
        else:
            raise ValueError(f"unsupported entity type: {entity_type}")
        for position, index in enumerate(overlapping_token_indices(offsets, mention["span"])):
            if labels[index] not in (0, IGNORE):
                raise ValueError("overlapping entity mentions are not representable by V3 BIO")
            labels[index] = begin if position == 0 else inside
    return labels


def _local(span, source_start):
    return [span[0] - source_start, span[1] - source_start]


def temporal_anchor_values(claim: Mapping, all_claim_ids: Sequence[str]) -> list[str]:
    return (
        ["speech-time", "context-reference"]
        + [f"temporal:{item['temporalId']}" for item in claim.get("temporalEvidence", [])]
        + [f"claim:{claim_id}" for claim_id in all_claim_ids]
    )


def build_v3_examples(
    row: Mapping,
    tokenizer,
    max_length: int,
    context: Mapping,
    *,
    max_referent_candidates: int = 16,
) -> list[dict]:
    if row.get("contractVersion") != CONTRACT_VERSION:
        raise ValueError("target builder accepts only MATRIX_NLU_CONTRACT_V3 rows")
    text = row["text"]
    mentions = row.get("mentions", [])
    claims = row.get("claims", [])
    critical_spans = [span for claim in claims for name in ("subjectSpans", "objectSpans") for span in claim.get(name, [])]
    candidate_table = build_candidate_table(
        text, mentions, context, critical_spans, max_referent_candidates
    )
    if candidate_table["requiredCandidateLost"]:
        raise ValueError("required referent candidate lost to bounded overflow")
    role_values = pointer_values(candidate_table)
    role_ids = {value: index for index, value in enumerate(role_values)}
    all_claim_ids = [str(claim["claimId"]) for claim in claims]

    encoded = tokenizer(
        text, max_length=max_length, padding="max_length", truncation=True,
        return_offsets_mapping=True,
    )
    boundary_offsets = encoded.pop("offset_mapping")
    examples = [{
        "kind": "boundary",
        "rowId": row["id"],
        "language": row["language"],
        "input_ids": encoded["input_ids"],
        "attention_mask": encoded["attention_mask"],
        "token_labels": {
            head: (bio(boundary_offsets, [claim["sourceSpan"] for claim in claims])
                   if head == "boundary" else [IGNORE] * max_length)
            for head in TOKEN_IDS
        },
        "fixed_sequence_labels": {head: IGNORE for head in FIXED_SEQUENCE_IDS},
        "role_pointer_labels": {head: IGNORE for head in ROLE_HEADS},
        "temporal_anchor_label": IGNORE,
    }]

    for claim in claims:
        source_start, source_end = claim["sourceSpan"]
        claim_text = text[source_start:source_end]
        encoded = tokenizer(
            claim_text, max_length=max_length, padding="max_length", truncation=True,
            return_offsets_mapping=True,
        )
        offsets = encoded.pop("offset_mapping")
        local_mentions = [
            {**mention, "span": _local(mention["span"], source_start)}
            for mention in mentions
            if source_start <= mention["span"][0] < mention["span"][1] <= source_end
        ]
        token_labels = {
            "boundary": [IGNORE] * max_length,
            "object": bio(offsets, [_local(span, source_start) for span in claim.get("objectSpans", [])]),
            "subject": bio(offsets, [_local(span, source_start) for span in claim.get("subjectSpans", [])]),
            "negation": bio(offsets, [_local(span, source_start) for span in claim.get("negationCueSpans", [])]),
            "temporal": bio(offsets, [_local(item["span"], source_start) for item in claim.get("temporalEvidence", [])]),
            "entity": entity_bio(offsets, local_mentions),
        }
        fixed = {
            head: FIXED_SEQUENCE_IDS[head][
                claim["temporalRelation"]["relation"] if head == "temporalRelation" else claim[head]
            ]
            for head in FIXED_SEQUENCE_IDS
        }
        roles = {}
        for head in ROLE_HEADS:
            value = claim[head]
            if value not in role_ids:
                raise ValueError(f"role target is not in deterministic candidate table: {head}={value}")
            roles[head] = role_ids[value]
        anchors = temporal_anchor_values(claim, all_claim_ids)
        anchor = claim["temporalRelation"].get("anchorRef")
        anchor_label = anchors.index(anchor) if anchor is not None else IGNORE
        examples.append({
            "kind": "claim",
            "rowId": f"{row['id']}:{claim['claimId']}",
            "language": row["language"],
            "input_ids": encoded["input_ids"],
            "attention_mask": encoded["attention_mask"],
            "token_labels": token_labels,
            "fixed_sequence_labels": fixed,
            "role_pointer_labels": roles,
            "role_pointer_values": role_values,
            "candidateMask": candidate_table["candidateMask"],
            "temporal_anchor_values": anchors,
            "temporal_anchor_label": anchor_label,
        })
    return examples
