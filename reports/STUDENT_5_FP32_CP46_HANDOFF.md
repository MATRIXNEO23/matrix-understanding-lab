# Student-5 FP32 CP46 — pre-flight stopped

STUDENT5_FP32 = BLOCKED

Starting HEAD: `241bc1abe6cad2856716c198f55430494f4811a7`.
Training was authorized, but no optimizer step was executed.

## Concrete failure

The newly acquired local CP45 archive failed the canonical pre-flight guard:

| Field | Expected | Independently observed |
|---|---|---|
| Archive bytes | 88,361,246 | 73,400,320 |
| Archive SHA-256 | `7804bfb245b71df9b835fff7ee00f6ec887e019772ae34c82d269d821d587191` | `8497ecf2167cf7948d954fe46301ca9b8e09024c30bc5af8828a818acad32980` |

`tools/student5_fp32/preflight.py:37` raised AssertionError and exited 1 before target replay.
The acquisition command had previously reported success and extracted an internal FP32 model with the expected 148,020,400 bytes / SHA-256 `d6e45891d1e0ec4ed023caaeb17c0dd0ae80a93b8bf877d275310b7f2837efa2`.
Two subsequent independent archive reads agreed on the shorter length and wrong hash.
The cause of this local discrepancy is **not established**.

This is not evidence that the durable CP45 Release is corrupt: live Release metadata retains the canonical size/digest, and the older CP45 remote-readback copy still verifies.
The owner's explicit instruction requires STOP on any unexpected pre-flight identity difference. No intact fallback copy was substituted after that failure.

## Preserved inputs and unfinished checks

- CP45 model ID: `student-5-minilm-40k-phase-a-fp32-working-copy`.
- Release `384399324`, asset `549697344`; [unchanged durable locator](https://github.com/MATRIXNEO23/matrix-understanding-lab/releases/tag/student5-minilm-40k-phase-a-fp32-working-copy-cp45).
- TRAIN `student5-matrix-nlu-v3-train-v2.1-cp43r2`, SHA-256 `f90ae775a44023c37bf0c3a5087d64746413cbec770ca36cf154d1d533544aa4`: verified unchanged.
- Existing immutable CP44 target gzip SHA-256 `1c31639c65a958e5490378df4956c3d6f036def003eb93336704fb6ca97cda45`: verified, 4,355 examples.
- Fresh target-builder/G03 replay: not reached. Prior G03 PASS remains preserved, not newly reasserted.
- Current tree, canonical index, CP36/CP44 historical selection evidence and four Release inventories did not identify an authenticated V3 DEV. Missing selection is **not this stop reason** and remains nonblocking under the new authorization.
- G04/G07 and general TRAIN review were not reopened. No DEV or Frozen payload was used.

## Execution and persistence

Training started=false; completed=false; duration=0; checkpoints created=0; checkpoints persisted=0.
Selected checkpoint/model/Release/asset/SHA: NONE.
All requested quality, language, head, regression and competitiveness metrics: NOT_EVALUATED.
Improvement/regression: NOT_MEASURED.

The draft ten-epoch frozen-backbone plan is preserved as `unexecuted-run-plan.json`, explicitly NOT_EXECUTED; it is not a trainer, selected recipe, or trained artifact.
No model artifact or Release was created. This report, machine-readable failure evidence, draft plan, checksum index and continuity are the only new persisted outputs.
Remote repository readback is verified by the executor before final handoff; the delivery commit is the commit introducing this report.

Evidence: `reports/evidence/student5-fp32-cp46/preflight-blocked.json`.
Recovery for a separately resumed task: acquire or reuse verified CP45 bytes only; check complete stable archive size/SHA immediately before pre-flight. Do not use the 73,400,320-byte local archive. Existing CP45 recovery instructions and artifact identities remain unchanged.
STOP; no automatic retry or next phase.

```text
sourcePristineModified=false
workingCopyInitialSnapshotModified=false
trainModified=false
quantizationExecuted=false
onnxExecuted=false
assemblingIntegrationExecuted=false
student4Modified=false
frozenUsedForTraining=false
nextWorkStarted=false
```
