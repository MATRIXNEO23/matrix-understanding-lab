# Matrix Understanding Lab — work continuity

Last updated: 2026-09-03T18:00:00Z  
Continuity schema: `matrix.lab.continuity.v1`  
Rule: update after every meaningful commit, training/benchmark, model/data or
strategy change, before long/risky work, and before ending any session.

## Repository state

- Repository: `MATRIXNEO23/matrix-understanding-lab`
- Branch: `main`
- HEAD verified after raw inference-evidence consolidation:
  `44db7995ce28236d79e4552d17934b1164cdb6ac`.
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

- Current gate: first trained multi-task teacher (`Gate 02`, long run in
  progress). Encoder and external-data provenance are green.
- Exact activity: GitHub Actions run `33786677296` (`Matrix-NLU Training`) is
  executing commit `37ef11c9...` with the frozen configuration below. Do not
  start another teacher run while it is active.
- In parallel, commit `9027ff3...` added the end-to-end learned decoder and
  deterministic invariant validator without touching a training-trigger path.
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

- Green local checks at current implementation:
  `python3 -m unittest discover -s matrix_nlu -p 'test_*.py' -v` (3 tests),
  `python3 -m py_compile matrix_nlu/probe_candidates.py`.
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
- First training configuration: teacher Geotrend 6x768 revision `36de33ec...`;
  seed 810923; max length 64; MASSIVE 3,000/600/1,000 rows per language,
  one auxiliary epoch; Matrix four epochs; batch 16; gradient accumulation 2;
  AdamW LR 3e-5, weight decay .01, warmup .1; P0.5 train repeat 3; CPU 4
  threads; checkpoint every epoch; resume auto; frozen tests once after
  dev-selected checkpoint.
- Training implementation commit:
  `37ef11c99785fb0fd56e99267f33e71d4c9e15e6`.
- Active training run: `33786677296`, status `in_progress` when this continuity
  checkpoint was written. Companion normal P0 and provenance workflows are
  `33786677289` and `33786677349`.
- Matrix-NLU training, frozen quality, ONNX parity, INT8, Android offline,
  RAM/PSS/CPU/latency gates: not run, therefore not green.

## Open errors, failed paths and blockers

- No architectural `DECISION_REQUIRED` is open.
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
- The teacher step is executing with Torch in run `33786677296`; no epoch/result
  is available yet. A dependency/model API error is a normal software fix; do
  not reinterpret it as a quality result or alter the frozen sets.
- `MatrixNluRuntime` currently reconstructs the encoder through the pinned Hub
  identifier before loading its state dict. This is acceptable only for the lab
  evaluator and is an open offline-export defect: the ONNX/runtime bundle must
  carry all model/tokenizer/config assets and must prove zero network access.
- The first implementation stores `earlyStoppingPatience=2` in configuration
  but does not yet consume it in the epoch loop. Do not claim early stopping was
  applied to the active run; evaluate the completed history before deciding
  whether a causal training fix is needed.

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
- Consolidated learned decoder/invariant validator:
  `9027ff3f177a6fcde57e5324e9ad27c7c15de4d4`.
- Consolidated end-to-end Typed Claim evaluator:
  `39fa4127fcc99a770f52ff86a84e11f44b60bd4f`.
- Consolidated raw prediction evidence and corrected boundary-confidence
  accounting: `44db7995ce28236d79e4552d17934b1164cdb6ac`.
- This continuity update is pending consolidation; it must not alter or restart
  the active training run.
- No runtime/production file is modified.

## NEXT ACTION

1. Commit this continuity-only update on top of `44db799...` without touching
   any training trigger path.
2. Inspect run `33786677296` steps/logs. If it fails, preserve any resumable
   checkpoint and apply only
   the causal software/dependency fix.
3. If it completes, download evidence and resume-checkpoint artifacts, record
   exact checksums/component metrics, run the end-to-end Typed Claim evaluator,
   and perform dev-led error analysis before any student or ONNX work.
