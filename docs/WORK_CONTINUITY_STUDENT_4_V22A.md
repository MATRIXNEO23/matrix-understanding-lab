# Work continuity addendum — Student-4-v2.2A Controlled Repair

Last updated: 2026-09-04T10:56:00+02:00  
Repository: `MATRIXNEO23/matrix-understanding-lab`  
Branch: `main`

## Current objective

Close the NLU repair loop after Student-4-v2.1 failed the unchanged dev gate. The next experiment is `student-4-v2.2a`, a targeted train/dev-only repair.

## Baseline

Student-4-v2.1 is closed as:

- `STOPPED_FOR_REVIEW`
- `FAILED_DEV_GATE`
- `DO_NOT_QUANTIZE`
- `DO_NOT_EXPORT_ONNX`
- `DO_NOT_TOUCH_FROZEN`
- `DO_NOT_PROMOTE`

Important v2.1 failure signals:

- Matrix exact-set `0.719577`
- Matrix negation F1 `0.509169`
- P0.5 exact-set `0.45`
- P0.5 predicate `0.75`
- Ownership corruption `2`, both Italian
- Residuals: span decoding `269`, semantic classification `99`, entity resolution `40`, authority/referent decoding `20`

## Repair hypothesis

Most exact-set / claim-exact degradation is expected to be downstream of:

1. negation failure, especially IT/ES Matrix;
2. predicate failure, especially P0.5 IT/EN/ES;
3. span decoding errors;
4. Italian ownership/referent corruption.

## Implemented files

- `matrix_nlu/build_dataset_v22a.py`
  - calls immutable v2 builder first;
  - appends only project-authored TRAIN rows;
  - keeps dev/frozen partitions unchanged;
  - repair rows are language-balanced so existing audit remains valid;
  - targets IT/ES negation, EN/IT/ES predicate, ownership, question/request separation.
- `matrix_nlu/train_v22a.py`
  - wrapper around existing `train.py`;
  - patches only `loss_for`;
  - supports config-driven head loss weights;
  - does not change model architecture.
- `matrix_nlu/train_config_v22a.json`
  - variant `student-4-v2.2a`;
  - same 4 retained layers;
  - seed `810924`;
  - LR `2.5e-5`;
  - P0.5 repeat `20`;
  - patience `3`;
  - weighted heads: `tokens.negation`, `sequence.predicate`, `sequence.polarity`, `sequence.ownerReferent`, `sequence.dialogueAct`, span heads.
- `matrix_nlu/controlled_dev_v22a.py`
  - validates variant, 4 layers, train/dev-only provenance, frozen deferred, checksum;
  - evaluates Matrix dev and P0.5 dev only;
  - invokes unchanged threshold selection;
  - records `onnxExported=false` and `quantizationExecuted=false`.
- `.github/workflows/matrix-nlu-student-4-v22a.yml`
  - fresh train/dev-only controlled repair workflow;
  - no frozen, no ONNX, no INT8, no package, no promotion.
- `reports/STUDENT_4_V22A_REPAIR_PLAN.md`
  - design and stop policy.

## Key commits

- `8049c51be310e8281c0a03c09f1b5d1e317c1ed8` — add v2.2A train-only repair dataset builder.
- `775d5299dd720c339d7431ad8e87f2e85b28ad5b` — add weighted v2.2A training wrapper.
- `6d79a6b5e6d9e2d7e8d8a5eea8c7c3fe45ce8f47` — add v2.2A repair training config.
- `e51407b7df6efb0d645f5da7e1ec995dd50667aa` — add v2.2A controlled dev stop.
- `b5b5d140cddc947256550ef070465acfdebe90f5` — add v2.2A controlled repair workflow.
- `7193cce175493edc1e4ec19bdb894f3cda74b2ab` — add v2.2A repair plan.
- `7cb1bee4e89521fbd6215c5c0c1e060f09f7b1ae` — fix v2.2A work-role repair predicates to span roles, not locations.

## Active run

Workflow: `Matrix-NLU Student-4 V2.2A Controlled Repair`  
Run: `33855798760`  
Job: `100968680425`  
Launch commit: `7cb1bee4e89521fbd6215c5c0c1e060f09f7b1ae`  
Status at handoff creation: `in_progress`

## Mandatory stop policy

During/after v2.2A:

- no frozen access;
- no ONNX export;
- no INT8/mixed quantization;
- no Android package;
- no production promotion;
- no gate lowering;
- no dev/frozen edits;
- no blind retrain if v2.2A fails.

If dev gate passes, next state is only:

`DEV_GATE_PASSED_AWAITING_FROZEN_AUTHORIZATION`

If dev gate fails:

`STOPPED_FOR_REVIEW`

## Next exact actions

1. Monitor run `33855798760`.
2. If it fails before training/eval due an infrastructure or dataset-contract issue, inspect the failing step and fix only that issue.
3. If it completes, read artifacts and extract:
   - Matrix/P0.5 exact-set;
   - claim exact;
   - negation F1 by language;
   - predicate by language;
   - span/entity residual counts;
   - ownership corruption;
   - threshold selection status.
4. Compare directly against Student-4-v2.1.
5. Write final report and update canonical continuity.
6. Do not quantize unless dev gate passes unchanged.
