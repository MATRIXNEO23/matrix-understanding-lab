# Student-5 FP32 working copy recovery

Model ID: student-5-minilm-40k-phase-a-fp32-working-copy
Version: CP45_INITIAL_BYTE_IDENTICAL
Release: https://github.com/MATRIXNEO23/matrix-understanding-lab/releases/tag/student5-minilm-40k-phase-a-fp32-working-copy-cp45
Archive: https://github.com/MATRIXNEO23/matrix-understanding-lab/releases/download/student5-minilm-40k-phase-a-fp32-working-copy-cp45/student5-minilm-40k-phase-a-fp32-working-copy-cp45.zip

Download this separate working-copy ZIP, MODEL_MANIFEST.json and SHA256SUMS
from the Release. If authentication is required, use the logged-in GitHub
Release UI. Do not regenerate or substitute any model.

Verify SHA256SUMS with `sha256sum -c SHA256SUMS` after downloading every listed
asset, then check archive size 88361246 and SHA-256
7804bfb245b71df9b835fff7ee00f6ec887e019772ae34c82d269d821d587191.
Extract into a NEW empty working directory, never the original pristine path.
Verify model/model.safetensors: 148020400 bytes, SHA-256
d6e45891d1e0ec4ed023caaeb17c0dd0ae80a93b8bf877d275310b7f2837efa2.
Verify the internal SHA256SUMS from the archive root as well.
The 18 archive files include weights, config, SentencePiece vocabulary,
tokenizer config/special tokens, token-id-remap and source metadata.

Use the matching pristine tokenizer with the copied model/config. No
backbone/vocabulary replacement or remap regeneration is needed.
MODEL_MANIFEST.json alongside the ZIP is authoritative for the working-copy
identity; IDs inside the unchanged source package record its provenance.

No training is authorized by this artifact. When separately authorized, only
the working copy may be modified. Original pristine files and its Release
remain untouched. Preserve this initial snapshot and save trained outputs
under a new version. TRAIN v2.1 and all 4355 CP44 prepared targets remain
unchanged. Do not search for or create DEV.
