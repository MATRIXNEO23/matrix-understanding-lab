"""Physical pristine BERT/V3/ONNX gate; no training, DEV or Frozen access."""
from __future__ import annotations

import argparse
import hashlib
import importlib.metadata
import json
import pathlib
import platform
import traceback

from contract_v3 import (
    ROLE_HEADS, TOKEN_LABELS, FIXED_SEQUENCE_LABELS, contract_fingerprint,
    write_bundle_contract, load_and_validate_bundle_contract,
)
from export_onnx_v3 import INPUT_NAMES, OUTPUT_NAMES, export_model_v3
from model_v3 import build_model_v3, parameter_summary_v3

MODEL_SHA = "d6e45891d1e0ec4ed023caaeb17c0dd0ae80a93b8bf877d275310b7f2837efa2"
FINGERPRINT = "7b0646e44243ad897760c0fcadbe141f1b8e88e3fd8d63a1789106571b9987b0"
TRAIN_SHA = "1118a900026f48cfcc290c3f9dc52a1a019a6a1f4761661f326c33770523140e"


def digest(path):
    h = hashlib.sha256()
    with pathlib.Path(path).open("rb") as f:
        for block in iter(lambda: f.read(1024 * 1024), b""):
            h.update(block)
    return h.hexdigest()


def save_json(path, value):
    pathlib.Path(path).write_text(json.dumps(value, indent=2, ensure_ascii=False) + "\n")


def flatten(result):
    values = []
    for name in OUTPUT_NAMES:
        parts = name.split(".")
        value = result["tokens" if parts[0] == "token" else "sequence"][parts[1]]
        if len(parts) == 3:
            value = value[parts[2]]
        values.append(value)
    return values


def run(args):
    import numpy as np
    import torch
    import onnx
    import onnxruntime as ort
    from transformers import BertModel, XLMRobertaTokenizer
    from safetensors.torch import save_file

    out = pathlib.Path(args.output)
    out.mkdir(parents=True, exist_ok=False)
    report = {
        "artifactId": args.artifact_id, "sourceCommit": args.source_commit,
        "status": "RUNNING", "stage": "A1", "seed": 3401,
        "qualityMeaning": "UNTRAINED_RUNTIME_MECHANICS_ONLY",
        "trainingExecuted": False, "optimizerCreated": False,
        "backpropExecuted": False, "devRead": False, "frozenRead": False,
        "pristineModified": False, "pathAModified": False, "student4Modified": False,
        "environment": {"python": platform.python_version(), "platform": platform.platform()},
    }
    for name in ("torch", "transformers", "onnx", "onnxruntime", "numpy", "sentencepiece", "safetensors"):
        report["environment"][name] = importlib.metadata.version(name)
    try:
        model_path = pathlib.Path(args.model)
        assert digest(model_path / "model.safetensors") == MODEL_SHA
        manifest = json.loads((model_path / "candidate-manifest.json").read_text())
        for entry in manifest["files"]:
            p = model_path / entry["path"]
            assert p.stat().st_size == entry["bytes"] and digest(p) == entry["sha256"]
        train = pathlib.Path(args.train_artifact)
        for line in (train / "SHA256SUMS").read_text().splitlines():
            expected, name = line.split(maxsplit=1)
            assert digest(train / name.lstrip("*")) == expected
        train_manifest = json.loads((train / "migration-manifest.json").read_text())
        train_hash = hashlib.sha256()
        for entry in train_manifest["outputFiles"]:
            train_hash.update((train / entry["path"]).read_bytes())
        assert train_hash.hexdigest() == TRAIN_SHA
        assert contract_fingerprint() == FINGERPRINT
        report["trainLogicalSha256"] = TRAIN_SHA
        report["pristineSha256"] = MODEL_SHA
        report["contractFingerprint"] = FINGERPRINT
        report["stage"] = "A2"
        save_json(out / "report.json", report)
        torch.manual_seed(3401)
        torch.set_num_threads(2)
        torch.set_num_interop_threads(1)
        tokenizer = XLMRobertaTokenizer.from_pretrained(str(model_path), local_files_only=True)
        encoder = BertModel.from_pretrained(str(model_path), local_files_only=True, attn_implementation="eager").eval()
        assert len(tokenizer) == 40000 and encoder.config.vocab_size == 40000
        assert [tokenizer.bos_token_id, tokenizer.pad_token_id, tokenizer.eos_token_id, tokenizer.unk_token_id, tokenizer.mask_token_id] == [0, 1, 2, 3, 39999]
        model = build_model_v3(encoder=encoder).eval()
        for p in model.parameters():
            p.requires_grad_(False)
        report["parameters"] = parameter_summary_v3(model)
        assert report["parameters"]["encoderLayers"] == 12
        assert report["parameters"]["hiddenSize"] == 384

        def inputs(texts, candidates, anchors):
            encoded = tokenizer(texts, padding=True, return_tensors="pt")
            ids, mask = encoded["input_ids"], encoded["attention_mask"]
            with torch.no_grad():
                hidden = encoder(input_ids=ids, attention_mask=mask).last_hidden_state
            # Runtime probes use real hidden vectors. These are not gold mention
            # candidates and cannot prove learned role resolution or NLU quality.
            ci = torch.arange(candidates) % hidden.shape[1]
            ai = torch.arange(anchors) % hidden.shape[1]
            ce, ae = hidden[:, ci].contiguous(), hidden[:, ai].contiguous()
            cm = torch.ones((len(texts), candidates), dtype=torch.long)
            am = torch.ones((len(texts), anchors), dtype=torch.long)
            if candidates > 2:
                cm[:, -1] = 0
            if anchors > 1:
                am[:, -1] = 0
            return ids, mask, ce, cm, ae, am

        probes = [
            (["Abito a Roma."], 4, 3),
            (["I do not live in Rome.", "No vivo en Roma."], 7, 2),
            (["Ieri vivevo a Padova, oggi abito a Roma."], 2, 1),
            (["Maybe Anna will arrive tomorrow.", "Prima lavoravo a Milano.", "Ana dice que vive en Madrid."], 16, 5),
        ]
        sample = inputs(*probes[0])
        with torch.no_grad():
            first = flatten(model(*sample))
        assert len(first) == 17
        report["a2"] = {"status": "PASS", "shapes": {n: list(t.shape) for n, t in zip(OUTPUT_NAMES, first)}}
        print("A2 REAL BERT/V3 FORWARD PASS", flush=True)
        save_json(out / "report.json", report)

        report["stage"] = "A3"
        onnx_path = out / "student5-v3-untrained-fp32.onnx"
        spec = export_model_v3(model, sample, onnx_path)
        graph = onnx.load(str(onnx_path))
        onnx.helper.set_model_props(graph, {"contractFingerprintSha256": FINGERPRINT, "artifactId": args.artifact_id, "qualityMeaning": report["qualityMeaning"]})
        onnx.save(graph, str(onnx_path))
        onnx.checker.check_model(str(onnx_path))
        assert [i.name for i in graph.graph.input] == list(INPUT_NAMES)
        assert [o.name for o in graph.graph.output] == list(OUTPUT_NAMES)
        assert all(node.domain in ("", "ai.onnx") for node in graph.graph.node)
        options = ort.SessionOptions()
        options.intra_op_num_threads = 2
        options.inter_op_num_threads = 1
        session = ort.InferenceSession(str(onnx_path), options, providers=["CPUExecutionProvider"])
        assert session.get_modelmeta().custom_metadata_map["contractFingerprintSha256"] == FINGERPRINT
        report["probes"] = []
        for texts, candidates, anchors in probes:
            batch = inputs(texts, candidates, anchors)
            with torch.no_grad():
                expected = [t.numpy() for t in flatten(model(*batch))]
            actual = session.run(None, {name: t.numpy() for name, t in zip(INPUT_NAMES, batch)})
            entry = {"texts": texts, "batch": len(texts), "sequence": batch[0].shape[1], "candidates": candidates, "anchors": anchors, "outputs": {}}
            for name, a, b in zip(OUTPUT_NAMES, expected, actual):
                assert a.shape == b.shape, name
                assert np.isfinite(a).all() and np.isfinite(b).all(), name
                np.testing.assert_allclose(b, a, rtol=1e-4, atol=1e-4, err_msg=name)
                if name.startswith("token."):
                    assert b.shape == (len(texts), batch[0].shape[1], len(TOKEN_LABELS[name.split('.')[1]]))
                elif name in ["sequence." + n for n in ROLE_HEADS]:
                    assert b.shape == (len(texts), candidates + 2)
                    if candidates > 2:
                        assert (b[:, candidates - 1] == -1e4).all()
                elif name.endswith(".anchor"):
                    assert b.shape == (len(texts), anchors)
                    if anchors > 1:
                        assert (b[:, -1] == -1e4).all()
                entry["outputs"][name] = {"shape": list(b.shape), "maxAbsoluteDelta": float(np.max(np.abs(a - b))), "argmaxEqual": bool(np.array_equal(a.argmax(-1), b.argmax(-1)))}
            report["probes"].append(entry)
        report["a3"] = {"status": "PASS", "spec": spec, "operators": sorted(set(n.op_type for n in graph.graph.node)), "numericalTolerance": {"atol": 1e-4, "rtol": 1e-4}, "probes": len(probes)}
        save_file({k: v.contiguous() for k, v in model.state_dict().items()}, str(out / "student5-v3-untrained.safetensors"))
        write_bundle_contract(out)
        load_and_validate_bundle_contract(out)
        assert digest(model_path / "model.safetensors") == MODEL_SHA
        report["status"] = "PHYSICAL_GATE_A_RUNTIME_PASS_PENDING_DURABLE_PUBLICATION"
        report["stage"] = "A4_PENDING"
        report["artifacts"] = {p.name: {"bytes": p.stat().st_size, "sha256": digest(p)} for p in out.iterdir() if p.is_file() and p.name != "report.json"}
        print("A3 ONNX CHECK/LOAD/DYNAMIC FORWARD/PARITY PASS", flush=True)
    except Exception:
        report["status"] = "FAIL"
        report["error"] = traceback.format_exc()
        raise
    finally:
        save_json(out / "report.json", report)
        sums = "".join(f"{digest(p)}  {p.name}\n" for p in sorted(out.iterdir()) if p.is_file() and p.name != "SHA256SUMS")
        (out / "SHA256SUMS").write_text(sums)


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    for arg in ("model", "train-artifact", "output", "source-commit", "artifact-id"):
        parser.add_argument("--" + arg, required=True)
    run(parser.parse_args())
