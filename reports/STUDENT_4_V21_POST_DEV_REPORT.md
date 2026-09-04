# Student-4-v2.1 — Post-run development gate report

Date: 2026-09-04  
Final decision: `STOPPED_FOR_REVIEW`  
Production status: `NOT PRODUCTION APPROVED`  
Frozen status: `NOT READ / NOT EVALUATED`

## Identity and immutable provenance

- Repository/branch: `MATRIXNEO23/matrix-understanding-lab` / `main`
- Source training run: `33837897457`
- Source training commit: `72f14286e89df88f41aedb169c7307b26b57eedf`
- Pipeline import fix: `3dd2be2cc45d4cde1b439fb261c8c167ab1eb4bb`
- Post-run workflow: `31ba96d40d6f662bbb253ce2c60146d8cf6f026e`
- Provenance hardening and final launch: `813126cbff80bfb6bc82636c87e8ac16b1a917a8`
- Final dev-only run: `33848931720`, job `100947061031`
- Evaluation artifact: `matrix-nlu-student-4-v21-post-dev-33848931720`, ID `9927657001`
- Artifact archive SHA-256:
  `2314694e5b45f6a95ba409808394013d3a43f92f6d798765fc5cdb01ff3fcb41`
- Model-state SHA-256:
  `6228fddb5240edaac58356ccd175f6a97e2bc0fccd6344ebf675f42103317bae`
- Training-result SHA-256:
  `5ec9406a1124b6a4eabea39177dbadc45856360e0fa9c1c52544026754531abf`
- Labels SHA-256:
  `65c421c5d9b7d2ff3f552150950db5c23db2401c4a5806a60725f7ec7b81b9bf`

The final run verified the required files, variant `student-4-v2.1`,
`studentLayers == 4`, `trainingSplitsRead == ["train", "dev"]`,
`frozenDataRead == false`, and the model-state checksum before inference.
It reused the preserved source bundle and did not train, resume, export,
quantize, package, promote, or execute frozen evaluation.

## Gate result

- Threshold candidates evaluated: 188, development only.
- Selection status: `FAILED_GATE`.
- Selected threshold: `null`.
- Controlled decision: `STOPPED_FOR_REVIEW`.
- Threshold process exit code: 2, handled as an expected controlled gate
  outcome; the workflow remained green so it could preserve all evidence.
- Gate policy was unchanged: selective accuracy >= 0.99, claim-count exact >=
  0.99, exact claim set >= 0.98, valid coverage >= 0.98, critical-family exact
  claim set >= 0.98 per family/language, ownership corruption = 0 and World
  Truth updates = 0.

At threshold 0, the combined Matrix + P0.5 result had claim-count exact 1.0,
exact claim set 0.699755, valid coverage 0.995265, selective accuracy 0.725975,
two ownership corruptions and zero World Truth updates. The highest selective
accuracy (1.0) occurred only at threshold 0.995933 with coverage 0.000947 and
exact claim set 0.0. Thresholding therefore cannot repair this candidate
without violating coverage and exact-set gates.

## Complete end-to-end dev summary

| Dataset/language | Obs. | Claims | Count exact | Exact set | Claim exact | Field exact | Span F1 | Entity F1 | Coverage | Selective acc. | Ownership corrupt. | Negation F1 | Predicate acc. | Temporal acc. |
|---|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|
| Matrix overall | 756 | 972 | 1.000000 | 0.719577 | 0.732510 | 0.994056 | 0.953494 | 0.985146 | 1.000000 | 0.732510 | 0 | 0.509169 | 0.989712 | 1.000000 |
| Matrix EN | 252 | 324 | 1.000000 | 0.952381 | 0.962963 | 1.000000 | 0.994439 | 1.000000 | 1.000000 | 0.962963 | 0 | 1.000000 | 1.000000 | 1.000000 |
| Matrix IT | 252 | 324 | 1.000000 | 0.611111 | 0.623457 | 0.985597 | 0.945368 | 0.970726 | 1.000000 | 0.623457 | 0 | 0.247012 | 1.000000 | 1.000000 |
| Matrix ES | 252 | 324 | 1.000000 | 0.595238 | 0.611111 | 0.996571 | 0.922417 | 0.985146 | 1.000000 | 0.611111 | 0 | 0.158228 | 0.969136 | 1.000000 |
| P0.5 overall | 60 | 84 | 1.000000 | 0.450000 | 0.607143 | 0.911376 | 0.977201 | 0.945701 | 0.940476 | 0.645570 | 2 | 0.940426 | 0.750000 | 0.892857 |
| P0.5 EN | 20 | 28 | 1.000000 | 0.550000 | 0.678571 | 0.932540 | 0.976744 | 0.970588 | 0.964286 | 0.703704 | 0 | 0.930818 | 0.785714 | 0.928571 |
| P0.5 IT | 20 | 28 | 1.000000 | 0.450000 | 0.607143 | 0.904762 | 0.978502 | 0.896104 | 0.964286 | 0.629630 | 2 | 0.968553 | 0.785714 | 0.857143 |
| P0.5 ES | 20 | 28 | 1.000000 | 0.350000 | 0.535714 | 0.896825 | 0.976427 | 0.973684 | 0.892857 | 0.600000 | 0 | 0.921053 | 0.678571 | 0.892857 |

World Truth updates were zero in every dataset and language. Matrix rejected
and abstained on zero claims. P0.5 rejected/abstained on 5/84 claims
(0.059524 overall; EN 1/28, IT 1/28, ES 3/28).

## Field/head and span status

| Field/head | Matrix dev | P0.5 dev | Status |
|---|---:|---:|---|
| `sequence.claimKind` | 1.000000 | 1.000000 | strong |
| `sequence.dialogueAct` | 1.000000 | 0.869048 | protected / weak on P0.5 |
| `sequence.predicate` | 0.989712 | 0.750000 | protected / critical on P0.5 |
| `sequence.subjectReferent` | 1.000000 | 0.916667 | protected |
| `sequence.targetReferent` | 1.000000 | 0.928571 | protected |
| `sequence.ownerReferent` | 1.000000 | 0.916667 | unsafe: two P0.5 IT corruptions |
| `sequence.perspectiveReferent` | 1.000000 | 1.000000 | strong, still invariant-protected |
| `sequence.polarity` | 0.956790 | 0.928571 | weak interaction with negation |
| `sequence.temporalRelation` | 1.000000 | 0.892857 | protected / weak on P0.5 |

Span-level results:

| Span metric | Matrix dev | P0.5 dev |
|---|---:|---:|
| source spans F1 | 0.994320 | 1.000000 |
| object span F1 | 0.994739 | 0.944932 |
| negation span F1 | 0.509169 | 0.940426 |
| temporal span F1 | 0.833333 | 0.571429 |

The original training-head values remain useful diagnostics but do not replace
end-to-end values. In particular, Matrix `tokens.negation` training accuracy
was 0.873621 at the best checkpoint while end-to-end negation span F1 is only
0.509169 (IT 0.247012; ES 0.158228). P0.5 predicate training accuracy was
0.809524, while end-to-end predicate accuracy is 0.75.

## Critical-family residuals at threshold 0

| Family | Obs. | Failed | Exact set | IT | EN | ES |
|---|---:|---:|---:|---:|---:|---:|
| negation | 156 | 101 | 0.352564 | 0.173077 | 0.730769 | 0.153846 |
| request | 6 | 6 | 0.000000 | 0.000000 | 0.000000 | 0.000000 |
| goal | 126 | 36 | 0.714286 | 0.714286 | 0.714286 | 0.714286 |
| correction | 6 | 5 | 0.166667 | 0.000000 | 0.500000 | 0.000000 |
| temporality | 594 | 140 | 0.764310 | 0.707071 | 0.909091 | 0.676768 |
| referents | 594 | 142 | 0.760943 | 0.702020 | 0.904040 | 0.676768 |
| third-party/report | 225 | 63 | 0.720000 | 0.613333 | 0.986667 | 0.560000 |
| multi-claim | 198 | 81 | 0.590909 | 0.500000 | 0.787879 | 0.484848 |

The deterministic residual taxonomy covers 245 failed observations and 428
individual errors:

| Error family | Count | IT | EN | ES |
|---|---:|---:|---:|---:|
| `MODEL_SPAN_DECODING` | 269 | 118 | 28 | 123 |
| `MODEL_SEMANTIC_CLASSIFICATION` | 99 | 58 | 13 | 28 |
| `MODEL_ENTITY_RESOLUTION` | 40 | 24 | 2 | 14 |
| `AUTHORITY_OR_REFERENT_DECODING` | 20 | 8 | 4 | 8 |

## Comparison with Student-4-v2

Student-4-v2.1 substantially improves Matrix end-to-end quality versus the
recorded Student-4-v2 dev baseline: exact set 0.719577 vs 0.560847, claim exact
0.732510 vs 0.619342, field exact 0.994056 vs 0.970736 and span F1 0.953494 vs
0.927804. It does not preserve the same direction on P0.5: exact set 0.45 vs
0.483333, claim exact 0.607143 vs 0.630952, field exact 0.911376 vs 0.916667
and entity F1 0.945701 vs 0.972851; span F1 improves to 0.977201 from 0.968394.
P0.5 ownership corruption remains 2. Therefore this is a useful research
baseline, not a production candidate.

## Targeted quantization preparation — not executed

The policy in
`docs/decisions/2026-09-04_STUDENT_4_V21_TARGETED_QUANTIZATION.md` is binding.
No quantization candidate may be tested while this dev gate is failed. If a
future corrected model passes dev, the prepared order is:

1. preserve the complete torch/FP32 baseline;
2. export and measure ONNX FP32;
3. test dynamic INT8 on eligible encoder weights;
4. test selective/mixed precision while protecting negation, predicate,
   dialogue act, subject/target referents, temporal relation, object-token
   decoding and authority/ownership/perspective invariants;
5. compare each candidate head-by-head, class-by-class and per language;
6. reject macro delta below -0.005, prefer protected-family delta no worse
   than -0.002, and require discussion before any protected delta down to
   -0.005; reject all critical qualitative regressions.

This section is preparation only. No FP32 ONNX export, INT8/mixed-precision
conversion, frozen gate, Android integration or production promotion was run.

## Reproducibility and final decision

The final artifact's present files match its `SHA256SUMS`. The archive digest
matches GitHub's recorded artifact digest. Matrix metrics, P0.5 metrics and the
threshold-selection report reproduce the preceding post-run byte-for-byte.
Key evidence SHA-256 values:

- Matrix metrics: `1cbd17a7982e683a022c78b0f4bd06d0b276af3dde117d6bbf7f8e9589a34f4f`
- P0.5 metrics: `50dc28f0541608d4d2fe7a28fc61f8140e58c114c77712c1e3211ce6e4d9777b`
- Error analysis: `d9bb27ed3f951613b6d7d6f15389f26fbccaaed54a35e8a77809bff0850a88cb`
- Threshold report: `57edaaf943f913e22b3eea0385360fb5820347c97e605495aa2dadc4f435b2fa`

Final decision: `STOPPED_FOR_REVIEW`. Preserve the model and evidence. Do not
lower gates, retrain blindly, change dev/test/frozen, quantize, open frozen,
package, integrate or promote automatically.
