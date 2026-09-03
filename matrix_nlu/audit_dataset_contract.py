#!/usr/bin/env python3
"""Audit Matrix-NLU train/dev annotation contracts without reading frozen test.

This tool reports structural annotation conventions.  It never rewrites data,
learns thresholds, or proposes surface-language runtime rules.
"""

from __future__ import annotations

import argparse
import collections
import hashlib
import json
import pathlib


ALLOWED_SPLITS = frozenset({"train", "dev"})
LANGUAGES = ("it", "en", "es")


def read_dataset(name: str, path: pathlib.Path) -> tuple[list[dict], dict]:
    data = path.read_bytes()
    rows = [json.loads(line) for line in data.decode("utf-8").splitlines()
            if line.strip()]
    observed_splits = sorted({row.get("split") for row in rows})
    forbidden = sorted(set(observed_splits) - ALLOWED_SPLITS)
    if forbidden:
        raise ValueError(
            f"dataset {name!r} contains forbidden split(s) {forbidden}; "
            "contract audit is train/dev only"
        )
    return rows, {
        "name": name,
        "path": str(path),
        "sha256": hashlib.sha256(data).hexdigest(),
        "bytes": len(data),
        "rows": len(rows),
        "claims": sum(len(row["claims"]) for row in rows),
        "splits": dict(sorted(collections.Counter(
            row["split"] for row in rows).items())),
        "languages": {language: sum(row["language"] == language for row in rows)
                      for language in LANGUAGES},
    }


def span_inside(inner, outer) -> bool:
    return inner is not None and outer is not None and (
        outer[0] <= inner[0] < inner[1] <= outer[1]
    )


def negation_shape(claim: dict) -> str:
    source = claim["spans"]["source"]
    negation = claim["spans"]["negation"]
    obj = claim["spans"]["object"]
    if negation is None:
        return "ABSENT"
    if negation == source:
        return "FULL_SOURCE"
    if obj is not None and negation == obj:
        return "OBJECT_ONLY"
    if obj is not None and span_inside(obj, negation):
        return "OBJECT_SUPERSET"
    if obj is not None and not (negation[0] < obj[1] and obj[0] < negation[1]):
        return "DISJOINT_FROM_OBJECT"
    return "OTHER_PARTIAL"


def _counter_rows(counter: collections.Counter) -> list[dict]:
    return [{"values": list(key), "count": value}
            for key, value in sorted(counter.items())]


def audit(named_datasets: list[tuple[str, pathlib.Path]]) -> dict:
    manifests = []
    negation = collections.Counter()
    temporal = collections.Counter()
    semantic_span_failures = []
    signature_shapes: dict[tuple[str, str], set[str]] = collections.defaultdict(set)
    exact_inputs: dict[tuple[str, str, str], list[dict]] = collections.defaultdict(list)

    for dataset_name, path in named_datasets:
        rows, manifest = read_dataset(dataset_name, path)
        manifests.append(manifest)
        for row in rows:
            provenance = row.get("provenance", {}).get("kind", "UNKNOWN")
            exact_inputs[(row["language"], row["text"].casefold(),
                          json.dumps(row.get("context", {}), sort_keys=True))].append({
                "dataset": dataset_name,
                "id": row["id"],
                "claims": [{"labels": claim["labels"], "spans": claim["spans"]}
                           for claim in row["claims"]],
            })
            for index, claim in enumerate(row["claims"]):
                spans = claim["spans"]
                source = spans["source"]
                for field in ("object", "subject", "negation", "temporal"):
                    value = spans.get(field)
                    if value is not None and not span_inside(value, source):
                        semantic_span_failures.append({
                            "dataset": dataset_name, "id": row["id"],
                            "claimIndex": index, "field": field,
                            "source": source, "span": value,
                        })
                for entity_index, entity in enumerate(spans.get("entities", [])):
                    if not span_inside(entity["span"], source):
                        semantic_span_failures.append({
                            "dataset": dataset_name, "id": row["id"],
                            "claimIndex": index,
                            "field": f"entities[{entity_index}]",
                            "source": source, "span": entity["span"],
                        })

                labels = claim["labels"]
                if labels["polarity"] == "NEGATIVE":
                    shape = negation_shape(claim)
                    signature = (labels["predicate"], labels["polarity"])
                    signature_shapes[signature].add(shape)
                    negation[(dataset_name, row["split"], provenance,
                              row["language"], labels["predicate"], shape)] += 1

                temporal[(dataset_name, row["split"], provenance,
                          row["language"], labels["temporalRelation"],
                          "PRESENT" if spans.get("temporal") else "ABSENT")] += 1

    exact_conflicts = []
    for (language, text, context), occurrences in sorted(exact_inputs.items()):
        if len({item["dataset"] for item in occurrences}) < 2:
            continue
        signatures = {json.dumps(item["claims"], sort_keys=True)
                      for item in occurrences}
        if len(signatures) > 1:
            exact_conflicts.append({
                "language": language,
                "text": text,
                "context": json.loads(context),
                "occurrences": occurrences,
            })

    conflicts = []
    if exact_conflicts:
        conflicts.append({
            "kind": "EXACT_INPUT_ANNOTATION_CONFLICT",
            "count": len(exact_conflicts),
            "byLanguage": {language: sum(item["language"] == language
                                         for item in exact_conflicts)
                           for language in LANGUAGES},
            "impact": "the same model input/context has more than one gold target",
            "resolution": "canonical annotation versioning required before retraining",
        })
    for signature, shapes in sorted(signature_shapes.items()):
        non_absent = shapes - {"ABSENT"}
        if "FULL_SOURCE" in non_absent and len(non_absent) > 1:
            conflicts.append({
                "kind": "NEGATION_SCOPE_CONVENTION_CONFLICT",
                "predicate": signature[0],
                "polarity": signature[1],
                "observedShapes": sorted(shapes),
                "impact": "one token head is supervised with incompatible span targets",
                "resolution": "canonical annotation versioning required before rewriting gold",
            })

    return {
        "schemaVersion": "matrix.nlu.dataset-contract-audit.v1",
        "scope": {
            "allowedSplits": sorted(ALLOWED_SPLITS),
            "frozenTestRead": False,
            "policy": "diagnostic only; no tuning, rewriting, or runtime rules",
        },
        "datasets": manifests,
        "semanticSpanContainment": {
            "failureCount": len(semantic_span_failures),
            "failures": semantic_span_failures[:100],
        },
        "exactInputAnnotationConflicts": {
            "count": len(exact_conflicts),
            "byLanguage": {language: sum(item["language"] == language
                                         for item in exact_conflicts)
                           for language in LANGUAGES},
            "examples": exact_conflicts[:100],
        },
        "negativeClaimScope": {
            "dimensions": ["dataset", "split", "provenance", "language",
                           "predicate", "shape"],
            "counts": _counter_rows(negation),
        },
        "temporalEvidence": {
            "dimensions": ["dataset", "split", "provenance", "language",
                           "temporalRelation", "spanState"],
            "counts": _counter_rows(temporal),
            "note": "absence can be legitimate for implicit tense; this section is evidence, not an automatic defect",
        },
        "contractConflicts": conflicts,
        "decisionRequired": bool(conflicts),
    }


def has_critical_findings(result: dict) -> bool:
    return bool(result["decisionRequired"] or
                result["semanticSpanContainment"]["failureCount"] or
                result["exactInputAnnotationConflicts"]["count"])


def parse_dataset(value: str) -> tuple[str, pathlib.Path]:
    if "=" not in value:
        raise argparse.ArgumentTypeError("expected NAME=PATH")
    name, raw_path = value.split("=", 1)
    if not name or not raw_path:
        raise argparse.ArgumentTypeError("expected non-empty NAME=PATH")
    return name, pathlib.Path(raw_path)


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--dataset", action="append", type=parse_dataset,
                        required=True, help="repeatable NAME=PATH; train/dev only")
    parser.add_argument("--output", type=pathlib.Path, required=True)
    parser.add_argument("--fail-on-conflict", action="store_true",
                        help="return nonzero after preserving a report with critical findings")
    args = parser.parse_args()
    result = audit(args.dataset)
    args.output.parent.mkdir(parents=True, exist_ok=True)
    args.output.write_text(json.dumps(result, indent=2, ensure_ascii=False) + "\n",
                           encoding="utf-8")
    print(json.dumps(result, indent=2, ensure_ascii=False))
    return 2 if args.fail_on_conflict and has_critical_findings(result) else 0


if __name__ == "__main__":
    raise SystemExit(main())
