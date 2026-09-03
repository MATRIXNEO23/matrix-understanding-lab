# Matrix-NLU trained model plan

Status: `IMPLEMENTED / FIRST TRAINING NOT YET RUN`  
Canonical architecture: `cf6395b0fefc254febe3c804751ca4b048f974d1`.

## Learned path

One shared pretrained multilingual encoder supports two learned passes:

1. full-observation token head predicts proposition-local claim boundaries;
2. each predicted claim span is encoded again and the shared heads predict
   dialogue act, predicate, subject/target/owner/perspective referent classes,
   polarity, temporal relation, claim kind, object/subject/negation/temporal
   spans and PERSON/LOCATION spans.

The first supervised run uses the pinned six-layer Geotrend exact-language
DistilmBERT as teacher and quality comparator. A four-layer student initialized
from evenly spaced pretrained teacher layers is evaluated only after the teacher
establishes the quality ceiling. Production integration is out of scope.

## Auxiliary pretraining

Before Matrix supervision, one epoch uses a deterministic, hash-verified sample
of MASSIVE:

- 3,000 train rows per language;
- 600 dev rows per language;
- 1,000 frozen test rows per language;
- learned auxiliary 60-way intent and BIO slot heads;
- official partitions retained; no Matrix predicate is derived from a MASSIVE
  intent at inference.

The Matrix stage uses 2,883 generated train observations plus the P0.5 train
partition repeated three times to prevent the larger synthetic layer from
drowning real regressions. Selection uses Matrix dev and P0.5 dev only. Frozen
Matrix, P0.5 and MASSIVE test sets are evaluated once after loading the
dev-selected checkpoint.

## Exact first configuration

- config: `matrix_nlu/train_config.json`;
- seed: `810923`;
- max sequence length: 64;
- MASSIVE epochs: 1;
- Matrix epochs: 4;
- batch size: 16; gradient accumulation: 2;
- AdamW learning rate: `3e-5`; weight decay: `0.01`; warmup: 10%;
- deterministic CPU algorithms; 4 Torch threads;
- checkpoint: after each epoch, including optimizer/scheduler/current and best
  state; `resume=auto` when a checkpoint is supplied in the output directory.

Long-running command:

```text
python matrix_nlu/train.py --config matrix_nlu/train_config.json --data-dir build/matrix-nlu/data --massive-dir build/matrix-nlu/massive --output-dir build/matrix-nlu/training
```

## Gate interpretation

The first run measures component quality and establishes causal error families.
It cannot alone mark the architecture ready: end-to-end Typed Claim decoding,
calibrated abstention, invariant-validator tests, ONNX parity, INT8 delta and
offline Android resource measurements remain separate gates. A failed quality
metric leads to dev-driven data/objective/model work, not linguistic runtime
rules and not OpenNLP production work.
