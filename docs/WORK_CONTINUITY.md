# Matrix Understanding Lab — work continuity

Last updated: 2026-09-03T17:29:00Z  
Continuity schema: `matrix.lab.continuity.v1`  
Rule: update after every meaningful commit, training/benchmark, model/data or
strategy change, before long/risky work, and before ending any session.

## Repository state

- Repository: `MATRIXNEO23/matrix-understanding-lab`
- Branch: `main`
- HEAD verified before the pending repair commit:
  `d2a388b340ce5430395526880266182d06324a07`.
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

- Current gate: encoder/data provenance selection (`Gate 01`, in progress).
- Exact activity: repair the six probe files atomically on top of `d2a388b...`,
  then let GitHub Actions workflow `Matrix-NLU Candidate Probe` resolve
  immutable Hugging Face revisions,
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
- `Geotrend/distilbert-base-en-fr-es-pt-it-cased` was initially considered but
  superseded by the exact-language `en-es-it` checkpoint. Do not train the
  5-language checkpoint unless the exact checkpoint fails a documented gate.
- XtremeDistil h256 is tagged English and reports English GLUE/SQuAD evidence;
  compact size alone cannot qualify it as the multilingual production encoder.
- Multilingual MiniLM has a large XLM-R embedding table; it is a reference until
  measured size disproves the mobile concern.
- Do not disable or bypass frozen test partitions; do not use any test result to
  train or choose a variant.
- Do not add linguistic regex/rules to the invariant validator.

## Consolidation state

- Intended files in `6bf5492...` (remote contents require the pending repair):
  `.github/workflows/matrix-nlu-probe.yml`,
  `docs/MATRIX_NLU_MODEL_DATA_PLAN.md`, `matrix_nlu/candidates.json`,
  `matrix_nlu/probe_candidates.py`, `matrix_nlu/requirements-probe.txt`,
  `matrix_nlu/test_probe_candidates.py`.
- File introduced by the current continuity checkpoint:
  `docs/WORK_CONTINUITY.md`.
- No runtime/production file is modified.

## NEXT ACTION

1. Replace all six literal-placeholder probe blobs plus this continuity update
   in one repair commit on top of `d2a388b...`; fast-forward `main` and verify
   the remote file contents.
2. Query workflow runs for the repair commit; wait for `Matrix-NLU Candidate Probe`
   to finish without restarting prior gates.
3. Download `matrix-nlu-candidate-probe`, record its artifact id/digest and the
   exact selected/rejected model revisions in this file.
4. If the primary probe is green, pin its immutable revision and begin the
   deterministic layered dataset builder; otherwise apply the documented model
   fallback sequence without returning to OpenNLP production work.
