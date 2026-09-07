# Student-5 continuity — current resume checkpoint

Updated: 2026-09-07
Repository: `MATRIXNEO23/matrix-understanding-lab`
Active execution branch: `student5-path-b-v3`
Production status: `NOT_PRODUCTION_APPROVED`
Current state: `A4_PASS / A4_ONLY_ASSIGNMENT_FINISHED / SUPERVISOR_GPT_REVIEW`

## Preserved history

- Checkpoints 1–29: `docs/continuity_archive/STUDENT_5_CP01_CP29_d1d4096c6df1c2331eabb33830f6edb577be053f.md`
- Checkpoints 30–32: `docs/continuity_archive/STUDENT_5_CP30_CP32_7acbd6a0081627baa26b44eb5d463ccc31895009.md`

Both archives are preserved byte-for-byte. Historical STOP labels remain evidence for their checkpoint date; the owner authorization and CP33 below govern the current resume.

## Accepted state before resume

```text
TASK 2.3 = ACCEPTED / DO NOT REPEAT
CP32 = GATE_A_BLOCKED_INPUT_ACCESS
firstFailingLayer = A1_CANONICAL_PRISTINE_BINARY_ACQUISITION
physicalBertLoad = NOT_EXECUTED
physicalOnnxExportLoad = NOT_EXECUTED
TASK 3 training = NOT_STARTED
Student-4 changed = false
Path A modified = false
pristine modified = false
TRAIN v1 modified = false
DEV used = false
Frozen read = false
```

Canonical pristine identity:

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

Authenticated GitHub metadata re-verification on 2026-09-07 confirms the private Release asset still exists, is uploaded, has the expected 88,361,246 bytes and GitHub digest matching the canonical archive SHA-256. CP32 failed because the previous Work runtime had metadata-only connector access and no authenticated Release-binary acquisition route.

## Checkpoint 33 — owner-authorized resume and method repair

Owner explicitly authorized immediate operational resume after CP32 and required the continuity/artifact method to be corrected so a future executor never depends on the owner's memory to find project artifacts.

Method changes committed on this branch:

```text
docs/MODEL_ARTIFACT_PERSISTENCE_POLICY.md
- machine-actionable recovery map mandatory
- exact locator/auth/acquisition method mandatory
- fresh-executor resume proof mandatory when possible
- access blocker must be discovered/fixed before dependent work starts

PROJECT_WORK_RULES.md
- continuity is executable handoff, not diary
- NEXT TASK READY requires locator + usable access route + identity + resume point
```

Resume package:

`prompts/WORK_STUDENT_5_PATH_B_V3_RESUME_CP32.md`

The package instructs Work to use its authenticated Cloud Browser / logged-in GitHub UI to download the existing private Release asset directly into the Work machine. The owner is not asked to download, copy or recreate the model.

After acquisition Work must fail closed unless archive bytes/SHA, ZIP integrity, internal SHA256SUMS, model bytes/SHA, tokenizer/mapping/manifest identities all match canonical values.

The downloaded copy is execution-only. The existing pristine Release remains the immutable canonical source and must not be replaced.

## Historical CP33 restart sequence — superseded by A4-only assignment below

```text
1. Work reads PROJECT_WORK_RULES.md, persistence policy, this continuity + both archives, original completion package, CP32 evidence, and CP32 resume prompt.
2. Work reports actual branch/HEAD and starts A1 authenticated pristine acquisition.
3. Use Work Cloud Browser / authenticated GitHub UI for private Release asset acquisition.
4. Verify canonical archive/model/tokenizer identities before any model operation.
5. Install isolated compatible runtime if needed.
6. A2 real pristine BERT/tokenizer + existing V3 16-head model construction + real forward.
7. A3 physical ONNX export/check/load/forward + all expected tensors/shapes/fingerprint/parity.
8. A4 persist retained Gate-A output as a NEW immutable artifact.
9. On Gate-A PASS continue automatically to Gate-B readiness and TASK 3 training under the original authorized completion package.
10. Stop only on a genuine package-defined blocker; do not ask for duplicate authorization.
```

## Non-overwrite guards

```text
DO NOT overwrite pristine
DO NOT overwrite Path A
DO NOT overwrite Student-4
DO NOT overwrite TRAIN V3 v1
DO NOT overwrite prior Path-B checkpoints/candidates
DO NOT use Path A INT8 as Path-B training base
DO NOT use Frozen for tuning
DO NOT integrate into Assembling in this workstream
```

## Historical supervisor state before A4-only assignment

This chat prepares and audits. Work executes the substantive model/runtime/training work. No duplicate training/export is launched here.

Current next action:

```text
OWNER: relaunch/continue Work using prompts/WORK_STUDENT_5_PATH_B_V3_RESUME_CP32.md
WORK: resume at A1 authenticated acquisition, then continue gates automatically on PASS
SUPERVISOR: verify repository-visible results before accepting any gate
```

## Checkpoint 34 — Work A1 recovered and independently verified

Date: 2026-09-07T05:21:38Z. Executor: this interactive Codex Work session.
Branch: `student5-path-b-v3`. Execution HEAD start: `955961d2e7907875312d599c7d2d8307bac81f66`.
Execution directory: `/workspace/scratch/0a50431faa34/student5-path-b`.
Sources are a selective, SHA-pinned snapshot from the GitHub connector, not a local Git checkout. Repository tree has no AGENTS.md.

The prescribed Cloud Browser route was actually used. The logged-in GitHub Release UI exposed asset `student5-minilm-phase-a-pruned-40k.zip`; clicking it delivered the 88,361,246-byte file to shared scratch. The browser download-event waiter timed out after 3 seconds, but the completed file was independently located and verified; no second download or credential extraction was used.

```text
A1 pristine acquisition = PASS
archive SHA-256 = 7804bfb245b71df9b835fff7ee00f6ec887e019772ae34c82d269d821d587191
archive ZIP integrity = PASS
internal SHA256SUMS = 17/17 PASS
candidate manifest payload bytes/SHA = 6/6 PASS
model bytes = 148020400
model SHA-256 = d6e45891d1e0ec4ed023caaeb17c0dd0ae80a93b8bf877d275310b7f2837efa2
mapping SHA-256 = da36a5e1a9057391da935354d895edb3bc3a959744aca6b6602e511f9d4ea9b9
SentencePiece SHA-256 = 748f8053688469d7dc98c135a28a3fc0713bdbb82853f86f8d7a254bada46f78
candidate manifest SHA-256 = a9d23de7816d487986316351c163f37a67d65d001861dbf042b9114c455f066d
TRAIN v1 per-file SHA256SUMS = 129/129 PASS
TRAIN v1 ordered shard SHA-256 = 1118a900026f48cfcc290c3f9dc52a1a019a6a1f4761661f326c33770523140e
TRAIN migration manifest SHA-256 = 87b4a43035d2e3d84a6d599e1f81b497af6e2f36e4ef2c470adb87341c17da98
TASK 2.3 = ACCEPTED / NOT REPEATED
A2 physical BERT/V3 forward = NEXT / NOT YET EXECUTED
A3 physical ONNX = NOT YET EXECUTED
A4 output publication = NOT YET EXECUTED
training / optimizer / backprop / quantization = NOT EXECUTED
DEV / Frozen = UNREAD
pristine / Path A / Student-4 / TRAIN v1 / previous versions = UNCHANGED
```

Recovery map: `reports/evidence/student5-path-b-cp34/recovery.json`. Canonical durable input remains Release 383143636, asset 545406840; scratch is an execution copy only. The same logged-in Release UI is the verified acquisition route for a fresh executor with that authentication. Never infer availability of this login in another session without checking.

Isolated runtime installation is in progress, using the repository's physical-probe pins (Torch 2.4.1+cpu, Transformers 4.44.2, ONNX 1.16.2, ORT 1.19.2; NumPy 1.26.4). No model operation has started.

Exact remaining work: finish pinned runtime; A2 real pristine BERT/tokenizer and existing V3 adapter forward; A3 export via existing V3 contract, checker/runtime load/forward, all 17 tensors, masks/dynamic axes/fingerprint/numerical parity; A4 new immutable retained output and registry/checksum/readback. On Gate-A PASS, identify permitted V3 DEV and gate/evaluator compatibility before training, then the original Gate B–E sequence. All CP33 guards and previously recorded coverage gaps remain open. No Assembling integration or promotion.

## Checkpoint 35a — physical Gate A executed; durable publication in progress

Date: 2026-09-07. Branch: `student5-path-b-v3`; executed source HEAD: `aa3ab11fffdd4e25305fdfe949726358e0514fce` (parent of this evidence commit).
Real pristine BERT/tokenizer load, V3 16 conceptual heads / 17 tensors, forward, ONNX opset 17 checker/load/forward and fingerprint guard PASS. Four batches / seven safe authored IT/EN/ES probes cover batch 1/2/3, sequence 7/9/16, candidates 2/4/7/16 and anchors 1/2/3/5. Masked slots PASS; all output argmax agree; maximum absolute delta 3.129243850708008e-07 (atol=rtol=1e-4). Model: 37,171,640 parameters including 172,088 new head parameters.

No optimizer/backprop/training, DEV or Frozen. Candidate embeddings use real token hidden states only to exercise mechanics; no learned semantic-quality claim. TracerWarning on fixed hidden dimension 384 is recorded; tested dynamic dimensions pass. TASK 2.3 not repeated; prior artifacts unchanged.

Evidence: `reports/evidence/student5-path-b-cp35/report.json`, `artifact-manifest.json`, `artifact-SHA256SUMS`.

Pending A4: upload NEW private prerelease `student5-path-b-v3-untrained-gate-a-cp35-20260907`, archive 176837978 bytes, SHA256 dfe20ae4cfa49656f557872f6ba2afeabef6caea06390f943ae8cd0945a37d71; perform fresh binary recovery/checksum/load, record release/asset IDs and registry entry. Local package `/workspace/scratch/student5-path-b-v3-untrained-gate-a-cp35-20260907.zip`; local copy alone does not close A4.

Then automatically examine Gate B permitted V3 DEV identity/evaluation contract, TRAIN coverage and acceptance criteria before any training. Remaining: frozen-backbone/head training, DEV/error analysis and TRAIN-only new versions, evidence-backed capacity escalation, taught FP32 lock/persistence, taught ONNX, protected quantization/parity/runtime, final one-shot Frozen only after lock, final handoff. STOP on genuine package blockers; do not invent V2/V3 gate equivalence. No promotion or Assembling integration.

## Checkpoint 35b — A4-only durable publication PASS; return to Supervisor GPT

Date: 2026-09-07. Branch: `student5-path-b-v3`. Assignment/start HEAD and release-tag commit: `4c101cac96eab925b600012d989988449d3f09b7`. This evidence commit is its direct child; resolve branch HEAD for the exact handoff commit. Issuer/reviewer: Supervisor GPT; executor: ChatGPT Work. Scope: `prompts/WORK_STUDENT_5_PATH_B_V3_RESUME_CP35A_A4_ONLY.md`. This assignment supersedes all historical automatic-continuation instructions above. Assignment ends at A4; no later work started or authorized by this checkpoint.

The retained local archive existed and matched CP35a exactly before upload. The browser's filechooser waiter timed out when used with the initial locator flow; the supported synchronized filechooser wait plus visible upload-control click succeeded. Exactly one asset was supplied and published as a new prerelease. No existing release/tag/asset was replaced.

```text
A4 = PASS
artifactId / releaseTag = student5-path-b-v3-untrained-gate-a-cp35-20260907
releaseId = 383886129
assetId = 548329150
assetName = student5-path-b-v3-untrained-gate-a-cp35-20260907.zip
bytes = 176837978
SHA-256 = dfe20ae4cfa49656f557872f6ba2afeabef6caea06390f943ae8cd0945a37d71
source model/export commit = aa3ab11fffdd4e25305fdfe949726358e0514fce
source evidence commit = e95571b7df4ff2ff56cf52d0603f1bb5d43f0250
fresh readback = PASS at 2026-09-07T07:03:10.041152+00:00
ZIP integrity = PASS
internal SHA256SUMS = 17/17 PASS
manifest/base lineage = PASS
status = UNTRAINED_GATE_A_RUNTIME_PROBE_ONLY / NOT_PRODUCTION_APPROVED
```

Primary persistent locator: https://github.com/MATRIXNEO23/matrix-understanding-lab/releases/tag/student5-path-b-v3-untrained-gate-a-cp35-20260907

Binary acquisition URL: https://github.com/MATRIXNEO23/matrix-understanding-lab/releases/download/student5-path-b-v3-untrained-gate-a-cp35-20260907/student5-path-b-v3-untrained-gate-a-cp35-20260907.zip

Working recovery route: public HTTPS GET (Python urllib.request.urlopen, no credentials) into a fresh output file, then independently verify bytes/SHA, ZIP integrity, internal SHA256SUMS and manifest lineage. The recovered file is distinct from the original upload archive. Browser upload uses `/home/oai/share/<archive name>` synchronized from `/workspace/scratch/<archive name>`; public recovery does not depend on that browser login. Last recovery proof: CP35b. Reproduction source is pinned above, but reproduction is not needed for this stored original binary.

Evidence: `reports/evidence/student5-path-b-cp35b-a4/publication.json`, `recovery.json`, `SHA256SUMS`; registry: `docs/STUDENT_ARTIFACT_REGISTRY.md`. CP35a files remain byte-for-byte unchanged, including their historical A4_PENDING status. This CP35b publication manifest records the new A4 result separately.

A1/A2/A3 and TASK 2.3 were not repeated. No model execution, training, optimizer, backprop, DEV, Frozen, quantization, Assembling work or promotion was performed during A4. Pristine, Path A, Student-4, TRAIN V3 v1 and prior Path-B files remain unchanged.

Exact disposition: report A4 PASS and evidence to Supervisor GPT; await review. This executor does not anticipate or start another assignment.
