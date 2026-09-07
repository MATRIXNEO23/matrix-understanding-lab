# WORK — STUDENT-5 PATH B MATRIX-NLU V3 COMPLETION

Status: **PREPARED / DO NOT EXECUTE UNLESS OWNER LAUNCHES AND AUTHORIZES THIS WORKSTREAM**  
Repository: `MATRIXNEO23/matrix-understanding-lab`  
Expected start branch: `main`  
Prepared start HEAD: `8337ce51a3f1012bbe5e3c93f5ba249290d59071`

## Mission

Complete Student-5 Path B from the exact preserved checkpoint after TASK 2.3, without restarting Student-5, without modifying Path A, without modifying Student-4, and without overwriting any existing artifact.

Target end state:

```text
Student-5 pristine 40k FP32
-> physical V3 BERT/model load
-> physical V3 16-head ONNX export/load/forward closure
-> Matrix-NLU V3 teaching/training
-> DEV evaluation + error mining + TRAIN-only repair loop
-> lock best taught FP32 candidate
-> export taught FP32 ONNX
-> quantize taught candidate using evidence-backed policy
-> FP32/quantized parity + runtime/regression
-> persist every retained version/checkpoint immutably in repository-owned storage
-> STOP with evidence; no automatic production promotion or Assembling integration
```

## Mandatory read order

Before any model operation read completely:

```text
PROJECT_WORK_RULES.md
docs/MODEL_ARTIFACT_PERSISTENCE_POLICY.md
docs/WORK_CONTINUITY_STUDENT_5.md
docs/STUDENT_ARTIFACT_REGISTRY.md
ARCHITETTURA.md
docs/MATRIX_NLU_CONTRACT_V3.md
reports/STUDENT_5_TRAIN_V3_MIGRATION.md
reports/STUDENT_5_15_HEAD_CONTRACT_AUDIT.md
reports/STUDENT_5_CONTRACT_REPAIR_DESIGN.md
prompts/WORK_STUDENT_5_ADULT_INTIMACY_ADDENDUM.md
```

The persistence policy is owner-mandated and binding. A task that produces a model is not closed while its only copy is a temporary GitHub Actions artifact.

## Immutable preserved inputs

### Student-5 pristine 40k

```text
releaseTag = student-5-minilm-40k-phase-a-pristine
releaseId = 383143636
assetId = 545406840
asset = student5-minilm-phase-a-pruned-40k.zip
archiveBytes = 88361246
archiveSha256 = 7804bfb245b71df9b835fff7ee00f6ec887e019772ae34c82d269d821d587191
modelBytes = 148020400
modelSha256 = d6e45891d1e0ec4ed023caaeb17c0dd0ae80a93b8bf877d275310b7f2837efa2
vocabSize = 40000
layers = 12
hiddenSize = 384
status = PRISTINE_PHASE_A_BACKBONE / NOT_MATRIX_NLU / NOT_PRODUCTION_APPROVED
```

This is the canonical Path-B training base. Verify every checksum before use. Do not mutate it.

### Student-5 Path A — preserve read-only

```text
logicalName = STUDENT_5_40K_UNTAUGHT_INT8
releaseTag = student-5-minilm-40k-untaught-int8-runtime-probe
releaseId = 383162517
assetId = 545486429
asset = student-5-minilm-40k-untaught-int8-runtime-probe.zip
pathAInt8OnnxBytes = 84457299
pathAInt8OnnxSha256 = f58463a6d1f4daca2e58c8e40f7f6d1cbaa7d107e9534160278bc46552e0304a
status = RUNTIME_PROBE_ONLY / NOT_MATRIX_NLU / NOT_PRODUCTION_APPROVED
```

Path A is reference-only for deployment/runtime lessons. Never use Path A INT8 as a training base. Never overwrite it.

### Student-4 baseline — preserve read-only

Student-4-v2.2A remains a comparative/regression baseline. Do not mutate, discard, rename over, or auto-replace it.

### Canonical V3 TRAIN artifact

```text
artifactId = student5-matrix-nlu-v3-train-v1
contract = MATRIX_NLU_CONTRACT_V3
contractFingerprint = 7b0646e44243ad897760c0fcadbe141f1b8e88e3fd8d63a1789106571b9987b0
locator = data/student5_v3/
rows = 3150
claims = 3990
datasetLogicalSha256 = 1118a900026f48cfcc290c3f9dc52a1a019a6a1f4761661f326c33770523140e
migrationManifestSha256 = 87b4a43035d2e3d84a6d599e1f81b497af6e2f36e4ef2c470adb87341c17da98
structuralViolations = 0
targetBuilderRows = 3150/3150 PASS
safeRegressionTestsAtTask2_3 = 56/56 PASS
```

TRAIN source is immutable. Repairs/augmentations, when justified by DEV error analysis, must be new TRAIN-only versioned artifacts with new IDs/checksums. Never overwrite `student5-matrix-nlu-v3-train-v1`.

## Contract target

Matrix-NLU V3 is frozen at:

```text
16 conceptual heads = 6 token + 10 sequence
```

Token heads:

```text
boundary
object
subject
negation
 temporal
entity
```

Sequence heads:

```text
dialogueAct
predicate
subjectReferent
targetReferent
ownerReferent
perspectiveReferent
sourceReferent
polarity
temporalRelation
claimKind
```

The runtime must preserve independent source/perspective roles, cue-only negation evidence, temporal relation/anchor semantics, candidate-pointer referents, field statuses, confidence/abstention and multi-claim decomposition. Do not reintroduce V2 sentinels or linguistic regex parsing.

---

# GATE A — TASK 2.4 PHYSICAL V3 MODEL/ONNX CLOSURE

TASK 2.4 is the exact next task recorded after TASK 2.3.

## A1. Verify immutable inputs

Before model load:

```text
verify main HEAD and working tree
verify pristine Release locator and SHA-256
verify V3 TRAIN artifact checksums without modifying it
verify Path A unchanged
verify Student-4 unchanged
verify Frozen unread
```

Create a new Path-B working/output directory. Never reuse Path-A output directories.

## A2. Physical Student-5 BERT/V3 load

Use the real pristine 40k BERT model with the implemented Student-5 V3 adapter in `matrix_nlu/model_v3.py`.

Prove, with a real forward pass:

```text
pristine tokenizer/model load PASS
BERT adapter load PASS
16-head V3 model construction PASS
candidate-pointer dimensions valid
real forward PASS
all expected tensor shapes recorded
no unexpected head/contract drift
```

No optimizer, backprop or training in this sub-gate.

## A3. Physical V3 ONNX export/load

Use the existing V3 export contract, not a parallel custom exporter.

Required evidence:

```text
opset recorded
inputs/outputs recorded
16 conceptual heads / expected tensors present
onnx checker PASS
ONNX Runtime load PASS
real forward PASS
sourceReferent output physically present
no custom/unexpected unsupported operator blocker
output shapes match the PyTorch V3 model
contract fingerprint guard PASS
```

Perform PyTorch-vs-ONNX numerical/parity checks on training-safe probes. Do not use Frozen.

## A4. Gate-A persistence

If the physical V3 FP32 export is retained for comparison or becomes a training/export reference, persist it as a uniquely named repository-owned artifact with:

```text
new logical artifact ID
new version name
SHA-256
byte size
source pristine artifact ID
contract fingerprint
commit/run provenance
persistent Release/LFS locator
manifest/registry entry
```

Never overwrite Path A FP32/INT8 exports.

## Gate-A decision

If a genuine architecture/contract/runtime blocker exists:

```text
STOP
preserve diagnostics + artifact/checksum if useful
record first failing layer and root cause
update continuity
DO NOT train around a broken export contract
```

If Gate A passes, continue automatically inside this authorized workstream to Gate B. Do not stop merely because TASK 2.4 historically had an owner-review boundary; this combined package exists specifically to complete Path B when the owner launches/authorizes it.

---

# GATE B — TASK 3 PATH-B MATRIX-NLU V3 TEACHING/TRAINING

## B1. Training start point

Start from the pristine Student-5 40k FP32 lineage, never Path A and never a quantized model.

Initial capacity strategy follows the approved escalation ladder:

```text
A. frozen 12-layer backbone + Matrix V3 heads
B. stronger/small head MLP or lightweight adapter capacity if evidence requires
C. unfreeze last 1–2 encoder layers if required
D. unfreeze last 3–4 encoder layers if required
E. full fine-tuning only as last resort and only with regression evidence
```

Do not jump directly to full fine-tuning.

Every escalation must preserve its prior best candidate as an immutable artifact/checkpoint before proceeding.

## B2. Training/evaluation loop

For every meaningful attempt:

```text
TRAIN
-> DEV evaluation
-> per-language + per-family error taxonomy
-> actual root-cause analysis
-> TRAIN-only repair/hard-example generation if justified
-> new versioned TRAIN artifact
-> retrain/new candidate
-> compare against previous Student-5 candidate
-> compare against Student-4-v2.2A baseline where contract comparison is meaningful
-> preserve best/meaningful candidates persistently
```

No DEV example may be copied into TRAIN. Frozen remains closed until the final candidate is locked.

## B3. Critical semantic families

Evaluate separately, not hidden inside a global score:

```text
negation
negation cue spans independent of polarity
temporal CURRENT/PAST/FUTURE and advanced relations when supported by evidence
subject/target/owner/perspective/source referents
source != perspective reports
ownership
third-party/report
belief/hypothesis
request
command
correction
goal/desire
span decoding
entity spans
multi-claim
ambiguity/abstention
IT
EN
ES
code-switch
colloquial/noisy input
adult/intimacy: consent, refusal, withdrawal, desire, boundaries
```

Hard invariants:

```text
ownership corruption = 0 on required gate set
invented World Truth = 0
no downstream-state fields emitted by NLU
```

Adult/intimacy content alone must never trigger a confidence penalty, semantic degradation or moderation label. Only adult material is allowed in authored training/probe data.

## B4. Known TRAIN coverage risks from TASK 2.3

Do not hide these:

```text
BELIEF = 0 in current V3 TRAIN
COMMAND = 0
REPORT/source attribution = 8 claims, IT only
advanced temporal BEFORE/AFTER/DURING/RECURRENT/AT_REFERENCE = 0
adult withdrawal = 1 IT claim
repeated text instances = 1561
```

Before training or during the first DEV/error-analysis cycle, determine which gaps materially block the required contract. If augmentation is needed, create a **new TRAIN-only dataset version**, with provenance and checksums, without changing the canonical v1 artifact.

Do not fabricate labels from unsupported text. Prefer balanced authored TRAIN-only examples plus controlled validation when provenance/license permit.

## B5. Confidence/calibration

Confidence is part of the contract.

```text
calibrate on allowed DEV only
critical uncertain fields must abstain/fail closed
no threshold tuning on Frozen
record per-head/per-family calibration evidence
```

Do not lower gates to obtain PASS.

## B6. Candidate preservation after each escalation

Any candidate used to justify an architectural/capacity decision must be persisted before moving on.

Minimum immutable artifacts:

```text
Path-B training base manifest
best frozen-backbone candidate if evaluated
best enhanced-head/adapter candidate if evaluated
best partially-unfrozen candidate if evaluated
locked taught FP32 model
locked taught FP32 ONNX export
quantized candidate(s) used in parity/runtime comparison
final selected candidate
```

Do not persist every transient optimizer step unless needed, but never delete/overwrite a registered comparison candidate without explicit owner authorization.

---

# GATE C — TAUGHT FP32 LOCK

Lock a taught FP32 candidate only when DEV evidence shows no critical systematic failure remaining within the accepted gate definition.

Before lock record:

```text
exact training config
base artifact ID
TRAIN dataset ID/SHA
DEV evaluation identity
per-language metrics
per-family metrics
error taxonomy
known residual defects
checkpoint/model SHA-256
reason for selecting this candidate over previous Student-5 candidates and Student-4 baseline
```

Persist the locked FP32 model permanently in repository-owned storage with unique release/tag/version.

Frozen remains unread until this lock is complete.

---

# GATE D — TAUGHT EXPORT + QUANTIZATION

## D1. FP32 ONNX

Export the locked taught FP32 candidate using the V3 exporter.

Required:

```text
checker/load/forward PASS
PyTorch-vs-ONNX semantic/parity PASS under defined gates
all 16 heads preserved
contract fingerprint preserved
runtime/output tensor census recorded
persistent unique artifact
```

## D2. Quantization

Use an evidence-backed mobile-oriented policy. Initial default from prior Matrix work is encoder INT8 with critical semantic heads preserved in FP32, but do not copy Student-4's recipe blindly if the Student-5 graph requires a better policy.

For every quantized candidate compare against taught FP32:

```text
size
operator coverage
load/forward
latency/RSS where measurable
per-head output parity
semantic decoded parity
negation
referents/source/perspective
temporal
multi-claim
IT/EN/ES/adult/code-switch slices
```

A smaller artifact that breaks a critical semantic family is not accepted.

Persist each retained quantized candidate immutably with a new version and SHA-256. Never overwrite the taught FP32 export.

---

# GATE E — FINAL EVALUATION / FROZEN POLICY

Frozen may be opened only after one candidate is locked and all tuning decisions are frozen.

Rules:

```text
one final Frozen evaluation for the locked candidate path
no Frozen-driven retraining
no Frozen-driven threshold tuning
no hard-example mining from Frozen
record exact Frozen run identity and result
```

If Frozen fails, report failure and stop. Do not silently iterate on Frozen.

Physical Moto integration remains separate from this NLU workstream unless the owner explicitly extends scope. Do not modify Assembling or Android repos here.

---

# PERSISTENCE / NON-OVERWRITE GATE — MANDATORY THROUGHOUT

Binding policy:

```text
docs/MODEL_ARTIFACT_PERSISTENCE_POLICY.md
```

For every retained artifact:

```text
unique logical ID
unique filename/version/tag
bytes
SHA-256
parent/base lineage
training data provenance if trained
training/export/quantization config
commit/workflow/run identity
persistent repository-owned locator
registry entry
continuity checkpoint
```

Allowed durable binary storage:

```text
Git-tracked file when small enough
Git LFS when appropriate
GitHub Release asset in MATRIXNEO23/matrix-understanding-lab
```

Not sufficient:

```text
GitHub Actions artifact only
local workspace only
/tmp only
unnamed latest file
pointer without recoverable binary
```

Never overwrite:

```text
Student-5 pristine
Path A artifacts
Student-4 baseline
prior Path-B checkpoints/candidates
prior datasets
prior FP32 exports
prior INT8 exports
release tags or registered filenames with different bytes
```

If storage pressure occurs, STOP and request owner authorization before deleting/pruning any registered artifact.

---

# Forbidden scope

Do NOT:

```text
modify MATRIXNEO23/assembling
modify MATRIXNEO23/memoria
modify Android/game/affective repositories
integrate Student-5 into the engine in this workstream
overwrite Student-4
modify Path A
train from Path A INT8
modify pristine 40k in place
lower quality gates
use Frozen for tuning
invent unsupported V3 labels
replace learned linguistic failures with regex parser patches
auto-promote to production
```

---

# Mandatory continuity

Update `docs/WORK_CONTINUITY_STUDENT_5.md` after:

```text
Gate A physical load/export
training start
any meaningful training attempt
any dataset repair/version
capacity escalation
candidate lock
FP32 export
quantization
DEV/Frozen evaluation
artifact publication/checksum
before any risky/long operation
before STOP/session end
```

Every checkpoint must include repo/branch/HEAD, active task, artifact IDs/checksums/locators, training/data config, tests/results, defects, exact remaining work and exact next action.

---

# Closure definition

This workstream may be reported COMPLETE only when all of the following are true:

```text
physical Student-5 V3 BERT load demonstrated
physical 16-head V3 ONNX export/load/forward demonstrated
Student-5 Path B actually trained as Matrix-NLU V3
DEV per-language/per-family error analysis completed
observed systematic defects fixed through TRAIN-only/evidence-backed work
best taught FP32 candidate locked and persisted
FP32 ONNX export persisted
quantized runtime candidate persisted
quantized-vs-FP32 semantic/parity/runtime evidence recorded
no critical systematic semantic failure remains under the accepted gates
Frozen handled according to one-shot policy if final gate is authorized/reached
Student-4 unchanged
Path A unchanged
pristine unchanged
all retained versions persistently recoverable in this repository
no artifact overwritten
registry + SHA-256 + lineage + continuity complete
```

Final status must distinguish explicitly:

```text
TRAINED_MATRIX_NLU_V3
EXPERIMENTAL_TEST_CANDIDATE / PRODUCTION status as actually earned
NOT_PRODUCTION_APPROVED unless all production gates truly pass
```

STOP after Path-B completion evidence. Do not integrate into Assembling automatically.
