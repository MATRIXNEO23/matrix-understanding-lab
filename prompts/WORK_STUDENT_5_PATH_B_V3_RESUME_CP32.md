# WORK RESUME — Student-5 Path B after CP32

Status: OWNER-AUTHORIZED RESUME PACKAGE
Repository: `MATRIXNEO23/matrix-understanding-lab`
Branch: `student5-path-b-v3`
Resume from latest branch HEAD; do not reset to an older checkpoint.

## Read first

1. `PROJECT_WORK_RULES.md`
2. `docs/MODEL_ARTIFACT_PERSISTENCE_POLICY.md`
3. `docs/WORK_CONTINUITY_STUDENT_5.md` including linked archive
4. `prompts/WORK_STUDENT_5_PATH_B_V3_COMPLETION.md`
5. CP32 preflight report/evidence

TASK 2.3 is accepted. Do not repeat it.

## Exact blocker to resolve

CP32 stopped at:

```text
A1_CANONICAL_PRISTINE_BINARY_ACQUISITION
```

The canonical binary is known and still exists:

```text
releaseTag = student-5-minilm-40k-phase-a-pristine
releaseId = 383143636
assetId = 545406840
assetName = student5-minilm-phase-a-pruned-40k.zip
assetBytes = 88361246
archiveSha256 = 7804bfb245b71df9b835fff7ee00f6ec887e019772ae34c82d269d821d587191
modelBytes = 148020400
modelSha256 = d6e45891d1e0ec4ed023caaeb17c0dd0ae80a93b8bf877d275310b7f2837efa2
releasePage = https://github.com/MATRIXNEO23/matrix-understanding-lab/releases/tag/student-5-minilm-40k-phase-a-pristine
```

Authenticated metadata access already proved the asset exists. The prior Work runtime failed because its connector could read Release metadata but not private binary bytes.

## Required recovery route

Use the authenticated **Work Cloud Browser / logged-in GitHub UI** to open the release page and download the private Release asset into the Work machine. Do not ask the owner to download/re-upload it manually.

If the Work browser session is not authenticated, use the normal Work/plugin connection flow available to that environment. Do not extract/reuse connector credentials manually and do not bypass access controls.

After acquisition, fail closed unless all of these pass:

```text
archive file exists locally
bytes = 88361246
SHA-256 = 7804bfb245b71df9b835fff7ee00f6ec887e019772ae34c82d269d821d587191
ZIP integrity PASS
internal SHA256SUMS PASS
model bytes = 148020400
model SHA-256 = d6e45891d1e0ec4ed023caaeb17c0dd0ae80a93b8bf877d275310b7f2837efa2
tokenizer/mapping/manifest identities match registry/continuity
```

The downloaded copy is an execution copy only. The canonical persistent source remains the existing Release asset. Do not modify or replace that Release.

## Continue automatically after A1 PASS

Once A1 identity is proven, continue the already-authorized completion package:

```text
A2 real pristine BERT/tokenizer load + V3 16-head construction + real forward
A3 physical ONNX export/check/load/forward + tensor/shape/fingerprint/parity evidence
A4 persist any retained Gate-A output under a NEW immutable identity
then Gate-B readiness and TASK 3 Path-B training according to WORK_STUDENT_5_PATH_B_V3_COMPLETION.md
```

Do not stop for owner re-authorization at the historical TASK 2.4 boundary; owner has already authorized continuation. Stop only on a genuine package-defined blocker.

## Non-overwrite / persistence

Never overwrite or mutate:

```text
Student-5 pristine Release
Student-5 Path A
Student-4
TRAIN V3 v1
prior Path-B candidates/checkpoints
prior FP32/INT8 exports
```

Every meaningful new candidate gets unique ID/name/SHA-256/provenance and persistent repository-owned storage.

## Continuity rule strengthened after CP32

Before any future checkpoint is called ready for the next task, verify that every required binary has a machine-actionable locator and acquisition route usable by the intended executor. Record locator, auth mode, bytes, SHA-256, last successful recovery proof and exact resume action.

## First Work update

Report immediately after pickup:

```text
branch
HEAD
CP32 read = true
active operation = A1 authenticated pristine acquisition
acquisition route actually used
whether asset bytes were obtained
```

Do not claim Gate A PASS until physical model/ONNX evidence exists.
