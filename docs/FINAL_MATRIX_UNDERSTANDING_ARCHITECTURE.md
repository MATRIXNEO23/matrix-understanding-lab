# FINAL — MATRIX UNDERSTANDING ARCHITECTURE

Date: 2026-09-03
Status: CANONICAL / IMPLEMENTATION AUTHORIZED IN LAB

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

Use a compact multilingual pretrained encoder suitable for distillation/fine-tuning, then train Matrix-specific multi-task heads. Select the concrete encoder by evidence for mobile exportability, multilingual quality, trainability, license/provenance and footprint; do not preserve a named base model if another compatible compact encoder gives materially higher probability of reaching the goal.

Primary deployment target:
- ONNX Runtime Mobile or a demonstrably superior compatible mobile runtime;
- INT8 quantization when the measured quality loss is acceptable;
- offline Android;
- no network runtime dependency.

OpenNLP Candidate B remains a benchmark/reference/fallback during development, not the final target if the trained compact NLU reaches near-perfect generalization.

## Training strategy — automatic by default
Training must be fully automatable by Work/CI:

`source data -> provenance/license validation -> normalization -> Matrix labeling/mapping -> train/dev/frozen test -> training -> validation -> error mining -> hard-example generation -> retraining -> compression/quantization -> mobile export -> benchmark -> artifact/checksum/provenance`

Work must iterate autonomously until the acceptance gate is reached or a technically documented blocker proves the selected family cannot meet the target within the Android budget. Ordinary failed experiments, hyperparameter changes, data balancing, retraining, compression trials and causal fixes are not reasons to return to the user.

The user must not be required to annotate datasets manually, choose hyperparameters, run training commands, or perform repeated exploratory phone tests.

## Data strategy
Use a layered dataset:

1. lawfully usable multilingual NLU data for general intent/slot robustness;
2. Matrix-specific generated and curated data matching the frozen claim contract;
3. adversarial paraphrases and noisy conversational inputs;
4. real Matrix failures promoted into regression families, without tuning directly on the final frozen test set.

MASSIVE is an approved candidate for broad multilingual intent/slot signal, but its ontology is not Matrix's ontology. It must be adapted rather than treated as the final label space.

All training inputs, generated data and derived artifacts require provenance records and license review appropriate to intended distribution.

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

The objective is linguistic competence and correct structured interpretation, not automatic activation of an erotic register. Context/state determines appropriateness; Understanding must accurately interpret the language.

No sexual content involving minors is permitted.

## Acceptance criterion — near-perfect, not decimal chasing
The goal is **near-perfect practical generalization**, not an artificial requirement to display exactly 99.00% or higher.

The final verdict must use a large, frozen, genuinely unseen and adversarial benchmark. A result slightly below 99% can be accepted when all of the following are true:
- performance is approximately in the high-98%/99% region on a genuinely difficult unseen benchmark;
- residual errors are rare, heterogeneous and non-systematic rather than evidence of a missing linguistic capability;
- worst-language performance remains close to overall performance;
- ownership/authority corruption = 0;
- invented World Truth = 0;
- no critical systematic failure on negation, requests, corrections, goals, consent/refusal interpretation, temporal interpretation, third-party references or multi-claim input;
- robustness remains strong on colloquial, incomplete, typo-heavy, code-switched and adult-domain inputs;
- confidence/abstention behavior prevents uncertain outputs from silently corrupting Matrix state.

A nominal score above 99% is NOT sufficient if achieved through benchmark contamination, easy cases, test-specific patches or hidden systematic failure.

Development benchmarks may be smaller, but they cannot be the final proof of generalization.

## Selection principle
Choose the path with the highest probability of producing the required finished component, not the smallest implementation effort and not a favorite library/model.

Training is preferred when:
- sufficient lawful data exists or can be generated/curated automatically;
- the capability is fundamentally linguistic/statistical rather than invariant;
- training can be reproduced and iterated automatically;
- the resulting runtime fits the Android budget.

If the selected encoder/training recipe stalls below near-perfect generalization, Work must perform root-cause analysis and may change encoder, objective, data mixture, distillation/compression strategy or mobile runtime within this architecture family without requesting micro-decisions. It must not revert to accumulating manual linguistic patches merely to lift the benchmark.

## Hardware budget
The GGUF remains the dominant memory consumer. Understanding must remain small enough for the target Moto G56.

Engineering targets before physical measurement:
- quality first among candidates that plausibly fit mobile constraints;
- aim for tens of MB incremental PSS, not hundreds;
- investigate/optimize if incremental PSS is expected to exceed ~80 MB;
- preliminary NO-GO if incremental PSS is expected to exceed ~100 MB without exceptional measurable quality benefit;
- inference must be bursty per utterance rather than continuous CPU load.

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
P0 remains evidence that the Matrix claim contract is tractable: Candidate B achieved approximately 0.9924 overall field exact, 1.0 claim-count exact, 1.0 negation F1, zero ownership violations and zero invented World Truth on the 66-case laboratory benchmark. It remains a strong oracle/fallback, but that benchmark is too small to establish near-perfect generalization.

## Final construction objective
Construct, train, compress and export a compact multilingual Matrix-NLU model that replaces linguistic guesswork with learned generalization while preserving strict Matrix invariants.

The implementation loop is authorized in this laboratory. Work should proceed autonomously through data acquisition/provenance, Matrix dataset construction, model selection within the compact multilingual family, multi-task training, adversarial evaluation, error mining, retraining, compression/quantization, ONNX/mobile packaging and CI automation until the near-perfect acceptance criterion is satisfied or a real architecture-level blocker is documented.

Only after the software/provenance/quality gates are green should a final Moto hardware probe be requested. Production integration remains a separate strangler-migration checkpoint after the trained model proves superiority.