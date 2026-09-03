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

