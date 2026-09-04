# Student-4-v2.2A — Controlled Repair report

Date: 2026-09-04  
Final decision: `EXPERIMENTAL_TEST_CANDIDATE / NOT_PRODUCTION_APPROVED`  
Frozen status: `NOT READ / NOT EVALUATED`  
Quantization status: `NOT EXECUTED`

## Identity and immutable provenance

- Repository/branch: `MATRIXNEO23/matrix-understanding-lab` / `main`
- Authoritative run: [33860928806](https://github.com/MATRIXNEO23/matrix-understanding-lab/actions/runs/33860928806)
- Run HEAD: `617aeca8a6abac4366eb13347fb88026307dc3b8`
- Job: `100984948899`, workflow conclusion `success`
- Variant/layers: `student-4-v2.2a` / 4 encoder layers
- Parameters: 58,599,411 total; 58,412,544 encoder; 186,867 heads
- Model-state SHA-256: `446b6a58265500001efd350f81d75867227cbfd3c6da699ed9c9330257d16a9c`
- Training-result SHA-256: `ddbc65ad5c291f56dbf277a4e75a8b7f138b5e6334f1471a6712649e2b7043cd`
- Labels SHA-256: `65c421c5d9b7d2ff3f552150950db5c23db2401c4a5806a60725f7ec7b81b9bf`

The workflow trained fresh with `studentLayers=4`, `--defer-frozen`, train/dev only, and no ONNX or quantization. Matrix training stopped normally at epoch 8/10 after three non-improving epochs; the best selection score was `0.9577545560826969` at epoch 5.

## Preserved artifacts

| Artifact | ID | Size | Archive SHA-256 |
|---|---:|---:|---|
| `matrix-nlu-student-4-v22a-report-33860928806` | `9938144318` | 302,085 B | `e71e153509e8f002fd74782ebb5667bb93b59438e6646c4c11723afe4be64129` |
| `matrix-nlu-student-4-v22a-bundle-33860928806` | `9938150338` | 217,603,720 B | `f2dfea052df525af741f8ddd98e279b5443645450d09f949970a6eac18edb987` |
| `matrix-nlu-student-4-v22a-resume-33860928806` | `9938165358` | 650,269,442 B | `ff66bd687fc55f1b767164b84795ad84aba4937130b7d8b0aead9afff5f018cd` |

The report archive was downloaded and its SHA-256 matches GitHub. All 23 report files represented in `SHA256SUMS` match; no mismatch or unlisted evidence file was found. Bundle and resumable checkpoint remain preserved even though the dev gate failed. The resumable checkpoint SHA-256 recorded by the run is `b57737a3e3f6acf9d72da86f918f730f9bb655839c6cf00f8b614d3b706f815b`.

## Pre-training audit repair

Run `33855798760` stopped in the dataset audit before training; it was not a training failure. The controlled repair now preserves the ordinary immutable-v2 audit and emits the intentionally imbalanced repair as a separate auxiliary file loaded only with `matrix-v2-train.jsonl`.

The standard audit is `PASS`: zero contradictory exact inputs, exact cross-split leakage, semantic-template leakage, or other audit failures. Its scope records `frozenPredictionsRead=false` and `frozenDataUsedForTuning=false`.

The repair file SHA-256 is `8be02976d46ba47d746ff7307d688d93595453221965b3de995d4b1de655799f`; its manifest SHA-256 is `5c4a142a6b226c64cbfac31ee9f8d525b10f8559ba0bb303bf815d6f6c63ed2e`. Independent verification found 375 unique rows, all `split=train`:

| Repair block | Rows |
|---|---:|
| IT core | 139 |
| ES core | 70 |
| EN core | 69 |
| Adult/intimacy IT | 60 |
| Cross-lingual contrast | 37 |

The adult/intimacy block is internally project-authored semantic robustness data: 15 desire/assert, 15 request, 11 consent, 8 refusal/boundary, and 11 common English terms inside Italian sentences. It uses ordinary semantic predicates only (`goal.object`, `consent.grant`, `consent.refuse`, `speech.unresolved`) and adds no safety, moderation, or censorship label.

Immutable dev hashes remain exactly:

- Matrix dev: `704e809f0e9ebace3a5c047989b74d354ac8811757a2644b0d9c04cfb0631012`
- P0.5 dev: `7533f56194431bd17b6f8544031d5436ca14ee6e209336da8133e1f05cdf0866`

## Development gate result

- Selection: `FAILED_GATE`
- Selected threshold: `null`
- Candidate thresholds evaluated: 190, development only
- Gates unchanged: selective accuracy >= 0.99, claim-count exact >= 0.99, exact-set >= 0.98, valid coverage >= 0.98, every critical-family/language exact-set >= 0.98, ownership corruption = 0, World Truth updates = 0
- Workflow controlled summary: `STOPPED_FOR_REVIEW`
- User-authorized experimental disposition: `EXPERIMENTAL_TEST_CANDIDATE / NOT_PRODUCTION_APPROVED`

At threshold zero, combined Matrix + P0.5 has claim-count exact `1.0`, exact-set `0.667892`, claim exact `0.709280`, field exact `0.956229`, valid coverage `0.995265`, selective accuracy `0.712655`, ownership corruption `2`, and World Truth updates `0`. No threshold satisfies the unchanged gate. The best zero-ownership point reaches exact-set `0.575980` with coverage `0.767992`, also far below the gate.

## Complete end-to-end dev metrics

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

World Truth updates are zero in every dataset and language.

## Comparison with Student-4-v2.1

The repair is mixed, not a gate-closing improvement.

- Matrix overall regresses: exact-set `0.719577 -> 0.679894`, claim exact `0.732510 -> 0.713992`, negation F1 `0.509169 -> 0.490644`, predicate `0.989712 -> 0.936214`, and temporal accuracy `1.0 -> 0.956790`.
- Matrix IT exact-set improves slightly `0.611111 -> 0.619048` and negation F1 improves `0.247012 -> 0.287037`, but predicate collapses `1.0 -> 0.808642` and temporal accuracy falls `1.0 -> 0.870370`.
- Matrix ES regresses in exact-set `0.595238 -> 0.523810` and negation F1 `0.158228 -> 0.129534`, despite predicate improving to `1.0`.
- Matrix EN remains strongest but exact-set falls `0.952381 -> 0.896825`.
- P0.5 improves in exact-set `0.450000 -> 0.516667`, claim exact `0.607143 -> 0.654762`, negation F1 `0.940426 -> 1.0`, and predicate `0.750000 -> 0.797619`.
- P0.5 ES exact-set improves `0.350000 -> 0.500000`; EN improves `0.550000 -> 0.600000`; IT remains `0.450000`.
- P0.5 still has two Italian ownership corruptions. Entity F1 regresses `0.945701 -> 0.903670` and temporal accuracy falls `0.892857 -> 0.880952`.

Residual analysis covers 271 failed observations and 759 individual errors: semantic classification 354, span decoding 293, authority/referent decoding 62, and entity resolution 50. Request remains 0/6 exact, correction 1/6 exact, and combined negation-family exact-set is only `0.262821`.

## Frozen guard, quantization, and decision

`FROZEN_GUARD.txt` records:

- `frozenDataRead=false`
- `frozenEvaluationExecuted=false`
- `trainingSplitsRead=train,dev`
- `onnxExported=false`
- `quantizationExecuted=false`

No production promotion is authorized. The FP32 bundle and resumable checkpoint are preserved for a possible later experimental quantization decision, but quantization has not been started. Any later INT8/mixed-precision experiment must compare protected heads and languages against this FP32 evidence and must not be described as production approval.

Final decision: **`EXPERIMENTAL_TEST_CANDIDATE / NOT_PRODUCTION_APPROVED`**.
