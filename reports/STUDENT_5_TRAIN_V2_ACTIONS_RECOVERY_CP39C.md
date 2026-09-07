Supervisor GPT — Student-5 TRAIN v2 GitHub Actions Recovery Report

ACTIONS_RECOVERY = NOT_FOUND

Scope: targeted historical Actions/cache/artifact recovery only. No candidate recreation.
Branch: student5-path-b-v3.
Verified starting HEAD: c968992340363ba3472bbe0733958526e3e7f417.
Final HEAD: the introducing commit of this report; exact SHA supplied after publication/readback.
Date: 2026-09-07.

## Finding and limits

The previous connector limitation is resolved for enumeration through a separate, authorized read-only REST interface available in the shell. Direct HTTPS requests returned HTTP 200 for all six cache pages, seven repository-wide artifact pages, four run pages and the workflow list. There are 576 distinct caches, 624 distinct artifacts, 302 distinct runs and 11 workflows. Pagination totals and Link headers were checked; there are no failed page requests. This is repository-wide enumeration, not an HEAD/branch-only query.

No original TRAIN v2 payload or complete original generation sources were recovered. All returned caches and artifacts predate the original assignment commit ff6ee962bcc7629ace9bcd69263ddbf497376df8 (2026-09-07T09:03:19Z). All returned runs are on main, and every run's latest update also predates that assignment. The global inventory covers refs returned by GitHub even though none other than main appears. No original-candidate archive is identified.

NOT_FOUND is scoped to the Actions records exposed by these successful repository-wide queries, including the formerly omitted cache inventory. It is not a claim of global nonexistence, nor proof that a particular unidentified deleted cache ever existed. No cache or artifact is declared expired/deleted without evidence. All 624 returned artifacts report expired=false.

HTTP response Date headers are preserved verbatim: the full inventories report 2026-09-07 12:26:31–12:27:00 GMT and the targeted lookups 12:27:58 GMT. These are the server-provided snapshot dates, not a claim of an independently observed wall-clock execution time. No inference is made about subsequent remote changes.

## Historical indices

The pinned CP39/CP39b continuity and recovery evidence identify:
- logical ID student5-matrix-nlu-v3-train-v2; data/student5_v3_train_v2/.
- original creation assignment ff6ee962bcc7629ace9bcd69263ddbf497376df8.
- recovery commit 663eecad745ab0f278e411f95b21da550ed6ed1a and final-search commit c968992340363ba3472bbe0733958526e3e7f417.
- final candidate claim: 1723 rows, 2416 claims, 18 shards; ordered SHA256 01d0a249ea05febb83142ead6b730a914de67495e37dec4fa2faf6b1ccc0d813.
- initial candidate claim: 1724 rows, 2417 claims; logical SHA256 cad7b3fd078adcfec558375b267749258578a98f5e2170a1e9e42e9350f56bfd.
- initial ZIP claim: 995905 bytes; SHA256 547957a5cf98db05a2f13a051e779398ecc5b46e3b570d89cf1d90f8e93f0128.
- source names student5_train_v2_authored.py, student5_train_v2_repair.py, audit_student5_train_v2.py; local helper cp39_finish_report.py.
- original scratch paths cp39-delivery/ and cp39-candidate-01-retained/.

These remain historical comparison targets, not newly verified candidate hashes. There is no surviving original candidate run ID, cache ID, artifact ID, or Actions upload receipt. All numerical IDs below identify other existing records and must not be mislabelled as candidate IDs.

## Surface-by-surface evidence

All relative API paths below use https://api.github.com/repos/MATRIXNEO23/matrix-understanding-lab/.

| Surface | Status | Query and result |
|---|---|---|
| Connector cache listing | API_LIMITATION | github_fetch actions/caches?per_page=100 and ref-filtered variant returned connector HTTPError 400 INVALID_ARGUMENT: URL not an allowed repository/search endpoint. This was a tool URL restriction, not a GitHub empty result. |
| Direct cache enumeration | CHECKED | GET actions/caches?per_page=100&page=1 through 6: HTTP 200, total_count=576, 576 unique IDs, final page 76. All refs are refs/heads/main. |
| Current-branch caches | CHECKED | GET actions/caches?ref=refs%2Fheads%2Fstudent5-path-b-v3&per_page=100: HTTP 200, total_count=0. |
| Candidate-key cache search | CHECKED | GET actions/caches?key=student5&per_page=100: HTTP 200, total_count=0. This supplements full enumeration rather than replacing it. |
| Connector global artifacts/workflows | API_LIMITATION | Both global list URLs returned the same connector 400 restriction; direct REST below succeeds. |
| Global artifacts, including those outside current branch/HEAD | CHECKED | GET actions/artifacts?per_page=100&page=1 through 7: HTTP 200, total_count=624, unique IDs=624, final page 24. |
| All historical runs | CHECKED | GET actions/runs?per_page=100&page=1 through 4: HTTP 200, total_count=302, unique IDs=302, final page 2. Same run ID set as CP39b. |
| Historical workflows | CHECKED | GET actions/workflows?per_page=100&page=1: HTTP 200, 11 workflows. All 10 workflow IDs used by the 302 runs are represented. The 11 pinned workflow YAML files were also read as code only. |
| Assignment SHA and subsequent runs | CHECKED | GET actions/runs?head_sha=ff6ee962bcc7629ace9bcd69263ddbf497376df8&per_page=100 and created=>=2026-09-07T09:03:19Z filter: HTTP 200, zero each. |
| Reruns | CHECKED | Inventory contains two run_attempt=2 records: 34080903226 and 33882172879. Direct GET actions/runs/{id}/attempts/1 returned HTTP 200 for each; both first attempts predate the assignment. Latest attempts are in the global inventory. |
| Surviving artifact direct ID | CHECKED | GET actions/artifacts/10006902236: HTTP 200, p05-training, created/updated 2026-09-07T06:32:25Z; unrelated pre-assignment artifact. |
| Original-candidate direct ID | IDENTIFIER_UNKNOWN | No original candidate run/artifact/cache ID survives in the historical evidence. Full global enumerations and SHA/time/ref/key queries were used instead. |

The 302 run conclusions are 185 success and 117 failure. No cancelled/in-progress run appears in the returned unfiltered inventory; none was excluded by a success-only filter.

Latest run: 34080903226, P0 Understanding Lab, main SHA 9493e97cbdf5e731ee161b24d91b511076decb19, workflow 349216495, attempt 2, updated 2026-09-07T06:32:40Z. The other September 7 runs 34080789651 and 34080779770 failed before this.

Latest run artifact IDs are 10006903130 (p0-android-probe), 10006902555 (p05-baseline), 10006902236 (p05-training), 10006901702 (p0-results). Across all 624 records the latest created/updated time is 06:32:27Z, before the original assignment. All artifact names, sizes, digests, run associations and dates are persisted in inventory.json.

## Cache-specific gap closure

The newest cache is 7403257447, created/last accessed 2026-09-07T06:32:37.168032000Z, 1396079 bytes, a Gradle cache keyed to main SHA 9493e97cbdf5e731ee161b24d91b511076decb19. No cache creation or last-access timestamp in the 576 records is later.

There are 572 gradle-prefixed caches, two setup-python pip caches and two model-cache keys:
- 7303790909: matrix-nlu-geotrend-36de33ec-v1, created 2026-09-03T20:26:32.268761000Z.
- 7329065465: matrix-nlu-geotrend-36de33ec-v22a, created 2026-09-04T13:01:45.358799000Z, 271460048 bytes.

Pinned YAML binds the model-cache keys to .cache/huggingface, with HF_HOME under github.workspace. Older v2/v21 key references in workflow code have no matching entry in the full inventory. Absence does not establish expiration or deletion; no such classification is asserted.

All cache IDs, refs, keys, versions, sizes and timestamps are preserved. The API metadata provides no archive download URL. No cache payload download was attempted because no returned entry was temporally/provenance-compatible with the original candidate or its original generator, and the source YAML identifies dependency/model caches. This is not a claim that their bytes were inspected. Restoring a cache by dispatching a new workflow was not performed and is unnecessary for the identified records. No potentially pertinent entry remains unclassified as merely “non-enumerable.”

GitHub CLI is absent; git and curl are installed. GH_TOKEN/GITHUB_TOKEN and /root/.config/gh/hosts.yml were absent in the presence-only checks. No credentials were printed or extracted. Direct curl and Python urllib.request succeeded without a manually supplied token, so no browser login, UI-only fallback or CLI installation was needed.

## Payload certification and scope

Recovered candidate payloads: zero. Candidate count/size/SHA cannot be recertified. Text reports, metadata and checksums were not counted as recovery. No unrelated mixed dataset/model archives were downloaded or opened; DEV and Frozen payloads were never read.

The only delivery changes are this report, inventory.json, SHA256SUMS and docs/WORK_CONTINUITY_STUDENT_5.md. Prior CP39/CP39b evidence remains intact. The publication tree is compared against the starting tree to require every pre-existing blob outside this allowlist to remain identical; no dataset/evaluator/decoder/calibration/workflow mutation is authorized.

Evidence: reports/evidence/student5-path-b-cp39c-actions-recovery/inventory.json contains API query URLs, response statuses and pagination headers, global records, direct lookup responses, hashes of raw local responses, connector failures and pinned workflow source/blob identities. SHA256SUMS covers the report, inventory and continuity. Reproduction uses read-only GET requests to the recorded URLs; pagination must be exhausted before interpreting absence.

trainingExecuted=false
canonicalDevRead=false
frozenDataRead=false
trainV1Modified=false
evaluatorModified=false
decoderModified=false
calibrationModified=false
quantizationExecuted=false
onnxExecuted=false
trainV2Recreated=false
nextWorkStarted=false

STOP. No verdict authorizes training or recreation. Await the next Supervisor GPT assignment.
