# Student-5 Matrix-NLU Contract V3 Implementation

## 1. Executive verdict

```text
TASK 2.2 = CONTRACT_V3_IMPLEMENTATION_PASS_WITH_NONBLOCKING_RISKS
contract = MATRIX_NLU_CONTRACT_V3
implementationP0Remaining = 0
trainingExecuted = false
canonicalDevUsed = false
Frozen = UNREAD
```

The frozen V3 contract is implemented as a separate canonical path with 16 heads (6 token, 10 sequence), deterministic referent candidates, five independent role pointers, plural span evidence, field-aware abstention, independent gold evaluation, and fail-closed bundle metadata. The nonblocking risks are physical Student-5/Torch loading and ONNX export, which were not executable in this environment because Torch, Transformers, ONNX, and ONNX Runtime are not installed. No result from random heads is presented as quality evidence.

## 2. Start and implementation HEAD

```text
HEAD start = db60bf1f8bc1fc227ea314d9354c58db9ada6150
implementation HEAD = 3aa9d135661f15647e9d4b75dde6779025ee5fcd
branch = main
```

The final documentation commit is recorded in `docs/WORK_CONTINUITY_STUDENT_5.md` and returned with the task handoff.

## 3. Files changed

Added V3 implementation modules:

- `matrix_nlu/contract_v3.py`
- `matrix_nlu/referent_candidates.py`
- `matrix_nlu/model_v3.py`
- `matrix_nlu/inference_v3.py`
- `matrix_nlu/evaluate_v3.py`
- `matrix_nlu/training_data_v3.py`
- `matrix_nlu/migrate_contract_v3.py`
- `matrix_nlu/export_onnx_v3.py`
- `matrix_nlu/synthetic_v3_fixtures.py`

Added tests:

- `matrix_nlu/test_contract_v3_core.py`
- `matrix_nlu/test_inference_v3.py`
- `matrix_nlu/test_evaluate_v3.py`
- `matrix_nlu/test_training_data_v3.py`
- `matrix_nlu/test_migrate_contract_v3.py`

Modified only one legacy implementation line: `matrix_nlu/evaluate_e2e.py` now accepts the canonical `CORRECT` label without the stale `CORRECTION` alias. Continuity and this report are documentation changes. No dataset, model weight, tokenizer, Student-4, Path-A, DEV, or Frozen file was changed.

## 4. Frozen V3 registry implemented

Token heads, in exact order: `boundary`, `object`, `subject`, `negation`, `temporal`, `entity`.

Sequence heads, in exact order: `dialogueAct`, `predicate`, `subjectReferent`, `targetReferent`, `ownerReferent`, `perspectiveReferent`, `sourceReferent`, `polarity`, `temporalRelation`, `claimKind`.

The fixed ordered labels match the frozen specification. `sourceReferent` is a first-class independent pointer. The runtime rejects `SELF`, `SUBJECT`, `KNOWN_ENTITY`, and `RECENT_ENTITY` in V3.

The deterministic registry fingerprint at the default `maxReferentCandidates=16` is:

```text
7b0646e44243ad897760c0fcadbe141f1b8e88e3fd8d63a1789106571b9987b0
```

## 5. Student-5 BERT adapter

`model_v3.py` resolves hidden size through architecture-neutral config fields and explicitly supports BERT `encoder.layer` as well as isolated DistilBERT compatibility through `transformer.layer`. The head attachment accepts an injected encoder or loads through `AutoModel` with `trust_remote_code=false`. A synthetic BERT-structure regression passes. No pretrained file was opened or mutated, no optimizer exists in this module, and no physical pristine load was run because the required ML packages are absent locally.

## 6. Sixteen-head architecture

Six token classifiers operate on sequence hidden states. Five categorical sequence classifiers operate on the pooled first-token state. Five role heads share one candidate projection but each owns an independent learned role query. `temporalRelation` has independent relation logits and anchor-pointer logits. This gives exactly 16 conceptual heads; the temporal head exports two tensors by design.

## 7. Candidate/pointer architecture

Candidate kinds are exactly `CONTEXT_SPEAKER`, `CONTEXT_OBSERVER`, `MENTION`, and `CONTEXT_ENTITY`; reserved IDs are `ctx:speaker` and `ctx:observer`. Mention IDs are assigned deterministically after span/type ordering. Candidate order preserves speaker, observer, mentions overlapping critical spans, remaining mentions, then optional context-only candidates.

The default maximum is versioned as 16. Overflow is surfaced with dropped IDs and lost-critical IDs. If a critical candidate is lost, decoding abstains instead of guessing. Each role chooses a candidate ID, `NONE`, or `UNKNOWN` using a separate masked pointer distribution.

## 8. Source/perspective separation

`sourceReferent` and `perspectiveReferent` are independent heads, fields, evaluator targets, and confidence entries. The regression for “Marco told me that Anna loves Luca” preserves source/perspective=Marco, subject/owner=Anna, target=Luca without a shared-subject shortcut.

## 9. Negation/polarity implementation

The negation token registry contains only `O`, `B-NEGATION_CUE`, and `I-NEGATION_CUE`. All BIO groups are preserved in `negationCueSpans[]`. `polarity` is independently decoded as `POSITIVE`, `NEGATIVE`, or `UNKNOWN`; neither field derives the other. Synthetic structural cases cover no cue, one cue, multiple/double cues, and metalinguistic examples in IT/EN/ES.

## 10. Temporal relation and anchor

The exact relation registry is implemented. `BEFORE`, `AFTER`, `DURING`, and `AT_REFERENCE` require a valid anchor reference; missing/invalid anchors make the claim structurally invalid and abstained. Accepted anchor namespaces implement speech time, context reference, temporal evidence, and claim references. No wall-clock value is fabricated.

## 11. Multi-span decoding

BIO decoding returns every valid non-overlapping group. Canonical claim fields are plural: `subjectSpans[]`, `objectSpans[]`, `negationCueSpans[]`, `temporalEvidence[]`, and `entityMentionIds[]`. A two-claim regression verifies both flat atomic claims and their distinct evidence survive decoding. Nested claims remain outside V3 by contract.

## 12. Confidence and abstention

Every semantic field can expose value, confidence, field status, and ranked alternatives. Claims expose `structuralStatus`, `interpretationStatus`, `overallInterpretationConfidence`, and diagnostics. Overall confidence is bounded by the minimum required critical-field confidence. Thresholds are optional versioned configuration; no final numeric thresholds were invented. Structural invalidity or configured low critical confidence can yield `ABSTAINED`.

## 13. Independent evaluator

`evaluate_v3.py` deliberately does not import the production decoder or validator. It independently normalizes authored V3 gold and scores claim count, categorical fields, all five pointer identities, plural spans, temporal relation/anchor, per-field status, interpretation status, ownership corruption, and source corruption. Regressions prove a wrong pointer is detected rather than mirrored into gold.

## 14. Bundle fingerprint validation

Bundle metadata records contract version, schema version, ordered heads, head types, ordered label registries, pointer special values, candidate kinds, statuses, temporal anchor kinds, candidate limit, and fingerprint. Runtime comparison is exact and fails closed on missing, reordered, obsolete, unexpected, or fingerprint-mismatched metadata.

## 15. V3 output schema

The canonical builder emits `contractVersion`, input, `observationSourceId`, speaker/observer refs, mentions, referent candidates, and claims. Claims carry the frozen linguistic evidence and status fields. A recursive ownership check rejects World Truth, Authority, Memory Admission, persistent consent/goal, relationship, affective, or behavior fields.

## 16. Architecture ownership audit

V3 produces linguistic evidence only. It performs schema validation, pointer validation, candidate masking, confidence propagation, and abstention. It does not decide truth, authority, admission, persistence, relationship, affect, consent state, goal state, or behavior.

## 17. Synthetic IT/EN/ES tests

The synthetic inventory includes equivalent Italian, English, and Spanish contract examples plus code-switch. Slice scoring treats language as metadata and uses one label contract for all languages. These are representability/structure tests, not NLU accuracy or learned-quality measurements.

## 18. Adult/intimacy synthetic stress tests

Adult-only synthetic cases cover desire, consent, refusal, withdrawal, third-party report, negation, time, role identity, and IT/EN/ES/code-switch. They use ordinary V3 labels and evaluator slices. No moderation, censorship, blocking, or confidence penalty is introduced.

## 19. Multi-claim tests

The inventory includes conjunction, report+belief, and past/current contrasts. The decoder regression produces two ordered flat claims for “I lived in Venice, now I live in Milan,” preserving distinct spans, entity mentions, predicates, and temporal relations. No recursive/nested claim behavior is fabricated.

## 20. Migration tooling status

`migrate_contract_v3.py` accepts only caller-supplied rows and classifies rows/fields as `DIRECT_REUSE`, `DETERMINISTIC_MIGRATION`, `NEEDS_REANNOTATION`, or `UNUSABLE`. It never performs file discovery or partition I/O and does not invent cue spans, role/source pointers, or temporal anchors. `training_data_v3.py` builds targets only from already-V3 caller-supplied rows. No canonical migration/reannotation was run; that is TASK 2.3.

## 21. ONNX structural probe

The export contract uses opset 17, dynamic batch/sequence/candidate/anchor axes, six inputs, and 17 output tensors representing 16 heads. Pointer dimensions are bounded at runtime; custom operators expected: none. Actual export/load was `NOT_EXECUTED` because `torch`, `transformers`, `onnx`, and `onnxruntime` are unavailable. This is explicitly a tooling risk, not a fabricated PASS and not quality evidence.

## 22. Parameter/runtime delta

At hidden size 384:

| Component | Parameters |
|---|---:|
| Token classifiers | 7,700 |
| Fixed sequence classifiers | 13,860 |
| Shared pointer projection | 147,456 |
| Five role queries | 1,920 |
| `NONE`/`UNKNOWN` embeddings | 768 |
| Temporal anchor query | 384 |
| **Total V3 heads** | **172,088** |

Estimated head bytes are 688,352 in FP32. A theoretical fully eligible INT8 weight estimate is 172,088 bytes, but no quantization was performed and embeddings/queries may remain FP32 in a real deployment. Expected ONNX operations are bounded standard tensor operations (`Gather`, `MatMul`, `Add`, `Concat`, masking/`Where`, and softmax-class operations).

## 23. IB-01 through IB-09 disposition

| ID | Disposition | Evidence |
|---|---|---|
| IB-01 | CLOSED | BERT `encoder.layer`/`hidden_size` adapter and regression; physical package-bound load remains an environment verification risk. |
| IB-02 | CLOSED | Independent candidate pointers; no V3 category binder, recent-entity, capitalization, or subject-reuse fallback. |
| IB-03 | CLOSED | Required-field confidence bound and configurable critical-field abstention. |
| IB-04 | CLOSED | Independent gold normalizer/evaluator with no production validator import. |
| IB-05 | OBSOLETE_BY_V3 | Identity is explicit in five pointer targets; missing proof is reannotation, not silent discard. |
| IB-06 | CLOSED | Exact metadata/fingerprint runtime guard fails closed. |
| IB-07 | CLOSED | All five pointer roles scored by candidate identity. |
| IB-08 | OBSOLETE_BY_V3 | Speaker is `ctx:speaker`; forbidden sentinels rejected. |
| IB-09 | CLOSED | Canonical `CORRECT`; stale evaluator alias removed. |

## 24. Remaining risks and test gate

```text
P0 implementation remaining = 0
P1 remaining = 2
  P1-ENV-PHYSICAL-BERT-LOAD
  P1-ENV-ONNX-EXPORT-LOAD
P2 remaining = 0
safe synthetic/data-independent tests = 43/43 PASS
Python compile = PASS
```

The two P1 items require only an environment containing the pinned ML/export toolchain. They do not change the frozen contract. Tests that could implicitly read canonical DEV/Frozen were not run.

Guard evidence from the start-to-implementation comparison shows only the listed V3 code/tests, one `CORRECT` alias repair, continuity, and this report. Therefore:

```text
Student-4 changed = false
canonical DEV used = false
Frozen read = false
Path A modified = false
pristine 40k modified = false
Path B started = false
optimizer created = false
backprop executed = false
Teaching executed = false
Training executed = false
Other repositories modified = false
```

## 25. Exact next task

```text
TASK 2.3 = NOT_STARTED
TASK 3 = NOT_STARTED
NEXT = AWAIT OWNER REVIEW BEFORE TASK 2.3
```

No dataset migration, reannotation, training, or automatic continuation was started.
