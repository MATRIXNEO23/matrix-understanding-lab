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
