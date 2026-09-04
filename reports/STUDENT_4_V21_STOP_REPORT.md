# Student-4-v2.1 — Controlled Stop Report

Final state: `STOPPED_FOR_REVIEW`  
Cause class: `WORKFLOW/INFRASTRUCTURE_FAILURE`  
Frozen status: `FROZEN NOT TOUCHED`

## Identity and run

- Repository/branch: `MATRIXNEO23/matrix-understanding-lab` / `main`
- Run ID: `33837897457`; workflow run 1; attempt 1
- Launch HEAD/commit: `72f14286e89df88f41aedb169c7307b26b57eedf`
- Job: `train-and-dev-only`, ID `100914050985`
- Failed step: 11, `Evaluate development and stop`; exit code 1
- Exact error:

  ```text
  Traceback (most recent call last):
    File "/home/runner/work/matrix-understanding-lab/matrix-understanding-lab/matrix_nlu/controlled_dev_v21.py", line 13, in <module>
      from matrix_nlu.pipeline_support import Step, atomic_json, run_step, sha256
  ModuleNotFoundError: No module named 'matrix_nlu'
  Error: Process completed with exit code 1.
  ```

Training completed successfully. The failure occurred before end-to-end dev
prediction, threshold selection or any dev gate decision. It is not classified
as a model failure or a dev-gate failure. Per the controlled-stop policy, it was
not corrected or rerun.

## Configuration

- Config: `matrix_nlu/train_config_v21.json`
- Config SHA-256: `1011dae1572c24b7aabb07c21027c2eab93aa285f17de536bc9bfa4a671b2964`
- Dataset/model: `matrix.nlu.dataset.v2` / `student-4-v2.1`
- Encoder: `Geotrend/distilbert-base-en-es-it-cased` revision
  `36de33ec579e47f6c4e10d982d0b93871267c3e6`, four retained layers
- Seed/max length: 810923 / 64
- MASSIVE: 1 epoch; 3,000 train and 600 dev per language; test count 0
- Matrix: maximum 8 epochs; batch 16; accumulation 2; LR `3e-5`;
  weight decay `0.01`; warmup `0.1`; P0.5 repeat 16; patience 2
- Loss: inverse-frequency-square-root token/sequence weights, cap 8
- Gates: unchanged. No automatic promotion.

## Dataset, provenance and audit

- Matrix train: 2,775 rows / 3,615 claims / 925 per language;
  SHA-256 `5118d37ce2ab19d5be171f757f448698085e3c222a4a627f9838329836185820`
- Matrix dev unchanged: 756 rows / 972 claims;
  SHA-256 `704e809f0e9ebace3a5c047989b74d354ac8811757a2644b0d9c04cfb0631012`
- P0.5 train/dev unchanged:
  `413f60ca17879ed9de440add7903b6e2abaebdfbbed6055b32c6e0b105cadfcd` /
  `7533f56194431bd17b6f8544031d5436ca14ee6e209336da8133e1f05cdf0866`
- Mapping/provenance SHA-256:
  `c53ffb13f5b0ebdc15892a9b18890f3caa3c16347600c679c2ecfeab321fcbbc`;
  1,322 claim corrections, 426 partition drops, 129 train additions
- Audit: PASS; zero incompatible duplicate gold, exact cross-split surface,
  semantic-template leakage and structural failures.
- Audit frozen scope was structural separation/checksum only; no predictions,
  tuning, evaluation or error analysis used frozen content.
- Training provenance: `trainingSplitsRead=[train,dev]`;
  `frozenDataRead=false`; `frozenEvaluationDeferred=true`.

## Training result

- Parameters: 58,599,411 total/trainable; encoder 58,412,544; heads 186,867
- Model-state size: 234,435,022 bytes; complete bundle payload 235,626,166 bytes
- Completed: MASSIVE epoch 1 plus Matrix epochs 1–7 of maximum 8
- Early stop: Matrix epoch 7, patience 2
- Best epoch: Matrix epoch 5
- Best dev selection score: `0.9676758069767126`
- Best checkpoint/model-state SHA-256:
  `6228fddb5240edaac58356ccd175f6a97e2bc0fccd6344ebf675f42103317bae`
- Latest resumable checkpoint: epoch 7, SHA-256
  `34cd061c4eec158b9fc89341030adbc122f0355f09923c54eefe0da72acf66e8`
- Training-result SHA-256:
  `5ec9406a1124b6a4eabea39177dbadc45856360e0fa9c1c52544026754531abf`

Latest epoch-7 metrics:

| Metric | Matrix dev | P0.5 dev |
|---|---:|---:|
| Train loss | 0.009006067 | 0.009006067 |
| Dev loss | 0.075984117 | 0.324663108 |
| Macro-head accuracy | 0.981289997 | 0.949732167 |
| Macro-head F1 | N/A — trainer does not emit it | N/A |

Latest per-head accuracy:

| Head | Matrix dev | P0.5 dev |
|---|---:|---:|
| claim kind | 1.000000 | 1.000000 |
| dialogue act | 1.000000 | 0.869048 |
| owner referent | 1.000000 | 1.000000 |
| perspective referent | 1.000000 | 1.000000 |
| polarity | 0.913580 | 0.928571 |
| predicate | 0.989712 | 0.821429 |
| subject referent | 1.000000 | 0.916667 |
| target referent | 1.000000 | 0.928571 |
| temporal relation | 1.000000 | 0.880952 |
| boundary token | 0.986904 | 1.000000 |
| entity token | 0.987964 | 0.987593 |
| negation token | 0.859579 | 0.985112 |
| object token | 0.981612 | 0.940447 |
| subject token | 1.000000 | 1.000000 |
| temporal token | 1.000000 | 0.987593 |

## Required end-to-end dev evidence

No end-to-end dev inference completed because the evaluator launcher failed at
module import. Therefore the following are unavailable and must not be inferred
from training-head accuracy: IT/EN/ES breakdown, claim-count exact, global or
per-language exact-set, field exact, span F1, entity F1, end-to-end negation and
temporal metrics, ownership corruption, invented World Truth, coverage,
selective accuracy, gate values/statuses, and family error analysis.

No gate is recorded as passed or failed. The only valid decision is
`STOPPED_FOR_REVIEW`.

## Comparison with Student-4-v2 baseline

- Best dev selection score: 0.967675807 vs 0.959051200,
  delta **+0.008624607**.
- Latest Matrix dev loss: 0.075984117 vs 0.260681200,
  delta **-0.184697083**; macro-head accuracy 0.981289997 vs 0.968186627,
  delta **+0.013103370**.
- Latest P0.5 dev loss: 0.324663108 vs 0.369114218,
  delta **-0.044451110**; macro-head accuracy 0.949732167 vs 0.948715431,
  delta **+0.001016737**.
- Training-head improvements include Matrix temporal relation to 1.0 and
  temporal token to 1.0; Matrix negation token regressed from 0.873621 to
  0.859579. P0.5 dialogue act improved from 0.857143 to 0.869048; other
  targeted P0.5 heads remain mixed.
- These are diagnostic training-head deltas only. A numeric end-to-end
  regression/generalization judgment is unavailable because dev inference did
  not run.

## Artifacts preserved

- Report artifact `9926693211`: 30,411 bytes; archive SHA-256
  `ae4772e9c4ad7b4d5d4583398d4bd8e6465196101f98f49cf82ec59d409c821d`
- Bundle artifact `9926696572`: 217,601,847 bytes; archive SHA-256
  `0855170a6b62e7ec577340199736a69365aef1cef22957024dceb1d86ea26936`
- Resume artifact `9926705228`: 649,139,558 bytes; archive SHA-256
  `1ac380ed7a166502e9f30997000b7951598c7db72ad402de4d31250b331ff63e`
- Full workflow/job logs, audit, manifests, provenance mapping, training
  history/progress, labels, model state, tokenizer and checkpoint are preserved.
- FP32 ONNX, INT8, latency/parity and package artifacts: not produced; these
  stages were outside the authorized dev-only run.

## Risks and decision

- P0: none observed; frozen remained closed and no production mutation occurred.
- P1: no valid end-to-end dev gate decision exists due to evaluator-launch
  infrastructure failure; the model must not be promoted.
- P2: Matrix negation token accuracy regressed relative to baseline; this is
  unconfirmed at end-to-end level.

Decision: `STOPPED_FOR_REVIEW`. Do not correct, rerun, change configuration,
open frozen, create V2.2/V3, export, package or promote without new explicit
supervisor authorization.
