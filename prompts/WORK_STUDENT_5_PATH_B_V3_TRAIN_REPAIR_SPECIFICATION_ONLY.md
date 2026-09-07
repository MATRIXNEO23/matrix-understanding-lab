# SUPERVISOR GPT → CHATGPT WORK

Status: **SUPERVISOR-GPT ASSIGNMENT / OWNER-AUTHORIZED / DESIGN ONLY**  
Repository: `MATRIXNEO23/matrix-understanding-lab`  
Branch: `student5-path-b-v3`  
Starting HEAD: `e81a2ae9e1d60c6af61a7d8d1baabed9171f3166`  
Accepted predecessor: `CP37 / TRAIN_CURRICULUM = REPAIR_REQUIRED_BEFORE_TRAINING`

## Authority and reporting chain

```text
OWNER = Alberto / final project authority
SUPERVISOR GPT = planner, reviewer and acceptance authority
EXECUTOR = ChatGPT Work
```

This assignment is issued by **Supervisor GPT**.

Work is asked to **design** the repair. Work is NOT authorized to apply it.

---

# SINGLE ASSIGNMENT

## STUDENT-5 V3 TRAIN REPAIR SPECIFICATION ONLY

Convert the verified CP37 findings into a precise, conservative, reviewable repair specification for a future NEW TRAIN version.

The purpose is to let Supervisor GPT and Alberto decide exactly what should change **before any dataset mutation occurs**.

Do not create or modify the repaired TRAIN in this assignment.

---

# READ FIRST

1. `PROJECT_WORK_RULES.md`
2. `docs/WORK_CONTINUITY_STUDENT_5.md`
3. `docs/MATRIX_NLU_CONTRACT_V3.md`
4. `reports/STUDENT_5_TRAIN_CURRICULUM_AUDIT_CP37.md`
5. `reports/evidence/student5-path-b-cp37-train-audit/`
6. `reports/STUDENT_5_TRAIN_V3_MIGRATION.md`
7. persisted Student-4 regression/repair reports referenced by CP37, only as historical evidence

Do not read DEV or Frozen payloads.

---

# DESIGN PRINCIPLES

The repair must be conservative.

```text
PRESERVE VALID WORK
FIX CONFIRMED DEFECTS
ADD MISSING TEACHING WHERE REQUIRED BY V3
REDUCE HARMFUL REDUNDANCY WITHOUT DESTROYING USEFUL CONTRASTS
DO NOT INVENT NEW SEMANTICS OUTSIDE THE FROZEN V3 CONTRACT
DO NOT LOWER GATES
DO NOT USE DEV/FROZEN TO DESIGN TRAIN
```

`student5-matrix-nlu-v3-train-v1` remains immutable and must be treated as the preserved baseline.

Any future repaired dataset must be a NEW version with distinct ID/checksum/lineage. This task only specifies that future version; it does not create it.

---

# REQUIRED REPAIR SPECIFICATION

For every CP37 issue, classify it as one of:

```text
CONFIRMED_ANNOTATION_DEFECT
SEMANTIC_POLICY_NEEDS_SUPERVISOR_DECISION
MISSING_CURRICULUM_COVERAGE
LANGUAGE_IMBALANCE
ROLE/VIEWPOINT_IMBALANCE
TEMPORAL_IMBALANCE
REDUNDANCY/TEMPLATE_CONCENTRATION
NEGATION/POLARITY_CONTRAST_GAP
SPAN/ENTITY_COVERAGE_GAP
ADULT_INTIMACY_SEMANTIC_GAP
CODE_SWITCH_GAP
PLAUSIBLE_STUDENT4_REGRESSION_RISK
PRESERVE_AS_IS
```

For each item provide:

```text
issueId
classification
CP37 evidence/source row IDs or evidence path
why it matters to V3
what is actually wrong vs merely sparse
recommended minimal action
existing examples to preserve
existing examples proposed for correction/relabel/removal from a FUTURE version, if any
new example families that would be needed, if any
languages required
heads/fields affected
risk of overcorrection
Student-4 recurrence risk, if relevant
Supervisor decision required? true/false
```

Do not describe heuristic flags as confirmed defects unless CP37 actually established them.

---

# REQUIRED COVERAGE AREAS

The specification must explicitly disposition at least:

### Dialogue act / claim kind
- zero `COMMAND` support;
- zero `BELIEF` support;
- sparse `REQUEST` and `CORRECT`;
- sparse, IT-only `REPORT`;
- whether/how `UNKNOWN` teaching is needed without turning uncertainty into noise.

### Referents / ownership / viewpoint / source
- owner currently always equals subject;
- perspective currently always speaker;
- independent `sourceReferent` teaching;
- `source != perspective` cases;
- third-party report/belief examples;
- multiple context-entity choices;
- `UNKNOWN` / `AMBIGUOUS` role states;
- cases where subject, owner, target, source and perspective genuinely differ.

### Temporal
- extremely sparse `PAST`;
- zero `BEFORE`, `AFTER`, `DURING`, `RECURRENT`, `AT_REFERENCE`;
- all supervised anchors currently `speech-time`;
- explicit temporal-span defects already confirmed by CP37;
- future-worded goal/current adjudication cases;
- IT/EN/ES balance.

### Negation / polarity
- cue-only negation contract must remain distinct from composed polarity;
- include contrast teaching where cue presence does not mechanically imply NEGATIVE and cue absence does not mechanically imply POSITIVE;
- double-negation/uncertain composition where supported by V3;
- multilingual cue/span coverage;
- do not conflate Student-4 negation regression with proven Student-5 damage.

### Spans / entity / subject
- confirmed explicit-English subject-span inconsistencies;
- missing/malformed spans identified by CP37;
- multiword subject/person examples where semantically useful;
- multiple non-overlapping groups where the contract allows them;
- distinguish annotation defect from tokenizer artifact.

### Adult intimacy / consent
Keep semantics ordinary and first-class as required by V3. The repair spec must separate, where linguistically applicable:

```text
desire
request
consent grant
consent refusal
withdrawal / revocation
boundary statement
current desire vs consent wording
```

Do not introduce censorship or a moderation path. Do not treat adult wording itself as an error or confidence penalty.

### Code-switch / noisy language
- current 11 code-switch examples are too concentrated around `speech.unresolved`/desire-like wording;
- specify broader useful code-switch semantic families without using DEV/Frozen;
- preserve identical V3 semantics across IT/EN/ES/code-switch.

### Redundancy
- CP37 found substantial exact/normalized repetition/template concentration;
- distinguish useful repeated contrast from harmful oversampling/template shortcut;
- do not delete duplicates blindly;
- define a deterministic future dedup/downweight/selection policy proposal with provenance preserved;
- if proposing numeric limits or ratios, justify them from evidence and mark them as RECOMMENDATION, not an already-approved gate.

---

# ANNOTATION-REPAIR TABLE

Produce a dedicated table of all **confirmed or adjudication-required existing-row issues** found by CP37, including at least:

- confirmed missing explicit temporal spans;
- future-worded goal/CURRENT cases requiring temporal decision;
- report-perspective cases requiring adjudication;
- opinion-wrapper cases requiring adjudication;
- explicit-English-I subject-span inconsistency set;
- malformed double-participant request cases.

For each row/group, state one of:

```text
KEEP_UNCHANGED
CORRECT_IN_FUTURE_V2
REMOVE_FROM_FUTURE_V2
NEEDS_SUPERVISOR_SEMANTIC_DECISION
```

Do not apply any of these actions now.

---

# FUTURE DATASET VERSION DESIGN

Propose, but do not create, a future repaired dataset identity.

Preferred logical pattern:

```text
student5-matrix-nlu-v3-train-v2
```

If another naming/version scheme is materially better, explain why. Do not reuse or overwrite `student5-matrix-nlu-v3-train-v1`.

The specification must define future lineage metadata:

```text
baseDatasetId
baseDatasetSha256
repairSpecificationId
newDatasetId
new version reason
source provenance classes
changed-row manifest
added-row manifest
removed/deactivated-row manifest if any
per-file SHA256SUMS
ordered dataset SHA-256
contract fingerprint
language/family census
```

No actual v2 bytes are produced in this task.

---

# FUTURE REPAIR ACCEPTANCE CHECKS

Define the checks that a later repaired TRAIN candidate must pass before Supervisor GPT can accept it for controlled training.

They must include at least:

```text
all intended files/checksums valid
V3 contract fingerprint unchanged unless separately approved
no DEV/Frozen provenance
all changed rows explicitly justified
all added rows project-authored or otherwise properly provenanced
no contradictory gold for identical input/context unless explicitly intentional and documented
coverage census for all 16 conceptual heads
IT/EN/ES/code-switch census by semantic family
role/viewpoint/source independence demonstrated in TRAIN
COMMAND/BELIEF/REPORT/temporal advanced families no longer structurally absent if the Supervisor approves those additions
negation cue/polarity independence represented
adult consent/refusal/withdrawal/desire distinctions represented across approved languages
redundancy materially reduced without deleting meaningful contrasts
all CP37 confirmed annotation defects resolved or explicitly quarantined
all unresolved semantic-policy cases either Supervisor-decided or excluded from the future candidate
TRAIN v1 remains byte-identical and recoverable
```

Do not invent a universal semantic-accuracy percentage here. This is a TRAIN curriculum/structure acceptance specification, not model-performance evaluation.

---

# STUDENT-4 REGRESSION SAFEGUARDS

Using only persisted Student-4 reports already authorized by CP37, identify safeguards for a future repaired TRAIN against recurrence of documented weaknesses in:

```text
negation
temporal
referents/report
correction/request
ownership
span decoding
IT/ES performance
```

For each safeguard distinguish:

```text
DIRECTLY_SUPPORTED_HISTORICAL_FAILURE
PLAUSIBLE_RECURRENCE_RISK
NOT_ESTABLISHED_CAUSATION
```

Do not claim the Student-5 pristine model is damaged; no such evidence exists.

---

# FORBIDDEN IN THIS ASSIGNMENT

```text
NO TRAIN mutation
NO new TRAIN shards
NO data augmentation execution
NO row relabeling execution
NO row deletion execution
NO DEV read/create/migration
NO Frozen read
NO training
NO optimizer
NO backprop
NO fine-tuning
NO model loading for training
NO evaluator/decoder/threshold repair
NO quantization
NO Assembling integration
NO production promotion
NO Student-4 modification
NO Path A modification
NO pristine modification
NO overwrite of any artifact/version
NO automatic next step
```

Documentation/report/evidence produced by this design-only assignment may be committed. Existing data/model artifacts must remain unchanged.

---

# REQUIRED VERDICT

Return exactly one substantive verdict:

```text
REPAIR_SPECIFICATION = READY_FOR_SUPERVISOR_OWNER_REVIEW
```

or

```text
REPAIR_SPECIFICATION = BLOCKED_NEEDS_SUPERVISOR_DECISION
```

`READY_FOR_SUPERVISOR_OWNER_REVIEW` means the repair can now be reviewed by Supervisor GPT and Alberto before any mutation.

`BLOCKED_NEEDS_SUPERVISOR_DECISION` means some semantic decision cannot be safely specified from existing evidence/contract alone; list each decision precisely. Do not guess.

---

# REPORTING DISCIPLINE

Begin the final response exactly with:

```text
Supervisor GPT — Student-5 TRAIN Repair Specification Report
```

Then provide:

- verdict;
- concise executive summary;
- issue-by-issue repair table;
- annotation-repair table;
- proposed future dataset version/lineage;
- acceptance checks;
- Student-4 safeguards;
- unresolved decisions requiring Supervisor/Owner;
- files/commit/evidence produced;
- final branch HEAD.

Not acceptable as the only completion response:

```text
::SKIP_COMPLETION::
SKIP_COMPLETION
DONE
COMPLETED
empty/sentinel-only response
```

If the interface suppresses the user-visible report, persist the complete report in the repository before termination so Supervisor GPT can audit it.

After the report, STOP. Do not create the repaired dataset and do not start training.

— **Supervisor GPT**