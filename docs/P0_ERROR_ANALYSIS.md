# Gate 11 — P0 error analysis

Evidence: immutable `p0.gold.v1`, unified result from commit
`fa8b76b911321921a391845ccdbeda5177fe807f`, GitHub Actions run
`33743338928`. No test-set result was used to change A or B.

## Summary by required family

| Error family | A — frozen deterministic | B — ICU/OpenNLP/Matrix | Interpretation |
|---|---|---|---|
| Segmentation | 4 case-level count mismatches | 0 | A loses the second coordinated claim in EN/ES S12/S13; B reaches 66/66 exact claim counts |
| POS/morphology | Not available as a distinct A stage | 2 IT/ES request cases | OpenNLP tags imperative `Apri` as `PROPN` and `Abre` as `ADP`; the current request rule consequently does not fire |
| Predicate mapping | 97 main-field mismatches | 2 main-field mismatches | B strips the Italian presence article in S08-it and prioritizes English `like` over `would like` in S16-en |
| Entity resolution | entity F1 `0.4231` | entity F1 `0.9032` | B has six non-equal case entity sets, detailed below |
| Negation | 45 main polarity mismatches; scope F1 `0.6429` | 0 main-field mismatches; scope F1 `1.0000` | B passes local-negation cases, including coordinated one-claim negation |
| Temporality | 34 main-field mismatches | 0 | B passes past/current/future fields in the frozen set |
| Ownership | 8 actual owner/perspective violations; 18 owner-family field mismatches | 0 owner/perspective violations | B's two `ownership`-bucket errors are missing request `target=SELF`, not speaker/owner/perspective leakage |
| Ambiguity | EN/ES structured cases mostly unresolved | No frozen ambiguity failure | B passes name-vs-adjective and question/hypothesis critical examples, but coverage is too small to claim general disambiguation |
| Code-switch | EN/ES variants unresolved | No frozen code-switch failure | B passes S21; one scenario cannot establish robustness |

## Candidate B residual main-field errors

| Case | Split | Observed | Immediate cause | Corrective disposition |
|---|---|---|---|---|
| S08-it | dev | expected object `il bar Aurora`, produced `bar Aurora` | Location article normalization is inconsistent with the gold object's surface policy | Report; no post-result patch |
| S16-en | test | expected `goal.object`, produced `preference.like` | Shorter preference marker `like` is evaluated before the goal marker `would like` | Report; a future mapper should use longest/specific marker or syntactic scope |
| S18-it | test | expected `REQUEST,target=SELF`, produced `ASSERT,target=null` | First-token POS is `PROPN`, so the POS-only imperative gate misses `Apri` | Report; future morphology or bounded imperative lexicon/model adaptation needed |
| S18-es | test | expected `REQUEST,target=SELF`, produced `ASSERT,target=null` | First-token POS is `ADP`, so the POS-only imperative gate misses `Abre` | Report; same limitation as Italian |

The evaluator's `errorFamilies.ownership=2` counts the missing `target` fields in
S18; the dedicated owner/perspective safety counter is zero. This distinction
prevents a dialogue-target failure from being misreported as belief leakage.

## Candidate B entity-resolution errors

Entity F1 uses exact normalized mention + type + link. The six case-level set
differences are:

| Case(s) | Expected | Produced | Category |
|---|---|---|---|
| S08-en | `Aurora bar / LOCATION:bar_aurora` | `Aurora bar / LOCATION:aurora_bar` | Surface-order/link canonicalization mismatch |
| S16-en | `Venice / LOCATION:venice` | no entity | Consequence of wrong predicate branch |
| S16-es | `Venecia / LOCATION:venice` | `Mañana / LOCATION:manana` and `Venecia / LOCATION:venecia` | Every `PROPN` in goal text is treated as a location; cross-language canonical link missing |
| S17-it/en/es | only `Marco / PERSON / OTHER:marco` | correct Marco plus empty `LOCATION:` | Question with intentionally unknown residence incorrectly materializes an empty location entity |

These errors do not invent World Truth—the `worldTruth` flag remains false—but
they show that high main-field exactness is not equivalent to robust entity
linking.

## Candidate A failure shape

A is intentionally frozen to the production-reference semantics. It remains
Italian-first: IT field exact is `0.9167`, while EN and ES are both `0.6281` and
their unknown rate is `1.0`. It also fails the absolute ownership gate with
eight owner/perspective violations. Its strengths are bounded false-positive
behavior (`falseStructuredClaimRate=0`) and zero invented World Truth. P0 does
not rewrite A to improve its score.

## What the gold does not establish

- only 22 scenario semantics/66 language variants exist;
- no noisy ASR, typos beyond a small colloquial slice, long discourse,
  adversarial casing, nested negation or broad code-switch distribution;
- reference resolution has only short, supplied context;
- confidence values are uncalibrated scores;
- no production memory admission or downstream game behavior is exercised.

Therefore Candidate B's quality result is a lab signal, not proof of general
language understanding or production readiness.
