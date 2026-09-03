#!/usr/bin/env python3
"""Download and inventory MASSIVE without mixing it into Matrix data."""

from __future__ import annotations

import argparse
import hashlib
import json
import pathlib
import shutil
import tarfile
import tempfile
import urllib.request
from collections import Counter


def hash_file(path: pathlib.Path) -> str:
    digest = hashlib.sha256()
    with path.open("rb") as source:
        for chunk in iter(lambda: source.read(1024 * 1024), b""):
            digest.update(chunk)
    return digest.hexdigest()


def safe_member(archive: tarfile.TarFile, suffix: str):
    matches = [member for member in archive.getmembers() if member.name.endswith(suffix)]
    if len(matches) != 1 or not matches[0].isfile():
        raise ValueError(f"expected exactly one regular archive member ending in {suffix!r}")
    return matches[0]


def inventory_jsonl(handle) -> dict:
    partitions = Counter()
    intents = Counter()
    scenarios = Counter()
    slots = Counter()
    rows = 0
    for raw in handle:
        row = json.loads(raw)
        rows += 1
        partitions[row["partition"]] += 1
        intents[row["intent"]] += 1
        scenarios[row["scenario"]] += 1
        annotated = row.get("annot_utt", "")
        for section in annotated.split("[")[1:]:
            if " : " in section:
                slots[section.split(" : ", 1)[0].strip()] += 1
    return {"rows": rows, "partitions": dict(sorted(partitions.items())),
            "intentCount": len(intents), "scenarioCount": len(scenarios),
            "slotTypesObserved": sorted(slots), "slotAnnotationCount": sum(slots.values())}


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--source", type=pathlib.Path, default=pathlib.Path("matrix_nlu/massive_source.json"))
    parser.add_argument("--output-dir", type=pathlib.Path, default=pathlib.Path("build/matrix-nlu/massive-provenance"))
    args = parser.parse_args()
    spec_bytes = args.source.read_bytes()
    spec = json.loads(spec_bytes)
    args.output_dir.mkdir(parents=True, exist_ok=True)
    with tempfile.TemporaryDirectory() as tmp:
        archive_path = pathlib.Path(tmp) / "massive.tar.gz"
        with urllib.request.urlopen(spec["url"], timeout=180) as response, archive_path.open("wb") as output:
            shutil.copyfileobj(response, output)
        actual_hash = hash_file(archive_path)
        expected_hash = spec.get("expectedSha256")
        with tarfile.open(archive_path, "r:gz") as archive:
            license_member = safe_member(archive, "/LICENSE")
            license_bytes = archive.extractfile(license_member).read()
            (args.output_dir / "MASSIVE-LICENSE.txt").write_bytes(license_bytes)
            locales = {}
            for locale in spec["locales"]:
                member = safe_member(archive, f"/data/{locale}.jsonl")
                with archive.extractfile(member) as source:
                    locales[locale] = inventory_jsonl((line.decode("utf-8") for line in source))
        result = {
            "schemaVersion": "matrix.nlu.massive-provenance.v1",
            "sourceSpecSha256": hashlib.sha256(spec_bytes).hexdigest(),
            "source": spec, "archiveBytes": archive_path.stat().st_size,
            "archiveSha256": actual_hash, "hashPinned": expected_hash is not None,
            "hashMatches": expected_hash == actual_hash if expected_hash else False,
            "licenseSha256": hashlib.sha256(license_bytes).hexdigest(), "locales": locales,
        }
        (args.output_dir / "manifest.json").write_text(json.dumps(result, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")
        print(json.dumps({"archiveBytes": result["archiveBytes"], "archiveSha256": actual_hash,
                          "hashPinned": result["hashPinned"], "locales": locales}, indent=2))
        if expected_hash is not None and expected_hash != actual_hash:
            raise SystemExit("MASSIVE archive hash differs from pinned provenance")


if __name__ == "__main__":
    main()
