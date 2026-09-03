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

This is the final hardware-optimized ecosystem direction for the Moto G56.