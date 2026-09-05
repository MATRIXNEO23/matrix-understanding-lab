#!/usr/bin/env python3
"""Controlled TRAIN-only V2 -> Matrix-NLU V3 migration.

The caller must provide explicit TRAIN files.  This module refuses paths whose
names imply DEV/Frozen/test, never discovers partitions, and never trains a model.
Authoring catalogs below are used only to reannotate already-authorized TRAIN
surfaces; they are not runtime linguistic rules.
"""

from __future__ import annotations

import argparse
import hashlib
import json
import pathlib
from collections import Counter, defaultdict
from typing import Iterable, Mapping, Sequence

from contract_v3 import (
    ANCHOR_REQUIRED_RELATIONS,
    CONTRACT_VERSION,
    DEFAULT_MAX_REFERENT_CANDIDATES,
    FIELD_STATUSES,
    FIXED_SEQUENCE_LABELS,
    FORBIDDEN_OUTPUT_FIELDS,
    FORBIDDEN_ROLE_VALUES,
    POINTER_SPECIAL_VALUES,
    ROLE_HEADS,
    contract_fingerprint,
)
from migrate_contract_v3 import classify_v2_rows
from referent_candidates import build_candidate_table
from training_data_v3 import build_v3_examples


TOOL_VERSION = "student5.task2.3.train-migration.v1"
OUTPUT_DATASET_ID = "student5-matrix-nlu-v3-train-v1"
SHARD_ROWS = 50
REQUIRED_CAPABILITIES = (
    "negation", "temporal", "referents", "source attribution",
    "third-party report", "belief", "hypothesis", "command", "request",
    "correction", "goal/desire", "ownership", "multi-claim",
    "adult consent", "adult refusal", "adult withdrawal", "adult desire",
)
EXPECTED_SOURCE_SHA256 = {
    "matrix-v2-train": "5118d37ce2ab19d5be171f757f448698085e3c222a4a627f9838329836185820",
    "v22a-repair-train": "8be02976d46ba47d746ff7307d688d93595453221965b3de995d4b1de655799f",
}

NEGATION_CUES = {
    "it": ("non", "mai", "più"),
    "en": ("not", "don't", "never", "cannot"),
    "es": ("no", "nunca"),
}

TEMPORAL_EXPRESSIONS = {
    "it": (
        "fino allo scorso anno", "in questo momento", "in questo periodo",
        "in precedenza", "più avanti", "da giovane", "nel 2020",
        "in futuro", "domani", "adesso", "oggi", "ora",
    ),
    "en": (
        "over the coming weeks", "when I was younger", "until last year",
        "in the future", "at this moment", "in due course", "before long",
        "at the moment", "previously", "in 2020", "tomorrow", "currently",
        "one day", "later", "today", "now",
    ),
    "es": (
        "hasta el año pasado", "en este momento", "más adelante",
        "en el futuro", "anteriormente", "actualmente", "de joven",
        "en 2020", "mañana", "ahora", "hoy",
    ),
}

POLARITY_REANNOTATIONS = {
    "mx-v22a-cross-001": "NEGATIVE",
}

EXPLICIT_CROSS_ENTITY_ROWS = {
    "mx-v22a-cross-000": "PERSON", "mx-v22a-cross-001": "PERSON", "mx-v22a-cross-002": "PERSON",
    "mx-v22a-cross-003": "LOCATION", "mx-v22a-cross-004": "LOCATION", "mx-v22a-cross-005": "LOCATION",
}
EXPLICIT_CROSS_SUBJECT_ROWS = {"mx-v22a-cross-030", "mx-v22a-cross-031", "mx-v22a-cross-032"}
QUESTION_ROLE_ROWS = {"mx-v22a-cross-018", "mx-v22a-cross-019", "mx-v22a-cross-020"}
REQUEST_ADDRESSEE_ROWS = {"mx-v22a-cross-033", "mx-v22a-cross-034", "mx-v22a-cross-035"}
ATTRIBUTED_REPORT_ROWS = {
    "mx-v22a-it-core-113", "mx-v22a-it-core-115", "mx-v22a-it-core-117", "mx-v22a-it-core-119",
    "mx-v22a-it-core-121", "mx-v22a-it-core-123", "mx-v22a-it-core-125", "mx-v22a-it-core-127",
}


class UnusableRow(ValueError):
    pass


def sha256(path: pathlib.Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def _assert_train_path(path: pathlib.Path) -> None:
    lowered = path.name.casefold()
    if "train" not in lowered or any(marker in lowered for marker in ("dev", "frozen", "test")):
        raise ValueError(f"not an explicit TRAIN-only source path: {path}")


def load_train_jsonl(path: pathlib.Path, expected_sha256: str) -> list[dict]:
    _assert_train_path(path)
    actual = sha256(path)
    if actual != expected_sha256:
        raise ValueError(f"TRAIN source checksum mismatch: {path}: {actual}")
    rows = [json.loads(line) for line in path.read_text(encoding="utf-8").splitlines() if line]
    if any(row.get("split") != "train" for row in rows):
        raise ValueError(f"non-TRAIN row in explicit source: {path}")
    return rows


def _boundary(text: str, index: int) -> bool:
    return index < 0 or index >= len(text) or not (text[index].isalnum() or text[index] == "_")


def exact_occurrences(text: str, phrases: Sequence[str]) -> list[list[int]]:
    """Return all non-overlapping exact authored phrases with token boundaries."""
    lowered = text.lower()
    candidates = []
    for phrase in sorted(set(phrases), key=lambda value: (-len(value), value)):
        needle = phrase.lower()
        start = 0
        while True:
            position = lowered.find(needle, start)
            if position < 0:
                break
            end = position + len(needle)
            if _boundary(lowered, position - 1) and _boundary(lowered, end):
                candidates.append((position, end))
            start = position + 1
    output = []
    for start, end in sorted(candidates):
        if not any(start < previous[1] and previous[0] < end for previous in output):
            output.append([start, end])
    return output


def _source_local_occurrences(row: Mapping, claim: Mapping, phrases: Sequence[str]) -> list[list[int]]:
    start, end = claim["spans"]["source"]
    return [[left + start, right + start] for left, right in exact_occurrences(row["text"][start:end], phrases)]


def _mentions(row: Mapping) -> list[dict]:
    entries = set()
    for claim in row["claims"]:
        for entity in claim.get("spans", {}).get("entities", []):
            if entity.get("type") in {"PERSON", "LOCATION"}:
                entries.add((int(entity["span"][0]), int(entity["span"][1]), entity["type"]))
        # V2 sometimes carried an explicit subject span without duplicating it
        # in spans.entities.  The span plus the explicit referent-role label is
        # sufficient authored evidence to restore the PERSON mention.
        subject = claim.get("spans", {}).get("subject")
        if subject is not None and claim.get("labels", {}).get("subjectReferent") in {"KNOWN_ENTITY", "RECENT_ENTITY"}:
            entries.add((int(subject[0]), int(subject[1]), "PERSON"))
    if row.get("id") in EXPLICIT_CROSS_ENTITY_ROWS:
        span = row["claims"][0]["spans"]["object"]
        entries.add((int(span[0]), int(span[1]), EXPLICIT_CROSS_ENTITY_ROWS[row["id"]]))
    if row.get("id") in EXPLICIT_CROSS_SUBJECT_ROWS:
        # These three authored equivalents begin with the same explicit PERSON
        # subject, "Marco"; V2 omitted its subject/entity spans.
        entries.add((0, 5, "PERSON"))
    return [
        {"mentionId": f"m{index}", "span": [start, end], "entityType": entity_type}
        for index, (start, end, entity_type) in enumerate(sorted(entries))
    ]


def _context(row: Mapping) -> dict:
    original = row.get("context", {})
    entities = []
    for surface, value in sorted(original.get("knownEntities", {}).items()):
        if isinstance(value, str):
            entities.append({"entityRef": value, "surfaceForms": [surface]})
        elif isinstance(value, Mapping) and isinstance(value.get("entityRef"), str):
            entities.append({"entityRef": value["entityRef"], "surfaceForms": [surface]})
    for value in sorted(str(item) for item in original.get("recentEntityRefs", [])):
        if value not in {item["entityRef"] for item in entities}:
            entities.append({"entityRef": value, "surfaceForms": []})
    return {
        "speaker": original.get("speaker"),
        "observer": original.get("observer"),
        "contextEntities": entities,
    }


def _overlaps(left: Sequence[int], right: Sequence[int]) -> bool:
    return left[0] < right[1] and right[0] < left[1]


def _mention_candidates(mentions: Sequence[Mapping], spans: Sequence[Sequence[int]], entity_type: str = "PERSON") -> list[str]:
    return [
        f"mention:{mention['mentionId']}"
        for mention in mentions
        if mention["entityType"] == entity_type and any(_overlaps(mention["span"], span) for span in spans)
    ]


def _unique(values: Iterable[str], reason: str) -> str:
    values = sorted(set(values))
    if len(values) != 1:
        raise UnusableRow(f"{reason}: expected one candidate, found {values}")
    return values[0]


def _map_role(
    value: str,
    head: str,
    row: Mapping,
    claim: Mapping,
    mentions: Sequence[Mapping],
    resolved_subject: str | None,
) -> str:
    if value == "SPEAKER" or value == "SELF":
        return "ctx:speaker"
    if value == "OBSERVER":
        return "ctx:observer"
    if value in POINTER_SPECIAL_VALUES:
        return value
    if value == "SUBJECT":
        if resolved_subject is None:
            raise UnusableRow(f"{head}: SUBJECT without resolved subject")
        return resolved_subject
    if value == "RECENT_ENTITY":
        refs = [str(item) for item in row.get("context", {}).get("recentEntityRefs", [])]
        return f"entity:{_unique(refs, head + ':recent')}"
    if value == "KNOWN_ENTITY":
        subject_span = claim.get("spans", {}).get("subject")
        if head == "subjectReferent" and subject_span is not None:
            return _unique(_mention_candidates(mentions, [subject_span]), head)
        if head == "subjectReferent":
            source_span = claim.get("spans", {}).get("source")
            values = _mention_candidates(mentions, [source_span]) if source_span is not None else []
            # This is a unique explicit V2 role target, not a first-mention
            # fallback.  Multiple or zero mentions remain fail-closed.
            return _unique(values, head + ":unique-explicit-role")
        object_span = claim.get("spans", {}).get("object")
        if head == "targetReferent" and object_span is not None:
            values = _mention_candidates(mentions, [object_span])
            if resolved_subject is not None:
                values = [item for item in values if item != resolved_subject]
            return _unique(values, head)
        raise UnusableRow(f"{head}: KNOWN_ENTITY lacks an explicit role span")
    if value is None:
        raise UnusableRow(f"{head}: missing V2 role value")
    raise UnusableRow(f"{head}: unsupported V2 role value {value}")


def _claim_kind(value: str) -> str:
    if value == "HYPOTHESIS":
        return "HYPOTHESIS"
    if value == "EXPLICIT":
        return "DIRECT"
    if value in {"DIRECT", "REPORT", "BELIEF", "UNKNOWN"}:
        return value
    raise UnusableRow(f"unsupported claimKind: {value}")


def _dialogue_act(value: str) -> str:
    return "ASSERT" if value == "HYPOTHESIS" else value


def _temporal_evidence(row: Mapping, claim: Mapping) -> list[dict]:
    spans = []
    existing = claim.get("spans", {}).get("temporal")
    if existing is not None:
        spans.append(list(existing))
    language = row["language"]
    scan_language = "it" if language == "code-switch" else language
    spans.extend(_source_local_occurrences(row, claim, TEMPORAL_EXPRESSIONS.get(scan_language, ())))
    unique = sorted({(start, end) for start, end in spans})
    return [{"temporalId": f"t{index}", "span": [start, end]} for index, (start, end) in enumerate(unique)]


def _negation_cues(row: Mapping, claim: Mapping) -> list[list[int]]:
    # V2 full-source negation marks authorize reannotation but are never reused as cues.
    if claim.get("spans", {}).get("negation") is None:
        return []
    language = row["language"]
    scan_language = "it" if language == "code-switch" else language
    return _source_local_occurrences(row, claim, NEGATION_CUES.get(scan_language, ()))


def _status(value: str) -> str:
    if value == "UNKNOWN":
        return "UNKNOWN"
    if value == "NONE":
        return "NOT_APPLICABLE"
    return "RESOLVED"


def migrate_row(row: Mapping, source_dataset_id: str) -> tuple[dict, dict]:
    if row.get("split") != "train":
        raise ValueError("migration accepts TRAIN rows only")
    mentions = _mentions(row)
    context = _context(row)
    language = "code-switch" if any(
        claim.get("family") == "v22a_adult_it_english_term" for claim in row["claims"]
    ) else row["language"]
    changed_fields = {
        "contractVersion", "mentions", "referentCandidates", "claims[].claimId",
        "claims[].labels.sourceReferent", "claims[].labels.claimKind",
        "claims[].fieldStatusByField", "migrationProvenance",
    }
    reason_codes = {
        "V3_CONTRACT_VERSION", "V3_DETERMINISTIC_MENTIONS",
        "V3_SOURCE_REANNOTATION", "V3_ROLE_POINTER_REANNOTATION",
        "V3_CLAIM_KIND_REANNOTATION", "V3_STATUS_MATERIALIZATION",
    }
    if language != row["language"]:
        changed_fields.add("language")
        reason_codes.add("EXPLICIT_CODE_SWITCH_FAMILY")
    if row["id"] in set(EXPLICIT_CROSS_ENTITY_ROWS) | EXPLICIT_CROSS_SUBJECT_ROWS | QUESTION_ROLE_ROWS | REQUEST_ADDRESSEE_ROWS:
        reason_codes.add("CONTROLLED_CROSS_LINGUAL_ROLE_REANNOTATION")
    if row["id"] in ATTRIBUTED_REPORT_ROWS:
        reason_codes.add("EXPLICIT_THIRD_PARTY_REPORT_REANNOTATION")
    if row["id"] == "mx-v22a-adult-it-046":
        changed_fields.add("claims[].family")
        reason_codes.add("CONTROLLED_ADULT_WITHDRAWAL_FAMILY_REANNOTATION")

    claims = []
    for index, old in enumerate(row["claims"]):
        labels_v2 = old["labels"]
        if row["id"] in QUESTION_ROLE_ROWS:
            subject, target = "ctx:observer", "ctx:speaker"
        elif row["id"] in EXPLICIT_CROSS_SUBJECT_ROWS:
            subject, target = _unique(_mention_candidates(mentions, [[0, 5]]), "cross-subject"), "NONE"
        else:
            subject = _map_role(labels_v2.get("subjectReferent"), "subjectReferent", row, old, mentions, None)
            if row["id"] in {"mx-v22a-cross-000", "mx-v22a-cross-001", "mx-v22a-cross-002"}:
                target = _unique(_mention_candidates(mentions, [old["spans"]["object"]]), "cross-target")
            elif row["id"] in REQUEST_ADDRESSEE_ROWS:
                target = "ctx:observer"
            else:
                target = _map_role(labels_v2.get("targetReferent"), "targetReferent", row, old, mentions, subject)
        owner = _map_role(labels_v2.get("ownerReferent"), "ownerReferent", row, old, mentions, subject)
        if row["id"] in QUESTION_ROLE_ROWS:
            owner = "ctx:observer"
        perspective = _map_role(labels_v2.get("perspectiveReferent"), "perspectiveReferent", row, old, mentions, subject)
        kind = "REPORT" if row["id"] in ATTRIBUTED_REPORT_ROWS else _claim_kind(labels_v2.get("claimKind"))
        source = subject if row["id"] in ATTRIBUTED_REPORT_ROWS else "ctx:speaker"
        if kind != _claim_kind(labels_v2.get("claimKind")):
            changed_fields.add("claims[].labels.claimKind")
        if kind == "REPORT" and source in {"NONE", "UNKNOWN", "ctx:speaker"}:
            raise UnusableRow("REPORT source cannot be reconstructed from this V2 row")
        cues = _negation_cues({**row, "language": language}, old)
        temporal = _temporal_evidence({**row, "language": language}, old)
        polarity = POLARITY_REANNOTATIONS.get(row["id"], labels_v2.get("polarity"))
        if polarity != labels_v2.get("polarity"):
            changed_fields.add("claims[].labels.polarity")
            reason_codes.add("CONTROLLED_POLARITY_CORRECTION")
        if old.get("spans", {}).get("negation") is not None:
            changed_fields.add("claims[].negationCueSpans")
            reason_codes.add("OVERT_NEGATION_CUE_REANNOTATION")
        if temporal or old.get("spans", {}).get("temporal") is not None:
            changed_fields.add("claims[].temporalEvidence")
            reason_codes.add("EXPLICIT_TEMPORAL_EVIDENCE_REANNOTATION")
        dialogue_act = _dialogue_act(labels_v2.get("dialogueAct"))
        if row["id"] in REQUEST_ADDRESSEE_ROWS:
            dialogue_act = "REQUEST"
        if dialogue_act != labels_v2.get("dialogueAct"):
            changed_fields.add("claims[].labels.dialogueAct")
            reason_codes.add("HYPOTHESIS_ACT_KIND_SEPARATION")
        relation = labels_v2.get("temporalRelation")
        if relation not in FIXED_SEQUENCE_LABELS["temporalRelation"]:
            raise UnusableRow(f"invalid temporal relation: {relation}")
        anchor_ref = "speech-time" if relation in {"CURRENT", "PAST", "FUTURE", "RECURRENT"} else None
        if relation in ANCHOR_REQUIRED_RELATIONS and anchor_ref is None:
            raise UnusableRow(f"temporal relation requires unrecoverable anchor: {relation}")
        source_span = list(old["spans"]["source"])
        subject_spans = ([list(old["spans"]["subject"])] if old["spans"].get("subject") is not None else
                         ([[0, 5]] if row["id"] in EXPLICIT_CROSS_SUBJECT_ROWS else []))
        object_spans = [] if old["spans"].get("object") is None else [list(old["spans"]["object"])]
        mention_ids = [
            mention["mentionId"] for mention in mentions
            if source_span[0] <= mention["span"][0] < mention["span"][1] <= source_span[1]
        ]
        labels = {
            "dialogueAct": dialogue_act,
            "predicate": labels_v2.get("predicate"),
            "subjectReferent": subject,
            "targetReferent": target,
            "ownerReferent": owner,
            "perspectiveReferent": perspective,
            "sourceReferent": source,
            "polarity": polarity,
            "temporalRelation": {"relation": relation, "anchorRef": anchor_ref},
            "claimKind": kind,
        }
        statuses = {
            "boundary": "RESOLVED", "subjectSpans": "RESOLVED",
            "objectSpans": "RESOLVED", "negationCueSpans": "RESOLVED",
            "temporalEvidence": "RESOLVED", "entityMentionIds": "RESOLVED",
            "dialogueAct": _status(dialogue_act), "predicate": "RESOLVED",
            **{head: _status(labels[head]) for head in ROLE_HEADS},
            "polarity": _status(polarity),
            "temporalRelation": _status(relation),
            "claimKind": _status(kind),
        }
        claims.append({
            "claimId": f"c{index}",
            "family": "v22a_adult_it_withdrawal" if row["id"] == "mx-v22a-adult-it-046" else old.get("family", "unclassified"),
            "sourceSpan": source_span,
            "subjectSpans": subject_spans,
            "objectSpans": object_spans,
            "negationCueSpans": cues,
            "temporalEvidence": temporal,
            "entityMentionIds": mention_ids,
            "labels": labels,
            "fieldStatusByField": statuses,
            "structuralStatus": "VALID",
            "interpretationStatus": "RESOLVED" if "UNKNOWN" not in labels.values() else "ABSTAINED",
        })

    critical = [span for claim in claims for field in ("subjectSpans", "objectSpans") for span in claim[field]]
    table = build_candidate_table(
        row["text"], mentions, context, critical,
        max_candidates=DEFAULT_MAX_REFERENT_CANDIDATES,
    )
    if table["requiredCandidateLost"]:
        raise UnusableRow("required referent candidate lost to bounded overflow")
    migrated = {
        "contractVersion": CONTRACT_VERSION,
        "contractFingerprintSha256": contract_fingerprint(),
        "datasetId": OUTPUT_DATASET_ID,
        "sourceDatasetId": source_dataset_id,
        "id": row["id"],
        "split": "train",
        "language": language,
        "text": row["text"],
        "context": context,
        "mentions": mentions,
        "referentCandidates": table["candidates"],
        "claims": claims,
        "adultOnly": bool(row.get("adultOnly", False)),
        "provenance": {
            "sourceRowId": row["id"],
            "sourceSchema": row.get("schemaVersion"),
            "sourceProvenance": row.get("provenance", {}),
            "migrationClass": "NEEDS_REANNOTATION",
            "finalDisposition": "REANNOTATED",
            "fieldsReannotated": sorted(changed_fields),
            "annotationReasonCodes": sorted(reason_codes),
            "contractVersion": CONTRACT_VERSION,
            "migrationToolVersion": TOOL_VERSION,
        },
    }
    record = {
        "rowId": migrated["id"],
        "sourceRowId": row["id"],
        "sourceDatasetId": source_dataset_id,
        "sourceLanguage": row["language"],
        "finalLanguage": language,
        "migrationClass": "NEEDS_REANNOTATION",
        "finalDisposition": "REANNOTATED",
        "changedFields": sorted(changed_fields),
        "reasonCodes": sorted(reason_codes),
    }
    return migrated, record


def _valid_span(span, text_length: int) -> bool:
    return isinstance(span, list) and len(span) == 2 and 0 <= span[0] < span[1] <= text_length


def validate_v3_row(row: Mapping) -> list[str]:
    errors = []
    text = row.get("text", "")
    if row.get("contractVersion") != CONTRACT_VERSION:
        errors.append("invalid contract version")
    if row.get("contractFingerprintSha256") != contract_fingerprint():
        errors.append("invalid contract fingerprint")
    if row.get("split") != "train":
        errors.append("non-TRAIN split")
    if row.get("language") not in {"it", "en", "es", "code-switch"}:
        errors.append("invalid language")
    mention_ids = [item.get("mentionId") for item in row.get("mentions", [])]
    if len(mention_ids) != len(set(mention_ids)):
        errors.append("duplicate mention ID")
    for mention in row.get("mentions", []):
        if not _valid_span(mention.get("span"), len(text)) or mention.get("entityType") not in {"PERSON", "LOCATION"}:
            errors.append("invalid mention")
    candidate_ids = [item.get("candidateId") for item in row.get("referentCandidates", [])]
    if len(candidate_ids) != len(set(candidate_ids)):
        errors.append("duplicate candidate ID")
    legal_pointers = set(candidate_ids) | set(POINTER_SPECIAL_VALUES)
    claim_ids = [claim.get("claimId") for claim in row.get("claims", [])]
    if len(claim_ids) != len(set(claim_ids)) or any(not value for value in claim_ids):
        errors.append("invalid or duplicate claim ID")
    for claim in row.get("claims", []):
        source = claim.get("sourceSpan")
        if not _valid_span(source, len(text)):
            errors.append("invalid source span")
            continue
        for field in ("subjectSpans", "objectSpans", "negationCueSpans"):
            spans = claim.get(field)
            if not isinstance(spans, list):
                errors.append(f"missing plural field {field}")
                continue
            ordered = sorted(spans)
            if any(not _valid_span(span, len(text)) or not (source[0] <= span[0] < span[1] <= source[1]) for span in spans):
                errors.append(f"invalid {field}")
            if any(_overlaps(left, right) for left, right in zip(ordered, ordered[1:])):
                errors.append(f"overlapping {field}")
        temporal_ids = []
        for item in claim.get("temporalEvidence", []):
            temporal_ids.append(item.get("temporalId"))
            if not _valid_span(item.get("span"), len(text)):
                errors.append("invalid temporal evidence")
        if len(temporal_ids) != len(set(temporal_ids)):
            errors.append("duplicate temporal ID")
        if any(value not in mention_ids for value in claim.get("entityMentionIds", [])):
            errors.append("invalid entity mention ID")
        labels = claim.get("labels", {})
        for head, registry in FIXED_SEQUENCE_LABELS.items():
            value = labels.get("temporalRelation", {}).get("relation") if head == "temporalRelation" else labels.get(head)
            if value not in registry:
                errors.append(f"invalid label {head}")
        for head in ROLE_HEADS:
            value = labels.get(head)
            if value in FORBIDDEN_ROLE_VALUES or value not in legal_pointers:
                errors.append(f"invalid pointer {head}")
        relation = labels.get("temporalRelation", {})
        anchor = relation.get("anchorRef")
        legal_anchors = {"speech-time", "context-reference"} | {f"temporal:{value}" for value in temporal_ids} | {f"claim:{value}" for value in claim_ids}
        if relation.get("relation") in ANCHOR_REQUIRED_RELATIONS and anchor not in legal_anchors:
            errors.append("missing required temporal anchor")
        if anchor is not None and anchor not in legal_anchors:
            errors.append("invalid temporal anchor")
        statuses = claim.get("fieldStatusByField", {})
        if not statuses or any(value not in FIELD_STATUSES for value in statuses.values()):
            errors.append("invalid field status")
    def visit(value):
        if isinstance(value, Mapping):
            for key, child in value.items():
                if key in FORBIDDEN_OUTPUT_FIELDS:
                    errors.append(f"downstream field leakage: {key}")
                visit(child)
        elif isinstance(value, list):
            for child in value:
                visit(child)
    visit(row)
    return sorted(set(errors))


class DryRunTokenizer:
    """Data-only offset tokenizer for exhaustive target-construction validation."""
    def __call__(self, text, max_length, padding, truncation, return_offsets_mapping):
        offsets, cursor = [], 0
        for token in text.split():
            start = text.index(token, cursor)
            end = start + len(token)
            offsets.append([start, end])
            cursor = end
        if len(offsets) > max_length:
            raise ValueError("dry-run tokenizer would truncate a TRAIN observation")
        padding_count = max_length - len(offsets)
        return {
            "input_ids": list(range(1, len(offsets) + 1)) + [0] * padding_count,
            "attention_mask": [1] * len(offsets) + [0] * padding_count,
            "offset_mapping": offsets + [[0, 0]] * padding_count,
        }


def target_builder_gate(rows: Sequence[Mapping]) -> dict:
    tokenizer = DryRunTokenizer()
    built = 0
    errors = []
    for row in rows:
        try:
            built += len(build_v3_examples(row, tokenizer, 256, row["context"]))
        except Exception as exc:  # fail-closed evidence, not a permissive fallback
            errors.append({"rowId": row.get("id"), "error": str(exc)})
    return {"rows": len(rows), "rowsBuildable": len(rows) - len(errors), "examplesBuilt": built, "errors": errors}


def _family_capabilities(row: Mapping, claim: Mapping) -> set[str]:
    labels = claim["labels"]
    family = claim.get("family", "")
    capabilities = {"ownership"}
    if claim["negationCueSpans"] or labels["polarity"] == "NEGATIVE": capabilities.add("negation")
    if claim["temporalEvidence"] or labels["temporalRelation"]["relation"] != "ATEMPORAL": capabilities.add("temporal")
    if any(labels[head] not in {"ctx:speaker", "ctx:observer", "NONE", "UNKNOWN"} for head in ROLE_HEADS): capabilities.add("referents")
    if labels["sourceReferent"] != "ctx:speaker": capabilities.add("source attribution")
    if labels["claimKind"] == "REPORT": capabilities.update(("source attribution", "third-party report"))
    if labels["claimKind"] == "BELIEF": capabilities.add("belief")
    if labels["claimKind"] == "HYPOTHESIS": capabilities.add("hypothesis")
    if labels["dialogueAct"] == "COMMAND": capabilities.add("command")
    if labels["dialogueAct"] == "REQUEST": capabilities.add("request")
    if labels["dialogueAct"] == "CORRECT": capabilities.add("correction")
    if labels["predicate"] == "goal.object": capabilities.add("goal/desire")
    if len(row["claims"]) > 1: capabilities.add("multi-claim")
    if row.get("adultOnly") and labels["predicate"] == "consent.grant": capabilities.add("adult consent")
    if row.get("adultOnly") and labels["predicate"] == "consent.refuse": capabilities.add("adult refusal")
    if row.get("adultOnly") and ("withdraw" in family or "boundary" in family and any(row["text"][a:b].casefold() in {"più", "anymore"} for a,b in claim["negationCueSpans"])): capabilities.add("adult withdrawal")
    if row.get("adultOnly") and labels["predicate"] == "goal.object": capabilities.add("adult desire")
    return capabilities


def statistics(rows: Sequence[Mapping], migration_records: Sequence[Mapping], unusable: Sequence[Mapping]) -> dict:
    language = Counter(row["language"] for row in rows)
    pointer = {head: Counter() for head in ROLE_HEADS}
    temporal = Counter()
    family = defaultdict(lambda: {"rows": set(), "claims": 0, "languages": Counter(), "migration": Counter()})
    negation = Counter()
    source = Counter()
    adults = defaultdict(Counter)
    negation_rows = Counter()
    for row in rows:
        row_has_negative = False
        row_has_cues = False
        row_has_multiple_cues = False
        for claim in row["claims"]:
            labels = claim["labels"]
            for head in ROLE_HEADS:
                value = labels[head]
                pointer[head]["UNKNOWN" if value == "UNKNOWN" else "NONE" if value == "NONE" else "RESOLVED_CANDIDATE"] += 1
            temporal[labels["temporalRelation"]["relation"]] += 1
            if labels["polarity"] == "NEGATIVE": negation["negativeClaims"] += 1
            row_has_negative = row_has_negative or labels["polarity"] == "NEGATIVE"
            if claim["negationCueSpans"]: negation["claimsWithCueSpans"] += 1
            row_has_cues = row_has_cues or bool(claim["negationCueSpans"])
            if len(claim["negationCueSpans"]) > 1: negation["claimsWithMultipleCues"] += 1
            row_has_multiple_cues = row_has_multiple_cues or len(claim["negationCueSpans"]) > 1
            negation[f"polarity{labels['polarity'].title()}"] += 1
            if claim["negationCueSpans"] and labels["polarity"] == "POSITIVE": negation["positivePolarityWithCue"] += 1
            if labels["claimKind"] == "REPORT": source["reportClaims"] += 1
            if labels["claimKind"] == "BELIEF": source["beliefClaims"] += 1
            if labels["sourceReferent"] == labels["perspectiveReferent"]: source["sourceEqualsPerspective"] += 1
            else: source["sourceDiffersPerspective"] += 1
            if labels["sourceReferent"] == "UNKNOWN": source["sourceUnknown"] += 1
            if labels["perspectiveReferent"] == "UNKNOWN": source["perspectiveUnknown"] += 1
            for capability in _family_capabilities(row, claim):
                entry = family[capability]; entry["rows"].add(row["id"]); entry["claims"] += 1; entry["languages"][row["language"]] += 1; entry["migration"]["REANNOTATED"] += 1
            if row.get("adultOnly"):
                adults[row["language"]][claim.get("family", "unclassified")] += 1
        negation_rows["negativeRows"] += int(row_has_negative)
        negation_rows["rowsWithCueSpans"] += int(row_has_cues)
        negation_rows["rowsWithMultipleCues"] += int(row_has_multiple_cues)
    required_anchor_claims = sum(temporal[name] for name in ANCHOR_REQUIRED_RELATIONS)
    valid_anchor_claims = sum(1 for row in rows for claim in row["claims"] if claim["labels"]["temporalRelation"]["relation"] in ANCHOR_REQUIRED_RELATIONS and claim["labels"]["temporalRelation"].get("anchorRef"))
    ids = Counter(row["id"] for row in rows)
    texts = Counter((row["language"], row["text"]) for row in rows)
    provenance_ids = Counter((row["sourceDatasetId"], row["provenance"]["sourceRowId"]) for row in rows)
    target_by_surface = defaultdict(set)
    for row in rows:
        target_by_surface[(row["language"], row["text"])].add(json.dumps([claim["labels"] for claim in row["claims"]], sort_keys=True))
    for capability in REQUIRED_CAPABILITIES:
        family[capability]
    migration_language = {
        language_name: {
            "original": sum(record.get("sourceLanguage") == language_name for record in migration_records) + sum(record.get("sourceLanguage") == language_name for record in unusable),
            "migrated": sum(record.get("finalLanguage") == language_name for record in migration_records),
            "reannotated": sum(record.get("finalLanguage") == language_name and record.get("finalDisposition") == "REANNOTATED" for record in migration_records),
            "unusable": sum(record.get("sourceLanguage") == language_name for record in unusable),
            "final": language[language_name],
        }
        for language_name in ("it", "en", "es", "code-switch")
    }
    pointer_summary = {}
    for head, counts in pointer.items():
        total = sum(counts.values())
        normalized = {name: counts[name] for name in ("RESOLVED_CANDIDATE", "NONE", "UNKNOWN", "AMBIGUOUS")}
        pointer_summary[head] = {
            "total": total,
            "counts": normalized,
            "percent": {name: round(100 * value / total, 6) if total else 0.0 for name, value in normalized.items()},
        }
    for key, value in negation_rows.items():
        negation[key] = value
    for key in ("reportClaims", "beliefClaims", "sourceEqualsPerspective", "sourceDiffersPerspective", "sourceUnknown", "perspectiveUnknown"):
        source[key] += 0
    return {
        "rows": len(rows), "claims": sum(len(row["claims"]) for row in rows),
        "languages": {name: language[name] for name in ("it", "en", "es", "code-switch")},
        "languageMigration": migration_language,
        "migration": {"REANNOTATED": len(rows), "UNUSABLE": len(unusable)},
        "referentPointers": pointer_summary,
        "negation": dict(sorted(negation.items())),
        "temporalRelations": {name: temporal[name] for name in FIXED_SEQUENCE_LABELS["temporalRelation"]},
        "temporalAnchors": {"relationsRequiringAnchors": required_anchor_claims, "validAnchors": valid_anchor_claims, "missingAnchors": required_anchor_claims - valid_anchor_claims},
        "sourcePerspective": dict(sorted(source.items())),
        "adultIntimacy": {lang: dict(sorted(values.items())) for lang, values in sorted(adults.items())},
        "familyCoverage": {name: {"rows": len(value["rows"]), "claims": value["claims"], "languages": dict(sorted(value["languages"].items())), "migration": dict(value["migration"])} for name, value in sorted(family.items())},
        "multiSpan": {"claimsWithMultipleSubjectSpans": sum(len(claim["subjectSpans"]) > 1 for row in rows for claim in row["claims"]), "claimsWithMultipleObjectSpans": sum(len(claim["objectSpans"]) > 1 for row in rows for claim in row["claims"]), "claimsWithMultipleNegationCues": negation["claimsWithMultipleCues"], "claimsWithMultipleTemporalEvidence": sum(len(claim["temporalEvidence"]) > 1 for row in rows for claim in row["claims"])},
        "multiClaimRows": sum(len(row["claims"]) > 1 for row in rows),
        "duplicates": {
            "duplicateRowIds": sum(value - 1 for value in ids.values() if value > 1),
            "duplicateTexts": sum(value - 1 for value in texts.values() if value > 1),
            "duplicateProvenance": sum(value - 1 for value in provenance_ids.values() if value > 1),
            "conflictingGoldForIdenticalText": sum(len(values) > 1 for values in target_by_surface.values()),
            "duplicateClaimIdsWithinRow": sum(len([c["claimId"] for c in row["claims"]]) != len({c["claimId"] for c in row["claims"]}) for row in rows),
        },
    }


def write_json(path: pathlib.Path, value) -> None:
    path.write_text(json.dumps(value, ensure_ascii=False, indent=2, sort_keys=True) + "\n", encoding="utf-8")


def _json_line(value: Mapping) -> str:
    return json.dumps(value, ensure_ascii=False, sort_keys=True) + "\n"


def write_jsonl_shards(directory: pathlib.Path, values: Sequence[Mapping]) -> tuple[list[dict], str]:
    """Write bounded text shards while preserving one canonical logical stream hash."""
    directory.mkdir(parents=True, exist_ok=True)
    for stale in directory.glob("part-*.jsonl"):
        stale.unlink()
    digest = hashlib.sha256()
    files = []
    for offset in range(0, len(values), SHARD_ROWS):
        shard_values = values[offset:offset + SHARD_ROWS]
        content = "".join(_json_line(value) for value in shard_values)
        digest.update(content.encode("utf-8"))
        path = directory / f"part-{offset // SHARD_ROWS:05d}.jsonl"
        path.write_text(content, encoding="utf-8")
        files.append({
            "path": str(path.name), "rows": len(shard_values),
            "bytes": path.stat().st_size, "sha256": sha256(path),
        })
    return files, digest.hexdigest()


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--matrix-train", type=pathlib.Path, required=True)
    parser.add_argument("--repair-train", type=pathlib.Path, required=True)
    parser.add_argument("--output-dir", type=pathlib.Path, required=True)
    parser.add_argument("--migration-commit", required=True)
    args = parser.parse_args()
    sources = [
        ("matrix-v2-train", args.matrix_train),
        ("v22a-repair-train", args.repair_train),
    ]
    source_rows = []
    source_inventory = []
    for source_id, path in sources:
        rows = load_train_jsonl(path, EXPECTED_SOURCE_SHA256[source_id])
        source_rows.extend((source_id, row) for row in rows)
        source_inventory.append({
            "sourceDatasetId": source_id, "sourcePath": path.name,
            "classification": "AUTHORIZED_TRAIN_SOURCE", "rows": len(rows),
            "claims": sum(len(row["claims"]) for row in rows),
            "languages": dict(sorted(Counter(row["language"] for row in rows).items())),
            "adultIntimacyRows": sum(bool(row.get("adultOnly")) for row in rows),
            "multiClaimRows": sum(len(row["claims"]) > 1 for row in rows),
            "schema": sorted(set(row.get("schemaVersion") for row in rows)),
            "sha256": EXPECTED_SOURCE_SHA256[source_id],
            "provenanceKinds": dict(sorted(Counter(row.get("provenance", {}).get("kind", "UNKNOWN") for row in rows).items())),
            "migrationEligibility": "NEEDS_REANNOTATION",
        })
    source_inventory.append({
        "sourceDatasetId": "p05-v2-train", "sourcePath": "not-opened-composite-gold-source",
        "classification": "HISTORICAL_REFERENCE_ONLY", "rows": 30, "claims": 45,
        "languages": {"en": 10, "es": 10, "it": 10},
        "sha256": "413f60ca17879ed9de440add7903b6e2abaebdfbbed6055b32c6e0b105cadfcd",
        "migrationEligibility": "EXCLUDED_PARTITION_NOT_DURABLY_SEPARATED",
        "reason": "TRAIN bytes cannot be opened independently without accessing forbidden partitions",
    })

    initial = classify_v2_rows([row for _, row in source_rows])
    migrated, records, unusable = [], [], []
    for source_id, row in source_rows:
        try:
            converted, record = migrate_row(row, source_id)
            migrated.append(converted); records.append(record)
        except UnusableRow as exc:
            unusable.append({
                "sourceDatasetId": source_id, "sourceRowId": row.get("id"),
                "sourceLanguage": row.get("language"), "finalLanguage": None,
                "migrationClass": "UNUSABLE", "finalDisposition": "UNUSABLE",
                "reason": str(exc),
            })
    migrated.sort(key=lambda row: row["id"])
    violations = [{"rowId": row["id"], "errors": errors} for row in migrated if (errors := validate_v3_row(row))]
    target_gate = target_builder_gate(migrated)
    stats = statistics(migrated, records, unusable)
    if violations or target_gate["errors"]:
        raise RuntimeError(f"V3 gate failed: violations={len(violations)} targetErrors={len(target_gate['errors'])}")

    output = args.output_dir
    output.mkdir(parents=True, exist_ok=True)
    dataset_shards, dataset_checksum = write_jsonl_shards(output / "train", migrated)
    inventory_path = output / "source-train-inventory.json"
    write_json(inventory_path, {"sources": source_inventory, "eligibleRows": len(source_rows), "forbiddenPartitionsOpened": False})
    provenance_values = [dict(record, recordType="MIGRATED") for record in records]
    provenance_values.extend(dict(record, recordType="UNUSABLE") for record in unusable)
    provenance_shards, provenance_checksum = write_jsonl_shards(output / "provenance", provenance_values)
    stats.update({"structuralViolations": len(violations), "targetBuilder": target_gate, "initialClassification": initial["counts"]})
    stats_path = output / "statistics.json"; write_json(stats_path, stats)
    manifest = {
        "contractVersion": CONTRACT_VERSION,
        "contractFingerprintSha256": contract_fingerprint(),
        "sourceDatasetId": [item[0] for item in sources],
        "sourceChecksums": EXPECTED_SOURCE_SHA256,
        "outputDatasetId": OUTPUT_DATASET_ID,
        "outputFormat": "canonical ordered JSONL shards",
        "outputFiles": [dict(item, path=f"train/{item['path']}") for item in dataset_shards],
        "outputChecksum": dataset_checksum,
        "provenanceFiles": [dict(item, path=f"provenance/{item['path']}") for item in provenance_shards],
        "provenanceChecksum": provenance_checksum,
        "migrationToolVersion": TOOL_VERSION,
        "migrationCommit": args.migration_commit,
        "rowCounts": {"eligibleSource": len(source_rows), "final": len(migrated), "retentionPercent": round(100 * len(migrated) / len(source_rows), 6)},
        "classificationCounts": initial["counts"],
        "finalDispositionCounts": {"REANNOTATED": len(migrated), "UNUSABLE": len(unusable)},
        "languageCounts": stats["languages"],
        "familyCounts": stats["familyCoverage"],
        "reannotationCounts": dict(sorted(Counter(reason for row in records for reason in row["reasonCodes"]).items())),
        "unusableCounts": dict(sorted(Counter(row["reason"] for row in unusable).items())),
        "guards": {"trainOnly": True, "canonicalDevUsed": False, "frozenDataRead": False, "trainingExecuted": False, "notProductionApproved": True},
        "files": {},
    }
    for path in (inventory_path, stats_path):
        manifest["files"][path.name] = {"sha256": sha256(path), "bytes": path.stat().st_size}
    manifest_path = output / "migration-manifest.json"; write_json(manifest_path, manifest)
    checksum_paths = [inventory_path, stats_path, manifest_path]
    checksum_paths.extend(sorted((output / "train").glob("part-*.jsonl")))
    checksum_paths.extend(sorted((output / "provenance").glob("part-*.jsonl")))
    sums = output / "SHA256SUMS"
    sums.write_text("".join(f"{sha256(path)}  {path.relative_to(output)}\n" for path in checksum_paths), encoding="utf-8")
    print(json.dumps({
        "dataset": str(output / "train"), "datasetSha256": dataset_checksum,
        "manifest": str(manifest_path), "manifestSha256": sha256(manifest_path),
        "rows": len(migrated), "claims": stats["claims"], "unusable": len(unusable),
        "violations": len(violations), "targetBuilder": target_gate,
    }, ensure_ascii=False, indent=2))


if __name__ == "__main__":
    main()
