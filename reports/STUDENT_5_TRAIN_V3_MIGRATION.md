# Student-5 TRAIN-only V2 → Matrix-NLU Contract V3 Migration

## 1. Executive verdict

`TRAIN_V3_MIGRATION_PASS_WITH_NONBLOCKING_RISKS`.

The canonical TRAIN-only artifact contains 3,150 rows and 3,990 flat atomic claims under `MATRIX_NLU_CONTRACT_V3`. All rows pass the V3 structural validator and target builder. The verdict carries coverage risks rather than migration failures: BELIEF and COMMAND are absent, report/source attribution is limited to eight Italian claims, advanced temporal relations are absent, adult withdrawal has one Italian row, and the inherited corpus contains 1,561 repeated texts.

No training, DEV/Frozen access, model mutation, Student-4 change, Path-A change, or production promotion occurred.

## 2. Start/final HEAD

- TASK 2.3 start: `f2bcf0beb85f1fab4c763ce1e7aaf5ceba1b1e04`
- Migration implementation used: `5e515ddadf9abe473ee2d99f34b8898df38da957`
- Durable artifact checkpoint: `117afd627ebe9f584b9328f1f78c63822980a49c`
- Final documentation checkpoint: recorded in the final task response.

## 3. TRAIN source inventory

| Source | Classification | Rows | Claims | Languages | Adult rows | Multi-claim rows | Schema |
|---|---|---:|---:|---|---:|---:|---|
| `matrix-v2-train` | AUTHORIZED_TRAIN_SOURCE | 2,775 | 3,615 | IT 925 / EN 925 / ES 925 | 108 | 699 | `matrix.nlu.dataset.v2` |
| `v22a-repair-train` | AUTHORIZED_TRAIN_SOURCE | 375 | 375 | IT 212 / EN 81 / ES 82 | 60 | 0 | `matrix.nlu.dataset.v2` |
| `p05-v2-train` | HISTORICAL_REFERENCE_ONLY / EXCLUDED | 30 recorded | 45 recorded | IT 10 / EN 10 / ES 10 | not opened | not opened | manifest evidence only |

`p05-v2-train` was not used because its TRAIN bytes were not durably separated from a combined source containing forbidden partitions. No combined source was opened.

## 4. Source provenance/checksums

| Source | SHA-256 | Provenance |
|---|---|---|
| Matrix V2 TRAIN | `5118d37ce2ab19d5be171f757f448698085e3c222a4a627f9838329836185820` | Canonical TRAIN-only generator output reconstructed with preserved train-drop metadata; checksum exact |
| v2.2A repair TRAIN | `8be02976d46ba47d746ff7307d688d93595453221965b3de995d4b1de655799f` | Explicit TRAIN member from authoritative report artifact `9938144318`; checksum exact |
| P0.5 V2 TRAIN, excluded | `413f60ca17879ed9de440add7903b6e2abaebdfbbed6055b32c6e0b105cadfcd` | Manifest evidence only; bytes not opened |

The complete per-family source inventory is machine-readable in `source-train-inventory.json`.

## 5. Migration classification counts

| Classification | Rows |
|---|---:|
| DIRECT_REUSE | 0 |
| DETERMINISTIC_MIGRATION | 0 |
| NEEDS_REANNOTATION | 3,150 |
| UNUSABLE | 0 |

All V2 rows need explicit reannotation because V2 cannot directly encode the new `sourceReferent`, five concrete pointer roles, cue-only negation evidence, V3 claim-kind registry, and field statuses.

## 6. DIRECT_REUSE

Zero. No V2 row already contained the exact V3 target contract.

## 7. DETERMINISTIC_MIGRATION

Zero final dispositions. Deterministic structure recovery is used inside controlled reannotation, but no row is classified as a lossless whole-row conversion.

## 8. NEEDS_REANNOTATION

All 3,150 eligible rows were reannotated with source row ID, original schema/provenance, changed fields, reason codes, contract version, and tool version. Exact row-ID catalogs are used for bounded corrections; they are not runtime language heuristics.

## 9. UNUSABLE

Zero after fail-closed repair. Earlier dry runs exposed 259 incomplete role mappings; these were resolved only when explicit V2 spans/context proved a unique identity. Multiple or absent candidate identities remain fail-closed in the migration tool.

## 10. Final V3 dataset

- Dataset ID: `student5-matrix-nlu-v3-train-v1`
- Contract: `MATRIX_NLU_CONTRACT_V3`
- Contract fingerprint: `7b0646e44243ad897760c0fcadbe141f1b8e88e3fd8d63a1789106571b9987b0`
- Rows: 3,150
- Claims: 3,990
- Retention: 100.0%
- Format: 63 ordered JSONL shards of 50 rows
- Logical dataset SHA-256: `1118a900026f48cfcc290c3f9dc52a1a019a6a1f4761661f326c33770523140e`
- Artifact checkpoint: [`117afd627ebe9f584b9328f1f78c63822980a49c`](https://github.com/MATRIXNEO23/matrix-understanding-lab/commit/117afd627ebe9f584b9328f1f78c63822980a49c)

## 11. Language distribution

| Language | Original eligible | Migrated | Reannotated | Unusable | Final |
|---|---:|---:|---:|---:|---:|
| IT | 1,137 | 1,126 | 1,126 | 0 | 1,126 |
| EN | 1,006 | 1,006 | 1,006 | 0 | 1,006 |
| ES | 1,007 | 1,007 | 1,007 | 0 | 1,007 |
| code-switch | 0 | 11 | 11 | 0 | 11 |

The 11 code-switch rows are the explicitly identified Italian adult/intimacy rows containing common English terms; they moved out of the IT count, so total retention remains 3,150.

## 12. Family distribution

| Capability | Rows | Claims | IT | EN | ES | Code-switch |
|---|---:|---:|---:|---:|---:|---:|
| Negation | 695 | 695 | 288 | 187 | 220 | 0 |
| Temporal | 2,463 | 2,622 | 950 | 830 | 831 | 11 |
| Referents | 838 | 838 | 303 | 260 | 275 | 0 |
| Source attribution / report | 8 | 8 | 8 | 0 | 0 | 0 |
| Belief | 0 | 0 | 0 | 0 | 0 | 0 |
| Hypothesis | 267 | 267 | 89 | 89 | 89 | 0 |
| Command | 0 | 0 | 0 | 0 | 0 | 0 |
| Request | 27 | 27 | 19 | 4 | 4 | 0 |
| Correction | 10 | 10 | 4 | 3 | 3 | 0 |
| Goal/desire | 627 | 627 | 245 | 192 | 190 | 0 |
| Ownership | 3,150 | 3,990 | 1,406 | 1,286 | 1,287 | 11 |
| Multi-claim | 699 | 1,539 | 513 | 513 | 513 | 0 |

## 13. Referent pointer distribution

| Head | Resolved | NONE | UNKNOWN | AMBIGUOUS |
|---|---:|---:|---:|---:|
| subjectReferent | 3,990 (100%) | 0 | 0 | 0 |
| targetReferent | 264 (6.616541%) | 3,726 (93.383459%) | 0 | 0 |
| ownerReferent | 3,990 (100%) | 0 | 0 | 0 |
| perspectiveReferent | 3,990 (100%) | 0 | 0 | 0 |
| sourceReferent | 3,990 (100%) | 0 | 0 | 0 |

All resolved targets point to a candidate present in the observation table. Forbidden V2 sentinels are zero. UNKNOWN is not used as a row-retention shortcut.

## 14. Source/perspective audit

- REPORT claims: 8
- BELIEF claims: 0
- `source == perspective`: 3,982
- `source != perspective`: 8
- source UNKNOWN: 0
- perspective UNKNOWN: 0

Representative audited row `mx-v22a-it-core-113`, “Giulia dice che non vuole venire a casa”: source and subject are `mention:m0` (Giulia), while perspective preserves the explicit V2 `ctx:speaker` evidence. The roles remain independent. Report coverage is Italian-only and is a P1 training-coverage risk.

## 15. Negation audit

- Negative rows/claims: 695/695
- Rows/claims with cue spans: 463/463
- Multiple-cue rows/claims: 13/13
- NEGATIVE polarity: 695
- POSITIVE polarity: 3,106
- POSITIVE polarity with overt cue: 0
- UNKNOWN polarity: 189

Representative cue-only spans were inspected in IT (`Non`), EN (`not`), and ES (`No`). The V2 full-claim negation span is never reused. The audited Spanish cross-lingual correction now records `No` at `[0,2]` and `NEGATIVE` independently.

## 16. Temporal/anchor audit

| Relation | Claims |
|---|---:|
| ATEMPORAL | 1,368 |
| CURRENT | 2,096 |
| PAST | 14 |
| FUTURE | 512 |
| BEFORE / AFTER / DURING / RECURRENT / AT_REFERENCE / UNKNOWN | 0 each |

Relations requiring V3 reference anchors: 0; valid anchors: 0; missing required anchors: 0. CURRENT/PAST/FUTURE claims use the speech-time anchor according to the frozen contract. Absence of advanced relations is a P1 coverage gap, not a validator failure.

## 17. Multi-span audit

- Multiple negation-cue spans: 13 claims
- Multiple subject spans: 0
- Multiple object spans: 0
- Multiple temporal evidence spans: 0

Plural arrays are present on every claim and all valid groups are preserved. Zero counts reflect the source evidence, not scalar decoding.

## 18. Multi-claim audit

699 rows contain multiple flat atomic claims, totaling 1,539 claims in this capability slice. Claim IDs are unique within every row; no recursive/nested claim structure was fabricated.

## 19. Adult/intimacy audit

Adult/intimacy remains ordinary linguistic evidence with no moderation label or confidence penalty.

| Slice | IT | EN | ES | Code-switch | Total claims |
|---|---:|---:|---:|---:|---:|
| Consent | 29 | 18 | 18 | 0 | 65 |
| Refusal | 26 | 18 | 18 | 0 | 62 |
| Desire | 30 | 0 | 0 | 0 | 30 |
| Withdrawal | 1 | 0 | 0 | 0 | 1 |
| English-term Italian code-switch family | 0 | 0 | 0 | 11 | 11 |

Representative withdrawal row `mx-v22a-adult-it-046`, “Non voglio continuare”, preserves cue `[0,3]`, NEGATIVE polarity, current speech-time relation, speaker ownership and observer target. All authored sexual data is adult-only.

## 20. UNKNOWN/NONE/AMBIGUOUS distribution

Across the five pointer heads: UNKNOWN 0, AMBIGUOUS 0; NONE occurs only for 3,726 target roles. Polarity UNKNOWN occurs on 189 claims. NONE and UNKNOWN remain distinct schema values. The lack of ambiguous pointer gold is a coverage risk for future teaching, not a migration error.

## 21. Contract validator results

V3 structural violations: **0** across all 3,150 rows. Specifically: zero invalid labels/head names, candidate pointers, forbidden sentinels, BIO/span structures, required anchors, field statuses, claim IDs, candidate IDs, contract fingerprints, or downstream-state fields.

## 22. Target builder results

- Rows loadable/buildable: 3,150 / 3,150 (100%)
- Training examples built by dry run: 7,140
- Invalid target rows: 0

This is target construction only. No model forward, optimizer, loss, backpropagation or training occurred.

## 23. Duplicate/conflict audit

- Duplicate row IDs: 0
- Duplicate claim IDs within row: 0
- Duplicate migrated provenance: 0
- Conflicting gold for identical language/text: 0
- Repeated language/text instances: 1,561

The repeated surfaces are inherited corpus redundancy and are retained with provenance; they are a nonblocking P1 risk for later training design.

## 24. Migration manifest

- Manifest: [`data/student5_v3/migration-manifest.json`](https://github.com/MATRIXNEO23/matrix-understanding-lab/blob/main/data/student5_v3/migration-manifest.json)
- Manifest SHA-256: `87b4a43035d2e3d84a6d599e1f81b497af6e2f36e4ef2c470adb87341c17da98`
- Tool version: `student5.task2.3.train-migration.v1`
- Provenance: 63 ordered JSONL shards, one record per eligible row
- Dataset: 63 ordered JSONL shards, 50 rows each

## 25. Artifact checksums

- Logical ordered TRAIN dataset: `1118a900026f48cfcc290c3f9dc52a1a019a6a1f4761661f326c33770523140e`
- Migration manifest: `87b4a43035d2e3d84a6d599e1f81b497af6e2f36e4ef2c470adb87341c17da98`
- Statistics: `11f5ff43ceea9a1de6e8a4e9149b4c8af0834290cf623f3c13db1c59acf0d5c4`
- Artifact files: 130
- Artifact file bytes: 13,137,799
- Per-file checksums: [`data/student5_v3/SHA256SUMS`](https://github.com/MATRIXNEO23/matrix-understanding-lab/blob/main/data/student5_v3/SHA256SUMS)

All entries in `SHA256SUMS` were verified locally after final generation. Git blob identities for the final changed files matched the locally computed Git blob hashes before the artifact checkpoint was committed.

## 26. Remaining risks

| Severity | Identifier | Status |
|---|---|---|
| P1 | P1-ENV-PHYSICAL-BERT-LOAD | OPEN; unchanged, needs TASK 2.4 physical evidence |
| P1 | P1-ENV-ONNX-EXPORT-LOAD | OPEN; unchanged, needs TASK 2.4 physical evidence |
| P1 | P1-DATA-BELIEF-COMMAND-ZERO | OPEN; no eligible TRAIN evidence, no augmentation authorized |
| P1 | P1-DATA-SOURCE-ATTRIBUTION-LANGUAGE | OPEN; 8 reports, IT only |
| P1 | P1-DATA-TEMPORAL-RELATION-COVERAGE | OPEN; no BEFORE/AFTER/DURING/RECURRENT/AT_REFERENCE |
| P1 | P1-DATA-ADULT-WITHDRAWAL-COVERAGE | OPEN; one IT claim |
| P1 | P1-DATA-DUPLICATE-SURFACES | OPEN; 1,561 repeated texts, zero conflicting gold |

P0 remaining: 0. P2 remaining: 0. These risks must not be hidden or treated as model-quality measurements.

## 27. Exact next task

```text
TASK 2.4 = NOT_STARTED
TASK 3 = NOT_STARTED
NEXT = AWAIT OWNER REVIEW BEFORE TASK 2.4
```

TASK 2.4 is the separately authorized physical Student-5 BERT load plus V3 ONNX export/load closure. This report does not authorize it.

## Guards

```text
Student-4 changed = false
DEV used = false
Frozen read = false
Path A modified = false
Pristine 40k modified = false
Path B started = false
Teaching executed = false
Training executed = false
Other repos modified = false
productionStatus = NOT_PRODUCTION_APPROVED
```
