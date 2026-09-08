# Student-5 CP47 — FP32 training completed, selection pending

STUDENT5_FP32 = TRAINING_COMPLETED_SELECTION_PENDING

Starting HEAD: `c9b4984fba6c3da71e27387c4008d78a52208385`. Final delivery SHA is the commit introducing this report and is returned in the final handoff.

## Recovery and immutable inputs

The invalid CP46 local archive was quarantined as `cp47/quarantine/INVALID-cp46.zip.disabled`; its former path is absent. A fresh download of CP45 Release 384399324 / asset 549697344 passed 88,361,246 bytes, archive SHA-256 `7804bfb245b71df9b835fff7ee00f6ec887e019772ae34c82d269d821d587191`, and internal FP32 SHA-256 `d6e45891d1e0ec4ed023caaeb17c0dd0ae80a93b8bf877d275310b7f2837efa2`. Rechecks before and after training passed.

TRAIN `student5-matrix-nlu-v3-train-v2.1-cp43r2` remains at SHA-256 `f90ae775a44023c37bf0c3a5087d64746413cbec770ca36cf154d1d533544aa4`. The target builder reproduced 4,355 examples exactly in ordered logical bytes; training consumed the immutable CP44 target file with SHA-256 `1c31639c65a958e5490378df4956c3d6f036def003eb93336704fb6ca97cda45`. G03 PASS: eight rows, 14 ambiguous fields and 28 ordered alternatives retained.

## Executed training

- One FP32 run at canonical capacity stage A: frozen 12-layer MiniLM encoder plus unchanged V3 heads. 37,171,640 total parameters; 172,088 trainable.
- Seed 810924; AdamW, LR 0.001, betas (0.9, 0.999), epsilon 1e-8, weight decay 0.01; linear warmup for 137 steps then linear decay; batch 32, accumulation 1, norm clipping 1.0.
- Ten epochs, 137 optimizer steps per epoch, 1,370 total; no early stopping or additional run. Every epoch checkpoint retained.
- CPU AMD EPYC 9V74, 9 visible logical CPUs, 4 torch threads; torch 2.4.1+cpu, transformers 4.44.2; all installed versions in training-manifest.json.
- Optimization plus checkpoint writes: 24.637829853 seconds. Including frozen feature preparation: 35.160938859 seconds. Download, initial model loading, packaging and publication are outside these duration figures.

Execution details were fixed before optimizer use in `tools/student5_fp32/train_cp47_config.json`. No runnable numerical Student-5 recipe was registered; this implements the existing stage-A plan with explicit parameters, without importing Student-4 loss weights. A frozen feature cache preserves the original head algebra. Its final parity error is at most 2.682209014892578e-7 across all real tokens and all sequence outputs. The initial padding-only comparison assertion was corrected before any optimizer step; no weights or targets were changed by that preparation retry.

Six token, five fixed categorical, five role-pointer and one temporal-anchor cross-entropies consume the existing V3 representation. AMBIGUOUS retains primary UNKNOWN; a conditional alternative-set probability term uses the plausible candidates without rank preferences or invented probability targets. Status/alternative tensor checks are persisted in target-consumption.json. Teacher-forced TRAIN claim/mention/temporal spans supply candidate features, as recorded; this is not an end-to-end runtime evaluation.

## Persistent checkpoints

Release **384423046**, archive asset **549780835**: [durable bundle](https://github.com/MATRIXNEO23/matrix-understanding-lab/releases/download/student5-matrix-nlu-v3-fp32-cp47-run1/student5-matrix-nlu-v3-fp32-cp47-run1.tar.xz).

Archive: 93,830,912 bytes; SHA-256 `029bc292c11091da3aa5742ac85017ffdbc7dbb7ba7be6fadc5cc603f07ceafa`. The archive holds complete FP32 weights for all ten checkpoints. Lossless compression shares repeated encoder bytes; no quantization occurred. Shared config/tokenizer/vocabulary/remap, architecture/source, optimizer/RNG states, manifests, metrics, checksums and recovery instructions are included.

| Checkpoint ID | Epoch / step | TRAIN mean batch loss | FP32 model SHA-256 |
|---|---:|---:|---|
| `student5-matrix-nlu-v3-fp32-cp47-run1-epoch-01` | 1 / 137 | 18.907279 | `dcf03bca3ead7bbd43573c9fddc20ef8c954132bb089625de969d35fa5609035` |
| `student5-matrix-nlu-v3-fp32-cp47-run1-epoch-02` | 2 / 274 | 7.447614 | `71e5b7558cb778db7c3eb40418e88c815745dea34144b1dbad9598f9fe10a265` |
| `student5-matrix-nlu-v3-fp32-cp47-run1-epoch-03` | 3 / 411 | 5.883487 | `45c1109e9258d53679f853622d19370f794d5ce274c47e44e4dd89261e50eb49` |
| `student5-matrix-nlu-v3-fp32-cp47-run1-epoch-04` | 4 / 548 | 5.516301 | `3c0f0fdfb64972c1f921508b2fdb25abde5871cbcc13725b0af0323bca7e1b1b` |
| `student5-matrix-nlu-v3-fp32-cp47-run1-epoch-05` | 5 / 685 | 5.223078 | `3f2e656832a435082ad7ac0e53ba401dd35237eb553fad5123a22a371d09a328` |
| `student5-matrix-nlu-v3-fp32-cp47-run1-epoch-06` | 6 / 822 | 5.100230 | `7b7f670bc265e6e1e11fb76c87875494e2d7325dbc45a0993dad413bbda6ead9` |
| `student5-matrix-nlu-v3-fp32-cp47-run1-epoch-07` | 7 / 959 | 5.021640 | `ee45bb926bd26f7278fc6c2cac02173774d3106dd4258a33c7cc826d4ab16663` |
| `student5-matrix-nlu-v3-fp32-cp47-run1-epoch-08` | 8 / 1096 | 4.947185 | `1e5cb002dfc770a45e01aca5c89578acc851d39dbcec2e305828d3bfffde2f20` |
| `student5-matrix-nlu-v3-fp32-cp47-run1-epoch-09` | 9 / 1233 | 4.951446 | `89956185f8ba446a0178ff231b65de3cc9f4cb3410ddb28a088bb488aca9e990` |
| `student5-matrix-nlu-v3-fp32-cp47-run1-epoch-10` | 10 / 1370 | 4.855911 | `f19920de1f6224f37fde056e6b2e423ff4905b215409684a53a5295a1a0ddc6d` |

Each model is 148,713,360 bytes. Exact per-checkpoint archive paths, common durable locator, Release and asset IDs are in `evidence/student5-fp32-cp47/checkpoint-locations.json`. Full per-head loss histories and supervision counts are in training-metrics.json.

## Verification and interpretation

Ten strict full-state loads passed; all checkpoint tensors are finite FP32 and every encoder tensor is byte-identical to recovered CP45. Tensor-only candidate permutation checks passed. The 28 relevant builder/G03/inference/evaluator unit regressions passed; these tests are software checks, not linguistic quality evaluation.

Remote readback: download all six Release assets into a separate directory, verify published size/SHA, extract the archive, verify all 58 internal checksum entries and all ten complete checkpoint hashes. Executed results are in remote-readback.json. The recovered model loading path is checked separately before final closure. Repository readback is likewise verified before the final handoff.

Training mean batch loss decreased from 18.907279 to 4.855911. This is TRAIN fit only. No checkpoint is selected by this decrease, no DEV is replaced, and no evaluation result or practical competitiveness is inferred. Per-language, per-head task accuracy, negation/temporal/referent/status quality and preservation/regression magnitudes remain NOT_EVALUATED. G04 remains pending authorized evaluation. G07 remains the existing evidence limitation; no Frozen data was read.

## Stop and continuity

Training is completed and all ten fixed epoch boundaries remain eligible for authorized selection. The only pending decision is checkpoint selection/evaluation against identifiable authorized material; this did not block or discard training. No automatic additional training round, data repair, quantization, ONNX or Engine integration follows.

```text
INVALID_LOCAL_COPY_REMOVED = true (quarantined)
CP45_RECOVERY = PASS
TRAINING_STARTED = true
TRAINING_COMPLETED = true
CHECKPOINTS_CREATED = 10
CHECKPOINTS_PERSISTED = 10
sourcePristineModified=false
workingCopyInitialSnapshotModified=false
trainModified=false
quantizationExecuted=false
onnxExecuted=false
assemblingIntegrationExecuted=false
student4Modified=false
frozenUsedForTraining=false
nextWorkStarted=false
```
