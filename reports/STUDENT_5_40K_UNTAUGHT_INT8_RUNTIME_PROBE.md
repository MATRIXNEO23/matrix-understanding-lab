# Student-5 40k untaught ONNX/INT8 runtime probe

Date: `2026-09-05`  
Repository: `MATRIXNEO23/matrix-understanding-lab`  
Branch: `main`  
Task: `TASK_1_UNTAUGHT_INT8_RUNTIME_PROBE`  
Verdict: `RUNTIME_PROBE_PASS`

## Scope and status

```text
logicalName = STUDENT_5_40K_UNTAUGHT_INT8
path = PATH_A_RUNTIME_DEPLOYMENT_PROBE
status = RUNTIME_PROBE_ONLY
nluStatus = NOT_MATRIX_NLU
productionStatus = NOT_PRODUCTION_APPROVED
TASK_2 = NOT_STARTED
PATH_B = NOT_STARTED
FROZEN = UNREAD
```

This task measures deployment behavior of the pristine representation-preserving backbone. It does not add or train the 15 Matrix semantic heads and it does not measure Matrix-NLU quality.

## Input identity

The only model input was the canonical TASK-0 Release asset.

- Pristine release: [Student-5 MiniLM 40k Phase-A Pristine](https://github.com/MATRIXNEO23/matrix-understanding-lab/releases/tag/student-5-minilm-40k-phase-a-pristine)
- Release ID: `383143636`
- Asset ID: `545406840`
- Asset: `student5-minilm-phase-a-pruned-40k.zip`
- Archive bytes: `88361246`
- Archive SHA-256: `7804bfb245b71df9b835fff7ee00f6ec887e019772ae34c82d269d821d587191`
- Model bytes: `148020400`
- Model SHA-256: `d6e45891d1e0ec4ed023caaeb17c0dd0ae80a93b8bf877d275310b7f2837efa2`
- Token-ID mapping SHA-256: `da36a5e1a9057391da935354d895edb3bc3a959744aca6b6602e511f9d4ea9b9`
- SentencePiece SHA-256: `748f8053688469d7dc98c135a28a3fc0713bdbb82853f86f8d7a254bada46f78`
- Candidate manifest SHA-256: `a9d23de7816d487986316351c163f37a67d65d001861dbf042b9114c455f066d`

Verification before export:

```text
archiveIntegrity = PASS
internalSha256Sums = 17/17 PASS
vocabSize = 40000
layers = 12
hiddenSize = 384
embeddingShape = [40000, 384]
specialTokenIds = bos:0 pad:1 eos:2 unk:3 mask:39999
huggingFaceSaveReload = PASS
realForward = PASS
pristine40kModified = false
```

Input hashes were recomputed again after all exports and remained identical.

## FP32 ONNX export

| Field | Value |
|---|---|
| Export API | `torch.onnx.export`, legacy TorchScript path |
| PyTorch | `2.8.0+cu128` |
| Transformers | `4.56.0` |
| ONNX | `1.18.0` |
| ONNX Runtime | `1.22.1` |
| Opset | `ai.onnx:17` |
| Inputs | `input_ids`, `attention_mask` |
| Outputs | `last_hidden_state`, `pooler_output` |
| Dynamic axes | batch and sequence for inputs/outputs |
| External tensor data | not required |
| FP32 ONNX bytes | `148202898` |
| FP32 ONNX SHA-256 | `799d86b9231721c0e7ff656b48cb609611c98ea75c8489e4edebeaf7e9d7de23` |

Validation:

```text
onnxChecker = PASS
onnxRuntimeLoad = PASS
forward = PASS
outputShapes = [1,10,384], [1,384]
allOutputsFinite = true
CPUExecutionProvider = PASS
```

Quantization was not started until strict HF-pristine versus ONNX-FP32 parity passed.

## Quantization method and operator census

Method: ONNX Runtime dynamic, per-channel signed QInt8 weight quantization for weight-bearing `MatMul`/`Gemm`; activations are dynamically quantized to UINT8. This method requires no calibration corpus, so neither canonical DEV nor Frozen was used.

Preservation policy:

- word/position/token-type embeddings remain FP32;
- LayerNormalization and one-dimensional parameters remain FP32;
- softmax, elementwise, reshape, gather and attention score/context MatMul operations without constant weights remain FP32;
- no Matrix heads exist and none were added.

| Census | FP32 graph | INT8 graph |
|---|---:|---:|
| Total nodes | 1043 | 1312 |
| MatMul | 96 | 24 |
| Gemm | 1 | 0 |
| Weight-bearing eligible MatMul/Gemm | 73 | — |
| MatMulInteger | 0 | 73 |
| DynamicQuantizeLinear | 0 | 49 |
| LayerNormalization | 25 | 25 |
| Gather | 32 | 32 |
| INT8 initializer tensors | 0 | 146 |
| INT8 initializer bytes | 0 | 21422976 |
| FP32 initializer tensors | 328 | 182 |
| FP32 initializer bytes | 148000512 | 62615040 |

```text
quantizedWeightBearingOperators = 73/73
coverageVsEligible = 100.0%
remainingFp32MatMul = 24
remainingFp32MatMulReason = dynamic attention score/context operands, not constant weights
calibrationDataUsed = false
```

The resulting graph contains substantial INT8 computation and is not merely labeled INT8.

INT8 output:

- bytes: `84457299`
- SHA-256: `f58463a6d1f4daca2e58c8e40f7f6d1cbaa7d107e9534160278bc46552e0304a`
- ONNX checker: PASS
- ONNX Runtime load: PASS
- real forward: PASS
- output shapes: `[1,10,384]`, `[1,384]`
- finite outputs: true

## Parity probe

The exact independent Phase-A probe was reused: 95 coverage rows, 161 unique semantic-comparison sentences and 36 contrast pairs. It includes general language, IT/EN/ES, code-switch and 50 adult/intimacy sentences. Exact canonical DEV and Frozen were not used.

### HF pristine FP32 versus ONNX FP32

The technical export sanity check passed (`minimum representation cosine >= 0.999999`, `maximum absolute delta <= 1e-4`). These are export-equivalence sanity limits, not Matrix quality gates.

| Slice | Sentences | Mean cosine | Minimum cosine | Mean absolute delta | Maximum absolute delta |
|---|---:|---:|---:|---:|---:|
| Overall | 95 | 0.9999999893 | 0.9999998808 | 1.048e-7 | 2.861e-6 |
| General | 45 | 0.9999999921 | 0.9999998808 | 1.026e-7 | 2.384e-6 |
| IT | 29 | 0.9999999918 | 0.9999998808 | 1.050e-7 | 2.861e-6 |
| EN | 29 | 1.0000000000 | 0.9999998808 | 1.033e-7 | 2.861e-6 |
| ES | 29 | 0.9999999733 | 0.9999998808 | 1.049e-7 | 2.861e-6 |
| Adult/intimacy | 50 | 0.9999999869 | 0.9999998808 | 1.069e-7 | 2.861e-6 |
| Code-switch | 8 | 1.0000000000 | 0.9999999404 | 1.095e-7 | 1.907e-6 |

Contrast cosine delta: mean `6.457e-8`, p95 `1.192e-7`, maximum `1.788e-7`. Spanish adult consent-withdrawal delta: `0.0`.

### ONNX FP32 versus ONNX INT8

No pre-existing canonical INT8 linguistic gate exists, so measurements are reported without inventing or lowering one.

| Slice | Sentences | Mean cosine | Minimum cosine | Mean absolute delta | Maximum absolute delta |
|---|---:|---:|---:|---:|---:|
| Overall | 95 | 0.9985922280 | 0.9974925518 | 0.014247 | 0.266195 |
| General | 45 | 0.9985940893 | 0.9975170493 | 0.013934 | 0.162763 |
| IT | 29 | 0.9985519545 | 0.9975170493 | 0.014392 | 0.135092 |
| EN | 29 | 0.9986616887 | 0.9977059364 | 0.013764 | 0.259234 |
| ES | 29 | 0.9986688186 | 0.9980143309 | 0.014283 | 0.180346 |
| Adult/intimacy | 50 | 0.9985905528 | 0.9974925518 | 0.014529 | 0.266195 |
| Adult IT | 14 | 0.9986285525 | 0.9980231524 | 0.014514 | 0.135092 |
| Adult EN | 14 | 0.9986575033 | 0.9977059364 | 0.014109 | 0.259234 |
| Adult ES | 14 | 0.9987037565 | 0.9983276129 | 0.014502 | 0.180346 |
| Code-switch | 8 | 0.9982087836 | 0.9974925518 | 0.015339 | 0.266195 |

Contrast cosine delta: mean `0.0025965770`, p95 `0.0056632161`, maximum `0.0084947348`. The maximum is Italian adult consent withdrawal, not the Spanish case.

Spanish adult consent withdrawal:

```text
FP32 pair cosine = 0.8060526848
INT8 pair cosine = 0.8042662144
absolute delta = 0.0017864704
```

Adult/intimacy mean representation cosine is effectively equal to general (`0.9985906` versus `0.9985941`); no disproportionate adult-domain degradation is observed. Relative-error ratios in the JSON are large around reference values close to zero, so representation cosine and absolute deltas are the stable interpretation.

## Technical benchmark

Environment:

```text
OS = Linux 6.18.35 x86_64, glibc 2.39
CPU = AMD EPYC 9V74 80-Core Processor
visible physical/logical cores = 9/9
Python = 3.12.13
ONNX Runtime = 1.22.1
provider = CPUExecutionProvider
intra-op threads = 1
inter-op threads = 1
execution = ORT_SEQUENTIAL
graph optimization = ORT_ENABLE_ALL
batch = 1
warmups per length = 5
measured runs per length = 30
```

FP32 and INT8 were benchmarked in separate fresh worker processes with identical settings.

| Model | Cold load | Warm reload | First inference seq32 | RSS increase after warm load | Peak RSS |
|---|---:|---:|---:|---:|---:|
| FP32 | 841.747 ms | 339.759 ms | 18.500 ms | 256581632 B | 351080448 B |
| INT8 | 309.258 ms | 177.313 ms | 7.517 ms | 128000000 B | 210198528 B |

Warm inference latency:

| Length | FP32 median | FP32 p95 | INT8 median | INT8 p95 |
|---:|---:|---:|---:|---:|
| 16 | 9.747 ms | 10.958 ms | 3.842 ms | 4.400 ms |
| 32 | 16.961 ms | 18.479 ms | 6.240 ms | 7.725 ms |
| 64 | 31.527 ms | 36.670 ms | 12.364 ms | 13.547 ms |

These values are desktop/container measurements, not Moto or Android results.

## Size

| Artifact | Bytes | SHA-256 |
|---|---:|---|
| FP32 ONNX | 148202898 | `799d86b9231721c0e7ff656b48cb609611c98ea75c8489e4edebeaf7e9d7de23` |
| INT8 ONNX | 84457299 | `f58463a6d1f4daca2e58c8e40f7f6d1cbaa7d107e9534160278bc46552e0304a` |
| Runtime artifact directory | 234933515 | internal `SHA256SUMS` covers 18 files |
| Published ZIP | 142463548 | `72eea0af4211959bdbc92be36387faf5b85da957830f9be0a6d0dd50ab7cedf6` |

INT8 graph reduction versus FP32 ONNX: `43.012384%`.

The measured INT8 graph is 602451 bytes above the Phase-A parameter-only estimate of 83854848 bytes. The difference comes from ONNX graph structure, quantization scales/zero-points and serialization metadata; the architecture, tokenizer and embeddings were not altered to chase the estimate.

## Mobile compatibility audit

```text
MOBILE_COMPATIBILITY_PROVISIONAL = RISK
standardOperatorsOnly = true
problematicCustomOrControlOperators = none
externalDataRequired = false
dynamicBatchAndSequence = true
MotoTest = NOT_EXECUTED
```

No static blocker was found. Remaining risks are the exact XLM-R SentencePiece integration, inclusion of the recorded operator set in a reduced ONNX Runtime Mobile build, the 84.5 MB graph, and device-specific latency/RSS. A later hardware task is required; no Android or Assembling modification occurred here.

## Artifact and integrity

- Runtime release: [Student-5 40k Untaught INT8 Runtime Probe](https://github.com/MATRIXNEO23/matrix-understanding-lab/releases/tag/student-5-minilm-40k-untaught-int8-runtime-probe)
- Release ID: `383162517`
- Asset ID: `545486429`
- Download: [student-5-minilm-40k-untaught-int8-runtime-probe.zip](https://github.com/MATRIXNEO23/matrix-understanding-lab/releases/download/student-5-minilm-40k-untaught-int8-runtime-probe/student-5-minilm-40k-untaught-int8-runtime-probe.zip)
- GitHub-recorded asset digest: `sha256:72eea0af4211959bdbc92be36387faf5b85da957830f9be0a6d0dd50ab7cedf6`
- ZIP integrity: PASS
- Extracted internal `SHA256SUMS`: 18/18 PASS
- Reproduction source: `matrix_nlu/student5_untaught_runtime_probe.py`

Non-blocking tool warnings are preserved in `runtime-manifest.json`: legacy-exporter deprecation, a constant attention-mask scalar tracer warning, and ONNX Runtime's general preprocessing suggestion. Dynamic lengths 16/32/64, full probe parity, checker and runtime execution all pass.

## Guards

```text
pristine40kModified = false
student4V22AChanged = false
canonicalDevUsed = false
frozenDataRead = false
frozenDataTokenized = false
frozenDataAnalyzed = false
frozenPredictionsRead = false
frozenDataUsedForTuning = false
teachingExecuted = false
matrixHeadsTrained = false
pathBStarted = false
otherRepositoriesModified = false
productionPromotionExecuted = false
```

## Verdict

```text
TASK_1 = RUNTIME_PROBE_PASS
TASK_2 = NOT_STARTED
TASK_3 = NOT_STARTED
PATH_B = NOT_STARTED
FROZEN = UNREAD
NEXT = AWAIT OWNER REVIEW BEFORE TASK 2
```

This is a successful runtime/deployment probe only. It is not evidence that Student-5 is a Matrix NLU and it does not authorize production use or automatic continuation.
