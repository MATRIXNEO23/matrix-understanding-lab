Supervisor GPT — Student-5 TRAIN v2 Build and Audit Report

TRAIN_V2_AUDIT = FAIL

Branch: student5-path-b-v3. Starting HEAD: 1396dd6c997ce0dbf5e4a5ce933437c82fc1c217. Preparation checkpoint: f63a212d3ced384e5c9914d78d35ee6edb56530f. Final HEAD: introducing commit of this report, supplied after remote readback. Work used pinned API snapshots, not a local Git checkout.

This is a NEW authorized construction, not recovery of the lost original v2. Dataset identity student5-matrix-nlu-v3-train-v2, version CP42_BUILD_1_AUDIT_LOCKED. Build then lock then audit; no candidate corrections after lock/audit. The full candidate is retained despite FAIL. No training-ready or learned-quality claim.

## Candidate and verification

Ordered dataset SHA-256: 34ee224723d77a452a7ea6e776c95a6f11b3355b4ebf53672f99cf35d0bd64a9
Observations: 3267; claims: 4101; additions: 123.
Dispositions: {'CORRECTED': 558, 'PRESERVED': 2586, 'DEACTIVATED': 6, 'NEWLY_AUTHORED': 123}. Corrected ROWS (558) differ from explicit-subject CLAIMS (628) because multi-claim observations exist.
Language observations: {'en': 1046, 'es': 1047, 'it': 1160, 'code-switch': 14}. Claims per language and family/head tables are in census.json.

Canonical input v1: 3150 observations / 3990 claims; SHA-256 1118a900026f48cfcc290c3f9dc52a1a019a6a1f4761661f326c33770523140e. All 129 per-file manifest checks and all 130 source-file identities verified. No v1 payload changed. Six malformed rows are kept byte/logically recoverable in quarantine and the immutable v1, not silently discarded.

Full training payload: data/student5_v3_train_v2/train.jsonl.gz; compressed 297117 bytes; uncompressed 12097663 bytes; compressed SHA-256 b6acf41e6634c2f89e6b8251fb5f816ec60fb0ca1cd6c90dfcbed46c2c12584c. Logical checksum is over decompressed UTF-8 JSONL, newline per row, compact sorted JSON. One shard; this retains the v1 ordered concatenation convention, not its serialization. Gzip mtime=0.

Reproduction in a separate empty verification directory produced byte-identical outputs, including gzip files and BUILD_LOCK. It regenerated the SAME candidate only, without corrective edits. All candidate file hashes match before and after audit. Fixed Contract V3 registry and existing target builder were read, never modified. 0 invariant-validator structural errors; 0 target-builder exceptions. Diagnostic lexical offsets were used for target support, not physical BERT tokenization; no model loaded. Synthetic confidence=1 is used solely to adapt stored gold into the existing structural validator, not as a learned confidence or calibration result.

## Construction details

Applied CP38 indexed corrections: explicit English I evidence (628 claims), six temporal evidence omissions, eight viewpoint assignments for reports of the holder’s own desire, six BELIEF wrappers, three explicit reflexive dispositions, eleven mixed-language desire predicate repairs. The 23 present-desire A02 cases retain CURRENT; the Spanish metalinguistic correction retains POSITIVE and no proposition-scoped No cue. All 404 implicit first-person controls recorded. New contrast families supplement valid retained curriculum. Text/gold provenance, claim before/after diffs, v1→v2 mappings, reasons and decision IDs are persisted. PRESERVED means semantic claims unchanged, not an assertion that every inherited annotation was independently proven correct. Dataset ID and provenance metadata change explicitly.

CP41 motivates binding/scope contrasts; it is not label-error evidence and no CP41 probe payload is included. D01–D07 remain approved; historical awaiting-approval metadata is superseded. No Student-4 model error is attributed to this pristine model.

## Curriculum census

Fixed sequence heads: {"dialogueAct": {"ASSERT": 3851, "QUESTION": 201, "REQUEST": 30, "COMMAND": 3, "CORRECT": 16, "UNKNOWN": 0}, "predicate": {"identity.name": 460, "identity.age": 441, "residence.place": 944, "presence.reported": 60, "preference.like": 979, "work.role": 270, "possession.has": 63, "goal.object": 680, "attribute.is": 56, "consent.grant": 76, "consent.refuse": 71, "speech.unresolved": 1}, "polarity": {"POSITIVE": 3208, "NEGATIVE": 701, "UNKNOWN": 192}, "temporalRelation": {"ATEMPORAL": 1371, "CURRENT": 2180, "PAST": 17, "FUTURE": 518, "BEFORE": 3, "AFTER": 3, "DURING": 3, "RECURRENT": 3, "AT_REFERENCE": 3, "UNKNOWN": 0}, "claimKind": {"DIRECT": 3811, "REPORT": 14, "BELIEF": 9, "HYPOTHESIS": 267, "UNKNOWN": 0}}

Role equality/divergence: {'owner=subject': 4086, 'source=perspective': 4095, 'perspective=speaker': 4087, 'perspective!=speaker': 14, 'owner!=subject': 15, 'source!=perspective': 6}. Nonzero divergence does not imply adequate independent-role teaching.
Temporal anchors: {'None': 1371, 'speech-time': 2718, 'temporal:t0': 9, 'context-reference': 3}. No cross-claim anchor example was added.
Claim-free observations: 6. The field-status registry uses RESOLVED for known, NOT_APPLICABLE for NONE; KNOWN is not a new V3 label.

Adult/intimacy additions cover desire, grant, refusal, withdrawal, request, physical description, explicit slang, hesitation, participant binding and code-switch in adult-only contexts. Three target languages have matched added contrasts. Explicit vocabulary is not mapped to UNKNOWN merely because explicit. Desire/grant/refusal/withdrawal are annotated separately; hesitation expresses genuine uncertainty. Exact family/language census and all raw rows are available. Coverage remains small; semantic defects below preclude adequacy claims. Code-switch has 14 observations and remains desire-heavy. Formal/informal, profanity, abbreviation and borrowed-term examples are annotated, but their presence alone is not broad linguistic coverage.

Preservation and review slices A–H are stored in slices.json. They index TRAIN only and are not independent held-out evaluation. No present model-regression percentage is asserted or invented.

## Complete findings register

Recommendations below are NOT applied. Each machine-readable finding includes complete affected row IDs, evidence, heads, consequence and recommendation. Empty affectedRows denotes a missing family/global limitation, not unrecorded examples. Near-duplicate and temporal lexical screens are review risks, not automatic semantic-equivalence or error classifiers.

### C01 — HIGH (2 affected row IDs)

Heads: all semantic labels
Evidence: "Identical language/text/context has different semantic payload; conflict groups persisted"
Likely consequence: Contradictory supervision or inconsistent span/status conventions
Recommended correction (NOT APPLIED): Adjudicate full-context equivalence; no automatic majority or similarity deletion

### C02 — MEDIUM (2189 affected row IDs)

Heads: all
Evidence: "Repeated exact surfaces retained; context may differ. Full groups in redundancy.json"
Likely consequence: Repetition can dominate scarce repair families
Recommended correction (NOT APPLIED): Review exact semantic equivalence with aliases; preserve true contextual contrasts

### C03 — MEDIUM (36 affected row IDs)

Heads: all
Evidence: {"largestSkeleton": " <SLOT> ", "rows": 36, "definition": "Object/entity span replacement; overlapping replacements are an approximate proxy"}
Likely consequence: Residual template shortcuts and low lexical variety
Recommended correction (NOT APPLIED): Review concentration by semantic family, preserve valid simple examples

### C04 — MEDIUM (189 affected row IDs)

Heads: all
Evidence: {"screen": "Within-language unique surface character-trigram Jaccard >= 0.85", "pairs": 432}
Likely consequence: Near-template concentration; similarity is not equivalence
Recommended correction (NOT APPLIED): Review pairs only; do not delete or relabel by score

### G01 — HIGH (0 affected row IDs)

Heads: dialogueAct, temporalRelation, claimKind
Evidence: {"zeroSupport": {"dialogueAct": ["UNKNOWN"], "temporalRelation": ["UNKNOWN"], "claimKind": ["UNKNOWN"]}}
Likely consequence: Full V3 class coverage remains incomplete
Recommended correction (NOT APPLIED): Author genuinely uncertain act/kind/time cases where linguistically justified, never pad UNKNOWN counts

### G02 — HIGH (123 affected row IDs)

Heads: dialogueAct, temporalRelation, sourceReferent, perspectiveReferent
Evidence: {"newRows": 123, "familyLanguageCounts": {"question": {"en": 62, "es": 62, "it": 62}, "command": {"it": 1, "en": 1, "es": 1}, "request": {"it": 1, "en": 1, "es": 1}, "metalinguistic_correction": {"it": 1, "en": 1, "es": 1}, "belief_wrapper": {"it": 1, "en": 1, "es": 1}, "direct_control": {"it": 1, "en": 1, "es": 1}, "desire_current_action_future": {"it": 1, "en": 1, "es": 1}, "desire_future": {"it": 1, "en": 1, "es": 1}, "temporal_PAST": {"it": 1, "en": 1, "es": 1}, "temporal_FUTURE": {"it": 1, "en": 1, "es": 1}, "temporal_BEFORE": {"it": 1, "en": 1, "es": 1}, "temporal_AFTER": {"it": 1, "en": 1, "es": 1}, "temporal_DURING": {"it": 1, "en": 1, "es": 1}, "temporal_RECURRENT": {"it": 1, "en": 1, "es": 1}, "temporal_AT_REFERENCE": {"it": 1, "en": 1, "es": 1}, "role_binding": {"it": 4, "en": 4, "es": 4}, "source_viewpoint": {"it": 2, "en": 2, "es": 2}, "owner_subject_permission": {"it": 1, "en": 1, "es": 1}, "adult_desire": {"it": 1, "en": 1, "es": 1}, "adult_grant": {"it": 1, "en": 1, "es": 1}, "adult_refusal": {"it": 1, "en": 1, "es": 1}, "adult_withdrawal": {"it": 1, "en": 1, "es": 1}, "adult_request": {"it": 1, "en": 1, "es": 1}, "adult_description": {"it": 1, "en": 1, "es": 1}, "adult_slang": {"it": 1, "en": 1, "es": 1}, "adult_hesitation": {"it": 1, "en": 1, "es": 1}, "profanity_preference": {"it": 1, "en": 1, "es": 1}, "borrowed_lexicon": {"it": 1, "en": 1, "es": 1}, "adult_code_switch": {"code-switch": 3}, "abbreviation_colloquial": {"it": 1, "en": 1, "es": 1}, "double_negation": {"it": 1, "en": 1, "es": 1}, "cue_free_negative": {"it": 1, "en": 1, "es": 1}, "grammatical_reflexive": {"it": 1, "en": 1, "es": 1}, "ambiguous_binding": {"it": 1, "en": 1, "es": 1}, "resolved_binding_control": {"it": 1, "en": 1, "es": 1}}}
Likely consequence: New families have only one/few constructions per language; nonzero support does not establish adequate diversity
Recommended correction (NOT APPLIED): Supervisor should review breadth and naturally varied contrasts before training

### G03 — HIGH (3 affected row IDs)

Heads: subjectReferent, ownerReferent, fieldStatus
Evidence: {"targetBuilder": "training_data_v3.py reads labels but does not consume fieldStatusByField/alternativesByField", "changed": false}
Likely consequence: UNKNOWN pointer is teachable but ranked ambiguity/field-status distinction is not a dedicated supervised target here
Recommended correction (NOT APPLIED): Keep this as separate Gate-B target/evaluation readiness blocker; do not modify evaluator/decoder in this task

### G04 — MEDIUM (2586 affected row IDs)

Heads: all
Evidence: {"sliceIndex": "slices.json", "heldOutEvaluationCreated": false}
Likely consequence: Training preservation controls cannot independently measure generalization/regression
Recommended correction (NOT APPLIED): Supervisor must specify separately authorized evaluation; no DEV/Frozen derivation now

### L01 — HIGH (1 affected row IDs)

Heads: negation
Evidence: {"text": "It is not true that I do not like jazz.", "storedSpans": [[6, 9], [28, 31]], "storedText": ["not", " li"]}
Likely consequence: Second cue supervises part of like rather than not
Recommended correction (NOT APPLIED): Correct second not span to [24,27) after Supervisor approval; current payload is untouched

### L02 — HIGH (3 affected row IDs)

Heads: boundary, negation, polarity, claimKind
Evidence: "Hesitation examples combine desire, disjunction and epistemic uncertainty in one flat claim; Spanish second no in no sé is not separately preserved"
Likely consequence: Scope/atomization may teach inconsistent cue coverage and uncertainty composition
Recommended correction (NOT APPLIED): Supervisor adjudicate flat V3 scope and proposition boundaries per language; no correction applied

### L03 — HIGH (15 affected row IDs)

Heads: subjectReferent, ownerReferent, targetReferent, predicate
Evidence: "New directives/permission use action-subject distinct from request/consent owner; semantic convention needs specific Supervisor review, not artificial identity divergence"
Likely consequence: Potential inconsistency with inherited request targets where owner=subject
Recommended correction (NOT APPLIED): Approve/adjudicate each construction against V3 role semantics before any corrective task

### L04 — HIGH (3 affected row IDs)

Heads: targetReferent, ownerReferent
Evidence: "A07 two reciprocal/reflexive forms now AMBIGUOUS; toccarti targets self; inherited owner convention retained"
Likely consequence: Current candidate mixes inherited request-owner convention with new directives; ambiguity may be conservatively overused
Recommended correction (NOT APPLIED): Review these three preserved texts individually; do not guess or silently normalize

### D01 — HIGH (39 affected row IDs)

Heads: temporalRelation
Evidence: "Legacy FUTURE goal rows with overt present want/voglio/quiero remain outside the 23 CURRENT A02 preservation group; all screened IDs retained"
Likely consequence: Potential contradiction of approved present-desire convention
Recommended correction (NOT APPLIED): Adjudicate each remaining desire-time scope; do not mass-flip keyword matches

### G05 — MEDIUM (14 affected row IDs)

Heads: all
Evidence: {"codeSwitchRows": 14, "families": {"v22a_adult_it_english_term": 11, "adult_code_switch": 3}}
Likely consequence: Code-switch remains concentrated in desire; borrowed-term monolingual tags are separate
Recommended correction (NOT APPLIED): Broaden natural mixed-language contextual families; preserve intelligible slang/adult cases as resolved when warranted

### G06 — MEDIUM (0 affected row IDs)

Heads: subject, entity, object, temporal
Evidence: {"object": {"positiveClaims": 3905, "groups": 3905, "multipleGroups": 0, "multiwordGroups": 2050}, "subject": {"positiveClaims": 1449, "groups": 1449, "multipleGroups": 0, "multiwordGroups": 0}, "negation": {"positiveClaims": 472, "groups": 489, "multipleGroups": 17, "multiwordGroups": 0}, "temporal": {"positiveClaims": 425, "groups": 425, "multipleGroups": 0, "multiwordGroups": 166}, "entity": {"positiveClaims": 2347, "groups": 2701, "multipleGroups": 342, "multiwordGroups": 930}}
Likely consequence: Positive multiword/plural groups remain sparse or absent; head coverage not equal span-variety coverage
Recommended correction (NOT APPLIED): Add linguistically justified multiword persons and multiple evidence groups after review

### G07 — MEDIUM (0 affected row IDs)

Heads: all
Evidence: {"statisticalDevDisjointness": "NOT_CHECKED", "sourceAllowlist": "authorized TRAIN v1 and project-authored declarations only", "devRead": false, "frozenRead": false}
Likely consequence: Provenance isolation is demonstrated; exact overlap with inaccessible protected payloads is not asserted
Recommended correction (NOT APPLIED): Keep protected-data protocol; authorized holder may perform future permitted separation check without leaking examples

## D01–D07 closure status

- D01: 23 A02 preserved CURRENT; remaining FUTURE present-want screen recorded as defect risk
- D02: 8 report viewpoint fixes plus 6 new explicit independent-source/viewpoint rows
- D03: 6 indexed wrapper corrections plus 3 new BELIEF/3 DIRECT controls
- D04: 6 quarantine; 3 indexed reflexive dispositions; new grammatical/nonproposition controls; L04 unresolved
- D05: indexed correction preserved positive without proposition cue; 3 new positive corrected residence examples
- D06: 6 zero-claim observations; 3 ambiguous and 3 resolved same-surface contexts; G03 target status limitation
- D07: new role/topic swaps, source-viewpoint and owner/action-subject distinctions; L03 semantic review remains

The matched-text conflict is mx-v22a-adult-it-015 versus mx-v22a-adult-it-027. The candidate changed the indexed A07 row but left its identical-context counterpart inherited, producing different resolved/ambiguous target supervision. It remains unfixed. D01 screening identifies 39 surviving FUTURE present-want cases outside the 23 A02 CURRENT group; per-row adjudication is required rather than blind relabelling. These findings are not hidden by successful schema checks.

## Persistence and exact stop

Dataset outputs: train.jsonl.gz, provenance-and-mapping.jsonl.gz, quarantine.jsonl.gz, construction-review.json, manifest.json, BUILD_LOCK.json under data/student5_v3_train_v2/. Scripts/design: tools/student5_cp42/build.py, authored.py, audit.py, DESIGN.md. Audit outputs: audit.json, census.json, structural.json, redundancy.json, slices.json, input-and-source-identities.json, SHA256SUMS under reports/evidence/student5-train-v2-audit-cp42/. Report: reports/STUDENT_5_TRAIN_V2_BUILD_AUDIT_CP42.md. Continuity: docs/WORK_CONTINUITY_STUDENT_5.md. All paths are repository-owned permanent artifacts; gzip files contain actual complete payloads, not references.

Reproduce using a checkout or pinned selective snapshot containing the declared canonical inputs:
```text
python tools/student5_cp42/build.py --repo <repo> --out <new-empty-candidate-dir>
python tools/student5_cp42/build.py --repo <repo> --out <new-empty-reproduction-dir>
python tools/student5_cp42/audit.py --repo <repo> --candidate <candidate-dir> --audit <new-empty-audit-dir> --reproduction <reproduction-dir>
```
The builder rejects an existing output; audit writes solely into a new separate directory and verifies candidate hashes unchanged. Neither script imports model/training/optimizer or reads DEV/Frozen. All supplied dataset inputs are authenticated v1. Statistical exact overlap against unread DEV/Frozen is NOT claimed; source-provenance isolation is the evidence available.

Remote publication/readback is verified after this report is committed, and exact commit/counts returned in handoff. Full input identities and checksums bind reproduction. No existing model, dataset, evaluator, decoder, calibration or workflow file is changed. Only continuity and new CP42 deliverables are written.

Guards:
trainingExecuted=false
quantizationExecuted=false
onnxExecuted=false
student5PristineModified=false
trainV1Modified=false
devUsedForTraining=false
frozenDataRead=false
postAuditCorrectionsExecuted=false
nextWorkStarted=false

STOP. Supervisor must review FAIL and choose any corrections in a new assignment. No v2.1, training, model preparation, quantization or ONNX. No active job remains.
