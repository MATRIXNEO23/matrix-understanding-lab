# Student model artifact registry

Date: `2026-09-05`  
Repository: `MATRIXNEO23/matrix-understanding-lab`  
Status: `CANONICAL_RECOVERY_MAP`

This registry records where Student-4-v2.2A and Student-5 MiniLM 40k can be found, which binary artifacts are durably reachable, and which preservation gaps remain. Both students must be preserved and operated on independently.

## Mandatory isolation rule

```text
Student-4-v2.2A = PRESERVE
Student-5-MiniLM-40k = PRESERVE
workMode = ONE_STUDENT_AT_A_TIME
crossStudentMutation = FORBIDDEN
crossStudentArtifactOverwrite = FORBIDDEN
automaticReplacement = FORBIDDEN
automaticPromotion = FORBIDDEN
```

Before switching students, record a continuity checkpoint identifying the exact input artifact, model checksum, active operation and proof that the other student was not modified.

## Student-4-v2.2A

Role: preserved comparative baseline and controlled experimental runtime candidate.  
Status: `EXPERIMENTAL_TEST_CANDIDATE / NOT_PRODUCTION_APPROVED`.  
Dev selection: `FAILED_GATE`.  
Frozen: `FROZEN_UNREAD`.

### Authoritative training and evaluation

- GitHub Actions run: [33860928806](https://github.com/MATRIXNEO23/matrix-understanding-lab/actions/runs/33860928806)
- Run HEAD: [`617aeca8a6abac4366eb13347fb88026307dc3b8`](https://github.com/MATRIXNEO23/matrix-understanding-lab/commit/617aeca8a6abac4366eb13347fb88026307dc3b8)
- Canonical report: [`reports/STUDENT_4_V22A_CONTROLLED_REPAIR_REPORT.md`](https://github.com/MATRIXNEO23/matrix-understanding-lab/blob/main/reports/STUDENT_4_V22A_CONTROLLED_REPAIR_REPORT.md)
- Model-state SHA-256: `446b6a58265500001efd350f81d75867227cbfd3c6da699ed9c9330257d16a9c`

### Training-run artifacts

These GitHub Actions artifacts are currently retrievable from the run page. Their recorded expiry is 2026-10-04; the run page is the preferred browser entry point.

| Purpose | Artifact name | ID | Bytes | GitHub digest |
|---|---|---:|---:|---|
| Report evidence | `matrix-nlu-student-4-v22a-report-33860928806` | `9938144318` | 302,085 | `sha256:e71e153509e8f002fd74782ebb5667bb93b59438e6646c4c11723afe4be64129` |
| FP32 training bundle | `matrix-nlu-student-4-v22a-bundle-33860928806` | `9938150338` | 217,603,720 | `sha256:f2dfea052df525af741f8ddd98e279b5443645450d09f949970a6eac18edb987` |
| Resumable checkpoint | `matrix-nlu-student-4-v22a-resume-33860928806` | `9938165358` | 650,269,442 | `sha256:ff66bd687fc55f1b767164b84795ad84aba4937130b7d8b0aead9afff5f018cd` |

API download endpoints, requiring repository authorization:

- report: `https://api.github.com/repos/MATRIXNEO23/matrix-understanding-lab/actions/artifacts/9938144318/zip`
- bundle: `https://api.github.com/repos/MATRIXNEO23/matrix-understanding-lab/actions/artifacts/9938150338/zip`
- resumable checkpoint: `https://api.github.com/repos/MATRIXNEO23/matrix-understanding-lab/actions/artifacts/9938165358/zip`

### Durable mixed/head-protected runtime copy

The experimental runtime package is stored through Git LFS in the `assembling` repository:

- [Mixed/head-protected ZIP](https://github.com/MATRIXNEO23/assembling/blob/a26cdcb8116f6cc96ba02a0f1e717b70cf45fb11/models/matrix-nlu/matrix-nlu-student-4-v22a-mixed-head-protected-local-20260904T1440Z.zip)
- [Assembling artifact manifest](https://github.com/MATRIXNEO23/assembling/blob/a26cdcb8116f6cc96ba02a0f1e717b70cf45fb11/vendor/matrix-understanding-lab/runtime-candidate/student-4-v2.2a/ASSEMBLING_ARTIFACT.json)
- Assembling snapshot: [`a26cdcb8116f6cc96ba02a0f1e717b70cf45fb11`](https://github.com/MATRIXNEO23/assembling/commit/a26cdcb8116f6cc96ba02a0f1e717b70cf45fb11)
- LFS ZIP bytes: `356134801`
- LFS ZIP SHA-256: `4998ce2f44dd8553d75f86b8d7975529f6a5f779de9107eef393648022d6ccb5`
- Mixed INT8 ONNX SHA-256: `738a4d052790367509d55487b649b71aaa029d839135693bb5be46f74d55ef70`
- FP32 ONNX reference SHA-256: `11c4f9e10c85badd1afa425cfe5f431035ec3ab61b41425f26479e58c71eb0d3`

The GitHub web page may display only the 134-byte LFS pointer. Retrieve the real 356,134,801-byte ZIP using Git LFS or the GitHub download control while authenticated.

### Student-4 preservation assessment

```text
canonicalReport = PRESENT
trainingRun = PRESENT
fp32Bundle = PRESENT_UNTIL_ACTIONS_RETENTION_EXPIRY
resumableCheckpoint = PRESENT_UNTIL_ACTIONS_RETENTION_EXPIRY
mixedRuntimeZip = PRESENT_IN_ASSEMBLING_GIT_LFS
runtimeManifest = PRESENT
preservationRisk = COPY_BUNDLE_AND_RESUME_BEFORE_2026_10_04
```

## Student-5 MiniLM 40k

Role: selected Phase-A representation-preserving backbone and primary future teaching candidate.  
Status: `PRUNING_CANDIDATE_SELECTED / NOT_MATRIX_NLU / NOT_PRODUCTION_APPROVED`.  
Frozen: `FROZEN_UNREAD`.

### Authoritative reports and reproducibility source

- [Quality-analysis dossier](https://github.com/MATRIXNEO23/matrix-understanding-lab/blob/main/reports/STUDENT_5_MINILM_40K_QUALITY_ANALYSIS.md)
- [Canonical deep-pruning report](https://github.com/MATRIXNEO23/matrix-understanding-lab/blob/main/reports/STUDENT_5_MINILM_DEEP_PRUNING.md)
- [Compatibility report](https://github.com/MATRIXNEO23/matrix-understanding-lab/blob/main/reports/STUDENT_5_MINILM_PRUNING_FEASIBILITY.md)
- [Student-5 continuity](https://github.com/MATRIXNEO23/matrix-understanding-lab/blob/main/docs/WORK_CONTINUITY_STUDENT_5.md)
- [Deterministic pruning implementation](https://github.com/MATRIXNEO23/matrix-understanding-lab/blob/main/matrix_nlu/student5_deep_pruning.py)
- [Pruning contract tests](https://github.com/MATRIXNEO23/matrix-understanding-lab/blob/main/matrix_nlu/test_student5_deep_pruning.py)
- Implementation commit: [`25546528917d42d70129f059ff56da672678c7d4`](https://github.com/MATRIXNEO23/matrix-understanding-lab/commit/25546528917d42d70129f059ff56da672678c7d4)
- Corrective report commit: [`a1d407d63d4dcb84033d8ac525cce0e2475c27e1`](https://github.com/MATRIXNEO23/matrix-understanding-lab/commit/a1d407d63d4dcb84033d8ac525cce0e2475c27e1)

### Selected artifact identity

| Field | Value |
|---|---|
| Vocabulary | `40000` |
| FP32 model bytes | `148020400` |
| Artifact-directory bytes | `150116913` |
| Archive bytes | `88361246` |
| Model SHA-256 | `d6e45891d1e0ec4ed023caaeb17c0dd0ae80a93b8bf877d275310b7f2837efa2` |
| Mapping SHA-256 | `da36a5e1a9057391da935354d895edb3bc3a959744aca6b6602e511f9d4ea9b9` |
| SentencePiece SHA-256 | `748f8053688469d7dc98c135a28a3fc0713bdbb82853f86f8d7a254bada46f78` |
| Candidate-manifest SHA-256 | `a9d23de7816d487986316351c163f37a67d65d001861dbf042b9114c455f066d` |
| Archive SHA-256 | `7804bfb245b71df9b835fff7ee00f6ec887e019772ae34c82d269d821d587191` |

### Student-5 durable binary locator

The canonical original Phase-A archive has been recovered, verified against every recorded identity hash, and published as a durable pre-release asset owned by this repository.

- Preservation report: [`reports/STUDENT_5_40K_PRISTINE_PRESERVATION.md`](https://github.com/MATRIXNEO23/matrix-understanding-lab/blob/main/reports/STUDENT_5_40K_PRISTINE_PRESERVATION.md)
- Release: [Student-5 MiniLM 40k Phase-A Pristine](https://github.com/MATRIXNEO23/matrix-understanding-lab/releases/tag/student-5-minilm-40k-phase-a-pristine)
- Release label: `Pre-release`
- Release ID: `383143636`
- Asset ID: `545406840`
- Tag: `student-5-minilm-40k-phase-a-pristine`
- Tag commit: `20230e52388560c537eb614083ca5a3bda29ecfc`
- Asset: [student5-minilm-phase-a-pruned-40k.zip](https://github.com/MATRIXNEO23/matrix-understanding-lab/releases/download/student-5-minilm-40k-phase-a-pristine/student5-minilm-phase-a-pruned-40k.zip)
- Asset bytes: `88361246`
- GitHub-recorded digest: `sha256:7804bfb245b71df9b835fff7ee00f6ec887e019772ae34c82d269d821d587191`
- Source classification: `ORIGINAL_RECOVERED`

```text
canonicalReports = PRESENT
generatorAndTests = PRESENT
modelIdentityAndChecksums = VERIFIED
remoteBinaryLocator = RECORDED
binaryPreservation = DURABLY_VERIFIED
artifactStatus = PRISTINE_PHASE_A_BACKBONE
nluStatus = NOT_MATRIX_NLU
productionStatus = NOT_PRODUCTION_APPROVED
```

A GitHub Release asset in this repository is the durable primary locator. It is not a retention-limited GitHub Actions artifact. Before use, verify its exact byte count and archive SHA-256 against the canonical identity table above.

### Student-5 Path-A untaught runtime probe

This artifact is a deployment probe derived from, but separate from, the immutable pristine Phase-A backbone.

```text
logicalName = STUDENT_5_40K_UNTAUGHT_INT8
status = RUNTIME_PROBE_ONLY
nluStatus = NOT_MATRIX_NLU
productionStatus = NOT_PRODUCTION_APPROVED
verdict = RUNTIME_PROBE_PASS
pathBStarted = false
```

- Report: [`reports/STUDENT_5_40K_UNTAUGHT_INT8_RUNTIME_PROBE.md`](https://github.com/MATRIXNEO23/matrix-understanding-lab/blob/main/reports/STUDENT_5_40K_UNTAUGHT_INT8_RUNTIME_PROBE.md)
- Reproduction source: [`matrix_nlu/student5_untaught_runtime_probe.py`](https://github.com/MATRIXNEO23/matrix-understanding-lab/blob/main/matrix_nlu/student5_untaught_runtime_probe.py)
- Release: [Student-5 40k Untaught INT8 Runtime Probe](https://github.com/MATRIXNEO23/matrix-understanding-lab/releases/tag/student-5-minilm-40k-untaught-int8-runtime-probe)
- Release ID: `383162517`
- Asset ID: `545486429`
- Asset: [student-5-minilm-40k-untaught-int8-runtime-probe.zip](https://github.com/MATRIXNEO23/matrix-understanding-lab/releases/download/student-5-minilm-40k-untaught-int8-runtime-probe/student-5-minilm-40k-untaught-int8-runtime-probe.zip)
- Asset bytes: `142463548`
- Asset/GitHub digest: `sha256:72eea0af4211959bdbc92be36387faf5b85da957830f9be0a6d0dd50ab7cedf6`
- FP32 ONNX: `148202898` bytes; SHA-256 `799d86b9231721c0e7ff656b48cb609611c98ea75c8489e4edebeaf7e9d7de23`
- INT8 ONNX: `84457299` bytes; SHA-256 `f58463a6d1f4daca2e58c8e40f7f6d1cbaa7d107e9534160278bc46552e0304a`
- Quantization: ONNX Runtime dynamic per-channel QInt8; 73/73 weight-bearing eligible MatMul/Gemm nodes quantized.
- Pristine input modified: false.
- Canonical DEV/Frozen used: false/false.
- Matrix heads/training: absent/not executed.

This Path-A artifact must never be used as the Path-B training base. Path B must restart from the pristine FP32 40k Release above.

### Student-5 Matrix-NLU V3 canonical TRAIN-only dataset

```text
artifactId = student5-matrix-nlu-v3-train-v1
contract = MATRIX_NLU_CONTRACT_V3
scope = TRAIN_ONLY
rows = 3150
claims = 3990
status = STRUCTURALLY_VALIDATED_WITH_NONBLOCKING_COVERAGE_RISKS
productionStatus = NOT_PRODUCTION_APPROVED
canonicalDevUsed = false
frozenDataRead = false
trainingExecuted = false
```

- Durable locator: [`data/student5_v3/`](https://github.com/MATRIXNEO23/matrix-understanding-lab/tree/main/data/student5_v3)
- Artifact checkpoint: [`117afd627ebe9f584b9328f1f78c63822980a49c`](https://github.com/MATRIXNEO23/matrix-understanding-lab/commit/117afd627ebe9f584b9328f1f78c63822980a49c)
- Ordered TRAIN dataset SHA-256: `1118a900026f48cfcc290c3f9dc52a1a019a6a1f4761661f326c33770523140e`
- Migration manifest SHA-256: `87b4a43035d2e3d84a6d599e1f81b497af6e2f36e4ef2c470adb87341c17da98`
- Source Matrix V2 TRAIN SHA-256: `5118d37ce2ab19d5be171f757f448698085e3c222a4a627f9838329836185820`
- Source v2.2A repair TRAIN SHA-256: `8be02976d46ba47d746ff7307d688d93595453221965b3de995d4b1de655799f`
- Report: [`reports/STUDENT_5_TRAIN_V3_MIGRATION.md`](https://github.com/MATRIXNEO23/matrix-understanding-lab/blob/main/reports/STUDENT_5_TRAIN_V3_MIGRATION.md)
- Per-file checksums: [`data/student5_v3/SHA256SUMS`](https://github.com/MATRIXNEO23/matrix-understanding-lab/blob/main/data/student5_v3/SHA256SUMS)

This is data-contract evidence only. It is not a trained model, quality approval, or authorization to start Path B.

## Switching checklist

Before starting work on either student:

1. Identify `activeStudent`.
2. Resolve the exact source location from this registry.
3. Verify the expected SHA-256 before use.
4. Create a separate output directory and artifact name.
5. Confirm the inactive student's files and checksums remain unchanged.
6. Update the relevant continuity file after every significant checkpoint.
7. Never use Student-4 weights as Student-5 input or Student-5 weights as Student-4 input.
8. Never overwrite an existing bundle, checkpoint, tokenizer, manifest, report, or runtime artifact.
9. Keep Frozen unread until separately authorized.
10. Never infer production approval from artifact availability.

## Current disposition

```text
activeStudent = Student-5-MiniLM-40k
Student-4-v2.2A = PRESERVED_BASELINE
Student-5-MiniLM-40k = SELECTED_PHASE_A_CANDIDATE
Student-4CrossMutation = false
Student-5CrossMutation = false
frozenDataRead = false
productionPromotionExecuted = false
```

## Student-5 Path B — CP35a untrained Gate-A artifact, preserved at CP35b

Status: `UNTRAINED_GATE_A_RUNTIME_PROBE_ONLY / NOT_PRODUCTION_APPROVED`. A4 durable preservation: `PASS`; Supervisor GPT review pending. No training dataset/run applies; no quantization. Format: ZIP containing FP32 safetensors and FP32 ONNX opset 17, tokenizer/config/mapping, contract, source, pinned environment and original report.

- Artifact ID/tag: `student5-path-b-v3-untrained-gate-a-cp35-20260907`
- Release: [383886129](https://github.com/MATRIXNEO23/matrix-understanding-lab/releases/tag/student5-path-b-v3-untrained-gate-a-cp35-20260907), prerelease.
- Asset: [student5-path-b-v3-untrained-gate-a-cp35-20260907.zip](https://github.com/MATRIXNEO23/matrix-understanding-lab/releases/download/student5-path-b-v3-untrained-gate-a-cp35-20260907/student5-path-b-v3-untrained-gate-a-cp35-20260907.zip), ID `548329150`.
- Archive bytes: `176837978`; SHA-256: `dfe20ae4cfa49656f557872f6ba2afeabef6caea06390f943ae8cd0945a37d71`.
- Source code/model-export commit: `aa3ab11fffdd4e25305fdfe949726358e0514fce`; evidence commit: `e95571b7df4ff2ff56cf52d0603f1bb5d43f0250`; assignment/tag commit: `4c101cac96eab925b600012d989988449d3f09b7`.
- Base/predecessor: `student-5-minilm-40k-phase-a-pristine`, Release `383143636`, asset `545406840`, model SHA-256 `d6e45891d1e0ec4ed023caaeb17c0dd0ae80a93b8bf877d275310b7f2837efa2`.
- Contract: `MATRIX_NLU_CONTRACT_V3`; fingerprint `7b0646e44243ad897760c0fcadbe141f1b8e88e3fd8d63a1789106571b9987b0`.
- FP32 safetensors: `148713328` bytes; SHA-256 `f77986e10bf5cf6011d893ee9785d0645d9f1d52ac0c38423fb71086e87366e5`.
- FP32 ONNX: `148360424` bytes; SHA-256 `fea789af9a68cecadc369f70b84efd61e29c0249a007e0f0a2b7773df8a9f8cb`.
- Working recovery: public HTTPS GET from the asset URL above, no credentials; verify exact archive bytes/SHA, ZIP integrity, all 17 internal hashes and base/source manifest. Fresh recovery PASS at `2026-09-07T07:03:10.041152+00:00`, checkpoint CP35b.
- Complete machine-actionable manifest: `reports/evidence/student5-path-b-cp35b-a4/publication.json`; independent readback: `recovery.json` in the same directory; evidence checksums: `SHA256SUMS`.
- Limits: new heads untrained; historical four-batch PyTorch/ONNX parity tests runtime mechanics only, no linguistic-quality claim; external candidate/anchor embeddings are not learned extraction evidence. All historical CP35a evidence remains unchanged.

No prior artifact/version overwritten. Assignment ends at A4; return to Supervisor GPT.


## Student-5 FP32 working copy — CP45

Model ID: `student-5-minilm-40k-phase-a-fp32-working-copy`
Version: `CP45_INITIAL_BYTE_IDENTICAL`; status: UNTRAINED_FP32_WORKING_COPY.
Source pristine Release 383143636 / asset 545406840 remains immutable.
Separate Release **384399324**, archive asset **549697344**.
Tag: `student5-minilm-40k-phase-a-fp32-working-copy-cp45`.
Tag source commit: `2bf43b6ce92436fbab0cb04580fc1f51f0a1fd0a`.
Filename: `student5-minilm-40k-phase-a-fp32-working-copy-cp45.zip`.
Release: https://github.com/MATRIXNEO23/matrix-understanding-lab/releases/tag/student5-minilm-40k-phase-a-fp32-working-copy-cp45
Archive: https://github.com/MATRIXNEO23/matrix-understanding-lab/releases/download/student5-minilm-40k-phase-a-fp32-working-copy-cp45/student5-minilm-40k-phase-a-fp32-working-copy-cp45.zip
Archive bytes 88361246; SHA-256
`7804bfb245b71df9b835fff7ee00f6ec887e019772ae34c82d269d821d587191`.
Internal model/model.safetensors bytes 148020400; SHA-256
`d6e45891d1e0ec4ed023caaeb17c0dd0ae80a93b8bf877d275310b7f2837efa2`.

Complete source archive bytes copied to a new physical file and separate
Release asset. Sidecar MODEL_MANIFEST.json (asset 549697449) assigns its new
identity; original IDs inside the unchanged ZIP represent source provenance.
SHA256SUMS asset 549697459; RECOVERY.md asset 549697481; source copy proof
asset 549697495. All five assets recovered freshly and verified against
upload bytes; remote ZIP/model match source. No training occurred.

Future training may modify only an extracted working copy from this separate
locator. Never change original pristine files/Release. Preserve this initial
snapshot and publish trained outputs under new immutable identities.
Recovery: public HTTPS GET succeeded at CP45; authenticated Release UI is
fallback if needed. Download all five assets, check SHA256SUMS, extract into
a NEW empty working directory and verify internal SHA256SUMS.
Full evidence: `reports/evidence/student5-fp32-working-copy-cp45/`; report:
`reports/STUDENT_5_FP32_WORKING_COPY_CP45.md`.

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
