# Model Artifact Persistence Policy

Status: **CANONICAL / OWNER-MANDATED**  
Effective date: 2026-09-07  
Repository: `MATRIXNEO23/matrix-understanding-lab`

## Purpose

Every meaningful model version, training checkpoint selected for comparison, exported runtime, quantized runtime, tokenizer bundle, and release candidate must remain durably recoverable from this repository. Temporary CI/Actions artifacts are transport only and must never be the sole durable copy.

## Non-overwrite rule

Existing versions are immutable.

Forbidden:

```text
overwrite an existing model file in place
reuse an existing version/tag/release name for different bytes
replace Path A with Path B
replace pristine with trained
replace trained FP32 with quantized INT8
replace Student-4 with Student-5
use a generic latest.onnx/latest.zip as the only durable identity
mutate a baseline after it has been registered
```

Every materially different model/checkpoint/runtime must receive a new immutable identity.

## Required persistent storage

For every retained version, the durable bytes must be stored using one of these repository-owned mechanisms:

1. Git-tracked file when safely below ordinary GitHub limits.
2. Git LFS when appropriate and repository storage policy permits it.
3. GitHub Release asset attached to this repository for large binary artifacts.

A GitHub Actions artifact is **not persistent storage** because it expires. If a workflow produces a model worth retaining, that model must be copied/promoted to one of the durable mechanisms above before the task may be reported closed.

## Mandatory registry metadata

Every persistent artifact must have versioned metadata committed in the repository containing at least:

```text
logical artifact ID
student/model family
path: A/B/other
version/checkpoint name
status
source/base artifact ID
training dataset ID + checksum when trained
training run/workflow ID and commit
architecture/contract version
format
quantization policy
byte size
SHA-256
persistent locator
GitHub release tag/ID + asset ID when applicable
created-at/checkpoint commit
parent/predecessor artifact IDs
known limitations
gate/test summary
```

The repository registry and `SHA256SUMS`/manifest are authoritative for identity. Artifact bytes whose SHA-256 does not match the registry must fail closed.

## Mandatory resumability and executable locator

A binary is not operationally preserved merely because it exists somewhere. Every artifact required by later work must have a machine-actionable recovery map in continuity/registry:

```text
primary durable locator
repository
exact release tag / release ID / asset ID OR exact Git/LFS path
filename
expected bytes
expected SHA-256
required authentication/access mode
known working acquisition method for the intended executor/Work
fallback locator or reproduction source when available
last successful recovery checkpoint
```

A sentence such as `saved in a Release` is insufficient.

Before closing a preservation/model-producing checkpoint, prove resumability from a clean execution context whenever technically possible:

```text
LOCATE -> ACQUIRE -> VERIFY BYTES -> VERIFY SHA-256 -> VERIFY MANIFEST/LINEAGE
```

If the intended executor cannot retrieve the artifact with its available authentication/tooling, record and fix that execution-access problem **before** starting the dependent task. Do not postpone discovery until training/export requires the model.

For private GitHub Release assets, continuity must record both exact Release/asset identity and the authenticated acquisition route. Metadata-only access is not a binary acquisition route. When Work has an authenticated Cloud Browser capable of downloading the private Release asset, that route may be used; the downloaded bytes must pass canonical SHA-256 before use.

## Student-5 preservation rules

The following lineages must remain permanently distinguishable:

```text
Student-5 pristine 40k FP32
Student-5 Path A untaught FP32 ONNX
Student-5 Path A untaught INT8 ONNX
Student-5 Path B trained checkpoints
Student-5 Path B trained FP32 export
Student-5 Path B trained quantized exports
Student-4-v2.2A comparative baseline
```

Path B must always start from the registered pristine FP32 lineage or an explicitly registered Path-B predecessor. It must never use the Path-A quantized artifact as a training base.

## Training/checkpoint preservation

Do not persist every transient optimizer step by default. Persist at minimum:

- initial immutable training base;
- each checkpoint that becomes the best candidate for a gate or materially changes architecture/data/training strategy;
- every candidate used for comparison against another version;
- final checkpoint of each training attempt retained for analysis;
- FP32 export used to create a quantized candidate;
- each quantized candidate used in parity/runtime evaluation;
- final promoted candidate.

If storage pressure requires pruning, no registered baseline/candidate may be deleted or replaced without explicit owner authorization.

## Closure gate for Work

A model-producing or preservation task is not closed until all retained outputs satisfy:

```text
persistent bytes exist in repository-owned storage
SHA-256 independently recorded
manifest/registry committed
lineage/base recorded
version name is unique
no previous artifact overwritten
workflow-temporary artifact is not the only copy
continuity records persistent locator and exact next step
machine-actionable acquisition route recorded
resume proof performed or access blocker fixed before dependent work
```

## Current binding decision

Owner instruction on 2026-09-07: all versions must be saved persistently in the repository and must not overwrite earlier versions. Continuity must let a fresh executor locate and recover every required artifact without relying on human memory.

This policy applies to Student-4, Student-5 Path A, Student-5 Path B, and future Matrix-NLU model versions unless the owner explicitly changes it.
