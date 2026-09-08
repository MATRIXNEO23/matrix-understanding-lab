# Student-5 FP32 — CP44 input preparation and selection dependency

STUDENT5_FP32 = BLOCKED. Training has not started.

Starting main: `6389e82c255c50964ce2df370a4682ba7206248b`.
The new Supervisor assignment authorizes FP32 training, post-training evaluation
and persistence. It supersedes earlier STOP boundaries and strict historical
acceptance thresholds. G03 remains PASS. G04 is post-training evaluation;
G07 is an evidence limitation and is not used to stop training.

## Completed, freshly verified work

- Authenticated the surviving original pristine archive against live GitHub
  Release metadata and CP41 identity: Release 383143636, asset 545406840,
  tag `student-5-minilm-40k-phase-a-pristine`, filename
  `student5-minilm-phase-a-pruned-40k.zip`, 88,361,246 bytes,
  archive SHA-256 `7804bfb245b71df9b835fff7ee00f6ec887e019772ae34c82d269d821d587191`.
- ZIP integrity and all 17 CP41 internal checks pass. The local model/tokenizer
  inputs equal the archive entries. Model is 148,020,400 bytes, SHA-256
  `d6e45891d1e0ec4ed023caaeb17c0dd0ae80a93b8bf877d275310b7f2837efa2`;
  all 199 stored tensors are F32. No model forward or optimizer ran.
- TRAIN `student5-matrix-nlu-v3-train-v2.1-cp43r2` remains at
  `data/student5_v3_train_v21/`, SHA-256
  `f90ae775a44023c37bf0c3a5087d64746413cbec770ca36cf154d1d533544aa4`.
  All dataset files match BUILD_LOCK and remain unchanged.
- Prepared all 4,355 target examples from 1,831 observations / 2,524 claims
  with the exact G03 builder and real pristine tokenizer. No errors.
  Fast offset-capable tokenizer is converted from the local pristine slow
  tokenizer; all 4,355 token-ID sequences match the canonical slow tokenizer,
  remain below vocabulary size 40,000 and fit within maxLength 256.
  Longest observed sequence is 33 tokens. No dataset annotation was changed.
- Exact 8 G03 rows and 14 ambiguous fields pass with real tokenization;
  primary UNKNOWN, independent roles, statuses and ordered alternatives remain intact.

The available CPU environment has Torch 2.4.1+cpu / Transformers 4.44.2;
complete dependency versions are in `preflight.json`. Lack of GPU is not the
blocker. No pristine analysis or general TRAIN audit was repeated.

## Exact unresolved prerequisite

**FP32-S01 — missing identified V3 selection/evaluation gold.**

The requested existing Student-5 selection method is DEV-based, recorded in
`prompts/WORK_STUDENT_5_PATH_B_V3_COMPLETION.md`, B2/B5 and Gate C. The same
canonical plan starts with a frozen 12-layer backbone and the existing V3 heads;
full backbone fine-tuning is not its default first attempt.

At the pinned starting HEAD, the repository, artifact registry and current
three-Release inventory do not identify an authorized V3 DEV artifact with
ID, locator, checksum and gold. The persisted CP36 record explicitly leaves
that identity null; it has not been replaced by a later identified selection
set. This finding is about the input needed to select and assess a checkpoint,
not an abstract TRAIN–DEV statistical overlap requirement.

The historical V2 DEV references have a different contract and negation-scope
representation. Their payloads were not opened, migrated or reannotated.
`synthetic_v3_fixtures.py` is explicitly software structure examples, mostly
texts/family names without complete gold, and does not establish a competitive
evaluation set. TRAIN preservation controls are not independent selection gold.
No alternative was silently substituted for the requested method.

The current assignment permits ordinary trainer/evaluation implementation and
minimal documented technical configuration choices. It does not identify the
missing selection gold or a replacement checkpoint-selection method. Starting
a run now would require choosing a different selection protocol without that
input. The prepared work is persisted; no optimizer was launched and no model
checkpoint is claimed.

Needed from Supervisor: the existing permitted V3 DEV ID/path/SHA and selection
reference, or an explicit scope to prepare separate V3 selection/evaluation
gold. FP32 training permission already exists and need not be repeated.
Once that input is identified, continue this authorized FP32 task using the
same pristine/TRAIN/target builder; do not reopen dataset repair or G03.

## Artifacts and reproduction

Evidence directory: `reports/evidence/student5-fp32-cp44/`.

- `preflight.json`: model/archive/internal hashes, TRAIN locks, tokenizer
  checks, target counts, eight G03 row results, dependencies and execution flags.
- `prepared-targets.jsonl.gz`: real-tokenizer targets, a derived preparation
  artifact only; not a new TRAIN version or trained model. Its compressed and
  ordered SHA-256 are in preflight.json.
- `selection-input.json`: selection authority, exact missing identity,
  current relevant path/blob inventory, Release metadata and required input.
- `SHA256SUMS`: code/evidence/report/continuity checksums.
- `remote-readback.json`: subsequent verified publication receipt.
- Source: `tools/student5_fp32/preflight.py`.

Reproduce from authenticated local pristine bytes, writing to a NEW directory:

```bash
python tools/student5_fp32/preflight.py --repo . \
  --pristine-archive /path/student5-minilm-phase-a-pruned-40k.zip \
  --model-dir /path/pristine/model --out /tmp/student5-fp32-preflight-new
```

Pristine durable recovery:
`https://github.com/MATRIXNEO23/matrix-understanding-lab/releases/tag/student-5-minilm-40k-phase-a-pristine`.
Use the authenticated Release asset download and verify the archive/model
hashes above; never regenerate or substitute the model. This execution reused
the CP34-acquired original archive and reverified it; no fresh download is claimed.

## Final state

TRAINING_STATUS = NOT_STARTED_MISSING_SELECTION_INPUT
TRAINING_DURATION = 0
BEST_CHECKPOINT = NONE
TRAINED_MODEL_ID = NONE
TRAINED_MODEL_PATH/ARTIFACT = NONE
TRAINED_MODEL_SHA256 = N/A
STUDENT5_FP32 = BLOCKED

Overall/per-head/IT/EN/ES/negation/temporal/referent/status/claimKind/dialogueAct
metrics and preservation/regression results are NOT_MEASURED. No improvement,
regression magnitude, competitive result or acceptance conclusion is claimed.
There is no training loss, optimizer configuration or checkpoint-selection
result because no run executed. No model artifact was produced.

trainDatasetModified=false
trainingExecuted=false
fineTuningExecuted=false
quantizationExecuted=false
onnxExecuted=false
androidIntegrationExecuted=false
student4Modified=false
frozenUsedForTraining=false
frozenRead=false
nextWorkStarted=false

STOP with this concrete selection-input dependency. No background job remains.
