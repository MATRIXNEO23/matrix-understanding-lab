# Student-5 pristine FP32 — separate working copy CP45

Working copy created and persistently published. No training executed.

Requested canonical HEAD: `6389e82c255c50964ce2df370a4682ba7206248b`.
Actual starting main HEAD: `2bf43b6ce92436fbab0cb04580fc1f51f0a1fd0a`.
The newer HEAD contains CP44's 4,355 prepared targets; it was preserved.

## Source and new identity

| Field | Source pristine | Separate working copy |
|---|---|---|
| Model ID | student-5-minilm-40k-phase-a-pristine | student-5-minilm-40k-phase-a-fp32-working-copy |
| Version | Original Phase A | CP45_INITIAL_BYTE_IDENTICAL |
| Release ID | 383143636 | 384399324 |
| Archive asset ID | 545406840 | 549697344 |
| Archive filename | student5-minilm-phase-a-pruned-40k.zip | student5-minilm-40k-phase-a-fp32-working-copy-cp45.zip |
| Archive bytes | 88,361,246 | 88,361,246 |
| Archive SHA-256 | 7804bfb245b71df9b835fff7ee00f6ec887e019772ae34c82d269d821d587191 | 7804bfb245b71df9b835fff7ee00f6ec887e019772ae34c82d269d821d587191 |
| model/model.safetensors bytes | 148,020,400 | 148,020,400 |
| FP32 model SHA-256 | d6e45891d1e0ec4ed023caaeb17c0dd0ae80a93b8bf877d275310b7f2837efa2 | d6e45891d1e0ec4ed023caaeb17c0dd0ae80a93b8bf877d275310b7f2837efa2 |

Persistent working-copy Release:
https://github.com/MATRIXNEO23/matrix-understanding-lab/releases/tag/student5-minilm-40k-phase-a-fp32-working-copy-cp45

Direct archive locator:
https://github.com/MATRIXNEO23/matrix-understanding-lab/releases/download/student5-minilm-40k-phase-a-fp32-working-copy-cp45/student5-minilm-40k-phase-a-fp32-working-copy-cp45.zip

The archive is an actual separate physical copy, not a pointer to the original
asset. It includes all 18 original files, including weights, config, tokenizer,
SentencePiece vocabulary, special tokens, token remap, internal checksums and
source metadata. Original and copied local archive inodes differ.
The copied package was also extracted to its own directory.

The sidecar MODEL_MANIFEST.json assigns the working-copy identity. Original
IDs inside the unchanged ZIP remain historical source provenance. This avoids
changing source metadata merely to rename the training base.

Future authorized training must use an extracted working copy recovered from
this new Release, never the original pristine files or original Release.
Keep this initial working-copy snapshot; persist future trained weights under
their own immutable version. This assignment does not start training.

## Verification and recovery

Canonical source Release/asset identity, byte count and GitHub digest were
freshly authenticated. The existing CP34-acquired source archive was reused;
its original bytes/SHA and FP32 model hash were verified before copying.
ZIP integrity and all 17 internal checksum entries pass. Source archive and
original local FP32 model were hashed again after publication/readback and
remain unchanged.

Fresh downloads of all five new Release assets were recovered into a separate
readback directory through their public HTTPS URLs. Every asset's size,
SHA-256 and bytes match the upload. The remotely recovered ZIP and internal
model were independently hashed; all 18 file identities, 17 internal checksums
and four sidecar checksum entries pass. No model loading or inference is needed
for byte identity. A browser download failed; HTTPS recovery succeeded.

Release metadata assets:

- MODEL_MANIFEST.json: asset 549697449.
- SHA256SUMS: asset 549697459.
- RECOVERY.md: asset 549697481.
- source-copy-verification.json: asset 549697495.

Download these with the working ZIP, verify `sha256sum -c SHA256SUMS`, then
extract into a NEW empty working directory and verify the internal SHA256SUMS.
The initial HTTP recovery needed no credentials. Authenticated GitHub Release
UI remains the fallback if repository access later requires authentication.
Exact locators, sizes, file hashes, lineage and recovery instructions are in
the sidecars, also persisted under
`reports/evidence/student5-fp32-working-copy-cp45/`.

Evidence files: MODEL_MANIFEST.json, SHA256SUMS (Release package checksums),
RECOVERY.md, source-copy-verification.json, release-metadata.json,
remote-readback.json, and REPOSITORY_SHA256SUMS (repository delivery checksums).

## Preserved material and stop state

TRAIN remains `student5-matrix-nlu-v3-train-v2.1-cp43r2`,
`data/student5_v3_train_v21/`, SHA-256
`f90ae775a44023c37bf0c3a5087d64746413cbec770ca36cf154d1d533544aa4`.
G03 = PASS. CP44's 4,355 target examples and all prior builder/audit/manifest/
checksum evidence remain unchanged. Repository verification compares every
pre-existing blob; only continuity, artifact-registry and module-index additions may differ.
The original pristine Release and all Student-4 artifacts remain untouched.

SOURCE_PRISTINE_UNCHANGED = true
WORKING_COPY_BYTE_IDENTITY_VERIFIED = true
REMOTE_READBACK = PASS
MANIFEST_PERSISTED = true
SHA256SUMS_PERSISTED = true
RECOVERY_INSTRUCTIONS_PERSISTED = true

trainingExecuted=false
fineTuningExecuted=false
quantizationExecuted=false
onnxExecuted=false
student5PristineModified=false
trainModified=false
devCreated=false
devModified=false
nextWorkStarted=false

STOP. No training, DEV search/creation, dataset repair or next task was started.

Concurrent main update `d922d6ad7e67d60f88c00dcf56b1e67bfe89f2da` introduced the mandatory module index during publication. Its rules and all index entries were preserved; the working-copy entry was completed with remote recovery evidence. Publication uses that newer main as parent.
