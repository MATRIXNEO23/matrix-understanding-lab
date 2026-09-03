# MASSIVE 1.0 provenance — Matrix-NLU auxiliary layer

Status: `HASH OBSERVED / PINNED RE-RUN PENDING`  
Use: auxiliary request-intent and slot-span supervision only.  
Matrix ontology: unchanged; MASSIVE intent names are not Matrix predicates.

## Immutable source evidence

- Source URL:
  `https://amazon-massive-nlu-dataset.s3.amazonaws.com/amazon-massive-dataset-1.0.tar.gz`
- Archive bytes: `39,500,415`
- Archive SHA-256:
  `7df623fd2d300a4d235d6ee5bd396c9a28258d3a0ccb29abdb054506eba153f8`
- License: CC BY 4.0, as declared by the Amazon MASSIVE NOTICE and the archive
  license file.
- Archived license SHA-256:
  `c2e6ea015269147de02117ebdd91f30ef09831251f5345fa8365273b1db1d435`.
- First inventory CI: run `33785721399`, commit `ac723626...`.
- First inventory artifact: `matrix-nlu-massive-provenance`, id
  `9905327516`, archive SHA-256
  `0cabeed0e47c548c9f7f11bf4fe65de297514221cbf6c9fa1870e334188ff30d`.

The first run intentionally had no expected archive hash. Its manifest and
license are preserved under `artifacts/matrix-nlu/massive/`. The hash is now
pinned in `matrix_nlu/massive_source.json`; only a second matching CI inventory
turns this gate green.

## Locale inventory

Each of `it-IT`, `en-US` and `es-ES` contains 16,521 rows with the official
partition counts below.

| Partition | Rows per locale | Permitted use |
|---|---:|---|
| train | 11,514 | auxiliary fitting |
| dev | 2,033 | auxiliary selection/error analysis |
| test | 2,974 | one-way frozen auxiliary evaluation only |

All three locales expose 60 intents, 18 scenarios and the same 55 observed slot
types. Slot annotation counts are 16,154 (IT), 16,171 (EN) and 15,916 (ES).

## Adaptation boundary

MASSIVE was localized from SLURP and is strong evidence for multilingual
requests and token spans. It does not encode Matrix ownership, perspective,
World Truth authority, belief admission, corrections or free conversational
claims. Therefore:

- train/dev/test partitions stay separate;
- MASSIVE trains auxiliary intent/slot heads or encoder representations;
- no MASSIVE intent or slot is copied directly into a Matrix predicate without
  an explicit Matrix-labelled supervision example;
- final Matrix quality is measured on independent typed claims and real
  regressions, not inferred from MASSIVE accuracy;
- attribution/license files accompany every derived training artifact.
