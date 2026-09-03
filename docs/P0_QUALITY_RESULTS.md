# Gate 08–09 — Unified runner and quality benchmark

Measured: 2026-09-03  
Commit: `fa8b76b911321921a391845ccdbeda5177fe807f`  
GitHub Actions run: `33743338928` — **SUCCESS**  
Artifact: `p0-results`, id `9888631519`, SHA-256
`67c498c076d425c215eca5a3b7c4529f77bcff0895441afc3485e060e8765409`

## Reproducibility boundary

The unified runner evaluated A and B against the same immutable `p0.gold.v1`:
22 scenarios and 66 parallel IT/EN/ES variants. Candidate C is represented in
the same result envelope as `CANDIDATE_C_NOT_READY`; it has no fabricated rows
or zero-valued metrics. Unit tests completed before the benchmark in the same
CI job. The generated artifact contains machine-readable JSON, all predictions
and diagnostics, plus a human-readable Markdown summary.

Command used by CI:

```text
gradle --no-daemon :core:test
gradle --no-daemon :cli:run
```

## Overall quality

| Metric | A — frozen deterministic | B — ICU + OpenNLP | C — compact ONNX |
|---|---:|---:|---:|
| Executed cases | 66 | 66 | not executed |
| Exact claim count | 0.9394 | **1.0000** | not available |
| Main-field exact | 0.7299 | **0.9924** | not available |
| Source-span F1 | 0.9412 | **1.0000** | not available |
| Negation-scope F1 | 0.6429 | **1.0000** | not available |
| Entity type/link F1 | 0.4231 | **0.9032** | not available |
| Unknown rate | 0.7500 | **0.0417** | not available |
| False structured claim rate | 0.0000 | 0.0000 | not available |
| Owner/perspective violations | **8** | **0** | not available |
| Invented World Truth | 0 | 0 | not available |
| Warm-like JVM p50 | 9,458 ns | 1,911,047 ns | not available |
| Warm-like JVM p95 | 1,200,481 ns | 4,508,986 ns | not available |

Latency is a single GitHub-hosted JVM wall-clock diagnostic. Candidate
construction/model loading occurs outside the timed per-case call. These values
are neither cold-init measurements nor Android CPU/PSS/thermal evidence.

## Per-language quality and worst language

| Candidate | Language | Main-field exact | Case exact | Claim-count exact | Unknown | Owner/perspective violations |
|---|---|---:|---:|---:|---:|---:|
| A | IT | 0.9167 | 0.6818 | 1.0000 | 0.2917 | 0 |
| A | EN | 0.6281 | 0.0000 | 0.9091 | 1.0000 | 4 |
| A | ES | 0.6281 | 0.0000 | 0.9091 | 1.0000 | 4 |
| B | IT | 0.9886 | 0.9091 | 1.0000 | 0.0417 | 0 |
| B | EN | **0.9962** | 0.9545 | 1.0000 | 0.0417 | 0 |
| B | ES | 0.9924 | 0.9545 | 1.0000 | 0.0417 | 0 |

- A worst language: EN/ES tie at field exact `0.6281` (runner reports EN by
  deterministic first-minimum ordering).
- B worst language: IT at field exact `0.9886`.
- B passes the zero-tolerance owner/perspective and World Truth gates on this
  gold set; A does not pass the ownership gate.

## Split report

| Candidate | Split | Cases | Main-field exact | Case exact | Claim-count exact |
|---|---|---:|---:|---:|---:|
| A | train | 21 | 0.7662 | 0.2381 | 1.0000 |
| A | dev | 18 | 0.7318 | 0.2222 | 0.7778 |
| A | test | 27 | 0.7003 | 0.2222 | 1.0000 |
| B | train | 21 | 1.0000 | 1.0000 | 1.0000 |
| B | dev | 18 | 0.9962 | 0.9444 | 1.0000 |
| B | test | 27 | 0.9832 | 0.8889 | 1.0000 |

The test set was not used for post-result tuning. Its residual errors are
reported, not patched, in the error-analysis gate.

## Gate conclusion

- Unified runner: **PASS**.
- Machine-readable JSON and human report: **PASS**.
- Candidate A trilingual quality/critical ownership gate: **FAIL**.
- Candidate B benchmark quality gate: **PASS on frozen P0 gold**.
- Candidate B production eligibility: **FAIL / LICENSE_BLOCKED** because the
  Italian OpenNLP POS artifact is trained from UD Italian VIT under
  `CC BY-NC-SA 3.0`; quality does not waive this stop condition.
- Candidate C: **CANDIDATE_C_NOT_READY**, not scored.
- Confidence values remain uncalibrated scores; no probability claim is made.

