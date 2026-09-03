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

from inference import MatrixNluRuntime, OnnxMatrixNluRuntime, validate_claim


FIELDS = ("dialogueAct", "predicate", "subject", "target", "owner", "perspective",
          "polarity", "temporalRelation", "claimKind")
SPAN_FIELDS = ("sourceSpans", "objectSpan", "negationSpan", "temporalSpan")
CRITICAL_FAMILIES = ("negation", "request", "goal", "correction", "temporality",
                     "referents", "thirdParty", "multiClaim")


def critical_families(row):
    claims = row["claims"]
    labels = [claim["labels"] for claim in claims]
    spans = [claim["spans"] for claim in claims]
    families = set()
    if any(item.get("polarity") == "NEGATIVE" or span.get("negation") is not None
           for item, span in zip(labels, spans)):
        families.add("negation")
    if any(item.get("dialogueAct") == "REQUEST" for item in labels):
        families.add("request")
    if any(str(item.get("predicate", "")).startswith("goal.") for item in labels):
        families.add("goal")
    if any(item.get("dialogueAct") in {"CORRECT", "CORRECTION"} for item in labels):
        families.add("correction")
    if any(item.get("temporalRelation") != "ATEMPORAL" or span.get("temporal") is not None
           for item, span in zip(labels, spans)):
        families.add("temporality")
    complex_referents = {"KNOWN_ENTITY", "UNKNOWN", "THIRD_PARTY", "OTHER", "OBSERVER"}
    if any(span.get("entities") or
           item.get("subjectReferent") != "SPEAKER" or
           item.get("targetReferent") != "NONE" or
           item.get("ownerReferent") not in {"SUBJECT", "SPEAKER", "NONE"} or
           item.get("perspectiveReferent") != "SPEAKER"
           for item, span in zip(labels, spans)):
        families.add("referents")
    if any(complex_referents.intersection({str(item.get(key)) for key in
           ("subjectReferent", "targetReferent", "ownerReferent", "perspectiveReferent")}) or
           any(entity.get("type") == "PERSON" and entity.get("referent") != "SPEAKER"
               for entity in span.get("entities", []))
           for item, span in zip(labels, spans)):
        families.add("thirdParty")
    if len(claims) > 1:
        families.add("multiClaim")
    return families


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


def calibration_summary(items, bin_count=10):
    if not items:
        return {"count": 0, "meanConfidence": 0.0, "brier": 0.0,
                "expectedCalibrationError": 0.0, "bins": []}
    bins = []
    ece = 0.0
    for index in range(bin_count):
        lower, upper = index / bin_count, (index + 1) / bin_count
        selected = [(confidence, correct) for confidence, correct in items
                    if lower <= confidence <= upper and
                    (index == bin_count - 1 or confidence < upper)]
        if not selected:
            continue
        confidence = sum(item[0] for item in selected) / len(selected)
        accuracy = sum(item[1] for item in selected) / len(selected)
        ece += len(selected) / len(items) * abs(confidence - accuracy)
        bins.append({"lower": lower, "upper": upper, "count": len(selected),
                     "meanConfidence": confidence, "accuracy": accuracy})
    return {"count": len(items),
            "meanConfidence": sum(item[0] for item in items) / len(items),
            "brier": sum((item[0] - item[1]) ** 2 for item in items) / len(items),
            "expectedCalibrationError": ece, "bins": bins}


def expected_claim(claim, row):
    raw = {"labels": claim["labels"], "spans": claim["spans"], "confidence": 1.0}
    return validate_claim(raw, row["text"], row["context"], claim["sourceId"], 0.0)


def score_rows(rows, predictions):
    aggregate = defaultdict(int)
    languages = defaultdict(lambda: defaultdict(int))
    calibration = []
    language_calibration = defaultdict(list)
    critical = defaultdict(lambda: defaultdict(int))
    critical_languages = defaultdict(lambda: defaultdict(lambda: defaultdict(int)))
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
                aggregate[f"field.{field}.correct"] += int(match)
                bucket[f"field.{field}.correct"] += int(match)
                aggregate[f"field.{field}.total"] += 1
                bucket[f"field.{field}.total"] += 1
                if not match:
                    all_exact = False
                    row_errors.append({"claim": index, "kind": "FIELD", "field": field,
                                       "expected": expected.get(field), "actual": observed.get(field)})
            for field in SPAN_FIELDS:
                counts = prf(character_items(expected.get(field)), character_items(observed.get(field)))
                for suffix, value in zip(("Tp", "Fp", "Fn"), counts):
                    aggregate[f"span{suffix}"] += value
                    bucket[f"span{suffix}"] += value
                    aggregate[f"span.{field}.{suffix}"] += value
                    bucket[f"span.{field}.{suffix}"] += value
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
            is_valid = observed.get("status") == "VALID"
            aggregate["validClaims"] += int(is_valid)
            bucket["validClaims"] += int(is_valid)
            aggregate["validExact"] += int(is_valid and all_exact)
            bucket["validExact"] += int(is_valid and all_exact)
            confidence = max(0.0, min(1.0, float(observed.get("confidence", 0.0))))
            calibration.append((confidence, int(all_exact)))
            language_calibration[row["language"]].append((confidence, int(all_exact)))
            aggregate["pairedClaims"] += 1
            bucket["pairedClaims"] += 1
            aggregate["rejected"] += int(observed.get("status") != "VALID")
            bucket["rejected"] += int(observed.get("status") != "VALID")
            aggregate["abstained"] += int(observed.get("predicate") == "speech.unresolved")
            bucket["abstained"] += int(observed.get("predicate") == "speech.unresolved")
            ownership_corruption = int(
                observed.get("status") == "VALID" and
                (observed.get("subject") != expected.get("subject") or
                 observed.get("owner") != expected.get("owner") or
                 observed.get("perspective") != expected.get("perspective")))
            aggregate["ownershipCorruption"] += ownership_corruption
            bucket["ownershipCorruption"] += ownership_corruption
            aggregate["worldTruthUpdates"] += int(observed.get("worldTruth", False))
        exact_set = count_exact and not row_errors
        aggregate["exactClaimSet"] += int(exact_set)
        bucket["exactClaimSet"] += int(exact_set)
        for family in critical_families(row):
            critical[family]["observations"] += 1
            critical[family]["exactClaimSet"] += int(exact_set)
            critical_languages[family][row["language"]]["observations"] += 1
            critical_languages[family][row["language"]]["exactClaimSet"] += int(exact_set)
        if row_errors:
            errors.append({"id": row["id"], "language": row["language"],
                           "text": row["text"], "errors": row_errors,
                           "gold": gold, "predicted": actual})

    def summarize(counts):
        observations = counts["observations"]
        paired = counts["pairedClaims"]
        result = {
            "observations": observations,
            "goldClaims": counts["goldClaims"],
            "predictedClaims": counts["predictedClaims"],
            "claimCountExact": counts["claimCountExact"] / max(1, observations),
            "exactClaimSet": counts["exactClaimSet"] / max(1, observations),
            "claimExact": counts["claimExact"] / max(1, counts["goldClaims"]),
            "fieldExact": counts["fieldCorrect"] / max(1, counts["fieldTotal"]),
            "spanF1": f1((counts["spanTp"], counts["spanFp"], counts["spanFn"])),
            "entityF1": f1((counts["entityTp"], counts["entityFp"], counts["entityFn"])),
            "rejectedRate": counts["rejected"] / max(1, paired),
            "abstentionRate": counts["abstained"] / max(1, paired),
            "validCoverage": counts["validClaims"] / max(1, counts["goldClaims"]),
            "validSelectiveAccuracy": counts["validExact"] / max(1, counts["validClaims"]),
            "ownershipCorruption": counts["ownershipCorruption"],
            "worldTruthUpdates": counts["worldTruthUpdates"],
        }
        result["fieldAccuracy"] = {
            field: counts[f"field.{field}.correct"] / max(1, counts[f"field.{field}.total"])
            for field in FIELDS
        }
        result["spanF1ByField"] = {
            field: f1((counts[f"span.{field}.Tp"], counts[f"span.{field}.Fp"],
                       counts[f"span.{field}.Fn"])) for field in SPAN_FIELDS
        }
        result["predicateAccuracy"] = result["fieldAccuracy"]["predicate"]
        result["negationF1"] = result["spanF1ByField"]["negationSpan"]
        result["temporalAccuracy"] = result["fieldAccuracy"]["temporalRelation"]
        return result
    overall = summarize(aggregate)
    overall["calibration"] = calibration_summary(calibration)
    by_language = {}
    for key, value in sorted(languages.items()):
        by_language[key] = summarize(value)
        by_language[key]["calibration"] = calibration_summary(language_calibration[key])
    worst_field = min((value["fieldExact"] for value in by_language.values()), default=0.0)
    worst_claim_set = min((value["exactClaimSet"] for value in by_language.values()), default=0.0)
    by_critical_family = {}
    for family in CRITICAL_FAMILIES:
        counts = critical[family]
        observations = counts["observations"]
        by_critical_family[family] = {
            "observations": observations,
            "failedObservations": observations - counts["exactClaimSet"],
            "exactClaimSet": counts["exactClaimSet"] / max(1, observations),
            "byLanguage": {
                language: {
                    "observations": critical_languages[family][language]["observations"],
                    "failedObservations": (
                        critical_languages[family][language]["observations"] -
                        critical_languages[family][language]["exactClaimSet"]),
                    "exactClaimSet": (
                        critical_languages[family][language]["exactClaimSet"] /
                        max(1, critical_languages[family][language]["observations"])),
                }
                for language in ("it", "en", "es")
            },
        }
    return {"overall": overall,
            "byLanguage": by_language,
            "worstLanguage": {"fieldExact": worst_field, "exactClaimSet": worst_claim_set},
            "byCriticalFamily": by_critical_family,
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
    parser.add_argument("--runtime", choices=("native", "onnx"), default="native")
    parser.add_argument("--onnx-model", type=pathlib.Path)
    args = parser.parse_args()
    rows = read_rows(args.dataset)
    if any(row["split"] != args.split for row in rows):
        raise SystemExit(f"dataset contains rows outside declared split {args.split}")
    if args.runtime == "onnx" and args.onnx_model is None:
        parser.error("--onnx-model is required with --runtime onnx")
    runtime = (OnnxMatrixNluRuntime(args.bundle, args.onnx_model, args.threshold)
               if args.runtime == "onnx" else MatrixNluRuntime(args.bundle, args.threshold))
    predictions = [runtime.interpret(row["text"], row["context"],
                                     f"benchmark:{row['id']}") for row in rows]
    metrics, errors = score_rows(rows, predictions)
    result = {"schemaVersion": "matrix.nlu.e2e-result.v1", "split": args.split,
              "runtime": args.runtime,
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
