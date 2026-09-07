"""Explicit authored TRAIN specifications, not mined/model-generated labels.
Every tuple declares semantics; text matching is used ONLY to locate declared evidence.
"""
import copy,sys
def authored_rows(repo):
 sys.path.insert(0,str(repo/'matrix_nlu'))
 from contract_v3 import contract_fingerprint,ROLE_HEADS
 from referent_candidates import build_mentions,build_candidate_table
 rows=[]
 def add(lang,family,text,obj=None,sub=None,predicate='goal.object',act='ASSERT',kind='DIRECT',polarity='POSITIVE',relation='CURRENT',temporal=(),cues=(),roles=None,entities=(),status=None,context=None,decisions=(),adult=False,register='neutral',reason='',zero=False):
  def sp(s):
   if isinstance(s,list):return s
   a=text.index(s);return [a,a+len(s)]
  ctx=context or {'speaker':'cp42-adult-speaker','observer':'cp42-adult-addressee','contextEntities':[]}
  mentions=build_mentions([{'type':t,'span':sp(s)} for s,t in entities],len(text))
  labels=dict(dialogueAct=act,predicate=predicate,claimKind=kind,polarity=polarity,subjectReferent='ctx:speaker',targetReferent='NONE',ownerReferent='ctx:speaker',perspectiveReferent='ctx:speaker',sourceReferent='ctx:speaker')
  labels.update(roles or {})
  evidence=[{'temporalId':f't{i}','span':sp(t)} for i,t in enumerate(temporal)]
  anchor='temporal:t0' if relation in ['BEFORE','AFTER','DURING'] else 'context-reference' if relation=='AT_REFERENCE' else None if relation in ['ATEMPORAL','UNKNOWN'] else 'speech-time'
  labels['temporalRelation']={'relation':relation,'anchorRef':anchor}
  subjects=[] if sub is None else [sp(sub)];objects=[] if obj is None else [sp(obj)]
  fs={k:('UNKNOWN' if v=='UNKNOWN' else 'NOT_APPLICABLE' if v=='NONE' else 'RESOLVED') for k,v in labels.items()}
  fs.update({k:'RESOLVED' for k in ['boundary','objectSpans','subjectSpans','negationCueSpans','temporalEvidence','entityMentionIds']})
  if relation=='UNKNOWN':fs['temporalRelation']='UNKNOWN'
  fs.update(status or {})
  c={'claimId':'c0','family':family,'sourceSpan':[0,len(text)],'objectSpans':objects,'subjectSpans':subjects,'negationCueSpans':[sp(t) for t in cues],'temporalEvidence':evidence,'entityMentionIds':[m['mentionId'] for m in mentions],'labels':labels,'fieldStatusByField':fs,'structuralStatus':'VALID','interpretationStatus':'AMBIGUOUS' if 'AMBIGUOUS' in fs.values() else 'ABSTAINED' if 'UNKNOWN' in fs.values() else 'RESOLVED'}
  if status:
   c['alternativesByField']={k:[{'value':'entity:adult-a','rank':1},{'value':'entity:adult-b','rank':2}] for k,v in status.items() if v=='AMBIGUOUS'}
  candidates=build_candidate_table(text,mentions,ctx,subjects+objects)['candidates']
  r={'id':f'cp42-{lang}-{family}-{len(rows):04d}','datasetId':'student5-matrix-nlu-v3-train-v2','sourceDatasetId':'cp42-project-authored-train-only','split':'train','language':lang,'text':text,'adultOnly':adult,'context':ctx,'mentions':mentions,'referentCandidates':candidates,'claims':[] if zero else [c],'contractVersion':'MATRIX_NLU_CONTRACT_V3','contractFingerprintSha256':contract_fingerprint(),'provenance':{'kind':'PROJECT_AUTHORED_TRAIN_ONLY','author':'ChatGPT Work','sourceHead':'1396dd6c997ce0dbf5e4a5ce933437c82fc1c217','disposition':'NEWLY_AUTHORED','language':lang,'families':[family],'heads':list(labels)+['boundary','object','subject','negation','temporal','entity'],'decisions':list(decisions),'reason':reason or family+' contrast: explicit semantic specification; no lexical classifier','register':register,'adultOnly':adult,'allParticipantsAdults':True,'source':'CP37/CP38 curriculum gaps; CP41 pooled similarity risk only, no protected payload or probe text copied','preservationGroup':'CONTROL' if 'control' in family else 'NEW_REPAIRED'}}
  rows.append(r);return r
 langs=['it','en','es']
 # Parallel semantic families with independently authored natural wording, not language-course vocabulary drills.
 triples=[
 ('command',[('Vieni a casa subito.','venire a casa','subito'),('Come home now.','Come home','now'),('Ven a casa ahora.','Ven a casa','ahora')]),
 ]
 for l,(t,o,tm) in zip(langs,triples[0][1]):
  # Surface object is the actual imperative phrase, not the dictionary infinitive.
  o='Vieni a casa' if l=='it' else o
  add(l,'command',t,o,act='COMMAND',temporal=[tm],roles={'subjectReferent':'ctx:observer','ownerReferent':'ctx:speaker'},decisions=['D07'],reason='Speaker directs addressee action; goal expressed is speaker’s directive, subject is addressee')
 for l,t,o in [('it','Per favore, puoi venire a casa?','venire a casa'),('en','Could you come home, please?','come home'),('es','¿Puedes venir a casa, por favor?','venir a casa')]:
  add(l,'request',t,o,act='REQUEST',roles={'subjectReferent':'ctx:observer','ownerReferent':'ctx:speaker'},decisions=['D07'],reason='Request expresses speaker-desired action by addressee, not an assertion of addressee desire')
 for l,t,o,s in [('it','Tu vivi a Milano?','Milano','Tu'),('en','Do you live in Leeds?','Leeds','you'),('es','¿Tú vives en Sevilla?','Sevilla','Tú')]:
  add(l,'question',t,o,s,predicate='residence.place',act='QUESTION',entities=[(o,'LOCATION')],roles={'subjectReferent':'ctx:observer','ownerReferent':'ctx:observer'})
 for l,t,o in [('it','No, abito a Bari.','Bari'),('en','No, I live in Bristol.','Bristol'),('es','No, vivo en Málaga.','Málaga')]:
  add(l,'metalinguistic_correction',t,o,'I' if l=='en' else None,predicate='residence.place',act='CORRECT',entities=[(o,'LOCATION')],decisions=['D05'],reason='Initial discourse No corrects previous wording; corrected residence proposition is positive; no proposition negation cue')
 for l,t,o in [('it','Penso di essere una persona paziente.','una persona paziente'),('en','I believe I am a patient person.','a patient person'),('es','Creo que soy una persona paciente.','una persona paciente')]:
  add(l,'belief_wrapper',t,o,'I' if l=='en' else None,predicate='attribute.is',kind='BELIEF',decisions=['D03'])
 for l,t,o in [('it','Sono una persona paziente.','una persona paziente'),('en','I am a patient person.','a patient person'),('es','Soy una persona paciente.','una persona paciente')]:
  add(l,'direct_control',t,o,'I' if l=='en' else None,predicate='attribute.is',decisions=['D03'])
 for l,t,o,tm in [('it','Voglio visitare il museo domani.','visitare il museo','domani'),('en','I want to visit the museum tomorrow.','visit the museum','tomorrow'),('es','Quiero visitar el museo mañana.','visitar el museo','mañana')]:
  add(l,'desire_current_action_future',t,o,'I' if l=='en' else None,temporal=[tm],decisions=['D01'])
 for l,t,o,tm in [('it','Domani vorrò riposare.','riposare','Domani'),('en','Tomorrow I will want to rest.','rest','Tomorrow'),('es','Mañana querré descansar.','descansar','Mañana')]:
  add(l,'desire_future',t,o,'I' if l=='en' else None,temporal=[tm],relation='FUTURE',decisions=['D01'])
 temporal_specs=[
 ('PAST',[('Ieri ero a Roma.','Roma','Ieri'),('Yesterday I was in Rome.','Rome','Yesterday'),('Ayer estaba en Roma.','Roma','Ayer')]),
 ('FUTURE',[('Domani sarò a Roma.','Roma','Domani'),('Tomorrow I will be in Rome.','Rome','Tomorrow'),('Mañana estaré en Roma.','Roma','Mañana')]),
 ('BEFORE',[('Prima della riunione ero a Roma.','Roma','della riunione'),('Before the meeting I was in Rome.','Rome','the meeting'),('Antes de la reunión estaba en Roma.','Roma','la reunión')]),
 ('AFTER',[('Dopo la riunione ero a Roma.','Roma','la riunione'),('After the meeting I was in Rome.','Rome','the meeting'),('Después de la reunión estaba en Roma.','Roma','la reunión')]),
 ('DURING',[('Durante la riunione ero a Roma.','Roma','la riunione'),('During the meeting I was in Rome.','Rome','the meeting'),('Durante la reunión estaba en Roma.','Roma','la reunión')]),
 ('RECURRENT',[('Ogni lunedì sono a Roma.','Roma','Ogni lunedì'),('Every Monday I am in Rome.','Rome','Every Monday'),('Cada lunes estoy en Roma.','Roma','Cada lunes')]),
 ('AT_REFERENCE',[('A quel punto ero a Roma.','Roma','A quel punto'),('At that point I was in Rome.','Rome','At that point'),('En ese momento estaba en Roma.','Roma','En ese momento')])]
 for rel,tri in temporal_specs:
  for l,(t,o,tm) in zip(langs,tri):
   ctx={'speaker':'cp42-adult-speaker','observer':'cp42-adult-addressee','contextEntities':[],'temporalReference':'end-of-discussed-meeting'} if rel=='AT_REFERENCE' else None
   add(l,'temporal_'+rel,t,o,'I' if l=='en' else None,predicate='presence.reported',relation=rel,temporal=[tm],entities=[(o,'LOCATION')],context=ctx,reason='Explicit event-time contrast with non-goal predicate; relation anchor is declared')
 # Binding variations require the target to occur before OR after subject, not first/recent candidate.
 for l in langs:
  for a,b in [('Marta','Paolo'),('Paolo','Marta')]:
   texts= {'it':[(f'{a} desidera baciare {b}.',a,b,f'baciare {b}'),(f'Quanto a {b}, {a} desidera baciarlo.' if b=='Paolo' else f'Quanto a {b}, {a} desidera baciarla.',a,b,'baciarlo' if b=='Paolo' else 'baciarla')], 'en':[(f'{a} wants to kiss {b}.',a,b,f'kiss {b}'),(f'As for {b}, {a} wants to kiss '+('him.' if b=='Paolo' else 'her.'),a,b,'kiss him' if b=='Paolo' else 'kiss her')], 'es':[(f'{a} desea besar a {b}.',a,b,f'besar a {b}'),(f'En cuanto a {b}, {a} desea '+('besarlo.' if b=='Paolo' else 'besarla.'),a,b,'besarlo' if b=='Paolo' else 'besarla')]}
   for t,s,target,o in texts[l]:
    ordered=sorted([s,target],key=t.index);ptr=lambda n:'mention:m'+str(ordered.index(n))
    add(l,'role_binding',t,o,s,entities=[(s,'PERSON'),(target,'PERSON')],roles={'subjectReferent':ptr(s),'ownerReferent':ptr(s),'targetReferent':ptr(target)},adult=True,decisions=['D07'],reason='Explicit desire holder and target, names and topic position counterbalanced; desire is not consent')
  for reporter,view in [('Marta','Paolo'),('Paolo','Marta')]:
   t={'it':f'{reporter} riferisce che, secondo {view}, Giulia vive a Torino.','en':f'{reporter} reports that, in {view}’s view, Giulia lives in Turin.','es':f'{reporter} cuenta que, según {view}, Giulia vive en Turín.'}[l]
   o={'it':'Torino','en':'Turin','es':'Turín'}[l]
   add(l,'source_viewpoint',t,o,'Giulia',predicate='residence.place',kind='REPORT',entities=[(reporter,'PERSON'),(view,'PERSON'),('Giulia','PERSON'),(o,'LOCATION')],roles={'subjectReferent':'mention:m2','ownerReferent':'mention:m2','sourceReferent':'mention:m0','perspectiveReferent':'mention:m1'},decisions=['D02','D07'],reason='Reporter, explicit viewpoint holder and embedded subject distinct; identity comes from exact named evidence')
 # Owner distinct from permissive action subject; equal-role consent controls below.
 for l,t,o,s in [('it','Tu hai il mio consenso a baciarmi.','baciarmi','Tu'),('en','You have my consent to kiss me.','kiss me','You'),('es','Tú tienes mi consentimiento para besarme.','besarme','Tú')]:
  add(l,'owner_subject_permission',t,o,s,predicate='consent.grant',roles={'subjectReferent':'ctx:observer','ownerReferent':'ctx:speaker','targetReferent':'ctx:speaker'},adult=True,decisions=['D07'],reason='Addressee is grammatical subject of having permission; speaker owns expressed consent. Requires Supervisor semantic review of action-subject convention.')
 adult_specs=[
 ('adult_desire','goal.object','ASSERT','POSITIVE',[('Voglio fare sesso con te.','fare sesso con te',()),('I want to have sex with you.','have sex with you',()),('Quiero tener sexo contigo.','tener sexo contigo',())]),
 ('adult_grant','consent.grant','ASSERT','POSITIVE',[('Acconsento a fare sesso con te.','fare sesso con te',()),('I consent to having sex with you.','having sex with you',()),('Consiento en tener sexo contigo.','tener sexo contigo',())]),
 ('adult_refusal','consent.refuse','ASSERT','NEGATIVE',[('Non acconsento a fare sesso con te.','fare sesso con te',('Non',)),('I do not consent to having sex with you.','having sex with you',('not',)),('No consiento en tener sexo contigo.','tener sexo contigo',('No',))]),
 ('adult_withdrawal','consent.refuse','CORRECT','POSITIVE',[('Ritiro il consenso a essere toccato.','essere toccato',()),('I withdraw consent to being touched.','being touched',()),('Retiro el consentimiento a que me toques.','que me toques',())]),
 ('adult_request','goal.object','REQUEST','POSITIVE',[('Ti va di fare sesso con me?','fare sesso con me',()),('Would you have sex with me, please?','have sex with me',()),('¿Te apetece tener sexo conmigo?','tener sexo conmigo',())]),
 ('adult_description','attribute.is','ASSERT','POSITIVE',[('Ho il pene irritato.','il pene irritato',()),('I have an irritated penis.','an irritated penis',()),('Tengo el pene irritado.','el pene irritado',())]),
 ('adult_slang','goal.object','ASSERT','POSITIVE',[('Ho voglia di scopare con te.','scopare con te',()),('I want to fuck you.','fuck you',()),('Quiero follar contigo.','follar contigo',())]),
 ('adult_hesitation','goal.object','ASSERT','UNKNOWN',[('Voglio fare sesso con te oppure no, non so.','fare sesso con te',('no','non')),('I want to have sex with you, or not; I am unsure.','have sex with you',('not',)),('Quiero tener sexo contigo o no, no sé.','tener sexo contigo',('no',))])]
 for fam,pred,act,pol,tri in adult_specs:
  for l,(t,o,cues) in zip(langs,tri):
   roles={'targetReferent':'ctx:observer'} if fam not in ['adult_description','adult_withdrawal'] else {}
   if fam=='adult_request':roles.update(subjectReferent='ctx:observer',ownerReferent='ctx:speaker',targetReferent='ctx:speaker')
   add(l,fam,t,o,'I' if l=='en' and t.startswith('I ') else None,predicate=pred,act=act,polarity=pol,cues=cues,roles=roles,adult=True,register='explicit-colloquial' if fam=='adult_slang' else 'descriptive',reason='Adult-only contextual semantics; '+fam+' is distinct from other consent/desire states; no downstream permission policy')
 for l,t,o in [('it','Mi piace un sacco questo cazzo di film.','questo cazzo di film'),('en','I really like this fucking film.','this fucking film'),('es','Me encanta esta puta película.','esta puta película')]:
  add(l,'profanity_preference',t,o,'I' if l=='en' else None,predicate='preference.like',register='profanity',reason='Profanity intensifies an intelligible preference, not UNKNOWN')
 for l,t,o in [('it','Voglio fare un check-in online.','fare un check-in online'),('en','I want to take a siesta.','take a siesta'),('es','Quiero hacer el check-in online.','hacer el check-in online')]:
  r=add(l,'borrowed_lexicon',t,o,'I' if l=='en' else None,register='borrowed-term');r['provenance']['componentLanguages']=[l,'en' if l!='en' else 'es']
 for l,t,o in [('it','Vorrei un po’ di dirty talk, se ti va.','un po’ di dirty talk'),('en','I want some dirty talk, por favor.','some dirty talk'),('es','Quiero un poco de dirty talk, si te apetece.','un poco de dirty talk')]:
  r=add('code-switch','adult_code_switch',t,o,'I' if l=='en' else None,adult=True,register='code-switch',reason='Natural mixed-language desire is comprehensible and does not imply consent');r['provenance']['componentLanguages']=[l,'en' if l!='en' else 'es'];r['provenance']['primaryLanguage']=l
 for l,t,o in [('it','Cmq voglio restare qui, dai.','restare qui'),('en','BTW, I wanna stay here.','stay here'),('es','Tb quiero quedarme aquí, vale.','quedarme aquí')]:
  add(l,'abbreviation_colloquial',t,o,'I' if l=='en' else None,register='abbreviation-informal')
 for l,t,o,cues in [('it','Non è vero che non mi piace il jazz.','il jazz',['Non','non']),('en','It is not true that I do not like jazz.','jazz',[[6,9],[28,31]]),('es','No es cierto que no me guste el jazz.','el jazz',['No','no'])]:
  add(l,'double_negation',t,o,predicate='preference.like',polarity='POSITIVE',cues=cues,reason='Overt denial of negative preference, two scope cues, positive composed polarity')
 for l,t,o in [('it','Detesto il rumore.','il rumore'),('en','I hate noise.','noise'),('es','Odio el ruido.','el ruido')]:
  add(l,'cue_free_negative',t,o,'I' if l=='en' else None,predicate='preference.like',polarity='NEGATIVE',relation='ATEMPORAL',reason='Lexical dislike expressed without a separable negation cue')
 for l,t,o in [('it','Puoi lavarti le mani?','lavarti le mani'),('en','Could you wash yourself?','wash yourself'),('es','¿Puedes lavarte las manos?','lavarte las manos')]:
  add(l,'grammatical_reflexive',t,o,act='REQUEST',roles={'subjectReferent':'ctx:observer','targetReferent':'ctx:observer','ownerReferent':'ctx:speaker'},decisions=['D04','D07'],reason='Explicit grammatical reflexive target is addressee self, request goal holder speaker')
 for l,t in [('it','...'),('en','—'),('es','…')]:add(l,'zero_claim_boundary',t,zero=True,decisions=['D06'],reason='Punctuation-only observation contains no proposition')
 for l,t in [('it','di a con il'),('en','of to with the'),('es','de a con el')]:add(l,'malformed_no_proposition',t,zero=True,decisions=['D04','D06'],reason='Function-word fragment without recoverable proposition; do not invent intent')
 for l,t,o,s in [('it','Lui vive a Pisa.','Pisa','Lui'),('en','He lives in York.','York','He'),('es','Él vive en Cádiz.','Cádiz','Él')]:
  for ambiguity in [True,False]:
   ctx={'speaker':'cp42-adult-speaker','observer':'cp42-adult-addressee','contextEntities':[{'entityRef':'adult-a','surfaceForms':['Paolo']},{'entityRef':'adult-b','surfaceForms':['Marco']}] if ambiguity else [{'entityRef':'adult-a','surfaceForms':['Paolo']}],'discourse':'Two equally salient adult men; no unique antecedent.' if ambiguity else 'Only Paolo is the established male antecedent.'}
   role='UNKNOWN' if ambiguity else 'entity:adult-a';status={'subjectReferent':'AMBIGUOUS','ownerReferent':'AMBIGUOUS'} if ambiguity else None
   add(l,'ambiguous_binding' if ambiguity else 'resolved_binding_control',t,o,s,predicate='residence.place',entities=[(o,'LOCATION')],roles={'subjectReferent':role,'ownerReferent':role},status=status,context=ctx,decisions=['D06','D07'],reason='Identical surface, different supplied antecedent context; unresolved only when genuinely competing candidates')
 return rows
