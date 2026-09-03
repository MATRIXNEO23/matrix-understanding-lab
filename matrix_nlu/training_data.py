"""Token alignment and datasets for shared Matrix/MASSIVE training."""

from __future__ import annotations

import json
import pathlib

from labels import SEQUENCE_IDS, TOKEN_IDS


IGNORE = -100


def read_jsonl(paths) -> list[dict]:
    rows = []
    for path in paths:
        with pathlib.Path(path).open(encoding="utf-8") as handle:
            rows.extend(json.loads(line) for line in handle if line.strip())
    return rows


def overlapping_token_indices(offsets, span):
    if span is None:
        return []
    start, end = span
    return [index for index, (left, right) in enumerate(offsets)
            if right > left and left < end and right > start]


def bio(offsets, spans, begin: int = 1, inside: int = 2):
    labels = [IGNORE if right <= left else 0 for left, right in offsets]
    for span in spans:
        indices = overlapping_token_indices(offsets, span)
        for position, index in enumerate(indices):
            labels[index] = begin if position == 0 else inside
    return labels


def entity_bio(offsets, entities):
    labels = [IGNORE if right <= left else 0 for left, right in offsets]
    for entity in entities:
        if entity["type"] == "PERSON":
            begin, inside = TOKEN_IDS["entity"]["B-PERSON"], TOKEN_IDS["entity"]["I-PERSON"]
        elif entity["type"] == "LOCATION":
            begin, inside = TOKEN_IDS["entity"]["B-LOCATION"], TOKEN_IDS["entity"]["I-LOCATION"]
        else:
            continue
        for position, index in enumerate(overlapping_token_indices(offsets, entity["span"])):
            labels[index] = begin if position == 0 else inside
    return labels


def encode(tokenizer, text: str, max_length: int):
    return tokenizer(text, max_length=max_length, padding="max_length", truncation=True,
                     return_offsets_mapping=True)


def empty_token_labels(length: int):
    return {head: [IGNORE] * length for head in TOKEN_IDS}


def empty_sequence_labels():
    return {head: IGNORE for head in SEQUENCE_IDS}


def matrix_examples(rows: list[dict], tokenizer, max_length: int) -> list[dict]:
    examples = []
    for row in rows:
        encoded = encode(tokenizer, row["text"], max_length)
        offsets = encoded.pop("offset_mapping")
        boundary = empty_token_labels(max_length)
        boundary["boundary"] = bio(offsets, [claim["spans"]["source"] for claim in row["claims"]])
        examples.append({"input_ids": encoded["input_ids"],
                         "attention_mask": encoded["attention_mask"],
                         "token_labels": boundary, "sequence_labels": empty_sequence_labels(),
                         "aux_intent": IGNORE, "aux_slot": [IGNORE] * max_length,
                         "kind": "boundary", "rowId": row["id"], "language": row["language"],
                         "family": "+".join(claim["family"] for claim in row["claims"])})
        for claim_index, claim in enumerate(row["claims"]):
            source_start, source_end = claim["spans"]["source"]
            claim_text = row["text"][source_start:source_end]
            encoded = encode(tokenizer, claim_text, max_length)
            offsets = encoded.pop("offset_mapping")
            def local(value):
                return None if value is None else [value[0] - source_start, value[1] - source_start]
            tokens = empty_token_labels(max_length)
            tokens["object"] = bio(offsets, [local(claim["spans"]["object"])]) if claim["spans"]["object"] else bio(offsets, [])
            tokens["subject"] = bio(offsets, [local(claim["spans"]["subject"])]) if claim["spans"]["subject"] else bio(offsets, [])
            tokens["negation"] = bio(offsets, [local(claim["spans"]["negation"])]) if claim["spans"]["negation"] else bio(offsets, [])
            tokens["temporal"] = bio(offsets, [local(claim["spans"]["temporal"])]) if claim["spans"]["temporal"] else bio(offsets, [])
            entities = [{**entity, "span": local(entity["span"])} for entity in claim["spans"]["entities"]]
            tokens["entity"] = entity_bio(offsets, entities)
            sequence = {head: SEQUENCE_IDS[head][claim["labels"][head]] for head in SEQUENCE_IDS}
            examples.append({"input_ids": encoded["input_ids"],
                             "attention_mask": encoded["attention_mask"],
                             "token_labels": tokens, "sequence_labels": sequence,
                             "aux_intent": IGNORE, "aux_slot": [IGNORE] * max_length,
                             "kind": "claim", "rowId": f"{row['id']}:{claim_index}",
                             "language": row["language"], "family": claim["family"]})
    return examples


def massive_slot_vocab(slot_types: list[str]):
    labels = ["O"]
    for value in slot_types:
        labels.extend((f"B-{value}", f"I-{value}"))
    return labels


def massive_examples(rows: list[dict], tokenizer, max_length: int,
                     intent_ids: dict[str, int], slot_types: list[str]) -> list[dict]:
    slot_ids = {value: index for index, value in enumerate(massive_slot_vocab(slot_types))}
    output = []
    for row in rows:
        encoded = encode(tokenizer, row["text"], max_length)
        offsets = encoded.pop("offset_mapping")
        labels = [IGNORE if right <= left else 0 for left, right in offsets]
        for slot in row["slots"]:
            indices = overlapping_token_indices(offsets, slot["span"])
            for position, index in enumerate(indices):
                prefix = "B" if position == 0 else "I"
                labels[index] = slot_ids[f"{prefix}-{slot['type']}"]
        output.append({"input_ids": encoded["input_ids"],
                       "attention_mask": encoded["attention_mask"],
                       "token_labels": empty_token_labels(max_length),
                       "sequence_labels": empty_sequence_labels(),
                       "aux_intent": intent_ids[row["intent"]], "aux_slot": labels,
                       "kind": "massive", "rowId": row["id"], "language": row["language"],
                       "family": row["scenario"]})
    return output


class ExampleDataset:
    def __init__(self, examples):
        self.examples = examples

    def __len__(self):
        return len(self.examples)

    def __getitem__(self, index):
        import torch
        row = self.examples[index]
        return {
            "input_ids": torch.tensor(row["input_ids"], dtype=torch.long),
            "attention_mask": torch.tensor(row["attention_mask"], dtype=torch.long),
            "token_labels": {k: torch.tensor(v, dtype=torch.long) for k, v in row["token_labels"].items()},
            "sequence_labels": {k: torch.tensor(v, dtype=torch.long) for k, v in row["sequence_labels"].items()},
            "aux_intent": torch.tensor(row["aux_intent"], dtype=torch.long),
            "aux_slot": torch.tensor(row["aux_slot"], dtype=torch.long),
        }
