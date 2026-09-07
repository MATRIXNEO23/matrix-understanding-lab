"""CP42 immutable-candidate audit. Writes ONLY --audit; no fixes, training or model imports."""
import argparse,collections,copy,gzip,hashlib,itertools,json,pathlib,re,sys
def sha(b):return hashlib.sha256(b).hexdigest()
def key(x):return json.dumps(x,ensure_ascii=False,sort_keys=True,separators=(',',':'))
def read(p):return [json.loads(l) for l in gzip.decompress(p.read_bytes()).splitlines()]
def main():
 ap=argparse.ArgumentParser();ap.add_argument('--repo',type=pathlib.Path,required=True);ap.add_argument('--candidate',type=pathlib.Path,required=True);ap.add_argument('--audit',type=pathlib.Path,required=True);ap.add_argument('--reproduction',type=pathlib.Path,required=True);a=ap.parse_args()
 assert not a.audit.exists(),'Audit output must be new';a.audit.mkdir(parents=True)
 lock=json.loads((a.candidate/'BUILD_LOCK.json').read_text());assert all(sha((a.candidate/p).read_bytes())==h for p,h in lock.items())
 initial={p.name:sha(p.read_bytes()) for p in a.candidate.iterdir() if p.is_file()}
 rows=read(a.candidate/'train.jsonl.gz');ledger=read(a.candidate/'provenance-and-mapping.jsonl.gz');quarantine=read(a.candidate/'quarantine.jsonl.gz');m=json.loads((a.candidate/'manifest.json').read_text());byid={r['id']:r for r in rows}
 sys.path.insert(0,str(a.repo/'matrix_nlu'))
 from contract_v3 import ROLE_HEADS,FIXED_SEQUENCE_LABELS,FIELD_STATUSES,contract_fingerprint
 from referent_candidates import build_candidate_table
 from training_data_v3 import build_v3_examples
 from inference_v3 import validate_claim_v3
 findings=[]
 def issue(code,severity,ids,heads,evidence,consequence,recommendation):
  findings.append({'id':code,'severity':severity,'affectedRows':sorted(set(ids)),'affectedHeads':heads,'evidence':evidence,'likelyTrainingConsequence':consequence,'recommendedCorrection':recommendation,'correctionApplied':False})
 langs=collections.Counter();heads={h:collections.Counter({v:0 for v in vals}) for h,vals in FIXED_SEQUENCE_LABELS.items()};roles={h:collections.Counter() for h in ROLE_HEADS};bylang={};families=collections.defaultdict(collections.Counter);statuses=collections.defaultdict(collections.Counter);spans=collections.defaultdict(collections.Counter);anchors=collections.Counter();candcounts=collections.Counter();roleeq=collections.Counter();kindpos=collections.defaultdict(collections.Counter);register=collections.Counter();adult=collections.defaultdict(collections.Counter);slices=collections.defaultdict(list)
 structural=[];targets=[];support=collections.defaultdict(collections.Counter);examples=0;problems=[];rawspan=[];zero=[];template=collections.defaultdict(list);exact=collections.defaultdict(list);ctxgroups=collections.defaultdict(list)
 class DiagnosticOffsets:
  def __call__(self,t,max_length,padding,truncation,return_offsets_mapping):
   offsets=[(m.start(),m.end()) for m in re.finditer(r'\w+|[^\w\s]',t)];assert len(offsets)<max_length
   n=len(offsets);return {'input_ids':[1]*n+[0]*(max_length-n),'attention_mask':[1]*n+[0]*(max_length-n),'offset_mapping':offsets+[(0,0)]*(max_length-n)}
 for r in rows:
  rid=r['id'];lang=r['language'];langs[lang]+=1;pr=r.get('provenance',{});register[pr.get('register','inherited-unclassified')]+=1
  if r.get('split')!='train' or not pr or not pr.get('reason') or r['datasetId']!='student5-matrix-nlu-v3-train-v2':problems.append(rid)
  if r['contractFingerprintSha256']!=contract_fingerprint():structural.append({'row':rid,'diagnostics':['fingerprint']})
  exact[(lang,r['text'])].append(rid);ctxgroups[key([lang,r['text'],r['context']])].append(rid)
  s=r['text'];replacements=sorted({tuple(m['span']) for m in r['mentions']}|{tuple(x) for c in r['claims'] for x in c['objectSpans']},reverse=True)
  for start,end in replacements:s=s[:start]+' <SLOT> '+s[end:]
  template[(lang,s)].append(rid)
  if not r['claims']:zero.append(rid)
  table=build_candidate_table(r['text'],r['mentions'],r['context'],[s for c in r['claims'] for k in ['objectSpans','subjectSpans'] for s in c[k]])
  candidateids=[x['candidateId'] for x in table['candidates']];candcounts[len(candidateids)]+=1
  for mn in r['mentions']:
   if not 0<=mn['span'][0]<mn['span'][1]<=len(r['text']):rawspan.append({'row':rid,'kind':'mention','span':mn['span'],'length':len(r['text'])})
  for c in r['claims']:
   z=c['labels'];fam=c.get('family','unspecified');families[fam][lang]+=1;slices['language:'+lang].append(rid);slices['family:'+fam].append(rid)
   if pr['disposition']=='PRESERVED':slices['A_preserved_curriculum'].append(rid)
   else:slices['B_new_or_repaired'].append(rid)
   for h,v in z.items():
    if h in ROLE_HEADS:
     roles[h][v.split(':')[0] if v.startswith(('mention:','entity:')) else v]+=1
     idx=candidateids.index(v) if v in candidateids else v;kindpos[h][str(idx)]+=1
    else:
     value=v['relation'] if h=='temporalRelation' else v
     heads[h][value]+=1;bylang.setdefault(lang,{}).setdefault(h,collections.Counter())[value]+=1
   for h,v in c['fieldStatusByField'].items():statuses[h][v]+=1
   if any(v not in FIELD_STATUSES for v in c['fieldStatusByField'].values()):structural.append({'row':rid,'diagnostics':['invalid field status']})
   roleeq['owner=subject' if z['ownerReferent']==z['subjectReferent'] else 'owner!=subject']+=1
   roleeq['source=perspective' if z['sourceReferent']==z['perspectiveReferent'] else 'source!=perspective']+=1
   roleeq['perspective=speaker' if z['perspectiveReferent']=='ctx:speaker' else 'perspective!=speaker']+=1
   anchors[str(z['temporalRelation']['anchorRef'])]+=1
   for h,ss in [('object',c['objectSpans']),('subject',c['subjectSpans']),('negation',c['negationCueSpans']),('temporal',[x['span'] for x in c['temporalEvidence']]),('entity',[x['span'] for x in r['mentions'] if x['mentionId'] in c['entityMentionIds']])]:
    spans[h]['positiveClaims']+=bool(ss);spans[h]['groups']+=len(ss);spans[h]['multipleGroups']+=len(ss)>1;spans[h]['multiwordGroups']+=sum(len(r['text'][s:e].split())>1 for s,e in ss)
   decoded={k:v for k,v in c.items() if k!='labels'};decoded['confidenceByField']={k:1.0 for k in c['fieldStatusByField']}
   for h,v in z.items():decoded[h]={'value':v,'confidence':1.0,'fieldStatus':c['fieldStatusByField'].get(h,'RESOLVED')}
   val=validate_claim_v3(decoded,text_length=len(r['text']),candidate_ids=candidateids,claim_ids=[x['claimId'] for x in r['claims']])
   if val['structuralStatus']!='VALID':structural.append({'row':rid,'claim':c['claimId'],'diagnostics':val['diagnostics']})
   if r.get('adultOnly'):adult[fam][lang]+=1;slices['D_adult'].append(rid)
   if any(x in ['UNKNOWN','AMBIGUOUS'] for x in c['fieldStatusByField'].values()):slices['E_uncertainty'].append(rid)
   if len(candidateids)>2:slices['F_binding'].append(rid)
   if c['negationCueSpans'] or z['polarity']!='POSITIVE':slices['G_negation_scope'].append(rid)
   if c['temporalEvidence']:slices['H_temporal'].append(rid)
  try:
   ex=build_v3_examples(r,DiagnosticOffsets(),256,r['context']);examples+=len(ex)
   for e in ex:
    for h,vs in e['token_labels'].items():support[h].update(v for v in vs if v!=-100)
  except Exception as exc:targets.append({'row':rid,'error':str(exc)})
 if structural or rawspan:issue('S01','CRITICAL',[x['row'] for x in structural+rawspan],['boundary','object','subject','entity','temporal'],'Existing V3 invariant validator / strict mention bounds reject stored annotations; full details in structural.json','Invalid offsets/pointers can misalign supervision','Review each affected original/new annotation; do not silently clamp offsets')
 if targets:issue('S02','CRITICAL',[x['row'] for x in targets],['target_builder'],'Existing pure target builder raises; diagnostic lexical offsets only','Candidate cannot be consumed consistently','Review recorded errors before authorizing dataset repair')
 if problems:issue('P01','CRITICAL',problems,['provenance'],'Missing provenance or incorrect identity/split','Untraceable training inputs','Restore explicit provenance via separately authorized correction')
 # All exact contexts with conflicting semantic payload; no majority vote, no deduplication performed.
 conflicts=[]
 def semantic(r):return [{k:v for k,v in c.items() if k not in ['family','claimId']} for c in r['claims']]
 for k,ids in ctxgroups.items():
  if len({key(semantic(byid[i])) for i in ids})>1:conflicts.append({'rows':ids,'variants':len({key(semantic(byid[i])) for i in ids})})
 if conflicts:issue('C01','HIGH',[i for g in conflicts for i in g['rows']],['all semantic labels'],'Identical language/text/context has different semantic payload; conflict groups persisted','Contradictory supervision or inconsistent span/status conventions','Adjudicate full-context equivalence; no automatic majority or similarity deletion')
 dup=[{'language':l,'text':t,'rows':ids} for (l,t),ids in exact.items() if len(ids)>1]
 if dup:issue('C02','MEDIUM',[i for g in dup for i in g['rows']],['all'],'Repeated exact surfaces retained; context may differ. Full groups in redundancy.json','Repetition can dominate scarce repair families','Review exact semantic equivalence with aliases; preserve true contextual contrasts')
 top=sorted([{'language':l,'skeleton':s,'rows':ids} for (l,s),ids in template.items()],key=lambda g:(-len(g['rows']),g['language'],g['skeleton']))
 issue('C03','MEDIUM',top[0]['rows'],['all'],{'largestSkeleton':top[0]['skeleton'],'rows':len(top[0]['rows']),'definition':'Object/entity span replacement; overlapping replacements are an approximate proxy'},'Residual template shortcuts and low lexical variety','Review concentration by semantic family, preserve valid simple examples')
 unique=[(l,t,ids[0]) for (l,t),ids in exact.items()];near=[]
 def grams(t):t=t.casefold();return {t[i:i+3] for i in range(max(1,len(t)-2))}
 gg=[grams(t) for l,t,i in unique]
 for i,(l,t,rid) in enumerate(unique):
  for j in range(i):
   if unique[j][0]!=l:continue
   score=len(gg[i]&gg[j])/max(1,len(gg[i]|gg[j]))
   if score>=.85:near.append({'left':unique[j][2],'right':rid,'trigramJaccard':score})
 if near:issue('C04','MEDIUM',[x[k] for x in near for k in ['left','right']],['all'],{'screen':'Within-language unique surface character-trigram Jaccard >= 0.85','pairs':len(near)},'Near-template concentration; similarity is not equivalence','Review pairs only; do not delete or relabel by score')
 missing={h:[v for v in vals if heads[h][v]==0] for h,vals in FIXED_SEQUENCE_LABELS.items()};missing={h:v for h,v in missing.items() if v}
 if missing:issue('G01','HIGH',[],list(missing),{'zeroSupport':missing},'Full V3 class coverage remains incomplete','Author genuinely uncertain act/kind/time cases where linguistically justified, never pad UNKNOWN counts')
 issue('G02','HIGH',[r['id'] for r in rows if r['id'].startswith('cp42')],['dialogueAct','temporalRelation','sourceReferent','perspectiveReferent'],{'newRows':m['added'],'familyLanguageCounts':{f:dict(v) for f,v in families.items() if not f.startswith(('v2','v22')) and any(r['id'].startswith('cp42') and any(c.get('family')==f for c in r['claims']) for r in rows)}},'New families have only one/few constructions per language; nonzero support does not establish adequate diversity','Supervisor should review breadth and naturally varied contrasts before training')
 issue('G03','HIGH',[r['id'] for r in rows if any(c['fieldStatusByField'].get('subjectReferent')=='AMBIGUOUS' for c in r['claims'])],['subjectReferent','ownerReferent','fieldStatus'],{'targetBuilder':'training_data_v3.py reads labels but does not consume fieldStatusByField/alternativesByField','changed':False},'UNKNOWN pointer is teachable but ranked ambiguity/field-status distinction is not a dedicated supervised target here','Keep this as separate Gate-B target/evaluation readiness blocker; do not modify evaluator/decoder in this task')
 issue('G04','MEDIUM',slices['A_preserved_curriculum'],['all'],{'sliceIndex':'slices.json','heldOutEvaluationCreated':False},'Training preservation controls cannot independently measure generalization/regression','Supervisor must specify separately authorized evaluation; no DEV/Frozen derivation now')
 # Exhaustive CP38 indexed group disposition plus explicit manual finding on the new double-negation annotation.
 badneg=[r['id'] for r in rows if r['id'].startswith('cp42-en-double_negation')]
 issue('L01','HIGH',badneg,['negation'],{'text':byid[badneg[0]]['text'],'storedSpans':byid[badneg[0]]['claims'][0]['negationCueSpans'],'storedText':[byid[badneg[0]]['text'][s:e] for s,e in byid[badneg[0]]['claims'][0]['negationCueSpans']]},'Second cue supervises part of like rather than not','Correct second not span to [24,27) after Supervisor approval; current payload is untouched')
 hes=[r['id'] for r in rows if r['id'].startswith('cp42') and 'adult_hesitation' in r['id']]
 issue('L02','HIGH',hes,['boundary','negation','polarity','claimKind'],'Hesitation examples combine desire, disjunction and epistemic uncertainty in one flat claim; Spanish second no in no sé is not separately preserved','Scope/atomization may teach inconsistent cue coverage and uncertainty composition','Supervisor adjudicate flat V3 scope and proposition boundaries per language; no correction applied')
 permiss=[r['id'] for r in rows if r['id'].startswith('cp42') and any(x in r['id'] for x in ['owner_subject_permission','command','request','grammatical_reflexive'])]
 issue('L03','HIGH',permiss,['subjectReferent','ownerReferent','targetReferent','predicate'],'New directives/permission use action-subject distinct from request/consent owner; semantic convention needs specific Supervisor review, not artificial identity divergence','Potential inconsistency with inherited request targets where owner=subject','Approve/adjudicate each construction against V3 role semantics before any corrective task')
 issue('L04','HIGH',['mx-v22a-adult-it-015','mx-v22a-adult-it-025','mx-v22a-adult-it-026'],['targetReferent','ownerReferent'],'A07 two reciprocal/reflexive forms now AMBIGUOUS; toccarti targets self; inherited owner convention retained','Current candidate mixes inherited request-owner convention with new directives; ambiguity may be conservatively overused','Review these three preserved texts individually; do not guess or silently normalize')
 future=[]
 for r in rows:
  for c in r['claims']:
   if c['labels']['predicate']=='goal.object' and c['labels']['temporalRelation']['relation']=='FUTURE' and re.search(r'\b(want|voglio|quiero)\b',r['text'][slice(*c['sourceSpan'])],re.I):future.append(r['id'])
 if future:issue('D01','HIGH',future,['temporalRelation'],'Legacy FUTURE goal rows with overt present want/voglio/quiero remain outside the 23 CURRENT A02 preservation group; all screened IDs retained','Potential contradiction of approved present-desire convention','Adjudicate each remaining desire-time scope; do not mass-flip keyword matches')
 cs=[r['id'] for r in rows if r['language']=='code-switch']
 issue('G05','MEDIUM',cs,['all'],{'codeSwitchRows':len(cs),'families':dict(collections.Counter(c.get('family') for r in rows if r['language']=='code-switch' for c in r['claims']))},'Code-switch remains concentrated in desire; borrowed-term monolingual tags are separate','Broaden natural mixed-language contextual families; preserve intelligible slang/adult cases as resolved when warranted')
 if spans['subject']['multipleGroups']==0 or spans['subject']['multiwordGroups']==0:issue('G06','MEDIUM',[],['subject','entity','object','temporal'],dict(spans),'Positive multiword/plural groups remain sparse or absent; head coverage not equal span-variety coverage','Add linguistically justified multiword persons and multiple evidence groups after review')
 issue('G07','MEDIUM',[],['all'],{'statisticalDevDisjointness':'NOT_CHECKED','sourceAllowlist':'authorized TRAIN v1 and project-authored declarations only','devRead':False,'frozenRead':False},'Provenance isolation is demonstrated; exact overlap with inaccessible protected payloads is not asserted','Keep protected-data protocol; authorized holder may perform future permitted separation check without leaking examples')
 base=a.repo/'data/student5_v3';baseok=all(sha((base/p).read_bytes())==h for p,h in m['baseFiles'].items())
 repro={p:sha((a.reproduction/p).read_bytes())==h for p,h in initial.items()};assert all(repro.values()),repro
 review=json.loads((a.candidate/'construction-review.json').read_text())
 census={'observations':len(rows),'claims':sum(len(r['claims']) for r in rows),'languages':langs,'fixedHeads':heads,'headsByLanguage':bylang,'roleKinds':roles,'roleCandidatePositions':kindpos,'roleEqualities':roleeq,'fieldStatuses':statuses,'positiveSpanSupport':spans,'diagnosticLexicalBioCounts':support,'diagnosticTargetExamples':examples,'anchors':anchors,'candidateCounts':candcounts,'families':families,'adultFamilies':adult,'register':register,'claimFreeRows':zero}
 verdict='FAIL' if any(f['severity'] in ['HIGH','CRITICAL'] for f in findings) else 'PASS'
 audit={'verdict':verdict,'candidateSha256':m['orderedDatasetSha256'],'candidateFilesBefore':initial,'candidateFilesAfter':{p.name:sha(p.read_bytes()) for p in a.candidate.iterdir() if p.is_file()},'reproducibilityFiles':repro,'base130FilesUnchanged':baseok,'provenanceComplete':not problems,'completeV1Accounting':len([x for x in ledger if x['oldId']])==3150,'structuralInvalidClaims':len(structural),'targetBuilderErrors':len(targets),'D01_D07':{'D01':'23 A02 preserved CURRENT; remaining FUTURE present-want screen recorded as defect risk','D02':'8 report viewpoint fixes plus 6 new explicit independent-source/viewpoint rows','D03':'6 indexed wrapper corrections plus 3 new BELIEF/3 DIRECT controls','D04':'6 quarantine; 3 indexed reflexive dispositions; new grammatical/nonproposition controls; L04 unresolved','D05':'indexed correction preserved positive without proposition cue; 3 new positive corrected residence examples','D06':'6 zero-claim observations; 3 ambiguous and 3 resolved same-surface contexts; G03 target status limitation','D07':'new role/topic swaps, source-viewpoint and owner/action-subject distinctions; L03 semantic review remains'},'explicitSubjectClaims':len(review['explicitSubjectIds']),'implicitSubjectControls':len(review['implicitSubjectPreservationIds']),'findings':findings,'scope':{'trainingExecuted':False,'quantizationExecuted':False,'onnxExecuted':False,'student5PristineModified':False,'trainV1Modified':False,'devUsedForTraining':False,'frozenDataRead':False,'postAuditCorrectionsExecuted':False,'nextWorkStarted':False}}
 assert audit['candidateFilesBefore']==audit['candidateFilesAfter'] and baseok
 for name,obj in [('audit.json',audit),('census.json',census),('structural.json',{'invariants':structural,'mentionBounds':rawspan,'targetErrors':targets}),('redundancy.json',{'exactSurfaceGroups':dup,'conflictingContexts':conflicts,'templateGroups':top,'nearPairs':near}),('slices.json',{k:sorted(set(v)) for k,v in slices.items()})]:
  (a.audit/name).write_text(json.dumps(obj,ensure_ascii=False,indent=2)+'\n')
 print(json.dumps({'verdict':verdict,'structuralInvalid':len(structural),'targetErrors':len(targets),'findings':[(x['id'],x['severity'],len(x['affectedRows'])) for x in findings],'languages':langs,'roleEqualities':roleeq,'fixedHeads':heads},ensure_ascii=False))
if __name__=='__main__':main()
