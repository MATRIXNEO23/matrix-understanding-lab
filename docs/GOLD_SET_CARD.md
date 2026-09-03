# P0 gold set card

## Identity and purpose

- ID: `p0.gold.v1`
- Frozen: 2026-09-03T10:10:00Z, before candidate implementation.
- Scope: Matrix Understanding contract only.
- Languages: Italian, English, Spanish; Italian is the primary product language.
- Shape: 22 parallel semantic scenarios, 66 utterance variants.
- Splits: S01-S07 train (21 variants), S08-S13 dev (18), S14-S22 test
  (27). The test split must not tune rules or model selection.

## Provenance

The utterances and Matrix annotations were authored specifically for this lab
from the frozen contract and mandatory families in
`P0_UNDERSTANDING_BENCHMARK_SPEC.md`. They are not copied from MASSIVE,
Universal Dependencies, OpenNLP model corpora, or the runtime test suite.
The three variants are parallel scenarios but are phrased naturally enough to
exercise language-specific grammar; they are not used as training data for any
third-party model.

License: repository project data, all rights retained by the repository owner.
No third-party text is redistributed.

## Coverage and limitations

All 17 required families occur at least once. This is a discriminating P0
dataset, not a production-scale language corpus. It is deliberately small and
must not be used to claim broad conversational accuracy or calibrated
confidence. A production decision requires later native-speaker expansion and
an independently held-out set.

Critical failures are owner/perspective leakage and invented World Truth. A
reported presence remains a reported claim in every language.

