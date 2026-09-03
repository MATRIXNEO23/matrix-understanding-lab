# Gate 02 — reproducible clean Italian POS training

Measured: 2026-09-03  
Pipeline commit: `47d9b15ce09af75d89e05677b39069ba6ede6cb8`  
GitHub Actions run: `33781321112` — **SUCCESS**  
Artifact: `p05-training`, id `9903733326`, archive SHA-256
`cd391f1e6c9077e844c154098a32a8d520d165c50d7c7447e6c8e3d2a6ef3d99`

## Selected artifact

| Field | Value |
|---|---|
| Resource | `opennlp-it-ud-markit-pos-p05.bin` |
| Configuration | `PERCEPTRON`, 100 iterations, cutoff 1 |
| Size | 126,860 bytes |
| Model SHA-256 | `14dca59954129b1f4554def4e16d1b626160f0289ab568f5a1efdd2d1bba91c7` |
| MarkIT dev token accuracy | 0.926243 |
| MarkIT frozen-test token accuracy | 0.920851 |

Selection used dev accuracy only, followed by smaller artifact and lexical ID
as deterministic tie-breakers. The MarkIT test result was computed only after
selection.

## Executed variants

| Variant | Dev token accuracy | Bytes | Selected |
|---|---:|---:|---|
| perceptron-i100-c1 | **0.926243** | **126,860** | yes |
| maxent-i200-c1 | 0.920473 | 417,199 | no |
| maxent-i100-c1 | 0.920281 | 416,913 | no |

All variants use exactly 611 upstream training sentences / 19,893 tokens in
fixed upstream order. The dev partition contains 341 sentences / 10,399 tokens;
the frozen test partition contains 340 / 10,196. OpenNLP is pinned to 2.5.11 and
the pipeline records Java version, immutable source URLs, Git blob SHA-1,
content SHA-256, normalized split SHA-256, parameters, outputs and attribution.

The `seed=20260903` is recorded as the experiment identity; no stochastic
shuffle is performed. Reproducibility will be enforced by comparing the model
hash on a second independent CI run before Gate 06 is closed.

## Gate 02 status

`PASS` for executable source-to-model automation and first CI training run.
Model-hash repeatability remains a Gate 06 assertion, not an unverified claim.
