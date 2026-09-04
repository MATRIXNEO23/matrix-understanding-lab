# WORK PROMPT — Student-5 Multilingual MiniLM IT/EN/ES Pruned

Repo: `MATRIXNEO23/matrix-understanding-lab`
Branch: `main`
Date: 2026-09-04

## Objective

Evaluate whether `microsoft/Multilingual-MiniLM-L12-H384` can become a better Matrix-NLU backbone than Student-4-v2.2A by pruning its very large multilingual vocabulary down to an IT/EN/ES-focused vocabulary while preserving the full 12-layer Transformer.

This is a controlled Student-5 experiment. Student-4-v2.2A remains the current R2/CANDIDATE baseline and must not be modified.

Primary hypothesis:

```text
Multilingual MiniLM L12-H384
12 Transformer layers
hidden size 384
vocab size 250037

→ prune vocabulary/embedding rows for IT+EN+ES
→ retain full 12-layer Transformer
→ add the same Matrix multi-task heads
→ compare quality/size/latency against Student-4-v2.2A
```

Official backbone facts to verify and pin before implementation:

```text
repository = microsoft/Multilingual-MiniLM-L12-H384
model_type = bert
tokenizer_class = XLMRobertaTokenizer
hidden_size = 384
intermediate_size = 1536
num_attention_heads = 12
num_hidden_layers = 12
vocab_size = 250037
```

Pin an exact upstream revision before any reproducible artifact is created.

## Canonical project rules — mandatory

1. DO NOT LOWER GATES.
2. Do not modify dev thresholds to make Student-5 pass.
3. Do not read, inspect, modify, tokenize, mine or otherwise use Frozen for pruning, tuning, training or debugging.
4. Do not modify canonical dev or frozen examples.
5. Any supervised augmentation must be TRAIN-ONLY.
6. Vocabulary selection must not use dev/frozen examples.
7. Student-4-v2.2A remains untouched and is the direct baseline.
8. Do not promote Student-5 automatically.
9. Do not quantize Student-5 before a real FP32 dev evaluation exists.
10. If later quantized, use Mixed / Head-Protected INT8 and preserve all 15 Matrix semantic heads in FP32.
11. Infrastructure failures are not model failures: fix import/PYTHONPATH/runner/dependency issues before judging the model.
12. Perform targeted error analysis instead of weakening acceptance criteria.

## Matrix heads to preserve exactly

Token heads:

```text
token.boundary
token.object
token.subject
token.negation
token.temporal
token.entity
```

Sequence heads:

```text
sequence.dialogueAct
sequence.predicate
sequence.subjectReferent
sequence.targetReferent
sequence.ownerReferent
sequence.perspectiveReferent
sequence.polarity
sequence.temporalRelation
sequence.claimKind
```

MASSIVE auxiliary heads remain auxiliary:

```text
massive.intent
massive.slot
```

## Important compatibility issue

Do NOT assume the current `matrix_nlu/model.py` works unchanged.

Current Student-4 code assumes DistilBERT internals:

```text
encoder.transformer.layer
encoder.config.dim
encoder.config.n_layers
```

Multilingual MiniLM is exposed as a BERT model and normally uses:

```text
encoder.encoder.layer
encoder.config.hidden_size
encoder.config.num_hidden_layers
```

Implement the minimum architecture-neutral abstraction needed, or create a Student-5-specific model builder. Do not break Student-4 compatibility.

Add regression tests proving both the existing DistilBERT path and the MiniLM path build correctly.

# PHASE A — Vocabulary-pruning feasibility

Do this before full Matrix training.

## A1. Pin and inspect upstream model

Record:

- exact Hugging Face repository and revision;
- license;
- config;
- tokenizer class/files;
- original parameter counts;
- original embedding parameter count;
- original FP32 model size;
- original tokenizer vocabulary size;
- special-token IDs and tokenizer/model ID mapping.

Do not assume SentencePiece piece IDs are identical to Hugging Face tokenizer IDs. Derive and test the actual mapping.

## A2. Build a vocabulary-selection corpus

Use only training-safe text.

Required sources:

- Matrix-NLU TRAIN partition only;
- v2/v2.2A TRAIN-only repair rows if useful;
- MASSIVE IT/EN/ES TRAIN partition only.

If these are too narrow for safe lexical coverage, add a public external IT/EN/ES corpus only when:

- license/provenance are explicit and recorded;
- it is used only for unsupervised vocabulary frequency/coverage analysis;
- no canonical Matrix dev/frozen text is included;
- the source can be pinned/reproduced.

Do not silently scrape arbitrary web text.

## A3. Test several target vocabulary sizes

At minimum test:

```text
40k
60k
80k
100k
```

Always preserve:

- all required special tokens;
- punctuation and digits;
- common Latin characters/diacritics used by IT/EN/ES;
- tokens required for robust names, contractions, code-switching and ordinary user chat;
- any tokenizer-control pieces required by XLM-R/SentencePiece.

Selection should be frequency-based with explicit safety rules, not language-name heuristics.

## A4. Produce a real pruned tokenizer + embedding table

The experiment is not complete if it only estimates parameter counts.

For each viable target vocabulary:

1. construct a loadable reduced tokenizer;
2. create deterministic old-token-id → new-token-id mapping;
3. slice/remap the original MiniLM word embeddings to exactly match the new tokenizer IDs;
4. update model/tokenizer config consistently;
5. preserve all non-embedding Transformer weights unchanged;
6. save a loadable Hugging Face-style pruned backbone artifact;
7. verify save/reload round trip.

Fail closed if special-token mapping or embedding/tokenizer alignment is uncertain.

## A5. Coverage/quality gate before training

Create a held-out tokenizer probe set that was NOT used to select vocabulary. It may be project-authored or sourced from a separate training-safe/public corpus, but must not use canonical dev/frozen.

Include IT, EN, ES and code-switching, with:

- ordinary conversation;
- negation;
- questions/requests;
- corrections;
- ownership/referents;
- temporal expressions;
- names and locations;
- accented characters;
- colloquial contractions;
- adult/intimacy semantic terms as ordinary NLU vocabulary, without moderation labels.

For every vocabulary candidate report:

```text
vocab size
embedding parameters
total parameters
FP32 bytes / estimated INT8 bytes
UNK rate by language
mean tokens per sentence by language
p95 tokens per sentence by language
tokenization inflation vs original MiniLM
code-switching tokenization inflation
special-token integrity
save/reload integrity
```

Also compare original MiniLM vs pruned MiniLM forward outputs on sentences whose token sequence is unchanged after remapping. With identical retained pieces/embeddings and unchanged Transformer weights, outputs should be numerically equivalent within a very tight tolerance.

## PHASE A GO/STOP GATE

Choose the smallest vocabulary that satisfies all of the following:

- special-token integrity = PASS;
- tokenizer/model ID alignment = PASS;
- save/reload = PASS;
- no abnormal UNK behavior in IT/EN/ES;
- tokenization inflation is acceptably small and documented;
- no catastrophic degradation on code-switching/names/diacritics;
- materially smaller than original MiniLM;
- expected runtime size is competitive with or smaller than Student-4-v2.2A Mixed (~149.7 MB).

Do NOT choose 40k merely because it is smallest. Prefer 60k/80k/100k if coverage is materially safer.

If no tested vocabulary passes, STOP and report `VOCAB_PRUNING_NOT_JUSTIFIED`. Do not train Student-5.

# PHASE B — Student-5 Matrix training

Proceed automatically only if Phase A passes.

## B1. Architecture

Use the selected pruned MiniLM backbone with all 12 Transformer layers retained initially.

Add the same Matrix token/sequence heads and MASSIVE auxiliary heads used by Student-4.

Do not reduce layers in the first Student-5 run. The purpose is to test whether deeper/narrower MiniLM beats the 4-layer DistilBERT student at a competitive size.

Model-builder code must be architecture-neutral and must keep Student-4 regressions green.

## B2. Training data

Use the existing canonical Matrix training pipeline and v2.2A TRAIN-only repair knowledge where appropriate.

Rules:

- canonical dev unchanged;
- Frozen unread;
- MASSIVE train/dev usage remains provenance-controlled;
- no test/frozen leakage;
- no arbitrary data augmentation without recorded provenance;
- do not simplify labels or remove hard cases to improve scores.

## B3. Training strategy

Start from a conservative configuration derived from Student-4-v2.2A, adjusted only where hidden size/model architecture requires it.

Retain targeted loss emphasis for fragile Matrix heads, especially:

```text
negation
predicate
polarity
ownerReferent
dialogueAct
subject/object/span heads
```

Do not blindly copy Student-4 learning-rate/layer assumptions if MiniLM requires a different stable optimizer configuration; document every change and rationale.

Use early stopping and preservation checkpoints.

## B4. Development evaluation

Run the same canonical dev and P0.5 evaluation used for Student-4-v2.2A.

Compare directly against Student-4-v2.2A on:

- Matrix exact claim set;
- P0.5 exact claim set;
- claim exact;
- negation F1 by IT/EN/ES;
- predicate by IT/EN/ES;
- dialogueAct;
- subject/target/owner/perspective referents;
- polarity;
- temporalRelation;
- span decoding residuals;
- entity resolution residuals;
- ownership corruption;
- third-party/report;
- correction;
- question/request;
- adult/intimacy semantic robustness;
- valid coverage;
- World Truth updates;
- parameter count and estimated runtime size.

Do not reinterpret a failed canonical gate as a pass.

## B5. Error analysis

If Student-5 misses the gate, perform a targeted error analysis before proposing another training run.

Identify whether failure comes from:

- vocabulary pruning/tokenization;
- MiniLM backbone adaptation;
- head training;
- class imbalance;
- span decoding;
- insufficient training examples;
- architecture mismatch.

Do not immediately enlarge the model or lower thresholds.

# PHASE C — Export/quantization policy

Do NOT execute Frozen automatically.

If Student-5 passes canonical dev gate:

```text
DEV_GATE_PASSED_AWAITING_FROZEN_AUTHORIZATION
```

Stop there unless the owner separately authorizes Frozen.

FP32 ONNX export may be prepared only after a valid FP32 dev result exists.

If mixed quantization is later authorized, quantize encoder/backbone while protecting all 15 Matrix heads in FP32 and compare every fragile head against FP32. Reject quantization if critical semantic metrics degrade materially.

# Required artifacts

Create at minimum:

```text
reports/STUDENT_5_MINILM_PRUNING_FEASIBILITY.md
reports/STUDENT_5_MINILM_DEV_REPORT.md          # only if Phase B runs
docs/WORK_CONTINUITY_STUDENT_5.md
```

Phase A artifact should include:

- pinned upstream revision/license;
- tested vocabulary sizes;
- coverage tables;
- tokenizer inflation tables;
- parameter/size estimates and actual saved sizes;
- chosen vocabulary and rationale;
- SHA-256 for pruned tokenizer/backbone files;
- explicit confirmation that Frozen was not read.

Phase B report should include:

- run/job/commit/artifact IDs;
- direct Student-4-v2.2A comparison;
- all critical metrics;
- regression/error analysis;
- canonical gate result;
- exact next action.

Update continuity after every significant checkpoint and before any long/risky operation.

# Final statuses

Phase A can end as:

```text
VOCAB_PRUNING_FEASIBLE
VOCAB_PRUNING_NOT_JUSTIFIED
INFRASTRUCTURE_BLOCKED
```

Phase B can end as:

```text
STUDENT_5_CANDIDATE
DEV_GATE_PASSED_AWAITING_FROZEN_AUTHORIZATION
STOPPED_FOR_REVIEW
```

No production promotion is allowed automatically.

# Execution style

Work autonomously until a defined GO/STOP gate is reached. Do not stop for cosmetic questions. Fix only real infrastructure/code issues, preserve provenance, keep Frozen closed, and report concise evidence rather than speculative commentary.
