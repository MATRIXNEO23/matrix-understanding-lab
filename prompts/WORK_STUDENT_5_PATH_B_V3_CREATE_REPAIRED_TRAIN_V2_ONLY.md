# SUPERVISOR GPT → CHATGPT WORK

Status: **SUPERVISOR-GPT ASSIGNMENT / OWNER-APPROVED / DATASET REPAIR ONLY**  
Repository: `MATRIXNEO23/matrix-understanding-lab`  
Branch: `student5-path-b-v3`  
Starting HEAD: `eef2682538dc91a5827bdd3eaff0be202f95a79e`  
Accepted predecessor: `CP38 / repair specification complete; semantic decisions approved by Owner + Supervisor`

## Authority

```text
OWNER = Alberto / final project authority
SUPERVISOR GPT = planner / reviewer / acceptance authority
EXECUTOR = ChatGPT Work
```

This assignment creates **only** a repaired TRAIN dataset version. It does not authorize training or Gate-B closure.

---

# SINGLE ASSIGNMENT

## CREATE AND VERIFY `student5-matrix-nlu-v3-train-v2` ONLY

Implement the conservative CP38 repair specification using the seven semantic decisions below. Preserve `student5-matrix-nlu-v3-train-v1` byte-for-byte and create a distinct v2 dataset with full provenance, change manifests, checksums and audit evidence.

Do not train a model in this assignment.

---

# READ FIRST

1. `PROJECT_WORK_RULES.md`
2. `docs/WORK_CONTINUITY_STUDENT_5.md`
3. `docs/MATRIX_NLU_CONTRACT_V3.md`
4. `reports/STUDENT_5_TRAIN_CURRICULUM_AUDIT_CP37.md`
5. `reports/STUDENT_5_TRAIN_REPAIR_SPECIFICATION_CP38.md`
6. `reports/evidence/student5-path-b-cp37-train-audit/`
7. `reports/evidence/student5-path-b-cp38-repair-spec/`
8. `reports/STUDENT_5_TRAIN_V3_MIGRATION.md`

Do not read DEV or Frozen payloads.

---

# OWNER + SUPERVISOR APPROVED SEMANTIC DECISIONS

These decisions are binding for v2 creation.

## D01 — present desire vs future desired action

```text
If the proposition is a person's present desire/state, temporalRelation = CURRENT.
Future timing of the desired action belongs to temporal/object evidence or downstream goal semantics when representable.
Use FUTURE only when the desire/commitment proposition itself is explicitly future-scoped.
```

Do not confuse time of wanting with time of the wanted action.

## D02 — perspective in reported propositions

```text
sourceReferent = linguistic attributor/source of the report.
perspectiveReferent = viewpoint holder only when the wording genuinely frames the embedded proposition from that person's viewpoint.
Do not mechanically copy sourceReferent → perspectiveReferent.
If viewpoint is not linguistically resolvable, use the contract's unresolved/UNKNOWN semantics rather than guessing.
```

## D03 — BELIEF vs DIRECT

```text
Use BELIEF when wording overtly encodes think/believe/opinion/mental stance as the evidential wrapper.
Use DIRECT for plain assertions, including subjective predicates, when no belief wrapper is linguistically expressed.
```

BELIEF is linguistic presentation, not downstream BeliefState.

## D04 — malformed/reflexive requests

```text
Genuinely malformed rows: quarantine/deactivate in v2; preserve provenance and original bytes/identity in v1.
Do not guess participant roles to rescue malformed gold.
Valid grammatical reflexive requests: annotate subject/target/owner according to actual semantics case-by-case and retain as useful contrasts.
```

## D05 — metalinguistic Spanish negation

```text
Annotate a negation cue only when it scopes over the atomic proposition represented by the claim.
A discourse/metalinguistic “No” used to correct prior wording does not mechanically make the corrected proposition NEGATIVE.
Preserve POSITIVE polarity when the corrected proposition itself is positive; use CORRECT dialogueAct and explicit scope evidence.
```

Cue presence and composed polarity remain independent.

## D06 — genuine no-claim observations

```text
Allow genuine zero-claim observations when the input contains no proposition supported by V3.
Use them as valid boundary-negative teaching examples.
Do not manufacture an unresolved claim merely to avoid an empty claim set.
Use UNKNOWN/abstention when a proposition exists but a critical field cannot be resolved.
```

## D07 — role-divergence teaching

```text
Add only semantically natural V3-compatible cases where ownerReferent != subjectReferent and/or sourceReferent != perspectiveReferent.
Do not force all roles to differ.
Do not create artificial identity divergence solely to balance counts.
Every divergence must be justified by the linguistic semantics of the authored TRAIN example.
```

---

# REPAIR EXECUTION RULES

Apply CP38 conservatively:

```text
PRESERVE VALID WORK
CORRECT CONFIRMED ANNOTATION DEFECTS
ADJUDICATE CP38 DECISION GROUPS USING D01-D07
ADD MISSING V3 TEACHING WHERE CP38 REQUIRES IT
BALANCE SEMANTIC FAMILIES ACROSS IT/EN/ES WITHOUT ARTIFICIAL QUOTAS
ADD CODE-SWITCH ONLY WHEN NATURAL AND SEMANTICALLY JUSTIFIED
REDUCE ONLY VERIFIED HARMFUL REDUNDANCY / EXACT-GOLD EQUIVALENCE
PRESERVE MEANINGFUL CONTRASTS
NO BLIND NEAR-DUPLICATE DELETION
NO KEYWORD-ONLY GOLD GENERATION
NO GATE LOWERING
```

### Existing-row repair

- Correct all confirmed annotation defects identified by CP37/CP38.
- Enumerate the full 628 explicit-English-`I` selector set before applying subject-span corrections; do not extrapolate from the 20 samples.
- Enumerate the full 404 implicit-first-person compliant selector set and preserve those valid implicit-subject cases.
- Correct the 6 confirmed temporal-span omissions.
- Apply D01 to the 23 present-desire/future-action cases.
- Apply D02 to the 8 reported-proposition viewpoint cases.
- Apply D03 to the 6 opinion-wrapper cases.
- Apply D04 to the 6 malformed participant requests and 3 grammatical reflexive requests separately.
- Apply D05 to the Spanish metalinguistic-negation case.
- Preserve the 8 CP37 negation-screen false positives unchanged for the affected field.
- Re-evaluate the 11 code-switch desire cases individually; do not blanket-map them.

### Missing teaching to add

Build targeted, project-authored TRAIN-only examples covering at minimum:

```text
dialogueAct: COMMAND, REQUEST, CORRECT, QUESTION, ASSERT contrasts
claimKind: BELIEF, REPORT, DIRECT, HYPOTHESIS contrasts
temporal: PAST + BEFORE/AFTER/DURING/RECURRENT/AT_REFERENCE where contract-valid
roles: source/perspective independence; owner/subject independence; multiple candidate choices
field status: linguistically motivated UNKNOWN / AMBIGUOUS / unresolved cases
boundary: genuine zero-claim examples per D06
negation: cue/polarity independence, including cue-free negative semantics and multi-cue/double-negation contrasts
spans: explicit/implicit subject, multiword/multiple spans where semantically natural
adult semantics: desire/request/consent/refusal/withdrawal/boundary distinctions without censorship or adult-word penalty
IT / EN / ES semantic parity
natural code-switch cases across more than one semantic family
```

Do not introduce semantics outside the frozen V3 contract.

---

# VERSIONING / LINEAGE

Create a NEW dataset identity only:

```text
logicalId = student5-matrix-nlu-v3-train-v2
suggested path = data/student5_v3_train_v2/
base = student5-matrix-nlu-v3-train-v1
base SHA = 1118a900026f48cfcc290c3f9dc52a1a019a6a1f4761661f326c33770523140e
contract = MATRIX_NLU_CONTRACT_V3
contract fingerprint = 7b0646e44243ad897760c0fcadbe141f1b8e88e3fd8d63a1789106571b9987b0
```

Required persistent metadata:

- dataset manifest;
- provenance for every v2 row;
- explicit `UNCHANGED / CORRECTED / ADDED / DEACTIVATED` disposition manifest;
- old→new row/claim lineage for corrected rows;
- deactivation reason for quarantined malformed rows;
- aliases/source IDs for deduplicated exact-equivalent rows;
- per-file SHA256SUMS;
- ordered logical dataset SHA-256;
- language/family/head census;
- change counts by repair-card/decision D01-D07;
- exact source HEAD and generated-data script/config identities.

V1 remains immutable and recoverable. Never overwrite, rename or delete it.

---

# REQUIRED VALIDATION BEFORE PASS

Run a **dataset-only** verification suite after creating v2.

At minimum prove:

1. v1 remains byte-identical and canonical SHA unchanged.
2. v2 schema/contract validation = 100% PASS for all stored rows/claims.
3. every modified/deactivated/added row has explicit provenance and reason.
4. no DEV/Frozen source/provenance appears in v2.
5. all CP37 confirmed defects targeted by this assignment are either fixed or explicitly BLOCKED with row IDs/reason.
6. all seven semantic decisions are applied consistently; provide concrete examples from v2.
7. COMMAND and BELIEF have non-zero, linguistically valid support.
8. REPORT, REQUEST, CORRECT, PAST and advanced temporal support is no longer pathologically one-language/one-template where the specification requires repair.
9. perspective/source and owner/subject are no longer artificially collapsed everywhere, while valid equal-role examples remain.
10. UNKNOWN/AMBIGUOUS/no-claim teaching exists only for linguistically justified cases.
11. adult semantics remain ordinary first-class semantics; no adult-term penalty/filter/censorship introduced.
12. exact duplicate/equivalence handling is deterministic and preserves aliases/provenance; near-duplicate similarity alone never deletes data.
13. IT/EN/ES and code-switch census is reported by semantic family, not merely total language count.
14. target builder can consume all v2 rows without violations.
15. no model training/load, optimizer, backprop or learned-quality claim occurred.

Do not invent a numeric model-quality claim from dataset counts.

---

# HARD FORBIDDEN SCOPE

```text
NO model training
NO optimizer
NO backprop
NO fine-tuning
NO model-weight change
NO DEV read/create/migration/modification
NO Frozen read/evaluation/modification
NO evaluator/decoder/threshold/calibration repair
NO quantization
NO ONNX export work
NO Assembling integration
NO production promotion
NO Student-4 modification
NO pristine modification
NO Path-A modification
NO TRAIN v1 modification
NO automatic next task
```

If a required repair cannot be completed without DEV/Frozen, evaluator changes, contract changes or a new semantic decision not covered by D01-D07, stop that item and report it as BLOCKED rather than guessing.

---

# FINAL VERDICT

Return exactly one substantive verdict:

```text
TRAIN_V2_REPAIR = PASS
```

or

```text
TRAIN_V2_REPAIR = BLOCKED
```

`PASS` means only that the repaired TRAIN v2 is structurally and pedagogically ready for **Supervisor review**. It does NOT authorize training because CP36 Gate-B DEV/evaluator/calibration blockers remain separate.

Required final report begins exactly:

```text
Supervisor GPT — Student-5 TRAIN v2 Repair Report
```

Report at minimum:

- starting/final branch HEAD;
- v1 immutable verification;
- v2 logical ID/path/rows/claims/checksum;
- counts UNCHANGED/CORRECTED/ADDED/DEACTIVATED;
- D01-D07 application summary;
- per-head/family/language census;
- duplicate/redundancy disposition;
- validation results;
- DEV/Frozen read=false proof;
- training=false proof;
- remaining blockers;
- report/evidence/manifest paths.

No `::SKIP_COMPLETION::`, sentinel-only, `DONE` or silent stop is acceptable.

After PASS/BLOCKED, stop and await Supervisor GPT.

— **Supervisor GPT**
