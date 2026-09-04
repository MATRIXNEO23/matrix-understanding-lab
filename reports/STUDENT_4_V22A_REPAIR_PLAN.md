# Student-4-v2.2A Controlled Repair Plan

Status: PREPARED_FOR_TRAIN_DEV_ONLY_RUN  
Baseline: Student-4-v2.1 = STOPPED_FOR_REVIEW / FAILED_DEV_GATE / DO_NOT_QUANTIZE  
Date: 2026-09-04

## Decision

Student-4-v2.2A is a targeted repair run. It is not a production candidate until it passes the unchanged development gate.

The run is allowed to train only on train/dev-visible material and must not read frozen. It must not export ONNX, quantize INT8, package Android, or promote any model.

## v2.1 failure signals being targeted

- Matrix exact-set: 0.719577
- Matrix negation F1: 0.509169
- P0.5 exact-set: 0.45
- P0.5 predicate: 0.75
- Ownership corruption: 2, both Italian
- Residuals: span decoding 269, semantic classification 99, entity resolution 40, authority/referent decoding 20

Working hypothesis: much of exact-set and claim-exact loss is downstream of negation, predicate and span errors.

## Repair strategy

1. Keep the same four-layer student architecture.
2. Add a train-only repair dataset on top of immutable v2.
3. Keep dev and frozen partitions unchanged.
4. Add weighted loss pressure on:
   - `tokens.negation`
   - `sequence.predicate`
   - `sequence.polarity`
   - `sequence.ownerReferent`
   - `sequence.dialogueAct`
   - span heads: boundary/object/subject/temporal/entity
5. Increase P0.5 train repeat from 16 to 20.
6. Use a slightly lower LR and patience 3 to reduce catastrophic forgetting.
7. Stop after unchanged dev gate.

## New files

- `matrix_nlu/build_dataset_v22a.py`
- `matrix_nlu/train_v22a.py`
- `matrix_nlu/train_config_v22a.json`
- `matrix_nlu/controlled_dev_v22a.py`
- `.github/workflows/matrix-nlu-student-4-v22a.yml`

## Dataset policy

`build_dataset_v22a.py` calls the immutable v2 builder first, then appends only project-authored train rows.

The v2.2A repair rows are balanced across IT/EN/ES so the existing v2 audit still applies. The content is targeted differently per language:

- Italian: negation, ownership correction, referents, predicate contrast.
- English: P0.5 predicate and claim-structure repair, plus controlled negation pairs.
- Spanish: negation repair first, then predicate contrast.

No dev text is generated from test/frozen. No frozen predictions are read. No frozen data is used for tuning.

## Controlled stop

`controlled_dev_v22a.py` validates:

- variant = `student-4-v2.2a`
- studentLayers = 4
- trainingSplitsRead = `["train", "dev"]`
- frozenDataRead = false
- frozenEvaluationDeferred = true
- model-state checksum

It then evaluates only Matrix dev and P0.5 dev and runs the existing threshold selector.

## Pass condition

Only the unchanged dev gate can authorize the next step. If it fails, v2.2A remains `STOPPED_FOR_REVIEW`.

If it passes, the only next authorized state is:

`DEV_GATE_PASSED_AWAITING_FROZEN_AUTHORIZATION`

Even then, frozen remains closed until separate explicit authorization.

## Quantization policy

Quantization remains blocked until a model passes dev. Targeted/mixed quantization may be considered only after:

1. dev pass,
2. ONNX FP32 validation,
3. FP32 vs ONNX parity,
4. head-sensitive degradation checks,
5. no regression on negation/predicate/ownership/span.
