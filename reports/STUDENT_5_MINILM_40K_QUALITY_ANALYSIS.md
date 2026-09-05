# Student-5 MiniLM 40k — Quality Analysis Dossier

Date: `2026-09-05`  
Repository: `MATRIXNEO23/matrix-understanding-lab`  
Component: `STUDENT_5_MINILM_40K_PHASE_A`  
Phase: `PHASE_A_VOCABULARY_PRUNING_FEASIBILITY`  
Decision: `PRUNING_CANDIDATE_SELECTED`  
Artifact role: `REPRESENTATION_PRESERVING_BACKBONE`  
NLU status: `NOT_MATRIX_NLU`  
Production status: `NOT_PRODUCTION_APPROVED`  
Frozen status: `FROZEN_UNREAD`

## 1. Executive quality conclusion

The 40k vocabulary candidate is the selected MiniLM Phase-A backbone. It passes every pruning-quality threshold declared before measurement and is the smallest passing candidate. It preserves all vocabulary pieces observed in the authorized TRAIN-only selection corpus, reports zero UNK across the independent IT/EN/ES/adult probe, retains high upstream representation similarity, and materially reduces the model footprint.

This result validates vocabulary pruning and representation preservation only. It does **not** establish Matrix-NLU task quality. Matrix heads have not been added or trained, canonical development evaluation has not been executed for Student-5, quantization has not been executed, Frozen has not been read, and no production promotion is authorized.

```text
selectedVocabSize = 40000
phaseAGate = PASS
decision = PRUNING_CANDIDATE_SELECTED
matrixHeadsTrained = false
canonicalDevEvaluated = false
quantizationExecuted = false
frozenDataRead = false
productionApproved = false
```

## 2. Upstream identity and architecture

| Field | Value |
|---|---|
| Upstream model | `microsoft/Multilingual-MiniLM-L12-H384` |
| Pinned revision | `6e8c1ec6b4ec4e3fc6eb7d2cd834fcd582b61daf` |
| License | MIT |
| Model/tokenizer | `BertModel` / `XLMRobertaTokenizer` |
| Hidden size | 384 |
| Transformer layers | 12 |
| Attention heads | 12 |
| Intermediate size | 1,536 |
| SentencePiece pieces | 250,000 |
| Reachable tokenizer IDs | 250,002 (`0..250001`) |
| Original embedding rows | 250,037 |
| Unreachable trailing embedding rows | 35 |
| Total parameters | 117,653,760 |
| Word-embedding parameters | 96,014,208 |
| All embedding parameters | 96,212,352 |
| Transformer parameters | 21,293,568 |
| Pooler parameters | 147,840 |
| Upstream FP32 weight bytes | 470,657,952 |
| Upstream weight SHA-256 | `cce170910f4d4f3b45be025508f51ef1ad6a1de69f2d46dce7e4603ad31aaaeb` |
| Upstream SentencePiece SHA-256 | `cfc8146abe2a0488e9e2a0c56de7952f7c11ab059eca145a0a727afce0db2865` |

The tokenizer-to-embedding mapping was audited for every reachable token ID. The 35 unreachable trailing embedding rows were intentionally omitted. The upstream configuration declares `pad_token_id=0` while the tokenizer exposes `<pad>=1`; each pruned artifact aligns the configuration to tokenizer padding ID 1 without modifying Transformer weights.

Special-token mapping for each candidate is `<s>=0`, `<pad>=1`, `</s>=2`, `<unk>=3`, and `<mask>=vocab_size-1`.

## 3. Authorized selection corpus and provenance

Vocabulary selection used 16,819 TRAIN-safe records totaling 3,651,427 bytes.

Selection-corpus SHA-256: `2412a5727eb51b993f3172f3dc4a4d08199e16382b90c2e62e5080e3e23b8558`.

| Source | Records | Boundary |
|---|---:|---|
| Matrix v1 | 2,991 | TRAIN only |
| Matrix v2 | 2,775 | TRAIN-only migration/additions |
| Student-4-v2.2A repair | 375 | Exact TRAIN-only repair artifact |
| MASSIVE IT | 3,000 | TRAIN partition only |
| MASSIVE EN | 3,000 | TRAIN partition only |
| MASSIVE ES | 3,000 | TRAIN partition only |
| Project-authored general coverage | 720 | Separate authored source |
| Project-authored adult/intimacy coverage | 1,206 | Adult-only semantic NLU coverage |
| Authored controls | 4 | Control rows |
| **Total** | **16,819** | **TRAIN-safe** |

MASSIVE archive SHA-256: `7df623fd2d300a4d235d6ee5bd396c9a28258d3a0ccb29abdb054506eba153f8`; license: CC-BY-4.0.

```text
canonicalDevUsedForVocabularySelection = false
nonTrainJsonDecoded = false
frozenDataRead = false
frozenDataTokenized = false
frozenDataAnalyzed = false
```

No arbitrary web corpus was added. Adult/intimacy examples were treated as ordinary semantic coverage, not as moderation or censorship labels, and involved adults only.

## 4. Construction and integrity checks

Each candidate contains:

- a real reduced SentencePiece model;
- bidirectional old-token-ID/new-token-ID mappings;
- a word-embedding table created by exact row copies;
- all 12 upstream Transformer layers;
- every non-word-embedding tensor unchanged;
- aligned BERT configuration and special-token files;
- an independently reloadable Hugging Face artifact;
- a manifest with sizes and SHA-256 values.

A protobuf compatibility error, `ModelProto.pieces_size`, was corrected to `len(ModelProto.pieces)`. This was an infrastructure-only fix; no corpus, gate, threshold, or selection rule changed.

Verification results:

```text
targetsBuilt = [40000, 60000, 80000, 100000]
allHuggingFaceSaveReloadChecks = PASS
allSpecialTokenChecks = PASS
allTokenizerEmbeddingAlignmentChecks = PASS
allNonEmbeddingWeightsBitExact = true
allObservedSelectionPiecesRetained = true
allRecordedFileHashesAndSizes = PASS
unitTests = 7/7 PASS
```

All four candidate artifacts were reloaded independently, retained 12 layers, aligned tokenizer IDs with embedding rows, and completed a real forward pass.

## 5. Candidate size comparison

The INT8 column is an analytical runtime-footprint estimate. **No Student-5 quantization was performed in Phase A.** Embeddings and one-dimensional parameters remain counted as FP32; eligible non-embedding matrices are counted at one byte per parameter.

| Vocab | Embedding params | Total params | Param reduction | FP32 model bytes | Artifact bytes | Tokenizer bytes | Estimated INT8 bytes | Est. reduction vs Student-4 Mixed | Gate |
|---:|---:|---:|---:|---:|---:|---:|---:|---:|---|
| Original | 96,014,208 | 117,653,760 | — | 470,657,952 | 475,734,505 | 5,069,203 | 406,471,680 | -171.50% | Reference |
| **40k** | **15,360,000** | **36,999,552** | **68.552%** | **148,020,400** | **150,116,913** | **885,726** | **83,854,848** | **43.989% smaller** | **PASS / selected** |
| 60k | 23,040,000 | 44,679,552 | 62.024% | 178,740,552 | 181,807,197 | 1,235,858 | 114,574,848 | 23.469% smaller | PASS |
| 80k | 30,720,000 | 52,359,552 | 55.497% | 209,460,584 | 213,508,337 | 1,596,966 | 145,294,848 | 2.950% smaller | PASS |
| 100k | 38,400,000 | 60,039,552 | 48.969% | 240,180,584 | 245,220,667 | 1,969,293 | 176,014,848 | 17.569% larger | FAIL size |

The selected 40k FP32 weight file is 68.550% smaller than upstream. The 60k candidate costs 30,720,000 additional estimated runtime bytes over 40k for only small quality improvements, so 40k lies on the Phase-A efficiency frontier.

## 6. Independent coverage probe

The project-authored probe is separate from the serialized vocabulary-selection corpus:

| Property | Value |
|---|---:|
| Coverage sentences | 95 |
| Semantic-comparison unique sentences | 161 |
| Semantic contrast pairs | 36 |
| Adult/intimacy sentences | 50 |
| Explicit code-switch cases | 8 |
| Exact probe/selection-text overlap | 0 |
| Canonical dev used | false |
| Frozen used | false |

All candidates have zero UNK on all reported slices.

### Tokenization metrics

Inflation is aggregate candidate token count divided by the exact upstream tokenizer token count.

| Vocab | Overall mean/p95 tokens | IT inflation | EN inflation | ES inflation | Adult inflation | Code-switch inflation | Names/locations inflation |
|---:|---:|---:|---:|---:|---:|---:|---:|
| Original | 12.453 / 17 | 1.000 | 1.000 | 1.000 | 1.000 | 1.000 | 1.000 |
| **40k** | **13.053 / 18** | **1.037634** | **1.037037** | **1.066852** | **1.039074** | **1.059406** | **1.060606** |
| 60k | 12.895 / 17 | 1.030 | 1.031 | 1.045 | 1.026 | 1.040 | 1.030 |
| 80k | 12.768 / 17 | 1.024 | 1.020 | 1.033 | 1.019 | 1.020 | 1.030 |
| 100k | 12.684 / 17 | 1.013 | 1.017 | 1.025 | 1.013 | 1.020 | 1.030 |

ES is the most affected selected-candidate language at 1.066852 inflation, still well within the declared 1.15 language threshold.

### Selected 40k adult/intimacy detail

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

Adult/intimacy 40k language slices:

| Language | Mean tokens | p95 tokens | Inflation | UNK |
|---|---:|---:|---:|---:|
| IT | 15.143 | 20 | 1.019 | 0 |
| EN | 13.714 | 17 | 1.038 | 0 |
| ES | 14.786 | 21 | 1.051 | 0 |

## 7. Representation-preservation quality

Mean-pooled last-hidden-state representations were compared against the pinned upstream model. Contrast families cover negation, question/request, correction, third-party statements, past/future temporal changes, and adult distinctions including desire/request, consent/refusal, consent withdrawal, preference/experience, target, and fact/hypothesis.

| Vocab | Mean cosine | Worst cosine | p05 cosine | Mean contrast delta | p95 contrast delta | Max contrast delta | Unchanged tokenization | Max forward delta |
|---:|---:|---:|---:|---:|---:|---:|---:|---:|
| **40k** | **0.995580** | **0.943703** | **0.976073** | **0.007855** | **0.045259** | **0.051024** | **103** | **0.0** |
| 60k | 0.996501 | 0.943703 | 0.979299 | 0.007855 | 0.045259 | 0.051024 | 111 | 0.0 |
| 80k | 0.997081 | 0.943703 | 0.979299 | 0.007497 | 0.045259 | 0.051024 | 120 | 0.0 |
| 100k | 0.997841 | 0.943703 | 0.987107 | 0.006775 | 0.045259 | 0.051024 | 132 | 0.0 |

For 40k, all three negation contrast pairs and all Italian consent/refusal/withdrawal contrasts have zero cosine-delta relative to upstream. The largest contrast delta, 0.051024, occurs on Spanish adult consent withdrawal; the declared gate uses mean <=0.02 and p95 <=0.05, both passing. On the 103 sentences whose tokenization is unchanged after explicit ID remapping, forward outputs are numerically identical.

## 8. Fixed gate matrix

Thresholds were defined before measurement and were not lowered.

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
| Est. INT8 vs 149,711,344 B | smaller | PASS | PASS | PASS | FAIL |

## 9. Artifact identity and checksums

### Selected 40k artifact

| Field | Value |
|---|---|
| Model SHA-256 | `d6e45891d1e0ec4ed023caaeb17c0dd0ae80a93b8bf877d275310b7f2837efa2` |
| Mapping SHA-256 | `da36a5e1a9057391da935354d895edb3bc3a959744aca6b6602e511f9d4ea9b9` |
| SentencePiece SHA-256 | `748f8053688469d7dc98c135a28a3fc0713bdbb82853f86f8d7a254bada46f78` |
| Candidate-manifest SHA-256 | `a9d23de7816d487986316351c163f37a67d65d001861dbf042b9114c455f066d` |
| FP32 model bytes | 148,020,400 |
| Artifact-directory bytes | 150,116,913 |
| Estimated runtime INT8 bytes | 83,854,848 |
| Preserved archive bytes | 88,361,246 |
| Preserved archive SHA-256 | `7804bfb245b71df9b835fff7ee00f6ec887e019772ae34c82d269d821d587191` |

### Other candidate identities

| Vocab | Model SHA-256 | Mapping SHA-256 | SentencePiece SHA-256 | Manifest SHA-256 |
|---:|---|---|---|---|
| 60k | `5e8278b0772bb7dc2a18139c288931446b1a1c2089254d0e5d13c85e35bf6c48` | `6490295a55dbb7bfbade04ef57386b711b444d855febea0cedf0826458062c91` | `fcd96533998f8ae231348ca29724567d4701e487ddb7c82ee0a9ef8d033766e8` | `fe3021e5acf8a861ab2982335b5a6b810185057f33f8f91c5cb39cf661a0bcd4` |
| 80k | `79711969c70b6f03929dcc2e813c3b77da3b95227e5c820c68a0c2820c692e42` | `2b5128b5c5cc96efabd82a0cd469b22099c399b4d8acaf271bbc3f07492b05db` | `a6e74b54adfcbd08078ebddf503aa5926d15a5b414e85714e15e6642c22c86f0` | `01c64d309516db92332025fb0754cc76fe3e65e64b9030a6c1503685db97eaef` |
| 100k | `051eac9b10ec7404e0eaa527256853318f70ec42ebfc7523945ca2378cd51966` | `0e3d2fb44aaabb623a85d75ee2fa0cbd37a41a08e5985e077122dc946e90738b` | `0080da898b8d288710361931d2f69b64a46e0d25fc606525146d9ba575ca95b9` | `af4f4f832848936245e19fb9ab53cc2d229d775f34e2d52104218124acf258f4` |

The selected archive contains the FP32 model, reduced tokenizer, bidirectional ID remap, aggregate and candidate manifests, corpus provenance, Frozen guard, reports, source, and `SHA256SUMS`. ZIP integrity and every recorded internal checksum pass.

Repository implementation/report commits: `25546528917d42d70129f059ff56da672678c7d4`, corrected by `a1d407d63d4dcb84033d8ac525cce0e2475c27e1`.

## 10. Matrix-NLU metrics that do not yet exist

The following metrics are intentionally reported as **not measured**, not zero:

| Matrix metric | Student-5 MiniLM 40k status |
|---|---|
| Exact-set accuracy | Not measured — no Matrix heads |
| Claim exact | Not measured — no Matrix heads |
| Negation F1 | Not measured — no Matrix heads |
| Predicate accuracy | Not measured — no Matrix heads |
| Ownership corruption | Not measured — no Matrix heads |
| Temporal accuracy | Not measured — no Matrix heads |
| Referent accuracy | Not measured — no Matrix heads |
| World Truth updates | Not measured — no Matrix runtime evaluation |
| Selective accuracy / calibration | Not measured — no trained confidence layer |
| Canonical dev gate | Not executed for Student-5 |

Student-4-v2.2A results must not be copied into this dossier as Student-5 metrics. They remain a separate comparative baseline for the future teaching phase.

## 11. Quality interpretation and residual risks

### What the evidence supports

- The 40k tokenizer/embedding reduction is internally consistent and reloadable.
- All observed TRAIN-selection pieces are retained.
- IT, EN, ES, adult/intimacy, code-switch, and name/location probes have zero UNK.
- Token inflation remains within every fixed Phase-A limit.
- Hidden representations stay close to the pinned upstream model.
- Unchanged tokenizations produce exactly unchanged forward outputs.
- The 40k candidate offers the strongest measured size/quality trade-off.

### What the evidence does not support

- It does not prove Matrix claim extraction, negation detection, predicate classification, ownership safety, temporal interpretation, or referent resolution.
- It does not prove calibrated abstention or downstream Memory/Authority safety.
- It does not constitute canonical-dev, Frozen, mobile, Assembling, or production validation.
- It does not establish actual INT8 parity, latency, or memory behavior.
- The probe is intentionally independent and multilingual but remains small.
- Zero UNK does not mean identical segmentation; Spanish has the highest selected-candidate inflation.

## 12. Required next evaluation stage

Only after separate authorization, the pristine 40k FP32 artifact may enter the Matrix teaching path. That stage must add/train the Matrix heads, evaluate canonical dev under unchanged gates, report per-language and per-family errors, preserve Student-4-v2.2A as comparison, and keep Frozen closed until a final candidate is locked.

The untaught runtime/INT8 path, if executed, must remain a separate infrastructure probe and must be labeled:

```text
STUDENT_5_40K_UNTAUGHT_INT8
RUNTIME_PROBE_ONLY
NOT_MATRIX_NLU
NOT_PRODUCTION_APPROVED
```

## 13. Mutation and safety guard

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

Final Phase-A disposition:

```text
PRUNING_CANDIDATE_SELECTED
selectedVocabSize = 40000
REPRESENTATION_PRESERVING_BACKBONE
NOT_MATRIX_NLU
FROZEN_UNREAD
NOT_PRODUCTION_APPROVED
```

Canonical detailed evidence remains in `reports/STUDENT_5_MINILM_DEEP_PRUNING.md`. This dossier exists as the analysis-ready quality summary for MiniLM/Student-5.
