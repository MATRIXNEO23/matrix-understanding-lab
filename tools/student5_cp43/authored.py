"""CP43 explicit, project-authored TRAIN declarations. No semantic classifier.
String lookup computes character offsets only; every label/role is specified below.
"""
import copy,sys

def authored_rows(repo):
 sys.path.insert(0,str(repo/'matrix_nlu'))
 from contract_v3 import contract_fingerprint,ROLE_HEADS
 from referent_candidates import build_mentions,build_candidate_table
 rows=[]
 def add(lang,family,text,obj=(),sub=(),pred='goal.object',act='ASSERT',kind='DIRECT',pol='POSITIVE',rel='CURRENT',tm=(),neg=(),entities=(),roles=None,ctx=None,adult=False,register='conversational',reason='',anchor=None,alts=None,source=None,more=None,group=None):
  context=copy.deepcopy(ctx or {'speaker':'cp43-adult-speaker','observer':'cp43-adult-observer','contextEntities':[]})
  def spans(vals):
   if isinstance(vals,str): vals=[vals]
   out=[]
   for val in vals:
    if isinstance(val,list): out.append(val);continue
    if isinstance(val,tuple):word,occ=val
    else:word,occ=val,0
    start=-1
    for _ in range(occ+1):start=text.index(word,start+1)
    out.append([start,start+len(word)])
   return out
  mentions=build_mentions([{'type':typ,'span':spans([surf])[0]} for surf,typ in entities],len(text))
  labels={'dialogueAct':act,'predicate':pred,'claimKind':kind,'polarity':pol,'subjectReferent':'ctx:speaker','targetReferent':'NONE','ownerReferent':'ctx:speaker','perspectiveReferent':'ctx:speaker','sourceReferent':'ctx:speaker'}
  labels.update(roles or {})
  labels['temporalRelation']={'relation':rel,'anchorRef':anchor if anchor is not None else ('temporal:t0' if rel in ['BEFORE','AFTER','DURING'] else 'context-reference' if rel=='AT_REFERENCE' else None if rel in ['ATEMPORAL','UNKNOWN'] else 'speech-time')}
  fs={k:('UNKNOWN' if val=='UNKNOWN' else 'NOT_APPLICABLE' if val=='NONE' else 'RESOLVED') for k,val in labels.items()}
  if rel=='UNKNOWN':fs['temporalRelation']='UNKNOWN'
  if pred=='speech.unresolved':fs['predicate']='UNKNOWN'
  fs.update({k:'RESOLVED' for k in ['boundary','objectSpans','subjectSpans','negationCueSpans','temporalEvidence','entityMentionIds']})
  c={'claimId':'c0','family':family,'sourceSpan':source or [0,len(text)],'objectSpans':spans(obj),'subjectSpans':spans(sub),'negationCueSpans':spans(neg),'temporalEvidence':[{'temporalId':f't{i}','span':s} for i,s in enumerate(spans(tm))],'entityMentionIds':[m['mentionId'] for m in mentions if (source or [0,len(text)])[0]<=m['span'][0]<m['span'][1]<=(source or [0,len(text)])[1]],'labels':labels,'fieldStatusByField':fs,'structuralStatus':'VALID','interpretationStatus':'RESOLVED'}
  if alts:
   c['alternativesByField']={h:[{'value':v,'rank':i+1} for i,v in enumerate(vs)] for h,vs in alts.items()}
   for h in alts:fs[h]='AMBIGUOUS'
  c['interpretationStatus']='AMBIGUOUS' if 'AMBIGUOUS' in fs.values() else 'ABSTAINED' if 'UNKNOWN' in fs.values() else 'RESOLVED'
  claims=[c] if family!='zero_claim' else []
  if more:claims.extend(more(c,spans))
  critical=[s for cl in claims for h in ['objectSpans','subjectSpans'] for s in cl[h]]
  r={'id':f'cp43-{lang}-{family}-{len(rows):04d}','datasetId':'student5-matrix-nlu-v3-train-v2.1-cp43r2','sourceDatasetId':'cp43-project-authored-train-only','split':'train','language':lang,'text':text,'adultOnly':adult,'context':context,'mentions':mentions,'referentCandidates':build_candidate_table(text,mentions,context,critical)['candidates'],'claims':claims,'contractVersion':'MATRIX_NLU_CONTRACT_V3','contractFingerprintSha256':contract_fingerprint(),'provenance':{'kind':'PROJECT_AUTHORED_TRAIN_ONLY','sourceHead':'270a0729c20ede548fe373f488029241fcbb35a3','disposition':'NEWLY_AUTHORED','reason':reason,'decisions':['D01','D02','D03','D04','D05','D06','D07'],'register':register,'family':family,'contrastGroup':group or family,'allParticipantsAdults':True,'license':'PROJECT_AUTHORED','protectedDataUsed':False}}
  assert reason
  rows.append(r);return r
 L=['it','en','es']
 # Two distinct directive constructions, each with a polite counterpart.
 for family,triples in [
 ('command_stop',[('Fermati subito, per favore.','Fermati','subito'),('Stop right now, please.','Stop','right now'),('Para ahora mismo, por favor.','Para','ahora mismo')]),
 ('command_privacy',[('Chiudi la porta, dai.','Chiudi la porta',None),('Close the door, will you.','Close the door',None),('Cierra la puerta, anda.','Cierra la puerta',None)]),
 ('request_privacy',[('Mi chiudi la porta, per favore?','chiudi la porta',None),('Could you close the door for me?','close the door',None),('¿Me cierras la puerta, por favor?','cierras la puerta',None)]),
 ('request_help',[('Puoi aiutarmi con questo casino?','aiutarmi con questo casino',None),('Would you help me with this mess?','help me with this mess',None),('¿Me ayudas con este lío?','ayudas con este lío',None)])]:
  for l,(t,o,time) in zip(L,triples):
   add(l,family,t,o,sub='you' if l=='en' and 'you' in t and family.startswith('request') else (),act='COMMAND' if family.startswith('command') else 'REQUEST',tm=[time] if time else (),roles={'subjectReferent':'ctx:observer','ownerReferent':'ctx:speaker','targetReferent':'ctx:speaker' if family=='request_help' else 'NONE'},reason='Explicit directive or conventional request; speaker goal, addressee action. Object/action differs from owner; no consent inference.')
 # Belief/direct and source/viewpoint contrasts with different predicates.
 for variant,triples in [('appearance',[('Credo che Anna sia stanca.','Anna','stanca'),('I think Anna is tired.','Anna','tired'),('Creo que Anna está cansada.','Anna','cansada')]),('residence',[('Secondo me Paolo abita a Genova.','Paolo','Genova'),('In my opinion Paolo lives in Genoa.','Paolo','Genoa'),('En mi opinión Paolo vive en Génova.','Paolo','Génova')])]:
  for l,(t,s,o) in zip(L,triples):
   ent=[(s,'PERSON')]+([(o,'LOCATION')] if variant=='residence' else [])
   add(l,'belief_'+variant,t,o,s,pred='residence.place' if variant=='residence' else 'attribute.is',kind='BELIEF',entities=ent,roles={'subjectReferent':'mention:m0','ownerReferent':'mention:m0'},reason='Overt mental stance belongs to speaker; embedded named subject owns described state. D03 BELIEF is not triggered by subjective adjective alone.')
 for l,t,o in [('it','Anna è stanca.','stanca'),('en','Anna is tired.','tired'),('es','Anna está cansada.','cansada')]:add(l,'direct_appearance',t,o,'Anna',pred='attribute.is',entities=[('Anna','PERSON')],roles={'subjectReferent':'mention:m0','ownerReferent':'mention:m0'},reason='Plain assertion without belief wrapper; same adjective as BELIEF control, D03.')
 for l in L:
  for reverse in [False,True]:
   reporter,view=('Nora','Diego') if not reverse else ('Diego','Nora')
   t={'it':f'Secondo {view}, Anna è stanca, riferisce {reporter}.','en':f'In {view}’s view, Anna is tired, {reporter} reports.','es':f'Según {view}, Anna está cansada, cuenta {reporter}.'}[l]
   o={'it':'stanca','en':'tired','es':'cansada'}[l]
   add(l,'report_postposed_source',t,o,'Anna',pred='attribute.is',kind='REPORT',entities=[(view,'PERSON'),('Anna','PERSON'),(reporter,'PERSON')],roles={'subjectReferent':'mention:m1','ownerReferent':'mention:m1','perspectiveReferent':'mention:m0','sourceReferent':'mention:m2'},reason='Reporter is last mention; explicit viewpoint first; subject middle. Match meaning, not first/recent candidate or fixed participant position.',group='source-position-swap')
   t={'it':f'{reporter} riferisce che, secondo {view}, Anna è stanca.','en':f'{reporter} reports that, in {view}’s view, Anna is tired.','es':f'{reporter} cuenta que, según {view}, Anna está cansada.'}[l]
   add(l,'report_preposed_source',t,o,'Anna',pred='attribute.is',kind='REPORT',entities=[(reporter,'PERSON'),(view,'PERSON'),('Anna','PERSON')],roles={'subjectReferent':'mention:m2','ownerReferent':'mention:m2','perspectiveReferent':'mention:m1','sourceReferent':'mention:m0'},reason='Same proposition and roles as postposed-source control, changed mention order. All identities are grounded separately.',group='source-position-swap')
  t={'it':'Anna dice che desidera riposare.','en':'Anna says she wants to rest.','es':'Anna dice que desea descansar.'}[l];o={'it':'riposare','en':'rest','es':'descansar'}[l]
  add(l,'report_equal_roles',t,o,'Anna',kind='REPORT',entities=[('Anna','PERSON')],roles={h:'mention:m0' for h in ['subjectReferent','ownerReferent','sourceReferent','perspectiveReferent']},reason='Named holder explicitly reports own desire: source=viewpoint=subject=owner legitimately coincide under D02. Preserve equal-role controls.')
 # Descriptive, attraction, explicit slang, consent and refusal are distinct supervision.
 families=[
 ('attraction','preference.like','ASSERT','POSITIVE',[('Mi attrai parecchio.','Mi attrai parecchio'),('I am really attracted to you.','attracted to you'),('Me atraes muchísimo.','Me atraes muchísimo')]),
 ('explicit_description','attribute.is','ASSERT','POSITIVE',[('Sono nuda e ho freddo.','nuda'),('I am naked and cold.','naked'),('Estoy desnuda y tengo frío.','desnuda')]),
 ('explicit_desire','goal.object','ASSERT','POSITIVE',[('Ho voglia di scopare, cazzo.','scopare'),('I really want to fuck.','fuck'),('Tengo ganas de follar, joder.','follar')]),
 ('negative_desire','goal.object','ASSERT','NEGATIVE',[('Non voglio un bacio.','un bacio'),('I do not want a kiss.','a kiss'),('No quiero un beso.','un beso')]),
 ('grant','consent.grant','ASSERT','POSITIVE',[('Ti do il permesso di baciarmi.','baciarmi'),('I give you permission to kiss me.','kiss me'),('Te doy permiso para besarme.','besarme')]),
 ('affirmative_refusal','consent.refuse','ASSERT','POSITIVE',[('Rifiuto questo contatto.','questo contatto'),('I refuse this contact.','this contact'),('Rechazo este contacto.','este contacto')]),
 ('withdrawal','consent.refuse','CORRECT','POSITIVE',[('Revoco il permesso di toccarmi.','toccarmi'),('I revoke permission to touch me.','touch me'),('Revoco el permiso para tocarme.','tocarme')]),
 ('negative_consent','consent.refuse','ASSERT','NEGATIVE',[('Non ti do il permesso di toccarmi.','toccarmi'),('I do not give you permission to touch me.','touch me'),('No te doy permiso para tocarme.','tocarme')])]
 for fam,pred,act,pol,tri in families:
  if fam=='explicit_description':continue # handled as two flat claims below, never flatten coordinated independent states.
  for l,(t,o) in zip(L,tri):
   cue=({'it':'Non','en':'not','es':'No'}[l],) if fam in ['negative_desire','negative_consent'] else ()
   target='ctx:observer' if fam in ['attraction','grant','withdrawal','negative_consent'] else 'NONE'
   add(l,fam,t,o,sub='I' if l=='en' else (),pred=pred,act=act,pol=pol,neg=cue,roles={'targetReferent':target},adult=True,register='explicit-slang' if fam=='explicit_desire' else 'intimate-conversational',reason='Literal '+fam+' semantics; desire/attraction/description/request/consent/refusal/withdrawal are not substituted for each other. Polarity is compositional, not adult-word or cue presence.',group='intimacy-distinction')
 for l,t,o in [('it','Ho la pelle nuda e arrossata.','la pelle nuda e arrossata'),('en','I have bare, red, irritated skin.','bare, red, irritated skin'),('es','Tengo la piel desnuda y enrojecida.','la piel desnuda y enrojecida')]:
  add(l,'explicit_description',t,o,sub='I' if l=='en' else (),pred='attribute.is',adult=True,reason='Physical description of speaker, not desire or permission. Multiword attribute retains explicit anatomical description without UNKNOWN.')
 # D05: same No token in corrected positive and genuinely negated propositions.
 for l,t,o,sub in [('it','No, il mio nome è Ada.','Ada','il mio nome'),('en','No, my name is Ada.','Ada','my name'),('es','No, mi nombre es Ada.','Ada','mi nombre')]:
  add(l,'metalinguistic_positive',t,o,sub,pred='identity.name',act='CORRECT',rel='ATEMPORAL',reason='Discourse No rejects prior wording, not positive name proposition. D05: no proposition-scoped negation cue.')
 for l,t,o in [('it','Non è vero che non desidero un abbraccio.','un abbraccio'),('en','It is not true that I do not want a hug.','a hug'),('es','No es cierto que no quiera un abrazo.','un abrazo')]:
  cues=['Non','non'] if l=='it' else [('not',0),('not',1)] if l=='en' else ['No','no']
  add(l,'double_negation_desire',t,o,sub='I' if l=='en' else (),neg=cues,adult=True,reason='Denial of negative desire yields positive desire with two exact cue spans; it does not grant consent.')
 # Uncertainty is caused by competing semantic evidence, not vocabulary.
 for l,t,o,neg in [('it','Non so se desidero un bacio.','un bacio','Non'),('en','I do not know whether I want a kiss.','a kiss','not'),('es','No sé si deseo un beso.','un beso','No')]:
  add(l,'uncertain_desire',t,o,sub=(('I',1),) if l=='en' else (),pol='UNKNOWN',kind='BELIEF',neg=[neg],adult=True,reason='Overt lack of knowledge about own desire; single embedded desire has unresolved polarity, not refusal or positive consent. Cue negates knowledge wrapper; no inferred desire polarity.')
 for l,t,o in [('it','A quanto pare, Anna vive a Roma.','Roma'),('en','Apparently, Anna lives in Rome.','Rome'),('es','Al parecer, Anna vive en Roma.','Roma')]:
  add(l,'unknown_evidential_kind',t,o,'Anna',pred='residence.place',kind='UNKNOWN',entities=[('Anna','PERSON'),(o,'LOCATION')],roles={'subjectReferent':'mention:m0','ownerReferent':'mention:m0','sourceReferent':'UNKNOWN'},reason='Apparently may convey hearsay or the speaker’s inference; wording does not establish REPORT versus BELIEF or its source. Residence and subject remain understood; genuine evidential uncertainty.')
 for l,t,o in [('it','Sono stato o sarò a Roma?','Roma'),('en','Was I or will I be in Rome?','Rome'),('es','¿Estuve o estaré en Roma?','Roma')]:
  add(l,'unknown_time',t,o,sub=(('I',0),('I',1)) if l=='en' else (),pred='presence.reported',act='QUESTION',rel='UNKNOWN',pol='UNKNOWN',tm={'it':['Sono stato','sarò'],'en':['Was','will'],'es':['Estuve','estaré']}[l],entities=[(o,'LOCATION')],reason='Question explicitly contrasts past and future for one presence proposition; neither temporal alternative is selected. This is not ordinary present desire with a future action.')
 for l,t,o in [('it','Tu abiti a Roma','Roma'),('en','You live in Rome','Rome'),('es','Tú vives en Roma','Roma')]:
  ctx={'speaker':'cp43-adult-speaker','observer':'cp43-adult-observer','contextEntities':[],'transcriptEvidence':{'source':'unpunctuated spoken transcript','intonationLost':True,'conversationContextLost':True,'possibleModes':['echo-confirmation-question','plain-assertion']}}
  add(l,'unknown_act_transcript',t,o,sub={'it':'Tu','en':'You','es':'Tú'}[l],pred='residence.place',act='UNKNOWN',entities=[(o,'LOCATION')],roles={'subjectReferent':'ctx:observer','ownerReferent':'ctx:observer'},ctx=ctx,reason='A damaged unpunctuated speech transcript explicitly lacks intonation/context: echo question versus assertion genuinely unresolved. Do not infer act from missing question mark. Lexical proposition remains intelligible.')
 # Several temporal relations across work, physical presence and description; no goal-time shortcut.
 for rel,tri in [
 ('PAST',[('Una volta lavoravo come cuoco.','cuoco','Una volta'),('I used to work as a cook.','cook','used to'),('Antes trabajaba de cocinero.','cocinero','Antes')]),
 ('BEFORE',[('Prima della cena ero in cucina.','in cucina','Prima della cena'),('Before dinner I was in the kitchen.','in the kitchen','Before dinner'),('Antes de cenar estaba en la cocina.','en la cocina','Antes de cenar')]),
 ('AFTER',[('Dopo il concerto ero stanco.','stanco','Dopo il concerto'),('After the concert I was tired.','tired','After the concert'),('Después del concierto estaba cansado.','cansado','Después del concierto')]),
 ('DURING',[('Durante la pausa ero in cortile.','in cortile','Durante la pausa'),('During the break I was in the yard.','in the yard','During the break'),('Durante el descanso estaba en el patio.','en el patio','Durante el descanso')]),
 ('AT_REFERENCE',[('In quel momento ero tranquillo.','tranquillo','In quel momento'),('At that moment I was calm.','calm','At that moment'),('En aquel momento estaba tranquilo.','tranquilo','En aquel momento')])]:
  for l,(t,o,time) in zip(L,tri):
   add(l,'temporal_'+rel,t,o,sub='I' if l=='en' else (),pred='work.role' if rel=='PAST' else 'attribute.is' if rel in ['AFTER','AT_REFERENCE'] else 'presence.reported',rel=rel,tm=[time],ctx={'speaker':'cp43-adult-speaker','observer':'cp43-adult-observer','contextEntities':[],'temporalReference':'the previously discussed pause'} if rel=='AT_REFERENCE' else None,reason='Explicit non-goal temporal state; full temporal expression preserved, relation and appropriate evidence/context anchor declared.')
 for l,t,o,times in [('it','Il lunedì e il giovedì lavoro come cuoco.','cuoco',['Il lunedì','il giovedì']),('en','On Mondays and on Thursdays I work as a cook.','cook',['On Mondays','on Thursdays']),('es','Los lunes y los jueves trabajo de cocinero.','cocinero',['Los lunes','los jueves'])]:
  add(l,'multiple_temporal',t,o,sub='I' if l=='en' else (),pred='work.role',rel='RECURRENT',tm=times,reason='One recurrent employment proposition with two explicitly stated recurring time groups, both retained.')
 for l,t,left,right,o0,o1 in [('it','Anna era qui; dopo io ero a Roma.','Anna era qui','dopo io ero a Roma.','qui','Roma'),('en','Anna was here; afterwards I was in Rome.','Anna was here','afterwards I was in Rome.','here','Rome'),('es','Anna estaba aquí; después yo estaba en Roma.','Anna estaba aquí','después yo estaba en Roma.','aquí','Roma')]:
  cut=t.index(';');start=t.index(right)
  def second(c,sp,st=start,oo=o1,ll=l,tx=t):
   z=copy.deepcopy(c);z['claimId']='c1';z['sourceSpan']=[st,len(tx)];z['objectSpans']=sp(oo);z['subjectSpans']=sp({'it':'io','en':'I','es':'yo'}[ll]);z['entityMentionIds']=['m1'];z['labels']['subjectReferent']=z['labels']['ownerReferent']='ctx:speaker';z['labels']['temporalRelation']={'relation':'AFTER','anchorRef':'claim:c0'};z['temporalEvidence']=[{'temporalId':'t0','span':sp({'it':'dopo','en':'afterwards','es':'después'}[ll])[0]}];return [z]
  add(l,'cross_claim_anchor',t,o0,'Anna',pred='presence.reported',rel='PAST',entities=[('Anna','PERSON'),(o1,'LOCATION')],roles={'subjectReferent':'mention:m0','ownerReferent':'mention:m0'},source=[0,cut],more=second,reason='Two non-overlapping atomic presence claims; second AFTER points to first claim, not an invented wall-clock date.')
 # Realistic mixed-language contrasts beyond desire; borrowing alone is not UNKNOWN.
 for fam,pred,act,pol,tri in [
 ('cs_description','attribute.is','ASSERT','POSITIVE',[('Sono proprio exhausted oggi.','exhausted'),('Estoy bastante exhausted hoy.','exhausted')]),
 ('cs_request','goal.object','REQUEST','POSITIVE',[('Mi fai un quick check, per favore?','un quick check'),('¿Me haces un quick check, por favor?','un quick check')]),
 ('cs_command','goal.object','COMMAND','POSITIVE',[('Fai il check-in adesso.','Fai il check-in'),('Haz el check-in ahora.','Haz el check-in')]),
 ('cs_negative_preference','preference.like','ASSERT','NEGATIVE',[('Non mi piace questo outfit.','questo outfit'),('No me gusta este outfit.','este outfit')]),
 ('cs_grant','consent.grant','ASSERT','POSITIVE',[('Acconsento al dirty talk con te.','al dirty talk con te'),('Consiento el dirty talk contigo.','el dirty talk contigo')]),
 ('cs_refusal','consent.refuse','ASSERT','POSITIVE',[('Rifiuto il dirty talk.','il dirty talk'),('Rechazo el dirty talk.','el dirty talk')]),
 ('cs_withdrawal','consent.refuse','CORRECT','POSITIVE',[('Revoco il consenso al dirty talk.','al dirty talk'),('Revoco el consentimiento al dirty talk.','al dirty talk')])]:
  for primary,(t,o) in zip(['it','es'],tri):
   roles={'subjectReferent':'ctx:observer','ownerReferent':'ctx:speaker'} if act in ['REQUEST','COMMAND'] else {}
   r=add('code-switch',fam,t,o,pred=pred,act=act,pol=pol,tm=[('oggi' if primary=='it' else 'hoy')] if fam=='cs_description' else [('adesso' if primary=='it' else 'ahora')] if fam=='cs_command' else (),neg=['Non' if primary=='it' else 'No'] if pol=='NEGATIVE' else (),roles=roles,adult=fam in ['cs_grant','cs_refusal','cs_withdrawal'],register='natural-english-borrowing',reason='Natural '+primary+'/English dialogue: '+fam+' is independently specified; familiar borrowed words do not determine polarity, uncertainty, or consent.')
   r['provenance']['componentLanguages']=[primary,'en'];r['provenance']['primaryLanguage']=primary
 # Multiword person, multiple object and repeated subject evidence; each has grounded single referent.
 for l,t,o,sub in [('it','Maria Rossi ama il jazz e il blues.',['il jazz','il blues'],'Maria Rossi'),('en','Maria Rossi likes jazz and blues.',['jazz','blues'],'Maria Rossi'),('es','María López disfruta del jazz y del blues.',['jazz','blues'],'María López')]:
  add(l,'multiword_subject_multiple_object',t,o,sub,pred='preference.like',rel='ATEMPORAL',entities=[(sub,'PERSON')],roles={'subjectReferent':'mention:m0','ownerReferent':'mention:m0'},reason='Full multiword person and two coordinated preference objects; no arbitrary split of the person name.')
 for l,t,o,subs in [('it','Anna, proprio lei, ama il jazz.','il jazz',['Anna','lei']),('en','Anna, she really likes jazz.','jazz',['Anna','she']),('es','Anna, ella sí disfruta del jazz.','jazz',['Anna','ella'])]:
  add(l,'multiple_subject_evidence',t,o,subs,pred='preference.like',rel='ATEMPORAL',entities=[('Anna','PERSON')],roles={'subjectReferent':'mention:m0','ownerReferent':'mention:m0'},reason='Left-dislocated proper name and resumptive pronoun jointly evidence the same person; two subject groups, not two arbitrarily merged people.')
 # Candidate order controls: same surface, supplied unique versus competing antecedents.
 for l,t,o,sub in [('it','Lei abita a Lucca.','Lucca','Lei'),('en','She lives in Bath.','Bath','She'),('es','Ella vive en Lugo.','Lugo','Ella')]:
  for situation in ['unique-first','unique-last','ambiguous']:
   ents=[{'entityRef':'woman-a','surfaceForms':['Ada'],'gender':'female'},{'entityRef':'man-b','surfaceForms':['Bruno'],'gender':'male'}]
   if situation=='unique-last':ents.reverse()
   if situation=='ambiguous':ents=[{'entityRef':'woman-a','surfaceForms':['Ada'],'gender':'female'},{'entityRef':'woman-b','surfaceForms':['Bea'],'gender':'female'}]
   ctx={'speaker':'cp43-adult-speaker','observer':'cp43-adult-observer','contextEntities':ents,'discourse':'Only the listed female candidate(s) can be antecedents; all are equally salient.'}
   value='UNKNOWN' if situation=='ambiguous' else 'entity:woman-a';alts={h:['entity:woman-a','entity:woman-b'] for h in ['subjectReferent','ownerReferent']} if situation=='ambiguous' else None
   add(l,'antecedent_'+situation,t,o,sub,pred='residence.place',entities=[(o,'LOCATION')],roles={'subjectReferent':value,'ownerReferent':value},ctx=ctx,alts=alts,reason='Explicit trusted context candidate features determine unique female antecedent regardless of list order; two compatible equally salient women require genuine ambiguity. Context consumption remains a separate readiness check.',group='antecedent-order')
 for l,t in [('it','ehm…'),('en','uh…'),('es','eh…')]:add(l,'zero_claim',t,reason='Conversational filled pause with no supported proposition; boundary-negative, not a fabricated UNKNOWN claim.')
 return rows
