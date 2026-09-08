---
base_model: intfloat/multilingual-e5-small
pipeline_tag: sentence-similarity
library_name: sentence-transformers
tags:
- sentence-transformers
- sentence-similarity
- feature-extraction
- token-pruning
---

# multilingual-e5-small-pruned

This model is a **token-embedding pruned** version of
[intfloat/multilingual-e5-small](https://huggingface.co/intfloat/multilingual-e5-small).

Token-embedding pruning clusters semantically similar tokens in the embedding
space (using DBSCAN) and merges each cluster into a single shared embedding,
shrinking the vocabulary and reducing memory without retraining the transformer
layers.

## How to use

```python
from sentence_transformers import SentenceTransformer

model = SentenceTransformer("jangedoo/multilingual-e5-small-pruned", trust_remote_code=True)
embeddings = model.encode(["Hello world", "How are you?"])
```

> **Note:** `trust_remote_code=True` is required because the model ships a small
> custom tokenizer class (`pruned_tokenizer.py`) that applies the id remapping
> after tokenization. No additional package installation is needed.

## Pruning statistics

| | Base | Pruned | Reduction |
|---|---:|---:|---:|
| Vocab size | 250,037 | 172,569 | 30.98% |
| Total parameters | 117,653,760 | 87,906,048 | 25.28% |
| Embedding parameters | 96,014,208 | 66,266,496 | 30.98% |
| Embedding size (MB) | 366.3 | 252.8 | 113.5 MB saved |

## Evaluation

| Dataset / Metric | Base | Pruned | Relative (base = 1.0) |
|---|---:|---:|---:|
| stsb / stsb_pearson_cosine | 0.8092 | 0.7925 | 0.9794 |
| stsb / stsb_spearman_cosine | 0.8359 | 0.8014 | 0.9588 |
| nanobeir / NanoClimateFEVER_cosine_accuracy@1 | 0.3000 | 0.2600 | 0.8667 |
| nanobeir / NanoClimateFEVER_cosine_accuracy@3 | 0.4200 | 0.3600 | 0.8571 |
| nanobeir / NanoClimateFEVER_cosine_accuracy@5 | 0.5000 | 0.3800 | 0.7600 |
| nanobeir / NanoClimateFEVER_cosine_accuracy@10 | 0.6600 | 0.5400 | 0.8182 |
| nanobeir / NanoClimateFEVER_cosine_precision@1 | 0.3000 | 0.2600 | 0.8667 |
| nanobeir / NanoClimateFEVER_cosine_precision@3 | 0.1533 | 0.1333 | 0.8696 |
| nanobeir / NanoClimateFEVER_cosine_precision@5 | 0.1160 | 0.0880 | 0.7586 |
| nanobeir / NanoClimateFEVER_cosine_precision@10 | 0.0880 | 0.0680 | 0.7727 |
| nanobeir / NanoClimateFEVER_cosine_recall@1 | 0.1500 | 0.1283 | 0.8556 |
| nanobeir / NanoClimateFEVER_cosine_recall@3 | 0.2000 | 0.1717 | 0.8583 |
| nanobeir / NanoClimateFEVER_cosine_recall@5 | 0.2433 | 0.1817 | 0.7466 |
| nanobeir / NanoClimateFEVER_cosine_recall@10 | 0.3530 | 0.2667 | 0.7554 |
| nanobeir / NanoClimateFEVER_cosine_ndcg@10 | 0.2927 | 0.2364 | 0.8076 |
| nanobeir / NanoClimateFEVER_cosine_mrr@10 | 0.3906 | 0.3305 | 0.8464 |
| nanobeir / NanoClimateFEVER_cosine_map@100 | 0.2358 | 0.1934 | 0.8202 |
| nanobeir / NanoDBPedia_cosine_accuracy@1 | 0.5800 | 0.6400 | 1.1034 |
| nanobeir / NanoDBPedia_cosine_accuracy@3 | 0.8400 | 0.7800 | 0.9286 |
| nanobeir / NanoDBPedia_cosine_accuracy@5 | 0.8800 | 0.8400 | 0.9545 |
| nanobeir / NanoDBPedia_cosine_accuracy@10 | 0.9600 | 0.9200 | 0.9583 |
| nanobeir / NanoDBPedia_cosine_precision@1 | 0.5800 | 0.6400 | 1.1034 |
| nanobeir / NanoDBPedia_cosine_precision@3 | 0.5400 | 0.5200 | 0.9630 |
| nanobeir / NanoDBPedia_cosine_precision@5 | 0.5200 | 0.4920 | 0.9462 |
| nanobeir / NanoDBPedia_cosine_precision@10 | 0.4300 | 0.3980 | 0.9256 |
| nanobeir / NanoDBPedia_cosine_recall@1 | 0.0755 | 0.0895 | 1.1861 |
| nanobeir / NanoDBPedia_cosine_recall@3 | 0.1534 | 0.1405 | 0.9156 |
| nanobeir / NanoDBPedia_cosine_recall@5 | 0.2049 | 0.1976 | 0.9641 |
| nanobeir / NanoDBPedia_cosine_recall@10 | 0.3126 | 0.2802 | 0.8963 |
| nanobeir / NanoDBPedia_cosine_ndcg@10 | 0.5371 | 0.5108 | 0.9510 |
| nanobeir / NanoDBPedia_cosine_mrr@10 | 0.7175 | 0.7211 | 1.0050 |
| nanobeir / NanoDBPedia_cosine_map@100 | 0.3988 | 0.3692 | 0.9256 |
| nanobeir / NanoFEVER_cosine_accuracy@1 | 0.6200 | 0.5400 | 0.8710 |
| nanobeir / NanoFEVER_cosine_accuracy@3 | 0.8800 | 0.8200 | 0.9318 |
| nanobeir / NanoFEVER_cosine_accuracy@5 | 0.9400 | 0.8800 | 0.9362 |
| nanobeir / NanoFEVER_cosine_accuracy@10 | 0.9800 | 0.9600 | 0.9796 |
| nanobeir / NanoFEVER_cosine_precision@1 | 0.6200 | 0.5400 | 0.8710 |
| nanobeir / NanoFEVER_cosine_precision@3 | 0.3000 | 0.2800 | 0.9333 |
| nanobeir / NanoFEVER_cosine_precision@5 | 0.1960 | 0.1800 | 0.9184 |
| nanobeir / NanoFEVER_cosine_precision@10 | 0.1020 | 0.1000 | 0.9804 |
| nanobeir / NanoFEVER_cosine_recall@1 | 0.5867 | 0.5067 | 0.8636 |
| nanobeir / NanoFEVER_cosine_recall@3 | 0.8433 | 0.7967 | 0.9447 |
| nanobeir / NanoFEVER_cosine_recall@5 | 0.9033 | 0.8567 | 0.9483 |
| nanobeir / NanoFEVER_cosine_recall@10 | 0.9333 | 0.9233 | 0.9893 |
| nanobeir / NanoFEVER_cosine_ndcg@10 | 0.7897 | 0.7353 | 0.9310 |
| nanobeir / NanoFEVER_cosine_mrr@10 | 0.7592 | 0.6909 | 0.9100 |
| nanobeir / NanoFEVER_cosine_map@100 | 0.7338 | 0.6652 | 0.9066 |
| nanobeir / NanoFiQA2018_cosine_accuracy@1 | 0.3600 | 0.3200 | 0.8889 |
| nanobeir / NanoFiQA2018_cosine_accuracy@3 | 0.5600 | 0.5200 | 0.9286 |
| nanobeir / NanoFiQA2018_cosine_accuracy@5 | 0.6200 | 0.5800 | 0.9355 |
| nanobeir / NanoFiQA2018_cosine_accuracy@10 | 0.6600 | 0.6800 | 1.0303 |
| nanobeir / NanoFiQA2018_cosine_precision@1 | 0.3600 | 0.3200 | 0.8889 |
| nanobeir / NanoFiQA2018_cosine_precision@3 | 0.2400 | 0.1933 | 0.8056 |
| nanobeir / NanoFiQA2018_cosine_precision@5 | 0.1800 | 0.1560 | 0.8667 |
| nanobeir / NanoFiQA2018_cosine_precision@10 | 0.1060 | 0.0960 | 0.9057 |
| nanobeir / NanoFiQA2018_cosine_recall@1 | 0.1801 | 0.1687 | 0.9371 |
| nanobeir / NanoFiQA2018_cosine_recall@3 | 0.3545 | 0.3174 | 0.8954 |
| nanobeir / NanoFiQA2018_cosine_recall@5 | 0.4403 | 0.3816 | 0.8666 |
| nanobeir / NanoFiQA2018_cosine_recall@10 | 0.4878 | 0.4738 | 0.9713 |
| nanobeir / NanoFiQA2018_cosine_ndcg@10 | 0.3956 | 0.3655 | 0.9240 |
| nanobeir / NanoFiQA2018_cosine_mrr@10 | 0.4630 | 0.4302 | 0.9292 |
| nanobeir / NanoFiQA2018_cosine_map@100 | 0.3380 | 0.2928 | 0.8664 |
| nanobeir / NanoHotpotQA_cosine_accuracy@1 | 0.7800 | 0.6800 | 0.8718 |
| nanobeir / NanoHotpotQA_cosine_accuracy@3 | 0.9200 | 0.9000 | 0.9783 |
| nanobeir / NanoHotpotQA_cosine_accuracy@5 | 0.9600 | 0.9200 | 0.9583 |
| nanobeir / NanoHotpotQA_cosine_accuracy@10 | 0.9800 | 0.9400 | 0.9592 |
| nanobeir / NanoHotpotQA_cosine_precision@1 | 0.7800 | 0.6800 | 0.8718 |
| nanobeir / NanoHotpotQA_cosine_precision@3 | 0.5000 | 0.4533 | 0.9067 |
| nanobeir / NanoHotpotQA_cosine_precision@5 | 0.3240 | 0.3040 | 0.9383 |
| nanobeir / NanoHotpotQA_cosine_precision@10 | 0.1720 | 0.1600 | 0.9302 |
| nanobeir / NanoHotpotQA_cosine_recall@1 | 0.3900 | 0.3400 | 0.8718 |
| nanobeir / NanoHotpotQA_cosine_recall@3 | 0.7500 | 0.6800 | 0.9067 |
| nanobeir / NanoHotpotQA_cosine_recall@5 | 0.8100 | 0.7600 | 0.9383 |
| nanobeir / NanoHotpotQA_cosine_recall@10 | 0.8600 | 0.8000 | 0.9302 |
| nanobeir / NanoHotpotQA_cosine_ndcg@10 | 0.7997 | 0.7254 | 0.9072 |
| nanobeir / NanoHotpotQA_cosine_mrr@10 | 0.8600 | 0.7879 | 0.9161 |
| nanobeir / NanoHotpotQA_cosine_map@100 | 0.7435 | 0.6629 | 0.8916 |
| nanobeir / NanoMSMARCO_cosine_accuracy@1 | 0.4200 | 0.4200 | 1.0000 |
| nanobeir / NanoMSMARCO_cosine_accuracy@3 | 0.5800 | 0.6000 | 1.0345 |
| nanobeir / NanoMSMARCO_cosine_accuracy@5 | 0.7600 | 0.6800 | 0.8947 |
| nanobeir / NanoMSMARCO_cosine_accuracy@10 | 0.8600 | 0.7800 | 0.9070 |
| nanobeir / NanoMSMARCO_cosine_precision@1 | 0.4200 | 0.4200 | 1.0000 |
| nanobeir / NanoMSMARCO_cosine_precision@3 | 0.1933 | 0.2000 | 1.0345 |
| nanobeir / NanoMSMARCO_cosine_precision@5 | 0.1520 | 0.1360 | 0.8947 |
| nanobeir / NanoMSMARCO_cosine_precision@10 | 0.0860 | 0.0780 | 0.9070 |
| nanobeir / NanoMSMARCO_cosine_recall@1 | 0.4200 | 0.4200 | 1.0000 |
| nanobeir / NanoMSMARCO_cosine_recall@3 | 0.5800 | 0.6000 | 1.0345 |
| nanobeir / NanoMSMARCO_cosine_recall@5 | 0.7600 | 0.6800 | 0.8947 |
| nanobeir / NanoMSMARCO_cosine_recall@10 | 0.8600 | 0.7800 | 0.9070 |
| nanobeir / NanoMSMARCO_cosine_ndcg@10 | 0.6187 | 0.5920 | 0.9568 |
| nanobeir / NanoMSMARCO_cosine_mrr@10 | 0.5436 | 0.5332 | 0.9808 |
| nanobeir / NanoMSMARCO_cosine_map@100 | 0.5517 | 0.5444 | 0.9868 |
| nanobeir / NanoNFCorpus_cosine_accuracy@1 | 0.4200 | 0.4000 | 0.9524 |
| nanobeir / NanoNFCorpus_cosine_accuracy@3 | 0.5000 | 0.5000 | 1.0000 |
| nanobeir / NanoNFCorpus_cosine_accuracy@5 | 0.5600 | 0.5600 | 1.0000 |
| nanobeir / NanoNFCorpus_cosine_accuracy@10 | 0.6400 | 0.6000 | 0.9375 |
| nanobeir / NanoNFCorpus_cosine_precision@1 | 0.4200 | 0.4000 | 0.9524 |
| nanobeir / NanoNFCorpus_cosine_precision@3 | 0.3267 | 0.3333 | 1.0204 |
| nanobeir / NanoNFCorpus_cosine_precision@5 | 0.3280 | 0.3040 | 0.9268 |
| nanobeir / NanoNFCorpus_cosine_precision@10 | 0.2520 | 0.2460 | 0.9762 |
| nanobeir / NanoNFCorpus_cosine_recall@1 | 0.0148 | 0.0233 | 1.5744 |
| nanobeir / NanoNFCorpus_cosine_recall@3 | 0.0442 | 0.0428 | 0.9684 |
| nanobeir / NanoNFCorpus_cosine_recall@5 | 0.0772 | 0.0685 | 0.8880 |
| nanobeir / NanoNFCorpus_cosine_recall@10 | 0.0999 | 0.0938 | 0.9389 |
| nanobeir / NanoNFCorpus_cosine_ndcg@10 | 0.2937 | 0.2873 | 0.9783 |
| nanobeir / NanoNFCorpus_cosine_mrr@10 | 0.4829 | 0.4625 | 0.9577 |
| nanobeir / NanoNFCorpus_cosine_map@100 | 0.1046 | 0.1013 | 0.9678 |
| nanobeir / NanoNQ_cosine_accuracy@1 | 0.5400 | 0.3400 | 0.6296 |
| nanobeir / NanoNQ_cosine_accuracy@3 | 0.6400 | 0.5200 | 0.8125 |
| nanobeir / NanoNQ_cosine_accuracy@5 | 0.7000 | 0.6000 | 0.8571 |
| nanobeir / NanoNQ_cosine_accuracy@10 | 0.8200 | 0.7200 | 0.8780 |
| nanobeir / NanoNQ_cosine_precision@1 | 0.5400 | 0.3400 | 0.6296 |
| nanobeir / NanoNQ_cosine_precision@3 | 0.2133 | 0.1733 | 0.8125 |
| nanobeir / NanoNQ_cosine_precision@5 | 0.1480 | 0.1240 | 0.8378 |
| nanobeir / NanoNQ_cosine_precision@10 | 0.0900 | 0.0760 | 0.8444 |
| nanobeir / NanoNQ_cosine_recall@1 | 0.4900 | 0.3400 | 0.6939 |
| nanobeir / NanoNQ_cosine_recall@3 | 0.5900 | 0.5000 | 0.8475 |
| nanobeir / NanoNQ_cosine_recall@5 | 0.6700 | 0.5900 | 0.8806 |
| nanobeir / NanoNQ_cosine_recall@10 | 0.8000 | 0.7000 | 0.8750 |
| nanobeir / NanoNQ_cosine_ndcg@10 | 0.6371 | 0.5086 | 0.7983 |
| nanobeir / NanoNQ_cosine_mrr@10 | 0.6107 | 0.4496 | 0.7362 |
| nanobeir / NanoNQ_cosine_map@100 | 0.5816 | 0.4546 | 0.7816 |
| nanobeir / NanoQuoraRetrieval_cosine_accuracy@1 | 0.8800 | 0.8400 | 0.9545 |
| nanobeir / NanoQuoraRetrieval_cosine_accuracy@3 | 1.0000 | 0.9600 | 0.9600 |
| nanobeir / NanoQuoraRetrieval_cosine_accuracy@5 | 1.0000 | 0.9600 | 0.9600 |
| nanobeir / NanoQuoraRetrieval_cosine_accuracy@10 | 1.0000 | 0.9600 | 0.9600 |
| nanobeir / NanoQuoraRetrieval_cosine_precision@1 | 0.8800 | 0.8400 | 0.9545 |
| nanobeir / NanoQuoraRetrieval_cosine_precision@3 | 0.4067 | 0.3733 | 0.9180 |
| nanobeir / NanoQuoraRetrieval_cosine_precision@5 | 0.2520 | 0.2280 | 0.9048 |
| nanobeir / NanoQuoraRetrieval_cosine_precision@10 | 0.1320 | 0.1180 | 0.8939 |
| nanobeir / NanoQuoraRetrieval_cosine_recall@1 | 0.7807 | 0.7540 | 0.9658 |
| nanobeir / NanoQuoraRetrieval_cosine_recall@3 | 0.9587 | 0.9253 | 0.9652 |
| nanobeir / NanoQuoraRetrieval_cosine_recall@5 | 0.9693 | 0.9320 | 0.9615 |
| nanobeir / NanoQuoraRetrieval_cosine_recall@10 | 0.9833 | 0.9393 | 0.9553 |
| nanobeir / NanoQuoraRetrieval_cosine_ndcg@10 | 0.9359 | 0.8947 | 0.9560 |
| nanobeir / NanoQuoraRetrieval_cosine_mrr@10 | 0.9333 | 0.8967 | 0.9607 |
| nanobeir / NanoQuoraRetrieval_cosine_map@100 | 0.9123 | 0.8732 | 0.9572 |
| nanobeir / NanoSCIDOCS_cosine_accuracy@1 | 0.4000 | 0.3000 | 0.7500 |
| nanobeir / NanoSCIDOCS_cosine_accuracy@3 | 0.6400 | 0.5200 | 0.8125 |
| nanobeir / NanoSCIDOCS_cosine_accuracy@5 | 0.7400 | 0.6000 | 0.8108 |
| nanobeir / NanoSCIDOCS_cosine_accuracy@10 | 0.8200 | 0.7800 | 0.9512 |
| nanobeir / NanoSCIDOCS_cosine_precision@1 | 0.4000 | 0.3000 | 0.7500 |
| nanobeir / NanoSCIDOCS_cosine_precision@3 | 0.3067 | 0.2333 | 0.7609 |
| nanobeir / NanoSCIDOCS_cosine_precision@5 | 0.2600 | 0.2000 | 0.7692 |
| nanobeir / NanoSCIDOCS_cosine_precision@10 | 0.1560 | 0.1400 | 0.8974 |
| nanobeir / NanoSCIDOCS_cosine_recall@1 | 0.0847 | 0.0627 | 0.7402 |
| nanobeir / NanoSCIDOCS_cosine_recall@3 | 0.1897 | 0.1437 | 0.7575 |
| nanobeir / NanoSCIDOCS_cosine_recall@5 | 0.2667 | 0.2057 | 0.7712 |
| nanobeir / NanoSCIDOCS_cosine_recall@10 | 0.3187 | 0.2887 | 0.9059 |
| nanobeir / NanoSCIDOCS_cosine_ndcg@10 | 0.3225 | 0.2703 | 0.8380 |
| nanobeir / NanoSCIDOCS_cosine_mrr@10 | 0.5353 | 0.4398 | 0.8216 |
| nanobeir / NanoSCIDOCS_cosine_map@100 | 0.2448 | 0.1997 | 0.8155 |
| nanobeir / NanoArguAna_cosine_accuracy@1 | 0.1000 | 0.1000 | 1.0000 |
| nanobeir / NanoArguAna_cosine_accuracy@3 | 0.4800 | 0.4400 | 0.9167 |
| nanobeir / NanoArguAna_cosine_accuracy@5 | 0.6200 | 0.4800 | 0.7742 |
| nanobeir / NanoArguAna_cosine_accuracy@10 | 0.7200 | 0.6200 | 0.8611 |
| nanobeir / NanoArguAna_cosine_precision@1 | 0.1000 | 0.1000 | 1.0000 |
| nanobeir / NanoArguAna_cosine_precision@3 | 0.1600 | 0.1467 | 0.9167 |
| nanobeir / NanoArguAna_cosine_precision@5 | 0.1240 | 0.0960 | 0.7742 |
| nanobeir / NanoArguAna_cosine_precision@10 | 0.0720 | 0.0620 | 0.8611 |
| nanobeir / NanoArguAna_cosine_recall@1 | 0.1000 | 0.1000 | 1.0000 |
| nanobeir / NanoArguAna_cosine_recall@3 | 0.4800 | 0.4400 | 0.9167 |
| nanobeir / NanoArguAna_cosine_recall@5 | 0.6200 | 0.4800 | 0.7742 |
| nanobeir / NanoArguAna_cosine_recall@10 | 0.7200 | 0.6200 | 0.8611 |
| nanobeir / NanoArguAna_cosine_ndcg@10 | 0.4121 | 0.3676 | 0.8920 |
| nanobeir / NanoArguAna_cosine_mrr@10 | 0.3128 | 0.2864 | 0.9156 |
| nanobeir / NanoArguAna_cosine_map@100 | 0.3267 | 0.2962 | 0.9067 |
| nanobeir / NanoSciFact_cosine_accuracy@1 | 0.6800 | 0.5200 | 0.7647 |
| nanobeir / NanoSciFact_cosine_accuracy@3 | 0.7400 | 0.6800 | 0.9189 |
| nanobeir / NanoSciFact_cosine_accuracy@5 | 0.7400 | 0.7400 | 1.0000 |
| nanobeir / NanoSciFact_cosine_accuracy@10 | 0.7800 | 0.7800 | 1.0000 |
| nanobeir / NanoSciFact_cosine_precision@1 | 0.6800 | 0.5200 | 0.7647 |
| nanobeir / NanoSciFact_cosine_precision@3 | 0.2533 | 0.2400 | 0.9474 |
| nanobeir / NanoSciFact_cosine_precision@5 | 0.1600 | 0.1600 | 1.0000 |
| nanobeir / NanoSciFact_cosine_precision@10 | 0.0880 | 0.0860 | 0.9773 |
| nanobeir / NanoSciFact_cosine_recall@1 | 0.6450 | 0.5000 | 0.7752 |
| nanobeir / NanoSciFact_cosine_recall@3 | 0.7150 | 0.6600 | 0.9231 |
| nanobeir / NanoSciFact_cosine_recall@5 | 0.7250 | 0.7250 | 1.0000 |
| nanobeir / NanoSciFact_cosine_recall@10 | 0.7800 | 0.7700 | 0.9872 |
| nanobeir / NanoSciFact_cosine_ndcg@10 | 0.7209 | 0.6455 | 0.8955 |
| nanobeir / NanoSciFact_cosine_mrr@10 | 0.7117 | 0.6116 | 0.8592 |
| nanobeir / NanoSciFact_cosine_map@100 | 0.7011 | 0.6058 | 0.8640 |
| nanobeir / NanoTouche2020_cosine_accuracy@1 | 0.4898 | 0.4082 | 0.8333 |
| nanobeir / NanoTouche2020_cosine_accuracy@3 | 0.8980 | 0.7959 | 0.8864 |
| nanobeir / NanoTouche2020_cosine_accuracy@5 | 0.9388 | 0.8776 | 0.9348 |
| nanobeir / NanoTouche2020_cosine_accuracy@10 | 0.9796 | 0.9592 | 0.9792 |
| nanobeir / NanoTouche2020_cosine_precision@1 | 0.4898 | 0.4082 | 0.8333 |
| nanobeir / NanoTouche2020_cosine_precision@3 | 0.5442 | 0.4150 | 0.7625 |
| nanobeir / NanoTouche2020_cosine_precision@5 | 0.4816 | 0.4163 | 0.8644 |
| nanobeir / NanoTouche2020_cosine_precision@10 | 0.4000 | 0.3429 | 0.8571 |
| nanobeir / NanoTouche2020_cosine_recall@1 | 0.0309 | 0.0251 | 0.8101 |
| nanobeir / NanoTouche2020_cosine_recall@3 | 0.1093 | 0.0844 | 0.7719 |
| nanobeir / NanoTouche2020_cosine_recall@5 | 0.1638 | 0.1409 | 0.8598 |
| nanobeir / NanoTouche2020_cosine_recall@10 | 0.2602 | 0.2243 | 0.8621 |
| nanobeir / NanoTouche2020_cosine_ndcg@10 | 0.4483 | 0.3753 | 0.8372 |
| nanobeir / NanoTouche2020_cosine_mrr@10 | 0.6885 | 0.5975 | 0.8679 |
| nanobeir / NanoTouche2020_cosine_map@100 | 0.3263 | 0.2599 | 0.7967 |
| nanobeir / NanoBEIR_mean_cosine_accuracy@1 | 0.5054 | 0.4437 | 0.8780 |
| nanobeir / NanoBEIR_mean_cosine_accuracy@3 | 0.6998 | 0.6458 | 0.9228 |
| nanobeir / NanoBEIR_mean_cosine_accuracy@5 | 0.7661 | 0.6998 | 0.9135 |
| nanobeir / NanoBEIR_mean_cosine_accuracy@10 | 0.8354 | 0.7876 | 0.9429 |
| nanobeir / NanoBEIR_mean_cosine_precision@1 | 0.5054 | 0.4437 | 0.8780 |
| nanobeir / NanoBEIR_mean_cosine_precision@3 | 0.3183 | 0.2842 | 0.8930 |
| nanobeir / NanoBEIR_mean_cosine_precision@5 | 0.2494 | 0.2219 | 0.8898 |
| nanobeir / NanoBEIR_mean_cosine_precision@10 | 0.1672 | 0.1516 | 0.9066 |
| nanobeir / NanoBEIR_mean_cosine_recall@1 | 0.3037 | 0.2660 | 0.8759 |
| nanobeir / NanoBEIR_mean_cosine_recall@3 | 0.4591 | 0.4233 | 0.9220 |
| nanobeir / NanoBEIR_mean_cosine_recall@5 | 0.5272 | 0.4769 | 0.9045 |
| nanobeir / NanoBEIR_mean_cosine_recall@10 | 0.5976 | 0.5508 | 0.9216 |
| nanobeir / NanoBEIR_mean_cosine_ndcg@10 | 0.5542 | 0.5011 | 0.9043 |
| nanobeir / NanoBEIR_mean_cosine_mrr@10 | 0.6161 | 0.5568 | 0.9037 |
| nanobeir / NanoBEIR_mean_cosine_map@100 | 0.4769 | 0.4245 | 0.8902 |
| nanobeir_ne / NanoClimateFEVER_cosine_accuracy@1 | 0.1000 | 0.0600 | 0.6000 |
| nanobeir_ne / NanoClimateFEVER_cosine_accuracy@3 | 0.3000 | 0.1000 | 0.3333 |
| nanobeir_ne / NanoClimateFEVER_cosine_accuracy@5 | 0.4200 | 0.2000 | 0.4762 |
| nanobeir_ne / NanoClimateFEVER_cosine_accuracy@10 | 0.5400 | 0.3400 | 0.6296 |
| nanobeir_ne / NanoClimateFEVER_cosine_precision@1 | 0.1000 | 0.0600 | 0.6000 |
| nanobeir_ne / NanoClimateFEVER_cosine_precision@3 | 0.1000 | 0.0333 | 0.3333 |
| nanobeir_ne / NanoClimateFEVER_cosine_precision@5 | 0.1000 | 0.0400 | 0.4000 |
| nanobeir_ne / NanoClimateFEVER_cosine_precision@10 | 0.0700 | 0.0380 | 0.5429 |
| nanobeir_ne / NanoClimateFEVER_cosine_recall@1 | 0.0300 | 0.0350 | 1.1667 |
| nanobeir_ne / NanoClimateFEVER_cosine_recall@3 | 0.1400 | 0.0450 | 0.3214 |
| nanobeir_ne / NanoClimateFEVER_cosine_recall@5 | 0.2073 | 0.0967 | 0.4662 |
| nanobeir_ne / NanoClimateFEVER_cosine_recall@10 | 0.2747 | 0.1533 | 0.5583 |
| nanobeir_ne / NanoClimateFEVER_cosine_ndcg@10 | 0.1836 | 0.0970 | 0.5282 |
| nanobeir_ne / NanoClimateFEVER_cosine_mrr@10 | 0.2279 | 0.1112 | 0.4881 |
| nanobeir_ne / NanoClimateFEVER_cosine_map@100 | 0.1241 | 0.0700 | 0.5636 |
| nanobeir_ne / NanoDBPedia_cosine_accuracy@1 | 0.4000 | 0.3800 | 0.9500 |
| nanobeir_ne / NanoDBPedia_cosine_accuracy@3 | 0.7600 | 0.6200 | 0.8158 |
| nanobeir_ne / NanoDBPedia_cosine_accuracy@5 | 0.8000 | 0.7400 | 0.9250 |
| nanobeir_ne / NanoDBPedia_cosine_accuracy@10 | 0.8200 | 0.8400 | 1.0244 |
| nanobeir_ne / NanoDBPedia_cosine_precision@1 | 0.4000 | 0.3800 | 0.9500 |
| nanobeir_ne / NanoDBPedia_cosine_precision@3 | 0.4133 | 0.3333 | 0.8065 |
| nanobeir_ne / NanoDBPedia_cosine_precision@5 | 0.3680 | 0.3360 | 0.9130 |
| nanobeir_ne / NanoDBPedia_cosine_precision@10 | 0.3260 | 0.2860 | 0.8773 |
| nanobeir_ne / NanoDBPedia_cosine_recall@1 | 0.0736 | 0.0736 | 1.0002 |
| nanobeir_ne / NanoDBPedia_cosine_recall@3 | 0.1475 | 0.1168 | 0.7921 |
| nanobeir_ne / NanoDBPedia_cosine_recall@5 | 0.1746 | 0.1629 | 0.9329 |
| nanobeir_ne / NanoDBPedia_cosine_recall@10 | 0.2453 | 0.2255 | 0.9193 |
| nanobeir_ne / NanoDBPedia_cosine_ndcg@10 | 0.4156 | 0.3676 | 0.8845 |
| nanobeir_ne / NanoDBPedia_cosine_mrr@10 | 0.5748 | 0.5297 | 0.9215 |
| nanobeir_ne / NanoDBPedia_cosine_map@100 | 0.3034 | 0.2661 | 0.8770 |
| nanobeir_ne / NanoFEVER_cosine_accuracy@1 | 0.3400 | 0.1800 | 0.5294 |
| nanobeir_ne / NanoFEVER_cosine_accuracy@3 | 0.5800 | 0.4600 | 0.7931 |
| nanobeir_ne / NanoFEVER_cosine_accuracy@5 | 0.6600 | 0.5800 | 0.8788 |
| nanobeir_ne / NanoFEVER_cosine_accuracy@10 | 0.8000 | 0.7000 | 0.8750 |
| nanobeir_ne / NanoFEVER_cosine_precision@1 | 0.3400 | 0.1800 | 0.5294 |
| nanobeir_ne / NanoFEVER_cosine_precision@3 | 0.1933 | 0.1533 | 0.7931 |
| nanobeir_ne / NanoFEVER_cosine_precision@5 | 0.1360 | 0.1200 | 0.8824 |
| nanobeir_ne / NanoFEVER_cosine_precision@10 | 0.0820 | 0.0720 | 0.8780 |
| nanobeir_ne / NanoFEVER_cosine_recall@1 | 0.3267 | 0.1800 | 0.5510 |
| nanobeir_ne / NanoFEVER_cosine_recall@3 | 0.5567 | 0.4500 | 0.8084 |
| nanobeir_ne / NanoFEVER_cosine_recall@5 | 0.6467 | 0.5567 | 0.8608 |
| nanobeir_ne / NanoFEVER_cosine_recall@10 | 0.7767 | 0.6767 | 0.8712 |
| nanobeir_ne / NanoFEVER_cosine_ndcg@10 | 0.5473 | 0.4206 | 0.7685 |
| nanobeir_ne / NanoFEVER_cosine_mrr@10 | 0.4854 | 0.3419 | 0.7043 |
| nanobeir_ne / NanoFEVER_cosine_map@100 | 0.4794 | 0.3463 | 0.7223 |
| nanobeir_ne / NanoFiQA2018_cosine_accuracy@1 | 0.2600 | 0.1000 | 0.3846 |
| nanobeir_ne / NanoFiQA2018_cosine_accuracy@3 | 0.4200 | 0.2400 | 0.5714 |
| nanobeir_ne / NanoFiQA2018_cosine_accuracy@5 | 0.4600 | 0.2600 | 0.5652 |
| nanobeir_ne / NanoFiQA2018_cosine_accuracy@10 | 0.5400 | 0.3600 | 0.6667 |
| nanobeir_ne / NanoFiQA2018_cosine_precision@1 | 0.2600 | 0.1000 | 0.3846 |
| nanobeir_ne / NanoFiQA2018_cosine_precision@3 | 0.1600 | 0.0867 | 0.5417 |
| nanobeir_ne / NanoFiQA2018_cosine_precision@5 | 0.1240 | 0.0600 | 0.4839 |
| nanobeir_ne / NanoFiQA2018_cosine_precision@10 | 0.0800 | 0.0400 | 0.5000 |
| nanobeir_ne / NanoFiQA2018_cosine_recall@1 | 0.1287 | 0.0640 | 0.4971 |
| nanobeir_ne / NanoFiQA2018_cosine_recall@3 | 0.2288 | 0.1807 | 0.7897 |
| nanobeir_ne / NanoFiQA2018_cosine_recall@5 | 0.2893 | 0.1872 | 0.6470 |
| nanobeir_ne / NanoFiQA2018_cosine_recall@10 | 0.3780 | 0.2352 | 0.6221 |
| nanobeir_ne / NanoFiQA2018_cosine_ndcg@10 | 0.2912 | 0.1687 | 0.5793 |
| nanobeir_ne / NanoFiQA2018_cosine_mrr@10 | 0.3572 | 0.1806 | 0.5056 |
| nanobeir_ne / NanoFiQA2018_cosine_map@100 | 0.2275 | 0.1385 | 0.6088 |
| nanobeir_ne / NanoHotpotQA_cosine_accuracy@1 | 0.7800 | 0.6600 | 0.8462 |
| nanobeir_ne / NanoHotpotQA_cosine_accuracy@3 | 0.8400 | 0.8000 | 0.9524 |
| nanobeir_ne / NanoHotpotQA_cosine_accuracy@5 | 0.8600 | 0.8200 | 0.9535 |
| nanobeir_ne / NanoHotpotQA_cosine_accuracy@10 | 0.9000 | 0.8400 | 0.9333 |
| nanobeir_ne / NanoHotpotQA_cosine_precision@1 | 0.7800 | 0.6600 | 0.8462 |
| nanobeir_ne / NanoHotpotQA_cosine_precision@3 | 0.3800 | 0.3467 | 0.9123 |
| nanobeir_ne / NanoHotpotQA_cosine_precision@5 | 0.2520 | 0.2200 | 0.8730 |
| nanobeir_ne / NanoHotpotQA_cosine_precision@10 | 0.1380 | 0.1180 | 0.8551 |
| nanobeir_ne / NanoHotpotQA_cosine_recall@1 | 0.3900 | 0.3300 | 0.8462 |
| nanobeir_ne / NanoHotpotQA_cosine_recall@3 | 0.5700 | 0.5200 | 0.9123 |
| nanobeir_ne / NanoHotpotQA_cosine_recall@5 | 0.6300 | 0.5500 | 0.8730 |
| nanobeir_ne / NanoHotpotQA_cosine_recall@10 | 0.6900 | 0.5900 | 0.8551 |
| nanobeir_ne / NanoHotpotQA_cosine_ndcg@10 | 0.6636 | 0.5728 | 0.8631 |
| nanobeir_ne / NanoHotpotQA_cosine_mrr@10 | 0.8132 | 0.7269 | 0.8938 |
| nanobeir_ne / NanoHotpotQA_cosine_map@100 | 0.5941 | 0.5034 | 0.8473 |
| nanobeir_ne / NanoMSMARCO_cosine_accuracy@1 | 0.2600 | 0.1800 | 0.6923 |
| nanobeir_ne / NanoMSMARCO_cosine_accuracy@3 | 0.5800 | 0.4400 | 0.7586 |
| nanobeir_ne / NanoMSMARCO_cosine_accuracy@5 | 0.6600 | 0.5200 | 0.7879 |
| nanobeir_ne / NanoMSMARCO_cosine_accuracy@10 | 0.7400 | 0.6800 | 0.9189 |
| nanobeir_ne / NanoMSMARCO_cosine_precision@1 | 0.2600 | 0.1800 | 0.6923 |
| nanobeir_ne / NanoMSMARCO_cosine_precision@3 | 0.1933 | 0.1467 | 0.7586 |
| nanobeir_ne / NanoMSMARCO_cosine_precision@5 | 0.1320 | 0.1040 | 0.7879 |
| nanobeir_ne / NanoMSMARCO_cosine_precision@10 | 0.0740 | 0.0680 | 0.9189 |
| nanobeir_ne / NanoMSMARCO_cosine_recall@1 | 0.2600 | 0.1800 | 0.6923 |
| nanobeir_ne / NanoMSMARCO_cosine_recall@3 | 0.5800 | 0.4400 | 0.7586 |
| nanobeir_ne / NanoMSMARCO_cosine_recall@5 | 0.6600 | 0.5200 | 0.7879 |
| nanobeir_ne / NanoMSMARCO_cosine_recall@10 | 0.7400 | 0.6800 | 0.9189 |
| nanobeir_ne / NanoMSMARCO_cosine_ndcg@10 | 0.4955 | 0.4125 | 0.8325 |
| nanobeir_ne / NanoMSMARCO_cosine_mrr@10 | 0.4174 | 0.3298 | 0.7901 |
| nanobeir_ne / NanoMSMARCO_cosine_map@100 | 0.4252 | 0.3412 | 0.8024 |
| nanobeir_ne / NanoNFCorpus_cosine_accuracy@1 | 0.2800 | 0.1600 | 0.5714 |
| nanobeir_ne / NanoNFCorpus_cosine_accuracy@3 | 0.4400 | 0.3400 | 0.7727 |
| nanobeir_ne / NanoNFCorpus_cosine_accuracy@5 | 0.4400 | 0.4800 | 1.0909 |
| nanobeir_ne / NanoNFCorpus_cosine_accuracy@10 | 0.4400 | 0.5600 | 1.2727 |
| nanobeir_ne / NanoNFCorpus_cosine_precision@1 | 0.2800 | 0.1600 | 0.5714 |
| nanobeir_ne / NanoNFCorpus_cosine_precision@3 | 0.2600 | 0.1933 | 0.7436 |
| nanobeir_ne / NanoNFCorpus_cosine_precision@5 | 0.2120 | 0.2240 | 1.0566 |
| nanobeir_ne / NanoNFCorpus_cosine_precision@10 | 0.1600 | 0.1840 | 1.1500 |
| nanobeir_ne / NanoNFCorpus_cosine_recall@1 | 0.0084 | 0.0054 | 0.6468 |
| nanobeir_ne / NanoNFCorpus_cosine_recall@3 | 0.0413 | 0.0296 | 0.7165 |
| nanobeir_ne / NanoNFCorpus_cosine_recall@5 | 0.0486 | 0.0483 | 0.9939 |
| nanobeir_ne / NanoNFCorpus_cosine_recall@10 | 0.0617 | 0.0802 | 1.3003 |
| nanobeir_ne / NanoNFCorpus_cosine_ndcg@10 | 0.1975 | 0.1976 | 1.0005 |
| nanobeir_ne / NanoNFCorpus_cosine_mrr@10 | 0.3500 | 0.2882 | 0.8235 |
| nanobeir_ne / NanoNFCorpus_cosine_map@100 | 0.0701 | 0.0660 | 0.9418 |
| nanobeir_ne / NanoNQ_cosine_accuracy@1 | 0.2000 | 0.1600 | 0.8000 |
| nanobeir_ne / NanoNQ_cosine_accuracy@3 | 0.3400 | 0.3000 | 0.8824 |
| nanobeir_ne / NanoNQ_cosine_accuracy@5 | 0.3400 | 0.3200 | 0.9412 |
| nanobeir_ne / NanoNQ_cosine_accuracy@10 | 0.4400 | 0.4600 | 1.0455 |
| nanobeir_ne / NanoNQ_cosine_precision@1 | 0.2000 | 0.1600 | 0.8000 |
| nanobeir_ne / NanoNQ_cosine_precision@3 | 0.1133 | 0.1000 | 0.8824 |
| nanobeir_ne / NanoNQ_cosine_precision@5 | 0.0680 | 0.0640 | 0.9412 |
| nanobeir_ne / NanoNQ_cosine_precision@10 | 0.0440 | 0.0460 | 1.0455 |
| nanobeir_ne / NanoNQ_cosine_recall@1 | 0.1800 | 0.1500 | 0.8333 |
| nanobeir_ne / NanoNQ_cosine_recall@3 | 0.3100 | 0.2800 | 0.9032 |
| nanobeir_ne / NanoNQ_cosine_recall@5 | 0.3100 | 0.3000 | 0.9677 |
| nanobeir_ne / NanoNQ_cosine_recall@10 | 0.4100 | 0.4200 | 1.0244 |
| nanobeir_ne / NanoNQ_cosine_ndcg@10 | 0.2951 | 0.2817 | 0.9545 |
| nanobeir_ne / NanoNQ_cosine_mrr@10 | 0.2767 | 0.2495 | 0.9016 |
| nanobeir_ne / NanoNQ_cosine_map@100 | 0.2685 | 0.2439 | 0.9087 |
| nanobeir_ne / NanoQuoraRetrieval_cosine_accuracy@1 | 0.8200 | 0.7400 | 0.9024 |
| nanobeir_ne / NanoQuoraRetrieval_cosine_accuracy@3 | 0.9000 | 0.8200 | 0.9111 |
| nanobeir_ne / NanoQuoraRetrieval_cosine_accuracy@5 | 0.9200 | 0.8600 | 0.9348 |
| nanobeir_ne / NanoQuoraRetrieval_cosine_accuracy@10 | 0.9800 | 0.9000 | 0.9184 |
| nanobeir_ne / NanoQuoraRetrieval_cosine_precision@1 | 0.8200 | 0.7400 | 0.9024 |
| nanobeir_ne / NanoQuoraRetrieval_cosine_precision@3 | 0.3533 | 0.3000 | 0.8491 |
| nanobeir_ne / NanoQuoraRetrieval_cosine_precision@5 | 0.2360 | 0.2040 | 0.8644 |
| nanobeir_ne / NanoQuoraRetrieval_cosine_precision@10 | 0.1320 | 0.1140 | 0.8636 |
| nanobeir_ne / NanoQuoraRetrieval_cosine_recall@1 | 0.7240 | 0.6773 | 0.9355 |
| nanobeir_ne / NanoQuoraRetrieval_cosine_recall@3 | 0.8380 | 0.7713 | 0.9204 |
| nanobeir_ne / NanoQuoraRetrieval_cosine_recall@5 | 0.8860 | 0.8260 | 0.9323 |
| nanobeir_ne / NanoQuoraRetrieval_cosine_recall@10 | 0.9660 | 0.8727 | 0.9034 |
| nanobeir_ne / NanoQuoraRetrieval_cosine_ndcg@10 | 0.8797 | 0.7971 | 0.9061 |
| nanobeir_ne / NanoQuoraRetrieval_cosine_mrr@10 | 0.8707 | 0.7867 | 0.9035 |
| nanobeir_ne / NanoQuoraRetrieval_cosine_map@100 | 0.8452 | 0.7688 | 0.9096 |
| nanobeir_ne / NanoSCIDOCS_cosine_accuracy@1 | 0.2000 | 0.1600 | 0.8000 |
| nanobeir_ne / NanoSCIDOCS_cosine_accuracy@3 | 0.3600 | 0.2800 | 0.7778 |
| nanobeir_ne / NanoSCIDOCS_cosine_accuracy@5 | 0.4600 | 0.4200 | 0.9130 |
| nanobeir_ne / NanoSCIDOCS_cosine_accuracy@10 | 0.5800 | 0.5000 | 0.8621 |
| nanobeir_ne / NanoSCIDOCS_cosine_precision@1 | 0.2000 | 0.1600 | 0.8000 |
| nanobeir_ne / NanoSCIDOCS_cosine_precision@3 | 0.1733 | 0.1267 | 0.7308 |
| nanobeir_ne / NanoSCIDOCS_cosine_precision@5 | 0.1480 | 0.1200 | 0.8108 |
| nanobeir_ne / NanoSCIDOCS_cosine_precision@10 | 0.0980 | 0.0840 | 0.8571 |
| nanobeir_ne / NanoSCIDOCS_cosine_recall@1 | 0.0420 | 0.0330 | 0.7857 |
| nanobeir_ne / NanoSCIDOCS_cosine_recall@3 | 0.1080 | 0.0770 | 0.7130 |
| nanobeir_ne / NanoSCIDOCS_cosine_recall@5 | 0.1557 | 0.1240 | 0.7966 |
| nanobeir_ne / NanoSCIDOCS_cosine_recall@10 | 0.2047 | 0.1730 | 0.8453 |
| nanobeir_ne / NanoSCIDOCS_cosine_ndcg@10 | 0.1883 | 0.1565 | 0.8312 |
| nanobeir_ne / NanoSCIDOCS_cosine_mrr@10 | 0.3002 | 0.2527 | 0.8416 |
| nanobeir_ne / NanoSCIDOCS_cosine_map@100 | 0.1343 | 0.1044 | 0.7773 |
| nanobeir_ne / NanoArguAna_cosine_accuracy@1 | 0.1200 | 0.0800 | 0.6667 |
| nanobeir_ne / NanoArguAna_cosine_accuracy@3 | 0.5200 | 0.4000 | 0.7692 |
| nanobeir_ne / NanoArguAna_cosine_accuracy@5 | 0.5800 | 0.5200 | 0.8966 |
| nanobeir_ne / NanoArguAna_cosine_accuracy@10 | 0.7400 | 0.6200 | 0.8378 |
| nanobeir_ne / NanoArguAna_cosine_precision@1 | 0.1200 | 0.0800 | 0.6667 |
| nanobeir_ne / NanoArguAna_cosine_precision@3 | 0.1733 | 0.1333 | 0.7692 |
| nanobeir_ne / NanoArguAna_cosine_precision@5 | 0.1160 | 0.1040 | 0.8966 |
| nanobeir_ne / NanoArguAna_cosine_precision@10 | 0.0740 | 0.0620 | 0.8378 |
| nanobeir_ne / NanoArguAna_cosine_recall@1 | 0.1200 | 0.0800 | 0.6667 |
| nanobeir_ne / NanoArguAna_cosine_recall@3 | 0.5200 | 0.4000 | 0.7692 |
| nanobeir_ne / NanoArguAna_cosine_recall@5 | 0.5800 | 0.5200 | 0.8966 |
| nanobeir_ne / NanoArguAna_cosine_recall@10 | 0.7400 | 0.6200 | 0.8378 |
| nanobeir_ne / NanoArguAna_cosine_ndcg@10 | 0.4276 | 0.3476 | 0.8130 |
| nanobeir_ne / NanoArguAna_cosine_mrr@10 | 0.3276 | 0.2602 | 0.7945 |
| nanobeir_ne / NanoArguAna_cosine_map@100 | 0.3367 | 0.2650 | 0.7870 |
| nanobeir_ne / NanoSciFact_cosine_accuracy@1 | 0.3200 | 0.2400 | 0.7500 |
| nanobeir_ne / NanoSciFact_cosine_accuracy@3 | 0.4800 | 0.4600 | 0.9583 |
| nanobeir_ne / NanoSciFact_cosine_accuracy@5 | 0.5400 | 0.5200 | 0.9630 |
| nanobeir_ne / NanoSciFact_cosine_accuracy@10 | 0.6600 | 0.5800 | 0.8788 |
| nanobeir_ne / NanoSciFact_cosine_precision@1 | 0.3200 | 0.2400 | 0.7500 |
| nanobeir_ne / NanoSciFact_cosine_precision@3 | 0.1667 | 0.1600 | 0.9600 |
| nanobeir_ne / NanoSciFact_cosine_precision@5 | 0.1120 | 0.1080 | 0.9643 |
| nanobeir_ne / NanoSciFact_cosine_precision@10 | 0.0700 | 0.0620 | 0.8857 |
| nanobeir_ne / NanoSciFact_cosine_recall@1 | 0.3050 | 0.2250 | 0.7377 |
| nanobeir_ne / NanoSciFact_cosine_recall@3 | 0.4600 | 0.4400 | 0.9565 |
| nanobeir_ne / NanoSciFact_cosine_recall@5 | 0.5100 | 0.5000 | 0.9804 |
| nanobeir_ne / NanoSciFact_cosine_recall@10 | 0.6250 | 0.5650 | 0.9040 |
| nanobeir_ne / NanoSciFact_cosine_ndcg@10 | 0.4596 | 0.4007 | 0.8720 |
| nanobeir_ne / NanoSciFact_cosine_mrr@10 | 0.4155 | 0.3574 | 0.8600 |
| nanobeir_ne / NanoSciFact_cosine_map@100 | 0.4093 | 0.3533 | 0.8632 |
| nanobeir_ne / NanoTouche2020_cosine_accuracy@1 | 0.3469 | 0.1224 | 0.3529 |
| nanobeir_ne / NanoTouche2020_cosine_accuracy@3 | 0.5510 | 0.3469 | 0.6296 |
| nanobeir_ne / NanoTouche2020_cosine_accuracy@5 | 0.6735 | 0.5510 | 0.8182 |
| nanobeir_ne / NanoTouche2020_cosine_accuracy@10 | 0.8571 | 0.7143 | 0.8333 |
| nanobeir_ne / NanoTouche2020_cosine_precision@1 | 0.3469 | 0.1224 | 0.3529 |
| nanobeir_ne / NanoTouche2020_cosine_precision@3 | 0.3333 | 0.1633 | 0.4898 |
| nanobeir_ne / NanoTouche2020_cosine_precision@5 | 0.3224 | 0.2122 | 0.6582 |
| nanobeir_ne / NanoTouche2020_cosine_precision@10 | 0.2939 | 0.1857 | 0.6319 |
| nanobeir_ne / NanoTouche2020_cosine_recall@1 | 0.0216 | 0.0091 | 0.4228 |
| nanobeir_ne / NanoTouche2020_cosine_recall@3 | 0.0678 | 0.0325 | 0.4793 |
| nanobeir_ne / NanoTouche2020_cosine_recall@5 | 0.1083 | 0.0700 | 0.6466 |
| nanobeir_ne / NanoTouche2020_cosine_recall@10 | 0.1892 | 0.1182 | 0.6244 |
| nanobeir_ne / NanoTouche2020_cosine_ndcg@10 | 0.3143 | 0.1835 | 0.5838 |
| nanobeir_ne / NanoTouche2020_cosine_mrr@10 | 0.4881 | 0.2811 | 0.5759 |
| nanobeir_ne / NanoTouche2020_cosine_map@100 | 0.2267 | 0.1326 | 0.5847 |
| nanobeir_ne / NanoBEIR_mean_cosine_accuracy@1 | 0.3405 | 0.2479 | 0.7279 |
| nanobeir_ne / NanoBEIR_mean_cosine_accuracy@3 | 0.5439 | 0.4313 | 0.7929 |
| nanobeir_ne / NanoBEIR_mean_cosine_accuracy@5 | 0.6010 | 0.5224 | 0.8691 |
| nanobeir_ne / NanoBEIR_mean_cosine_accuracy@10 | 0.6952 | 0.6226 | 0.8957 |
| nanobeir_ne / NanoBEIR_mean_cosine_precision@1 | 0.3405 | 0.2479 | 0.7279 |
| nanobeir_ne / NanoBEIR_mean_cosine_precision@3 | 0.2318 | 0.1751 | 0.7555 |
| nanobeir_ne / NanoBEIR_mean_cosine_precision@5 | 0.1790 | 0.1474 | 0.8237 |
| nanobeir_ne / NanoBEIR_mean_cosine_precision@10 | 0.1263 | 0.1046 | 0.8281 |
| nanobeir_ne / NanoBEIR_mean_cosine_recall@1 | 0.2008 | 0.1571 | 0.7826 |
| nanobeir_ne / NanoBEIR_mean_cosine_recall@3 | 0.3514 | 0.2910 | 0.8281 |
| nanobeir_ne / NanoBEIR_mean_cosine_recall@5 | 0.4005 | 0.3432 | 0.8570 |
| nanobeir_ne / NanoBEIR_mean_cosine_recall@10 | 0.4847 | 0.4161 | 0.8585 |
| nanobeir_ne / NanoBEIR_mean_cosine_ndcg@10 | 0.4122 | 0.3388 | 0.8218 |
| nanobeir_ne / NanoBEIR_mean_cosine_mrr@10 | 0.4542 | 0.3612 | 0.7953 |
| nanobeir_ne / NanoBEIR_mean_cosine_map@100 | 0.3419 | 0.2769 | 0.8098 |

## Citation

If you use this model or the pruning approach, please cite:

```bibtex
@misc{subedi2025tokenpruning,
  author = {Sanjaya Subedi},
  title  = {Token Embedding Pruning for Sentence Transformers},
  year   = {2026},
  note   = {Available at: [link to be added upon publication]}
}
```
