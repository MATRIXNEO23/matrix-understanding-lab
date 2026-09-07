"""Inference-only diagnostics. No NLU labels, training, protected data or network model fetch."""
import json, pathlib, hashlib, sys
import numpy as np
import torch
from transformers import BertModel, XLMRobertaTokenizer

root=pathlib.Path(__file__).parent
modeldir=pathlib.Path(sys.argv[1])
expected='d6e45891d1e0ec4ed023caaeb17c0dd0ae80a93b8bf877d275310b7f2837efa2'
sha=lambda p:hashlib.sha256(p.read_bytes()).hexdigest()
assert sha(modeldir/'model.safetensors')==expected
torch.set_num_threads(2)
torch.manual_seed(41)
model,info=BertModel.from_pretrained(modeldir,local_files_only=True,output_loading_info=True)
assert not info['missing_keys'] and not info['unexpected_keys']
model.eval(); model.requires_grad_(False)
tok=XLMRobertaTokenizer.from_pretrained(modeldir,local_files_only=True)
pairs=json.loads((root/'probes.json').read_text())
texts=list(dict.fromkeys(t for p in pairs for t in (p['left'],p['right'])))
vectors={}; tokens={}
with torch.inference_mode():
 for t in texts:
  encoded=tok(t,return_tensors='pt',truncation=False)
  assert encoded['input_ids'].shape[1]<=512
  hidden=model(**encoded).last_hidden_state
  vector=torch.nn.functional.normalize(hidden.mean(1),dim=-1)[0]
  assert torch.isfinite(hidden).all()
  vectors[t]=vector.tolist()
  ids=encoded['input_ids'][0].tolist()
  tokens[t]={'ids':ids,'pieces':tok.convert_ids_to_tokens(ids),'unknown':ids.count(tok.unk_token_id)}
 results=[dict(p,cosine=float(np.dot(vectors[p['left']],vectors[p['right']])),l2=float(np.linalg.norm(np.array(vectors[p['left']])-vectors[p['right']]))) for p in pairs]
 encoded=tok(texts[0],return_tensors='pt')
 repeat=torch.nn.functional.normalize(model(**encoded).last_hidden_state.mean(1),dim=-1)[0]
 repeatdelta=float(torch.max(torch.abs(repeat-torch.tensor(vectors[texts[0]]))))
assert sha(modeldir/'model.safetensors')==expected
out={'modelSha256':expected,'parameters':sum(p.numel() for p in model.parameters()),'dtype':str(next(model.parameters()).dtype),'loading':info,'repeatMaxDelta':repeatdelta,'torch':torch.__version__,'transformers':__import__('transformers').__version__,'pairs':results,'tokens':tokens,'vectors':vectors,'semantics':'Representation sensitivity only; cosine is NOT role/claim accuracy. Bare backbone has no MATRIX NLU heads.'}
(root/'results.json').write_text(json.dumps(out,ensure_ascii=False,indent=2)+'\n')
print(json.dumps({'texts':len(texts),'pairs':len(pairs),'unknownTokens':sum(x['unknown'] for x in tokens.values()),'repeatMaxDelta':repeatdelta,'parameters':out['parameters']}))
