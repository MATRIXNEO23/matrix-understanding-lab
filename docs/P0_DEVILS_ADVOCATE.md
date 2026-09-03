# Gate 12 — Devil's Advocate

Target under attack: Candidate B, because it has the best executed quality
result. “Best measured” is not “production winner”.

## Strongest case against Candidate B

1. **The Italian model is a release blocker.** The published OpenNLP Italian
   POS artifact derives from UD Italian VIT (`CC BY-NC-SA 3.0`). The model
   repository's Apache declaration does not erase training-data terms. Without
   written rights or a compatible retrain, B cannot ship commercially.
2. **The score can overstate generalization.** The gold contains 22 semantic
   scenarios, with parallel variants. B's deterministic mapper contains domain
   marker lists close to those families. A `0.9924` field-exact score on 66 rows
   is not evidence for open-domain IT/EN/ES understanding.
3. **POS is not carrying all the advertised value.** Most typed semantics still
   comes from hand-authored marker ordering and extraction. Test failures show
   both sides: `would like` loses to `like`, while mislabeled imperatives make
   `Apri`/`Abre` assertions. This can become a multilingual rule pile with a
   statistical tagger in front.
4. **Entity linking is materially weaker than headline field accuracy.** Entity
   F1 is `0.9032`; goals can label a temporal token as a location, questions can
   emit an empty location, and translated locations lack canonical links.
5. **Android cost is not yet known.** JVM warm-like p95 is about 4.51 ms, but no
   real Moto G56 PSS/CPU/cold/thermal output exists yet. OpenNLP constrained-
   runtime PRs and an OOM-path fix justify a physical device gate, not optimism.
6. **ICU parity is an assumption until measured.** JVM uses ICU4J 78.1; Android
   uses the platform ICU version supplied by the device. Unicode boundary
   behavior can differ across platform releases. The Android probe must compare
   quality as well as footprint.
7. **Confidence is uncalibrated.** The mapper's fixed `0.88/0.45` values are
   scores. They cannot drive risk-sensitive admission as probabilities without
   calibration on a larger, independent set.

## Adversarial cases required before any production proposal

- nested and contrastive coordination; negation that attaches across clauses;
- lowercase names, capitalized common words and person/location homonyms;
- multiple people and places in one clause, empty/unknown arguments and quoted
  speech;
- Italian/Spanish clitics and imperatives, pro-drop person/number ambiguity;
- spelling errors, missing accents, emoji/punctuation noise and ASR-like text;
- longer history with stale references and contradictory corrections;
- mixed-language clauses rather than a single controlled code-switch token;
- entity aliases that require a registry rather than locale-specific slugs.

These cases must be independently annotated and frozen before tuning. Patching
the current test rows would invalidate the evidentiary value of the test split.

## Partial/reimplementation alternatives reconsidered

| Route | Why it might beat B | Cost/risk | Gate-12 status |
|---|---|---|---|
| Platform ICU + OpenNLP tools + newly trained compatible IT/EN/ES models | Preserves the light, already-measured structure and removes published-model provenance ambiguity | Requires a much larger Matrix-domain corpus, compatible data inventory, training, held-out evaluation and model cards | `ADAPT` — strongest successor hypothesis, not ready |
| ICU + independent Duckling-inspired temporal/numeral component | Composable positive/negative corpora could replace fragile time/number markers with a bounded subparser | Must be independently implemented/tested; does not solve claims, ownership or entities | `REIMPLEMENT_FROM_PRINCIPLES` — useful subtask composition |
| ICU + UDPipe dependency/morphology via NDK | Dependency heads could improve clause scope, imperatives and arguments across languages | Native integration, model license audit and PSS/latency may outweigh four residual main-field errors | `PARTIAL_REUSE/ADAPT` — benchmark only after expanded gold justifies it |
| spaCy/Stanza/Tint as offline oracles | Rich morphology/dependencies can localize whether mapper or linguistic analysis failed; Tint is Italian-specific | Python/GPL/model-license/size constraints prevent direct Android production use | `REFERENCE_ONLY`; Italian options retained as reserve |
| MiniLM similarity alongside B | Could help alias/entity retrieval | 118 MB INT8 model is large and still cannot emit structured claims | `PARTIAL_REUSE`, not justified for P0 front-end |
| DistilmBERT/MASSIVE-derived joint model | Learned intent/span heads may reduce rule accumulation | Current Matrix data is far too small; encoder footprint and ontology mismatch remain | `ADAPT`, requires a new authorized data/model project |

## Could a composition beat the favorite?

Possibly, but no composition has earned that claim yet. The most credible future
experiment is not “add every NLP library”; it is:

1. keep platform ICU boundaries;
2. retrain only the smallest linguistic model(s) that reduce errors on a larger
   independently frozen Matrix set, using commercially compatible data;
3. add a bounded temporal/numeral component only if error analysis shows value;
4. retain typed deterministic safety rules for ownership and World Truth;
5. compare the composition against frozen A and B on the same Moto G56 probe.

UD Italian MarkIT (`CC BY 4.0`) and TWITTIRO (`CC BY-SA 4.0`) are useful Italian
reserves, but neither is sufficient alone: MarkIT is small/grammar-oriented and
TWITTIRO is irony-heavy with share-alike obligations. spaCy Italian and Tint
remain reference oracles, not silent dependencies.

## Survival verdict

- **Benchmark quality:** B survives; it is the strongest implemented prototype.
- **Safety on frozen critical cases:** B survives (zero owner/perspective and
  World Truth violations).
- **Provenance/license:** B fails production eligibility.
- **Generalization:** not established.
- **Android footprint:** instrumentation prepared; physical measurement pending.

Candidate B therefore does not survive as a production replacement. The honest
recommendation is `KEEP` the current production front-end while retaining B as
an `ADAPT` research baseline. No production integration is authorized.

Primary issue/reference set:

- https://github.com/apache/opennlp/pull/1035
- https://github.com/apache/opennlp/pull/1066
- https://github.com/apache/opennlp/pull/1081
- https://github.com/apache/opennlp-models
- https://github.com/UniversalDependencies/UD_Italian-VIT/blob/master/LICENSE.txt
- https://unicode-org.github.io/icu/userguide/boundaryanalysis/
- https://developer.android.com/reference/android/icu/text/BreakIterator
