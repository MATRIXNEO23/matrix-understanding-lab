# Gate 03 — P0.5 expanded gold set card

Frozen: 2026-09-03T17:00:00Z  
Artifact: `gold/p05-gold-v1.json`  
SHA-256: `08c216641bdc071059c5dfd261a271dedc481a6879705ffb06c57164f01b9ea1`

## Shape

The P0.5 set contains 88 semantic scenarios and 264 independently localized
IT/EN/ES utterances. It preserves all 22 P0 scenarios and adds 66 new scenarios
before any P0.5 mapper fix.

| Split | Scenarios | Utterances | Permitted use |
|---|---:|---:|---|
| train | 29 | 87 | Component training and implementation evidence |
| dev | 28 | 84 | Variant selection and causal error analysis |
| test | 31 | 93 | Locked final measurement; not a tuning corpus |

The file is generated deterministically by `tools/build_p05_gold.py`. A repeated
generation must reproduce the byte-identical hash above. The recorded parent
P0 gold SHA-256 is
`85ae9320bea512cda2a3748bc49acc610a7b9d9dd17eee5222a2616faea6a99a`.

## Coverage added

- two- and three-claim coordination with mixed predicate types;
- negation confined to one proposition;
- person/location collisions and multi-token locations;
- six independent imperative verb families per language;
- modal goals separated from player preferences;
- past/future expressions co-occurring with locations;
- questions, hypotheses, recent-pronoun resolution and NPC-speaker ownership;
- explicit unknown, malformed, colloquial, lowercase-entity and code-switched
  input;
- corrections/supersession and preservation of provenance spans.

The benchmark does not introduce World Truth expectations. Ownership and
perspective retain zero-tolerance gates. Confidence is not evaluated as a
calibrated probability.

## Independence and leakage boundary

The new surface forms are not copies of the four original P0 residual strings.
They deliberately repeat semantic families while varying entities, objects,
verbs, proposition count and word order. The generator is an auditable authoring
mechanism, not runtime logic and not training-time data augmentation.

The frozen semantic test partition cannot update the POS model, a semantic
classifier, deterministic rules or hyperparameters. A test failure may justify
only a general causal correction that also passes distinct train/dev regressions;
every such iteration must be recorded rather than silently replacing this set.

## Gate 03 status

`PASS`: hundreds of IT/EN/ES utterances, frozen partitions, generation hash,
required adversarial families and integrity tests are present before P0.5 mapper
changes.
