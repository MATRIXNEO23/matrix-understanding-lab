# Owner Override — Student-4-v2.2A

Last updated: 2026-09-04T15:39+02:00
Repository: `MATRIXNEO23/matrix-understanding-lab`
Variant: `student-4-v2.2a`

## User authorization

The project owner explicitly authorized continuing with the v2.2A artifact and revoked the previous blanket order that blocked quantization after the failed dev gate.

User instruction:

```text
io lo autorizzo e revoco l'ordine
```

## Scope of the override

This override authorizes:

```text
EXPERIMENTAL_TEST_CANDIDATE packaging
ONNX FP32 export for reference
Mixed / Head-Protected INT8 quantization
external/practical testing by the project owner
integration-lab evaluation with the semantic controller gate
```

This override revokes only the previous operational prohibition:

```text
DO_NOT_QUANTIZE unless dev gate passes
```

## Non-overridden facts

This override does not change the measured technical result:

```text
Student-4-v2.2A decision = STOPPED_FOR_REVIEW
selectionStatus = FAILED_GATE
selectedThreshold = null
frozenDataRead = false
frozenEvaluationExecuted = false
```

The model remains technically below the unchanged approval gate.

## Production status language

Allowed label:

```text
OWNER_AUTHORIZED_EXPERIMENTAL_TEST_CANDIDATE
NOT_TECHNICALLY_GATE_APPROVED
FAILED_DEV_GATE_CARRY_OVER
FROZEN_UNREAD
```

Do not label as:

```text
TECHNICALLY_APPROVED_FOR_PRODUCTION
PASSED_DEV_GATE
PASSED_FROZEN
CANONICAL_PRODUCTION_MODEL
```

unless a future run actually satisfies the required gates or the owner explicitly creates a separate production-risk override document.

## Required safety around Matrix memory

Even with owner authorization, the model must not directly write memory or persistent affect.

Required runtime architecture:

```text
NLU Proposal
→ Semantic Consistency Controller / Coherence Guard
→ Authority Resolver
→ Memory Admission
→ MemoryRepository
```

Allowed use:

```text
NLU proposes interpretation.
Controller verifies negation, referents, polarity, confidence and target/owner consistency.
Authority decides source/truth/report/hypothesis/correction.
MemoryAdmission saves only if safe.
```

Forbidden use:

```text
NLU writes memory directly.
GGUF writes memory directly.
Affective Engine writes persistent relationship state from unadmitted claims.
Failed-gate v2.2A is treated as technically gate-passed.
```

## Quantization direction

Proceed with:

```text
Mixed / Head-Protected INT8
```

Preferred protection rule:

```text
Quantize encoder/backbone where possible.
Keep Matrix semantic heads FP32 when possible.
```

Heads to protect:

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

## Next Work task

Fix the failed experimental mixed quantization workflow and produce an artifact without touching frozen or retraining.

Known failed workflow:

```text
Workflow: Matrix-NLU Student-4 V2.2A Experimental Mixed Quantization
Run: 33882172879
Commit: 2d4efa2f9abd390175daedab6810b59ef52413d5
```

Expected output artifact:

```text
matrix-nlu-student-4-v22a-mixed-head-protected-<run_id>
```

Required manifest fields:

```text
productionStatus = OWNER_AUTHORIZED_EXPERIMENTAL_TEST_CANDIDATE_NOT_TECHNICALLY_GATE_APPROVED
failedDevGateCarryOver = true
frozenDataRead = false
frozenEvaluationExecuted = false
fp32OnnxSha256
mixedInt8OnnxSha256
protectedHeads
excludedQuantizationNodes
parityFp32VsMixed
latencyCpu
```
