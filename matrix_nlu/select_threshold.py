#!/usr/bin/env python3
"""Select an admission threshold using development evidence only."""

from __future__ import annotations

import argparse
import json
import pathlib

from evaluate_e2e import read_rows, score_rows
from inference import validate_claim


def read_predictions(path):
    with path.open(encoding="utf-8") as handle:
        return [json.loads(line) for line in handle if line.strip()]


def apply_threshold(rows, evidence, threshold):
    if [row["id"] for row in rows] != [item["id"] for item in evidence]:
        raise ValueError("dataset and prediction IDs/order differ")
    predictions = []
    for row, item in zip(rows, evidence):
        previous = item["prediction"]
        claims = [validate_claim(raw, row["text"], row["context"],
                                 f"calibration:{row['id']}", threshold)
                  for raw in previous["rawClaims"]]
        predictions.append({**previous, "claims": claims, "worldTruthUpdates": 0})
    return predictions


def choose_threshold(rows, evidence, minimum_accuracy, minimum_claim_count=0.99):
    confidences = sorted({float(raw["confidence"]) for item in evidence
                          for raw in item["prediction"]["rawClaims"]})
    candidates = sorted({0.0, 1.0, *(min(1.0, value + 1e-9) for value in confidences)})
    curve = []
    for threshold in candidates:
        metrics, _ = score_rows(rows, apply_threshold(rows, evidence, threshold))
        point = {"threshold": threshold, **metrics["overall"]}
        curve.append(point)
    eligible = [point for point in curve
                if point["validSelectiveAccuracy"] >= minimum_accuracy and
                point["claimCountExact"] >= minimum_claim_count and
                point["ownershipCorruption"] == 0 and point["worldTruthUpdates"] == 0]
    # Zero-coverage points are not evidence of useful calibration.
    eligible = [point for point in eligible if point["validCoverage"] > 0]
    selected = max(eligible, key=lambda point: (point["validCoverage"],
                                                point["validSelectiveAccuracy"],
                                                -point["threshold"])) if eligible else None
    return {"schemaVersion": "matrix.nlu.threshold-selection.v1",
            "policy": {"selectionSplit": "dev", "minimumSelectiveAccuracy": minimum_accuracy,
                       "minimumClaimCountExact": minimum_claim_count,
                       "ownershipCorruptionMaximum": 0, "worldTruthUpdatesMaximum": 0,
                       "optimization": "maximum valid coverage"},
            "status": "PASS" if selected else "FAILED_GATE",
            "selectedThreshold": None if selected is None else selected["threshold"],
            "selectedMetrics": selected, "curve": curve}


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--dataset", action="append", type=pathlib.Path, required=True)
    parser.add_argument("--predictions", action="append", type=pathlib.Path, required=True)
    parser.add_argument("--minimum-selective-accuracy", type=float, default=0.99)
    parser.add_argument("--minimum-claim-count-exact", type=float, default=0.99)
    parser.add_argument("--output", type=pathlib.Path, required=True)
    args = parser.parse_args()
    if len(args.dataset) != len(args.predictions):
        raise SystemExit("provide one --predictions file per --dataset")
    rows, evidence = [], []
    for dataset, predictions in zip(args.dataset, args.predictions):
        current_rows = read_rows(dataset)
        if any(row["split"] != "dev" for row in current_rows):
            raise SystemExit("threshold selection accepts development partitions only")
        rows.extend(current_rows)
        evidence.extend(read_predictions(predictions))
    result = choose_threshold(rows, evidence, args.minimum_selective_accuracy,
                              args.minimum_claim_count_exact)
    args.output.parent.mkdir(parents=True, exist_ok=True)
    args.output.write_text(json.dumps(result, indent=2) + "\n")
    print(json.dumps(result, indent=2))
    if result["status"] != "PASS":
        raise SystemExit(2)


if __name__ == "__main__":
    main()
