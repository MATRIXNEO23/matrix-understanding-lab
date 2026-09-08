"""Apply explicit CP43 repair ledger to immutable CP42 bytes; never loads a model."""
import argparse,collections,copy,gzip,hashlib,json,pathlib,sys
HERE=pathlib.Path(__file__).parent
SOURCE='data/student5_v3_train_v2';DEST='data/student5_v3_train_v21'
SOURCE_SHA='b6acf41e6634c2f89e6b8251fb5f816ec60fb0ca1cd6c90dfcbed46c2c12584c'
HEAD='270a0729c20ede548fe373f488029241fcbb35a3';ID='student5-matrix-nlu-v3-train-v2.1-cp43r2'
def js(x):return json.dumps(x,ensure_ascii=False,sort_keys=True,separators=(',',':'))
def sha(b):return hashlib.sha256(b).hexdigest()
def load(p):return json.loads(p.read_text())
def readrows(p):return [json.loads(l) for l in gzip.decompress(p.read_bytes()).splitlines()]
def semantic(r):
 x={k:copy.deepcopy(r.get(k)) for k in ['text','language','context','mentions','referentCandidates','adultOnly','contractVersion','contractFingerprintSha256']}
 x['claims']=[{k:copy.deepcopy(v) for k,v in c.items() if k!='family'} for c in r['claims']]
 return x
def fielddiff(a,b,p=''):
 if isinstance(a,dict) and isinstance(b,dict):
  return [d for k in sorted(set(a)|set(b)) for d in fielddiff(a.get(k),b.get(k),p+'/'+k)]
 if isinstance(a,list) and isinstance(b,list) and len(a)==len(b):
  return [d for i,(x,y) in enumerate(zip(a,b)) for d in fielddiff(x,y,p+'/'+str(i))]
 return [] if a==b else [{'path':p,'before':a,'after':b}]
def construct(repo):
 p=repo/SOURCE;assert sha((p/'train.jsonl.gz').read_bytes())==SOURCE_SHA
 source_hashes={q.name:sha(q.read_bytes()) for q in p.iterdir() if q.is_file()}
 assert all(source_hashes[k]==v for k,v in load(p/'BUILD_LOCK.json').items())
 old=readrows(p/'train.jsonl.gz');assert len(old)==3267
 spec=load(HERE/'repairs.json')['rows'];sys.path.insert(0,str(repo/'matrix_nlu'))
 from referent_candidates import build_candidate_table
 review=[];interim=[];quarantine=[]
 original={r['id']:r for r in old}
 for r0 in old:
  r=copy.deepcopy(r0);s=spec.get(r['id']);reasons=[];issues=[]
  if s:
   assert s['text']==r['text'],r['id'];reasons=s['reasons'];issues=s['issues']
   for u in s['updates']:
    loc=r
    for k in u['path'][:-1]:loc=loc[k]
    loc[u['path'][-1]]=copy.deepcopy(u['value'])
  if s and s['quarantine']:
   quarantine.append({'sourceRow':r0,'disposition':'QUARANTINED','issues':issues,'reason':reasons});review.append({'oldId':r0['id'],'oldRowSha256':sha(js(r0).encode()),'newId':None,'disposition':'QUARANTINED','reason':reasons,'issues':issues,'beforeAfter':[]});continue
  # Keep status/value consistency after explicit field changes. This is representation normalization, not semantic prediction.
  for c in r['claims']:
   fs=c['fieldStatusByField'];z=c['labels']
   for h,value in z.items():
    v=value.get('relation') if isinstance(value,dict) else value
    if v=='NONE':fs[h]='NOT_APPLICABLE'
    elif v=='UNKNOWN':fs[h]='AMBIGUOUS' if h in c.get('alternativesByField',{}) else 'UNKNOWN'
    elif h not in c.get('alternativesByField',{}):fs[h]='RESOLVED'
   c['interpretationStatus']='AMBIGUOUS' if 'AMBIGUOUS' in fs.values() else 'ABSTAINED' if 'UNKNOWN' in fs.values() else 'RESOLVED'
  critical=[span for c in r['claims'] for k in ['objectSpans','subjectSpans'] for span in c[k]]
  r['referentCandidates']=build_candidate_table(r['text'],r['mentions'],r['context'],critical)['candidates']
  changes=fielddiff(semantic(r0),semantic(r));disposition='CORRECTED' if changes else 'PRESERVED'
  if changes and not reasons:reasons=['Normalize field status to exact stored label/alternatives; no lexical or semantic relabeling.']
  reasons=reasons or ['Preserve complete inherited semantic teaching; not a blanket certification of unseen linguistic interpretations.']
  review.append({'oldId':r0['id'],'oldRowSha256':sha(js(r0).encode()),'newId':r['id'],'disposition':disposition,'reason':reasons,'issues':issues,'beforeAfter':changes})
  interim.append(r)
 # Deduplicate only full byte-canonical semantic equality including complete context, candidates, all spans/status/alternatives.
 groups=collections.defaultdict(list)
 for r in interim:groups[sha(js(semantic(r)).encode())].append(r)
 rev={x['oldId']:x for x in review};kept=[];exact_groups=[]
 for key,rr in groups.items():
  representative=rr[0];aliases=[r['id'] for r in rr[1:]]
  if aliases:
   exact_groups.append({'classification':'A','semanticSha256':key,'representativeId':representative['id'],'sourceIds':[r['id'] for r in rr],'proof':'Complete language/text/context/mentions/candidate table/claims (except family taxonomy) equality; no near-similarity deletion.','deactivatedCount':len(aliases)})
  for r in rr[1:]:
   v=rev[r['id']];v['preDedupDisposition']=v['disposition'];v['disposition']='DEACTIVATED_EXACT_REDUNDANT';v['newId']=representative['id'];v['representativeId']=representative['id'];v['equivalenceSha256']=key;v['issues']=sorted(set(v['issues']+['C02','C03','C04']));v['reason'].append('Exact complete teaching equals retained representative after authorized repairs; retain original bytes in quarantine and alias identity, reduce repeated exposure.')
   quarantine.append({'sourceRow':original[r['id']],'repairedSemanticRow':r,'disposition':v['disposition'],'representativeId':representative['id'],'reason':v['reason']})
  v=rev[representative['id']];representative['datasetId']=ID
  representative['provenance']={'kind':'AUTHORIZED_CP42_DERIVATIVE','sourceHead':HEAD,'sourceDatasetId':'student5-matrix-nlu-v3-train-v2','sourcePayloadSha256':SOURCE_SHA,'parentId':representative['id'],'parentRowSha256':sha(js(original[representative['id']]).encode()),'parentProvenance':original[representative['id']]['provenance'],'disposition':v['disposition'],'reason':v['reason'],'issues':v['issues'],'aliases':aliases,'aliasFamilies':sorted({c.get('family','unspecified') for rr0 in rr for c in rr0['claims']}),'protectedDataUsed':False}
  kept.append(representative)
 from authored import authored_rows
 added=authored_rows(repo);out=kept+added;by={r['id']:r for r in out};assert len(by)==len(out)
 for v in review:
  if v['newId']:v['newRowSha256']=sha(js(by[v['newId']]).encode())
 for r in added:review.append({'oldId':None,'newId':r['id'],'newRowSha256':sha(js(r).encode()),'disposition':'NEWLY_AUTHORED','reason':[r['provenance']['reason']],'issues':['G01','G02','G05','G06'],'beforeAfter':[{'path':'/','before':None,'after':semantic(r)}]})
 # Every original affected ID is accounted for, including overlap, preserved decisions and aliases.
 cp42=load(repo/'reports/evidence/student5-train-v2-audit-cp42/audit.json');issue_rows=[]
 for issue in cp42['findings']:
  entries=[copy.deepcopy(rev[rid]) for rid in issue['affectedRows']]
  issue_rows.append({'issueId':issue['id'],'originalSeverity':issue['severity'],'originalCount':len(issue['affectedRows']),'rowDispositions':entries,'globalIssue':not entries})
 assert len([v for v in review if v['oldId']])==3267
 return out,review,quarantine,exact_groups,issue_rows,source_hashes
def pack(path,rows):
 b=(''.join(js(r)+'\n' for r in rows)).encode();path.write_bytes(gzip.compress(b,mtime=0));return {'path':path.name,'rows':len(rows),'uncompressedBytes':len(b),'compressedBytes':path.stat().st_size,'orderedSha256':sha(b),'compressedSha256':sha(path.read_bytes())}
def main():
 ap=argparse.ArgumentParser();ap.add_argument('--repo',type=pathlib.Path,required=True);ap.add_argument('--out',type=pathlib.Path,required=True);a=ap.parse_args();a.repo=a.repo.resolve();assert not a.out.exists(),'Refuse to overwrite any existing candidate'
 rows,ledger,q,groups,issues,source_hashes=construct(a.repo)
 a.out.mkdir(parents=True)
 payload=pack(a.out/'train.jsonl.gz',rows);pack(a.out/'provenance-and-mapping.jsonl.gz',ledger);pack(a.out/'quarantine.jsonl.gz',q);pack(a.out/'correction-register.jsonl.gz',issues)
 (a.out/'exact-redundancy-decisions.json').write_text(json.dumps(groups,ensure_ascii=False,indent=2)+'\n')
 inputpaths=[a.repo/SOURCE/n for n in source_hashes]+[HERE/'repairs.json',HERE/'authored.py',HERE/'build.py',a.repo/'matrix_nlu/contract_v3.py',a.repo/'matrix_nlu/referent_candidates.py',a.repo/'reports/evidence/student5-train-v2-audit-cp42/audit.json']
 manifest={'id':ID,'version':'CP43_REPAIR_2_AUDIT_LOCKED','startingHead':HEAD,'sourceId':'student5-matrix-nlu-v3-train-v2','sourcePath':SOURCE,'sourceCompressedSha256':SOURCE_SHA,'sourceFiles':source_hashes,'baseTrainV1OrderedSha256':'1118a900026f48cfcc290c3f9dc52a1a019a6a1f4761661f326c33770523140e','observations':len(rows),'claims':sum(len(r['claims']) for r in rows),'dispositions':dict(collections.Counter(v['disposition'] for v in ledger)),'languages':dict(collections.Counter(r['language'] for r in rows)),'trainPayload':payload,'inputs':{str(p.relative_to(a.repo)):sha(p.read_bytes()) for p in inputpaths},'method':'Read immutable CP42; apply exact reviewed row specifications; representation status normalization; full-semantic exact redundancy reduction with aliases; explicitly authored targeted additions. No source v1 rebuilding.','knownStatusEncoding':'KNOWN means RESOLVED in frozen Contract V3; NONE=NOT_APPLICABLE, UNKNOWN unresolved, AMBIGUOUS primary UNKNOWN plus genuine ranked alternatives.','trainingExecuted':False,'fineTuningExecuted':False,'quantizationExecuted':False,'onnxExecuted':False,'devUsedForTraining':False,'frozenDataRead':False}
 (a.out/'manifest.json').write_text(json.dumps(manifest,ensure_ascii=False,indent=2)+'\n')
 lock={p.name:sha(p.read_bytes()) for p in sorted(a.out.iterdir())};(a.out/'BUILD_LOCK.json').write_text(json.dumps(lock,indent=2)+'\n')
 (a.out/'SHA256SUMS').write_text(''.join(sha(p.read_bytes())+'  '+p.name+'\n' for p in sorted(a.out.iterdir()) if p.name!='SHA256SUMS'))
 assert source_hashes=={p.name:sha(p.read_bytes()) for p in (a.repo/SOURCE).iterdir() if p.is_file()}
 print(json.dumps({k:manifest[k] for k in ['id','observations','claims','languages','dispositions','trainPayload']},ensure_ascii=False))
if __name__=='__main__':main()
