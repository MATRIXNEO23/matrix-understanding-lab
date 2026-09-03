# Matrix Understanding Lab

Laboratorio isolato per il benchmark P0 dell'Understanding di Matrix Engine.

## Scopo
Confrontare, senza modificare il runtime stabile di Neon Tides/Matrix Engine, tre approcci per il front-end linguistico trilingue IT/EN/ES:

1. baseline deterministica corrente;
2. ICU + Apache OpenNLP + semantic mapper Matrix;
3. NLU ONNX compatto + semantic mapper Matrix.

Il laboratorio non sostituisce Matrix Engine. Deve misurare quale front-end soddisfa meglio il contratto semantico Matrix con il minor costo possibile su Android/Moto G56.

## Vincoli
- italiano lingua primaria; inglese e spagnolo obbligatori;
- offline;
- Android-first;
- ownership/perspective/provenance Matrix preservate;
- nessun GGUF aggiuntivo per l'Understanding;
- licenze e provenance obbligatorie;
- nessuna promozione Observation/Belief -> World Truth;
- niente integrazione nel runtime principale finché P0 non produce un verdetto documentato;
- benchmark qualità + RAM/PSS + CPU + latenza + dimensione APK/modelli;
- baseline Matrix principale congelata: `ae82d5cf843d52b3d60caadd161e4a5516fc5d0d`.

Leggere `docs/P0_UNDERSTANDING_BENCHMARK_SPEC.md` prima di implementare.

## P0 status

P0 è completo come benchmark isolato. La raccomandazione production è `KEEP`:
Candidate B vince il confronto qualità congelato, ma non è idoneo alla
produzione per la provenance del modello italiano e per le misure Moto G56
ancora pendenti; Candidate C non è pronto. Nessuna integrazione production è
autorizzata.

Evidenze principali:

- `docs/P0_QUALITY_RESULTS.md` — unified A/B metrics;
- `docs/P0_ERROR_ANALYSIS.md` — residual errors by required family;
- `docs/P0_DEVILS_ADVOCATE.md` — attack on the leading candidate;
- `docs/MOBILE_PROBE.md` — offline Android/Moto G56 procedure;
- `docs/P0_VERDICT.md` — final A/B/C and partial-candidate tables.

La CI esegue unit test, benchmark unificato e build del probe Android debug con:

```text
gradle --no-daemon :core:test
gradle --no-daemon :cli:run
gradle --no-daemon :android-probe:assembleDebug
```
