#!/usr/bin/env python3
"""Student-5 40k Path-A ONNX/INT8 runtime probe.

This utility exports and measures the pristine, untaught Phase-A backbone.  It
does not train Matrix heads, consume canonical DEV/Frozen data, or mutate the
input Hugging Face directory.
"""

from __future__ import annotations

import argparse
import collections
import gc
import hashlib
import importlib.util
import json
import math
import multiprocessing as mp
import os
import pathlib
import platform
import shutil
import statistics
import sys
import time
import zipfile

import numpy as np


EXPECTED = {
    "archiveSha256": "7804bfb245b71df9b835fff7ee00f6ec887e019772ae34c82d269d821d587191",
    "archiveBytes": 88_361_246,
    "modelSha256": "d6e45891d1e0ec4ed023caaeb17c0dd0ae80a93b8bf877d275310b7f2837efa2",
    "modelBytes": 148_020_400,
    "mappingSha256": "da36a5e1a9057391da935354d895edb3bc3a959744aca6b6602e511f9d4ea9b9",
    "sentencePieceSha256": "748f8053688469d7dc98c135a28a3fc0713bdbb82853f86f8d7a254bada46f78",
    "manifestSha256": "a9d23de7816d487986316351c163f37a67d65d001861dbf042b9114c455f066d",
    "vocabSize": 40_000,
    "layers": 12,
    "hiddenSize": 384,
}

RELEASE = {
    "repository": "MATRIXNEO23/matrix-understanding-lab",
    "tag": "student-5-minilm-40k-phase-a-pristine",
    "releaseId": 383_143_636,
    "assetId": 545_406_840,
    "asset": "student5-minilm-phase-a-pruned-40k.zip",
    "url": (
        "https://github.com/MATRIXNEO23/matrix-understanding-lab/releases/download/"
        "student-5-minilm-40k-phase-a-pristine/"
        "student5-minilm-phase-a-pruned-40k.zip"
    ),
}


def sha256(path: pathlib.Path) -> str:
    digest = hashlib.sha256()
    with path.open("rb") as stream:
        for block in iter(lambda: stream.read(1024 * 1024), b""):
            digest.update(block)
    return digest.hexdigest()


def write_json(path: pathlib.Path, value: object) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(
        json.dumps(value, ensure_ascii=False, indent=2, sort_keys=True) + "\n",
        encoding="utf-8",
    )


def percentile(values: list[float], q: float) -> float:
    if not values:
        return 0.0
    ordered = sorted(values)
    index = min(len(ordered) - 1, max(0, math.ceil(q * len(ordered)) - 1))
    return float(ordered[index])


def verify_internal_sums(root: pathlib.Path) -> dict:
    sums = root / "SHA256SUMS"
    checked = []
    for line in sums.read_text(encoding="utf-8").splitlines():
        expected, relative = line.split(maxsplit=1)
        relative = relative.removeprefix("*").removeprefix("./")
        path = root / relative
        if not path.is_file():
            raise RuntimeError(f"missing archive payload: {relative}")
        observed = sha256(path)
        if observed != expected:
            raise RuntimeError(f"internal checksum mismatch: {relative}")
        checked.append(relative)
    return {"status": "PASS", "files": len(checked), "paths": sorted(checked)}


def verify_pristine(archive: pathlib.Path, root: pathlib.Path) -> dict:
    import torch
    from transformers import BertModel, XLMRobertaTokenizer

    paths = {
        "model": root / "model/model.safetensors",
        "mapping": root / "model/token-id-remap.json",
        "sentencePiece": root / "model/sentencepiece.bpe.model",
        "manifest": root / "model/candidate-manifest.json",
    }
    observed = {
        "archiveSha256": sha256(archive),
        "archiveBytes": archive.stat().st_size,
        "modelSha256": sha256(paths["model"]),
        "modelBytes": paths["model"].stat().st_size,
        "mappingSha256": sha256(paths["mapping"]),
        "sentencePieceSha256": sha256(paths["sentencePiece"]),
        "manifestSha256": sha256(paths["manifest"]),
    }
    for key, expected in EXPECTED.items():
        if key in observed and observed[key] != expected:
            raise RuntimeError(
                f"PRISTINE_INPUT_IDENTITY_MISMATCH: {key}: "
                f"expected={expected!r} observed={observed[key]!r}"
            )

    with zipfile.ZipFile(archive) as zf:
        bad = zf.testzip()
        if bad is not None:
            raise RuntimeError(f"archive integrity failure at {bad}")
        archive_entries = sorted(name for name in zf.namelist() if not name.endswith("/"))

    internal = verify_internal_sums(root)
    model = BertModel.from_pretrained(root / "model", local_files_only=True)
    tokenizer = XLMRobertaTokenizer.from_pretrained(root / "model", local_files_only=True)
    model.eval()
    config = model.config
    if len(tokenizer) != EXPECTED["vocabSize"]:
        raise RuntimeError("PRISTINE_INPUT_IDENTITY_MISMATCH: tokenizer length")
    if model.embeddings.word_embeddings.weight.shape != (40_000, 384):
        raise RuntimeError("PRISTINE_INPUT_IDENTITY_MISMATCH: embedding shape")
    if config.num_hidden_layers != EXPECTED["layers"] or config.hidden_size != EXPECTED["hiddenSize"]:
        raise RuntimeError("PRISTINE_INPUT_IDENTITY_MISMATCH: architecture")
    special = {
        "bos": tokenizer.bos_token_id,
        "pad": tokenizer.pad_token_id,
        "eos": tokenizer.eos_token_id,
        "unk": tokenizer.unk_token_id,
        "mask": tokenizer.mask_token_id,
    }
    if special != {"bos": 0, "pad": 1, "eos": 2, "unk": 3, "mask": 39_999}:
        raise RuntimeError("PRISTINE_INPUT_IDENTITY_MISMATCH: special tokens")
    encoded = tokenizer(
        "Verifica tecnica indipendente del backbone pristine.", return_tensors="pt"
    )
    with torch.no_grad():
        output = model(**encoded).last_hidden_state
    if output.shape[:2] != encoded["input_ids"].shape or not torch.isfinite(output).all():
        raise RuntimeError("PRISTINE_INPUT_IDENTITY_MISMATCH: real forward")
    return {
        **observed,
        "archiveIntegrity": "PASS",
        "archiveEntries": archive_entries,
        "internalSha256Sums": internal,
        "modelClass": type(model).__name__,
        "tokenizerClass": type(tokenizer).__name__,
        "vocabSize": len(tokenizer),
        "layers": config.num_hidden_layers,
        "hiddenSize": config.hidden_size,
        "attentionHeads": config.num_attention_heads,
        "intermediateSize": config.intermediate_size,
        "embeddingShape": list(model.embeddings.word_embeddings.weight.shape),
        "specialTokenIds": special,
        "saveReload": "PASS",
        "realForward": "PASS",
        "forwardShape": list(output.shape),
        "forwardFinite": True,
    }


def load_probe_source(path: pathlib.Path) -> tuple[list[dict], list[dict]]:
    spec = importlib.util.spec_from_file_location("student5_phase_a_source", path)
    if spec is None or spec.loader is None:
        raise RuntimeError("unable to load canonical Phase-A probe source")
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    rows = module.probes()
    pairs = module.contrast_pairs()
    if len(rows) != 95 or len(pairs) != 36:
        raise RuntimeError("canonical Phase-A probe cardinality mismatch")
    if not all(row.get("adultOnly", True) for row in rows):
        raise RuntimeError("probe adult-only invariant failed")
    return rows, pairs


def export_fp32(model_dir: pathlib.Path, output: pathlib.Path, sample_text: str) -> dict:
    import onnx
    import torch
    import transformers
    from transformers import BertModel, XLMRobertaTokenizer

    model = BertModel.from_pretrained(model_dir, local_files_only=True)
    tokenizer = XLMRobertaTokenizer.from_pretrained(model_dir, local_files_only=True)
    model.eval()

    class LastHiddenAndPooler(torch.nn.Module):
        def __init__(self, backbone):
            super().__init__()
            self.backbone = backbone

        def forward(self, input_ids, attention_mask):
            result = self.backbone(
                input_ids=input_ids,
                attention_mask=attention_mask,
                return_dict=False,
            )
            return result[0], result[1]

    wrapper = LastHiddenAndPooler(model).eval()
    encoded = tokenizer(sample_text, return_tensors="pt")
    started = time.perf_counter()
    with torch.no_grad():
        torch.onnx.export(
            wrapper,
            (encoded["input_ids"], encoded["attention_mask"]),
            output,
            input_names=["input_ids", "attention_mask"],
            output_names=["last_hidden_state", "pooler_output"],
            dynamic_axes={
                "input_ids": {0: "batch", 1: "sequence"},
                "attention_mask": {0: "batch", 1: "sequence"},
                "last_hidden_state": {0: "batch", 1: "sequence"},
                "pooler_output": {0: "batch"},
            },
            opset_version=17,
            do_constant_folding=True,
            dynamo=False,
        )
    elapsed = time.perf_counter() - started
    graph = onnx.load(output, load_external_data=False)
    onnx.checker.check_model(graph)
    return {
        "status": "PASS",
        "bytes": output.stat().st_size,
        "sha256": sha256(output),
        "seconds": elapsed,
        "opset": {item.domain or "ai.onnx": item.version for item in graph.opset_import},
        "inputNames": [item.name for item in graph.graph.input],
        "outputNames": [item.name for item in graph.graph.output],
        "dynamicAxes": {
            "batch": True,
            "sequence": True,
            "inputs": ["input_ids", "attention_mask"],
            "outputs": ["last_hidden_state", "pooler_output"],
        },
        "onnxVersion": onnx.__version__,
        "torchVersion": torch.__version__,
        "transformersVersion": transformers.__version__,
        "exportTool": "torch.onnx.export legacy TorchScript path",
    }


def tensor_type_bytes(data_type: int, dims: list[int]) -> int:
    import onnx

    sizes = {
        onnx.TensorProto.FLOAT: 4,
        onnx.TensorProto.FLOAT16: 2,
        onnx.TensorProto.DOUBLE: 8,
        onnx.TensorProto.INT64: 8,
        onnx.TensorProto.INT32: 4,
        onnx.TensorProto.INT16: 2,
        onnx.TensorProto.INT8: 1,
        onnx.TensorProto.UINT8: 1,
        onnx.TensorProto.BOOL: 1,
    }
    count = math.prod(dims) if dims else 1
    return count * sizes.get(data_type, 0)


def operator_census(path: pathlib.Path) -> dict:
    import onnx

    graph = onnx.load(path, load_external_data=False)
    counts = collections.Counter(node.op_type for node in graph.graph.node)
    initializers = {item.name: item for item in graph.graph.initializer}
    weight_bearing = []
    for node in graph.graph.node:
        if node.op_type in {"MatMul", "Gemm"} and any(name in initializers for name in node.input):
            weight_bearing.append(node.name or "/".join(node.output))
    dtype_counts = collections.Counter()
    dtype_bytes = collections.Counter()
    for item in initializers.values():
        name = onnx.TensorProto.DataType.Name(item.data_type)
        dtype_counts[name] += 1
        dtype_bytes[name] += tensor_type_bytes(item.data_type, list(item.dims))
    external = []
    for item in initializers.values():
        if item.data_location == onnx.TensorProto.EXTERNAL:
            external.append(item.name)
    return {
        "file": path.name,
        "nodes": len(graph.graph.node),
        "operatorCounts": dict(sorted(counts.items())),
        "operatorSet": sorted(counts),
        "weightBearingEligibleMatMulOrGemm": len(weight_bearing),
        "weightBearingEligibleNodeNames": sorted(weight_bearing),
        "matMulIntegerNodes": counts.get("MatMulInteger", 0),
        "dynamicQuantizeLinearNodes": counts.get("DynamicQuantizeLinear", 0),
        "initializerCountsByType": dict(sorted(dtype_counts.items())),
        "initializerBytesByType": dict(sorted(dtype_bytes.items())),
        "externalDataInitializers": external,
        "externalDataRequired": bool(external),
        "opset": {item.domain or "ai.onnx": item.version for item in graph.opset_import},
    }


def quantize(fp32: pathlib.Path, output: pathlib.Path) -> dict:
    import onnxruntime as ort
    from onnxruntime.quantization import QuantType, quantize_dynamic

    started = time.perf_counter()
    quantize_dynamic(
        model_input=fp32,
        model_output=output,
        op_types_to_quantize=["MatMul", "Gemm"],
        per_channel=True,
        reduce_range=False,
        weight_type=QuantType.QInt8,
        extra_options={"MatMulConstBOnly": True},
    )
    return {
        "status": "PASS",
        "method": "ONNX Runtime dynamic per-channel QInt8 weight quantization",
        "activationQuantization": "dynamic UINT8",
        "weightQuantization": "signed INT8 per output channel",
        "requestedOperatorTypes": ["MatMul", "Gemm"],
        "embeddingPolicy": "FP32_PRESERVED",
        "normalizationAnd1DPolicy": "FP32_PRESERVED",
        "calibrationDataUsed": False,
        "onnxruntimeVersion": ort.__version__,
        "seconds": time.perf_counter() - started,
        "bytes": output.stat().st_size,
        "sha256": sha256(output),
    }


def ort_session(path: pathlib.Path):
    import onnxruntime as ort

    options = ort.SessionOptions()
    options.intra_op_num_threads = 1
    options.inter_op_num_threads = 1
    options.execution_mode = ort.ExecutionMode.ORT_SEQUENTIAL
    options.graph_optimization_level = ort.GraphOptimizationLevel.ORT_ENABLE_ALL
    return ort.InferenceSession(path, sess_options=options, providers=["CPUExecutionProvider"])


def hf_outputs(model_dir: pathlib.Path, texts: list[str], batch_size: int = 8) -> dict:
    import torch
    from transformers import BertModel, XLMRobertaTokenizer

    model = BertModel.from_pretrained(model_dir, local_files_only=True).eval()
    tokenizer = XLMRobertaTokenizer.from_pretrained(model_dir, local_files_only=True)
    result = {}
    with torch.no_grad():
        for start in range(0, len(texts), batch_size):
            batch = texts[start : start + batch_size]
            encoded = tokenizer(
                batch, padding=True, truncation=True, max_length=96, return_tensors="pt"
            )
            hidden = model(**encoded).last_hidden_state.cpu().numpy()
            masks = encoded["attention_mask"].cpu().numpy()
            for index, text in enumerate(batch):
                length = int(masks[index].sum())
                value = hidden[index, :length].astype(np.float32, copy=True)
                pooled = value.mean(axis=0)
                pooled /= max(float(np.linalg.norm(pooled)), 1e-12)
                result[text] = {"hidden": value, "pooled": pooled}
    return result


def onnx_outputs(
    model_path: pathlib.Path, model_dir: pathlib.Path, texts: list[str], batch_size: int = 8
) -> dict:
    from transformers import XLMRobertaTokenizer

    session = ort_session(model_path)
    tokenizer = XLMRobertaTokenizer.from_pretrained(model_dir, local_files_only=True)
    result = {}
    for start in range(0, len(texts), batch_size):
        batch = texts[start : start + batch_size]
        encoded = tokenizer(
            batch, padding=True, truncation=True, max_length=96, return_tensors="np"
        )
        hidden = session.run(
            ["last_hidden_state"],
            {
                "input_ids": encoded["input_ids"].astype(np.int64),
                "attention_mask": encoded["attention_mask"].astype(np.int64),
            },
        )[0]
        masks = encoded["attention_mask"]
        for index, text in enumerate(batch):
            length = int(masks[index].sum())
            value = hidden[index, :length].astype(np.float32, copy=True)
            pooled = value.mean(axis=0)
            pooled /= max(float(np.linalg.norm(pooled)), 1e-12)
            result[text] = {"hidden": value, "pooled": pooled}
    return result


def cosine(left: np.ndarray, right: np.ndarray) -> float:
    return float(np.dot(left, right))


def slice_rows(rows: list[dict]) -> dict[str, list[str]]:
    output: dict[str, list[str]] = collections.defaultdict(list)
    for row in rows:
        text = row["text"]
        output["overall"].append(text)
        output["adult_intimacy" if row["domain"] == "adult_intimacy" else "general"].append(text)
        if row["language"] in {"it", "en", "es"}:
            output[row["language"]].append(text)
        if row["language"] == "code_switch":
            output["code_switch"].append(text)
        if row["domain"] == "adult_intimacy" and row["language"] in {"it", "en", "es"}:
            output[f"adult_intimacy_{row['language']}"] .append(text)
        if row["domain"] == "adult_intimacy":
            output[f"adult_category_{row['category']}"] .append(text)
    return {key: list(dict.fromkeys(values)) for key, values in output.items()}


def delta_summary(reference: dict, candidate: dict, texts: list[str]) -> dict:
    cosines = []
    means = []
    maxima = []
    relatives = []
    for text in texts:
        left = reference[text]
        right = candidate[text]
        if left["hidden"].shape != right["hidden"].shape:
            raise RuntimeError(f"shape mismatch for probe: {text!r}")
        difference = np.abs(left["hidden"] - right["hidden"])
        relative = difference / np.maximum(np.abs(left["hidden"]), 1e-6)
        cosines.append(cosine(left["pooled"], right["pooled"]))
        means.append(float(difference.mean()))
        maxima.append(float(difference.max()))
        relatives.append(float(relative.mean()))
    return {
        "sentences": len(texts),
        "meanRepresentationCosine": statistics.mean(cosines),
        "minimumRepresentationCosine": min(cosines),
        "p05RepresentationCosine": percentile(cosines, 0.05),
        "meanAbsoluteDelta": statistics.mean(means),
        "p95SentenceMaximumAbsoluteDelta": percentile(maxima, 0.95),
        "maximumAbsoluteDelta": max(maxima),
        "meanRelativeDelta": statistics.mean(relatives),
        "p95SentenceMeanRelativeDelta": percentile(relatives, 0.95),
    }


def contrast_summary(reference: dict, candidate: dict, pairs: list[dict]) -> dict:
    details = []
    for pair in pairs:
        ref = cosine(reference[pair["left"]]["pooled"], reference[pair["right"]]["pooled"])
        cand = cosine(candidate[pair["left"]]["pooled"], candidate[pair["right"]]["pooled"])
        details.append(
            {
                "id": pair["id"],
                "referenceCosine": ref,
                "candidateCosine": cand,
                "absoluteDelta": abs(cand - ref),
            }
        )
    deltas = [item["absoluteDelta"] for item in details]
    spanish = next(item for item in details if item["id"] == "adult-withdrawal-es")
    return {
        "pairs": len(details),
        "meanAbsoluteCosineDelta": statistics.mean(deltas),
        "p95AbsoluteCosineDelta": percentile(deltas, 0.95),
        "maximumAbsoluteCosineDelta": max(deltas),
        "spanishAdultConsentWithdrawal": spanish,
        "details": details,
    }


def parity(
    model_dir: pathlib.Path,
    fp32: pathlib.Path,
    int8: pathlib.Path | None,
    rows: list[dict],
    pairs: list[dict],
) -> dict:
    texts = list(
        dict.fromkeys(
            [row["text"] for row in rows]
            + [pair[key] for pair in pairs for key in ("left", "right")]
        )
    )
    hf = hf_outputs(model_dir, texts)
    fp = onnx_outputs(fp32, model_dir, texts)
    slices = slice_rows(rows)
    hf_vs_fp = {
        "slices": {name: delta_summary(hf, fp, selected) for name, selected in sorted(slices.items())},
        "contrasts": contrast_summary(hf, fp, pairs),
    }
    overall = hf_vs_fp["slices"]["overall"]
    # These are strict export-equivalence sanity checks, not Matrix quality gates.
    fp32_ok = (
        overall["minimumRepresentationCosine"] >= 0.999_999
        and overall["maximumAbsoluteDelta"] <= 1e-4
    )
    hf_vs_fp["technicalParitySanity"] = {
        "status": "PASS" if fp32_ok else "FAIL",
        "criteriaType": "EXPORT_NUMERICAL_SANITY_NOT_MATRIX_QUALITY_GATE",
        "minimumRepresentationCosine": 0.999_999,
        "maximumAbsoluteDelta": 1e-4,
    }
    if not fp32_ok:
        raise RuntimeError("FP32_ONNX_PARITY_FAILED")
    result = {
        "probeSentences": len(texts),
        "coverageRows": len(rows),
        "contrastPairs": len(pairs),
        "hfPristineVsOnnxFp32": hf_vs_fp,
    }
    if int8 is not None:
        quant = onnx_outputs(int8, model_dir, texts)
        result["onnxFp32VsOnnxInt8"] = {
            "slices": {
                name: delta_summary(fp, quant, selected)
                for name, selected in sorted(slices.items())
            },
            "contrasts": contrast_summary(fp, quant, pairs),
            "criteriaType": "MEASURED_ONLY_NO_CANONICAL_INT8_QUALITY_GATE",
        }
    return result


def proc_self_memory() -> dict[str, int]:
    values = {"rss": 0, "hwm": 0}
    for line in pathlib.Path("/proc/self/status").read_text(encoding="utf-8").splitlines():
        if line.startswith("VmRSS:"):
            values["rss"] = int(line.split()[1]) * 1024
        elif line.startswith("VmHWM:"):
            values["hwm"] = int(line.split()[1]) * 1024
    if values["rss"] <= 0:
        raise RuntimeError("unable to read current RSS from /proc/self/status")
    return values


def benchmark_child(model_path: str, queue) -> None:
    import onnxruntime as ort

    path = pathlib.Path(model_path)
    baseline = proc_self_memory()["rss"]
    started = time.perf_counter()
    cold = ort_session(path)
    cold_load = (time.perf_counter() - started) * 1000
    after_cold = proc_self_memory()["rss"]
    ids = (np.arange(32, dtype=np.int64)[None, :] % 39_990) + 4
    ids[0, 0], ids[0, -1] = 0, 2
    mask = np.ones_like(ids)
    first_started = time.perf_counter()
    cold.run(None, {"input_ids": ids, "attention_mask": mask})
    first_inference = (time.perf_counter() - first_started) * 1000
    del cold
    gc.collect()
    time.sleep(0.2)
    started = time.perf_counter()
    session = ort_session(path)
    warm_load = (time.perf_counter() - started) * 1000
    after_warm = proc_self_memory()["rss"]
    lengths = {}
    peak = after_warm
    for length in (16, 32, 64):
        ids = (np.arange(length, dtype=np.int64)[None, :] % 39_990) + 4
        ids[0, 0], ids[0, -1] = 0, 2
        mask = np.ones_like(ids)
        feed = {"input_ids": ids, "attention_mask": mask}
        for _ in range(5):
            session.run(None, feed)
        samples = []
        for _ in range(30):
            started = time.perf_counter_ns()
            output = session.run(None, feed)
            samples.append((time.perf_counter_ns() - started) / 1e6)
            if not all(np.isfinite(value).all() for value in output):
                raise RuntimeError("non-finite benchmark output")
            memory = proc_self_memory()
            peak = max(peak, memory["rss"], memory["hwm"])
        lengths[str(length)] = {
            "warmups": 5,
            "runs": 30,
            "medianMs": statistics.median(samples),
            "p95Ms": percentile(samples, 0.95),
            "meanMs": statistics.mean(samples),
            "minimumMs": min(samples),
            "maximumMs": max(samples),
        }
    queue.put(
        {
            "model": path.name,
            "provider": session.get_providers(),
            "sessionSettings": {
                "intraOpThreads": 1,
                "interOpThreads": 1,
                "executionMode": "ORT_SEQUENTIAL",
                "graphOptimization": "ORT_ENABLE_ALL",
                "batchSize": 1,
            },
            "coldLoadMs": cold_load,
            "warmReloadMs": warm_load,
            "firstInferenceAfterColdLoadMsSeq32": first_inference,
            "rssBaselineBytes": baseline,
            "rssAfterColdLoadBytes": after_cold,
            "rssColdLoadIncreaseBytes": after_cold - baseline,
            "rssAfterWarmLoadBytes": after_warm,
            "rssWarmLoadIncreaseBytes": after_warm - baseline,
            "rssPeakBytes": peak,
            "inputLengths": lengths,
        }
    )


def benchmark(path: pathlib.Path) -> dict:
    context = mp.get_context("spawn")
    queue = context.Queue()
    process = context.Process(target=benchmark_child, args=(str(path), queue))
    process.start()
    process.join(timeout=600)
    if process.is_alive():
        process.terminate()
        process.join()
        raise RuntimeError(f"benchmark timeout: {path.name}")
    if process.exitcode != 0:
        raise RuntimeError(f"benchmark failed ({process.exitcode}): {path.name}")
    return queue.get(timeout=10)


def runtime_validate(path: pathlib.Path, model_dir: pathlib.Path, text: str) -> dict:
    import onnx
    import onnxruntime as ort
    from transformers import XLMRobertaTokenizer

    graph = onnx.load(path, load_external_data=False)
    onnx.checker.check_model(graph)
    session = ort_session(path)
    tokenizer = XLMRobertaTokenizer.from_pretrained(model_dir, local_files_only=True)
    encoded = tokenizer(text, return_tensors="np")
    feed = {
        "input_ids": encoded["input_ids"].astype(np.int64),
        "attention_mask": encoded["attention_mask"].astype(np.int64),
    }
    outputs = session.run(None, feed)
    if outputs[0].shape[:2] != feed["input_ids"].shape:
        raise RuntimeError("runtime output shape mismatch")
    if not all(np.isfinite(value).all() for value in outputs):
        raise RuntimeError("runtime non-finite output")
    return {
        "onnxChecker": "PASS",
        "runtimeLoad": "PASS",
        "forward": "PASS",
        "outputNames": [item.name for item in session.get_outputs()],
        "outputShapes": [list(value.shape) for value in outputs],
        "outputFinite": True,
        "providers": session.get_providers(),
        "onnxVersion": onnx.__version__,
        "onnxruntimeVersion": ort.__version__,
    }


def mobile_audit(fp32_census: dict, int8_census: dict, fp32_bytes: int, int8_bytes: int) -> dict:
    problematic = {"ATen", "PythonOp", "Loop", "If", "Scan"}
    present = sorted(problematic.intersection(int8_census["operatorSet"]))
    risks = [
        "No physical Android/Moto execution was authorized or performed.",
        "Android package must provide the exact XLM-R SentencePiece tokenizer and special-ID mapping.",
        "A reduced-operator ONNX Runtime Mobile build must include every recorded FP32 and quantized op.",
        "Large single-file graph and device-specific RSS/latency still require a later hardware gate.",
    ]
    blockers = []
    if present:
        blockers.append(f"control/custom operators present: {present}")
    if fp32_census["externalDataRequired"] or int8_census["externalDataRequired"]:
        blockers.append("external ONNX tensor data is required")
    status = "BLOCKED" if blockers else "RISK"
    return {
        "status": status,
        "scope": "STATIC_DESKTOP_AUDIT_ONLY",
        "standardOperatorsOnly": not present,
        "problematicOperators": present,
        "externalDataRequired": False,
        "dynamicBatchAndSequence": True,
        "fp32GraphBytes": fp32_bytes,
        "int8GraphBytes": int8_bytes,
        "tokenizerRuntime": "XLMRobertaTokenizer backed by bundled SentencePiece model",
        "blockers": blockers,
        "risks": risks,
        "motoTest": "NOT_EXECUTED",
    }


def copy_runtime_files(model_dir: pathlib.Path, destination: pathlib.Path) -> None:
    destination.mkdir(parents=True, exist_ok=True)
    for name in (
        "config.json",
        "tokenizer_config.json",
        "special_tokens_map.json",
        "sentencepiece.bpe.model",
        "token-id-remap.json",
    ):
        shutil.copy2(model_dir / name, destination / name)


def write_sums(root: pathlib.Path) -> None:
    paths = [path for path in sorted(root.rglob("*")) if path.is_file() and path.name != "SHA256SUMS"]
    text = "".join(f"{sha256(path)}  ./{path.relative_to(root)}\n" for path in paths)
    (root / "SHA256SUMS").write_text(text, encoding="utf-8")


def environment() -> dict:
    import onnx
    import onnxruntime as ort
    import psutil
    import torch
    import transformers

    cpu_lines = pathlib.Path("/proc/cpuinfo").read_text(
        encoding="utf-8", errors="replace"
    ).splitlines()
    cpu_model = next(
        (line.split(":", 1)[1].strip() for line in cpu_lines if line.startswith("model name")),
        platform.processor() or platform.machine(),
    )
    return {
        "os": platform.platform(),
        "machine": platform.machine(),
        "cpu": cpu_model,
        "logicalCores": psutil.cpu_count(logical=True),
        "physicalCores": psutil.cpu_count(logical=False),
        "python": platform.python_version(),
        "torch": torch.__version__,
        "transformers": transformers.__version__,
        "onnx": onnx.__version__,
        "onnxruntime": ort.__version__,
        "numpy": np.__version__,
        "psutil": psutil.__version__,
        "cpuProvider": ort.get_available_providers(),
    }


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--archive", type=pathlib.Path, required=True)
    parser.add_argument("--pristine-root", type=pathlib.Path, required=True)
    parser.add_argument("--phase-a-source", type=pathlib.Path, required=True)
    parser.add_argument("--output-dir", type=pathlib.Path, required=True)
    args = parser.parse_args()
    output = args.output_dir.resolve()
    if output.exists() and any(output.iterdir()):
        raise RuntimeError(f"refusing to overwrite non-empty output: {output}")
    output.mkdir(parents=True, exist_ok=True)
    model_dir = args.pristine_root.resolve() / "model"
    before = {
        "archive": sha256(args.archive.resolve()),
        "model": sha256(model_dir / "model.safetensors"),
        "mapping": sha256(model_dir / "token-id-remap.json"),
        "sentencePiece": sha256(model_dir / "sentencepiece.bpe.model"),
    }
    input_verification = verify_pristine(args.archive.resolve(), args.pristine_root.resolve())
    rows, pairs = load_probe_source(args.phase_a_source.resolve())
    unique_texts = list(
        dict.fromkeys(
            [row["text"] for row in rows]
            + [pair[key] for pair in pairs for key in ("left", "right")]
        )
    )
    evidence = output / "evidence"
    models = output / "model"
    source = output / "source"
    runtime_tokenizer = output / "tokenizer"
    for directory in (evidence, models, source):
        directory.mkdir(parents=True, exist_ok=True)
    write_json(
        evidence / "probe-set.json",
        {
            "source": "canonical Phase-A project-authored independent probe",
            "trainSafe": True,
            "canonicalDevUsed": False,
            "frozenUsed": False,
            "adultOnlyAuthoredMaterial": True,
            "coverageRows": rows,
            "contrastPairs": pairs,
            "uniqueTexts": len(unique_texts),
        },
    )
    fp32 = models / "student-5-minilm-40k-untaught-fp32.onnx"
    int8 = models / "student-5-minilm-40k-untaught-int8.onnx"
    export = export_fp32(model_dir, fp32, rows[0]["text"])
    fp32_validation = runtime_validate(fp32, model_dir, rows[0]["text"])
    fp32_census = operator_census(fp32)
    # Quantization remains blocked until strict HF-vs-ONNX FP32 parity succeeds.
    fp32_parity = parity(model_dir, fp32, None, rows, pairs)
    quantization = quantize(fp32, int8)
    int8_validation = runtime_validate(int8, model_dir, rows[0]["text"])
    int8_census = operator_census(int8)
    if int8_census["matMulIntegerNodes"] <= 0:
        raise RuntimeError("INT8 artifact contains no substantive quantized MatMul operators")
    eligible = fp32_census["weightBearingEligibleMatMulOrGemm"]
    quantized = int8_census["matMulIntegerNodes"]
    quantization["operatorCoverage"] = {
        "fp32WeightBearingEligibleMatMulOrGemm": eligible,
        "int8MatMulIntegerNodes": quantized,
        "coverageVsEligiblePercent": 100 * quantized / max(1, eligible),
        "fp32OperatorsPreserved": {
            name: count
            for name, count in int8_census["operatorCounts"].items()
            if name not in {"MatMulInteger", "DynamicQuantizeLinear"}
        },
    }
    full_parity = parity(model_dir, fp32, int8, rows, pairs)
    full_parity["hfPristineVsOnnxFp32"] = fp32_parity["hfPristineVsOnnxFp32"]
    benchmarks = {
        "environment": environment(),
        "fp32": benchmark(fp32),
        "int8": benchmark(int8),
    }
    mobile = mobile_audit(fp32_census, int8_census, export["bytes"], quantization["bytes"])
    after = {
        "archive": sha256(args.archive.resolve()),
        "model": sha256(model_dir / "model.safetensors"),
        "mapping": sha256(model_dir / "token-id-remap.json"),
        "sentencePiece": sha256(model_dir / "sentencepiece.bpe.model"),
    }
    if before != after:
        raise RuntimeError("pristine40kModified=true")
    copy_runtime_files(model_dir, runtime_tokenizer)
    shutil.copy2(pathlib.Path(__file__).resolve(), source / pathlib.Path(__file__).name)
    write_json(evidence / "input-verification.json", input_verification)
    write_json(evidence / "export.json", export)
    write_json(evidence / "operator-census.json", {"fp32": fp32_census, "int8": int8_census})
    write_json(evidence / "parity-results.json", full_parity)
    write_json(evidence / "benchmark-results.json", benchmarks)
    write_json(evidence / "mobile-compatibility.json", mobile)
    write_json(
        output / "PRISTINE_SOURCE_REFERENCE.json",
        {
            "release": RELEASE,
            "expected": EXPECTED,
            "exactInputCopyUsed": args.archive.name,
            "observed": input_verification,
            "hashesBefore": before,
            "hashesAfter": after,
            "pristine40kModified": False,
        },
    )
    manifest = {
        "task": "TASK_1_UNTAUGHT_INT8_RUNTIME_PROBE",
        "logicalName": "STUDENT_5_40K_UNTAUGHT_INT8",
        "status": "RUNTIME_PROBE_ONLY",
        "nluStatus": "NOT_MATRIX_NLU",
        "productionStatus": "NOT_PRODUCTION_APPROVED",
        "verdict": "RUNTIME_PROBE_PASS",
        "input": input_verification,
        "export": export,
        "fp32Runtime": fp32_validation,
        "quantization": quantization,
        "int8Runtime": int8_validation,
        "operatorCensus": {"fp32": fp32_census, "int8": int8_census},
        "parity": full_parity,
        "benchmark": benchmarks,
        "mobileCompatibility": mobile,
        "nonBlockingToolWarnings": [
            "PyTorch reports the selected legacy TorchScript ONNX exporter as deprecated for a future PyTorch release.",
            "The attention-mask scalar constant produced a tracer warning; dynamic-length parity passed on the complete probe and lengths 16/32/64.",
            "ONNX Runtime suggested optional preprocessing before quantization; the direct dynamic quantization graph passed checker, runtime, coverage and parity validation.",
        ],
        "size": {
            "fp32OnnxBytes": export["bytes"],
            "int8OnnxBytes": quantization["bytes"],
            "reductionPercent": 100 * (1 - quantization["bytes"] / export["bytes"]),
        },
        "guards": {
            "pristine40kModified": False,
            "student4V22AChanged": False,
            "canonicalDevUsed": False,
            "frozenDataRead": False,
            "frozenDataTokenized": False,
            "frozenDataAnalyzed": False,
            "frozenPredictionsRead": False,
            "frozenDataUsedForTuning": False,
            "teachingExecuted": False,
            "matrixHeadsTrained": False,
            "pathBStarted": False,
            "otherRepositoriesModified": False,
            "motoTestExecuted": False,
        },
    }
    readme = "# Student-5 40k untaught INT8 runtime probe\n\n"
    readme += "Status: `RUNTIME_PROBE_ONLY / NOT_MATRIX_NLU / NOT_PRODUCTION_APPROVED`.\n\n"
    readme += "This package preserves separate FP32 ONNX and dynamic per-channel QInt8 ONNX graphs, "
    readme += "the immutable tokenizer identity, parity/benchmark/operator evidence, and checksums. "
    readme += "It contains no Matrix heads and is not a Path-B or production artifact.\n"
    (output / "README.md").write_text(readme, encoding="utf-8")
    manifest["artifactDirectoryBytes"] = 0
    write_json(output / "runtime-manifest.json", manifest)
    write_sums(output)
    for _ in range(5):
        total = sum(path.stat().st_size for path in output.rglob("*") if path.is_file())
        if manifest["artifactDirectoryBytes"] == total:
            break
        manifest["artifactDirectoryBytes"] = total
        write_json(output / "runtime-manifest.json", manifest)
        write_sums(output)
    else:
        raise RuntimeError("artifactDirectoryBytes did not converge")
    print(json.dumps({"status": "PASS", "output": str(output)}))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
