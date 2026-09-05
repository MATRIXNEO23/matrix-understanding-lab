# Student-5 Matrix-NLU Contract Repair Design

## 1. Executive verdict

```text
TASK 2.1 = CONTRACT_V3_FROZEN
contract = MATRIX_NLU_CONTRACT_V3
currentHeadCount = 15
proposedHeadCount = 16
headCountChangeRequired = true
implementationExecuted = false
trainingExecuted = false
```

The architecture can be frozen without further owner choice. The minimum correct repair keeps the six token responsibilities, changes four existing referent classifiers into concrete candidate-pointer heads, adds one dedicated `sourceReferent` pointer, separates dialogue act from epistemic/evidential kind, makes negation cue evidence independent from polarity, expands temporal relations, and makes uncertainty fail closed.

The sixteenth head is not cosmetic. `source` and `perspective` can differ, and no existing head can own source identity without semantic overloading. A hidden second output inside `perspectiveReferent` would only disguise the same head-count change.

This task changed documentation only. It did not implement V3, migrate data, train, read DEV/Frozen, modify Student-4, or modify Path A.

## 2. Baseline TASK 2 findings

TASK 2 found 15 registered heads but blocked the contract on seven drifts:

| ID | Finding | V3 disposition |
|---|---|---|
| `CD-01-NEGATION-POLARITY` | full-source negation is derived from polarity | cue evidence and polarity are independent |
| `CD-02-ACT-KIND-HYPOTHESIS` | hypothesis duplicated across two heads | hypothesis exists only in `claimKind` |
| `CD-03-REPORT-BELIEF-COMMAND` | generic distinctions absent | COMMAND in act; REPORT/BELIEF in kind |
| `CD-04-REFERENT-ROLE-LINK` | provenance class is not concrete identity | candidate pointer heads + new source pointer |
| `CD-05-TEMPORAL-RELATIONS` | BEFORE/AFTER/DURING absent | expanded relation registry + anchor reference |
| `CD-06-CONFIDENCE-ABSTENTION` | critical token confidence is diagnostic only | field status + conservative gate |
| `CD-07-CLAIMKIND-UNKNOWN` | missing kind is forced | explicit UNKNOWN and ambiguity/abstention |

All seven design drifts are closed in V3. The nine implementation bugs remain mapped for TASK 2.2; none was edited here.

## 3. Design principles

1. Model linguistic evidence, not downstream state.
2. Give every identity-bearing role a concrete mention/context candidate.
3. Keep syntactic/surface evidence distinct from composed semantics.
4. Use explicit NONE, UNKNOWN, AMBIGUOUS, and abstention semantics.
5. Prefer bounded tensor operations and deterministic decoding for Android/ONNX.
6. Version all label orders and migration rules; never reinterpret V2 silently.
7. Treat adult/intimacy as ordinary semantics and a stress test, never moderation.
8. Use identical contract semantics for IT, EN, ES, and code-switch input.

## 4. Current 15-head contract

V2 has six BIO token heads and nine fixed-label sequence classifiers. Its concrete registry remains documented in `reports/STUDENT_5_15_HEAD_CONTRACT_AUDIT.md`; V3 does not modify `matrix_nlu/labels.py` in this task.

The current fixed referent labels (`KNOWN_ENTITY`, `RECENT_ENTITY`) encode provenance, not which entity occupies a role. The current decoder then reuses `subject_mention` for target/owner/perspective binding. That is the central data-to-identity failure V3 removes.

## 5. Proposed versioned contract

The complete normative contract is `docs/MATRIX_NLU_CONTRACT_V3.md`.

| Layer | V3 output |
|---|---|
| observation | input identity, speaker/observer context, mention table, candidate table |
| claim boundary | flat atomic source spans and stable claim IDs |
| surface evidence | subject/object/negation cue/temporal/entity spans |
| conversational | dialogue act |
| proposition | predicate, composed polarity, temporal relation/anchor |
| attribution | claim kind, subject/target/owner/perspective/source pointers |
| confidence | per-field confidence/status, structural status, interpretation status |

Forbidden in this output: authority, truth, Memory Admission, persistent consent/goal state, RelationshipState, AffectiveState, or behavior decision.

## 6. Head-count decision

```text
token heads = 6
sequence heads = 10
total heads = 16
HEAD_COUNT_CHANGE_REQUIRED = true
```

The only added semantic head is `sourceReferent`. The four existing role heads remain, but their output type changes from provenance categories to pointers over a shared candidate table.

Why 15 cannot remain honest:

- `claimKind=REPORT` says that attribution exists but not who said it;
- `perspective` is viewpoint, while `source` is linguistic attributor;
- entity BIO says which spans are people/places but not which person is source;
- decoder heuristics cannot supply missing learned responsibility without guessing.

## 7. Token-head responsibilities

| Head | Frozen responsibility | Important V3 rule |
|---|---|---|
| `boundary` | flat atomic claim spans | preserve every group; no first-span truncation |
| `object` | surface value/object | never target identity |
| `subject` | explicit subject mention | implicit subject may have no span but must have pointer |
| `negation` | overt cue spans | never whole source; independent of polarity |
| `temporal` | explicit temporal evidence | preserve all spans |
| `entity` | mention span + PERSON/LOCATION type | role comes from pointer heads, not entity type |

The V3 token registry changes `B/I-NEGATION` to `B/I-NEGATION_CUE` to make the semantic break visible.

## 8. Sequence-head responsibilities

| Head | Frozen responsibility | Output form |
|---|---|---|
| `dialogueAct` | conversational action | six labels |
| `predicate` | Matrix domain proposition | retained 12 labels |
| `subjectReferent` | concrete subject identity | candidate pointer |
| `targetReferent` | concrete directed target | candidate pointer |
| `ownerReferent` | whose state/property/goal/consent | candidate pointer |
| `perspectiveReferent` | viewpoint holder | candidate pointer |
| `sourceReferent` | linguistic attributor | candidate pointer |
| `polarity` | composed proposition polarity | three labels |
| `temporalRelation` | time relation and anchor | ten labels + pointer |
| `claimKind` | evidential/epistemic presentation | five labels |

## 9. DialogueAct vs ClaimKind

Frozen registries:

```text
dialogueAct = ASSERT, QUESTION, REQUEST, COMMAND, CORRECT, UNKNOWN
claimKind   = DIRECT, REPORT, BELIEF, HYPOTHESIS, UNKNOWN
```

The heads are orthogonal. An assertion may be DIRECT, REPORT, BELIEF, or HYPOTHESIS. A question can ask about a reported or hypothetical proposition. `CORRECT` denotes linguistic correction only and cannot supersede memory.

| Example | dialogueAct | claimKind |
|---|---|---|
| Bob lives in Rome. | ASSERT | DIRECT |
| Does Bob live in Rome? | QUESTION | DIRECT |
| Please tell Bob to leave. | REQUEST | DIRECT |
| Bob, leave now. | COMMAND | DIRECT |
| Alice says Bob lives in Rome. | ASSERT | REPORT |
| I think Bob is angry. | ASSERT | BELIEF |
| Maybe Bob is angry. | ASSERT | HYPOTHESIS |
| No, Bob lives in Milan. | CORRECT | DIRECT |

## 10. Report / belief / command semantics

- REPORT requires an attributable `sourceReferent`; if source is unresolved, the claim cannot be RESOLVED.
- BELIEF identifies linguistic framing, not accepted belief or truth. Its perspective holder and source are separately represented.
- COMMAND is conversational force and does not create a persistent GoalState or authorize behavior.
- `presence.reported` remains only a domain predicate for presence evidence; it cannot encode REPORT.

## 11. Negation vs polarity

V3 chooses cue-only token evidence. Scope graphs were considered but rejected for this initial mobile contract because they require cue-scope pairing, overlapping structures, and substantially more annotation. Atomic claim boundaries are the scope unit. Hard cases abstain.

| Phenomenon | Negation evidence | Polarity |
|---|---|---|
| positive assertion | none | POSITIVE |
| simple negative | cue(s) | NEGATIVE |
| double negation | two cue groups | composed result, possibly POSITIVE |
| negative concord | all overt cue groups | one composed result |
| metalinguistic negation | cue preserved | composed result or UNKNOWN |

No deterministic implication is permitted in either direction between cue presence and polarity.

## 12. Temporal model

V3 separates explicit spans from semantic relation. The sequence registry is:

```text
ATEMPORAL, CURRENT, PAST, FUTURE, BEFORE, AFTER,
DURING, RECURRENT, AT_REFERENCE, UNKNOWN
```

BEFORE/AFTER/DURING/AT_REFERENCE require an anchor pointer to speech time, context reference time, a temporal evidence ID, or a claim ID. `INTERVAL` is retained as expression shape/evidence rather than incorrectly added as a relation label.

## 13. Entity / role-link architecture

The selected design is an observation-level candidate table plus five masked pointer heads. Candidates include speaker, observer, detected mentions, and explicitly supplied stable context entities. Mention IDs are deterministic. Exact context binding may add an EntityRef; uncertain identity remains unresolved.

| Problem | Option | Heads affected | Dataset / decoder impact | Runtime impact | Pros | Cons | Verdict |
|---|---|---|---|---|---|---|---|
| role linking | A: add token BIO role heads | +5 token heads | many overlapping BIO targets | several token classifiers | direct spans | overlap conflicts; head bloat | REJECT |
| role linking | B: entity mentions + role pointers | 4 changed + source added | candidate IDs and pointer targets | bounded MatMul/softmax | compact, multi-entity, deterministic | needs candidate builder/masks | **ADOPT** |
| role linking | C: free start/end pointers per role | 5 pointer heads | span pair targets | two distributions/role | no entity dependency | can point to invalid/non-entity spans | REFERENCE_ONLY |
| role linking | D: deterministic regex/first-recent | none | decoder heuristic | tiny | easy | language-specific guessing and proven corruption | NOT_SUITABLE |

The selected approach adapts span/candidate scoring ideas while keeping a single encoder pass and bounded tensors.

## 14. Source / perspective separation

| Option | Representation | Semantic correctness | Cost | Verdict |
|---|---|---|---|---|
| source equals perspective | one existing pointer | fails when attribution and viewpoint differ | none | REJECT |
| source hidden in claimKind | REPORT label plus heuristic | cannot identify person | none | REJECT |
| one multi-slot perspective head | two outputs under one name | semantically opaque; hides added classifier | same as added head | REJECT |
| dedicated `sourceReferent` | independent pointer over same candidates | complete and auditable | one role query/head | **ADOPT** |

`Marco told me that Anna loves Luca` therefore supports speaker=current speaker, source=Marco, subject/owner=Anna, target=Luca, perspective=Marco without defaults.

## 15. Confidence / abstention

V3 freezes semantics, not numerical thresholds:

- every field has confidence and `RESOLVED/UNKNOWN/AMBIGUOUS/NOT_APPLICABLE`;
- every claim has `VALID/INVALID` structure and `RESOLVED/AMBIGUOUS/ABSTAINED` interpretation;
- overall confidence cannot exceed the least-confident required critical field;
- threshold values belong to versioned evaluation/runtime configuration and must be calibrated in a later authorized task;
- critical token uncertainty can force abstention;
- invalid pointers, missing temporal anchors, and registry mismatch fail closed.

## 16. Unknown / ambiguity semantics

`NONE` means known absence/non-applicability. `UNKNOWN` means insufficient evidence. `AMBIGUOUS` means two or more materially plausible alternatives; the primary role value is UNKNOWN and ranked alternatives remain diagnostics. Missing annotation is a dataset error, never a model label. `speech.unresolved` is a predicate fallback and does not replace field-level UNKNOWN.

## 17. Multi-claim behavior

V3 supports multiple flat, non-overlapping atomic claims in one observation and a shared mention table for cross-claim reference. Each claim has its own act, kind, roles, polarity, and time. This handles:

- `I live in Rome and I love coffee.` as two claims;
- `Alice said Bob left, but I think he will return.` as REPORT plus BELIEF with shared Bob mention/context identity;
- `I used to live in Venice, now I live in Milan.` as PAST plus CURRENT;
- `Anna said she wanted Luca yesterday, but today she doesn't.` as separate attributed/time/polarity claims.

Recursive nested claim graphs are intentionally unsupported in V3. If flat atomic representation would lose source or proposition identity, the affected field/claim abstains. This is a documented P1 limitation, not permission to guess.

## 18. Adult/intimacy stress test

The V3 structure distinguishes interest/desire (`preference.like` or `goal.object` according to utterance), request (dialogue act), consent/refusal (predicates), withdrawal (new claim/correction plus temporal and polarity evidence), source, owner, perspective, and target.

Examples such as `Anna said she doesn't want Luca`, `I agreed yesterday, but not now`, and their adult-only explicit/slang/code-switch equivalents use ordinary heads and pointers. No moderation class, confidence penalty, block, or semantic downgrade is introduced. Unfamiliar wording degrades to `speech.unresolved`, not a hard error.

## 19. IT / EN / ES stress test

All closed labels are language-neutral and all role values are stable IDs rather than surface forms. BIO offsets and pointer candidates preserve language-specific evidence without English syntax rules. Negative concord in Italian/Spanish is represented as multiple cues with one composed polarity. Code-switch terms do not change label meaning.

No quality benchmark was performed; representability alone was audited, as required.

## 20. Dataset migration design

| Field | Type | Required | Unknown | Scope | V2 migration |
|---|---|---:|---|---|---|
| `contractVersion` | string | yes | none | row | new constant |
| `mentions[]` | typed spans + ID | yes | empty array | observation | conditional from entity spans |
| `claimId` | string | yes | none | claim | deterministic |
| plural evidence spans | arrays | yes | empty array | claim | conditional |
| negation cue spans | span array | yes | empty array | claim | needs reannotation for v2 negatives |
| five role pointers | candidate IDs/special | yes | UNKNOWN | claim | four mostly reannotation; source new |
| temporal relation | label + anchor | yes | UNKNOWN | claim | old coarse labels reusable |
| field statuses | enum | yes | UNKNOWN | field | deterministic only with complete V3 target |

TRAIN rows are classified as DIRECT_REUSE, DETERMINISTIC_MIGRATION, NEEDS_REANNOTATION, or UNUSABLE. The migration tool must be fail-closed and produce provenance counts. No dataset was opened or modified in TASK 2.1; DEV/Frozen migration is not authorized.

## 21. Decoder contract

The future decoder must validate contract and label order, preserve all spans, build one deterministic candidate table, decode roles independently, preserve source/perspective, require temporal anchors, compute field-aware confidence, and abstain on structural/critical uncertainty. It must never infer identity from first-recent or another role's mention, and must never emit downstream truth/admission/state decisions.

## 22. Evaluator independence requirements

Gold normalization and prediction decoding must be separate implementations. The evaluator must score exact claim sets, all span groups, each categorical label, pointer identity, source/perspective distinction, relation anchors, field statuses, abstention, ownership/source corruptions, and independent IT/EN/ES plus adult/intimacy slices. It must not use the production validator as its gold oracle.

## 23. Implementation bug mapping

| ID | Valid after V3? | Type | Before TASK 3? | Disposition |
|---|---|---|---:|---|
| `IB-01-STUDENT5-BERT-ADAPTER` | yes | implementation-only | yes | implement architecture-neutral BERT adapter |
| `IB-02-MULTI-KNOWN-BIND` | mechanism obsolete, regression remains | implementation/decoder | yes | remove category binder; test distinct role pointers |
| `IB-03-TOKEN-CONFIDENCE-NOT-GATING` | yes | implementation-only | yes | implement V3 field/claim gating |
| `IB-04-EVALUATOR-SHARED-ORACLE` | yes | evaluator architecture | yes | independent gold path |
| `IB-05-ENTITY-REFERENT-DROPPED` | old field obsolete | migration/training target | yes | role targets move to pointer fields; reject silent drop |
| `IB-06-BUNDLE-LABEL-ORDER-UNVALIDATED` | yes | implementation-only | yes | require contract/registry fingerprint |
| `IB-07-ENTITY-REFERENT-NOT-SCORED` | superseded | evaluator | yes | score all five pointers by candidate identity |
| `IB-08-SELF-SENTINEL` | obsolete | migration/decoder | yes | remove literal SELF; map only with evidence |
| `IB-09-CORRECTION-ALIAS` | yes | implementation cleanup | no, but TASK 2.2 preferred | canonical label remains CORRECT |

`IMPLEMENTATION_BUGS_MAPPED = 9/9`.

## 24. Runtime / parameter impact

The design adds one semantic head and replaces fixed referent classifications with five bounded pointer scorers over shared candidate embeddings. With hidden size 384, role-query vectors are only about 1,920 learned values plus biases; even if TASK 2.2 uses one shared 384x384 candidate projection, added storage remains under about 0.6 MB FP32 and far less when quantized. Exact counts belong to implementation verification.

Candidate scoring can use standard Gather/MatMul/Add/Mask/Softmax operations. A versioned maximum candidate count avoids ragged mobile graphs. No runtime dependency is introduced by this design. Annotation and evaluator cost, not parameter size, are the principal tradeoff.

## 25. Alternative designs rejected

| Problem | Option | Heads affected | Dataset impact | Decoder impact | Params/runtime | Pros | Cons | Verdict |
|---|---|---|---|---|---|---|---|---|
| negation | full-source span from polarity | unchanged | none | trivial | none | compatible with V2 | duplicates polarity, loses cues | REJECT |
| negation | cue + full scope graph | structured token/pair outputs | high reannotation | graph pairing | moderate | richest semantics | unnecessary V3 burden | REFERENCE_ONLY |
| negation | cue-only + composed polarity | existing token + sequence | focused reannotation | simple groups | negligible | compact, independent | difficult scope abstains | **ADOPT** |
| act/kind | one combined cross-product head | one large head | cross-product labels | simple | more logits/data sparsity | single decision | conflates independent axes | REJECT |
| act/kind | orthogonal registries | same two heads | targeted migration | simple | negligible | compositional and clear | breaking label order | **ADOPT** |
| report source | derive from perspective | none | easy | heuristic | none | minimal | semantically false cases | REJECT |
| report source | dedicated pointer | +1 sequence | source annotation | same pointer decoder | tiny | exact/auditable | one extra target | **ADOPT** |

## 26. V2 to proposed contract migration table

| V2 | V3 | Class |
|---|---|---|
| unaffected BIO labels | same responsibility | CONDITIONAL |
| full-source negative span | negation cue spans | NO_MAPPING |
| act HYPOTHESIS | act ASSERT + kind HYPOTHESIS | CONDITIONAL |
| kind EXPLICIT | DIRECT/REPORT/BELIEF/UNKNOWN | LOSSY |
| SPEAKER/OBSERVER role classes | context candidate IDs | LOSSLESS |
| KNOWN/RECENT role classes | concrete candidate ID | NO_MAPPING |
| SELF/SUBJECT sentinels | concrete candidate ID | CONDITIONAL |
| no source | source pointer | NO_MAPPING |
| old temporal labels | same labels | LOSSLESS |
| relative temporal meaning | expanded label + anchor | NO_MAPPING |
| no status/abstention | V3 field/claim status | CONDITIONAL |

Overall: `V2 MIGRATION = PARTIAL / BREAKING`.

## 27. P0 / P1 / P2 remaining

Contract-design blockers after freeze:

```text
P0 contract = 0
P1 contract = 2
  - flat-only nested-claim limitation
  - intentionally narrow predicate ontology
P2 contract = 0
```

Known implementation work still blocking TASK 3:

```text
P0 implementation = 4 (IB-01, IB-02, IB-03, IB-04)
P1 implementation = 2 (IB-06, IB-07; IB-05/IB-08 are superseded but need migration tests)
P2 implementation = 1 (IB-09)
```

These do not prevent freezing the semantic contract; they prevent training until TASK 2.2 implements and regresses it.

## 28. Frozen contract decision

All required architectural choices are closed:

```text
HEAD COUNT = 16
ROLE LINK = bounded candidate pointers
SOURCE = dedicated pointer
NEGATION = cue evidence
POLARITY = independent composed label
TEMPORAL = expanded relation + anchor
DIALOGUE ACT = conversational action
CLAIM KIND = evidential/epistemic kind
CONFIDENCE = field-aware fail-closed
UNKNOWN/AMBIGUITY = explicit and distinct
OUTPUT/DATASET/DECODER/EVALUATOR = versioned normative contracts
```

Verdict: **`CONTRACT_V3_FROZEN`**.

## 29. Exact next implementation task

No implementation is authorized now. After owner review, TASK 2.2 should implement `MATRIX_NLU_CONTRACT_V3`, its schemas, candidate pointers, decoder/validator, independent evaluator, versioned registry checks, and safe TRAIN migration tooling. It must not train or read DEV/Frozen unless separately authorized.

```text
TASK 2.2 = NOT_STARTED
TASK 3 = NOT_STARTED
NEXT = AWAIT OWNER REVIEW BEFORE TASK 2.2
```

## Technical references and reuse classification

| Source | Relevant idea | Classification |
|---|---|---|
| [Pointer Networks, NeurIPS 2015](https://proceedings.neurips.cc/paper/2015/hash/29921001f2f04bd3baee84a12e98098f-Abstract.html) | output positions over variable input candidates | ADAPT |
| [End-to-end Neural Coreference Resolution, EMNLP 2017](https://aclanthology.org/D17-1018/) | span candidates and antecedent scoring | ADAPT |
| [DyGIE++, EMNLP-IJCNLP 2019](https://aclanthology.org/D19-1585/) | contextual span representations across entities/relations/events | REFERENCE_ONLY |
| [PURE, NAACL 2021](https://aclanthology.org/2021.naacl-main.5/) | explicit entity spans feeding relation decisions | ADAPT |
| [TimeML, AAAI 2003](https://aaai.org/papers/0005-ss03-07-005-timeml-robust-specification-of-event-and-temporal-expressions-in-text/) | separate temporal expressions from temporal links | ADAPT |
| [*SEM 2012 Negation Shared Task](https://aclanthology.org/S12-1035/) | cue and scope are distinct negation structures | REFERENCE_ONLY; V3 adopts cue only |

No external system or dependency is copied. These sources support the choice to separate mentions from role/link decisions, temporal evidence from relations, and negation cues from composed meaning.

## Guard evidence

```text
Student-4 changed = false
canonical DEV used = false
Frozen read = false
Path A modified = false
Path B started = false
Teaching executed = false
Training executed = false
Other repositories modified = false
```

Only the TASK 2.1 documentation files and Student-5 continuity are within scope.
