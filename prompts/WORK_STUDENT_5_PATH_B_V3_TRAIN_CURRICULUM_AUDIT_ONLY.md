# SUPERVISOR GPT → CHATGPT WORK

Status: **SUPERVISOR-GPT ASSIGNMENT / OWNER-AUTHORIZED AUDIT**  
Repository: `MATRIXNEO23/matrix-understanding-lab`  
Branch: `student5-path-b-v3`  
Reference accepted audit HEAD: `2904edb04cac52eb7cca677f10e0e36842e8e6e2`  
Predecessor checkpoint: `CP36 / GATE_B_READINESS = BLOCKED`

## Authority and reporting chain

```text
OWNER = Alberto / final project authority
SUPERVISOR GPT = project supervisor, technical planner and acceptance authority
EXECUTOR = ChatGPT Work
```

This is a single bounded audit issued by Supervisor GPT.

Work must not redesign the training strategy, create new data, fix the evaluator, create a DEV set, or start training. The purpose is to give Supervisor GPT hard evidence about whether the current immutable TRAIN V3 teaches the intended Matrix-NLU V3 behavior coherently and safely.

---

# SINGLE ASSIGNMENT

## STUDENT-5 V3 TRAIN CURRICULUM AUDIT ONLY

Answer this question with repository-backed evidence:

> Is `student5-matrix-nlu-v3-train-v1` pedagogically coherent and sufficiently targeted for the 16-head Matrix-NLU V3 model, or would training it now predictably teach gaps/imbalances that risk reproducing Student-4-style regressions?

This is **not** a structural checksum audit. CP36 already proved TRAIN integrity. This audit is about **what the dataset teaches**.

---

# REQUIRED AUDIT

Audit the immutable TRAIN V3 dataset read-only against:

- `docs/MATRIX_NLU_CONTRACT_V3.md` and its frozen fingerprint;
- the accepted 16 conceptual heads / 17 output tensors;
- the owner-approved target semantics for IT/EN/ES;
- documented Student-4 v2/v2.1/v2.2A failure and repair history, read-only, solely to identify regression patterns that Student-5 must not repeat;
- TASK 2.3 migration/provenance evidence.

Do not use DEV or Frozen payloads.

## 1. Per-head curriculum coverage

For every V3 head, report label/value distribution and effective supervised support.

Token heads:

```text
boundary
object
subject
negation
temporal
entity
```

Sequence heads:

```text
dialogueAct
predicate
subjectReferent
targetReferent
ownerReferent
perspectiveReferent
sourceReferent
polarity
temporalRelation
claimKind
```

Identify:

- labels/classes with zero examples;
- critically rare labels/classes;
- highly dominant classes likely to encourage trivial/default prediction;
- heads where nominal row count overstates real positive supervision;
- language skew inside each important class.

## 2. Semantic-family coverage

Quantify IT / EN / ES / code-switch coverage for at least:

```text
negation
simple temporal
advanced temporal relations
subject/target referents
owner
perspective
source != perspective
third-party/report
belief
hypothesis
request
genuine command
correction
goal/desire
preference
entity/span decoding
multi-claim
ambiguity / unresolved / abstention
adult consent
adult refusal
adult withdrawal/revocation
adult desire/arousal statements
ownership-sensitive statements
```

Do not merge semantically distinct families merely to make counts look healthy.

## 3. Dataset pedagogy / quality hazards

Check, read-only:

- repeated exact surfaces and repeated semantic templates;
- near-duplicate concentration where it can dominate gradients;
- label contradictions or same/similar surface with incompatible gold without a justified context distinction;
- migration artifacts from V2 that may preserve V2 semantics incompatible with V3;
- synthetic/template regularities that could let the model shortcut instead of learning semantics;
- examples where source/owner/perspective can be guessed from position rather than meaning;
- imbalance that could damage capacities already present in the pristine multilingual encoder;
- whether cue-only negation semantics are consistently represented;
- whether explicit temporal spans are represented consistently when required;
- whether first-person implicit-subject semantics follow the approved rule consistently.

Do not modify or deduplicate the dataset in this task.

## 4. Student-4 regression comparison

Using only existing documented Student-4 evidence/history, identify which known Student-4 weaknesses could plausibly recur under the current Student-5 TRAIN curriculum.

At minimum compare:

```text
negation
temporalità
referenti
third-party/report
correction
goal/request
ownership
span decoding
IT/ES weakness
source/perspective if applicable to V3
```

Do not infer causation where historical evidence does not prove it. Classify each linkage as:

```text
DIRECTLY_SUPPORTED
PLAUSIBLE_RISK
NOT_ESTABLISHED
```

## 5. Teaching-quality verdict

Return one of:

```text
TRAIN_CURRICULUM = FIT_FOR_CONTROLLED_TRAINING
```

or

```text
TRAIN_CURRICULUM = REPAIR_REQUIRED_BEFORE_TRAINING
```

`FIT_FOR_CONTROLLED_TRAINING` does NOT mean Gate B PASS; CP36 DEV/evaluator blockers remain separate.

`REPAIR_REQUIRED_BEFORE_TRAINING` must identify the minimal TRAIN-only repair categories needed, but **must not create or modify data** in this assignment.

---

# HARD GUARDS

```text
NO training
NO optimizer
NO backprop
NO fine-tuning
NO model-weight changes
NO augmentation
NO TRAIN mutation
NO DEV read
NO DEV creation/migration
NO Frozen read
NO evaluator/decoder repair
NO threshold/calibration repair
NO quantization
NO Assembling integration
NO Student-4 modification
NO pristine modification
NO Path A modification
NO overwrite of any artifact/version
```

Student-4 may be inspected read-only only through already-persisted reports/docs/evidence needed for comparison.

If some historical Student-4 evidence needed for a claim is unavailable, report `NOT_ESTABLISHED`; do not invent a causal explanation.

---

# REQUIRED PERSISTENT OUTPUT

Create a substantive report and machine-readable evidence under a new CP37 identity, without overwriting CP36.

At minimum persist:

```text
reports/STUDENT_5_TRAIN_CURRICULUM_AUDIT_CP37.md
reports/evidence/student5-path-b-cp37-train-audit/
```

Include reproducible scripts/commands when they add objective evidence, plus checksums for new evidence.

Update `docs/WORK_CONTINUITY_STUDENT_5.md` with:

- starting/final HEAD;
- exact audit verdict;
- confirmed coverage gaps;
- Student-4 regression-risk mapping;
- explicit statement that TRAIN/DEV/Frozen/model bytes were not modified;
- exact next disposition = return to Supervisor GPT, no follow-on work.

---

# REPORT TO SUPERVISOR GPT

Final user-visible response must begin exactly:

```text
Supervisor GPT — Student-5 TRAIN Curriculum Audit Report
```

Then state:

```text
TRAIN_CURRICULUM = FIT_FOR_CONTROLLED_TRAINING
```

or

```text
TRAIN_CURRICULUM = REPAIR_REQUIRED_BEFORE_TRAINING
```

Summarize only the decisive findings, evidence paths, resulting HEAD, and whether any files outside new audit evidence/continuity changed.

The following are NOT acceptable final responses:

```text
::SKIP_COMPLETION::
SKIP_COMPLETION
DONE
COMPLETED
empty/sentinel-only response
```

A sentinel is NON-COMPLIANT. If the interface internally emits one, the full substantive report must still be persisted in repository evidence/continuity before termination so Supervisor GPT can audit it.

Do not stop silently.
Do not begin remediation.
Do not begin Gate B evaluator/DEV work.
Do not begin training.

Return the audit to Supervisor GPT and wait.

— **Supervisor GPT**