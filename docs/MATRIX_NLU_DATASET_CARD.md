# Matrix-NLU generated/curated dataset card

Status: `BUILDER LOCALLY VERIFIED / CI CONSOLIDATION PENDING`  
Generator: `matrix_nlu/build_dataset.py`  
Schema: `matrix.nlu.dataset.v1`  
Seed: `810923`

## Purpose

This dataset supervises the Matrix-specific learned heads that cannot be
obtained by copying MASSIVE labels: claim boundaries, dialogue act, predicate,
subject/target/owner/perspective referents, polarity and negation span,
temporality, entity/span types, claim kind and World Truth prohibition.

The templates are authoring infrastructure in the isolated lab. They are not
runtime parsers, regular expressions or fallback linguistic rules.

## Separation

Train, dev and frozen test use different surface-template families and disjoint
names, locations, preference objects and professions. The frozen test includes
multi-token places absent from train/dev and paraphrase structures that do not
appear in training. Multi-claim records contain two and three proposition-local
claims with shifted character spans.

The initial generated shape is:

| Split | Records per language before multi/adult additions | Role |
|---|---:|---|
| train | 700 | learned-head fitting only |
| dev | 180 | variant choice, calibration and causal fixes |
| test | 360 | frozen evaluation only; never tune |

The locally verified manifest is:

| Split | Records | Per language | Claims | SHA-256 |
|---|---:|---:|---:|---|
| train | 2,883 | 961 | 3,723 | `6f42718a0b25f32e8c3711148c72ac2ab6415bb57ca7161eb9ac6a8a589b8045` |
| dev | 756 | 252 | 972 | `aa19e414a5d5dd1bc3ec9c1e257b8224b568a2a7460a92f31875ce3741003177` |
| frozen test | 1,482 | 494 | 1,914 | `8f1b267fb9f1b76d0f304cd26d88dfcef82fd6434f5ea182985a164960effba2` |

CI must reproduce these hashes before training is authorized.

The P0.5 adapter preserves the original partitions as separate files:

| Split | Records | Claims | SHA-256 |
|---|---:|---:|---|
| train | 87 | 105 | `8426018bd4ec9d06c5bc9cfc0d668c2f8b4208add14a0a413694153f5f4ab95b` |
| dev | 84 | 108 | `b48753dc07adee70538e890473a2df08524260fdaec31d9946f2e5c57183582b` |
| frozen test | 93 | 111 | `5ef8f8bf6ed761df8f91dbd0dcc415d4b62c783759d6d10a229b4fba4c6ee505` |

The regression `non amo i locali affollati` is learned-head evidence with
`preference.like` and negative polarity; it is not implemented as a runtime
rule.

## Provenance and license

- All generated text and annotations in this layer are project-authored.
- Every row records generator seed, template split and source ID.
- External datasets are not copied into these JSONL files.
- MASSIVE remains a separate CC BY 4.0 auxiliary layer with its own immutable
  source digest and official partitions.
- P0/P0.5 real regressions remain separate frozen evidence and are not silently
  duplicated across partitions. The adapter emits P0.5 train/dev/test separately;
  training may consume only P0.5 train, selection only P0.5 dev, and final
  evaluation only P0.5 test.

## Adult-domain safety boundary

The canonical specification requires adult-character consent/refusal coverage.
This builder includes bounded, non-graphic grant/refusal utterances in all three
languages and all splits, tagged `adultOnly=true`. The validation gate rejects
minor/child terms in any adult-only row. It does not create sexual content
involving minors.

## Known limitations before training

- Generated paraphrases alone cannot prove real conversational robustness;
  MASSIVE auxiliary data, independent frozen P0/P0.5 regressions and additional
  noisy/adversarial evaluation remain mandatory.
- The initial dataset does not by itself calibrate uncertainty or abstention.
- A high score on this generator cannot satisfy the final quality gate if errors
  remain systematic by language or critical semantic family.
