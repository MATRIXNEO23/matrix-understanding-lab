# Student-4-v2.2A Final Repair Mix

Date: 2026-09-04
Status: FINAL MIX DECISION / TRAIN-ONLY REPAIR SPEC

## Binding constraints

- Do not lower gates.
- Do not modify dev.
- Do not modify or read frozen.
- Do not export ONNX before dev gate passes.
- Do not quantize before dev gate passes.
- Do not promote to production automatically.
- All augmentation in this document is TRAIN-ONLY.
- Adult/intimacy rows are semantic robustness rows, not moderation/safety/censorship rows.

## Final dataset size

Student-4-v2.2A repair dataset: 375 new TRAIN-ONLY examples.

## Final block distribution

| Block | Examples | Percent |
|---|---:|---:|
| IT core | 139 | 37.07% |
| ES core | 70 | 18.67% |
| EN core | 69 | 18.40% |
| Adult/intimacy IT | 60 | 16.00% |
| Cross-lingual contrast | 37 | 9.87% |
| Total | 375 | 100.00% |

## Reasoning

The allocation is intentionally not language-balanced. It is error-driven:

- Italian remains the main target language and keeps the largest repair share.
- Spanish is kept high enough to address the severe negation failure, but not allowed to dominate.
- English is increased because P0.5 predicate/claim-structure errors remain important and adult Italian may include common English terms.
- Adult/intimacy Italian is integrated into v2.2A, not postponed to a separate phase.
- Cross-lingual contrast protects against shortcuts across IT/ES/EN negation and predicate patterns.

## Internal target allocation

### IT core — 139 examples

| Target | Examples | Purpose |
|---|---:|---|
| Negation | 63 | Repair IT Matrix negation collapse and exact-set cascade |
| Predicate | 28 | Repair P0.5 predicate and claim typing |
| Ownership/referents | 22 | Prevent Italian owner/perspective corruption |
| Question/request/correction/report | 15 | Separate question/request/report/correction from stable facts |
| Span/temporal | 11 | Reduce span and temporal decoding cascades |
| Total | 139 | |

### ES core — 70 examples

| Target | Examples | Purpose |
|---|---:|---|
| Negation | 46 | Main ES fix: Matrix negation collapse |
| Predicate | 16 | Repair P0.5 predicate weakness |
| Referents/span | 6 | Keep subject/object/referent consistency |
| Question/request | 2 | Minimal dialogueAct protection |
| Total | 70 | |

### EN core — 69 examples

| Target | Examples | Purpose |
|---|---:|---|
| Predicate | 38 | Main EN fix: P0.5 predicate/claim typing |
| Claim structure / multi-claim | 12 | Improve exact-set/claim-exact on hard cases |
| DialogueAct/correction | 10 | Separate request/question/correction from facts |
| Negation | 7 | Maintain existing strong negation without overfitting |
| Span/temporal | 2 | Minimal stability coverage |
| Total | 69 | |

### Adult/intimacy IT — 60 examples

| Target | Examples | Purpose |
|---|---:|---|
| Desire/assert | 15 | Classify intimate desire as semantic intent, not error |
| Request | 15 | Classify direct intimate requests without blocking |
| Consent | 11 | Recognize positive consent patterns |
| Refusal/boundary | 8 | Recognize refusal, limit, stop, not-now patterns |
| Common English terms inside Italian sentences | 11 | Avoid false errors on common English intimate slang/loanwords |
| Total | 60 | |

Rules for this block:

- No public adult dataset is imported raw.
- No safety/moderation label is used.
- No automatic blocking/censorship label is introduced.
- Terms can map to REQUEST, ASSERT, QUESTION, goal.object, consent.grant, consent.refuse or speech.unresolved.
- Unknown adult terms must not become hard errors or stable memory facts.
- Refusal/limit examples must remain present even if fewer than desire/request rows.

### Cross-lingual contrast — 37 examples

| Target | Examples | Purpose |
|---|---:|---|
| Negation triplets/pairs | 15 | Align IT/ES/EN negation semantics |
| Predicate triplets/pairs | 10 | Align predicate selection |
| Question/request contrast | 6 | Prevent facts from being inferred from questions/requests |
| Correction/ownership contrast | 6 | Protect authority and owner routing |
| Total | 37 | |

## Expected dev focus

Primary post-training checks:

- IT Matrix negation F1.
- ES Matrix negation F1.
- EN/IT/ES P0.5 predicate accuracy.
- Matrix and P0.5 exact-set.
- Matrix and P0.5 claim-exact.
- Ownership corruption must be zero.
- World Truth invented must remain zero.
- Adult/intimacy rows must not introduce block/censor behavior.

## Stop policy

Stop and do not quantize if any of the following is true:

- Dev gate fails.
- Ownership corruption is above zero.
- World Truth updates are above zero.
- Negation remains unsafe in IT or ES.
- Predicate remains unsafe on P0.5.
- Exact-set does not improve enough to justify the repair.
- Adult/intimacy robustness causes censorship-like classification or false hard errors.

## Final decision

Use this mix as the canonical Student-4-v2.2A repair distribution.

Student-4-v2.2A is still a research candidate until it passes the unchanged dev gate. No frozen access, ONNX export, INT8/mixed quantization, Android integration or production promotion is authorized by this document.
