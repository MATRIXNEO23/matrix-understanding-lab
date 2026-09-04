# Matrix-NLU Model Acceptance Tiers

Last updated: 2026-09-04T16:35+02:00
Repository: `MATRIXNEO23/matrix-understanding-lab`
Schema: `matrix.nlu.acceptance-tiers.v2`

## Purpose

Matrix-NLU must not be evaluated with only two states: `perfect` or `rejected`.

The project needs an intermediate operational standard because practical runtime testing can be valuable before a model is technically approved for production.

This document defines separate acceptance tiers so that:

- high production standards remain intact;
- imperfect models can still be tested under controlled conditions;
- failed canonical gates are not rewritten as success;
- owner-authorized experiments are allowed without contaminating frozen evaluation;
- memory and persistent affect remain protected by deterministic controllers.

## Core rule

```text
Lowering an operational tier does not change the measured model quality.
It only changes what kind of controlled use is allowed.
```

## Canonical Training / Repair Protocol

The following rules are canonical for all future Matrix-NLU training, repair, evaluation and quantization cycles.

### 1. Do not lower gates

```text
DO NOT LOWER ACCEPTANCE GATES TO MAKE A MODEL PASS.
```

Do not modify acceptance thresholds, canonical dev requirements or frozen criteria merely to convert a failing result into a passing result.

If a model does not meet the canonical gate, preserve the measured failure and either:

- perform targeted repair;
- classify it in the appropriate R0/R1/R2 tier;
- or stop the experiment.

Operational tiering and owner authorization never rewrite measured metrics.

### 2. Fix infrastructure before judging the model

Infrastructure failures must be resolved before interpreting a run as a model-quality result.

Examples include:

- Python import errors;
- incorrect `PYTHONPATH`;
- incorrect package/module invocation;
- missing dependencies;
- runner failures;
- artifact download/upload failures;
- broken evaluation entry points.

Preferred fixes include correcting `PYTHONPATH`, package layout, or launching the evaluator as a Python module when appropriate.

A run that never executes a valid evaluation must be classified as an infrastructure failure, not as a model failure.

### 3. Perform targeted error analysis before retraining

When a gate or fragile semantic family fails, inspect the residual errors before starting another training cycle.

For example, when `predicate`, `negation`, referents, ownership, correction, temporal or another critical head fails on `p05Dev` or Matrix dev:

1. isolate the failing examples;
2. classify the failure mode;
3. determine whether the error originates in data, labels, span decoding, loss weighting, model capacity or downstream decoding;
4. add or rebalance TRAIN-ONLY examples specifically covering those edge cases;
5. preserve dev and frozen unchanged;
6. rerun the same canonical evaluation for direct comparison.

Do not use blind dataset growth as a substitute for error analysis.

### 4. Use targeted mixed-precision quantization

When quantization is required, prefer:

```text
Mixed / Head-Protected INT8
```

Quantize the encoder/backbone where practical while protecting the Matrix semantic heads that are fragile or directly affect interpretation, authority and memory safety.

Protected heads:

```text
token.boundary
token.object
token.subject
token.negation
token.temporal
token.entity
sequence.dialogueAct
sequence.predicate
sequence.subjectReferent
sequence.targetReferent
sequence.ownerReferent
sequence.perspectiveReferent
sequence.polarity
sequence.temporalRelation
sequence.claimKind
```

MASSIVE auxiliary heads do not require the same protection unless a future measured regression justifies it.

### 5. Quantization must be compared against FP32

Never accept a quantized artifact solely because export succeeded.

For every quantized candidate:

- retain an FP32 ONNX reference;
- run parity checks on representative IT/EN/ES probes;
- compare fragile-head predictions and metrics against FP32;
- record size, latency and checksums;
- reject or revise quantization if critical semantic heads materially degrade.

The quantized artifact must not silently trade away negation, predicate, referent, ownership, polarity, temporal or claim classification quality merely to reduce model size.

### 6. Canonical repair loop

```text
INFRASTRUCTURE VALID
→ TRAIN
→ CANONICAL DEV EVALUATION
→ TARGETED ERROR ANALYSIS
→ TRAIN-ONLY REPAIR
→ RE-EVALUATION WITH UNCHANGED GATES
→ FP32 EXPORT
→ MIXED / HEAD-PROTECTED QUANTIZATION
→ FP32 VS QUANTIZED PARITY
→ ACCEPTANCE TIER DECISION
→ FROZEN ONLY WHEN AUTHORIZED BY THE APPLICABLE GATE
```

Frozen data must never be used as repair or debugging material.

## Tier R0 — Research Baseline

Status label:

```text
RESEARCH_BASELINE
STOPPED_FOR_REVIEW
NOT_RUNTIME_APPROVED
```

Allowed:

- inspect metrics;
- compare against previous runs;
- preserve artifacts;
- use for error analysis;
- design the next repair.

Not allowed:

- app runtime integration;
- memory admission;
- persistent affect updates;
- frozen evaluation as debugging material;
- production claims.

Use when:

- training failed;
- dev metrics are too weak for practical runtime tests;
- artifacts are incomplete;
- source provenance is unclear.

## Tier R1 — Experimental Artifact Candidate

Status label:

```text
EXPERIMENTAL_ARTIFACT_CANDIDATE
NOT_PRODUCTION_APPROVED
FROZEN_UNREAD
```

Allowed:

- export ONNX;
- produce FP32 reference artifact;
- produce INT8 or mixed/head-protected quantized artifact;
- run parity, size and latency checks;
- test locally with fixed probe sentences.

Not allowed:

- autonomous memory writes;
- autonomous authority decisions;
- persistent affect deltas;
- gameplay integration without visible experimental label;
- production claims.

Minimum conditions:

- software regression tests pass;
- training completed or a preserved model artifact exists;
- frozen data was not read;
- artifact manifest explicitly marks the model as experimental;
- no dev/frozen data edits.

## Tier R2 — Controlled Runtime Candidate

Status label:

```text
OWNER_APPROVED_CONTROLLED_RUNTIME_CANDIDATE
FAILED_CANONICAL_DEV_GATE_CARRY_OVER_ALLOWED
NOT_TECHNICALLY_PRODUCTION_VALIDATED
FROZEN_UNREAD
```

This is the intermediate standard.

It exists for models that are not production-approved but are useful enough for practical app/lab testing behind guards.

Allowed:

- app/lab runtime testing;
- ONNX FP32 runtime checks;
- mixed/head-protected INT8 runtime checks;
- controlled comparison against GGUF behavior;
- user practical evaluation on real prompts;
- integration into `assembling` as an NLU proposal source.

Not allowed:

- claiming canonical dev gate passed;
- claiming production approval;
- reading frozen for debugging;
- direct memory writes;
- direct persistent relationship/emotion mutation;
- using NLU output as final truth.

Mandatory runtime architecture:

```text
NLU proposal
→ Semantic Consistency Controller
→ Authority Resolver
→ Memory Admission
→ Affective Engine
→ Prompt Builder
→ GGUF
```

Mandatory controller behavior:

```text
if negation/polarity/referent/owner confidence is weak → transient only
if target is not explicitly present or context-bound → do not invent Luna as target
if dialogueAct is QUESTION or REQUEST → no stable memory
if source is THIRD_PARTY_REPORT → not world truth
if owner/perspective is unresolved → no stable memory
if model confidence is high but heads conflict → abstain/hold
```

Suggested minimum metrics for R2:

```text
workflow success = true
software tests = pass
frozenDataRead = false
worldTruthUpdates = 0
Matrix exactClaimSet >= 0.65
P0.5 exactClaimSet >= 0.50
validCoverage >= 0.90
no uncontrolled production export
```

Known tolerated weaknesses at R2:

- negation/polarity weakness is tolerated only if controller blocks stable memory;
- ownership corruption is tolerated only if controller blocks stable memory and persistent affect;
- request/correction/third-party weakness is tolerated only if output is treated as proposal, not truth.

R2 does not require perfection.

R2 requires containment.

## Tier R3 — Production Candidate

Status label:

```text
DEV_GATE_PASSED_AWAITING_FROZEN_AUTHORIZATION
NOT_YET_PRODUCTION_APPROVED
```

Allowed:

- request owner authorization for frozen evaluation;
- prepare production package candidate;
- perform stricter parity/quantization checks;
- prepare integration plan.

Not allowed:

- production deployment before frozen pass;
- treating dev pass alone as final approval.

Minimum conditions:

- canonical dev gate passes unchanged;
- `selectedThreshold != null`;
- ownership corruption is zero or explicitly accepted by a stricter controller policy;
- critical-family regressions are absent or documented;
- frozen is still unread before owner authorization.

## Tier R4 — Production Approved

Status label:

```text
APPROVED_FOR_PRODUCTION
```

Allowed:

- stable integration as production NLU component;
- production packaging;
- controlled memory admission, still through Authority and MemoryAdmission;
- persistent affect signals, still gated by memory admission.

Required:

- canonical dev gate passed;
- frozen evaluation authorized and passed;
- final artifact manifest complete;
- owner explicitly approves production use;
- rollback path exists.

## Applying the tier system to Student-4-v2.2A

Student-4-v2.2A measured state:

```text
workflow = success
training = success
dev evaluation = success
canonical dev gate = failed
selectedThreshold = null
frozenDataRead = false
frozenEvaluationExecuted = false
onnxExported in original run = false
quantizationExecuted in original run = false
```

Therefore:

```text
Production tier: NOT R3 / NOT R4
Intermediate tier: eligible for R2 only by explicit owner authorization
Artifact tier: eligible for R1/R2 export and mixed/head-protected quantization
```

Student-4-v2.2A must be labeled:

```text
OWNER_APPROVED_CONTROLLED_RUNTIME_CANDIDATE
FAILED_CANONICAL_DEV_GATE_CARRY_OVER_ALLOWED
FROZEN_UNREAD
NOT_TECHNICALLY_PRODUCTION_VALIDATED
```

## Owner override rule

The owner may authorize R2 even when the canonical dev gate fails.

This does not alter the canonical metrics.

It only permits controlled runtime testing under mandatory guards.

## Quantization rule for R2

For R2, preferred quantization is:

```text
Mixed / Head-Protected INT8
```

Quantize:

```text
encoder / backbone
```

Protect:

```text
token.boundary
token.object
token.subject
token.negation
token.temporal
token.entity
sequence.dialogueAct
sequence.predicate
sequence.subjectReferent
sequence.targetReferent
sequence.ownerReferent
sequence.perspectiveReferent
sequence.polarity
sequence.temporalRelation
sequence.claimKind
```

The artifact manifest must include:

```text
acceptanceTier = R2
productionApproved = false
frozenDataRead = false
frozenEvaluationExecuted = false
canonicalDevGatePassed = false
ownerRuntimeOverride = true
protectedHeads = [...]
```

## Final principle

```text
Do not chase perfection before practical testing.
Do not pretend practical testing equals production approval.
Do not lower canonical gates to hide a model weakness.
Fix infrastructure first, repair measured errors second, quantize only with FP32 comparison.
```
