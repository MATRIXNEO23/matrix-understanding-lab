# Matrix-NLU Model Acceptance Tiers

Last updated: 2026-09-04T15:40+02:00
Repository: `MATRIXNEO23/matrix-understanding-lab`
Schema: `matrix.nlu.acceptance-tiers.v1`

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

This is the new intermediate standard.

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
```
