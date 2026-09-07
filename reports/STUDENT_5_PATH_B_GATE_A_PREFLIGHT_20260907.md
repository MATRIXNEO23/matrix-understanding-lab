# Student-5 Path B — Gate-A preflight, 2026-09-07

## Result

**GATE_A_BLOCKED_INPUT_ACCESS — workstream NOT COMPLETE.**

This is an input-acquisition/environment blocker before physical model loading. It is not a BERT, ONNX, training, or quality failure. No new model candidate was produced. Existing historical structural tests are not reasserted as physical evidence.

## Execution identity

- Repository: `MATRIXNEO23/matrix-understanding-lab`.
- Branch: `student5-path-b-v3` (not main).
- HEAD start: `aca5968bc26f8d4d4ef22327f0d225b9685e1474`.
- Persistent preflight checkpoint: `4c010cf99f022662394405870aaada0b043d84ff`.
- Local execution label: `student5-path-b-v3-preflight-20260907-aca5968`, identifying this interactive Work preflight, not a GitHub run.
- HEAD final: the commit introducing this report and CP32; use its Git history, not a fabricated self-referential hash.
- TASK 2.3 remains accepted and was not rerun.

## Sources read

The full current continuity and linked CP01–29 archive were read, together with every mandatory source from the assigned package:

1. PROJECT_WORK_RULES.md
2. docs/MODEL_ARTIFACT_PERSISTENCE_POLICY.md
3. docs/WORK_CONTINUITY_STUDENT_5.md and its immutable history archive
4. docs/STUDENT_ARTIFACT_REGISTRY.md
5. ARCHITETTURA.md
6. docs/MATRIX_NLU_CONTRACT_V3.md
7. reports/STUDENT_5_TRAIN_V3_MIGRATION.md
8. reports/STUDENT_5_15_HEAD_CONTRACT_AUDIT.md
9. reports/STUDENT_5_CONTRACT_REPAIR_DESIGN.md
10. prompts/WORK_STUDENT_5_ADULT_INTIMACY_ADDENDUM.md
11. docs/ADULT_INTIMACY_NLU_COVERAGE.md (required by addendum)
12. prompts/WORK_STUDENT_5_PATH_B_V3_COMPLETION.md
13. matrix_nlu/model_v3.py and matrix_nlu/export_onnx_v3.py

Repository tree metadata was inspected without opening dataset partitions. No AGENTS.md exists in the inspected tree. The existing exporter file provides the structural specification (opset, axes and names); it does not itself execute torch.onnx.export. No alternative exporter or contract redesign was introduced.

## First failing layer and exact evidence

**A1 — acquire the canonical pristine archive.**

The authenticated GitHub connection successfully read [asset 545406840 metadata](https://api.github.com/repos/MATRIXNEO23/matrix-understanding-lab/releases/assets/545406840):

| Evidence | Observed value |
|---|---|
| Release ID / tag | 383143636 / student-5-minilm-40k-phase-a-pristine |
| Asset | student5-minilm-phase-a-pruned-40k.zip |
| Asset state | uploaded |
| Bytes | 88,361,246 |
| GitHub digest | sha256:7804bfb245b71df9b835fff7ee00f6ec887e019772ae34c82d269d821d587191 |
| Metadata versus canonical expected identity | MATCH |
| Independent checksum of downloaded archive | NOT EXECUTED |
| Model checksum / tokenizer alignment / reload | NOT EXECUTED |

The direct unauthenticated Release download URL returned HTTP 404 at 2026-09-07T04:01:10Z. The repository is private. This does **not** mean the asset disappeared: the authenticated metadata proves it remains present.

The available authenticated connector explicitly rejects binary/non-UTF-8 responses through its fetch operation. Its advertised binary-download operation supports GitHub Actions artifacts, not Release assets. No advertised Release-binary download/upload operation or configured local GitHub token was available. No token was extracted from the connector, proxy, unrelated tool, or account.

Filename search in the current workspace, /tmp and installed runtime tree found no named Student-5/MiniLM/pristine copy. This is a bounded search, not a claim that no copy exists anywhere.

## Local environment and remote-runner evidence

- Python: 3.12.13.
- Missing modules: torch, transformers, onnx, onnxruntime, sentencepiece.
- NumPy present.
- PyPI responded HTTP 200: package installation may be feasible. Missing packages alone are not a network/access blocker, and no installation attempt is claimed.
- Installing dependencies cannot supply the authenticated private pristine archive. No model operation was started without the exact input.
- Zero GitHub Actions runs were returned for the execution branch.
- Latest existing main run [34080903226](https://github.com/MATRIXNEO23/matrix-understanding-lab/actions/runs/34080903226) failed with job 101615840792, no steps, and empty runner name. It was not launched or rerun by this work.
- Attempt to read its check-run annotations was rejected by the connector endpoint allowlist. No bypass was attempted. Billing/permissions/runner cause is **unverified**; this report does not infer the reason.
- No workflow was created and no remote execution was silently substituted for this Work session.

## Gate status

| Gate | Result |
|---|---|
| Branch/HEAD and mandatory source reading | DONE |
| Canonical Release metadata identity | MATCH, metadata only |
| A1 independent archive/model/tokenizer hashes | BLOCKED before download |
| A1 TRAIN-v1 checksums | PENDING; no migration repeated |
| A2 real pristine BERT + V3 16-head forward | NOT EXECUTED |
| A3 ONNX checker/load/forward/numerical parity | NOT EXECUTED |
| A4 retained new model artifact persistence | NOT APPLICABLE; no model produced |
| Gate B readiness/training | NOT STARTED |
| Gates C/D/E | NOT STARTED |

`P1-ENV-PHYSICAL-BERT-LOAD` and `P1-ENV-ONNX-EXPORT-LOAD` remain OPEN. This checkpoint does not close either with source inspection, fake encoders, random-only replacement models, or structural tests.

## Persistence and immutable boundaries

The preflight and STOP records are Git-tracked in the same repository, with machine-readable diagnostics and SHA256SUMS. The historical CP01–29 archive is not edited. Only new diagnostic/report files and current Student-5 continuity are changed.

No binary was downloaded, regenerated, overwritten, deleted, repackaged or published. Student-4, pristine, Path A, all prior candidates, TRAIN v1, DEV and Frozen were not modified. The artifact registry is unchanged because no new model artifact exists. The physical hashes of preserved binaries were not independently recomputed in this session.

## Exact work remaining

1. Restore a normally configured authenticated path for reading the canonical private Release binary and publishing new uniquely named repository-owned binaries. No new model/task authorization is needed; this is an execution capability requirement, not a request for the owner to recreate/download source files manually.
2. Resume A1 at the latest branch HEAD; re-read continuity, download asset 545406840, verify archive bytes/SHA and all internal canonical identities, verify TRAIN v1 checksums without modifying it.
3. Install the pinned compatible runtime in an isolated environment; perform A2 on the real pristine BERT/tokenizer and existing V3 adapter, with no optimizer/backprop.
4. Execute A3 using the existing V3 structural export contract: physical ONNX load/forward, numerical parity, all 17 expected tensors for 16 conceptual heads, candidate/anchor masks, dynamic shapes, and fingerprint.
5. Persist any retained Gate-A export under a new immutable version before considering A closed.
6. On A PASS, continue automatically to Gate B under the already-authorized package. First identify permitted V3 DEV data, evaluation boundaries and acceptance criteria. Missing evaluation contract is a STOP, not license to reinterpret V2.
7. Address known coverage risks only through new versioned TRAIN data, never by overwriting accepted v1: BELIEF/COMMAND zero, eight Italian REPORT claims, advanced temporal relations zero, one Italian withdrawal, absent pointer ambiguity gold, 1,561 repeated text instances.
8. Follow the frozen-backbone-first capacity ladder; preserve every meaningful candidate before escalation. Real DEV family/language analysis, TRAIN-only repair, and independent evaluator evidence are required.
9. Gates C/D: lock taught FP32, durable reference/export, separate head-protected quantization, semantic/numerical parity and runtime evidence.
10. Gate E only after candidate/thresholds/recipe lock: one final Frozen evaluation, never feedback tuning. No production promotion or Assembling integration.

## Guards

```text
student4V22AChanged = false
pristine40kModified = false
pathAModified = false
trainV1Modified = false
canonicalDevUsed = false
frozenDataRead = false
frozenDataTokenized = false
frozenDataAnalyzed = false
frozenPredictionsRead = false
optimizerCreated = false
backpropExecuted = false
trainingExecuted = false
teachingExecuted = false
quantizationExecuted = false
otherRepositoriesModified = false
productionPromotionExecuted = false
workstreamComplete = false
```

STOP at Gate A input acquisition. No background run or deferred automatic completion is claimed.

