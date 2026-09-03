# SENIOR SUPERVISOR EXECUTION PLAN — MATRIX ENGINE

Date: 2026-09-03
Status: CANONICAL SUPERVISION METHOD

## Purpose
Prevent wasted hours, architecture drift and destructive trial-and-error while building the complete Matrix Engine. Work receives bounded implementation checkpoints only after the supervisor has closed the technical design of that checkpoint.

## Roles
- User: product direction, visible behavior, final acceptance.
- ChatGPT supervisor: architecture, research, component selection, contracts, risk analysis, gate design, counter-review and integration authorization.
- Work: implementation, automated training, tests, benchmarks, builds, ordinary fixes and bounded tuning inside the authorized checkpoint.

## Core rule
Work may be autonomous inside a closed checkpoint, but must not make architecture-level decisions. Before Work is authorized to spend substantial time on a component, the supervisor must establish that the selected path has strong evidence of producing the required result.

## Mandatory Gate 0 before every component
The supervisor must close all of the following before implementation:
1. exact functional requirements and forbidden behaviors;
2. input/output contract and state ownership;
3. dependency graph and integration points;
4. strongest mature project/algorithm/library candidates;
5. Android/offline compatibility;
6. RAM/CPU/storage budget;
7. training-data availability and lawful provenance when training is involved;
8. zero-cost training route or a no-training alternative;
9. known failure modes and mitigations;
10. acceptance benchmark, adversarial cases and invariants;
11. rollback/canary strategy;
12. stopping conditions for experiments;
13. evidence that no cheaper/safer mature solution was overlooked.

If a material item is unresolved, Work must not begin a long implementation/training run. A short isolated risk-elimination experiment is allowed only when uncertainty cannot be removed analytically.

## Component order and closed design intent

### C1 — Matrix Understanding
Target: compact multilingual trained Matrix-NLU for IT/EN/ES, mobile export, near-perfect unseen generalization.
Learned: intent/dialogue act, predicate, spans/entities, negation, temporal signals, goals/requests/corrections, multi-claim signals.
Deterministic only: schema, authority/ownership, provenance, World Truth rules and structurally invalid-output rejection.
Training: automatic, resumable, free-only, provenance-tracked.
Canary: compare trained NLU against P0 Candidate B and frozen Matrix baseline before authority transfer.

### C2 — Typed Claim / Authority Contract
Target: one canonical contract consumed by every later component.
Must freeze WORLD_TRUTH, OBSERVATION, REPORT, BELIEF, INFERENCE, GOAL, COMMITMENT, RELATIONSHIP_STATE and EMOTION_STATE semantics before Memory implementation.
No LLM may directly mutate WORLD_TRUTH.

### C3 — Memory Authority
Target: Room/SQLite as one persistent authority; full history stays on disk.
Required operations: admission, correction/supersession, invalidation, provenance, time validity, actor/owner links, salience, confidence and retrieval metadata.
No second competing memory store.

### C4 — Memory Admission
Target: learnable classifier/ranker for ambiguous admission plus deterministic authority constraints.
Classes: IGNORE, EPISODIC, SEMANTIC, RELATIONSHIP, GOAL, CORRECTION.
Automatic training/evaluation only if lawful data and zero-cost compute are sufficient; otherwise use the strongest mature non-training alternative selected at Gate 0.

### C5 — Retrieval
Target: two-stage mobile retrieval.
Stage A: indexed filtering/FTS/entity/time/location/goal constraints.
Stage B: tiny learned or calibrated reranker using relevance, actor, recency, salience, emotion, goal, confidence, validity and novelty.
Embeddings/vector DB only if a frozen benchmark proves a meaningful gain that justifies footprint.

### C6 — Emotion / Relationship
Target: compact FAtiMA-inspired appraisal architecture, reimplemented/adapted for Matrix rather than importing a heavyweight runtime blindly.
Short-term emotions and persistent relationship state are separate.
Runtime must remain arithmetic/state-update heavy, not LLM-dependent.
Weights/ranking may be trained automatically if useful and free.

### C7 — Goals / Intentions / Agency
Target: Matrix BDI-lite informed by mature BDI systems such as Jason but without full AgentSpeak overhead unless benchmark proves it worthwhile.
Game actions come from a validated action catalog; a learned ranker may score feasible actions.
GGUF can express or suggest, never bypass action/state validation.

### C8 — Reflection / Belief Revision
Target: bounded triggered reflection, not continuous cognition.
Flow: retrieve evidence -> bounded reflection -> candidate insight/belief revision -> typed parsing -> provenance/confidence validation -> store or reject.
Reuse existing GGUF only; never load a second large reflection model.
Triggers include salience threshold, repeated conflict/pattern, relationship milestone, unresolved goal and scheduled consolidation.

### C9 — Scheduler / Catch-up
Target: event-driven foreground scheduler plus persisted due events and bounded catch-up on resume.
No continuous background cognition.
Dormant NPCs should consume near-zero inference CPU.

### C10 — NPC-NPC Autonomy
Target: three simulation levels.
L0 dormant: persisted schedule/state only.
L1 low-detail: deterministic/event simulation, no GGUF.
L2 high-detail: retrieval/appraisal/goals and bounded GGUF only for consequential encounters.
The same memory/emotion/agency contracts used for player interactions must be used for NPC-NPC interactions.

### C11 — GGUF Context / Rendering
Target: Matrix decides state/context; GGUF renders natural language and selected open-ended social content.
Token priority: scene/world facts -> active goals -> retrieved memories -> relation/emotion -> persona slice -> recent turns -> reflection insight.
Never send full memory/history.

### C12 — Full Matrix Core Integration
Integrate only green components through strangler/canary migration. Old production paths remain available until the replacement proves superiority and integration safety.

## Automatic training policy
For every learnable component:
`data/provenance -> frozen split -> training -> validation -> error mining -> hard examples -> retraining -> compression/export -> benchmark -> artifact/checksum`.

Requirements:
- 0 EUR training mandatory;
- user performs no manual annotation or hyperparameter selection;
- Work iterates ordinary training failures autonomously;
- frozen final test is never used for tuning;
- architecture change requires supervisor review.

## Automatic deterministic repair policy
For deterministic failures:
`failure -> minimal reproducer -> root-cause class -> candidate patch -> unit/property/regression/integration -> differential comparison -> accept/reject -> nearby regression generation`.

A patch is rejected when it merely fixes the target case while harming prior behavior or generalization. Structural deterministic changes require property/fuzz/mutation testing.

## Validation depth
Every deterministic component requires unit, edge, regression, integration and property tests. Critical parsers/resolvers also require fuzzing/mutation where practical.
Every learned component requires frozen unseen, language-split, adversarial, calibration/abstention and robustness testing.
Every stateful component requires replay, save/load, corruption/recovery, ordering, duplicate-event and long-sequence tests.
The ecosystem requires autonomous multi-NPC simulations, stochastic-seed sweeps where relevant, stress, soak/endurance, memory-growth and resource-budget tests.

## Anti-waste rules
- Never start a multi-hour training run before dataset/provenance, objective, metric and architecture have passed Gate 0.
- Never integrate two unverified new components simultaneously.
- Never debug a downstream component against an unstable upstream contract.
- Never replace a green baseline without canary/differential evidence.
- Never use phone testing to discover bugs reproducible in CI/JVM/emulator.
- Never repeat a failed experiment already documented in continuity unless a changed premise justifies it.
- Never chase a headline metric while hiding critical systematic failures.

## Checkpoints and rollback
Each component checkpoint must begin from a known green commit and end with:
- implementation commit(s);
- all required tests/benchmarks;
- human + machine-readable results;
- artifacts/checksums/provenance where applicable;
- continuity update;
- explicit PASS/FAIL;
- supervisor counter-review.

Production integration is forbidden until counter-review authorizes it.

## Continuity
`docs/WORK_CONTINUITY.md` is mandatory and must include branch/HEAD, canonical spec commit, active gate, completed experiments, current experiment/configuration, dataset/provenance, artifacts/checksums, green/red tests, failed approaches not to repeat, current blockers and exact NEXT ACTION.
Training should use resumable checkpoints whenever technically possible.

## Hardware budget — Moto G56
GGUF remains dominant. The cognitive stack excluding GGUF should normally target roughly 50–100 MB incremental PSS, preferably near the lower half.
- Matrix-NLU: target 25–45 MB; investigate above 60 MB.
- Room/SQLite/FTS + caches: 8–20 MB.
- emotion/goals/agency: 2–8 MB.
- scheduler: <5 MB.
- retrieval buffers: 5–15 MB.
- reflection transient context: 10–25 MB reused/bounded.
No second general-purpose LLM.

## Phone policy
Moto testing is late-stage only. Before it, CI/emulator/JVM must eliminate functional, training, regression, export and packaging failures. Final hardware probe measures PSS, CPU, NLU/retrieval/GGUF latency, thermals, catch-up and autonomous encounter cost.

## Supervisor decision principle
The supervisor does not send Work to discover an architecture by brute force. Research and comparison happen first. Work receives the highest-confidence design supported by evidence. Experiments are used only to resolve irreducible empirical uncertainty and must be bounded, isolated and reversible.

## Current Understanding status
The ongoing Matrix-NLU work is aligned with this plan and should not be stopped merely because this document is added. Existing resumable training, MASSIVE provenance, invariant decoder, end-to-end evaluator, abstention/calibration and authority property tests are reusable foundations for C1/C2. The current training run should continue unless a concrete Gate-0 violation or architecture-level blocker is identified.
