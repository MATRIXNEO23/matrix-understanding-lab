#!/usr/bin/env python3
"""Build supervisor-approved ``matrix.nlu.dataset.v2`` without rewriting v1."""

from __future__ import annotations

import argparse
import copy
import difflib
import hashlib
import json
import pathlib
import re
import tempfile
import unicodedata
from collections import Counter, defaultdict

import build_dataset as v1

SCHEMA = "matrix.nlu.dataset.v2"
MANIFEST_SCHEMA = "matrix.nlu.dataset-manifest.v2"
MAPPING_SCHEMA = "matrix.nlu.dataset-v1-to-v2-mapping.v1"
V1_HASHES = {
    "matrix": {
        "train": "803a565e9bb7e88de269b1002603ea86a4bbb832c06183d537525596c4575b6d",
        "dev": "aa19e414a5d5dd1bc3ec9c1e257b8224b568a2a7460a92f31875ce3741003177",
        "test": "8f1b267fb9f1b76d0f304cd26d88dfcef82fd6434f5ea182985a164960effba2",
    },
    "p05": {
        "train": "8426018bd4ec9d06c5bc9cfc0d668c2f8b4208add14a0a413694153f5f4ab95b",
        "dev": "b48753dc07adee70538e890473a2df08524260fdaec31d9946f2e5c57183582b",
        "test": "5ef8f8bf6ed761df8f91dbd0dcc415d4b62c783759d6d10a229b4fba4c6ee505",
    },
}
V2_HASHES = {
    "matrix": {
        "train": "e6190bf4fe0c5d326242920be6b3e0fbcb6f6fc593f4d7a017ffd08f74bb0eff",
        "dev": "704e809f0e9ebace3a5c047989b74d354ac8811757a2644b0d9c04cfb0631012",
        "test": "458f79ecaa9ec547c53a55ba68c45531e88e0ae5a0d6ee405222632d85919228",
    },
    "p05": {
        "train": "413f60ca17879ed9de440add7903b6e2abaebdfbbed6055b32c6e0b105cadfcd",
        "dev": "7533f56194431bd17b6f8544031d5436ca14ee6e209336da8133e1f05cdf0866",
        "test": "a729045ac17356321f2b8c6624554c8bf8ad22fd794e2c0718876734de0aabc2",
    },
}

# Authoring-time evidence only; never shipped as runtime linguistic rules.
EXPLICIT_TEMPORAL_EXPRESSIONS = {
    "it": ("in questo momento", "più avanti", "in futuro", "domani", "prima", "adesso", "oggi", "ora"),
    "en": ("at the moment", "in the future", "in future", "previously", "tomorrow", "currently", "used to", "today", "later", "now"),
    "es": ("en este momento", "más adelante", "en el futuro", "actualmente", "mañana", "antes", "ahora", "hoy"),
}


def sha256(path: pathlib.Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def _target(row: dict) -> str:
    return json.dumps([{"labels": c["labels"], "spans": c["spans"]}
                       for c in row["claims"]], ensure_ascii=False, sort_keys=True)


def exact_surface(row: dict) -> str:
    return json.dumps([row["language"], row["text"].casefold().strip(),
                       row.get("context", {})], ensure_ascii=False, sort_keys=True)


def split_surface(row: dict) -> str:
    return json.dumps([row["language"], " ".join(row["text"].casefold().split())],
                      ensure_ascii=False)


def _replace_semantic_spans(row: dict) -> str:
    candidates = []
    for claim in row["claims"]:
        source = claim["spans"]["source"]
        for field in ("object", "subject", "temporal"):
            span = claim["spans"].get(field)
            if span is not None and span != source:
                candidates.append((span[0], span[1], f"<{field}>"))
        for entity in claim["spans"].get("entities", []):
            span = entity["span"]
            if span != source:
                candidates.append((span[0], span[1], f"<entity:{entity['type']}>"))
    selected, occupied = [], set()
    for start, end, marker in sorted(candidates,
                                     key=lambda x: (-(x[1] - x[0]), x[0], x[2])):
        positions = set(range(start, end))
        if not positions & occupied:
            selected.append((start, end, marker))
            occupied |= positions
    text = row["text"]
    for start, end, marker in sorted(selected, key=lambda x: x[0], reverse=True):
        text = text[:start] + marker + text[end:]
    return re.sub(r"[^\w<>:]+", " ", unicodedata.normalize("NFKC", text).casefold()).strip()


def semantic_signature(row: dict) -> str:
    labels = [{key: claim["labels"][key] for key in sorted(claim["labels"])}
              for claim in row["claims"]]
    families = [claim.get("family", "") for claim in row["claims"]]
    return json.dumps([row["language"], _replace_semantic_spans(row), labels, families],
                      ensure_ascii=False, sort_keys=True)


def semantic_group(row: dict) -> str:
    labels = [{key: claim["labels"][key] for key in sorted(claim["labels"])}
              for claim in row["claims"]]
    return json.dumps([row["language"], labels], ensure_ascii=False, sort_keys=True)


def _explicit_temporal(row: dict, claim: dict) -> tuple[list[int] | None, str | None]:
    existing = claim["spans"].get("temporal")
    if existing is not None:
        return list(existing), row["text"][existing[0]:existing[1]]
    start, end = claim["spans"]["source"]
    fragment = row["text"][start:end]
    for expression in sorted(EXPLICIT_TEMPORAL_EXPRESSIONS[row["language"]],
                             key=len, reverse=True):
        match = re.search(r"(?<!\w)" + re.escape(expression) + r"(?!\w)",
                          fragment, flags=re.IGNORECASE | re.UNICODE)
        if match:
            absolute = start + match.start()
            finish = start + match.end()
            return [absolute, finish], row["text"][absolute:finish]
    return None, None


def _migrate(rows: list[dict], dataset: str) -> tuple[list[dict], list[dict]]:
    migrated, corrections = copy.deepcopy(rows), []
    for row in migrated:
        row["schemaVersion"] = SCHEMA
        row["provenance"] = {**row.get("provenance", {}),
                             "migratedFromSchema": v1.SCHEMA,
                             "migratedFromRowId": row["id"],
                             "migrationPolicy": "SUPERVISOR_OPTION_A",
                             "annotationContract": SCHEMA,
                             "leakageFamily": f"{dataset}:{row['split']}:{row['id']}"}
        for index, claim in enumerate(row["claims"]):
            before, spans, labels = copy.deepcopy(claim["spans"]), claim["spans"], claim["labels"]
            spans["negation"] = list(spans["source"]) if labels["polarity"] == "NEGATIVE" else None
            if labels["subjectReferent"] == "SPEAKER":
                spans["subject"] = None
            temporal, temporal_text = _explicit_temporal(row, claim)
            spans["temporal"] = temporal
            claim["annotationPolicy"] = {
                "version": SCHEMA,
                "negationSurface": "SEMANTIC_SCOPE" if spans["negation"] else "NONE",
                "subjectSurface": "IMPLICIT" if labels["subjectReferent"] == "SPEAKER" else
                                  ("EXPLICIT" if spans.get("subject") else "NONE"),
                "temporalSurface": "EXPLICIT" if temporal_text else
                                   ("IMPLICIT" if labels["temporalRelation"] != "ATEMPORAL" else "NONE"),
                "temporalExpression": temporal_text,
            }
            changed = {field: {"v1": before.get(field), "v2": spans.get(field)}
                       for field in ("subject", "negation", "temporal")
                       if before.get(field) != spans.get(field)}
            if changed:
                corrections.append({"dataset": dataset, "rowId": row["id"],
                                    "split": row["split"], "language": row["language"],
                                    "claimIndex": index, "sourceId": claim["sourceId"],
                                    "changes": changed})
    return migrated, corrections


def v2_train_augmentations() -> tuple[list[dict], list[dict]]:
    """Supply train-only labels missing from v1 without copying held-out text."""
    templates = {
        "it": (("mi considero una persona paziente", "una persona paziente"),
               ("ritengo di essere molto curioso", "molto curioso"),
               ("di carattere sono piuttosto prudente", "piuttosto prudente"),
               ("mi descriverei come una persona creativa", "una persona creativa")),
        "en": (("I consider myself a patient person", "a patient person"),
               ("I regard myself as very curious", "very curious"),
               ("my character is rather cautious", "rather cautious"),
               ("I would describe myself as a creative person", "a creative person")),
        "es": (("me considero una persona paciente", "una persona paciente"),
               ("me veo como alguien muy curioso", "alguien muy curioso"),
               ("mi carácter es bastante prudente", "bastante prudente"),
               ("me describiría como una persona creativa", "una persona creativa")),
    }
    rows, additions = [], []
    for language, examples in templates.items():
        for index, (text, object_text) in enumerate(examples):
            row_id = f"mx-v2-train-{language}-attribute-{index:02d}"
            start = text.index(object_text)
            claim = {
                "labels": {"dialogueAct": "ASSERT", "predicate": "attribute.is",
                           "subjectReferent": "SPEAKER", "targetReferent": "NONE",
                           "ownerReferent": "SUBJECT", "perspectiveReferent": "SPEAKER",
                           "polarity": "POSITIVE", "temporalRelation": "CURRENT",
                           "claimKind": "EXPLICIT", "worldTruth": False},
                "spans": {"source": [0, len(text)], "object": [start, start + len(object_text)],
                          "subject": None, "negation": None, "temporal": None,
                          "entities": []},
                "sourceId": f"matrix-v2-authored:{row_id}:0",
                "family": "attribute_is_v2_train",
                "annotationPolicy": {"version": SCHEMA, "negationSurface": "NONE",
                                     "subjectSurface": "IMPLICIT", "temporalSurface": "IMPLICIT",
                                     "temporalExpression": None},
            }
            rows.append({
                "schemaVersion": SCHEMA, "id": row_id, "split": "train",
                "language": language, "text": text,
                "context": {"speaker": "PLAYER", "observer": "luna",
                            "knownEntities": {}, "recentEntityRefs": []},
                "claims": [claim], "adultOnly": False,
                "provenance": {"kind": "MATRIX_AUTHORED_V2_AUGMENTATION",
                               "createdInVersion": SCHEMA, "parentSchema": v1.SCHEMA,
                               "migrationPolicy": "SUPERVISOR_OPTION_A",
                               "annotationContract": SCHEMA,
                               "leakageFamily": f"matrix:train:{row_id}",
                               "generatorSeed": v1.SEED, "license": "PROJECT_AUTHORED"},
            })
            additions.append({"dataset": "matrix", "rowId": row_id, "split": "train",
                              "language": language, "reason": "TRAIN_LABEL_COVERAGE",
                              "predicate": "attribute.is"})

    past_templates = {
        "it": (("fino allo scorso anno abitavo a Treviso", "Treviso", "fino allo scorso anno"),
               ("da giovane vivevo a Padova", "Padova", "da giovane"),
               ("in precedenza risiedevo vicino a Torino", "Torino", "in precedenza"),
               ("nel 2020 vivevo a Bari", "Bari", "nel 2020")),
        "en": (("until last year I lived in Bristol", "Bristol", "until last year"),
               ("when I was younger I lived in Leeds", "Leeds", "when I was younger"),
               ("previously I resided near Oxford", "Oxford", "previously"),
               ("in 2020 I lived in York", "York", "in 2020")),
        "es": (("hasta el año pasado vivía en Bilbao", "Bilbao", "hasta el año pasado"),
               ("de joven vivía en Toledo", "Toledo", "de joven"),
               ("anteriormente residía cerca de Murcia", "Murcia", "anteriormente"),
               ("en 2020 vivía en Cádiz", "Cádiz", "en 2020")),
    }
    for language, examples in past_templates.items():
        for index, (text, place, temporal_text) in enumerate(examples):
            row_id = f"mx-v2-train-{language}-past-{index:02d}"
            object_start, temporal_start = text.index(place), text.index(temporal_text)
            claim = {
                "labels": {"dialogueAct": "ASSERT", "predicate": "residence.place",
                           "subjectReferent": "SPEAKER", "targetReferent": "NONE",
                           "ownerReferent": "SUBJECT", "perspectiveReferent": "SPEAKER",
                           "polarity": "POSITIVE", "temporalRelation": "PAST",
                           "claimKind": "EXPLICIT", "worldTruth": False},
                "spans": {"source": [0, len(text)],
                          "object": [object_start, object_start + len(place)],
                          "subject": None, "negation": None,
                          "temporal": [temporal_start, temporal_start + len(temporal_text)],
                          "entities": [{"span": [object_start, object_start + len(place)],
                                        "type": "LOCATION", "referent": "LOCATION"}]},
                "sourceId": f"matrix-v2-authored:{row_id}:0",
                "family": "past_residence_v2_train",
                "annotationPolicy": {"version": SCHEMA, "negationSurface": "NONE",
                                     "subjectSurface": "IMPLICIT", "temporalSurface": "EXPLICIT",
                                     "temporalExpression": temporal_text},
            }
            rows.append({
                "schemaVersion": SCHEMA, "id": row_id, "split": "train",
                "language": language, "text": text,
                "context": {"speaker": "PLAYER", "observer": "luna",
                            "knownEntities": {}, "recentEntityRefs": []},
                "claims": [claim], "adultOnly": False,
                "provenance": {"kind": "MATRIX_AUTHORED_V2_AUGMENTATION",
                               "createdInVersion": SCHEMA, "parentSchema": v1.SCHEMA,
                               "migrationPolicy": "SUPERVISOR_OPTION_A",
                               "annotationContract": SCHEMA,
                               "leakageFamily": f"matrix:train:{row_id}",
                               "generatorSeed": v1.SEED, "license": "PROJECT_AUTHORED"},
            })
            additions.append({"dataset": "matrix", "rowId": row_id, "split": "train",
                              "language": language, "reason": "TRAIN_LABEL_COVERAGE",
                              "predicate": "residence.place", "temporalRelation": "PAST"})
    return rows, additions


def _remove_conflicts_and_leakage(tagged: list[tuple[str, dict]]) -> tuple[list[tuple[str, dict]], list[dict]]:
    drops, keep = [], set(range(len(tagged)))
    groups = defaultdict(list)
    for position, (dataset, row) in enumerate(tagged):
        groups[(row["split"], exact_surface(row))].append((position, dataset, row))
    for group in groups.values():
        if len({_target(row) for _, _, row in group}) <= 1:
            continue
        winner = min(group, key=lambda item: (item[1] != "p05", item[2]["id"]))
        for position, dataset, row in group:
            if position != winner[0]:
                keep.discard(position)
                drops.append({"dataset": dataset, "rowId": row["id"], "split": row["split"],
                              "language": row["language"], "reason": "INCOMPATIBLE_EXACT_TARGET",
                              "retainedRowId": winner[2]["id"]})

    accepted_exact = {"test": set(), "dev": set()}
    accepted_semantic = {"test": defaultdict(set), "dev": defaultdict(set)}
    for split in ("test", "dev", "train"):
        ordered = sorted(enumerate(tagged), key=lambda item: (item[1][1]["id"], item[1][0]))
        for position, (dataset, row) in ordered:
            if position not in keep or row["split"] != split:
                continue
            exact = split_surface(row)
            group_key, skeleton = semantic_group(row), _replace_semantic_spans(row)
            higher = ("test",) if split == "dev" else (("test", "dev") if split == "train" else ())
            exact_hit = any(exact in accepted_exact[level] for level in higher)
            semantic_hit = any(
                difflib.SequenceMatcher(None, skeleton, candidate, autojunk=False).ratio() >= 0.97
                for level in higher for candidate in sorted(accepted_semantic[level][group_key])
            )
            if exact_hit or semantic_hit:
                keep.discard(position)
                drops.append({"dataset": dataset, "rowId": row["id"], "split": row["split"],
                              "language": row["language"],
                              "reason": "DEV_TOO_CLOSE_TO_FROZEN_TEST" if split == "dev" else "TRAIN_TOO_CLOSE_TO_HELD_OUT",
                              "matchKind": "EXACT_SURFACE" if exact_hit else "SEMANTIC_TEMPLATE"})
            elif split in accepted_exact:
                accepted_exact[split].add(exact)
                accepted_semantic[split][group_key].add(skeleton)

    # Gold scenarios are authored as IT/EN/ES translation triplets.  If one
    # translation collides with a higher partition, drop the whole triplet so
    # decontamination cannot silently create language skew.
    def sibling_key(dataset: str, row: dict) -> tuple[str, str, str]:
        if dataset == "p05":
            stem = re.sub(r"-(it|en|es)$", "-LANG", row["id"])
        else:
            stem = re.sub(r"-(it|en|es)-", "-LANG-", row["id"], count=1)
        return dataset, row["split"], stem

    dropped_keys = {sibling_key(dataset, row)
                    for position, (dataset, row) in enumerate(tagged)
                    if position not in keep}
    for position, (dataset, row) in enumerate(tagged):
        if position in keep and sibling_key(dataset, row) in dropped_keys:
            keep.discard(position)
            drops.append({"dataset": dataset, "rowId": row["id"],
                          "split": row["split"], "language": row["language"],
                          "reason": "DEV_TOO_CLOSE_TO_FROZEN_TEST" if row["split"] == "dev" else "TRAIN_TOO_CLOSE_TO_HELD_OUT",
                          "matchKind": "TRANSLATION_SIBLING"})
    return [item for position, item in enumerate(tagged) if position in keep], drops


def _verify_v1(matrix_rows: list[dict], p05_rows: list[dict]) -> None:
    with tempfile.TemporaryDirectory() as directory:
        root = pathlib.Path(directory)
        manifests = {"matrix": v1.write(matrix_rows, root, "matrix"),
                     "p05": v1.write(p05_rows, root, "p05")}
    actual = {dataset: {split: manifests[dataset]["files"][split]["sha256"]
                        for split in v1.SPLITS} for dataset in manifests}
    if actual != V1_HASHES:
        raise RuntimeError(f"immutable v1 checksum mismatch: {actual}")


def build(p05_gold: pathlib.Path) -> tuple[dict[str, list[dict]], dict]:
    matrix_v1 = v1.build_records()
    v1.validate(matrix_v1)
    p05_v1 = v1.load_p05(p05_gold)
    v1.validate(p05_v1, require_generated_coverage=False)
    _verify_v1(matrix_v1, p05_v1)
    matrix_v2, matrix_corrections = _migrate(matrix_v1, "matrix")
    p05_v2, p05_corrections = _migrate(p05_v1, "p05")
    additions, added_rows = v2_train_augmentations()
    matrix_v2.extend(additions)
    kept, drops = _remove_conflicts_and_leakage(
        [("matrix", row) for row in matrix_v2] + [("p05", row) for row in p05_v2])
    records = {source: [row for dataset, row in kept if dataset == source]
               for source in ("matrix", "p05")}
    corrections = matrix_corrections + p05_corrections
    mapping = {
        "schemaVersion": MAPPING_SCHEMA, "from": v1.SCHEMA, "to": SCHEMA,
        "approval": "SUPERVISOR_OPTION_A", "immutableV1HashesVerified": V1_HASHES,
        "contract": {"negation": "SEMANTIC_SCOPE",
                     "implicitFirstPersonSubject": "NULL_SPAN_WITH_SUBJECT_REFERENT_SPEAKER",
                     "explicitTemporalExpression": "SPAN_REQUIRED"},
        "counts": {"claimCorrections": len(corrections), "partitionDrops": len(drops),
                   "trainAdditions": len(added_rows)},
        "claimCorrections": sorted(corrections, key=lambda item: (item["dataset"], item["split"], item["language"], item["rowId"], item["claimIndex"])),
        "partitionDrops": sorted(drops, key=lambda item: (item["dataset"], item["split"], item["language"], item["rowId"])),
        "trainAdditions": sorted(added_rows, key=lambda item: (item["language"], item["rowId"])),
    }
    return records, mapping


def write_dataset(records: list[dict], output_dir: pathlib.Path, prefix: str,
                  v1_hashes: dict[str, str]) -> dict:
    output_dir.mkdir(parents=True, exist_ok=True)
    files = {}
    for split in v1.SPLITS:
        path = output_dir / f"{prefix}-{split}.jsonl"
        rows = sorted((row for row in records if row["split"] == split), key=lambda row: row["id"])
        path.write_text("".join(json.dumps(row, ensure_ascii=False, sort_keys=True) + "\n" for row in rows), encoding="utf-8")
        files[split] = {"path": path.name, "records": len(rows),
                        "claims": sum(len(row["claims"]) for row in rows),
                        "languages": dict(sorted(Counter(row["language"] for row in rows).items())),
                        "sha256": sha256(path)}
    manifest = {"schemaVersion": MANIFEST_SCHEMA, "datasetSchema": SCHEMA,
                "seed": v1.SEED, "generator": "matrix_nlu/build_dataset_v2.py",
                "prefix": prefix, "sourceV1Hashes": v1_hashes, "files": files,
                "separation": "frozen > dev > train; exact and semantic-family disjointness",
                "worldTruthExpected": 0}
    (output_dir / f"{prefix}-manifest.json").write_text(
        json.dumps(manifest, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    return manifest


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--output-dir", type=pathlib.Path, default=pathlib.Path("build/matrix-nlu/data-v2"))
    parser.add_argument("--p05-gold", type=pathlib.Path, default=pathlib.Path("gold/p05-gold-v1.json"))
    args = parser.parse_args()
    records, mapping = build(args.p05_gold)
    manifests = {source: write_dataset(records[source], args.output_dir, f"{source}-v2", V1_HASHES[source])
                 for source in ("matrix", "p05")}
    actual_v2 = {source: {split: manifests[source]["files"][split]["sha256"]
                          for split in v1.SPLITS} for source in manifests}
    if actual_v2 != V2_HASHES:
        raise RuntimeError(f"immutable v2 checksum mismatch: expected={V2_HASHES} actual={actual_v2}")
    mapping["v2Files"] = {source: manifests[source]["files"] for source in manifests}
    mapping_path = args.output_dir / "v1-to-v2-corrections.json"
    mapping_path.write_text(json.dumps(mapping, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")
    print(json.dumps({"schemaVersion": SCHEMA, "manifests": manifests,
                      "mapping": {"path": str(mapping_path), "sha256": sha256(mapping_path), **mapping["counts"]}},
                     indent=2, ensure_ascii=False))


if __name__ == "__main__":
    main()
