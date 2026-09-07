Supervisor GPT — Student-5 TRAIN Repair Specification Report

**REPAIR_SPECIFICATION = BLOCKED_NEEDS_SUPERVISOR_DECISION**

Checkpoint CP38, 2026-09-07. Issuer/reviewer: Supervisor GPT; final authority: Alberto; executor: ChatGPT Work.
Repository `MATRIXNEO23/matrix-understanding-lab`; branch `student5-path-b-v3`.
Starting HEAD `6cd1fac17bdceca742a8bf2932e0872ee5907601` verified remotely before work.
Repair specification ID `student5-v3-train-repair-spec-cp38-v1`.
Final delivery HEAD is the immutable introducing commit of this report, resolved with `git log -1 --format=%H -- reports/STUDENT_5_TRAIN_REPAIR_SPECIFICATION_CP38.md`; its exact SHA is returned after remote verification. This avoids an impossible self-referential commit hash inside its own content.

## Executive finding and scope

The conservative repair is now specified for review, with issue dispositions, preservation rules, lineage and later acceptance checks. It cannot be treated as an approved or executable dataset repair: time-of-desire semantics, reported viewpoint, opinion wrappers, participant intent and metalinguistic scope remain unresolved. Additional role-divergence and no-claim semantics must not be invented to fill coverage. These precise decisions cause the BLOCKED verdict; the document itself is complete, not an abandoned attempt.

Confirmed span defects can be corrected in a separately authorized future version. Sparse classes require targeted teaching, not bulk relabeling of valid examples. Existing valid equality of roles, implicit first-person subjects, cue-free semantic opposition and meaningful contrasts must survive. No new example sentences or replacement gold are authored by this specification. All row references below are existing CP37 evidence, and all future actions are proposals.

Only documentation and CP37 evidence payloads were read in this assignment. No raw TRAIN shards, DEV payloads, Frozen payloads, models or evaluator/decoder code were loaded or executed. No training, optimizer, backprop, augmentation, dataset creation/change, evaluator/decoder/threshold change, quantization, Assembling integration or promotion occurred. No workflow or background model process was launched. Gate A and TASK 2.3 were not repeated. CP36 Gate B readiness remains independently BLOCKED and is not closed by this design.

## Source identity and evidence limits

The owner-supplied starting HEAD contains the assignment prompt; its internal predecessor reference `e81a2ae9e1d60c6af61a7d8d1baabed9171f3166` identifies accepted CP37, not an instruction to roll the branch back. The exact source files read and their Git blob/SHA-256 identities are in [input-identities.json](evidence/student5-path-b-cp38-repair-spec/input-identities.json). All 140 CP37 inspected input identities match current Git metadata, including the 130 TRAIN artifact paths. This is an identity bridge to executed CP37 findings; no fresh full TRAIN checksum audit or model test is claimed.

Canonical base: `student5-matrix-nlu-v3-train-v1`, `data/student5_v3/`, 3150 observations/3990 claims. Ordered SHA-256 `1118a900026f48cfcc290c3f9dc52a1a019a6a1f4761661f326c33770523140e`; migration manifest SHA-256 `87b4a43035d2e3d84a6d599e1f81b497af6e2f36e4ef2c470adb87341c17da98`. V3 fingerprint `7b0646e44243ad897760c0fcadbe141f1b8e88e3fd8d63a1789106571b9987b0` remains unchanged. Lineage: Matrix V2 TRAIN SHA `5118d37ce2ab19d5be171f757f448698085e3c222a4a627f9838329836185820` and v2.2A repair TRAIN SHA `8be02976d46ba47d746ff7307d688d93595453221965b3de995d4b1de655799f`. Excluded combined P0.5 partitions remain excluded; their payloads were not opened.

Primary sources: [CP37 audit](STUDENT_5_TRAIN_CURRICULUM_AUDIT_CP37.md), its [census](evidence/student5-path-b-cp37-train-audit/curriculum.json), [semantic review](evidence/student5-path-b-cp37-train-audit/semantic-review.json), [review screens](evidence/student5-path-b-cp37-train-audit/review-evidence.json), [migration report](STUDENT_5_TRAIN_V3_MIGRATION.md), and [frozen V3 contract](../docs/MATRIX_NLU_CONTRACT_V3.md). “Frozen contract” here means the fixed specification document, never the held-out Frozen dataset. Historical reports are listed in the safeguard section. Earlier migration P1/nonblocking labels remain historical evidence; accepted CP37 subsequently required repair before training. The migration report's adult desire30 combines ASSERT15+REQUEST15; CP37 correctly separates them. Its refusal62 includes withdrawal1; CP37 uses refusal61 plus withdrawal1. No contradictory claim of a new recount is made.

CP37 lexical token counts are annotation diagnostics, not BERT/WordPiece counts, gradient evidence or trained quality. Duplicate screens establish concentration, not automatic semantic equivalence. The 628 explicit-I and 404 implicit-subject groups have only 20 stored sample IDs each; their exact selectors and total counts are preserved, but no fabricated complete row manifest is supplied.

## Issue-by-issue repair specification

Every action below is future-only and requires a later assignment. “Semantic decision” is separate from owner approval to execute: even rows marked false are not authorized for mutation now. The machine-readable [issue register](evidence/student5-path-b-cp38-repair-spec/issue-register.json) preserves all required fields.

### R01 — MISSING_CURRICULUM_COVERAGE

| Required item | Specification |
| --- | --- |
| Evidence | reports/evidence/student5-path-b-cp37-train-audit/curriculum.json#/sequenceLabelCounts/dialogueAct |
| Why V3 requires attention | V3 sections 4.1 and 14 distinguish imperative force from request. |
| Wrong versus sparse | COMMAND=0; REQUEST=27 (19/4/4); CORRECT=10 (4/3/3); sparsity is not proof current labels are wrong. |
| Minimal proposed action | Propose separate imperative/request/assertion/question/correction contrast families, including negated and third-party acts; review conversational force in each language. |
| Preserve | Valid 198 questions, existing requests/corrections and direct assertions. |
| Existing-row disposition | No blanket ASSERT→COMMAND or question-mark→QUESTION mapping. Malformed requests governed by A06. |
| Proposed new families | Command versus polite request; correction versus denial; same predicate under different acts. |
| Languages | IT/EN/ES; semantically valid code-switch |
| Heads / fields | dialogueAct, boundary, predicate, targetReferent, polarity |
| Overcorrection risk | Turning every imperative form into command or every interrogative into question. |
| Student-4 recurrence | Request 0/6 and correction 1/6 historically; recurrence plausible, cause unproven. |
| Semantic decision required | False |

### R02 — MISSING_CURRICULUM_COVERAGE

| Required item | Specification |
| --- | --- |
| Evidence | reports/evidence/student5-path-b-cp37-train-audit/curriculum.json#/sequenceLabelCounts/claimKind |
| Why V3 requires attention | V3 4.2: DIRECT/REPORT/BELIEF/HYPOTHESIS are independent of act and truth. |
| Wrong versus sparse | BELIEF=0; REPORT=8 IT-only negative goals; HYPOTHESIS=267 is useful. |
| Minimal proposed action | Propose overt belief and report families with varied holders, embedded subjects, predicates, polarity and order; preserve DIRECT/HYPOTHESIS. |
| Preserve | 267 hypotheses, valid direct third-party assertions and report wording. |
| Existing-row disposition | Six opinion wrappers and eight report viewpoints await D02/D03, not automatic relabeling. |
| Proposed new families | Self/other belief; reporter distinct from embedded subject; report versus presence.reported predicate. |
| Languages | IT/EN/ES; code-switch attribution |
| Heads / fields | claimKind, dialogueAct, sourceReferent, perspectiveReferent, subjectReferent, ownerReferent |
| Overcorrection risk | Using REPORT as predicate or BELIEF as downstream BeliefState; keyword-only labels. |
| Student-4 recurrence | Third-party family weakness documented; independent V3 source-head failure not measured. |
| Semantic decision required | True |

### R03 — MISSING_CURRICULUM_COVERAGE

| Required item | Specification |
| --- | --- |
| Evidence | reports/evidence/student5-path-b-cp37-train-audit/curriculum.json#/statuses |
| Why V3 requires attention | V3 4/8: UNKNOWN differs from NONE; ambiguity is field status with UNKNOWN primary pointer. |
| Wrong versus sparse | No role UNKNOWN/AMBIGUOUS, act/kind/temporal UNKNOWN; 189 abstained polarity-UNKNOWN claims already exist. |
| Minimal proposed action | Propose linguistically motivated unresolved acts/kinds/roles/temporal composition and tied-candidate examples, paired with disambiguated versions; use only relevant unknown fields. |
| Preserve | 189 existing abstained claims and correctly absent target NONE. |
| Existing-row disposition | Do not mark clear labels unknown to fill a quota; no change to existing resolved examples without evidence. |
| Proposed new families | Ambiguous referent choice, absent required reference, unresolved flat scope, unclear act; separate known absence. |
| Languages | IT/EN/ES and code-switch |
| Heads / fields | All affected sequence heads; fieldStatus, alternatives, interpretationStatus; no new status head |
| Overcorrection risk | Inventing probabilistic confidences or universal ambiguity labels; treating unfamiliar words as unknown. |
| Student-4 recurrence | Referent errors historically observed; fabricated uncertainty would damage valid coverage. |
| Semantic decision required | False |

### R04 — ROLE/VIEWPOINT_IMBALANCE

| Required item | Specification |
| --- | --- |
| Evidence | reports/evidence/student5-path-b-cp37-train-audit/curriculum.json#/roleEqualities |
| Why V3 requires attention | V3 5: five roles are independently justified; equality may be correct. |
| Wrong versus sparse | owner=subject 3990/3990; perspective=speaker 3990/3990. Not 3990 annotation defects. |
| Minimal proposed action | Preserve correct equality; require per-role linguistic rationale, counterpart examples with changed role evidence, and Supervisor decision on valid owner≠semantic-subject and source≠perspective constructions within flat V3. |
| Preserve | 832 non-speaker owners; 824 direct source≠subject cases; legitimate speaker perspective. |
| Existing-row disposition | Eight report perspectives reviewed in A03; no mass copying or forcing inequality. |
| Proposed new families | Multi-actor attribution/viewpoint with explicit evidence, and only semantically defensible divergent owner cases after D07. |
| Languages | IT/EN/ES; code-switch where natural |
| Heads / fields | subject/target/owner/perspective/sourceReferent, candidate identity |
| Overcorrection risk | Five distinct roles are not a requirement that all five identities differ in every example; inventing owner labels solely to break equality. |
| Student-4 recurrence | Two IT ownership corruptions persisted historically; curriculum copying risk plausible, causation not established. |
| Semantic decision required | True |

### R05 — ROLE/VIEWPOINT_IMBALANCE

| Required item | Specification |
| --- | --- |
| Evidence | reports/evidence/student5-path-b-cp37-train-audit/curriculum.json#/roleMentionPositions |
| Why V3 requires attention | V3 5/11 prohibit first-recent selection and substituting provenance category for identity. |
| Wrong versus sparse | All 717 context-bearing observations offer one context entity; eight report sources all start the claim; no ambiguous choice. |
| Minimal proposed action | Propose multiple eligible context entities, reordered mentions, explicit binding and controlled distractors; retain deterministic IDs and overflow/critical-candidate abstention contract. |
| Preserve | Existing known-entity links and all valid multi-entity mention evidence. |
| Existing-row disposition | No reassignment based on candidate index or identity name. |
| Proposed new families | Same roles with mention/order changes; two or more context choices with unique binding or explicit ambiguity. |
| Languages | IT/EN/ES; code-switch referents |
| Heads / fields | All five pointers, subject/entity spans, candidate table/mask/status |
| Overcorrection risk | New contexts that accidentally change truth conditions; treating index diversity as semantic correctness. |
| Student-4 recurrence | Authority/referent residuals 20→62 historically; first-candidate shortcut remains only a plausible risk. |
| Semantic decision required | False |

### R06 — TEMPORAL_IMBALANCE

| Required item | Specification |
| --- | --- |
| Evidence | reports/evidence/student5-path-b-cp37-train-audit/curriculum.json#/sequenceLabelCounts/temporalRelation |
| Why V3 requires attention | V3 4.4/7 require time distinctions independent of predicate. |
| Wrong versus sparse | PAST=14 (12/1/1); eleven IT goals with da ieri. FUTURE=510 goals+2 grants. |
| Minimal proposed action | Propose past/current/future contrasts across suitable existing predicates and multilingual wording; distinguish ongoing-from-past from completed state, without mechanically mapping tense tokens. |
| Preserve | Valid 1368 ATEMPORAL, current states and coherent future examples. |
| Existing-row disposition | 23 CURRENT goal cases held for D01; no blanket tense rewrite. |
| Proposed new families | Past residence/work/presence/consent and corresponding present/future where ontology applies. |
| Languages | IT/EN/ES; code-switch time expressions |
| Heads / fields | temporalRelation, temporalEvidence, predicate, boundary |
| Overcorrection risk | Reclassifying stable atemporal properties or present desire from a future adverb alone. |
| Student-4 recurrence | Historical IT temporal 1→0.870370; recurrence plausible, no causal transfer. |
| Semantic decision required | False |

### R07 — TEMPORAL_IMBALANCE

| Required item | Specification |
| --- | --- |
| Evidence | reports/evidence/student5-path-b-cp37-train-audit/curriculum.json#/temporalAnchorCounts |
| Why V3 requires attention | V3 4.4/7 requires explicit reference identity; 16th conceptual semantics retain 17 tensors. |
| Wrong versus sparse | BEFORE/AFTER/DURING/RECURRENT/AT_REFERENCE=0; all 2622 supervised anchors speech-time. |
| Minimal proposed action | Propose each advanced relation with a justified anchor: evidence ID, context time, or other flat claim where supported; require anchor-choice contrasts and unresolved missing-reference cases. |
| Preserve | Speech-time anchoring for CURRENT/PAST/FUTURE and ignored anchor on ATEMPORAL. |
| Existing-row disposition | No global reassignment of existing anchors. |
| Proposed new families | Before/after/during referenced event; recurrent schedule; context-reference placement; different valid anchor choices. |
| Languages | IT/EN/ES; selected code-switch |
| Heads / fields | temporalRelation label+anchor tensor, temporal spans, claim IDs/status |
| Overcorrection risk | Inventing wall-clock dates, overlapping nested claims, or new anchor policy outside V3; RECURRENT not forced to use a made-up anchor. |
| Student-4 recurrence | Historical temporal weakness relevant as risk; Student-4 lacks equivalent advanced-anchor metric. |
| Semantic decision required | False |

### R08 — CONFIRMED_ANNOTATION_DEFECT

| Required item | Specification |
| --- | --- |
| Evidence | reports/evidence/student5-path-b-cp37-train-audit/review-evidence.json#/heuristicReviewScreens/temporalCatalogMissing |
| Why V3 requires attention | V3 7 preserves every explicit temporal span independently of relation. |
| Wrong versus sparse | Six confirmed missing IT spans: attualmente and five più tardi. |
| Minimal proposed action | Specify adding only the complete attualmente/più tardi evidence in future v2, verified at observation offsets; relation separately gated by D01. |
| Preserve | Original text, candidates and unaffected gold. |
| Existing-row disposition | A01 CORRECT_IN_FUTURE_V2; no bytes changed now. |
| Proposed new families | No new rows required to fix these six; broader temporal families R06/R07. |
| Languages | IT corrections; IT/EN/ES later reviewed span census |
| Heads / fields | temporal evidence IDs/spans; token.temporal |
| Overcorrection risk | Confusing più tardi with negation or silently changing CURRENT while adding evidence. |
| Student-4 recurrence | Span and temporal regression warning, not proof these six caused it. |
| Semantic decision required | False |

### R09 — SEMANTIC_POLICY_NEEDS_SUPERVISOR_DECISION

| Required item | Specification |
| --- | --- |
| Evidence | reports/evidence/student5-path-b-cp37-train-audit/semantic-review.json#/groups/futureWordingCurrentRelation |
| Why V3 requires attention | V3 supplies one relation for each atomic proposition, not separate desired-event and desire-state clocks. |
| Wrong versus sparse | 23 goal/CURRENT cases with later/domani/più tardi versus FUTURE templates; two plausible time targets. |
| Minimal proposed action | D01 must select consistent annotation scope and handling of mixed-time desire; retain explicit time spans under either decision; ambiguous unresolved flat cases excluded pending decision. |
| Preserve | Unambiguous future event goals and current wanting whose timing is explicit. |
| Existing-row disposition | A02 NEEDS_SUPERVISOR_SEMANTIC_DECISION. |
| Proposed new families | Matched present wanting/future desired action contrasts only after rule accepted. |
| Languages | Existing IT15/EN8; rule applies ES/code-switch too |
| Heads / fields | predicate, temporalRelation/anchor, temporalEvidence, boundary/status |
| Overcorrection risk | Automatic future-word→FUTURE or keeping all CURRENT without resolving the competing convention. |
| Student-4 recurrence | Historical temporal failures support caution, not one unique corrected gold. |
| Semantic decision required | True |

### R10 — NEGATION/POLARITY_CONTRAST_GAP

| Required item | Specification |
| --- | --- |
| Evidence | reports/evidence/student5-path-b-cp37-train-audit/curriculum.json#/cueByPolarity |
| Why V3 requires attention | V3 6 separates overt cues from composed polarity. |
| Wrong versus sparse | 463 cue claims all NEGATIVE; no cue with POSITIVE/UNKNOWN; 232 negative/no-cue cases may be correct. |
| Minimal proposed action | Propose overt-cue positive/unknown composition, negative concord, double negation and cue-free lexical opposition; preserve every representable cue and flat-scope abstention. |
| Preserve | Correct 232 negative/no-cue cases after semantic review; 13 multiple-cue groups and valid negatives. |
| Existing-row disposition | Do not manufacture a cue for semantic opposition; A09 handles metalinguistic case. |
| Proposed new families | never/nunca/mai and morphological/lexical diversity, positive double-negation versus negative-concord contrasts where interpretation supports it. |
| Languages | IT/EN/ES; code-switch negation |
| Heads / fields | negation BIO groups, polarity, boundary, interpretationStatus |
| Overcorrection risk | Treating two negatives as universally positive across languages; reverting V2 full-scope spans. |
| Student-4 recurrence | Historical negation F1 losses directly supported; V2 full-scope metric is not V3 cue baseline. |
| Semantic decision required | False |

### R11 — CONFIRMED_ANNOTATION_DEFECT

| Required item | Specification |
| --- | --- |
| Evidence | reports/evidence/student5-path-b-cp37-train-audit/semantic-review.json#/groups/explicitFirstPersonMissingSubject |
| Why V3 requires attention | V3 token.subject preserves explicit grammatical/semantic subject evidence. |
| Wrong versus sparse | 628 EN explicit claim-initial I instances omit span; distinct from 404 valid bounded implicit IT/ES cases. |
| Minimal proposed action | Propose explicit I span restoration only for the exact bounded set, verifying each observation offset and grammatical role; preserve speaker pointer; review other explicit-subject omissions separately, not inferred as confirmed. |
| Preserve | 404 compliant implicit-first-person instances; all correct non-speaker subject spans. |
| Existing-row disposition | A05 CORRECT_IN_FUTURE_V2; exact selector preserved; CP37 stores only 20 sample IDs for this 628-count group. |
| Proposed new families | Broader explicit/implicit subject contrasts without changing speaker identity. |
| Languages | EN correction; IT/EN/ES contrast |
| Heads / fields | subjectSpans/token.subject; retain subjectReferent and other validated fields |
| Overcorrection risk | Annotating implicit pronouns that are not present; treating Italian article I as English I; extending regex to unreviewed rows. |
| Student-4 recurrence | Historical span weakness supports repair need; BERT subword counts not measured here. |
| Semantic decision required | False |

### R12 — SPAN/ENTITY_COVERAGE_GAP

| Required item | Specification |
| --- | --- |
| Evidence | reports/evidence/student5-path-b-cp37-train-audit/curriculum.json#/tokenEffectiveSupport |
| Why V3 requires attention | V3 3.1 preserves all non-overlapping groups; character spans differ from tokenizer pieces. |
| Wrong versus sparse | No multiword subject/PERSON; object/subject/temporal multi-group=0. Lexical I labels missing is not evidence of BERT behavior. |
| Minimal proposed action | Propose semantically natural multiword person/subject and plural evidence groups; whole-span and multi-claim examples with independently justified pointers and boundaries. |
| Preserve | 699 multi-claim rows, 324 multi-entity claims, existing plural negation and valid multiword locations/objects. |
| Existing-row disposition | No artificial split of one word/mention to populate an I label; no merging independent claims. |
| Proposed new families | Multiword PERSON/subject; several temporal expressions and other non-overlapping groups only if one atomic claim permits them. |
| Languages | IT/EN/ES; code-switch names/expressions |
| Heads / fields | Six token heads, mentions, entityMentionIds, pointers, sourceSpan |
| Overcorrection risk | Destroying atomicity or duplicate mention identity; filling label counts through tokenizer artifacts. |
| Student-4 recurrence | Span residuals 269→293 and entity F1 decline historically; no tested V3 tokenizer effect. |
| Semantic decision required | False |

### R13 — ADULT_INTIMACY_SEMANTIC_GAP

| Required item | Specification |
| --- | --- |
| Evidence | reports/evidence/student5-path-b-cp37-train-audit/curriculum.json#/familyCoverage |
| Why V3 requires attention | V3 13 keeps desire/request/grant/refusal/withdrawal/boundary distinct and vocabulary-neutral. |
| Wrong versus sparse | Adult desire ASSERT15 IT; REQUEST15 IT; consent65, refusal61, withdrawal1 IT; EN/ES consent/refusal repetitive. |
| Minimal proposed action | Propose separate adult-only families for desire assertion, request, grant, refusal, withdrawal/revocation, boundary and current-desire-versus-consent; use existing ontology and contextual evidence, never persistent state. |
| Preserve | Valid consent/grant/refusal and the IT withdrawal; valid nonadult goals and requests equally preserved. |
| Existing-row disposition | Malformed participants A06/A07 and code-switch A08 only; no censorship or automatic label penalty. |
| Proposed new families | Grant versus refusal versus withdrawal with explicit earlier grant and current refusal as flat claims; desire≠consent; time-limited boundary; linguistic applicability reviewed. |
| Languages | IT/EN/ES; useful adult code-switch |
| Heads / fields | dialogueAct, predicate, polarity, temporalRelation, five roles, boundary, adultOnly provenance |
| Overcorrection risk | Inventing consent.withdraw label, treating arousal as consent, or treating desire as permission; arousal screen zero is not universal absence proof. |
| Student-4 recurrence | Historical request/ownership/span weaknesses apply as plausible risk, not measured adult-specific V3 regression. |
| Semantic decision required | False |

### R14 — CODE_SWITCH_GAP

| Required item | Specification |
| --- | --- |
| Evidence | reports/evidence/student5-path-b-cp37-train-audit/semantic-review.json#/groups/codeSwitchUnresolved |
| Why V3 requires attention | V3 4.5/13 forbids semantic downgrade solely for unfamiliar/adult vocabulary. |
| Wrong versus sparse | 11 declared code-switch desire cases all speech.unresolved, narrow vocabulary/family. |
| Minimal proposed action | Propose correcting clear goal/desire predicate in those exact cases after row review, retaining explicit role/time evidence; broaden semantic families and natural switching patterns, with provenance languages declared. |
| Preserve | Underlying adult vocabulary, speaker desire and observer target where justified. |
| Existing-row disposition | A08 CORRECT_IN_FUTURE_V2; no automatic classifier or regenerated sentences here. |
| Proposed new families | Code-switch ordinary preference/residence/work, request/consent/refusal, report, negation and time; unknown only for real evidential insufficiency. |
| Languages | Natural IT/EN, ES/EN, IT/ES switches; language tag code-switch, component languages recorded |
| Heads / fields | predicate, dialogueAct, role pointers, temporal/polarity spans |
| Overcorrection risk | Replacing all code-switch UNKNOWN or speech.unresolved indiscriminately, or unnatural English insertion as coverage. |
| Student-4 recurrence | No historical code-switch per-head causal metric; plausible undesirable unresolved shortcut. |
| Semantic decision required | False |

### R15 — CODE_SWITCH_GAP

| Required item | Specification |
| --- | --- |
| Evidence | reports/evidence/student5-path-b-cp37-train-audit/curriculum.json#/familyCoverage |
| Why V3 requires attention | Identical V3 semantics apply under language variation. |
| Wrong versus sparse | Noisy-language capability unverified; declared code-switch count not automatic language identification. |
| Minimal proposed action | Propose limited project-authored orthographic/punctuation/diacritic variation with human-verified meaning and offsets; distinguish recoverable noise from genuine ambiguity. |
| Preserve | Well-formed existing observations, including unusual but interpretable vocabulary. |
| Existing-row disposition | No automatic spelling cleanup of v1 or noise augmentation execution. |
| Proposed new families | Meaning-preserving typo/spacing variation and truly unresolved counterpart; no external held-out examples. |
| Languages | IT/EN/ES and code-switch where natural |
| Heads / fields | boundary, six span heads, affected sequence/status fields |
| Overcorrection risk | Meaning-changing typo presented as equivalent; using accent/case folding for destructive dedup. |
| Student-4 recurrence | IT/ES robustness is historical concern; noisy Student-5 regression not measured. |
| Semantic decision required | False |

### R16 — REDUNDANCY/TEMPLATE_CONCENTRATION

| Required item | Specification |
| --- | --- |
| Evidence | reports/evidence/student5-path-b-cp37-train-audit/curriculum.json#/duplicates |
| Why V3 requires attention | Curriculum diversity must preserve semantic evidence rather than inflate count. |
| Wrong versus sparse | 1561 excess exact surfaces, 2878 normalized claim excess; 333 skeletons; near similarity is only a screen. |
| Minimal proposed action | Recommend deterministic whole-observation exact-equivalence selection with provenance aliases, after annotation decisions; retain all distinct context/gold/contrast cases. Near/template groups review-only. See policy below. |
| Preserve | Every meaningful polarity, temporal, role, language or context contrast; strong simple base families and unique valid examples. |
| Existing-row disposition | Future duplicate deactivation only via reviewed equivalence manifest; no blanket claim-level deletion or approved sampler changes. |
| Proposed new families | New diversity only to approved semantic gaps, not template quota filling. |
| Languages | All languages separately plus cross-language census |
| Heads / fields | Whole observation, all heads/status/context/lineage |
| Overcorrection risk | Deleting negative/positive near pairs or stripping multi-claim examples; imposing numeric balance without semantic evidence. |
| Student-4 recurrence | Historical repair changed data/loss/repeats together; exact causal redundancy effect NOT_ESTABLISHED. |
| Semantic decision required | False |

### R17 — LANGUAGE_IMBALANCE

| Required item | Specification |
| --- | --- |
| Evidence | reports/evidence/student5-path-b-cp37-train-audit/curriculum.json#/familyCoverage |
| Why V3 requires attention | V3 semantics equal across languages; similar totals do not imply per-family coverage. |
| Wrong versus sparse | 1126/1006/1007 observations plus11 switches conceal absent report/belief and sparse EN/ES past/request/adult distinctions. |
| Minimal proposed action | Propose family×language×unique-surface×label cross-tabs and matched semantic coverage for every approved family, with natural language-specific realizations. |
| Preserve | Strong EN patterns and valid IT/ES self/third-party/property/negation examples. |
| Existing-row disposition | No dropping EN or mass repeating IT/ES to achieve equal totals. |
| Proposed new families | Missing language realizations in R01–R15, after policy approval. |
| Languages | IT/EN/ES and separately code-switch |
| Heads / fields | All 16 heads, semantic family/status and uniqueness census |
| Overcorrection risk | Literal translations with wrong force/polarity; global language equality masking family holes. |
| Student-4 recurrence | IT temporal/predicate and ES negation/exact-set regressions observed; preserving EN also needed. |
| Semantic decision required | False |

### R18 — SEMANTIC_POLICY_NEEDS_SUPERVISOR_DECISION

| Required item | Specification |
| --- | --- |
| Evidence | reports/evidence/student5-path-b-cp37-train-audit/semantic-review.json#/groups/reportedPerspective |
| Why V3 requires attention | V3 5/14 reporter viewpoint example conflicts with inherited perspective defaults. |
| Wrong versus sparse | Eight reports speaker perspective; source=subject=reported person; concrete tension, not authority to copy source everywhere. |
| Minimal proposed action | D02: adjudicate these eight reported desire viewpoints using V3 normative Anna/Marco examples; recommend attributed holder when wording supports it. Specify scope for separate reporter and viewpoint. |
| Preserve | Report wording and source/subject/owner identities when supported. |
| Existing-row disposition | A03 NEEDS_SUPERVISOR_SEMANTIC_DECISION. |
| Proposed new families | Only after rule: reporter≠embedded subject and source≠perspective flat cases with explicit evidence. |
| Languages | IT existing; IT/EN/ES future |
| Heads / fields | perspectiveReferent, sourceReferent, claimKind, boundary |
| Overcorrection risk | Source→perspective automatic rule would defeat independent head. |
| Student-4 recurrence | No same-head Student-4 source metric; third-party/ownership warning only. |
| Semantic decision required | True |

### R19 — SEMANTIC_POLICY_NEEDS_SUPERVISOR_DECISION

| Required item | Specification |
| --- | --- |
| Evidence | reports/evidence/student5-path-b-cp37-train-audit/semantic-review.json#/groups/opinionWrapperReview |
| Why V3 requires attention | V3 BELIEF includes opinion/thought; lexicalized evaluations may need an annotation rule. |
| Wrong versus sparse | Six consider/considero cases DIRECT; bounded review set, not six proven wrong labels. |
| Minimal proposed action | D03: decide overt propositional/self-description opinion wrapper versus lexicalized preference assertion; recommend BELIEF for actual holder-marked thought, not keyword matching. |
| Preserve | Semantic attribute/preference content, explicit subjects and linguistic polarity. |
| Existing-row disposition | A04 NEEDS_SUPERVISOR_SEMANTIC_DECISION. |
| Proposed new families | Overt believe/think/opinion versus direct property after consistent policy. |
| Languages | IT2/EN2/ES2 existing |
| Heads / fields | claimKind, source/perspective, predicate, subject spans |
| Overcorrection risk | Relabeling every consider form and changing predicate to belief state. |
| Student-4 recurrence | BELIEF has no directly comparable Student-4 head regression; risk of inconsistent V3 targets. |
| Semantic decision required | True |

### R20 — SEMANTIC_POLICY_NEEDS_SUPERVISOR_DECISION

| Required item | Specification |
| --- | --- |
| Evidence | CP37 report section 3, malformedDoubleConTeConMe and listed reflexive requests |
| Why V3 requires attention | Participant wording must justify owner/subject/target independently. |
| Wrong versus sparse | Six malformed double-participant instances (four surfaces), plus three reflexive requests require reading; intended target cannot be guessed. |
| Minimal proposed action | D04: approve exclusion/quarantine of malformed six from a future active candidate, or separately approve intended participant rewrite; review reflexive three separately. Recommend exclusion until intent is settled. |
| Preserve | Valid adult requests and all original v1 text/provenance. |
| Existing-row disposition | A06/A07 NEEDS_SUPERVISOR_SEMANTIC_DECISION; no automatic text deletion. |
| Proposed new families | Replacement families only if separately approved, with explicit participant semantics. |
| Languages | IT existing; IT/EN/ES future request quality review |
| Heads / fields | text, sourceSpan, subject/object, target/owner/subjectReferent, dialogueAct |
| Overcorrection risk | Guessing intended sexual participant or repairing text without recomputing all offsets. |
| Student-4 recurrence | Historical request/ownership weakness relevant; malformed syntax not proven model corruption. |
| Semantic decision required | True |

### R21 — SEMANTIC_POLICY_NEEDS_SUPERVISOR_DECISION

| Required item | Specification |
| --- | --- |
| Evidence | reports/evidence/student5-path-b-cp37-train-audit/review-evidence.json#/heuristicReviewScreens/cueCatalogMismatch |
| Why V3 requires attention | V3 6.5 preserves metalinguistic cue but may require UNKNOWN/abstention when flat scope cannot assign it. |
| Wrong versus sparse | One ES correction no cue; eight Italian più screen hits are false negation alarms. |
| Minimal proposed action | D05: decide whether discourse No can remain with positive corrected proposition under one flat claim or requires unresolved composition; cue preservation is required, scope/claim disposition must be explicit. |
| Preserve | Positive corrected residence content; eight comparative/affirmative più cases retain negation unchanged. |
| Existing-row disposition | A09 NEEDS_SUPERVISOR_SEMANTIC_DECISION; A10 KEEP_UNCHANGED for negation only. |
| Proposed new families | Metalinguistic correction versus propositional negative assertion contrasts after decision. |
| Languages | ES existing; IT/EN/ES later |
| Heads / fields | negationCueSpans, polarity, boundary, interpretationStatus |
| Overcorrection risk | Changing corrected positive fact to NEGATIVE just because No appears; mistaking più tardi for negation. |
| Student-4 recurrence | Correction1/6 and negation failures historically support caution, not automatic target. |
| Semantic decision required | True |

### R22 — PRESERVE_AS_IS

| Required item | Specification |
| --- | --- |
| Evidence | CP37 report sections 1–3; reports/evidence/student5-path-b-cp37-train-audit/curriculum.json |
| Why V3 requires attention | Conservative repair preserves useful work and invariants. |
| Wrong versus sparse | No exact same-input/context conflicts under CP37 comparator; useful direct predicates, 699 multi-claim rows and implicit-subject convention. |
| Minimal proposed action | Freeze v1; preserve every valid unique behavior, correct equal-role case, atemporal label, multi-span group and negative-cue convention; review overlapping issue fields separately. |
| Preserve | All valid examples outside approved change/deactivation manifests, with alias accounting for reviewed redundancy. |
| Existing-row disposition | A11 KEEP_UNCHANGED for implicit subject field; no global gold regeneration. |
| Proposed new families | None solely for preservation. |
| Languages | All |
| Heads / fields | All heads and provenance |
| Overcorrection risk | Treating structurally valid as semantically certified, or treating a KEEP field as certification of all fields in the row. |
| Student-4 recurrence | Historical mixed repair reinforces non-regression safeguards; pristine damage unproven. |
| Semantic decision required | False |

### R23 — MISSING_CURRICULUM_COVERAGE

| Required item | Specification |
| --- | --- |
| Evidence | reports/evidence/student5-path-b-cp37-train-audit/curriculum.json#/tokenEffectiveSupport/boundary |
| Why V3 requires attention | Boundary has O labels; V3 unresolved predicate and empty observation are not interchangeable. |
| Wrong versus sparse | All3150 observations contain a claim; absence teaching unverified. |
| Minimal proposed action | D06: clarify permitted genuine no-claim observation semantics/schema versus speech.unresolved and abstained atomic claim before proposing claim-free data. Do not assume boundary-O availability authorizes empty gold. |
| Preserve | All existing meaningful observations and unresolved claims. |
| Existing-row disposition | No current row proposed for empty claim conversion. |
| Proposed new families | Only if approved: genuine non-propositional no-claim versus resolvable claim contrast; no generated rows now. |
| Languages | IT/EN/ES; code-switch |
| Heads / fields | boundary, claims[], predicate/status |
| Overcorrection risk | Erasing valid speech evidence to fill O examples; implicitly changing schema. |
| Student-4 recurrence | No established historical no-claim failure; missing supervision is a bounded risk. |
| Semantic decision required | True |

### R24 — PLAUSIBLE_STUDENT4_REGRESSION_RISK

| Required item | Specification |
| --- | --- |
| Evidence | CP37 report sections 3–4 and persisted Student-4 reports |
| Why V3 requires attention | Preserve multilingual teaching while avoiding unsupported causal claims. |
| Wrong versus sparse | Synthetic concentrated labels; no retention target or trained Student-5 measurements. |
| Minimal proposed action | Require preservation census and semantic review of valid baseline families; keep dataset acceptance separate from later model-quality/non-regression gates. No architecture, loss, sampler or encoder schedule recommendation here. |
| Preserve | All valid direct/self/third-party and EN/IT/ES strengths, immutable pristine. |
| Existing-row disposition | No Student-4/pristine/Path-A change; no new evaluation artifacts inferred. |
| Proposed new families | Only approved teaching gaps above. |
| Languages | IT/EN/ES |
| Heads / fields | Whole curriculum and later independent quality review, outside current execution |
| Overcorrection risk | Claiming repaired counts prevent forgetting or that pristine is damaged. |
| Student-4 recurrence | DIRECTLY_SUPPORTED historical mixed repair; PLAUSIBLE_RECURRENCE_RISK; NOT_ESTABLISHED_CAUSATION. |
| Semantic decision required | False |

## Annotation-repair table: existing rows only

Actions apply to the stated field/issue, not automatic whole-row acceptance. Groups overlap and counts must not be summed. Before any future candidate, join all dispositions by original rowId+claimId; a unresolved semantic issue blocks activating the affected gold even if a different span fix is deterministic. No existing row is presently removed, relabeled, quarantined or rewritten.

| Group | CP37 scope / exact IDs or selector | Proposed disposition | Reason / control |
| --- | --- | --- | --- |
| A01 | mx-v2-train-it-generalization-known_third_party-002:c0, mx-v22a-it-core-067:c0, mx-v22a-it-core-072:c0, mx-v22a-it-core-077:c0, mx-v22a-it-core-082:c0, mx-v22a-it-core-087:c0 | CORRECT_IN_FUTURE_V2 | Restore six explicit temporal evidence spans only; five relation decisions overlap A02. Decision: no additional semantic-policy decision for stated field |
| A02 | mx-v22a-en-core-002:c0, mx-v22a-en-core-007:c0, mx-v22a-en-core-012:c0, mx-v22a-en-core-017:c0, mx-v22a-en-core-022:c0, mx-v22a-en-core-027:c0, mx-v22a-en-core-032:c0, mx-v22a-en-core-037:c0, mx-v22a-it-core-003:c0, mx-v22a-it-core-009:c0, mx-v22a-it-core-015:c0, mx-v22a-it-core-021:c0, mx-v22a-it-core-027:c0, mx-v22a-it-core-033:c0, mx-v22a-it-core-039:c0, mx-v22a-it-core-045:c0, mx-v22a-it-core-051:c0, mx-v22a-it-core-057:c0, mx-v22a-it-core-067:c0, mx-v22a-it-core-072:c0, mx-v22a-it-core-077:c0, mx-v22a-it-core-082:c0, mx-v22a-it-core-087:c0 | NEEDS_SUPERVISOR_SEMANTIC_DECISION | Time of wanting versus desired action; no new relation gold chosen. Decision: D01 |
| A03 | mx-v22a-it-core-113:c0, mx-v22a-it-core-115:c0, mx-v22a-it-core-117:c0, mx-v22a-it-core-119:c0, mx-v22a-it-core-121:c0, mx-v22a-it-core-123:c0, mx-v22a-it-core-125:c0, mx-v22a-it-core-127:c0 | NEEDS_SUPERVISOR_SEMANTIC_DECISION | Reported viewpoint versus inherited speaker perspective; no source-copy rule. Decision: D02 |
| A04 | mx-v2-train-en-attribute-00:c0, mx-v2-train-en-generalization-negative_preference-005:c0, mx-v2-train-es-attribute-00:c0, mx-v2-train-es-generalization-negative_preference-000:c0, mx-v2-train-it-attribute-00:c0, mx-v2-train-it-generalization-negative_preference-005:c0 | NEEDS_SUPERVISOR_SEMANTIC_DECISION | Overt opinion versus lexicalized direct evaluation. Decision: D03 |
| A05 | 628 instances; 20 sample IDs in linked evidence. Exact CP37 selector from review_semantics.py: language=='en', re.match(r'^I\b', claim text), empty subjectSpans. Count628; CP37 persisted first20 IDs only. Future authorized executor must enumerate complete group from pinned v1; do not treat these20 as full manifest. | CORRECT_IN_FUTURE_V2 | Restore explicit English I subject evidence after row/offset review, preserving other justified fields. Decision: no additional semantic-policy decision for stated field |
| A06 | mx-v22a-adult-it-016:c0, mx-v22a-adult-it-017:c0, mx-v22a-adult-it-018:c0, mx-v22a-adult-it-024:c0, mx-v22a-adult-it-028:c0, mx-v22a-adult-it-029:c0 | NEEDS_SUPERVISOR_SEMANTIC_DECISION | Recommend quarantine/exclusion until intended participants are decided; no automatic rewrite. Decision: D04 |
| A07 | mx-v22a-adult-it-015:c0, mx-v22a-adult-it-025:c0, mx-v22a-adult-it-026:c0 | NEEDS_SUPERVISOR_SEMANTIC_DECISION | Reflexive request forms with external target: linguistic review, not automatically malformed. Decision: D04 |
| A08 | mx-v22a-adult-it-049:c0, mx-v22a-adult-it-050:c0, mx-v22a-adult-it-051:c0, mx-v22a-adult-it-052:c0, mx-v22a-adult-it-053:c0, mx-v22a-adult-it-054:c0, mx-v22a-adult-it-055:c0, mx-v22a-adult-it-056:c0, mx-v22a-adult-it-057:c0, mx-v22a-adult-it-058:c0, mx-v22a-adult-it-059:c0 | CORRECT_IN_FUTURE_V2 | Clear desire wording should use covered goal semantics after individual review; not an all-code-switch conversion rule. Decision: no additional semantic-policy decision for stated field |
| A09 | mx-v2-train-es-generalization-dialogue_correct-005:c0 | NEEDS_SUPERVISOR_SEMANTIC_DECISION | Metalinguistic No cue must be preserved; proposition/flat-scope polarity status requires decision. Decision: D05 |
| A10 | mx-v22a-adult-it-007:c0, mx-v22a-adult-it-020:c0, mx-v22a-adult-it-033:c0, mx-v22a-it-core-067:c0, mx-v22a-it-core-072:c0, mx-v22a-it-core-077:c0, mx-v22a-it-core-082:c0, mx-v22a-it-core-087:c0 | KEEP_UNCHANGED | Negation false positives only; five temporal omissions still corrected separately under A01. Decision: no additional semantic-policy decision for stated field |
| A11 | 404 instances; 20 sample IDs in linked evidence. Bounded CP37 IT/ES prefix selector in review_semantics.py; first20 IDs persisted, full count404. No rerun needed for this design task. | KEEP_UNCHANGED | 404 IT/ES implicit-subject cases comply for subject evidence/pointer; not blanket certification of every other field. Decision: no additional semantic-policy decision for stated field |

The [annotation-dispositions.json](evidence/student5-path-b-cp38-repair-spec/annotation-dispositions.json) binds every group to the precise CP37 source and records whether listed IDs are complete. A01 contains six complete row IDs; A02 has23, A03 has8, A04 has6, A06 has6, A07 has3, A08 has11, A09 has1 and A10 has8. A05's exact selector is English + claim text beginning `I` at a word boundary + empty subjectSpans, as implemented by CP37 `review_semantics.py`. The future executor must enumerate and review the complete 628-instance group from pinned v1 before producing a changed-row manifest. This design does not claim that a sample is a full manifest. A11's 404 valid implicit-subject cases remain unchanged for that field; they are not universal proof of implicit-subject parser coverage.

No unconditional `REMOVE_FROM_FUTURE_V2` action is assigned to a semantic issue: malformed intent first needs D04. Redundant exact-equivalence instances may later be deactivated only under the separately approved selection proposal below. Text repair, if selected by Supervisor, must update every dependent offset/candidate link and receive new-row lineage; deleting one phrase while keeping stale spans is forbidden.

## Deterministic future redundancy policy — RECOMMENDATION, not an approved gate

1. Resolve or quarantine annotation-policy cases first. Derive a review-only equivalence key from language, exact Unicode observation text (no case/diacritic/negation/whitespace folding), complete speaker/observer/context identities and discourse anchors, and complete semantic gold. Canonicalize only JSON map ordering and incidental local mention/claim ID renamings through span/type/reference-preserving bijections. Keep all statuses, alternatives and critical dependencies. Preserve metadata/provenance differences in an alias ledger; if a difference changes semantics or cannot be proven incidental, do not merge.
2. Proposed deterministic selection is one active representative per **reviewed exact semantic-equivalence group**, ordered by original sourceDatasetId, original rowId, then old row SHA-256. Retain alias entries for every original instance and its provenance. “One” is a recommendation justified by repeated identical teaching, not an approved class quota or weighting schedule. If any row has unresolved annotations, quarantine its affected group until adjudicated rather than hiding it behind a cleaner duplicate.
3. Never deduplicate isolated normalized claims out of multi-claim observations. Boundary teaching and discourse/candidate context must remain intact. Same text with different context, status, polarity, actor or anchor is a contrast, not an automatic duplicate. Contradictory exact input+context is a review blocker, never a majority vote; intentional ambiguity must be represented consistently or quarantined with explicit Supervisor disposition.
4. CP37's >=0.90 near-similarity screen and333 skeleton groups produce reviewer queues only. No distance threshold deletes data. Mark each pair/group KEEP_CONTRAST, KEEP_DISTINCT, EXACT_EQUIVALENT_APPROVED or UNRESOLVED, recording reasons. Prefer the least invasive exact-equivalence deactivation first. No additional sampler, repetition multiplier, loss weight or numeric language ratio is specified.
5. Report before/after active row counts, unique surfaces/claims, exact-equivalence multiplicities, context/role/temporal/polarity contrasts, family-language support and skeleton concentration, with all deactivated IDs. “Materially reduced” must be reviewed against those measurements and preserved meaning, not asserted from a smaller file. No exact future row count, reduction percentage or checksum is promised; the CP37 surface counts do not equal the stronger contextual equivalence key.
6. If exact selection disproportionately reduces a critical family, preserve the unique semantic representatives and flag the gap for approved authored diversity. Do not silently reinflate it with repeats or delete a strong language to balance totals. All active/inactive aliases remain recoverable from immutable v1 and the future manifests.

## Proposed future dataset identity and lineage

Proposed ID `student5-matrix-nlu-v3-train-v2`; proposed distinct directory `data/student5_v3_train_v2/`. Both are design names only: neither exists as a new artifact from CP38. Do not reuse `data/student5_v3/` for v2. The preserved v1 remains the rollback baseline; later v2 would require a new artifact/checksum identity and registry entry only after actual creation and verification.

| Future metadata field | Required value or definition |
| --- | --- |
| baseDatasetId | student5-matrix-nlu-v3-train-v1 |
| baseDatasetSha256 | 1118a900026f48cfcc290c3f9dc52a1a019a6a1f4761661f326c33770523140e |
| baseRepository / branch / sourceCommit | MATRIXNEO23/matrix-understanding-lab / student5-path-b-v3 / this specification's pinned starting HEAD and original v1 artifact commit117afd627ebe9f584b9328f1f78c63822980a49c |
| repairSpecificationId | student5-v3-train-repair-spec-cp38-v1 plus immutable accepted specification commit, report SHA-256 and Supervisor decision record |
| newDatasetId | student5-matrix-nlu-v3-train-v2 — proposed, NOT CREATED |
| new version reason | Conservative CP37 annotation repair, approved missing semantic families, language support and reviewed redundancy; no contract expansion |
| source provenance classes | INHERITED_AUTHORIZED_TRAIN_UNCHANGED; INHERITED_AUTHORIZED_TRAIN_CORRECTED; PROJECT_AUTHORED_TRAIN_ONLY; other licensed/provenanced source only if separately approved. No DEV/Frozen-derived class |
| changed-row manifest | Old/new IDs and row SHA-256; base shard/line; field-level before/after diff; issue/group/decision IDs; evidence reason; author/reviewer; text-change flag and dependent-offset validation; unmodified field confirmation |
| added-row manifest | New unique ID, origin/author/date, project-authored assertion or approved source/license locator, languages, intended semantic contrasts, family/heads, adultOnly when applicable, semantic review and contract validation |
| removed/deactivated manifest | Old ID/hash/source, reason, exact-equivalence key and retained representative/alias or unresolved-policy quarantine; reviewer/decision and reversibility; never silent loss |
| unchanged/alias inventory | Every retained base row mapped without field changes; duplicate provenance aliases preserved; all original rows accounted for exactly once per final disposition with issue overlaps resolved |
| per-file SHA256SUMS | Actual bytes after creation; sorted relative paths, no self-hash; include all dataset/manifests/census payloads required for recovery |
| ordered dataset SHA-256 | Compute over declared ordered shard bytes using the same v1 logical hashing convention, record encoding/newline/order; separate from per-file digests. UNKNOWN UNTIL CREATED |
| contract fingerprint | 7b0646e44243ad897760c0fcadbe141f1b8e88e3fd8d63a1789106571b9987b0; no new labels, heads or pointer meanings |
| language/family census | Raw and unique observations/claims; source families plus explicit operational family definitions; IT/EN/ES and component-language-tagged code-switch; all heads/classes/statuses/anchors and contrast support, including zeros |
| durable recovery | Exact repo paths/commit, immutable artifact ID if needed, bytes/SHA, authenticated access route verified by future executor, and readback evidence; no scratch-only handoff |

No actual changed-row gold, new TRAIN shard, new dataset hash, v2 registry entry or trained candidate is produced here. The design evidence JSON is a specification, not a loadable dataset or augmentation output.

## Future repaired-TRAIN acceptance checks

These are proposed dataset acceptance checks for Supervisor review. Passing them would not establish learned accuracy, clear CP36 readiness, authorize training or replace model-performance gates.

| Check | Required later proof / failure handling |
| --- | --- |
| C01 Identity and complete accounting | Verify every intended file/byte/SHA, ordered shard digest, manifest lineage and all old-row dispositions. Fail on missing/unlisted required file, accidental overwrite or unexplained change. Recover v1 and demonstrate all130 artifact Git blobs unchanged. |
| C02 Fixed V3 semantics | Fingerprint and ordered registries unchanged; six token + ten sequence heads, temporal label+anchor counted as one conceptual head/two tensors. Structural validation is necessary but not sufficient; no new predicate/status head or downstream state field. |
| C03 Provenance isolation | All inherited sources bind to authorized TRAIN; all additions project-authored or explicitly approved with license/provenance. No DEV/Frozen read or derivative source. Ledger records authors and input allowlist. Do not claim statistical DEV disjointness without permitted identity/access; CP36 separation remains independently unresolved. |
| C04 Justified edits | Every changed row links to CP37 issue, exact evidence and approved disposition. Full group enumeration, not20 samples for628 targets. All dependent spans/pointers valid after any text repair. No default global reannotation. |
| C05 Gold consistency | No contradictory gold for identical complete input/context. Any intentionally divergent interpretation must be documented and Supervisor-decided with supported ambiguity/status representation or excluded; never duplicated conflicting resolved targets silently. |
| C06 Complete head census | Report all classes including zeros and both raw/unique support for all16 conceptual heads. Token positives/plural groups and observation boundaries; independent pointer kinds/choices/statuses; temporal relation plus anchor identity. Distinguish lexical diagnostic counts from actual tokenizer target checks if separately authorized later. |
| C07 Family and language support | IT/EN/ES/code-switch family census using fixed definitions, natural language review and preserved contrasts. COMMAND/BELIEF/REPORT and five advanced temporal families no longer structurally absent if additions approved; any unapproved gap remains explicit and cannot be claimed complete. No universal numeric ratio is invented. |
| C08 Role and attribution independence | Demonstrate supported per-role evidence and context choices, non-speaker viewpoints, reporter≠embedded subject, separately approved source≠perspective and owner divergence. Preserve valid role equalities. D07 unresolved means full independence criterion cannot PASS. UNKNOWN versus NONE and AMBIGUOUS/alternatives must be correctly represented. |
| C09 Temporal and negation composition | Correct all six explicit-span omissions; approved D01 scope consistent; required anchors valid with more than speech-time teaching when families approved. Cue/polarity independence includes positive/unknown cue cases and valid negative/no-cue cases; multilingual negative concord not forced positive. |
| C10 Span and boundary evidence | Explicit-I group fixed or individually quarantined; implicit-subject emptiness preserved; useful multiword/plural groups valid; all observation offsets preserved and no recursive/overlapping atomization. Claim-free additions only if D06 accepted. |
| C11 Adult semantics | Approved languages distinguish desire/assertion, request, grant, refusal, withdrawal and boundary, including current desire versus consent. AdultOnly provenance where applicable; no censorship labels or confidence penalty. No persistent ConsentState inferred from text labels. |
| C12 Redundancy with preservation | Before/after exact/contextual equivalence and template census; aliases and decisions for every deactivation; critical semantic contrasts retained. Reviewer verifies material reduction and strong-family preservation; a raw count decrease alone does not PASS. |
| C13 CP37 closure | Every confirmed defect corrected or explicitly quarantined. Every unresolved semantic case has Supervisor decision or is excluded from active future candidate with manifest; exclusion must not hide required family gaps. No heuristic false positive counted as fixed. |
| C14 Independent semantic review and stop | Supervisor reviews linguistic correctness by issue, family and language; checksum/shape/validator results alone cannot establish it. No invented semantic-accuracy percentage. Then stop for a new assignment; DEV identity/evaluator/calibration/error-analysis repair and actual quality testing remain outside this specification. |

Head inventory for C06: token.boundary/object/subject/negation/temporal/entity; sequence.dialogueAct/predicate/subjectReferent/targetReferent/ownerReferent/perspectiveReferent/sourceReferent/polarity/temporalRelation/claimKind. Field statuses and abstention are contract/validator outputs, not extra neural heads. Required uncertainty examples must not silently create target tensors or depend on unimplemented status semantics; later readiness must verify target/evaluation support before any training.

## Student-4 regression safeguards, using persisted reports only

Historical sources read: [v2.1 post-run](STUDENT_4_V21_POST_DEV_REPORT.md), [v2.2A controlled repair](STUDENT_4_V22A_CONTROLLED_REPAIR_REPORT.md), [v2.1 stop report](STUDENT_4_V21_STOP_REPORT.md), [v2.2A repair plan](STUDENT_4_V22A_REPAIR_PLAN.md). Their bytes are pinned in input-identities.json. The plan is intent; measured final reports govern observed results. No historical DEV payload or individual held-out error example was imported into proposed TRAIN families.

| Area | DIRECTLY_SUPPORTED_HISTORICAL_FAILURE | PLAUSIBLE_RECURRENCE_RISK and proposed safeguard | NOT_ESTABLISHED_CAUSATION |
| --- | --- | --- | --- |
| Negation | Matrix F1 0.509169→0.490644; ES0.158228→0.129534 despite IT0.247012→0.287037 | R10/C09 preserve cue-free opposition and add genuine cue/composition contrasts; review IT/EN/ES separately | Cannot infer V3 cue performance from V2 full-scope F1 or prove TRAIN alone caused decline |
| Temporal | IT accuracy1.0→0.870370; P0.5 overall0.892857→0.880952 | R06–R09/C09 resolve target convention and spans; diversify justified anchors and predicates | No measured Student-5 temporal degradation; future-word relabeling not justified by old metric |
| Referents/report | v2.1 referent family exact-set0.760943; report0.72 (IT0.613333/ES0.56); authority/referent errors20→62 | R02–R05/C08 multiple-candidate choices, explicit source/viewpoint and uncertainty, preserved direct cases | Student-4 had no independent V3 source head; cannot claim same-head regression |
| Correction/request | Request0/6, correction1/6 in both reports | R01/R20/R21 require clear force, participant and correction-scope decisions and multilingual contrasts | No evidence sparse counts alone caused failures; do not copy held-out examples |
| Ownership | Two P0.5 IT corruptions persisted; Matrix ownership corruption0 | R04/C08 independent role justification, preserve valid owner=subject, reject guessed identity | Owner equality in v1 is a shortcut opportunity, not3990 corrupt labels |
| Span/entity | Span residuals269→293; P0.5 entity F1 0.945701→0.903670 | R08/R11/R12/C10 positive multiword/plural evidence, exact offsets and valid implicit subjects | No BERT tokenization experiment or causal contribution of628 omissions measured here |
| IT/ES and EN preservation | Matrix ES exact-set0.595238→0.523810; IT predicate1→0.808642; EN exact-set0.952381→0.896825 | R17/R22/C07/C12 family-specific language review, preserve valid EN and IT/ES strengths | Overall language totals or more repair rows do not prove quality improvement |

The historical intervention changed data, loss and repeats together; it does not isolate curriculum causation. The v2.1 import stop was infrastructure failure, not a failed learned-quality measurement. Pristine Student-5 damage is NOT_ESTABLISHED; immutable model artifacts were not touched. Dataset repair cannot guarantee absence of forgetting. Later model checks remain necessary and separately authorized; no training strategy or gate relaxation is proposed.

## Decisions requiring Supervisor/Owner review

The following are concrete semantic blockers, not repeated requests for permission to perform the current design task. Work recommends dispositions but does not decide them unilaterally.

| Decision | Affected groups | Exact unresolved decision | Recommendation for review |
| --- | --- | --- | --- |
| D01 | A02 / R09 | For goal.object with present wanting and a later desired action, which event/state does the single temporalRelation describe? How must conflicting legacy FUTURE templates be treated? | Choose one explicit linguistic convention for all languages; preserve temporal surface evidence regardless. Do not mass-relabel adverb matches. Until decided, affected targets excluded/quarantined from a future candidate, with justification. |
| D02 | A03 / R18 | For the eight reported desires, is perspective the attributed person as in V3 Anna-said, rather than inherited ctx:speaker? What wording establishes a different viewpoint than source? | Recommend attributed holder for supported cases; require per-row signoff and distinct evidence for source/perspective. No automatic copying. |
| D03 | A04 / R19 | Which of six consider/considero clauses are overt holder-marked opinion/BELIEF versus lexicalized DIRECT evaluation? | Apply V3 BELIEF when propositional opinion wrapper is actually present; document approved linguistic boundary. No keyword-only decision. |
| D04 | A06/A07 / R20 | For six doubled-participant requests, approve exclusion or specify intended participants/text repair? For three reflexive requests, is current participant binding valid? | Recommend quarantine of the six malformed instances rather than guessing intent; separately adjudicate the three reflexives. No removal or rewrite performed. |
| D05 | A09 / R21 | Does initial metalinguistic No attach safely to the flat positive correction or require an unresolved/abstained proposition? | Preserve cue; never automatically flip positive corrected content. Approve exact boundary/polarity/status convention before reuse. |
| D06 | R23 | Does current V3 permit genuine no-claim observations, and how are those distinguished from speech.unresolved or abstained claims? | Do not introduce empty-gold examples until schema/semantic interpretation is approved; this optional coverage cannot silently alter V3. |
| D07 | R04/R18 | Which constructions under fixed V3 support owner different from semantic subject, and source different from perspective, while remaining faithful flat atomic claims? | Do not force all five roles unequal. Approve linguistic definitions/representable families; use already-supported reporter≠embedded-subject and non-speaker-viewpoint cases, but do not claim those alone establish owner≠subject or source≠perspective. |

Separately approve the scope/languages of missing families, the exact-equivalence selection/deactivation policy, and any future dataset implementation assignment. Those are review items, not new permanent gates invented by Work. No numeric quotas, ratios, loss weights, optimizer settings or unfreezing schedule are selected. Existing CP36 blockers (permitted DEV V3 identity, evaluation/decoder/calibration/error-analysis gaps) remain independently open. Do not treat approval of this document as Gate B PASS.

## Delivery, reproducibility and exact stop

Produced only this new CP38 report, `reports/evidence/student5-path-b-cp38-repair-spec/` (issue register, annotation dispositions, decisions, source identities, design-validation result and SHA256SUMS), and the appended current continuity. CP37, TRAIN v1, Student-4, Path A, pristine, evaluator/decoder, registry and prior artifacts remain unchanged. The final remote Git tree comparison must show exactly these allowed documentation/evidence paths; no other existing blob change is allowed. Checksums bind the delivered files; identity checks establish preservation, not linguistic acceptance or learned quality.

All CP37 counts are attributed to its already-executed audit. This task freshly verified input document bytes against Git identities and the140-entry CP37 metadata bridge, produced a conservative specification and reviewed completeness/cross-references. It did not rerun CP37's target construction or create replacement gold. Readback of the new report/continuity and final tree identities is verified before handoff. No tasks/workflows were launched or left active.

Recovery for this design: fetch this report, evidence directory and continuity through the authenticated GitHub connector at the final immutable commit; verify SHA256SUMS and source identities. All review inputs are repository-backed. Final commit identity can be recovered from the introducing commit rather than local scratch. Next action belongs to Supervisor GPT: review D01–D07 and the bounded proposed changes, then issue a separate assignment if appropriate. Work stops here. No TRAIN v2, remediation, training or readiness follow-on starts.
