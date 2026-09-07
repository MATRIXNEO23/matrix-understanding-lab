# WORK — Student-5 Path B — CP35a / A4 ONLY

Status: **SUPERVISOR-GPT ASSIGNMENT / OWNER-AUTHORIZED IMMEDIATE STEP**
Repository: `MATRIXNEO23/matrix-understanding-lab`
Branch: `student5-path-b-v3`
Reference HEAD at handoff: `e95571b7df4ff2ff56cf52d0603f1bb5d43f0250`

## Authority and reporting chain

```text
OWNER = Alberto / final project authority
SUPERVISOR GPT = this supervising ChatGPT session
EXECUTOR = ChatGPT Work
```

Work executes this assignment. Supervisor GPT defines the immediate scope, verifies repository-visible evidence, accepts/rejects the gate result, and prepares any later assignment. Work must not expand this assignment into later work on its own.

If the step completes, return the evidence to **Supervisor GPT** for review. If blocked, report the blocker immediately to **Supervisor GPT** with the exact attempted operations and minimum required intervention. Do not silently stop.

## Read first

1. `PROJECT_WORK_RULES.md`
2. `docs/MODEL_ARTIFACT_PERSISTENCE_POLICY.md`
3. `docs/WORK_CONTINUITY_STUDENT_5.md`
4. `reports/evidence/student5-path-b-cp35/report.json`
5. `reports/evidence/student5-path-b-cp35/artifact-manifest.json`
6. `reports/evidence/student5-path-b-cp35/artifact-SHA256SUMS`

Do not repeat TASK 2.3. Do not repeat A1/A2/A3 unless a readback/integrity check strictly required for A4 proves that the retained local package no longer matches CP35a evidence.

## ONLY objective

Close **A4 durable publication** for the already-produced CP35a Gate-A artifact.

Known retained package from CP35a:

```text
logical intent = UNTRAINED_GATE_A_RUNTIME_PROBE_ONLY
archive name = student5-path-b-v3-untrained-gate-a-cp35-20260907.zip
expected bytes = 176837978
expected SHA-256 = dfe20ae4cfa49656f557872f6ba2afeabef6caea06390f943ae8cd0945a37d71
previous Work local path = /workspace/scratch/student5-path-b-v3-untrained-gate-a-cp35-20260907.zip
source evidence commit = e95571b7df4ff2ff56cf52d0603f1bb5d43f0250
```

The repository is now public. Publish using a NEW repository-owned prerelease/release identity. Do not overwrite any existing release/tag/asset.

Preferred tag if still unused:

`student5-path-b-v3-untrained-gate-a-cp35-20260907`

If that exact tag or asset already exists, DO NOT mutate/replace it. Record the collision and use a new unique suffix only if the existing object is not the same registered artifact and doing so remains consistent with the persistence policy.

## Required execution

1. Re-read CP35a evidence and verify the local retained package still exists.
2. Verify local bytes and SHA-256 exactly match the CP35a expected identity before publication.
3. Publish the archive to repository-owned durable storage as a NEW release/prerelease asset.
4. Perform a fresh recovery/readback of the uploaded binary through a normal supported authenticated/public route.
5. Verify recovered bytes and SHA-256 independently against the expected identity.
6. Record exact release tag, release ID, asset ID, asset name, bytes, SHA-256, source/head lineage and status in the artifact registry/manifest surfaces required by repository policy.
7. Update `docs/WORK_CONTINUITY_STUDENT_5.md` with the real A4 result and exact evidence.

A4 is PASS only if:

```text
persistent repository-owned bytes exist
unique release/tag/asset identity exists
fresh recovery/readback succeeded
recovered bytes = 176837978
recovered SHA-256 = dfe20ae4cfa49656f557872f6ba2afeabef6caea06390f943ae8cd0945a37d71
registry/manifest/lineage are committed
no prior artifact/version was overwritten
```

## Autonomy inside this step

You may resolve ordinary A4 subproblems yourself: authenticated/public GitHub UI access, supported upload route, release creation, readback, checksum tooling, registry updates, and documentation fixes needed to close A4.

Do not stop merely because one upload mechanism is unavailable. Try another normal supported route available in Work/GitHub. Do not bypass access controls or extract credentials.

STOP only if A4 cannot be completed without owner action, destructive overwrite, unsupported credential handling, or a real integrity mismatch. If STOP occurs, immediately state the exact blocker, what was tried, what remains, and the smallest owner decision/action required. Do not silently terminate.

## Hard guards

```text
NO training
NO optimizer
NO backprop
NO DEV
NO Frozen
NO quantization
NO Assembling integration
NO production promotion
NO modification of pristine
NO modification of Path A
NO modification of Student-4
NO modification of TRAIN V3 v1
NO overwrite of prior Path-B artifacts
```

Do not execute or describe the next workstream after A4. Finish this assignment at A4 PASS or explicit A4 BLOCKED and report back to Supervisor GPT.

## First update

Report immediately after pickup:

```text
branch
HEAD
CP35a read = true
active operation = A4_DURABLE_PUBLICATION_ONLY
local retained package present = true/false
local bytes/SHA match CP35a = true/false
publication route selected
supervisor = GPT
```

## Final update

Return only the actual A4 result with persistent locator/IDs/checksum evidence and the resulting branch HEAD. Do not claim completion from metadata alone.

---

**Issued by: Supervisor GPT**  
Role: Matrix Engine supervisor / architecture / evidence audit / Work coordination  
Authority: owner-authorized supervision; no authority to override owner decisions  
Executor: ChatGPT Work
