"""Bounded G03 verification. No training, semantic audit or dataset generation."""
import argparse
import copy
import gzip
import hashlib
import importlib.util
import json
import pathlib
import re
import sys

HEAD = '8ee33811fde3aa9646a8d4eff1d5160c37ee76a4'
SHA = 'f90ae775a44023c37bf0c3a5087d64746413cbec770ca36cf154d1d533544aa4'
IDS = [
    'mx-v22a-adult-it-015', 'mx-v22a-adult-it-025',
    'cp42-it-ambiguous_binding-0117', 'cp42-en-ambiguous_binding-0119',
    'cp42-es-ambiguous_binding-0121', 'cp43-it-antecedent_ambiguous-0121',
    'cp43-en-antecedent_ambiguous-0124', 'cp43-es-antecedent_ambiguous-0127',
]


def canonical(value):
    return json.dumps(value, ensure_ascii=False, sort_keys=True, separators=(',', ':')).encode()


def sha(value):
    return hashlib.sha256(value).hexdigest()


class Offsets:
    """Deterministic lexical offsets for pure target checks, not a model tokenizer."""
    def __call__(self, text, max_length, padding, truncation, return_offsets_mapping):
        spans = [(m.start(), m.end()) for m in re.finditer(r'\w+|[^\w\s]', text)]
        assert len(spans) < max_length
        pad = max_length - len(spans)
        return {'input_ids': [1] * len(spans) + [0] * pad,
                'attention_mask': [1] * len(spans) + [0] * pad,
                'offset_mapping': spans + [(0, 0)] * pad}


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('--repo', type=pathlib.Path, required=True)
    parser.add_argument('--out', type=pathlib.Path, required=True)
    args = parser.parse_args()
    repo = args.repo.resolve()
    sys.path.insert(0, str(repo / 'matrix_nlu'))
    from contract_v3 import FIELD_STATUSES, ROLE_HEADS
    from inference_v3 import validate_claim_v3
    from training_data_v3 import build_v3_examples, IGNORE
    evidence = repo / 'reports/evidence/student5-g03-closure'
    baseline_path = evidence / 'training_data_v3.before.py'
    spec = importlib.util.spec_from_file_location('g03_before', baseline_path)
    baseline = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(baseline)
    candidate = repo / 'data/student5_v3_train_v21'
    original_files = {p.name: sha(p.read_bytes()) for p in candidate.iterdir() if p.is_file()}
    assert original_files['train.jsonl.gz'] == SHA
    lock = json.loads((candidate / 'BUILD_LOCK.json').read_text())
    assert all(original_files[k] == v for k, v in lock.items())
    manifest = json.loads((candidate / 'manifest.json').read_text())
    assert manifest['trainPayload']['compressedSha256'] == SHA
    payload = gzip.decompress((candidate / 'train.jsonl.gz').read_bytes())
    assert sha(payload) == manifest['trainPayload']['orderedSha256']
    rows = [json.loads(line) for line in payload.splitlines()]
    g03 = json.loads((repo / 'reports/evidence/student5-train-v21-cp43/status-target-readiness.json').read_text())
    assert g03['ambiguousRows'] == IDS
    selected = {}
    counts = {s: 0 for s in FIELD_STATUSES}
    h_before = hashlib.sha256()
    h_projection = hashlib.sha256()
    h_after = hashlib.sha256()
    h_repeat = hashlib.sha256()
    total_examples = total_claims = alternatives = 0
    new_keys = {'role_status_labels', 'role_alternative_pointer_labels', 'role_alternative_mask'}
    for row in rows:
        original = canonical(row)
        before = baseline.build_v3_examples(row, Offsets(), 256, row['context'])
        after = build_v3_examples(row, Offsets(), 256, row['context'])
        repeat = build_v3_examples(copy.deepcopy(row), Offsets(), 256, copy.deepcopy(row['context']))
        projected = [{k: v for k, v in example.items() if k not in new_keys} for example in after]
        assert before == projected, row['id']
        assert after == repeat and canonical(row) == original, row['id']
        for hasher, value in [(h_before, before), (h_projection, projected), (h_after, after), (h_repeat, repeat)]:
            hasher.update(canonical(value) + b'\n')
        total_examples += len(after)
        for head in ROLE_HEADS:
            assert after[0]['role_status_labels'][head] == IGNORE
            assert after[0]['role_alternative_mask'][head] == [0] * 16
        for claim, target in zip(row['claims'], after[1:]):
            total_claims += 1
            values = target['role_pointer_values']
            for head in ROLE_HEADS:
                status = FIELD_STATUSES[target['role_status_labels'][head]]
                counts[status] += 1
                assert status == claim['fieldStatusByField'][head]
                assert values[target['role_pointer_labels'][head]] == claim['labels'][head]
                decoded = [{'value': values[index], 'rank': rank + 1}
                           for rank, (index, active) in enumerate(zip(target['role_alternative_pointer_labels'][head], target['role_alternative_mask'][head])) if active]
                assert decoded == claim.get('alternativesByField', {}).get(head, [])
                alternatives += len(decoded)
            raw = {k: copy.deepcopy(v) for k, v in claim.items() if k != 'labels'}
            raw['confidenceByField'] = {h: 1.0 for h in claim['fieldStatusByField']}
            for head, value in claim['labels'].items():
                raw[head] = {'value': value, 'confidence': 1.0, 'fieldStatus': claim['fieldStatusByField'][head]}
                if head in claim.get('alternativesByField', {}):
                    raw[head]['alternatives'] = copy.deepcopy(claim['alternativesByField'][head])
            checked = validate_claim_v3(raw, text_length=len(row['text']),
                                       candidate_ids=values[:-2], claim_ids=[c['claimId'] for c in row['claims']])
            assert checked['structuralStatus'] == 'VALID', (row['id'], checked['diagnostics'])
        if row['id'] in IDS:
            assert len(row['claims']) == 1
            claim = row['claims'][0]
            request = row['id'].startswith('mx-')
            expected = {'subjectReferent': 'ctx:observer' if request else 'UNKNOWN',
                        'ownerReferent': 'ctx:speaker' if request else 'UNKNOWN',
                        'targetReferent': 'UNKNOWN' if request else 'NONE',
                        'perspectiveReferent': 'ctx:speaker', 'sourceReferent': 'ctx:speaker'}
            assert {h: claim['labels'][h] for h in ROLE_HEADS} == expected
            pair = ['ctx:observer', 'ctx:speaker'] if request else (
                ['entity:adult-a', 'entity:adult-b'] if row['id'].startswith('cp42-') else ['entity:woman-a', 'entity:woman-b'])
            ambiguous_heads = ['targetReferent'] if request else ['subjectReferent', 'ownerReferent']
            expected_alts = {h: [{'value': v, 'rank': i + 1} for i, v in enumerate(pair)] for h in ambiguous_heads}
            assert claim['alternativesByField'] == expected_alts
            assert claim['interpretationStatus'] == 'AMBIGUOUS'
            assert checked['interpretationStatus'] == 'AMBIGUOUS'
            selected[row['id']] = {
                'rowId': row['id'], 'rowSha256': sha(original), 'language': row['language'],
                'text': row['text'], 'family': claim['family'], 'context': row['context'],
                'canonicalRoles': expected, 'statuses': {h: claim['fieldStatusByField'][h] for h in ROLE_HEADS},
                'orderedAlternatives': expected_alts,
                'reason': ('D04/D07: addressee performs the requested action, requester owns the requested goal; '
                           'colloquial reflexive with con me does not uniquely distinguish self-action with companion from reciprocal action.'
                           if request else 'D06/D07: supplied context explicitly has two equally salient compatible antecedents; '
                           'subject and owner share the unresolved residence holder, while interpersonal target is inapplicable. '
                           'The location mention is object evidence, not an interpersonal target.'),
                'beforeTargets': {k: before[1][k] for k in ['role_pointer_labels', 'role_pointer_values']},
                'beforeStatusSupport': False, 'beforeAlternativesSupport': False,
                'afterTargets': {k: after[1][k] for k in ['role_pointer_labels', 'role_pointer_values', *sorted(new_keys)]},
                'structuralStatus': checked['structuralStatus'], 'interpretationStatus': checked['interpretationStatus'],
                'rowModified': False, 'result': 'PASS',
            }
    assert set(selected) == set(IDS)
    assert original_files == {p.name: sha(p.read_bytes()) for p in candidate.iterdir() if p.is_file()}
    assert h_before.hexdigest() == h_projection.hexdigest()
    assert h_after.hexdigest() == h_repeat.hexdigest()
    result = {
        'startingHead': HEAD, 'G03': 'PASS', 'rowsTotal': 8, 'rowsPass': 8,
        'sourceTrainId': manifest['id'], 'finalTrainId': manifest['id'], 'trainSha256': SHA,
        'datasetBytesChanged': False, 'candidateFilesSha256': original_files,
        'observations': len(rows), 'claims': total_claims, 'targetExamples': total_examples,
        'roleStatusCounts': counts, 'alternativeEntries': alternatives,
        'structuralValidation': 'PASS', 'buildLockMatch': True, 'manifestMatch': True,
        'unrelatedLegacyTargetsUnchanged': True, 'legacyTargetSha256': h_before.hexdigest(),
        'projectedTargetSha256': h_projection.hexdigest(),
        'deterministicTargetRebuildMatch': True, 'targetSha256': h_after.hexdigest(),
        'repeatedTargetSha256': h_repeat.hexdigest(),
        'datasetRebuilt': False,
        'scope': 'Mechanical builder compatibility and structural checks across existing TRAIN; exact semantic adjudication restricted to eight G03 rows. '
                 'Dataset deterministic reproduction remains the persisted CP43 proof for the unchanged SHA; fresh deterministic check here rebuilds targets twice. '
                 'No model/tokenizer loading, loss, calibration, general audit, G04 or G07 work.',
        'trainingExecuted': False, 'fineTuningExecuted': False, 'quantizationExecuted': False,
        'onnxExecuted': False, 'nextWorkStarted': False,
    }
    args.out.mkdir(parents=True, exist_ok=True)
    for name, value in [('verification.json', result), ('eight-row-verification.json', [selected[i] for i in IDS])]:
        (args.out / name).write_text(json.dumps(value, ensure_ascii=False, indent=2) + '\n')
    print(json.dumps(result, indent=2))


if __name__ == '__main__':
    main()
