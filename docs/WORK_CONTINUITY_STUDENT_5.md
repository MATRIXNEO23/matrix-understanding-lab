# Student-5 continuity — MiniLM deep vocabulary pruning

Repository: `MATRIXNEO23/matrix-understanding-lab`  
Branch: `main`  
Phase: `PHASE_A_VOCABULARY_PRUNING_FEASIBILITY`  
Production status: `NOT_PRODUCTION_APPROVED`

## Canonical authority

- Phase-A execution prompt: `Pasted markdown(2).md`, received 2026-09-04 and treated as the controlling prompt.
- Repository prompt: `prompts/WORK_STUDENT_5_MINILM_IT_EN_ES_PRUNED.md`.
- Mandatory addendum: `prompts/WORK_STUDENT_5_ADULT_INTIMACY_ADDENDUM.md`.
- Adult/intimacy policy: `docs/ADULT_INTIMACY_NLU_COVERAGE.md`.
- Starting repository HEAD: `447bd5128a52433d7094b35b401eb3fa3d9fd932`.

The controlling Phase-A prompt overrides the older repository prompt only where the latter would automatically continue into Phase B. This execution stops after the Phase-A GO/STOP decision and does not teach Matrix heads, fine-tune MiniLM, quantize Student-5, read Frozen, or integrate into Assembling.

## Immutable boundaries

```text
student4V22AChanged = false
canonicalDevUsedForVocabularySelection = false
frozenDataRead = false
frozenDataTokenized = false
frozenDataAnalyzed = false
teachingExecuted = false
matrixHeadsTrained = false
quantizationExecuted = false
productionPromotionExecuted = false
```

Only Matrix TRAIN, Matrix v2 TRAIN, v2.2A TRAIN-only repair, and MASSIVE TRAIN IT/EN/ES may enter vocabulary selection. Probe material must be separate and training-safe.

## Checkpoint 1 — upstream pin and execution start

Timestamp: `2026-09-04T17:18Z`

```text
repository = microsoft/Multilingual-MiniLM-L12-H384
revision = 6e8c1ec6b4ec4e3fc6eb7d2cd834fcd582b61daf
license = MIT
modelTypeExpected = bert
tokenizerClassExpected = XLMRobertaTokenizer
vocabSizeExpected = 250037
hiddenSizeExpected = 384
layersExpected = 12
attentionHeadsExpected = 12
intermediateSizeExpected = 1536
```

The official model card confirms that the checkpoint uses `BertModel` with `XLMRobertaTokenizer` and warns that `AutoTokenizer` is not valid for this checkpoint. The exact token-ID/embedding-row relationship remains a fail-closed audit item and must pass before any pruned artifact can be accepted.

Current activity: create the pinned local environment, retrieve exact upstream files, audit configuration/tokenizer/special-token mapping, and count model/embedding/Transformer parameters.

Next checkpoint: after deterministic tokenizer/embedding alignment and upstream integrity are verified.


## Checkpoint 2 — upstream alignment and TRAIN-only corpus complete

Timestamp: `2026-09-04T17:27Z`

Upstream audit:

```text
revision = 6e8c1ec6b4ec4e3fc6eb7d2cd834fcd582b61daf
modelType = bert
tokenizerClass = XLMRobertaTokenizer
sentencePiecePieces = 250000
tokenizerVocabSize = 250002
modelEmbeddingRows = 250037
reachableTokenizerIds = 0..250001
unreachableTrailingEmbeddingRows = 35
totalParameters = 117653760
wordEmbeddingParameters = 96014208
allEmbeddingParameters = 96212352
transformerParameters = 21293568
poolerParameters = 147840
upstreamPytorchBytes = 470657952
upstreamPytorchSha256 = cce170910f4d4f3b45be025508f51ef1ad6a1de69f2d46dce7e4603ad31aaaeb
sentencePieceSha256 = cfc8146abe2a0488e9e2a0c56de7952f7c11ab059eca145a0a727afce0db2865
```

The tokenizer-to-embedding mapping is deterministic for every reachable ID: XLM-R special IDs are handled explicitly, ordinary SentencePiece pieces use the tokenizer's offset mapping, and the 35 unreachable trailing model rows are excluded. The upstream config declares `pad_token_id=0` while the tokenizer exposes `<pad>=1`; pruned artifacts will align config padding to ID 1 without modifying Transformer weights.

TRAIN-only vocabulary-selection corpus:

```text
records = 16819
sha256 = 2412a5727eb51b993f3172f3dc4a4d08199e16382b90c2e62e5080e3e23b8558
Matrix v1 TRAIN = 2991
Matrix v2 TRAIN = 2775
v2.2A repair TRAIN-only = 375
MASSIVE TRAIN IT = 3000
MASSIVE TRAIN EN = 3000
MASSIVE TRAIN ES = 3000
authored general coverage = 720
authored adult/intimacy coverage = 1206
authored control rows = 4
```

MASSIVE source archive:

```text
sha256 = 7df623fd2d300a4d235d6ee5bd396c9a28258d3a0ccb29abdb054506eba153f8
license = CC-BY-4.0
nonTrainJsonDecoded = false
```

The Matrix v2 reconstruction used only v1 TRAIN, v2 TRAIN-only migrations/additions, and the canonical TRAIN drop IDs from audit control metadata. Canonical dev/frozen texts were not opened, tokenized, analyzed, or used for vocabulary selection.

Current activity: build actual 40k/60k/80k/100k SentencePiece tokenizers and matching BERT embedding tables, then execute save/reload and all-ID alignment checks.


## Checkpoint 3 — four real pruning candidates built

Timestamp: `2026-09-04T19:34Z`

A protobuf compatibility error (`ModelProto.pieces_size`) was corrected to `len(ModelProto.pieces)`; this was an infrastructure-only fix before candidate construction. No data, gate, or selection policy changed.

```text
targetsBuilt = [40000, 60000, 80000, 100000]
allHuggingFaceSaveReloadChecks = PASS
allSpecialTokenChecks = PASS
allTokenizerEmbeddingAlignmentChecks = PASS
allNonEmbeddingWeightsBitExact = true
allObservedSelectionPiecesRetained = true
allUnkRatesIT_EN_ES_Adult = 0
semanticProbeSentences = 161
semanticContrastPairs = 36
canonicalDevUsed = false
frozenDataRead = false
```

Preliminary gate results:

| Vocab | FP32 model bytes | Est. runtime INT8 bytes | Gate |
|---:|---:|---:|---|
| 40k | 148,020,400 | 83,854,848 | PASS |
| 60k | 178,740,552 | 114,574,848 | PASS |
| 80k | 209,460,584 | 145,294,848 | PASS |
| 100k | 240,180,584 | 176,014,848 | FAIL size gate |

The smallest passing candidate is 40k. It has zero UNK on the separate IT/EN/ES/adult probe, mean token inflation 1.046/1.045/1.075 for IT/EN/ES, adult inflation 1.042, mean representation cosine 0.995580, worst cosine 0.943703, mean contrast delta 0.007855, p95 contrast delta 0.045259, and exact-forward delta 0 for unchanged tokenizations.

Current activity: independently verify every recorded checksum, prepare complete comparison reports, and package the selected Phase-A artifact. No Phase-B work is authorized.


## Checkpoint 4 — final Phase-A selection and preserved artifact

Timestamp: `2026-09-04T19:45Z`

Final decision:

```text
decision = PRUNING_CANDIDATE_SELECTED
selectedVocabSize = 40000
selectedModelSha256 = d6e45891d1e0ec4ed023caaeb17c0dd0ae80a93b8bf877d275310b7f2837efa2
selectedFp32ModelBytes = 148020400
selectedArtifactDirectoryBytes = 150116913
estimatedRuntimeInt8Bytes = 83854848
estimatedReductionVsStudent4Mixed = 43.988982%
archiveBytes = 88361246
archiveSha256 = 7804bfb245b71df9b835fff7ee00f6ec887e019772ae34c82d269d821d587191
status = NOT_PRODUCTION_APPROVED
frozen = FROZEN_UNREAD
```

Selection evidence:

- UNK IT/EN/ES/adult-intimacy: 0 for every slice.
- Aggregate token inflation: IT 1.037634, EN 1.037037, ES 1.066852, adult/intimacy 1.039074, code-switch 1.059406, names/locations 1.060606.
- Mean representation cosine: 0.995580; worst: 0.943703.
- Mean/p95 semantic-contrast cosine delta: 0.007855/0.045259.
- Exact-forward maximum delta on 103 unchanged-tokenization sentences: 0.
- Exact selection/probe text overlap: 0, enforced fail-closed.
- All recorded file sizes and SHA-256 values independently pass.
- All four Hugging Face artifacts reload, preserve 12 layers, align tokenizer and embeddings, and execute a real forward.
- Unit tests: 7/7 PASS.
- 60k and 80k also pass. 100k fails only the unchanged material-size gate.
- The 60k quality difference is small and does not justify 30,720,000 additional estimated runtime bytes over 40k.

The selected archive contains the model, real reduced tokenizer, bidirectional token-ID remap, aggregate and candidate manifests, corpus provenance, Frozen guard, reports, source, and `SHA256SUMS`. ZIP integrity and every internal checksum pass.

Repository implementation/report commits: `25546528917d42d70129f059ff56da672678c7d4`, corrected by `a1d407d63d4dcb84033d8ac525cce0e2475c27e1`.

Canonical report: `reports/STUDENT_5_MINILM_DEEP_PRUNING.md`. Compatibility report: `reports/STUDENT_5_MINILM_PRUNING_FEASIBILITY.md`.

Phase A stops here. Matrix teaching, the 15 Matrix heads, fine-tuning, canonical-dev downstream evaluation, quantization, Frozen access, Assembling integration, and production promotion remain unexecuted and require separate authorization.

## Checkpoint 5 — approved completion plan, execution NOT started

Timestamp: `2026-09-05`

Owner-approved direction: complete Matrix-NLU using Student-5 40k as the primary candidate while keeping Student-4-v2.2A as a frozen comparative baseline. Work execution has NOT started from this checkpoint; this section records the plan only.

### Repository and architecture boundary

Writable repository for this workstream:

```text
MATRIXNEO23/matrix-understanding-lab
```

Authoritative architecture file to read and respect before implementation:

```text
ARCHITETTURA.md @ main
```

Hard boundary:
- do not modify `assembling`;
- do not modify `memoria`;
- do not modify affective, game, historical or any other repository;
- other repositories may be read only when needed for compatibility context;
- all NLU code, training, tests, reports, artifacts and continuity updates stay in `matrix-understanding-lab`.

### Student roles

```text
Student-4-v2.2A
= preserved comparative baseline / regression reference
= do not discard
= do not auto-promote

Student-5 MiniLM 40k Phase-A artifact
= primary continuation candidate
= same pristine 40k base feeds two separate experimental paths
```

The two Student-5 paths must remain independent. Quantizing path A must never mutate or become the training base for path B.

### Path A — immediate untaught quantized runtime probe

Purpose: isolate deployment/runtime risk before spending training effort.

```text
Student-5 40k pristine Phase-A
→ no Matrix teaching
→ ONNX export
→ encoder INT8 / technically appropriate quantization
→ desktop/runtime verification
→ size / load / latency / memory measurements
→ optional late Android probe only if software/runtime checks justify it
```

Required status label:

```text
STUDENT_5_40K_UNTAUGHT_INT8
RUNTIME_PROBE_ONLY
NOT_MATRIX_NLU
NOT_PRODUCTION_APPROVED
```

Path-A results may justify export/runtime/infrastructure fixes, but its linguistic quality must not be used as evidence for Matrix-NLU capability or to contaminate Path-B training decisions.

### Path B — Matrix teaching and quality path

Start again from the same pristine Student-5 40k Phase-A artifact, never from the quantized Path-A artifact.

Target initial architecture: preserve the existing Matrix 15-head contract unless a contract audit proves a missing indispensable output.

Sequence heads:
- `sequence.dialogueAct`;
- `sequence.predicate`;
- `sequence.subjectReferent`;
- `sequence.targetReferent`;
- `sequence.ownerReferent`;
- `sequence.perspectiveReferent`;
- `sequence.polarity`;
- `sequence.temporalRelation`;
- `sequence.claimKind`.

Token/span heads:
- `token.boundary`;
- `token.subject`;
- `token.object`;
- `token.entity`;
- `token.negation`;
- `token.temporal`.

Confidence/calibration and claim decomposition are mandatory output behavior even if implemented without adding new learned heads.

### Capacity escalation policy

Do not jump immediately to full fine-tuning. Increase trainable capacity only when evidence requires it:

```text
A. frozen 12-layer backbone + Matrix heads
↓ if insufficient
B. stronger/small MLP or adapter capacity
↓ if insufficient
C. unfreeze last 1–2 encoder layers
↓
D. unfreeze last 3–4 encoder layers if justified
↓
E. full fine-tuning only as last resort with regression evidence
```

Every escalation must compare against the previous Student-5 configuration and Student-4-v2.2A baseline. Preserve capabilities already strong; do not trade one critical family for another silently.

### Priority linguistic families

Training/error-mining priority:
- negation;
- temporal interpretation;
- subject/target/owner/perspective referents;
- ownership;
- third-party/report;
- correction;
- goal/request;
- span decoding;
- multi-claim decomposition/signals;
- Italian weaknesses;
- Spanish weaknesses;
- ambiguity/hypothesis;
- code-switch IT/EN/ES;
- colloquial, incomplete and typo/noisy input.

### Mandatory adult/intimacy coverage

Adult/intimacy coverage is a critical NLU family, not optional and not a censorship layer.

All authored sexual training/probe material must involve adults only.

Coverage must include, where linguistically relevant:
- attraction, desire and arousal;
- intimate/sexual requests;
- consent grant;
- refusal, withdrawal and boundaries;
- initiation and reciprocal participation;
- escalation/de-escalation;
- anatomy/action references and explicit vocabulary;
- slang and colloquial language in IT/EN/ES;
- code-switching;
- roles and consensual power dynamics;
- sexual-health/protection language when semantically relevant;
- negation, temporal relation, hypothesis, correction, report and referents inside adult contexts;
- ambiguity;
- coercion/pressure/threat distinguished semantically from consensual intimacy.

Hard rule:

```text
adult/intimacy content alone
≠ automatic block
≠ automatic confidence penalty
≠ automatic semantic degradation
```

Understanding must interpret the language accurately and emit the ordinary structured Matrix semantics. No sexual content involving minors is permitted.

### Training and error-mining loop

After each meaningful training attempt:

```text
TRAIN
→ DEV evaluation
→ per-language + per-family error taxonomy
→ causal/root-cause analysis
→ TRAIN-only hard-example/repair generation
→ retrain
→ regression comparison
```

Do not repair systematic linguistic failures with accumulating regex or hand-authored language-specific parser patches. Deterministic logic remains for schema/invariants, not as a replacement for learned Understanding.

### Quality gates

Do not judge completion from one global metric.

The final candidate must show no critical systematic failure on:
- negation;
- temporal interpretation;
- referents;
- ownership/perspective;
- third-party/report;
- request;
- correction;
- goal;
- multi-claim;
- adult/intimacy including consent/refusal/boundaries;
- IT/EN/ES and code-switch robustness.

Hard invariants:

```text
ownership corruption = 0
invented World Truth = 0
```

Target remains near-perfect practical generalization on a genuinely difficult unseen benchmark, not decimal chasing. A nominal >99% is insufficient if a critical family remains systematically broken.

### Confidence and abstention

Confidence is part of the NLU contract, not a cosmetic post-process.

- calibrate per-head/per-output confidence on development evidence;
- uncertain critical output must fail closed/abstain rather than silently corrupt downstream state;
- thresholds are chosen on allowed development data only;
- do not tune thresholds on Frozen.

### Frozen policy

Frozen remains closed during:
- training;
- architecture/capacity selection;
- error mining;
- hard-example generation;
- hyperparameter tuning;
- threshold calibration;
- quantization recipe selection.

Only after a candidate is locked may the final Frozen evaluation run. Frozen results must not be fed back into training.

### Post-teaching compression path

Once a taught FP32 Student-5 candidate reaches the quality gate:

```text
Student-5 40k taught FP32
= quality reference
        ↓
encoder INT8 + protected semantic heads FP32 by default
        ↓ parity tests
Student-5 40k taught mixed/INT8 candidate
```

Alternative mixed precision is allowed only when measured evidence shows it preserves critical quality better within the mobile budget.

Required comparisons:

```text
Student-4-v2.2A FP32/mixed baseline
vs Student-5 taught FP32
vs Student-5 taught mixed/INT8
```

### Mobile/runtime gate

Physical Moto G56 testing remains late-stage.

Before phone testing, CI/desktop/runtime checks must cover:
- ONNX correctness;
- tokenizer/model reload;
- output parity;
- package integrity/checksums;
- estimated/runtime memory;
- cold/warm latency where measurable;
- unsupported operators/runtime failures.

Path A may be used to discover deployment problems early, but repeated phone testing during linguistic iteration is not required.

### Completion sequence

```text
S5-A 40k untaught runtime probe
→ report/checkpoint

S5-B pristine 40k + Matrix teaching
→ DEV/error mining/controlled TRAIN-only repair
→ capacity escalation only as justified

S5-C taught FP32 candidate lock
→ quantization/mixed precision
→ parity/regression

S5-D final candidate
→ Frozen once
→ late Moto hardware gate
→ production integration remains separate
```

### STOP / non-promotion rules

- do not lower existing acceptance gates to obtain PASS;
- do not modify Frozen;
- do not auto-promote Student-5;
- do not discard Student-4 baseline prematurely;
- do not integrate into Assembling from this workstream;
- do not modify another repository;
- if a genuine architecture-level blocker is found, preserve artifacts/reports/continuity and stop with evidence instead of hiding the failure.

Next action when execution is explicitly authorized: prepare the Work prompt from this checkpoint, requiring Work to read `ARCHITETTURA.md` first and to operate only inside `MATRIXNEO23/matrix-understanding-lab`.

## Checkpoint 6 — MiniLM 40k quality dossier consolidated

Timestamp: `2026-09-05`

A dedicated, analysis-ready quality dossier has been created at:

```text
reports/STUDENT_5_MINILM_40K_QUALITY_ANALYSIS.md
```

It consolidates Phase-A identity, upstream pin, architecture, TRAIN-only provenance, all candidate size results, IT/EN/ES/adult/code-switch tokenization metrics, representation-preservation metrics, fixed gate thresholds, artifact checksums, residual risks, and the exact boundary between measured pruning quality and unmeasured Matrix-NLU quality.

The earlier Student-4-v2.2A dossier created under the mistaken interpretation of “the new NLU” was removed. Student-4 remains only the preserved comparative baseline; no Student-4 model or evidence artifact was modified.

Current authoritative interpretation:

```text
component = STUDENT_5_MINILM_40K_PHASE_A
decision = PRUNING_CANDIDATE_SELECTED
artifactRole = REPRESENTATION_PRESERVING_BACKBONE
nluStatus = NOT_MATRIX_NLU
matrixHeadsTrained = false
canonicalDevEvaluated = false
quantizationExecuted = false
frozenDataRead = false
productionStatus = NOT_PRODUCTION_APPROVED
```

No Matrix exact-set, claim-exact, negation, predicate, ownership, temporal, referent, World Truth, or calibration metric exists yet for Student-5. Those fields are marked “not measured” rather than copied from Student-4 or represented as zero.

No training, quantization, Frozen access, data modification, gate change, Assembling integration, or production promotion occurred during this documentation checkpoint.


## Checkpoint 7 — mandatory two-student isolation policy

Timestamp: `2026-09-05`

Owner-mandated preservation rule:

```text
Student-4-v2.2A = PRESERVED_COMPARATIVE_BASELINE
Student-5-MiniLM-40k = PRESERVED_PRIMARY_CANDIDATE
workMode = ONE_STUDENT_AT_A_TIME
crossStudentMutation = FORBIDDEN
automaticReplacement = FORBIDDEN
automaticPromotion = FORBIDDEN
```

Operational contract:

- both Student-4-v2.2A and Student-5 MiniLM 40k must remain preserved;
- only one student workstream may be active at a time;
- training, export, quantization, repair, configuration, checkpoints, reports and artifacts for the active student must not modify or overwrite the other student;
- artifacts, manifests, checksums and evaluation evidence must remain separately named and traceable;
- changing the active student requires an explicit continuity checkpoint identifying the source artifact and verifying that the previously active student remains unchanged;
- Student-4 results may be used only as a comparative baseline while Student-5 is active;
- Student-5 artifacts must remain untouched when future work explicitly returns to Student-4;
- neither student may be discarded, silently replaced, or production-promoted as a side effect of work on the other.

Current lock:

```text
activeStudent = Student-5-MiniLM-40k
activeOperation = DOCUMENTATION_AND_QUALITY_ANALYSIS
Student-4-v2.2AChanged = false
Student-5TrainingExecuted = false
Student-5QuantizationExecuted = false
frozenDataRead = false
productionPromotionExecuted = false
```

The MiniLM quality dossier remains `reports/STUDENT_5_MINILM_40K_QUALITY_ANALYSIS.md`. This checkpoint changes documentation only; it performs no training, export, quantization, data mutation, Frozen access, gate change, or integration.


## Checkpoint 8 — canonical artifact recovery locations recorded

Timestamp: `2026-09-05`

Canonical recovery registry:

```text
docs/STUDENT_ARTIFACT_REGISTRY.md
```

The registry now records:

- Student-4 authoritative training run, report, bundle artifact, resumable checkpoint, digests and expiry dates;
- Student-4 durable mixed/head-protected ZIP and manifest locations in `MATRIXNEO23/assembling` Git LFS;
- Student-5 reports, deterministic generator, tests, implementation commits, selected model/archive sizes and SHA-256 identities;
- mandatory one-student-at-a-time isolation and checksum verification rules;
- the unresolved Student-5 preservation gap: no durable remote binary locator is presently recorded for the 40k archive.

Preservation status:

```text
Student-4MixedRuntime = DURABLY_LOCATED_IN_ASSEMBLING_GIT_LFS
Student-4BundleAndResume = ACTIONS_ARTIFACTS_EXPIRING_2026_10_04
Student-5ReportsAndReproductionSource = DURABLY_LOCATED_IN_REPOSITORY
Student-5BinaryArchive = REMOTE_LOCATOR_NOT_RECORDED
nextPreservationAction = RECOVER_OR_REGENERATE_STUDENT5_ARCHIVE_AND_PUBLISH_WITH_SHA256
```

No artifact was overwritten and neither student was modified by this documentation checkpoint. Frozen remained unread.
