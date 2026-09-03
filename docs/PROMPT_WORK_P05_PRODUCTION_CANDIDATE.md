# WORK PROMPT — P0.5 PRODUCTION CANDIDATE

## Modalità
`CODEX-L3 — ALTO / STRICT EXECUTION`

## Obiettivo
Trasformare Candidate B (`ICU + Apache OpenNLP + Matrix Semantic Mapper`) da baseline di laboratorio a candidato production utilizzabile nel Matrix Core Prototype v1, senza modificare ancora la repo production `MATRIXNEO23/8.10.9evo3-solo-gpt`.

## Problemi da risolvere concretamente
1. **Licenza/provenance italiano**: il modello italiano P0 è bloccato per derivazione non-commerciale. Va sostituito con training/provenance commercialmente compatibile.
2. **Residual errors**: correggere alla causa S08-it, S16-en, S18-it, S18-es e verificare il falso hint `Mañana -> LOCATION` in S16-es senza hardcode dei caseId/test string.
3. **Generalizzazione insufficiente**: 22 scenari sono pochi. Ampliare il corpus adversarial prima di qualsiasi tuning finale.
4. **Autonomia di Work**: dataset conversion, training, validation, artifact, checksum, report e CI devono essere automatizzati end-to-end; nessun addestramento manuale dell'utente.
5. **Riduzione test telefono**: tutto ciò che è verificabile in CI/JVM/emulatore deve essere verificato prima del Moto. Il Moto è gate hardware finale per PSS/CPU/latency/thermal e integrazione reale.

## Decisioni tecniche già approvate
- direzione favorita: `Android ICU + Apache OpenNLP + Matrix Semantic Mapper`;
- ONNX custom non è priorità e non va iniziato salvo fallimento dimostrato del percorso B;
- mantenere typed claims, ownership, perspective, provenance e World Truth safety;
- niente B4, vector DB, graph DB, BDI, appraisal o reflection production in questo checkpoint;
- niente modifica GGUF/personality/sampling;
- niente espansione massiva di regex come soluzione.

## Gate P0.5

### Gate 00 — Truth
Verifica HEAD, working tree, P0 verdict, risultati machine-readable e commit di riferimento. Nessuna modifica production.

### Gate 01 — Clean Italian data plan
Costruire una matrice di corpus italiani candidati con licenza/provenance verificata. Escludere dal training production qualsiasi corpus/modello con clausola NC o provenance ambigua. Distinguere chiaramente `training_allowed`, `reference_only`, `rejected_for_training`.

Priorità: corpus UD italiani con licenza commercialmente compatibile e provenienza verificabile; non assumere che BY-SA sia automaticamente adatto al packaging finale: documentare gli obblighi e preferire BY/Apache/MIT/public-domain quando la qualità è sufficiente.

### Gate 02 — Automated trainer
Implementare pipeline riproducibile:
`source datasets -> normalization/conversion -> frozen train/dev/test -> OpenNLP training -> model artifact -> checksum -> metadata/provenance -> benchmark`.

Deve essere lanciabile da Work/CI senza intervento manuale dell'utente. Versioni, seed e input devono essere bloccati.

### Gate 03 — Expanded adversarial benchmark
Prima di correggere i residuali, ampliare il gold set con nuovi casi indipendenti IT/EN/ES, con italiano primario. Includere almeno:
- imperativi/request;
- `would like` / `vorrei` / `me gustaría` come goal vs preference;
- articoli/preposizioni fuse dei luoghi;
- temporal words omonime/ambigue (`mañana`, `prima`, `after`, ecc.);
- pro-drop e pronomi;
- multi-claim;
- correzioni;
- ipotesi;
- negazioni;
- entità multi-token;
- input colloquiali/incompleti;
- code-switch;
- false positives identity/attribute.

Congelare un test set nuovo prima dei fix.

### Gate 04 — Causal residual fixes
Correggere i failure P0 alla causa, mai per caseId/stringa test-specifica.

Obblighi:
- S08-it: normalizzazione coerente del location object senza rompere source span/entity mention;
- S16-en: distinguere desiderio/goal da semplice preference;
- S18-it/es: riconoscimento request/imperative robusto anche quando POS sbaglia la prima parola;
- S16-es: impedire che un'espressione temporale già riconosciuta venga promossa anche a LOCATION salvo evidenza indipendente.

Aggiungere regressioni linguistiche equivalenti non identiche.

### Gate 05 — Production-clean Italian model benchmark
Confrontare:
A. P0 B originale lab-only;
B. nuovo modello italiano clean;
C. eventuali varianti clean minime necessarie.

Metriche minime:
- main-field exact;
- claim-count exact;
- entity F1;
- negation F1;
- unknown rate;
- ownership violations;
- invented World Truth;
- worst-language;
- test-split frozen.

GO quality preliminare: test field exact >= 0.97, zero ownership violations, zero invented World Truth. Se il clean model non raggiunge il gate, non integrare: produrre root-cause e candidato successivo.

### Gate 06 — CI autonomy
CI deve produrre automaticamente:
- unit/regression tests;
- full benchmark JSON;
- human report;
- trained model artifact + SHA-256 + provenance;
- Android probe APK;
- size breakdown;
- no-INTERNET permission check;
- failure summary.

### Gate 07 — Pre-Moto elimination
Prima del telefono eseguire tutto ciò che è possibile su CI/emulatore/JVM. Non chiedere all'utente test esplorativi per bug funzionali già riproducibili offline.

### Gate 08 — Moto final probe package
Preparare un solo pacchetto di test Moto con istruzioni minime e output automatico. Deve misurare PSS, CPU, cold/warm latency, APK/model bytes e thermal loop. L'utente deve idealmente solo installare/eseguire/esportare il JSON.

Target RAM incrementale consigliato: mantenere l'Understanding nell'ordine di poche decine di MB PSS; un incremento nell'ordine di centinaia di MB è NO-GO salvo beneficio eccezionale documentato.

### Gate 09 — Verdict
Produrre uno dei tre verdetti:
- `GO_PRODUCTION_CANDIDATE`: clean provenance + quality gate + CI complete; manca solo Moto hardware gate;
- `GO_LAB_ONLY`: qualità buona ma licenza/provenance ancora bloccata;
- `NO_GO`: qualità/generalizzazione/costo non sufficienti.

Non modificare production in questo checkpoint. Tornare al supervisore con evidenze e raccomandazione esatta.

## Regola Senior Engineer
Se durante il lavoro emerge un'alternativa più matura, più leggera o più robusta che risolve uno dei sottoproblemi senza cambiare l'intero stack, Work deve valutarla come `REUSE / ADAPT / REIMPLEMENT_FROM_PRINCIPLES / REFERENCE_ONLY`, non ignorarla. Se richiede una nuova decisione architetturale sostanziale, fermarsi con `DECISION_REQUIRED` e raccomandazione motivata.

## Handoff richiesto
Riportare:
- HEAD/commit;
- corpus realmente usati e licenze;
- pipeline trainer riproducibile;
- dimensione e SHA-256 modello;
- benchmark vecchio vs clean;
- error analysis;
- regressioni;
- CI run/artifact;
- APK probe;
- cosa resta non verificato;
- verdetto Gate 09.
