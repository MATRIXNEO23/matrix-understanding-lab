"""One deterministic CP47 FP32 head-training run; no DEV/Frozen discovery.

Uses the unchanged V3 architecture and immutable CP44 prepared targets.
The cache is an execution optimization for the frozen encoder, not a new model.
"""
import argparse
import collections
import gzip
import hashlib
import importlib.metadata
import json
import math
import os
import pathlib
import platform
import random
import shutil
import sys
import time


def sha(path):
    return hashlib.sha256(pathlib.Path(path).read_bytes()).hexdigest()


def write_json(path, value):
    pathlib.Path(path).write_text(json.dumps(value, ensure_ascii=False, indent=2) + '\n')


def heads_from_hidden(model, hidden, candidates, candidate_mask, anchors, anchor_mask):
    """Exact algebra of model_v3.forward after the frozen encoder call."""
    import torch
    from contract_v3 import ROLE_HEADS
    token_hidden, pooled = model.dropout(hidden), model.dropout(hidden[:, 0])
    projected = model.candidate_projection(candidates)
    specials = model.pointer_special_embeddings.unsqueeze(0).expand(len(hidden), -1, -1)
    all_candidates = torch.cat((projected, specials), dim=1)
    all_mask = torch.cat((candidate_mask, torch.ones((len(hidden), 2), dtype=candidate_mask.dtype)), dim=1)
    scale = model.hidden_size ** -0.5
    roles = {h: (torch.bmm(all_candidates, (pooled + model.role_queries[h]).unsqueeze(-1)).squeeze(-1) * scale).masked_fill(all_mask == 0, -1e4) for h in ROLE_HEADS}
    anchor_logits = (torch.bmm(model.candidate_projection(anchors), (pooled + model.temporal_anchor_query).unsqueeze(-1)).squeeze(-1) * scale).masked_fill(anchor_mask == 0, -1e4)
    fixed = {h: head(pooled) for h, head in model.fixed_sequence_heads.items() if h != 'temporalRelation'}
    return {'tokens': {h: head(token_hidden) for h, head in model.token_heads.items()}, 'sequence': {**fixed, **roles, 'temporalRelation': {'relation': model.fixed_sequence_heads['temporalRelation'](pooled), 'anchor': anchor_logits}}}


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('--repo', type=pathlib.Path, required=True)
    parser.add_argument('--source', type=pathlib.Path, required=True)
    parser.add_argument('--archive', type=pathlib.Path, required=True)
    parser.add_argument('--config', type=pathlib.Path, required=True)
    parser.add_argument('--out', type=pathlib.Path, required=True)
    args = parser.parse_args()
    repo, source, out = args.repo.resolve(), args.source.resolve(), args.out.resolve()
    sys.path.insert(0, str(repo / 'matrix_nlu'))
    import torch
    import torch.nn.functional as F
    from safetensors.torch import save_file, load_file
    from transformers import XLMRobertaTokenizerFast
    from model_v3 import build_model_v3, parameter_summary_v3
    from contract_v3 import ROLE_HEADS, TOKEN_LABELS, FIXED_SEQUENCE_LABELS, FIELD_STATUSES, contract_descriptor, contract_fingerprint
    from referent_candidates import build_candidate_table
    cfg = json.loads(args.config.read_text())
    assert sha(args.archive) == cfg['archiveSha256'] and args.archive.stat().st_size == 88361246
    assert sha(source / 'model.safetensors') == cfg['sourceModelSha256']
    train = repo / 'data/student5_v3_train_v21/train.jsonl.gz'
    targets_path = repo / 'reports/evidence/student5-fp32-cp44/prepared-targets.jsonl.gz'
    assert sha(train) == cfg['trainSha256'] and sha(targets_path) == cfg['preparedTargetsSha256']
    rows = [json.loads(l) for l in gzip.decompress(train.read_bytes()).splitlines()]
    targets = [json.loads(l) for l in gzip.decompress(targets_path.read_bytes()).splitlines()]
    assert len(targets) == 4355
    out.mkdir(parents=True, exist_ok=False)
    random.seed(cfg['seed']); torch.manual_seed(cfg['seed'])
    torch.set_num_threads(cfg['threads']); torch.set_num_interop_threads(1)
    torch.use_deterministic_algorithms(True)
    model = build_model_v3(str(source), local_files_only=True).float()
    for p in model.encoder.parameters():
        p.requires_grad_(False)
    model.eval()
    parameters = parameter_summary_v3(model)
    assert parameters['heads'] == 172088 and parameters['encoderLayers'] == 12
    assert all(p.dtype == torch.float32 for p in model.parameters())
    original_encoder = {k: v.detach().clone() for k, v in model.encoder.state_dict().items()}
    tok = XLMRobertaTokenizerFast.from_pretrained(source, local_files_only=True, from_slow=True)
    run_start = time.perf_counter()
    manifest = {**cfg, 'status': 'PREPARING_FEATURES', 'parameters': parameters, 'python': sys.version, 'platform': platform.platform(), 'cpu': platform.processor(), 'cpuCount': os.cpu_count(), 'cudaAvailable': torch.cuda.is_available(), 'device': 'cpu', 'dependencies': {p: importlib.metadata.version(p) for p in ['torch','transformers','numpy','safetensors','tokenizers','sentencepiece','protobuf']}, 'contractFingerprint': contract_fingerprint(), 'optimizerSteps': 0, 'trainingStarted': False, 'trainingCompleted': False}
    write_json(out / 'training-manifest.json', manifest)
    write_json(out / 'architecture.json', contract_descriptor())
    shutil.copy2(args.config, out / 'training-config.json')
    shutil.copytree(source, out / 'tokenizer-and-source-config', ignore=shutil.ignore_patterns('model.safetensors'))
    code_dir = out / 'source'; code_dir.mkdir()
    for name in ['model_v3.py','contract_v3.py','referent_candidates.py','training_data_v3.py']:
        shutil.copy2(repo / 'matrix_nlu' / name, code_dir / name)
    shutil.copy2(__file__, code_dir / 'train_cp47.py')
    # Cache unique input token sequences in deterministic insertion order.
    sequences = {}
    def register(text):
        encoded = tok(text, truncation=True, max_length=256, return_offsets_mapping=True)
        key = tuple(encoded['input_ids'])
        sequences.setdefault(key, None)
        return key, encoded['offset_mapping']
    for t in targets:
        key = tuple(t['input_ids'][:sum(t['attention_mask'])]); sequences.setdefault(key, None)
    row_specs = {}
    descriptions = {'ctx:speaker': 'speaker: I, me, io, yo', 'ctx:observer': 'listener: you, tu, tú', 'speech-time': 'speech time: now, adesso, ahora', 'context-reference': 'context reference time'}
    desc_keys = {k: register(v)[0] for k, v in descriptions.items()}
    target_specs = []
    idx = 0
    for row in rows:
        full_key, offsets = register(row['text'])
        critical = [s for c in row['claims'] for h in ('subjectSpans','objectSpans') for s in c.get(h, [])]
        table = build_candidate_table(row['text'], row['mentions'], row['context'], critical, 16)
        specs = []
        for c in table['candidates']:
            if c['kind'] == 'MENTION':
                specs.append(('span', full_key, offsets, c['span']))
            elif c['kind'] == 'CONTEXT_ENTITY':
                # Input metadata only; never opaque entity ID or a gold role label.
                text = 'context entity: ' + ' / '.join(c.get('surfaceForms', []))
                specs.append(('text', register(text)[0]))
            else:
                specs.append(('text', desc_keys[c['candidateId']]))
        assert targets[idx]['rowId'] == row['id']
        target_specs.append((specs, [('text', desc_keys['speech-time'])])); idx += 1
        by_claim = {c['claimId']: c for c in row['claims']}
        for c in row['claims']:
            t = targets[idx]; assert t['rowId'] == row['id'] + ':' + c['claimId']
            assert t['role_pointer_values'][:-2] == [x['candidateId'] for x in table['candidates']]
            temporal = {e['temporalId']: e for e in c.get('temporalEvidence', [])}
            anchors = []
            for value in t['temporal_anchor_values']:
                if value in desc_keys:
                    anchors.append(('text', desc_keys[value]))
                elif value.startswith('claim:'):
                    anchors.append(('span', full_key, offsets, by_claim[value[6:]]['sourceSpan']))
                else:
                    anchors.append(('span', full_key, offsets, temporal[value[9:]]['span']))
            target_specs.append((specs, anchors)); idx += 1
    assert idx == len(targets)
    keys = list(sequences)
    with torch.no_grad():
        for start in range(0, len(keys), 32):
            chunk = keys[start:start+32]; n = max(map(len, chunk))
            ids = torch.full((len(chunk), n), tok.pad_token_id, dtype=torch.long)
            mask = torch.zeros_like(ids)
            for j, key in enumerate(chunk):
                ids[j, :len(key)] = torch.tensor(key); mask[j, :len(key)] = 1
            hidden = model.encoder(input_ids=ids, attention_mask=mask).last_hidden_state
            for j, key in enumerate(chunk):
                sequences[key] = hidden[j, :len(key)].clone()
            if start % 320 == 0:
                print(json.dumps({'phase': 'frozen_feature_cache', 'encoded': min(start+32, len(keys)), 'total': len(keys)}), flush=True)
    def feature(spec):
        hidden = sequences[spec[1]]
        if spec[0] == 'text':
            return hidden[1:-1].mean(0)
        indices = [j for j, (a,b) in enumerate(spec[2]) if b > a and a < spec[3][1] and b > spec[3][0]]
        assert indices, spec
        return hidden[indices].mean(0)
    features = []
    status_counts = collections.Counter(); ambiguous = []
    for t, (cs, ans) in zip(targets, target_specs):
        key = tuple(t['input_ids'][:sum(t['attention_mask'])])
        candidates = torch.zeros(16, 384); candidate_mask = torch.zeros(16, dtype=torch.long)
        for i, spec in enumerate(cs):
            candidates[i] = feature(spec); candidate_mask[i] = 1
        anchors = torch.stack([feature(s) for s in ans])
        roles = dict(t['role_pointer_labels'])
        for h in ROLE_HEADS:
            status = t['role_status_labels'][h]
            if status == -100:
                assert roles[h] == -100; continue
            status_counts[FIELD_STATUSES[status]] += 1
            value = t['role_pointer_values'][roles[h]]
            assert (status == 0 and value not in ['NONE','UNKNOWN']) or (status == 3 and value == 'NONE') or (status in [1,2] and value == 'UNKNOWN')
            if value in ['NONE','UNKNOWN']:
                roles[h] = 16 + ['NONE','UNKNOWN'].index(value)
            alts = [v for v,m in zip(t['role_alternative_pointer_labels'][h], t['role_alternative_mask'][h]) if m]
            assert all(0 <= v < len(cs) for v in alts)
            if status == 2:
                assert len(alts) >= 2 and roles[h] == 17
                ambiguous.append({'rowId': t['rowId'], 'head': h, 'status': 'AMBIGUOUS', 'primary': 'UNKNOWN', 'orderedAlternatives': [t['role_pointer_values'][v] for v in alts]})
        features.append((sequences[key], candidates, candidate_mask, anchors, roles))
    assert len(ambiguous) == 14 and len(set(a['rowId'] for a in ambiguous)) == 8
    write_json(out / 'target-consumption.json', {'preparedExamples': len(targets), 'immutablePreparedTargetsSha256': sha(targets_path), 'roleStatusCounts': dict(status_counts), 'g03Fields': ambiguous, 'g03Rows': 8, 'g03FieldsTotal': 14, 'g03AlternativesTotal': sum(len(a['orderedAlternatives']) for a in ambiguous), 'opaqueIdsUsedAsInput': False, 'semanticLabelsUsedAsInput': False, 'teacherForcedTrainingSpans': True})
    def batch(indices):
        n = max(len(features[i][0]) for i in indices); a = max(len(features[i][3]) for i in indices)
        hidden = torch.zeros(len(indices), n, 384); anchors = torch.zeros(len(indices), a, 384); amask = torch.zeros(len(indices), a, dtype=torch.long)
        for j,i in enumerate(indices):
            hidden[j,:len(features[i][0])] = features[i][0]
            anchors[j,:len(features[i][3])] = features[i][3]; amask[j,:len(features[i][3])] = 1
        return hidden, torch.stack([features[i][1] for i in indices]), torch.stack([features[i][2] for i in indices]), anchors, amask
    def flatten_output(pred):
        return {**{'token.'+h: v for h,v in pred['tokens'].items()}, **{'sequence.'+h: v for h,v in pred['sequence'].items() if h != 'temporalRelation'}, 'sequence.temporalRelation': pred['sequence']['temporalRelation']['relation'], 'sequence.temporalAnchor': pred['sequence']['temporalRelation']['anchor']}
    # Numerical proof that caching preserves all seventeen physical outputs.
    ids = list(range(min(8, len(targets)))); b = batch(ids); n = b[0].shape[1]
    with torch.no_grad():
        direct = model(torch.tensor([targets[i]['input_ids'][:n] for i in ids]), torch.tensor([targets[i]['attention_mask'][:n] for i in ids]), *b[1:])
        cached = heads_from_hidden(model, *b)
        # Padded token states are deliberately absent from the cache and carry
        # IGNORE labels. Compare every real token and every sequence output.
        active = torch.tensor([targets[i]['attention_mask'][:n] for i in ids]).bool()
        errors = {}
        for h,v in flatten_output(direct).items():
            difference = (v - flatten_output(cached)[h]).abs()
            errors[h] = (difference[active] if h.startswith('token.') else difference).max().item()
        assert max(errors.values()) < 1e-5, errors
    write_json(out / 'forward-parity.json', {'maxAbsoluteErrorByOutput': errors, 'pass': True})
    def losses(pred, indices):
        flat = flatten_output(pred); terms = {}; counts = {}
        for h, logits in flat.items():
            group, name = h.split('.', 1)
            if group == 'token':
                labels = torch.tensor([targets[i]['token_labels'][name][:logits.shape[1]] for i in indices])
            elif name in ROLE_HEADS:
                labels = torch.tensor([features[i][4][name] for i in indices])
            elif name == 'temporalAnchor':
                labels = torch.tensor([targets[i]['temporal_anchor_label'] for i in indices])
            else:
                labels = torch.tensor([targets[i]['fixed_sequence_labels'][name] for i in indices])
            valid = labels != -100
            counts[h] = int(valid.sum())
            if counts[h]:
                terms[h] = F.cross_entropy(logits.reshape(-1, logits.shape[-1]), labels.reshape(-1), ignore_index=-100)
        alt_terms = []
        for j,i in enumerate(indices):
            for h in ROLE_HEADS:
                if targets[i]['role_status_labels'][h] == 2:
                    alts = [v for v,m in zip(targets[i]['role_alternative_pointer_labels'][h], targets[i]['role_alternative_mask'][h]) if m]
                    logits = pred['sequence'][h][j,:16]
                    # Set probability only: annotation order carries no probability.
                    alt_terms.append(torch.logsumexp(logits[features[i][2].bool()],0) - torch.logsumexp(logits[alts],0))
        if alt_terms:
            terms['diagnostic.alternativeSet'] = torch.stack(alt_terms).mean(); counts['diagnostic.alternativeSet'] = len(alt_terms)
        return terms, counts
    trainable = [p for p in model.parameters() if p.requires_grad]
    optimizer = torch.optim.AdamW(trainable, lr=cfg['learningRate'], betas=tuple(cfg['betas']), eps=cfg['epsilon'], weight_decay=cfg['weightDecay'])
    per_epoch = math.ceil(len(targets) / cfg['batchSize']); total_steps = cfg['epochs'] * per_epoch
    warmup = math.ceil(total_steps * cfg['warmupRatio'])
    def lr_factor(step):
        return (step + 1) / warmup if step < warmup else max(0., (total_steps-step) / (total_steps-warmup))
    scheduler = torch.optim.lr_scheduler.LambdaLR(optimizer, lr_factor)
    manifest.update(status='TRAINING', stepsPerEpoch=per_epoch, plannedSteps=total_steps, warmupSteps=warmup, featurePreparationSeconds=time.perf_counter()-run_start, trainingStarted=True)
    write_json(out / 'training-manifest.json', manifest)
    print(json.dumps({'phase': 'TRAINING_STARTED', 'steps': total_steps, 'trainableParameters': sum(p.numel() for p in trainable)}), flush=True)
    start_train = time.perf_counter(); metrics = []; step = 0
    for epoch in range(1, cfg['epochs']+1):
        model.train(); model.encoder.eval()
        order = torch.randperm(len(targets)).tolist(); sums = collections.Counter(); counts = collections.Counter(); totals = []
        for start in range(0, len(order), cfg['batchSize']):
            indices = order[start:start+cfg['batchSize']]
            optimizer.zero_grad(set_to_none=True)
            pred = heads_from_hidden(model, *batch(indices))
            terms, nums = losses(pred, indices); loss = sum(terms.values())
            assert torch.isfinite(loss)
            loss.backward(); norm = torch.nn.utils.clip_grad_norm_(trainable, cfg['gradientClipNorm'], error_if_nonfinite=True)
            optimizer.step(); scheduler.step(); step += 1
            totals.append(loss.item())
            for h,v in terms.items():
                sums[h] += v.item() * nums[h]; counts[h] += nums[h]
        assert all(torch.equal(v, original_encoder[k]) for k,v in model.encoder.state_dict().items())
        ckpt_id = cfg['runId'] + f'-epoch-{epoch:02d}'
        checkpoint = out / ckpt_id; checkpoint.mkdir()
        model.eval()
        weights = checkpoint / 'model.safetensors'
        save_file({k:v.detach().contiguous() for k,v in sorted(model.state_dict().items())}, str(weights), metadata={'format':'pt'})
        # Store resumable optimizer/RNG state alongside each eligible epoch.
        torch.save({'optimizer':optimizer.state_dict(),'scheduler':scheduler.state_dict(),'torchRng':torch.get_rng_state(),'pythonRng':random.getstate(),'epoch':epoch,'step':step}, checkpoint / 'training-state.pt')
        metric = {'checkpointId':ckpt_id,'epoch':epoch,'step':step,'meanStepTotalLoss':sum(totals)/len(totals),'perHeadMeanLoss':{h:sums[h]/counts[h] for h in sums},'supervisionCounts':dict(counts),'elapsedTrainingSeconds':time.perf_counter()-start_train,'modelBytes':weights.stat().st_size,'modelSha256':sha(weights),'encoderByteIdentical':True,'eligible':True,'selected':False,'metricScope':'TRAIN loss during optimization; not held-out quality'}
        write_json(checkpoint / 'checkpoint.json', metric); metrics.append(metric)
        write_json(out / 'training-metrics.json', metrics)
        print(json.dumps(metric), flush=True)
    assert step == total_steps
    assert sha(args.archive) == cfg['archiveSha256'] and sha(source / 'model.safetensors') == cfg['sourceModelSha256']
    assert sha(train) == cfg['trainSha256'] and sha(targets_path) == cfg['preparedTargetsSha256']
    manifest.update(status='TRAINING_COMPLETED_SELECTION_PENDING', trainingCompleted=True, optimizerSteps=step, trainingDurationSeconds=time.perf_counter()-start_train, totalElapsedSeconds=time.perf_counter()-run_start, checkpointsCreated=len(metrics), selectedCheckpoint=None, encoderUnchanged=True, sourceSnapshotUnchanged=True, trainUnchanged=True, preparedTargetsUnchanged=True, evaluationExecuted=False, frozenUsedForTraining=False)
    write_json(out / 'training-manifest.json', manifest)
    print(json.dumps({'phase':'TRAINING_COMPLETED','durationSeconds':manifest['trainingDurationSeconds'],'checkpoints':len(metrics)}), flush=True)


if __name__ == '__main__':
    main()
