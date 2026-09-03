# ARCHITETTURA — MODELLO AI CON MEMORIA IN PYTHON

Status: progettazione, nessun codice applicativo ancora autorizzato.

## Obiettivo
Costruire un sistema AI locale/modulare in Python con memoria persistente, recupero coerente dei ricordi, contesto conversazionale, reflection controllata, diagnostica e test automatici. L'architettura deve essere separata in componenti sostituibili e verificabili, evitando che il modello linguistico scriva direttamente nello stato canonico.

## 1. Elenco esatto dei file

### Root

- `main.py` — entry point dell'applicazione e avvio del ciclo conversazionale.
- `config.py` — configurazione centralizzata di percorsi, limiti, modelli, soglie e feature flag.
- `requirements.txt` — dipendenze Python bloccate e riproducibili.
- `.env.example` — esempio delle sole variabili d'ambiente opzionali, senza segreti reali.
- `README.md` — istruzioni di installazione, avvio, test e struttura del progetto.

### Package `matrix_ai/`

- `matrix_ai/__init__.py` — inizializzazione del package.
- `matrix_ai/types.py` — dataclass/enum canonici per messaggi, claim, ricordi, eventi, emozioni, goal e risultati.
- `matrix_ai/contracts.py` — contratti e invarianti tra i moduli.
- `matrix_ai/pipeline.py` — orchestratore end-to-end del flusso input -> memoria -> reasoning -> risposta -> write-back.

### Package `matrix_ai/llm/`

- `matrix_ai/llm/__init__.py` — package LLM.
- `matrix_ai/llm/backend.py` — interfaccia astratta per il backend linguistico.
- `matrix_ai/llm/llama_cpp_backend.py` — adapter locale per modelli GGUF via llama.cpp.
- `matrix_ai/llm/prompt_builder.py` — costruzione token-aware del contesto da inviare al modello.
- `matrix_ai/llm/output_parser.py` — parsing e validazione dell'output strutturato del modello.

### Package `matrix_ai/understanding/`

- `matrix_ai/understanding/__init__.py` — package Understanding.
- `matrix_ai/understanding/normalizer.py` — normalizzazione Unicode/testuale non semantica.
- `matrix_ai/understanding/model.py` — wrapper del modello NLU addestrato.
- `matrix_ai/understanding/decoder.py` — conversione dell'output NLU in claim strutturati.
- `matrix_ai/understanding/validator.py` — verifica delle invarianti di authority, ownership, provenance e schema.

### Package `matrix_ai/memory/`

- `matrix_ai/memory/__init__.py` — package memoria.
- `matrix_ai/memory/models.py` — schema dei record di memoria.
- `matrix_ai/memory/database.py` — connessione SQLite e gestione transazioni.
- `matrix_ai/memory/schema.py` — creazione/migrazione schema e indici FTS5.
- `matrix_ai/memory/repository.py` — CRUD canonico dei ricordi.
- `matrix_ai/memory/admission.py` — decisione IGNORE/EPISODIC/SEMANTIC/RELATIONSHIP/GOAL/CORRECTION.
- `matrix_ai/memory/retrieval.py` — recupero candidati tramite filtri, FTS5 e scoring.
- `matrix_ai/memory/reranker.py` — reranking leggero dei ricordi candidati.
- `matrix_ai/memory/consolidation.py` — deduplicazione, aggiornamento, correzione e consolidamento dei ricordi.

### Package `matrix_ai/cognition/`

- `matrix_ai/cognition/__init__.py` — package cognitivo.
- `matrix_ai/cognition/emotions.py` — stato emotivo breve e aggiornamenti appraisal-driven.
- `matrix_ai/cognition/relationships.py` — stato relazionale persistente tra entità.
- `matrix_ai/cognition/goals.py` — creazione, priorità, scadenza e completamento dei goal.
- `matrix_ai/cognition/intentions.py` — selezione dell'intenzione attiva da beliefs/goals/stato.
- `matrix_ai/cognition/reflection.py` — reflection bounded con provenance e belief revision.
- `matrix_ai/cognition/action_selector.py` — generazione, filtro e ranking delle azioni possibili.

### Package `matrix_ai/world/`

- `matrix_ai/world/__init__.py` — package mondo.
- `matrix_ai/world/state.py` — stato canonico del mondo.
- `matrix_ai/world/events.py` — tipi di evento e registro eventi.
- `matrix_ai/world/authority.py` — separazione WORLD_TRUTH/OBSERVATION/REPORT/BELIEF/INFERENCE.
- `matrix_ai/world/scheduler.py` — scheduler event-driven per attività, reflection e interazioni autonome.

### Package `matrix_ai/agents/`

- `matrix_ai/agents/__init__.py` — package agenti.
- `matrix_ai/agents/persona.py` — profilo stabile del personaggio.
- `matrix_ai/agents/agent_state.py` — stato runtime compatto del singolo NPC.
- `matrix_ai/agents/agent.py` — ciclo percezione -> memoria -> appraisal -> goal -> azione.
- `matrix_ai/agents/multi_agent.py` — coordinamento NPC-NPC e gestione degli incontri.

### Package `matrix_ai/training/`

- `matrix_ai/training/__init__.py` — package training automatico.
- `matrix_ai/training/datasets.py` — acquisizione, provenance, normalizzazione e split dei dataset.
- `matrix_ai/training/labels.py` — mapping dei dataset esterni nello schema Matrix.
- `matrix_ai/training/train_nlu.py` — training automatico del modello Understanding.
- `matrix_ai/training/train_admission.py` — training del classificatore di memory admission.
- `matrix_ai/training/train_retrieval.py` — training del reranker di memoria.
- `matrix_ai/training/train_action_ranker.py` — training del ranker delle azioni.
- `matrix_ai/training/evaluate.py` — valutazione unificata su dev/frozen test.
- `matrix_ai/training/export.py` — export ONNX, quantizzazione e checksum degli artifact.
- `matrix_ai/training/experiment_tracker.py` — registro locale riproducibile di configurazioni, seed, metriche e artifact.

### Package `matrix_ai/diagnostics/`

- `matrix_ai/diagnostics/__init__.py` — package diagnostica.
- `matrix_ai/diagnostics/tracing.py` — trace strutturato input -> claim -> memoria -> decisione -> output.
- `matrix_ai/diagnostics/metrics.py` — metriche qualità, latenza, memoria e regressioni.
- `matrix_ai/diagnostics/audit.py` — controlli automatici su provenance, invarianti e contaminazioni.

### Test

- `tests/conftest.py` — fixture condivise.
- `tests/test_contracts.py` — test dei contratti e invarianti.
- `tests/test_understanding.py` — unit/regression/adversarial dell'Understanding.
- `tests/test_memory_database.py` — persistenza e migrazioni SQLite.
- `tests/test_memory_admission.py` — classificazione e safety dell'admission.
- `tests/test_memory_retrieval.py` — recall/ranking/coerenza del retrieval.
- `tests/test_memory_consolidation.py` — correzioni, deduplica e aggiornamento temporale.
- `tests/test_emotions.py` — traiettorie emotive e decadimento.
- `tests/test_relationships.py` — evoluzione coerente delle relazioni.
- `tests/test_goals.py` — lifecycle dei goal.
- `tests/test_reflection.py` — reflection, provenance e belief revision.
- `tests/test_action_selector.py` — fattibilità e ranking delle azioni.
- `tests/test_multi_agent.py` — scenari NPC-NPC.
- `tests/test_pipeline.py` — end-to-end dell'intera pipeline.
- `tests/test_properties.py` — property-based test delle invarianti.
- `tests/test_fuzz.py` — fuzzing di input e stato.
- `tests/test_soak.py` — simulazioni lunghe e rilevamento drift/leak.

### Dataset e artifact

- `data/README.md` — regole di provenance/licenza e struttura dei dati.
- `data/raw/.gitkeep` — placeholder per dataset sorgente non necessariamente versionati.
- `data/processed/.gitkeep` — placeholder per dataset normalizzati/splittati.
- `data/gold/.gitkeep` — benchmark gold/frozen.
- `artifacts/.gitkeep` — modelli, ONNX, checksum e report generati.
- `docs/WORK_CONTINUITY.md` — stato canonico di continuità e NEXT ACTION esatta.

## 2. Responsabilità sintetica per file

Le responsabilità sono definite nell'elenco precedente e sono vincolanti: ogni file deve avere una sola responsabilità primaria; nessun file applicativo può diventare un contenitore generico di logica appartenente a moduli diversi.

## 3. Ordine esatto di costruzione

1. `config.py`
2. `matrix_ai/types.py`
3. `matrix_ai/contracts.py`
4. `matrix_ai/world/authority.py`
5. `matrix_ai/world/state.py`
6. `matrix_ai/world/events.py`
7. `tests/test_contracts.py`
8. `matrix_ai/memory/models.py`
9. `matrix_ai/memory/database.py`
10. `matrix_ai/memory/schema.py`
11. `matrix_ai/memory/repository.py`
12. `tests/test_memory_database.py`
13. `matrix_ai/understanding/normalizer.py`
14. `matrix_ai/understanding/model.py`
15. `matrix_ai/understanding/decoder.py`
16. `matrix_ai/understanding/validator.py`
17. `tests/test_understanding.py`
18. `matrix_ai/training/datasets.py`
19. `matrix_ai/training/labels.py`
20. `matrix_ai/training/experiment_tracker.py`
21. `matrix_ai/training/train_nlu.py`
22. `matrix_ai/training/evaluate.py`
23. `matrix_ai/training/export.py`
24. `matrix_ai/memory/admission.py`
25. `matrix_ai/training/train_admission.py`
26. `tests/test_memory_admission.py`
27. `matrix_ai/memory/retrieval.py`
28. `matrix_ai/memory/reranker.py`
29. `matrix_ai/training/train_retrieval.py`
30. `tests/test_memory_retrieval.py`
31. `matrix_ai/memory/consolidation.py`
32. `tests/test_memory_consolidation.py`
33. `matrix_ai/cognition/emotions.py`
34. `tests/test_emotions.py`
35. `matrix_ai/cognition/relationships.py`
36. `tests/test_relationships.py`
37. `matrix_ai/cognition/goals.py`
38. `tests/test_goals.py`
39. `matrix_ai/cognition/intentions.py`
40. `matrix_ai/cognition/action_selector.py`
41. `matrix_ai/training/train_action_ranker.py`
42. `tests/test_action_selector.py`
43. `matrix_ai/llm/backend.py`
44. `matrix_ai/llm/llama_cpp_backend.py`
45. `matrix_ai/llm/prompt_builder.py`
46. `matrix_ai/llm/output_parser.py`
47. `matrix_ai/cognition/reflection.py`
48. `tests/test_reflection.py`
49. `matrix_ai/world/scheduler.py`
50. `matrix_ai/agents/persona.py`
51. `matrix_ai/agents/agent_state.py`
52. `matrix_ai/agents/agent.py`
53. `matrix_ai/agents/multi_agent.py`
54. `tests/test_multi_agent.py`
55. `matrix_ai/diagnostics/tracing.py`
56. `matrix_ai/diagnostics/metrics.py`
57. `matrix_ai/diagnostics/audit.py`
58. `matrix_ai/pipeline.py`
59. `tests/test_pipeline.py`
60. `tests/test_properties.py`
61. `tests/test_fuzz.py`
62. `tests/test_soak.py`
63. `main.py`
64. `README.md`
65. `requirements.txt`
66. `.env.example`
67. `data/README.md`
68. `docs/WORK_CONTINUITY.md`

Regola: non si passa al file/blocco successivo finché il contratto del blocco corrente e i relativi test non sono verdi.

## 4. Librerie esatte

### Runtime core

- Python `3.12.x` — versione runtime di riferimento.
- `pydantic==2.11.7` — validazione dei contratti e configurazioni strutturate.
- `pydantic-settings==2.10.1` — caricamento configurazione e variabili d'ambiente.
- `orjson==3.11.3` — serializzazione JSON veloce e deterministica.
- `structlog==25.4.0` — logging strutturato.

### Database/memoria

- `sqlite3` — modulo standard Python, database canonico locale.
- SQLite `FTS5` — full-text search integrata, nessun vector DB obbligatorio.
- `aiosqlite==0.21.0` — accesso asincrono leggero a SQLite quando necessario.

### NLU / training

- `torch==2.8.0` — training locale/CI quando disponibile gratuitamente.
- `transformers==4.56.0` — encoder multilingue e training heads.
- `datasets==4.0.0` — caricamento e preprocessing dei dataset.
- `tokenizers==0.22.0` — tokenizzazione efficiente.
- `accelerate==1.10.1` — training riproducibile CPU/GPU gratuita.
- `scikit-learn==1.7.1` — classificatori/ranker leggeri e metriche.
- `numpy==2.3.2` — calcolo numerico.
- `onnx==1.18.0` — formato/export del modello.
- `onnxruntime==1.22.1` — inferenza ONNX e verifica pre-mobile.
- `optimum==1.27.0` — export/ottimizzazione Hugging Face -> ONNX quando utile.

### LLM locale

- `llama-cpp-python==0.3.16` — backend GGUF locale per dialogo/reflection durante sviluppo desktop.

### Test e qualità

- `pytest==8.4.1` — test runner.
- `pytest-asyncio==1.1.0` — test asincroni.
- `hypothesis==6.138.7` — property-based testing.
- `coverage==7.10.5` — coverage.
- `ruff==0.12.11` — lint e formattazione.
- `mypy==1.17.1` — type checking statico.

### Benchmark/diagnostica

- `psutil==7.0.0` — CPU/RAM/process metrics durante benchmark desktop/CI.
- `rich==14.1.0` — report CLI leggibili durante sviluppo.

## Librerie che NON sono dipendenze canoniche

Non sono previste come base del progetto: LangChain, ChromaDB, FAISS, Pinecone, Weaviate, Milvus o altri framework/database vettoriali. Possono essere benchmarkati soltanto se un gate futuro dimostra un vantaggio misurabile che giustifica costo e complessità.

## Regola architetturale finale

`INPUT -> UNDERSTANDING -> TYPED CLAIMS -> AUTHORITY -> MEMORY ADMISSION -> SQLITE MEMORY -> RETRIEVAL -> EMOTION/RELATIONSHIP -> GOALS/INTENTIONS -> REFLECTION/DECISION -> LLM RENDERING -> VALIDATED EVENT -> WRITE-BACK`

Il modello linguistico non possiede l'autorità sullo stato canonico. La memoria resta persistente e interrogabile; ogni inferenza/reflection conserva provenance e confidence; ogni componente ha test isolati e test di integrazione prima del passaggio al componente successivo.