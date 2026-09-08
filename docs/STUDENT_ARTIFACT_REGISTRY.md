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
