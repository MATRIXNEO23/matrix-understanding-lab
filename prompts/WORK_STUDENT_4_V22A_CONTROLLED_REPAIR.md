# WORK PROMPT — Student-4-v2.2A Controlled Repair

Repo: `MATRIXNEO23/matrix-understanding-lab`
Branch: `main`
Date: 2026-09-04

## Objective

Complete Student-4-v2.2A controlled repair using the final repair mix recorded in:

`docs/STUDENT_4_V22A_FINAL_REPAIR_MIX.md`

This is a targeted train-only repair cycle intended to fix Student-4-v2.1 dev failures without lowering gates and without touching frozen.

## Baseline

Student-4-v2.1 final state:

- Decision: `STOPPED_FOR_REVIEW`
- Dev gate: `FAILED_GATE`
- Selected threshold: `null`
- Do not quantize v2.1.
- Do not export ONNX v2.1.
- Do not promote v2.1.

Source evidence:

- Final dev-only run: `33848931720`
- Artifact: `9927657001`
- Artifact digest: `sha256:2314694e5b45f6a95ba409808394013d3a43f92f6d798765fc5cdb01ff3fcb41`
- Report: `reports/STUDENT_4_V21_POST_DEV_REPORT.md`

## Mandatory constraints

1. Do not lower gates.
2. Do not modify dev.
3. Do not read or modify frozen.
4. Do not export ONNX unless dev gate passes.
5. Do not quantize unless dev gate passes and ONNX FP32 is validated.
6. Do not promote to production automatically.
7. All new augmentation must be TRAIN-ONLY.
8. Preserve strong capacities from v2.1.
9. Adult/intimacy examples must be semantic robustness examples, not safety/moderation/censorship examples.
10. Unknown adult/intimate terms must not become hard errors, censorship labels or stable memory facts.

## Final repair mix

Create exactly 375 new train-only repair examples:

| Block | Examples |
|---|---:|
| IT core | 139 |
| ES core | 70 |
| EN core | 69 |
| Adult/intimacy IT | 60 |
| Cross-lingual contrast | 37 |
| Total | 375 |

## Internal allocation

### IT core — 139

- Negation: 63
- Predicate: 28
- Ownership/referents: 22
- Question/request/correction/report: 15
- Span/temporal: 11

### ES core — 70

- Negation: 46
- Predicate: 16
- Referents/span: 6
- Question/request: 2

### EN core — 69

- Predicate: 38
- Claim structure / multi-claim: 12
- DialogueAct/correction: 10
- Negation: 7
- Span/temporal: 2

### Adult/intimacy IT — 60

- Desire/assert: 15
- Request: 15
- Consent: 11
- Refusal/boundary: 8
- Common English terms inside Italian sentences: 11

Important adult/intimacy rules:

- Use censored or neutral authored surfaces where appropriate.
- Do not import raw public adult datasets.
- Do not use moderation labels such as unsafe/block/censor.
- Map to existing Matrix labels only: `ASSERT`, `REQUEST`, `QUESTION`, `goal.object`, `consent.grant`, `consent.refuse`, `speech.unresolved`, `POSITIVE`, `NEGATIVE`.
- If semantics are intentionally unknown, use `speech.unresolved`, not error/block.
- These rows are for NLU robustness only.

### Cross-lingual contrast — 37

- Negation triplets/pairs: 15
- Predicate triplets/pairs: 10
- Question/request contrast: 6
- Correction/ownership contrast: 6

## Required implementation work

1. Fix the current v2.2A pre-training audit failure before starting real training.
   - The previous run `33855798760` stopped before training at `Audit v2.2A dataset before training`.
   - Treat it as dataset/audit contract failure, not model failure.

2. Update or replace the v2.2A repair dataset builder so it produces the final 375-example mix.
   - Preserve immutable v2 dev/test content and hashes.
   - Repair examples must be train-only.
   - Mapping/provenance must explicitly state train-only augmentation.
   - Record block counts and internal target counts.

3. Adjust the v2.2A audit contract.
   - It must still fail closed on schema, checksums, leakage, malformed spans, unknown labels, worldTruth, unknown authority, and dev/frozen mutation.
   - It must allow the intentional train-only language distribution: IT core 139, ES core 70, EN core 69, Adult IT 60, Cross 37.
   - It must not require ordinary train language balance for the v2.2A repair rows.
   - It must verify dev/test are unchanged and frozen predictions are not read.

4. Keep model architecture unchanged unless there is explicit evidence after this run that capacity is required.
   - Same 4-layer Student architecture for v2.2A.
   - No ONNX, no INT8, no mixed quantization during this run.

5. Training configuration.
   - Variant must be `student-4-v2.2A`.
   - Dataset version evidence must identify base `matrix.nlu.dataset.v2` plus v2.2A train-only repair overlay.
   - Use defer-frozen mode.
   - Keep gate thresholds unchanged.

6. Run controlled training and dev-only evaluation.
   - Software regression tests first.
   - Build v2.2A train-only repair dataset.
   - Audit v2.2A dataset.
   - Prepare MASSIVE train/dev with test-per-language 0.
   - Train fresh Student-4-v2.2A.
   - Evaluate dev-only and stop.
   - Upload report, bundle and preservation checkpoint artifacts.

7. Required post-run report.
   Create `reports/STUDENT_4_V22A_CONTROLLED_REPAIR_REPORT.md` with:
   - final decision;
   - run id, job id, commit, artifacts, checksums;
   - comparison against Student-4-v2.1;
   - per-language Matrix and P0.5 metrics;
   - IT Matrix negation F1;
   - ES Matrix negation F1;
   - EN/IT/ES P0.5 predicate;
   - exact-set and claim-exact deltas;
   - ownership corruption;
   - World Truth updates;
   - adult/intimacy robustness notes;
   - whether dev gate passed;
   - explicit quantization decision: allowed only if dev passed, otherwise blocked.

8. Update `docs/WORK_CONTINUITY.md`.
   Include:
   - HEAD/branch;
   - active objective;
   - final mix document;
   - latest run id/job id;
   - artifacts/checksums;
   - gate status;
   - exact next step.

## Stop policy

Stop and do not continue to ONNX/quantization/frozen if any of these occur:

- dataset audit fails;
- dev gate fails;
- ownership corruption > 0;
- World Truth updates > 0;
- IT or ES negation remains unsafe;
- P0.5 predicate remains unsafe;
- exact-set/claim-exact fail to improve enough;
- adult/intimacy rows introduce censorship-like labels or false hard errors;
- provenance cannot prove train/dev-only and frozen closed.

## Expected final state

Either:

`DEV_GATE_PASSED_AWAITING_FROZEN_AUTHORIZATION`

or:

`STOPPED_FOR_REVIEW`

In both cases, preserve evidence. Do not automatically proceed to frozen, ONNX, INT8/mixed quantization, Android integration or production promotion.
