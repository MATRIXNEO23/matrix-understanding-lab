"""CP37 read-only TRAIN curriculum census. No model/DEV/Frozen access.

Unicode lexical BIO counts use the existing pure target builder, not the BERT
tokenizer. They measure annotation support, never actual training gradients.
Family predicates and heuristic review screens are explicit below.
"""
import argparse, ast, collections as C, difflib, hashlib, json, math, pathlib, re, sys

LANGS=('it','en','es','code-switch')
def sha(b): return hashlib.sha256(b).hexdigest()
def canon(x): return json.dumps(x,sort_keys=True,ensure_ascii=False,separators=(',',':'))
def counts(items): return dict(C.Counter(items))
def norm(s): return ' '.join(s.casefold().split())
def spans_text(r,spans): return [r['text'][a:b] for a,b in spans]
def snap(r,c):
    return {'rowId':r['id'],'claimId':c['claimId'],'language':r['language'],'text':r['text'][slice(*c['sourceSpan'])],'sourceSpan':c['sourceSpan'],'labels':c['labels'],'subjectSpans':spans_text(r,c['subjectSpans']),'negationCues':spans_text(r,c['negationCueSpans']),'temporalEvidence':spans_text(r,[t['span'] for t in c['temporalEvidence']]),'family':c['family'],'context':r['context']}

class LexicalAuditTokenizer:
    def __call__(self,text,**kw):
        off=[(m.start(),m.end()) for m in re.finditer(r"\w+(?:['’]\w+)*|[^\w\s]",text)]
        limit=kw['max_length']; assert len(off)<=limit
        return {'input_ids':[1]*len(off)+[0]*(limit-len(off)),'attention_mask':[1]*len(off)+[0]*(limit-len(off)),'offset_mapping':off+[(0,0)]*(limit-len(off))}

def main():
    ap=argparse.ArgumentParser();ap.add_argument('--train',type=pathlib.Path,required=True);ap.add_argument('--source',type=pathlib.Path,required=True);ap.add_argument('--tree',type=pathlib.Path,required=True);ap.add_argument('--output',type=pathlib.Path,required=True);a=ap.parse_args()
    assert a.train.name=='student5_v3';sys.path.insert(0,str(a.source))
    from contract_v3 import TOKEN_LABELS,FIXED_SEQUENCE_LABELS,ROLE_HEADS,contract_fingerprint
    from training_data_v3 import build_v3_examples
    meta=json.loads(a.tree.read_text());entries={e['path']:e for e in meta['entries']}
    man=json.loads((a.train/'migration-manifest.json').read_text());raw=b''.join((a.train/e['path']).read_bytes() for e in man['outputFiles']);assert sha(raw)==man['outputChecksum']
    rows=[json.loads(l) for l in raw.splitlines() if l]; assert all(r['split']=='train' for r in rows)
    inputchecks=[]
    for path,e in entries.items():
        f=a.train/path.removeprefix('data/student5_v3/') if path.startswith('data/student5_v3/') else a.source.parent/path
        if not f.is_file():continue
        b=f.read_bytes();h=hashlib.sha1(b'blob '+str(len(b)).encode()+b'\0'+b).hexdigest();assert h==e['sha'],path
        inputchecks.append({'path':path,'gitBlobSha':h,'sha256':sha(b),'bytes':len(b)})
    claims=[(r,c) for r in rows for c in r['claims']]
    seq={h:{v:{l:0 for l in LANGS} for v in vs} for h,vs in FIXED_SEQUENCE_LABELS.items()}
    seq_unique={h:C.defaultdict(set) for h in seq};roles={h:C.defaultdict(C.Counter) for h in ROLE_HEADS};role_indices={h:C.Counter() for h in ROLE_HEADS}
    token={h:{v:{l:0 for l in LANGS} for v in vs} for h,vs in TOKEN_LABELS.items()}
    support={h:{'examples':0,'positiveExamples':0,'groups':0,'multipleGroupExamples':0,'byLanguage':{l:{'examples':0,'positiveExamples':0,'groups':0} for l in LANGS}} for h in TOKEN_LABELS}
    status=C.defaultdict(C.Counter);anchors=C.defaultdict(C.Counter);kindcounts=C.Counter(); all_templates=C.defaultdict(list); surfaceclaims=C.defaultdict(list)
    flags=C.defaultdict(list);cue_surface=C.defaultdict(C.Counter);temporal_surface=C.defaultdict(C.Counter); cue_polarity=C.defaultdict(C.Counter); role_equal=C.Counter();role_positions=C.defaultdict(C.Counter)
    # Catalog-based screens are bounded evidence review, not a general parser.
    tree=ast.parse((a.source/'train_v3_migration.py').read_text());catalog={}
    for n in tree.body:
        if isinstance(n,ast.Assign) and isinstance(n.targets[0],ast.Name) and n.targets[0].id in ('NEGATION_CUES','TEMPORAL_EXPRESSIONS'):catalog[n.targets[0].id]=ast.literal_eval(n.value)
    extra_temporal={'en':('yesterday','used to'),'it':('ieri','attualmente','più tardi'),'es':('ayer',)}
    families={k:[] for k in ['negation_polarity_negative','negation_overt_cue','simple_temporal_non_atemporal','temporal_evidence','advanced_temporal','subject_non_speaker','target_present','owner_non_speaker','perspective_non_speaker','source_differs_perspective','source_differs_subject','third_party_report','belief','hypothesis','request','command','correction','goal_desire_all','goal_desire_assertion','preference','entity_spans','subject_spans','object_spans','multi_claim','ambiguity','abstained','unknown_any_field','unresolved_predicate','adult_consent','adult_refusal_excluding_withdrawal','adult_withdrawal','adult_desire_assertion','adult_request','adult_code_switch','adult_arousal_lexical_screen','ownership_sensitive_non_speaker']}
    for r in rows:
        examples=build_v3_examples(r,LexicalAuditTokenizer(),256,r['context'])
        for ex in examples:
            kindcounts[ex['kind']]+=1
            for h,ys in ex['token_labels'].items():
                valid=[v for v in ys if v!=-100]
                if not valid:continue
                s=support[h];positive=any(v>0 for v in valid);groups=sum(TOKEN_LABELS[h][v].startswith('B-') for v in valid)
                s['examples']+=1;s['positiveExamples']+=positive;s['groups']+=groups;s['multipleGroupExamples']+=groups>1
                for k,v in [('examples',1),('positiveExamples',int(positive)),('groups',groups)]:s['byLanguage'][r['language']][k]+=v
                for v in valid:token[h][TOKEN_LABELS[h][v]][r['language']]+=1
            if ex['kind']=='claim':
                for h,v in ex['role_pointer_labels'].items():role_indices[h][str(v)]+=1
        for c in r['claims']:
            l=r['language'];z=c['labels'];text=r['text'][slice(*c['sourceSpan'])];cl=(r,c);low=text.casefold(); key=(l,norm(text));surfaceclaims[key].append(cl)
            for h in seq:
                v=z[h]['relation'] if h=='temporalRelation' else z[h];seq[h][v][l]+=1;seq_unique[h][v].add(key)
            for h in ROLE_HEADS:
                v=z[h];role_kind=('MENTION' if v.startswith('mention:') else 'CONTEXT_ENTITY' if v.startswith('entity:') else v);roles[h][role_kind][l]+=1
                if v.startswith('mention:'):
                    m=next(m for m in r['mentions'] if 'mention:'+m['mentionId']==v);pos=m['span'][0]-c['sourceSpan'][0];role_positions[h]['atClaimStart' if pos==0 else 'laterInClaim' if pos>0 else 'earlierOutsideClaim']+=1
            for h in ['ownerReferent','perspectiveReferent','sourceReferent']:role_equal[h+'EqualsSubject']+=z[h]==z['subjectReferent']
            role_equal['sourceEqualsPerspective']+=z['sourceReferent']==z['perspectiveReferent']
            for h,v in c['fieldStatusByField'].items():status[h][v]+=1
            status['interpretationStatus'][c['interpretationStatus']]+=1
            anchors[str(z['temporalRelation']['anchorRef'])][l]+=1
            for cue in spans_text(r,c['negationCueSpans']):cue_surface[l][cue.casefold()]+=1
            for t in spans_text(r,[t['span'] for t in c['temporalEvidence']]):temporal_surface[l][t.casefold()]+=1
            cue_polarity['withCue' if c['negationCueSpans'] else 'withoutCue'][z['polarity']]+=1
            adv=z['temporalRelation']['relation'] in {'BEFORE','AFTER','DURING','RECURRENT','AT_REFERENCE'}
            adult=r.get('adultOnly',False);wd='withdrawal' in c['family'];pred=z['predicate'];act=z['dialogueAct'];unknown=any(v=='UNKNOWN' for v in c['fieldStatusByField'].values())
            tests=[z['polarity']=='NEGATIVE',bool(c['negationCueSpans']),z['temporalRelation']['relation'] in {'CURRENT','PAST','FUTURE'},bool(c['temporalEvidence']),adv,z['subjectReferent']!='ctx:speaker',z['targetReferent'] not in {'NONE','UNKNOWN'},z['ownerReferent']!='ctx:speaker',z['perspectiveReferent']!='ctx:speaker',z['sourceReferent']!=z['perspectiveReferent'],z['sourceReferent']!=z['subjectReferent'],z['claimKind']=='REPORT',z['claimKind']=='BELIEF',z['claimKind']=='HYPOTHESIS',act=='REQUEST',act=='COMMAND',act=='CORRECT',pred=='goal.object',pred=='goal.object' and act=='ASSERT',pred=='preference.like',bool(c['entityMentionIds']),bool(c['subjectSpans']),bool(c['objectSpans']),len(r['claims'])>1,c['interpretationStatus']=='AMBIGUOUS',c['interpretationStatus']=='ABSTAINED',unknown,pred=='speech.unresolved',adult and pred=='consent.grant',adult and pred=='consent.refuse' and not wd,adult and wd,adult and pred=='goal.object' and act=='ASSERT',adult and act=='REQUEST',adult and l=='code-switch',adult and bool(re.search(r'\b(eccitat\w*|arous\w*|horny|excitad\w*)\b',low)),z['ownerReferent']!='ctx:speaker']
            assert len(tests)==len(families)
            for fam,yes in zip(families,tests):
                if yes:families[fam].append(cl)
            lang='it' if l=='code-switch' else l
            for category,names,annotated in [('cueCatalogMismatch',catalog['NEGATION_CUES'].get(lang,()),c['negationCueSpans']),('temporalCatalogMissing',catalog['TEMPORAL_EXPRESSIONS'].get(lang,())+extra_temporal.get(lang,()),[t['span'] for t in c['temporalEvidence']])]:
                for phrase in names:
                    for m in re.finditer(r'(?<!\w)'+re.escape(phrase)+r'(?!\w)',low):
                        start,end=m.start()+c['sourceSpan'][0],m.end()+c['sourceSpan'][0]
                        if not any(s<=start and e>=end for s,e in annotated):flags[category].append({'phrase':phrase,**snap(r,c)})
            if any(s==c['sourceSpan'] for s in c['negationCueSpans']):flags['fullSourceNegationSpan'].append(snap(r,c))
            if z['subjectReferent']=='ctx:speaker' and not c['subjectSpans']:flags['speakerEmptySubject'].append(snap(r,c))
            pronoun={'it':'io','en':'i','es':'yo','code-switch':'io'}[l]
            if re.match(r'^'+pronoun+r'\b',low) and not c['subjectSpans']:flags['explicitFirstPersonEmptySubjectScreen'].append(snap(r,c))
            # Delexicalized annotated surface skeleton, not a semantic-equivalence claim.
            spans=[(s,e,'<VALUE>') for s,e in c['objectSpans']]+[(m['span'][0],m['span'][1],'<'+m['entityType']+'>') for m in r['mentions'] if c['sourceSpan'][0]<=m['span'][0]<m['span'][1]<=c['sourceSpan'][1]]
            chosen=[]
            for s,e,label in sorted(spans,key=lambda v:(v[0],-(v[1]-v[0]),v[2])):
                if not any(s<ee and e>ss for ss,ee,_ in chosen):chosen.append((s,e,label))
            skel=text
            for s,e,label in sorted(chosen,reverse=True):skel=skel[:s-c['sourceSpan'][0]]+label+skel[e-c['sourceSpan'][0]:]
            all_templates[(l,norm(skel))].append(cl)
    def family_info(items):
        return {'claims':len(items),'rows':len({r['id'] for r,c in items}),'uniqueClaimSurfaces':len({(r['language'],norm(r['text'][slice(*c['sourceSpan'])])) for r,c in items}),'byLanguage':{l:sum(r['language']==l for r,c in items) for l in LANGS},'uniqueByLanguage':{l:len({norm(r['text'][slice(*c['sourceSpan'])]) for r,c in items if r['language']==l}) for l in LANGS}}
    def fingerprint(r,c):
        start=c['sourceSpan'][0];z=dict(c['labels']);cand={d['candidateId']:d for d in r['referentCandidates']}
        for h in ROLE_HEADS:
            v=z[h];d=cand.get(v,{})
            if d.get('span'):z[h]={'relativeSpan':[x-start for x in d['span']],'entityType':d.get('entityType')}
            elif d.get('resolvedEntityRef'):z[h]={'kind':d['kind'],'ref':d['resolvedEntityRef']}
        return canon({'labels':z,**{k:[[s-start,e-start] for s,e in c[k]] for k in ['subjectSpans','objectSpans','negationCueSpans']},'temporalEvidence':[[x['span'][0]-start,x['span'][1]-start] for x in c['temporalEvidence']],'mentions':[{'span':[m['span'][0]-start,m['span'][1]-start],'type':m['entityType']} for m in r['mentions'] if c['sourceSpan'][0]<=m['span'][0]<m['span'][1]<=c['sourceSpan'][1]],'interpretationStatus':c['interpretationStatus'],'fieldStatus':c['fieldStatusByField']})
    rowgroups=C.defaultdict(list)
    for r in rows:rowgroups[(r['language'],r['text'])].append(r)
    conflict=[]; contextvariants=[]
    for key,items in rowgroups.items():
        samecontext=C.defaultdict(list)
        for r in items:samecontext[canon(r['context'])].append(r)
        for ctx,rr in samecontext.items():
            if len({canon([fingerprint(r,c) for c in r['claims']]) for r in rr})>1:conflict.append({'language':key[0],'text':key[1],'rowIds':[r['id'] for r in rr]})
        if len(samecontext)>1:contextvariants.append({'language':key[0],'text':key[1],'rowIds':[r['id'] for r in items]})
    claim_conflicts=[]
    for key,items in surfaceclaims.items():
        byctx=C.defaultdict(list)
        for r,c in items:byctx[canon(r['context'])].append((r,c))
        for ctx,cc in byctx.items():
            if len({fingerprint(r,c) for r,c in cc})>1:claim_conflicts.append({'language':key[0],'text':key[1],'examples':[snap(r,c) for r,c in cc[:8]],'count':len(cc),'status':'REVIEW_REQUIRED_CLAIM_CONTEXT_MAY_DIFFER'})
    near=[];near_nodes=set();bylang=C.defaultdict(list)
    for key,items in rowgroups.items():bylang[key[0]].append((norm(key[1]),items))
    for l,vals in bylang.items():
        for i,(x,xitems) in enumerate(vals):
            for y,yitems in vals[i+1:]:
                if x==y or min(len(x),len(y))/max(len(x),len(y))<0.85:continue
                ratio=difflib.SequenceMatcher(None,x,y,autojunk=False).ratio()
                if ratio>=0.90:
                    near_nodes.update([r['id'] for r in xitems+yitems]);near.append({'language':l,'ratio':ratio,'leftId':xitems[0]['id'],'rightId':yitems[0]['id'],'leftText':x,'rightText':y,'multiplicity':len(xitems)+len(yitems),'sequenceGoldDiffers':xitems[0]['claims'][0]['labels']!=yitems[0]['claims'][0]['labels']})
    templ=sorted(all_templates.items(),key=lambda kv:(-len(kv[1]),kv[0]));freq=[len(v) for _,v in templ]
    examples={'heuristicReviewScreens':{k:{'count':len(v),'byLanguage':counts(x['language'] for x in v),'examples':v[:20]} for k,v in flags.items()},'sameObservationContextConflicts':conflict,'sameTextDifferentContextGroups':contextvariants,'claimSurfaceGoldReviewGroups':claim_conflicts,'nearDuplicatePairsTotal':len(near),'nearDuplicatePairsFirst50':near[:50],'templateGroups':[{'language':k[0],'skeleton':k[1],**family_info(v),'exampleIds':[v[0][0]['id'],v[0][1]['claimId']]} for k,v in templ]}
    for h,values in seq.items():
        for v,langs in values.items():langs['total']=sum(langs.values());langs['uniqueClaimSurfaces']=len(seq_unique[h][v])
    result={'scope':'TRAIN_CURRICULUM_AUDIT_ONLY','startingHead':meta['startingHead'],'trainIdentity':{'artifactId':man['outputDatasetId'],'path':'data/student5_v3/','logicalSha256':sha(raw),'rows':len(rows),'claims':len(claims),'contractFingerprint':contract_fingerprint()},'inputIdentityChecks':inputchecks,'rowLanguages':counts(r['language'] for r in rows),'claimLanguages':counts(r['language'] for r,c in claims),'targetExamples':dict(kindcounts),'tokenCountMethod':'Existing build_v3_examples with Unicode lexical audit offsets; no BERT tokenizer/model, no truncation at 256 lexical units. Counts are annotation-support diagnostics, not training-token or gradient counts.','tokenLabelCounts':token,'tokenEffectiveSupport':support,'sequenceLabelCounts':seq,'roleValueKindCounts':{h:dict(v) for h,v in roles.items()},'rolePointerIndexCounts':dict(role_indices),'roleMentionPositions':dict(role_positions),'roleEqualities':dict(role_equal),'temporalAnchorCounts':dict(anchors),'statuses':dict(status),'familyCoverage':{k:family_info(v) for k,v in families.items()},'rawFamilyCoverage':{f:family_info([(r,c) for r,c in claims if c['family']==f]) for f in sorted({c['family'] for r,c in claims})},'cueSurfaces':dict(cue_surface),'temporalSurfaces':dict(temporal_surface),'cueByPolarity':dict(cue_polarity),'duplicates':{'uniqueExactObservationSurfaces':len(rowgroups),'excessExactObservationInstances':len(rows)-len(rowgroups),'uniqueNormalizedClaimSurfaces':len(surfaceclaims),'excessNormalizedClaimInstances':len(claims)-len(surfaceclaims),'sameObservationContextConflicts':len(conflict),'sameTextDifferentContextGroups':len(contextvariants),'claimSurfaceGoldReviewGroups':len(claim_conflicts),'topExactObservationMultiplicities':[{'language':k[0],'text':k[1],'count':len(v)} for k,v in sorted(rowgroups.items(),key=lambda kv:-len(kv[1]))[:20]],'nearDuplicateMethod':'All distinct observation surfaces within language, SequenceMatcher character ratio>=0.90 after casefold/space normalization; screen only, opposite-polarity pairs may be valuable contrasts.','nearDuplicatePairs':len(near),'rowsInNearDuplicatePairs':len(near_nodes),'delexicalizedSkeletonGroups':len(templ),'largestSkeletonClaims':max(freq),'top10SkeletonClaims':sum(freq[:10]),'skeletonEffectiveGroupCount':len(claims)**2/sum(n*n for n in freq)},'reviewScreenCounts':{k:len(v) for k,v in flags.items()},'guards':{'devRead':False,'frozenRead':False,'trainingExecuted':False,'optimizerExecuted':False,'modelExecuted':False,'datasetModified':False,'remediationExecuted':False}}
    result['curriculumConfounds']={'reportPredicatePolaritySourceEqualsSubject':counts(canon([c['labels']['predicate'],c['labels']['polarity'],c['labels']['sourceReferent']==c['labels']['subjectReferent']]) for r,c in claims if c['labels']['claimKind']=='REPORT'),'futurePredicates':counts(c['labels']['predicate'] for r,c in claims if c['labels']['temporalRelation']['relation']=='FUTURE'),'pastPredicates':counts(c['labels']['predicate'] for r,c in claims if c['labels']['temporalRelation']['relation']=='PAST'),'abstainedDialogueActs':counts(c['labels']['dialogueAct'] for r,c in claims if c['interpretationStatus']=='ABSTAINED'),'contextEntityCountDistribution':counts(str(len(r['context']['contextEntities'])) for r in rows),'maxWhitespaceWordsInSubjectSpan':max(len(r['text'][s:e].split()) for r,c in claims for s,e in c['subjectSpans']),'maxWhitespaceWordsInPersonSpan':max(len(r['text'][slice(*m['span'])].split()) for r in rows for m in r['mentions'] if m['entityType']=='PERSON')}
    a.output.mkdir(parents=True,exist_ok=True)
    (a.output/'curriculum.json').write_text(json.dumps(result,indent=2,ensure_ascii=False)+'\n')
    (a.output/'review-evidence.json').write_text(json.dumps(examples,indent=2,ensure_ascii=False)+'\n')
    print(json.dumps({'identity':result['trainIdentity'],'duplicates':result['duplicates'],'screens':result['reviewScreenCounts'],'familyCoverage':result['familyCoverage'],'roles':result['roleValueKindCounts'],'statuses':result['statuses']},ensure_ascii=False))

if __name__=='__main__':main()
