# CP47 recovery — all ten FP32 checkpoints

Download `student5-matrix-nlu-v3-fp32-cp47-run1.tar.xz` from the Student-5 repository Release tag `student5-matrix-nlu-v3-fp32-cp47-run1`. The exact HTTPS asset locator is in MODEL_MANIFEST.json. Release/asset numeric IDs and archive SHA-256 are also recorded in the canonical repository index after publication.

Verify the archive with the separately published ARCHIVE_SHA256SUMS before extraction. Extract with `tar -xJf student5-matrix-nlu-v3-fp32-cp47-run1.tar.xz` in a new empty directory. The top-level directory is `student5-matrix-nlu-v3-fp32-cp47-run1`.

Inside that directory run `sha256sum -c SHA256SUMS`. Every checkpoint has complete FP32 V3 model weights, optimizer/scheduler/RNG state and checkpoint metadata. Config/tokenizer/vocabulary/remap are shared unchanged files under tokenizer-and-source-config; architecture and implementation source are included. No pristine download is required for model recovery.

Use the versions in training-manifest.json (including torch 2.4.1+cpu and transformers 4.44.2). Run `python recover_checkpoint.py --epoch 1` (through 10). This verifies all file checksums, initializes the unchanged V3 architecture from local config and strictly loads the chosen full state dictionary. It performs no training. The loader returns the model for programmatic use. Candidate/anchor feature construction is specified in source/train_cp47.py; runtime integration and confidence calibration are not approved by this bundle.

Full model SHA-256 for each epoch is in MODEL_MANIFEST.json and that epoch's checkpoint.json. Never overwrite these files. A future training run must create a new identity and output directory. All ten epochs remain eligible; none is selected, evaluated or production approved.

The .tar.xz file uses lossless compression with a 256 MiB dictionary to share repeated frozen encoder bytes across the complete checkpoint files. This is ordinary storage compression, not weight quantization. Decompression needs roughly 256 MiB dictionary memory plus extracted disk space of about 1.5 GB.
