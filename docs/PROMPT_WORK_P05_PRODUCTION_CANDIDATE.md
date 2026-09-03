# WORK PROMPT — P0.5 PRODUCTION CANDIDATE

## Modalità
`CODEX-L3 — ALTO / STRICT EXECUTION / AUTONOMOUS UNTIL GATE`

## Obiettivo
Trasformare Candidate B (`ICU + Apache OpenNLP + Matrix Semantic Mapper`) da baseline di laboratorio a candidato production utilizzabile nel Matrix Core Prototype v1, senza modificare ancora la repo production `MATRIXNEO23/8.10.9evo3-solo-gpt`.

## Mandato di autonomia — OBBLIGATORIO
Work non deve fermarsi al primo tentativo, al primo modello addestrato o ai primi fix verdi. Deve iterare autonomamente per tutto il tempo necessario su ricerca, dataset, conversione, training, error analysis, fix causali, regressioni e benchmark finché accade una delle due condizioni:

1. raggiunge tutti i gate di qualità/provenance/CI definiti sotto; oppure
2. incontra un blocco realmente non risolvibile con gli strumenti e le fonti disponibili e produce `DECISION_REQUIRED` con evidenze, alternative già provate e raccomandazione tecnica.

Non chiedere all'utente scelte tecniche intermedie. Non tornare al supervisore per micro-decisioni, fallimenti ordinari di training, regressioni correggibili o tuning necessario. Correggere e proseguire.

Ogni iterazione deve preservare un test set congelato e non deve ottimizzare direttamente sui casi di test. Se un fix migliora un caso ma peggiora regressioni o generalizzazione, annullarlo o sostituirlo con una soluzione causale migliore.

## Problemi da risolvere concretamente
1. **Licenza/provenance italiano**: il modello italiano P0 è bloccato per derivazione non-commerciale. Va sostituito con training/provenance commercialmente compatibile.
2. **Residual errors**: correggere alla causa S08-it, S16-en, S18-it, S18-es e il falso hint `Mañana -> LOCATION` in S16-es senza hardcode dei caseId/test string.
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

## Budget hardware stimato per decisioni autonome
Questi numeri sono budget di progetto, non misure fisiche già verificate:
- modelli POS correnti: ~4 MB non compressi;
- target PSS incrementale Understanding: **+20–50 MB** rispetto alla baseline app;
- warning: **>80 MB PSS incrementali** richiede root-cause/ottimizzazione;
- NO-GO preliminare: **>100 MB PSS incrementali** salvo beneficio qualitativo eccezionale documentato;
- CPU: parsing deve essere burst breve, non carico continuo; target pratico p95 per singolo utterance tale da non occupare stabilmente un core tra messaggi;
- il GGUF resta di gran lunga il costo dominante: non sacrificare robustezza linguistica per pochi MB se il componente resta entro il budget sopra.

Work deve usare questi budget per proseguire autonomamente senza chiedere misure Moto anticipate. Il Moto viene richiesto solo dopo il GO software/provenance.

## Gate P0.5

### Gate 00 — Truth
Verifica HEAD, working tree, P0 verdict, risultati machine-readable e commit di riferimento. Nessuna modifica production.

### Gate 01 — Clean Italian data plan
Costruire una matrice di corpus italiani candidati con licenza/provenance verificata. Escludere dal training production qualsiasi corpus/modello con clausola NC o provenance ambigua. Distinguere chiaramente `training_allowed`, `reference_only`, `rejected_for_training`.

Priorità: corpus UD italiani con licenza commercialmente compatibile e provenienza verificabile. Preferire BY/Apache/MIT/public-domain quando la qualità è sufficiente; BY-SA può essere usato solo dopo aver documentato obblighi e compatibilità dell'artefatto derivato. Non usare VIT, PoSTWITA o ParTUT nel modello production se la clausola NC resta applicabile.

Non fermarsi se il primo corpus clean non raggiunge qualità sufficiente: provare combinazioni clean, bilanciamento, normalizzazione e training settings riproducibili finché il gate qualità è raggiunto o le alternative clean realistiche sono esaurite.

### Gate 02 — Automated trainer
Implementare pipeline riproducibile:
`source datasets -> normalization/conversion -> frozen train/dev/test -> OpenNLP training -> model artifact -> checksum -> metadata/provenance -> benchmark`.

Deve essere lanciabile da Work/CI senza intervento manuale dell'utente. Versioni, seed e input devono essere bloccati. Work può iterare autonomamente su parametri di training purché ogni esperimento sia registrato e il test congelato non venga usato per tuning.

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

Congelare un test set nuovo prima dei fix. Ampliare abbastanza da evitare che il verdetto dipenda da poche decine di frasi; preferire centinaia di utterance generate/curate con famiglie e paraphrase indipendenti, mantenendo tracciabilità delle origini e separazione train/dev/test.

### Gate 04 — Causal residual fixes
Correggere i failure P0 alla causa, mai per caseId/stringa test-specifica.

Classi causali obbligatorie:
- **argument normalization**: S08-it; normalizzazione coerente del location object senza rompere source span/entity mention;
- **modal semantics**: S16-en; `would like to + VERB` e equivalenti devono essere goal/desiderio quando introducono un'azione, non semplice preference;
- **imperative detection**: S18-it/es; il dialogue act REQUEST non può dipendere unicamente dal POS, perché il tagger può classificare male forme imperative; usare segnali strutturali/lessico-morfologici generalizzabili e test equivalenti;
- **temporal/entity exclusivity**: S16-es; un token/span già accettato come temporal expression non può diventare LOCATION senza evidenza indipendente.

Per ogni classe: aggiungere regressioni nuove non identiche, eseguire l'intera suite, fare error analysis, correggere e ripetere finché il gate è raggiunto. Non fermarsi con "quasi risolto" se restano violazioni critiche o regressioni deterministiche.

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

GO quality:
- frozen test field exact **>= 0.97**;
- claim-count exact **>= 0.99**;
- ownership violations **0**;
- invented World Truth **0**;
- nessuna regressione critica su negazione/entity/temporalità/request;
- worst-language non deve collassare rispetto alla media.

Se il clean model non raggiunge il gate, Work deve continuare autonomamente con root-cause, corpus clean alternativi/combinati e training/fix causali. Fermarsi solo quando le opzioni sensate sono realmente esaurite o il gate è raggiunto.

### Gate 06 — CI autonomy
CI deve produrre automaticamente:
- unit/regression tests;
- full benchmark JSON;
- human report;
- trained model artifact + SHA-256 + provenance;
- Android probe APK;
- size breakdown;
- no-INTERNET permission check;
- failure summary;
- storico sintetico degli esperimenti utili/scartati.

### Gate 07 — Pre-Moto elimination
Prima del telefono eseguire tutto ciò che è possibile su CI/emulatore/JVM. Non chiedere all'utente test esplorativi per bug funzionali già riproducibili offline. Nessun Moto finché Gate 01–06 non sono verdi o il supervisore non lo richiede esplicitamente.

### Gate 08 — Moto final probe package
Preparare un solo pacchetto di test Moto con istruzioni minime e output automatico. Deve misurare PSS, CPU, cold/warm latency, APK/model bytes e thermal loop. L'utente deve idealmente solo installare/eseguire/esportare il JSON.

### Gate 09 — Verdict
Produrre uno dei tre verdetti:
- `GO_PRODUCTION_CANDIDATE`: clean provenance + quality gate + CI complete; manca solo Moto hardware gate;
- `GO_LAB_ONLY`: qualità buona ma licenza/provenance ancora bloccata dopo aver esaurito opzioni clean ragionevoli;
- `NO_GO`: qualità/generalizzazione/costo non sufficienti dopo iterazione documentata.

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
- numero/riassunto iterazioni svolte;
- CI run/artifact;
- APK probe;
- cosa resta non verificato;
- verdetto Gate 09.
