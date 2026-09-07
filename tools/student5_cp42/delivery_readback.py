import base64, concurrent.futures, hashlib, json, pathlib, urllib.request, gzip
entries=json.loads(pathlib.Path('cp42-readback-entries.json').read_text())
out=pathlib.Path('cp42-remote-readback');out.mkdir(exist_ok=True)
def fetch(e):
 req=urllib.request.Request('https://api.github.com/repos/MATRIXNEO23/matrix-understanding-lab/git/blobs/'+e['sha'],headers={'Accept':'application/vnd.github+json'})
 with urllib.request.urlopen(req,timeout=45) as response:
  j=json.load(response)
 assert j['encoding']=='base64'
 b=base64.b64decode(j['content']);expected=(pathlib.Path('cp42-delivery')/e['path']).read_bytes()
 assert b==expected,e['path']
 target=out/e['path'];target.parent.mkdir(parents=True,exist_ok=True);target.write_bytes(b)
 return {'path':e['path'],'gitBlobSha':j['sha'],'bytes':len(b),'sha256':hashlib.sha256(b).hexdigest(),'exactReadback':True}
with concurrent.futures.ThreadPoolExecutor(max_workers=4) as pool:results=list(pool.map(fetch,entries))
checks=(out/'reports/evidence/student5-train-v2-audit-cp42/SHA256SUMS').read_text().splitlines()
for line in checks:
 h,p=line.split(maxsplit=1);assert hashlib.sha256((out/p).read_bytes()).hexdigest()==h,p
candidate=out/'data/student5_v3_train_v2';m=json.loads((candidate/'manifest.json').read_text());raw=gzip.decompress((candidate/'train.jsonl.gz').read_bytes());assert hashlib.sha256(raw).hexdigest()==m['orderedDatasetSha256']
rows=[json.loads(l) for l in raw.splitlines()];assert len(rows)==m['observations'] and sum(len(r['claims']) for r in rows)==m['claims']
audit=json.loads((out/'reports/evidence/student5-train-v2-audit-cp42/audit.json').read_text())
assert all(hashlib.sha256((candidate/p).read_bytes()).hexdigest()==h for p,h in audit['candidateFilesAfter'].items())
bad=next(r for r in rows if r['id']=='cp42-en-double_negation-0103')
result={'files':results,'manifestChecks':len(checks),'orderedDatasetSha256':m['orderedDatasetSha256'],'observations':len(rows),'claims':sum(len(r['claims']) for r in rows),'auditedCandidateExact':True,'wrongSpanPreserved':bad['claims'][0]['negationCueSpans']==[[6,9],[28,31]],'access':'Direct GitHub REST Git Blob API application/vnd.github+json; base64 decode. Text-only connector binary read rejected; direct REST succeeded.'}
pathlib.Path('cp42-remote-receipt.json').write_text(json.dumps(result,indent=2)+'\n')
print(json.dumps({k:v for k,v in result.items() if k!='files'}))
