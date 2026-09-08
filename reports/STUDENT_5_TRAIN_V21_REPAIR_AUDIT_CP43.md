# CP43 — repaired TRAIN v2.1, dataset-only delivery

REPAIRED_TRAIN_AUDIT = BLOCKED

Repository: MATRIXNEO23/matrix-understanding-lab; main. Starting HEAD: 270a0729c20ede548fe373f488029241fcbb35a3. Final introducing commit and remote readback receipt are supplied after publication. The source CP42 TRAIN remains immutable.

REPAIRED_TRAIN_ID = student5-matrix-nlu-v3-train-v2.1-cp43r2

VERSION = CP43_REPAIR_2_AUDIT_LOCKED

REPAIRED_TRAIN_PATH = data/student5_v3_train_v21/

REPAIRED_TRAIN_SHA256 = f90ae775a44023c37bf0c3a5087d64746413cbec770ca36cf154d1d533544aa4

ORDERED_JSONL_SHA256 = 6d3b1c77c29c639c04956c480529edc7195f80182f422b51d08f5e38ef896ee4

OBSERVATIONS = 1831

CLAIMS = 2524

Source: student5-matrix-nlu-v3-train-v2 / CP42_BUILD_1_AUDIT_LOCKED, data/student5_v3_train_v2/, compressed SHA256 b6acf41e6634c2f89e6b8251fb5f816ec60fb0ca1cd6c90dfcbed46c2c12584c. Input is that exact candidate, not a reconstruction from TRAIN v1. D01–D07 were applied, never reopened.

The result is not authorized or ready for training. CP42_ISSUES_TOTAL=16; CP42_ISSUES_RESOLVED=13 in dataset scope; CP42_ISSUES_REMAINING=3. NEW_ISSUES_FOUND=1 during post-repair audit (N05, four missing temporal spans); NEW_ISSUES_REMAINING=0 after revision 2. No acceptance criterion was lowered.

## Material changes and preservation

Disposition ledger: {"PRESERVED": 1625, "CORRECTED": 75, "DEACTIVATED_EXACT_REDUNDANT": 1559, "QUARANTINED": 8, "NEWLY_AUTHORED": 131}. Language observations: {"en": 582, "es": 581, "it": 640, "code-switch": 28}. Every original one of 3,267 source row IDs is mapped, retained, aliased, or quarantined with original payload and hash. There are 1,625 semantically unchanged retained rows, 75 corrected retained rows, 1,559 redundant source rows aliased to retained equivalents, eight quarantined rows, and 131 new targeted rows. Corrections performed before deduplication are retained in before/after records even when the corrected row becomes an alias. These counts must not be confused with the CP42 builder's historical corrected-row counts.

- L01: repaired second not to [25,28), preserving first [6,9) and positive composed polarity; the old audit recommendation [24,27) was not applied.
- D01: all 39 identified rows individually accounted for. The 38 present-want/quiero/voglio goal constructions become CURRENT, with future action evidence preserved. The explicit future-want control remains FUTURE. No keyword-wide relabeling outside the exact reviewed set.
- C01/L04: identical Italian request counterparts now have the same target ambiguity and alternatives; requester owns requested goal. Explicit self-touch and own-body target refer to the addressee; no forced equality or inequality. Colloquial reciprocal/self readings remain genuinely ambiguous, with deterministic tie ordering of alternatives rather than invented confidence.
- L03: the 15 new CP42 directive/permission constructions were adjudicated and their independent owner/action-subject roles preserved; inconsistent inherited indirect-request owners were aligned case by case. Explicit English you subject spans restored in three new request/reflexive controls.
- L02: three composite hesitation statements quarantined intact because a unique safe flat decomposition was not established. Targeted single embedded uncertainty examples preserve UNKNOWN only for actual semantic uncertainty.
- Further exact-row review distinguished wanting/willingness from permission, affirmative refusal from negation, explicit stop command from assumed prior consent withdrawal, and corrected overly broad object evidence. Exact text, before/after field paths, reasons and source hashes are in repairs.json and the correction/mapping ledgers. No vocabulary is censored.
- 131 targeted authored additions broaden acts/kinds, genuine UNKNOWN, time/anchors, multiword/multiple spans, binding/role order, descriptions/slang/profanity/intimacy, code-switch across several semantic families, and zero-claim pauses. This is targeted coverage, not a balanced-percentage claim or generic-language expansion.
- KNOWN is represented as RESOLVED in frozen V3. NONE is NOT_APPLICABLE; unresolved UNKNOWN is distinct from AMBIGUOUS (UNKNOWN primary plus plausible alternatives). Dataset status consistency passes; consumer readiness is separately blocked by G03.

## Complete CP42 disposition register

| Issue | Original severity | Outcome | Evidence/action |
|---|---|---|---|
| C01 | HIGH | RESOLVED | No same-context conflicting gold remains; Italian pair adjudicated together. |
| C02 | MEDIUM | RESOLVED | Full semantic/context equality used for exact redundant reduction; originals and aliases retained. |
| C03 | MEDIUM | RESOLVED | Repeated concentration reduced; actual complement spans replace full-sentence objects in exact reviewed constructions. |
| C04 | MEDIUM | RESOLVED_REVIEW | Near pairs classified/preserved as contrasts or lexical/control variants; no similarity-score deletion. Remaining near pairs are disclosed below. |
| G01 | HIGH | RESOLVED | Every fixed class has support, including contextually justified act/kind/time UNKNOWN; no unfamiliar-word fallback. |
| G02 | HIGH | RESOLVED_DATASET_SCOPE | 131 targeted additions plus per-row semantic corrections; coverage does not prove learned generalization. |
| G03 | HIGH | REMAINING | Current production target builder does not consume statuses/ranked alternatives as dedicated target data. |
| G04 | MEDIUM | REMAINING | TRAIN preservation controls are not held-out evaluation. |
| L01 | HIGH | RESOLVED | Exact second-not cue fixed; full cue scan passes. |
| L02 | HIGH | RESOLVED_BY_QUARANTINE | Three original compound hesitation rows excluded intact; new single-proposition uncertainty coverage. |
| L03 | HIGH | RESOLVED | Natural owner/action-subject distinctions adjudicated; inherited inconsistencies corrected, valid equalities preserved. |
| L04 | HIGH | RESOLVED_DATASET_SCOPE | Grounded self/reflexive/companion/ambiguous alternatives with consistent owner conventions. |
| D01 | HIGH | RESOLVED | 38 present-desire repairs and one explicit future-desire preservation; exact IDs recorded. |
| G05 | MEDIUM | RESOLVED | Code-switch expanded beyond desire to description, request, command, negative preference, grant, refusal, withdrawal. |
| G06 | MEDIUM | RESOLVED | Multiword subjects and multiple subject/object/temporal groups now represented. |
| G07 | MEDIUM | REMAINING | Source allowlist verified; statistical overlap with unread DEV/Frozen is unverified, not asserted absent. |

`correction-register.jsonl.gz` enumerates every original affected row, including each C02/C04 row; `provenance-and-mapping.jsonl.gz` records every source/new row and every field-level before/after. Counts of overlapping issue groups are never added together as an error total.

## Redundancy before/after

| Measure | CP42 source | Repaired |
|---|---:|---:|
| Observations | 3267 | 1831 |
| Exact surface groups | 627 | 6 |
| Rows in exact surface groups | 2189 | 15 |
| Full semantic duplicate groups | 623 | 0 |
| Same-context conflicting groups | 1 | 0 |
| Near pairs, same-language trigram Jaccard ≥0.85 | 432 | 432 |
| Near-pair representative row IDs | 189 | 189 |
| Largest object/entity-masked template group | 36 | 16 |

624 exact-equality groups are reduced after adjudication (the original source had 623; adjudication resolves the conflicting pair into another equal group). 432 near pairs remain intentionally: similarity is not semantic redundancy. No claim that the near-pair count fell. The six remaining identical-surface groups have distinct antecedent/context teaching. A–F classifications, complete groups, representative IDs and equality hashes are persisted. Language is part of the equivalence key: multilingual equivalents are never collapsed across IT/EN/ES. Different literal values/spans/context/roles remain distinct. Role count and object variation are not quotas.

## Coverage and anti-shortcut evidence

Fixed heads: `{"dialogueAct": {"ASSERT": 2383, "QUESTION": 65, "REQUEST": 37, "COMMAND": 12, "CORRECT": 24, "UNKNOWN": 3}, "predicate": {"identity.name": 292, "identity.age": 441, "residence.place": 450, "presence.reported": 51, "preference.like": 560, "work.role": 104, "possession.has": 34, "goal.object": 465, "attribute.is": 72, "consent.grant": 26, "consent.refuse": 28, "speech.unresolved": 1}, "polarity": {"POSITIVE": 2047, "NEGATIVE": 417, "UNKNOWN": 60}, "temporalRelation": {"ATEMPORAL": 789, "CURRENT": 1429, "PAST": 18, "FUTURE": 252, "BEFORE": 6, "AFTER": 9, "DURING": 6, "RECURRENT": 6, "AT_REFERENCE": 6, "UNKNOWN": 3}, "claimKind": {"DIRECT": 2402, "REPORT": 29, "BELIEF": 18, "HYPOTHESIS": 72, "UNKNOWN": 3}}`.

Role equality/divergence: `{"ownerReferent=subjectReferent": 2482, "sourceReferent=perspectiveReferent": 2503, "perspective=speaker": 2495, "ownerReferent!=subjectReferent": 42, "perspective!=speaker": 29, "sourceReferent!=perspectiveReferent": 21}`.

Span support: `{"subject": {"positiveClaims": 779, "groups": 783, "multipleGroups": 4, "multiwordGroups": 6}, "object": {"positiveClaims": 2466, "groups": 2469, "multipleGroups": 3, "multiwordGroups": 1122}, "negation": {"positiveClaims": 299, "groups": 311, "multipleGroups": 12, "multiwordGroups": 0}, "temporal": {"positiveClaims": 286, "groups": 292, "multipleGroups": 6, "multiwordGroups": 133}, "entity": {"positiveClaims": 1230, "groups": 1391, "multipleGroups": 137, "multiwordGroups": 450}}`.

Anchors: `{"None": 792, "speech-time": 1705, "temporal:t0": 18, "context-reference": 6, "claim:c0": 3}`.

104 claim-family labels are represented. Explicit source/viewpoint/subject names are permuted across first/middle/last positions; equal-role reported desire controls coexist. Antecedent controls include unique-first, unique-last, and genuinely competing candidates; status-consumer/context readiness is not silently assumed. Positive corrected propositions contain no D05 discourse-negation cue. Desire, attraction, description, request, grant, refusal and withdrawal use explicit separate constructions. Explicit content does not automatically get UNKNOWN or negative polarity.

The full audit scans every stored row and claim for V3 invariants, bounds, flat-claim overlap, pointer/candidate integrity, anchors, statuses, alternatives, cue substrings, identity, provenance, census and redundancy; the existing pure target builder is exercised with diagnostic lexical offsets. It does not load pristine or claim real-tokenizer parity or model quality. Explicit semantic acceptance checks cover D01, D05, D06, D07, L01–L04, cross-claim anchors and multiple spans. This is full dataset-only auditing with bounded explicit semantic review, not a claim that software alone proves all language semantics.

## Remaining issues

- **G03 — HIGH — count=8**. Heads: fieldStatus, alternativesByField, subjectReferent, ownerReferent, targetReferent. Evidence: `matrix_nlu/training_data_v3.py; status-target-readiness.json`. Risk: Current consumer emits primary pointer/fixed targets, not explicit status/ranked alternatives; dataset repairs cannot establish calibrated ambiguity behavior. Action: Authorize a separate target/evaluation/calibration readiness task under frozen V3; do not train merely because dataset is structurally valid.
  Rows: `mx-v22a-adult-it-015`, `mx-v22a-adult-it-025`, `cp42-it-ambiguous_binding-0117`, `cp42-en-ambiguous_binding-0119`, `cp42-es-ambiguous_binding-0121`, `cp43-it-antecedent_ambiguous-0121`, `cp43-en-antecedent_ambiguous-0124`, `cp43-es-antecedent_ambiguous-0127`.
- **G04 — MEDIUM — count=1625**. Heads: all. Evidence: `preservation-and-controls.json`. Risk: TRAIN controls verify preservation but cannot establish held-out regression/generalization. Action: Retain separate authorized Gate-B evaluation requirement; no DEV examples added.
- **G07 — MEDIUM — count=0**. Heads: provenance. Evidence: `integrity.json`. Risk: Exact statistical disjointness from unread protected DEV/Frozen cannot be asserted. Source allowlist and byte identities are verified. Action: Only authorized data holder may later verify protected overlap without exposing training material.

G04's 1,625 IDs are complete in audit.json; G07 is a global verification limit, not zero detected contamination. The current task uses only authorized TRAIN inputs. Historical parent provenance is preserved verbatim, including older rationale strings referring to DEV-family generalization; these strings are not treated as proof of protected-data disjointness. No DEV/Frozen payload was read in this task.

Eight source rows are safely quarantined and remain available for Supervisor review: the three L02 adult_hesitation rows; mx-v22a-en-core-067 and -068 (ability/availability wrongly mapped to consent; V3 modality mapping unresolved); mx-v22a-adult-it-042, -045 and -048 (elliptical/refusal/readiness interpretation lacks necessary prior proposition or secure ontology mapping). The affected material is excluded, not replaced by guessed UNKNOWN or removed because of adult vocabulary. The eight full original payloads are separate QUARANTINED records; the same archive also contains 1,559 recoverable exact-redundancy deactivations with explicit distinct disposition.

## New post-repair issue and preserved first revision

N05, HIGH, four new code-switch rows: cp43-code-switch-cs_description-0099/-0100 and cp43-code-switch-cs_command-0103/-0104. Missing temporalEvidence for oggi/hoy/adesso/ahora. Risk: time cues would lack token supervision. It was found in an additional semantic scan after the first automated audit and corrected in revision 2 before delivery. Final audit has no unresolved new issue.

The entire first candidate, its original automated audit, sources and supplemental FAIL finding are retained under `reports/evidence/student5-train-v21-cp43-build1/`. Its original automated BLOCKED result was incomplete with respect to N05; SUPPLEMENTAL_AUDIT.json records effective FAIL. `revision2-semantic-diff.json` proves exactly four temporal-evidence changes and 1,827 unchanged semantic rows. Candidate identity/version and payload SHA changed; neither locked revision was overwritten. An early local path-normalization error happened before a BUILD_LOCK was created; it was corrected in builder setup and never represented as a completed candidate.

## Validation and persistence

STRUCTURAL_VALIDATION = PASS (0 errors; 0 target-builder exceptions)
DETERMINISTIC_REBUILD_MATCH = true (all 8 candidate files byte-identical, including gzip and BUILD_LOCK)
BUILD_LOCK_MATCH = true
MANIFEST_MATCH = true
PROVENANCE_MATCH = true
TRAIN_V1_UNCHANGED = true (baseline 130 Git identities; refreshed remote proof in receipt)
TRAIN_V2_SOURCE_UNCHANGED = true (all six original CP42 files)
DEV_USED_FOR_TRAINING = false
FROZEN_DATA_READ = false

Reproduction of the final candidate:

```text
python tools/student5_cp43/build.py --repo <pinned-repository-root> --out <new-empty-directory>
python tools/student5_cp43/build.py --repo <pinned-repository-root> --out <second-new-empty-directory>
python tools/student5_cp43/audit.py --repo <pinned-repository-root> --candidate <first-directory> --reproduction <second-directory> --out <new-empty-audit-directory>
```

Reproduction is an audit requirement of this assignment, not authorization for future training or rebuilding CP42. The builder refuses an existing candidate output directory. Source hashes in the manifest and delivery source inventory bind every input and script. The archived build1 sources can be restored into an isolated overlay of the same repository to reproduce its separate candidate; do not overwrite the final source scripts.

Canonical artifacts:

- data/student5_v3_train_v21/{train.jsonl.gz,provenance-and-mapping.jsonl.gz,correction-register.jsonl.gz,quarantine.jsonl.gz,exact-redundancy-decisions.json,manifest.json,BUILD_LOCK.json,SHA256SUMS}
- tools/student5_cp43/{repairs.json,authored.py,build.py,audit.py,DESIGN.md}
- reports/evidence/student5-train-v21-cp43/{audit.json,census.json,source-census.json,all-claims-review.jsonl.gz,duplicates-before.json,duplicates-after.json,semantic-invariants.json,status-target-readiness.json,preservation-and-controls.json,integrity.json,source-CP42-Supervisor-handoff.md,source-CP42-verified-findings.json.gz,train-v1-baseline-proof.json,SHA256SUMS}
- reports/evidence/student5-train-v21-cp43-build1/: complete superseded candidate/audit/sources plus supplemental finding and exact revision diff.
- reports/STUDENT_5_TRAIN_V21_REPAIR_AUDIT_CP43.md; docs/WORK_CONTINUITY_STUDENT_5.md.
- Remote receipt and complete delivery inventory are added after data-commit readback. Commits use [skip ci] to avoid the existing push-triggered P0 trainer; no workflow is dispatched.

```text
trainingExecuted=false
fineTuningExecuted=false
quantizationExecuted=false
onnxExecuted=false
student5PristineModified=false
postAuditTrainingStarted=false
nextWorkStarted=false
```

STOP after publication/readback. G03, G04 and G07 require Supervisor action; neither successful structural validation nor a future PASS would authorize training.

## Remote readback completed

Data commit: f9f237db57a178a77e263128441469ed132722eb. All 53 published files downloaded at that exact commit; SHA256, byte counts and Git blob identities match. Candidate SHA256 independently recalculated from remote bytes: f90ae775a44023c37bf0c3a5087d64746413cbec770ca36cf154d1d533544aa4. Manifest, BUILD_LOCK and every new-row provenance hash pass. All 130 v1 and six source v2 Git blobs unchanged; every pre-existing repository blob except the intended continuity update is unchanged. Workflow runs for data commit: 0. Receipt: reports/evidence/student5-train-v21-cp43/remote-readback.json. The receipt-only final commit SHA is supplied in the final handoff after its own readback. Candidate/source bytes are unchanged by that commit. STOP; no training or next task.
