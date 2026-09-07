"""Bounded CP37 semantic review inventory. Reads TRAIN only; creates no gold."""
import argparse, collections, json, pathlib, re

def main():
    ap=argparse.ArgumentParser();ap.add_argument('--train',type=pathlib.Path,required=True);ap.add_argument('--output',type=pathlib.Path,required=True);a=ap.parse_args()
    assert a.train.name=='student5_v3'
    m=json.loads((a.train/'migration-manifest.json').read_text());rows=[json.loads(l) for e in m['outputFiles'] for l in (a.train/e['path']).read_text().splitlines()];assert all(r['split']=='train' for r in rows)
    def snapshot(r,c):return {'rowId':r['id'],'claimId':c['claimId'],'language':r['language'],'sourceDatasetId':r['sourceDatasetId'],'text':r['text'][slice(*c['sourceSpan'])],'labels':c['labels'],'temporalEvidence':[r['text'][slice(*t['span'])] for t in c['temporalEvidence']],'subjectSpans':[r['text'][s:e] for s,e in c['subjectSpans']],'negationCues':[r['text'][s:e] for s,e in c['negationCueSpans']]}
    groups={k:[] for k in ['codeSwitchUnresolved','reportedPerspective','futureWordingCurrentRelation','malformedDoubleConTeConMe','explicitFirstPersonMissingSubject','implicitFirstPersonBoundedScreen','opinionWrapperReview']}
    for r in rows:
        for c in r['claims']:
            t=r['text'][slice(*c['sourceSpan'])];z=c['labels'];s=snapshot(r,c)
            if r['language']=='code-switch' and z['predicate']=='speech.unresolved':groups['codeSwitchUnresolved'].append(s)
            if z['claimKind']=='REPORT':groups['reportedPerspective'].append(s)
            if z['predicate']=='goal.object' and z['temporalRelation']['relation']=='CURRENT' and re.search(r'\b(domani|tomorrow|mañana|later|più tardi)\b',t,re.I):groups['futureWordingCurrentRelation'].append(s)
            if 'con te con me' in t:groups['malformedDoubleConTeConMe'].append(s)
            if r['language']=='en' and re.match(r'^I\b',t) and not c['subjectSpans']:groups['explicitFirstPersonMissingSubject'].append(s)
            if r['language'] in {'it','es'} and re.match(r'^(mi chiamo|abito|vivo|voglio|vorrei|ho|sono|me llamo|quiero|tengo|soy)\b',t,re.I):groups['implicitFirstPersonBoundedScreen'].append(s)
            if re.search(r'\b(consider|considero)\b',t,re.I):groups['opinionWrapperReview'].append(s)
    report={'scope':'READ_ONLY_TRAIN_SEMANTIC_REVIEW','definitions':{'codeSwitchUnresolved':'Observed label correlation; clear desire wording conflicts with vocabulary-neutral ontology coverage. No replacement gold authored.','reportedPerspective':'Eight report labels compared to V3 viewpoint definition and normative Anna-said example; legacy speaker perspective requires semantic adjudication.','futureWordingCurrentRelation':'Temporal target ambiguity: time of wanting versus time of desired action. Screen establishes heterogeneous supervision, not a unique corrected label.','malformedDoubleConTeConMe':'Exact duplicated participant phrase; six row instances/four unique surfaces, reviewed as template quality issue.','explicitFirstPersonMissingSubject':'English explicit I at claim start, no subject span; distinct from correctly empty implicit first-person subjects.','implicitFirstPersonBoundedScreen':'Limited IT/ES first-person lexical prefixes; descriptive annotation consistency check, not a universal grammatical parser.','opinionWrapperReview':'Overt consider/considero wrapper with DIRECT; reviewer decision needed under BELIEF definition.'},'groups':{k:{'count':len(v),'uniqueSurfaces':len({(x['language'],x['text']) for x in v}),'byLanguage':dict(collections.Counter(x['language'] for x in v)),'examples':v if len(v)<=30 else v[:20]} for k,v in groups.items()},'implicitScreenNonSpeakerOrNonemptySubject':sum(x['labels']['subjectReferent']!='ctx:speaker' or bool(x['subjectSpans']) for x in groups['implicitFirstPersonBoundedScreen']),'devRead':False,'frozenRead':False,'goldCreatedOrChanged':False}
    a.output.write_text(json.dumps(report,ensure_ascii=False,indent=2)+'\n')
    print(json.dumps({k:{kk:vv for kk,vv in v.items() if kk!='examples'} for k,v in report['groups'].items()},ensure_ascii=False))

if __name__=='__main__':main()
