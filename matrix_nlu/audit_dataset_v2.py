#!/usr/bin/env python3
"""Fail-closed structural, authority, provenance and leakage audit for v2."""

from __future__ import annotations

import argparse
import collections
import difflib
import hashlib
import json
import pathlib

from build_dataset_v2 import (SCHEMA, V1_HASHES, _replace_semantic_spans,
                              exact_surface, semantic_group, split_surface)
from labels import SEQUENCE_IDS

SPLITS = ("train", "dev", "test")
LANGUAGES = ("it", "en", "es")


def _load(path: pathlib.Path) -> tuple[list[dict], str]:
    raw = path.read_bytes()
    return ([json.loads(line) for line in raw.decode("utf-8").splitlines() if line.strip()],
            hashlib.sha256(raw).hexdigest())


def _inside(span, source) -> bool:
    return (isinstance(span, list) and len(span) == 2 and
            all(isinstance(value, int) for value in span) and
            source[0] <= span[0] < span[1] <= source[1])


def audit(data_dir: pathlib.Path) -> dict:
    failures = collections.defaultdict(list)
    datasets, tagged = {}, []
    mapping_path = data_dir / "v1-to-v2-corrections.json"
    try:
        mapping = json.loads(mapping_path.read_text(encoding="utf-8"))
    except (OSError, json.JSONDecodeError) as error:
        mapping = {}
        failures["provenance"].append({"reason": "mapping unreadable", "detail": str(error)})

    for dataset in ("matrix", "p05"):
        prefix = f"{dataset}-v2"
        manifest_path = data_dir / f"{prefix}-manifest.json"
        try:
            manifest = json.loads(manifest_path.read_text(encoding="utf-8"))
        except (OSError, json.JSONDecodeError) as error:
            failures["provenance"].append({"dataset": dataset, "reason": "manifest unreadable", "detail": str(error)})
            continue
        if manifest.get("datasetSchema") != SCHEMA or manifest.get("sourceV1Hashes") != V1_HASHES[dataset]:
            failures["provenance"].append({"dataset": dataset, "reason": "manifest schema or v1 hashes"})
        datasets[dataset] = {"manifest": str(manifest_path), "splits": {}}
        for split in SPLITS:
            path = data_dir / f"{prefix}-{split}.jsonl"
            rows, digest = _load(path)
            expected = manifest.get("files", {}).get(split, {}).get("sha256")
            if digest != expected:
                failures["checksum"].append({"path": str(path), "expected": expected, "actual": digest})
            counts = dict(sorted(collections.Counter(row.get("language") for row in rows).items()))
            if set(counts) != set(LANGUAGES) or max(counts.values()) - min(counts.values()) > 2:
                failures["languageBalance"].append({"dataset": dataset, "split": split, "counts": counts})
            datasets[dataset]["splits"][split] = {
                "path": str(path), "sha256": digest, "records": len(rows),
                "claims": sum(len(row.get("claims", [])) for row in rows), "languages": counts,
            }
            tagged.extend((dataset, row) for row in rows)

    exact_targets = collections.defaultdict(set)
    exact_splits = collections.defaultdict(set)
    semantic_by_split = collections.defaultdict(lambda: collections.defaultdict(set))
    observed = {split: collections.defaultdict(set) for split in SPLITS}
    required_labels = set(SEQUENCE_IDS) | {"worldTruth"}
    required_spans = {"source", "object", "subject", "negation", "temporal", "entities"}

    for dataset, row in tagged:
        location = {"dataset": dataset, "id": row.get("id"), "split": row.get("split")}
        if (row.get("schemaVersion") != SCHEMA or row.get("split") not in SPLITS or
                row.get("language") not in LANGUAGES or not row.get("claims")):
            failures["schema"].append(location)
            continue
        provenance = row.get("provenance", {})
        migrated = (provenance.get("migratedFromSchema") == "matrix.nlu.dataset.v1" and
                    provenance.get("migratedFromRowId") == row.get("id") and
                    provenance.get("migrationPolicy") == "SUPERVISOR_OPTION_A")
        authored = (provenance.get("kind") == "MATRIX_AUTHORED_V2_AUGMENTATION" and
                    provenance.get("createdInVersion") == SCHEMA and
                    provenance.get("parentSchema") == "matrix.nlu.dataset.v1" and
                    provenance.get("migrationPolicy") == "SUPERVISOR_OPTION_A")
        if not (migrated or authored):
            failures["provenance"].append({**location, "reason": "row lineage"})

        key = exact_surface(row)
        target = json.dumps([{"labels": c["labels"], "spans": c["spans"]}
                             for c in row["claims"]], sort_keys=True, ensure_ascii=False)
        exact_targets[key].add(target)
        exact_splits[split_surface(row)].add(row["split"])
        semantic_by_split[semantic_group(row)][row["split"]].add(_replace_semantic_spans(row))

        for index, claim in enumerate(row["claims"]):
            where = {**location, "claimIndex": index}
            labels, spans = claim.get("labels", {}), claim.get("spans", {})
            if set(labels) != required_labels or set(spans) != required_spans:
                failures["schema"].append({**where, "reason": "claim fields"})
                continue
            for head, vocabulary in SEQUENCE_IDS.items():
                if labels[head] not in vocabulary:
                    failures["labels"].append({**where, "head": head, "value": labels[head]})
                else:
                    observed[row["split"]][head].add(labels[head])
            source = spans["source"]
            if not (isinstance(source, list) and len(source) == 2 and
                    all(isinstance(value, int) for value in source) and
                    0 <= source[0] < source[1] <= len(row["text"])):
                failures["spans"].append({**where, "field": "source"})
                continue
            for field in ("object", "subject", "negation", "temporal"):
                if spans[field] is not None and not _inside(spans[field], source):
                    failures["spans"].append({**where, "field": field})
            for entity_index, entity in enumerate(spans["entities"]):
                if (set(entity) != {"span", "type", "referent"} or
                        entity.get("type") not in {"PERSON", "LOCATION"} or
                        not _inside(entity.get("span"), source)):
                    failures["spans"].append({**where, "field": f"entities[{entity_index}]"})

            policy = claim.get("annotationPolicy", {})
            expected_negation = source if labels["polarity"] == "NEGATIVE" else None
            if spans["negation"] != expected_negation or policy.get("negationSurface") != (
                    "SEMANTIC_SCOPE" if expected_negation else "NONE"):
                failures["conventions"].append({**where, "reason": "negation scope"})
            if labels["subjectReferent"] == "SPEAKER" and (
                    spans["subject"] is not None or policy.get("subjectSurface") != "IMPLICIT"):
                failures["conventions"].append({**where, "reason": "implicit first-person subject"})
            if policy.get("temporalSurface") == "EXPLICIT":
                temporal = spans["temporal"]
                expression = policy.get("temporalExpression")
                if temporal is None or row["text"][temporal[0]:temporal[1]] != expression:
                    failures["conventions"].append({**where, "reason": "explicit temporal span"})
            elif spans["temporal"] is not None:
                failures["conventions"].append({**where, "reason": "temporal span/policy mismatch"})

            if labels["worldTruth"] is not False:
                failures["ownershipAuthority"].append({**where, "reason": "invented World Truth"})
            if labels["ownerReferent"] == "UNKNOWN" or labels["perspectiveReferent"] == "UNKNOWN":
                failures["ownershipAuthority"].append({**where, "reason": "unknown authority"})
            context = row.get("context", {})
            for field in ("subjectReferent", "targetReferent", "ownerReferent", "perspectiveReferent"):
                value = labels[field]
                if value == "KNOWN_ENTITY" and not context.get("knownEntities"):
                    failures["ownershipAuthority"].append({**where, "field": field, "reason": "missing known binding"})
                if value == "RECENT_ENTITY" and not context.get("recentEntityRefs"):
                    failures["ownershipAuthority"].append({**where, "field": field, "reason": "missing recent binding"})

    contradictory = sum(len(targets) > 1 for targets in exact_targets.values())
    exact_leakage = sum(len(splits) > 1 for splits in exact_splits.values())
    semantic_leakage = 0
    near_examples = []
    for group, by_split in semantic_by_split.items():
        for left, right in (("train", "dev"), ("train", "test"), ("dev", "test")):
            for a in sorted(by_split[left]):
                for b in sorted(by_split[right]):
                    similarity = difflib.SequenceMatcher(None, a, b, autojunk=False).ratio()
                    if similarity >= 0.97:
                        semantic_leakage += 1
                        if len(near_examples) < 100:
                            near_examples.append({"splits": [left, right],
                                                  "similarity": similarity,
                                                  "groupSha256": hashlib.sha256(group.encode()).hexdigest(),
                                                  "leftSha256": hashlib.sha256(a.encode()).hexdigest(),
                                                  "rightSha256": hashlib.sha256(b.encode()).hexdigest()})
    if contradictory:
        failures["incompatibleGold"].append({"count": contradictory})
    if exact_leakage:
        failures["exactSurfaceLeakage"].append({"count": exact_leakage})
    if semantic_leakage:
        failures["semanticFamilyLeakage"].extend(near_examples)
    for split in ("dev", "test"):
        for head, values in observed[split].items():
            missing = sorted(values - observed["train"].get(head, set()))
            if missing:
                failures["labelCoverage"].append({"split": split, "head": head, "missing": missing})

    if mapping:
        if (mapping.get("schemaVersion") != "matrix.nlu.dataset-v1-to-v2-mapping.v1" or
                mapping.get("immutableV1HashesVerified") != V1_HASHES):
            failures["provenance"].append({"reason": "mapping schema or v1 hashes"})
        for dataset, split_files in mapping.get("v2Files", {}).items():
            for split, metadata in split_files.items():
                actual = datasets.get(dataset, {}).get("splits", {}).get(split, {}).get("sha256")
                if metadata.get("sha256") != actual:
                    failures["checksum"].append({"dataset": dataset, "split": split,
                                                 "reason": "mapping v2 checksum"})

    failure_count = sum(len(items) for items in failures.values())
    failure_details = {key: value[:100] for key, value in sorted(failures.items()) if value}
    flat_failures = [{"category": key, **item}
                     for key, values in sorted(failures.items()) for item in values[:100]]
    return {
        "schemaVersion": "matrix.nlu.dataset-v2-audit.v1",
        "status": "PASS" if failure_count == 0 else "FAILED_GATE",
        "datasetSchema": SCHEMA,
        "scope": {"frozenContentUse": "STRUCTURAL_SEPARATION_AND_CHECKSUM_ONLY",
                  "frozenPredictionsRead": False, "frozenDataUsedForTuning": False},
        "frozenPredictionsRead": False,
        "frozenDataUsedForTuning": False,
        "datasets": datasets,
        "invariants": {"contradictoryExactInputCount": contradictory,
                       "crossSplitExactSurfaceCount": exact_leakage,
                       "crossSplitSemanticTemplateCount": semantic_leakage,
                       "failureCount": failure_count},
        "failureCounts": {key: len(value) for key, value in sorted(failures.items())},
        "migration": {"path": str(mapping_path),
                      "sha256": hashlib.sha256(mapping_path.read_bytes()).hexdigest() if mapping_path.exists() else None,
                      "counts": mapping.get("counts")},
        "failures": flat_failures,
        "failureDetails": failure_details,
    }


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--data-dir", type=pathlib.Path, default=pathlib.Path("build/matrix-nlu/data-v2"))
    parser.add_argument("--output", type=pathlib.Path, required=True)
    parser.add_argument("--fail-on-error", action="store_true")
    args = parser.parse_args()
    result = audit(args.data_dir)
    args.output.parent.mkdir(parents=True, exist_ok=True)
    args.output.write_text(json.dumps(result, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")
    print(json.dumps(result, indent=2, ensure_ascii=False))
    return 2 if args.fail_on_error and result["status"] != "PASS" else 0


if __name__ == "__main__":
    raise SystemExit(main())
