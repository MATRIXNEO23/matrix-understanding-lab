#!/usr/bin/env python3
"""Resolve immutable model revisions and mobile-relevant facts without training.

The probe deliberately downloads only metadata/config/tokenizer assets. Weight
sizes come from Hub metadata, so a rejected 100+ MB model is never pulled into
the runner merely to prove that it is too large.
"""

from __future__ import annotations

import argparse
import hashlib
import json
import pathlib
import time
from collections import Counter

SAMPLES = {
    "it": (
        "Non amo i locali affollati",
        "Ho 44 anni e vivo a San Vendemiano",
        "Forse Luna non sarà a New York domani",
    ),
    "en": (
        "I do not like crowded venues",
        "I am 44 years old and I live in San Vendemiano",
        "Maybe Luna will not be in New York tomorrow",
    ),
    "es": (
        "No me gustan los locales llenos",
        "Tengo 44 años y vivo en San Vendemiano",
        "Quizá Luna no estará en Nueva York mañana",
    ),
}


def sha256(path: pathlib.Path) -> str:
    digest = hashlib.sha256()
    with path.open("rb") as handle:
        for chunk in iter(lambda: handle.read(1024 * 1024), b""):
            digest.update(chunk)
    return digest.hexdigest()


def weight_bytes(siblings) -> int:
    extensions = (".safetensors", ".bin", ".onnx")
    preferred = [s for s in siblings if s.rfilename.endswith("model.safetensors")]
    if not preferred:
        preferred = [s for s in siblings if s.rfilename.endswith("pytorch_model.bin")]
    if not preferred:
        preferred = [s for s in siblings if s.rfilename.endswith(extensions)]
    return sum((s.size or 0) for s in preferred)


def tokenize_probe(tokenizer) -> dict:
    rows = {}
    for language, samples in SAMPLES.items():
        lang_rows = []
        for text in samples:
            tokens = tokenizer.tokenize(text)
            unk = sum(token == tokenizer.unk_token for token in tokens)
            lang_rows.append({
                "text": text,
                "tokens": tokens,
                "tokenCount": len(tokens),
                "unknownCount": unk,
                "charactersPerToken": round(len(text) / max(1, len(tokens)), 4),
            })
        rows[language] = lang_rows
    return rows


def probe(candidate: dict, api) -> dict:
    from transformers import AutoConfig, AutoTokenizer

    repo = candidate["repository"]
    info = api.model_info(repo, files_metadata=True)
    revision = info.sha
    config = AutoConfig.from_pretrained(repo, revision=revision, trust_remote_code=False)
    tokenizer = AutoTokenizer.from_pretrained(repo, revision=revision, use_fast=True,
                                              trust_remote_code=False)
    card = info.card_data.to_dict() if info.card_data else {}
    siblings = list(info.siblings or [])
    weights = weight_bytes(siblings)
    hidden = getattr(config, "hidden_size", getattr(config, "dim", None))
    layers = getattr(config, "num_hidden_layers", getattr(config, "n_layers", None))
    heads = getattr(config, "num_attention_heads", getattr(config, "n_heads", None))
    vocab = getattr(config, "vocab_size", len(tokenizer))
    license_value = card.get("license")
    result = {
        **candidate,
        "resolvedRevision": revision,
        "licenseDeclared": license_value,
        "licenseMatchesExpectation": license_value == candidate["expectedLicense"],
        "library": getattr(config, "model_type", type(config).__name__),
        "architecture": list(getattr(config, "architectures", []) or []),
        "hiddenSize": hidden,
        "layers": layers,
        "attentionHeads": heads,
        "vocabSize": vocab,
        "hubWeightBytes": weights,
        "estimatedDynamicInt8WeightBytes": weights // 4 if weights else None,
        "languagesDeclared": card.get("language"),
        "tokenization": tokenize_probe(tokenizer),
        "files": [
            {"name": s.rfilename, "bytes": s.size}
            for s in siblings
            if s.rfilename.endswith((".json", ".txt", ".model", ".safetensors", ".bin", ".onnx"))
        ],
    }
    return result


def decide(rows: list[dict]) -> dict:
    by_role = {row["role"]: row for row in rows}
    primary = by_role["PRIMARY_PROBE"]
    reasons = []
    if "error" in primary:
        reasons.append(f"primary probe failed: {primary['errorType']}: {primary['error']}")
        return {
            "selectedForTraining": None, "selectedRevision": None,
            "blockingReasons": reasons,
            "referenceProbeErrors": [row["id"] for row in rows if "error" in row and row is not primary],
            "note": "Selection authorizes lab training only; Android PSS and quality remain measured gates.",
        }
    if not primary["licenseMatchesExpectation"]:
        reasons.append("declared license does not match the reviewed expectation")
    for language in ("it", "en", "es"):
        unknowns = sum(x["unknownCount"] for x in primary["tokenization"][language])
        if unknowns:
            reasons.append(f"{language} tokenizer emitted {unknowns} unknown tokens")
    estimated = primary.get("estimatedDynamicInt8WeightBytes")
    if estimated and estimated > 80 * 1024 * 1024:
        reasons.append("estimated INT8 weights exceed the 80 MiB investigation threshold")
    return {
        "selectedForTraining": None if reasons else primary["repository"],
        "selectedRevision": None if reasons else primary["resolvedRevision"],
        "blockingReasons": reasons,
        "referenceProbeErrors": [row["id"] for row in rows if "error" in row and row is not primary],
        "note": "Selection authorizes lab training only; Android PSS and quality remain measured gates.",
    }


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--candidates", type=pathlib.Path, default=pathlib.Path("matrix_nlu/candidates.json"))
    parser.add_argument("--output", type=pathlib.Path, default=pathlib.Path("build/matrix-nlu/candidate-probe.json"))
    args = parser.parse_args()
    source_bytes = args.candidates.read_bytes()
    source = json.loads(source_bytes)
    from huggingface_hub import HfApi

    api = HfApi()
    rows = []
    for candidate in source["candidates"]:
        try:
            rows.append(probe(candidate, api))
        except Exception as error:  # preserve every completed probe in the artifact
            rows.append({**candidate, "errorType": type(error).__name__, "error": str(error)})
    payload = {
        "schemaVersion": "matrix.nlu.candidate-probe.v1",
        "generatedUnixSeconds": int(time.time()),
        "candidateSpecSha256": hashlib.sha256(source_bytes).hexdigest(),
        "targetLanguages": source["targetLanguages"],
        "candidates": rows,
        "decision": decide(rows),
    }
    args.output.parent.mkdir(parents=True, exist_ok=True)
    args.output.write_text(json.dumps(payload, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")
    print(json.dumps(payload["decision"], indent=2))
    if any("error" in row for row in rows):
        raise SystemExit("one or more candidate probes failed; inspect preserved artifact")


if __name__ == "__main__":
    main()
