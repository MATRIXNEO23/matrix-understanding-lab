"""Read-only Gate-B readiness audit; no model, training or held-out I/O."""
import argparse, ast, collections, copy, hashlib, json, pathlib, sys

def digest(data):
    return hashlib.sha256(data).hexdigest()

def main():
    ap = argparse.ArgumentParser()
    ap.add_argument('--train', type=pathlib.Path, required=True)
    ap.add_argument('--tree', type=pathlib.Path, required=True)
    ap.add_argument('--source', type=pathlib.Path, required=True)
    ap.add_argument('--output', type=pathlib.Path, required=True)
    args = ap.parse_args()
    sys.path.insert(0, str(args.source))
    import evaluate_v3
    from test_evaluate_v3 import gold_and_prediction
    expected_tree = json.loads(args.tree.read_text())
    git_checks = []
    for e in expected_tree:
        name = e['path'].removeprefix('data/student5_v3/')
        data = (args.train / name).read_bytes()
        sha = hashlib.sha1(b'blob '+str(len(data)).encode()+b'\0'+data).hexdigest()
        git_checks.append({'path':e['path'], 'match':sha==e['sha']})
    sha_checks=[]
    for line in (args.train/'SHA256SUMS').read_text().splitlines():
        sha,name=line.split('  ',1)
        sha_checks.append({'path':name,'match':digest((args.train/name).read_bytes())==sha})
    manifest=json.loads((args.train/'migration-manifest.json').read_text())
    data=b''.join((args.train/e['path']).read_bytes() for e in manifest['outputFiles'])
    rows=[json.loads(line) for line in data.splitlines() if line]
    provenance=[json.loads(line) for e in manifest['provenanceFiles'] for line in (args.train/e['path']).read_text().splitlines() if line]
    splits=collections.Counter(r.get('split') for r in rows)
    sources=collections.Counter(r.get('sourceDatasetId') for r in rows)
    templates=collections.Counter(r.get('provenance',{}).get('sourceProvenance',{}).get('templateSplit','not-recorded') for r in rows)
    train={'artifactId':manifest['outputDatasetId'],'logicalSha256':digest(data),'expectedLogicalSha256':manifest['outputChecksum'],'manifestSha256':digest((args.train/'migration-manifest.json').read_bytes()),'gitBlobChecks':git_checks,'perFileSha256Checks':sha_checks,'rows':len(rows),'claims':sum(len(r['claims']) for r in rows),'splits':dict(splits),'sourceDatasetCounts':dict(sources),'sourceTemplateSplitCounts':dict(templates),'provenanceRecords':len(provenance),'provenanceSourceCounts':dict(collections.Counter(r['sourceDatasetId'] for r in provenance)),'languages':dict(collections.Counter(r['language'] for r in rows)),'nonTrainRows':sum(r.get('split')!='train' for r in rows)}
    train['integrityPass']=all(e['match'] for e in git_checks+sha_checks) and train['logicalSha256']==manifest['outputChecksum'] and train['manifestSha256']=='87b4a43035d2e3d84a6d599e1f81b497af6e2f36e4ef2c470adb87341c17da98'
    gold,prediction=gold_and_prediction()
    baseline=evaluate_v3.score_v3_rows([gold],[prediction])
    probes={}
    for name in ['wrongBoundary','wrongMentionIdentity','forbiddenDownstreamField','extraClaim','missingClaim']:
        p=copy.deepcopy(prediction)
        if name=='wrongBoundary': p['claims'][0]['sourceSpan']=[1,len(gold['text'])]
        if name=='wrongMentionIdentity': p['mentions'][0]['span']=[6,10]
        if name=='forbiddenDownstreamField': p['worldTruth']=True
        if name=='extraClaim': p['claims'].append(copy.deepcopy(p['claims'][0]))
        if name=='missingClaim': p['claims']=[]
        try: probes[name]={'rejected':False,'metrics':evaluate_v3.score_v3_rows([gold],[p])}
        except Exception as ex: probes[name]={'rejected':True,'exception':type(ex).__name__+': '+str(ex)}
    functions={}
    identities={}
    for name in ['evaluate_v3.py','inference_v3.py','referent_candidates.py','contract_v3.py','select_threshold.py','analyze_errors.py']:
        raw=(args.source/name).read_bytes()
        identities[name]={'sha256':digest(raw),'bytes':len(raw)}
        tree=ast.parse(raw)
        functions[name]=[n.name for n in tree.body if isinstance(n,(ast.FunctionDef,ast.ClassDef))]
    report={'scope':'GATE_B_READINESS_ONLY','sourceHead':'1ef81d3e8d7b92d9cbd2bf5f54e6d3d1918f8973','train':train,'softwareProbes':{'fixture':'existing test_evaluate_v3.gold_and_prediction; English synthetic test fixture, not DEV','baseline':baseline,'mutations':probes},'sourceIdentities':identities,'topLevelFunctions':functions,'devRead':False,'frozenRead':False,'trainingExecuted':False,'modelExecuted':False,'datasetModified':False,'devToTrainCopyPerformed':False,'trainDevOverlapVerified':False}
    args.output.write_text(json.dumps(report,indent=2)+'\n')
    print(json.dumps({'trainIntegrityPass':train['integrityPass'],'trainRows':len(rows),'trainFiles':len(git_checks),'fileShaChecks':len(sha_checks),'splits':dict(splits),'templates':dict(templates),'probeResults':{n:({'rejected':r['rejected']} if r['rejected'] else {'claimExact':r['metrics']['claimExact'],'claimCountExact':r['metrics']['claimCountExact'],'ownershipCorruptions':r['metrics']['ownershipCorruptions']}) for n,r in probes.items()}}))

if __name__=='__main__':
    main()
