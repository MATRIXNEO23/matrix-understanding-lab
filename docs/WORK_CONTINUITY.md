# Matrix Understanding Lab — work continuity

Last updated: 2026-09-04T15:50:00+02:00
Continuity schema: `matrix.lab.continuity.v1`  
Rule: update after every meaningful commit, training/benchmark, model/data or
strategy change, before long/risky work, and before ending any session.


## LATEST — Student-4-v2.2A Controlled Repair

- Authoritative run [`33860928806`](https://github.com/MATRIXNEO23/matrix-understanding-lab/actions/runs/33860928806), job `100984948899`, completed successfully as workflow infrastructure at run HEAD `617aeca8a6abac4366eb13347fb88026307dc3b8`.
- Model decision: `EXPERIMENTAL_TEST_CANDIDATE / NOT_PRODUCTION_APPROVED`. The unchanged dev selection is `FAILED_GATE`, selected threshold `null`; no gate was lowered.
- Training: fresh `student-4-v2.2a`, 4 encoder layers, 58,599,411 parameters, train/dev only, `defer-frozen`. Early stop at Matrix epoch 8/10; best score `0.9577545560826969` at epoch 5.
- Model-state SHA-256: `446b6a58265500001efd350f81d75867227cbfd3c6da699ed9c9330257d16a9c`; resumable checkpoint SHA-256: `b57737a3e3f6acf9d72da86f918f730f9bb655839c6cf00f8b614d3b706f815b`.
- Preserved report artifact `9938144318`, digest `e71e153509e8f002fd74782ebb5667bb93b59438e6646c4c11723afe4be64129`; bundle `9938150338`, digest `f2dfea052df525af741f8ddd98e279b5443645450d09f949970a6eac18edb987`; resume `9938165358`, digest `ff66bd687fc55f1b767164b84795ad84aba4937130b7d8b0aead9afff5f018cd`.
- Report archive digest matches GitHub; all 23 present evidence files represented in `SHA256SUMS` match with no mismatch. Standard dataset audit is `PASS`.
- Repair auxiliary SHA-256 `8be02976d46ba47d746ff7307d688d93595453221965b3de995d4b1de655799f`: 375 unique train-only rows, exactly IT core 139, ES core 70, EN core 69, adult/intimacy IT 60, cross-lingual 37. Adult subset is project-authored semantic robustness and adds no safety/censorship label.
- Matrix dev overall: exact-set `0.679894`, claim exact `0.713992`, negation F1 `0.490644`, predicate `0.936214`, ownership corruption `0`. Exact-set IT/ES/EN: `0.619048 / 0.523810 / 0.896825`; negation F1: `0.287037 / 0.129534 / 1.0`; predicate: `0.808642 / 1.0 / 1.0`.
- P0.5 dev overall: exact-set `0.516667`, claim exact `0.654762`, negation F1 `1.0`, predicate `0.797619`, ownership corruption `2` (both IT). Exact-set IT/ES/EN: `0.45 / 0.50 / 0.60`; predicate: `0.857143 / 0.75 / 0.785714`.
- Compared with v2.1, P0.5 improves, but Matrix overall regresses and IT predicate/temporal plus ES negation remain critical. Therefore this is preserved for practical experimental review, not production approval.
- `FROZEN_GUARD.txt`: `frozenDataRead=false`, `frozenEvaluationExecuted=false`, `trainingSplitsRead=train,dev`, `onnxExported=false`, `quantizationExecuted=false`. Frozen was not read; dev was not modified; no ONNX, INT8, packaging, or promotion occurred.
- Complete report: `reports/STUDENT_4_V22A_CONTROLLED_REPAIR_REPORT.md`, introduced by commit `12ac2cfebdce171392893d5692d17d03e8317886`.
- Exact next activity: user review of FP32 metrics and an explicit decision on practical/quantization testing. Preserve bundle and checkpoint; do not automatically quantize, open frozen, alter dev/gates, retrain, package, or promote.

## LATEST — Student-4-v2.1 post-run dev gate

- Source training run/commit: `33837897457` /
  `72f14286e89df88f41aedb169c7307b26b57eedf`. Training was not repeated.
- Import fix commit: `3dd2be2cc45d4cde1b439fb261c8c167ab1eb4bb`;
  post-run workflow commit:
  `31ba96d40d6f662bbb253ce2c60146d8cf6f026e`.
- Final provenance-hardening/run HEAD:
  `813126cbff80bfb6bc82636c87e8ac16b1a917a8`, branch `main`.
  It requires the three bundle files and verifies variant
  `student-4-v2.1`, `studentLayers == 4`,
  `trainingSplitsRead == ["train", "dev"]`, `frozenDataRead == false`,
  and model checksum.
- Final dev-only run: `33848931720`, job `100947061031`, SUCCESS as
  infrastructure execution. Evaluation artifact
  `matrix-nlu-student-4-v21-post-dev-33848931720`, ID `9927657001`,
  archive SHA-256
  `2314694e5b45f6a95ba409808394013d3a43f92f6d798765fc5cdb01ff3fcb41`.
- Controlled model decision: `STOPPED_FOR_REVIEW`. Threshold selection is
  `FAILED_GATE` across 188 dev-only candidates; selected threshold is
  `null`. Gates were not lowered.
- Threshold-zero combined result: claim-count exact `1.0`, exact claim set
  `0.6997549019607843`, valid coverage `0.9952651515151515`, selective
  accuracy `0.7259752616555661`, ownership corruption `2`, World Truth
  updates `0`.
- Matrix dev: exact set `0.7195767195767195`, claim exact
  `0.7325102880658436`, field exact `0.994055784179241`, span F1
  `0.9534940610475388`, entity F1 `0.9851455733808675`, negation F1
  `0.5091693635382956`.
- P0.5 dev: exact set `0.45`, claim exact `0.6071428571428571`, field
  exact `0.9113756613756614`, span F1 `0.9772014222965907`, entity F1
  `0.9457013574660633`, predicate `0.75`, temporal relation
  `0.8928571428571429`, with two IT ownership corruptions.
- Residual error counts: span decoding `269`, semantic classification `99`,
  entity resolution `40`, authority/referent decoding `20`; 245 failed
  observations. Weak critical families remain negation, request, correction,
  goal, temporality, referents, third-party/report and multi-claim, especially
  IT/ES.
- Complete metrics, per-language/head/family tables, checksums and baseline
  comparison: `reports/STUDENT_4_V21_POST_DEV_REPORT.md`.
- Targeted quantization policy:
  `docs/decisions/2026-09-04_STUDENT_4_V21_TARGETED_QUANTIZATION.md`.
  It is recorded but NOT executed. Because dev failed, do not export ONNX,
  quantize, read frozen, retrain blindly, alter thresholds/datasets, integrate
  Android, package or promote.
- Exact next activity: supervisor review of the dev evidence and a separate
  authorization for any targeted fine-tune/retraining decision. Frozen remains
  closed.

## Repository state

- Repository: `MATRIXNEO23/matrix-understanding-lab`
- Branch: `main`
- HEAD entering the controlled-stop documentation update:
  `a556095d84cd2c8f39b54c957e3b15e8bbb93132`.
- Training launch commit:
  `37ef11c99785fb0fd56e99267f33e71d4c9e15e6`.
- Last consolidated implementation commit:
  `c5640655ff1febee043335406a85fb338b7a8b42`
  (`ci: block retraining on inconsistent annotation contracts`).
- Last audit/handoff commit:
  `846748547f892b483effb85b8cf71cb62f669f6e`
  (`docs: record blocking annotation contract decision`).
- Production Matrix repository/runtime: frozen reference only; no production
  files have been modified.
- Frozen production semantic reference:
  `ae82d5cf843d52b3d60caadd161e4a5516fc5d0d`.

## ACTIVE CONTROLLED RUN — Student-4-v2.1

- **STOPPED:** run `33837897457`, launch commit
  `72f14286e89df88f41aedb169c7307b26b57eedf`, job
  `train-and-dev-only` `100914050985`. Training completed through Matrix
  epoch 7 (best epoch 5, best score `0.9676758069767126`), but step 11
  `Evaluate development and stop` exited 1 before inference with
  `ModuleNotFoundError: No module named 'matrix_nlu'`.
- Cause: `WORKFLOW/INFRASTRUCTURE_FAILURE`, not a model or dev-gate failure.
  No end-to-end dev metrics or gate decision exist. Per mandatory policy, no
  correction or rerun was attempted.
- Recoverable latest checkpoint SHA-256
  `34cd061c4eec158b9fc89341030adbc122f0355f09923c54eefe0da72acf66e8`;
  best model-state SHA-256
  `6228fddb5240edaac58356ccd175f6a97e2bc0fccd6344ebf675f42103317bae`.
  Report/bundle/resume artifacts: `9926693211`, `9926696572`,
  `9926705228`.
- Frozen evidence remains `frozenDataRead=false`,
  `trainingSplitsRead=[train,dev]`, `frozenEvaluationDeferred=true`.
  **FROZEN NOT TOUCHED**.
- Full evidence and baseline comparison:
  `reports/STUDENT_4_V21_STOP_REPORT.md`.
- Final state: `STOPPED_FOR_REVIEW`. Exact next activity: wait for supervisor
  review. No new run, fix, hyperparameter/dataset/model/pipeline change,
  frozen access, V2.2/V3, export, packaging or promotion is authorized.

- Supervisor authorization replaces the prior stop only for one fresh
  `student-4-v2.1` experiment. Baseline remains `student-4-v2` research-only;
  no production promotion is authorized.
- Preparation HEAD: `3be3238a32c840beecd57e1c3109e88571b1696a`, branch `main`.
  The run uses `matrix.nlu.dataset.v2` with train-only generalization revision
  from `a556095d84cd2c8f39b54c957e3b15e8bbb93132`; Matrix train hash
  `5118d37ce2ab19d5be171f757f448698085e3c222a4a627f9838329836185820`.
  Matrix dev and P0.5 dev remain unchanged at
  `704e809f0e9ebace3a5c047989b74d354ac8811757a2644b0d9c04cfb0631012`
  and `7533f56194431bd17b6f8544031d5436ca14ee6e209336da8133e1f05cdf0866`.
- Configuration SHA-256
  `1011dae1572c24b7aabb07c21027c2eab93aa285f17de536bc9bfa4a671b2964`:
  same four-layer architecture, seed, learning settings, loss weighting and
  dev gates as Student-4-v2. No capacity or gate change; MASSIVE frozen sample
  count is zero because the controlled run is train/dev-only.
- Workflow `Matrix-NLU Student-4 V2.1 Controlled Stop` has no dispatch/resume
  entry and stops after exactly one dev threshold decision. It never invokes
  the frozen-capable `auto_test.py`, never exports/packages/promotes, and emits
  explicit `frozenDataRead=false`, `trainingSplitsRead=[train,dev]` evidence.
- Exact next activity: create one trigger commit, observe the single run,
  preserve its artifacts, then write `reports/STUDENT_4_V21_STOP_REPORT.md`
  and update this file. Regardless of dev outcome, do not rerun and do not
  open frozen without new explicit authorization.

## CONTROLLED STOP — Student-4-v2

- Stop status: `WORK SAFELY STOPPED`. Branch `main`; repository
  `MATRIXNEO23/matrix-understanding-lab`. This section is documentation only.
  No new Student-4-v2 run may start without a new explicit supervisor
  authorization. Do not resume, retrain, alter dataset/model/hyperparameters/
  gates/pipeline, open frozen, package, promote or begin later modules.
- Canonical references remain
  `docs/FINAL_MATRIX_UNDERSTANDING_ARCHITECTURE.md` at
  `cf6395b0fefc254febe3c804751ca4b048f974d1` and the approved original v2
  dataset checkpoint `d2d455a33e5f725e0189010d081d0973aeb0b9a6`.
- Failed workflow: `Matrix-NLU Student-4 V2 Checkpoint`, run `33826815562`,
  source commit `f04b069d8c989d7894d6028367987c2baf79bbfb`, branch `main`; job
  `train-dev-frozen-export-package` id `100881136163`; failing workflow step
  7 `Run audited Student-4-v2 checkpoint pipeline`. The inner stage was
  `select-threshold-from-development-only`: `select_threshold.py` exited 2;
  `auto_test.py` reported exactly
  `RuntimeError: step 'select-threshold-from-development-only' failed with exit code 2`;
  the enclosing workflow shell step exited 1.
- Cause classification: `DEV_GATE_FAILURE`, not `TRAINING_FAILURE`.
  `auto_train.py` completed `SUCCESS` in 7,793.116555 seconds. None of the 189
  dev-only threshold points met the unchanged combined accuracy, coverage,
  ownership and critical-family gates.
- Run dataset/provenance: `matrix.nlu.dataset.v2`; Matrix train/dev/test hashes
  `e6190bf4fe0c5d326242920be6b3e0fbcb6f6fc593f4d7a017ffd08f74bb0eff` /
  `704e809f0e9ebace3a5c047989b74d354ac8811757a2644b0d9c04cfb0631012` /
  `458f79ecaa9ec547c53a55ba68c45531e88e0ae5a0d6ee405222632d85919228`;
  P0.5 train/dev/test `413f60ca17879ed9de440add7903b6e2abaebdfbbed6055b32c6e0b105cadfcd` /
  `7533f56194431bd17b6f8544031d5436ca14ee6e209336da8133e1f05cdf0866` /
  `a729045ac17356321f2b8c6624554c8bf8ad22fd794e2c0718876734de0aabc2`;
  v1-to-v2 mapping
  `ca0ec3dd9f4283a849d166fdca02193ca75cbea8b88bcbda5890378786c223bb`.
  Pre-training audit was PASS with zero contradictions, span/schema/
  convention/authority failures and zero exact or semantic-template leakage.
- Configuration used: `student-4-v2`, four retained Geotrend encoder layers,
  seed 810923, max length 64; MASSIVE auxiliary 3,000/600 train/dev examples
  per language for one epoch; Matrix maximum 8 epochs, batch 16, gradient
  accumulation 2, LR `3e-5`, weight decay `0.01`, warmup `0.1`, P0.5 repeat
  16, patience 2, inverse-frequency-square-root token/sequence weights capped
  at 8. Training stopped normally at Matrix epoch 6 after two non-improving
  epochs; best model is epoch 4.
- Latest epoch-6 values: train loss `0.009445434005818132`; Matrix dev loss
  `0.26068120008265533`, macro-head accuracy `0.968186626758156`; P0.5 dev
  loss `0.36911421846598386`, macro-head accuracy `0.9487154305239973`.
  Best epoch-4 score `0.9590511996891526`; epoch-4 train loss
  `0.015433126276367025`, Matrix dev loss/macro `0.24845617968175146` /
  `0.9690468189636554`, P0.5 dev loss/macro `0.34759796168655155` /
  `0.9490555804146498`. A macro F1 is not emitted by the trainer; valid
  end-to-end span/entity F1 values are recorded below.
- Latest epoch-6 per-head Matrix dev accuracies: claim kind `1.0`, dialogue act
  `0.989712`, owner `1.0`, perspective `1.0`, polarity `0.870370`, predicate
  `0.952675`, subject `1.0`, target `0.962963`, temporal relation `0.969136`,
  boundary `0.986904`, entity `0.987964`, negation token `0.873621`, object
  token `0.943497`, subject token `1.0`, temporal token `0.985958`. P0.5:
  claim kind `1.0`, dialogue act `0.857143`, owner/perspective `1.0`, polarity
  `0.916667`, predicate `0.821429`, subject/target `0.928571`, temporal
  relation `0.904762`, boundary `0.997658`, entity `0.987593`, negation token
  `0.962779`, object token `0.940447`, subject token `1.0`, temporal token
  `0.985112`.
- Threshold-zero Matrix dev: claim-count exact `0.997354`, exact-set
  `0.560847`, claim exact `0.619342`, field exact `0.970736`, span F1
  `0.927804`, entity F1 `0.982728`, coverage `1.0`, ownership corruption `0`,
  invented World Truth `0`. By-language exact-set: EN `0.785714`, ES
  `0.547619`, IT `0.349206` (worst IT); field exact EN `0.975309`, ES
  `0.963649`, IT `0.973251`.
- Threshold-zero P0.5 dev: claim-count exact `0.983333`, exact-set `0.483333`,
  claim exact `0.630952`, field exact `0.916667`, span F1 `0.968394`, entity
  F1 `0.972851`, ownership corruption `2`, World Truth `0`. Exact-set EN
  `0.6`, IT `0.5`, ES `0.35` (worst ES); field exact EN `0.936508`, IT
  `0.924603`, ES `0.888889`.
- Recoverable checkpoint: `checkpoints/latest.pt`, SHA-256
  `c003f19ea4f7e2c0b800a1e2758c07357856a24ed98460b67e1816d09c8ef30d`,
  epoch 6/8, with optimizer, scheduler, history, current model and embedded
  `bestModel` from epoch 4. Best exported training model `model-state.pt`,
  SHA-256
  `a4897d74970c6f16db4025d6df2b54e34dd34fbe8976b526976d9fd04e75b20f`;
  training-result SHA-256
  `d0e046642383182a6e55504171abddba8ac6826396a6888f21a321973d1e82ff`.
- Preserved GitHub artifacts: report id `9922954442`, 353,528 bytes, archive
  SHA-256 `f28f3d8e0ac33dd7fb84b22f382fc4e7024469f544502456fdd1ea4bae2892e9`;
  model bundle id `9922957297`, 217,601,926 bytes, archive SHA-256
  `28af0eb9300f70f9f6f1f8846aadacb87f57a5ad300f6d87570386185714a6ef`;
  resume artifact id `9922965503`, 646,873,821 bytes, archive SHA-256
  `6bb7f268a8c9a2931261dddd2f9566aef16eb3fe71a8684a798c2eb33a4cc02f`.
  Report includes all automation/training/dev logs, raw dev predictions/errors,
  threshold curve, failure summary, audit/manifests and checksum inventory.
  Dev-error-analysis SHA-256
  `ae085cf4cfd2c7428920f0c10469cfcda08e735290bd7aa785d6859e4592e716`;
  threshold-selection SHA-256
  `3dcbdac5f437bf551383a3ac1dae4eadfc761307c76cf24e2dee412b8b268e6b`.
- Frozen verification: training-result has `frozenDataRead=false`,
  `trainingSplitsRead=[train,dev]`, frozen status
  `DEFERRED_UNTIL_DEV_THRESHOLD_GATE`; auto-test has
  `frozenDataUsedForTuning=false` and stopped at dev selection.
  **FROZEN NOT TOUCHED**.
- Current HEAD note: commit `a556095d...`, made before this stop order, contains
  an untrained train-only v2 augmentation and documentation; it was not used by
  failed run `33826815562`. Its ordinary P0 run `33835437163` and candidate
  probe `33835437180` are green, but no Student-4-v2 run was launched from it.
  Preserve it unchanged and do not execute it without new authorization.
- Exact activity at STOP: artifact/checkpoint verification and continuity-only
  commit. No experimental correction, rerun, frozen access, packaging,
  production integration, Memory, B4, Emotion, Reflection, Agency or NPC-NPC
  work is active. The older `docs/P05_OPENNLP_HANDOFF.md` is a separate,
  immutable P0.5 baseline handoff and is intentionally unchanged.

## Canonical specification and objective

- Canonical specification:
  `docs/FINAL_MATRIX_UNDERSTANDING_ARCHITECTURE.md` at
  `cf6395b0fefc254febe3c804751ca4b048f974d1`.
- Hardware/runtime-budget supplement added concurrently and preserved:
  `docs/FINAL_MATRIX_ECOSYSTEM_MOTO_G56.md` at
  `21e1de86fc0ecf8ce86d59b71ab89e2bccc827ea`. It does not supersede the
  trained Understanding architecture; for this gate it adds the 25–45 MB
  Matrix-NLU target, 60 MB warning ceiling, offline/ONNX/INT8 and zero-cost
  training constraints.
- Maximum-depth validation strategy appended to that supplement at
  `968953a9b6dade4d039577f989f31292d959d1f8`; it requires a large genuinely
  unseen adversarial IT/EN/ES benchmark, Italian-primary reporting, confidence
  calibration, repeated seeds/dispersion where stochasticity matters and
  permanent regression evidence. This was a concurrent documentation-only
  commit and is preserved in the current lineage.
- Canonical supervision method added concurrently and preserved at
  `docs/SENIOR_SUPERVISOR_EXECUTION_PLAN.md`, commit
  `16d53e55bdc419717ddda717e7fc00aae5690192`. For current component C1 it
  confirms the trained Matrix-NLU direction, OpenNLP canary, bounded autonomy,
  zero-cost/resumable training, no frozen-test tuning, and explicitly says the
  current training should continue absent a concrete Gate-0 violation.
- Python memory architecture blueprint added concurrently and preserved at
  root `ARCHITETTURA.md`, commit
  `4ef989f2a0fc0a0f246ef4e03f186b600cdb8e9a`. Its own status says design only
  and no application code authorized; therefore it does not authorize starting
  Memory or another component and does not alter the active C1 training.
- Canonical automated train/test policy added concurrently and preserved at
  `docs/AUTOMATED_TRAIN_TEST_PIPELINE_POLICY.md`, commit
  `6e6a0c473ef929035d188005776e5a83355887ca`. It requires one-command,
  resumable, provenance-locked, failure-preserving automation and confirms that
  ordinary training/data/calibration faults are autonomous C1 work, not user
  decisions. The active training plus `matrix-nlu-post-train.yml` implement the
  previous two-stage form. Commit `732725fd...` now adds a strict single
  orchestration entry point; its control-flow/unit gates are green, while its
  model-dependent execution waits for the already-running teacher artifact.
- A one-command training orchestrator was added concurrently at `auto_train.py`,
  commit `3f9cfa1b8e60db875cdbd8fc405f94e0f81f6b36`. It runs software tests,
  dataset/MASSIVE preparation and resumable training, validates checksums and
  preserves/promotes a last-good bundle atomically. It has not been executed and
  must not be invoked while run `33786677296` is active. Its eventual integration
  with post-training quality/export gates is now implemented at `732725fd...`.
  Teacher and student outputs/checkpoints are isolated so a four-layer run
  cannot consume an incompatible six-layer checkpoint.
- The specification was reread in full after the controlled P0.5 stop.
- Current objective: build and objectively gate the trained IT/EN/ES
  Matrix-NLU in this lab only:
  `text -> tokenizer -> compact pretrained multilingual Transformer -> learned
  Matrix multi-task heads -> Typed Claims -> deterministic invariant validator`.
- OpenNLP Candidate B is frozen as baseline/oracle/fallback. Do not continue
  training or semantic-rule fixes intended to make it the production solution.
- Do not request Moto G56 tests until provenance, software, frozen quality,
  calibration, ONNX parity, INT8 and offline Android gates are green.

## Completed checkpoints and evidence

### P0 baseline laboratory

- P0 benchmark completed in the isolated lab; production verdict was `KEEP`.
- Canonical P0 evidence remains in `docs/P0_*`, `docs/CANDIDATE_*`,
  `gold/p0-gold-v1.json`, and archived benchmark artifacts.
- P0 gold SHA-256:
  `85ae9320bea512cda2a3748bc49acc610a7b9d9dd17eee5222a2616faea6a99a`.

### P0.5 OpenNLP work — controlled stop, preserved

- Data plan commit:
  `263690efbe76fe05655909ccdcd4ce2c9fe0dfc6`.
- Clean Italian trainer/API/CI commits:
  `cd801e169deb68170efc7592db948cc482dd17ca`,
  `84be3d3b2aef8d368ed518dd49d6060f806206f5`,
  `47d9b15ce09af75d89e05677b39069ba6ede6cb8`.
- Expanded frozen gold commit:
  `86cd30db7bb3b12f52bf70e198a38f29f961de10`.
- Expanded pre-fix benchmark commit:
  `cf1a7b990bf587f696a2e289fb7071a3e7cfa8ad`.
- Controlled-stop preservation commit:
  `5b9bb591586c8bb03acb49d40dbb156d53bd5a95`.
- Full handoff: `docs/P05_OPENNLP_HANDOFF.md`.
- P0.5 gold: 88 scenarios / 264 IT/EN/ES cases; train 87, dev 84,
  frozen test 93 cases. SHA-256:
  `08c216641bdc071059c5dfd261a271dedc481a6879705ffb06c57164f01b9ea1`.
- Selected clean Italian POS variant: perceptron, iterations 100, cutoff 1,
  MarkIT source revision `e210079df0aea331ec1dcaa90648d815ce94c3ce`,
  CC BY 4.0.
- Selected POS model: 126,860 bytes; SHA-256
  `14dca59954129b1f4554def4e16d1b626160f0289ab568f5a1efdd2d1bba91c7`;
  dev accuracy `0.926243`, frozen test accuracy `0.920851`.
- Alternative preserved POS models:
  - maxent i200/c1: 417,199 bytes, SHA prefix `40f5ad`;
  - maxent i100/c1: 416,913 bytes, SHA prefix `d9dae4`.
- Expanded Candidate B baseline: 264 cases; overall field exact
  `0.9851290685`; frozen-test field exact `0.9803439803`; claim-count exact
  `1.0`; span F1 `1.0`; negation F1 `0.9375`; entity F1 `0.766169`;
  ownership violations `0`; invented World Truth `0`; worst-language field
  exact (IT) `0.981481`.
- Preserved artifacts under `artifacts/p05-opennlp-baseline/`, including all
  models, license, manifest and expanded results.
- CI `33781321112`: green; artifact `p05-training` id `9903733326`, archive
  digest prefix `cd391f1e`.
- CI `33782141363`: green (expanded gold).
- CI `33782429036`: green; artifact `p05-baseline` id `9904168628`, digest
  prefix `99b63ea`.
- No further OpenNLP production-directed fix/training is authorized.

### Matrix-NLU trained architecture transition

- Canonical architecture commit `cf6395b0...` is incorporated as the controlling
  specification.
- Model/data planning and candidate-probe commit:
  `6bf5492fd4155e4e77b2a6e514a793f8e5e6c5ff`.
- Plan: `docs/MATRIX_NLU_MODEL_DATA_PLAN.md`.
- Candidate probe inputs SHA-256:
  `d169d72bc50b2b928690cf294c538100024a96c578c25337f2d3f02a0a87a96c`.
- Local dependency-free probe tests: 3/3 green; Python byte compilation green.

## Current gate and exact activity

- Dataset-v2 pre-training checkpoint completed locally under the supervisor's
  approved Option A. The original v1 builder/data/checkpoints/artifacts/results
  were not changed. All six v1 dataset hashes were reconstructed and matched
  before v2 generation.
- Frozen `matrix.nlu.dataset.v2` hashes:
  Matrix train/dev/test `e6190bf4...` / `704e809f...` / `458f79ec...`;
  P0.5 train/dev/test `413f60ca...` / `7533f561...` / `a729045a...`.
  Reproducible v1-to-v2 mapping SHA-256 is `ca0ec3dd...`.
- Mapping evidence: 1,322 claim corrections, 426 structural anti-leakage drops,
  and 24 balanced train-only IT/EN/ES additions. The additions close previously
  absent train coverage for `attribute.is` and `PAST`; no held-out surface was
  copied.
- Pre-training audit is `PASS`: zero incompatible gold inputs, zero invalid or
  out-of-source spans, zero schema/label/convention/ownership/authority/
  provenance/checksum errors, and zero exact-surface or >=0.97 normalized
  semantic near-paraphrase leakage across train/dev/frozen. Frozen predictions
  and frozen quality were not read.
- Software suite after the checkpoint: 71/71 green. Exact contract and hashes
  are documented in `docs/MATRIX_NLU_DATASET_V2.md`.
- Dataset-v2 checkpoint commit:
  `d2d455a33e5f725e0189010d081d0973aeb0b9a6`
  (`feat: freeze audited matrix nlu dataset v2`).
- The fresh `student-4-v2` orchestration is locally complete: config, training,
  status, checkpoint, last-good training/package and verification directories
  are variant-isolated. The trainer rejects v2 without `--defer-frozen`, reads
  and hashes only train/dev plus manifests/config, and records
  `frozenDataRead=false`; `auto_test.py` infers v2 from the bundle and cannot
  open frozen/adversarial data until dev-only threshold selection passes.
  The 1-click v2 dry-run, Python byte compilation, all Matrix workflow YAML
  files and 71/71 tests are green. Training has not started.
- Orchestration checkpoint commit:
  `42e065cf80b7dcc5d0903733ed79b26fdded1122`
  (`ci: isolate student-4-v2 train and evaluation gates`). The connector did
  not expose push-run status through combined commit statuses; the pipeline
  still repeats the complete software and dataset gates before it can train.
- Pre-trigger hardening consolidated on top of `42e065c`: the original
  v1 one-click workflow has been restored byte-for-byte in behavior and a new
  `.github/workflows/matrix-nlu-student-4-v2.yml` isolates v2 triggers and
  artifacts. Checkpoints now carry and enforce dataset/config/variant/layer
  identity; the evaluation package is explicitly `counter-review`, never
  production. Dev threshold selection and frozen gates now report and enforce
  critical-family exactness for negation, request, goal, correction,
  temporality, referents, third parties and multi-claim inputs. Frozen coverage
  contains every family in every target language.
- Hardening checkpoint commit:
  `238eba30fbee5c633a059043a13d80bde17dd263`
  (`ci: harden isolated student-4-v2 gates`). Its ordinary P0/probe CI is in
  progress; it does not launch a second training run.
- A concurrent writer committed the one-time trigger early at
  `f5920ca602d053e050a562a13ee744b06b7a366e`, launching run `33818777290`
  on the preceding `42e065c` pipeline. That run is fresh, v2-only,
  train/dev-only before calibration, and currently in its strict pipeline
  step. Because it predates checkpoint identity and critical-family reporting,
  it will be treated as training evidence only unless all evidence can be
  revalidated through the hardened post-training path; no second run is being
  launched while it is active.
- Current activity: monitor run `33818777290`, preserve its isolated artifacts,
  verify hardening CI, and revalidate any completed bundle through the hardened
  dev/frozen/export path without retraining if possible. Exact configuration:
  dataset v2, four-layer
  Geotrend student, seed 810923, MASSIVE auxiliary 3000/600 per language for
  train/dev, Matrix 4 epochs, batch 16, accumulation 2, LR 3e-5, patience 2.
  No v1 checkpoint may be restored into this variant. Production/runtime,
  Memory, B4, Emotion, Reflection, Agency and NPC-NPC remain untouched.
- Hardened bundle revalidation is implemented in the new, separate
  `.github/workflows/matrix-nlu-student-4-v2-post.yml`: it downloads the
  immutable model bundle from run `33818777290`, asserts v2/four-layer/
  train-dev-only provenance, reruns the v2 audit and software suite, performs
  dev-only threshold selection, and only then permits frozen/error-analysis/
  ONNX/INT8/parity/package gates. It never invokes training and packages only
  a counter-review candidate. Local suite is 72/72 green; workflow YAML parses.
- Run `33818777290` completed all MASSIVE and four Matrix epochs, then failed
  during final provenance serialization because `train.py` requested the
  nonexistent `massive-manifest.json`; the canonical preparer writes
  `build/matrix-nlu/massive/manifest.json`. This is an ordinary post-training
  code fault, not a model or dataset gate failure. Frozen data, dev threshold,
  error analysis and ONNX were not run. Final checkpoint state is Matrix epoch
  4/4, best dev head-average `0.9499156251469446`; resume is preserved.
- Run `33818777290` artifacts: report id `9919724554`, 41,624 bytes, archive
  digest `sha256:2b0261201fe9ea7e2292ee6f4e40982c1582b413768e15dba6c9f02913c588ab`;
  model bundle id `9919728536`, 217,595,894 bytes, digest
  `sha256:06e6f991f2bbeb100ff45a1a905b5a93f79796b7eaf9b9697920521e986115e4`;
  resume id `9919738635`, 646,922,522 bytes, digest
  `sha256:0c1ee169905e7abf8a45b36a7f2ead4f27922ff7fbbf75a6a26ab3f3fc755a77`.
- Recovery pending consolidation: correct the MASSIVE manifest path; validate
  external resume evidence against source run, v2 audit, variant/layers and
  checkpoint SHA-256; permit adoption only for this pre-identity v2 checkpoint;
  then resume from epoch 4 without replaying training. Local suite is 73/73
  green, dry-run carries explicit `--resume-evidence`, and all YAML parses.
- Recovery checkpoint `e02948093595eaf6f2e9a9b39b4937cdf843a028`
  (`fix: resume completed student-4-v2 checkpoint safely`) passed CI: P0 run
  `33825683892` success and candidate-probe run `33825683886` success. Exact
  next action is to commit `pipeline/student-4-v2-resume.trigger` containing
  source run `33818777290`; the isolated workflow will verify and adopt its
  epoch-4 checkpoint, serialize the missing training result, then execute dev
  calibration and only conditionally frozen/export/package gates.
- Resume trigger commit `353a5163da7bfe4421073f2bd2239eb90188f2d6`
  launched run `33825895948`. It verified and adopted only the explicitly
  named v2 checkpoint, serialized the training result, evaluated Matrix/P0.5
  dev at threshold zero, classified the dev residuals and failed the unchanged
  development gate. Frozen/adversarial data remained unread; ONNX, INT8,
  parity and packaging did not start. Model state SHA-256 is
  `b91793c8ae742b889085c9a531248944351b567365532791bdb549c5104ea523`;
  parameter count is 58,599,411 (58,412,544 encoder; 186,867 heads).
- Run `33825895948` dev metrics at threshold zero: Matrix claim-count exact
  `1.0`, exact claim set `0.574074`, field exact `0.954275`, span F1
  `0.928985`, entity F1 `0.981110`, valid coverage `1.0`, selective exact
  `0.631687`, ownership corruption `30`, invented World Truth `0`; Matrix
  worst-language exact-set/field-exact are `0.507937` / `0.945130`. P0.5
  claim-count exact is `0.983333`, exact claim set `0.3`, field exact
  `0.899471`, span F1 `0.956095`, entity F1 `0.951501`, valid coverage
  `0.940476`, selective exact `0.531646`, ownership corruption `4`, invented
  World Truth `0`; P0.5 worst-language exact-set/field-exact are `0.25` /
  `0.892857`. No one of the 189 dev-only threshold points passes.
- Dev-only residual evidence shows underlearned rare classes rather than a
  calibratable threshold defect: Matrix includes 126 NEGATIVE-to-POSITIVE
  polarity errors and 126 missing negation spans, 72 temporal-relation errors,
  30 subject/owner referent errors and 96 missing temporal spans; P0.5 includes
  REQUEST-to-ASSERT and CORRECT-to-ASSERT errors plus rare predicate/referent
  failures. The corresponding train labels are strongly imbalanced (for
  example Matrix ASSERT 3060 versus HYPOTHESIS 267 and QUESTION 183; only
  three PAST claims; P0.5 has six REQUEST and three CORRECT claims before
  repetition).
- Run `33825895948` artifacts: report id `9920008253`, 321,019 bytes, digest
  `sha256:e86efb9f8bd78ef805135aafc5fb269ac28dd8ce0f0c69e659d77ba66df9cce3`;
  bundle id `9920012353`, 217,600,162 bytes, digest
  `sha256:a52bc3247f45c6f82fa42c077a4835a8df1c1907a2e0b45ab774da2a3102dee1`;
  resume id `9920022732`, 646,923,260 bytes, digest
  `sha256:8c4ecf068aa976341c82b22c14d2b8a0cf2cce5b26951a7167a5cf82a06adafe`.
- Current uncommitted remediation is derived only from that dev evidence:
  inverse-square-root class-balanced token/sequence loss capped at 8, Matrix
  maximum epochs 8, P0.5 train repeat 16, and dev residual classification
  before threshold selection so failed runs retain their error analysis.
  Dataset v2, architecture, seed, all gates and production/runtime remain
  unchanged. A distinct `student-4-v2-retrain.trigger` always starts fresh;
  checkpoint adoption remains possible only via an explicit workflow-dispatch
  run id. Local regression/property/integration suite is 74/74 green. Exact
  next action: commit this dev-only remediation, require P0/probe CI green,
  then launch one fresh audited Student-4-v2 run.
- Dev-only remediation checkpoint
  `909dd2f1a786bfe2eac61c2d1921b4ebd27679c5` passed both required push
  guards: P0 run `33826601373` success and candidate-probe run `33826601401`
  success. No training was launched by that commit. Exact next action is the
  one-time `student-4-v2-retrain.trigger` commit; it must start with an empty
  training directory, rerun the dataset audit before training, and keep frozen
  sealed unless the unchanged dev gates pass.
- Fresh rebalanced run `33826815562`, launched by
  `f04b069d8c989d7894d6028367987c2baf79bbfb`, completed training and failed
  only at unchanged dev threshold selection. It stopped after Matrix epoch 6
  through patience 2; best head-average was `0.9590511996891526` at epoch 4.
  Frozen/adversarial remained unread (`frozenDataRead=false`, train/dev only),
  and ONNX/INT8/parity/package did not start. Model state SHA-256:
  `a4897d74970c6f16db4025d6df2b54e34dd34fbe8976b526976d9fd04e75b20f`.
- Run `33826815562` threshold-zero dev: Matrix claim-count exact `0.997354`,
  exact-set `0.560847`, claim exact `0.619342`, field exact `0.970736`, span F1
  `0.927804`, entity F1 `0.982728`, coverage `1.0`, ownership corruption `0`,
  invented World Truth `0`; worst language is Italian exact-set `0.349206`
  (EN `0.785714`, ES `0.547619`). P0.5 exact-set improved to `0.483333`,
  claim exact `0.630952`, field exact `0.916667`, span F1 `0.968394`, entity
  F1 `0.972851`, ownership corruption `2`, World Truth `0`; worst language is
  Spanish exact-set `0.35` (IT `0.5`, EN `0.6`). Best combined exact-set is
  `0.555147` at threshold `0.86332758` with ownership corruption `2`; the best
  zero-ownership point reaches only exact-set `0.471814` and coverage
  `0.640152`. Therefore no dev threshold passes.
- Preserved run `33826815562` artifacts: report id `9922954442`, 353,528 bytes,
  digest `sha256:f28f3d8e0ac33dd7fb84b22f382fc4e7024469f544502456fdd1ea4bae2892e9`;
  bundle id `9922957297`, 217,601,926 bytes, digest
  `sha256:28af0eb9300f70f9f6f1f8846aadacb87f57a5ad300f6d87570386185714a6ef`;
  resume id `9922965503`, 646,873,821 bytes, digest
  `sha256:6bb7f268a8c9a2931261dddd2f9566aef16eb3fe71a8684a798c2eb33a4cc02f`.
- Dev-only residual analysis classifies 363 failed observations: semantic
  classification 267, span decoding 383 error instances, authority/referent
  52, entity resolution 40 and claim segmentation 3. Matrix still misses all
  126 held-out negative-preference polarities and their semantic-scope spans;
  temporal spans and consent/target transfer also remain systematic. This
  proves weighting/extra epochs alone are insufficient and justifies new
  train-only lexical diversity; no frozen prediction informed this decision.
- Current pre-training dataset correction adds 105 project-authored,
  split-distinct examples (35 per IT/EN/ES) for negative semantic scope,
  explicit future spans, consent/OBSERVER, REQUEST/CORRECT and bound
  third-party referents. Matrix v2 train becomes 2,775 observations / 3,615
  claims, balanced 925/language, SHA-256
  `5118d37ce2ab19d5be171f757f448698085e3c222a4a627f9838329836185820`.
  Matrix dev/test hashes remain `704e809f...` / `458f79ec...`; all P0.5 hashes
  remain unchanged. Mapping SHA-256 is
  `c53ffb13f5b0ebdc15892a9b18890f3caa3c16347600c679c2ecfeab321fcbbc`,
  with 1,322 corrections, 426 leakage drops and 129 train additions. Clean
  audit is PASS: zero contradictions, invalid spans, convention failures,
  authority failures, exact leakage or >=0.97 semantic-template leakage;
  frozen predictions read=false. Focused dataset tests are 6/6 green. Exact
  next action: commit the augmentation, run the full repository CI, then start
  a fresh v2 run only after every pre-training audit is green.

- First trained multi-task teacher (`Gate 02`) completed successfully in
  GitHub Actions run `33786677296` at `2026-09-03T20:26:35Z`; every setup,
  training and artifact step is green. It must not be rerun.
- Current gate: authorized `matrix.nlu.dataset.v2` migration and pre-training
  audit closure. Supervisor approved Option A: semantic negation scope, null
  span for implicit first-person subject, explicit temporal expressions always
  spanned, v1 immutability and a fresh isolated `student-4-v2` variant. The
  strict end-to-end TypedClaim gate correctly
  rejected the immutable teacher artifact. Post-gate run
  `33802563626` completed `failure` at dev threshold selection and did not
  consume frozen data or start ONNX export.
- Preserved post-gate artifact id `9911772359`, archive digest
  `sha256:2340e9b07f3d7e72bffb23b33f56e64e1af3dcf17a19a944bf80d241dad44e13`,
  246,077 bytes. It contains exact Matrix/P0.5 dev metrics, raw predictions,
  error JSONL, the 253-point threshold curve, logs and failure summary.
- Matrix dev at threshold 0.5: claim-count exact `0.920635`, exact claim set
  `0.105820`, field exact `0.900549`, span F1 `0.893356`, entity F1
  `0.931615`, valid coverage `0.938272`, selective exact accuracy `0.131579`,
  World Truth updates `0`; overall ownership corruption `50`.
- P0.5 dev at threshold 0.5: claim-count exact `1.0`, exact claim set
  `0.130952`, field exact `0.929012`, span F1 `0.948318`, entity F1
  `0.957111`, valid coverage `0.916667`, selective exact accuracy `0.323232`,
  ownership corruption `0`, World Truth updates `0`.
- No threshold passes: best combined dev selective exact accuracy is
  `0.533333` at threshold `0.992749...` and best exact claim set is
  `0.108333` at threshold `0.0`; this is a model/decoder quality failure, not
  a calibration-only failure.
- First causal classification from dev evidence only: (1) every correctly
  detected entity is reported without the gold `referent`, so exact entity
  equality is structurally impossible in the present decoder; (2) per-language
  ownership corruption is falsely reported as zero because the evaluator only
  increments the aggregate bucket; (3) actual learned residuals remain in
  predicate, polarity/negation scope, temporal relation, object span and
  pronominal/known-entity subject binding. The first two are deterministic
  implementation defects; the latter families require learned-data/objective
  analysis. No linguistic regex repair is authorized.
- Deterministic decoder/evaluator repair
  `6ff5c3959407f0304e725fadbb0f3a37376524ec`: predicted entity spans now gain
  categorical referents only from already-learned semantic-role overlap or an
  exact supplied-context binding; locations remain `LOCATION` and unresolved
  people remain explicitly `UNKNOWN`. No capitalization, city/person list or
  linguistic regex was added. Per-language ownership corruption is now counted
  with the same zero-tolerance semantics as the aggregate. Full local suite is
  48/48 green and all automation/Matrix-NLU Python byte-compiles.
- Train-only causal data correction
  `f74679738af501e9ca823d3c4745e7a399ef0fce`: each generated semantic family
  now has five independently authored train paraphrases per language and the
  train multi-claim generator rotates four coordination/discourse-marker forms
  per language. Added 108 balanced IT/EN/ES train-only observations for the
  existing `RECENT_ENTITY` contract, which previously had zero train examples
  despite nine P0.5 dev claims. P0.5 train repeat changed from 3 to 8 to address
  dev-observed rare-label underrepresentation (`CORRECT`, `REQUEST`,
  `presence.reported`, hypotheses and local negation scope). This is learned
  supervision only; no runtime regex or surface rule was added.
- New Matrix train: 2,991 records / 3,831 claims, SHA-256
  `803a565e9bb7e88de269b1002603ea86a4bbb832c06183d537525596c4575b6d`,
  balanced at 997 observations per language. The pre-existing Matrix dev hash
  remains exactly `aa19e414...` and frozen test remains exactly `8f1b267f...`;
  P0.5 train/dev/test hashes remain `8426018b...` / `b48753dc...` /
  `5ef8f8bf...`. A regression now fails if either generated dev or frozen test
  changes. Full local suite: 50/50 green; byte-compilation, one-click dry-run
  and all workflow YAML parsing are green.
- One-time student launch commit
  `6d8d463f76a3ff7de292b947a5854d308d8a9c3c`; strict one-click run
  `33804574916` completed `failure` only at the strict dev threshold gate on
  the exact augmented dataset/code lineage. Variant is `student-4`; its output
  and checkpoint paths are isolated from teacher evidence. Training itself is
  `SUCCESS`: 6,525.49 s, model state SHA-256
  `5cdec7d486540253c6f4cdd7cdd0c4b56cc1e04ab7a05e7c769366f6d041b0f8`,
  58,599,411 total parameters (58,412,544 encoder; 186,867 heads), four
  encoder layers. Best dev head-average is `0.9638816146` at Matrix epoch 2;
  epochs 3–4 did not improve the selection score. MASSIVE auxiliary dev
  head-average is `0.6400880031`.
- Student DEV end-to-end at threshold 0.0: Matrix claim-count `1.0`, exact-set
  `0.6402116402`, field exact `0.9700502972`, span F1 `0.9579878556`, entity F1
  `0.9811095645`, coverage `0.9897119342`, ownership corruption `0`, invented
  World Truth `0`; worst-language exact-set is Italian `0.4682539683`.
  P0.5 claim-count `1.0`, exact-set `0.3571428571`, field exact
  `0.9187242798`, span F1 `0.9386692696`, entity F1 `0.9801324503`, coverage
  `0.9074074074`, ownership corruption `0`, invented World Truth `0`.
  No dev threshold passes; frozen end-to-end/ONNX/package were therefore not
  executed.
- Preserved one-click artifact id `9915949750`, 1,083,583,721 bytes, archive
  digest `sha256:dd60f8dd8df6e2bd2bee0f5d53c1fcc15e991241682043fdf143d79953dac5d4`.
  It contains the resumable checkpoint, model, raw predictions and complete
  logs, but exceeds the 512 MiB connector download ceiling. Operational fix
  `e5f9ea68cf4aa3c646dffe0023317731dedb62ee` launches evidence-extraction run
  `33814528873` to split the immutable source artifact into a small report and
  a sub-512-MiB model bundle without retraining. That extraction run completed
  successfully without training. Report artifact id `9916044936` is 257,577
  bytes with archive digest
  `sha256:9b51700e14b9ca2044eba8ba23820609132b3f63b3ada174ce413b2aa4ff9e75`;
  model-bundle artifact id `9916049420` is 217,601,947 bytes with archive
  digest
  `sha256:27c35bb23231e279da7bc27c574e841d4f857fffb557cf0fcba2428609f5e61c`.
  The report archive has been downloaded, checksum-verified and extracted
  locally. The model bundle was resumed from its existing 168 MiB partial
  transfer (not restarted), archive-checksum verified, extracted, and all eight
  internal `SHA256SUMS` entries pass. The serialized model state is 234,435,022
  bytes and exactly matches SHA-256 `5cdec7d...`. Its 58,599,411 parameters imply
  234,397,644 theoretical FP32 parameter bytes (223.54 MiB) and a 58,599,411-byte
  INT8 lower bound (55.88 MiB), inside the canonical 45–60 MiB review band but
  not yet an actual exported ONNX/INT8 measurement. The original large artifact
  remains the resumable checkpoint source for Actions.
- Student DEV error analysis is complete and used no frozen output for repair
  choices. Matrix has 272 error rows: object span 172, polarity 84, temporal
  relation 48, predicate 40, entity 40, source span 36, temporal span 30,
  target 30 and claim kind 30; Italian is the worst language with 134 rows.
  P0.5 has 54 error rows: predicate 22, dialogue act 15, object 15, negation
  scope 12, entity 12, subject/owner 10 each. The dominant residuals expose a
  supervision-contract inconsistency: generated Matrix negatives label only a
  cue token while P0.5 labels the complete negated clause, and at least one
  temporal expression is semantically predicted but absent from its gold span.
  No regex/decoder workaround is justified from this evidence.
- Train/dev contract audit commit
  `0f4dc7afe9daf09a6a0d53b577738a69a4f810d8` introduced a diagnostic-only,
  split-enforcing audit; commit `00101513a4ec1df8b825226451ba93d197fab94c`
  proved seven exact text+context inputs with incompatible gold targets (IT 2,
  EN 3, ES 2). They include `non amo i locali affollati`, `I do not like rain`
  and `No me gusta la lluvia`, plus four name declarations whose implicit
  speaker subject is alternately null or the name/object span. A deterministic
  model cannot satisfy both targets. Two broader negation-scope convention
  conflicts are also present; semantic-span containment failures are zero.
  Machine-readable evidence SHA-256 is
  `8a1fbb2bb6a07952540104f32327d4f729003683cc5cc637a6e355b387f062fb`.
- Pipeline safety commit `c5640655ff1febee043335406a85fb338b7a8b42`
  runs that audit after deterministic dataset generation and before MASSIVE or
  training, preserves the report, and stops on conflicts. The one-click CI now
  uploads bounded report, deployable bundle and isolated resume artifacts
  instead of a single >1 GiB archive. It does not touch the training trigger.
- Formal blocker and bounded options are documented in
  `docs/DECISION_REQUIRED_MATRIX_NLU_ANNOTATION_CONTRACT.md` at
  `846748547f892b483effb85b8cf71cb62f669f6e`. Recommended resolution is a
  versioned v2 correction retaining the current heads: `negation` means semantic
  scope, implicit first-person subject span is null, explicit temporal-span
  policy is made consistent, and every v1 file/hash/result remains immutable.
- Split-isolation regression commit
  `4d67aaf921bfa9cfa0e88cc274ba118f384ecd8d`: train surfaces must be disjoint
  from both dev and frozen generated surfaces, every dev label must have train
  supervision, and every semantic span must be contained in its claim source.
  Full local suite is 53/53 green. This test-only descendant does not alter or
  restart the active run; P0 CI for launch commit `6d8d463...` is green as run
  `33804575007`.
- P0 CI for continuity HEAD `c6b511076...` is green as run `33814617275`.
- The automatic `workflow_run` edge did not fire after the source workflow was
  renamed for one-click operation. Fix `16754f79e26caa003679ffb70b512f6226c13627`
  added a bounded explicit trigger; `ffdbb224059ad27b7b544aa988e4cc2665a4159d`
  records the immutable source run and started the post-gate without training.
- In parallel, commit `9027ff3...` added the end-to-end learned decoder and
  deterministic invariant validator without touching a training-trigger path.
- Automation checkpoint `732725fd94241e8523cb6692f1a05cfd4b8a1ee7`
  added/hardened `auto_train.py`, created `auto_test.py` and
  `run_pipeline.py`, and added failure-safe shared support. The one-click order
  is prepare/verify -> train/resume -> dev validation/threshold -> frozen
  Matrix+P0.5 -> FP32/INT8 ONNX frozen evaluation -> package/report. Critical
  failures preserve logs, checkpoints, candidate evidence and the prior
  last-good package. Teacher evidence and production package promotion are
  deliberately distinct.
- The same checkpoint added per-language/worst-language frozen gates, strict
  zero ownership/World Truth gates, residual taxonomy, exact dev-only threshold
  provenance, offline ONNX runtime evaluation over the complete frozen set,
  INT8 quality-delta checks and theoretical FP32/INT8 size evidence.
- CI checkpoint `a6818f971dc55ba2c5faf7f2eb3bb8d8e7d081f1`
  replaced the duplicated post-training shell sequence with the same strict
  `auto_test.py` entry point used locally. The workflow still consumes the
  immutable artifact from run `33786677296`, fails on critical dev/frozen/ONNX
  gates, and uploads status, logs and partial evidence with `if: always()`.
- Resumability checkpoint `4c237fef443e1bd07c6ba34d31fc63012657e8a4`
  makes the training automation variant-safe and observable: teacher and
  student use different output/checkpoint/status/log paths; `train.py` writes
  atomic batch/epoch progress; the configured dev-only early-stopping patience
  is now effective; and the CI definition is a single 1-click pipeline with an
  optional explicit checkpoint source. Expensive execution is manual or bound
  to the one-time `pipeline/student-4.trigger`, preventing training from being
  relaunched by ordinary source edits. No trigger file exists yet.
- Resume correctness fix `a841a67e7586d8ec50b8876d42329636042b4a4e`
  prevents a completed MASSIVE auxiliary stage from being replayed when a
  matrix-stage checkpoint is restored, treats early-stopped/completed stage
  checkpoints as terminal, and carries prior-stage history in new checkpoints.
  Resume-policy tests bring the local suite to 45/45 green.
- Split-integrity checkpoint `be3538a68e401727c2f56d77aedfda24c8b2e118`
  makes non-dev threshold input a hard error and packages a machine-readable
  split-separation record with exact dev/frozen SHA-256 values. Frozen data is
  evaluated only after the dev threshold gate and is never an optimizer or
  threshold-selection input. Local suite: 46/46 green.
- State-preservation fix `b7572c4c947fb771e6a87d1844ba0ec84f0ba60b`
  carries variant/output metadata into terminal training status, reports the
  correct teacher-versus-production promoted destination, and checks the
  correct variant-specific checkpoint on interruption/failure. The 46-test
  suite and byte compilation remain green.
- Execution-bounds fix `07119f939a54b9fc99361dd439dda9811b13a245`
  rejects seed/config drift, resolves checkpoint preservation against an
  explicitly supplied bundle, and gives the model-dependent post-training
  evaluator the same six-hour bound as the one-click job. Unit/byte/YAML checks
  remain green; no training trigger was touched.
- Current candidate configuration:
  - primary probe: `Geotrend/distilbert-base-en-es-it-cased`;
  - quality/size counterexample: `microsoft/Multilingual-MiniLM-L12-H384`;
  - compact size reference with English-only risk:
    `microsoft/xtremedistil-l6-h256-uncased`.
- Planned training strategy if the probe clears provenance/tokenization:
  exact-language 6-layer DistilmBERT as teacher/quality comparator; evaluate a
  4-layer student initialized from pretrained teacher layers and trained with
  supervised plus logit distillation for the mobile candidate. This is a plan,
  not yet a result or final selection.
- Planned data strategy: MASSIVE IT/EN/ES as licensed auxiliary
  request/intent/slot evidence; Matrix-generated/curated typed claims;
  adversarial/noisy adult-only coverage; real regressions. MASSIVE labels must
  not silently become Matrix predicates.

## Tests and CI state

- Current local software/property/regression/integration suite: 60/60 green.
  All `auto_*.py`, `run_pipeline.py` and `matrix_nlu/*.py` byte-compile; all five
  workflow YAML files parse; student-4 one-click dry-run is green. The contract
  gate intentionally exits `2` after preserving its report because the current
  v1 data contains critical conflicts.
- Candidate Probe runs `33815343446`, `33815504206` and `33815613927` are
  green for the audit/pipeline commits. P0 runs `33815343409`, `33815504380`,
  `33815613991`, `33815709498` and final handoff run `33815787611` are green.
  Run `33815787611` completed every unit, clean Italian trainer, unified A/B,
  expanded P0.5 baseline, Android footprint/offline and artifact-upload step.

- Green local checks at current implementation (`732725fd...`):
  `python -m unittest discover -s matrix_nlu -p 'test_*.py' -v` (42/42),
  full `python -m py_compile auto_train.py auto_test.py run_pipeline.py
  matrix_nlu/*.py`, and `python run_pipeline.py --dry-run --student-layers 4`.
  The suite covers unit, dataset/property, regression, integration, authority,
  ownership, World Truth, claim count, abstention, gate failure and atomic
  promotion control flow. This is software evidence only; model quality remains
  pending the active run.
- CI for `5b9bb591...`: no associated workflow run; do not report PASS.
- CI probe run `33784078023` on `d2a388b...`: red before job creation because
  the six newly uploaded files contained literal serialization placeholders
  (`$f0` ... `$f5`) rather than their local contents. This is a repository
  transfer defect, not a model/probe result. The normal P0 workflow run
  `33784079607` is in progress on the same HEAD.
- Repair commit `19cc3542d6b0d65dd7332f94dd7e6bfed1c36c20` restored and
  remotely verified all six probe source files.
- CI probe run `33784241590` on `19cc3542...`: red at the candidate-tokenizer
  step after dependency install and 3/3 unit tests passed. The exact cause is
  missing `sentencepiece`, required to instantiate the MiniLM/XLM-R slow
  tokenizer for fast-tokenizer conversion. This is a dependency defect, not a
  candidate quality/provenance result. Fix: pin `sentencepiece==0.2.0`.
- Dependency commit `0acef2f46b8827fa15bb033bddae9be10f9f9d1d`:
  SentencePiece installed; normal P0 CI run `33784416259` green.
- Probe run `33784416207` on `0acef2f...`: 3/3 probe tests green, then
  MiniLM/XLM-R tokenizer conversion failed because `protobuf` was missing.
  Exact causal fix pending: pin `protobuf==5.28.3`. The probe now preserves
  partial per-candidate results and uploads artifacts even if one reference
  candidate fails.
- Matrix dataset builder locally verified: 9/9 combined Python tests green.
  Train: 2,883 records / 3,723 claims, SHA-256
  `6f42718a0b25f32e8c3711148c72ac2ab6415bb57ca7161eb9ac6a8a589b8045`.
  Dev: 756 / 972, SHA-256
  `aa19e414a5d5dd1bc3ec9c1e257b8224b568a2a7460a92f31875ce3741003177`.
  Frozen test: 1,482 / 1,914, SHA-256
  `8f1b267fb9f1b76d0f304cd26d88dfcef82fd6434f5ea182985a164960effba2`.
  All are balanced IT/EN/ES; World Truth expectations are zero.
- Candidate/model probe CI `33784868028` on `c6875b9e...`: green. Artifact
  id `9905024154`, archive SHA-256
  `7714de59bc05f227eebbdde351fa739c61df82f0ae7e0a3c1b6a904f0198d7d0`;
  probe JSON SHA-256
  `565c6ae9fc946a10daa77c08c3b2205f4f94a0756c7409758c4b1307a414e382`.
  CI reproduced all three dataset JSONL hashes exactly.
- Selected lab-training encoder:
  `Geotrend/distilbert-base-en-es-it-cased` revision
  `36de33ec579e47f6c4e10d982d0b93871267c3e6`, Apache-2.0, 6x768,
  vocabulary 38,628, weights 292,888,832 bytes, estimated dynamic INT8
  73,222,208 bytes, zero unknown probe tokens in IT/EN/ES.
- Multilingual MiniLM revision `6e8c1ec6...`: 470,657,952-byte weights,
  estimated INT8 117,664,488 bytes; quality reference, not mobile candidate.
- XtremeDistil h256 revision `8d58f0e6...`: 51,044,621-byte weights,
  estimated INT8 12,761,155 bytes, but declared language is English; size
  reference only.
- Encoder/model pinning commit:
  `d8ef350ad723156cd6b8fd64509a64ae7575107c`; it also preserves
  `artifacts/matrix-nlu/probes/candidate-probe-c6875b9.json`.
- Matrix-NLU workflow run `33785421435` on `d8ef350...`: encoder-probe job
  green, MASSIVE job red before download. Cause: unit test invoked as
  `python -m unittest matrix_nlu/test_probe_massive.py` while its direct module
  import expects `matrix_nlu` on `sys.path`. Fix is the same discovery mode
  already used by the green combined test job. This is not a data/provenance
  result.
- P0.5 adapter locally verified within 13/13 combined tests. It emits train
  87 records/105 claims SHA `8426018b...`, dev 84/108 SHA `b48753dc...`, frozen
  test 93/111 SHA `5ef8f8bf...`; the frozen test is never merged into training.
- P0.5 adapter/MASSIVE invocation fix commit:
  `ac723626bd36dbfdc03aa651d9728fc16292455b`.
- Matrix-NLU probe run `33785721399` on `ac723626...`: all jobs green.
  MASSIVE 1.0 source archive is 39,500,415 bytes, SHA-256
  `7df623fd2d300a4d235d6ee5bd396c9a28258d3a0ccb29abdb054506eba153f8`;
  archive license SHA-256
  `c2e6ea015269147de02117ebdd91f30ef09831251f5345fa8365273b1db1d435`.
  Each of IT/EN/ES has 11,514 train, 2,033 dev and 2,974 test rows; 60
  intents, 18 scenarios and 55 observed slot types. Artifact id `9905327516`,
  artifact SHA-256
  `0cabeed0e47c548c9f7f11bf4fe65de297514221cbf6c9fa1870e334188ff30d`.
  This was the intentional unpinned observation run; a matching pinned rerun is
  still required.
- Pinned provenance CI `33785912634` on `de7cea4...`: all jobs green;
  `hashPinned=true`, `hashMatches=true`. MASSIVE artifact id `9905400586`,
  artifact SHA-256
  `d977b5cc52602a1e26db2079a9ec29918f5eea9ad750b411513c16cceb893c10`,
  manifest SHA-256
  `38ad629ae5469466f72eeee8f00675172a34dad03bc98589462c352727d2b4b1`.
  External-data provenance is `PASS`.
- Current training software local checks: 19/19 unit tests green and every
  Python source byte-compiles. Torch/Transformers execution is intentionally a
  CI gate because those pinned packages are not present in the Work container.
- Decoder/invariant checkpoint `9027ff3f177a6fcde57e5324e9ad27c7c15de4d4`:
  full local suite 23/23 green and all `matrix_nlu/*.py` byte-compile. Covered:
  learned claim-boundary grouping, context-only known-entity binding, rejection
  of an unbound third party, low-confidence abstention with provenance, no
  World Truth mutation. This commit did not retrigger the active teacher run.
- End-to-end benchmark checkpoint
  `39fa4127fcc99a770f52ff86a84e11f44b60bd4f`: full local suite 26/26 green;
  `matrix_nlu/evaluate_e2e.py` reports exact claim count, typed fields, character
  span/entity F1, per-language quality, abstention/rejection, ownership
  corruption and World Truth updates, with complete JSONL error evidence. Its
  CLI requires an explicit `dev` or `test` split so dev-led selection remains
  separate from the one-time frozen-test run.
- Raw-evidence checkpoint `44db7995ce28236d79e4552d17934b1164cdb6ac`:
  every benchmark prediction now retains learned raw labels/spans/confidence,
  post-validator Typed Claims and boundary confidence computed only over real
  non-special tokens. The evaluator writes a prediction JSONL beside metrics
  and error JSONL. Local suite remains 26/26 green and byte-compilation green.
- Auditable-abstention checkpoint
  `ffc2de565c1d04968b932ab6f1eb5a05b4236c57`: low-confidence but
  context-valid output is now explicitly `ABSTAINED_LOW_CONFIDENCE`, never a
  semantically `VALID` claim; it still retains raw evidence and provenance and
  remains non-admissible. Per-head sequence/token confidences are recorded.
  The evaluator now reports ten-bin ECE, Brier score and mean confidence overall
  and per language. Full local suite 26/26 and byte-compilation remain green.
- Dev-only calibration checkpoint
  `2c85ca19b5d1daefd11b44a939a2186893902883`: threshold selection accepts
  only datasets declared `split=dev`, maximizes valid coverage subject to
  selective exact accuracy >= 0.99 and zero ownership/World Truth corruption,
  and cannot PASS through zero coverage. Full local suite 29/29 and
  byte-compilation are green. No frozen-test evidence has been consumed.
- Causal threshold-gate correction
  `2f6a603cce44b5d062731f1f99891df8fe640a19`: selection also requires claim
  count exact >= 0.99, preventing extra/missing claims from being hidden by a
  high paired-claim selective score. Neighboring regression added; full local
  suite 30/30 and byte-compilation are green.
- Deterministic validator property checkpoint
  `b161d5dd1553207de7465b7bc1eb37606a002f1b`: all combinations of supported
  subject/owner/perspective referent classes at low confidence are checked to
  remain non-valid, non-admissible and unable to promote World Truth; malformed
  source-span boundary classes are rejected. Full local suite 32/32 and
  byte-compilation are green.
- Maximum-quality metric checkpoint
  `781373ab899e5854401ceba0f1c7e1b31efa1fbd`: end-to-end output now includes
  exact claim set, per-field accuracy, per-span F1, explicit predicate,
  negation and temporal metrics, and worst-language scores. Dev threshold PASS
  additionally requires exact claim set >= 0.98 and valid coverage >= 0.98;
  selective accuracy or abstention cannot conceal a near-empty system. Full
  local suite remains 32/32 and byte-compilation green.
- ONNX-export software checkpoint
  `2e965e6802cfaa37504f6c9586032c05396a320a`: fixed-shape export uses the
  bundle's declared max length, stable named outputs for every learned head,
  opset 17 FP32 plus per-channel dynamic INT8, source/artifact SHA-256 and byte
  counts, native-vs-ORT argmax/logit parity on IT/EN/ES probes, and measured
  median/p95/max latency. The corrected p95 uses nearest-rank. Full local suite
  34/34 and byte-compilation are green. No ONNX export has yet executed, so
  export/parity/size/latency gates remain unverified.
- Post-training automation checkpoint
  `ea1655004d4fea31d8d911ab45d3c27e6f21dff3`: when the active training run
  completes successfully, `.github/workflows/matrix-nlu-post-train.yml`
  downloads its immutable evidence, reproduces datasets and 34-test software
  gate, produces Matrix/P0.5 dev predictions, selects threshold from dev only,
  and runs frozen Matrix/P0.5 plus FP32/INT8 export only after that dev gate.
  Exact source-run and file checksums are uploaded. Workflow YAML parses green
  locally. It does not trigger or duplicate teacher training.
- Failure-evidence correction
  `c32e4127861d1929af622017fe2189a6c6801fb3`: the post-training workflow now
  records source-run/resource/checksum evidence under `if: always()`, including
  when the dev threshold gate fails, instead of losing the causal handoff.
  YAML parse and the 34-test local suite are green.
- First training configuration: teacher Geotrend 6x768 revision `36de33ec...`;
  seed 810923; max length 64; MASSIVE 3,000/600/1,000 rows per language,
  one auxiliary epoch; Matrix four epochs; batch 16; gradient accumulation 2;
  AdamW LR 3e-5, weight decay .01, warmup .1; P0.5 train repeat 3; CPU 4
  threads; checkpoint every epoch; resume auto; frozen tests once after
  dev-selected checkpoint.
- Training implementation commit:
  `37ef11c99785fb0fd56e99267f33e71d4c9e15e6`.
- Teacher training run `33786677296`: PASS. Model state SHA-256
  `7a68f41545fd531176e1a3bbe2b06920e043ed554fc85437c9be08d16670973a`;
  72,775,155 parameters; 291,150,286-byte serialized state;
  best dev head-average `0.9511465670`. Epoch selection scores:
  MASSIVE `0.6702257722`; Matrix `0.9405758642`, `0.9459914824`,
  `0.9496920553`, `0.9511465670`.
- Teacher evidence artifact id `9911479813`, archive digest
  `sha256:08c0c3ccc6dfe2a7cd492b998c5556edceb190acc8eda84ed42ac5bb3dab7901`,
  270,145,913 bytes. Resume artifact id `9911500930`, archive digest
  `sha256:733895971eeb98bf9d333d890663c2fa6f956d6ed8fba61aa2ba2375037bdc22`,
  855,149,758 bytes. Both are retained for 30 days by the source workflow.
- Head-level frozen evidence was emitted once by the original trainer:
  Matrix macro-head `0.9259638152`, P0.5 `0.9502517095`, MASSIVE after
  Matrix fine-tuning `0.1296912960`. These are diagnostic results, not
  end-to-end PASS and not tuning inputs. Dev already exposes systematic
  predicate/temporal/polarity/dialogue-act gaps; the post-gate will provide
  exact TypedClaim errors without tuning on frozen.
- End-to-end frozen quality, ONNX parity/INT8 and desktop latency remain
  deliberately unexecuted because both teacher run `33802563626` and student
  run `33804574916` failed the dev gate.
  Android physical PSS/latency remains a later gate.

## Open errors, failed paths and blockers

- `RESOLVED_BY_SUPERVISOR / MIGRATION_IN_PROGRESS`: dataset v1 contains
  seven exact input/context collisions with different span targets and mixed
  negation-scope conventions. The supervisor authorized Option A and explicit
  dataset v2. Preserve all v1 assets/hashes/results, migrate through versioned
  outputs and mapping evidence, and do not launch `student-4-v2` until every v2
  audit is green. Do not lower exact gates, add regex, or encode benchmark
  provenance into runtime output.

- `DECISION_REQUIRED / NON-BLOCKING FOR ACTIVE BASELINE`: the maximum benchmark
  now requires third-party reports and nested belief attribution. The current
  learned contract has one `subject` span plus categorical
  subject/owner/perspective referents. `bind(KNOWN_ENTITY)` can therefore bind
  owner/perspective only through the subject mention. It cannot safely represent
  and bind two distinct named roles in input such as a known reporter plus a
  different known claim subject. Choosing the first PERSON entity would be an
  unsafe heuristic; adding role-specific spans, an entity-index pointer head or
  explicitly limiting nesting is an architecture/contract choice for the
  supervisor. The active teacher is still a valid first baseline and must
  continue; it simply cannot close this newly explicit maximum-benchmark family.
- The Hugging Face primary model revision and metadata are verified and pinned;
  no open encoder-provenance issue remains.
- Shell access to Hugging Face timed out in the Work container. Do not repeat
  it; use GitHub Actions network access and preserve the resulting artifact.
- Failed repository-transfer method: constructing a `jq` object by interpolating
  shell variables through a JSON string produced literal `$fN` values. Do not
  repeat it. The repair reads each file as base64, decodes it in the tool
  process and verifies the remote blobs after commit.
- Probe failure `33784241590`: do not retry unchanged; SentencePiece was added
  for XLM-R-family tokenizers in `0acef2f...`.
- Probe failure `33784416207`: do not retry unchanged; protobuf was pinned in
  `c6875b9e...` after XLMRobertaConverter required it.
- MASSIVE job in run `33785421435`: do not retry unchanged; use unittest
  discovery with `-s matrix_nlu`, otherwise the test module import fails before
  the archive is downloaded.
- `Geotrend/distilbert-base-en-fr-es-pt-it-cased` was initially considered but
  superseded by the exact-language `en-es-it` checkpoint. Do not train the
  5-language checkpoint unless the exact checkpoint fails a documented gate.
- XtremeDistil h256 is tagged English and reports English GLUE/SQuAD evidence;
  compact size alone cannot qualify it as the multilingual production encoder.
- Multilingual MiniLM has a large XLM-R embedding table and measured estimated
  INT8 weights of about 117.7 MB, above the preliminary 100 MB no-go band. Do
  not train it as the mobile candidate absent exceptional new evidence.
- Do not disable or bypass frozen test partitions; do not use any test result to
  train or choose a variant.
- Do not add linguistic regex/rules to the invariant validator.
- The teacher step in run `33786677296` is complete; do not rerun it. Its dev
  score is below the near-perfect target, so it is teacher/baseline evidence
  rather than a production candidate.
- `MatrixNluRuntime` currently reconstructs the encoder through the pinned Hub
  identifier before loading its state dict. This is acceptable only for the lab
  evaluator and is an open offline-export defect: the ONNX/runtime bundle must
  carry all model/tokenizer/config assets and must prove zero network access.
- Early stopping is implemented for subsequent runs by `4c237fef...`; it was
  not present in immutable teacher run `33786677296`, so do not retroactively
  claim it was applied there.

## Consolidation state

- Probe files were initially malformed in `6bf5492...` and were restored in
  `19cc3542...`:
  `.github/workflows/matrix-nlu-probe.yml`,
  `docs/MATRIX_NLU_MODEL_DATA_PLAN.md`, `matrix_nlu/candidates.json`,
  `matrix_nlu/probe_candidates.py`, `matrix_nlu/requirements-probe.txt`,
  `matrix_nlu/test_probe_candidates.py`.
- Consolidated dataset commit: `c6875b9e492cd0827ada0bc27c9471dcd4454a21`.
- Consolidated model pin/MASSIVE probe commit:
  `d8ef350ad723156cd6b8fd64509a64ae7575107c`.
- Consolidated P0.5 adapter/MASSIVE test-path commit:
  `ac723626bd36dbfdc03aa651d9728fc16292455b`.
- Consolidated MASSIVE hash/provenance commit:
  `de7cea4376d9a2bb7886e6ad6c6c10878541012f`.
- Consolidated training implementation:
  `37ef11c99785fb0fd56e99267f33e71d4c9e15e6`.
- Hardware blueprint commit, concurrently added and preserved:
  `21e1de86fc0ecf8ce86d59b71ab89e2bccc827ea`.
- Maximum-depth validation supplement, concurrently added and preserved:
  `968953a9b6dade4d039577f989f31292d959d1f8`.
- Senior supervisor execution plan, concurrently added and preserved:
  `16d53e55bdc419717ddda717e7fc00aae5690192`.
- Python memory blueprint (design only), concurrently added and preserved:
  `4ef989f2a0fc0a0f246ef4e03f186b600cdb8e9a`.
- Automated training/testing policy, concurrently added and preserved:
  `6e6a0c473ef929035d188005776e5a83355887ca`.
- One-command auto-training implementation, concurrently added and preserved:
  `3f9cfa1b8e60db875cdbd8fc405f94e0f81f6b36` (not executed).
- Strict one-click verification/package pipeline and isolated teacher/student
  resume outputs: `732725fd94241e8523cb6692f1a05cfd4b8a1ee7`.
- CI adoption of the strict post-training entry point:
  `a6818f971dc55ba2c5faf7f2eb3bb8d8e7d081f1`.
- Variant-safe resume/progress and one-click CI definition:
  `4c237fef443e1bd07c6ba34d31fc63012657e8a4`.
- Completed-stage resume idempotence:
  `a841a67e7586d8ec50b8876d42329636042b4a4e`.
- Auditable dev/frozen separation:
  `be3538a68e401727c2f56d77aedfda24c8b2e118`.
- Variant-specific terminal state/report correction:
  `b7572c4c947fb771e6a87d1844ba0ec84f0ba60b`.
- Immutable seed/bundle/timeout bounds:
  `07119f939a54b9fc99361dd439dda9811b13a245`.
- Explicit immutable post-gate recovery:
  `16754f79e26caa003679ffb70b512f6226c13627`,
  `ffdbb224059ad27b7b544aa988e4cc2665a4159d`.
- Consolidated learned decoder/invariant validator:
  `9027ff3f177a6fcde57e5324e9ad27c7c15de4d4`.
- Consolidated end-to-end Typed Claim evaluator:
  `39fa4127fcc99a770f52ff86a84e11f44b60bd4f`.
- Consolidated raw prediction evidence and corrected boundary-confidence
  accounting: `44db7995ce28236d79e4552d17934b1164cdb6ac`.
- Consolidated explicit abstention state, per-head confidence diagnostics and
  calibration metrics: `ffc2de565c1d04968b932ab6f1eb5a05b4236c57`.
- Consolidated dev-only threshold selection gate:
  `2c85ca19b5d1daefd11b44a939a2186893902883`.
- Claim-count false-PASS correction:
  `2f6a603cce44b5d062731f1f99891df8fe640a19`.
- Deterministic authority/source-span property regressions:
  `b161d5dd1553207de7465b7bc1eb37606a002f1b`.
- Maximum-quality metrics and nontrivial coverage/claim-set gate:
  `781373ab899e5854401ceba0f1c7e1b31efa1fbd`.
- Audited ONNX FP32/INT8 export implementation:
  `2e965e6802cfaa37504f6c9586032c05396a320a`.
- Automated dev -> threshold -> frozen -> ONNX gate:
  `ea1655004d4fea31d8d911ab45d3c27e6f21dff3`.
- Failed-gate evidence preservation fix:
  `c32e4127861d1929af622017fe2189a6c6801fb3`.
- Student report/model extraction evidence:
  `e5f9ea68cf4aa3c646dffe0023317731dedb62ee`, with continuity checkpoints
  `093b49626d2581ad7d7be27b4fc6f800a423f429` and
  `60e21e6cfe9cccd70f355a3fd6c040beb39f3853`.
- Train/dev annotation audit and machine-readable evidence:
  `0f4dc7afe9daf09a6a0d53b577738a69a4f810d8`,
  `00101513a4ec1df8b825226451ba93d197fab94c`.
- Pre-training conflict gate and bounded CI artifacts:
  `c5640655ff1febee043335406a85fb338b7a8b42`.
- Formal blocking decision record:
  `846748547f892b483effb85b8cf71cb62f669f6e`.
- This continuity update is pending consolidation; it does not alter or restart
  training.
- No runtime/production file is modified.

## NEXT ACTION

1. Commit `pipeline/student-4-v2.trigger` and identify/monitor the resulting
   one-click run without relaunching completed stages.
2. If interrupted, restore only that run's isolated `latest.pt` through the
   explicit `resume_run_id`; never reuse student-4 v1 state.
3. Select threshold on dev only, then run frozen/adversarial, ONNX/INT8/parity
   and package only if each preceding gate passes; preserve all failure evidence
   without lowering gates.
4. Carry the independent nested-attribution contract issue to supervisor
   counter-review; do not invent a binding heuristic or start B4.
