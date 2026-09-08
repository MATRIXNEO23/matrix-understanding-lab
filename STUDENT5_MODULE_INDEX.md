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

## CP46 — authorized FP32 attempt stopped at archive pre-flight

Starting main HEAD: `241bc1abe6cad2856716c198f55430494f4811a7`.
Status: `STUDENT5_FP32 = BLOCKED`; training not started; zero checkpoints and no new model Release.
The fresh local CP45 ZIP read back as 73,400,320 bytes / SHA-256 `8497ecf2167cf7948d954fe46301ca9b8e09024c30bc5af8828a818acad32980`, failing the required 88,361,246-byte canonical identity. User-required STOP on unexpected identity mismatch applied. Cause not established; CP45 durable Release metadata and older verified recovery copy remain canonical. No source artifact was modified.
TRAIN and existing 4,355 prepared-target bytes verified unchanged; fresh builder/G03 replay was not reached. Historical G03 PASS is preserved. Missing DEV selection is not the blocker and must not block an otherwise valid resumed run under the current authorization.
Handoff: `reports/STUDENT_5_FP32_CP46_HANDOFF.md`.
Evidence/recovery details: `reports/evidence/student5-fp32-cp46/preflight-blocked.json`; `SHA256SUMS` covers new evidence. `unexecuted-run-plan.json` is draft only, zero optimizer steps.
Canonical CP45 model/release/asset/checksums/recovery locator above are unchanged. No trained model, evaluation, quantization, ONNX, Engine integration, Student-4 change, or DEV/Frozen use occurred. STOP after evidence readback; no automatic next task.

## CP47 — FP32 head training completed; checkpoint selection pending

Starting HEAD: `c9b4984fba6c3da71e27387c4008d78a52208385`. Status: `TRAINING_COMPLETED_SELECTION_PENDING`. No checkpoint selected or production/runtime integration approved.

CP45 recovered fresh and verified: Release 384399324 / asset 549697344, 88,361,246 bytes, archive SHA-256 `7804bfb245b71df9b835fff7ee00f6ec887e019772ae34c82d269d821d587191`, FP32 SHA-256 `d6e45891d1e0ec4ed023caaeb17c0dd0ae80a93b8bf877d275310b7f2837efa2`. CP46 invalid local ZIP quarantined. TRAIN v2.1 and immutable 4,355 prepared targets unchanged; G03 eight rows/14 fields/28 alternatives PASS.

One run: canonical stage A, frozen 12-layer encoder + 172,088 V3 head parameters; 10 epochs / 1,370 optimizer steps; 24.637829853 s optimization plus checkpoint writes, 35.160938859 s including cached feature preparation. Configuration/code: `tools/student5_fp32/train_cp47_config.json`, `train_cp47.py`, `verify_cp47.py`. No architecture or label changes; exact training adapter/loss/runtime details are recorded.

### Durable checkpoint recovery

- Repository/branch: `MATRIXNEO23/matrix-understanding-lab` / `main`.
- New Release: **384423046**, tag `student5-matrix-nlu-v3-fp32-cp47-run1`; source tag commit is the starting HEAD above.
- Archive asset: **549780835**, `student5-matrix-nlu-v3-fp32-cp47-run1.tar.xz`, **93830912 bytes**.
- Archive SHA-256: `029bc292c11091da3aa5742ac85017ffdbc7dbb7ba7be6fadc5cc603f07ceafa`.
- Exact acquisition URL: https://github.com/MATRIXNEO23/matrix-understanding-lab/releases/download/student5-matrix-nlu-v3-fp32-cp47-run1/student5-matrix-nlu-v3-fp32-cp47-run1.tar.xz
- Access: HTTPS download; GitHub authenticated Release access if required. Fresh HTTPS readback succeeded in CP47. Use only this exact immutable asset and verify size/SHA before extraction.
- Recover: extract the tar.xz into a new directory; check internal `SHA256SUMS`; run included `recover_checkpoint.py --epoch N`. Every epoch contains full FP32 weights and optimizer/scheduler/RNG state; config/tokenizer/vocabulary/remap and source are shared in the bundle.
- Remote proof: six assets downloaded, all 58 internal checksum entries and all ten model hashes verified. Recovered epoch-01 strict full-model load PASS. All ten checkpoints also passed strict load, finite-FP32 and frozen-encoder equality checks; 28 software regressions PASS.
- Machine-readable per-checkpoint paths/Release/asset/metrics: `reports/evidence/student5-fp32-cp47/checkpoint-locations.json`.

| New checkpoint identity | Epoch / step | TRAIN mean batch loss | Full FP32 SHA-256 |
|---|---:|---:|---|
| `student5-matrix-nlu-v3-fp32-cp47-run1-epoch-01` | 1 / 137 | 18.907279 | `dcf03bca3ead7bbd43573c9fddc20ef8c954132bb089625de969d35fa5609035` |
| `student5-matrix-nlu-v3-fp32-cp47-run1-epoch-02` | 2 / 274 | 7.447614 | `71e5b7558cb778db7c3eb40418e88c815745dea34144b1dbad9598f9fe10a265` |
| `student5-matrix-nlu-v3-fp32-cp47-run1-epoch-03` | 3 / 411 | 5.883487 | `45c1109e9258d53679f853622d19370f794d5ce274c47e44e4dd89261e50eb49` |
| `student5-matrix-nlu-v3-fp32-cp47-run1-epoch-04` | 4 / 548 | 5.516301 | `3c0f0fdfb64972c1f921508b2fdb25abde5871cbcc13725b0af0323bca7e1b1b` |
| `student5-matrix-nlu-v3-fp32-cp47-run1-epoch-05` | 5 / 685 | 5.223078 | `3f2e656832a435082ad7ac0e53ba401dd35237eb553fad5123a22a371d09a328` |
| `student5-matrix-nlu-v3-fp32-cp47-run1-epoch-06` | 6 / 822 | 5.100230 | `7b7f670bc265e6e1e11fb76c87875494e2d7325dbc45a0993dad413bbda6ead9` |
| `student5-matrix-nlu-v3-fp32-cp47-run1-epoch-07` | 7 / 959 | 5.021640 | `ee45bb926bd26f7278fc6c2cac02173774d3106dd4258a33c7cc826d4ab16663` |
| `student5-matrix-nlu-v3-fp32-cp47-run1-epoch-08` | 8 / 1096 | 4.947185 | `1e5cb002dfc770a45e01aca5c89578acc851d39dbcec2e305828d3bfffde2f20` |
| `student5-matrix-nlu-v3-fp32-cp47-run1-epoch-09` | 9 / 1233 | 4.951446 | `89956185f8ba446a0178ff231b65de3cc9f4cb3410ddb28a088bb488aca9e990` |
| `student5-matrix-nlu-v3-fp32-cp47-run1-epoch-10` | 10 / 1370 | 4.855911 | `f19920de1f6224f37fde056e6b2e423ff4905b215409684a53a5295a1a0ddc6d` |

All models are 148,713,360 bytes; each is stored under `student5-matrix-nlu-v3-fp32-cp47-run1/<checkpointId>/model.safetensors` inside the common archive above. All ten remain eligible, none selected. Epoch losses are TRAIN optimization diagnostics, not held-out accuracy or a selection rule.

Companion Release assets: `ARCHIVE_SHA256SUMS` (ID 549780936, SHA-256 `2ddbdc4f0c332548665585d003f97ca2d1cc4843226a7b9fbad890a29e7b4c59`); `MODEL_MANIFEST.json` (ID 549780942, SHA-256 `48f3fb6a9e693fdf8f651197fde836b7d2660296242f3cbc776730fdbbd18332`); `RECOVERY.md` (ID 549780957, SHA-256 `de554f3f81742b0bfaa0f91c39c4ea37baf393dd35f4cdbcfc0c21b303622de7`); `training-manifest.json` (ID 549780992, SHA-256 `a12881f009a27a4cf5b13377493122dfcc7c9aef963a8e7fc09e72503bed6d60`); `training-metrics.json` (ID 549780967, SHA-256 `52e445a29002c1e9217d5c26bc16ea9d2f8a8ed269cfe0ce2e7bcfca34bd7b18`).

Handoff: `reports/STUDENT_5_FP32_CP47_HANDOFF.md`. Evidence directory: `reports/evidence/student5-fp32-cp47/` (model/training manifests, full per-head losses, checksums, provenance, recovery, target consumption, tests and remote readback).

G04 practical regression evaluation remains pending identifiable authorized evaluation input; G07 remains the documented evidence limitation. No DEV creation/substitution, Frozen use, quantization, ONNX, Student-4 change or Assembling integration occurred. Existing artifact identities remain unchanged. STOP after persistence/readback; no automatic retraining or next phase.

## CP48 — canonical checkpoint-selection input recovery

Starting HEAD: `045b5f06ea6ce0371d3e3e5a14cbeb5864f3d0ef`.
Status: `STUDENT5_FP32_SELECTION = BLOCKED_MISSING_CANONICAL_EVAL_SET`.
CP47 training remains completed with all ten eligible checkpoints persistently registered in Release 384423046 / asset 549780835. Zero checkpoints evaluated in CP48; no selected model, no Release created, no artifact identity changed, no new training. Metrics/regressions/competitiveness remain unmeasured.

Recovery examined both branch trees, five Releases / 14 assets / five tags, 306 Actions runs, 637 artifact records, 588 cache records, 11 workflows, 266 main commit metadata records and 24 pinned documents. DEV V2, P0/P05 gold, MASSIVE development, pruning corpora and V3 software fixtures have different documented roles; none was authenticated as the authorized Student-5 V3 selection set. Two historical Actions ZIPs could not be materialized (reference HTTP 403, direct API HTTP 401); their contents are an explicit search limitation. No assertion that every historical archive was inspected.

Handoff: `reports/STUDENT_5_FP32_SELECTION_CP48.md`.
Evidence: `reports/evidence/student5-fp32-selection-cp48/`; `SHA256SUMS` pins report/evidence bytes, `result.json` records exact status, `candidate-set-register.json` records historical candidates, and `checkpoint-comparison.json` records all ten NOT_EVALUATED states. These are recovery evidence, not a model or evaluation dataset. Recover report/evidence from their introducing commit on main and verify checksums; final delivery response records remote readback and commit SHA.

Required existing input: exact dataset ID, permitted split/V3-target selection provenance, recoverable repository path/ref or Release/asset locator, expected byte size and SHA-256. Historical name may differ from DEV V3. No replacement/gold generation or silent V2 substitution authorized. Once authenticated under a separate continuation, evaluate all ten existing checkpoints consistently; never select on TRAIN loss. G04 awaits evaluation; G07 not reopened. No TRAIN, DEV, pristine, CP45, CP47 checkpoint, Student-4 or Assembling changes. STOP after report/index readback.

CP48 delivery readback: commit `a07f10ea57e61ef8c3e0ecd923721bb73be2a3ec`, all 18 delivered files byte-identical to local verified SHA-256 / Git blobs; all other existing repository blobs unchanged. Exact per-file proof: `reports/evidence/student5-fp32-selection-cp48/remote-readback.json`. The proof and its checksum are persisted in the following delivery-receipt commit; final branch HEAD is returned in the handoff. No model selection was performed.
