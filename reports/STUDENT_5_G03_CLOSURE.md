# Student-5 — G03 target preparation closure

G03 = PASS. Starting main: `8ee33811fde3aa9646a8d4eff1d5160c37ee76a4`.

The exact eight G03 rows pass. All annotations and all eight files in
`data/student5_v3_train_v21/` remain byte-identical. Final TRAIN remains
`student5-matrix-nlu-v3-train-v2.1-cp43r2`, SHA-256
`f90ae775a44023c37bf0c3a5087d64746413cbec770ca36cf154d1d533544aa4`.
No new candidate, manifest, BUILD_LOCK or provenance revision is necessary.

## Exact canonical adjudication

| Row ID | Subject | Owner | Target | Ordered ambiguous alternatives |
|---|---|---|---|---|
| mx-v22a-adult-it-015 | ctx:observer | ctx:speaker | UNKNOWN / AMBIGUOUS | target: ctx:observer, ctx:speaker |
| mx-v22a-adult-it-025 | ctx:observer | ctx:speaker | UNKNOWN / AMBIGUOUS | target: ctx:observer, ctx:speaker |
| cp42-it-ambiguous_binding-0117 | UNKNOWN / AMBIGUOUS | UNKNOWN / AMBIGUOUS | NONE / NOT_APPLICABLE | subject and owner: entity:adult-a, entity:adult-b |
| cp42-en-ambiguous_binding-0119 | UNKNOWN / AMBIGUOUS | UNKNOWN / AMBIGUOUS | NONE / NOT_APPLICABLE | subject and owner: entity:adult-a, entity:adult-b |
| cp42-es-ambiguous_binding-0121 | UNKNOWN / AMBIGUOUS | UNKNOWN / AMBIGUOUS | NONE / NOT_APPLICABLE | subject and owner: entity:adult-a, entity:adult-b |
| cp43-it-antecedent_ambiguous-0121 | UNKNOWN / AMBIGUOUS | UNKNOWN / AMBIGUOUS | NONE / NOT_APPLICABLE | subject and owner: entity:woman-a, entity:woman-b |
| cp43-en-antecedent_ambiguous-0124 | UNKNOWN / AMBIGUOUS | UNKNOWN / AMBIGUOUS | NONE / NOT_APPLICABLE | subject and owner: entity:woman-a, entity:woman-b |
| cp43-es-antecedent_ambiguous-0127 | UNKNOWN / AMBIGUOUS | UNKNOWN / AMBIGUOUS | NONE / NOT_APPLICABLE | subject and owner: entity:woman-a, entity:woman-b |

Concrete role pointers have status RESOLVED (the frozen V3 encoding of KNOWN).
Source and perspective remain ctx:speaker / RESOLVED for all eight.
D04 preserves the colloquial reflexive/reciprocal alternatives in the two
requests; D07 keeps requester ownership separate from action subject.
D06/D07 preserve the two explicitly equally salient antecedents in each
residence proposition. Residence location is object evidence; interpersonal
target is NONE. These are propositions with unresolved fields, not zero claims.
The supplied ranks are deterministic diagnostic order, not likelihood claims.

## Minimal production change

Only `matrix_nlu/training_data_v3.py` changes production behavior.
`role_supervision` reads each of the five roles independently and adds:

- `role_status_labels`: indices into unchanged Contract V3 FIELD_STATUSES:
  RESOLVED=0, UNKNOWN=1, AMBIGUOUS=2, NOT_APPLICABLE=3.
- `role_alternative_pointer_labels`: candidate pointer indices in annotated
  rank order, padded to max_referent_candidates with -100. Position i means
  diagnostic rank i+1; candidate order cannot replace annotation rank order.
- `role_alternative_mask`: 1 for a supplied alternative, 0 for padding.

Boundary examples use -100 status labels and entirely masked alternatives.
Ordinary legacy callers lacking explicit status retain literal inference:
candidate ID -> RESOLVED, NONE -> NOT_APPLICABLE, UNKNOWN -> UNKNOWN.
Alternatives require explicit status. Contradictory pointer/status, malformed
ranks, duplicate or missing candidates, overflow and ambiguity with fewer
than two distinct candidates fail closed. Existing primary pointer targets
remain UNKNOWN for ambiguity; the builder never selects an alternative.

The new fields are consumed and validated during target preparation and
materialized as numeric targets. They are not additional neural output heads,
calibrated confidence targets, soft probability distributions or an invented
ranking loss. V3 alternatives remain diagnostic. Future training preparation
must retain these fields alongside primary pointer targets; this task does
not execute a trainer or claim learned/calibrated behavior.

## Focused verification

28 unit/regression tests PASS: existing builder, inference and evaluator
synthetic checks, plus nine G03 tests. No DEV or Frozen payloads are loaded.
Tests exercise all five roles, KNOWN/NONE/UNKNOWN/AMBIGUOUS, ordered candidate
lookup, independent roles, unchanged input, zero claims and invalid inputs.

Mechanical compatibility and structural validation pass for 1,831 existing
observations, 2,524 claims and 4,355 prepared examples. All existing target
fields are exactly equal before/after, including G03 primaries. Their ordered
digest is `f6762dcfe070a8cc2b881405956628d948717e51da1c30e10fd689146cdbe9c1`.
The 14 ambiguous role fields contain 28 ordered alternatives. Status counts
are RESOLVED 10,269; UNKNOWN 3; AMBIGUOUS 14; NOT_APPLICABLE 2,334.

Two fresh target constructions are identical, SHA-256
`af211fb17bd802548128c324dbe794281b6407b9eadd744f63ffdba44340d5ed`.
This is a deterministic **target** rebuild. The unchanged dataset retains its
previous CP43 deterministic reproduction proof; it was not regenerated here.
The test tokenizer supplies lexical offsets only, with no model load.

## Evidence and reproduction

New evidence directory: `reports/evidence/student5-g03-closure/`.

- `eight-row-verification.json`: exact row IDs/hashes, text, context, semantic
  reason, canonical roles/status/alternatives, before/after targets and results.
- `verification.json`: complete focused totals, equality hashes and dataset locks.
- `training_data_v3.before.py`: exact starting builder for executable comparison.
- `unit-tests.txt`: results for the 28 tests.
- `source-integrity.json`: 20 pinned input Git blobs and original builder identity.
- `SHA256SUMS`: code and evidence integrity inventory.
- `remote-readback.json`: publication verification receipt, added after readback.

Reproduce without model or dataset generation:

```bash
python tools/student5_g03/verify.py --repo . --out /tmp/student5-g03-verification
cd matrix_nlu
python -m unittest test_training_data_v3 test_training_data_v3_g03 test_inference_v3 test_evaluate_v3 -v
```

Authoritative existing inputs used:

- `docs/MATRIX_NLU_CONTRACT_V3.md` (sections 4.6, 5, 8).
- `prompts/WORK_STUDENT_5_PATH_B_V3_CREATE_REPAIRED_TRAIN_V2_ONLY.md` (D01–D07).
- `reports/evidence/student5-train-v21-cp43/status-target-readiness.json`.
- `data/student5_v3_train_v21/train.jsonl.gz`, `manifest.json`, `BUILD_LOCK.json`.
- Existing `contract_v3.py`, `referent_candidates.py`, `inference_v3.py`,
  `evaluate_v3.py`, `synthetic_v3_fixtures.py` and the three existing test modules
  named above, all under `matrix_nlu/`.
- `docs/WORK_CONTINUITY_STUDENT_5.md` for the continuation record.

## Supervisor stop state

G03 is closed within the authorized target-preparation scope. G04 remains a
post-training evaluation requirement. G07 remains separately documented and
was not reopened. No general semantic/curriculum audit was launched.
No unresolved G03 item remains. No training is authorized by this report.

trainingExecuted=false
fineTuningExecuted=false
quantizationExecuted=false
onnxExecuted=false
nextWorkStarted=false

STOP. Await separate Supervisor FP32 training authorization.
