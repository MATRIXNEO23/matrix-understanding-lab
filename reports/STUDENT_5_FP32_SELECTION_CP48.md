# Student-5 CP48 — checkpoint selection blocked

`STUDENT5_FP32_SELECTION = BLOCKED_MISSING_CANONICAL_EVAL_SET`

Starting HEAD: `045b5f06ea6ce0371d3e3e5a14cbeb5864f3d0ef` on `MATRIXNEO23/matrix-understanding-lab/main`.

No existing authorized Student-5 V3 checkpoint-selection set could be authenticated. Dataset ID, recoverable locator, expected SHA-256, and provenance tying the split and V3 targets to checkpoint selection remain missing. This is a recovery result, not proof that no such set exists anywhere. The historical name need not contain “DEV V3”.

`CHECKPOINTS_EVALUATED = 0`, not 10. Epochs 01–10 remain preserved and eligible in CP47 Release **384423046**, asset **549780835**. No winner, selected-model ID, selected Release/asset or selected-model SHA exists. All overall/per-head/language/semantic/regression metrics are **NOT_MEASURED**. No regression class or practical competitiveness can be assigned. TRAIN loss was not used to select an epoch.

## Search performed

- Both live branches and their complete recursive trees: main (615 entries) and student5-path-b-v3 (489 entries). The historical branch adds no unique dataset path; only four existing file blobs differ from main.
- All five Releases / 14 assets and five tags; these register pristine/working models, untrained probes and CP47 checkpoints, not an authenticated V3 selection corpus.
- All 306 Actions run records, 637 artifact records, 588 cache records and 11 workflow records, with pagination exhausted. Cache metadata identifies 584 Gradle, two pip and two Hugging Face model caches; no selection-data cache locator was identified.
- All 266 reachable main commit metadata records, plus repository commit searches for `dev`, `gold` and `selection`. This is not a claim to have opened every historical tree or ZIP.
- 24 pinned source documents, manifests, workflow/source files and continuity references. Every exact path/ref/blob SHA and relevant text location is listed in `source-document-register.json.gz`.
- Two targeted historical Actions archives: p05-training **10035624558** (run 34170700425) and Student-4 v2.1 post-dev **9927657001** (run 33848931720). The connector supplied references, but original and refreshed reference materialization failed HTTP 403; direct REST ZIP downloads failed HTTP 401. Their members and payloads were not inspected. Metadata/documents classify their historical roles; archive contents are an explicit access limitation.

## Historical material found and why it was not substituted

| Material | Established historical role | Missing requirement for this selection |
|---|---|---|
| matrix-v2-dev.jsonl / p05-v2-dev.jsonl | Student-4 / V2 validation; documentary SHA identities exist | Authorized Student-5 V3 identity/compatibility mapping; V2 negation and referent targets differ |
| P0 / P05 gold v1 | Original task gold with train/dev/test splits | Compatible V3 target evidence and Student-5 selection provenance; mixed payloads were not opened |
| MASSIVE DEV IT/EN/ES | Auxiliary intent/slot development | MATRIX V3 all-head referent/status/alternatives gold and selection linkage |
| Phase-A “selection corpus” | TRAIN-safe vocabulary pruning, 16,819 records | It is not held-out MATRIX NLU checkpoint-selection gold |
| V3 fixtures / CP35 Gate-A | Software contract tests / untrained runtime probe | Validated generalization gold and selection authorization |

The V3 migration documentation explicitly migrated TRAIN only. CP36 readiness, CP44 selection-input evidence, CP47 selection-status and the current canonical index all leave the authorized V3 selection identity unset. No silent DEV V2 substitution or new labels were created. Detailed documentary hashes, evidence paths and dispositions are in `candidate-set-register.json`; those historical dataset hashes were not freshly recomputed from gold payloads.

## Continuation input required

An **existing** selection dataset needs: dataset ID, exact recoverable path and commit or Release/asset locator, expected byte identity/SHA-256, and provenance establishing the permitted split, canonical V3 labels and checkpoint-selection role. Its historical name may differ. An authenticated link to the existing material resolves the present task blocker; neither retraining nor replacement data is requested.

CP47 training remains `TRAINING_COMPLETED_SELECTION_PENDING`. Existing model archive SHA-256 remains `029bc292c11091da3aa5742ac85017ffdbc7dbb7ba7be6fadc5cc603f07ceafa`; recovery instructions and all ten immutable identities remain in the CP47 index and Release. CP48 did not re-download models or alter those identities. G04 practical regression assessment remains unmeasured; G07 was not reopened.

## Persisted evidence and recovery

Evidence root: `reports/evidence/student5-fp32-selection-cp48/`.

- `result.json`: exact blocked handoff, missing identity and operation flags.
- `search-scope.json`: counts, artifact-name census and limitations.
- `candidate-set-register.json`: all plausible historical material and documentary identities.
- `checkpoint-comparison.json` / `.csv`: ten rows, all explicitly NOT_EVALUATED; original CP47 identity references retained.
- `source-document-register.json.gz`: 24 source paths, pinned Git blob identities and matching excerpts.
- `repository-metadata.json.gz`: branches/trees, Release metadata and commit-search results.
- `actions-runs-inventory.json.gz`, `artifacts-inventory.json.gz`, `caches-inventory.json.gz`, `commits-inventory.json.gz`, `tags-inventory.json.gz`, `workflows-inventory.json.gz`: complete enumerated metadata snapshots, with page evidence where collected.
- `archive-access-results.json`: actual failed archive acquisition routes; no signed URLs persisted.
- `SHA256SUMS`: SHA-256 for all CP48 evidence files except itself, plus this report.

Recover from the commit introducing this report, decompress JSON gzip files directly, and verify `SHA256SUMS` from the repository root. Remote content readback is verified after commit; the final response identifies the delivered commit. The canonical index and continuity are appended; no old artifact is overwritten.

```text
trainingExecuted=false
trainModified=false
devCreated=false
devModified=false
quantizationExecuted=false
onnxExecuted=false
assemblingIntegrationExecuted=false
student4Modified=false
frozenUsedForTraining=false
nextWorkStarted=false
```

STOP. No training, replacement data, selection by TRAIN loss, export or integration has been started.
