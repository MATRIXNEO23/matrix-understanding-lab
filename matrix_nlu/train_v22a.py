#!/usr/bin/env python3
"""Weighted Student-4-v2.2A trainer wrapper.

The base trainer stays unchanged. This wrapper only replaces ``loss_for`` with a
config-driven weighted variant so the v2.2A run spends capacity on the observed
failure heads without changing architecture, dev/frozen splits or gates.
"""

from __future__ import annotations

import json
import pathlib
import sys

import train as base

IGNORE = base.IGNORE
CONFIG = None


def _config_path() -> pathlib.Path:
    for index, arg in enumerate(sys.argv):
        if arg == "--config" and index + 1 < len(sys.argv):
            return pathlib.Path(sys.argv[index + 1])
        if arg.startswith("--config="):
            return pathlib.Path(arg.split("=", 1)[1])
    return pathlib.Path("matrix_nlu/train_config.json")


def _load_config() -> dict:
    global CONFIG
    if CONFIG is None:
        CONFIG = json.loads(_config_path().read_text(encoding="utf-8"))
    return CONFIG


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
            functional.cross_entropy(
                outputs["massive_intent"], batch["aux_intent"], ignore_index=IGNORE
            ) * weight
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


base.loss_for = loss_for

if __name__ == "__main__":
    base.main()
