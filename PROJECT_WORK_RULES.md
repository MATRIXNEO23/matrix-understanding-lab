# Regole canoniche di lavoro

Stato: CANONICO
Data: 2026-09-07

## Una repository alla volta

Salvo indicazione esplicita del proprietario, si lavora su una sola repository alla volta.

- Una sola repository è il target di lavoro attivo.
- Le altre repository possono essere lette solo quando serve verificare dipendenze o contesto.
- Non si scrive su altre repository senza istruzione esplicita del proprietario.
- Il cambio di repository attiva richiede istruzione esplicita.
- Se una modifica di un componente richiede aggiornamenti di codice, test, documentazione o continuità nella repository attiva, tali aggiornamenti vanno mantenuti coerenti nello stesso workstream.
- Non creare specifiche parallele quando esiste già un documento canonico aggiornabile.

## Repository storiche = backup

Le repository/versioni precedenti o superate sono backup/checkpoint di recupero, non target di sviluppo normale.

- Restano integre come riferimento e via di ritorno.
- Si consultano o recuperano componenti da esse se la linea corrente arriva a un punto morto, introduce una regressione grave o serve confrontare una soluzione precedente valida.
- Non si riprende automaticamente un'intera vecchia repo: si recuperano solo i componenti/commit necessari con provenienza chiara.
- Non si modificano o cancellano le repo backup senza istruzione esplicita del proprietario.

## Artifact modello persistenti e non sovrascrivibili

La policy canonica è:

`docs/MODEL_ARTIFACT_PERSISTENCE_POLICY.md`

Regole obbligatorie:

- ogni versione/modello/checkpoint importante deve essere recuperabile in modo persistente dalla repository;
- GitHub Actions artifacts sono temporanei e non possono essere l'unica copia;
- per file grandi usare Git LFS o GitHub Release asset della stessa repository, con manifest/checksum/versione committati;
- non sovrascrivere mai artifact, tag, versioni o baseline esistenti;
- Student-4, Student-5 pristine, Path A e Path B restano linee distinte;
- ogni nuova versione materiale riceve un nuovo identificativo e SHA-256;
- un task che produce un modello non è chiuso finché artifact persistente + manifest/registry + checksum + lineage non sono salvati.

## Continuità realmente riprendibile

La continuity non è un semplice diario. Deve permettere a un nuovo executor/Work di ripartire senza memoria umana aggiuntiva.

Per ogni input/artifact indispensabile al passo successivo deve contenere:

```text
cosa serve
perché serve
repository
branch/HEAD di riferimento
locator esatto
release/tag/asset ID o path Git/LFS
filename
bytes attesi
SHA-256 atteso
modalità di accesso/autenticazione necessaria
procedura di acquisizione prevista per l'executor
fallback/reproduction source se esiste
ultimo checkpoint in cui il recupero è stato verificato
```

Prima di chiudere una sessione o dichiarare pronto il passo successivo, verificare che gli artifact necessari siano **non solo esistenti ma recuperabili dall'ambiente che dovrà usarli**.

Regola:

```text
NEXT TASK READY
!=
ARTIFACT EXISTS

NEXT TASK READY
=
ARTIFACT LOCATED + ACCESS ROUTE KNOWN + IDENTITY CHECKSUM KNOWN + RESUME POINT RECORDED
```

Se l'accesso non è disponibile, il blocker va scoperto e registrato prima della fine del checkpoint precedente, non scaricato sul proprietario alla sessione successiva.

Queste regole riguardano il metodo di lavoro e non modificano da sole l'architettura runtime.
