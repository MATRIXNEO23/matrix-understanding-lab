# Unified benchmark results

Gold: `p05.expanded.v1` (same frozen 264 variants for every executable candidate).

| Candidate | Status | Field exact | Worst language | Claim-count exact | Span F1 | Negation F1 | Entity F1 | Ownership violations | World Truth | p50 ns | p95 ns |
|---|---|---:|---|---:|---:|---:|---:|---:|---:|---:|---:|
| A_BASELINE_FROZEN | READY | 0.7341 | en (0.6260) | 0.8750 | 0.8781 | 0.6034 | 0.3404 | 42 | 0 | 4440 | 623565 |
| B_ICU_OPENNLP_MATRIX | LAB_ONLY_LICENSE_BLOCKED | 0.9851 | it (0.9815) | 1.0000 | 1.0000 | 0.9375 | 0.7662 | 0 | 0 | 834305 | 3022483 |
| C_ONNX_COMPACT | CANDIDATE_C_NOT_READY | — | — | — | — | — | — | — | — | — | — |

Candidate C has no quality or footprint values because Gate 06 found no valid model; this is not scored as zero.

Latency is a single CI/JVM wall-clock diagnostic, not a Moto G56 measurement. Confidence values are scores, not calibrated probabilities.
