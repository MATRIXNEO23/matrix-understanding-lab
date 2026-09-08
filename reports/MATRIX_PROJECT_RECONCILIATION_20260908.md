# MATRIX — riconciliazione del progetto, 8 settembre 2026

**Esito: inventario e riconciliazione completati; validazione funzionale complessiva ancora da eseguire.** Nessun componente viene promosso perché un documento lo chiama “completo”. Non è stata trovata una prova della catena Engine completa con NLU/GGUF reali e memoria persistente. Questo non dimostra che tutto il lavoro sia errato.

## Stato Git verificato

| Repository | HEAD sorgente verificato | Ruolo osservato |
|---|---|---|
| MATRIXNEO23/assembling | `8e94db9e692e387f8ef2b5d528f8dd3f1c1d8fcf` | Contratti e integrazione Kotlin/JVM; 80 file Git, 27 sorgenti Kotlin e 18 file test |
| MATRIXNEO23/matrix-understanding-lab | `815b1ca53e12ed392499e5ddce0d6d97431e7b99` | Laboratorio NLU, Student-4/5, dataset e candidato E5 isolato |

Entrambi gli HEAD corrispondono al passaggio di consegne. Tutti gli 80 blob testuali Assembling sono stati recuperati e verificati rispetto al loro Git SHA; 17 file mirati del laboratorio sono stati recuperati allo stesso modo. La lettura semantica è stata mirata a collegamenti, stati e prove, non una revisione di ogni algoritmo. Nessun working tree dell’utente è stato osservato.

La repository di scrittura di questo verbale è soltanto `matrix-understanding-lab`; Assembling è stato letto come dipendenza, senza modifiche. Nessun reset o rollback del lavoro precedente.

## Che cosa dimostrano i test esistenti

Il run Assembling **34191239860**, job **101949567727**, è al HEAD corrente. Ho recuperato il log: `gradle test`, task `:test`, `BUILD SUCCESSFUL in 43s`. Il codice contiene 150 annotazioni `@Test` in 18 file: è un censimento statico, non un conteggio di test eseguiti ricavato da XML. I report JUnit individuali non sono stati recuperati.

I sei test di `MatrixAssemblingOrchestratorIntegrationTest.kt` forniscono claim già costruiti mediante `integration-static-nlu`, usano `EchoGgufAdapter` e mantengono la memoria disabilitata. Sono prove utili di alcune invarianti e di quel percorso di integrazione. **Non misurano comprensione linguistica del modello, qualità del GGUF o persistenza reale.** Le suite V3/Authority usano anch’esse output strutturati di prova; non sono test linguistici del modello.

Non ho avviato nuove suite o workflow in questa fase di riconciliazione. Il runtime locale dispone di Java, ma non di `gradle`/`kotlinc` sul PATH. La prova di esecuzione qui recuperata è il log CI esistente, non una ripetizione locale.

## Registro sintetico dei componenti

| Componente | Classificazione | Prova e limite |
|---|---|---|
| MIP + MatrixTurnFrame | VERIFIED, limitato al contratto | MIP è autorità semantica; TurnFrame è contenitore del turno. Ruoli distinti e compatibili, non sostituti |
| Adapter Understanding V3 | VERIFIED, mapping con fixture | Implementazione e test presenti; bridge NLU reale non dimostrato |
| V3 → Authority | VERIFIED, confine con fixture | Proiezione/ambiguità testate; recupero multi-claim resta intenzionalmente unresolved quando non associabile |
| Coherence | VERIFIED, invarianti coperte | Esistono controlli; il percorso Basic consuma typedClaims legacy |
| Orchestrator / prompt / diagnostica | IMPLEMENTED_NOT_FUNCTIONALLY_VERIFIED per la catena reale | Test con NLU statico e GGUF echo; confine V3→prompt completo non dimostrato |
| Affective | IMPLEMENTED_NOT_FUNCTIONALLY_VERIFIED | Adapter Kotlin e prototipo Python presenti; la CI JVM non esegue il prototipo come runtime cross-language |
| Memory preflight | VERIFIED, assenza scritture anticipate | Non equivale a memoria persistente |
| Memory/retrieval/consolidation persistenti | NOT_IMPLEMENTED / NOT_WIRED nella repo corrente | Documentazione e codice concordano; build JVM, non Android/Room |
| Relationship / Intimacy / Goals / Decision | NOT_WIRED nella repo corrente | Domini riservati, non provati da riepiloghi affettivi o prompt |
| GGUF reale / validatore semantico | NOT_WIRED nella repo corrente | Interfacce e fake echo; validatore opzionale di test |
| Percorsi compatibility legacy | Obsoleti per nuovi caller canonici | Da preservare; non convertirli implicitamente in V3 |
| Entity Resolution separato | UNKNOWN | Riferimenti/candidati esistono; nessun modulo autonomo identificato nelle superfici esaminate |
| Student-4 v2.2A | FAILED sul gate DEV storico; R2 separato | Non production approved; autorizzazione storica a runtime controllato non equivale a gate superato |
| Student-5 FP32 CP47 | Training documentato e artefatti registrati; qualità NON VERIFICATA | Dieci checkpoint; selezione BLOCKED, zero valutati, nessun vincitore |
| TRAIN/G03 | VERIFIED nei test/rapporti preesistenti | Preparazione target non equivale a predizione corretta del modello; dataset non ri-auditato |
| E5 | Import verificato; funzione MATRIX NON VERIFICATA | Hash e upload LFS nei log; nessuna inferenza MATRIX dimostrata |
| Colab 2/8 | UNKNOWN quanto a riproducibilità | Solo resoconto ricevuto; mancano notebook, regola di scoring e output grezzi |
| ARCHITETTURA.md del laboratorio | DESIGN_ONLY | Piano Python dichiarato “progettazione”, non descrizione del codice Kotlin corrente |

Il registro macchina include percorsi precisi, test associati, limiti e verifica successiva per ciascuna voce. `VERIFIED` si applica soltanto alla proprietà indicata: non significa che il modulo funzioni in ogni condizione o nel prodotto completo. Un componente non cablato non è classificato come implementazione guasta.

## Collegamenti da chiarire prima di riprendere sviluppo

1. **Percorso V3 fino al prompt.** `CanonicalUnderstandingV3Adapter` popola `canonicalUnderstandingV3` e conserva il divieto di auto-popolare i vecchi campi. Il prompt root richiede invece `requireSemantic()` e `requireAuthority()` legacy. Le prove di orchestrazione esaminate usano `UnderstandingLabAdapter` legacy. Il percorso completo canonico non è dimostrato: è un gap di collegamento/verifica da riprodurre, non un bug runtime già riprodotto qui. Non inventare campi legacy per farlo apparire collegato.
2. **Persistenza e backend reali.** L’orchestratore attuale termina dopo generazione/validazione opzionale. Non collega il futuro `PersistentConsolidationPort`. Mancano prove di scrittura atomica, riavvio, recupero e supersede. Non iniziare un nuovo modulo prima di individuare il target autorizzato e le implementazioni esistenti.
3. **Ambito dei piani architetturali.** Assembling contiene Kotlin/JVM e indica come passo futuro Memory Kotlin/Room in un target Android appropriato. `ARCHITETTURA.md` nel laboratorio descrive un piano Python con `matrix_ai/*` ancora in progettazione. Nessuna prova recuperata autorizza a trattare uno come sostituzione dell’altro. Non scegliere automaticamente un pivot.
4. **Stati storici.** Rapporti CP-U1 e rapporti Student-4 precedenti possono descrivere stati poi superati da CP-U2/U3 o R2. Vanno interpretati con commit, scope e successori; non sommati come istruzioni simultanee.

## Correzioni fattuali al passaggio di consegne

- L’esito Student-5 **è disponibile** nell’indice e nelle evidenze CP48: selezione bloccata, zero checkpoint valutati, nessun epoch scelto. Release **384423046** / asset **549780835**, 93.830.912 byte, SHA `029bc292c11091da3aa5742ac85017ffdbc7dbb7ba7be6fadc5cc603f07ceafa`. Metadati riletti ora; il download e i caricamenti FP32 furono verificati nel precedente lavoro di questa conversazione, non ripetuti qui.
- I 134 byte Student-4 sono **un puntatore Git LFS valido**: OID `4998ce2f44dd8553d75f86b8d7975529f6a5f779de9107eef393648022d6ccb5`, payload atteso **356.134.801 byte**, coincidenti col manifest. Non è un modello vuoto. Non ho verificato in questa fase il nuovo download LFS del payload.
- E5 nel laboratorio è un import effettivo: log run **34191899115**, job **101951491202**, hash modello `e8de21ecee219f55eb9a29e3f0ba7a6167756b6109512d201895b3158e97ae3e`, **351.646.568 byte**, upload LFS **2/2**. Anche il tokenizer è LFS: **17.082.735 byte**, SHA `6040ba36e3e2f7b2fa6ae076b69d024a08666bea4c345105a32e542900fcc7e7`. Upload riuscito non equivale a download verificato oggi o caricamento corretto col tokenizer pruned.
- In Assembling restano workflow fetch E5 e directory README/script candidato. Run **34191239854**, artifact **10042298574**, **216.231.681 byte**, SHA `d1d93b2f002183c7bfef0726366dafdc10fd4d3f8561eab947b12d13a2d6bd4a` confermati da metadati e log. Non è integrazione nel runtime; nessun file è stato cancellato.
- La continuità Student-4 documenta una successiva autorizzazione **R2 controlled runtime**. Il fallimento del gate production resta: non ripristinare un vecchio divieto assoluto di quantizzazione come se non fosse mai stato superato, né trattare R2 come production approval. Nessuna quantizzazione nuova eseguita.
- Il risultato Colab 2/8 resta un’affermazione del resoconto, senza notebook/raw log acquisiti. Non è un gate, non valuta i dieci checkpoint e non autorizza una sostituzione del modello.

## Prossimo checkpoint proposto, non avviato

**Una sola verifica: collegamento canonico Understanding V3 → Authority → prompt.** Riprendere l’HEAD Assembling congelato, rileggere le asserzioni esistenti, eseguire la suite deterministica con log/XML, poi provare quel confine con input strutturati leciti e senza auto-inventare dati legacy. Documentare la prima interruzione e distinguere contratto testato da inferenza reale. Non includere training, scelta modello, Memory Room o E5 nel medesimo task.

Le successive verifiche reali di NLU, backend affettivo, GGUF, Memory e Android restano necessarie e separate. Prima di eseguirle servono le implementazioni/artefatti/target appropriati. Questa proposta non cambia l’architettura né avvia un nuovo modulo.

## Prove persistite

Directory: `reports/evidence/matrix-project-reconciliation-20260908/`.

- `result.json`: scope, HEAD, operazioni, limiti e prossimo checkpoint proposto.
- `component-register.json`: ogni componente, percorsi, prove, limiti, test da usare.
- `findings.json`: otto punti di riconciliazione con priorità e azione raccomandata.
- `artifact-identities.json`: OID LFS, dimensioni, Release/artifact e distinzione presenza/readback/inferenza.
- `execution-evidence.json`: estratti dei tre log reali recuperati e loro hash.
- `source-register.json.gz`: 97 file recuperati, repository/ref/percorso/Git SHA/SHA-256/dimensione.
- `repository-trees.json.gz`: entrambi gli alberi Git fotografati.
- `remote-metadata.json.gz`: HEAD, run, job, Release, artifact e commit acquisiti. Le liste run sono limitate a 20 Assembling e 10 Lab, non un censimento totale.
- `SHA256SUMS`: checksum delle nuove prove e di questo verbale; verifica dalla root del laboratorio.

Indici/continuità precedenti conservati e aggiornati per aggiunta nel laboratorio. Nessun cambiamento a codice, modelli, dataset, Student-4, Assembling o contratti. Nessun training, quantizzazione, export, lettura Frozen o nuovo benchmark avviato. Il presente passaggio completa la ricognizione; **non chiude la verifica funzionale del progetto**.
