# Canonical Adult / Intimacy NLU Coverage

Repository: `MATRIXNEO23/matrix-understanding-lab`
Date: 2026-09-04
Status: CANONICAL TRAINING / PRUNING COVERAGE POLICY

## Purpose

Matrix-NLU must preserve and understand adult sexual/intimate language as ordinary semantic input. This domain is commercially important for the intended product and must not be treated as a marginal edge case.

This policy is about NLU comprehension, vocabulary coverage and semantic classification. It is not a moderation taxonomy and must not turn ordinary adult/intimate language into generic `unsafe`, `block`, `censor` or equivalent labels.

All authored training/evaluation material under this policy is adult-only. Do not create or use sexual content involving minors.

## Mandatory coverage in vocabulary pruning

Any vocabulary-pruned backbone must retain robust IT/EN/ES coverage for adult/intimate language, including colloquial forms and code-switching. Frequency alone must not delete important low-frequency semantic pieces.

Coverage must include, at minimum:

- sexual and intimate vocabulary used in ordinary conversation;
- anatomy and body-part terminology relevant to adult intimacy;
- attraction, arousal, desire and sexual interest;
- romantic intimacy and physical affection;
- sexual requests, invitations and proposals;
- consent granting, consent refusal, withdrawal of consent and boundaries;
- preference statements, likes/dislikes and personal limits;
- partner/relationship terminology and role language;
- orientation and identity vocabulary when relevant to semantic understanding;
- common slang, euphemisms, abbreviations and colloquial sexual expressions;
- common English sexual/intimacy terms embedded in Italian or Spanish sentences;
- common Italian/Spanish terms embedded in English sentences;
- sexting/chat-style wording, spelling variation, contractions and informal punctuation;
- references to sexual practices and preferences at a level required for classification and intent understanding;
- references to protection, contraception and sexual-health context when semantically relevant;
- negated sexual intent (`does not want`, refusal, disinterest, boundary statements);
- hypothetical, conditional, past and future sexual/intimate statements;
- questions vs requests vs assertions vs corrections in adult/intimate contexts;
- third-party reports about adult/intimate topics;
- ownership, target, subject and perspective resolution in adult/intimate statements;
- ambiguity and unresolved sexual/intimate language;
- coercion/non-consent/assault references as semantic situations that must be distinguished from consensual adult intimacy, without treating every sexual statement as coercive or unsafe by default.

## Mandatory semantic distinctions

The model must learn to distinguish, where the existing Matrix label contract permits:

```text
DESIRE / PREFERENCE
REQUEST
QUESTION
ASSERTION
CORRECTION
CONSENT_GRANT
CONSENT_REFUSE
BOUNDARY / WITHDRAWAL
NEGATED_DESIRE
HYPOTHESIS / CONDITIONAL
THIRD_PARTY_REPORT
UNRESOLVED / AMBIGUOUS
```

These distinctions must be represented using the existing Matrix heads and labels rather than inventing a parallel moderation classifier.

Critical heads include:

```text
token.boundary
token.object
token.subject
token.negation
token.temporal
token.entity
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

## Pruning gate

A pruned vocabulary is NOT acceptable if it materially worsens adult/intimacy tokenization relative to general IT/EN/ES text.

Report separately for adult/intimacy probes:

```text
UNK rate by language
mean tokens per sentence
p95 tokens per sentence
tokenization inflation vs original MiniLM
code-switching inflation
coverage of slang/euphemisms
coverage of anatomy/body terminology
coverage of consent/refusal/boundary language
coverage of request/desire/question/correction contrasts
coverage of negation and temporal forms
```

Do not select a smaller vocabulary if the size saving comes from disproportionately damaging this domain.

## Training policy

Tokenization alone is not semantic understanding.

After pruning passes, supervised Matrix training must contain TRAIN-ONLY adult/intimacy examples sufficient to teach the Matrix heads how to map the backbone representation to the required semantic contract.

Training should include balanced contrast sets, for example conceptually:

```text
desire vs request
consent vs refusal
request vs assertion
question vs request
positive vs negated desire
current vs past vs future intent
self vs partner vs third-party target
speaker perspective vs reported third-party perspective
correction vs original statement
explicit vs hypothetical claim
```

Do not use canonical dev/frozen material to build these training examples.

## Anti-forgetting rule

Student-5 should initially keep the MiniLM backbone frozen and train only the Matrix translator/heads. This preserves the pretrained language competence as much as possible.

Only after targeted error analysis may progressively more capacity be introduced (small adapter/MLP, then optionally a very small number of final backbone layers). Full-backbone fine-tuning is not the default.

## Acceptance principle

Adult/intimacy performance is a first-class Matrix-NLU quality dimension.

A candidate that performs well on general language but is materially weak on adult/intimacy semantics must be reported as having a domain limitation and must not be promoted merely on aggregate metrics.

The objective is robust adult semantic understanding, not censorship and not unrestricted memory admission. Stable memory, authority and persistent affect remain controlled by the downstream Matrix architecture.
