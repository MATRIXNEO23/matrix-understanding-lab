"""CP42 build ONCE. Reads authorized TRAIN v1 only; no model or protected data imports."""
import argparse, collections, copy, gzip, hashlib, json, pathlib, re, sys
ROOT=pathlib.Path(__file__).parent
def js(x): return json.dumps(x,ensure_ascii=False,sort_keys=True,separators=(',',':'))
def sha(b): return hashlib.sha256(b).hexdigest()
def pack(path,rows):
 b=(''.join(js(r)+'\n' for r in rows)).encode();path.write_bytes(gzip.compress(b,mtime=0));return {'path':path.name,'bytes':len(b),'compressedBytes':path.stat().st_size,'sha256':sha(b),'compressedSha256':sha(path.read_bytes())}
def span(text,s):
 start=text.index(s);return [start,start+len(s)]
def main():
 ap=argparse.ArgumentParser();ap.add_argument('--repo',type=pathlib.Path,required=True);ap.add_argument('--out',type=pathlib.Path,required=True);a=ap.parse_args()
 if a.out.exists():raise SystemExit('Output exists: refusing overwrite or post-audit repair')
 p=a.repo/'data/student5_v3';basehash={str(f.relative_to(p)):sha(f.read_bytes()) for f in p.rglob('*') if f.is_file()}
 for l in (p/'SHA256SUMS').read_text().splitlines():
  h,n=l.split(maxsplit=1);assert basehash[n]==h,(n,'input checksum')
 m=json.loads((p/'migration-manifest.json').read_text());raw=b''.join((p/e['path']).read_bytes() for e in m['outputFiles']);assert sha(raw)=='1118a900026f48cfcc290c3f9dc52a1a019a6a1f4761661f326c33770523140e'
 rows=[json.loads(l) for l in raw.decode().splitlines()]; assert len(rows)==3150
 groups=json.loads((a.repo/'reports/evidence/student5-path-b-cp38-repair-spec/annotation-dispositions.json').read_text())['groups']
 ids={g['annotationGroupId']:{x['rowId'] for x in g['storedExampleIds']} for g in groups}
 sys.path.insert(0,str(a.repo/'matrix_nlu'));from contract_v3 import ROLE_HEADS
 out=[];ledger=[];quarantine=[];reviews=[];explicit=[];implicit=[]
 for r in rows:
  original=copy.deepcopy(r); reasons=[];decisions=[]
  if r['id'] in ids['A06']:
   quarantine.append(original);ledger.append({'oldId':r['id'],'newId':None,'disposition':'DEACTIVATED','reason':'CP38 A06 / approved D04 malformed doubled participant; no guessed repair','decisions':['D04'],'oldRowSha256':sha(js(original).encode())});continue
  for c in r['claims']:
   z=c['labels'];text=r['text'][slice(*c['sourceSpan'])]
   if r['language']=='en' and re.match(r'^I\b',text) and not c['subjectSpans']:
    explicit.append([r['id'],c['claimId']]);c['subjectSpans']=[[c['sourceSpan'][0],c['sourceSpan'][0]+1]];reasons.append('CP38 A05 explicit I at claim start; subject evidence only')
   if r['language'] in {'it','es'} and re.match(r'^(mi chiamo|abito|vivo|voglio|vorrei|ho|sono|me llamo|quiero|tengo|soy)\b',text,re.I):implicit.append([r['id'],c['claimId']])
   if r['id'] in ids['A01']:
    surface='attualmente' if 'attualmente' in r['text'] else 'più tardi';c['temporalEvidence']=[{'temporalId':'t0','span':span(r['text'],surface)}];reasons.append('CP38 A01 restore documented temporal evidence')
   if r['id'] in ids['A02']:
    assert z['temporalRelation']['relation']=='CURRENT';decisions.append('D01');reviews.append({'id':r['id'],'decision':'D01','disposition':'PRESERVE_CURRENT','reason':'Present wanting; future cue scopes desired action, not desire state'})
   if r['id'] in ids['A03']:
    # Every indexed row is an explicit report of the named holder's own desire.
    assert 'dice che non vuole' in r['text'];z['perspectiveReferent']=z['subjectReferent'];reasons.append('CP38 A03 named holder reports own desire; viewpoint linguistically that holder');decisions.append('D02')
   if r['id'] in ids['A04']:
    z['claimKind']='BELIEF';reasons.append('CP38 A04 explicit consider/considero mental assessment wrapper, including self-assessment');decisions.append('D03')
   if r['id'] in ids['A07']:
    # Preserve text. Toccare se stessi is a clear reflexive, unlike ambiguous reciprocal baciarsi/abbracciarsi con me.
    if r['id'].endswith('-026'):
     z['targetReferent']='ctx:observer';reasons.append('CP38 A07 toccarti reflexive targets addressee self; con me companion is not reflexive target')
    else:
     z['targetReferent']='UNKNOWN';c['fieldStatusByField']['targetReferent']='AMBIGUOUS';c['interpretationStatus']='AMBIGUOUS';c['alternativesByField']={'targetReferent':[{'value':'ctx:observer','rank':1},{'value':'ctx:speaker','rank':2}]};reasons.append('CP38 A07 reflexive/reciprocal reading not uniquely resolved; preserve text and alternatives, no invented participant')
    decisions.append('D04')
   if r['id'] in ids['A08']:
    assert r['text'].startswith('Voglio ') and z['predicate']=='speech.unresolved';z['predicate']='goal.object';reasons.append('CP38 A08 individually enumerated present desire, mixed-language object, unchanged participant evidence');reviews.append({'id':r['id'],'text':r['text'],'reason':'Overt Voglio frames this object as present desire; English object is not grounds for unresolved predicate'})
   if r['id'] in ids['A09']:
    assert z['polarity']=='POSITIVE' and not c['negationCueSpans'];decisions.append('D05');reviews.append({'id':r['id'],'decision':'D05','disposition':'PRESERVE_POSITIVE_NO_CLAIM_CUE','reason':'Discourse no corrects wording; does not negate positive residence proposition'})
  # Only dataset identity/provenance metadata changes for preserved rows; semantic payload byte-equivalence recorded separately.
  r['datasetId']='student5-matrix-nlu-v3-train-v2';r['provenance']={'kind':'AUTHORIZED_TRAIN_V1_DERIVATIVE','sourceHead':'1396dd6c997ce0dbf5e4a5ce933437c82fc1c217','parentId':original['id'],'parentProvenance':original['provenance'],'disposition':'CORRECTED' if reasons else 'PRESERVED','reason':reasons or ['Preserve inherited curriculum; not blanket semantic certification'],'decisions':sorted(set(decisions)),'language':r['language'],'families':sorted({c.get('family','unspecified') for c in r['claims']}),'heads':sorted({k for c in r['claims'] for k in c['labels']})}
  changes=[{'claimId':c['claimId'],'before':o,'after':c} for o,c in zip(original['claims'],r['claims']) if o!=c]
  ledger.append({'oldId':original['id'],'newId':r['id'],'disposition':r['provenance']['disposition'],'oldRowSha256':sha(js(original).encode()),'newRowSha256':sha(js(r).encode()),'reason':r['provenance']['reason'],'decisions':r['provenance']['decisions'],'changes':changes})
  out.append(r)
 assert len(explicit)==628 and len(implicit)==404,(len(explicit),len(implicit))
 from authored import authored_rows
 added=authored_rows(a.repo)
 for r in added:ledger.append({'oldId':None,'newId':r['id'],'disposition':'NEWLY_AUTHORED','newRowSha256':sha(js(r).encode()),'reason':r['provenance']['reason'],'decisions':r['provenance']['decisions']})
 out+=added;a.out.mkdir(parents=True)
 payload=pack(a.out/'train.jsonl.gz',out);pack(a.out/'provenance-and-mapping.jsonl.gz',ledger);pack(a.out/'quarantine.jsonl.gz',quarantine)
 (a.out/'construction-review.json').write_text(json.dumps({'explicitSubjectIds':explicit,'implicitSubjectPreservationIds':implicit,'semanticDispositions':reviews},ensure_ascii=False,indent=2)+'\n')
 manifest={'id':'student5-matrix-nlu-v3-train-v2','version':'CP42_BUILD_1_AUDIT_LOCKED','startingHead':'1396dd6c997ce0dbf5e4a5ce933437c82fc1c217','baseOrderedSha256':sha(raw),'baseFiles':basehash,'observations':len(out),'claims':sum(len(r['claims']) for r in out),'added':len(added),'dispositions':dict(collections.Counter(x['disposition'] for x in ledger)),'orderedDatasetSha256':payload['sha256'],'orderedHashConvention':'SHA256 concatenation of UTF-8 JSONL shard bytes, lexicographic shard order; one train.jsonl.gz, hash its decompressed bytes. JSON sort_keys=True compact separators newline per row. gzip mtime=0.','trainPayload':payload,'sourceInputs':['data/student5_v3/','reports/evidence/student5-path-b-cp38-repair-spec/annotation-dispositions.json'],'protectedDataRead':False,'trainingExecuted':False,'postAuditCorrectionsExecuted':False}
 (a.out/'manifest.json').write_text(json.dumps(manifest,indent=2)+'\n')
 assert basehash=={str(f.relative_to(p)):sha(f.read_bytes()) for f in p.rglob('*') if f.is_file()}
 (a.out/'BUILD_LOCK.json').write_text(json.dumps({f.name:sha(f.read_bytes()) for f in sorted(a.out.iterdir()) if f.is_file()},indent=2)+'\n')
 print(json.dumps({k:manifest[k] for k in ['observations','claims','added','dispositions','orderedDatasetSha256']}))
if __name__=='__main__':main()
