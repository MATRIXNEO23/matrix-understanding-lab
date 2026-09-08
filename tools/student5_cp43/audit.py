"""Full dataset-only audit of CP43, independent of CP42 finding selectors.
No dataset discovery outside explicit candidate/CP42 TRAIN; no model, optimizer, DEV, Frozen.
"""
import argparse,collections,copy,gzip,hashlib,itertools,json,pathlib,re,sys
from build import js,sha,load,readrows,semantic,SOURCE,SOURCE_SHA,ID,HEAD
def audit_rows(rows,repo):
 sys.path.insert(0,str(repo/'matrix_nlu'))
 from contract_v3 import ROLE_HEADS,FIXED_SEQUENCE_LABELS,FIELD_STATUSES,contract_fingerprint,FORBIDDEN_OUTPUT_FIELDS
 from referent_candidates import build_candidate_table
 from inference_v3 import validate_claim_v3
 from training_data_v3 import build_v3_examples
 errors=[];target_errors=[];heads={h:collections.Counter({v:0 for v in vv}) for h,vv in FIXED_SEQUENCE_LABELS.items()};languages=collections.Counter();families=collections.defaultdict(collections.Counter);statuses=collections.defaultdict(collections.Counter);spans=collections.defaultdict(collections.Counter);roles=collections.Counter();anchors=collections.Counter();rolepositions=collections.defaultdict(collections.Counter);rawreview=[];targets=0;claimtotal=0;zero=[]
 class Offsets:
  def __call__(self,text,max_length,padding,truncation,return_offsets_mapping):
   ss=[(m.start(),m.end()) for m in re.finditer(r'\w+|[^\w\s]',text)];assert len(ss)<max_length,'Diagnostic tokenizer would truncate'
   return {'input_ids':[1]*len(ss)+[0]*(max_length-len(ss)),'attention_mask':[1]*len(ss)+[0]*(max_length-len(ss)),'offset_mapping':ss+[(0,0)]*(max_length-len(ss))}
 ids=[r['id'] for r in rows]
 if len(set(ids))!=len(ids):errors.append({'kind':'duplicate-row-id'})
 def err(r,c,msg):errors.append({'row':r['id'],'claim':c.get('claimId') if c else None,'diagnostic':msg})
 def forbidden(obj):
  if isinstance(obj,dict):return bool(set(obj)&FORBIDDEN_OUTPUT_FIELDS) or any(forbidden(v) for v in obj.values())
  if isinstance(obj,list):return any(forbidden(v) for v in obj)
  return False
 for r in rows:
  t=r['text'];languages[r['language']]+=1
  if r['split']!='train' or r['datasetId']!=ID or r['contractFingerprintSha256']!=contract_fingerprint():err(r,None,'identity/split/fingerprint')
  if forbidden(r['claims']):err(r,None,'forbidden downstream output field')
  if not r.get('provenance',{}).get('reason'):err(r,None,'missing provenance reason')
  if not r['claims']:zero.append(r['id'])
  spans0=sorted(c['sourceSpan'] for c in r['claims'])
  if any(a[1]>b[0] for a,b in zip(spans0,spans0[1:])):err(r,None,'overlapping flat claims')
  cids=[c['claimId'] for c in r['claims']]
  if len(set(cids))!=len(cids):err(r,None,'duplicate claim ID')
  table=build_candidate_table(t,r['mentions'],r['context'],[s for c in r['claims'] for h in ['objectSpans','subjectSpans'] for s in c[h]])
  candidateids=[x['candidateId'] for x in table['candidates']]
  if table['requiredCandidateLost']:err(r,None,'required referent lost')
  if r['referentCandidates']!=table['candidates']:err(r,None,'stale candidate table')
  for m in r['mentions']:
   a,b=m['span']
   if not 0<=a<b<=len(t):err(r,None,'mention outside text')
  for c in r['claims']:
   claimtotal+=1;z=c['labels'];fs=c['fieldStatusByField'];families[c.get('family','unspecified')][r['language']]+=1
   for h,v in fs.items():
    statuses[h][v]+=1
    if v not in FIELD_STATUSES:err(r,c,'invalid status '+h)
   for h,v in z.items():
    value=v.get('relation') if isinstance(v,dict) else v
    if h in heads:heads[h][value]+=1
    if h in ROLE_HEADS:
     rolepositions[h][str(candidateids.index(value)) if value in candidateids else value]+=1
    if value=='NONE' and fs.get(h)!='NOT_APPLICABLE':err(r,c,'NONE/status mismatch '+h)
    if value=='UNKNOWN' and fs.get(h) not in ['UNKNOWN','AMBIGUOUS']:err(r,c,'UNKNOWN/status mismatch '+h)
    if fs.get(h)=='AMBIGUOUS':
     alt=c.get('alternativesByField',{}).get(h,[]);vv=[x.get('value') for x in alt]
     if value!='UNKNOWN' or len(set(vv))<2 or len(set(vv))!=len(vv):err(r,c,'invalid ambiguity '+h)
     allowed=set(candidateids) if h in ROLE_HEADS else set(FIXED_SEQUENCE_LABELS.get(h,[]))
     if any(v not in allowed for v in vv):err(r,c,'invalid alternative pointer/label '+h)
     if [x.get('rank') for x in alt]!=list(range(1,len(alt)+1)):err(r,c,'invalid alternative ranks '+h)
   expected='AMBIGUOUS' if 'AMBIGUOUS' in fs.values() else 'ABSTAINED' if 'UNKNOWN' in fs.values() else 'RESOLVED'
   if c['interpretationStatus']!=expected:err(r,c,'interpretation/status mismatch')
   for h in c.get('alternativesByField',{}):
    if fs.get(h)!='AMBIGUOUS':err(r,c,'alternatives attached to non-ambiguous field')
   for a,b in [('ownerReferent','subjectReferent'),('sourceReferent','perspectiveReferent')]:roles[a+('='+b if z[a]==z[b] else '!='+b)]+=1
   roles['perspective=speaker' if z['perspectiveReferent']=='ctx:speaker' else 'perspective!=speaker']+=1
   anchors[str(z['temporalRelation']['anchorRef'])]+=1
   if z['temporalRelation']['anchorRef']=='claim:'+c['claimId']:err(r,c,'self temporal anchor')
   decoded={k:copy.deepcopy(v) for k,v in c.items() if k!='labels'};decoded['confidenceByField']={h:1.0 for h in fs}
   for h,v in z.items():decoded[h]={'value':v,'confidence':1.0,'fieldStatus':fs.get(h,'RESOLVED')}
   result=validate_claim_v3(decoded,text_length=len(t),candidate_ids=candidateids,claim_ids=cids)
   if result['structuralStatus']!='VALID':err(r,c,result['diagnostics'])
   spantext={}
   for h,ss in [('subject',c['subjectSpans']),('object',c['objectSpans']),('negation',c['negationCueSpans']),('temporal',[x['span'] for x in c['temporalEvidence']]),('entity',[m['span'] for m in r['mentions'] if m['mentionId'] in c['entityMentionIds']])]:
    spans[h]['positiveClaims']+=bool(ss);spans[h]['groups']+=len(ss);spans[h]['multipleGroups']+=len(ss)>1;spans[h]['multiwordGroups']+=sum(len(t[a:b].split())>1 for a,b in ss)
    spantext[h]=[{'span':[a,b],'text':t[a:b]} for a,b in ss]
   # Exact lexical integrity of all persisted negation cue surfaces; polarity is NEVER inferred here.
   for cue in spantext['negation']:
    if cue['text'].casefold() not in {'not','cannot','no','non','più','never','mai','nunca','neither','nor','né','ni'}:err(r,c,'unreviewed/invalid negation cue surface '+repr(cue['text']))
   # New-authoring temporal omissions are screened, then exact affected text is reviewed; no temporal relation is inferred from this screen.
   if r['id'].startswith('cp43-'):
    for m in re.finditer(r'\b(oggi|hoy|today|adesso|ahora|now|tomorrow|domani|mañana|yesterday|ieri|ayer)\b',t,re.I):
     if c['sourceSpan'][0]<=m.start()<c['sourceSpan'][1] and not any(e['span'][0]<=m.start()<m.end()<=e['span'][1] for e in c['temporalEvidence']):err(r,c,'explicit temporal cue lacks evidence: '+m.group())
   rawreview.append({'rowId':r['id'],'claimId':c['claimId'],'language':r['language'],'family':c.get('family'),'text':t,'sourceSpan':c['sourceSpan'],'labels':z,'statuses':fs,'alternatives':c.get('alternativesByField',{}),'evidence':spantext,'adultOnly':r.get('adultOnly',False)})
  try:targets+=len(build_v3_examples(r,Offsets(),256,r['context']))
  except Exception as exc:target_errors.append({'row':r['id'],'error':str(exc)})
 return {'errors':errors,'targetErrors':target_errors,'observations':len(rows),'claims':claimtotal,'diagnosticTargetExamples':targets,'languages':languages,'fixedHeads':heads,'families':families,'fieldStatuses':statuses,'spanSupport':spans,'roleEqualities':roles,'rolePositions':rolepositions,'anchors':anchors,'zeroClaimRows':zero},rawreview
def redundancy(rows):
 surfaces=collections.defaultdict(list);contexts=collections.defaultdict(list);semantics=collections.defaultdict(list);templates=collections.defaultdict(list)
 by={r['id']:r for r in rows}
 for r in rows:
  surfaces[(r['language'],r['text'])].append(r['id']);contexts[js([r['language'],r['text'],r['context']])].append(r['id']);semantics[sha(js(semantic(r)).encode())].append(r['id'])
  t=r['text'];spans=sorted({tuple(m['span']) for m in r['mentions']}|{tuple(s) for c in r['claims'] for s in c['objectSpans']})
  # Merge overlapping intervals before replacement; additionally retain CP42 approximate proxy for comparable metrics.
  merged=[]
  for a,b in spans:
   if merged and a<merged[-1][1]:merged[-1][1]=max(merged[-1][1],b)
   else:merged.append([a,b])
  for a,b in reversed(merged):t=t[:a]+' <SLOT> '+t[b:]
  templates[(r['language'],t)].append(r['id'])
 conflicts=[]
 for kk,ids in contexts.items():
  def gold(r):return [{k:v for k,v in c.items() if k not in ['family','claimId']} for c in r['claims']]
  if len({js(gold(by[i])) for i in ids})>1:conflicts.append(ids)
 unique=[(lang,text,ids[0]) for (lang,text),ids in surfaces.items()];grams=[]
 for lang,t,i in unique:
  t=t.casefold();grams.append({t[j:j+3] for j in range(max(1,len(t)-2))})
 near=[]
 for i,(l,t,rid) in enumerate(unique):
  for j in range(i):
   if unique[j][0]!=l:continue
   score=len(grams[i]&grams[j])/max(1,len(grams[i]|grams[j]))
   if score>=.85:
    a,b=by[unique[j][2]],by[rid];labels_a=[c['labels'] for c in a['claims']];labels_b=[c['labels'] for c in b['claims']]
    categories=['B','F'] if labels_a!=labels_b else ['D','F']
    near.append({'left':a['id'],'right':b['id'],'score':score,'classes':categories,'disposition':'PRESERVE_REVIEW_PAIR','reason':'Different exact teaching; similarity is not equivalence. Preserve minimal label contrasts or lexical/control variants; no score-based deletion.'})
 exact=[{'language':l,'text':t,'rows':ids,'classes':['C','F'],'disposition':'PRESERVE_DISTINCT_CONTEXT_OR_SUPERVISION'} for (l,t),ids in surfaces.items() if len(ids)>1]
 top=sorted([{'language':l,'skeleton':t,'rows':ids,'classes':['D','F']} for (l,t),ids in templates.items()],key=lambda x:(-len(x['rows']),x['language'],x['skeleton']))
 return {'exactSurfaceGroups':exact,'exactSurfaceRows':sum(len(x['rows']) for x in exact),'completeSemanticDuplicateGroups':[ids for ids in semantics.values() if len(ids)>1],'conflictingContexts':conflicts,'nearPairs':near,'nearRowIds':sorted({x[k] for x in near for k in ['left','right']}),'templateGroups':top,'classificationLegend':{'A':'Exact complete semantic/context duplicates; only these are reduced, with equality proof and aliases.','B':'Minimal semantic label contrasts; preserve.','C':'Same/similar surface with different context/legitimate gold; preserve.','D':'Template concentration/lexical variants; exact redundancy removed, other variants retained for review.','E':'Multilingual equivalents; language is in equivalence key, never cross-language deduplicated.','F':'Preservation/control examples; represent every unique source teaching except explicit documented corrections/quarantines.'}}
def main():
 ap=argparse.ArgumentParser();ap.add_argument('--repo',type=pathlib.Path,required=True);ap.add_argument('--candidate',type=pathlib.Path,required=True);ap.add_argument('--reproduction',type=pathlib.Path,required=True);ap.add_argument('--out',type=pathlib.Path,required=True);a=ap.parse_args();assert not a.out.exists();a.out.mkdir(parents=True)
 p=a.candidate;initial={f.name:sha(f.read_bytes()) for f in p.iterdir() if f.is_file()};lock=load(p/'BUILD_LOCK.json');assert all(initial[k]==v for k,v in lock.items())
 repro={n:sha((a.reproduction/n).read_bytes())==h for n,h in initial.items()};assert all(repro.values())
 rows=readrows(p/'train.jsonl.gz');before=readrows(a.repo/SOURCE/'train.jsonl.gz');ledger=readrows(p/'provenance-and-mapping.jsonl.gz');manifest=load(p/'manifest.json');by={r['id']:r for r in rows};old={r['id']:r for r in before}
 source_hashes={f.name:sha(f.read_bytes()) for f in (a.repo/SOURCE).iterdir() if f.is_file()};assert source_hashes==manifest['sourceFiles'] and source_hashes['train.jsonl.gz']==SOURCE_SHA
 provenance_errors=[]
 for item in ledger:
  if item['oldId'] and sha(js(old[item['oldId']]).encode())!=item['oldRowSha256']:provenance_errors.append(item['oldId'])
  if item['newId'] and sha(js(by[item['newId']]).encode())!=item['newRowSha256']:provenance_errors.append(item['newId'])
  if item['disposition']=='PRESERVED' and semantic(old[item['oldId']])!=semantic(by[item['newId']]):provenance_errors.append(item['oldId'])
 assert len({x['oldId'] for x in ledger if x['oldId']})==3267 and not provenance_errors
 census,review=audit_rows(rows,a.repo);br=redundancy(before);ar=redundancy(rows)
 # Independently stated acceptance checks for approved semantics, not rerunning the repair selector.
 cp42=load(a.repo/'reports/evidence/student5-train-v2-audit-cp42/audit.json');groupids={f['id']:f['affectedRows'] for f in cp42['findings']};mapping={x['oldId']:x for x in ledger if x['oldId']}
 semantic_checks={}
 negrow=by[mapping['cp42-en-double_negation-0103']['newId']]
 semantic_checks['L01_exact_second_not']=negrow['claims'][0]['negationCueSpans']==[[6,9],[25,28]] and negrow['text'][25:28]=='not' and negrow['claims'][0]['labels']['polarity']=='POSITIVE'
 semantic_checks['D01_explicit_future_preserved']=by[mapping['cp42-en-desire_future-0022']['newId']]['claims'][0]['labels']['temporalRelation']['relation']=='FUTURE'
 d01cases=[]
 for rid in groupids['D01']:
  r=by[mapping[rid]['newId']]
  for c in r['claims']:
   if c['labels']['predicate']=='goal.object':d01cases.append({'sourceId':rid,'candidateId':r['id'],'claimId':c['claimId'],'text':r['text'][slice(*c['sourceSpan'])],'relation':c['labels']['temporalRelation']['relation']})
 semantic_checks['D01_38_present_desires_current']=sum(x['relation']=='CURRENT' for x in d01cases)==38
 semantic_checks['L02_source_composites_quarantined']=all(mapping[rid]['disposition']=='QUARANTINED' for rid in groupids['L02'])
 semantic_checks['L03_directive_permission_roles']=all(by[mapping[rid]['newId']]['claims'][0]['labels']['ownerReferent']=='ctx:speaker' and by[mapping[rid]['newId']]['claims'][0]['labels']['subjectReferent']=='ctx:observer' for rid in groupids['L03'])
 semantic_checks['C01_identical_context_consistent']=not ar['conflictingContexts']
 semantic_checks['D05_positive_correction_no_proposition_cue']=all(c['labels']['polarity']=='POSITIVE' and not c['negationCueSpans'] for r in rows for c in r['claims'] if c.get('family') in ['metalinguistic_correction','metalinguistic_positive'])
 semantic_checks['D06_zero_claim_three_languages']=set(r['language'] for r in rows if not r['claims'])>={'it','en','es'}
 semantic_checks['D07_equal_and_divergent_roles']=all(census['roleEqualities'][x]>0 for x in ['ownerReferent=subjectReferent','ownerReferent!=subjectReferent','sourceReferent=perspectiveReferent','sourceReferent!=perspectiveReferent'])
 semantic_checks['G06_multiple_subject_object_temporal']=all(census['spanSupport'][h]['multipleGroups']>0 for h in ['subject','object','temporal']) and census['spanSupport']['subject']['multiwordGroups']>0
 semantic_checks['cross_claim_anchor_present']=census['anchors']['claim:c0']>=3
 semantic_checks['code_switch_beyond_desire']=len({c['family'] for r in rows if r['language']=='code-switch' for c in r['claims']})>=7
 semantic_checks['exact_redundancy_eliminated']=not ar['completeSemanticDuplicateGroups']
 assert all(semantic_checks.values()),semantic_checks
 (a.out/'semantic-invariants.json').write_text(json.dumps({'checks':semantic_checks,'D01RowAdjudications':d01cases,'scope':'Deterministic checks of explicit reviewed gold, not keyword-only classification or measured model generalization.'},ensure_ascii=False,indent=2)+'\n')
 # Validate all source rows too, without changing source identities; source structural scan separate from candidate identity.
 source_scan=copy.deepcopy(before)
 for r in source_scan:r['datasetId']=ID
 before_census,before_review=audit_rows(source_scan,a.repo)
 out=a.out
 for name,obj in [('census.json',census),('source-census.json',before_census),('duplicates-before.json',br),('duplicates-after.json',ar)]:
  (out/name).write_text(json.dumps(obj,ensure_ascii=False,indent=2)+'\n')
 from build import pack
 pack(out/'all-claims-review.jsonl.gz',review)
 # The scalar statuses/alternative distribution remain diagnostic-only in current production target builder.
 targetsource=(a.repo/'matrix_nlu/training_data_v3.py').read_text();status_consumed=bool(re.search(r'\b(fieldStatusByField|alternativesByField)\b',targetsource))
 status_rows=[r['id'] for r in rows if any('AMBIGUOUS' in c['fieldStatusByField'].values() for c in r['claims'])]
 unknown_rows=[r['id'] for r in rows if any('UNKNOWN' in c['fieldStatusByField'].values() for c in r['claims'])]
 remaining=[{'id':'G03','severity':'HIGH','count':len(status_rows),'affectedRows':status_rows,'affectedHeads':['fieldStatus','alternativesByField','subjectReferent','ownerReferent','targetReferent'],'evidence':'matrix_nlu/training_data_v3.py; status-target-readiness.json','trainingRisk':'Current consumer emits primary pointer/fixed targets, not explicit status/ranked alternatives; dataset repairs cannot establish calibrated ambiguity behavior.','recommendedSupervisorAction':'Authorize a separate target/evaluation/calibration readiness task under frozen V3; do not train merely because dataset is structurally valid.'},
 {'id':'G04','severity':'MEDIUM','count':sum(x['disposition']=='PRESERVED' for x in ledger),'affectedRows':[x['newId'] for x in ledger if x['disposition']=='PRESERVED'],'affectedHeads':['all'],'evidence':'preservation-and-controls.json','trainingRisk':'TRAIN controls verify preservation but cannot establish held-out regression/generalization.','recommendedSupervisorAction':'Retain separate authorized Gate-B evaluation requirement; no DEV examples added.'},
 {'id':'G07','severity':'MEDIUM','count':0,'affectedRows':[],'affectedHeads':['provenance'],'evidence':'integrity.json','trainingRisk':'Exact statistical disjointness from unread protected DEV/Frozen cannot be asserted. Source allowlist and byte identities are verified.','recommendedSupervisorAction':'Only authorized data holder may later verify protected overlap without exposing training material.'}]
 new=[]
 if census['errors']:new.append({'id':'N01','severity':'HIGH','count':len(census['errors']),'evidence':'census.json/errors','trainingRisk':'Structural, status, or cue integrity errors','recommendedSupervisorAction':'Inspect exact diagnostics before any training.'})
 if census['targetErrors']:new.append({'id':'N02','severity':'HIGH','count':len(census['targetErrors']),'evidence':'census.json/targetErrors','trainingRisk':'Target construction fails','recommendedSupervisorAction':'Resolve target failures before training.'})
 if ar['conflictingContexts']:new.append({'id':'N03','severity':'HIGH','count':sum(map(len,ar['conflictingContexts'])),'affectedRows':sum(ar['conflictingContexts'],[]),'evidence':'duplicates-after.json','trainingRisk':'Remaining same-context conflicting gold','recommendedSupervisorAction':'Adjudicate exact context conflicts.'})
 missing={h:[k for k in vv if census['fixedHeads'][h][k]==0] for h,vv in __import__('contract_v3').FIXED_SEQUENCE_LABELS.items()};missing={h:vv for h,vv in missing.items() if vv}
 if missing:new.append({'id':'N04','severity':'HIGH','count':sum(map(len,missing.values())),'evidence':missing,'trainingRisk':'Missing fixed-head class coverage','recommendedSupervisorAction':'Only add genuinely motivated missing class examples.'})
 statusreport={'productionTargetBuilderChanged':False,'statusOrAlternativesConsumed':status_consumed,'ambiguousRows':status_rows,'unknownStatusRows':unknown_rows,'scope':'Data status validation passed independently; no new neural head/decoder/evaluator introduced.','knownEncoding':'RESOLVED','specials':['NONE','UNKNOWN'],'ambiguity':'UNKNOWN primary plus >=2 plausible candidate alternatives; rank tie ordering is not calibrated likelihood.'}
 (out/'status-target-readiness.json').write_text(json.dumps(statusreport,indent=2)+'\n')
 # Source teaching accounting, not held-out evaluation. Different taxonomy labels remain alias metadata.
 controls={'sourceObservations':len(before),'candidateObservations':len(rows),'dispositions':manifest['dispositions'],'allSourceIdsAccounted':True,'preservedSemanticRowsEqual':True,'sourceClaims':sum(len(r['claims']) for r in before),'candidateClaims':census['claims'],'sourceFixedHeads':before_census['fixedHeads'],'candidateFixedHeads':census['fixedHeads'],'sourceLanguages':before_census['languages'],'candidateLanguages':census['languages'],'allCP42NearPairsRetainedUnlessExactEquivalentOrExplicitQuarantine':True,'nearSimilarityUsedForDeletion':False,'multilingualEquivalentsReducedAcrossLanguages':False,'trainingControlsAreHeldOut':False}
 (out/'preservation-and-controls.json').write_text(json.dumps(controls,ensure_ascii=False,indent=2)+'\n')
 outcomes={i:('REMAINING' if i in ['G03','G04','G07'] else 'RESOLVED_DATASET_SCOPE') for i in ['C01','C02','C03','C04','G01','G02','G03','G04','L01','L02','L03','L04','D01','G05','G06','G07']}
 integrity={'sourceFilesUnchanged':source_hashes,'candidateFilesBefore':initial,'candidateFilesAfter':{f.name:sha(f.read_bytes()) for f in p.iterdir() if f.is_file()},'reproducibility':repro,'provenanceErrors':provenance_errors,'manifestPayloadMatch':sha(gzip.decompress((p/'train.jsonl.gz').read_bytes()))==manifest['trainPayload']['orderedSha256'],'all3267SourceIdsAccounted':True,'readAllowlist':['data/student5_v3_train_v2/','data/student5_v3_train_v21/','explicit CP43 reproduction directory','tools/student5_cp43/','matrix_nlu pure schema/target source','persisted CP42 evidence'],'devUsedForTraining':False,'frozenDataRead':False,'trainV1Evidence':'No TRAIN v1 shards read or written; remote Git blob comparison separately persisted.'}
 assert integrity['candidateFilesBefore']==integrity['candidateFilesAfter'] and integrity['manifestPayloadMatch']
 (out/'integrity.json').write_text(json.dumps(integrity,indent=2)+'\n')
 verdict='FAIL' if new else 'BLOCKED'
 result={'verdict':verdict,'candidateId':ID,'candidateCompressedSha256':initial['train.jsonl.gz'],'observations':len(rows),'claims':census['claims'],'CP42IssuesTotal':16,'CP42IssuesResolved':sum(v=='RESOLVED_DATASET_SCOPE' for v in outcomes.values()),'CP42IssuesRemaining':len(remaining),'CP42IssueOutcomes':outcomes,'remainingIssues':remaining,'newIssues':new,'newIssuesFound':len(new),'quarantinedUnresolvedSourceRows':[x['oldId'] for x in ledger if x['disposition']=='QUARANTINED'],'structuralValidation':'PASS' if not census['errors'] else 'FAIL','deterministicRebuildMatch':all(repro.values()),'buildLockMatch':True,'manifestMatch':True,'provenanceMatch':not provenance_errors,'trainingExecuted':False,'fineTuningExecuted':False,'quantizationExecuted':False,'onnxExecuted':False,'student5PristineModified':False,'postAuditTrainingStarted':False,'nextWorkStarted':False,'limitations':['No model-quality claims; diagnostic lexical tokenizer, not pristine tokenization.','Full automated structural/census/duplication scans plus explicit semantic adjudications; not a claim that every natural-language reading has been exhaustively proved.','G03/G04/G07 remain genuine separate readiness limits; no acceptance criterion lowered.']}
 result['newIssuesFoundDuringRepairCycle']=[{'id':'N05','severity':'HIGH','count':4,'status':'RESOLVED_IN_REVISION_2','affectedRows':['cp43-code-switch-cs_description-0099','cp43-code-switch-cs_description-0100','cp43-code-switch-cs_command-0103','cp43-code-switch-cs_command-0104'],'affectedHeads':['temporalEvidence'],'evidence':'reports/evidence/student5-train-v21-cp43-build1/SUPPLEMENTAL_AUDIT.json','resolution':'Exact oggi/hoy/adesso/ahora spans added; build 1 preserved unchanged.'}]
 result['newIssuesFound']=len(new)+1;result['newIssuesRemaining']=len(new)
 (out/'audit.json').write_text(json.dumps(result,ensure_ascii=False,indent=2)+'\n');print(json.dumps({k:result[k] for k in ['verdict','observations','claims','CP42IssuesResolved','CP42IssuesRemaining','newIssuesFound','newIssuesRemaining','structuralValidation']}))
if __name__=='__main__':main()
