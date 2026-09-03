# Controlled stop — P0.5 OpenNLP work preservation

Date: 2026-09-03  
Status: **STOPPED AS PRODUCTION DIRECTION; RETAINED AS BASELINE / ORACLE / FALLBACK**

## Scope preserved

The OpenNLP P0.5 branch of work is intentionally stopped before any mapper
patch intended to turn Candidate B into the production solution. Nothing from
this checkpoint was integrated into the production Matrix repository.

The following completed work remains valid and reproducible:

- clean Italian dataset selection, license/provenance boundary and immutable
  source manifest;
- automated MarkIT download, integrity verification, CoNLL-U conversion,
  OpenNLP training, dev-only variant selection and frozen-test evaluation;
- three trained Italian POS variants and their checksums;
- expanded pre-fix Matrix gold: 88 scenarios / 264 IT/EN/ES utterances;
- integrity tests and a unified pre-fix A/B benchmark;
- Android/offline probe build from the unchanged P0 Candidate B path.

## Commit trail

| Commit | Preserved result |
|---|---|
| `263690efbe76fe05655909ccdcd4ce2c9fe0dfc6` | Clean Italian data plan |
| `cd801e169deb68170efc7592db948cc482dd17ca` | Reproducible trainer implementation |
| `84be3d3b2aef8d368ed518dd49d6060f806206f5` | Trainer exercised by CI |
| `47d9b15ce09af75d89e05677b39069ba6ede6cb8` | OpenNLP 2.5 API compatibility fix; successful training run |
| `86cd30db7bb3b12f52bf70e198a38f29f961de10` | Expanded gold frozen before mapper fixes |
| `cf1a7b990bf587f696a2e289fb7071a3e7cfa8ad` | Expanded pre-fix benchmark automated in CI |

No P0.5 semantic mapper fix was applied. In particular, article
normalization, modal goal/preference, imperative detection and
temporal/entity-exclusivity remain the known Candidate B residual families;
they are evidence for the learned Matrix-NLU, not a mandate to accumulate new
production rules.

## Clean Italian training snapshot

Source: UD Italian MarkIT at
`e210079df0aea331ec1dcaa90648d815ce94c3ce`, `CC BY 4.0`.

| Variant | Dev token accuracy | Bytes | SHA-256 | Disposition |
|---|---:|---:|---|---|
| perceptron-i100-c1 | **0.926243** | 126,860 | `14dca59954129b1f4554def4e16d1b626160f0289ab568f5a1efdd2d1bba91c7` | Selected fallback artifact |
| maxent-i200-c1 | 0.920473 | 417,199 | `40f5ad3d39a334711dd13750b1d8f3be9e8004a4e0676ba11af65a50bd7d595c` | Retained experiment |
| maxent-i100-c1 | 0.920281 | 416,913 | `d9dae43d0c3cc0eb0e6671063ea4b59122f4f8a506de1a5e343dd60e812a9fdc` | Retained experiment |

Selected frozen-test token accuracy: `0.920851`. The committed training
manifest contains source SHA-1/SHA-256, normalized split hashes, sentence/token
counts, tool versions, parameters, selection rule and attribution.

CI run `33781321112` at `47d9b15…` was `SUCCESS`. Its `p05-training` artifact
id is `9903733326`, archive SHA-256
`cd391f1e6c9077e844c154098a32a8d520d165c50d7c7447e6c8e3d2a6ef3d99`.

## Expanded pre-fix benchmark snapshot

Gold: `gold/p05-gold-v1.json`, SHA-256
`08c216641bdc071059c5dfd261a271dedc481a6879705ffb06c57164f01b9ea1`.
The benchmark was frozen and committed before any P0.5 mapper modification.

| Metric | A frozen baseline | B original OpenNLP/Matrix |
|---|---:|---:|
| Cases | 264 | 264 |
| Field exact | 0.734115 | **0.985129** |
| Frozen-test field exact | 0.736549 | **0.980344** |
| Claim-count exact | 0.875000 | **1.000000** |
| Source-span F1 | 0.878136 | **1.000000** |
| Negation-scope F1 | 0.603448 | **0.937500** |
| Entity type/link F1 | 0.340426 | **0.766169** |
| Ownership violations | 42 | **0** |
| Invented World Truth | 0 | **0** |
| Worst-language field exact | EN 0.626033 | IT 0.981481 |

This is evidence of a strong fallback, not a production verdict. The entity
score, limited gold scale and rule-based linguistic mapper remain material
weaknesses.

CI run `33782429036` at `cf1a7b9…` was `SUCCESS`. Artifacts:

- `p05-baseline`, id `9904168628`, archive SHA-256
  `99b63ea1360235932d627db99cc82e4b334bd28934634482e29f16ed5d5cf38f`;
- `p05-training`, id `9904168033`, archive SHA-256
  `1c5ff404cabdb51b3e67dc3dee4b9b31bb82d793e16a29d935bee5d0e92fd9f7`;
- `p0-android-probe`, id `9904169547`, archive SHA-256
  `14fcdc3a3d5a8c096ab8f77ff985fba059c4c56f73dee4fedd16a566b9e49cc3`.

## Preserved repository artifacts

`artifacts/p05-opennlp-baseline/` contains the exact three model binaries,
training manifest, MarkIT license notice, and expanded benchmark JSON/Markdown
from the successful CI runs. The raw upstream corpus is not duplicated in Git:
it remains byte-addressed and reproducibly fetched from immutable URLs by the
committed trainer.

## Gate disposition

- Old P0.5 Gate 00–03: completed and preserved.
- Old P0.5 Gate 04–09: stopped; no production promotion.
- Candidate B: baseline/oracle/fallback only.
- Moto G56: not requested and not executed for this stopped direction.
- Production Matrix runtime: untouched.

The next work must follow `docs/FINAL_MATRIX_UNDERSTANDING_ARCHITECTURE.md` at
`cf6395b0fefc254febe3c804751ca4b048f974d1`, after that file is read
integrally. This handoff does not pre-empt or reinterpret the new canonical
acceptance criteria.
