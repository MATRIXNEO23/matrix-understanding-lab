#!/usr/bin/env python3
"""Verify, extract and deterministically sample MASSIVE auxiliary supervision."""

from __future__ import annotations

import argparse
import hashlib
import json
import pathlib
import random
import re
import shutil
import tarfile
import tempfile
import urllib.request
from collections import Counter

import probe_massive


ANNOTATION = re.compile(r"\[([^:\]]+)\s*:\s*([^\]]+)]")
LANGUAGE = {"it-IT": "it", "en-US": "en", "es-ES": "es"}


def parse_annotated(value: str) -> tuple[str, list[dict]]:
    text_parts = []
    slots = []
    position = 0
    cursor = 0
    for match in ANNOTATION.finditer(value):
        prefix = value[cursor:match.start()]
        text_parts.append(prefix)
        position += len(prefix)
        slot_value = match.group(2)
        start = position
        text_parts.append(slot_value)
        position += len(slot_value)
        slots.append({"span": [start, position], "type": match.group(1).strip()})
        cursor = match.end()
    text_parts.append(value[cursor:])
    return "".join(text_parts), slots


def select(rows: list[dict], limit: int, seed: int) -> list[dict]:
    ordered = sorted(rows, key=lambda row: (str(row["id"]), row["utt"]))
    random.Random(seed).shuffle(ordered)
    return ordered[:min(limit, len(ordered))]


def digest(path: pathlib.Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--source", type=pathlib.Path, default=pathlib.Path("matrix_nlu/massive_source.json"))
    parser.add_argument("--output-dir", type=pathlib.Path, default=pathlib.Path("build/matrix-nlu/massive"))
    parser.add_argument("--train-per-language", type=int, default=3000)
    parser.add_argument("--dev-per-language", type=int, default=600)
    parser.add_argument("--test-per-language", type=int, default=1000)
    parser.add_argument("--seed", type=int, default=810923)
    args = parser.parse_args()
    spec = json.loads(args.source.read_text(encoding="utf-8"))
    if not spec.get("expectedSha256"):
        raise SystemExit("MASSIVE expectedSha256 must be pinned before preparation")
    args.output_dir.mkdir(parents=True, exist_ok=True)
    selected = {split: [] for split in ("train", "dev", "test")}
    with tempfile.TemporaryDirectory() as temporary:
        archive_path = pathlib.Path(temporary) / "massive.tar.gz"
        with urllib.request.urlopen(spec["url"], timeout=180) as response, archive_path.open("wb") as output:
            shutil.copyfileobj(response, output)
        actual = probe_massive.hash_file(archive_path)
        if actual != spec["expectedSha256"]:
            raise SystemExit(f"MASSIVE hash mismatch: expected {spec['expectedSha256']}, got {actual}")
        with tarfile.open(archive_path, "r:gz") as archive:
            license_member = probe_massive.safe_member(archive, "/LICENSE")
            license_bytes = archive.extractfile(license_member).read()
            (args.output_dir / "MASSIVE-LICENSE.txt").write_bytes(license_bytes)
            for locale_index, locale in enumerate(spec["locales"]):
                member = probe_massive.safe_member(archive, f"/data/{locale}.jsonl")
                with archive.extractfile(member) as handle:
                    rows = [json.loads(line) for line in handle]
                for split, limit in (("train", args.train_per_language),
                                     ("dev", args.dev_per_language),
                                     ("test", args.test_per_language)):
                    candidates = [row for row in rows if row["partition"] == split]
                    for row in select(candidates, limit, args.seed + locale_index * 101 + len(split)):
                        reconstructed, slots = parse_annotated(row["annot_utt"])
                        # Localizations occasionally differ only in whitespace;
                        # spans are authoritative over the reconstructed string.
                        selected[split].append({
                            "id": f"massive:{locale}:{row['id']}", "language": LANGUAGE[locale],
                            "locale": locale, "split": split, "text": reconstructed,
                            "intent": row["intent"], "scenario": row["scenario"], "slots": slots,
                            "originalTextMatches": " ".join(reconstructed.split()) == " ".join(row["utt"].split()),
                            "sourceId": f"massive-1.0:{locale}:{row['id']}",
                        })
    intents = sorted({row["intent"] for rows in selected.values() for row in rows})
    slot_types = sorted({slot["type"] for rows in selected.values() for row in rows for slot in row["slots"]})
    files = {}
    for split, rows in selected.items():
        path = args.output_dir / f"massive-{split}.jsonl"
        rows.sort(key=lambda row: row["id"])
        path.write_text("".join(json.dumps(row, ensure_ascii=False, sort_keys=True) + "\n" for row in rows), encoding="utf-8")
        files[split] = {"records": len(rows), "sha256": digest(path),
                        "languages": dict(sorted(Counter(row["language"] for row in rows).items())),
                        "exactOriginalText": sum(row["originalTextMatches"] for row in rows)}
    label_path = args.output_dir / "massive-labels.json"
    label_path.write_text(json.dumps({"intents": intents, "slotTypes": slot_types}, indent=2) + "\n", encoding="utf-8")
    manifest = {"schemaVersion": "matrix.nlu.massive-derived.v1", "source": spec,
                "seed": args.seed, "files": files, "intentCount": len(intents),
                "slotTypeCount": len(slot_types), "labelsSha256": digest(label_path),
                "licenseSha256": hashlib.sha256(license_bytes).hexdigest()}
    (args.output_dir / "manifest.json").write_text(json.dumps(manifest, indent=2) + "\n", encoding="utf-8")
    print(json.dumps(manifest, indent=2))


if __name__ == "__main__":
    main()
