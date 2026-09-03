# AUTOMATIC TRAINING FIRST POLICY

## Regola canonica
Quando una capacità di Matrix può essere ottenuta in modo affidabile tramite training automatico e sono disponibili dati sufficienti con provenance/licenza compatibili, Work deve valutare il percorso di training **prima** di espandere manualmente regole, regex, lessici o mapper.

La domanda non è se il componente sappia già fare la funzione. La domanda è: **può apprenderla automaticamente con il materiale disponibile, mantenendo i contratti Matrix e il budget Android?**

## Obbligo di valutazione
Per ogni sottoproblema linguistico o semantico, confrontare almeno:
1. regola deterministica manuale;
2. training automatico di un componente esistente (es. OpenNLP o altro trainer maturo);
3. training/adattamento automatico di un componente Matrix;
4. soluzione ibrida: segnali linguistici addestrati + mapper Matrix deterministico.

La scelta deve essere basata su qualità, generalizzazione, footprint, costo di manutenzione, riproducibilità, licenza/provenance e capacità di esecuzione autonoma in CI.

## Autonomia
Se il training è tecnicamente supportato e i dati sono disponibili, Work deve automatizzare end-to-end:
`dataset -> validation/provenance -> conversion -> split frozen -> training -> evaluation -> error analysis -> retraining/tuning -> artifact -> checksum -> CI report`.

Non richiedere all'utente addestramento manuale, selezione di iperparametri o interventi tra iterazioni ordinarie.

Work deve iterare autonomamente fino a raggiungere il gate o dimostrare con evidenze che il training non è competitivo.

## Deterministico Matrix
Il fatto che il mapper Matrix sia oggi rule-based non impedisce di addestrare componenti che producano i segnali o le decisioni necessarie. Sono ammesse, se validate:
- modelli POS/morfologici/NER addestrati;
- classificatori di dialogue act/predicate/intent;
- slot/span tagger;
- ranker o resolver addestrati;
- rule induction o ottimizzazione automatica di regole/lessici;
- distillazione di comportamento in un componente leggero;
- combinazioni ibride con safety/ownership/provenance deterministici.

Non generare automaticamente codice/regole e promuoverlo senza regressioni complete. Ogni modifica appresa deve superare test congelati e safety gates.

## Priorità per P0.5
Nel lavoro corrente su Candidate B, prima di aggiungere fix linguistici manuali ripetitivi, Work deve verificare se il problema può essere assorbito da training/adattamento automatico con dati puliti. I fix deterministici restano appropriati per invarianti di sicurezza, ownership, provenance, exclusivity e normalizzazioni formalizzabili; la copertura linguistica generale deve preferire apprendimento automatico quando i dati e il footprint lo rendono conveniente.
