"""Checkpoint integrity and tensor regression checks, never dataset evaluation."""
import argparse
import hashlib
import json
import pathlib
import sys


def main():
    p = argparse.ArgumentParser()
    p.add_argument('--bundle', type=pathlib.Path, required=True)
    p.add_argument('--source-model', type=pathlib.Path, required=True)
    p.add_argument('--out', type=pathlib.Path, required=True)
    args = p.parse_args()
    root = args.bundle.resolve(); sys.path.insert(0, str(root / 'source'))
    import torch
    from safetensors.torch import load_file
    from transformers import AutoConfig, AutoModel
    from model_v3 import build_model_v3
    from contract_v3 import ROLE_HEADS
    torch.set_num_threads(4); torch.manual_seed(810924)
    assert hashlib.sha256(args.source_model.read_bytes()).hexdigest() == 'd6e45891d1e0ec4ed023caaeb17c0dd0ae80a93b8bf877d275310b7f2837efa2'
    pristine = load_file(str(args.source_model))
    model = build_model_v3(encoder=AutoModel.from_config(AutoConfig.from_pretrained(root / 'tokenizer-and-source-config', local_files_only=True)))
    results = []
    for entry in json.loads((root / 'training-metrics.json').read_text()):
        path = root / entry['checkpointId'] / 'model.safetensors'
        assert path.stat().st_size == entry['modelBytes']
        assert hashlib.sha256(path.read_bytes()).hexdigest() == entry['modelSha256']
        state = load_file(str(path)); model.load_state_dict(state, strict=True)
        assert all(v.dtype == torch.float32 and torch.isfinite(v).all() for v in state.values())
        encoder = {k[8:]:v for k,v in state.items() if k.startswith('encoder.')}
        assert set(encoder) == set(pristine)
        assert all(torch.equal(v, pristine[k]) for k,v in encoder.items())
        results.append({'checkpointId':entry['checkpointId'],'modelSha256':entry['modelSha256'],'strictLoad':True,'allTensorsFiniteFp32':True,'encoderByteIdenticalToRecoveredCp45':True})
    assert len(results) == 10 and len({r['modelSha256'] for r in results}) == 10
    model.eval()
    # Tensor-only unit probe: candidate ordering cannot change corresponding scores.
    candidates = torch.randn(2,16,384); cmask = torch.ones(2,16,dtype=torch.long)
    anchors = torch.randn(2,4,384); amask = torch.ones(2,4,dtype=torch.long)
    ids = torch.tensor([[0,25,50,2],[0,51,26,2]]); mask = torch.ones_like(ids)
    permutation = torch.randperm(16)
    with torch.no_grad():
        a = model(ids,mask,candidates,cmask,anchors,amask)
        b = model(ids,mask,candidates[:,permutation],cmask[:,permutation],anchors,amask)
    errors = {}
    for h in ROLE_HEADS:
        reordered = torch.cat((a['sequence'][h][:,:16][:,permutation],a['sequence'][h][:,16:]),dim=1)
        errors[h] = (reordered-b['sequence'][h]).abs().max().item()
        assert errors[h] < 1e-5
    result = {'checkpoints':results,'candidatePermutationMaxError':errors,'softwareProbeOnly':True,'evaluationExecuted':False,'pass':True}
    args.out.write_text(json.dumps(result,indent=2)+'\n')
    print(json.dumps({'checkpointsVerified':len(results),'strictLoad':'PASS','fp32Finite':'PASS','encoderUnchanged':'PASS','candidatePermutation':'PASS'}))


if __name__ == '__main__':
    main()
