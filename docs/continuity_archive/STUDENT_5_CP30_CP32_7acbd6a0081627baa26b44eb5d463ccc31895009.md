# Student-5 continuity — current handoff and complete preserved history

Updated: 2026-09-07
Repository: `MATRIXNEO23/matrix-understanding-lab`
Active execution branch: `student5-path-b-v3`
Execution HEAD start: `aca5968bc26f8d4d4ef22327f0d225b9685e1474`
Latest completed checkpoint before CP32: `4c010cf99f022662394405870aaada0b043d84ff`
Production status: `NOT_PRODUCTION_APPROVED`
Current state: `GATE_A_BLOCKED_INPUT_ACCESS / PHYSICAL_MODEL_EXECUTION_NOT_STARTED`
Current result and exact remaining work: **Checkpoint 32** below. CP30 is retained as historical handoff.

## Complete continuity — no history discarded

The full preceding continuity file, checkpoints 1–29, is preserved byte-for-byte at:

[Full Student-5 checkpoints 1–29](continuity_archive/STUDENT_5_CP01_CP29_d1d4096c6df1c2331eabb33830f6edb577be053f.md)

Its Git blob is exactly `d1d4096c6df1c2331eabb33830f6edb577be053f`, the same blob returned for the prior canonical file. It retains all original requirements, authorizations, constraints, operations, results, source pins, model/tokenizer/corpus identities, artifact locations, defect inventories, guards and unfinished work. This is an immutable history archive, not a competing specification. Read it completely together with this current checkpoint and the canonical task before execution. Historical STOP/NOT_STARTED statements describe their checkpoint dates; the authorization below governs the next task.

No model, tokenizer, dataset, implementation, test, release or previous artifact is modified by this checkpoint. Only continuity documentation is updated; the previous continuity bytes are retained in the same commit.

## Checkpoint 30 — interruption, responsibility correction and Work handoff

### Owner direction

The owner accepted TASK 2.3 and explicitly said `via` to TASK 2.4 / continuation of Path B. The subsequent interruption, `ma non deve farlo work?`, clarifies execution responsibility: the substantive work belongs to Work, not to a duplicate implementation started in the supervisor chat.

- This chat: prepare a complete assignment, preserve continuity, review repository-visible results and defects, check scope and persistence, and report evidence honestly.
- Work: execute TASK 2.4, then the authorized Path-B workstream subject to its gates and stop conditions.
- Owner: launch/use the Work session with the prepared assignment; no model download, manual source copying or duplicate setup is requested.
- Authorization is already given. Do not ask the owner to approve the same task again merely because of this handoff.
- A prepared branch or prompt is NOT evidence that Work has started. No separate Work run/session identifier has been verified here.

### Exact interrupted operation and completed preparation

1. TASK 2.3 completion report was checked against commit `5e49a2d81ecf054a543e3e92f76260fafeca9cc6`; migration accepted within its structural/data scope.
2. Persistence policy saved in `docs/MODEL_ARTIFACT_PERSISTENCE_POLICY.md` at `bb706323c7391571bdc3de93122a249af850163d`, referenced from `PROJECT_WORK_RULES.md` at `8337ce51a3f1012bbe5e3c93f5ba249290d59071`.
3. Complete Work package saved in `prompts/WORK_STUDENT_5_PATH_B_V3_COMPLETION.md` at `9493e97cbdf5e731ee161b24d91b511076decb19`.
4. Branch `student5-path-b-v3` prepared at that package commit. Its HEAD was re-read during this interruption and is still `9493e97cbdf5e731ee161b24d91b511076decb19`.
5. The supervisor read `matrix_nlu/model_v3.py` and `matrix_nlu/export_onnx_v3.py` to inspect the handoff prerequisites. These were reads, not new implementation or model execution.
6. Owner interrupted before physical model loading/export/training. Supervisor execution stops here and the assignment is handed to Work.

No physical BERT load, forward, ONNX export, new training, optimizer, backpropagation, new benchmark or model publication was executed in the interrupted preparation. No new test PASS or model-quality metric is claimed.

### Work ledger

```text
executor = WORK
supervisor = THIS_CHAT
assignment = prompts/WORK_STUDENT_5_PATH_B_V3_COMPLETION.md
assignmentSourceCommit = 9493e97cbdf5e731ee161b24d91b511076decb19
executionRepository = MATRIXNEO23/matrix-understanding-lab
executionBranch = student5-path-b-v3
authorization = OWNER_GIVEN_VIA
workSessionId = NOT_REPORTED
workRunId = NOT_REPORTED
workStarted = NOT_VERIFIED
currentTask = TASK_2_4_PHYSICAL_V3_BERT_ONNX
TASK_2_4_RESULT = NOT_EXECUTED_HERE
TASK_3_TRAINING_RESULT = NOT_EXECUTED_HERE
```

The active branch above supersedes the task's older prepared `main` start-branch label. Work must fetch and inspect the existing `student5-path-b-v3` branch; never reset it to an older preparation SHA or overwrite intervening work. If Work has already started elsewhere, identify its actual branch/HEAD/run and reconcile before another execution. Never duplicate a live run.

## Accepted baseline and preserved inputs

### TASK 2.3

```text
checkpoint = 5e49a2d81ecf054a543e3e92f76260fafeca9cc6
verdict = TRAIN_V3_MIGRATION_PASS_WITH_NONBLOCKING_RISKS
artifactId = student5-matrix-nlu-v3-train-v1
locator = data/student5_v3/
rows = 3150
claims = 3990
retention = 100 percent
reportedSafeTests = 56/56 PASS
reportedStructuralViolations = 0
reportedTargetBuilderRows = 3150/3150 PASS
reportedInvalidPointers = 0
reportedForbiddenV2Sentinels = 0
reportedMissingRequiredAnchors = 0
logicalDatasetSha256 = 1118a900026f48cfcc290c3f9dc52a1a019a6a1f4761661f326c33770523140e
migrationManifestSha256 = 87b4a43035d2e3d84a6d599e1f81b497af6e2f36e4ef2c470adb87341c17da98
DEVUsedInTask2_3 = false
FrozenReadInTask2_3 = false
trainingExecutedInTask2_3 = false
```

These are preserved TASK 2.3 results, not tests rerun during this handoff. Do not redo the migration. Zero missing required anchors does not prove advanced temporal coverage: those relation categories were absent.

### Student-5 pristine FP32 40k — immutable Path-B base

```text
releaseTag = student-5-minilm-40k-phase-a-pristine
releaseId = 383143636
assetId = 545406840
assetName = student5-minilm-phase-a-pruned-40k.zip
archiveBytes = 88361246
archiveSha256 = 7804bfb245b71df9b835fff7ee00f6ec887e019772ae34c82d269d821d587191
modelBytes = 148020400
modelSha256 = d6e45891d1e0ec4ed023caaeb17c0dd0ae80a93b8bf877d275310b7f2837efa2
layers = 12
hiddenSize = 384
vocabSize = 40000
```

### Student-5 Path A — completed untaught runtime probe, preserve separately

```text
releaseTag = student-5-minilm-40k-untaught-int8-runtime-probe
releaseId = 383162517
assetId = 545486429
archiveBytes = 142463548
archiveSha256 = 72eea0af4211959bdbc92be36387faf5b85da957830f9be0a6d0dd50ab7cedf6
int8Bytes = 84457299
int8Sha256 = f58463a6d1f4daca2e58c8e40f7f6d1cbaa7d107e9534160278bc46552e0304a
status = RUNTIME_PROBE_ONLY / NOT_MATRIX_NLU / NOT_PRODUCTION_APPROVED
```

Do not train from Path A. The listed artifact identities are preserved registry/history values; this handoff did not re-download or rehash the binaries. Work must verify them before use.

Student-4-v2.2A stays the separate comparative baseline. Student-5 Path B is the primary continuation candidate. Neither the no-overwrite rule nor one-student-at-a-time rule is a reason to silently return to Student-4 development. See `docs/STUDENT_ARTIFACT_REGISTRY.md` and the full continuity archive for Student-4 run/artifact/digest identities.

## Exact remaining work, in dependency order

1. **Work pickup and preservation preflight.** Read the mandatory documents in the prepared task, this current checkpoint and its complete history archive. Record real branch/HEAD, workspace state, executor/run ID and authorization. Verify preserved source identities and persistent storage availability without overwriting anything.
2. **TASK 2.4 / Gate A.** Load the real pristine 40k BERT/tokenizer; attach the existing V3 16 conceptual heads (6 token + 10 sequence, including independent `sourceReferent`); run real forward; export through the V3 exporter contract; ONNX checker/load/forward; compare PyTorch/ONNX tensors and shapes, pointer masks/dynamic dimensions and contract fingerprint. Preserve any retained untrained structural export under a new name. Untrained heads and synthetic inputs prove runtime mechanics only, not linguistic comprehension.
3. **Gate-A blocker handling.** Report and preserve the first actual runtime/contract failure; do not conceal it or train around a broken interface. The prepared task's STOP policy applies. Gate A passing permits continuation to Gate B within the already-authorized assignment, not an automatic claim that the model is complete.
4. **Path-B training readiness.** Verify V3 training data and evaluation compatibility. Address documented coverage needs only through new versioned TRAIN-only artifacts with provenance. Preserve v1. Before training/selection, identify permitted V3 DEV data, evaluation boundaries and acceptance criteria without rewriting canonical DEV or opening Frozen. If the needed evaluation contract is missing, report that blocker rather than inventing an equivalence to V2.
5. **TASK 3 / Gate B training.** Start from pristine FP32 lineage. Follow the existing escalation ladder: frozen backbone + heads, then stronger small heads/adapters if justified, then last 1–2 layers, then 3–4, full fine-tuning only as last resort with evidence. Each meaningful run retains configuration, source and dataset hashes, checkpoint, metrics and error analysis. Compare Student-4 only on semantically comparable outputs; never fabricate V3 fields for that baseline.
6. **Quality loop.** Real raw input -> real NLU -> actual decoded V3 -> independent expected/actual comparison, per language/family. DEV error analysis -> new TRAIN-only repair -> new candidate -> identical retest/regression. No regex substitute for learned linguistic understanding; no gate lowering; no proof from an aggregate score alone.
7. **Gate C.** Lock and persist the taught FP32 candidate only after the specified quality criteria and critical-family checks, with residual errors explicit.
8. **Gate D.** Export taught FP32; validate numerical and decoded semantic parity; quantize a separate candidate with protected semantic heads as the initial policy; compare quality and runtime including IT/EN/ES, negation, source/perspective, referents, time, multi-claim and relevant consent/refusal/withdrawal language. Preserve FP32 and all retained INT8/mixed candidates separately.
9. **Gate E.** Apply the prepared assignment's final Frozen policy only after the final candidate and all tuning/quantization decisions are locked. Frozen is never a training, selection, repair or calibration source. Stop on final failure; no repeated tuning on Frozen.
10. **Durable closeout and supervisor review.** Verify repository-owned binary recovery, independent readback/checksums, manifests, lineage, reports and complete remaining work. No Assembling integration, phone build or production promotion in this workstream. Supervisor audits actual results before any later integration assignment.

### Known unresolved prerequisites/risks — do not omit

- Physical BERT/V3 load and physical V3 ONNX export/load remain unexecuted prerequisites after TASK 2.3.
- Current v1 TRAIN: BELIEF 0, COMMAND 0, REPORT/source attribution 8 Italian-only claims, advanced temporal relations 0, withdrawal 1 Italian example.
- Five-role UNKNOWN/AMBIGUOUS gold coverage is absent in the migration report; recorded token/span arrays alone do not prove multi-span learning coverage.
- 1,561 repeated text instances require explicit duplicate/leakage handling; no reported conflicting gold for identical text does not establish generalization.
- Migration structural validity is not annotation-quality, learned-quality or runtime evidence. Do not relabel these coverage gaps as solved merely because the migration passed.

## Persistence, interruption and scope guards

Use `docs/MODEL_ARTIFACT_PERSISTENCE_POLICY.md` and the prepared task as binding instructions. Preserve pristine, Path A, Student-4, each retained Path-B candidate/checkpoint, FP32/INT8 export and dataset version under distinct IDs/names/tags and SHA-256. Registered bytes must not change in place. No force-push/reset, asset replacement or silent `latest` overwrite. A pointer or expiring Actions artifact alone is not a durable model backup.

On each meaningful checkpoint or interruption save completed work AND all remaining substeps, pending tests/fixes/regressions, current run/config/dataset, errors and exact resume action before unrelated work. Preserve historic evidence; never replace an old result with a new claim.

The supervisor must not start duplicate implementation, training or export while Work owns execution. Until a run/commit/checkpoint is observed, status remains **assignment authorized/prepared, execution not verified started**. Do not claim background monitoring or future delivery.

## Immediate next action

Deliver the existing assignment to Work on `student5-path-b-v3`, together with this continuity entry. Start at TASK 2.4, not TASK 2.3 and not direct training. The owner has already authorized continuation; Work must obey its gates, preserve versions persistently and report its actual execution identity and results. No action is requested from the owner to download model bundles or recreate source files.

## Checkpoint 31 — Work pickup and Gate-A preservation preflight

Date: 2026-09-07. Executor: Codex Work, current interactive execution (not an Actions run).
Local execution label: `student5-path-b-v3-preflight-20260907-aca5968`.

```text
executionBranch = student5-path-b-v3
HEAD_start = aca5968bc26f8d4d4ef22327f0d225b9685e1474
activeTask = TASK_2_4_PHYSICAL_V3_BERT_ONNX
activeOperation = GATE_A1_INPUT_AND_ENVIRONMENT_PREFLIGHT
TASK_2_3 = ACCEPTED_NOT_REPEATED
workStarted = true (repository/environment preflight only)
physicalModelLoadStarted = false
trainingStarted = false
actionsRunsOnExecutionBranchObserved = 0
```

Read the complete current continuity and immutable CP01–29 archive, all ten mandatory package sources, and the adult/intimacy coverage policy. Inspected the actual `model_v3.py` adapter and `export_onnx_v3.py` structural export specification at the start commit. Repository tree metadata contains no AGENTS.md. No dataset partition was opened.

The canonical release asset `545406840` remains present, uploaded, 88,361,246 bytes, with GitHub digest `sha256:7804bfb245b71df9b835fff7ee00f6ec887e019772ae34c82d269d821d587191`. This is **remote metadata evidence, not an independent binary checksum verification**. Direct unauthenticated archive access from the local runtime returned HTTP 404. The configured GitHub fetch connector can read the private repository and release metadata but explicitly cannot download non-UTF-8 release binaries; its binary-download operation supports Actions artifacts, not Release assets. No credentials were extracted or repurposed.

Local Python is 3.12.13. Module discovery found no torch, transformers, onnx, onnxruntime or sentencepiece. PyPI is reachable (HTTP 200), so missing packages alone are potentially installable and are not evidence of a network-wide denial. The named pristine archive/model was not located by filename search in the current workspace, /tmp or installed runtime tree. Older workspace directories were left untouched.

Next operation: record the exact input-access/runner evidence and either proceed through a normally configured authenticated binary path, or preserve a Gate-A BLOCKED report if none is usable. Do not build from upstream, regenerate pristine, substitute Path A, use structural tests as physical evidence, or train around Gate A.

Guards at this checkpoint: DEV unread/unused; Frozen unread; Student-4 unchanged; pristine unchanged; Path A unchanged; TRAIN v1 unchanged; no model forward/optimizer/backprop/training/quantization; no other repository modified. Mandatory remaining work is still the complete Gate-A A1–A4 sequence, then readiness and Gates B–E described above.

## Checkpoint 32 — Gate-A input-access STOP, no training

Date: 2026-09-07. Branch: `student5-path-b-v3`.
HEAD start: `aca5968bc26f8d4d4ef22327f0d225b9685e1474`.
Previous persisted checkpoint: `4c010cf99f022662394405870aaada0b043d84ff`.
HEAD final: the Git commit introducing CP32 and its report (recorded in the final handoff); no self-referential SHA is invented.

```text
activeTask = TASK_2_4_PHYSICAL_V3_BERT_ONNX
workstreamStatus = GATE_A_BLOCKED_INPUT_ACCESS
firstFailingLayer = A1_CANONICAL_PRISTINE_BINARY_ACQUISITION
physicalBertLoad = NOT_EXECUTED
physicalOnnxExportLoad = NOT_EXECUTED
TASK_2_3 = ACCEPTED_NOT_REPEATED
TASK_3_TRAINING = NOT_STARTED
Gates_B_C_D_E = NOT_STARTED
workstreamComplete = false
```

The canonical pristine Release asset is present, uploaded and metadata-matching, but this runtime has no configured authenticated Release-binary download/publication operation. Direct private Release URL returned 404; authenticated connector supplies metadata and explicitly does not handle Release binary bytes. No credentials were extracted or repurposed. Local archive/model SHA verification is **not performed**. Missing Torch/Transformers/ONNX dependencies remain uninstalled; PyPI is reachable, so dependency absence is not the primary access blocker.

The existing main Actions run `34080903226` has a failed job with no steps/runner name. Its detailed annotations endpoint was rejected by the connector allowlist. Cause is unverified; do not assert billing failure. No new job was launched; no workflow was created or rerun. No alternate route bypassing access restrictions was attempted.

Persistent evidence:

- [Gate-A preflight report](../reports/STUDENT_5_PATH_B_GATE_A_PREFLIGHT_20260907.md)
- [Machine-readable diagnostics](../reports/evidence/student5-path-b-gate-a-preflight-20260907/diagnostics.json)
- [Checksums](../reports/evidence/student5-path-b-gate-a-preflight-20260907/SHA256SUMS)
- Report SHA-256: `a0f6dd80eb8af4d1ce1d91988a24c106fa27092dd1672e12683b97a370b62b41`.
- Diagnostics SHA-256: `31e77f72aa9e403116002b232b38830c962dd91dcaf103e668aac04c4bad7319`.

No new candidate/model artifact exists. The artifact registry and all previously preserved versions are unchanged. The only repository changes in this execution are current Student-5 continuity and new preflight diagnostics/report/checksums; the CP01–29 archive stays byte-identical. No physical test PASS or learned-quality result is claimed.

### Remaining prerequisites and exact resumption

1. Supply a normally configured authenticated Release-binary acquisition/publication capability to the execution environment; the workstream is already authorized, so do not ask for duplicate task approval or manually recreate pristine.
2. Resume A1 at the actual latest branch HEAD: exact pristine archive/internal checksums, TRAIN-v1 checksum verification (not migration), separate immutable source/output locations.
3. Install isolated pinned runtime; A2 real pristine BERT/V3 construction and forward; A3 physical ONNX using existing export contract, all tensors/masks/dynamic shapes/fingerprint and numerical parity; A4 durable distinct retained artifact.
4. If A passes, continue automatically under the assigned package to Gate-B readiness: establish permitted V3 DEV identity and gate/evaluator compatibility before training or selection. Do not invent V2 equivalence.
5. Continue actual frozen-backbone-first training, independent DEV analysis, versioned TRAIN repairs, capacity escalation only with evidence and durable previous candidates; then taught FP32 lock, taught ONNX and protected-head quantization/parity/runtime persistence.
6. Frozen remains unread until the package's final locked-candidate one-shot gate; no Frozen feedback. No Assembling or production promotion.

Carry forward all previously documented coverage gaps and both physical-environment P1 items as OPEN. No model/source/dataset/evaluator changes were made to hide them.

```text
Student-4 changed = false
DEV used = false
Frozen read/tokenized/analyzed/predictionsRead = false
Path A modified = false
pristine40kModified = false
TRAIN v1 modified = false
Path B training started = false
optimizerCreated = false
backpropExecuted = false
teachingExecuted = false
trainingExecuted = false
quantizationExecuted = false
otherRepositoriesModified = false
productionPromotionExecuted = false
NEXT = RESTORE AUTHENTICATED BINARY EXECUTION CAPABILITY, THEN RESUME GATE A1
```

STOP with explicit owner-facing report. No background work or future automatic delivery is promised.

