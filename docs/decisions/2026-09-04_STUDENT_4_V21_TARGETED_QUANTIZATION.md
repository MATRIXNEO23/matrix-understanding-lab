# Student-4-v2.1 — Targeted Quantization Policy

Date: 2026-09-04
Status: DECISION RECORDED / NOT YET EXECUTED
Repository: `MATRIXNEO23/matrix-understanding-lab`
Reference run: `33837897457`
Reference commit: `72f14286e89df88f41aedb169c7307b26b57eedf`

## Decision

Student-4-v2.1 must not be quantized with a blind global strategy.

Quantization must be targeted and metric-aware: protect the weak heads/classes first, then compress only the parts that prove stable under measured degradation gates.

The goal is Android/offline deployment without destroying the exact capabilities Matrix Engine needs most: negation, predicate, dialogue act, ownership, perspective, subject/target referents and temporal relation.

## Current evidence from controlled run

Run `33837897457` completed training and stopped during the development evaluation step because of a Python import/package error, not because the model quality collapsed.

Training evidence already available:

- Variant: `student-4-v2.1`
- Encoder layers: 4
- Parameters: 58,599,411
- Best dev score: 0.9676758069767126
- Early stop: epoch 7, patience 2
- Best observed point: around epoch 5
- Frozen data: not read
- Training splits: train/dev only

Strong areas observed on dev:

- `sequence.claimKind`
- `sequence.ownerReferent`
- `sequence.perspectiveReferent`
- most Matrix dev structural heads

Weak / protected areas:

- `tokens.negation` on Matrix dev
- `sequence.predicate` on P05 dev
- `sequence.dialogueAct` on P05 dev
- `sequence.subjectReferent` on P05 dev
- `sequence.targetReferent` on P05 dev
- `sequence.temporalRelation` on P05 dev

## Mandatory order

1. Fix the controlled dev gate mechanics first.
2. Re-evaluate the existing saved bundle from run `33837897457` without retraining.
3. Select threshold from dev only.
4. Produce per-head and per-language metric baselines.
5. Only then test quantization candidates.
6. Do not access frozen evaluation until dev-only gates justify it and explicit authorization is given.

## Quantization rule

Do not apply one global INT8/INT4 policy to the whole model and assume it is safe.

Use a sensitivity matrix:

- baseline FP32 / original checkpoint;
- dynamic INT8 all eligible layers;
- mixed precision with encoder quantized and fragile heads protected;
- optional per-head protection for weak output heads;
- optional selective quantization only for stable heads/layers;
- reject any candidate that improves size but damages protected metrics.

## Protected metrics

A quantized candidate must be rejected if it causes unacceptable degradation in any protected area:

- Matrix `tokens.negation`;
- P05 `sequence.predicate`;
- P05 `sequence.dialogueAct`;
- P05 `sequence.subjectReferent`;
- P05 `sequence.targetReferent`;
- P05 `sequence.temporalRelation`;
- per-language performance for IT/EN/ES;
- authority/ownership/perspective invariants;
- abstention/threshold behavior.

## Practical policy

Preferred initial strategy:

- quantize stable encoder components first;
- keep classifier heads for weak labels in higher precision if measurable degradation appears;
- keep threshold selection tied to each quantized candidate, but never tune on frozen;
- compare package size, latency, RAM and accuracy together;
- treat quantization as a deployment candidate, not as a training result.

## Hard constraints

- No frozen data for tuning.
- No production promotion from dev-only evidence.
- No accepting a smaller model if negation, predicate or dialogueAct regress materially.
- No hiding class-specific regressions behind high macro averages.
- No replacing the controlled-stop purpose with an unconditional green CI.

## Current next step

Use the saved artifacts from run `33837897457`:

- report: `matrix-nlu-student-4-v21-report-33837897457`
- bundle: `matrix-nlu-student-4-v21-bundle-33837897457`
- resume checkpoint: `matrix-nlu-student-4-v21-resume-33837897457`

Then run a dev-only post-check that fixes the `matrix_nlu` import path and produces the missing controlled dev summary and threshold report.

Only after that, add the targeted quantization benchmark.
