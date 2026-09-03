# Gate 13 — P0 Understanding verdict

Date: 2026-09-03  
Scope: isolated `matrix-understanding-lab`; production Matrix reference frozen at
`ae82d5cf843d52b3d60caadd161e4a5516fc5d0d` and not modified.

## Executive verdict

**Recommendation: `KEEP`.** Keep the current production front-end until a
candidate passes provenance, expanded generalization and physical Moto G56
footprint gates. Candidate B is the strongest implemented research baseline and
the preferred `ADAPT` direction, but it is not eligible to replace production:
its Italian POS artifact derives from non-commercial data and no real-device
measurement has yet been returned. Candidate C is not ready and was not faked.

No integration, B4 work, GGUF/personality change or production architecture
change is authorized by this result.

## A/B/C comparison

| Dimension | A — frozen deterministic | B — ICU + OpenNLP + Matrix mapper | C — compact ONNX |
|---|---|---|---|
| Anti-discard class | `FULL_CANDIDATE` (current reference) | `FULL_CANDIDATE` (lab composition) | No full candidate; components retained below |
| Executed gold rows | 66 | 66 | Not executed by specification |
| Main-field exact | `0.7299` | **`0.9924`** | Not available |
| Exact claim count | `0.9394` | **`1.0000`** | Not available |
| Source-span F1 | `0.9412` | **`1.0000`** | Not available |
| Negation-scope F1 | `0.6429` | **`1.0000`** | Not available |
| Entity type/link F1 | `0.4231` | **`0.9032`** | Not available |
| Worst-language field exact | EN/ES `0.6281` | IT `0.9886` | Not available |
| Owner/perspective violations | **8 — critical fail** | **0 — pass** | Not measured |
| Invented World Truth | 0 | 0 | Not measured |
| JVM warm-like p50/p95 | 9,458 / 1,200,481 ns | 1,911,047 / 4,508,986 ns | Not available |
| Android/offline | Existing reference semantics; not packaged by this lab | Offline probe packaged; 5,636,633-byte APK, platform ICU, no network permission declared | ORT feasible as substrate; no valid model selected |
| License/provenance | No new external model introduced | **Production blocked:** Italian VIT-derived model is `CC BY-NC-SA 3.0`; EN/ES share-alike review also required | Runtime/base-model declarations usable, but no Matrix task model/data artifact |
| Generalization | Fails EN/ES and ownership on this set | Best P0 quality; only 22 semantic scenarios and four residual main-field errors | Not established |
| Production disposition | `KEEP` temporarily | `ADAPT`, do not integrate | `CANDIDATE_C_NOT_READY` |

JVM latency is a CI wall-clock diagnostic with model construction outside each
case. It is not Android CPU/PSS/cold/thermal evidence. Confidence values are
scores, not calibrated probabilities.

## Partial, adaptable and reference candidates retained

| Candidate/component | Classification | Possible future Matrix value | Stop/next evidence |
|---|---|---|---|
| Android platform ICU / ICU4J parity adapter | `PARTIAL_REUSE` | Unicode-aware boundaries without Android model payload | Verify platform-vs-ICU4J parity on Moto corpus |
| Apache OpenNLP tools | `PARTIAL_REUSE` | Maintained trainable JVM POS runtime | Android PSS/CPU plus domain-trained model needed |
| Published OpenNLP IT/EN/ES POS models | `PARTIAL_REUSE` (lab only) | Reproducible trilingual benchmark signal | Replace/clear model-data licenses before production |
| Matrix semantic mapper prototype | `ADAPT` | Typed claim and safety mapping | Expand independently frozen gold; avoid rule accumulation |
| spaCy small IT/EN/ES pipelines | `REFERENCE_ONLY`; dependency ideas `REIMPLEMENT_FROM_PRINCIPLES` | Rich morphology/dependency/NER oracle; Italian reserve | Python/non-Android; Italian model non-commercial; no direct adoption |
| Stanza | `REFERENCE_ONLY` / `ADAPT` | Trilingual UD morphology/dependency ablation oracle | PyTorch/model footprint and treebank licenses need separate audit |
| Tint | `REFERENCE_ONLY` / `REIMPLEMENT_FROM_PRINCIPLES` | Italian pro-drop/dependency/entity-link reference | GPL-3.0, 156 MB release archive, old release; Italian reserve only |
| UDPipe | `PARTIAL_REUSE` / `ADAPT` | Potential compact NDK morphology/dependency signal | Compatible model training, NDK build and device cost required |
| Duckling time/numeral design | `REIMPLEMENT_FROM_PRINCIPLES` | Bounded IT/EN/ES temporal and numeric normalization | Independent implementation and same-gold ablation required |
| UD Italian MarkIT | `ADAPT` | CC BY 4.0 Italian dependency slice | Small grammar-example domain; not sufficient alone |
| UD Italian TWITTIRO | `ADAPT` / `REFERENCE_ONLY` | Social-text syntax and punctuation reserve | Share-alike review, irony bias and Matrix annotations required |
| UD Italian PoSTWITA / ParTUT | `REFERENCE_ONLY` | Italian robustness/error oracle | Non-commercial licenses block standard production training |
| ONNX Runtime Mobile | `PARTIAL_REUSE` | Mature offline Android execution substrate | Only useful after a valid task model exists |
| Multilingual MiniLM | `PARTIAL_REUSE` / `REFERENCE_ONLY` | Semantic retrieval or alias similarity | 118 MB INT8 arm64 file and no structured Matrix head |
| Multilingual DistilmBERT | `ADAPT` | Base encoder for a future joint model | New data/training/compression project; current P0 data insufficient |
| MASSIVE + joint intent/slot methodology | `REFERENCE_ONLY` / `ADAPT` | Multilingual data/process patterns | Ontology mismatch; third-party provenance and Matrix labels needed |

No item was marked `REJECT` merely for missing IT/EN/ES coverage, runtime
language, Android packaging, size or license. Retaining reference value does not
waive production eligibility gates. In particular, Italian-only options are
kept as reserves, not promoted over the common trilingual benchmark.

## Frozen evidence and gates

- Contract/gold: 22 scenarios, 66 natural parallel variants; train 7 scenarios
  / 21 variants, dev 6 / 18, locked test 9 / 27.
- Gates 00–03: repository truth, frozen contract, gold-before-candidates and A
  baseline completed.
- Gates 04–05: B research, lateral anti-discard review, implementation and unit
  tests completed.
- Gates 06–07: C research completed as bounded negative result; implementation
  skipped by specification because no valid reproducible model was found.
- Gates 08–09: unified machine-readable runner and per-language/worst-language
  metrics completed. B passes frozen quality/safety but fails production license.
- Gate 10: Android probe source and CI build pass at `de377a7549…`; artifact
  `9889461911`, APK SHA-256 `5f117c38…ff506`; physical Moto measurement remains
  pending.
- Gate 11: residuals classified without post-test tuning.
- Gate 12: B does not survive production license/generalization/mobile scrutiny;
  it survives only as the leading research baseline.

## Decision boundary

No architectural decision is required to close P0. A future production proposal
does require supervisor authorization for a new data/model adaptation project,
including dataset rights and an expanded frozen benchmark. Until then:

- production: `KEEP`;
- B: retain as `ADAPT` baseline;
- C: retain partial components, no implementation;
- Moto G56: execute the documented probe and return raw JSON;
- Matrix runtime: unchanged.
