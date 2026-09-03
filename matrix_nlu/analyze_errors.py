#!/usr/bin/env python3
"""Deterministic residual taxonomy; it reports evidence and never tunes from test."""

from __future__ import annotations

import argparse
import collections
import json
import pathlib


def classify(error: dict) -> str:
    if error["kind"] == "CLAIM_COUNT":
        return "MODEL_CLAIM_SEGMENTATION"
    if error["kind"] == "ENTITY":
        return "MODEL_ENTITY_RESOLUTION"
    if error["kind"] == "SPAN":
        return "MODEL_SPAN_DECODING"
    if error["kind"] == "FIELD" and error.get("field") in {
            "subject", "owner", "perspective", "target"}:
        return "AUTHORITY_OR_REFERENT_DECODING"
    if error["kind"] == "FIELD":
        return "MODEL_SEMANTIC_CLASSIFICATION"
    return "NON_DETERMINATO"


def analyze(path: pathlib.Path) -> dict:
    counts = collections.Counter()
    languages = collections.Counter()
    examples = collections.defaultdict(list)
    observations = 0
    with path.open(encoding="utf-8") as handle:
        for line in handle:
            if not line.strip():
                continue
            row = json.loads(line)
            observations += 1
            for error in row["errors"]:
                family = classify(error)
                counts[family] += 1
                languages[(row["language"], family)] += 1
                if len(examples[family]) < 10:
                    examples[family].append({"id": row["id"], "language": row["language"],
                                             "text": row["text"], "error": error})
    return {
        "schemaVersion": "matrix.nlu.error-analysis.v1",
        "source": str(path),
        "failedObservations": observations,
        "classification": "evidence taxonomy; causal attribution requires train/dev reproduction",
        "families": [{"family": family, "count": count,
                      "byLanguage": {language: languages[(language, family)]
                                     for language in ("it", "en", "es")},
                      "examples": examples[family]}
                     for family, count in sorted(counts.items())],
        "fixPolicy": "Do not patch frozen examples. Reproduce family on train/dev, classify cause, patch candidate, run full regression/property suite, accept only without regression.",
    }


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--errors", type=pathlib.Path, required=True)
    parser.add_argument("--output", type=pathlib.Path, required=True)
    args = parser.parse_args()
    result = analyze(args.errors)
    args.output.parent.mkdir(parents=True, exist_ok=True)
    args.output.write_text(json.dumps(result, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")
    print(json.dumps(result, indent=2, ensure_ascii=False))


if __name__ == "__main__":
    main()
