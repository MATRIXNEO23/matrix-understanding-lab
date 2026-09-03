# FINAL — MATRIX UNDERSTANDING ARCHITECTURE

Date: 2026-09-03
Status: CANONICAL DIRECTION FOR NEXT IMPLEMENTATION

## Goal
Build the most accurate practical offline Android Understanding component for Matrix, with IT/EN/ES support, automatic training, structured Matrix output, low runtime footprint, and minimal dependence on manual rule patching.

## Final architecture choice
The target architecture is:

`USER TEXT -> tokenizer/boundary handling -> compact multilingual Transformer encoder -> Matrix multi-task heads -> Typed Claims -> deterministic invariant validator -> Matrix memory/runtime`

The trained NLU model, not a hand-built parser, is responsible for linguistic interpretation.

### Learned responsibilities
The model should learn, jointly where practical:
- dialogue act / intent;
- Matrix predicate classification;
- subject / target / referent signals;
- entity and span tagging;
- negation;
- temporal relation / temporal expression;
- hypothesis/correction/request/goal distinctions;
- multi-claim linguistic decomposition or the signals needed to produce it;
- ambiguity resolution relevant to the Matrix claim contract.

### Deterministic responsibilities
Deterministic logic is retained only for strict invariants and safety/authority rules that should not depend on linguistic guesswork:
- schema validation;
- ownership/authority constraints;
- provenance/source IDs;
- World Truth promotion rules;
- memory write permissions/admission invariants;
- consistency checks and rejection of structurally invalid output.

Deterministic linguistic patching is not the target solution. Regex/rule additions are allowed only as bounded preprocessing/normalization where they are language-independent or formally justified, not as an accumulating substitute for model capability.

## Model strategy
Do not train a language model from random initialization.

Use a compact multilingual pretrained encoder suitable for distillation/fine-tuning, then train Matrix-specific multi-task heads. The implementation should be selected for mobile exportability and quantization, with ONNX Runtime Mobile as the primary deployment substrate unless a demonstrably better mobile runtime emerges before integration.

Preferred deployment form:
- ONNX;
- INT8 quantized if quality loss remains within the quality gate;
- offline Android;
- no network runtime dependency.

OpenNLP Candidate B remains a strong benchmark/reference/fallback during development, but is not the final target architecture if the trained compact NLU reaches the required quality.

## Training strategy — automatic by default
Training must be fully automatable by Work/CI:

`source data -> provenance/license validation -> normalization -> Matrix labeling/mapping -> train/dev/frozen test -> training -> validation -> error mining -> hard-example generation -> retraining -> quantization -> ONNX export -> benchmark -> artifact/checksum/provenance`

Work must iterate autonomously until the quality gate is reached or a technically documented blocker proves the selected architecture cannot meet the target within the Android budget.

The user must not be required to annotate datasets manually, choose hyperparameters, run training commands, or perform repeated exploratory phone tests.

## Data strategy
Use a layered dataset:

1. permissively licensed multilingual NLU data for general intent/slot robustness;
2. Matrix-specific generated and curated data matching the frozen claim contract;
3. adversarial paraphrases and noisy conversational inputs;
4. real Matrix failures promoted into regression families, without tuning directly on the final frozen test set.

MASSIVE is an approved research/training candidate because it supplies broad multilingual intent/slot data, but its ontology is not Matrix's ontology. It must be adapted, not treated as the final label space.

## Adult-domain coverage
For exclusively adult characters and adult interactions, the training corpus must include natural language covering:
- romantic;
- sensual;
- erotic;
- sexually explicit registers;
- consent and refusal;
- initiation and reciprocal participation;
- attraction/desire;
- escalation/de-escalation;
- body/action references;
- narrative/action descriptions;
- ambiguity, negation and temporal references within adult contexts.

The goal is linguistic competence and correct structured interpretation, not automatic activation of an erotic register. Context/state determines when such content is appropriate; the NLU must simply understand it accurately.

No data involving minors or sexual content involving minors is permitted.

## Quality target
The project goal is near-perfect practical Understanding, not 'good enough'.

The architecture is accepted only after a large frozen unseen benchmark shows:
- overall field exact >= 0.99 target;
- worst-language performance close to overall performance;
- ownership violations = 0;
- invented World Truth = 0;
- no critical collapse on negation, requests, corrections, goals, temporal interpretation, third-party references or multi-claim input;
- strong robustness on colloquial, incomplete, typo-heavy and code-switched inputs.

A smaller P0-style benchmark may be used during development but cannot be the final proof of generalization.

## Success-probability principle
Choose the path with the highest probability of producing the required finished component, not merely the smallest implementation effort.

Training is preferred when:
- sufficient lawful data exists or can be generated/curated automatically;
- the capability is fundamentally linguistic/statistical rather than an invariant;
- training can be reproduced and iterated automatically;
- the resulting runtime fits the Android budget.

Manual deterministic linguistic logic is preferred only when the problem is truly rule-like/invariant or when it measurably improves reliability without becoming an accumulating patch system.

## Hardware budget
The GGUF remains the dominant memory consumer. The Understanding model should remain small enough for the target Moto G56.

Design targets:
- prioritize quality first among candidates that fit mobile constraints;
- aim for tens of MB incremental PSS, not hundreds;
- investigate/optimize if incremental PSS exceeds ~80 MB;
- preliminary NO-GO if incremental PSS exceeds ~100 MB without exceptional measurable quality benefit;
- inference should be bursty per utterance, not continuous CPU load.

These are engineering budgets until physical measurement is performed.

## Phone-testing policy
No repeated Moto testing during ordinary linguistic development.

CI/JVM/emulator must eliminate functional, training, regression, export and packaging failures first. The Moto is a late hardware gate for:
- real PSS;
- real CPU;
- cold/warm latency;
- thermal behavior;
- Android integration with the complete Matrix/GGUF runtime.

## What is no longer the target
Do not spend the main implementation effort on:
- expanding the old frozen deterministic parser;
- accumulating regex fixes to mimic general language understanding;
- treating OpenNLP + manual mapper as automatically final merely because P0 scored highly;
- building B4/BDI/vector DB/graph DB before the Matrix Core Understanding path is resolved;
- training a large general-purpose LLM solely for Understanding.

## Current evidence
P0 remains important evidence: Candidate B (`ICU + OpenNLP + Matrix mapper`) achieved approximately 0.9924 overall field exact, 1.0 claim-count exact, 1.0 negation F1, zero ownership violations and zero invented World Truth on the 66-case laboratory benchmark. This proves that the Matrix claim contract is tractable and provides a strong baseline/oracle, but the benchmark is too small to establish near-perfect generalization.

## Final implementation objective
Create a compact multilingual Matrix-NLU model, trained automatically and exported for Android, that replaces linguistic guesswork with learned generalization while preserving strict deterministic Matrix invariants.

Once it passes the large frozen quality gate and Android budget, integrate it into the canonical Matrix Core pipeline using strangler migration, with P0 Candidate B retained only as benchmark/fallback until the new model has proven superiority.