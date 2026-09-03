# Gate 04 — Candidate B research

Research date: 2026-09-03. Candidate: Android ICU + Apache OpenNLP + Matrix
semantic mapper.

## BUILD / REUSE / ADAPT decision

- **REUSE** Android platform ICU `android.icu.text.BreakIterator` on API 24+ for
  Unicode/locale-aware word segmentation. The JVM benchmark uses the matching
  ICU4J algorithm behind an injected `WordSegmenter`; the Android probe swaps in
  platform ICU so ICU4J need not be shipped in an APK.
- **REUSE for lab only** Apache OpenNLP 2.5.11 and the 1.3.0 UD POS model
  artifacts for Italian, English and Spanish.
- **BUILD** the Matrix-specific semantic mapper. OpenNLP POS tags do not express
  speaker, owner, perspective, World authority or the Matrix predicate taxonomy.
- Do not include OpenNLP sentence/tokenizer models: ICU already supplies the
  boundary function needed by this experiment. This keeps the comparison
  discriminating and avoids six redundant model artifacts.

### Anti-discard classification (retroactive)

The labels below supersede the earlier shorthand `REUSE/BUILD`. A missing
language, a non-Android implementation, size, or a non-adoptable published
model license is not by itself a reason to discard the underlying component or
principle.

| Asset | Classification | Value retained for Matrix | P0 use |
|---|---|---|---|
| Candidate B composition (platform ICU + OpenNLP POS + Matrix mapper) | `FULL_CANDIDATE` | Complete IT/EN/ES experimental path | Implemented and scored, lab only |
| Android platform ICU / ICU4J parity adapter | `PARTIAL_REUSE` | Unicode word boundaries without a packaged tokenizer model | Used by B |
| Apache OpenNLP tools | `PARTIAL_REUSE` | Maintained JVM POS runtime and trainable MaxEnt pipeline | Used by B |
| Published OpenNLP IT/EN/ES POS artifacts | `PARTIAL_REUSE` | Reproducible trilingual lab signal | Used by B; production license stop |
| Matrix semantic mapper | `ADAPT` | Typed owner/perspective/provenance and predicate mapping | Authored for the lab; not production-authorized |

## Versions and provenance

| Component | Pinned version/source | Provenance | License/status |
|---|---|---|---|
| Android ICU | platform API 24+ | Android API / Unicode ICU | Unicode license; runtime platform component |
| ICU4J JVM parity adapter | 78.1 | Unicode ICU project | Unicode license; CLI benchmark only |
| OpenNLP tools | 2.5.11, release 2026-07-24 | Apache OpenNLP | Apache-2.0 |
| OpenNLP models | 1.3.0 | Apache model Maven artifacts | Repository declares Apache-2.0; training-data caveat below |
| Italian POS | `opennlp-it-ud-vit-pos-1.3-2.5.4.bin`, SHA-256 `d38e645d…18f1` | UD Italian VIT | Source treebank CC BY-NC-SA 3.0 |
| English POS | `opennlp-en-ud-ewt-pos-1.3-2.5.4.bin`, SHA-256 `510b8908…52ce` | UD English EWT | Source treebank CC BY-SA 4.0 |
| Spanish POS | `opennlp-es-ud-gsd-pos-1.3-2.5.4.bin`, SHA-256 `c1d7e327…55cd5` | UD Spanish GSD | Source treebank CC BY-SA 4.0 |

The OpenNLP model repository says its published artifacts are Apache-2.0 and
its root NOTICE names only ASF. The Italian training treebank itself is
unambiguously non-commercial. This conflict cannot be resolved by engineering
interpretation: Candidate B may be measured in this isolated research lab, but
is **LICENSE_BLOCKED_FOR_PRODUCTION** until the model's commercial rights are
confirmed in writing or the Italian POS model is retrained from a compatible
corpus. Share-alike obligations for EN/ES also require legal review.

## Maintenance and recent issues/PRs

- Apache OpenNLP is active; 2.5.11 is the current stable 2.x release examined.
- The model repository was updated in 2026; PR #42 released the 1.3.0 artifacts.
- OpenNLP PR #1035 addresses an out-of-memory allocation path. PRs #1066/#1081
  address unsupported XML parser security options on constrained runtimes.
  Neither proves Android support; they reinforce the need for a real D8/build
  gate and device memory probe.
- The models are explicitly described as suitable for testing/getting started;
  Apache recommends training domain-specific models for specialized use.
- The OpenNLP language detector is not selected: upstream says it works best on
  at least two sentences, incompatible with Matrix's frequent short turns. The
  benchmark receives the language explicitly.

Primary sources:

- https://developer.android.com/reference/android/icu/text/BreakIterator
- https://unicode-org.github.io/icu/userguide/boundaryanalysis/
- https://github.com/apache/opennlp/releases/tag/opennlp-2.5.11
- https://github.com/apache/opennlp-models
- https://github.com/apache/opennlp-models/pull/42
- https://github.com/apache/opennlp/pull/1035
- https://github.com/apache/opennlp/pull/1066
- https://github.com/apache/opennlp/pull/1081
- https://github.com/UniversalDependencies/UD_Italian-VIT/blob/master/LICENSE.txt
- https://github.com/UniversalDependencies/UD_English-EWT/blob/master/LICENSE.txt
- https://github.com/UniversalDependencies/UD_Spanish-GSD/blob/master/LICENSE.txt

## Android/offline/footprint expectations

All inference is local. Platform ICU adds no packaged model. OpenNLP tools and
three POS artifacts must be dexed/packaged; their actual dependency bytes, APK
bytes, init time, warm latency and PSS are measured by later gates. No numerical
footprint is asserted before the build. The supervisor's initial PSS target is
40 MB delta; exceeding it requires a material quality gain and a decision.

The Android build gate established a minimum API constraint: OpenNLP 2.5.11
contains `MethodHandle.invoke` usage in Snowball classes, which D8 supports from
API 26. The lab probe therefore targets min SDK 26 (compatible with the Moto G56)
rather than implying that ICU's API-24 availability is sufficient for the whole
composition.

## Known limits before implementation

1. POS/morphology helps disambiguate proper name vs adjective and find verbs,
   but does not perform dependency parsing or coreference.
2. Domain predicates and ownership still require deterministic Matrix logic.
3. A shared mapper can become a new multilingual rule pile if POS evidence is
   ignored; diagnostics therefore record tokens/tags and which rule consumed
   them.
4. Capitalization remains unreliable in chat; known entity IDs and predicate
   argument position outrank casing.
5. Commercial adoption is blocked by model-data provenance even if quality wins.

## Mandatory lateral research

This pass looked for mature single-language and subtask components that could
replace or improve part of B. None was added after the frozen benchmark started:
doing so would change the measured candidate and invite test-set tuning. They
remain explicit reserves for a future, separately authorized experiment.

| Candidate | Evidence and footprint signal | Classification | What it could improve | Why not used in B |
|---|---|---|---|---|
| spaCy small IT/EN/ES pipelines 3.8.0 | Tokenization, morphology, POS, dependency parsing and NER; wheels are 13,030,943 B IT, 12,806,118 B EN and 12,884,212 B ES. spaCy itself is MIT and actively maintained (3.8.16 inspected). Italian model is 12 MB and `CC BY-NC-SA 3.0` | `REFERENCE_ONLY` for the published trio; `REIMPLEMENT_FROM_PRINCIPLES` for feature ablations | Dependency-backed clause boundaries, proper-name/entity evidence and imperative detection | Python/non-Android deployment, three runtimes/models, domain mismatch, and Italian non-commercial model. Italian option retained as reserve, not discarded |
| Stanza 1.14.0 | Apache-2.0 Python/PyTorch pipeline; 70+ language packages with UD tokenization, morphology, POS, lemma and dependency; offline model install supported | `REFERENCE_ONLY`; selected lightweight processors may be `ADAPT` after model/data audit | Strong morphology/dependency oracle for error attribution across IT/EN/ES | No direct Android path, model/package footprint not measured, per-treebank licenses still apply |
| Tint 0.2 | Italian Java pipeline over Stanford CoreNLP with POS, dependencies and entity linking; GPL-3.0; latest binary release 2018, archive 156,404,585 B | `REFERENCE_ONLY` and `REIMPLEMENT_FROM_PRINCIPLES` | Italian-specific pro-drop, dependency and entity-linking behavior | GPL/large/old package is unsuitable as a production dependency. Kept as an Italian reserve/reference |
| UDPipe 2.1.0 | MPL-2.0 C++ library for tokenization, tagging, lemmatization and dependency parsing; trainable and potentially NDK-capable | `PARTIAL_REUSE` runtime or `ADAPT` with compatible retraining | Compact dependency signal and consistent UD features | Published model page states non-commercial/default treebank terms; NDK integration and actual footprint unmeasured |
| Duckling 0.2.0.0 / current main | BSD rule engine; dedicated IT, EN and ES rule/corpus trees exist for `Time` and `Numeral` | `REIMPLEMENT_FROM_PRINCIPLES` | Temporal and numeric normalization with positive/negative corpora and composable rules | Haskell runtime is not a reasonable Android dependency; direct code copying is unnecessary. Principles can inform an independent bounded Matrix parser |
| UD Italian MarkIT | 1,300 marked-construction sentences; dependencies manually corrected; `CC BY 4.0` | `ADAPT` | Commercially compatible Italian dependency training/evaluation slice | Small, grammar-example domain; insufficient alone |
| UD Italian TWITTIRO | Italian ironic tweets/social text; `CC BY-SA 4.0` | `ADAPT` / `REFERENCE_ONLY` | Chat-like punctuation, mentions and non-canonical syntax | Share-alike/product review required; irony-heavy and not Matrix annotated |
| UD Italian PoSTWITA and ParTUT | Italian social/parallel syntax resources, both non-commercial | `REFERENCE_ONLY` | Italian robustness/error analysis | `CC BY-NC-SA 4.0` blocks normal commercial model adoption |

No listed asset is `REJECT`: each retains measurable algorithmic, dataset or
oracle value. This does **not** make each asset production-eligible. The
production decision still requires a composed IT/EN/ES result to beat the same
gold set and pass actual Android cost and provenance gates.

Additional primary sources:

- https://github.com/explosion/spacy-models/releases/tag/it_core_news_sm-3.8.0
- https://github.com/explosion/spacy-models/releases/tag/en_core_web_sm-3.8.0
- https://github.com/explosion/spacy-models/releases/tag/es_core_news_sm-3.8.0
- https://github.com/stanfordnlp/stanza/releases/tag/v1.14.0
- https://stanfordnlp.github.io/stanza/download_models.html
- https://github.com/dhfbk/tint/releases/tag/0.2
- https://github.com/ufal/udpipe/releases/tag/v2.1.0
- https://ufal.mff.cuni.cz/udpipe/2/models
- https://github.com/facebook/duckling
- https://github.com/UniversalDependencies/UD_Italian-MarkIT
- https://github.com/UniversalDependencies/UD_Italian-TWITTIRO
- https://github.com/UniversalDependencies/UD_Italian-PoSTWITA
- https://github.com/UniversalDependencies/UD_Italian-ParTUT
