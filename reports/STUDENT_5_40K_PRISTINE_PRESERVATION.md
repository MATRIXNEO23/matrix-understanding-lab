# Student-5 MiniLM 40k pristine preservation

Date: `2026-09-05`  
Repository: `MATRIXNEO23/matrix-understanding-lab`  
Branch: `main`  
Task: `TASK_0_PRISTINE_PRESERVATION`  
Result: `PASS`

## Disposition

```text
artifact = Student-5 MiniLM 40k Phase-A
artifactSource = ORIGINAL_RECOVERED
status = PRISTINE_PHASE_A_BACKBONE
role = REPRESENTATION_PRESERVING_BACKBONE
nluStatus = NOT_MATRIX_NLU
productionStatus = NOT_PRODUCTION_APPROVED
automaticContinuation = FORBIDDEN
nextTask = NOT_AUTHORIZED
```

The original Phase-A archive was recovered from an existing preserved project output. No regeneration, retraining, teaching, Matrix-head construction, ONNX export, quantization, DEV use, Frozen access, or production promotion was performed.

## Durable remote locator

- Release: [Student-5 MiniLM 40k Phase-A Pristine](https://github.com/MATRIXNEO23/matrix-understanding-lab/releases/tag/student-5-minilm-40k-phase-a-pristine)
- Release label: `Pre-release`
- Release ID: `383143636`
- Asset ID: `545406840`
- Tag: `student-5-minilm-40k-phase-a-pristine`
- Tag commit: `20230e52388560c537eb614083ca5a3bda29ecfc`
- Asset: [student5-minilm-phase-a-pruned-40k.zip](https://github.com/MATRIXNEO23/matrix-understanding-lab/releases/download/student-5-minilm-40k-phase-a-pristine/student5-minilm-phase-a-pruned-40k.zip)
- Asset bytes: `88361246`
- GitHub-recorded asset digest: `sha256:7804bfb245b71df9b835fff7ee00f6ec887e019772ae34c82d269d821d587191`

This Release asset belongs to the authorized repository and is not a retention-limited GitHub Actions artifact.

## Canonical identity verification

| Check | Expected | Observed | Result |
|---|---:|---:|---|
| Vocabulary size | `40000` | `40000` | PASS |
| Encoder layers | `12` | `12` | PASS |
| Hidden size | `384` | `384` | PASS |
| FP32 model bytes | `148020400` | `148020400` | PASS |
| Artifact-directory bytes | `150116913` | `150116913` | PASS |
| Archive bytes | `88361246` | `88361246` | PASS |
| Model SHA-256 | `d6e45891d1e0ec4ed023caaeb17c0dd0ae80a93b8bf877d275310b7f2837efa2` | same | PASS |
| Token-ID mapping SHA-256 | `da36a5e1a9057391da935354d895edb3bc3a959744aca6b6602e511f9d4ea9b9` | same | PASS |
| SentencePiece SHA-256 | `748f8053688469d7dc98c135a28a3fc0713bdbb82853f86f8d7a254bada46f78` | same | PASS |
| Candidate manifest SHA-256 | `a9d23de7816d487986316351c163f37a67d65d001861dbf042b9114c455f066d` | same | PASS |
| Archive SHA-256 | `7804bfb245b71df9b835fff7ee00f6ec887e019772ae34c82d269d821d587191` | same | PASS |

Upstream identity:

```text
repository = microsoft/Multilingual-MiniLM-L12-H384
revision = 6e8c1ec6b4ec4e3fc6eb7d2cd834fcd582b61daf
```

The candidate manifest's `artifactDirectoryBytes` is the sum of its six declared model payload files. The self-manifest is intentionally outside that declared payload-size total.

## Archive verification

- ZIP structural integrity: PASS.
- Internal `SHA256SUMS`: 17/17 files PASS.
- Candidate-manifest file table: 6/6 declared model payload files PASS.
- Missing expected files: none.
- Unexpected payload files: none.
- Frozen dataset files: none; only the textual `FROZEN_GUARD.txt` evidence file is present.
- `FROZEN_GUARD.txt`: consistent with all Task-0 invariants.

Payload file set:

```text
FROZEN_GUARD.txt
README.md
SHA256SUMS
evidence/student5-deep-pruning-manifest.json
evidence/student5-vocab-selection-corpus-manifest.json
evidence/upstream-audit.json
model/candidate-manifest.json
model/config.json
model/model.safetensors
model/sentencepiece.bpe.model
model/special_tokens_map.json
model/token-id-remap.json
model/tokenizer_config.json
reports/STUDENT_5_MINILM_DEEP_PRUNING.md
reports/STUDENT_5_MINILM_PRUNING_FEASIBILITY.md
source/student5_deep_pruning.py
source/student5_pruning_corpus.py
source/test_student5_deep_pruning.py
```

## Tokenizer and model verification

Special-token mapping:

| Token | ID |
|---|---:|
| BOS | 0 |
| PAD | 1 |
| EOS | 2 |
| UNK | 3 |
| MASK | 39999 |

Verified fail-closed:

- mapping policy: `NEW_HF_ID_EMBEDDING_ROW_COPIED_FROM_DECLARED_OLD_HF_ID`;
- tokenizer length = embedding rows = `40000`;
- Hugging Face local save/reload succeeds;
- model class = `BertModel`;
- tokenizer class = `XLMRobertaTokenizer`;
- embedding shape = `[40000, 384]`;
- total parameters = `36999552`;
- word-embedding parameters = `15360000`;
- non-word-embedding parameters = `21639552`;
- non-word-embedding tensors = `198`, consistent with Phase-A unchanged-weight evidence;
- real offline forward succeeds on a neutral, non-DEV probe;
- forward output shape = `[1, 17, 384]`;
- all forward values are finite.

## Data and repository guards

```text
student4V22AChanged = false
canonicalDevUsed = false
frozenDataRead = false
frozenDataTokenized = false
frozenDataAnalyzed = false
frozenPredictionsRead = false
teachingExecuted = false
matrixHeadsTrained = false
quantizationExecuted = false
productionPromotionExecuted = false
otherRepositoriesModified = false
```

Student-4 was not read, downloaded, rewritten, trained, exported, quantized, or otherwise modified. No repository outside `MATRIXNEO23/matrix-understanding-lab` was modified.

## Task-0 gate

```text
canonicalStudent5ArtifactRecoveredOrBitExactRegenerated = true
artifactSource = ORIGINAL_RECOVERED
modelSha256Verified = true
mappingSha256Verified = true
sentencePieceSha256Verified = true
manifestSha256Verified = true
archiveSha256Verified = true
durableRemoteLocatorRecorded = true
durableRemoteLocatorBelongsToMatrixUnderstandingLab = true
student4V22AChanged = false
teachingExecuted = false
quantizationExecuted = false
canonicalDevUsed = false
frozenDataRead = false
otherRepositoriesModified = false
TASK_0 = PASS
NEXT = AWAIT OWNER REVIEW BEFORE TASK 1
```
