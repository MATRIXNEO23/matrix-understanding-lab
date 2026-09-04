# Student-5 MiniLM — Phase A deep vocabulary pruning

Date: `2026-09-04`  
Repository: `MATRIXNEO23/matrix-understanding-lab`  
Phase: `PHASE_A_VOCABULARY_PRUNING_FEASIBILITY`  
Decision: `PRUNING_CANDIDATE_SELECTED`  
Selected vocabulary: `40000`  
Production status: `NOT_PRODUCTION_APPROVED`

## Executive decision

Phase A is a GO at vocabulary size 40k. The 40k, 60k, and 80k variants pass every threshold declared before measurement; 100k fails only the material-size requirement against the 149,711,344-byte Student-4-v2.2A Mixed reference. The 40k variant is selected because it is the smallest passing artifact and the measured improvements from 60k are small relative to its additional 30,720,000 estimated runtime bytes.

This decision authorizes only a later, separately approved teaching experiment. It does not authorize Matrix-head training, fine-tuning, quantization, Frozen evaluation, Assembling integration, or production promotion.

## Boundaries and integrity

```text
student4V22AChanged = false
canonicalDevUsedForVocabularySelection = false
canonicalDevUsedForProbe = false
frozenDataRead = false
frozenDataTokenized = false
frozenDataAnalyzed = false
teachingExecuted = false
matrixHeadsTrained = false
quantizationExecuted = false
assemblingIntegrationExecuted = false
productionPromotionExecuted = false
```

Adult/intimacy material was treated as ordinary semantic NLU coverage, never as moderation or safety classification. Authored examples refer only to adults; no minors are present.

## Upstream pin and audit

| Field | Value |
|---|---|
| Repository | `microsoft/Multilingual-MiniLM-L12-H384` |
| Revision | `6e8c1ec6b4ec4e3fc6eb7d2cd834fcd582b61daf` |
| License | MIT |
| Model type | `BertModel` / `bert` |
| Tokenizer | `XLMRobertaTokenizer` |
| SentencePiece pieces | 250,000 |
| Reachable tokenizer IDs | 250,002 (`0..250001`) |
| Embedding rows | 250,037 |
| Unreachable trailing rows | 35 |
| Hidden size | 384 |
| Transformer layers | 12 |
| Attention heads | 12 |
| Intermediate size | 1,536 |
| Total parameters | 117,653,760 |
| Word-embedding parameters | 96,014,208 |
| All embedding parameters | 96,212,352 |
| Transformer parameters | 21,293,568 |
| Pooler parameters | 147,840 |
| Upstream FP32 weight bytes | 470,657,952 |
| Upstream estimated INT8 bytes | 406,471,680 |
| Upstream tokenizer bytes | 5,069,203 |
| Weight SHA-256 | `cce170910f4d4f3b45be025508f51ef1ad6a1de69f2d46dce7e4603ad31aaaeb` |
| SentencePiece SHA-256 | `cfc8146abe2a0488e9e2a0c56de7952f7c11ab059eca145a0a727afce0db2865` |

The complete reachable tokenizer-ID to embedding-row relation is deterministic. XLM-R control/special IDs are handled explicitly, ordinary SentencePiece pieces use the tokenizer offset, and the mask is remapped explicitly. The upstream model has 35 embedding rows with no reachable tokenizer ID; these rows are intentionally omitted. The upstream config says `pad_token_id=0` while its tokenizer uses `<pad>=1`; every pruned config is aligned to tokenizer ID 1.

Special-token mapping in each candidate is `<s>=0`, `<pad>=1`, `</s>=2`, `<unk>=3`, and `<mask>=vocab_size-1`.

## TRAIN-safe vocabulary-selection corpus

Selection corpus: 16,819 records, 3,651,427 bytes.  
SHA-256: `2412a5727eb51b993f3172f3dc4a4d08199e16382b90c2e62e5080e3e23b8558`.

| Source | Records | Constraint |
|---|---:|---|
| Matrix v1 TRAIN | 2,991 | TRAIN only |
| Matrix v2 TRAIN | 2,775 | TRAIN-only migration/additions; 345 canonical TRAIN drop IDs applied |
| Student-4-v2.2A repair | 375 | Exact repair TRAIN-only artifact |
| MASSIVE IT | 3,000 | TRAIN partition only |
| MASSIVE EN | 3,000 | TRAIN partition only |
| MASSIVE ES | 3,000 | TRAIN partition only |
| Project-authored general coverage | 720 | Separate authored source |
| Project-authored adult/intimacy coverage | 1,206 | Adult-only ordinary NLU coverage |
| Authored controls | 4 | Control rows |

MASSIVE archive SHA-256 is `7df623fd2d300a4d235d6ee5bd396c9a28258d3a0ccb29abdb054506eba153f8`; license is CC-BY-4.0. Non-TRAIN JSON payloads were rejected at the raw partition marker and were not decoded (`nonTrainJsonDecoded=false`). No arbitrary web scraping or optional public corpus was used.

## Construction method

For each target, pieces observed in the selection corpus are ranked first by frequency; remaining capacity is filled using the original SentencePiece score and old ID as deterministic tie breakers. Required special/control pieces are always retained. Each candidate contains:

- a real reduced SentencePiece model;
- both `oldTokenIdToNewTokenId` and `newTokenIdToOldTokenId` mappings;
- an embedding table built by exact row copies from the declared old IDs;
- the original 12 Transformer layers and every non-word-embedding tensor unchanged;
- updated BERT config and special-token files;
- an independently loadable Hugging Face artifact;
- a candidate manifest with file sizes and SHA-256 values.

All pieces actually observed in the 16,819-row selection corpus fit in and are retained by all four candidates.

## Size and parameter results

The INT8 column is an estimate only: embeddings and one-dimensional parameters remain FP32 while eligible non-embedding matrices are counted at one byte per parameter. No quantization was performed in Phase A.

| Vocab | Embedding params | Total params | Parameter reduction | FP32 model bytes | Artifact bytes | Tokenizer bytes | Estimated INT8 bytes | INT8 reduction vs Student-4 Mixed | Gate |
|---:|---:|---:|---:|---:|---:|---:|---:|---:|---|
| Original | 96,014,208 | 117,653,760 | — | 470,657,952 | 475,734,505 | 5,069,203 | 406,471,680 | -171.50% | Reference |
| 40k | 15,360,000 | 36,999,552 | 68.552% | 148,020,400 | 150,116,913 | 885,726 | 83,854,848 | 43.989% smaller | PASS |
| 60k | 23,040,000 | 44,679,552 | 62.024% | 178,740,552 | 181,807,197 | 1,235,858 | 114,574,848 | 23.469% smaller | PASS |
| 80k | 30,720,000 | 52,359,552 | 55.497% | 209,460,584 | 213,508,337 | 1,596,966 | 145,294,848 | 2.950% smaller | PASS |
| 100k | 38,400,000 | 60,039,552 | 48.969% | 240,180,584 | 245,220,667 | 1,969,293 | 176,014,848 | 17.569% larger | FAIL size |

The selected 40k model file is 68.550% smaller than the upstream FP32 weight file. Its estimated runtime footprint is 83,854,848 bytes (about 80.0 MiB), 43.989% below Student-4-v2.2A Mixed.

## Separate coverage probe

The probe is project-authored and separate from the serialized vocabulary-selection corpus. It has 95 coverage sentences: 29 each for IT/EN/ES plus multilingual controls; 50 are adult/intimacy and 8 are explicit code-switch cases. Semantic comparison expands this to 161 unique sentences and 36 contrast pairs. Canonical dev and Frozen were not used.

### Coverage and tokenization by candidate

All reported UNK rates are 0. The inflation column is aggregate token-count inflation against the exact upstream tokenizer; mean and p95 are candidate tokens per sentence.

| Vocab | Slice | UNK | Mean tokens | p95 tokens | Inflation |
|---:|---|---:|---:|---:|---:|
| Original | IT | 0 | 12.828 | 17 | 1.000 |
| Original | EN | 0 | 12.103 | 18 | 1.000 |
| Original | ES | 0 | 12.379 | 17 | 1.000 |
| Original | Adult/intimacy | 0 | 13.820 | 17 | 1.000 |
| Original | Code-switch | 0 | 12.625 | 14 | 1.000 |
| Original | Names/locations | 0 | 11.000 | 12 | 1.000 |
| 40k | IT | 0 | 13.310 | 17 | 1.038 |
| 40k | EN | 0 | 12.552 | 18 | 1.037 |
| 40k | ES | 0 | 13.207 | 18 | 1.067 |
| 40k | Adult/intimacy | 0 | 14.360 | 18 | 1.039 |
| 40k | Code-switch | 0 | 13.375 | 17 | 1.059 |
| 40k | Names/locations | 0 | 11.667 | 14 | 1.061 |
| 60k | IT | 0 | 13.207 | 17 | 1.030 |
| 60k | EN | 0 | 12.483 | 18 | 1.031 |
| 60k | ES | 0 | 12.931 | 17 | 1.045 |
| 60k | Adult/intimacy | 0 | 14.180 | 17 | 1.026 |
| 60k | Code-switch | 0 | 13.125 | 17 | 1.040 |
| 60k | Names/locations | 0 | 11.333 | 13 | 1.030 |
| 80k | IT | 0 | 13.138 | 17 | 1.024 |
| 80k | EN | 0 | 12.345 | 18 | 1.020 |
| 80k | ES | 0 | 12.793 | 17 | 1.033 |
| 80k | Adult/intimacy | 0 | 14.080 | 17 | 1.019 |
| 80k | Code-switch | 0 | 12.875 | 16 | 1.020 |
| 80k | Names/locations | 0 | 11.333 | 13 | 1.030 |
| 100k | IT | 0 | 13.000 | 17 | 1.013 |
| 100k | EN | 0 | 12.310 | 18 | 1.017 |
| 100k | ES | 0 | 12.690 | 17 | 1.025 |
| 100k | Adult/intimacy | 0 | 14.000 | 17 | 1.013 |
| 100k | Code-switch | 0 | 12.875 | 16 | 1.020 |
| 100k | Names/locations | 0 | 11.333 | 13 | 1.030 |

For completeness, overall candidate mean/p95 values are 13.053/18 (40k), 12.895/17 (60k), 12.768/17 (80k), and 12.684/17 (100k), versus 12.453/17 upstream.

### Selected 40k adult/intimacy coverage

The table provides category-specific measurements, including formal/colloquial/vulgar/slang phrasing, consent and boundaries, desire, requests, correction, conditional consent, temporal and third-party statements, anatomy/practices, health, and code-switching.

| Category | Sentences | UNK | Mean tokens | p95 tokens | Inflation |
|---|---:|---:|---:|---:|---:|
| Anatomy | 3 | 0 | 19.333 | 21 | 1.018 |
| Code-switch | 8 | 0 | 13.375 | 17 | 1.059 |
| Conditional consent | 3 | 0 | 14.333 | 15 | 1.049 |
| Consent/boundary | 6 | 0 | 14.667 | 16 | 1.048 |
| Correction | 3 | 0 | 16.667 | 18 | 1.020 |
| Desire | 6 | 0 | 14.500 | 16 | 1.036 |
| Health | 3 | 0 | 14.667 | 17 | 1.000 |
| Practice | 3 | 0 | 14.000 | 15 | 1.000 |
| Request | 6 | 0 | 11.667 | 13 | 1.061 |
| Slang/vulgar | 3 | 0 | 16.000 | 17 | 1.067 |
| Temporal | 3 | 0 | 14.667 | 17 | 1.023 |
| Third party | 3 | 0 | 12.333 | 13 | 1.057 |

Adult/intimacy by language at 40k: IT mean 15.143, p95 20, inflation 1.019; EN mean 13.714, p95 17, inflation 1.038; ES mean 14.786, p95 21, inflation 1.051. Every language-specific adult slice has zero UNK.

## Pre-teaching semantic preservation

Mean-pooled last-hidden-state vectors were compared with the pinned upstream model. The 36 contrast pairs cover negation, question/request, correction, third-party statements, past/future temporal changes, and adult distinctions for desire/request, consent/refusal, consent withdrawal, preference/experience, target, and explicit fact/hypothesis.

| Vocab | Mean representation cosine | Worst cosine | p05 cosine | Mean contrast cosine delta | p95 contrast delta | Max contrast delta | Unchanged-tokenization sentences | Max forward delta |
|---:|---:|---:|---:|---:|---:|---:|---:|---:|
| 40k | 0.995579 | 0.943703 | 0.976073 | 0.007845 | 0.045259 | 0.051024 | 103 | 0.0 |
| 60k | 0.996500 | 0.943703 | 0.979299 | 0.007845 | 0.045259 | 0.051024 | 111 | 0.0 |
| 80k | 0.997080 | 0.943703 | 0.979299 | 0.007487 | 0.045259 | 0.051024 | 120 | 0.0 |
| 100k | 0.997840 | 0.943703 | 0.987107 | 0.006765 | 0.045259 | 0.051024 | 132 | 0.0 |

At 40k, all three negation contrast pairs and all consent/refusal/withdrawal contrasts in Italian have zero cosine-delta relative to upstream. The largest 40k contrast delta is 0.051024 on Spanish adult consent withdrawal; the declared gate is based on mean (`<=0.02`) and p95 (`<=0.05`), both of which pass. When tokenization is unchanged after explicit ID remapping, the model forward is numerically identical (`max delta = 0`).

## Gate thresholds and results

Thresholds were fixed before measurement:

| Check | Threshold | 40k | 60k | 80k | 100k |
|---|---:|---|---|---|---|
| Special tokens | PASS | PASS | PASS | PASS | PASS |
| Tokenizer/model alignment | PASS | PASS | PASS | PASS | PASS |
| Save/reload | PASS | PASS | PASS | PASS | PASS |
| Selection pieces retained | all | PASS | PASS | PASS | PASS |
| UNK IT/EN/ES/adult | <=0.001 | PASS | PASS | PASS | PASS |
| Mean IT/EN/ES inflation | <=1.15 | PASS | PASS | PASS | PASS |
| Code-switch inflation | <=1.20 | PASS | PASS | PASS | PASS |
| Adult inflation | <=1.15 | PASS | PASS | PASS | PASS |
| Adult disproportion vs language mean | <=0.05 | PASS | PASS | PASS | PASS |
| Names/location inflation | <=1.20 | PASS | PASS | PASS | PASS |
| Mean representation cosine | >=0.98 | PASS | PASS | PASS | PASS |
| Worst representation cosine | >=0.90 | PASS | PASS | PASS | PASS |
| Mean contrast delta | <=0.02 | PASS | PASS | PASS | PASS |
| p95 contrast delta | <=0.05 | PASS | PASS | PASS | PASS |
| Exact forward delta | <=1e-6 | PASS | PASS | PASS | PASS |
| Estimated INT8 vs 149,711,344 bytes | smaller | PASS | PASS | PASS | FAIL |

## Artifact identity

| Vocab | Model SHA-256 | Mapping SHA-256 | SentencePiece SHA-256 | Candidate manifest SHA-256 |
|---:|---|---|---|---|
| 40k | `d6e45891d1e0ec4ed023caaeb17c0dd0ae80a93b8bf877d275310b7f2837efa2` | `da36a5e1a9057391da935354d895edb3bc3a959744aca6b6602e511f9d4ea9b9` | `748f8053688469d7dc98c135a28a3fc0713bdbb82853f86f8d7a254bada46f78` | `65f2b0e26b8f46ea16e6a9d0328a5bfdb3cfb29fa2f4f40ff046c09af8fb2fc8` |
| 60k | `5e8278b0772bb7dc2a18139c288931446b1a1c2089254d0e5d13c85e35bf6c48` | `6490295a55dbb7bfbade04ef57386b711b444d855febea0cedf0826458062c91` | `fcd96533998f8ae231348ca29724567d4701e487ddb7c82ee0a9ef8d033766e8` | `9fcd7df21921c397ec66d7865f6a731ef069b79f54f4d6c17f0edcf5c610b230` |
| 80k | `79711969c70b6f03929dcc2e813c3b77da3b95227e5c820c68a0c2820c692e42` | `2b5128b5c5cc96efabd82a0cd469b22099c399b4d8acaf271bbc3f07492b05db` | `a6e74b54adfcbd08078ebddf503aa5926d15a5b414e85714e15e6642c22c86f0` | `48d4fb7f71acd7d2a42ecf219fb00dee9ff11272ea488933cdea50173fb3835e` |
| 100k | `051eac9b10ec7404e0eaa527256853318f70ec42ebfc7523945ca2378cd51966` | `0e3d2fb44aaabb623a85d75ee2fa0cbd37a41a08e5985e077122dc946e90738b` | `0080da898b8d288710361931d2f69b64a46e0d25fc606525146d9ba575ca95b9` | `44a06edb14fd550dd6010d18efd09bcff1bea05fab09e6866adf86a86174bbf5` |

Every file size and SHA-256 recorded in the aggregate manifest was independently recomputed after generation: `ALL_RECORDED_FILE_HASHES_AND_SIZES_PASS`. All four artifacts were independently reloaded and executed after the build.

## Selection rationale

The 60k variant improves aggregate token inflation over 40k by about 0.8 percentage points for IT, 0.6 for EN, 2.2 for ES, and 1.3 for adult/intimacy. Mean representation cosine improves by 0.000921. These are not material enough to justify 30,720,000 additional estimated runtime bytes (36.6% over the 40k estimate). The 40k candidate remains comfortably inside every declared quality threshold and preserves every token observed in the selection corpus, so 40k is the efficient frontier for Phase A.

## Residual risks

- The probe is deliberately independent and multilingual but small; it is not a substitute for downstream Matrix dev evaluation.
- Zero UNK does not guarantee equal subword segmentation; ES has the largest selected-candidate inflation at 1.067.
- No Matrix semantic heads exist on this artifact, so claim, referent, negation, predicate, ownership, and temporal task accuracy have not yet been measured.
- The INT8 number is a deterministic footprint estimate, not a quantized model measurement.
- The candidate remains an upstream representation-preserving backbone, not a trained Student-5.

## Final Phase-A decision and next step

```text
PRUNING_CANDIDATE_SELECTED
selectedVocabSize = 40000
FROZEN_UNREAD
NOT_PRODUCTION_APPROVED
```

Recommended next step: preserve the 40k artifact as the only Phase-B input and, only after explicit authorization, perform Matrix teaching/fine-tuning using TRAIN and canonical dev under unchanged gates. Do not quantize, open Frozen, integrate into Assembling, or promote before that separate phase is complete.
