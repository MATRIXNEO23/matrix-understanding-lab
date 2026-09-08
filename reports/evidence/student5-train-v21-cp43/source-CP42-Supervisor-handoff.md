```text
CURRENT_HEAD = 270a0729c20ede548fe373f488029241fcbb35a3
TRAIN_V2_ID = student5-matrix-nlu-v3-train-v2
TRAIN_V2_SHA256 = b6acf41e6634c2f89e6b8251fb5f816ec60fb0ca1cd6c90dfcbed46c2c12584c
AUDIT_VERDICT = FAIL
```

Supervisor handoff — CP42_BUILD_1_AUDIT_LOCKED

Il candidato è esattamente quello persistito al commit canonico di main: 3.267 osservazioni, 4.101 claim, 123 aggiunte; IT 1.160, EN 1.046, ES 1.047, code-switch 14. Il registro originale contiene 16 rilievi: 9 HIGH, 7 MEDIUM. Nessuna correzione applicata. La riuscita del workflow non rende il candidato pronto per il training.

Lo SHA richiesto identifica i byte **compressi** di `train.jsonl.gz` (297.117 byte). Lo SHA logico dei 12.097.663 byte JSONL decompressi è `34ee224723d77a452a7ea6e776c95a6f11b3355b4ebf53672f99cf35d0bd64a9`; entrambi sono stati ricalcolati e coincidono con manifest e audit.

Due precisazioni della verifica attuale, da leggere prima di decidere le correzioni:

- **L01:** il difetto di negazione è confermato, ma anche la raccomandazione originale contiene un offset errato. Nel testo persistito il secondo `not` è **[25,28)**; [24,27) seleziona `" no"`, mentre lo span attuale [28,31) seleziona `" li"`. La raccomandazione di questo handoff è [25,28), senza applicarla.
- **D01 del registro:** 39 indica righe selezionate da uno screening, non errori confermati. Include `cp42-en-desire_future-0022`, «Tomorrow I will want to rest.», con FUTURE coerente con il desiderio esplicitamente futuro previsto dalla decisione D01. Le altre 38 righe sono ereditate e richiedono esame individuale. Il registro originale non è stato riscritto.

Tipi assegnati per il handoff: `annotation` = confirmed annotation defect; `coverage` = curriculum coverage defect; `imbalance` = imbalance; `semantic` = semantic-policy issue, da applicare alle decisioni D01–D07 già approvate senza riaprirle; `observation` = non-blocking observation rispetto alla validità delle annotazioni, pur potendo limitare la readiness. Nessun problema di integrità del candidato è stato riscontrato. La raccomandazione errata L01 è un problema nell'evidenza di audit, non un mismatch del payload.

Tutti i rilievi hanno **AUTO_FIX_APPLIED = false**. I conteggi sono righe uniche per rilievo, salvo indicazione diversa; si sovrappongono e non vanno sommati. Zero righe per una lacuna significa famiglia assente o limitazione globale. `CP42-verified-findings.json` contiene gli ID completi di ogni rilievo e i conteggi/ID per famiglia; le famiglie sono indicizzate su tutti i claim delle righe coinvolte, quindi eventuali claim collaterali non sono automaticamente difettosi.

| ISSUE_ID | SEVERITY | TYPE | COUNT; AFFECTED_ROWS/FAMILIES | AFFECTED_HEADS | EVIDENCE_FILE | TRAINING_RISK; RECOMMENDED_CORRECTION |
|---|---|---|---|---|---|---|
| C01 | HIGH | annotation | 2: `mx-v22a-adult-it-015`, `mx-v22a-adult-it-027`; `v22a_adult_it_request` | Registro: tutti i label semantici. Differenza effettiva: targetReferent, fieldStatus, interpretationStatus, alternativesByField | E1, E2, payload | Testo/contesto identici «Puoi abbracciarti con me?» con UNKNOWN/AMBIGUOUS contro ctx:speaker/RESOLVED: supervisione contraddittoria. Adjudicare insieme entrambi secondo D04/D07, senza voto di maggioranza o deduplica automatica. |
| C02 | MEDIUM | imbalance | 2.189 righe in 627 gruppi di superficie identica; più famiglie/contesti | tutti | E1, E2 | Ripetizioni possono dominare famiglie rare. Verificare equivalenza semantica e alias; preservare i veri contrasti contestuali. Non sono 2.189 duplicati sicuramente eliminabili. |
| C03 | MEDIUM | imbalance | 36 EN: adult_consent 28; consent_grant_v2_train_generalization 4; consent_refuse_v2_train_generalization 4 | tutti | E1, E2 | Concentrazione nel massimo scheletro ` <SLOT> `. Proxy approssimativo per sovrapposizione di sostituzioni: esaminare varietà per famiglia, mantenendo esempi semplici validi. |
| C04 | MEDIUM | imbalance | 189 ID rappresentativi, 432 coppie fra superfici uniche nella stessa lingua | tutti | E1, E2 | Possibili scorciatoie da template. Jaccard di trigrammi ≥0,85 è solo screening; rivedere le coppie senza cancellazioni/label derivati dal punteggio. |
| G01 | HIGH | coverage | 3 classi assenti; 0 claim per UNKNOWN in ciascuna | dialogueAct, temporalRelation, claimKind | E1, E3 | Nessun target positivo per queste classi. Aggiungere solo casi di vera incertezza giustificata, senza quote artificiali e senza penalizzare lessico esplicito. |
| G02 | HIGH | coverage | Tutte le 123 nuove osservazioni; generalmente 1 o pochi costrutti per famiglia/lingua | dialogueAct, temporalRelation, sourceReferent, perspectiveReferent | E1, E3, payload | Supporto nonzero insufficiente per generalizzare. Rivedere ampiezza e contrasti naturali IT/EN/ES, registri realistici, slang e intimità. Nessuna soglia numerica inventata. |
| G03 | HIGH | coverage | 3: cp42-it-ambiguous_binding-0117, cp42-en-ambiguous_binding-0119, cp42-es-ambiguous_binding-0121 | subjectReferent, ownerReferent, fieldStatus; alternativesByField | E1, E5 | Il target builder usa label/puntatori ma non supervisiona esplicitamente status e alternative ordinate: UNKNOWN è apprendibile, la distinzione AMBIGUOUS/status no come target dedicato. Bloccatore separato Gate-B; assegnazione successiva specifica se approvata, nessuna modifica ora a target/evaluator/decoder. |
| G04 | MEDIUM | observation | 2.586 righe PRESERVED; slice A–H tutte TRAIN | tutti | E1, E4 | Le slice non misurano indipendentemente regressione/generalizzazione. Occorre valutazione separatamente autorizzata; nessuna percentuale di qualità deducibile e nessun uso DEV/Frozen ora. |
| L01 | HIGH | annotation | 1: cp42-en-double_negation-0103; double_negation | negation / negationCueSpans | E1, payload | [28,31) seleziona `" li"` e insegna evidenza di negazione sbagliata. Proposta verificata: **[25,28)**. La proposta originale [24,27) è errata. |
| L02 | HIGH | semantic | 3 adult_hesitation: cp42-it-…-0087, cp42-en-…-0088, cp42-es-…-0089 | boundary, negation, polarity, claimKind | E1, payload | Desiderio, disgiunzione e incertezza epistemica in un claim piatto; secondo no di «no sé» ES non separatamente preservato. Rivedere scope, cue e confini proposizionali per lingua secondo V3. Nessuna equiparazione automatica esitazione=rifiuto. |
| L03 | HIGH | semantic | 15, tre per famiglia: command, request, adult_request, grammatical_reflexive, owner_subject_permission | subjectReferent, ownerReferent, targetReferent, predicate | E1, payload | Convenzione owner della richiesta/consenso distinta da soggetto dell'azione può essere incoerente con gli esempi ereditati. Adjudicare le 15 costruzioni secondo D07 e contratto, senza imporre né uguaglianza né disuguaglianza. |
| L04 | HIGH | semantic | 3: mx-v22a-adult-it-015, -025, -026; v22a_adult_it_request | targetReferent, ownerReferent | E1, payload, construction-review | Due forme reciproche/riflessive AMBIGUOUS, toccarti risolto sul sé dell'interlocutore; owner ereditato. Rischio di ambiguità sovrautilizzata e convenzioni miste. Esame individuale delle tre frasi, coordinato con C01; non indovinare partecipanti. |
| D01 | HIGH | semantic | 39 selezionate: future_goal 34; explicit_future_goal_v2_train_generalization 4; desire_future 1 | temporalRelation | E1, payload, audit.py | Possibile confusione fra tempo del desiderio e dell'azione. **Non 39 difetti confermati:** il controllo «Tomorrow I will want to rest.» è coerente con FUTURE. Esaminare le altre 38 individualmente secondo D01 approvata; niente cambio massivo da keyword. Le 23 A02 CURRENT sono un gruppo distinto. |
| G05 | MEDIUM | imbalance | 14 code-switch: v22a_adult_it_english_term 11, adult_code_switch 3 | tutti | E1, E3 | Code-switch concentrato sul desiderio. Ampliare famiglie miste naturali, senza trasformare parole straniere/slang/adulte in UNKNOWN; prestiti monolingui sono conteggi separati. |
| G06 | MEDIUM | coverage | Lacuna globale: subject 1.449 gruppi, 0 multiword e 0 multipli; object 3.905 gruppi, 0 multipli; temporal 425 gruppi, 0 multipli | subject, entity, object, temporal | E1, E3 | Copertura dell'head non implica varietà degli span. Aggiungere solo persone multiword e gruppi multipli linguisticamente giustificati. Entity ha già 930 gruppi multiword e 342 claim con gruppi multipli: non è una classe completamente assente. |
| G07 | MEDIUM | observation | Limite globale; sovrapposizione statistica DEV/Frozen NOT_CHECKED | tutti / provenienza | E1, input identities | Origine autorizzata TRAIN/progetto dimostrata; non dimostrata disgiunzione esatta da payload protetti non letti. Non è leakage confermato. Mantenere il protocollo: eventuale verifica solo da soggetto autorizzato, senza esporre esempi. |

Ulteriori osservazioni già nel rapporto/censimento CP42, non nuovi ISSUE_ID del registro:

- **Squilibrio dei ruoli:** su 4.101 claim, owner=subject 4.086 e divergenza 15; source=perspective 4.095 e divergenza 6; perspective=speaker 4.087, diversa 14. Rischio di scorciatoie di ruolo collegato a G02/L03. Non prescrive bilanciamento artificiale.
- **Ancoraggio temporale:** None 1.371; speech-time 2.718; temporal:t0 9; context-reference 3; nessun esempio di anchor cross-claim. Lacuna di copertura di temporalRelation.anchorRef, da valutare con contrasti naturali; nessuna modifica ora.
- **Classi rare:** COMMAND 3, BELIEF 9, REPORT 14, PAST 17; BEFORE/AFTER/DURING/RECURRENT/AT_REFERENCE 3 ciascuna. ASSERT 3.851 e DIRECT 3.811 predominano. Conteggi di claim, non risultati del modello.
- **Limite della validazione:** 7.368 esempi diagnostici con offset lessicali, non tokenizzazione del modello pristine. Il validatore ha usato confidence=1 sintetica sugli ori per adattamento strutturale. Zero eccezioni non prova correttezza semantica, calibrazione o readiness con tokenizer reale.
- Sei osservazioni zero-claim sono presenti; RESOLVED e NOT_APPLICABLE sono gli status V3 pertinenti, senza introdurre KNOWN. Lessico adulto/intimo è trattato come normale semantica NLU. Consenso, rifiuto, revoca e desiderio restano distinti; copertura minima non dimostra adeguatezza linguistica ampia.

D01–D07 restano approvate. Evidenza della loro applicazione nel candidato: 23 A02 CURRENT preservate; D02 8 viewpoint corretti e 6 nuovi contrasti source/viewpoint; D03 6 wrapper corretti più 3 BELIEF e 3 DIRECT nuovi; D04 6 quarantene e 3 disposizioni riflessive con L04 pendente; D05 correzione metalinguistica positiva preservata e 3 nuovi contrasti; D06 6 zero-claim e 3 contesti ambigui/3 risolti sulla stessa superficie, con limite G03; D07 contrasti di binding/ruoli presenti, L03 pendente. Le 558 righe CORRECTED appartengono alla costruzione CP42 già eseguita, non sono correzioni di questa sessione.

STRUCTURAL_VALIDATION = PASS_PERSISTED_CP42 (0 invariant errors, 0 mention-bounds errors, 0 target-builder errors; evidenza autenticata, non rieseguita)
DETERMINISTIC_REBUILD_MATCH = PASS_PERSISTED_CP42 (6/6 output identici; candidato attuale coincide con before/after audit; nessun rebuild eseguito qui)
BUILD_LOCK_MATCH = true (5/5 hash del lock più hash del BUILD_LOCK stesso uguale ad audit before/after)
MANIFEST_MATCH = true (identità, versione, checkpoint, hash compressi/logici, byte, righe, claim e disposizioni verificati)
PROVENANCE_MATCH = true (3.267/3.267 hash nuove righe; lineage e hash old ricontrollati in memoria per 3.150 origini; 6 quarantene; mapping univoco)
TRAIN_V1_UNCHANGED = true (130/130 blob Git identici al checkpoint 1396dd6c997ce0dbf5e4a5ce933437c82fc1c217; nessuna aggiunta/rimozione/modifica)

La verifica di TRAIN v1 confronta direttamente i tree Git completi dei due commit. Il checksum ordinato canonico `1118a900026f48cfcc290c3f9dc52a1a019a6a1f4761661f326c33770523140e` coincide nei manifest autenticati; 129 checksum nel suo SHA256SUMS e l'hash del file SHA256SUMS coincidono con i 130 baseFiles di v2. Non è stato ricalcolato il checksum concatenando gli shard v1 in questa sessione. La verifica di lineage è un controllo interno del registro/before-after, con autenticazione del payload originale garantita dalla continuità dei blob Git; non è una nuova revisione semantica di tutte le annotazioni.

Verifica attuale delle evidenze: 28 file scaricati al commit canonico e autenticati contro il relativo Git blob; 21/21 voci del SHA256SUMS CP42 coincidono. Tutti i 16 affectedRows sono risolvibili nel candidato. Nessun builder, training, audit generativo o workflow avviato.

Run GitHub verificato: 34170700425, nome P0 Understanding Lab, workflow .github/workflows/p0.yml, main/270a0729c20ede548fe373f488029241fcbb35a3, completed/success. Artifact verificato nei metadati: p05-training, ID 10035624558, digest sha256:b864389c59f57a78a414ce0aa74cb6b0a3c885d6200cf60c551868aaacc84a75, non scaduto. Il ZIP dell'artifact non è stato scaricato né ricalcolato: il candidato è stato verificato direttamente nei file permanenti della repository. Il nome dell'artifact non dimostra che sia stato addestrato Student-5 TRAIN v2.

Chiavi evidenze della tabella (tutte al commit canonico):

- E1 = reports/evidence/student5-train-v2-audit-cp42/audit.json
- E2 = reports/evidence/student5-train-v2-audit-cp42/redundancy.json
- E3 = reports/evidence/student5-train-v2-audit-cp42/census.json
- E4 = reports/evidence/student5-train-v2-audit-cp42/slices.json
- E5 = matrix_nlu/training_data_v3.py
- payload = data/student5_v3_train_v2/train.jsonl.gz
- construction-review = data/student5_v3_train_v2/construction-review.json
- input identities = reports/evidence/student5-train-v2-audit-cp42/input-and-source-identities.json
- audit.py = tools/student5_cp42/audit.py

Inventario completo dei file di audit/evidenza/supporto usati o autenticati per questa consegna (path esatti; hash e dimensioni nel JSON allegato):

- [PROJECT_WORK_RULES.md](https://github.com/MATRIXNEO23/matrix-understanding-lab/blob/270a0729c20ede548fe373f488029241fcbb35a3/PROJECT_WORK_RULES.md)
- [data/student5_v3/SHA256SUMS](https://github.com/MATRIXNEO23/matrix-understanding-lab/blob/270a0729c20ede548fe373f488029241fcbb35a3/data/student5_v3/SHA256SUMS)
- [data/student5_v3/migration-manifest.json](https://github.com/MATRIXNEO23/matrix-understanding-lab/blob/270a0729c20ede548fe373f488029241fcbb35a3/data/student5_v3/migration-manifest.json)
- [data/student5_v3_train_v2/BUILD_LOCK.json](https://github.com/MATRIXNEO23/matrix-understanding-lab/blob/270a0729c20ede548fe373f488029241fcbb35a3/data/student5_v3_train_v2/BUILD_LOCK.json)
- [data/student5_v3_train_v2/construction-review.json](https://github.com/MATRIXNEO23/matrix-understanding-lab/blob/270a0729c20ede548fe373f488029241fcbb35a3/data/student5_v3_train_v2/construction-review.json)
- [data/student5_v3_train_v2/manifest.json](https://github.com/MATRIXNEO23/matrix-understanding-lab/blob/270a0729c20ede548fe373f488029241fcbb35a3/data/student5_v3_train_v2/manifest.json)
- [data/student5_v3_train_v2/provenance-and-mapping.jsonl.gz](https://github.com/MATRIXNEO23/matrix-understanding-lab/blob/270a0729c20ede548fe373f488029241fcbb35a3/data/student5_v3_train_v2/provenance-and-mapping.jsonl.gz)
- [data/student5_v3_train_v2/quarantine.jsonl.gz](https://github.com/MATRIXNEO23/matrix-understanding-lab/blob/270a0729c20ede548fe373f488029241fcbb35a3/data/student5_v3_train_v2/quarantine.jsonl.gz)
- [data/student5_v3_train_v2/train.jsonl.gz](https://github.com/MATRIXNEO23/matrix-understanding-lab/blob/270a0729c20ede548fe373f488029241fcbb35a3/data/student5_v3_train_v2/train.jsonl.gz)
- [docs/MATRIX_NLU_CONTRACT_V3.md](https://github.com/MATRIXNEO23/matrix-understanding-lab/blob/270a0729c20ede548fe373f488029241fcbb35a3/docs/MATRIX_NLU_CONTRACT_V3.md)
- [docs/WORK_CONTINUITY_STUDENT_5.md](https://github.com/MATRIXNEO23/matrix-understanding-lab/blob/270a0729c20ede548fe373f488029241fcbb35a3/docs/WORK_CONTINUITY_STUDENT_5.md)
- [matrix_nlu/training_data_v3.py](https://github.com/MATRIXNEO23/matrix-understanding-lab/blob/270a0729c20ede548fe373f488029241fcbb35a3/matrix_nlu/training_data_v3.py)
- [prompts/WORK_STUDENT_5_PATH_B_V3_CREATE_REPAIRED_TRAIN_V2_ONLY.md](https://github.com/MATRIXNEO23/matrix-understanding-lab/blob/270a0729c20ede548fe373f488029241fcbb35a3/prompts/WORK_STUDENT_5_PATH_B_V3_CREATE_REPAIRED_TRAIN_V2_ONLY.md)
- [reports/STUDENT_5_TRAIN_V2_BUILD_AUDIT_CP42.md](https://github.com/MATRIXNEO23/matrix-understanding-lab/blob/270a0729c20ede548fe373f488029241fcbb35a3/reports/STUDENT_5_TRAIN_V2_BUILD_AUDIT_CP42.md)
- [reports/evidence/student5-train-v2-audit-cp42/SHA256SUMS](https://github.com/MATRIXNEO23/matrix-understanding-lab/blob/270a0729c20ede548fe373f488029241fcbb35a3/reports/evidence/student5-train-v2-audit-cp42/SHA256SUMS)
- [reports/evidence/student5-train-v2-audit-cp42/audit.json](https://github.com/MATRIXNEO23/matrix-understanding-lab/blob/270a0729c20ede548fe373f488029241fcbb35a3/reports/evidence/student5-train-v2-audit-cp42/audit.json)
- [reports/evidence/student5-train-v2-audit-cp42/census.json](https://github.com/MATRIXNEO23/matrix-understanding-lab/blob/270a0729c20ede548fe373f488029241fcbb35a3/reports/evidence/student5-train-v2-audit-cp42/census.json)
- [reports/evidence/student5-train-v2-audit-cp42/delivery-entries.json](https://github.com/MATRIXNEO23/matrix-understanding-lab/blob/270a0729c20ede548fe373f488029241fcbb35a3/reports/evidence/student5-train-v2-audit-cp42/delivery-entries.json)
- [reports/evidence/student5-train-v2-audit-cp42/input-and-source-identities.json](https://github.com/MATRIXNEO23/matrix-understanding-lab/blob/270a0729c20ede548fe373f488029241fcbb35a3/reports/evidence/student5-train-v2-audit-cp42/input-and-source-identities.json)
- [reports/evidence/student5-train-v2-audit-cp42/redundancy.json](https://github.com/MATRIXNEO23/matrix-understanding-lab/blob/270a0729c20ede548fe373f488029241fcbb35a3/reports/evidence/student5-train-v2-audit-cp42/redundancy.json)
- [reports/evidence/student5-train-v2-audit-cp42/remote-readback.json](https://github.com/MATRIXNEO23/matrix-understanding-lab/blob/270a0729c20ede548fe373f488029241fcbb35a3/reports/evidence/student5-train-v2-audit-cp42/remote-readback.json)
- [reports/evidence/student5-train-v2-audit-cp42/slices.json](https://github.com/MATRIXNEO23/matrix-understanding-lab/blob/270a0729c20ede548fe373f488029241fcbb35a3/reports/evidence/student5-train-v2-audit-cp42/slices.json)
- [reports/evidence/student5-train-v2-audit-cp42/structural.json](https://github.com/MATRIXNEO23/matrix-understanding-lab/blob/270a0729c20ede548fe373f488029241fcbb35a3/reports/evidence/student5-train-v2-audit-cp42/structural.json)
- [tools/student5_cp42/DESIGN.md](https://github.com/MATRIXNEO23/matrix-understanding-lab/blob/270a0729c20ede548fe373f488029241fcbb35a3/tools/student5_cp42/DESIGN.md)
- [tools/student5_cp42/audit.py](https://github.com/MATRIXNEO23/matrix-understanding-lab/blob/270a0729c20ede548fe373f488029241fcbb35a3/tools/student5_cp42/audit.py)
- [tools/student5_cp42/authored.py](https://github.com/MATRIXNEO23/matrix-understanding-lab/blob/270a0729c20ede548fe373f488029241fcbb35a3/tools/student5_cp42/authored.py)
- [tools/student5_cp42/build.py](https://github.com/MATRIXNEO23/matrix-understanding-lab/blob/270a0729c20ede548fe373f488029241fcbb35a3/tools/student5_cp42/build.py)
- [tools/student5_cp42/delivery_readback.py](https://github.com/MATRIXNEO23/matrix-understanding-lab/blob/270a0729c20ede548fe373f488029241fcbb35a3/tools/student5_cp42/delivery_readback.py)

Ulteriori evidenze API read-only: branches/main; git/trees/270a0729c20ede548fe373f488029241fcbb35a3?recursive=1; git/trees/1396dd6c997ce0dbf5e4a5ce933437c82fc1c217?recursive=1; actions/runs/34170700425; actions/runs/34170700425/artifacts, nella repository indicata. Il JSON allegato conserva il confronto dei 130 blob.

Le dichiarazioni finali seguenti riguardano le azioni di questo incarico e concordano con i guard CP42 persistiti; non intendono negare training storici precedenti del progetto.

```text
trainingExecuted=false
fineTuningExecuted=false
quantizationExecuted=false
onnxExecuted=false
student5PristineModified=false
trainV1Modified=false
postAuditCorrectionsExecuted=false
nextWorkStarted=false
```

STOP. Nessuna correzione, v2.1, ricostruzione o attività successiva avviata. Il Supervisor decide l'eventuale insieme di correzioni.
