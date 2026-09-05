# Matrix-NLU Contract V3

Status: **FROZEN FOR IMPLEMENTATION REVIEW**  
Contract identifier: `MATRIX_NLU_CONTRACT_V3`  
Design checkpoint: Student-5 TASK 2.1  
Implementation status: **NOT IMPLEMENTED**  
Training status: **NOT STARTED**

## 1. Purpose and boundary

This specification defines the versioned linguistic contract between the multilingual encoder, Matrix multi-task heads, deterministic decoder, and downstream Typed Claims.

The output is **structured linguistic evidence**. It does not decide authority, truth, persistence, memory admission, relationship state, affective state, persistent consent state, goal state, or behavior. Those remain downstream responsibilities.

The canonical flow is:

```text
USER TEXT
-> tokenizer / claim boundary
-> multilingual Transformer encoder
-> Matrix multi-task heads
-> MatrixNluOutput.claims[]
-> deterministic invariant validator
-> downstream Typed Claims
```

V3 replaces, but does not silently overwrite, the V2 contract. A bundle MUST declare its contract identifier and exact ordered registries.

## 2. Frozen design decisions

| Decision | V3 freeze |
|---|---|
| Head count | 16: 6 token + 10 sequence |
| Role linking | mention/candidate pointers, never provenance categories as identity |
| Source | dedicated `sourceReferent` pointer head |
| Negation | cue spans only; independent from composed polarity |
| Polarity | claim-level composed semantic polarity |
| Dialogue act | conversational action |
| Claim kind | epistemic/evidential presentation |
| Temporal | evidence spans plus claim-level relation and explicit anchor reference |
| Unknown | distinct from known absence and ambiguity |
| Confidence | field-level, conservative overall confidence, fail-closed critical fields |
| Multi-claim | flat atomic claims with observation-level mention IDs; recursive nesting is unsupported in V3 |
| Languages | identical semantics for IT, EN, ES, and code-switch input |
| Adult/intimacy | ordinary first-class semantics; no censorship/moderation path |

`HEAD_COUNT_CHANGE_REQUIRED = true`. The one additional head is necessary because `source != perspective`; encoding source in `claimKind`, `perspectiveReferent`, entity type, or decoder heuristics would recreate an unowned or duplicated responsibility.

## 3. Head registry

### 3.1 Token heads (6)

| Ordered name | Labels / output | Responsibility |
|---|---|---|
| `boundary` | `O, B-CLAIM, I-CLAIM` | Flat atomic claim spans in the observation |
| `object` | `O, B-OBJECT, I-OBJECT` | Surface value/object evidence, not target identity |
| `subject` | `O, B-SUBJECT, I-SUBJECT` | Explicit grammatical/semantic subject mention |
| `negation` | `O, B-NEGATION_CUE, I-NEGATION_CUE` | Linguistic negation cues only |
| `temporal` | `O, B-TEMPORAL, I-TEMPORAL` | Explicit temporal expressions |
| `entity` | `O, B-PERSON, I-PERSON, B-LOCATION, I-LOCATION` | Mention spans and coarse entity type |

Token heads MAY emit multiple non-overlapping BIO groups. Decoders MUST preserve every valid group; silently selecting the first group is forbidden. Span offsets are UTF-8 JSON character offsets `[start, end)` into the complete observation.

### 3.2 Sequence heads (10)

| Ordered name | Output | Responsibility |
|---|---|---|
| `dialogueAct` | closed categorical | Conversational action performed by the speaker |
| `predicate` | closed categorical | Matrix domain predicate ontology |
| `subjectReferent` | candidate pointer | Entity filling the proposition subject role |
| `targetReferent` | candidate pointer | Entity toward which the proposition/action is directed |
| `ownerReferent` | candidate pointer | Entity whose state/property/goal/consent is expressed |
| `perspectiveReferent` | candidate pointer | Viewpoint holder from whose perspective the proposition is framed |
| `sourceReferent` | candidate pointer | Linguistic source/attributor of the proposition |
| `polarity` | closed categorical | Composed semantic polarity of the claim |
| `temporalRelation` | relation label + anchor pointer | Relation of the claim event/state to a temporal anchor |
| `claimKind` | closed categorical | Epistemic/evidential manner in which the proposition is presented |

The five referent heads share one pointer contract but remain separate semantic heads. They score a bounded candidate table; `KNOWN_ENTITY` and `RECENT_ENTITY` are not legal pointer values.

## 4. Closed label registries

### 4.1 `dialogueAct`

Ordered labels:

```text
ASSERT
QUESTION
REQUEST
COMMAND
CORRECT
UNKNOWN
```

- `ASSERT`: present a proposition, including a reported, believed, or hypothetical proposition.
- `QUESTION`: seek information or confirmation.
- `REQUEST`: ask another participant to perform or provide something while preserving request force.
- `COMMAND`: direct another participant to act with imperative force.
- `CORRECT`: explicitly replace or retract linguistic content in the current discourse. It never performs Memory supersession.
- `UNKNOWN`: act cannot be resolved from linguistic evidence.

`HYPOTHESIS` is forbidden as a dialogue act; hypothesis belongs to `claimKind`.

### 4.2 `claimKind`

Ordered labels:

```text
DIRECT
REPORT
BELIEF
HYPOTHESIS
UNKNOWN
```

- `DIRECT`: proposition is presented directly, without an overt report, belief, or hypothetical wrapper.
- `REPORT`: proposition is attributed linguistically to a source.
- `BELIEF`: proposition is presented as a belief, opinion, or thought of a holder.
- `HYPOTHESIS`: proposition is marked as possible, conditional, conjectural, or uncertain.
- `UNKNOWN`: evidence cannot distinguish the epistemic/evidential kind.

These labels describe wording, not truth. `REPORT` is not `presence.reported`; `BELIEF` does not create BeliefState; `HYPOTHESIS` is not a low-confidence fallback.

### 4.3 `polarity`

Ordered labels:

```text
POSITIVE
NEGATIVE
UNKNOWN
```

`POSITIVE` and `NEGATIVE` are the composed polarity of the atomic proposition after linguistic negation is interpreted. `UNKNOWN` is mandatory when composition cannot be resolved. Double negation may have two cue spans and `POSITIVE` polarity. A negation cue does not mechanically force `NEGATIVE`, and absence of a cue does not mechanically force `POSITIVE`.

### 4.4 `temporalRelation`

Ordered labels:

```text
ATEMPORAL
CURRENT
PAST
FUTURE
BEFORE
AFTER
DURING
RECURRENT
AT_REFERENCE
UNKNOWN
```

- `ATEMPORAL`: temporal placement is not applicable to the predicate.
- `CURRENT`, `PAST`, `FUTURE`: relation to speech time.
- `BEFORE`, `AFTER`, `DURING`: relation to the explicit `temporalAnchorRef`.
- `RECURRENT`: repeated/habitual time pattern.
- `AT_REFERENCE`: relation to a discourse/context reference time that is neither necessarily speech time nor a surface date.
- `UNKNOWN`: relation cannot be resolved.

`INTERVAL` is an expression shape, not a relation, and therefore is not a sequence label. Interval surface evidence remains in `temporalEvidence[]`; its normalized form is downstream/optional linguistic metadata. `temporalAnchorRef` is required for `BEFORE`, `AFTER`, `DURING`, and `AT_REFERENCE`, otherwise the field MUST be unresolved.

### 4.5 `predicate`

V3 retains the ordered initial ontology:

```text
identity.name
identity.age
residence.place
presence.reported
preference.like
work.role
possession.has
goal.object
attribute.is
consent.grant
consent.refuse
speech.unresolved
```

`presence.reported` means a reported/detected presence predicate only. It MUST NOT stand in for the `REPORT` claim kind. `goal.object` is linguistic goal/desire evidence, not persistent GoalState. `consent.grant` and `consent.refuse` are linguistic evidence, not persistent ConsentState. Uncovered predicates degrade to `speech.unresolved`; unfamiliar or adult vocabulary alone MUST NOT cause rejection.

### 4.6 Pointer special values

Every referent pointer chooses exactly one candidate ID or one of:

```text
NONE
UNKNOWN
```

- `NONE`: the role is known not to apply.
- `UNKNOWN`: the role applies or may apply but cannot be bound safely.

`SELF`, `SUBJECT`, `KNOWN_ENTITY`, and `RECENT_ENTITY` are forbidden V3 output labels. If two roles share an identity, both point to the same candidate ID. Ambiguity is represented by `fieldStatus=AMBIGUOUS`, primary value `UNKNOWN`, and ranked alternatives; it is not a third special pointer.

## 5. Referent candidate and role-link contract

### 5.1 Observation-level candidate table

The decoder creates a stable table before role decoding:

```json
{
  "candidateId": "mention:m2",
  "kind": "MENTION",
  "mentionId": "m2",
  "span": [25, 29],
  "entityType": "PERSON",
  "resolvedEntityRef": null,
  "resolutionStatus": "UNRESOLVED"
}
```

Candidate kinds are:

```text
CONTEXT_SPEAKER
CONTEXT_OBSERVER
MENTION
CONTEXT_ENTITY
```

Stable reserved IDs are `ctx:speaker` and `ctx:observer`. Mention IDs are assigned by observation start offset, then end offset, then entity label. Context entity IDs are supplied by trusted runtime context and MUST have stable opaque EntityRefs.

Exact surface-to-context matching may attach `resolvedEntityRef`; heuristic capitalization, first-recent selection, and reuse of the subject mention for another role are forbidden. A mention remains a valid linguistic candidate even when entity resolution is unknown.

The implementation MUST define a versioned `maxReferentCandidates` and deterministic overflow policy. Truncation MUST retain speaker/observer and all candidates overlapping a critical predicted span before optional context-only candidates. Any required role lost to overflow causes abstention.

### 5.2 Pointer semantics

- `subjectReferent`: entity that semantically fills the subject argument.
- `targetReferent`: entity toward which the act/state is directed; `NONE` is allowed.
- `ownerReferent`: entity whose property, preference, goal, or consent is asserted; must not default to speaker.
- `perspectiveReferent`: viewpoint holder; may equal source but is not derived from it.
- `sourceReferent`: quoted/reported/belief source or current speaker for direct self-attribution; must not default from perspective when evidence differs.

The same candidate can fill multiple roles. Different candidates MUST remain distinct even when all are PERSON mentions.

Example:

```text
Marco told me that Anna loves Luca.
speaker     = ctx:speaker
source      = mention:m0 (Marco)
subject     = mention:m1 (Anna)
target      = mention:m2 (Luca)
owner       = mention:m1 (Anna)
perspective = mention:m0 (Marco)
```

### 5.3 Chosen architecture

V3 adopts mention candidates plus masked pointer scoring. Entity/subject/object token representations and reserved context candidates form the candidate table; each role head scores candidate embeddings plus `NONE` and `UNKNOWN`. A bounded tensor and mask keep export ONNX/mobile-friendly. This is an adaptation of span/antecedent scoring, not an imported runtime dependency.

## 6. Negation contract

`token.negation` annotates **cue spans only**. It does not annotate the whole source span and does not attempt scope in V3.

Rules:

1. Preserve every overt lexical or morphological cue that tokenizer offsets can represent.
2. Multiple cues produce multiple BIO groups.
3. Negative concord cues are preserved as separate evidence while polarity is composed once.
4. Double negation preserves both cues; polarity may be positive.
5. Metalinguistic or attribution negation preserves the cue. If flat atomic decomposition cannot assign its proposition safely, `polarity=UNKNOWN` and the claim abstains rather than guessing.
6. A cue may occur with positive, negative, or unknown composed polarity.
7. No cue is emitted for purely implicit semantic opposition unless surface evidence exists.

V3 intentionally defers full cue-to-scope graphs. They add annotation and decoder complexity not required for the initial Typed Claim contract. Claim boundaries provide the atomic scope unit; cases that exceed flat scope are `UNRESOLVED`, never forced.

## 7. Temporal contract

`token.temporal` preserves all explicit temporal spans as `temporalEvidence[]`, each with a stable ID. `sequence.temporalRelation` supplies a relation and, when required, an anchor pointer:

```json
{
  "relation": "AFTER",
  "temporalAnchorRef": "temporal:t0",
  "confidence": 0.0,
  "fieldStatus": "RESOLVED"
}
```

Anchor kinds are speech time, context reference time, another temporal evidence ID, or another claim ID in the same observation. No wall-clock time is fabricated by the NLU. `yesterday/now/tomorrow` map to PAST/CURRENT/FUTURE relative to speech time; `before/after/during` require anchors; `every Friday` maps to RECURRENT; `used to` maps to PAST with cue evidence.

## 8. Confidence, validity, ambiguity, and abstention

Each field has:

```text
value
confidence
fieldStatus = RESOLVED | UNKNOWN | AMBIGUOUS | NOT_APPLICABLE
alternatives[] (optional, diagnostic)
```

Each claim has:

```text
structuralStatus = VALID | INVALID
interpretationStatus = RESOLVED | AMBIGUOUS | ABSTAINED
overallInterpretationConfidence
diagnostics[]
```

The invariant validator, not a neural head, owns structural validity and abstention. Critical fields are claim-dependent but include boundary, predicate, subject, owner, perspective, source where attribution is present, target where the predicate requires it, negation when polarity depends on it, temporal relation/anchor where temporal evidence is asserted, and relevant entity pointers.

The overall confidence MUST be conservative: it MUST NOT exceed the minimum confidence of any required critical field. A calibrated aggregation may lower it further. Threshold values are versioned runtime/evaluation configuration calibrated only in an authorized later task; no threshold is frozen here.

Fail-closed rules:

- invalid span, invalid pointer, missing required anchor, or registry mismatch -> `structuralStatus=INVALID`;
- required critical field below its threshold -> `interpretationStatus=ABSTAINED`;
- materially competing referent candidates -> `AMBIGUOUS` with no guessed primary identity;
- abstained/invalid claims emit no World Truth or Memory Admission decision;
- low token confidence is never only an invisible diagnostic.

## 9. MatrixNluOutput schema

Normative conceptual schema:

```json
{
  "contractVersion": "MATRIX_NLU_CONTRACT_V3",
  "input": "...",
  "observationSourceId": "...",
  "speakerRef": "...",
  "observerRef": "...",
  "mentions": [],
  "referentCandidates": [],
  "claims": [
    {
      "claimId": "c0",
      "sourceSpan": [0, 10],
      "subjectSpans": [],
      "objectSpans": [],
      "negationCueSpans": [],
      "temporalEvidence": [],
      "entityMentionIds": [],
      "dialogueAct": {},
      "predicate": {},
      "subjectReferent": {},
      "targetReferent": {},
      "ownerReferent": {},
      "perspectiveReferent": {},
      "sourceReferent": {},
      "polarity": {},
      "temporalRelation": {},
      "claimKind": {},
      "confidenceByField": {},
      "overallInterpretationConfidence": 0.0,
      "structuralStatus": "VALID",
      "interpretationStatus": "RESOLVED",
      "diagnostics": []
    }
  ]
}
```

`worldTruth`, `memoryAdmission`, authority, belief confidence, persistent consent, persistent goal, relationship, affective state, and behavior decision are forbidden fields in the V3 NLU output.

## 10. Dataset target schema

V3 training rows remain observation-based and language-neutral:

```json
{
  "contractVersion": "MATRIX_NLU_CONTRACT_V3",
  "id": "...",
  "language": "it|en|es|code-switch",
  "text": "...",
  "mentions": [
    {"mentionId": "m0", "span": [0, 5], "entityType": "PERSON"}
  ],
  "claims": [
    {
      "claimId": "c0",
      "family": "...",
      "sourceSpan": [0, 20],
      "subjectSpans": [[0, 5]],
      "objectSpans": [],
      "negationCueSpans": [],
      "temporalEvidence": [],
      "entityMentionIds": ["m0"],
      "labels": {
        "dialogueAct": "ASSERT",
        "predicate": "attribute.is",
        "subjectReferent": "mention:m0",
        "targetReferent": "NONE",
        "ownerReferent": "mention:m0",
        "perspectiveReferent": "ctx:speaker",
        "sourceReferent": "ctx:speaker",
        "polarity": "POSITIVE",
        "temporalRelation": {"relation": "CURRENT", "anchorRef": "speech-time"},
        "claimKind": "DIRECT"
      }
    }
  ]
}
```

Required fields are contract version, row/claim IDs, language, text, source span, mention table, all ten sequence targets, and explicit empty arrays/special pointers. `null` MUST NOT conflate NONE, UNKNOWN, and missing annotation. Character spans must lie within text and claim-scoped spans must lie within their source span unless explicitly observation-scoped.

The trainer MUST encode role targets against the exact deterministic candidate table that the decoder will build. Registry order and candidate policy are bundle metadata and MUST be validated at load.

## 11. Decoder semantic contract

The decoder MUST:

1. validate contract ID and exact ordered registries before reading logits;
2. reconstruct all valid BIO groups and preserve their observation offsets;
3. build one deterministic observation-level mention/candidate table;
4. decode each role independently to a candidate ID or legal special value;
5. never bind a role using another role's mention;
6. never choose the first recent/known entity as an identity shortcut;
7. preserve source and perspective independently;
8. compose polarity independently from cue existence;
9. require temporal anchors for relative labels;
10. apply structural and confidence gates before emitting a resolved Typed Claim candidate;
11. preserve ambiguity and abstention explicitly;
12. produce no downstream state decision.

Recursive nested claims are not part of V3. The boundary head produces flat atomic, non-overlapping claim spans. Cross-claim references use observation-level mention IDs and claim IDs. If faithful flattening is impossible, the affected claim is `ABSTAINED`/`UNKNOWN`, not heuristically nested.

## 12. Evaluator independence

Gold construction and prediction decoding MUST be independent implementations. The evaluator MUST NOT call the production validator to create gold outputs. It must score at least:

- ordered registry identity;
- claim boundary exactness;
- all token span groups, including cue/entity multiplicity;
- every categorical head;
- each role pointer against candidate identity;
- source/perspective distinction;
- temporal relation plus anchor;
- field status and abstention behavior;
- end-to-end exact claim set;
- ownership/source corruption counts;
- IT/EN/ES and adult/intimacy slices without censorship penalties.

## 13. Language and domain invariants

All labels and pointer semantics are language-independent. Dataset annotations may differ only in spans and lexical evidence, not label meaning. IT, EN, ES, negative concord, pronouns, and code-switch input use the same candidate/pointer and status contracts.

Adult/intimacy language is processed identically to other semantic content. Desire, request, consent, refusal, withdrawal, boundary, correction, time, source, ownership, and perspective remain distinct. No moderation label, automatic confidence penalty, block, or semantic downgrade is permitted. Authored sexual examples must concern adults.

## 14. Required examples

| Utterance | Required distinctions |
|---|---|
| `Bob lives in Rome.` | ASSERT + DIRECT; source speaker; subject/owner Bob |
| `Does Bob live in Rome?` | QUESTION + DIRECT; no forced truth |
| `Please tell Bob to leave.` | REQUEST, not COMMAND; target Bob |
| `Bob, leave now.` | COMMAND; target/subject Bob; CURRENT |
| `Alice says Bob lives in Rome.` | ASSERT + REPORT; source Alice, subject/owner Bob |
| `I think Bob is angry.` | ASSERT + BELIEF; source/perspective speaker, subject/owner Bob |
| `Maybe Bob is angry.` | ASSERT + HYPOTHESIS |
| `No, I was wrong, Bob lives in Milan.` | CORRECT + DIRECT; no Memory supersession |
| `It is not true that I hate coffee.` | cue `not`; polarity derived compositionally or UNKNOWN |
| `I never disliked it.` | cue `never`; composed polarity may be POSITIVE |
| `I agreed yesterday, but not now.` | two flat claims; past grant vs current negative/refusal evidence |
| `Anna said she does not want Luca.` | REPORT; source/perspective Anna; subject/owner Anna; target Luca; cue preserved |

Equivalent IT/ES examples MUST receive the same semantic labels. Code-switch terms do not alter the contract.

## 15. V2 to V3 migration

| V2 field/label | V3 | Class | Rule |
|---|---|---|---|
| six token head names | same names | CONDITIONAL | negation semantics and plural spans break compatibility |
| `boundary/object/subject/temporal/entity` BIO | same responsibility | CONDITIONAL | valid only where scalar/multiplicity constraints remain satisfied |
| full-source negative `spans.negation` | cue spans | NO_MAPPING | requires cue reannotation; no language heuristic migration |
| `dialogueAct ASSERT/CORRECT/QUESTION/REQUEST/UNKNOWN` | same labels | LOSSLESS | index order changes and bundle must declare V3 |
| `dialogueAct HYPOTHESIS` | `dialogueAct ASSERT` + `claimKind HYPOTHESIS` | CONDITIONAL | confirm conversational force from annotation |
| `claimKind EXPLICIT` | `DIRECT/REPORT/BELIEF/UNKNOWN` | LOSSY | wrapper semantics require reannotation |
| `claimKind HYPOTHESIS` | `HYPOTHESIS` | LOSSLESS | subject to independent dialogue act target |
| `KNOWN_ENTITY/RECENT_ENTITY` | concrete candidate ID | NO_MAPPING | category lacks identity; reannotation required |
| `SPEAKER/OBSERVER` | `ctx:speaker/ctx:observer` | LOSSLESS | deterministic rename |
| target `SELF` | concrete candidate ID | CONDITIONAL | map only with explicit role semantics; never literal SELF |
| owner/perspective `SUBJECT` | same candidate as subject | CONDITIONAL | only after subject pointer is unambiguous |
| no source field | `sourceReferent` | NO_MAPPING | new target required |
| polarity labels | same labels | CONDITIONAL | target must be independently composed, not copied from cue |
| temporal `ATEMPORAL/CURRENT/PAST/FUTURE/UNKNOWN` | same labels | LOSSLESS | new anchor rules still apply |
| before/after/during absent | new relation labels | NO_MAPPING | affected examples require annotation |
| no field status | field/claim statuses | DETERMINISTIC_MIGRATION | derive only from complete V3 labels; otherwise UNKNOWN |

Overall migration classification: **PARTIAL / BREAKING**. Existing TRAIN material divides into:

- `DIRECT_REUSE`: unaffected span/predicate examples after V3 validation;
- `DETERMINISTIC_MIGRATION`: speaker/observer IDs and exact unchanged labels;
- `NEEDS_REANNOTATION`: negation, wrapper kind, multi-entity roles, source, relative temporal cases;
- `UNUSABLE`: rows whose original annotations cannot distinguish required V3 states.

DEV and Frozen migration is not authorized by this design task.

## 16. Forbidden shortcuts

- derive negation spans from polarity;
- derive polarity directly from cue presence;
- duplicate hypothesis in dialogue act and claim kind;
- encode report with `presence.reported`;
- treat `KNOWN_ENTITY`/`RECENT_ENTITY` as concrete identity;
- default unresolved subject, owner, source, or perspective to speaker;
- collapse source into perspective;
- bind target/owner/perspective/source from the subject mention;
- discard all but the first predicted span;
- ignore critical token confidence;
- force missing `claimKind` to DIRECT;
- construct evaluator gold through the production decoder;
- emit memory, truth, authority, consent-state, or goal-state decisions;
- apply adult/intimacy moderation or confidence penalties.

## 17. Implementation gate

TASK 2.2 may implement this contract only after owner review. It must begin from the pristine Student-5 FP32 40k path when model work is eventually authorized; the Path-A INT8 runtime probe is never a training base.

Before any head training, TASK 2.2 must implement and test the registry, V3 schemas, candidate builder, pointer outputs, decoder/validator, independent evaluator, BERT adapter, bundle contract checks, and safe migration tooling without reading canonical DEV or Frozen.

This freeze does not authorize TASK 2.2, TASK 3, Path B, training, DEV access, or Frozen access.
