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
