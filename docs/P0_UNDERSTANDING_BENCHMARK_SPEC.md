# P0 — Matrix Understanding Benchmark Specification

## Obiettivo
Determinare quale front-end linguistico offre il miglior compromesso fra qualità semantica Matrix, robustezza trilingue e costo mobile.

## Candidati
A. Baseline deterministica corrente Matrix.
B. Android ICU + Apache OpenNLP + semantic mapper Matrix.
C. Modello NLU ONNX compatto + semantic mapper Matrix.

Nessun candidato è vincitore a priori.

## Target linguistico
- Italiano: primario.
- Inglese: obbligatorio.
- Spagnolo: obbligatorio.

La stessa struttura semantica deve essere prodotta nelle tre lingue.

## Contratto Matrix da preservare
Output minimo per claim:
- speaker;
- subject;
- target;
- owner;
- perspective/belief holder;
- dialogue act;
- predicate;
- object;
- polarity;
- negation scope;
- temporal validity;
- entity spans/resolution;
- provenance/source spans/source IDs;
- explicit/hypothesis/unknown.

Il linguaggio può cambiare; il contratto semantico no.

## Famiglie di test obbligatorie
1. identità/nome;
2. età;
3. preferenze e avversioni;
4. lavoro/ruolo;
5. residenza e presenza;
6. possesso;
7. terze persone/NPC;
8. pronomi e riferimenti recenti;
9. multi-claim/coordinazione;
10. negazione locale;
11. correzione/supersession;
12. passato/presente/futuro;
13. domande/richieste/ipotesi;
14. ambiguità lessicale;
15. nomi propri vs aggettivi (`sono Alberto` vs `sono bello` e equivalenti EN/ES);
16. code-switch controllato;
17. input colloquiali, punteggiatura imperfetta e forme brevi.

## Gold set
Creare un dataset Matrix-specifico versionato con split train/dev/test bloccato. Le frasi IT/EN/ES devono essere parafrasi naturali, non mere traduzioni meccaniche. MASSIVE/UD e altri dataset possono fornire esempi o pretraining, ma non sostituiscono l'annotazione Matrix.

Il test set finale non deve essere usato per tarare le regole o il modello.

## Metriche qualità
- exact match numero claim;
- exact/F1 dei campi principali;
- span F1;
- negation-scope F1;
- entity type/link F1;
- owner/perspective exact;
- unknown rate;
- false structured claim rate;
- leakage ownership: tolleranza zero sul critical set;
- invented World Truth: tolleranza zero.

Confidence non va chiamata probabilità calibrata finché non viene misurata con Brier/ECE.

## Metriche mobile
Sul Moto G56 o build Android equivalente misurare:
- cold init;
- warm p50/p95;
- peak PSS/delta PSS rispetto alla baseline;
- CPU;
- dimensione APK;
- dimensione modelli/dati;
- thermal loop su sequenza prolungata;
- nessuna rete.

Budget iniziale di supervisione, non criterio finale:
- ICU/OpenNLP: obiettivo indicativo delta PSS <= 40 MB;
- ONNX compatto: obiettivo indicativo delta PSS <= 80 MB;
- valori superiori richiedono un guadagno di qualità sostanziale e decisione esplicita.

## Regola BUILD/REUSE/ADAPT
Prima di scrivere un parser custom, verificare se la stessa capacità è già fornita in modo maturo da ICU, OpenNLP, standard Unicode, modelli/data compatibili o algoritmi pubblicati. Non importare dipendenze complete quando basta un componente/algoritmo più piccolo.

## Research Depth Protocol
Per ogni dipendenza/modello/dataset candidato:
1. documentazione/repository/paper primari;
2. release/commit e manutenzione;
3. GitHub Issues/PR recenti per bug e limiti;
4. esperienza pratica/community quando utile;
5. secondo passaggio Devil's Advocate contro il candidato favorito;
6. licenza, provenance, compatibilità commerciale e Android/offline;
7. motivazione finale KEEP/REUSE/ADAPT/REJECT.

## Stop conditions
Non integrare nulla nel runtime principale se:
- manca licenza/provenance;
- richiede rete;
- rompe ownership/perspective;
- inventa World Truth;
- non generalizza nelle tre lingue;
- il costo mobile supera il beneficio;
- il confronto non usa lo stesso gold set.

## Deliverable P0
Produrre:
- codice/prototipi isolati;
- gold set versionato;
- runner unico;
- risultati per lingua e worst-language;
- profilo RAM/CPU/latency/dimensione;
- tabella comparativa A/B/C;
- error analysis;
- Devil's Advocate del vincitore;
- raccomandazione `KEEP / ADAPT / REPLACE` per il front-end Understanding Matrix.

Nessuna modifica alla personalità Luna, al GGUF o alla memoria production è ammessa in P0.