# Student-5 — audit del contratto Matrix-NLU a 15 head

Date: `2026-09-05`  
Repository: `MATRIXNEO23/matrix-understanding-lab`  
Branch: `main`  
Task: `TASK_2_15_HEAD_CONTRACT_AUDIT`  
Code/document baseline: `8a9a375c4bbd5b9d03f6f68f036059a3df414881`  
Verdict: `ARCHITECTURAL_CONTRACT_CHANGE_REQUIRED`

## 1. Executive verdict

The repository contains exactly the expected six token heads and nine sequence heads. Their Python registry is deterministic, all label lists are unique, model outputs and ONNX output names use registry insertion order, and the ordinary two-pass boundary/claim data flow is internally recognizable.

The semantic contract is nevertheless not sufficient to authorize TASK 3. Four architecture-level blockers require a head/label/schema semantic decision that TASK 2 is forbidden to make:

1. `token.negation` is not independent of `sequence.polarity` in the canonical v2 target contract. Every negative claim is forced to use the complete source as its negation span and every non-negative claim is forced to have no negation span. This duplicates the polarity decision and cannot represent a surface negation whose composed semantic polarity differs, such as “It is not true that I hate coffee.”
2. `HYPOTHESIS` is encoded simultaneously as a `dialogueAct` and a `claimKind`. At the same time the registry has no generic `REPORT`, `BELIEF`, or `COMMAND` state. The canonical requirement to distinguish dialogue function from epistemic/claim kind is therefore both duplicated and incomplete.
3. Categorical `KNOWN_ENTITY`/`RECENT_ENTITY` values do not identify which mention is the target, owner, perspective or reported source when multiple entities occur. The dataset carries per-entity `referent` annotations, but the entity training target discards them and learns only PERSON/LOCATION. There is no target/owner/perspective/source span or link output that can disambiguate the roles.
4. `temporalRelation` contains only `ATEMPORAL/CURRENT/PAST/FUTURE/UNKNOWN`; the required relative relations `before/after/during` cannot be represented without changing label semantics or the label set.

These are contract issues, not evidence that Student-5 cannot learn. No head, label, dataset, decoder, model or test was changed. Path B and TASK 3 remain not started.

## 2. Sources inspected

The following canonical sources were read completely before the code audit:

1. `PROJECT_WORK_RULES.md`
2. `ARCHITETTURA.md`
3. `docs/FINAL_MATRIX_UNDERSTANDING_ARCHITECTURE.md`
4. `docs/STUDENT_5_WORK_DISPATCH_POLICY.md`
5. `docs/WORK_CONTINUITY_STUDENT_5.md`
6. `docs/STUDENT_ARTIFACT_REGISTRY.md`
7. `docs/ADULT_INTIMACY_NLU_COVERAGE.md`
8. `reports/STUDENT_5_MINILM_40K_QUALITY_ANALYSIS.md`
9. `reports/STUDENT_5_MINILM_DEEP_PRUNING.md`
10. `reports/STUDENT_5_40K_UNTAUGHT_INT8_RUNTIME_PROBE.md`

Contract and implementation sources inspected:

- `matrix_nlu/labels.py`
- `matrix_nlu/model.py`
- `matrix_nlu/training_data.py`
- `matrix_nlu/train.py`
- `matrix_nlu/inference.py`
- `matrix_nlu/evaluate_e2e.py`
- `matrix_nlu/export_onnx.py`
- `matrix_nlu/audit_dataset_contract.py`
- `matrix_nlu/audit_dataset_v2.py`
- `matrix_nlu/build_dataset.py`
- `matrix_nlu/build_dataset_v2.py`
- `matrix_nlu/v2_train_generalization.py`
- the pertinent `matrix_nlu/test_*.py` contract/inference/evaluator/export tests
- `docs/DECISION_REQUIRED_MATRIX_NLU_ANNOTATION_CONTRACT.md`
- `docs/MATRIX_NLU_DATASET_CARD.md`
- `docs/MATRIX_NLU_DATASET_V2.md`
- `docs/MATRIX_NLU_MODEL_DATA_PLAN.md`
- `docs/MATRIX_NLU_TRAINING_PLAN.md`

No JSONL dataset partition was opened. Canonical DEV and Frozen were not read, decoded, generated, evaluated or used. Builders/auditors were inspected as source code only; tests that reconstruct or load DEV/test partitions were deliberately not executed.

## 3. Exact 15-head registry

Source of truth: `matrix_nlu/labels.py`.

| Level | Head | Exact labels in index order | Count | Registry status |
|---|---|---|---:|---|
| TOKEN | `boundary` | `O, B-CLAIM, I-CLAIM` | 3 | PRESENT |
| TOKEN | `object` | `O, B-OBJECT, I-OBJECT` | 3 | PRESENT |
| TOKEN | `subject` | `O, B-SUBJECT, I-SUBJECT` | 3 | PRESENT |
| TOKEN | `negation` | `O, B-NEGATION, I-NEGATION` | 3 | PRESENT / SEMANTIC BLOCKER |
| TOKEN | `temporal` | `O, B-TEMPORAL, I-TEMPORAL` | 3 | PRESENT |
| TOKEN | `entity` | `O, B-PERSON, I-PERSON, B-LOCATION, I-LOCATION` | 5 | PRESENT / ROLE-LINK BLOCKER |
| SEQUENCE | `dialogueAct` | `ASSERT, CORRECT, QUESTION, REQUEST, HYPOTHESIS, UNKNOWN` | 6 | PRESENT / SEMANTIC BLOCKER |
| SEQUENCE | `predicate` | `identity.name, identity.age, residence.place, presence.reported, preference.like, work.role, possession.has, goal.object, attribute.is, consent.grant, consent.refuse, speech.unresolved` | 12 | PRESENT / LIMITED |
| SEQUENCE | `subjectReferent` | `SPEAKER, OBSERVER, KNOWN_ENTITY, RECENT_ENTITY, UNKNOWN` | 5 | PRESENT |
| SEQUENCE | `targetReferent` | `NONE, SELF, SPEAKER, OBSERVER, KNOWN_ENTITY, RECENT_ENTITY, UNKNOWN` | 7 | PRESENT / ROLE-LINK BLOCKER |
| SEQUENCE | `ownerReferent` | `SUBJECT, SPEAKER, OBSERVER, KNOWN_ENTITY, RECENT_ENTITY, UNKNOWN` | 6 | PRESENT / ROLE-LINK BLOCKER |
| SEQUENCE | `perspectiveReferent` | `SPEAKER, SUBJECT, OBSERVER, KNOWN_ENTITY, RECENT_ENTITY, UNKNOWN` | 6 | PRESENT / ROLE-LINK BLOCKER |
| SEQUENCE | `polarity` | `POSITIVE, NEGATIVE, UNKNOWN` | 3 | PRESENT / SEMANTIC BLOCKER |
| SEQUENCE | `temporalRelation` | `ATEMPORAL, CURRENT, PAST, FUTURE, UNKNOWN` | 5 | PRESENT / COVERAGE BLOCKER |
| SEQUENCE | `claimKind` | `EXPLICIT, HYPOTHESIS` | 2 | PRESENT / SEMANTIC BLOCKER |

Registry structure checks:

```text
totalHeads = 15
tokenHeads = 6
sequenceHeads = 9
duplicateHeadNames = 0
duplicateLabelsWithinHead = 0
registryStructure = PASS
registrySemanticSufficiency = BLOCKED
```

## 4. Head-by-head audit

### 4.1 `token.boundary`

- **Level:** TOKEN.
- **Semantic responsibility:** proposition-local claim spans in the full observation.
- **Input target source:** every claim `spans.source` in a JSONL row.
- **Output type / labels:** per-token BIO logits; 3 labels.
- **Null/unknown:** `O`; no explicit UNKNOWN. No predicted span yields no claim.
- **Relationships:** owns decomposition only; distinct from entity and from claim-local semantic heads.
- **Dependencies/ambiguity:** tokenizer offset mapping and non-overlapping BIO groups; conjunction punctuation is not interpreted deterministically.
- **Dataset encoding:** a dedicated boundary example per observation; every other token head and sequence head is `IGNORE=-100`.
- **Decoder:** `groups_from_tags` reconstructs all B/I groups and each group is re-encoded as a claim.
- **Runtime consumer:** `MatrixNluRuntime.interpret`.
- **Tests:** two-claim group reconstruction is covered; empty/overlap/confidence behavior lacks full tests.
- **Adult/intimacy and IT/EN/ES:** language-independent BIO; applies normally to adult claims.
- **Verdict:** `PASS_WITH_RISK`.

### 4.2 `token.object`

- **Level:** TOKEN.
- **Semantic responsibility:** claim value/object surface span, not target identity.
- **Input target source:** `claim.spans.object`, localized to the claim crop.
- **Output type / labels:** one BIO object span; 3 labels.
- **Null/unknown:** all `O` means null; no explicit unknown span.
- **Relationships:** distinct from `targetReferent`; may overlap entity/temporal spans.
- **Dependencies/ambiguity:** schema permits one scalar span; decoder silently keeps only the first predicted group.
- **Dataset encoding:** token BIO on claim examples only.
- **Decoder:** `scalar_span`, then globalized to observation offsets.
- **Runtime consumer:** Typed Claim `objectSpan`.
- **Tests:** generic BIO alignment is covered; multiple object groups are not.
- **Adult/intimacy and IT/EN/ES:** ordinary semantic value span; no domain-specific behavior.
- **Verdict:** `PASS_WITH_RISK`.

### 4.3 `token.subject`

- **Level:** TOKEN.
- **Semantic responsibility:** explicit subject mention span.
- **Input target source:** `claim.spans.subject`; canonical implicit speaker uses null.
- **Output type / labels:** one BIO subject span; 3 labels.
- **Null/unknown:** all `O` for implicit/no explicit surface; identity is carried by `subjectReferent`.
- **Relationships:** subject surface is not subject identity; distinct from `subjectReferent`.
- **Dependencies/ambiguity:** explicit mention is also commonly a PERSON entity span.
- **Dataset encoding:** claim-local BIO; v2 audits implicit `SPEAKER` subject as null.
- **Decoder:** first span only; surface text is used to bind `KNOWN_ENTITY`.
- **Runtime consumer:** top-level subject binding and entity-role attachment.
- **Tests:** known/unknown subject binding and implicit speaker behavior are partially covered.
- **Adult/intimacy and IT/EN/ES:** needed for third-party adult statements; language-independent labels.
- **Verdict:** `PASS_WITH_RISK`.

### 4.4 `token.negation`

- **Level:** TOKEN.
- **Semantic responsibility expected by TASK 2:** surface negation token/scope evidence independent from composed polarity.
- **Input target source:** v2 `claim.spans.negation`.
- **Output type / labels:** BIO span; 3 labels.
- **Null/unknown:** all `O` means no negation evidence.
- **Relationships:** must be distinct from `sequence.polarity`.
- **Known dependency:** canonical v2 audit enforces `negation = source` exactly when polarity is NEGATIVE and `null` otherwise.
- **Ambiguity/blocker:** the enforced one-to-one relation duplicates polarity and cannot encode nested/scope-changing negation such as “not true that I hate”.
- **Dataset encoding:** full claim source for every negative claim, never a cue-only or nested scope.
- **Decoder:** reconstructs first BIO group as `negationSpan`.
- **Runtime consumer:** Typed Claim diagnostic span; token confidence does not participate in claim admission.
- **Tests:** v2 tests confirm the coupling rather than the required separation.
- **Adult/intimacy and IT/EN/ES:** critical for refusal/withdrawal; the blocker is language-independent.
- **Verdict:** `ARCHITECTURAL_PROBLEM`.

### 4.5 `token.temporal`

- **Level:** TOKEN.
- **Semantic responsibility:** explicit temporal expression span.
- **Input target source:** `claim.spans.temporal`; implicit tense may remain null.
- **Output type / labels:** one BIO temporal span; 3 labels.
- **Null/unknown:** all `O` for absent/implicit expression.
- **Relationships:** distinct from `temporalRelation`.
- **Dependencies/ambiguity:** canonical v2 annotation policy records EXPLICIT/IMPLICIT/NONE.
- **Dataset encoding:** explicit source-contained span; implicit tense has no span.
- **Decoder:** first span only, globalized to observation offsets.
- **Runtime consumer:** Typed Claim `temporalSpan`.
- **Tests:** explicit-vs-implicit convention is covered by v2 tests but not rerun in this task.
- **Adult/intimacy and IT/EN/ES:** ordinary temporal evidence across all domains/languages.
- **Verdict:** `PASS_WITH_RISK` because the paired sequence relation is insufficient.

### 4.6 `token.entity`

- **Level:** TOKEN.
- **Semantic responsibility:** PERSON/LOCATION type and span.
- **Input target source:** dataset entities include `span/type/referent`.
- **Output type / labels:** BIO PERSON/LOCATION logits; 5 labels.
- **Null/unknown:** `O`; no OTHER/UNKNOWN entity type.
- **Relationships:** distinct from claim boundary and semantic role heads.
- **Dependencies/ambiguity:** the learned target discards dataset `entity.referent`; multiple PERSON entities therefore have no learned role link.
- **Dataset encoding:** `entity_bio` consumes only `type` and `span`.
- **Decoder:** reconstructs PERSON/LOCATION, then heuristically assigns a categorical referent from subject overlap, identity-name object overlap or exact known surface.
- **Runtime consumer:** Typed Claim `entities`.
- **Tests:** type/span reconstruction and simple context lookup are covered; multi-person role identity is not.
- **Adult/intimacy and IT/EN/ES:** critical to subject/target/perspective in adult third-party language; domain-neutral labels.
- **Verdict:** `ARCHITECTURAL_PROBLEM`.

### 4.7 `sequence.dialogueAct`

- **Level:** SEQUENCE.
- **Semantic responsibility:** conversational function.
- **Input target source:** `claim.labels.dialogueAct`.
- **Output type / labels:** claim-level categorical logits; 6 labels.
- **Null/unknown:** `UNKNOWN`.
- **Relationships:** must differ from predicate and claim kind.
- **Dependencies/ambiguity:** `HYPOTHESIS` duplicates `claimKind=HYPOTHESIS`; generic REPORT and COMMAND are absent.
- **Dataset encoding:** one label per claim crop; builder sets both dialogueAct and claimKind to HYPOTHESIS for hypotheses.
- **Decoder:** argmax by static module label order.
- **Runtime consumer:** Typed Claim and candidate admission hint.
- **Tests:** assertion/request/correction/hypothesis coverage exists, but semantic separation is not tested.
- **Adult/intimacy and IT/EN/ES:** request/question/assertion/correction can be ordinary adult acts; no censorship branch.
- **Verdict:** `ARCHITECTURAL_PROBLEM`.

### 4.8 `sequence.predicate`

- **Level:** SEQUENCE.
- **Semantic responsibility:** Matrix predicate ontology.
- **Input target source:** `claim.labels.predicate`.
- **Output type / labels:** claim-level categorical logits; 12 labels.
- **Null/unknown:** `speech.unresolved` is the explicit fallback.
- **Relationships:** independent from dialogue act, polarity and claim kind.
- **Dependencies/ambiguity:** `presence.reported` is a presence predicate, not a generic evidential REPORT act; `goal.object` is linguistic goal content, not persistent GoalState.
- **Dataset encoding:** one exact predicate per claim.
- **Decoder:** argmax; low global sequence confidence downgrades the emitted predicate to `speech.unresolved`.
- **Runtime consumer:** Typed Claim predicate.
- **Tests:** registry coverage and predicate scoring exist; ontology exhaustiveness is not established.
- **Adult/intimacy and IT/EN/ES:** `preference.like`, `goal.object`, `consent.grant/refuse`, and unresolved provide coarse domain coverage.
- **Verdict:** `PASS_WITH_RISK`.

### 4.9 `sequence.subjectReferent`

- **Level:** SEQUENCE.
- **Semantic responsibility:** categorical subject identity source.
- **Input target source:** `claim.labels.subjectReferent`.
- **Output type / labels:** claim-level categorical logits; 5 labels.
- **Null/unknown:** `UNKNOWN`; no NONE.
- **Relationships:** distinct from explicit subject span; may feed owner/perspective SUBJECT.
- **Dependencies/ambiguity:** KNOWN_ENTITY binding requires the subject mention to match context; RECENT_ENTITY always selects the first recent ref.
- **Dataset encoding:** one label per claim; context supplies speaker/observer/known/recent identifiers.
- **Decoder:** binds using subject surface and context.
- **Runtime consumer:** top-level concrete subject and entity referent assignment.
- **Tests:** simple known entity, recent categories and fail-closed unknown are partially covered.
- **Adult/intimacy and IT/EN/ES:** critical and domain-neutral.
- **Verdict:** `PASS_WITH_RISK`.

### 4.10 `sequence.targetReferent`

- **Level:** SEQUENCE.
- **Semantic responsibility:** semantic target category, distinct from object/value span.
- **Input target source:** `claim.labels.targetReferent`.
- **Output type / labels:** claim-level categorical logits; 7 labels.
- **Null/unknown:** `NONE`, `UNKNOWN`; `SELF` exists but has no documented concrete-ID contract.
- **Relationships:** distinct from object and subject.
- **Dependencies/ambiguity:** no target mention span/link exists. KNOWN_ENTITY is bound from the subject mention, so multiple-person claims cannot identify target correctly.
- **Dataset encoding:** one category per claim; entity referent annotations are not used as training targets.
- **Decoder:** `bind(..., subject_mention)`; SELF returns the literal string `SELF`.
- **Runtime consumer:** Typed Claim target.
- **Tests:** no direct multi-entity target-binding test.
- **Adult/intimacy and IT/EN/ES:** essential for request/consent semantics.
- **Verdict:** `ARCHITECTURAL_PROBLEM`.

### 4.11 `sequence.ownerReferent`

- **Level:** SEQUENCE.
- **Semantic responsibility:** ownership/claim authority category.
- **Input target source:** `claim.labels.ownerReferent`.
- **Output type / labels:** claim-level categorical logits; 6 labels.
- **Null/unknown:** `UNKNOWN`; no NONE; unresolved binding rejects the claim.
- **Relationships:** SUBJECT is a relational value; owner must not be assumed equal to speaker.
- **Dependencies/ambiguity:** no owner mention/link exists; KNOWN_ENTITY binding incorrectly reuses subject mention.
- **Dataset encoding:** categorical label only.
- **Decoder:** binds SUBJECT or context category and requires non-null result.
- **Runtime consumer:** Typed Claim owner and invariant validation.
- **Tests:** SUBJECT/known subject and wrong-owner metric are covered; owner distinct from subject among multiple people is not.
- **Adult/intimacy and IT/EN/ES:** critical for consent/refusal provenance.
- **Verdict:** `ARCHITECTURAL_PROBLEM`.

### 4.12 `sequence.perspectiveReferent`

- **Level:** SEQUENCE.
- **Semantic responsibility:** epistemic/reported perspective category.
- **Input target source:** `claim.labels.perspectiveReferent`.
- **Output type / labels:** claim-level categorical logits; 6 labels.
- **Null/unknown:** `UNKNOWN`; unresolved binding rejects the claim.
- **Relationships:** perspective is not observation source, speaker or subject.
- **Dependencies/ambiguity:** no perspective/source mention or link output exists. KNOWN_ENTITY reuses subject mention.
- **Dataset encoding:** categorical label only; direct third-party assertions exist, but generic reported-source supervision is not owned.
- **Decoder:** context binding with the subject mention.
- **Runtime consumer:** Typed Claim perspective and candidate admission validation.
- **Tests:** only speaker/subject/simple known paths; no distinct reported source test.
- **Adult/intimacy and IT/EN/ES:** critical for third-party adult reports.
- **Verdict:** `ARCHITECTURAL_PROBLEM`.

### 4.13 `sequence.polarity`

- **Level:** SEQUENCE.
- **Semantic responsibility:** composed semantic polarity.
- **Input target source:** `claim.labels.polarity`.
- **Output type / labels:** claim-level categorical logits; 3 labels.
- **Null/unknown:** `UNKNOWN`.
- **Relationships:** must differ from surface negation.
- **Dependencies/ambiguity:** v2 makes its NEGATIVE value determine the entire negation span, creating duplicated supervision and blocking nested negation.
- **Dataset encoding:** one label per claim.
- **Decoder:** argmax retained even when predicate is downgraded on low confidence.
- **Runtime consumer:** Typed Claim polarity.
- **Tests:** negative family coverage exists; compositional negation separation is absent.
- **Adult/intimacy and IT/EN/ES:** essential for refusal/withdrawal and negated desire.
- **Verdict:** `ARCHITECTURAL_PROBLEM`.

### 4.14 `sequence.temporalRelation`

- **Level:** SEQUENCE.
- **Semantic responsibility:** semantic time relation.
- **Input target source:** `claim.labels.temporalRelation`.
- **Output type / labels:** claim-level categorical logits; 5 labels.
- **Null/unknown:** `UNKNOWN`; ATEMPORAL is explicit.
- **Relationships:** distinct from explicit temporal token span.
- **Dependencies/ambiguity:** CURRENT/PAST/FUTURE cover now/yesterday/tomorrow/used-to/will coarsely, but BEFORE/AFTER/DURING have no representable state.
- **Dataset encoding:** one label per claim, with independent explicit/implicit span policy.
- **Decoder:** argmax to Typed Claim.
- **Runtime consumer:** temporal semantics downstream.
- **Tests:** coarse temporal metrics exist; relative-relation coverage is not tested.
- **Adult/intimacy and IT/EN/ES:** domain-neutral and necessary for past/present/future consent/desire.
- **Verdict:** `ARCHITECTURAL_PROBLEM`.

### 4.15 `sequence.claimKind`

- **Level:** SEQUENCE.
- **Semantic responsibility expected:** epistemic/evidential claim kind distinct from conversational act.
- **Input target source:** `claim.labels.claimKind`.
- **Output type / labels:** claim-level categorical logits; 2 labels.
- **Null/unknown:** no UNKNOWN/NONE.
- **Relationships:** HYPOTHESIS exactly overlaps the same dialogueAct label in builders; REPORT/BELIEF states are absent.
- **Dependencies/ambiguity:** low-confidence claims still carry an EXPLICIT or HYPOTHESIS value even when status is abstained.
- **Dataset encoding:** one label per claim.
- **Decoder:** argmax by static label order.
- **Runtime consumer:** Typed Claim and BELIEF_CANDIDATE vs MEMORY_CANDIDATE hint.
- **Tests:** no independence matrix against dialogueAct.
- **Adult/intimacy and IT/EN/ES:** should support hypothetical/report/correction distinctions uniformly; currently incomplete.
- **Verdict:** `ARCHITECTURAL_PROBLEM`.

## 5. Label registry audit

The concrete registry is structurally stable but semantically blocked:

- every expected head exists exactly once;
- list order defines training IDs, native output dimensions and ONNX output order;
- `ids()` deterministically maps label to zero-based index;
- the bundle stores a copy in `labels.json`;
- the runtime does not validate that bundled Matrix label order equals the imported static registry;
- `claimKind` alone lacks an unknown state;
- `CORRECTION` is checked as a legacy alias by the evaluator even though only `CORRECT` is a real label.

Result:

```text
LABEL_REGISTRY = BLOCKED
structuralRegistry = PASS
semanticCoverage = BLOCKED
orderValidationAtRuntime = MISSING
```

## 6. Token-head contract

Token heads are trained using fast-tokenizer character offsets. Special/padding tokens receive `IGNORE=-100`; ordinary outside tokens receive index 0. Boundary supervision uses full observations. Other token heads use claim-local crops and localized character spans.

Important constraints:

- object, subject, negation and temporal decode to at most one scalar span;
- entity supports multiple spans but only PERSON and LOCATION types;
- boundary supports multiple claims;
- overlap across different heads is representable;
- overlapping entities of different types cannot be represented in the single BIO entity head;
- canonical v2 negation supervision makes token negation redundant with polarity.

## 7. Sequence-head contract

All nine sequence heads consume the same first-token pooled hidden vector for a claim crop. Each receives an independent linear classifier and cross-entropy term. Missing sequence targets use `IGNORE=-100`.

The implementation has no structural enforcement of legal combinations. Examples of currently possible outputs include `dialogueAct=HYPOTHESIS` with `claimKind=EXPLICIT`, or `predicate=consent.grant` with `polarity=NEGATIVE`. The validator does not reject such semantic contradictions.

## 8. Referent / ownership audit

The category vocabularies can name speaker, observer, subject, known and recent entity classes, but category is not concrete identity. The overall contract lacks a learned role-to-mention link for target, owner, perspective and reported source.

A synthetic contract-only probe, using no dataset, demonstrated the current decoder behavior:

```text
text = Alice says Bob loves Anna
context knownEntities = Alice/Bob/Anna
predicted subjectReferent = KNOWN_ENTITY
predicted targetReferent = KNOWN_ENTITY
predicted ownerReferent = SUBJECT
predicted perspectiveReferent = KNOWN_ENTITY

decoded subject = npc:bob
decoded target = npc:bob
decoded owner = npc:bob
decoded perspective = npc:bob
status = VALID
```

All three PERSON entities are returned only as `referent=KNOWN_ENTITY`. The intended target Anna and perspective/source Alice are not expressible by the current output. The dangerous fallback is not always “speaker”; it is worse in multi-entity claims: `KNOWN_ENTITY` target/owner/perspective silently reuse the subject mention and can be accepted as VALID.

Example assessment:

| Utterance | Contract assessment |
|---|---|
| I love Anna | subject speaker and target known entity need a target link; category alone is ambiguous |
| Alice says Bob loves Anna | BLOCKED: subject, target and reported source/perspective are three different people with no role links |
| Marco told me that Anna loves Luca | BLOCKED for the same reason, plus report source |
| I think Bob is angry | coarse hypothesis/attribute representation possible, but belief vs hypothesis and Bob role binding remain ambiguous |
| Anna wants Luca to leave | subject/target categories exist but no target link; leaving event predicate is not explicit in the current ontology |

Result: `REFERENT / OWNERSHIP = BLOCKED`.

## 9. DialogueAct vs ClaimKind

The two heads are not independent in the authored contract:

```text
hypothesis row:
dialogueAct = HYPOTHESIS
claimKind = HYPOTHESIS
```

Conversely, assertion/question/request/correction are dialogue acts while claimKind remains EXPLICIT. Generic report, belief and command have no canonical encoding. `presence.reported` cannot solve this because it changes the domain predicate and only describes reported presence.

This is `DUPLICATED_SEMANTIC_RESPONSIBILITY` plus `UNOWNED_SEMANTIC_RESPONSIBILITY`.

Result: `DIALOGUE ACT / CLAIM KIND = BLOCKED`.

## 10. Negation vs Polarity

Nominal heads are separate, but the v2 contract enforces:

```text
polarity == NEGATIVE  => negationSpan == complete sourceSpan
polarity != NEGATIVE  => negationSpan == null
```

Thus the token head does not independently detect a negation cue or compositional scope. Positive, double-negated, metalinguistic and embedded-negation statements cannot preserve both surface negation and composed polarity. The current v2 tests explicitly assert this coupling.

Result: `NEGATION / POLARITY = BLOCKED`.

## 11. Temporal contract

The token/sequence separation itself is sound:

- explicit expression: temporal span plus relation;
- implicit tense: relation without span;
- atemporal: no span plus ATEMPORAL.

The relation label set is too coarse for the requested BEFORE/AFTER/DURING relations. Mapping them into PAST/CURRENT/FUTURE would change semantics and lose the referenced event relation.

Result: `TEMPORAL = BLOCKED`.

## 12. Multi-claim contract

Representable mechanics:

- boundary BIO can produce multiple source spans;
- each source span is re-encoded independently;
- claim-local sequence and token heads are emitted independently;
- source character spans and the observation source ID are preserved per result.

Risks:

- no learned ordering/link constraints beyond BIO order;
- overlapping/nested claims are not representable by one BIO sequence;
- object/subject/negation/temporal keep only the first predicted group;
- reported source and cross-claim coreference cannot be linked;
- every claim receives the same runtime observation source ID, which is provenance but not linguistic reported-source identity.

Result: `MULTI-CLAIM = RISK`.

## 13. Adult / intimacy contract

There is no safety, moderation, blocking or censorship head. Adult/intimacy uses ordinary Matrix outputs.

Coarsely representable:

| Capability | Existing encoding |
|---|---|
| sexual interest/preference | `preference.like` |
| current desire/intention | `goal.object` plus temporal/polarity |
| request | `dialogueAct=REQUEST` |
| consent | `consent.grant` |
| refusal/withdrawal/boundary | `consent.refuse`, polarity/temporal, optionally CORRECT |
| hypothetical adult statement | current duplicated HYPOTHESIS pair |
| explicit/slang/code-switch | tokenizer + ordinary heads; no special semantic downgrade |

The domain remains at risk because consent/refusal involving multiple people depends on blocked target/owner/perspective links; nested negation is blocked; and third-party reports are unowned. Sexual interest versus current desire versus consent is coarsely distinguishable through predicate, but desire versus persistent GoalState must remain a downstream decision.

Result: `ADULT / INTIMACY = RISK`, with the global P0 referent/negation blockers applying directly to consent and withdrawal.

## 14. IT / EN / ES contract

The head and label vocabularies are language-independent. The runtime has no language-specific regex parser and uses fast-tokenizer character offsets. Phase-A and Path-A already established technical tokenizer/representation coverage for IT/EN/ES and code-switch; that evidence is not Matrix task quality.

No label was found with a different declared meaning by language. The same architecture blockers apply in all three languages. Spanish and code-switch need later learnability evidence, but TASK 2 does not perform quality evaluation.

Result: `IT / EN / ES = RISK` (language-neutral contract, blocked semantics shared across languages).

## 15. Dataset → targets → outputs → decoder matrix

| Layer | Actual contract | Alignment | Finding |
|---|---|---|---|
| JSONL row | `schemaVersion,id,split,language,text,context,claims,adultOnly,provenance` | Defined | PASS |
| Claim labels | 9 sequence heads plus deterministic `worldTruth=false` | Registry-checked by v2 audit | PASS structurally |
| Claim spans | `source,object,subject,negation,temporal,entities` | Training data consumes all span fields | RISK |
| Boundary target | all source spans on full observation | `token.boundary` | PASS |
| Claim crop | source substring, local offsets | five claim-local token heads + nine sequence heads | PASS |
| Entity target | dataset has `span,type,referent` | model learns only span/type | BLOCKED |
| Model output | 6 token + 9 sequence + 2 MASSIVE auxiliary outputs | Dimensions/order from static registries | PASS structurally |
| Decoder labels | argmax using imported static registry | bundled Matrix label order not validated | RISK |
| Span decoder | BIO groups; scalar fields keep first | schema has scalar spans | RISK |
| Concrete referents | categorical heads + context | target/owner/perspective use subject mention | BLOCKED |
| Confidence | per-head values recorded | admission threshold uses only 9 sequence confidences | BLOCKED for critical token confidence |
| Authority | `worldTruth=false` deterministic | no learned World Truth output | PASS |
| Admission | decoder emits candidate/reject/no-admission hint | downstream ownership boundary is blurred | RISK |
| Evaluator | gold and prediction both pass through `validate_claim` | shared binding bugs can be masked | BLOCKED as independent proof |

Overall result: `DATASET → TARGET → OUTPUT → DECODER = BLOCKED`.

## 16. Duplicate / unowned responsibility analysis

### Duplicated semantic responsibility

1. `NEGATIVE polarity ↔ full-source negation span` is enforced one-to-one.
2. `dialogueAct=HYPOTHESIS ↔ claimKind=HYPOTHESIS` is authored as the same decision.

### Unowned semantic responsibility

1. generic reported-speech act and linguistic report source;
2. belief/opinion kind distinct from hypothesis;
3. command distinct from request;
4. relative temporal relation BEFORE/AFTER/DURING;
5. concrete target/owner/perspective mention-to-context identity link.

## 17. Architecture-layer ownership audit

The 15 learned heads remain NLU heads. None directly predicts World Truth, persistent memory permission, RelationshipState, AffectiveState, ConsentState, GoalState or behavior.

Positive boundaries:

- `worldTruth` is always forced false;
- low-confidence/invalid claims cannot be promoted;
- `goal.object` is linguistic goal evidence, not persistent GoalState;
- `consent.grant/refuse` is linguistic evidence, not downstream persistent ConsentState.

Risk:

- `validate_claim` emits a field named `memoryAdmission` with `MEMORY_CANDIDATE/BELIEF_CANDIDATE/NO_ADMISSION/REJECT`. These are candidate/invariant hints rather than a database write, but the name and branching overlap the separately specified Memory Admission layer. The final architecture should keep the decision downstream.

Result: `ARCHITECTURE OWNERSHIP = RISK`.

## 18. Implementation bugs found

No bugs were fixed in TASK 2.

| ID | Severity | Finding | Evidence / impact |
|---|---|---|---|
| `IB-01-STUDENT5-BERT-ADAPTER` | P0 | `build_model` assumes DistilBERT `encoder.transformer.layer`, `config.dim`, `config.n_layers`; Student-5 is `BertModel` with `encoder.layer`, `hidden_size`, `num_hidden_layers`. | B0 cannot instantiate the existing heads on pristine Student-5 without an implementation adapter. No contract semantics need change for this fix. |
| `IB-02-MULTI-KNOWN-BIND` | P0 | target/owner/perspective `KNOWN_ENTITY` binding reuses `subject_mention`. | Synthetic probe decoded Bob as subject, target, owner and perspective and accepted VALID. |
| `IB-03-TOKEN-CONFIDENCE-NOT-GATING` | P0 | overall claim confidence is geometric mean of sequence heads only. | Low-confidence negation/temporal/object/entity output can still be admitted as VALID. |
| `IB-04-EVALUATOR-SHARED-ORACLE` | P0 | evaluator constructs gold through the same `validate_claim` used by predictions. | Deterministic binding defects can appear correct in gold and evade ownership-corruption metrics. |
| `IB-05-ENTITY-REFERENT-DROPPED` | P1 | `entity_bio` ignores dataset `entity.referent`. | Dataset → target information loss and no learned role association. |
| `IB-06-BUNDLE-LABEL-ORDER-UNVALIDATED` | P1 | runtime reads bundle labels only for MASSIVE dimensions and decodes Matrix with imported constants. | A mismatched bundle could silently decode indices under a different registry order. |
| `IB-07-ENTITY-REFERENT-NOT-SCORED` | P1 | evaluator entity items include only character and type. | Incorrect entity referent categories are not included in entity F1. |
| `IB-08-SELF-SENTINEL` | P1 | target SELF binds to literal `SELF`, not a context identity. | Downstream identity contract is undocumented/fragile. |
| `IB-09-CORRECTION-ALIAS` | P2 | evaluator checks `CORRECTION` although only `CORRECT` is registered. | Stale non-blocking alias indicates naming drift. |

Implementation bug count: **9**.

## 19. Contract drift found

| ID | Severity | Canonical expectation | Actual contract |
|---|---|---|---|
| `CD-01-NEGATION-POLARITY` | P0 | token negation independent from semantic polarity | v2 forces full-source negation iff NEGATIVE |
| `CD-02-ACT-KIND-HYPOTHESIS` | P0 | dialogueAct distinct from claimKind | HYPOTHESIS duplicated in both |
| `CD-03-REPORT-BELIEF-COMMAND` | P0 | report/belief/command distinctions | no generic labels/ownership |
| `CD-04-REFERENT-ROLE-LINK` | P0 | source/subject/target/owner/perspective distinguishable | categories exist, concrete multi-entity role links do not |
| `CD-05-TEMPORAL-RELATIONS` | P0 | before/after/during representable | only atemporal/current/past/future/unknown |
| `CD-06-CONFIDENCE-ABSTENTION` | P1 | uncertain critical output fails closed per output | token confidence is diagnostic only |
| `CD-07-CLAIMKIND-UNKNOWN` | P1 | unknown/ambiguous handling | claimKind always explicit or hypothesis |

Contract drift count: **7**.

## 20. Contract coverage matrix

| Semantic capability | Owning head(s) | Representable? | Ambiguity / risk |
|---|---|---|---|
| claim boundary | boundary | YES | nested/overlapping claims unsupported |
| subject surface | subject | YES | one span only |
| object/value | object | YES | overloaded value; one span |
| target identity | targetReferent + entity/object | NO reliably | no target link |
| entity type/span | entity | YES | only PERSON/LOCATION |
| negation evidence | negation | NO independently | derived from polarity in v2 |
| polarity | polarity | YES coarse | coupled to negation |
| temporal expression | temporal | YES | one span |
| temporal relation | temporalRelation | PARTIAL | before/after/during missing |
| dialogue act | dialogueAct | PARTIAL | report/command missing; hypothesis overlap |
| predicate | predicate | PARTIAL | narrow ontology plus unresolved fallback |
| subject referent | subjectReferent + subject | YES for simple cases | recent picks first |
| target referent | targetReferent | NO reliably | category not role link |
| owner | ownerReferent | NO reliably | category not role link |
| perspective | perspectiveReferent | NO reliably | category not role link |
| third-party report | perspectiveReferent + claimKind/dialogueAct | NO | report source and act unowned |
| correction | dialogueAct=CORRECT | YES linguistically | must not auto-supersede memory |
| request | dialogueAct=REQUEST | YES | command not distinct |
| goal-language | predicate=goal.object | YES coarse | not GoalState |
| belief-language | claimKind/dialogueAct | NO distinctly | belief absent; hypothesis duplicated |
| hypothesis | dialogueAct + claimKind | YES but duplicated | two heads own same decision |
| multi-claim | boundary + all claim heads | PARTIAL | no nesting/cross-claim links |
| adult desire | preference.like / goal.object | YES coarse | preference vs current desire risk |
| consent | consent.grant | YES | referent binding risk |
| refusal | consent.refuse + polarity | YES coarse | negation coupling risk |
| withdrawal | consent.refuse + temporal/correction | PARTIAL | no dedicated state; downstream distinction |
| boundary/limit | consent.refuse | PARTIAL | coarse predicate |
| code-switch | tokenizer + all heads | structurally YES | no task-quality evidence in TASK 2 |

## 21. P0 / P1 / P2

### P0 — 9

1. `CD-01-NEGATION-POLARITY`
2. `CD-02-ACT-KIND-HYPOTHESIS`
3. `CD-03-REPORT-BELIEF-COMMAND`
4. `CD-04-REFERENT-ROLE-LINK`
5. `CD-05-TEMPORAL-RELATIONS`
6. `IB-01-STUDENT5-BERT-ADAPTER`
7. `IB-02-MULTI-KNOWN-BIND`
8. `IB-03-TOKEN-CONFIDENCE-NOT-GATING`
9. `IB-04-EVALUATOR-SHARED-ORACLE`

### P1 — 6

1. `CD-06-CONFIDENCE-ABSTENTION`
2. `CD-07-CLAIMKIND-UNKNOWN`
3. `IB-05-ENTITY-REFERENT-DROPPED`
4. `IB-06-BUNDLE-LABEL-ORDER-UNVALIDATED`
5. `IB-07-ENTITY-REFERENT-NOT-SCORED`
6. `IB-08-SELF-SENTINEL`

### P2 — 1

1. `IB-09-CORRECTION-ALIAS`

## 22. Validation executed

Safe, data-independent validation at the audited checkpoint:

```text
python -m unittest -v test_inference.py test_evaluate_e2e.py
12 tests run
12 PASS
```

Additional static validation:

```text
exact 15-head registry assertion = PASS
token/sequence head counts = 6/9 PASS
duplicate label assertion = PASS
py_compile labels/model/training_data/inference/evaluate_e2e = PASS
synthetic multi-known-entity decoder probe = REPRODUCED P0
```

Not executed by design:

- `test_training_data.py`
- `test_build_dataset.py`
- `test_dataset_v2.py`
- dataset audit commands that load train/dev/test files

Those tests reconstruct or open DEV/test partitions. Running them would violate this TASK's `canonicalDevUsed=false` / `Frozen unread` boundary. The pre-existing canonical documentation records the prior v2 audit as green; TASK 2 does not reassert it from fresh dataset access.

## 23. Required architecture decision

TASK 3 must not start until the owner reviews a versioned contract change proposal. The minimum decision surface is:

| Head/field | Problem | Evidence | Impact | Change that would be required | Why TASK 2 cannot do it |
|---|---|---|---|---|---|
| negation + polarity | one-to-one coupled targets | v2 audit and tests | nested/composed negation unrepresentable | define independent cue/scope evidence and composed polarity semantics | changes dataset/head semantic contract |
| dialogueAct + claimKind | HYPOTHESIS duplicated; report/belief/command absent | registry + builders | dialogue/evidential identity ambiguous | reassign responsibilities and version labels | label semantics/set change |
| entity + target/owner/perspective/source | category lacks role-to-mention identity | training_data + decoder probe | silent ownership/perspective corruption | add/derive an explicit role-link representation with unambiguous target schema | output/dataset/decoder contract change |
| temporalRelation | before/after/during absent | exact label registry | relative time meaning lost | extend or formally redefine temporal relation ontology | label set/semantics change |

Implementation-only repairs such as the Student-5 BERT adapter, bundle label validation, confidence aggregation and evaluator independence should be handled only after the architectural contract is owner-approved, in a separately authorized task.

## 24. Final gate decision

```text
TASK_2 = ARCHITECTURAL_CONTRACT_CHANGE_REQUIRED
HEADS_FOUND = 15
TOKEN_HEADS = 6
SEQUENCE_HEADS = 9
LABEL_REGISTRY = BLOCKED
DATASET_TARGET_OUTPUT_DECODER = BLOCKED
REFERENT_OWNERSHIP = BLOCKED
NEGATION_POLARITY = BLOCKED
TEMPORAL = BLOCKED
DIALOGUE_ACT_CLAIM_KIND = BLOCKED
MULTI_CLAIM = RISK
ADULT_INTIMACY = RISK
IT_EN_ES = RISK
ARCHITECTURE_OWNERSHIP = RISK
TASK_3 = NOT_STARTED
PATH_B = NOT_STARTED
FROZEN = UNREAD
```

Guards:

```text
student4V22AChanged = false
canonicalDevUsed = false
frozenDataRead = false
frozenDataTokenized = false
frozenDataAnalyzed = false
frozenPredictionsRead = false
pathAModified = false
pathBStarted = false
teachingExecuted = false
trainingExecuted = false
otherRepositoriesModified = false
```

Next action:

```text
AWAIT OWNER REVIEW OF ARCHITECTURAL_CONTRACT_CHANGE_REQUIRED
```
