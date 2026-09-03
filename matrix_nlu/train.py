#!/usr/bin/env python3
"""Resumable staged training for the canonical learned Matrix-NLU."""

from __future__ import annotations

import argparse
import hashlib
import json
import math
import pathlib
import random
import time
from collections import defaultdict

from labels import SEQUENCE_LABELS, TOKEN_LABELS
from model import build_model, parameter_summary
from training_data import (IGNORE, ExampleDataset, massive_examples, massive_slot_vocab,
                           matrix_examples, read_jsonl)
from pipeline_support import atomic_json


def seed_everything(seed: int):
    import numpy as np
    import torch
    random.seed(seed)
    np.random.seed(seed)
    torch.manual_seed(seed)
    torch.use_deterministic_algorithms(True)


def sha256(path: pathlib.Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def move(batch, device):
    return {key: ({name: value.to(device) for name, value in item.items()}
                  if isinstance(item, dict) else item.to(device))
            for key, item in batch.items()}


def loss_for(outputs, batch):
    import torch
    import torch.nn.functional as functional
    terms = []
    for head, logits in outputs["tokens"].items():
        labels = batch["token_labels"][head]
        if torch.any(labels != IGNORE):
            terms.append(functional.cross_entropy(logits.reshape(-1, logits.shape[-1]),
                                                  labels.reshape(-1), ignore_index=IGNORE))
    for head, logits in outputs["sequence"].items():
        labels = batch["sequence_labels"][head]
        if torch.any(labels != IGNORE):
            terms.append(functional.cross_entropy(logits, labels, ignore_index=IGNORE))
    if torch.any(batch["aux_intent"] != IGNORE):
        terms.append(functional.cross_entropy(outputs["massive_intent"], batch["aux_intent"],
                                              ignore_index=IGNORE))
    if torch.any(batch["aux_slot"] != IGNORE):
        terms.append(functional.cross_entropy(outputs["massive_slot"].reshape(-1, outputs["massive_slot"].shape[-1]),
                                              batch["aux_slot"].reshape(-1), ignore_index=IGNORE))
    if not terms:
        raise ValueError("batch has no supervised head")
    return sum(terms) / len(terms)


def evaluate(model, loader, device) -> dict:
    import torch
    totals = defaultdict(int)
    correct = defaultdict(int)
    losses = []
    model.eval()
    with torch.no_grad():
        for raw in loader:
            batch = move(raw, device)
            outputs = model(batch["input_ids"], batch["attention_mask"])
            losses.append(float(loss_for(outputs, batch)))
            for group, label_group in (("tokens", batch["token_labels"]),
                                       ("sequence", batch["sequence_labels"])):
                for head, logits in outputs[group].items():
                    labels = label_group[head]
                    mask = labels != IGNORE
                    key = f"{group}.{head}"
                    totals[key] += int(mask.sum())
                    correct[key] += int(((logits.argmax(-1) == labels) & mask).sum())
            for key, logits, labels in (("massive.intent", outputs["massive_intent"], batch["aux_intent"]),
                                        ("massive.slot", outputs["massive_slot"], batch["aux_slot"])):
                mask = labels != IGNORE
                totals[key] += int(mask.sum())
                correct[key] += int(((logits.argmax(-1) == labels) & mask).sum())
    accuracies = {key: correct[key] / totals[key] for key in totals if totals[key]}
    score = sum(accuracies.values()) / max(1, len(accuracies))
    return {"loss": sum(losses) / max(1, len(losses)), "macroHeadAccuracy": score,
            "accuracy": dict(sorted(accuracies.items())), "supervisedCounts": dict(sorted(totals.items()))}


def train_stage(model, train_loader, dev_loaders, device, stage: str, epochs: int,
                config: dict, output_dir: pathlib.Path, resume: dict | None = None):
    import torch
    optimizer = torch.optim.AdamW(model.parameters(), lr=config["matrix"]["learningRate"],
                                  weight_decay=config["matrix"]["weightDecay"])
    accumulation = config["matrix"]["gradientAccumulation"]
    updates_per_epoch = math.ceil(len(train_loader) / accumulation)
    total_updates = max(1, updates_per_epoch * epochs)
    warmup = int(total_updates * config["matrix"]["warmupRatio"])
    scheduler = torch.optim.lr_scheduler.LambdaLR(
        optimizer, lambda step: min(1.0, (step + 1) / max(1, warmup)) *
        max(0.0, (total_updates - step) / max(1, total_updates - warmup)))
    start_epoch = 0
    best_score = -1.0
    best_state = None
    history = []
    epochs_without_improvement = 0
    if resume and resume.get("stage") == stage:
        model.load_state_dict(resume["model"])
        optimizer.load_state_dict(resume["optimizer"])
        scheduler.load_state_dict(resume["scheduler"])
        start_epoch = resume["nextEpoch"]
        best_score = resume["bestScore"]
        best_state = resume.get("bestModel")
        history = resume.get("history", [])
        epochs_without_improvement = resume.get("epochsWithoutImprovement", 0)
    for epoch in range(start_epoch, epochs):
        model.train()
        optimizer.zero_grad(set_to_none=True)
        running = 0.0
        started = time.monotonic()
        for batch_index, raw in enumerate(train_loader):
            batch = move(raw, device)
            loss = loss_for(model(batch["input_ids"], batch["attention_mask"]), batch)
            (loss / accumulation).backward()
            running += float(loss.detach())
            if (batch_index + 1) % accumulation == 0 or batch_index + 1 == len(train_loader):
                torch.nn.utils.clip_grad_norm_(model.parameters(), 1.0)
                optimizer.step()
                scheduler.step()
                optimizer.zero_grad(set_to_none=True)
            if (batch_index + 1) % 50 == 0 or batch_index + 1 == len(train_loader):
                atomic_json(output_dir / "training-progress.json", {
                    "schemaVersion": "matrix.nlu.training-progress.v1", "status": "RUNNING",
                    "stage": stage, "epoch": epoch + 1, "epochs": epochs,
                    "batch": batch_index + 1, "batches": len(train_loader),
                    "fraction": (batch_index + 1) / max(1, len(train_loader)),
                    "runningLoss": running / (batch_index + 1),
                    "elapsedSeconds": time.monotonic() - started,
                })
        dev = {name: evaluate(model, loader, device) for name, loader in dev_loaders.items()}
        score = sum(value["macroHeadAccuracy"] for value in dev.values()) / len(dev)
        entry = {"stage": stage, "epoch": epoch + 1,
                 "trainLoss": running / max(1, len(train_loader)), "dev": dev,
                 "selectionScore": score, "seconds": time.monotonic() - started}
        history.append(entry)
        print(json.dumps(entry, ensure_ascii=False))
        if score > best_score:
            best_score = score
            best_state = {key: value.detach().cpu().clone() for key, value in model.state_dict().items()}
            epochs_without_improvement = 0
        else:
            epochs_without_improvement += 1
        checkpoint = {"stage": stage, "nextEpoch": epoch + 1, "model": model.state_dict(),
                      "optimizer": optimizer.state_dict(), "scheduler": scheduler.state_dict(),
                      "bestScore": best_score, "bestModel": best_state, "history": history,
                      "epochsWithoutImprovement": epochs_without_improvement}
        torch.save(checkpoint, output_dir / "checkpoints" / "latest.pt")
        atomic_json(output_dir / "training-progress.json", {
            "schemaVersion": "matrix.nlu.training-progress.v1", "status": "EPOCH_COMPLETE",
            "stage": stage, "epoch": epoch + 1, "epochs": epochs,
            "bestScore": best_score, "epochsWithoutImprovement": epochs_without_improvement,
            "checkpoint": str(output_dir / "checkpoints" / "latest.pt"),
        })
        patience = config["matrix"].get("earlyStoppingPatience")
        if patience is not None and epochs_without_improvement >= int(patience):
            print(json.dumps({"stage": stage, "event": "EARLY_STOP",
                              "patience": int(patience), "epoch": epoch + 1}))
            break
    model.load_state_dict(best_state)
    return history, best_score


def loader(examples, batch_size, shuffle, seed):
    import torch
    generator = torch.Generator().manual_seed(seed)
    return torch.utils.data.DataLoader(ExampleDataset(examples), batch_size=batch_size,
                                       shuffle=shuffle, generator=generator, num_workers=0)


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--config", type=pathlib.Path, default=pathlib.Path("matrix_nlu/train_config.json"))
    parser.add_argument("--data-dir", type=pathlib.Path, default=pathlib.Path("build/matrix-nlu/data"))
    parser.add_argument("--massive-dir", type=pathlib.Path, default=pathlib.Path("build/matrix-nlu/massive"))
    parser.add_argument("--output-dir", type=pathlib.Path, default=pathlib.Path("build/matrix-nlu/training"))
    parser.add_argument("--student-layers", type=int)
    args = parser.parse_args()
    import torch
    from transformers import AutoTokenizer

    config_bytes = args.config.read_bytes()
    config = json.loads(config_bytes)
    seed_everything(config["seed"])
    torch.set_num_threads(4)
    args.output_dir.mkdir(parents=True, exist_ok=True)
    (args.output_dir / "checkpoints").mkdir(parents=True, exist_ok=True)
    model_spec = config["model"]
    tokenizer = AutoTokenizer.from_pretrained(model_spec["repository"], revision=model_spec["revision"],
                                              use_fast=True, trust_remote_code=False)
    labels = json.loads((args.massive_dir / "massive-labels.json").read_text())
    slot_vocab = massive_slot_vocab(labels["slotTypes"])
    network = build_model(model_spec["repository"], model_spec["revision"], len(labels["intents"]),
                          len(slot_vocab), args.student_layers)
    device = torch.device("cpu")
    network.to(device)
    batch_size = config["matrix"]["batchSize"]
    max_length = config["maxLength"]

    massive_train_rows = read_jsonl([args.massive_dir / "massive-train.jsonl"])
    massive_dev_rows = read_jsonl([args.massive_dir / "massive-dev.jsonl"])
    massive_test_rows = read_jsonl([args.massive_dir / "massive-test.jsonl"])
    intent_ids = {value: index for index, value in enumerate(labels["intents"])}
    massive_train = massive_examples(massive_train_rows, tokenizer, max_length, intent_ids, labels["slotTypes"])
    massive_dev = massive_examples(massive_dev_rows, tokenizer, max_length, intent_ids, labels["slotTypes"])
    massive_test = massive_examples(massive_test_rows, tokenizer, max_length, intent_ids, labels["slotTypes"])

    matrix_train_rows = read_jsonl([args.data_dir / "matrix-train.jsonl"])
    p05_train_rows = read_jsonl([args.data_dir / "p05-train.jsonl"])
    matrix_train_rows += p05_train_rows * config["matrix"]["p05TrainRepeat"]
    matrix_dev_rows = read_jsonl([args.data_dir / "matrix-dev.jsonl"])
    p05_dev_rows = read_jsonl([args.data_dir / "p05-dev.jsonl"])
    matrix_test_rows = read_jsonl([args.data_dir / "matrix-test.jsonl"])
    p05_test_rows = read_jsonl([args.data_dir / "p05-test.jsonl"])
    matrix_train = matrix_examples(matrix_train_rows, tokenizer, max_length)
    matrix_dev = matrix_examples(matrix_dev_rows, tokenizer, max_length)
    p05_dev = matrix_examples(p05_dev_rows, tokenizer, max_length)
    matrix_test = matrix_examples(matrix_test_rows, tokenizer, max_length)
    p05_test = matrix_examples(p05_test_rows, tokenizer, max_length)

    resume = None
    checkpoint_path = args.output_dir / "checkpoints" / "latest.pt"
    if config.get("resume") == "auto" and checkpoint_path.exists():
        resume = torch.load(checkpoint_path, map_location="cpu", weights_only=False)
    history = []
    aux_history, _ = train_stage(
        network, loader(massive_train, batch_size, True, config["seed"]),
        {"massiveDev": loader(massive_dev, batch_size * 2, False, config["seed"])},
        device, "massive-aux", config["massive"]["epochs"], config, args.output_dir, resume)
    history.extend(aux_history)
    matrix_history, best = train_stage(
        network, loader(matrix_train, batch_size, True, config["seed"] + 1),
        {"matrixDev": loader(matrix_dev, batch_size * 2, False, config["seed"]),
         "p05Dev": loader(p05_dev, batch_size * 2, False, config["seed"])},
        device, "matrix", config["matrix"]["epochs"], config, args.output_dir,
        resume if resume and resume.get("stage") == "matrix" else None)
    history.extend(matrix_history)

    # Frozen tests are touched only after the dev-selected model is loaded.
    frozen = {
        "matrixTest": evaluate(network, loader(matrix_test, batch_size * 2, False, config["seed"]), device),
        "p05Test": evaluate(network, loader(p05_test, batch_size * 2, False, config["seed"]), device),
        "massiveTest": evaluate(network, loader(massive_test, batch_size * 2, False, config["seed"]), device),
    }
    torch.save(network.state_dict(), args.output_dir / "model-state.pt")
    tokenizer.save_pretrained(args.output_dir / "tokenizer")
    (args.output_dir / "labels.json").write_text(json.dumps({"sequence": SEQUENCE_LABELS,
        "tokens": TOKEN_LABELS, "massiveIntents": labels["intents"], "massiveSlots": slot_vocab}, indent=2) + "\n")
    result = {"schemaVersion": "matrix.nlu.training-result.v1",
              "configSha256": hashlib.sha256(config_bytes).hexdigest(),
              "config": config, "studentLayers": args.student_layers,
              "parameters": parameter_summary(network), "bestDevScore": best,
              "history": history, "frozen": frozen}
    result["inputHashes"] = {str(path): sha256(path) for path in
                             list(sorted(args.data_dir.glob("*.jsonl"))) +
                             list(sorted(args.massive_dir.glob("massive-*.jsonl")))}
    result["modelStateSha256"] = sha256(args.output_dir / "model-state.pt")
    (args.output_dir / "training-result.json").write_text(json.dumps(result, indent=2) + "\n")
    print(json.dumps({"bestDevScore": best, "parameters": result["parameters"],
                      "frozen": frozen, "modelStateSha256": result["modelStateSha256"]}, indent=2))


if __name__ == "__main__":
    main()
