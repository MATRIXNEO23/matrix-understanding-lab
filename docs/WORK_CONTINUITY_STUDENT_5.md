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

The smallest passing candidate is 40k. It has zero UNK on the separate IT/EN/ES/adult probe, mean token inflation 1.046/1.045/1.075 for IT/EN/ES, adult inflation 1.042, mean representation cosine 0.995579, worst cosine 0.943703, mean contrast delta 0.007845, p95 contrast delta 0.045259, and exact-forward delta 0 for unchanged tokenizations.

Current activity: independently verify every recorded checksum, prepare complete comparison reports, and package the selected Phase-A artifact. No Phase-B work is authorized.
