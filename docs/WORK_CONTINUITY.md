# Matrix Understanding Lab — work continuity

Last updated: 2026-09-03T18:17:00Z  
Continuity schema: `matrix.lab.continuity.v1`  
Rule: update after every meaningful commit, training/benchmark, model/data or
strategy change, before long/risky work, and before ending any session.

## Repository state

- Repository: `MATRIXNEO23/matrix-understanding-lab`
- Branch: `main`
- HEAD verified before the pending MASSIVE hash-pin commit:
  `ac723626bd36dbfdc03aa651d9728fc16292455b`.
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

- Current gate: external data provenance (`Gate 01`, encoder portion passed;
  MASSIVE archive hash pinning in progress).
- Exact activity: preserve the first MASSIVE inventory/license, pin its archive
  hash and rerun the same inventory. No training has started.
  declared licenses, config dimensions, weight sizes and IT/EN/ES tokenizer
  evidence for all three candidates. No model training has started.
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
- Matrix-NLU training, frozen quality, ONNX parity, INT8, Android offline,
  RAM/PSS/CPU/latency gates: not run, therefore not green.

## Open errors, failed paths and blockers

- No architectural `DECISION_REQUIRED` is open.
- The Hugging Face primary model revision and exact declared metadata remain
  unverified until the probe artifact is retrieved.
- Shell access to Hugging Face timed out in the Work container. Do not repeat
  it; use GitHub Actions network access and preserve the resulting artifact.
- Failed repository-transfer method: constructing a `jq` object by interpolating
  shell variables through a JSON string produced literal `$fN` values. Do not
  repeat it. The repair reads each file as base64, decodes it in the tool
  process and verifies the remote blobs after commit.
- Probe failure `33784241590`: do not retry unchanged; SentencePiece must be
  installed for XLM-R-family tokenizers. The pending commit contains that fix.
- Probe failure `33784416207`: do not retry unchanged; after SentencePiece,
  XLMRobertaConverter explicitly required protobuf. The pending commit pins it.
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

## Consolidation state

- Intended files in `6bf5492...` (remote contents require the pending repair):
  `.github/workflows/matrix-nlu-probe.yml`,
  `docs/MATRIX_NLU_MODEL_DATA_PLAN.md`, `matrix_nlu/candidates.json`,
  `matrix_nlu/probe_candidates.py`, `matrix_nlu/requirements-probe.txt`,
  `matrix_nlu/test_probe_candidates.py`.
- Consolidated dataset commit: `c6875b9e492cd0827ada0bc27c9471dcd4454a21`.
- Consolidated model pin/MASSIVE probe commit:
  `d8ef350ad723156cd6b8fd64509a64ae7575107c`.
- Consolidated P0.5 adapter/MASSIVE test-path commit:
  `ac723626bd36dbfdc03aa651d9728fc16292455b`.
- Pending consolidation: pinned MASSIVE source, first manifest/license artifact,
  provenance document and this continuity update.
- No runtime/production file is modified.

## NEXT ACTION

1. Commit the MASSIVE hash pin, first inventory/license artifact, provenance doc
   and continuity on top of `ac723626...`.
2. Wait for the pinned MASSIVE rerun and verify `hashPinned=true` plus
   `hashMatches=true`; preserve that manifest.
3. Mark data provenance green and implement the shared two-pass multi-task model
   and resumable training configuration before starting the long training run.
