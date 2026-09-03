# PROMPT WORK — P0 MATRIX UNDERSTANDING LAB

## Modalità
`CODEX-L3 — ALTO / STRICT BENCHMARK LAB`

## Missione
Lavora esclusivamente su `MATRIXNEO23/matrix-understanding-lab`.

Leggi integralmente:
1. `README.md`;
2. `docs/P0_UNDERSTANDING_BENCHMARK_SPEC.md`.

Usa come riferimento semantico il runtime Matrix principale congelato `MATRIXNEO23/8.10.9evo3-solo-gpt` commit `ae82d5cf843d52b3d60caadd161e4a5516fc5d0d`, ma NON modificarlo.

Obiettivo: costruire il benchmark P0 che confronta:
A. baseline deterministica Matrix;
B. ICU + Apache OpenNLP + mapper Matrix;
C. NLU ONNX compatto + mapper Matrix.

## Regola critica
Non assumere che B o C siano migliori. Devi provare o falsificare la superiorità con gli stessi casi, metriche e vincoli.

Prima di implementare ogni candidato applica BUILD/REUSE/ADAPT/REIMPLEMENT/REFERENCE/REJECT e Research Depth Protocol: fonti primarie, issue/PR recenti, manutenzione, licenza/provenance, Android/offline, Devil's Advocate.

### Regola anti-scarto prematuro — OBBLIGATORIA
Il requisito finale Matrix è IT/EN/ES con italiano primario, ma **un candidato NON deve essere eliminato dalla ricerca soltanto perché non copre da solo tutte e tre le lingue**.

Per ogni tecnologia, algoritmo, modello, dataset, lessico o motore trovato, classificare separatamente:
- `FULL_CANDIDATE`: può concorrere direttamente come soluzione completa IT/EN/ES;
- `PARTIAL_REUSE`: componente maturo riusabile per una o più lingue o sottoproblemi;
- `ADAPT`: riusabile con adattamento/training/configurazione compatibile;
- `REIMPLEMENT_FROM_PRINCIPLES`: implementazione diretta non adatta, ma algoritmo/architettura/comportamento pubblico è abbastanza valido da meritare una reimplementazione indipendente Matrix;
- `REFERENCE_ONLY`: utile come benchmark, tassonomia, gold source, algoritmo di riferimento o confronto, ma non come dipendenza production;
- `REJECT`: non offre valore sufficiente neppure come componente/reference, con motivo documentato.

`non multilingue`, `non Android-ready`, `linguaggio diverso`, `dipendenza troppo pesante` o `licenza non adottabile direttamente` **non equivalgono automaticamente a REJECT**. Prima valutare se il candidato contiene un algoritmo, dataset, struttura, tassonomia, modello per singola lingua o principio tecnico migliore del nostro che possa essere adattato, combinato o reimplementato legalmente e tecnicamente.

Il prodotto finale deve comunque soddisfare IT/EN/ES: una composizione di componenti specializzati è ammessa come candidato se il risultato complessivo è più accurato/leggero/manutenibile di un unico componente multilingue.

Non favorire la composizione per principio: deve vincere sul benchmark globale e sul costo Android.

## Gate

### Gate 00 — Truth
Verifica repo, branch, working tree e struttura del laboratorio. Leggi la specifica. Nessuna modifica alla repo Matrix principale.

### Gate 01 — Contract extraction
Estrarre dal Matrix principale solo il contratto necessario dell'Understanding: schema claim, ownership, perspective, provenance, predicate taxonomy e casi Golden rilevanti. Non trascinare dipendenze UI/gameplay non necessarie.

### Gate 02 — Gold-set design
Creare schema dati versionato e dataset Matrix-specifico IT/EN/ES con split bloccato. Includere famiglie e casi critici della specifica, inclusi falsi positivi (`sono Alberto`/`sono bello` e equivalenti).

### Gate 03 — Baseline A
Portare nel laboratorio una baseline riproducibile del comportamento deterministico corrente, mantenendo la semantica del commit congelato. Test e risultati separati per lingua.

### Gate 04 — Candidate B research
Verificare versioni correnti, modelli IT/EN/ES disponibili, licenze e footprint teorico di ICU/OpenNLP. Cercare issue/PR recenti e limiti.

Inoltre eseguire una ricerca laterale di componenti/algoritmi maturi che possano migliorare Candidate B anche se monolingua o parziali. Non scartarli per sola copertura linguistica: classificarli con la tassonomia anti-scarto e registrare cosa potrebbero sostituire/migliorare in Matrix.

Documentare cosa viene realmente usato, cosa resta reference e cosa viene escluso con motivazione.

### Gate 05 — Candidate B implementation
Implementare il minimo necessario ICU/OpenNLP + mapper Matrix. È ammessa una composizione con componenti `PARTIAL_REUSE/ADAPT` emersi dal Gate 04 solo se mantiene confronto riproducibile e non gonfia artificialmente B. Niente dipendenze superflue. Nessun hardcode del test set.

### Gate 06 — Candidate C research
Selezionare un approccio ONNX compatto realistico per joint classification/span tagging o equivalente. Verificare runtime mobile, quantizzazione, licenza/provenance, dimensione e disponibilità dati IT/EN/ES.

Applicare anche qui la regola anti-scarto: un modello/algoritmo eccellente su una sola lingua o sottotask può essere `PARTIAL_REUSE`, `ADAPT`, `REIMPLEMENT_FROM_PRINCIPLES` o `REFERENCE_ONLY` e deve restare nell'analisi. Se non esiste un candidato C completo legalmente e tecnicamente valido entro lo scope, documentare `CANDIDATE_C_NOT_READY` invece di inventarne uno.

### Gate 07 — Candidate C implementation
Implementare solo se Gate 06 trova un candidato valido e riproducibile. Altrimenti saltare con evidenza, senza bloccare A/B.

### Gate 08 — Unified runner
Un solo runner e uno stesso gold set per A/B/C. Output machine-readable e report umano.

### Gate 09 — Quality benchmark
Misurare metriche della specifica per lingua e worst-language. Critical ownership/World Truth violations sono failure assolute.

### Gate 10 — Mobile footprint plan/measurement
Preparare e, se tecnicamente possibile nel laboratorio, produrre build Android/probe per misurare cold/warm latency, PSS, CPU, APK/model bytes e thermal loop su Moto G56. Se il telefono non è accessibile a Work, predisporre strumentazione e artifact per il test manuale senza inventare misure.

### Gate 11 — Error analysis
Classificare errori per famiglia: segmentation, POS/morphology, predicate mapping, entity resolution, negation, temporalità, ownership, ambiguity, code-switch.

### Gate 12 — Devil's Advocate
Attaccare il candidato migliore: cercare bug noti, casi adversarial, manutenzione/licenza/footprint e alternative più leggere. Riesaminare anche i migliori `PARTIAL_REUSE/ADAPT/REIMPLEMENT_FROM_PRINCIPLES`: verificare se una composizione o reimplementazione mirata potrebbe battere il favorito. Il vincitore deve sopravvivere a questo passaggio.

### Gate 13 — Verdict
Produrre tabella finale A/B/C e una seconda tabella dei candidati parziali/reference con classificazione e possibile valore futuro. Raccomandazione `KEEP / ADAPT / REPLACE` per il front-end Matrix. Non autorizzare integrazione production: torna al supervisore.

## Divieti
- non modificare `8.10.9evo3-solo-gpt`;
- non iniziare B4, memoria Room, retrieval, BDI, appraisal o reflection production;
- non cambiare Luna/GGUF/sampling;
- non utilizzare servizi cloud come dipendenza runtime;
- non usare il test set per taratura;
- non nascondere unknown/failure con fallback che inventa claim;
- non importare dataset/modelli senza record licenza/provenance;
- non copiare codice/modelli incompatibili: `REIMPLEMENT_FROM_PRINCIPLES` richiede progettazione indipendente basata su principi/algoritmi/spec pubbliche e provenance documentata.

## Handoff
Riportare commit finali, struttura, dataset/gold split, dipendenze/versioni/licenze, risultati A/B/C, failure critiche, stime/misure mobile, limiti, Devil's Advocate, tabella `FULL_CANDIDATE/PARTIAL_REUSE/ADAPT/REIMPLEMENT_FROM_PRINCIPLES/REFERENCE_ONLY/REJECT` e raccomandazione. Terminare con: `P0 pronto per contro-review del supervisore; nessuna integrazione production autorizzata.`