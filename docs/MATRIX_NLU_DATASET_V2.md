# Matrix-NLU dataset v2

Status: `FROZEN_PRETRAINING_AUDIT_PASS`  
Dataset schema: `matrix.nlu.dataset.v2`  
Supervisor decision: Option A in
`DECISION_REQUIRED_MATRIX_NLU_ANNOTATION_CONTRACT.md`

## Immutable lineage

The v2 builder reconstructs v1 in memory with the original
`matrix_nlu/build_dataset.py` and refuses to proceed unless all six historical
v1 hashes match. It never overwrites v1 files, checkpoints, model artifacts, or
results. The complete per-claim correction, train-only addition, and partition
drop mapping is emitted as `v1-to-v2-corrections.json`.

## Canonical annotation contract

- `negation` is the semantic scope. A negative claim uses the complete claim
  source; a non-negative claim has no negation span. Cue-only supervision is
  forbidden.
- An implicit first-person subject has `subject=null` and
  `subjectReferent=SPEAKER`. A declared name remains object/entity evidence.
- Every explicit temporal expression authored in the source has a temporal
  span. Tense without an explicit expression may remain spanless.
- Every row records the v1 lineage or an explicit v2 train-only augmentation
  lineage and the `SUPERVISOR_OPTION_A` migration policy.

## Frozen v2 checksums

| Dataset | Train | Dev | Frozen test |
|---|---|---|---|
| Matrix | `5118d37ce2ab19d5be171f757f448698085e3c222a4a627f9838329836185820` | `704e809f0e9ebace3a5c047989b74d354ac8811757a2644b0d9c04cfb0631012` | `458f79ecaa9ec547c53a55ba68c45531e88e0ae5a0d6ee405222632d85919228` |
| P0.5 | `413f60ca17879ed9de440add7903b6e2abaebdfbbed6055b32c6e0b105cadfcd` | `7533f56194431bd17b6f8544031d5436ca14ee6e209336da8133e1f05cdf0866` | `a729045ac17356321f2b8c6624554c8bf8ad22fd794e2c0718876734de0aabc2` |

Reproducible v1-to-v2 mapping SHA-256:
`c53ffb13f5b0ebdc15892a9b18890f3caa3c16347600c679c2ecfeab321fcbbc`.

The mapping records 1,322 claim corrections, 426 anti-leakage partition drops,
and 129 balanced IT/EN/ES train-only additions. The additions close label
coverage and add distinct-surface supervision for dev-observed semantic
families (negative scope, explicit temporality, consent, request/correction
and third-party referents) without copying held-out rows. Matrix train is now
2,775 observations / 3,615 claims, exactly 925 observations per language;
Matrix dev/frozen and every P0.5 split remain byte-identical to the original
v2 checkpoint.

## Pre-training gate

`audit_dataset_v2.py` validates schema and label vocabularies, source-contained
spans, annotation conventions, ownership/authority, World Truth prohibition,
lineage, manifests/checksums, train coverage, exact input contradictions,
surface overlap, and normalized semantic near-paraphrases at similarity 0.97.
Frozen content is read only for structural split isolation/checksums; model
predictions and frozen quality are not read and cannot guide training or
threshold selection.

Current deterministic result: 66/66 software tests green and all dataset-v2
audit failure counters equal zero.
