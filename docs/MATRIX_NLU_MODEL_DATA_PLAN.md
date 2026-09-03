# Matrix-NLU model and data plan

Status: `GATE 01 IN PROGRESS — LAB ONLY`  
Canonical architecture: `cf6395b0fefc254febe3c804751ca4b048f974d1`  
Production runtime: frozen and out of scope.

## Decision boundary

The stopped OpenNLP Candidate B is retained as benchmark, oracle and bounded
fallback. It is not the production architecture. Matrix-NLU will use a compact
pretrained multilingual Transformer, learned multi-task heads and a deterministic
validator limited to Matrix invariants. Linguistic regex/rule accumulation is
explicitly forbidden.

## Encoder shortlist

| Candidate | Intended role | Evidence before probe | Risk to resolve |
|---|---|---|---|
| `Geotrend/distilbert-base-en-es-it-cased` | primary training candidate | exact IT/EN/ES vocabulary-pruned DistilmBERT; Apache-2.0; public model index reports 73.2M parameters | immutable revision, tokenizer coverage, actual weight/INT8 size and Android PSS |
| `microsoft/Multilingual-MiniLM-L12-H384` | quality reference | mature multilingual distilled encoder; 21M Transformer parameters | XLM-R embeddings dominate total size and may exceed the mobile no-go band |
| `microsoft/xtremedistil-l6-h256-uncased` | size reference only | MIT; 13M parameters | model card is tagged English and reports only English benchmarks; not accepted as multilingual without contrary evidence |

The metadata/tokenizer probe records immutable Hub revisions and declared
licenses before a weight is used. If the exact-language DistilmBERT clears this
gate, the first learned system will use it as teacher. A 4-layer student formed
from pretrained teacher layers plus supervised/logit distillation is the planned
mobile candidate; the 6-layer teacher remains the quality comparator. This keeps
the encoder pretrained while targeting tens, rather than hundreds, of megabytes.

No model is production-approved by this document. The model family may change
autonomously if quality, export or mobile resource evidence stalls.

## Layered training data

| Layer | Use | License/provenance policy | Leakage control |
|---|---|---|---|
| MASSIVE IT/EN/ES | auxiliary request/intent and slot-span supervision | dataset CC BY 4.0; pin download digest and retain NOTICE/attribution | preserve official train/dev/test partitions; never tune on official test |
| Matrix generated/curated | full typed-claim heads, multi-claim and ownership semantics | repository-authored generator, seed and generator commit recorded | held-out template families, lexicons and compositions |
| adversarial/noisy | incomplete grammar, typos, code-switch, negation, correction, temporal, third party, consent/refusal | repository-authored with adult-only safety constraints | independently frozen benchmark generator/data |
| real regressions | previous Moto and P0/P0.5 failures | source IDs and frozen hashes retained | frozen tests are not training input |

MASSIVE ontology is auxiliary evidence, not the Matrix ontology. Its 60 intents
and 55 slots must be mapped into a small task family or used as auxiliary heads;
they must not silently become Matrix predicates.

Italian remains primary, with English and Spanish mandatory. Italian-only
resources previously reviewed remain reserve components and are not discarded
solely for lacking trilingual coverage.

## Learned output and deterministic boundary

Learned heads cover claim boundaries, dialogue act, predicate, semantic roles,
entity/span types, negation, temporality, hypothesis/correction/request/goal and
ambiguity/confidence. The invariant validator may only:

- enforce schema and char-span validity;
- bind speaker/observer identifiers supplied by context;
- forbid implicit promotion to World Truth;
- enforce ownership/authority and memory admission permissions;
- abstain/reject internally inconsistent low-confidence output.

It may not infer predicates, split clauses, detect negation or repair language by
regex. OpenNLP predictions can score or diagnose the student but cannot be copied
into production output as a hidden deterministic mapper.

## Required gates before Moto

1. immutable model/data revisions, licenses, notices and byte hashes;
2. deterministic dataset build with disjoint train/dev/frozen test;
3. multi-task unit/integration tests and zero ownership/World Truth corruption;
4. near-perfect frozen adversarial quality with no systematic critical family;
5. calibrated confidence/abstention and error analysis by language/family;
6. ONNX export parity, INT8 quality delta, offline Android build and measured
   artifact/RAM/CPU/latency evidence;
7. green CI with reproducible artifacts.

Moto G56 testing is deliberately not requested until all software, quality and
provenance gates above are green.

## Primary sources

- Geotrend model card and *Load What You Need: Smaller Versions of Multilingual
  BERT* (SustaiNLP/EMNLP 2020).
- Microsoft Multilingual MiniLM and XtremeDistil model cards/papers.
- Amazon MASSIVE repository, dataset NOTICE and CC BY 4.0 license.
- ONNX Runtime quantization and mobile deployment documentation.
