#!/usr/bin/env python3
"""Weighted Student-4-v2.2A trainer wrapper.

The base trainer stays unchanged. This wrapper does two v2.2A-specific things:

1. Appends ``v22a-repair-train.jsonl`` only when the base trainer reads
   ``matrix-v2-train.jsonl``. Dev and frozen paths are never augmented.
2. Replaces ``loss_for`` with a config-driven weighted variant so the repair run
   spends capacity on the observed failure heads without changing architecture
   or gates.
"""

from __future__ import annotations

import json
import pathlib
import sys

import train as base

IGNORE = base.IGNORE
CONFIG = None
ORIGINAL_READ_JSONL = base.read_jsonl
REPAIR_FILE_NAME = "v22a-repair-train.jsonl"
REPAIR_MANIFEST_NAME = "v22a-repair-train-manifest.json"


def _arg_path(flag: str, default: str) -> pathlib.Path:
    for index, arg in enumerate(sys.argv):
        if arg == flag and index + 1 < len(sys.argv):
            return pathlib.Path(sys.argv[index + 1])
        if arg.startswith(flag + "="):
            return pathlib.Path(arg.split("=", 1)[1])
    return pathlib.Path(default)


def _config_path() -> pathlib.Path:
    return _arg_path("--config", "matrix_nlu/train_config.json")


def _data_dir() -> pathlib.Path:
    return _arg_path("--data-dir", "build/matrix-nlu/data")


def _output_dir() -> pathlib.Path:
    return _arg_path("--output-dir", "build/matrix-nlu/training")


def _load_config() -> dict:
    global CONFIG
    if CONFIG is None:
        CONFIG = json.loads(_config_path().read_text(encoding="utf-8"))
    return CONFIG


def _read_jsonl_with_repair(paths) -> list[dict]:
    rows = ORIGINAL_READ_JSONL(paths)
    path_names = {pathlib.Path(path).name for path in paths}
    if "matrix-v2-train.jsonl" not in path_names:
        return rows
    repair_path = _data_dir() / REPAIR_FILE_NAME
    if not repair_path.is_file():
        raise RuntimeError(f"missing v2.2A train-only repair file: {repair_path}")
    repair_rows = ORIGINAL_READ_JSONL([repair_path])
    if any(row.get("split") != "train" for row in repair_rows):
        raise RuntimeError("v2.2A repair file contains non-train rows")
    print(json.dumps({
        "event": "V22A_REPAIR_AUXILIARY_LOADED",
        "baseRows": len(rows),
        "repairRows": len(repair_rows),
        "file": str(repair_path),
    }, ensure_ascii=False))
    return rows + repair_rows


def _head_weight(group: str, head: str) -> float:
    weights = _load_config().get("headLossWeights", {})
    return float(weights.get(group, {}).get(head, 1.0))


def _aux_weight(name: str) -> float:
    weights = _load_config().get("headLossWeights", {})
    return float(weights.get("massive", {}).get(name, 1.0))


def loss_for(outputs, batch, class_weights=None):
    import torch
    import torch.nn.functional as functional

    weighted_terms = []
    normalizer = 0.0
    for head, logits in outputs["tokens"].items():
        labels = batch["token_labels"][head]
        if torch.any(labels != IGNORE):
            weight = _head_weight("tokens", head)
            value = functional.cross_entropy(
                logits.reshape(-1, logits.shape[-1]),
                labels.reshape(-1),
                ignore_index=IGNORE,
                weight=(class_weights or {}).get("tokens", {}).get(head),
            )
            weighted_terms.append(value * weight)
            normalizer += weight

    for head, logits in outputs["sequence"].items():
        labels = batch["sequence_labels"][head]
        if torch.any(labels != IGNORE):
            weight = _head_weight("sequence", head)
            value = functional.cross_entropy(
                logits,
                labels,
                ignore_index=IGNORE,
                weight=(class_weights or {}).get("sequence", {}).get(head),
            )
            weighted_terms.append(value * weight)
            normalizer += weight

    if torch.any(batch["aux_intent"] != IGNORE):
        weight = _aux_weight("intent")
        weighted_terms.append(
            functional.cross_entropy(outputs["massive_intent"], batch["aux_intent"], ignore_index=IGNORE) * weight
        )
        normalizer += weight

    if torch.any(batch["aux_slot"] != IGNORE):
        weight = _aux_weight("slot")
        weighted_terms.append(
            functional.cross_entropy(
                outputs["massive_slot"].reshape(-1, outputs["massive_slot"].shape[-1]),
                batch["aux_slot"].reshape(-1),
                ignore_index=IGNORE,
            ) * weight
        )
        normalizer += weight

    if not weighted_terms:
        raise ValueError("batch has no supervised head")
    return sum(weighted_terms) / max(1.0e-6, normalizer)


def _record_repair_evidence() -> None:
    output = _output_dir() / "training-result.json"
    if not output.is_file():
        return
    result = json.loads(output.read_text(encoding="utf-8"))
    data = _data_dir()
    repair_path = data / REPAIR_FILE_NAME
    manifest_path = data / REPAIR_MANIFEST_NAME
    result["v22aRepairAuxiliary"] = {
        "file": str(repair_path),
        "manifest": str(manifest_path),
        "fileSha256": base.sha256(repair_path),
        "manifestSha256": base.sha256(manifest_path),
        "policy": "TRAIN_ONLY_AUXILIARY; dev/frozen not augmented; no censorship labels",
    }
    result.setdefault("inputHashes", {})[str(repair_path)] = base.sha256(repair_path)
    result.setdefault("inputHashes", {})[str(manifest_path)] = base.sha256(manifest_path)
    output.write_text(json.dumps(result, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")


base.read_jsonl = _read_jsonl_with_repair
base.loss_for = loss_for

if __name__ == "__main__":
    base.main()
    _record_repair_evidence()
