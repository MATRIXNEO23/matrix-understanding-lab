# AUTOMATED TRAIN / TEST / PIPELINE POLICY

Status: CANONICAL EXECUTION POLICY
Date: 2026-09-03

## Purpose
For every learnable Matrix component, training/loading, testing, artifact publication and regression validation must be automated end-to-end. The user must not be required to choose datasets, annotate examples manually, run training steps, interpret stack traces, or repeat exploratory phone tests.

This policy generalizes the `auto_train.py`, `auto_test.py`, `run_pipeline.py` pattern into a production-grade Matrix workflow.

## 1. Automatic training / loading
Every learnable component must expose a deterministic automation entry point equivalent to:

`data acquisition -> provenance/license validation -> normalization -> split freeze -> training/loading -> validation -> checkpoint -> artifact -> checksum -> metadata`

### Required behavior
- Work selects the concrete lawful dataset(s) and training strategy from the component's approved architecture; the user is not asked to choose.
- Synthetic/dummy data may be generated for smoke/bootstrap tests, but final quality gates must use real or validated generated Matrix-domain data with frozen unseen splits.
- Training must be resumable when technically possible.
- Random seeds, model revision, dataset revision, split hashes and hyperparameters must be recorded.
- Progress must be visible in logs/progress bars where useful.
- Existing valid artifacts must never be overwritten in-place during training.
- New artifacts are written to temporary/versioned paths and promoted atomically only after validation succeeds.
- On failure, previous known-good artifacts remain intact.
- Training cost must remain EUR 0; if a recipe requires paid compute, Work must choose a lighter/free-compatible recipe or a different approved component strategy.
- Every produced artifact gets SHA-256 plus provenance/license metadata.

## 2. Automatic testing
A component is never accepted because a script prints `OK`.

Testing must attempt to break the component and must include, as applicable:
- normal positive cases;
- empty/null/malformed/boundary inputs;
- adversarial inputs;
- multilingual IT/EN/ES variants;
- colloquial/typo/incomplete/code-switched inputs for language components;
- memory recall and false-memory prevention;
- correction/contradiction cases;
- ownership/authority/World Truth invariants;
- multi-entity/multi-claim cases;
- deterministic regression corpus;
- property-based tests;
- fuzz tests;
- mutation tests for deterministic logic where useful;
- randomized scenario tests with reproducible seeds;
- integration tests against adjacent Matrix contracts;
- persistence/restart/recovery tests;
- stress/soak tests for stateful components;
- resource-budget checks when measurable in CI/emulator.

Every test must record expected versus actual behavior in machine-readable results. Failures must not abort unrelated test cases unless continuing would corrupt state.

## 3. Frozen evaluation
Training/tuning may use TRAIN and DEV only.

A FROZEN TEST set must be created before final tuning and must not be used to select thresholds, prompts, weights, hyperparameters or rules.

The final report must distinguish:
- train score;
- dev score;
- frozen unseen test score;
- worst-language score;
- critical-invariant failures;
- abstention/unknown rate where applicable.

A nominal high score does not pass if the test is contaminated, too easy, or hides systematic failure.

## 4. Automatic error loop
When a test fails:

`failure -> minimal reproduction -> root-cause classification -> candidate fix/training change -> targeted test -> full regression suite -> accept/reject -> continuity update`

For learned components, Work may autonomously alter approved training settings, data balance, hard-example generation, encoder variant within the approved architecture family, compression or quantization.

For deterministic components, Work may generate/implement candidate repairs only inside the approved contract and must accept a repair only if the entire deterministic and integration suite remains green.

No case-ID/string-specific patching is allowed as a substitute for general capability.

## 5. One-command pipeline
Every component must eventually provide a single pipeline entry point equivalent to:

`prepare -> train/load -> validate -> test -> package -> report`

The pipeline must:
- stop before testing if training/artifact validation fatally fails;
- never promote a failed artifact;
- measure elapsed time by stage and total;
- persist logs/results even on failure;
- produce a clear machine-readable exit status;
- produce a human summary;
- update `docs/WORK_CONTINUITY.md` after meaningful stages;
- be resumable from the last safe checkpoint where possible.

## 6. CI gate
CI must run the same canonical pipeline, not a weaker duplicate.

A commit cannot be declared verified while required tests are red.

CI artifacts must include as applicable:
- trained model/database/index artifact;
- checksums;
- provenance/license manifest;
- benchmark JSON;
- human-readable report;
- failure/error analysis;
- Android probe/APK when relevant;
- size/resource breakdown.

## 7. Matrix component application
This policy applies to:
- Matrix-NLU;
- memory admission classifier;
- retrieval reranker;
- emotion/appraisal learned tuning;
- action ranking;
- any future learned classifier/ranker;
- deterministic repair loops for authority, schema, scheduler, memory consistency and other deterministic modules.

Room/SQLite memory persistence itself is not 'trained'; its schema, admission/retrieval behavior, migration and recovery are validated through deterministic/integration/property/stress tests.

## 8. Phone testing
Functional or linguistic failures reproducible in CI/JVM/emulator must not be delegated to the user for discovery.

Moto G56 is a late hardware gate for measurements that genuinely require the physical device: PSS, CPU, real latency, thermal behavior, complete GGUF integration and long-running Android behavior.

## 9. Acceptance principle
The objective is a functioning component, not completion of the automation script.

Work continues within the approved architecture until:
1. the component satisfies its predeclared quality/invariant/resource gates; or
2. a real architecture-level blocker is demonstrated with exhausted approved alternatives and evidence for supervisor review.

Ordinary failed training runs, bugs, threshold calibration, data balancing or regression fixes are not reasons to ask the user for technical decisions.
