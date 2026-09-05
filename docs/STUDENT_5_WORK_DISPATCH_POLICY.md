# Student-5 Work Dispatch Policy

Date: `2026-09-05`
Status: `CANONICAL_EXECUTION_CONTROL`
Repository: `MATRIXNEO23/matrix-understanding-lab`

## Purpose

This document controls how the already-approved Student-5 completion plan is dispatched to Work.

The full technical plan remains recorded in `docs/WORK_CONTINUITY_STUDENT_5.md` and is supported by:

- `ARCHITETTURA.md`
- `docs/FINAL_MATRIX_UNDERSTANDING_ARCHITECTURE.md`
- `docs/ADULT_INTIMACY_NLU_COVERAGE.md`
- `reports/STUDENT_5_MINILM_40K_QUALITY_ANALYSIS.md`
- `reports/STUDENT_5_MINILM_DEEP_PRUNING.md`
- `docs/STUDENT_ARTIFACT_REGISTRY.md`

This file does not replace those documents. It only defines the owner-approved execution discipline.

## Hard execution rule — one Work task at a time

```text
workDispatchMode = ONE_TASK_AT_A_TIME
automaticContinuationToNextStage = FORBIDDEN
multiStagePromptExecution = FORBIDDEN
```

Work must receive only one bounded checkpoint/task at a time.

Each Work instruction must:

1. name exactly one active task/checkpoint;
2. define allowed files/operations for that task;
3. preserve all other Student-5 stages as NOT AUTHORIZED YET;
4. stop after completing, testing, reporting and checkpointing that task;
5. update `docs/WORK_CONTINUITY_STUDENT_5.md` before stopping;
6. return evidence/results for owner review before the next task is issued.

Work must never infer authorization for the next stage merely because the current stage succeeds.

## Repository boundary

Only this repository may be modified:

```text
MATRIXNEO23/matrix-understanding-lab
```

Other repositories are read-only context and must not be modified.

In particular, do not modify `assembling`, `memoria`, affective/game repositories, or historical repositories.

## Student isolation

```text
activeStudent = Student-5-MiniLM-40k
Student-4-v2.2A = PRESERVED_COMPARATIVE_BASELINE
crossStudentMutation = FORBIDDEN
```

Student-4 may be read for comparison only. It must not be retrained, re-quantized, repaired, overwritten, or promoted while Student-5 is active.

## Adult / intimacy requirement

Adult/intimacy is a first-class NLU quality family throughout Student-5 work.

Do not remove or marginalize coverage of:

- desire/arousal/attraction;
- explicit adult sexual language;
- requests/questions/assertions/corrections;
- consent, refusal, withdrawal and boundaries;
- adult consensual role/power language;
- negation and temporal distinctions;
- third-party/report semantics;
- subject/target/owner/perspective;
- IT/EN/ES slang and code-switch;
- ambiguity;
- coercion/non-consent distinguished from consensual intimacy.

Adult/intimacy must remain semantic NLU coverage, not a censorship/moderation classifier. Authored sexual material must involve adults only.

## Frozen guard

Frozen remains unread until a separately authorized final candidate-lock task.

```text
frozenDataRead = false
frozenDataTokenized = false
frozenDataAnalyzed = false
frozenPredictionsRead = false
frozenDataUsedForTuning = false
```

No individual Work task before candidate lock may weaken this rule.

## Approved global sequence

The owner-approved global sequence is preserved as follows, but only ONE numbered item may be dispatched to Work at a time.

### TASK 0 — preserve/recover pristine Student-5 40k binary

Current artifact registry reports:

```text
remoteBinaryLocator = NOT_RECORDED
binaryPreservation = NOT_YET_DURABLY_VERIFIED
```

Before quantization or teaching, recover the exact pristine Student-5 40k artifact if it still exists, or deterministically regenerate it from the pinned source only if required.

Acceptance requires exact recorded identity/checksums, including:

```text
selectedVocabSize = 40000
modelSha256 = d6e45891d1e0ec4ed023caaeb17c0dd0ae80a93b8bf877d275310b7f2837efa2
archiveSha256 = 7804bfb245b71df9b835fff7ee00f6ec887e019772ae34c82d269d821d587191
```

Record a durable remote locator inside `matrix-understanding-lab` or another owner-authorized durable location without modifying other repositories.

If exact identity cannot be reproduced, STOP with evidence. Do not silently substitute a different backbone.

### TASK 1 — Path A: untaught ONNX/INT8 runtime probe

Only after TASK 0 is verified.

```text
STUDENT_5_40K_UNTAUGHT_INT8
RUNTIME_PROBE_ONLY
NOT_MATRIX_NLU
NOT_PRODUCTION_APPROVED
```

Purpose: isolate ONNX/quantization/runtime risk before Matrix teaching.

Must not mutate the pristine FP32 artifact and must not become Path-B training input.

### TASK 2 — audit the existing 15-head Matrix contract

Only after Path A is checkpointed.

Verify the current 15 heads and their labels/contracts against the canonical repository documents.

Do not change the contract during this task. If a contract change appears necessary, stop with `ARCHITECTURAL_CONTRACT_CHANGE_REQUIRED`.

### TASK 3 — B0 head-learnability probe

Return to the pristine FP32 40k artifact.

Train the existing Matrix heads with the 12-layer backbone frozen.

Purpose: measure how much Matrix semantics is already decodable without encoder adaptation.

### TASK 4 — B0 evaluation and causal error taxonomy

Evaluate canonical DEV only for permitted development purposes.

Report per-language and per-family results, including adult/intimacy, and compare with Student-4-v2.2A.

No repair/training changes are authorized inside the same task unless explicitly included in a later owner instruction.

### TASK 5+ — controlled TRAIN-only repair and capacity escalation

Dispatch each repair/escalation as its own bounded task.

Allowed escalation order remains:

```text
frozen backbone + heads
→ bounded stronger heads/adapters if justified
→ unfreeze last 1–2 layers if justified
→ unfreeze last 3–4 layers if justified
→ full fine-tuning only as last resort
```

Do not skip directly to full fine-tuning.

Every step must preserve strengths, compare regressions and use TRAIN-only repairs.

### LATE TASK — candidate FP32 lock

Only after all DEV/capability gates are satisfied and no critical systematic family failure remains.

Lock configuration, dataset, thresholds and checksum before any Frozen access.

### LATE TASK — taught-model quantization/parity

Quantize only the locked/approved taught FP32 candidate, preserving critical heads in FP32 by default unless evidence supports otherwise.

### FINAL TASK — Frozen evaluation

This must be separately authorized.

Frozen is one-way evidence. Its result must not be used to tune or retrain the same candidate cycle.

### SEPARATE FUTURE TASK — Moto / Assembling integration

Not part of this dispatch plan unless separately authorized by the owner.

## Per-task stop requirement

At the end of every dispatched task, Work must STOP even if the next step seems obvious.

Required final state:

```text
currentTask = COMPLETE or BLOCKED
nextTask = NOT_STARTED
otherRepositoriesModified = false
Student-4Changed = false
FrozenRead = false
productionPromotionExecuted = false
```

A new owner prompt is required before `nextTask` may begin.

## No auto-promotion

Work may produce experimental/research/candidate statuses but may not declare `PRODUCTION_APPROVED` autonomously.

## Continuity requirement

`docs/WORK_CONTINUITY_STUDENT_5.md` remains the canonical state/history file and must be updated after every dispatched task with:

- current HEAD/branch;
- exact task executed;
- artifact input/output identities;
- tests/metrics;
- adult/intimacy status;
- Frozen status;
- Student-4 unchanged proof;
- blockers/risks;
- exact next task, marked `NOT_STARTED / OWNER_AUTHORIZATION_REQUIRED`.
