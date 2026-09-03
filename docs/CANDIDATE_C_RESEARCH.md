# Gate 06 — Candidate C: compact ONNX NLU research

Date of research: 2026-09-03  
Status: **CANDIDATE_C_NOT_READY**  
Production status: **REJECT (P0); no integration authorized**

## Decision in one sentence

ONNX Runtime is a mature, offline-capable Android execution substrate, but no
small, reproducible, provenance-complete IT/EN/ES model was found that already
emits the frozen Matrix claim contract; the available multilingual encoders do
not solve the task, and the frozen P0 training data (39 train+dev variants) is
insufficient to train and validate a joint model without leaking the test set.

This is a negative research result, not an implementation failure. Gate 07 is
therefore skipped as required by the work prompt rather than filled with a
heuristic presented as an ONNX candidate.

## Required capability

Candidate C would have to produce, for every independent claim, claim boundary
and source span plus speaker, subject, target, owner, perspective, dialogue act,
predicate/object, polarity, negation scope, temporal validity, entity type/link,
and explicit/hypothesis/unknown. It must preserve Observation/Belief boundaries
and must never promote an inferred fact to World Truth.

A sentence embedding, intent label, POS sequence, or generic NER result is not
equivalent to that contract. A valid C therefore needs a Matrix-specific joint
head (or an explicitly specified set of heads) and a deterministic mapper with
documented uncertainty behavior.

## BUILD / REUSE / ADAPT assessment

| Option | Evidence | Matrix gap | Decision |
|---|---|---|---|
| ONNX Runtime Mobile | Android Java package, CPU default, XNNPACK and NNAPI available; model and runtime must fit device memory | Execution substrate only; it provides no NLU semantics | `REUSE_LATER`, not a candidate by itself |
| `paraphrase-multilingual-MiniLM-L12-v2` | Apache-2.0 card; IT/EN/ES among 50 languages; 384-dimensional sentence embeddings; arm64 INT8 ONNX is 118 MB | Embeddings for similarity/search, not claim segmentation, spans, negation, ownership, temporal validity, or Matrix predicates | `REJECT_FOR_C` |
| `distilbert-base-multilingual-cased` | Apache-2.0; 104 languages; 134M parameters, 6 layers, 768 hidden; intended for downstream fine-tuning | Masked-LM encoder, not a trained Matrix joint model; not compact for the stated mobile budget without an unproven training/export/quantization project | `REJECT_FOR_P0` |
| MASSIVE + XLM-R/mT5 joint intent/slot code | >1M utterances, 52 languages, 60 intents and 55 slots; official code trains XLM-R Base or mT5 | Voice-assistant intent/slot ontology does not contain Matrix owner/perspective, provenance, World Truth safety, negation scope, temporal validity or open predicates; base encoders are not the compact deployable model requested | `ADAPT_REQUIRES_NEW_PROJECT` |
| Train a new compact joint model on P0 gold | Exact target schema available | Only 21 train + 18 dev language variants; test is locked and cannot be used for tuning. This cannot support a credible trilingual learned candidate | `NOT_READY` |

## Runtime, Android and offline feasibility

ONNX Runtime v1.29.0 is the current tagged release inspected (2026-08-12) and
the runtime itself is MIT licensed. The official mobile guide provides Android
Java/C/C++ packages, CPU execution by default, and optional XNNPACK/NNAPI. It
explicitly requires measuring binary size, model size, latency and power on the
target device. Quantization can reduce FP32 weights by roughly four times, and
a model-derived reduced-operator/custom build can shrink the runtime.

This makes offline Android execution technically feasible **after** a suitable
model exists. It does not make an unsuitable encoder a Matrix Understanding
model. Hardware acceleration is also not a portable assumption: the official
guide warns that NNAPI performance is model/device specific and partitioning
can make it worse; recent Android/QNN reports include complete silent fallback
to CPU on Snapdragon hardware. A future probe must confirm the execution
provider from profiling rather than infer it from successful session creation.

## Footprint evidence and budget risk

| Component/model | Published evidence | Consequence |
|---|---:|---|
| ONNX Runtime prebuilt AAR example (v1.18) | 24,415,212 bytes | Runtime overhead exists before model/tokenizer |
| ONNX Runtime custom AAR example (ResNet operator set) | 7,532,309 bytes | Reduced-op builds can help, but are model-specific engineering |
| Multilingual MiniLM arm64 INT8 ONNX | 118 MB | Already exceeds the initial ONNX model/PSS comfort implied by the 80 MB delta-PSS budget; tokenizer and activations are extra |
| Multilingual MiniLM FP32 ONNX | 470 MB | Not a compact phone candidate |
| DistilmBERT | 134M parameters | Quantized weights alone are roughly 134 MB before tokenizer/runtime/activations; also lacks a Matrix head |

The file sizes are not PSS measurements and must not be reported as such. No
Candidate-C RAM, CPU, latency, APK or thermal number is fabricated because no
valid model was selected or packaged.

## Provenance and licenses

| Asset | License/provenance evidence | P0 conclusion |
|---|---|---|
| ONNX Runtime | Microsoft repository, MIT license | Clear for runtime evaluation |
| Multilingual MiniLM | Hugging Face model card/API: Apache-2.0; Sentence-Transformers; 50 languages; exported ONNX files | License declaration is usable, but task mismatch is decisive; downstream training corpus provenance would need a product review before adoption |
| DistilmBERT multilingual | Model card: Apache-2.0; distilled multilingual BERT trained on concatenated Wikipedia in 104 languages | Usable base-model declaration, but no Matrix task head or Matrix task data |
| MASSIVE | Amazon/Alexa repository and paper; localized from SLURP; repository points to LICENSE/NOTICE/THIRD-PARTY records | Potentially useful source corpus, not a substitute for Matrix annotations; all third-party terms must travel with any derived training pipeline |
| Frozen P0 gold | Locally authored Matrix-specific benchmark, locked split | Benchmark evidence only; too small to establish a learned model |

No external model or dataset has been copied into this repository.

## Reproducibility boundary

There is no candidate artifact hash because no valid candidate artifact exists.
A future Gate 06 may be reopened only with all of the following pinned:

1. model architecture and exact upstream revision/hash;
2. tokenizer and preprocessing revisions;
3. task heads and label mapping for every frozen Matrix field;
4. training datasets, licenses, provenance, and immutable split manifests;
5. export and quantization commands plus parity tolerances;
6. ONNX Runtime version, operator set, Android ABI and execution-provider policy;
7. evaluation on the untouched P0 test set and a substantially larger external
   adversarial set;
8. actual Moto G56 cold/warm PSS, CPU, p50/p95, APK/model bytes and thermal loop.

## Recent maintenance and failure signals

- ONNX Runtime v1.29.0 is actively maintained and includes Android-related
  telemetry and security work; this supports runtime maturity.
- ONNX Runtime issue #31353 (opened 2026-08-01) reports QNN HTP session creation
  that appears successful while profiling shows every node on CPU. This is a
  relevant measurement hazard, not proof that all QNN deployments fail.
- Issues #28899 and #28784 document the device/provider-specific nature of
  Android acceleration and the risk of CPU fallback. The baseline plan must
  therefore start on CPU and treat an accelerator as a measured optimization.

## Sources (primary)

- ONNX Runtime mobile development guide: https://onnxruntime.ai/docs/tutorials/mobile/
- ONNX Runtime custom builds: https://onnxruntime.ai/docs/build/custom.html
- ONNX Runtime quantization: https://onnxruntime.ai/docs/performance/model-optimizations/quantization.html
- ONNX Runtime NNAPI provider: https://onnxruntime.ai/docs/execution-providers/NNAPI-ExecutionProvider.html
- ONNX Runtime v1.29.0 release: https://github.com/microsoft/onnxruntime/releases/tag/v1.29.0
- ONNX Runtime MIT license: https://github.com/microsoft/onnxruntime/blob/main/LICENSE
- ONNX Runtime Android/QNN issue #31353: https://github.com/microsoft/onnxruntime/issues/31353
- ONNX Runtime Android acceleration issue #28784: https://github.com/microsoft/onnxruntime/issues/28784
- ONNX Runtime Qualcomm issue #28899: https://github.com/microsoft/onnxruntime/issues/28899
- Multilingual MiniLM model card and files: https://huggingface.co/sentence-transformers/paraphrase-multilingual-MiniLM-L12-v2
- DistilmBERT multilingual model card: https://huggingface.co/distilbert/distilbert-base-multilingual-cased
- MASSIVE official repository: https://github.com/alexa/massive

## Gate 06 / Gate 07 disposition

- Gate 06: **PASS as a bounded negative result**.
- Candidate C: **CANDIDATE_C_NOT_READY**.
- Gate 07: **SKIPPED_BY_SPEC**; no fake implementation, no model import, no test
  tuning, no cloud dependency.
- Production: **NO CHANGE / NO AUTHORIZATION**.

