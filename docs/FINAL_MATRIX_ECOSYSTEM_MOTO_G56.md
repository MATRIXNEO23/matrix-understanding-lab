# FINAL MATRIX ECOSYSTEM — MOTO G56 OPTIMIZED

Date: 2026-09-03
Status: CANONICAL HARDWARE-OPTIMIZED BLUEPRINT

## Target
Build the complete Matrix Engine for the Moto G56 with offline operation, IT/EN/ES, near-perfect practical Understanding, coherent persistent memory, emotions/relationships, reflection, autonomous NPC-NPC interaction, local GGUF dialogue, automatic/free training where learning is useful, and minimal manual phone testing.

## Hard hardware strategy
The GGUF remains the dominant RAM consumer. Everything else must be engineered to stay small, event-driven and mostly disk-backed.

Target incremental PSS excluding GGUF:
- Matrix-NLU runtime + model: 25–45 MB target, 60 MB warning ceiling;
- Room/SQLite/FTS + active caches: 8–20 MB;
- emotion/relationship/goal/agency state: 2–8 MB;
- scheduler/event queue: <5 MB;
- retrieval/ranking working buffers: 5–15 MB;
- reflection temporary context: bounded and reused, 10–25 MB transient;
- total Matrix cognitive stack target: about 50–100 MB incremental PSS excluding GGUF, with a design goal near the lower half during ordinary dialogue.

No second general-purpose LLM is allowed for NLU, memory, emotion or agency.

## CPU strategy
No continuous cognition loops.

Per-user-turn flow is bursty:
1. NLU inference;
2. indexed memory retrieval;
3. appraisal/goal ranking;
4. one GGUF generation when needed;
5. write-back.

NPC autonomy is event-driven. Only NPCs affected by an event are activated. Inactive NPCs consume effectively no inference CPU.

Reflection runs only on triggers and with a strict per-frame/per-turn budget. Heavy reflection is deferred until after immediate UI response.

## 1. Understanding
Architecture:
`text -> compact multilingual Transformer -> Matrix multi-task heads -> TypedClaims`

Deployment:
- ONNX Runtime Mobile;
- INT8 when quality loss is negligible;
- one shared model for IT/EN/ES;
- no OpenNLP model set in final runtime if Matrix-NLU wins;
- tokenizer/model loaded once and reused.

Model-selection rule:
choose the smallest compact multilingual encoder that reaches near-perfect unseen quality after Matrix fine-tuning. Do not choose by popularity.

Training is automatic and free-only. If the chosen encoder cannot be trained within free compute, switch to a lighter encoder/training recipe rather than requiring paid compute.

## 2. World and belief authority
One typed state contract with WORLD_TRUTH, OBSERVATION, REPORT, BELIEF, INFERENCE, GOAL, COMMITMENT, RELATIONSHIP_STATE and EMOTION_STATE.

Only game-state events can create/modify WORLD_TRUTH. Language models never mutate canonical state directly.

This module is deterministic and tiny.

## 3. Memory
Primary storage: Room/SQLite + FTS.

Do not keep full NPC memory in RAM.

In RAM keep only:
- current conversation working set;
- top retrieved memories;
- compact relationship/emotion state;
- active goals;
- small LRU metadata cache.

Everything else stays on disk.

Memory records include owner, entities, type, timestamp, validity, provenance, confidence, salience, emotional weight, status and optional links.

## 4. Memory admission
Use a tiny trainable classifier/ranker for ambiguous admission decisions, while hard authority/provenance rules remain deterministic.

Outputs:
IGNORE / EPISODIC / SEMANTIC / RELATIONSHIP / GOAL / CORRECTION.

Training/evaluation/retraining is automatic from labeled Matrix scenarios and synthetic variants.

## 5. Retrieval
Two-stage retrieval optimized for mobile:

Stage A — cheap candidate generation:
- entity/actor indexes;
- time/location filters;
- active-goal filters;
- FTS text search.

Stage B — tiny reranker:
features = relevance + actor + recency + importance + emotion + active-goal + confidence + validity + novelty.

Optional embeddings are allowed only if they materially improve recall after benchmark. No vector DB.

Return a small top-K set only, normally 6–12 memories per reasoning/generation step.

## 6. Emotions and relationships
Implement a compact FAtiMA-inspired appraisal core in Kotlin/Java, not the full framework runtime.

Persist only compact state vectors per NPC/relationship.

Short-term emotion vectors decay over time; persistent relationship dimensions update from evaluated events.

Weights/mappings may be trained/tuned automatically offline using scenario preference data. Runtime is simple arithmetic and state updates, so RAM/CPU cost is negligible.

## 7. Goals and agency
Implement Matrix BDI-lite, not a full AgentSpeak interpreter.

Each NPC stores only:
- active beliefs relevant to current context;
- active goals;
- one/few committed intentions;
- bounded action candidate list.

Action catalog is deterministic for game-world actions. A tiny learned ranker can score feasible actions from context/personality/emotion/goal features.

The GGUF may propose social/dialogue content, but cannot bypass legal action/state validation.

## 8. Reflection
Reflection is not always-on.

Triggers:
- salient event threshold;
- repeated pattern/conflict;
- relationship milestone;
- unresolved-goal threshold;
- scheduled low-frequency consolidation.

Flow:
`retrieve small memory bundle -> bounded GGUF reflection prompt -> parse into candidate claims -> validate provenance/confidence -> store insight or belief revision`

Reuse the already-loaded GGUF; never load another reflection model.

Reflection has a hard token/context budget and is deferred when immediate dialogue latency matters.

## 9. NPC-NPC autonomy
Only simulate consequential NPCs at high detail.

Three levels:

L0 dormant:
no inference, only persisted schedule/state.

L1 low-detail simulation:
deterministic schedule/event transitions and compact relationship effects; no GGUF call.

L2 high-detail encounter:
activate retrieval/appraisal/goals and, only when dialogue or nuanced social action matters, one or more bounded GGUF generations.

Use L2 only for NPCs/events relevant to the current world/story/player vicinity or major relationships.

This allows many NPCs without multiplying LLM cost.

## 10. Scheduler
Foreground event-driven scheduler only.

When app is closed, persist next due events and world checkpoint. On resume, compute elapsed time and run bounded catch-up simulation.

Do not maintain continuous background NPC cognition.

Reflection, NPC conversations and expensive events are queued and budgeted.

## 11. GGUF context packing
Never send full memory/history.

Context priority:
1. current scene/world facts;
2. active goal/intention;
3. top retrieved memories;
4. relationship/emotion state;
5. relevant persona slice;
6. recent turns;
7. optional reflection insight.

Use token-aware packing and hard budgets.

## 12. Automatic training ecosystem
Every learnable component gets an automatic free-only pipeline:

### Matrix-NLU
multilingual data -> Matrix labels -> train/dev/frozen test -> training -> adversarial mining -> retraining -> quantization -> ONNX -> benchmark.

### Memory admission
scenario events -> gold admission class -> train tiny classifier -> regression/adversarial -> artifact.

### Retrieval reranker
query-memory relevance pairs -> ranking training -> frozen retrieval benchmark -> artifact.

### Emotion/appraisal tuning
scenario preference pairs -> optimize weights/ranker -> trajectory validation.

### Action ranking
state/action preference pairs -> train tiny ranker -> simulated trajectories -> regression.

Training cost policy: 0 EUR mandatory. If a candidate requires paid GPU/service, switch model/training strategy.

## 13. CI and self-continuity
Work must maintain `docs/WORK_CONTINUITY.md` after each meaningful checkpoint/training/benchmark and before any likely stop.

CI must automatically produce:
- unit/integration/regression tests;
- frozen NLU benchmark;
- memory admission benchmark;
- retrieval benchmark;
- emotion/trajectory benchmark;
- autonomous NPC simulation benchmark;
- model artifacts/checksums/provenance;
- Android APK/probe;
- size breakdown;
- failure summary.

Work continues autonomously through ordinary failures and tuning until the current gate is met or a true architecture-level blocker is proven.

## 14. Phone testing policy
The Moto is a late hardware gate only.

Before phone testing, CI/emulator must prove functional correctness, quality, packaging and artifact reproducibility.

One final probe should measure:
- total PSS and delta vs baseline;
- CPU bursts and idle CPU;
- NLU latency;
- retrieval latency;
- GGUF end-to-end latency;
- thermal loop;
- catch-up simulation cost;
- autonomous NPC encounter cost.

## 15. Final end-to-end pipeline

`PLAYER/NPC/WORLD EVENT`
-> `Matrix-NLU`
-> `Typed Claims`
-> `Authority/Belief Resolver`
-> `Memory Admission`
-> `Room/SQLite Memory`
-> `Hybrid Retrieval`
-> `Appraisal + Relationship`
-> `Goals/Intentions`
-> `Reflection if triggered`
-> `Action Selection`
-> `NPC/NPC or NPC/Player interaction`
-> `GGUF language rendering only when needed`
-> `validated event/state update`
-> `memory write-back`
-> `scheduler`

## 16. Final implementation order
1. Finish Matrix-NLU training/export.
2. Freeze canonical TypedClaim/authority contract.
3. Implement Room/SQLite memory + admission.
4. Implement hybrid retrieval + tiny reranker.
5. Implement FAtiMA-inspired emotion/relationship core.
6. Implement Matrix BDI-lite goals/intentions/action ranking.
7. Implement bounded reflection using the existing GGUF.
8. Implement event scheduler/catch-up.
9. Implement 3-level NPC autonomy and NPC-NPC interaction.
10. Integrate token-aware GGUF context/rendering.
11. Run full autonomous simulations in CI.
12. Perform one final Moto hardware gate.

## 17. Maximum-depth validation strategy
Validation is a first-class subsystem of Matrix, not a final checklist. Every deterministic, learned and generative component must have its own oracle strategy, regressions and cross-module tests. A component is not considered complete because a happy-path benchmark passes.

### 17.1 Deterministic contract tests
For every deterministic module and every substantial deterministic change, automatically require:
- unit tests for the complete public contract;
- boundary and pathological inputs;
- null/empty/duplicate/out-of-order data;
- invariant and property tests;
- regression tests for every previous bug;
- integration tests with every directly connected module;
- serialization/deserialization round trips;
- deterministic replay from the same seed/state;
- idempotency tests where applicable;
- state-machine transition coverage;
- migration/backward-compatibility tests for persisted state.

CI must block on any deterministic regression.

### 17.2 Automatic deterministic repair
Deterministic corrections are automatic by default.

When a deterministic regression, invariant failure or integration divergence is detected, Work must run an autonomous repair loop:

`failure -> minimal reproducer -> root-cause classification -> candidate patch generation -> unit/property/regression/integration suite -> differential comparison -> accept/reject -> repeat`

Rules:
- never patch by test ID or exact test string;
- prefer general invariant/contract fixes over local branches;
- generate at least one neighboring regression/property case for every accepted fix;
- reject any patch that improves the target failure but causes a previous deterministic regression;
- preserve deterministic replay and serialization compatibility unless the migration is intentional and tested;
- record rejected patch attempts so they are not repeated;
- continue autonomously through ordinary repair cycles without asking the user;
- if several candidate fixes are valid, select the one with lower complexity, lower runtime cost and wider contract correctness;
- use differential testing against the previous verified commit and, where available, against a trusted reference implementation;
- run mutation/property/fuzz tests after structural fixes to detect overfitting to known cases.

A deterministic module is not considered repaired until the complete deterministic and integration suite is green.

### 17.3 Matrix-NLU maximum benchmark
The final NLU benchmark must be large, frozen, genuinely unseen and adversarial, with separate IT/EN/ES reporting and Italian primary weighting.

Required families include:
- identity vs attribute ambiguity;
- subject/object/reference resolution;
- pronouns and pro-drop;
- multi-entity and multi-claim utterances;
- negation, double negation and scoped negation;
- corrections and self-corrections;
- hypotheses and uncertainty;
- request/command/question/goal/preference distinctions;
- temporal expressions, tense and relative time;
- location/time lexical collisions;
- typos, missing accents, punctuation noise and ASR-like errors;
- slang, colloquial abbreviations and incomplete sentences;
- code-switch IT/EN/ES;
- long user messages and claim-density stress;
- third-party reports and nested belief attribution;
- romantic, sensual, erotic and sexually explicit adult-domain language;
- consent, refusal, hesitation, change of mind and escalation/de-escalation among adults;
- paraphrase families that share meaning but not surface form;
- minimal pairs differing in exactly one semantic feature.

Metrics must include field exact, exact claim set, entity/span F1, predicate/intent accuracy, negation F1, temporal accuracy, ownership/authority violations, invented World Truth, calibration/abstention quality and worst-language performance.

No tuning may use the final frozen test set.

### 17.4 Learned-component robustness
Memory admission, retrieval reranking, appraisal tuning and action ranking require:
- frozen train/dev/test separation;
- repeated seeds where training stochasticity matters;
- confidence intervals or dispersion across runs;
- class imbalance testing;
- hard-negative mining;
- distribution-shift cases;
- ablation tests for major feature groups;
- calibration tests;
- fallback/abstention tests;
- artifact reproducibility from locked inputs/versions;
- quantized vs non-quantized quality comparison.

A learned component cannot replace a simpler baseline unless it shows a material improvement without critical regressions.

### 17.5 Memory correctness tests
Memory must be tested as a temporal knowledge system, not only as CRUD.

Required scenarios:
- first admission;
- duplicate observation;
- same fact reported by multiple actors;
- conflicting reports;
- correction/retraction;
- changing truth over time;
- stale vs current fact;
- belief differing from World Truth;
- third-party knowledge boundaries;
- secrets and limited visibility;
- relationship-specific memory;
- emotionally salient event retention;
- irrelevant-memory suppression;
- memory expiry/decay when defined;
- consolidation without information loss;
- save/restore and database migration;
- thousands of memories per NPC;
- corruption/recovery behavior where practical.

Authority tests must prove that OBSERVATION/REPORT/BELIEF/INFERENCE never silently become WORLD_TRUTH.

### 17.6 Retrieval evaluation
Build a gold query-memory benchmark with relevant, partially relevant, distractor and dangerous memories.

Measure at least:
- Recall@K;
- Precision@K;
- MRR/NDCG or equivalent ranking metric;
- actor correctness;
- temporal correctness;
- unresolved-goal recall;
- suppression of invalidated/stale memories;
- latency under increasing database size;
- retrieved-token budget efficiency.

Adversarial tests must contain highly lexically similar but semantically wrong memories.

### 17.7 Emotion and relationship trajectory tests
Do not test only one-step deltas. Simulate trajectories over hours/days/weeks of game time.

Verify:
- bounded values;
- decay and recovery;
- repeated positive/negative events;
- contradictory events;
- personality-dependent appraisal differences;
- relationship asymmetry;
- jealousy/trust/attraction-like dimensions when enabled;
- no runaway accumulation;
- no unexplained state changes;
- deterministic replay for deterministic appraisal paths;
- learned-ranker stability on unseen trajectories.

Use counterfactual tests: changing only one event or one personality trait should produce explainable differences.

### 17.8 Reflection tests
Reflection must be attacked for hallucination and memory corruption.

Required checks:
- trigger fires only when intended;
- no trigger storms;
- same evidence does not create endless duplicate reflections;
- insight provenance points to supporting memories;
- unsupported inference is rejected or marked uncertain;
- contradictions cause belief revision rather than duplicate truths;
- reflection cannot mutate World Truth directly;
- token/context budgets are respected;
- reflection failure leaves canonical state valid;
- replay with mocked GGUF outputs covers malformed, empty, contradictory and overconfident responses.

### 17.9 Agency/BDI-lite tests
For goals, intentions and actions test:
- feasible vs impossible actions;
- goal conflicts;
- priority inversion;
- plan failure/recovery;
- changing beliefs invalidating an intention;
- personality/emotion effects on action ranking;
- no impossible state transitions;
- no action loops;
- deterministic action validation independent of GGUF wording.

### 17.10 Autonomous multi-NPC simulation
CI must run accelerated simulations without the player.

Required scales:
- 3–5 NPC functional scenarios;
- medium population stress scenarios;
- long simulated time horizons;
- repeated seeded runs for reproducibility.

Measure:
- coherent encounters and schedules;
- memory propagation boundaries;
- relationship evolution;
- goal creation/completion/failure;
- reflection frequency;
- event-queue growth;
- duplicate-event rate;
- deadlocks/livelocks;
- impossible co-location or time states;
- GGUF-call budget;
- storage growth;
- catch-up correctness after simulated app closure.

Inject failures: missing events, reordered events, duplicate events, partial save, delayed processing and malformed GGUF outputs.

### 17.11 End-to-end scenario tests
Create canonical stories that traverse the whole engine:

`input -> NLU -> claim -> memory -> emotion -> goal -> reflection -> action -> NPC interaction -> GGUF -> write-back -> later retrieval`.

Each scenario defines expected invariants and important checkpoints rather than brittle exact prose.

Include:
- first meeting to long-term relationship;
- secrets and third-party rumors;
- conflict/correction/reconciliation;
- goal promises and broken promises;
- time/location changes;
- autonomous NPC interaction while player is elsewhere;
- adult relationship/consent state changes for adult characters;
- save/restart/catch-up mid-scenario.

### 17.12 Fuzzing, property and mutation testing
Apply property-based/fuzz testing to parsers, serializers, memory transitions, event queues and deterministic validators.

Use mutation testing on high-risk deterministic modules to verify tests actually detect broken logic.

Fuzz model-facing structured outputs so malformed JSON/claims/GGUF responses can never corrupt canonical state.

### 17.13 Performance and soak testing
Before Moto, run JVM/emulator stress where possible:
- increasing memory DB sizes;
- large event queues;
- many dormant NPCs;
- repeated retrieval;
- repeated NLU inference;
- reflection bursts;
- save/load loops;
- catch-up over large elapsed times;
- multi-hour accelerated engine simulation.

Track latency distributions, heap growth, file/database growth, GC pressure and leaks.

No unbounded memory or queue growth is acceptable.

### 17.14 Final Moto torture gate
The late hardware gate is not a single happy-path interaction. The final probe must include:
- cold/warm start repetitions;
- long dialogue session;
- repeated NLU/retrieval cycles;
- several reflections;
- high-detail NPC encounters;
- autonomous catch-up;
- GGUF generation loops;
- screen/background/resume lifecycle transitions where allowed;
- thermal observation;
- PSS/CPU/latency distributions, not only one sample;
- final database/state integrity check.

All functional failures found on Moto must first receive an automated reproducer when possible before another phone iteration.

### 17.15 Release gate
Release candidate requires all of the following:
- deterministic suites green;
- learned-component frozen benchmarks green;
- zero critical ownership/World Truth corruption;
- memory/retrieval/emotion/reflection/agency integration green;
- long autonomous simulation green;
- fuzz/property/mutation gates green for high-risk modules;
- CI reproducible artifacts/checksums/provenance;
- Android packaging green;
- final Moto torture gate inside hardware budgets;
- no unresolved critical/high severity regression.

Failures become permanent regression tests. Work must continue autonomously through ordinary failures until gates are green or a genuine architecture-level blocker is demonstrated.

This is the final hardware-optimized ecosystem direction for the Moto G56.