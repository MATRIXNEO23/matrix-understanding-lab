# Student-4-v2.2A — NLU Quality Analysis Dossier

Date: 2026-09-05  
Repository: `MATRIXNEO23/matrix-understanding-lab`  
Purpose: canonical, analysis-ready consolidation of Student-4-v2.2A development evidence and the later Mixed / Head-Protected INT8 export.  
Evidence scope: development-only plus post-run FP32/INT8 parity probes. Frozen data and predictions were not read.

## 1. Decision and interpretation boundary

Canonical development decision:

```text
selectionStatus = FAILED_GATE
selectedThreshold = null
controlledDecision = STOPPED_FOR_REVIEW
canonicalDevGatePassed = false
```

Authorized runtime disposition:

```text
acceptanceTier = R2
OWNER_APPROVED_CONTROLLED_RUNTIME_CANDIDATE
EXPERIMENTAL_TEST_CANDIDATE_NOT_PRODUCTION_APPROVED
FAILED_CANONICAL_DEV_GATE_CARRY_OVER_ALLOWED
FAILED_DEV_GATE_CARRY_OVER
FROZEN_UNREAD
NOT_TECHNICALLY_PRODUCTION_VALIDATED
productionApproved = false
```

This dossier does not reinterpret the failed gate as a pass. The model may be used only as a controlled NLU proposal source behind semantic consistency, Authority and Memory Admission boundaries.

## 2. Immutable provenance

### Training

- Authoritative workflow run: [33860928806](https://github.com/MATRIXNEO23/matrix-understanding-lab/actions/runs/33860928806)
- Run HEAD: `617aeca8a6abac4366eb13347fb88026307dc3b8`
- Job: `100984948899`
- Workflow conclusion: `success`
- Variant: `student-4-v2.2a`
- Encoder layers: 4
- Total/trainable parameters: 58,599,411
- Encoder parameters: 58,412,544
- Head parameters: 186,867
- Model-state SHA-256: `446b6a58265500001efd350f81d75867227cbfd3c6da699ed9c9330257d16a9c`
- Training-result SHA-256: `ddbc65ad5c291f56dbf277a4e75a8b7f138b5e6334f1471a6712649e2b7043cd`
- Labels SHA-256: `65c421c5d9b7d2ff3f552150950db5c23db2401c4a5806a60725f7ec7b81b9bf`
- Best selection score: `0.9577545560826969`, epoch 5
- Training ended normally at epoch 8/10 after three non-improving epochs.

### Preserved GitHub artifacts

| Artifact | ID | Size | Archive SHA-256 |
|---|---:|---:|---|
| `matrix-nlu-student-4-v22a-report-33860928806` | 9938144318 | 302,085 B | `e71e153509e8f002fd74782ebb5667bb93b59438e6646c4c11723afe4be64129` |
| `matrix-nlu-student-4-v22a-bundle-33860928806` | 9938150338 | 217,603,720 B | `f2dfea052df525af741f8ddd98e279b5443645450d09f949970a6eac18edb987` |
| `matrix-nlu-student-4-v22a-resume-33860928806` | 9938165358 | 650,269,442 B | `ff66bd687fc55f1b767164b84795ad84aba4937130b7d8b0aead9afff5f018cd` |

Report digest matched GitHub. Its 23 files represented in `SHA256SUMS` passed verification. The resumable checkpoint SHA-256 recorded by the run is `b57737a3e3f6acf9d72da86f918f730f9bb655839c6cf00f8b614d3b706f815b`.

## 3. Training configuration

- Encoder: `Geotrend/distilbert-base-en-es-it-cased`
- Immutable revision: `36de33ec579e47f6c4e10d982d0b93871267c3e6`
- Seed: 810924
- Maximum sequence length: 64
- MASSIVE auxiliary phase: 1 epoch, 3,000 train and 600 dev examples per language, no MASSIVE test read
- Matrix phase: maximum 10 epochs
- Batch size: 16
- Gradient accumulation: 2
- Learning rate: 0.000025
- Weight decay: 0.01
- Warmup ratio: 0.12
- P0.5 train repeat: 20
- Early-stopping patience: 3
- Class weighting: inverse-frequency square root, maximum 10.0
- Configuration SHA-256: `e39049dc7dca1260850a958463f6a9f48dd7d25c1fa85d6ff9900b965ff1a0a9`

### Loss weights

| Head | Weight | Head | Weight |
|---|---:|---|---:|
| `token.boundary` | 1.40 | `sequence.dialogueAct` | 1.70 |
| `token.object` | 1.35 | `sequence.predicate` | 3.40 |
| `token.subject` | 1.20 | `sequence.subjectReferent` | 1.45 |
| `token.negation` | 4.00 | `sequence.targetReferent` | 1.45 |
| `token.temporal` | 1.25 | `sequence.ownerReferent` | 1.90 |
| `token.entity` | 1.15 | `sequence.perspectiveReferent` | 1.25 |
| `massive.intent` | 0.85 | `sequence.polarity` | 2.30 |
| `massive.slot` | 0.85 | `sequence.temporalRelation` | 1.45 |
|  |  | `sequence.claimKind` | 1.00 |

## 4. Dataset and audit evidence

The standard immutable-v2 audit passed with zero contradictory exact inputs, exact cross-split leakage, semantic-template leakage or other audit failures.

The repair was a separate train-only auxiliary dataset:

| Repair block | Rows |
|---|---:|
| IT core | 139 |
| ES core | 70 |
| EN core | 69 |
| Adult/intimacy IT | 60 |
| Cross-lingual contrast | 37 |
| **Total** | **375** |

All 375 records were unique and `split=train`. Adult/intimacy data was project-authored semantic robustness data, with no safety/moderation/censorship labels.

Important hashes:

| Evidence | SHA-256 |
|---|---|
| Matrix train | `5118d37ce2ab19d5be171f757f448698085e3c222a4a627f9838329836185820` |
| Matrix dev | `704e809f0e9ebace3a5c047989b74d354ac8811757a2644b0d9c04cfb0631012` |
| P0.5 train | `413f60ca17879ed9de440add7903b6e2abaebdfbbed6055b32c6e0b105cadfcd` |
| P0.5 dev | `7533f56194431bd17b6f8544031d5436ca14ee6e209336da8133e1f05cdf0866` |
| Repair JSONL | `8be02976d46ba47d746ff7307d688d93595453221965b3de995d4b1de655799f` |
| Repair manifest | `5c4a142a6b226c64cbfac31ee9f8d525b10f8559ba0bb303bf815d6f6c63ed2e` |
| Dataset audit | `65fa62b5f942e702b4d8be450676f09f840f11f67923a41c72350963fbc00b00` |

## 5. Unchanged development gate

The threshold selector evaluated 190 development-only candidates. Required gates remained:

- selective accuracy >= 0.99;
- claim-count exact >= 0.99;
- exact claim set >= 0.98;
- valid coverage >= 0.98;
- every critical-family/language exact set >= 0.98;
- ownership corruption = 0;
- World Truth updates = 0.

At threshold 0, combined Matrix + P0.5:

| Metric | Value |
|---|---:|
| Claim-count exact | 1.000000 |
| Exact claim set | 0.667892 |
| Claim exact | 0.709280 |
| Field exact | 0.956229 |
| Valid coverage | 0.995265 |
| Selective accuracy | 0.712655 |
| Ownership corruption | 2 |
| World Truth updates | 0 |

No threshold passed. The best zero-ownership point reached only exact set `0.575980` at coverage `0.767992`.

## 6. Complete end-to-end dev metrics

| Dataset/language | Obs. | Claims | Count exact | Exact set | Claim exact | Field exact | Span F1 | Entity F1 | Coverage | Selective acc. | Ownership corrupt. | Negation F1 | Predicate acc. | Temporal acc. |
|---|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|
| Matrix overall | 756 | 972 | 1.000000 | 0.679894 | 0.713992 | 0.959762 | 0.939775 | 0.980292 | 1.000000 | 0.713992 | 0 | 0.490644 | 0.936214 | 0.956790 |
| Matrix IT | 252 | 324 | 1.000000 | 0.619048 | 0.666667 | 0.921811 | 0.941958 | 0.970726 | 1.000000 | 0.666667 | 0 | 0.287037 | 0.808642 | 0.870370 |
| Matrix ES | 252 | 324 | 1.000000 | 0.523810 | 0.555556 | 0.957476 | 0.898748 | 0.970726 | 1.000000 | 0.555556 | 0 | 0.129534 | 1.000000 | 1.000000 |
| Matrix EN | 252 | 324 | 1.000000 | 0.896825 | 0.919753 | 1.000000 | 0.981132 | 1.000000 | 1.000000 | 0.919753 | 0 | 1.000000 | 1.000000 | 1.000000 |
| P0.5 overall | 60 | 84 | 1.000000 | 0.516667 | 0.654762 | 0.915344 | 0.975916 | 0.903670 | 0.940476 | 0.696203 | 2 | 1.000000 | 0.797619 | 0.880952 |
| P0.5 IT | 20 | 28 | 1.000000 | 0.450000 | 0.607143 | 0.916667 | 0.979167 | 0.851351 | 1.000000 | 0.607143 | 2 | 1.000000 | 0.857143 | 0.821429 |
| P0.5 ES | 20 | 28 | 1.000000 | 0.500000 | 0.642857 | 0.904762 | 0.975791 | 0.894737 | 0.892857 | 0.720000 | 0 | 1.000000 | 0.750000 | 0.892857 |
| P0.5 EN | 20 | 28 | 1.000000 | 0.600000 | 0.714286 | 0.924603 | 0.972973 | 0.970588 | 0.928571 | 0.769231 | 0 | 1.000000 | 0.785714 | 0.928571 |

World Truth updates were zero for every dataset and language.

## 7. Field/head accuracy

| Dataset/language | Dialogue act | Predicate | Subject | Target | Owner | Perspective | Polarity | Temporal relation | Claim kind |
|---|---:|---:|---:|---:|---:|---:|---:|---:|---:|
| Matrix overall | 0.958848 | 0.936214 | 1.000000 | 0.956790 | 1.000000 | 1.000000 | 0.870370 | 0.956790 | 0.958848 |
| Matrix IT | 0.938272 | 0.808642 | 1.000000 | 0.870370 | 1.000000 | 1.000000 | 0.870370 | 0.870370 | 0.938272 |
| Matrix ES | 0.938272 | 1.000000 | 1.000000 | 1.000000 | 1.000000 | 1.000000 | 0.740741 | 1.000000 | 0.938272 |
| Matrix EN | 1.000000 | 1.000000 | 1.000000 | 1.000000 | 1.000000 | 1.000000 | 1.000000 | 1.000000 | 1.000000 |
| P0.5 overall | 0.869048 | 0.797619 | 0.916667 | 0.928571 | 0.916667 | 1.000000 | 0.928571 | 0.880952 | 1.000000 |
| P0.5 IT | 0.857143 | 0.857143 | 0.928571 | 0.928571 | 0.928571 | 1.000000 | 0.928571 | 0.821429 | 1.000000 |
| P0.5 ES | 0.857143 | 0.750000 | 0.892857 | 0.928571 | 0.892857 | 1.000000 | 0.928571 | 0.892857 | 1.000000 |
| P0.5 EN | 0.892857 | 0.785714 | 0.928571 | 0.928571 | 0.928571 | 1.000000 | 0.928571 | 0.928571 | 1.000000 |

Training-head accuracy is not a substitute for end-to-end decoding. At the selected checkpoint, Matrix `tokens.negation` training accuracy was approximately `0.873621`, while end-to-end Matrix negation-span F1 was only `0.490644`.

## 8. Span quality

| Dataset/language | Source F1 | Object F1 | Negation F1 | Temporal-span F1 |
|---|---:|---:|---:|---:|
| Matrix overall | 0.992578 | 0.954069 | 0.490644 | 0.832132 |
| Matrix IT | 0.993395 | 0.948628 | 0.287037 | 0.858696 |
| Matrix ES | 0.989696 | 0.967123 | 0.129534 | 0.822430 |
| Matrix EN | 0.994626 | 0.945496 | 1.000000 | 0.800000 |
| P0.5 overall | 1.000000 | 0.922575 | 1.000000 | 0.000000 |
| P0.5 IT | 1.000000 | 0.937500 | 1.000000 | 0.000000 |
| P0.5 ES | 1.000000 | 0.920097 | 1.000000 | 0.000000 |
| P0.5 EN | 1.000000 | 0.909548 | 1.000000 | 0.000000 |

The P0.5 temporal-span score of zero must be interpreted alongside temporal-relation accuracy: the relation classifier is partly correct, but exact temporal token extraction is not.

## 9. Confidence calibration

| Dataset/language | Mean confidence | Claim exact/accuracy | Brier | ECE |
|---|---:|---:|---:|---:|
| Matrix overall | 0.958852 | 0.713992 | 0.243336 | 0.244860 |
| Matrix IT | 0.950761 | 0.666667 | 0.290422 | 0.284094 |
| Matrix ES | 0.950950 | 0.555556 | 0.364534 | 0.395395 |
| Matrix EN | 0.974844 | 0.919753 | 0.075051 | 0.055091 |
| P0.5 overall | 0.962473 | 0.654762 | 0.302307 | 0.307712 |
| P0.5 IT | 0.951459 | 0.607143 | 0.330916 | 0.344316 |
| P0.5 ES | 0.971863 | 0.642857 | 0.322050 | 0.329006 |
| P0.5 EN | 0.964099 | 0.714286 | 0.253955 | 0.249813 |

Primary calibration finding: confidence is substantially too high relative to exact correctness, especially Matrix ES and P0.5 IT/ES. Thresholding cannot correct this without collapsing coverage.

## 10. Critical-family exact-set results

### Matrix dev

| Family | Obs. | Failed | Exact set | IT | EN | ES |
|---|---:|---:|---:|---:|---:|---:|
| Negation | 144 | 114 | 0.208333 | 0.000000 | 0.625000 | 0.000000 |
| Goal | 126 | 42 | 0.666667 | 0.666667 | 0.666667 | 0.666667 |
| Temporality | 552 | 166 | 0.699275 | 0.630435 | 0.858696 | 0.608696 |
| Referents | 552 | 166 | 0.699275 | 0.630435 | 0.858696 | 0.608696 |
| Third-party/report | 216 | 110 | 0.490741 | 0.277778 | 0.833333 | 0.361111 |
| Multi-claim | 180 | 72 | 0.600000 | 0.600000 | 0.766667 | 0.433333 |

Matrix dev has no request or correction observations in this family view.

### P0.5 dev

| Family | Obs. | Failed | Exact set | IT | EN | ES |
|---|---:|---:|---:|---:|---:|---:|
| Negation | 12 | 1 | 0.916667 | 0.750000 | 1.000000 | 1.000000 |
| Request | 6 | 6 | 0.000000 | 0.000000 | 0.000000 | 0.000000 |
| Correction | 6 | 5 | 0.166667 | 0.000000 | 0.500000 | 0.000000 |
| Temporality | 42 | 19 | 0.547619 | 0.500000 | 0.642857 | 0.500000 |
| Referents | 42 | 23 | 0.452381 | 0.357143 | 0.571429 | 0.428571 |
| Third-party/report | 9 | 7 | 0.222222 | 0.333333 | 0.333333 | 0.000000 |
| Multi-claim | 18 | 1 | 0.944444 | 0.833333 | 1.000000 | 1.000000 |

P0.5 has no goal observations in this family view. Combined Matrix + P0.5 negation-family exact set is `0.262821`.

## 11. Residual error taxonomy

The development error analysis covers 271 failed observations and 759 individual errors. The taxonomy is evidence-oriented; causal attribution still requires train/dev reproduction.

| Error family | Total | IT | EN | ES | Share |
|---|---:|---:|---:|---:|---:|
| `MODEL_SEMANTIC_CLASSIFICATION` | 354 | 201 | 13 | 140 | 46.64% |
| `MODEL_SPAN_DECODING` | 293 | 106 | 45 | 142 | 38.60% |
| `AUTHORITY_OR_REFERENT_DECODING` | 62 | 48 | 6 | 8 | 8.17% |
| `MODEL_ENTITY_RESOLUTION` | 50 | 23 | 3 | 24 | 6.59% |
| **Total** | **759** | **378** | **67** | **314** | **100%** |

Representative recurrent patterns:

- IT target hallucination: a missing target is decoded as `luna`;
- ES polarity inversion on positive/negative preference language;
- ES hypotheses decoded as assertions/explicit claims;
- ES person entities added when only a location entity is gold;
- object spans truncated on consent/refusal examples;
- request remains 0/6 exact;
- correction remains 1/6 exact.

Fix policy remains: do not patch Frozen examples; reproduce the family on train/dev, classify the cause, patch the candidate and accept only after full regression/property testing.

## 12. Comparison with Student-4-v2.1

### Overall deltas

| Dataset | Metric | v2.1 | v2.2A | Delta |
|---|---|---:|---:|---:|
| Matrix | Exact set | 0.719577 | 0.679894 | -0.039683 |
| Matrix | Claim exact | 0.732510 | 0.713992 | -0.018518 |
| Matrix | Field exact | 0.994056 | 0.959762 | -0.034294 |
| Matrix | Span F1 | 0.953494 | 0.939775 | -0.013719 |
| Matrix | Entity F1 | 0.985146 | 0.980292 | -0.004854 |
| Matrix | Negation F1 | 0.509169 | 0.490644 | -0.018525 |
| Matrix | Predicate accuracy | 0.989712 | 0.936214 | -0.053498 |
| Matrix | Temporal accuracy | 1.000000 | 0.956790 | -0.043210 |
| P0.5 | Exact set | 0.450000 | 0.516667 | +0.066667 |
| P0.5 | Claim exact | 0.607143 | 0.654762 | +0.047619 |
| P0.5 | Field exact | 0.911376 | 0.915344 | +0.003968 |
| P0.5 | Span F1 | 0.977201 | 0.975916 | -0.001285 |
| P0.5 | Entity F1 | 0.945701 | 0.903670 | -0.042031 |
| P0.5 | Negation F1 | 0.940426 | 1.000000 | +0.059574 |
| P0.5 | Predicate accuracy | 0.750000 | 0.797619 | +0.047619 |
| P0.5 | Temporal accuracy | 0.892857 | 0.880952 | -0.011905 |

### Exact-set deltas by language

| Dataset/language | v2.1 | v2.2A | Delta |
|---|---:|---:|---:|
| Matrix IT | 0.611111 | 0.619048 | +0.007937 |
| Matrix ES | 0.595238 | 0.523810 | -0.071428 |
| Matrix EN | 0.952381 | 0.896825 | -0.055556 |
| P0.5 IT | 0.450000 | 0.450000 | 0.000000 |
| P0.5 ES | 0.350000 | 0.500000 | +0.150000 |
| P0.5 EN | 0.550000 | 0.600000 | +0.050000 |

Interpretation: v2.2A improves the small P0.5 challenge set, especially ES, but regresses the larger Matrix dev set. This is a mixed repair, not a gate-closing improvement. Two P0.5 Italian ownership corruptions remain unchanged.

## 13. Post-run Mixed / Head-Protected INT8 artifact

The authoritative training run itself recorded:

```text
onnxExported = false
quantizationExecuted = false
```

A later, explicitly authorized local post-run process exported and quantized the exact same model-state bytes. This distinction preserves the original run evidence.

### Artifact identity

- Execution ID: `local-20260904T1440Z`
- Artifact: `matrix-nlu-student-4-v22a-mixed-head-protected-local-20260904T1440Z.zip`
- Size: 356,134,801 B
- SHA-256: `4998ce2f44dd8553d75f86b8d7975529f6a5f779de9107eef393648022d6ccb5`
- ZIP integrity: PASS
- Internal checksums: 13/13 PASS
- Export implementation commit: `d77354ffb51fb9fa0cee8cca6dc5448ad09b2c68`
- Verification test commit: `0098d4e8fa953665d38006d22d74ab479d94b4c9`
- Export-policy/unit tests: 6/6 PASS

| Model | Size | SHA-256 |
|---|---:|---|
| FP32 ONNX reference | 234,454,909 B | `11c4f9e10c85badd1afa425cfe5f431035ec3ab61b41425f26479e58c71eb0d3` |
| Mixed/head-protected INT8 | 149,711,344 B | `738a4d052790367509d55487b649b71aaa029d839135693bb5be46f74d55ef70` |

Size reduction: `36.144931%`.

### Quantization structure

- Dynamic INT8 applied to encoder/backbone only.
- 32 encoder linear nodes selected.
- 24 `MatMulInteger` nodes produced.
- Every quantized linear operator is under `/model/encoder/`.
- 24 protected exclusion names cover native head nodes and ORT Gemm-to-MatMul rewrites.
- All 15 Matrix heads resolve to FP32 compute operators and FLOAT initializers.
- Protected-head violations: 0.
- `token.negation` remains `/model/negation/MatMul` with FLOAT weights and is not quantized.
- MASSIVE auxiliary heads are outside the mandatory protection surface.

Protected FP32 heads:

```text
token.boundary
token.object
token.subject
token.negation
token.temporal
token.entity
sequence.dialogueAct
sequence.predicate
sequence.subjectReferent
sequence.targetReferent
sequence.ownerReferent
sequence.perspectiveReferent
sequence.polarity
sequence.temporalRelation
sequence.claimKind
```

### FP32 vs mixed parity

| Check | Result |
|---|---:|
| Direct logit argmax | 77/102 |
| Protected-head argmax | 73/90 |
| Decoded semantic exact | 5/6 |
| Decoded negation-span exact | 6/6 |
| Protected heads structurally FP32 | 15/15 PASS |
| Protected-head violations | 0 |

Known difference: one Spanish probe changes `sequence.dialogueAct`. The head itself remains FP32; the difference is an indirect consequence of the quantized encoder representation. This must remain a known quality limitation.

### CPU benchmark

30 repetitions in the local CPU benchmark:

| Model | Median | p95 |
|---|---:|---:|
| FP32 | 7.900361 ms | 22.984074 ms |
| Mixed INT8 | 4.428863 ms | 19.327552 ms |

Median speedup: `1.783835x`.

This benchmark is a controlled desktop/local result, not a physical Moto G56 measurement.

## 14. Quality conclusions

### Strong evidence

- exact claim count is 1.0 on Matrix and P0.5;
- Matrix ownership corruption is zero;
- World Truth updates are zero everywhere;
- EN remains the strongest language;
- P0.5 negation F1 is 1.0;
- all protected heads remain structurally FP32;
- mixed INT8 materially reduces size and median CPU latency;
- Frozen remained unread.

### Blocking weaknesses

- unchanged canonical dev gate failed;
- no usable selected threshold exists;
- Matrix negation is extremely weak in IT and ES;
- Matrix IT predicate/target/temporal decoding regressed;
- Matrix ES polarity and calibration are poor;
- P0.5 requests and corrections remain severe failures;
- P0.5 has two Italian ownership corruptions;
- confidence is overestimated relative to correctness;
- semantic classification and span decoding account for 85.24% of individual residual errors;
- one Spanish semantic parity probe changes after encoder INT8.

### Proper runtime use

The model must remain a proposal source:

```text
NLU proposal
→ Semantic Consistency / Coherence
→ Authority Resolver
→ Memory Admission
→ downstream affective/decision/prompt layers
```

It must not independently decide truth, write memory, mutate persistent affect, convert reports/questions/requests into stable facts, or assign Luna as target without explicit/context-bound evidence.

## 15. Evidence-file checksums

| Evidence file | SHA-256 |
|---|---|
| Matrix end-to-end dev metrics | `4803a142fd05c87a909a4d6f46767273e3509470631b153e19da7703ccadd35a` |
| P0.5 end-to-end dev metrics | `964303cdd012655e38e8ad334cd436069554eeec45f612b50e11f73373f71c76` |
| Development error analysis | `e13a732b593d96efdedd9a06d5ab70cac0b9965cbebde41d1fc5680ae693bbd8` |
| Threshold selection | `8d6b1e59b536a5780ac00e72563ecbc417aaa4c23469fb5d3eb86be01f2755dd` |
| Controlled-stop summary | `209db3ded986ed3236098b6c0a6435142295031b2e2f3195549b9352e4666539` |
| Training result | `ddbc65ad5c291f56dbf277a4e75a8b7f138b5e6334f1471a6712649e2b7043cd` |

## 16. Frozen and mutation guard

```text
trainingSplitsRead = [train, dev]
frozenDataRead = false
frozenEvaluationExecuted = false
frozenPredictionsRead = false
retrainingExecutedDuringQuantization = false
productionPromotionExecuted = false
```

No Frozen metric is present in this dossier. No gate was lowered. No dev/test/Frozen data was modified.

Final decision: **`EXPERIMENTAL_TEST_CANDIDATE / NOT_PRODUCTION_APPROVED`**.
