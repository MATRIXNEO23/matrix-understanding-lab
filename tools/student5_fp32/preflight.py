"""Authenticate immutable inputs and prepare real-tokenizer targets; no optimizer."""
import argparse
import collections
import gzip
import hashlib
import importlib.metadata
import json
import pathlib
import platform
import sys
import zipfile

TRAIN_SHA = 'f90ae775a44023c37bf0c3a5087d64746413cbec770ca36cf154d1d533544aa4'
ARCHIVE_SHA = '7804bfb245b71df9b835fff7ee00f6ec887e019772ae34c82d269d821d587191'
MODEL_SHA = 'd6e45891d1e0ec4ed023caaeb17c0dd0ae80a93b8bf877d275310b7f2837efa2'


def sha(data):
    return hashlib.sha256(data).hexdigest()


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('--repo', type=pathlib.Path, required=True)
    parser.add_argument('--pristine-archive', type=pathlib.Path, required=True)
    parser.add_argument('--model-dir', type=pathlib.Path, required=True)
    parser.add_argument('--out', type=pathlib.Path, required=True)
    args = parser.parse_args()
    repo = args.repo.resolve()
    sys.path.insert(0, str(repo / 'matrix_nlu'))
    from training_data_v3 import build_v3_examples
    from contract_v3 import FIELD_STATUSES, ROLE_HEADS
    from transformers import XLMRobertaTokenizer, XLMRobertaTokenizerFast
    from safetensors import safe_open
    provenance = json.loads((repo / 'reports/evidence/student5-pristine-analysis-cp41/provenance.json').read_text())
    archive = args.pristine_archive.read_bytes()
    assert len(archive) == 88361246 and sha(archive) == ARCHIVE_SHA
    checks = []
    with zipfile.ZipFile(args.pristine_archive) as z:
        assert z.testzip() is None
        for item in provenance['internalChecks']:
            data = z.read(item['path'])
            assert len(data) == item['bytes'] and sha(data) == item['sha256']
            if item['path'].startswith('model/'):
                assert (args.model_dir / item['path'][6:]).read_bytes() == data
            checks.append({'path': item['path'], 'sha256': sha(data), 'pass': True})
    model_file = args.model_dir / 'model.safetensors'
    assert sha(model_file.read_bytes()) == MODEL_SHA
    dtypes = collections.Counter()
    with safe_open(str(model_file), framework='pt', device='cpu') as f:
        for key in f.keys():
            dtypes[str(f.get_slice(key).get_dtype())] += 1
    assert set(dtypes) == {'F32'}
    dataset_dir = repo / 'data/student5_v3_train_v21'
    dataset_hashes = {p.name: sha(p.read_bytes()) for p in dataset_dir.iterdir() if p.is_file()}
    assert dataset_hashes['train.jsonl.gz'] == TRAIN_SHA
    lock = json.loads((dataset_dir / 'BUILD_LOCK.json').read_text())
    assert all(dataset_hashes[k] == v for k, v in lock.items())
    slow = XLMRobertaTokenizer.from_pretrained(args.model_dir, local_files_only=True)
    fast = XLMRobertaTokenizerFast.from_pretrained(args.model_dir, local_files_only=True, from_slow=True)
    tokenizer_checks = 0
    max_tokens = 0

    class CheckedTokenizer:
        def __call__(self, text, **kwargs):
            nonlocal tokenizer_checks, max_tokens
            expected = slow(text, truncation=False)['input_ids']
            actual = fast(text, truncation=False)['input_ids']
            assert expected == actual, 'fast/slow token-ID mismatch'
            assert max(actual) < 40000 and len(actual) <= kwargs['max_length']
            tokenizer_checks += 1
            max_tokens = max(max_tokens, len(actual))
            return fast(text, **kwargs)

    rows = [json.loads(line) for line in gzip.decompress((dataset_dir / 'train.jsonl.gz').read_bytes()).splitlines()]
    g03_ids = json.loads((repo / 'reports/evidence/student5-train-v21-cp43/status-target-readiness.json').read_text())['ambiguousRows']
    targets = []
    errors = []
    g03 = []
    for row in rows:
        try:
            built = build_v3_examples(row, CheckedTokenizer(), 256, row['context'])
            targets.extend(built)
            if row['id'] in g03_ids:
                claim, target = row['claims'][0], built[1]
                for h in ROLE_HEADS:
                    assert FIELD_STATUSES[target['role_status_labels'][h]] == claim['fieldStatusByField'][h]
                    assert target['role_pointer_values'][target['role_pointer_labels'][h]] == claim['labels'][h]
                    actual = [{'rank': i + 1, 'value': target['role_pointer_values'][v]}
                              for i, (v, mask) in enumerate(zip(target['role_alternative_pointer_labels'][h], target['role_alternative_mask'][h])) if mask]
                    assert actual == claim.get('alternativesByField', {}).get(h, [])
                g03.append({'rowId': row['id'], 'pass': True, 'ambiguousFields': [h for h in ROLE_HEADS if claim['fieldStatusByField'][h] == 'AMBIGUOUS']})
        except Exception as exc:
            errors.append({'rowId': row['id'], 'errorType': type(exc).__name__, 'error': str(exc)})
    args.out.mkdir(parents=True, exist_ok=False)
    payload = (''.join(json.dumps(t, ensure_ascii=False, sort_keys=True, separators=(',', ':')) + '\n' for t in targets)).encode()
    packed = gzip.compress(payload, mtime=0)
    (args.out / 'prepared-targets.jsonl.gz').write_bytes(packed)
    result = {
        'startingHead': '6389e82c255c50964ce2df370a4682ba7206248b',
        'pristineIdentity': provenance['releaseTag'], 'archiveSha256': ARCHIVE_SHA,
        'modelSha256': MODEL_SHA, 'modelTensorDtypes': dict(dtypes), 'internalChecks': checks,
        'trainId': rows[0]['datasetId'], 'trainSha256': TRAIN_SHA, 'datasetFilesSha256': dataset_hashes,
        'targetBuilderSha256': sha((repo / 'matrix_nlu/training_data_v3.py').read_bytes()),
        'preparedExamples': len(targets), 'rows': len(rows), 'claims': sum(len(r['claims']) for r in rows),
        'tokenizerIdComparisons': tokenizer_checks, 'maxObservedTokens': max_tokens, 'maxLength': 256,
        'fastTokenizerMethod': 'XLMRobertaTokenizerFast.from_pretrained(local pristine, from_slow=True); every text compared to canonical slow token IDs',
        'targetPreparationErrors': errors, 'g03Rows': g03,
        'preparedTargetsSha256': sha(packed), 'preparedTargetsOrderedSha256': sha(payload),
        'dependencies': {p: importlib.metadata.version(p) for p in ['torch','transformers','numpy','safetensors','tokenizers','sentencepiece','protobuf']},
        'python': sys.version, 'platform': platform.platform(),
        'scope': 'Input authentication and real-tokenizer target preparation only. Not a dataset semantic audit, model quality evaluation or training run.',
        'trainingExecuted': False, 'optimizerExecuted': False, 'modelForwardExecuted': False,
        'quantizationExecuted': False, 'onnxExecuted': False, 'frozenRead': False,
        'trainDatasetModified': False,
    }
    assert sha(model_file.read_bytes()) == MODEL_SHA
    assert dataset_hashes == {p.name: sha(p.read_bytes()) for p in dataset_dir.iterdir() if p.is_file()}
    (args.out / 'preflight.json').write_text(json.dumps(result, ensure_ascii=False, indent=2) + '\n')
    print(json.dumps({k: result[k] for k in ['modelTensorDtypes','preparedExamples','tokenizerIdComparisons','maxObservedTokens','targetPreparationErrors','g03Rows']}, indent=2))


if __name__ == '__main__':
    main()
