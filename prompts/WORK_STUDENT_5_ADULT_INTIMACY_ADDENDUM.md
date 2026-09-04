# WORK ADDENDUM — Student-5 Adult / Intimacy Coverage

This addendum is MANDATORY for:

`prompts/WORK_STUDENT_5_MINILM_IT_EN_ES_PRUNED.md`

Read and enforce:

`docs/ADULT_INTIMACY_NLU_COVERAGE.md`

Do not treat adult/intimacy as a small edge-case sample.

For Student-5 pruning and pre-teaching comparison, adult/intimacy is a first-class domain and must receive explicit coverage metrics separate from aggregate IT/EN/ES metrics.

Mandatory coverage includes:

- sexual/intimate vocabulary;
- anatomy/body terminology relevant to adult intimacy;
- attraction/arousal/desire;
- romantic/physical intimacy;
- requests/invitations/proposals;
- consent/refusal/withdrawal/boundaries;
- preferences/likes/dislikes/limits;
- relationship/partner/role terminology;
- orientation/identity vocabulary when semantically relevant;
- slang/euphemisms/abbreviations/chat spelling;
- IT/EN/ES code-switching;
- sexual-health/protection/contraception vocabulary where relevant;
- practices/preferences terminology needed for NLU classification;
- negation;
- temporal forms;
- hypothetical/conditional forms;
- questions vs requests vs assertions vs corrections;
- third-party reports;
- subject/target/owner/perspective resolution;
- ambiguous/unresolved language;
- coercion/non-consent/assault references distinguished semantically from consensual adult intimacy.

All authored training/probe material must be adult-only. Do not create or use sexual content involving minors.

Pruning MUST NOT preferentially destroy adult/intimacy vocabulary simply because some pieces are low-frequency.

Report separately:

```text
adult/intimacy UNK rate by IT/EN/ES
adult/intimacy token inflation
adult/intimacy p95 token length
slang/euphemism coverage
anatomy/body coverage
consent/refusal/boundary coverage
negation coverage
code-switching coverage
semantic contrast preservation before teaching
```

Before teaching, run contrast probes on the ORIGINAL and each PRUNED MiniLM candidate for:

```text
desire vs request
consent vs refusal
request vs assertion
question vs request
positive vs negated desire
present vs past vs future intent
self/partner/third-party target
speaker vs reported third-party perspective
correction vs original statement
explicit vs hypothetical claim
```

Tokenization alone is not enough. If Phase A passes, supervised Matrix teaching must include TRAIN-ONLY adult/intimacy contrast examples using the existing Matrix heads/labels.

Do not invent a censorship taxonomy. Adult/intimacy language remains ordinary NLU semantics. Downstream Authority/Memory Admission continue to decide persistence and truth.

A Student-5 candidate that is strong in aggregate but materially weak on adult/intimacy semantics must be reported as domain-limited and must not be treated as clearly superior to Student-4-v2.2A.
