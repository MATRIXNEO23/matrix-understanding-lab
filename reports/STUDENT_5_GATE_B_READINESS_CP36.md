# Supervisor GPT — Gate B Readiness Report

Student-5 Path B, checkpoint CP36.

Date: 2026-09-07. Issuer/reviewer: Supervisor GPT. Executor: ChatGPT Work.
Scope: GATE B READINESS ONLY.
Branch: `student5-path-b-v3`.
Starting HEAD: `cfe905aff7a1076fd2cf455041babb782ccf7289`.
Earlier execution-source HEAD: `1ef81d3e8d7b92d9cbd2bf5f54e6d3d1918f8973`.
The previous read-only monitoring interruption left the audit unpublished. This assignment recovers and publishes it. Current-tree verification confirms all 378 previously inspected path entries unchanged, including 130 TRAIN files and nine execution-source files; only the new readiness assignment appears among new relevant paths. Executed probe results are reused with that explicit provenance, not claimed as newly rerun. See `resume-validation.json`.
Delivery identity: the commit introducing this report, directly descended from that HEAD; exact final SHA is returned in the handoff. No self-referential commit SHA is embedded.

**GATE_B_READINESS = BLOCKED**

Gate A/A4 is accepted by Supervisor GPT; A1/A2/A3/A4 and TASK 2.3 were not repeated. This audit checked existing TRAIN bytes and software evaluation behavior. It did not run a model, training, optimizer, backprop, fine-tuning, augmentation, quantization, Frozen evaluation or Assembling integration. No dataset, model, previous evidence or artifact was overwritten.

## Identities and findings

| Component | Identity and evidence | Readiness |
|---|---|---|
| Authorized TRAIN | `student5-matrix-nlu-v3-train-v1`, `data/student5_v3/`, 3,150 rows / 3,990 claims | Integrity PASS |
| TRAIN logical SHA-256 | `1118a900026f48cfcc290c3f9dc52a1a019a6a1f4761661f326c33770523140e` | Ordered 63-shard bytes match |
| TRAIN migration manifest SHA-256 | `87b4a43035d2e3d84a6d599e1f81b497af6e2f36e4ef2c470adb87341c17da98` | Exact match |
| Contract | `MATRIX_NLU_CONTRACT_V3`; fingerprint `7b0646e44243ad897760c0fcadbe141f1b8e88e3fd8d63a1789106571b9987b0` | Existing frozen target; no changes |
| Allowed DEV V3 | No registered identity, checksum, locator or authorized V3 migration found in the inspected current tree/registry/Release inventory and dataset documentation | BLOCKED; no DEV opened or substituted |
| Evaluator | `matrix_nlu/evaluate_v3.py`, SHA-256 `b28aafa7b553b5ae8ffe1a2edddf3f269c1ed5892c2dba05f2bf4a4cd3cab7c4` | Partial scorer, insufficient for required gate |
| Decoder helpers | `matrix_nlu/inference_v3.py`, SHA-256 `731b6729c63b7cdf28c7383d7bcfe79932a14717fd254458710567f5766927fe` | V3 helpers exist; complete model-to-evaluation path not demonstrated |
| Calibration | `matrix_nlu/select_threshold.py`, SHA-256 `48a6b1af3898e349ff38951b4b6c7caae84fc2bea35d2888e768093352f1d998` | Imports legacy evaluator/decoder; no demonstrated V3 calibration path |
| Error analysis | `matrix_nlu/analyze_errors.py`, SHA-256 `e989a957c52ea540b8f9cd733700817c12ff65df4f0f334ef4540c59d02c5060` | Legacy residual input; no connected V3 per-family pipeline |

All source identities above match both the earlier execution-source HEAD and current starting HEAD. Nine local software-source copies, including imported test fixtures, were independently checked against their Git blob IDs: 9/9 match. See [source-integrity.json](evidence/student5-path-b-cp36-readiness/source-integrity.json).

## Executed TRAIN integrity and contamination checks

[Runtime evidence](evidence/student5-path-b-cp36-readiness/runtime-readiness-evidence.json) records:
- 130/130 TRAIN-directory Git blob hashes match current repository metadata.
- 129/129 per-file SHA-256 entries match; logical dataset and manifest match their authorized identities.
- All 3,150 rows have split `train`; 3,150 provenance records exist.
- Row/provenance source counts agree: Matrix V2 TRAIN 2,775; v2.2A repair TRAIN 375.
- Languages: IT 1,126; EN 1,006; ES 1,007; code-switch 11.
- Embedded source templateSplit is train for 2,655 rows and absent for 495. An absent embedded field is not affirmative evidence of a leak; source IDs and immutable manifest remain the provenance evidence.
- No DEV was copied into TRAIN, no data was changed, no new examples were produced.

**DEV copied into TRAIN = false. Contaminazione DEV→TRAIN = UNKNOWN for independent dataset separation.** No split/provenance violation was detected in the audited TRAIN, and no contamination was introduced by this assignment.
This does **not** certify pairwise TRAIN–DEV disjointness. That check is `UNVERIFIABLE_MISSING_DEV_V3_IDENTITY`; no DEV V3 artifact is identified to compare. This unverified requirement contributes to BLOCKED. Existing repeated TRAIN surfaces are not by themselves evidence of DEV contamination.

**Frozen read = false.** Only repository path metadata, selected docs/source and the authorized TRAIN directory were read. No Frozen payload, examples, evaluation, tuning or error mining was accessed. This is an execution-scope declaration supported by the read-only probe and audited inputs, not a claim about every historical actor.

## Executed evaluator fault probes

The reproducible [readiness_probe.py](evidence/student5-path-b-cp36-readiness/readiness_probe.py) imports the existing `test_evaluate_v3.gold_and_prediction` software fixture. It mutates predictions in memory only. The fixture is English synthetic software data, **not DEV** and not learned-model output. It does not prove linguistic quality in any language.

| Injected prediction defect | claimExact | claimCountExact | Result |
|---|---:|---:|---|
| None, baseline | 1.0 | 1.0 | Control |
| Wrong claim sourceSpan boundary | 1.0 | 1.0 | Not detected |
| Wrong mention-table span identity | 1.0 | 1.0 | Not detected |
| Forbidden downstream `worldTruth` field | 1.0 | 1.0 | Not rejected or scored |
| Extra duplicated claim | 1.0 | 0.0 | Count detects excess; paired claim metric remains perfect |
| Missing claim | 0.0 | 0.0 | Negative control detected |

All three first defect cases retained perfect returned accuracy metrics and zero corruption counts. This demonstrates evaluator limitations, not a claim that the decoder normally emits those defects. The decoder has its own forbidden-field guard; the evaluator lacks independent rejection/scoring for imported invalid predictions.

Static source confirms:
- sourceSpan is validated in gold but not compared in prediction scoring.
- entityMentionIds are compared without independently scoring mention-table spans/entity identity.
- rows/claims are paired by position; no row-ID alignment validation or full exactClaimSet metric is provided.
- returned slices use language:domain, not the required semantic family taxonomy, and expose only fieldExact/rolePointerExact per slice.
- source and owner role comparisons exist, but are not a full per-head/per-family acceptance gate.

Historical DEV references are explicitly V1/V2, not V3. `docs/MATRIX_NLU_DATASET_V2.md` records Matrix V2 DEV SHA-256 `704e809f0e9ebace3a5c047989b74d354ac8811757a2644b0d9c04cfb0631012` and P0.5 V2 DEV `7533f56194431bd17b6f8544031d5436ca14ee6e209336da8133e1f05cdf0866`. Their documented negation-scope/schema semantics differ from V3 cue-only semantics. No DEV payload was read, migrated, rebuilt or relabeled. These historical identities do not supply the missing approved V3 DEV identity.

Current scorer definitions: claimCountExact is the fraction of rows with equal claim counts; claimExact is exact matching of all compared fields over position-paired claims, excluding unmatched extras from that denominator; fieldExact covers four categorical values, rolePointerExact the five referent pointers, spanGroupExact five span/mention-ID groups, temporalExact relation plus anchor, and fieldStatusExact their corresponding statuses. Each ratio is zero when its denominator is zero. Ownership/source corruption counts record mismatching paired role fields. These definitions explain why claimExact is not exactClaimSet and why a global score cannot close the required gate.

## Decoder, calibration and IT/EN/ES error analysis

V3 BIO grouping, candidate pointers, independent source/perspective roles, temporal validation, field statuses, confidence-threshold arguments and output guards exist. `build_matrix_output_v3` accepts already-built mentions/candidates/raw claims. It is not a demonstrated tokenizer/model-logits-to-claims evaluation entry point. Candidate/anchor embeddings are external model inputs. Accepted Gate-A physical tensor execution does not establish this semantic evaluation pipeline, and was not rerun.

`select_threshold.py` imports `evaluate_e2e.score_rows` and `inference.validate_claim`, consumes the legacy evidence structure and sets `worldTruthUpdates`. A direct import rename is not a verified V3 repair. V3 per-field calibration, admissibility and metric mappings need an explicit compatible path.

`analyze_errors.py` can count IT/EN/ES residual categories given legacy error records. Its referent classification uses old subject/owner/perspective/target keys. The V3 scorer returns aggregates, not those residual records, and the pipeline does not supply the required independent sourceReferent and critical-family analysis. Therefore IT/EN/ES per-family error-analysis readiness is **not demonstrated**, despite helper functionality.

## Evaluation criteria to preserve

Authority: [current Supervisor readiness-only assignment](../prompts/WORK_STUDENT_5_PATH_B_V3_GATE_B_READINESS_ONLY.md), [completion package, Gate B/B3/B5 and Gate C](../prompts/WORK_STUDENT_5_PATH_B_V3_COMPLETION.md), [V3 contract](../docs/MATRIX_NLU_CONTRACT_V3.md), [acceptance tiers](../docs/MODEL_ACCEPTANCE_TIERS.md). The latest readiness-only assignment controls execution scope and supersedes automatic continuation.

Required hard invariants: ownership corruption = 0 on required gate set; invented World Truth = 0; no downstream-state fields emitted. Calibrate on allowed DEV only; critical uncertainty must abstain/fail closed. Never tune on Frozen or lower gates.

Required independent slices: negation and cue spans/polarity; temporal and supported advanced relations; all five referents and source!=perspective; ownership; report/third party; belief/hypothesis; request; command; correction; goal/desire; spans/entities; multi-claim; ambiguity/abstention; IT/EN/ES, code-switch/noisy input; adult consent/refusal/withdrawal/desire/boundaries. Adult content alone must not cause a confidence penalty.

Existing legacy numerical defaults in `select_threshold.py`: selective accuracy >=0.99, claim-count exact >=0.99, exact claim set >=0.98, valid coverage >=0.98, critical-family/language exact claim set >=0.98, ownership/world-truth counters zero. These values are recorded **as legacy definitions**, not silently adopted or relaxed as V3-equivalent metrics. The current V3 scorer does not compute their full equivalents. A V3 evaluation/calibration configuration and handling of empty required slices remain unspecified/unverified. Runtime confidence thresholds must be derived later from authorized DEV; their absence before calibration is not itself a demand to invent fixed probabilities.

Known accepted TRAIN coverage risks remain: BELIEF/COMMAND absent; REPORT 8 IT-only; advanced temporal relations absent; adult withdrawal one IT claim; repeated surfaces 1,561. No augmentation or reclassification of TASK 2.3 acceptance occurred. Their material effect cannot be established without the missing DEV/evaluation path.

## Residual blockers and handoff

1. Identify an authorized, recoverable V3 DEV artifact with ID/version, locator, SHA-256, V3 gold/provenance and split/family/language coverage; then independently verify separation from immutable TRAIN. No V2 substitution or DEV creation is authorized by this audit.
2. Complete/correct V3 evaluation and the model-to-decoder evaluation connection, including boundary/entity identity/full claim sets, input alignment/contract rejection and safety invariants.
3. Define and verify the V3 metric/gate mapping, DEV-only calibration interface and connected IT/EN/ES per-family residual analysis.

These are data-identity and substantive evaluation-pipeline gaps, not merely a broken path or ordinary configuration typo. Only documentation/evidence was changed within this assignment. No unapproved metric definition, dataset migration or evaluator redesign was substituted to obtain PASS.

Supervisor GPT receives this completed readiness audit with BLOCKED. No background task or workflow was launched or left running. Next action is Supervisor disposition of these explicit blockers; this executor starts no follow-on work. Full Path B training and later gates remain not executed and outside this assignment.

## Reproduction and evidence persistence

From the delivery commit, with Python 3.10+ and repository source available:

```bash
python reports/evidence/student5-path-b-cp36-readiness/readiness_probe.py --train data/student5_v3 --tree reports/evidence/student5-path-b-cp36-readiness/train-tree.json --source matrix_nlu --output /tmp/student5-cp36-readiness-recheck.json
```

This reads authorized TRAIN and imports safe software fixtures only. It writes only the specified evidence output. Do not run training or any Frozen test suite.

Evidence directory: [student5-path-b-cp36-readiness](evidence/student5-path-b-cp36-readiness/). `inventory.json` preserves the original search scope and metadata; `resume-validation.json` binds it to the current HEAD, and `resume-release-inventory.json` records the refreshed Release inventory; `source-integrity.json` binds execution sources to Git blobs; `runtime-readiness-evidence.json` holds all executed results; `result.json` records the scoped verdict. `SHA256SUMS` covers these evidence files, this report and the updated continuity.
