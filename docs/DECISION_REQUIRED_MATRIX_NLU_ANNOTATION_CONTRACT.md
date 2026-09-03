# DECISION_REQUIRED — Matrix-NLU annotation contract

Status: `BLOCKING_C1_RETRAIN_AND_FROZEN_GATE`  
Scope: Matrix-NLU lab only; production/runtime untouched  
Evidence artifact: `artifacts/matrix-nlu/dev-contract-audit-student-4.json`  
Evidence SHA-256: `8a1fbb2bb6a07952540104f32327d4f729003683cc5cc637a6e355b387f062fb`

## Decision requested

Authorize or reject a versioned correction of the Matrix-NLU annotation
contract before another training run. The current v1 supervision assigns
different span targets to identical model inputs and therefore cannot satisfy
the near-perfect exact TypedClaim gates as written.

## Reproduced evidence

The train/dev-only audit reads four declared datasets and rejects every row
whose split is not `train` or `dev`. It did not read the frozen test partitions.
All 4,016 observations and 5,016 claims pass source-span containment.

Seven exact input/context collisions have incompatible gold outputs:

| Language | Identical input | Incompatible field |
|---|---|---|
| IT | `mi chiamo alberto` | implicit speaker subject: `null` vs name/object span |
| IT | `non amo i locali affollati` | negation cue `[0,3]` vs semantic scope `[0,26]` |
| EN | `my name is albert` | implicit speaker subject: `null` vs name/object span |
| EN | `my name is clara` | implicit speaker subject: `null` vs name/object span |
| EN | `i do not like rain` | negation cue `[5,8]` vs semantic scope `[0,18]` |
| ES | `me llamo alberto` | implicit speaker subject: `null` vs name/object span |
| ES | `no me gusta la lluvia` | negation cue `[0,2]` vs semantic scope `[0,21]` |

This is not merely class imbalance. A deterministic model receiving the same
text and context cannot emit both exact targets. The broader convention audit
also finds mixed cue/full-scope supervision for negative `preference.like` and
`residence.place`. Matrix generated DEV has 126 FUTURE claims with no temporal
span, while P0.5 DEV has six FUTURE claims with an explicit temporal span; this
temporal variance needs the same canonical review, although implicit tense can
legitimately have no surface span.

Student-4 DEV evidence is consistent with the defect: claim count reached
1.0, ownership corruption and invented World Truth reached zero, while exact
span errors remained dominant and no threshold could pass. Another unchanged
training run would repeat an impossible objective.

## Options considered

### A — Version v2 with one canonical semantic span per field (recommended)

- Define existing `negation` as the semantic negation scope, not the cue.
- Keep an implicit first-person `subject` span `null`; the stated name remains
  the object/entity span and `subjectReferent=SPEAKER` carries ownership.
- Define when an explicit temporal expression must receive a temporal span;
  implicit grammatical tense may remain spanless.
- Regenerate and re-freeze corrected v2 train/dev/test assets while preserving
  every v1 file/hash/result as immutable historical evidence.

This is the smallest coherent change and keeps the current model heads. It
still requires canonical approval because frozen-gold hashes and annotation
semantics change.

### B — Add separate negation cue and scope fields

Represent `negationCueSpan` and `negationScopeSpan` independently, then add or
derive the corresponding model output. This is semantically richer but changes
the TypedClaim/model contract and is a larger architectural decision than C1
needs to remove the present contradiction.

### C — Relax exact-span gates

Score overlap or exclude these fields from exact claim equality. Rejected as a
local workaround: it weakens the published gate and leaves downstream span
semantics ambiguous.

### D — Learn dataset/provenance-specific outputs

Rejected. Runtime inputs do not contain the benchmark source identity, and
making output depend on it would be benchmark overfitting rather than language
understanding.

## Required supervisor resolution

Choose the canonical meaning/versioning policy for negation, implicit subject
and explicit temporal spans. Recommendation: authorize Option A as
`matrix.nlu.dataset.v2`, preserve v1 immutably, and require a fresh named model
variant rather than resuming student-4 as if its supervision were unchanged.

Until that resolution, the one-click pipeline now writes the audit report and
fails before MASSIVE preparation/training. Existing student-4 checkpoints,
reports and model artifacts remain preserved. No B4 or production integration
is authorized by this document.
