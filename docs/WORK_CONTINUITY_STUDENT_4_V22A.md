# Work continuity addendum — Student-4-v2.2A Controlled Repair

Last updated: 2026-09-04T16:49+02:00  
Repository: `MATRIXNEO23/matrix-understanding-lab`  
Branch: `main`
Continuity schema: `matrix.nlu.student-4.v22a.continuity.v3`

## Current state after owner decision

Student-4-v2.2A completed training and dev-only evaluation successfully, but did not pass the original canonical dev gate.

The owner has explicitly revoked the earlier absolute `DO_NOT_QUANTIZE` operational order and authorized an intermediate runtime standard.

New active status:

```text
OWNER_APPROVED_CONTROLLED_RUNTIME_CANDIDATE
FAILED_CANONICAL_DEV_GATE_CARRY_OVER_ALLOWED
FROZEN_UNREAD
NOT_TECHNICALLY_PRODUCTION_VALIDATED
```

Important distinction:

```text
Canonical production gate: still failed.
Controlled runtime tier: owner-authorized for practical testing.
```

## Acceptance tier policy

A new intermediate standard was added:

```text
docs/MODEL_ACCEPTANCE_TIERS.md
```

The project now distinguishes:

```text
R0 = Research Baseline
R1 = Experimental Artifact Candidate
R2 = Controlled Runtime Candidate
R3 = Production Candidate
R4 = Production Approved
```

Student-4-v2.2A is not R3/R4.

Student-4-v2.2A is allowed as R2 only because the owner explicitly accepted that practical runtime testing is useful even before production-level perfection.

## Current objective

Produce a mixed/head-protected INT8 artifact for Student-4-v2.2A as an experimental controlled runtime candidate.

This is not a production approval.

The artifact must be labelled:

```text
OWNER_APPROVED_CONTROLLED_RUNTIME_CANDIDATE
FAILED_CANONICAL_DEV_GATE_CARRY_OVER_ALLOWED
FROZEN_UNREAD
NOT_TECHNICALLY_PRODUCTION_VALIDATED
```

## Baseline

Student-4-v2.1 is closed as:

- `STOPPED_FOR_REVIEW`
- `FAILED_DEV_GATE`
- `DO_NOT_PROMOTE`

Important v2.1 failure signals:

- Matrix exact-set `0.719577`
- Matrix negation F1 `0.509169`
- P0.5 exact-set `0.45`
- P0.5 predicate `0.75`
- Ownership corruption `2`, both Italian
- Residuals: span decoding `269`, semantic classification `99`, entity resolution `40`, authority/referent decoding `20`

## Student-4-v2.2A training result

Workflow:

```text
Matrix-NLU Student-4 V2.2A Controlled Repair
Run: 33860928806
Job: 100984948899
Commit: 617aeca8a6abac4366eb13347fb88026307dc3b8
Conclusion: success
```

Completed steps:

- software regression tests;
- v2.2A train-only repair dataset build;
- immutable v2 data audit;
- MASSIVE auxiliary supervision preparation;
- fresh Student-4-v2.2A training;
- development-only controlled evaluation;
- checksums and frozen guard;
- report/bundle/resume artifact upload.

Artifacts:

```text
matrix-nlu-student-4-v22a-report-33860928806
id: 9938144318
size: 302085 bytes
digest: sha256:e71e153509e8f002fd74782ebb5667bb93b59438e6646c4c11723afe4be64129

matrix-nlu-student-4-v22a-bundle-33860928806
id: 9938150338
size: 217603720 bytes
digest: sha256:f2dfea052df525af741f8ddd98e279b5443645450d09f949970a6eac18edb987

matrix-nlu-student-4-v22a-resume-33860928806
id: 9938165358
size: 650269442 bytes
digest: sha256:ff66bd687fc55f1b767164b84795ad84aba4937130b7d8b0aead9afff5f018cd
```

## v2.2A dev verdict

Controlled stop result:

```text
decision = STOPPED_FOR_REVIEW
selectionStatus = FAILED_GATE
selectedThreshold = null
frozenDataRead = false
frozenEvaluationExecuted = false
onnxExported = false
quantizationExecuted = false
```

This remains true.

The owner-approved intermediate tier does not rewrite this as a pass.

## Key metrics observed

Matrix dev:

```text
observations = 756
goldClaims = 972
predictedClaims = 972
claimCountExact = 1.0
exactClaimSet = 0.6798941798941799
claimExact = 0.7139917695473251
fieldExact = 0.9597622313671696
spanF1 = 0.9397748747021609
entityF1 = 0.980291683090264
validCoverage = 1.0
validSelectiveAccuracy = 0.7139917695473251
ownershipCorruption = 0
worldTruthUpdates = 0
negationF1 = 0.49064449064449067
temporalAccuracy = 0.9567901234567902
```

Matrix dev by language:

```text
EN exactClaimSet = 0.8968253968253969
ES exactClaimSet = 0.5238095238095238
IT exactClaimSet = 0.6190476190476191
```

P0.5 dev:

```text
observations = 60
goldClaims = 84
predictedClaims = 84
claimCountExact = 1.0
exactClaimSet = 0.5166666666666667
claimExact = 0.6547619047619048
fieldExact = 0.9153439153439153
spanF1 = 0.9759162303664921
entityF1 = 0.9036697247706422
validCoverage = 0.9404761904761905
validSelectiveAccuracy = 0.6962025316455697
ownershipCorruption = 2
worldTruthUpdates = 0
negationF1 = 1.0
temporalAccuracy = 0.8809523809523809
```

P0.5 dev by language:

```text
EN exactClaimSet = 0.6
ES exactClaimSet = 0.5
IT exactClaimSet = 0.45
```

## Interpretation

Student-4-v2.2A is not production-ready, but it is useful enough to test in a controlled runtime architecture.

Strong points:

- training completed;
- regression tests passed;
- frozen remained unread;
- artifacts preserved;
- Matrix claim count is exact;
- Matrix ownership corruption is zero;
- EN is strong;
- P0.5 negation improved strongly;
- world truth updates remain zero.

Weak points:

- canonical dev gate failed;
- selected threshold is null;
- Matrix negation remains weak, especially IT/ES;
- P0.5 ownership corruption still exists;
- request/correction/third-party remain weak;
- model confidence is too high relative to actual exact correctness;
- semantic classification and span decoding residuals remain significant.

## Mandatory runtime containment

Student-4-v2.2A may only be used as an NLU proposal source behind the controlled architecture:

```text
NLU proposal
→ Semantic Consistency Controller
→ Authority Resolver
→ Memory Admission
→ Affective Engine
→ Prompt Builder
→ GGUF
```

The NLU must not:

- decide truth by itself;
- write memory;
- change persistent affect;
- assign Luna as target unless explicitly present or context-bound;
- turn third-party reports into world truth;
- turn questions/requests into stable facts.

## Quantization decision

Owner-authorized quantization mode:

```text
Mixed / Head-Protected INT8
```

Quantize:

```text
encoder / backbone
```

Protect in FP32:

```text
token.boundary
token.object
token.subject
token.negation
token.temporal
token.entity
sequence.dialogueAct
sequence.predicate
sequence.subjectReferent
sequence.targetReferent
sequence.ownerReferent
sequence.perspectiveReferent
sequence.polarity
sequence.temporalRelation
sequence.claimKind
```

Required manifest labels:

```text
acceptanceTier = R2
productionApproved = false
frozenDataRead = false
frozenEvaluationExecuted = false
canonicalDevGatePassed = false
ownerRuntimeOverride = true
```

## Files already added for mixed quantization

- `matrix_nlu/export_mixed_head_protected_onnx.py`
- updated `matrix_nlu/test_export_onnx.py`
- `.github/workflows/matrix-nlu-student-4-v22a-mixed-quantization.yml`
- `docs/MODEL_ACCEPTANCE_TIERS.md`

Relevant commits:

```text
8fe6faf523469b453dcf8f1ee023656f236b3447
202b4ff0b431a91ca5da0aac2380a46b7580d827
2d4efa2f9abd390175daedab6810b59ef52413d5
4756962baac25317c4e8d14f7e6d85b728a69958
1fc9001a016148b521880add2e074a62fd117397
```

## Known issue to resume from

The first mixed/head-protected quantization workflow run failed immediately:

```text
Workflow: Matrix-NLU Student-4 V2.2A Experimental Mixed Quantization
Run: 33882172879
Head SHA: 2d4efa2f9abd390175daedab6810b59ef52413d5
Conclusion: failure
```

The job log was not retrievable through the connector at the time of handoff.

Work should inspect the run directly and fix only the minimal cause.

## Next exact actions for Work

1. Inspect failed run `33882172879` directly from GitHub Actions.
2. Fix the minimum issue in the mixed quantization workflow/script.
3. Do not rerun training.
4. Do not read frozen.
5. Do not edit dev/test/frozen data.
6. Export FP32 ONNX reference.
7. Export mixed/head-protected INT8 ONNX.
8. Verify parity FP32 vs mixed INT8.
9. Record file sizes, SHA256, protected heads, excluded nodes and latency.
10. Upload artifact:

```text
matrix-nlu-student-4-v22a-mixed-head-protected-<run_id>
```

11. Preserve labels:

```text
OWNER_APPROVED_CONTROLLED_RUNTIME_CANDIDATE
FAILED_CANONICAL_DEV_GATE_CARRY_OVER_ALLOWED
FROZEN_UNREAD
NOT_TECHNICALLY_PRODUCTION_VALIDATED
```

## Final rule

```text
Do not chase perfection before runtime testing.
Do not pretend runtime testing equals production approval.
```


## Local quantization checkpoint 1 — source verified

Timestamp: `2026-09-04T14:40Z`

GitHub-hosted runners remained unavailable before checkout, so the owner authorized continuing in an isolated local runtime without waiting for GitHub Actions.

Authoritative source:

```text
trainingRunId = 33860928806
trainingRunHead = 617aeca8a6abac4366eb13347fb88026307dc3b8
bundleArtifactId = 9938150338
bundleArtifactName = matrix-nlu-student-4-v22a-bundle-33860928806
bundleArchiveSha256 = f2dfea052df525af741f8ddd98e279b5443645450d09f949970a6eac18edb987
modelStateSha256 = 446b6a58265500001efd350f81d75867227cbfd3c6da699ed9c9330257d16a9c
```

Verification:

- GitHub artifact digest matched the downloaded archive byte-for-byte;
- archive integrity passed;
- archive contains only runtime bundle files: `training-result.json`, `labels.json`, `model-state.pt`, and tokenizer files;
- no train/dev/test/frozen dataset is present or read;
- `studentLayers = 4`;
- `trainingSplitsRead = [train, dev]`;
- `frozenDataRead = false`;
- five mixed-export policy regression tests passed locally;
- no retraining, gate change, production promotion, or dataset modification occurred.

Active labels remain:

```text
EXPERIMENTAL_TEST_CANDIDATE_NOT_PRODUCTION_APPROVED
FROZEN_UNREAD
FAILED_DEV_GATE_CARRY_OVER
```

Next action: export FP32 ONNX, quantize encoder/backbone dynamically to INT8 while excluding every Matrix semantic head, then verify parity and CPU latency.


## Local quantization checkpoint 2 — bundle checkpoint defect

Timestamp: `2026-09-04T14:44Z`

The pinned local environment and five export-policy tests completed successfully. The immutable encoder revision `36de33ec579e47f6c4e10d982d0b93871267c3e6` downloaded successfully after increasing only the transport timeout.

Loading the preserved bundle then exposed a real artifact defect:

```text
model-state.pt bytes = 203292672
model-state.pt sha256 = 446b6a58265500001efd350f81d75867227cbfd3c6da699ed9c9330257d16a9c
PyTorch error = PytorchStreamReader failed reading zip archive: failed finding central directory
ZIP EOCD signature = absent
```

The checksum matches the run record, so the local download is intact; the file preserved in the bundle itself is incomplete as a PyTorch ZIP container. No ONNX file or quantized output was accepted from this attempt.

Recovery action within the existing authorization: inspect the resumable checkpoint artifact from the same authoritative run `33860928806` and recover the exact trained state if a valid loadable checkpoint is present. This is not retraining and does not access datasets.

Constraints remain unchanged: `FROZEN_UNREAD`, `FAILED_DEV_GATE_CARRY_OVER`, and `EXPERIMENTAL_TEST_CANDIDATE_NOT_PRODUCTION_APPROVED`.


## Local quantization checkpoint 3 — exact state recovered

Timestamp: `2026-09-04T14:49Z`

The resumable artifact exceeds the connector's 512 MiB transfer ceiling, so it was not partially downloaded or altered. A safe recovery mirror was found in the immediately preceding deterministic v2.2A run `33860905849`.

The recovered `model-state.pt` is cryptographically identical to the model state declared by authoritative run `33860928806`:

```text
expected modelStateSha256 = 446b6a58265500001efd350f81d75867227cbfd3c6da699ed9c9330257d16a9c
recovery mirror sha256     = 446b6a58265500001efd350f81d75867227cbfd3c6da699ed9c9330257d16a9c
PyTorch loadable           = true
state entries              = 102
parameter values           = 58599411
```

The local recovery bundle combines the authoritative run's `training-result.json`, `labels.json`, and tokenizer with that exact-checksum model state. This does not substitute another trained model: the recovered bytes match the authoritative model checksum exactly.

No retraining, dataset access, threshold change, frozen access, or production promotion occurred. Next action: execute FP32 ONNX export and mixed/head-protected dynamic INT8 quantization.


## Local quantization checkpoint 4 — verified artifact assembled

Timestamp: `2026-09-04T17:05Z`

The mixed/head-protected export completed locally from the exact model state of authoritative training run `33860928806`. The technical fix was limited to selecting quantizable nodes by encoder node name, preventing non-encoder nodes that merely consume encoder values from entering the INT8 selection set.

Implementation and regression-test commits:

```text
exportImplementationCommit = d77354ffb51fb9fa0cee8cca6dc5448ad09b2c68
verificationTestCommit      = 0098d4e8fa953665d38006d22d74ab479d94b4c9
unitTests                    = 6/6 PASS
```

Artifact identity:

```text
localExecutionId = local-20260904T1440Z
artifactName = matrix-nlu-student-4-v22a-mixed-head-protected-local-20260904T1440Z.zip
artifactBytes = 356134801
artifactSha256 = 4998ce2f44dd8553d75f86b8d7975529f6a5f779de9107eef393648022d6ccb5
archiveIntegrity = PASS
payloadChecksums = 13/13 PASS
```

ONNX files:

| Model | Bytes | SHA-256 |
|---|---:|---|
| FP32 reference | 234454909 | `11c4f9e10c85badd1afa425cfe5f431035ec3ab61b41425f26479e58c71eb0d3` |
| Mixed / Head-Protected INT8 | 149711344 | `738a4d052790367509d55487b649b71aaa029d839135693bb5be46f74d55ef70` |

The mixed model is 36.144931% smaller. The local 30-repetition CPU benchmark measured median latency of 7.900361 ms for FP32 and 4.428863 ms for mixed INT8 (1.783835x median speedup); p95 was 22.984074 ms and 19.327552 ms respectively.

Structural verification:

- both ONNX graphs pass `onnx.checker` and initialize with ONNX Runtime CPU;
- 32 encoder linear nodes were selected, producing 24 `MatMulInteger` nodes;
- every quantized linear operator is under `/model/encoder/`;
- 24 protected exclusion names cover native head nodes and ONNX Runtime Gemm-to-MatMul rewrites;
- 15/15 Matrix heads resolve to FP32 compute operators and FLOAT initializers;
- protected-head violations: zero;
- `token.negation` is `/model/negation/MatMul` with a FLOAT initializer and is not quantized;
- MASSIVE auxiliary heads remain outside the mandatory protection surface.

Protected token heads:

```text
token.boundary
token.object
token.subject
token.negation
token.temporal
token.entity
```

Protected sequence/semantic heads:

```text
sequence.dialogueAct
sequence.predicate
sequence.subjectReferent
sequence.targetReferent
sequence.ownerReferent
sequence.perspectiveReferent
sequence.polarity
sequence.temporalRelation
sequence.claimKind
```

Parity evidence:

- direct FP32-vs-mixed logit argmax: 77/102 output/probe comparisons;
- protected-head argmax: 73/90 comparisons;
- decoded semantic result: 5/6 probes exact;
- decoded negation spans: 6/6 exact;
- the only decoded semantic difference was `sequence.dialogueAct` on the Spanish probe; its head remains FP32 and the difference is an indirect effect of the INT8 encoder representation.

This parity result is evidence for controlled runtime testing, not a production gate pass. The artifact includes the FP32 reference, mixed INT8 model, manifest, per-head validation report, decoded parity evidence, `SHA256SUMS`, `FROZEN_GUARD.txt`, labels, tokenizer and non-weight runtime configuration.

Final carry-over state:

```text
productionStatus = EXPERIMENTAL_TEST_CANDIDATE_NOT_PRODUCTION_APPROVED
productionApproved = false
frozenStatus = FROZEN_UNREAD
decisionCarryOver = FAILED_DEV_GATE_CARRY_OVER
sourceDevDecision = STOPPED_FOR_REVIEW_FAILED_DEV_GATE
frozenDataRead = false
frozenEvaluationExecuted = false
frozenPredictionsRead = false
retrainingExecuted = false
productionPromotionExecuted = false
```


## Local quantization checkpoint 5 — durable artifact handoff

Timestamp: `2026-09-04T17:12Z`

The verified ZIP was persisted without changing its bytes. Resume identifiers:

```text
artifactFileId = file_00000000c5f08230a3c38ae78b8801d2
artifactLibraryFileId = libfile_f6171d59f4e481918e6a82698e6441c5
artifactSha256 = 4998ce2f44dd8553d75f86b8d7975529f6a5f779de9107eef393648022d6ccb5
artifactBytes = 356134801
```

The archive passed `unzip -t`; its internal `SHA256SUMS` verified every one of the 13 payload files. The handoff does not change the model decision or authorize frozen evaluation or production promotion.
