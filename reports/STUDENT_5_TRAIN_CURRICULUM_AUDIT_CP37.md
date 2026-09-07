# Supervisor GPT — Student-5 TRAIN Curriculum Audit Report

**TRAIN_CURRICULUM = REPAIR_REQUIRED_BEFORE_TRAINING**

Date: 2026-09-07. Checkpoint CP37. Issuer/reviewer: Supervisor GPT; executor: ChatGPT Work.
Repository: `MATRIXNEO23/matrix-understanding-lab`; branch: `student5-path-b-v3`.
Starting HEAD: `39ca73b9a461e4435fdf1f5e5f8172c7d303dc16`.
Final delivery HEAD: the direct child introducing this report, returned after remote verification in the handoff. Resolve its immutable identity with `git log -1 --format=%H -- reports/STUDENT_5_TRAIN_CURRICULUM_AUDIT_CP37.md`.
Assignment: [TRAIN curriculum audit only](../prompts/WORK_STUDENT_5_PATH_B_V3_TRAIN_CURRICULUM_AUDIT_ONLY.md).

## Decision and limits

The immutable curriculum teaches a narrow, mostly declarative self/third-person property extractor with substantial inherited repetition. It does not yet supply coherent coverage of the full V3 behavior: independent attribution/viewpoint, unknown/ambiguous role binding, genuine command/belief, advanced temporal anchors, multilingual refusal/withdrawal/desire contrasts and cue/polarity independence. Several concrete annotation defects or unresolved semantic conventions also remain. Starting supervised fitting now would expose the model to those targets; whether/how much measured quality would regress is **not established without an authorized experiment**, which was not performed.

This verdict assesses pedagogy, not TASK 2.3 structural acceptance. CP36 integrity remains accepted. Gate A remains accepted and was not rerun. CP36 DEV/evaluator blockers remain separate and unresolved; this report does not repair them or authorize training.

No training, optimizer, loss optimization, backprop, fine-tuning, model loading, augmentation, dataset edits, DEV/Frozen payload access, evaluator/decoder repair, calibration repair, quantization or Assembling work occurred. Existing Student-4 reports were read solely as historical evidence; no Student-4 model or held-out payload was opened.

## Inputs, provenance and method

TRAIN: `student5-matrix-nlu-v3-train-v1`, `data/student5_v3/`, 3,150 observations / 3,990 claims.
Ordered dataset SHA-256: `1118a900026f48cfcc290c3f9dc52a1a019a6a1f4761661f326c33770523140e`.
Contract: `MATRIX_NLU_CONTRACT_V3`, fingerprint `7b0646e44243ad897760c0fcadbe141f1b8e88e3fd8d63a1789106571b9987b0`.
Architecture remains 16 conceptual heads / 17 output tensors; temporal relation and anchor have distinct tensors within one conceptual head.

Lineage documented in the [migration report](STUDENT_5_TRAIN_V3_MIGRATION.md): 2,775 Matrix V2 TRAIN observations plus the exact 375-observation v2.2A repair TRAIN. Source SHA-256 values are respectively `5118d37ce2ab19d5be171f757f448698085e3c222a4a627f9838329836185820` and `8be02976d46ba47d746ff7307d688d93595453221965b3de995d4b1de655799f`. All 3,150 are reannotated V3; this is not an untouched V2 label copy. P0.5 TRAIN was excluded in TASK 2.3 because it was not independently separated from forbidden payloads. No MASSIVE auxiliary payload is part of this artifact. Neither excluded source was reconstructed here.

The CP37 census reads all authorized TRAIN shards, binds bytes and inspected sources to current Git metadata (140 matches), and counts actual stored annotations. It does not rerun migration or claim a new structural gate. Scripts enumerate every fixed class including zeros, all five role values, statuses, span support and language slices.

For token BIO distributions only, the existing pure `build_v3_examples` is called with explicitly named **Unicode lexical audit offsets**, max length 256 and no truncation. These are annotation-support counts, **not physical BERT/WordPiece token counts**, training gradients or learned performance. Padding is ignored. It yields 3,150 boundary examples and 3,990 claim examples; other heads are masked in boundary examples, and boundary is masked in claim examples. Thus 7,140 target examples must not be represented as 7,140 positive examples per head. Sequence labels have 3,990 supervised slots per head; temporal anchor is ignored on ATEMPORAL claims.

Whole-corpus exact duplicate checks are objective. Near-duplicate screening uses within-language normalized character similarity >=0.90; it is a concentration screen, not an equivalence classifier. Delexicalized skeletons replace annotated object/entity spans; they are surface-template proxies, not a complete semantic-template ontology. Potential linguistic defects are separately adjudicated below; no heuristic flag is silently counted as a proven error.

Primary machine evidence: [curriculum.json](evidence/student5-path-b-cp37-train-audit/curriculum.json), [review-evidence.json](evidence/student5-path-b-cp37-train-audit/review-evidence.json), [semantic-review.json](evidence/student5-path-b-cp37-train-audit/semantic-review.json). Scripts preserve definitions and sample IDs. All reported counts refer to stored TRAIN, not DEV.

## 1. Per-head curriculum coverage

### Token heads: effective positive support

| Head | Supervised examples | Positive examples | BIO groups | Examples with multiple groups | All-O lexical accuracy |
| --- | --- | --- | --- | --- | --- |
| boundary | 3150 | 3150 | 3990 | 699 | 6.60% |
| object | 3990 | 3794 | 3794 | 0 | 70.54% |
| subject | 3990 | 767 | 767 | 0 | 96.48% |
| negation | 3990 | 463 | 476 | 13 | 97.81% |
| temporal | 3990 | 389 | 389 | 0 | 97.24% |
| entity | 3990 | 2296 | 2620 | 324 | 83.69% |

All-O accuracy is a trivial annotation baseline, not an evaluated model. It illustrates why token accuracy can conceal poor positive span recovery, particularly negation (97.81% O), temporal (97.24% O) and subject (96.48% O). All boundary observations contain a claim: zero claim-free/O-only observations teach safe absence.

| Head / lexical label | IT | EN | ES | Code-switch | Total |
| --- | --- | --- | --- | --- | --- |
| boundary / O | 559 | 489 | 489 | 0 | 1537 |
| boundary / B-CLAIM | 1406 | 1286 | 1287 | 11 | 3990 |
| boundary / I-CLAIM | 6127 | 6232 | 5379 | 35 | 17773 |
| object / O | 5189 | 5572 | 4557 | 33 | 15351 |
| object / B-OBJECT | 1336 | 1223 | 1224 | 11 | 3794 |
| object / I-OBJECT | 1008 | 723 | 885 | 2 | 2618 |
| subject / O | 7264 | 7278 | 6408 | 46 | 20996 |
| subject / B-SUBJECT | 269 | 240 | 258 | 0 | 767 |
| subject / I-SUBJECT | 0 | 0 | 0 | 0 | 0 |
| negation / O | 7312 | 7408 | 6521 | 46 | 21287 |
| negation / B-NEGATION_CUE | 221 | 110 | 145 | 0 | 476 |
| negation / I-NEGATION_CUE | 0 | 0 | 0 | 0 | 0 |
| temporal / O | 7294 | 7355 | 6467 | 46 | 21162 |
| temporal / B-TEMPORAL | 160 | 115 | 114 | 0 | 389 |
| temporal / I-TEMPORAL | 79 | 48 | 85 | 0 | 212 |
| entity / O | 6311 | 6366 | 5490 | 46 | 18213 |
| entity / B-PERSON | 479 | 420 | 435 | 0 | 1334 |
| entity / I-PERSON | 0 | 0 | 0 | 0 | 0 |
| entity / B-LOCATION | 433 | 422 | 431 | 0 | 1286 |
| entity / I-LOCATION | 310 | 310 | 310 | 0 | 930 |

`I-SUBJECT`, `I-PERSON` and `I-NEGATION_CUE` are zero **under this lexical audit tokenizer**. No annotated subject or PERSON mention exceeds one whitespace word. WordPiece splitting could yield internal I labels, but would not create missing multiword-subject/person examples. Object/subject/temporal have zero claims with multiple groups; entity has 324 and negation only 13 (12 IT, one ES, zero EN). This preserves nominal plural-span format while providing uneven teaching of plural spans.

### Five fixed sequence heads: every class

| Head / class | IT | EN | ES | Code-switch | Claims | Unique claim surfaces |
| --- | --- | --- | --- | --- | --- | --- |
| dialogueAct / ASSERT | 1321 | 1207 | 1216 | 11 | 3755 | 1019 |
| dialogueAct / QUESTION | 62 | 72 | 64 | 0 | 198 | 59 |
| dialogueAct / REQUEST | 19 | 4 | 4 | 0 | 27 | 24 |
| dialogueAct / COMMAND | 0 | 0 | 0 | 0 | 0 | 0 |
| dialogueAct / CORRECT | 4 | 3 | 3 | 0 | 10 | 10 |
| dialogueAct / UNKNOWN | 0 | 0 | 0 | 0 | 0 | 0 |
| predicate / identity.name | 155 | 156 | 149 | 0 | 460 | 76 |
| predicate / identity.age | 147 | 147 | 147 | 0 | 441 | 222 |
| predicate / residence.place | 313 | 302 | 311 | 0 | 926 | 207 |
| predicate / presence.reported | 13 | 13 | 13 | 0 | 39 | 15 |
| predicate / preference.like | 321 | 329 | 320 | 0 | 970 | 192 |
| predicate / work.role | 94 | 85 | 91 | 0 | 270 | 98 |
| predicate / possession.has | 39 | 10 | 14 | 0 | 63 | 34 |
| predicate / goal.object | 245 | 192 | 190 | 0 | 627 | 165 |
| predicate / attribute.is | 21 | 12 | 14 | 0 | 47 | 34 |
| predicate / consent.grant | 30 | 21 | 19 | 0 | 70 | 31 |
| predicate / consent.refuse | 27 | 19 | 19 | 0 | 65 | 26 |
| predicate / speech.unresolved | 1 | 0 | 0 | 11 | 12 | 12 |
| polarity / POSITIVE | 1055 | 1036 | 1004 | 11 | 3106 | 806 |
| polarity / NEGATIVE | 288 | 187 | 220 | 0 | 695 | 252 |
| polarity / UNKNOWN | 63 | 63 | 63 | 0 | 189 | 54 |
| temporalRelation / ATEMPORAL | 456 | 456 | 456 | 0 | 1368 | 216 |
| temporalRelation / CURRENT | 768 | 657 | 660 | 11 | 2096 | 807 |
| temporalRelation / PAST | 12 | 1 | 1 | 0 | 14 | 9 |
| temporalRelation / FUTURE | 170 | 172 | 170 | 0 | 512 | 80 |
| temporalRelation / BEFORE | 0 | 0 | 0 | 0 | 0 | 0 |
| temporalRelation / AFTER | 0 | 0 | 0 | 0 | 0 | 0 |
| temporalRelation / DURING | 0 | 0 | 0 | 0 | 0 | 0 |
| temporalRelation / RECURRENT | 0 | 0 | 0 | 0 | 0 | 0 |
| temporalRelation / AT_REFERENCE | 0 | 0 | 0 | 0 | 0 | 0 |
| temporalRelation / UNKNOWN | 0 | 0 | 0 | 0 | 0 | 0 |
| claimKind / DIRECT | 1309 | 1197 | 1198 | 11 | 3715 | 1032 |
| claimKind / REPORT | 8 | 0 | 0 | 0 | 8 | 8 |
| claimKind / BELIEF | 0 | 0 | 0 | 0 | 0 | 0 |
| claimKind / HYPOTHESIS | 89 | 89 | 89 | 0 | 267 | 72 |
| claimKind / UNKNOWN | 0 | 0 | 0 | 0 | 0 | 0 |

ASSERT is 3,755/3,990 (94.11%); DIRECT 3,715/3,990 (93.11%). COMMAND, dialogueAct UNKNOWN, BELIEF, claimKind UNKNOWN and six temporal labels are absent. REQUEST has only 27 claims and CORRECT 10. These are census findings, not newly imposed numeric acceptance thresholds. All predicates occur, but `speech.unresolved` is concentrated in 11 code-switch rows and one IT correction; EN/ES have no such targets.

Only 14 PAST targets exist: IT 12, EN one, ES one. Eleven are IT goal statements with “da ieri”, not broad past-event supervision. FUTURE is 510 goal.object + two consent.grant; temporal relation can therefore correlate strongly with predicate/template. CURRENT and ATEMPORAL together cover 86.82% of claims. The anchor tensor receives 2,622 identical `speech-time` labels, all index zero; 1,368 are ignored. There are no supervised context-reference, temporal-evidence or cross-claim anchor selections. All five advanced relations have zero support.

### Five independent referent heads

Counts below use stable candidate kinds/reserved identities, not arbitrary mention IDs as reusable classes. An absent kind has zero support. All heads have zero UNKNOWN; AMBIGUOUS is a field status, not an extra pointer label.

| Head / pointer kind | IT | EN | ES | Code-switch | Claims |
| --- | --- | --- | --- | --- | --- |
| subjectReferent / ctx:speaker | 1092 | 1035 | 1020 | 11 | 3158 |
| subjectReferent / ctx:observer | 23 | 11 | 3 | 0 | 37 |
| subjectReferent / MENTION | 255 | 204 | 228 | 0 | 687 |
| subjectReferent / CONTEXT_ENTITY | 36 | 36 | 36 | 0 | 108 |
| subjectReferent / NONE | 0 | 0 | 0 | 0 | 0 |
| subjectReferent / UNKNOWN | 0 | 0 | 0 | 0 | 0 |
| targetReferent / ctx:speaker | 26 | 14 | 6 | 0 | 46 |
| targetReferent / ctx:observer | 81 | 37 | 46 | 11 | 175 |
| targetReferent / MENTION | 12 | 20 | 11 | 0 | 43 |
| targetReferent / CONTEXT_ENTITY | 0 | 0 | 0 | 0 | 0 |
| targetReferent / NONE | 1287 | 1215 | 1224 | 0 | 3726 |
| targetReferent / UNKNOWN | 0 | 0 | 0 | 0 | 0 |
| ownerReferent / ctx:speaker | 1092 | 1035 | 1020 | 11 | 3158 |
| ownerReferent / ctx:observer | 23 | 11 | 3 | 0 | 37 |
| ownerReferent / MENTION | 255 | 204 | 228 | 0 | 687 |
| ownerReferent / CONTEXT_ENTITY | 36 | 36 | 36 | 0 | 108 |
| ownerReferent / NONE | 0 | 0 | 0 | 0 | 0 |
| ownerReferent / UNKNOWN | 0 | 0 | 0 | 0 | 0 |
| perspectiveReferent / ctx:speaker | 1406 | 1286 | 1287 | 11 | 3990 |
| perspectiveReferent / ctx:observer | 0 | 0 | 0 | 0 | 0 |
| perspectiveReferent / MENTION | 0 | 0 | 0 | 0 | 0 |
| perspectiveReferent / CONTEXT_ENTITY | 0 | 0 | 0 | 0 | 0 |
| perspectiveReferent / NONE | 0 | 0 | 0 | 0 | 0 |
| perspectiveReferent / UNKNOWN | 0 | 0 | 0 | 0 | 0 |
| sourceReferent / ctx:speaker | 1398 | 1286 | 1287 | 11 | 3982 |
| sourceReferent / ctx:observer | 0 | 0 | 0 | 0 | 0 |
| sourceReferent / MENTION | 8 | 0 | 0 | 0 | 8 |
| sourceReferent / CONTEXT_ENTITY | 0 | 0 | 0 | 0 | 0 |
| sourceReferent / NONE | 0 | 0 | 0 | 0 | 0 |
| sourceReferent / UNKNOWN | 0 | 0 | 0 | 0 | 0 |

The owner target equals the subject target in **3,990/3,990** claims. This is not evidence that each equality is wrong; it means copying the subject perfectly reproduces owner gold and never exercises a genuinely independent owner decision. 832 non-speaker owners are useful supervision, but must not be advertised as 3,990 difficult ownership cases.

Perspective is **always ctx:speaker**. Source is speaker in 3,982/3,990; the remaining eight are reports, IT only, all negative `goal.object`, with source=subject at the start of the claim. None tests a reporter distinct from the embedded subject inside a REPORT. Direct third-person claims do supply 824 source!=subject instances, but they do not close that report-specific gap. All 717 context-bearing observations have exactly one context entity; no example requires choosing between multiple context entities.

Of 687 mention-subject targets, 260 start the claim and 427 occur later. Thus “every subject is first token” is false. But all eight report-source targets are at claim start, owner always copies subject, perspective always selects the reserved speaker, and all 43 mention-target targets occur later. These are measured positional correlations and plausible shortcut opportunities, not proof of a learned shortcut. Runtime candidate indices for every head are preserved in machine evidence.

## 2. Semantic-family coverage

Each row below defines a distinct predicate over stored gold. Counts are **claims** unless specified; families overlap and must not be summed. “Simple temporal” means CURRENT/PAST/FUTURE labels, not necessarily an explicit span. “Owner/subject non-speaker” is an operational sensitive-case proxy. Adult predicates are restricted to `adultOnly=true`; untagged consent rows are not silently counted as adult. Arousal is a bounded lexical screen, not a full semantic detector. The raw source-family taxonomy is also preserved in curriculum.json.

| Operational family | IT | EN | ES | Code-switch | Claims | Unique claim surfaces |
| --- | --- | --- | --- | --- | --- | --- |
| negation_polarity_negative | 288 | 187 | 220 | 0 | 695 | 252 |
| negation_overt_cue | 209 | 110 | 144 | 0 | 463 | 194 |
| simple_temporal_non_atemporal | 950 | 830 | 831 | 11 | 2622 | 896 |
| temporal_evidence | 160 | 115 | 114 | 0 | 389 | 147 |
| advanced_temporal | 0 | 0 | 0 | 0 | 0 | 0 |
| subject_non_speaker | 314 | 251 | 267 | 0 | 832 | 276 |
| target_present | 119 | 71 | 63 | 11 | 264 | 150 |
| owner_non_speaker | 314 | 251 | 267 | 0 | 832 | 276 |
| perspective_non_speaker | 0 | 0 | 0 | 0 | 0 | 0 |
| source_differs_perspective | 8 | 0 | 0 | 0 | 8 | 8 |
| source_differs_subject | 306 | 251 | 267 | 0 | 824 | 268 |
| third_party_report | 8 | 0 | 0 | 0 | 8 | 8 |
| belief | 0 | 0 | 0 | 0 | 0 | 0 |
| hypothesis | 89 | 89 | 89 | 0 | 267 | 72 |
| request | 19 | 4 | 4 | 0 | 27 | 24 |
| command | 0 | 0 | 0 | 0 | 0 | 0 |
| correction | 4 | 3 | 3 | 0 | 10 | 10 |
| goal_desire_all | 245 | 192 | 190 | 0 | 627 | 165 |
| goal_desire_assertion | 228 | 180 | 186 | 0 | 594 | 139 |
| preference | 321 | 329 | 320 | 0 | 970 | 192 |
| entity_spans | 800 | 735 | 761 | 0 | 2296 | 517 |
| subject_spans | 269 | 240 | 258 | 0 | 767 | 236 |
| object_spans | 1336 | 1223 | 1224 | 11 | 3794 | 1051 |
| multi_claim | 513 | 513 | 513 | 0 | 1539 | 492 |
| ambiguity | 0 | 0 | 0 | 0 | 0 | 0 |
| abstained | 63 | 63 | 63 | 0 | 189 | 54 |
| unknown_any_field | 63 | 63 | 63 | 0 | 189 | 54 |
| unresolved_predicate | 1 | 0 | 0 | 11 | 12 | 12 |
| adult_consent | 29 | 18 | 18 | 0 | 65 | 26 |
| adult_refusal_excluding_withdrawal | 25 | 18 | 18 | 0 | 61 | 22 |
| adult_withdrawal | 1 | 0 | 0 | 0 | 1 | 1 |
| adult_desire_assertion | 15 | 0 | 0 | 0 | 15 | 12 |
| adult_request | 15 | 0 | 0 | 0 | 15 | 12 |
| adult_code_switch | 0 | 0 | 0 | 11 | 11 | 11 |
| adult_arousal_lexical_screen | 0 | 0 | 0 | 0 | 0 | 0 |
| ownership_sensitive_non_speaker | 314 | 251 | 267 | 0 | 832 | 276 |

The 699 multi-claim observations are 233 per IT/EN/ES, with 1,539 total claims; code-switch has zero. Whole-observation multi-claim quantity does not establish semantic variety: these contain only 492 distinct normalized claim surfaces, drawn heavily from repeated basic families.

The migration report's “adult desire = 30” combines **15 desire assertions and 15 requests**. CP37 separates them. Its “adult refusal = 62” includes the sole withdrawal; CP37 reports **61 refusal + one withdrawal**. Consent/refusal EN and ES each have only five unique claim surfaces despite 18 claim instances per family/language. Desire assertions and adult requests are IT-only; withdrawal has one IT example, zero EN/ES. No arousal statement was identified by the bounded screen or inspected adult block; this is distinct from a desire-to-act assertion.

All 11 code-switch-labelled rows use the same `Voglio <English term> con te` structure and `speech.unresolved`; no general IT/EN/ES switching variety, noisy negation, multilingual uncertainty or non-adult switching family is represented under that label. Mixed English terms also occur in some IT-labelled adult rows; therefore 11 is the **declared code-switch count**, not an exhaustive language-identification claim. Malformed synthetic requests are not credited as intentionally annotated noisy-input robustness.

189 ABSTAINED examples exist, so “no abstention data” would be false. They are entirely polarity UNKNOWN: 183 QUESTION and six REQUEST. All role pointers are resolved/known absence; zero AMBIGUOUS fields or claims. No referent ambiguity, unknown binding or temporal-anchor uncertainty is taught. Abstention/status is validator behavior, not an extra neural head; the current target builder does not directly supervise a status tensor. These examples provide polarity UNKNOWN supervision, not calibrated confidence evidence.

## 3. Pedagogy and annotation hazards

### Repetition, effective diversity and contradictions

- 3,150 observations collapse to **1,589 exact language/text surfaces**, with **1,561 repeated excess instances (49.56%)**. The maximum exact surface appears 14 times; adult baseline consent/refusal each repeat one sentence 14 times per language.
- 3,990 claims collapse to **1,112 normalized language/claim surfaces**, with **2,878 repeated excess instances (72.13%)**. This is input diversity, not statistically independent effective sample size.
- The defined delexicalization yields **333 skeleton groups**. Largest group: 36 claims; top ten: 359. Inverse-concentration proxy is 155.68 groups; it must not be called a measured gradient/sample ESS. Many skeletons differ only in small template choices.
- Whole-observation same-text/same-context contradictory gold: **0**; claim-surface gold conflicts after candidate-relative normalization: **0** under the implemented comparison. This bounded result does not certify all paraphrases semantically consistent.
- Near-surface screening finds **1,077 pairs involving 481 observations**. Some are valuable opposite-polarity or other contrast pairs; they are not all harmful duplicates. First 50 examples plus full algorithm/counts are persisted. No deletion/deduplication or retraining occurred.

These repetitions would repeat exposures under ordinary uniform sampling. No actual sampler, gradient magnitudes, effective training weights or forgetting has been measured. Do not assume the former Student-4 repeat/loss settings apply to Student-5; training-strategy redesign is outside scope.

### Concrete semantic findings and review disposition

1. **Cue/polarity independence is absent from positive supervision.** All 463 claims with cues are NEGATIVE. No positive/unknown polarity has any annotated cue, despite the V3 contract allowing both. 232 negative claims have no cue; lexical dislike/implicit opposition can validly explain such cases, so they are not counted as omissions. Cues are only IT `non/più`, EN `not/cannot`, ES `no`; no observed never/nunca/mai or broader construction variety. No cue equals an entire claim span: the V2 full-source convention was actually replaced. The migration source gates cue recovery on old negation annotations, which is a documented mechanism preserving old selection boundaries; it does not prove every cue is wrong.
2. **Missing explicit temporal spans: six confirmed IT examples in the bounded screen.** `mx-v2-train-it-generalization-known_third_party-002` contains “attualmente” with no temporalEvidence. `mx-v22a-it-core-067/072/077/082/087` contain “più tardi” with no evidence span. This violates preservation of explicit temporal expressions independently of how the final relation is adjudicated. The catalog screen is a lower bound, not universal recall.
3. **Temporal target convention requires adjudication.** 23 goal claims with future wording (`domani/later/più tardi`) have CURRENT, whereas base future-goal templates teach FUTURE. Examples: `mx-v22a-en-core-002`, `mx-v22a-it-core-003`. Time of present wanting and time of the desired action are distinct readings; this audit does not invent corrected labels. The corpus does not expose an explicit consistent distinction, creating a plausible template-dependent teaching conflict.
4. **Code-switch desires are taught as unresolved.** All 11 declared code-switch rows (`mx-v22a-adult-it-049` through `059`) contain explicit desire wording and target, yet have `speech.unresolved`. Example `mx-v22a-adult-it-050`: “Voglio kiss con te”. V3 supports `goal.object` and says unfamiliar/adult vocabulary alone must not drive rejection. This is an objective label concentration plus semantic mismatch with vocabulary-neutral goal evidence; it is not measured moderation or a learned confidence penalty. No replacement data/labels were generated.
5. **Reported perspective conflicts with the intended distinctions.** All eight report examples retain speaker perspective. `mx-v22a-it-core-113` (“Giulia dice che non vuole venire a casa”) has source/subject/owner Giulia but perspective speaker. Contract section 5 and its normative Anna-said example require attention to the reported viewpoint. This is a concrete contract tension for Supervisor adjudication, not evidence that any non-speaker owner should mechanically supply perspective. No reporter!=embedded-subject REPORT is taught.
6. **Explicit and implicit subject evidence must not be conflated.** A bounded IT/ES first-person-prefix screen covers 404 instances (216 IT/188 ES) with empty subject spans and speaker pointers, zero violations of that intended implicit-subject convention. In contrast, 628 English instances (185 unique surfaces) begin with explicit “I” and still have no subject span. Example `mx-train-en-00003`, “I love jazz”. The token-head responsibility is explicit subject evidence; this inherited annotation convention requires reconciliation. These are not 628 failures of the *implicit* first-person rule. The pattern is language-conditioned; the Italian article “I” was explicitly excluded from the English-pronoun screen.
7. **Template grammar/participant quality.** Six adult-request row instances/four unique surfaces contain “con te con me” (`016/017/018/024/028/029` in `mx-v22a-adult-it-*`). Other reviewed requests contain reflexive forms with an externally directed target (`015/025/026`). These mechanically assembled participant phrases need linguistic review; they are not corrected here or counted as proven learned ownership corruption.
8. **BELIEF zero can hide wrapper misannotation.** Six reviewed `consider/considero` opinion/self-description claims retain DIRECT, e.g. `mx-v2-train-en-attribute-00`. The opinion/thought definition of BELIEF merits explicit adjudication. A keyword alone is not a sufficient automatic relabeling rule, so six is a review set, not six indisputable errors.
9. **Metalinguistic negation review.** `mx-v2-train-es-generalization-dialogue_correct-005` includes “no, mi residencia correcta es Alicante” with positive polarity and no cue. V3 preserves metalinguistic negation cues while allowing positive composed polarity. The audit flags one relevant discourse case; the other eight lexical cue-screen hits are affirmative/comparative “più” and are **false positives as negation omissions**, not defects. Five of them separately reveal the temporal-span omission already counted above.

All row IDs, original labels and bounded screens are in semantic-review.json/review-evidence.json. No edits, replacement gold, augmentation or evaluator changes were made. Findings distinguish annotation defects, coverage gaps and adjudication questions instead of turning every screen into an error count.

### Pristine encoder risk

The artifact contains mostly synthetic Matrix-specific labels with strong default correlations and no general representation-retention target. It cannot demonstrate preservation of pretrained multilingual abilities. If later work changes encoder weights, overspecialization/forgetting is a **PLAUSIBLE_RISK**; actual damage to pristine is **NOT_ESTABLISHED**. Under a genuinely frozen-backbone strategy encoder weights would not change, but heads can still learn shortcuts. No model was loaded, compared or changed here, and no training strategy is prescribed by this audit.

## 4. Student-4 regression comparison

Authoritative persisted history read here: [v2.1 post-run report](STUDENT_4_V21_POST_DEV_REPORT.md), [v2.2A controlled repair report](STUDENT_4_V22A_CONTROLLED_REPAIR_REPORT.md), [v2.1 infrastructure stop](STUDENT_4_V21_STOP_REPORT.md), [v2.2A repair plan](STUDENT_4_V22A_REPAIR_PLAN.md). These reports document historical metrics; no DEV payload or model was opened. v2 baseline values are cited only where these persisted reports explicitly compare them.

`DIRECTLY_SUPPORTED` means a documented historical observation or byte-identical source lineage, not a proven cause of Student-5 failure. `PLAUSIBLE_RISK` is a curriculum-to-possible-recurrence inference. `NOT_ESTABLISHED` marks absent causal/per-head comparison evidence. Hypotheses in the prepared repair plan are not treated as results; the final measured report supersedes its intended balance claims.

| Pattern | Historical evidence (DIRECTLY_SUPPORTED) | Student-5 exposure | Recurrence linkage |
| --- | --- | --- | --- |
| Negation | v2.1→v2.2A Matrix F1 0.509169→0.490644; IT 0.247012→0.287037; ES 0.158228→0.129534 | 463 cue claims, narrow cue inventory, all cues NEGATIVE, O dominance | PLAUSIBLE_RISK |
| Temporality | Matrix accuracy 1.0→0.956790; IT 1.0→0.870370; P0.5 0.892857→0.880952 | PAST 14 (one EN/ES); anchor constant; six missing spans; time convention review | PLAUSIBLE_RISK |
| Referents | v2.1 referent-family exact set 0.760943; authority/referent residuals 20→62 after repair | No UNKNOWN/AMBIGUOUS role; single context entity only; copyable roles | PLAUSIBLE_RISK |
| Third-party/report | v2.1 family exact set 0.72 (IT 0.613333, ES 0.56) | Eight negative-goal reports, IT-only; all source=subject; no embedded reporter contrast | PLAUSIBLE_RISK |
| Correction | Exact 1/6 in v2.1 and v2.2A | Only 10 CORRECT targets; one metalinguistic cue review | PLAUSIBLE_RISK |
| Goal/request | v2.1 goal-family exact set 0.714286; request 0/6 in both reports | 627 nominal goals include sparse requests; 27 REQUEST (19/4/4); malformed IT block | PLAUSIBLE_RISK |
| Ownership | Two P0.5 IT corruptions persisted; Matrix zero | 832 non-speaker owners, but owner=subject always; zero unknown binding | PLAUSIBLE_RISK |
| Span decoding | Residuals 269→293; P0.5 entity F1 0.945701→0.903670 | Rare subject/temporal positives, no multiword PERSON/subject, explicit-I omission | PLAUSIBLE_RISK |
| IT/ES robustness | Matrix ES exact set 0.595238→0.523810; IT predicate 1.0→0.808642; EN still strongest | IT-heavy repair inherited; class-specific asymmetry persists despite near-balanced overall totals | PLAUSIBLE_RISK |
| Source/perspective independent V3 head | Student-4 did not have the independent V3 source head; no comparable head metric | Perspective constant and source distribution 99.8% speaker | NOT_ESTABLISHED for historical same-head regression; PLAUSIBLE_RISK for V3 |
| Shared repair lineage | V2 TRAIN and 375-row v2.2A repair exact source hashes match V3 migration inventory | Same source surfaces materially retained after V3 reannotation | DIRECTLY_SUPPORTED for lineage; causal contribution NOT_ESTABLISHED |

The v2.1 import error was an infrastructure stop after successful training, not a semantic failure. Subsequent published evaluation provides the semantic metrics above. The v2.2A intervention changed data, loss and repeat settings together; the reports do not isolate curriculum causation. Student-5 uses a different encoder/architecture and V3 cue semantics, so V2 negation F1 is a warning pattern, not a numerically transferable V3 baseline.

## 5. Minimal TRAIN-only repair categories for Supervisor disposition

These are categories identified by the audit, not an implementation plan, approved new labels, numeric quotas or generated examples. No remediation begins here.

1. Adjudicate and correct existing semantic inconsistencies in a **new** TRAIN version: missing temporal cues, time-of-desire versus action convention, explicit/implicit subject evidence, reported viewpoint, code-switch desire ontology, malformed/reflexive request participants, opinion wrappers and metalinguistic cue treatment.
2. Supply targeted IT/EN/ES support for genuinely missing behaviors: COMMAND, BELIEF, uncertain/ambiguous role binding, non-speaker viewpoint and multi-actor source/perspective distinctions; preserve correct self and direct-third-party cases without forcing artificial role inequality.
3. Supply coherent temporal and span diversity: usable past support in all three languages, advanced relation/anchor cases required by the contract, plural spans and multiword subject/person extent, plus negation-cue/polarity contrasts. Zero advanced support must not silently redefine the frozen contract.
4. Separate adult consent, refusal, withdrawal, desire assertion, request and arousal coverage across languages and broader code-switch contexts; preserve vocabulary-neutral semantics and adult-only scope.
5. Address exact/template repetition and class/language dominance only after annotation adjudication, preserving useful contrast pairs and provenance in a new immutable TRAIN artifact. Audit does not select a sampler, loss, encoder unfreezing strategy or augmentation volume.

Training on the existing v1 unchanged is therefore not recommended for the full assigned V3 behavior. There is useful retained supervision, but structural validity and raw row count are insufficient teaching-quality evidence. The Supervisor may accept/reject this audit and issue a bounded next task; Work neither self-accepts the gate nor executes repairs.

## Reproduction, persistence and stop

From this delivery commit, Python 3.10+; no ML libraries required:

```bash
python reports/evidence/student5-path-b-cp37-train-audit/audit_curriculum.py --train data/student5_v3 --source matrix_nlu --tree reports/evidence/student5-path-b-cp37-train-audit/inputs-tree.json --output /tmp/student5-cp37-review
python reports/evidence/student5-path-b-cp37-train-audit/review_semantics.py --train data/student5_v3 --output /tmp/student5-cp37-review/semantic-review.json
```

Only the selected pure target-builder functions are called; no training command is invoked. Inputs-tree.json binds input/source/report identities to starting HEAD. SHA256SUMS covers the new evidence/report and continuity. CP36 is unchanged. No files outside the new CP37 report/evidence and `docs/WORK_CONTINUITY_STUDENT_5.md` are intentionally modified; final remote tree comparison verifies this before handoff.

Disposition: **return this substantive audit to Supervisor GPT; stop and await the next assignment**. CP36 Gate B readiness remains BLOCKED. No model/optimizer process or workflow was launched or left active. No remediation or subsequent work is running.
