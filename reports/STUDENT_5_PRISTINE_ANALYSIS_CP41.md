Supervisor GPT — Student-5 FP32 Pristine Pre-Training Analysis Report

STUDENT5_PRISTINE_ANALYSIS = BLOCKED

Branch: student5-path-b-v3. Starting HEAD: 3bb4d42010c254785b02a327a0469c3d16c4902a. Final HEAD is the introducing commit of this report, returned in the handoff. Local delivery is a selective API snapshot, not a Git checkout; no clean-git-status claim is made.

The corrected subject is authenticated and physically executed. This BLOCKED verdict is NOT the former CP40 missing-trained-checkpoint blocker. CP40 remains historical; pristine is now the expressly authorized subject. Authentication and exploratory representation analysis are complete. A complete semantic-capability diagnosis and empirically certified training specification are not established. We do not equate backbone distances with correct Matrix-NLU decisions.

## Authentication

Canonical release: https://github.com/MATRIXNEO23/matrix-understanding-lab/releases/tag/student-5-minilm-40k-phase-a-pristine

Release ID 383143636; asset ID 545406840; student5-minilm-phase-a-pruned-40k.zip; 88,361,246 bytes; archive SHA-256 7804bfb245b71df9b835fff7ee00f6ec887e019772ae34c82d269d821d587191.
Internal model/model.safetensors: 148,020,400 bytes; SHA-256 d6e45891d1e0ec4ed023caaeb17c0dd0ae80a93b8bf877d275310b7f2837efa2.
All 17 internal SHA256SUMS entries match. Existing CP34-downloaded bytes were reused and freshly hashed against current Release metadata; no new binary download is claimed. The canonical asset remains the durable model copy. Recovery requires authenticated Release download; the connector alone cannot deliver binary assets.

Lineage: microsoft/Multilingual-MiniLM-L12-H384@6e8c1ec6b4ec4e3fc6eb7d2cd834fcd582b61daf, Phase-A vocabulary pruning. BertModel, 12 layers, hidden 384, 12 attention heads, vocabulary 40,000, 36,999,552 parameters. XLMRobertaTokenizer with corresponding reduced SentencePiece vocabulary and persisted token remap. Load reports zero missing/unexpected keys, dtype torch.float32. It is PRISTINE relative to Matrix training, not randomly initialized: upstream pretraining is historical. No Matrix claim/role heads are present.

## Executed methodology and evidence

NEW_REPRODUCED_ANALYSIS: 33 manually authored contrast pairs, 11 families × IT/EN/ES, 64 distinct texts. Inputs are diagnostic examples only, not TRAIN v2 or gold supervision. No TRAIN/DEV/Frozen payload was loaded. No claim of exact disjointness against unread protected sets is made; provenance is newly authored.

CPU Torch 2.4.1+cpu, Transformers 4.44.2, NumPy 1.26.4. Model eval, all parameters requires_grad=false, inference_mode, local_files_only. Untruncated input; all sequences fit position capacity. Normalized mean last-layer pooling includes special tokens and is explicitly a diagnostic readout, not the project decoder. Raw token IDs, pieces, 384-dimensional vectors and every pair's cosine/L2 are retained. Repeat inference max delta 0.0; 0 unknown tokens among all 64 texts; all hidden states finite. Model SHA checked before and after execution unchanged. No upstream model comparison was newly run.

HISTORICAL_EVIDENCE: preserved archive pruning manifest, separately extracted into historical-summary.json. Its 161-sentence preservation test and 36 contrasts compare the pruned backbone to upstream; they are not Matrix-NLU accuracy. Historical reports of unchanged non-embedding tensors are provenance evidence, not a new bitwise upstream comparison here.

## Empirical findings and error-analysis boundaries

Present on the tested sample: usable IT/EN/ES tokenization without UNK, reproducible finite contextual representations and nonzero representation changes for all authored contrasts. These are real forward results. They do not establish semantic role decodability, multilingual parity on a population, correct consent interpretation, or claim extraction.

Observed representation risks: source/viewpoint swaps have cosine 0.999045 IT, 0.999598 EN, 0.999140 ES; subject/object swaps 0.999367 IT, 0.998823 EN, 0.996815 ES. Word overlap dominates this pooled representation on these examples. This warns against using sentence cosine to assign roles. It does not prove that token-level information has been lost or that a future trained head must fail.

Positive versus negative desire about touch remains close: 0.983471 IT, 0.982953 EN, 0.977047 ES. Negation cannot safely be inferred from similarity alone. Corrected-positive versus negative pairs differ, but no polarity output exists to grade. Malformed requests also yield finite vectors (cosine to grammatical counterparts 0.913430–0.960877); finite output provides no grammatical-validity or abstention guarantee.

Missing task interface: the pristine exposes hidden states/pooler, not subject, referent, ownership, perspective, source, polarity, temporalRelation, dialogueAct, predicate, claimKind, claim count or field status. Their correctness, systematic confusion rates, UNKNOWN behavior and role independence remain UNMEASURED. No Student-4 failure was imported. No regression versus a prior Student-5 semantic baseline is claimed because no comparable baseline was evaluated.

## Approved D01–D07 mapping

The approved semantics are taken from prompts/WORK_STUDENT_5_PATH_B_V3_CREATE_REPAIRED_TRAIN_V2_ONLY.md at starting HEAD. The older decisions.json awaiting-approval status is superseded; no decision is reopened.

| Decision | Student-5 evidence | Classification | Training implication / limit |
|---|---|---|---|
| D01 desire time | D01-it/en/es cosine 0.945579–0.972888; present wanting and future wanting distinct but close | observed_risk; insufficient_coverage | Contrast desire time against desired-action time; CURRENT for present desire under approved rule. No temporal label error measured. |
| D02 source/perspective | D02-it/en/es swapped attribution/viewpoint cosine 0.999045–0.999598 | observed_risk | Teach linguistically justified independent binding; never copy source mechanically. No token-level binding failure established. |
| D03 BELIEF/DIRECT | D03-it/en/es wrapper contrasts 0.911102–0.969601 | other_evidence; missing_capability | Representation responds to wrapper; missing claimKind readout. Teach overt wrapper versus plain subjective assertion. |
| D04 malformed/reflexive | D04-it/en/es and malformed-it/en/es produce finite distinct representations | observed_risk; insufficient_coverage | Finite output is not validity; preserve grammatical reflexives and quarantine malformed gold, never guess roles. |
| D05 metalinguistic negation | D05-es cosine 0.894437; polarity-es 0.977047 | other_evidence; observed_risk | Distinguish discourse No from proposition negation; teach scope separately. No observed classifier error. |
| D06 zero-claim/UNKNOWN | D06-it/en/es punctuation versus proposition 0.617789–0.687069; no count/status output | missing_capability; insufficient_coverage | Teach genuine zero claims separately from an existing proposition with unresolved fields. Punctuation sample is not exhaustive boundary coverage. |
| D07 independent roles | D07-it/en/es role swaps 0.996815–0.999367 | observed_risk; insufficient_coverage | Preserve token/candidate evidence and natural divergence; owner/subject independence is not established by simple subject/object swaps. |

## Provisional operational specification (not a certified dataset specification)

1. Learn explicit V3 outputs: spans/referents, claim boundaries/count, predicate, claimKind, dialogue act, polarity, time and field status. Backbone vectors alone supply no such outputs.
2. Reinforce binding and scope with minimal contrasts in each language: swapped participants/attributors, belief wrappers, current desire versus future desire/action, proposition versus metalinguistic negation. Every gold must be linguistically adjudicated under approved D01–D07.
3. Preserve observed token coverage and contextual sensitivity; retain valid equal-role cases as well as natural divergence. Preserve grammatical reflexives and positive corrected propositions. Treat adult consent/refusal as ordinary semantics without lexical penalties.
4. Correct the prospective risk of sentence-similarity shortcuts; do not assert existing supervised errors. Future readout must use relevant token/candidate evidence and be independently evaluated; no architecture change is implemented here.
5. Include real zero-claim boundaries, unresolved existing propositions, grammatical/malformed contrasts, natural role divergence, matched negation scope and temporal contrasts. This is a diagnostic-motivated proposal, not generated TRAIN or exhaustive coverage.
6. Do not introduce keyword-only gold, automatic source=perspective/owner=subject copying, artificial all-roles-different examples, malformed repaired intent by guessing, cosine-derived labels, Student-4 errors relabelled as Student-5 evidence, or DEV/Frozen-derived training examples.
7. Balance semantic contrast families across IT/EN/ES, report per-family counts and natural code-switch separately; no numeric quota is justified by these 33 pairs. Larger representative coverage remains necessary before fixing sampling weights.
8. Anti-regression checks must preserve tokenization identity, valid equal-role cases, positive/no-negation controls, valid reflexives, and matched language semantics. Future trained-model measures must score exact bindings and scope, not cosine separation.
9. Before training: immutable v1 hashes, complete row provenance, schema/target-builder validation, semantic adjudication, language/family census, justified ambiguity and empty claims, duplicate policy preserving meaningful contrasts, contamination audit, and separately accepted Gate-B DEV/evaluator/decoder/calibration readiness. Existing acceptance criteria must not be lowered.

TRAIN v1 relationship: no row-level reuse is certified from these probes. It remains immutable material requiring explicit semantic/provenance review. Neither TRAIN v1 + D01–D07 nor the diagnostic texts are automatically approved TRAIN v2. Prior CP37/CP38 curriculum audits are separate evidence, not backbone measurements.

## Blockers and scope closure

The remaining blocker is insufficient evidence for a COMPLETE semantic pre-training diagnosis: a bare backbone supplies no validated V3 semantic readout, and the small representation battery cannot establish missing/present label capabilities, field confusions, ownership independence or population-level coverage. Creating random heads or fitting a classifier would not resolve this honestly within the assignment. Supervisor review must decide a suitable further analysis method/scope; no dataset or model work is started in anticipation.

Files produced: this report; PLAN.md; probe.py; probes.json; results.json; provenance.json; historical-summary.json; SHA256SUMS; continuity update. Permanent destination: reports/evidence/student5-pristine-analysis-cp41/ and reports/STUDENT_5_PRISTINE_ANALYSIS_CP41.md. Results contain complete vectors for reproducibility. Run: python probe.py <authenticated extracted model directory>, with the declared pinned dependencies. The runner verifies model identity before/after; acquire model from the canonical Release, not from a regenerated substitute.

Publication must be followed by exact remote readback of every file and manifest checks. This report's commit and remote verification counts are supplied in the final handoff. Prior reports, datasets, model artifacts and runtime files are preserved.

trainingExecuted=false
trainV2Created=false
quantizationExecuted=false
onnxExecuted=false
student5PristineModified=false
trainV1Modified=false
evaluatorModified=false
decoderModified=false
calibrationModified=false
nextWorkStarted=false
canonicalDevRead=false
frozenDataRead=false

STOP. No continuing job, training or dataset creation is authorized by this report.
