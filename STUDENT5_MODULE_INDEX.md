# MATRIX / Student-5 — Canonical Module & Artifact Index

This file is the canonical operational index for Student-5. It must be updated whenever a new persistent model, dataset, builder, evaluation artifact, release, checkpoint, workflow output, or recovery route is created or superseded.

## Update rule

For every new Student-5 work item, update this file before the task is considered complete. Each entry must contain: what it is, why it exists, canonical repo/branch/HEAD if relevant, exact path or Release/asset locator, version/model/dataset ID, expected bytes when known, SHA-256, status, dependencies, and recovery/readback notes.

A new chat/session must treat this file as the first operational lookup before searching ad hoc.

## Canonical repository

- Repository: `MATRIXNEO23/matrix-understanding-lab`
- Canonical branch: `main`

## Model artifacts

### 1. Student-5 pristine FP32 backbone
- Model ID: `student-5-minilm-40k-phase-a-pristine`
- Purpose: immutable canonical pristine backbone; never train/overwrite in place.
- Release ID: `383143636`
- Release tag: `student-5-minilm-40k-phase-a-pristine`
- Asset ID: `545406840`
- Asset: `student5-minilm-phase-a-pruned-40k.zip`
- Archive bytes: `88,361,246`
- Archive SHA-256: `7804bfb245b71df9b835fff7ee00f6ec887e019772ae34c82d269d821d587191`
- Internal FP32 `model/model.safetensors` bytes: `148,020,400`
- Internal FP32 SHA-256: `d6e45891d1e0ec4ed023caaeb17c0dd0ae80a93b8bf877d275310b7f2837efa2`
- Status: pristine, NOT_MATRIX_NLU, not production approved, Frozen unread.
- Recovery: GitHub Release asset; verify archive SHA and internal SHA256SUMS before use.

### 2. Student-5 separate FP32 working copy
- Model ID: `student-5-minilm-40k-phase-a-fp32-working-copy`
- Version: `CP45_INITIAL_BYTE_IDENTICAL`
- Purpose: only copy allowed to become the future trained FP32 lineage; original pristine remains untouched.
- Release ID: `384399324`
- Release tag: `student5-minilm-40k-phase-a-fp32-working-copy-cp45`
- Main asset ID: `549697344`
- Main asset: `student5-minilm-40k-phase-a-fp32-working-copy-cp45.zip`
- Archive bytes: `88,361,246`
- Archive SHA-256: `7804bfb245b71df9b835fff7ee00f6ec887e019772ae34c82d269d821d587191`
- Internal FP32 SHA-256: `d6e45891d1e0ec4ed023caaeb17c0dd0ae80a93b8bf877d275310b7f2837efa2`
- Companion assets: `MODEL_MANIFEST.json`, `SHA256SUMS`, `RECOVERY.md`, `source-copy-verification.json`.
- Status: untrained, byte-identical initial working snapshot.
- Recovery: use Release + `RECOVERY.md`; preserve this snapshot and create a new identity for any trained output.
- Repository/branch: `MATRIXNEO23/matrix-understanding-lab`, `main`; Release tag source HEAD `2bf43b6ce92436fbab0cb04580fc1f51f0a1fd0a`.
- Persistent locator: https://github.com/MATRIXNEO23/matrix-understanding-lab/releases/tag/student5-minilm-40k-phase-a-fp32-working-copy-cp45
- Internal FP32 model bytes: `148,020,400`; complete archive has 18 files.
- Companion asset IDs: MODEL_MANIFEST `549697449`; SHA256SUMS `549697459`; RECOVERY `549697481`; source-copy-verification `549697495`.
- Source dependency: pristine Release `383143636` / asset `545406840`, verified unchanged before/after copying and remote recovery.
- CP45 readback: PASS; all five assets freshly downloaded via HTTPS into a separate directory; complete byte identity, archive/model hashes, 18 file identities, 17 internal checksums and four sidecar checksum entries verified.
- Evidence: `reports/evidence/student5-fp32-working-copy-cp45/remote-readback.json`; manifest/checksums/recovery in the same directory.
- Handoff: `reports/STUDENT_5_FP32_WORKING_COPY_CP45.md`; repository delivery commit identified by this report's introduction on main.
- Local working extraction, convenience only: `/workspace/scratch/student5-fp32-working-copy-cp45/working-package/model`. No training executed.

### 3. Student-5 original INT8 ONNX runtime probe
- Status ID: `STUDENT_5_40K_UNTAUGHT_INT8`
- Purpose: original quantized runtime probe of the pristine 40k backbone; not Matrix NLU, not production approved.
- Release ID: `383162517`
- Release tag: `student-5-minilm-40k-untaught-int8-runtime-probe`
- Asset ID: `545486429`
- Asset: `student-5-minilm-40k-untaught-int8-runtime-probe.zip`
- Archive bytes: `142,463,548`
- Archive SHA-256: `72eea0af4211959bdbc92be36387faf5b85da957830f9be0a6d0dd50ab7cedf6`
- FP32 ONNX bytes: `148,202,898`
- FP32 ONNX SHA-256: `799d86b9231721c0e7ff656b48cb609611c98ea75c8489e4edebeaf7e9d7de23`
- INT8 ONNX bytes: `84,457,299`
- INT8 ONNX SHA-256: `f58463a6d1f4daca2e58c8e40f7f6d1cbaa7d107e9534160278bc46552e0304a`
- Quantized weight-bearing operators: `73/73`
- FP32→INT8 mean representation cosine: `0.9985922280`
- FP32→INT8 minimum representation cosine: `0.9974925518`
- Mobile status: static compatibility risk; no physical Moto validation recorded in this release.
- Recovery: GitHub Release asset; archive contains FP32/INT8 ONNX, tokenizer/config, manifest, operator census, parity/benchmark, provenance, source and SHA256SUMS.

## TRAIN datasets

### 4. Student-5 TRAIN v1
- Dataset ID: canonical pre-repair Student-5 V3 TRAIN.
- Path: `data/student5_v3/`
- Ordered dataset SHA-256: `1118a900026f48cfcc290c3f9dc52a1a019a6a1f4761661f326c33770523140e`
- Observations: `3,150`
- Claims: `3,990`
- Status: immutable historical source; do not overwrite.

### 5. Student-5 TRAIN v2 — CP42 audit-locked source candidate
- Dataset ID: `student5-matrix-nlu-v3-train-v2`
- Version: `CP42_BUILD_1_AUDIT_LOCKED`
- Path: `data/student5_v3_train_v2/`
- TRAIN SHA-256: `b6acf41e6634c2f89e6b8251fb5f816ec60fb0ca1cd6c90dfcbed46c2c12584c`
- Starting source checkpoint: `1396dd6c997ce0dbf5e4a5ce933437c82fc1c217`
- Contents include: `train.jsonl.gz`, `manifest.json`, `BUILD_LOCK.json`, `construction-review.json`, `provenance-and-mapping.jsonl.gz`, `quarantine.jsonl.gz`.
- Status: historical immutable source for v2.1; CP42 audit found issues.

### 6. Student-5 TRAIN v2.1 repaired candidate
- Dataset ID: `student5-matrix-nlu-v3-train-v2.1-cp43r2`
- Path: `data/student5_v3_train_v21/`
- SHA-256: `f90ae775a44023c37bf0c3a5087d64746413cbec770ca36cf154d1d533544aa4`
- Observations: `1,831`
- Claims: `2,524`
- Preserved rows: `1,625`
- Corrected retained rows: `75`
- Added targeted rows: `131`
- Quarantined rows: `8`
- Exact redundant repetitions deactivated: `1,559`
- G03: PASS after target-builder support work.
- Status: current canonical TRAIN candidate for future FP32 training; do not modify in place.

## Target preparation / builder

### 7. G03 target-preparation support
- Canonical closure HEAD: `6389e82c255c50964ce2df370a4682ba7206248b`
- Scope: status + ordered alternatives + subject/owner/target referents for 8 G03 rows.
- G03 rows: `8/8 PASS`
- Ambiguous fields preserved: `14`
- Ordered alternatives preserved: `28`
- Target examples prepared: `4,355`
- Tests: `28 PASS`
- Unrelated targets unchanged: true.
- Status: canonical target-preparation mechanism for Student-5 V3.

## Audit / analysis checkpoints

### 8. CP37 TRAIN curriculum audit
- Report: `reports/STUDENT_5_TRAIN_CURRICULUM_AUDIT_CP37.md`
- Purpose: curriculum coverage, imbalance, repetition, class support, role/temporal risks.
- Status: historical evidence used to build/repair TRAIN v2.

### 9. CP38 TRAIN repair specification
- Report: `reports/STUDENT_5_TRAIN_REPAIR_SPECIFICATION_CP38.md`
- Evidence: `reports/evidence/student5-path-b-cp38-repair-spec/`
- Purpose: issue-by-issue repair design; historical `AWAITING_SUPERVISOR_OWNER` flags for D01–D07 are superseded by later approval.

### 10. CP41 pristine pre-training analysis
- Report: `reports/STUDENT_5_PRISTINE_ANALYSIS_CP41.md`
- Evidence: `reports/evidence/student5-pristine-analysis-cp41/`
- Purpose: authenticated pristine execution and representation diagnostics; no Matrix heads, no supervised semantic accuracy claim.
- Key caution: do not use sentence cosine/word overlap as a role shortcut.

### 11. CP42 TRAIN v2 audit
- Source candidate: `data/student5_v3_train_v2/`
- Purpose: full audit of TRAIN v2; 16 findings; later repaired in CP43/v2.1.
- Status: historical audit evidence.

### 12. CP43 repaired TRAIN v2.1 audit
- Evidence root: `reports/evidence/student5-train-v21-cp43/`
- Additional build1 evidence: `reports/evidence/student5-train-v21-cp43-build1/`
- Outcome: 13/16 CP42 issues resolved; N05 new issue found and resolved; residual G03/G04/G07 initially documented.
- G03 later closed PASS at HEAD `6389e82c255c50964ce2df370a4682ba7206248b`.
- G04: post-training regression evaluation requirement, not pre-training dataset defect.
- G07: provenance/overlap evidence limitation; no proven contamination.

## Canonical semantic decisions

### 13. D01–D07
- D01: desire time
- D02: source/perspective
- D03: BELIEF/DIRECT
- D04: malformed/reflexive
- D05: metalinguistic negation
- D06: zero-claim/UNKNOWN
- D07: independent roles
- Status: approved; do not reopen automatically.

## Current training state

### 14. FP32 training authorization attempt
- Last training-attempt HEAD after blocker report: `2bf43b6ce92436fbab0cb04580fc1f51f0a1fd0a`
- Pristine verified: PASS
- TRAIN verified: PASS
- Target preparation: 4,355 examples, PASS
- Training executed: false
- Blocker reported by Work: missing identified canonical checkpoint-selection DEV/gold input.
- Important continuity rule: do NOT create or recreate a DEV/gold set merely because the locator is missing. Recover the original authorized evaluation material first. Treat the label `DEV V3` as descriptive unless/until an original artifact with exact identity is found.

## Permanent recovery / continuity rules

1. Never overwrite pristine models, historical TRAIN versions, or quantized reference artifacts.
2. Every trained/quantized/exported model gets a new immutable ID and SHA-256.
3. Every persistent model artifact must carry manifest, SHA256SUMS, provenance/lineage, exact locator, and recovery instructions.
4. Every new TRAIN version must carry builder/source, provenance, mapping, audit evidence and checksum identity.
5. Every task that creates or changes a Student-5 artifact must update this file before the task is considered complete.
6. A new session must read `STUDENT5_MODULE_INDEX.md` first, then `WORK_CONTINUITY*` / relevant checkpoint handoff, then execute from the latest verified checkpoint.
7. Do not claim an artifact is saved until remote readback / SHA verification is complete.
8. Do not recreate missing canonical artifacts merely because their locator is temporarily unknown; recover first.

## Next update trigger

Update this index immediately when any of these occur:
- canonical DEV/gold locator is recovered;
- FP32 training starts/completes;
- trained FP32 model is persisted;
- quantized post-training model is created;
- ONNX export is created;
- benchmark/evaluation artifact becomes canonical;
- Android/Assembling integration creates a new production candidate;
- any model/dataset is superseded, quarantined, or promoted.
