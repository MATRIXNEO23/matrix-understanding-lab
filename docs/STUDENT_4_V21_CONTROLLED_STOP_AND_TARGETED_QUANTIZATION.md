# Student-4-v2.1 — Controlled Stop, Metric Review and Targeted Quantization

Data: 2026-09-04
Repo: `MATRIXNEO23/matrix-understanding-lab`
Run osservato: `33837897457`
Commit del run: `72f14286e89df88f41aedb169c7307b26b57eedf`

## Decisione operativa

Lo stop del run `33837897457` va interpretato come **controlled stop per valutazione metrica dev prima di qualunque accesso frozen**, non come fallimento qualitativo del modello.

Non procedere con retraining cieco e non aprire frozen/test finché il dev gate ufficiale non è completato e discusso.

## Stato reale del run

- Software regression tests: PASS.
- Dataset v2 build: PASS.
- Dataset audit: PASS.
- MASSIVE auxiliary train/dev supervision: completata.
- Training Student-4-v2.1: completato.
- Early stop: epoch 7, patience 2.
- Best dev score: `0.9676758069767126`.
- Frozen: NON letto.
- Artifact caricati:
  - `matrix-nlu-student-4-v21-report-33837897457`
  - `matrix-nlu-student-4-v21-bundle-33837897457`
  - `matrix-nlu-student-4-v21-resume-33837897457`

La failure finale del job è meccanica:

```text
ModuleNotFoundError: No module named 'matrix_nlu'
```

Causa probabile: lancio diretto dello script `matrix_nlu/controlled_dev_v21.py` senza garantire che la root repo sia nel `PYTHONPATH` / modulo importabile nel contesto GitHub Actions.

## Regola immediata

Prima di qualunque nuovo training:

1. Correggere il packaging/import del controlled dev gate.
2. Valutare il bundle già prodotto dal run `33837897457`.
3. Generare `controlled-stop-summary.json`, `threshold-selection.json`, `dev-error-analysis.json` e predizioni dev complete.
4. Solo dopo decidere se:
   - accettare il dev gate;
   - fare targeted fine-tune sulle famiglie deboli;
   - modificare dataset/supervision;
   - passare a frozen gate autorizzato.

## Metriche principali già viste dal training

### Best dev generale

- Best dev score: `0.9676758069767126`.
- Parametri totali: `58,599,411`.
- Encoder layers: `4`.

### Epoch 5 — punto migliore osservato

`matrixDev`

- macroHeadAccuracy: `0.9856194464793223`
- sequence.claimKind: `1.0`
- sequence.dialogueAct: `1.0`
- sequence.ownerReferent: `1.0`
- sequence.perspectiveReferent: `1.0`
- sequence.polarity: `0.9567901234567902`
- sequence.predicate: `0.9897119341563786`
- sequence.subjectReferent: `1.0`
- sequence.targetReferent: `1.0`
- sequence.temporalRelation: `1.0`
- tokens.boundary: `0.9869036482694107`
- tokens.entity: `0.9879638916750251`
- tokens.negation: `0.8736208625877633`
- tokens.object: `0.9893012370444667`
- tokens.subject: `1.0`
- tokens.temporal: `1.0`

`p05Dev`

- macroHeadAccuracy: `0.9497321674741029`
- sequence.claimKind: `1.0`
- sequence.dialogueAct: `0.8690476190476191`
- sequence.ownerReferent: `1.0`
- sequence.perspectiveReferent: `1.0`
- sequence.polarity: `0.9285714285714286`
- sequence.predicate: `0.8095238095238095`
- sequence.subjectReferent: `0.9166666666666666`
- sequence.targetReferent: `0.9285714285714286`
- sequence.temporalRelation: `0.8928571428571429`
- tokens.boundary: `1.0`
- tokens.entity: `0.9875930521091811`
- tokens.negation: `0.9826302729528535`
- tokens.object: `0.9429280397022333`
- tokens.subject: `1.0`
- tokens.temporal: `0.9875930521091811`

## Interpretazione tecnica

Il modello non è collassato. Il comportamento è promettente ma non ancora promuovibile.

Punti forti:

- owner/perspective molto stabili;
- claimKind stabile;
- matrixDev molto alto;
- loss e early stop coerenti;
- nessuna evidenza che frozen sia stato letto.

Punti deboli da proteggere:

- `tokens.negation` su matrixDev: fragile;
- `p05Dev.sequence.predicate`: fragile;
- `p05Dev.sequence.dialogueAct`: sotto soglia desiderata;
- `p05Dev.sequence.subjectReferent`: da monitorare;
- `p05Dev.sequence.targetReferent`: da monitorare;
- `p05Dev.sequence.temporalRelation`: da monitorare;
- `tokens.object` su p05Dev: da monitorare.

## Quantizzazione mirata

La quantizzazione NON deve essere globale e cieca.

Obiettivo: ridurre dimensione e latenza senza degradare le parti deboli del modello.

### Regola

Prima della quantizzazione:

1. Completare il dev gate sul bundle `33837897457`.
2. Salvare baseline FP32/torch completa.
3. Eseguire export ONNX non quantizzato.
4. Misurare dev head-by-head e token-class-by-token-class.

Dopo la quantizzazione:

1. Ripetere identica valutazione dev.
2. Confrontare delta per ogni head/classe.
3. Bloccare il candidato se peggiora le famiglie fragili oltre soglia.

### Protezione teste/classi deboli

Proteggere o quantizzare in modo meno aggressivo:

- head/token path legati a `tokens.negation`;
- classifier/head di `sequence.predicate`;
- `sequence.dialogueAct`;
- `sequence.subjectReferent`;
- `sequence.targetReferent`;
- `sequence.temporalRelation`;
- token classifier `tokens.object`.

Più permissivi su componenti stabili:

- `sequence.claimKind`;
- `sequence.ownerReferent`;
- `sequence.perspectiveReferent`;
- eventuali layer/weights che non producono delta significativo su classi fragili.

### Candidati di quantizzazione da provare

Ordine raccomandato:

1. ONNX FP32 baseline.
2. Dynamic INT8 standard su pesi encoder, senza cambiare soglie.
3. Dynamic INT8 selettivo con esclusione/protezione delle teste fragili.
4. Se disponibile e stabile: mixed precision / per-channel weight-only.
5. Evitare quantizzazione aggressiva su activation se degrada negation/predicate.

### Gate minimi di accettazione

Un quantizzato è accettabile solo se:

- `matrixDev.macroHeadAccuracy` resta vicino alla baseline;
- `p05Dev.macroHeadAccuracy` resta vicino alla baseline;
- `tokens.negation` non peggiora in modo materiale;
- `p05Dev.sequence.predicate` non peggiora;
- nessun head forte collassa;
- threshold selection resta valida;
- size/latency migliorano abbastanza da giustificare il rischio.

Soglie iniziali conservative:

- delta massimo macro: `-0.005`;
- delta massimo su famiglie fragili: `-0.002` preferito, `-0.005` massimo da discutere;
- zero regressioni qualitative critiche su esempi dev di negazione, predicate, referenti e temporalità.

## Blocco operativo

Non promuovere Student-4-v2.1 a runtime Android e non aprire frozen gate finché non esistono:

- controlled dev gate completo;
- error analysis leggibile;
- threshold selection;
- baseline FP32/ONNX;
- confronto quantizzato mirato;
- decisione esplicita `KEEP / RETRAIN / TARGETED_FINE_TUNE / QUANTIZE / REJECT`.

## Prossima azione corretta

Usare il bundle già salvato dal run `33837897457` e rilanciare solo la valutazione controllata dev dopo fix import, senza rifare training.
