"""End-to-end learned decoding and deterministic Matrix invariant validation."""

from __future__ import annotations

import json
import math
import pathlib

from labels import SEQUENCE_LABELS, TOKEN_LABELS
from model import build_model


def groups_from_tags(offsets, tags, begin_ids=(1,), inside_ids=(2,)):
    groups = []
    current = []
    for offset, tag in zip(offsets, tags):
        if offset[1] <= offset[0]:
            continue
        if tag in begin_ids:
            if current:
                groups.append(current)
            current = [offset]
        elif tag in inside_ids:
            if not current:
                current = [offset]
            else:
                current.append(offset)
        elif current:
            groups.append(current)
            current = []
    if current:
        groups.append(current)
    return [[group[0][0], group[-1][1]] for group in groups]


def scalar_span(offsets, tags):
    groups = groups_from_tags(offsets, tags)
    return groups[0] if groups else None


def entity_spans(offsets, tags):
    entities = []
    for entity_type, begin, inside in (("PERSON", 1, 2), ("LOCATION", 3, 4)):
        for span in groups_from_tags(offsets, tags, (begin,), (inside,)):
            entities.append({"span": span, "type": entity_type})
    return sorted(entities, key=lambda item: item["span"])


def find_known(mention: str | None, known: dict) -> str | None:
    if not mention:
        return None
    normalized = mention.casefold().strip(" ¿?.,;:!")
    for surface, identifier in known.items():
        if surface.casefold() == normalized:
            return identifier
    return None


def bind(referent: str, context: dict, subject: str | None,
         subject_mention: str | None) -> str | None:
    if referent == "NONE":
        return None
    if referent == "SELF":
        return "SELF"
    if referent == "SUBJECT":
        return subject
    if referent == "SPEAKER":
        return context["speaker"]
    if referent == "OBSERVER":
        return context["observer"]
    if referent == "KNOWN_ENTITY":
        return find_known(subject_mention, context.get("knownEntities", {}))
    if referent == "RECENT_ENTITY":
        recent = context.get("recentEntityRefs", [])
        return recent[0] if recent else None
    return None


def _overlaps(left: list[int] | None, right: list[int] | None) -> bool:
    return bool(left and right and left[0] < right[1] and right[0] < left[1])


def resolve_entity_referents(raw: dict, text: str, context: dict) -> list[dict]:
    """Attach categorical referents using already-learned roles and context.

    Entity type/span are learned outputs.  Referential identity is derived only
    when an entity overlaps a learned semantic role or exactly matches supplied
    context; otherwise it remains explicitly UNKNOWN.  This does not guess a
    person from capitalization or surface-language rules.
    """
    labels = raw["labels"]
    spans = raw["spans"]
    output = []
    for entity in spans.get("entities", []):
        resolved = dict(entity)
        if "referent" in resolved:
            output.append(resolved)
            continue
        entity_span = entity.get("span")
        if entity.get("type") == "LOCATION":
            referent = "LOCATION"
        elif _overlaps(entity_span, spans.get("subject")):
            referent = labels["subjectReferent"]
        elif (labels.get("predicate") == "identity.name" and
              _overlaps(entity_span, spans.get("object"))):
            referent = labels["subjectReferent"]
        else:
            mention = text[slice(*entity_span)] if entity_span else None
            referent = "KNOWN_ENTITY" if find_known(
                mention, context.get("knownEntities", {})) else "UNKNOWN"
        resolved["referent"] = referent
        output.append(resolved)
    return output


def validate_claim(raw: dict, text: str, context: dict, source_id: str,
                   threshold: float) -> dict:
    source = raw["spans"]["source"]
    diagnostics = []
    if not (0 <= source[0] < source[1] <= len(text)):
        return {"status": "REJECTED_INVARIANT", "diagnostics": ["invalid source span"],
                "worldTruth": False, "memoryAdmission": "REJECT"}
    subject_span = raw["spans"].get("subject")
    subject_mention = text[slice(*subject_span)] if subject_span else None
    subject = bind(raw["labels"]["subjectReferent"], context, None, subject_mention)
    if subject is None:
        diagnostics.append("subject referent could not be bound to supplied context")
    owner = bind(raw["labels"]["ownerReferent"], context, subject, subject_mention)
    perspective = bind(raw["labels"]["perspectiveReferent"], context, subject, subject_mention)
    target = bind(raw["labels"]["targetReferent"], context, subject, subject_mention)
    confidence = raw["confidence"]
    valid = subject is not None and owner is not None and perspective is not None
    if confidence < threshold:
        diagnostics.append(f"confidence {confidence:.6f} below threshold {threshold:.6f}")
    confident = confidence >= threshold
    admitted = valid and confident
    act = raw["labels"]["dialogueAct"]
    kind = raw["labels"]["claimKind"]
    memory = "BELIEF_CANDIDATE" if admitted and kind == "HYPOTHESIS" else (
        "MEMORY_CANDIDATE" if admitted and act in {"ASSERT", "CORRECT"} else "NO_ADMISSION")
    if not valid:
        memory = "REJECT"
    return {
        "status": ("REJECTED_INVARIANT" if not valid else
                   "VALID" if confident else "ABSTAINED_LOW_CONFIDENCE"),
        "speaker": context["speaker"], "subject": subject, "target": target,
        "owner": owner, "perspective": perspective,
        "dialogueAct": act,
        "predicate": raw["labels"]["predicate"] if admitted else "speech.unresolved",
        "objectSpan": raw["spans"].get("object"),
        "polarity": raw["labels"]["polarity"],
        "negationSpan": raw["spans"].get("negation"),
        "temporalRelation": raw["labels"]["temporalRelation"],
        "temporalSpan": raw["spans"].get("temporal"),
        "entities": resolve_entity_referents(raw, text, context),
        "claimKind": kind, "confidence": confidence,
        "sourceSpans": [source], "sourceIds": [source_id],
        "worldTruth": False, "memoryAdmission": memory,
        "diagnostics": diagnostics,
    }


class MatrixNluRuntime:
    def __init__(self, bundle: pathlib.Path, confidence_threshold: float = 0.5):
        import torch
        from transformers import AutoTokenizer
        self.torch = torch
        self.bundle = bundle
        result = json.loads((bundle / "training-result.json").read_text())
        labels = json.loads((bundle / "labels.json").read_text())
        spec = result["config"]["model"]
        self.max_length = int(result["config"]["maxLength"])
        self.tokenizer = AutoTokenizer.from_pretrained(bundle / "tokenizer", use_fast=True)
        self.model = build_model(spec["repository"], spec["revision"],
                                 len(labels["massiveIntents"]), len(labels["massiveSlots"]),
                                 result.get("studentLayers"))
        self.model.load_state_dict(torch.load(bundle / "model-state.pt", map_location="cpu", weights_only=True))
        self.model.eval()
        self.threshold = confidence_threshold

    def _run(self, text):
        encoded = self.tokenizer(text, max_length=self.max_length, padding="max_length", truncation=True,
                                 return_offsets_mapping=True, return_tensors="pt")
        offsets = encoded.pop("offset_mapping")[0].tolist()
        attention = encoded["attention_mask"][0].tolist()
        with self.torch.no_grad():
            output = self.model(encoded["input_ids"], encoded["attention_mask"])
        return offsets, attention, output

    def interpret(self, text: str, context: dict, source_id: str) -> dict:
        offsets, attention, first = self._run(text)
        boundary_probs = first["tokens"]["boundary"].softmax(-1)[0]
        boundary_tags = boundary_probs.argmax(-1).tolist()
        claim_spans = groups_from_tags(offsets, boundary_tags)
        raw_claims = []
        for source_start, source_end in claim_spans:
            claim_text = text[source_start:source_end]
            local_offsets, _, output = self._run(claim_text)
            labels = {}
            sequence_confidence = {}
            for head, values in SEQUENCE_LABELS.items():
                probabilities = output["sequence"][head].softmax(-1)[0]
                index = int(probabilities.argmax())
                labels[head] = values[index]
                sequence_confidence[head] = float(probabilities[index])
            token_tags = {}
            token_confidence = {}
            for head, logits in output["tokens"].items():
                probabilities = logits.softmax(-1)[0]
                token_tags[head] = probabilities.argmax(-1).tolist()
                real = [float(probabilities[index].max())
                        for index, (start, end) in enumerate(local_offsets) if end > start]
                token_confidence[head] = sum(real) / max(1, len(real))
            def globalize(span):
                return None if span is None else [span[0] + source_start, span[1] + source_start]
            entities = [{**entity, "span": globalize(entity["span"])}
                        for entity in entity_spans(local_offsets, token_tags["entity"])]
            raw_claims.append({"labels": labels,
                "spans": {"source": [source_start, source_end],
                          "object": globalize(scalar_span(local_offsets, token_tags["object"])),
                          "subject": globalize(scalar_span(local_offsets, token_tags["subject"])),
                          "negation": globalize(scalar_span(local_offsets, token_tags["negation"])),
                          "temporal": globalize(scalar_span(local_offsets, token_tags["temporal"])),
                          "entities": entities},
                "confidenceByHead": {"sequence": sequence_confidence,
                                     "tokens": token_confidence},
                "confidence": math.prod(max(value, 1e-9)
                                        for value in sequence_confidence.values()) **
                              (1 / len(sequence_confidence))})
        claims = [validate_claim(raw, text, context, source_id, self.threshold) for raw in raw_claims]
        real_token_confidence = [float(boundary_probs[index].max())
                                 for index, (start, end) in enumerate(offsets)
                                 if attention[index] and end > start]
        return {"input": text, "observationSourceId": source_id,
                "claimBoundarySpans": claim_spans,
                "boundaryConfidence": (sum(real_token_confidence) /
                                       max(1, len(real_token_confidence))),
                "rawClaims": raw_claims, "claims": claims, "worldTruthUpdates": 0}


class OnnxMatrixNluRuntime(MatrixNluRuntime):
    """Offline ONNX implementation sharing exactly the audited claim decoder."""

    def __init__(self, bundle: pathlib.Path, model_path: pathlib.Path,
                 confidence_threshold: float = 0.5):
        import onnxruntime as ort
        import torch
        from transformers import AutoTokenizer
        result = json.loads((bundle / "training-result.json").read_text())
        self.torch = torch
        self.bundle = bundle
        self.max_length = int(result["config"]["maxLength"])
        self.tokenizer = AutoTokenizer.from_pretrained(bundle / "tokenizer", use_fast=True,
                                                       local_files_only=True)
        self.session = ort.InferenceSession(str(model_path), providers=["CPUExecutionProvider"])
        self.output_names = tuple([f"token.{name}" for name in TOKEN_LABELS] +
                                  [f"sequence.{name}" for name in SEQUENCE_LABELS] +
                                  ["massive.intent", "massive.slot"])
        self.threshold = confidence_threshold

    def _run(self, text):
        import numpy as np
        encoded = self.tokenizer(text, max_length=self.max_length, padding="max_length",
                                 truncation=True, return_offsets_mapping=True,
                                 return_tensors="np")
        offsets = encoded.pop("offset_mapping")[0].tolist()
        attention = encoded["attention_mask"][0].tolist()
        observed = self.session.run(list(self.output_names), {
            "input_ids": encoded["input_ids"].astype(np.int64),
            "attention_mask": encoded["attention_mask"].astype(np.int64),
        })
        values = iter(observed)
        output = {
            "tokens": {name: self.torch.from_numpy(next(values)) for name in TOKEN_LABELS},
            "sequence": {name: self.torch.from_numpy(next(values)) for name in SEQUENCE_LABELS},
            "massive_intent": self.torch.from_numpy(next(values)),
            "massive_slot": self.torch.from_numpy(next(values)),
        }
        return offsets, attention, output
