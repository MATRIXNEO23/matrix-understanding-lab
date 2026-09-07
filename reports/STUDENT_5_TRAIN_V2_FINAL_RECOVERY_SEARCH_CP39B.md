Supervisor GPT — Student-5 TRAIN v2 Final Recovery Search Report

ORIGINAL_TRAIN_V2_RECOVERY = NOT_FOUND

Repository: MATRIXNEO23/matrix-understanding-lab
Branch: `student5-path-b-v3`
Starting HEAD verificato: `663eecad745ab0f278e411f95b21da550ed6ed1a`
Data: 2026-09-07
Final HEAD: commit che introduce questo rapporto, figlio diretto dello starting HEAD; lo SHA esatto viene consegnato in chat dopo pubblicazione e lettura remota. Risoluzione: `git log -1 --format=%H -- reports/STUDENT_5_TRAIN_V2_FINAL_RECOVERY_SEARCH_CP39B.md`.

Non è stata trovata una copia del candidato originale, né un insieme completo dei suoi sorgenti originali che ne permetta il recupero esatto, nelle superfici accessibili e pertinenti controllate. NOT_FOUND è riferito a queste superfici: non dimostra “non esiste in assoluto”. Nessun dato è stato rigenerato.

## Cosa è stato cercato

Identità `student5-matrix-nlu-v3-train-v2`; directory prevista `data/student5_v3_train_v2/`; vecchie directory `cp39-delivery/` e `cp39-candidate-01-retained/`; script `student5_train_v2_authored.py`, `student5_train_v2_repair.py`, `audit_student5_train_v2.py`, `cp39_finish_report.py`; manifest, repair-proof, disposition/alias ledger, semantic census, report, shard e archivi.

Indizi storici conservati ma NON ricertificati:
- candidato finale: 1.723 righe / 2.416 claim;
- SHA logico `01d0a249ea05febb83142ead6b730a914de67495e37dec4fa2faf6b1ccc0d813`;
- primo candidato: SHA logico `cad7b3fd078adcfec558375b267749258578a98f5e2170a1e9e42e9350f56bfd`;
- ZIP iniziale: 995.905 byte, SHA `547957a5cf98db05a2f13a051e779398ecc5b46e3b570d89cf1d90f8e93f0128`;
- file massimo previsto 474.130 byte, consegna storicamente descritta come 85 file / circa 12.323.461 byte.

Questi riferimenti hanno guidato ricerca per nomi, path, dimensioni, metadati, contenuti documentali e hash. Nessuna corrispondenza testuale è stata considerata recupero dei payload.

## Superfici effettivamente controllate

| Superficie | Verifica eseguita | Esito |
|---|---|---|
| Working tree, file non tracciati, checkout/worktree | Inventario locale di workspace e directory temporanee; ricerca di repository Git e marker sorgenti | Nessuna checkout valida della repository; restano soltanto i cinque file documentali del recovery precedente |
| Stash, reflog, oggetti locali non raggiungibili | Tentati status, worktree list, stash list, reflog e fsck | Exit 128: /workspace/.git è vuota, non un object database; nessuno stash/reflog recuperabile in tale directory |
| Branch e tag remoti | Inventario di tutti i ref pubblicati e tree ricorsivi dei rispettivi HEAD | Due branch e tre tag; nessun candidato |
| History Git raggiungibile | Tre pagine fino al commit radice; tree ricorsivi di tutti i 247 commit | 247/247 tree non troncati; 655 coppie path/blob distinte, nessun candidato o sorgente originale |
| Pull request | Elenco state=all | Nessuna PR restituita in questa repository |
| Actions runs | Tutte le quattro pagine | 302 run esaminati |
| Actions artifact | Elenco per ognuno dei 302 run, conteggi completi per pagina | 624 record artifact, nessun match di candidato; ultimo aggiornamento 2026-09-07 06:32:27 UTC, precedente all'incarico delle 09:03:19 UTC |
| Releases | Tutte le tre Release e relativi asset | Solo pristine, Path A e Gate A CP35 |
| Archivi locali | SHA256 dell'archivio e directory dei membri dei tre ZIP sopravvissuti | Due modelli noti e un archivio di log Android/MLC; nessun membro dataset/script candidato |
| Directory temporanee/cache accessibili | Metadati in workspace, /tmp, /var/tmp, cache, staging e directory output; confronto nomi e dimensioni | Nessun candidato individuato; esclusi software/tool cache non pertinenti |
| Sessioni persistenti locali | Inventario degli 11 archivi disponibili e date | Ultima modifica 26 agosto; nessun archivio della precedente esecuzione CP39 individuato; contenuti non aperti |
| File cancellati ancora aperti | Destinazioni accessibili dei descrittori /proc/*/fd | Nessun riferimento pertinente; 132 entry non leggibili o scomparse durante l'ispezione |
| File persistenti Library | Sette pagine esaurite: 1.217 elementi owned; shared zero; ricerche aggiuntive per hash, path e nomi | Nessun file candidato; nessun elemento file creato/modificato dopo l'incarico. Risultati ranked non pertinenti non considerati match |
| Continuità/report e stato in memoria noto | Lettura remota dei documenti CP39, ricerca marker nei documenti locali; controllo handle storico noto | Solo descrizioni e checksum; handle cp39PendingDelivery assente, nessun payload |

Il commit radice raggiunto è `f17c3af1124d500c24145c3241b2821e7ac69e07`. Tutti i cinque ref remoti inventariati appartengono alla storia dei 247 commit. I due soli commit nella storia dal momento dell'incarico originale sono l'incarico stesso e il rapporto del recovery precedente. La ricerca della history ha esaminato metadati/tree, non payload DEV/Frozen.

L'endpoint globale artifact era rifiutato dal connettore; gli endpoint per-run hanno consentito di completare comunque l'inventario dei 624 record. Nessun artifact richiedeva una pagina ulteriore. I payload di artifact precedenti all'incarico e non pertinenti non sono stati scaricati o aperti.

## Archivi sopravvissuti: identità e distinzione

- `student5-path-b-v3-untrained-gate-a-cp35-20260907.zip`: 176.837.978 byte, 18 membri; SHA `dfe20ae4cfa49656f557872f6ba2afeabef6caea06390f943ae8cd0945a37d71`. Corrisponde al Gate A, non al candidato TRAIN.
- `student5-minilm-phase-a-pruned-40k.zip`: 88.361.246 byte, 22 membri; SHA `7804bfb245b71df9b835fff7ee00f6ec887e019772ae34c82d269d821d587191`. Corrisponde al pristine.
- `logs_89829753362.zip`: 99.466 byte, 13 membri; SHA `c287bbb3721b9a06ba8e05f07b8040f9d59ea6cfa762c59a65473cfc22573466`. I nomi dei membri identificano fasi build Android/MLC; nessun payload dati o sorgente candidato. Contenuto dei log non estratto.

È stato calcolato l'hash dei bytes compressi e ispezionato l'indice ZIP; nessun modello caricato e nessun file Frozen estratto. Un nome come candidate-manifest nel pristine non è stato confuso con il candidato TRAIN v2.

## Superfici non accessibili o limiti

1. Inventario cache GitHub Actions: endpoint rifiutato dal connettore con HTTP 400 INVALID_ARGUMENT; nessuna capacità alternativa esposta per enumerarlo. Non dichiaro vuote le cache.
2. Reflog lato server, oggetti Git dangling/unreachable remoti: non enumerabili mediante API esposte. Non esiste un database Git locale sopravvissuto; nessuno SHA Git di un commit/blob originale candidato è disponibile. Lo SHA256 logico non è un Git object ID interrogabile.
3. Storage potato, snapshot dell'host, backup non montati o versioni cancellate non esposte: non accessibili. Nessun tentativo di aggirare i limiti.
4. I 132 descrittori non leggibili/scomparsi non sono stati certificati vuoti.
5. L'inventario Library riguarda ciò che il servizio espone attualmente, non prova assenza in backup/versioni eliminate non esposte. Le ricerche ranked hanno restituito anche risultati storici non pertinenti: nessuna inferenza di exact-match dagli snippet.
6. Le sessioni locali disponibili sono precedenti all'incarico; non consentono di recuperare la trascrizione integrale dell'esecuzione originale.

Non è stata individuata una copia parziale ambigua da certificare: il limite è l'assenza di copie nelle superfici verificate e l'impossibilità di escludere quelle non esposte. Non attribuisco FOUND a ricordi, checksum o resoconti.

## Scope, persistenza e prove

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
trainV2Recreated=false
nextWorkStarted=false
```

Nessuna applicazione D01–D07, rigenerazione, training, optimizer, backprop, modello caricato, workflow dispatch o lavoro successivo. Nessun candidato trovato è stato modificato. Student-4, pristine, Path A, TRAIN v1 e codice restano protetti mediante confronto dell'intero tree di consegna con lo starting HEAD.

File di sola documentazione/evidenza della consegna:
- questo rapporto;
- `docs/WORK_CONTINUITY_STUDENT_5.md`, aggiornamento di stato e appendice, storico conservato;
- `reports/evidence/student5-path-b-cp39b-final-search/search.json`;
- `reports/evidence/student5-path-b-cp39b-final-search/git-history.json`;
- `reports/evidence/student5-path-b-cp39b-final-search/actions-inventory.json`;
- `reports/evidence/student5-path-b-cp39b-final-search/SHA256SUMS`.

SHA256SUMS copre gli altri cinque file; confronto blob Git prima della pubblicazione e readback remoto sono i controlli di consegna. Il final HEAD esatto è riportato nel messaggio finale dopo tali controlli. Gli inventari persistono ID run/artifact, date, digest, riferimenti e path necessari a verificare le conclusioni, senza copiare payload DEV/Frozen né dati Library non pertinenti.

Esempi di richieste effettivamente eseguite:
```text
GET /repos/MATRIXNEO23/matrix-understanding-lab/git/matching-refs/
GET /repos/MATRIXNEO23/matrix-understanding-lab/commits?sha=student5-path-b-v3&per_page=100&page=1..3
GET /repos/MATRIXNEO23/matrix-understanding-lab/git/trees/{each_of_247_commits}?recursive=1
GET /repos/MATRIXNEO23/matrix-understanding-lab/actions/runs?per_page=100&page=1..4
GET /repos/MATRIXNEO23/matrix-understanding-lab/actions/runs/{each_of_302_runs}/artifacts?per_page=100
GET /repos/MATRIXNEO23/matrix-understanding-lab/releases?per_page=100
```

Dalla checkout del commit di consegna, il revisore può verificare:
```sh
sha256sum -c reports/evidence/student5-path-b-cp39b-final-search/SHA256SUMS
git diff --name-status 663eecad745ab0f278e411f95b21da550ed6ed1a HEAD
git diff --exit-code 663eecad745ab0f278e411f95b21da550ed6ed1a HEAD -- data matrix_nlu .github
```

Questi ultimi comandi sono istruzioni per il revisore, non una dichiarazione di checkout locale esistente. Le verifiche Git di consegna usano l'API autenticata e confrontano tutti i blob.

Nessun verdetto di questa ricerca autorizza ricreazione o training. TRAIN_V2_REPAIR resta BLOCKED; CP36 Gate B resta separatamente BLOCKED. STOP e attesa del prossimo incarico del Supervisor GPT.
