Supervisor GPT — Student-5 TRAIN v2 Repair Report

TRAIN_V2_REPAIR = BLOCKED

Data audit: 2026-09-07. Incarico: RECOVERY / COMPLETION AUDIT ONLY.
Repository: MATRIXNEO23/matrix-understanding-lab.
Branch remoto verificato: `student5-path-b-v3`.
Starting HEAD verificato: `ff6ee962bcc7629ace9bcd69263ddbf497376df8`.
Starting tree effettivo: `614e9154e2c4ba67fa7c3a22dc17514ff31e3e9e`.
Final HEAD di questa consegna: commit che introduce questo rapporto, figlio diretto dello starting HEAD; risolvere con `git log -1 --format=%H -- reports/STUDENT_5_TRAIN_V2_REPAIR_RECOVERY_CP39.md`. Il rapporto in chat indica lo SHA esatto dopo pubblicazione e lettura remota.

Il candidato precedente NON è certificabile: non è presente nel tree del branch e la copia locale, insieme agli script e alle prove non pubblicate, non è più disponibile dopo la manutenzione del workspace. Il recovery rileva una perdita di persistenza e impossibilità di verificare requisiti obbligatori. Si applica lo STOP del punto 7 dell'incarico; non si ricostruisce gold dalla memoria e non si avvia un nuovo dataset.

## Stato reale prima del recovery

- Il ref remoto era ancora lo starting HEAD. Il suo commit aggiunge soltanto l'incarico di creazione TRAIN v2 ed è figlio di CP38 `eef2682538dc91a5827bdd3eaff0be202f95a79e`.
- Il tree completo (437 entry, non troncato) non contiene `data/student5_v3_train_v2/`, report CP39, script `student5_train_v2_*` o checkpoint CP39. La continuity pubblicata termina a CP38.
- Nessun run Actions restituito per il branch (total_count=0). Tre Release restituite: pristine, Path A runtime probe, Gate A CP35; nessun candidato TRAIN v2 fra i relativi asset. Sono stati letti solo metadati, non archivi/modelli.
- Workspace corrente inizialmente vuoto. `git status --short --branch` termina con exit 128: `fatal: not a git repository (or any of the parent directories): .git`. Non esiste quindi un git status locale “clean” del precedente lavoro né un reflog locale recuperabile.
- Assenti `cp39-delivery/`, `cp39-candidate-01-retained/`, `student5-path-b/repo/`. Ricerca dei nomi pertinenti nelle altre tre directory scratch disponibili: nessun candidato corrispondente.
- Ricerche Library per nomi/logical ID/CP39 e query alternativa: nessuna copia pertinente recuperabile individuata. Questo è l'esito della ricerca, non una prova di assenza da qualunque backup possibile. Nessun payload non pertinente è stato aperto.

## Cosa risulta dalla cronologia, ma non è ricertificabile

La cronologia di sessione conservata descrive una precedente generazione locale e un audit indipendente, fermati prima della pubblicazione Git. Distingue esplicitamente CREATED_AND_LOCALLY_VERIFIED_NOT_YET_PUBLISHED da una consegna persistente. Non assumo che non sia avvenuta esecuzione; non posso trasformare quel resoconto in prova dei bytes ora mancanti.

Tracce utili esclusivamente per riconoscere una futura copia recuperata, NON risultati nuovamente verificati:
- candidato finale dichiarato: 1.723 righe / 2.416 claim; 18 shard; 85 file di consegna previsti;
- SHA logico dichiarato: `01d0a249ea05febb83142ead6b730a914de67495e37dec4fa2faf6b1ccc0d813`;
- disposizioni dichiarate: UNCHANGED 1007, CORRECTED 578, ADDED 138, DEACTIVATED 1565;
- primo candidato dichiarato: 1.724 righe / 2.417 claim, preservato prima di una correzione di equivalenza;
- ZIP del primo candidato dichiarato: 995.905 byte, SHA `547957a5cf98db05a2f13a051e779398ecc5b46e3b570d89cf1d90f8e93f0128`;
- vecchio percorso: `/workspace/scratch/0a50431faa34/cp39-delivery/`;
- audit precedente dichiarava un blocker owner/subject: nessuna divergenza accettata, pur con esempi source/perspective distinti.

Questi numeri e SHA non costituiscono manifest, checksum ricalcolati, prova semantica o prova di proprietà del candidato. Non si dichiara che i file siano recuperabili da tali stringhe. L'eventuale blocker semantico storico non viene certificato senza i dati: il blocker verificato oggi è la perdita delle prove.

## Cosa è stato completato ora

Solo audit di recupero, confronto identità Git, lettura del prompt canonico e della continuity, ricerca delle copie, rapporto sostanziale e aggiornamento della continuity. Nessuna rigenerazione o modifica del TRAIN. La consegna prevista contiene soltanto questi cinque file:
1. `reports/STUDENT_5_TRAIN_V2_REPAIR_RECOVERY_CP39.md` (nuovo).
2. `reports/evidence/student5-path-b-cp39-recovery/audit.json` (nuovo).
3. `reports/evidence/student5-path-b-cp39-recovery/starting-tree.json` (nuovo; metadati Git, nessun payload dataset).
4. `reports/evidence/student5-path-b-cp39-recovery/SHA256SUMS` (nuovo).
5. `docs/WORK_CONTINUITY_STUDENT_5.md` (aggiornato senza rimuovere lo storico).

Questi file documentano un recovery BLOCKED, non sostituiscono l'artifact TRAIN v2 mancante. La verifica del tree prima della pubblicazione deve escludere ogni altra modifica.

## Artifact e integrità

| Campo | TRAIN v1 | TRAIN v2 |
|---|---|---|
| Logical ID | student5-matrix-nlu-v3-train-v1 | student5-matrix-nlu-v3-train-v2 richiesto |
| Path | data/student5_v3/ | data/student5_v3_train_v2/ assente |
| File Git | 130 | 0 al punto di partenza |
| Dimensione aggregata Git attuale | 13.139.472 byte sui 130 file | non verificabile |
| Righe / claim | 3150 / 3990, dalle prove canoniche immutate | non verificabili |
| SHA logico | 1118a900026f48cfcc290c3f9dc52a1a019a6a1f4761661f326c33770523140e | non verificabile |
| Provenance | manifest e 63 shard di lineage esistenti, identità Git conservate | non verificabile |
| Validator / target builder nel recovery | non rieseguiti | impossibili senza candidato |

I 130/130 blob TRAIN v1 corrispondono esattamente alla baseline persistente `reports/evidence/student5-path-b-cp38-repair-spec/input-identities.json`; l'intero identity bridge di 140 path corrisponde 140/140. È una verifica di immutabilità per identità Git, non un nuovo calcolo SHA256 sui payload. Il manifest immutato riporta lo SHA logico e il fingerprint V3 `7b0646e44243ad897760c0fcadbe141f1b8e88e3fd8d63a1789106571b9987b0`. Nessun dato TRAIN v1 è stato modificato.

## Verifica esplicita D01–D07

L'approvazione è presente nel prompt canonico al blob `e79406b72f7559de474629e5956ebd23e4a43e78`. Il suo starting HEAD interno è il predecessore CP38; l'HEAD esplicito del recovery governa senza rollback. La continuity CP38 registra storicamente decisioni aperte; il prompt successivo le approva. Questo recovery aggiorna la distinzione senza richiedere nuova approvazione.

| Decisione | Requisito da verificare sul candidato | Esito attuale |
|---|---|---|
| D01 | desiderio presente CURRENT; FUTURE solo per proposizione desiderio esplicitamente futura | NON VERIFICABILE: righe e diff mancanti |
| D02 | source e viewpoint distinti, nessuna copia meccanica | NON VERIFICABILE: gold/provenance mancanti |
| D03 | BELIEF per wrapper mentale esplicito, DIRECT per asserti senza wrapper | NON VERIFICABILE |
| D04 | sei malformed disattivati; reflexive adjudicate singolarmente con originali preservati | NON VERIFICABILE sul v2; originali v1 Git immutati |
| D05 | No metalinguistico fuori dallo scope del claim positivo CORRECT | NON VERIFICABILE: esempi e scope evidence mancanti |
| D06 | zero-claim naturali e UNKNOWN distinti | NON VERIFICABILE |
| D07 | indipendenza ruoli linguisticamente giustificata; nessuna divergenza artificiale | NON VERIFICABILE; precedente dubbio owner/subject solo storico |

Anche enumerazioni complete 628/404, sei omissioni temporali, 11 casi code-switch, conteggi per lingua/famiglia/head, alias deterministici, assenza provenance DEV/Frozen, contrastività semantica, schema 100% e consumo di tutte le righe dal target builder non sono certificabili sul candidato scomparso. Nessun requisito è dichiarato PASS per sostituire tale mancanza.

## Scope e limiti delle prove negative

Per le azioni di questo recovery:

```text
trainingExecuted=false
canonicalDevRead=false
frozenDataRead=false
trainV1Modified=false
evaluatorModified=false
decoderModified=false
calibrationModified=false
quantizationExecuted=false
onnxExecuted=false
nextWorkStarted=false
```

Nessun import/runtime modello, optimizer, backprop, generatore TRAIN, workflow dispatch, DEV/Frozen payload o output Frozen è stato eseguito/letto. Undici definizioni workflow sono state ispezionate per il trigger: i push sono limitati a main; il commit documentale sul branch non avvia quei workflow. Student-4, Path A, pristine, contratto, evaluator/decoder/calibration e tutti gli altri artifact tracciati restano identici nel confronto completo dei blob.

Limite: queste conferme descrivono le azioni osservabili di questo recovery e lo stato Git. Non sono un audit completo retroattivo di tutti i processi della sessione precedente, il cui log locale è perduto. La cronologia nega quelle attività, ma non è prova indipendente sufficiente; l'assenza di run del branch non esclude da sola processi locali storici.

## Prove riproducibili e blocker residui

Evidenze macchina: `reports/evidence/student5-path-b-cp39-recovery/audit.json` e `starting-tree.json`; SHA256SUMS copre rapporto, continuity e le due prove JSON.

Con una checkout autenticata che conserva il commit finale:
```sh
git rev-parse student5-path-b-v3
git show -s --format=fuller ff6ee962bcc7629ace9bcd69263ddbf497376df8
git ls-tree -r ff6ee962bcc7629ace9bcd69263ddbf497376df8 -- data/student5_v3_train_v2
git diff --name-status ff6ee962bcc7629ace9bcd69263ddbf497376df8 HEAD
git diff --exit-code ff6ee962bcc7629ace9bcd69263ddbf497376df8 HEAD -- data/student5_v3 matrix_nlu
sha256sum -c reports/evidence/student5-path-b-cp39-recovery/SHA256SUMS
```
I comandi qui elencati sono una procedura per il revisore, non una dichiarazione di esecuzione in una checkout locale assente. Le letture/confronti effettivi sono stati eseguiti mediante API Git autenticate; hash dei file di consegna calcolati localmente con Python.

R01: candidato, script di generazione e risultati originali non pubblicati e non recuperati; violazione della persistenza richiesta dal prompt.
R02: impossibilità di verificare integralmente requisiti obbligatori D01–D07, provenance, checksum e validazione. Si applica lo STOP del recovery, non una ricostruzione spacciata per lavoro preesistente.

Per una futura ripresa servono i bytes originali del candidato, script/config e ledger/prove originali, da confrontare con gli indizi storici; se nessuna copia è recuperabile, occorre una ricostruzione controllata disposta dal Supervisor che tratti come nuova esecuzione ogni risultato rigenerato. V1 e CP37/CP38 sono ancora disponibili in Git per quella eventuale ripresa. Non è necessario ricreare o ricaricare il pristine. Non viene avviata adesso alcuna ricostruzione né remediation semantica.

CP36 Gate B resta separatamente BLOCKED. Il rapporto non chiude Gate B né autorizza training. STOP dopo consegna al Supervisor GPT.
