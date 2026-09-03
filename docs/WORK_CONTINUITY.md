# Matrix Understanding Lab — work continuity

Last updated: 2026-09-03T21:06:00Z  
Continuity schema: `matrix.lab.continuity.v1`  
Rule: update after every meaningful commit, training/benchmark, model/data or
strategy change, before long/risky work, and before ending any session.

## Repository state

- Repository: `MATRIXNEO23/matrix-understanding-lab`
- Branch: `main`
- HEAD verified before this continuity update:
  `36cd3ce1704fe16a2582fc5896eccb96fc189695`.
- Training launch commit:
  `37ef11c99785fb0fd56e99267f33e71d4c9e15e6`.
- Last consolidated implementation commit:
  `6bf5492fd4155e4e77b2a6e514a793f8e5e6c5ff`
  (`feat: add Matrix-NLU provenance candidate probe`)
- Production Matrix repository/runtime: frozen reference only; no production
  files have been modified.
- Frozen production semantic reference:
  `ae82d5cf843d52b3d60caadd161e4a5516fc5d0d`.

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

- First trained multi-task teacher (`Gate 02`) completed successfully in
  GitHub Actions run `33786677296` at `2026-09-03T20:26:35Z`; every setup,
  training and artifact step is green. It must not be rerun.
- Current gate: dev-only causal repair after the strict end-to-end TypedClaim
  gate correctly rejected the immutable teacher artifact. Post-gate run
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
  deliberately unexecuted because run `33802563626` failed the dev gate.
  Android physical PSS/latency remains a later gate.

## Open errors, failed paths and blockers

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
- This continuity update is pending consolidation; it does not alter or restart
  the active training run.
- No runtime/production file is modified.

## NEXT ACTION

1. Commit this continuity update on top of `36cd3ce...` without touching a
   training trigger path.
2. Patch and unit-test the two deterministic dev-evidence defects: auditable
   entity referent binding in the existing validator contract and correct
   per-language ownership-corruption accounting.
3. Reproduce every repair candidate on train/dev only; classify the causal
   family, patch learned data/objective/decoder as justified, then run the full
   regression/property suite. Never use frozen results for tuning.
4. Do not launch the four-layer candidate unchanged: the current six-layer
   teacher is far below the dev gate, so a smaller model with the same unresolved
   defects would waste compute. After dev-causal corrections are regression
   green, run the isolated four-layer candidate through `run_pipeline.py` and
   require the complete production quality/size/package gate.
5. Carry the nested-attribution contract issue above to supervisor counter-review;
   continue all independent single-level C1 quality/export work without inventing
   a binding heuristic.
