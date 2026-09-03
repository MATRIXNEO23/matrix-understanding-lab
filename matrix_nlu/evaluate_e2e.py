#!/usr/bin/env python3
"""End-to-end Typed Claim benchmark with deterministic, auditable metrics.

Dev threshold selection and frozen-test evaluation are deliberately separate
commands.  The evaluator never changes model weights or the frozen datasets.
"""

from __future__ import annotations

import argparse
import json
import pathlib
from collections import defaultdict

from inference import MatrixNluRuntime, validate_claim


FIELDS = ("dialogueAct", "predicate", "subject", "target", "owner", "perspective",
          "polarity", "temporalRelation", "claimKind")
SPAN_FIELDS = ("sourceSpans", "objectSpan", "negationSpan", "temporalSpan")


def character_items(span):
    if span is None:
        return set()
    if span and isinstance(span[0], list):
        return {(index, "SPAN") for item in span for index in range(item[0], item[1])}
    return {(index, "SPAN") for index in range(span[0], span[1])}


def entity_items(entities):
    return {(index, item["type"]) for item in entities
            for index in range(item["span"][0], item["span"][1])}


def prf(gold, predicted):
    true_positive = len(gold & predicted)
    return true_positive, len(predicted - gold), len(gold - predicted)


def f1(counts):
    tp, fp, fn = counts
    return 0.0 if 2 * tp + fp + fn == 0 else 2 * tp / (2 * tp + fp + fn)


def expected_claim(claim, row):
    raw = {"labels": claim["labels"], "spans": claim["spans"], "confidence": 1.0}
    return validate_claim(raw, row["text"], row["context"], claim["sourceId"], 0.0)


def score_rows(rows, predictions):
    aggregate = defaultdict(int)
    languages = defaultdict(lambda: defaultdict(int))
    errors = []
    for row, predicted in zip(rows, predictions):
        gold = [expected_claim(claim, row) for claim in row["claims"]]
        actual = predicted["claims"]
        bucket = languages[row["language"]]
        aggregate["observations"] += 1
        bucket["observations"] += 1
        count_exact = len(gold) == len(actual)
        aggregate["claimCountExact"] += int(count_exact)
        bucket["claimCountExact"] += int(count_exact)
        aggregate["goldClaims"] += len(gold)
        bucket["goldClaims"] += len(gold)
        aggregate["predictedClaims"] += len(actual)
        bucket["predictedClaims"] += len(actual)
        row_errors = []
        for index in range(max(len(gold), len(actual))):
            if index >= len(gold) or index >= len(actual):
                row_errors.append({"claim": index, "kind": "CLAIM_COUNT"})
                continue
            expected, observed = gold[index], actual[index]
            all_exact = True
            for field in FIELDS:
                match = expected.get(field) == observed.get(field)
                aggregate["fieldCorrect"] += int(match)
                bucket["fieldCorrect"] += int(match)
                aggregate["fieldTotal"] += 1
                bucket["fieldTotal"] += 1
                if not match:
                    all_exact = False
                    row_errors.append({"claim": index, "kind": "FIELD", "field": field,
                                       "expected": expected.get(field), "actual": observed.get(field)})
            for field in SPAN_FIELDS:
                counts = prf(character_items(expected.get(field)), character_items(observed.get(field)))
                for suffix, value in zip(("Tp", "Fp", "Fn"), counts):
                    aggregate[f"span{suffix}"] += value
                    bucket[f"span{suffix}"] += value
                if expected.get(field) != observed.get(field):
                    all_exact = False
                    row_errors.append({"claim": index, "kind": "SPAN", "field": field,
                                       "expected": expected.get(field), "actual": observed.get(field)})
            counts = prf(entity_items(expected.get("entities", [])),
                         entity_items(observed.get("entities", [])))
            for suffix, value in zip(("Tp", "Fp", "Fn"), counts):
                aggregate[f"entity{suffix}"] += value
                bucket[f"entity{suffix}"] += value
            if expected.get("entities", []) != observed.get("entities", []):
                all_exact = False
                row_errors.append({"claim": index, "kind": "ENTITY",
                                   "expected": expected.get("entities", []),
                                   "actual": observed.get("entities", [])})
            aggregate["claimExact"] += int(all_exact)
            bucket["claimExact"] += int(all_exact)
            aggregate["pairedClaims"] += 1
            bucket["pairedClaims"] += 1
            aggregate["rejected"] += int(observed.get("status") != "VALID")
            bucket["rejected"] += int(observed.get("status") != "VALID")
            aggregate["abstained"] += int(observed.get("predicate") == "speech.unresolved")
            bucket["abstained"] += int(observed.get("predicate") == "speech.unresolved")
            aggregate["ownershipCorruption"] += int(
                observed.get("status") == "VALID" and
                (observed.get("subject") != expected.get("subject") or
                 observed.get("owner") != expected.get("owner") or
                 observed.get("perspective") != expected.get("perspective")))
            aggregate["worldTruthUpdates"] += int(observed.get("worldTruth", False))
        if row_errors:
            errors.append({"id": row["id"], "language": row["language"],
                           "text": row["text"], "errors": row_errors,
                           "gold": gold, "predicted": actual})

    def summarize(counts):
        observations = counts["observations"]
        paired = counts["pairedClaims"]
        return {
            "observations": observations,
            "goldClaims": counts["goldClaims"],
            "predictedClaims": counts["predictedClaims"],
            "claimCountExact": counts["claimCountExact"] / max(1, observations),
            "claimExact": counts["claimExact"] / max(1, counts["goldClaims"]),
            "fieldExact": counts["fieldCorrect"] / max(1, counts["fieldTotal"]),
            "spanF1": f1((counts["spanTp"], counts["spanFp"], counts["spanFn"])),
            "entityF1": f1((counts["entityTp"], counts["entityFp"], counts["entityFn"])),
            "rejectedRate": counts["rejected"] / max(1, paired),
            "abstentionRate": counts["abstained"] / max(1, paired),
            "ownershipCorruption": counts["ownershipCorruption"],
            "worldTruthUpdates": counts["worldTruthUpdates"],
        }
    return {"overall": summarize(aggregate),
            "byLanguage": {key: summarize(value) for key, value in sorted(languages.items())},
            "errorCount": len(errors)}, errors


def read_rows(path):
    with path.open(encoding="utf-8") as handle:
        return [json.loads(line) for line in handle if line.strip()]


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--bundle", type=pathlib.Path, required=True)
    parser.add_argument("--dataset", type=pathlib.Path, required=True)
    parser.add_argument("--split", choices=("dev", "test"), required=True)
    parser.add_argument("--threshold", type=float, required=True)
    parser.add_argument("--output-dir", type=pathlib.Path, required=True)
    args = parser.parse_args()
    rows = read_rows(args.dataset)
    if any(row["split"] != args.split for row in rows):
        raise SystemExit(f"dataset contains rows outside declared split {args.split}")
    runtime = MatrixNluRuntime(args.bundle, args.threshold)
    predictions = [runtime.interpret(row["text"], row["context"],
                                     f"benchmark:{row['id']}") for row in rows]
    metrics, errors = score_rows(rows, predictions)
    result = {"schemaVersion": "matrix.nlu.e2e-result.v1", "split": args.split,
              "threshold": args.threshold, "dataset": str(args.dataset), **metrics}
    args.output_dir.mkdir(parents=True, exist_ok=True)
    (args.output_dir / f"e2e-{args.split}.json").write_text(json.dumps(result, indent=2) + "\n")
    with (args.output_dir / f"e2e-{args.split}-errors.jsonl").open("w", encoding="utf-8") as handle:
        for error in errors:
            handle.write(json.dumps(error, ensure_ascii=False) + "\n")
    with (args.output_dir / f"e2e-{args.split}-predictions.jsonl").open("w", encoding="utf-8") as handle:
        for row, prediction in zip(rows, predictions):
            handle.write(json.dumps({"id": row["id"], "language": row["language"],
                                     "prediction": prediction}, ensure_ascii=False) + "\n")
    print(json.dumps(result, indent=2))


if __name__ == "__main__":
    main()
