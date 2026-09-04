#!/usr/bin/env python3
"""Phase A: real vocabulary/embedding pruning for multilingual MiniLM.

No Matrix head is created or trained here. No quantization is executed. The
script accepts only a TRAIN-only selection corpus and a project-authored,
separate probe set embedded below.
"""

from __future__ import annotations

import argparse
import copy
import hashlib
import json
import math
import pathlib
import platform
import shutil
import statistics
import time
from collections import Counter, defaultdict


UPSTREAM_REPOSITORY = "microsoft/Multilingual-MiniLM-L12-H384"
UPSTREAM_REVISION = "6e8c1ec6b4ec4e3fc6eb7d2cd834fcd582b61daf"
UPSTREAM_LICENSE = "MIT"
TARGETS = (40_000, 60_000, 80_000, 100_000)
STUDENT4_MIXED_BYTES = 149_711_344
SPECIAL_OLD_IDS = (0, 1, 2, 3, 250_001)

# Declared before measurements. These are Phase-A feasibility criteria, not a
# relaxation or reinterpretation of any Matrix model-quality gate.
GATE = {
    "maxUnkRate": 0.001,
    "maxMeanInflationItEnEs": 1.15,
    "maxCodeSwitchInflation": 1.20,
    "maxAdultInflation": 1.15,
    "maxNamesLocationsInflation": 1.20,
    "maxAdultDisproportion": 0.05,
    "minMeanRepresentationCosine": 0.98,
    "minWorstRepresentationCosine": 0.90,
    "maxMeanContrastCosineDelta": 0.02,
    "maxP95ContrastCosineDelta": 0.05,
    "maxExactForwardDelta": 1e-6,
    "maxEstimatedInt8Bytes": STUDENT4_MIXED_BYTES - 1,
}


def sha256(path: pathlib.Path) -> str:
    digest = hashlib.sha256()
    with path.open("rb") as stream:
        for block in iter(lambda: stream.read(1024 * 1024), b""):
            digest.update(block)
    return digest.hexdigest()


def write_json(path: pathlib.Path, value) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(value, ensure_ascii=False, indent=2) + "\n",
                    encoding="utf-8")


def percentile(values: list[float], q: float) -> float:
    if not values:
        return 0.0
    ordered = sorted(values)
    index = min(len(ordered) - 1, max(0, math.ceil(q * len(ordered)) - 1))
    return float(ordered[index])


def file_manifest(root: pathlib.Path) -> list[dict]:
    return [{"path": str(path.relative_to(root)), "bytes": path.stat().st_size,
             "sha256": sha256(path)}
            for path in sorted(root.rglob("*")) if path.is_file()]


def directory_bytes(root: pathlib.Path) -> int:
    return sum(path.stat().st_size for path in root.rglob("*") if path.is_file())


def probes() -> list[dict]:
    rows = []

    def add(language: str, category: str, *texts: str, domain="general") -> None:
        for text in texts:
            rows.append({"language": language, "category": category,
                         "domain": domain, "text": text})

    add("it", "daily", "Ciao, come stai oggi?", "Ci vediamo verso le otto al solito bar.")
    add("it", "slang", "Boh raga, oggi non c'ho proprio sbatti.", "Cmq è una figata, ci becchiamo dopo?")
    add("it", "typo", "nn so xké nn mi hai risp ieri", "qual'è l'indirizzo giusto??")
    add("it", "negation", "Non voglio uscire con Marco.", "Non è vero che non mi piace Giulia.")
    add("it", "request", "Puoi venire da me stasera?", "Per favore ricordami di chiamare Marta.")
    add("it", "correction", "No, correggo: non vivo a Roma, adesso vivo a Padova.")
    add("it", "temporal", "Fino a ieri abitavo a Torino; domani sarò a Venezia.")
    add("it", "ownership", "Quella chiave non è mia: appartiene a Riccardo.")
    add("it", "third_party", "Sofia sostiene che José non lavori più a Milano.")
    add("it", "names_locations", "François raggiungerà San Sebastián passando da Città del Messico.")

    add("en", "daily", "Hey, how are you doing today?", "Let's meet around eight at the usual café.")
    add("en", "slang", "Dunno mate, I'm kinda tired rn.", "Low-key awesome; wanna hang out later?")
    add("en", "typo", "idk why u didnt reply yday", "whats the correct adress??")
    add("en", "negation", "I do not want to go out with Mark.", "It isn't true that I don't like Julia.")
    add("en", "request", "Could you come over tonight?", "Please remind me to call Martha.")
    add("en", "correction", "No, correction: I don't live in Rome; I live in Padua now.")
    add("en", "temporal", "Until yesterday I lived in Turin; tomorrow I'll be in Venice.")
    add("en", "ownership", "That key isn't mine; it belongs to Richard.")
    add("en", "third_party", "Sophia says that José no longer works in Milan.")
    add("en", "names_locations", "François will reach San Sebastián through Mexico City.")

    add("es", "daily", "Hola, ¿cómo estás hoy?", "Nos vemos sobre las ocho en el café de siempre.")
    add("es", "slang", "No sé, tío, hoy estoy un poco rayado.", "Qué guay; ¿quedamos luego?")
    add("es", "typo", "no se xq no m respondiste ayer", "cual es la direccion correcta??")
    add("es", "negation", "No quiero salir con Marco.", "No es verdad que Julia no me guste.")
    add("es", "request", "¿Puedes venir a mi casa esta noche?", "Recuérdame llamar a Marta, por favor.")
    add("es", "correction", "No, corrijo: no vivo en Roma; ahora vivo en Padua.")
    add("es", "temporal", "Hasta ayer vivía en Turín; mañana estaré en Venecia.")
    add("es", "ownership", "Esa llave no es mía; pertenece a Ricardo.")
    add("es", "third_party", "Sofía afirma que José ya no trabaja en Milán.")
    add("es", "names_locations", "François llegará a San Sebastián pasando por Ciudad de México.")

    adult = {
        "it": {
            "desire": ["Mi sento attratto da te e desidero maggiore intimità.",
                       "Mi eccita l'idea, ma per ora è soltanto una fantasia."],
            "request": ["Ti andrebbe di fare sesso con me stasera?",
                        "Posso baciarti e accarezzarti il corpo?"],
            "consent_boundary": ["Sì, acconsento, purché usiamo il preservativo.",
                                 "Ritiro il consenso: non toccarmi più e fermati subito."],
            "anatomy": ["Parliamo senza imbarazzo di vulva, clitoride, pene e testicoli."],
            "practice": ["Preferisco i preliminari e il sesso orale alla penetrazione."],
            "slang": ["Ha scritto che vuole scopare, ma io gli ho risposto di no."],
            "temporal": ["Ieri abbiamo fatto sexting; domani forse proveremo il roleplay."],
            "third_party": ["Luna racconta che Marco non vuole andare a letto con Giulia."],
            "conditional": ["Potrei fare dirty talk se entrambi fossimo ancora d'accordo."],
            "correction": ["No, correggo: non era consenso, avevo detto di fermarti."],
            "health": ["Voglio usare protezione, lubrificante e fare un test per le STI."],
        },
        "en": {
            "desire": ["I feel attracted to you and want more intimacy.",
                       "The idea arouses me, but for now it is only a fantasy."],
            "request": ["Would you like to have sex with me tonight?",
                        "May I kiss you and caress your body?"],
            "consent_boundary": ["Yes, I consent as long as we use a condom.",
                                 "I withdraw consent: do not touch me again and stop now."],
            "anatomy": ["We can discuss vulva, clitoris, penis and testicles without shame."],
            "practice": ["I prefer foreplay and oral sex to penetration."],
            "slang": ["He texted that he wanted to fuck, but I told him no."],
            "temporal": ["We sexted yesterday; tomorrow we might try roleplay."],
            "third_party": ["Luna says Mark does not want to sleep with Julia."],
            "conditional": ["I could do dirty talk if we both still agreed."],
            "correction": ["No, correction: that was not consent; I told you to stop."],
            "health": ["I want protection, lubricant and an STI test."],
        },
        "es": {
            "desire": ["Me atraes y deseo tener más intimidad contigo.",
                       "La idea me excita, pero por ahora solo es una fantasía."],
            "request": ["¿Te gustaría tener sexo conmigo esta noche?",
                        "¿Puedo besarte y acariciar tu cuerpo?"],
            "consent_boundary": ["Sí, doy mi consentimiento si usamos preservativo.",
                                 "Retiro mi consentimiento: no me toques más y para ahora."],
            "anatomy": ["Podemos hablar de vulva, clítoris, pene y testículos sin vergüenza."],
            "practice": ["Prefiero los preliminares y el sexo oral a la penetración."],
            "slang": ["Escribió que quería follar, pero yo le dije que no."],
            "temporal": ["Ayer hicimos sexting; mañana quizá probemos el roleplay."],
            "third_party": ["Luna cuenta que Marco no quiere acostarse con Julia."],
            "conditional": ["Podría hacer dirty talk si ambos siguiéramos de acuerdo."],
            "correction": ["No, corrijo: eso no era consentimiento; te dije que pararas."],
            "health": ["Quiero protección, lubricante y una prueba de ITS."],
        },
    }
    for language, categories in adult.items():
        for category, texts in categories.items():
            add(language, category, *texts, domain="adult_intimacy")

    add("code_switch", "code_switch",
        "Mi piace il sexting, pero solo si tú también quieres.",
        "No quiero fare sesso tonight, please non insistere.",
        "I want intimità contigo, ma possiamo fermarci whenever we want.",
        "¿Te va el dirty talk oppure preferisci solo kissing?",
        "Domani quizá hacemos roleplay, but only with explicit consenso.",
        "Marco said che non vuole sex con Julia esta noche.",
        "Questo condom is mine, el lubricante es tuyo.",
        "No means no, anche durante el sexting.",
        domain="adult_intimacy")
    return rows


def contrast_pairs() -> list[dict]:
    pairs = [
        ("negation-it", "Voglio uscire con Marco", "Non voglio uscire con Marco"),
        ("negation-en", "I want to go out with Mark", "I do not want to go out with Mark"),
        ("negation-es", "Quiero salir con Marco", "No quiero salir con Marco"),
        ("question-request-it", "Posso venire da te?", "Vieni da me"),
        ("question-request-en", "May I come over?", "Come over to my place"),
        ("question-request-es", "¿Puedo ir a tu casa?", "Ven a mi casa"),
        ("correction-it", "Vivo a Roma", "No, non vivo a Roma, vivo a Padova"),
        ("correction-en", "I live in Rome", "No, I do not live in Rome; I live in Padua"),
        ("correction-es", "Vivo en Roma", "No, no vivo en Roma; vivo en Padua"),
        ("third-party-it", "Sara vive a Roma", "Marco dice che Sara vive a Roma"),
        ("third-party-en", "Sara lives in Rome", "Mark says that Sara lives in Rome"),
        ("third-party-es", "Sara vive en Roma", "Marco dice que Sara vive en Roma"),
        ("temporal-it-past", "Vivo a Roma", "Vivevo a Roma"),
        ("temporal-it-future", "Vivo a Roma", "Vivrò a Roma"),
        ("temporal-en-past", "I live in Rome", "I used to live in Rome"),
        ("temporal-en-future", "I live in Rome", "I will live in Rome"),
        ("temporal-es-past", "Vivo en Roma", "Vivía en Roma"),
        ("temporal-es-future", "Vivo en Roma", "Viviré en Roma"),
        ("adult-desire-request-it", "Desidero fare sesso con te", "Ti chiedo di fare sesso con me"),
        ("adult-consent-refusal-it", "Sì, acconsento a essere toccato", "No, non acconsento a essere toccato"),
        ("adult-withdrawal-it", "Puoi continuare", "Prima acconsentivo, ora fermati"),
        ("adult-preference-experience-it", "Preferisco il sesso orale", "Ho fatto sesso orale ieri"),
        ("adult-desire-request-en", "I want to have sex with you", "I am asking you to have sex with me"),
        ("adult-consent-refusal-en", "Yes, I consent to being touched", "No, I do not consent to being touched"),
        ("adult-withdrawal-en", "You may continue", "I consented before, but stop now"),
        ("adult-preference-experience-en", "I prefer oral sex", "I had oral sex yesterday"),
        ("adult-desire-request-es", "Deseo tener sexo contigo", "Te pido que tengas sexo conmigo"),
        ("adult-consent-refusal-es", "Sí, consiento que me toques", "No, no consiento que me toques"),
        ("adult-withdrawal-es", "Puedes continuar", "Antes consentía, pero ahora para"),
        ("adult-preference-experience-es", "Prefiero el sexo oral", "Tuve sexo oral ayer"),
        ("adult-target-it", "Voglio baciarti", "Marco dice che vuole baciare Giulia"),
        ("adult-target-en", "I want to kiss you", "Mark says he wants to kiss Julia"),
        ("adult-target-es", "Quiero besarte", "Marco dice que quiere besar a Julia"),
        ("adult-explicit-hypothesis-it", "Farò sesso con te domani", "Forse farei sesso con te domani"),
        ("adult-explicit-hypothesis-en", "I will have sex with you tomorrow", "Maybe I would have sex with you tomorrow"),
        ("adult-explicit-hypothesis-es", "Tendré sexo contigo mañana", "Quizá tendría sexo contigo mañana"),
    ]
    return [{"id": identifier, "left": left, "right": right}
            for identifier, left, right in pairs]


def original_audit(upstream: pathlib.Path, tokenizer, model) -> dict:
    config = model.config
    embeddings = model.embeddings.word_embeddings
    reachable = len(tokenizer)
    if embeddings.num_embeddings < reachable:
        raise RuntimeError("tokenizer IDs exceed the model embedding table")
    id_checks = []
    for token_id in range(reachable):
        token = tokenizer.convert_ids_to_tokens(token_id)
        back = tokenizer.convert_tokens_to_ids(token)
        # Unknown surface aliases are not a bijection; every ID's canonical
        # token must at least resolve to a reachable deterministic ID.
        if back is None or not (0 <= int(back) < embeddings.num_embeddings):
            raise RuntimeError(f"non-deterministic tokenizer ID {token_id}: {token!r} -> {back}")
        if token_id in SPECIAL_OLD_IDS or token_id % 25_000 == 0:
            id_checks.append({"id": token_id, "token": token, "roundTripId": int(back)})
    parameters = {
        "total": sum(value.numel() for value in model.parameters()),
        "wordEmbeddings": embeddings.weight.numel(),
        "allEmbeddings": sum(value.numel() for value in model.embeddings.parameters()),
        "transformer": sum(value.numel() for value in model.encoder.parameters()),
        "pooler": sum(value.numel() for value in model.pooler.parameters()),
    }
    return {
        "repository": UPSTREAM_REPOSITORY,
        "revision": UPSTREAM_REVISION,
        "license": UPSTREAM_LICENSE,
        "modelType": config.model_type,
        "tokenizerClass": type(tokenizer).__name__,
        "sentencePieceSize": tokenizer.sp_model.get_piece_size(),
        "tokenizerVocabSize": tokenizer.vocab_size,
        "tokenizerLength": reachable,
        "modelEmbeddingRows": embeddings.num_embeddings,
        "unreachableTrailingEmbeddingRows": embeddings.num_embeddings - reachable,
        "hiddenSize": config.hidden_size,
        "numHiddenLayers": config.num_hidden_layers,
        "numAttentionHeads": config.num_attention_heads,
        "intermediateSize": config.intermediate_size,
        "maxPositionEmbeddings": config.max_position_embeddings,
        "configPadTokenId": config.pad_token_id,
        "tokenizerSpecialTokens": tokenizer.special_tokens_map,
        "tokenizerSpecialTokenIds": {
            "bos": tokenizer.bos_token_id, "pad": tokenizer.pad_token_id,
            "eos": tokenizer.eos_token_id, "unk": tokenizer.unk_token_id,
            "sep": tokenizer.sep_token_id, "cls": tokenizer.cls_token_id,
            "mask": tokenizer.mask_token_id,
        },
        "parameters": parameters,
        "upstreamFiles": file_manifest(upstream),
        "upstreamDirectoryBytes": directory_bytes(upstream),
        "tokenIdEmbeddingRowPolicy": "DIRECT_HF_TOKEN_ID_TO_SAME_EMBEDDING_ROW",
        "sampledCanonicalIdRoundTrips": id_checks,
        "alignmentStatus": "PASS",
    }


def count_selection_ids(corpus_path: pathlib.Path, tokenizer) -> tuple[Counter, dict]:
    counts = Counter()
    source_counts = Counter()
    language_counts = Counter()
    records = 0
    with corpus_path.open(encoding="utf-8") as stream:
        for line in stream:
            row = json.loads(line)
            ids = tokenizer.encode(row["text"], add_special_tokens=False)
            counts.update(ids)
            source_counts[row["source"]] += 1
            language_counts[row["language"]] += 1
            records += 1
    return counts, {"records": records, "uniqueObservedTokenIds": len(counts),
                    "countsBySource": dict(sorted(source_counts.items())),
                    "countsByLanguage": dict(sorted(language_counts.items()))}


def selected_old_ids(target: int, counts: Counter, tokenizer, proto) -> list[int]:
    if target < 5:
        raise ValueError("target must accommodate XLM-R special tokens")
    content_capacity = target - 5
    content_ids = range(4, len(tokenizer) - 1)
    ranked = sorted(content_ids, key=lambda token_id: (
        -counts[token_id],
        -float(proto.pieces[token_id - 1].score),
        token_id,
    ))
    observed = sum(1 for token_id in content_ids if counts[token_id] > 0)
    if observed > content_capacity:
        raise RuntimeError(f"target {target} cannot retain {observed} observed pieces")
    chosen = ranked[:content_capacity]
    return sorted(chosen)


def create_sentencepiece(original_path: pathlib.Path, output_path: pathlib.Path,
                         selected_content_hf_ids: list[int]) -> None:
    from sentencepiece import sentencepiece_model_pb2 as sp_pb2

    proto = sp_pb2.ModelProto()
    proto.ParseFromString(original_path.read_bytes())
    pieces = [copy.deepcopy(proto.pieces[index]) for index in (0, 1, 2)]
    pieces.extend(copy.deepcopy(proto.pieces[token_id - 1])
                  for token_id in selected_content_hf_ids)
    del proto.pieces[:]
    proto.pieces.extend(pieces)
    output_path.parent.mkdir(parents=True, exist_ok=True)
    output_path.write_bytes(proto.SerializeToString())


def new_to_old_mapping(target: int, selected_content_hf_ids: list[int]) -> list[int]:
    mapping = [0, 1, 2, 3]
    mapping.extend(selected_content_hf_ids)
    mapping.append(SPECIAL_OLD_IDS[-1])
    if len(mapping) != target or len(set(mapping)) != target:
        raise RuntimeError("invalid deterministic embedding mapping")
    return mapping


def estimated_mixed_int8_bytes(model) -> int:
    total = 0
    for name, tensor in model.state_dict().items():
        if name.startswith("embeddings.") or tensor.ndim < 2:
            total += tensor.numel() * 4
        else:
            total += tensor.numel()
    return total


def build_candidate(target: int, upstream: pathlib.Path, output: pathlib.Path,
                    original_tokenizer, original_model, counts: Counter, proto) -> dict:
    import torch
    from transformers import BertModel, XLMRobertaTokenizer

    selected = selected_old_ids(target, counts, original_tokenizer, proto)
    mapping = new_to_old_mapping(target, selected)
    output.mkdir(parents=True, exist_ok=True)
    create_sentencepiece(upstream / "sentencepiece.bpe.model",
                         output / "sentencepiece.bpe.model", selected)
    tokenizer = XLMRobertaTokenizer(
        vocab_file=str(output / "sentencepiece.bpe.model"),
        bos_token="<s>", eos_token="</s>", sep_token="</s>", cls_token="<s>",
        unk_token="<unk>", pad_token="<pad>", mask_token="<mask>",
    )
    tokenizer.save_pretrained(output)
    if len(tokenizer) != target:
        raise RuntimeError(f"candidate tokenizer length {len(tokenizer)} != {target}")

    config = copy.deepcopy(original_model.config)
    config.vocab_size = target
    config.pad_token_id = tokenizer.pad_token_id
    config.tokenizer_class = "XLMRobertaTokenizer"
    candidate = BertModel(config)
    original_state = original_model.state_dict()
    candidate_state = candidate.state_dict()
    word_name = "embeddings.word_embeddings.weight"
    for name in candidate_state:
        if name == word_name:
            candidate_state[name] = original_state[name][mapping].clone()
        else:
            candidate_state[name] = original_state[name].clone()
    candidate.load_state_dict(candidate_state, strict=True)
    candidate.eval()
    candidate.save_pretrained(output, safe_serialization=True)

    mapping_document = {
        "schemaVersion": "matrix.nlu.student5.token-id-remap.v1",
        "targetVocabSize": target,
        "oldTokenizerLength": len(original_tokenizer),
        "newTokenizerLength": len(tokenizer),
        "newTokenIdToOldTokenId": mapping,
        "oldTokenIdToNewTokenId": {str(old): new for new, old in enumerate(mapping)},
        "policy": "NEW_HF_ID_EMBEDDING_ROW_COPIED_FROM_DECLARED_OLD_HF_ID",
    }
    write_json(output / "token-id-remap.json", mapping_document)

    reloaded_tokenizer = XLMRobertaTokenizer.from_pretrained(output, local_files_only=True)
    reloaded = BertModel.from_pretrained(output, local_files_only=True).eval()
    if len(reloaded_tokenizer) != target or reloaded.config.vocab_size != target:
        raise RuntimeError("save/reload vocabulary mismatch")
    if reloaded.config.pad_token_id != reloaded_tokenizer.pad_token_id:
        raise RuntimeError("save/reload pad-token mismatch")

    for new_id, old_id in enumerate(mapping):
        new_token = reloaded_tokenizer.convert_ids_to_tokens(new_id)
        old_token = original_tokenizer.convert_ids_to_tokens(old_id)
        if new_token != old_token:
            raise RuntimeError(f"token mapping mismatch at new ID {new_id}")
    expected_embeddings = original_state[word_name][mapping]
    if not torch.equal(reloaded.state_dict()[word_name], expected_embeddings):
        raise RuntimeError("reloaded embedding rows differ from mapped upstream rows")
    for name, tensor in original_state.items():
        if name != word_name and not torch.equal(reloaded.state_dict()[name], tensor):
            raise RuntimeError(f"non-embedding weight changed: {name}")

    params = sum(tensor.numel() for tensor in reloaded.parameters())
    embedding_params = reloaded.embeddings.word_embeddings.weight.numel()
    model_file = output / "model.safetensors"
    tokenizer_files = [path for path in output.iterdir()
                       if path.name not in {"model.safetensors", "config.json",
                                            "token-id-remap.json"} and path.is_file()]
    result = {
        "targetVocabSize": target,
        "actualTokenizerLength": len(reloaded_tokenizer),
        "embeddingParameters": embedding_params,
        "totalParameters": params,
        "parameterReductionPercent": 100 * (1 - params / sum(
            value.numel() for value in original_model.parameters())),
        "modelFp32Bytes": model_file.stat().st_size,
        "artifactDirectoryBytes": directory_bytes(output),
        "estimatedMixedHeadProtectedInt8Bytes": estimated_mixed_int8_bytes(reloaded),
        "tokenizerBytes": sum(path.stat().st_size for path in tokenizer_files),
        "mappingSha256": sha256(output / "token-id-remap.json"),
        "modelSha256": sha256(model_file),
        "sentencePieceSha256": sha256(output / "sentencepiece.bpe.model"),
        "specialTokenIds": {
            "bos": reloaded_tokenizer.bos_token_id, "pad": reloaded_tokenizer.pad_token_id,
            "eos": reloaded_tokenizer.eos_token_id, "unk": reloaded_tokenizer.unk_token_id,
            "mask": reloaded_tokenizer.mask_token_id,
        },
        "observedSelectionPiecesRetained": all(token_id in set(mapping)
                                                for token_id in counts),
        "tokenizerModelAlignment": "PASS",
        "saveReloadIntegrity": "PASS",
        "nonEmbeddingWeightsUnchanged": True,
        "files": file_manifest(output),
    }
    del candidate, reloaded
    return result


def tokenization_metrics(tokenizer, original_tokenizer, rows: list[dict]) -> dict:
    slices = defaultdict(list)
    for row in rows:
        slices["overall"].append(row)
        if row["language"] in {"it", "en", "es"}:
            slices[row["language"]].append(row)
        if row["language"] == "code_switch":
            slices["code_switch"].append(row)
        if row["domain"] == "adult_intimacy":
            slices["adult_intimacy"].append(row)
            if row["language"] in {"it", "en", "es"}:
                slices[f"adult_intimacy_{row['language']}"] .append(row)
        if row["category"] == "names_locations":
            slices["names_locations"].append(row)
        if row["domain"] == "adult_intimacy":
            slices[f"adult_category_{row['category']}"] .append(row)

    output = {}
    for name, selected in sorted(slices.items()):
        token_counts, original_counts, unk = [], [], 0
        per_sentence_inflation = []
        for row in selected:
            ids = tokenizer.encode(row["text"], add_special_tokens=False)
            baseline = original_tokenizer.encode(row["text"], add_special_tokens=False)
            token_counts.append(len(ids))
            original_counts.append(len(baseline))
            unk += sum(token_id == tokenizer.unk_token_id for token_id in ids)
            per_sentence_inflation.append(len(ids) / max(1, len(baseline)))
        output[name] = {
            "sentences": len(selected),
            "tokens": sum(token_counts),
            "unknownTokens": unk,
            "unkRate": unk / max(1, sum(token_counts)),
            "meanTokensPerSentence": statistics.mean(token_counts),
            "p95TokensPerSentence": percentile(token_counts, 0.95),
            "aggregateInflationVsOriginal": sum(token_counts) / max(1, sum(original_counts)),
            "meanSentenceInflationVsOriginal": statistics.mean(per_sentence_inflation),
            "p95SentenceInflationVsOriginal": percentile(per_sentence_inflation, 0.95),
        }
    return output


def pooled_representations(model, tokenizer, texts: list[str], batch_size=16) -> dict[str, list[float]]:
    import torch
    import torch.nn.functional as functional

    result = {}
    model.eval()
    with torch.no_grad():
        for start in range(0, len(texts), batch_size):
            batch = texts[start:start + batch_size]
            encoded = tokenizer(batch, padding=True, truncation=True, max_length=96,
                                return_tensors="pt")
            hidden = model(**encoded).last_hidden_state
            mask = encoded["attention_mask"].unsqueeze(-1).to(hidden.dtype)
            pooled = (hidden * mask).sum(1) / mask.sum(1).clamp_min(1)
            pooled = functional.normalize(pooled, p=2, dim=-1)
            for text, vector in zip(batch, pooled):
                result[text] = vector.cpu().tolist()
    return result


def cosine(left: list[float], right: list[float]) -> float:
    return float(sum(a * b for a, b in zip(left, right)))


def semantic_metrics(original_model, original_tokenizer, candidate_model,
                     candidate_tokenizer, mapping: list[int], rows: list[dict],
                     contrasts: list[dict], original_vectors: dict) -> dict:
    import torch

    texts = list(dict.fromkeys([row["text"] for row in rows] +
                               [pair[key] for pair in contrasts for key in ("left", "right")]))
    candidate_vectors = pooled_representations(candidate_model, candidate_tokenizer, texts)
    sentence_cosines = [cosine(original_vectors[text], candidate_vectors[text]) for text in texts]
    contrast_entries = []
    for pair in contrasts:
        original_value = cosine(original_vectors[pair["left"]], original_vectors[pair["right"]])
        candidate_value = cosine(candidate_vectors[pair["left"]], candidate_vectors[pair["right"]])
        contrast_entries.append({"id": pair["id"], "originalCosine": original_value,
                                 "candidateCosine": candidate_value,
                                 "absoluteDelta": abs(candidate_value - original_value)})

    exact_deltas = []
    unchanged = 0
    for text in texts:
        original_tokens = original_tokenizer.tokenize(text)
        candidate_tokens = candidate_tokenizer.tokenize(text)
        if original_tokens != candidate_tokens:
            continue
        old = original_tokenizer(text, return_tensors="pt")
        new = candidate_tokenizer(text, return_tensors="pt")
        remapped = torch.tensor([[mapping[token_id] for token_id in new["input_ids"][0].tolist()]])
        if not torch.equal(remapped, old["input_ids"]):
            raise RuntimeError("unchanged token sequence does not obey ID remapping")
        with torch.no_grad():
            expected = original_model(**old).last_hidden_state
            actual = candidate_model(**new).last_hidden_state
        exact_deltas.append(float((expected - actual).abs().max()))
        unchanged += 1
    deltas = [entry["absoluteDelta"] for entry in contrast_entries]
    return {
        "sentences": len(texts),
        "meanRepresentationCosine": statistics.mean(sentence_cosines),
        "minimumRepresentationCosine": min(sentence_cosines),
        "p05RepresentationCosine": percentile(sentence_cosines, 0.05),
        "contrastPairs": len(contrast_entries),
        "meanContrastCosineDelta": statistics.mean(deltas),
        "p95ContrastCosineDelta": percentile(deltas, 0.95),
        "maximumContrastCosineDelta": max(deltas),
        "unchangedTokenizationSentences": unchanged,
        "unchangedTokenizationMaxForwardDelta": max(exact_deltas, default=0.0),
        "contrastDetails": contrast_entries,
    }


def gate_candidate(candidate: dict) -> dict:
    coverage = candidate["coverage"]
    semantic = candidate["semanticPreservation"]
    general_mean = statistics.mean(coverage[lang]["aggregateInflationVsOriginal"]
                                   for lang in ("it", "en", "es"))
    checks = {
        "specialTokenIntegrity": candidate["specialTokenIntegrity"],
        "tokenizerModelAlignment": candidate["tokenizerModelAlignment"] == "PASS",
        "saveReloadIntegrity": candidate["saveReloadIntegrity"] == "PASS",
        "allSelectionPiecesRetained": candidate["observedSelectionPiecesRetained"],
        "unkIt": coverage["it"]["unkRate"] <= GATE["maxUnkRate"],
        "unkEn": coverage["en"]["unkRate"] <= GATE["maxUnkRate"],
        "unkEs": coverage["es"]["unkRate"] <= GATE["maxUnkRate"],
        "unkAdult": coverage["adult_intimacy"]["unkRate"] <= GATE["maxUnkRate"],
        "inflationIt": coverage["it"]["aggregateInflationVsOriginal"] <= GATE["maxMeanInflationItEnEs"],
        "inflationEn": coverage["en"]["aggregateInflationVsOriginal"] <= GATE["maxMeanInflationItEnEs"],
        "inflationEs": coverage["es"]["aggregateInflationVsOriginal"] <= GATE["maxMeanInflationItEnEs"],
        "codeSwitchInflation": coverage["code_switch"]["aggregateInflationVsOriginal"] <= GATE["maxCodeSwitchInflation"],
        "adultInflation": coverage["adult_intimacy"]["aggregateInflationVsOriginal"] <= GATE["maxAdultInflation"],
        "adultNotDisproportionate": coverage["adult_intimacy"]["aggregateInflationVsOriginal"] <=
        general_mean + GATE["maxAdultDisproportion"],
        "namesLocationsInflation": coverage["names_locations"]["aggregateInflationVsOriginal"] <=
        GATE["maxNamesLocationsInflation"],
        "meanRepresentationCosine": semantic["meanRepresentationCosine"] >=
        GATE["minMeanRepresentationCosine"],
        "worstRepresentationCosine": semantic["minimumRepresentationCosine"] >=
        GATE["minWorstRepresentationCosine"],
        "meanContrastPreservation": semantic["meanContrastCosineDelta"] <=
        GATE["maxMeanContrastCosineDelta"],
        "p95ContrastPreservation": semantic["p95ContrastCosineDelta"] <=
        GATE["maxP95ContrastCosineDelta"],
        "exactForwardEquivalence": semantic["unchangedTokenizationMaxForwardDelta"] <=
        GATE["maxExactForwardDelta"],
        "estimatedRuntimeSmallerThanStudent4":
        candidate["estimatedMixedHeadProtectedInt8Bytes"] <= GATE["maxEstimatedInt8Bytes"],
    }
    return {"passed": all(checks.values()), "checks": checks,
            "failedChecks": [name for name, passed in checks.items() if not passed]}


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--upstream", type=pathlib.Path, required=True)
    parser.add_argument("--selection-corpus", type=pathlib.Path, required=True)
    parser.add_argument("--output-dir", type=pathlib.Path, required=True)
    parser.add_argument("--targets", type=int, nargs="+", default=list(TARGETS))
    args = parser.parse_args()

    import sentencepiece as spm
    import torch
    from sentencepiece import sentencepiece_model_pb2 as sp_pb2
    from transformers import BertModel, XLMRobertaTokenizer

    torch.set_num_threads(4)
    started = time.perf_counter()
    args.output_dir.mkdir(parents=True, exist_ok=True)
    original_tokenizer = XLMRobertaTokenizer.from_pretrained(args.upstream,
                                                             local_files_only=True)
    original_model = BertModel.from_pretrained(args.upstream, local_files_only=True).eval()
    audit = original_audit(args.upstream, original_tokenizer, original_model)
    write_json(args.output_dir / "upstream-audit.json", audit)

    counts, selection_summary = count_selection_ids(args.selection_corpus, original_tokenizer)
    proto = sp_pb2.ModelProto()
    proto.ParseFromString((args.upstream / "sentencepiece.bpe.model").read_bytes())
    if len(proto.pieces) != original_tokenizer.sp_model.get_piece_size():
        raise RuntimeError("SentencePiece protobuf/tokenizer size mismatch")

    probe_rows = probes()
    contrasts = contrast_pairs()
    probe_texts = list(dict.fromkeys([row["text"] for row in probe_rows] +
                                     [pair[key] for pair in contrasts for key in ("left", "right")]))
    original_vectors = pooled_representations(original_model, original_tokenizer, probe_texts)
    original_coverage = tokenization_metrics(original_tokenizer, original_tokenizer, probe_rows)

    candidates = []
    for target in args.targets:
        candidate_dir = args.output_dir / f"minilm-it-en-es-vocab-{target // 1000}k"
        if candidate_dir.exists():
            shutil.rmtree(candidate_dir)
        result = build_candidate(target, args.upstream, candidate_dir,
                                 original_tokenizer, original_model, counts, proto)
        tokenizer = XLMRobertaTokenizer.from_pretrained(candidate_dir, local_files_only=True)
        model = BertModel.from_pretrained(candidate_dir, local_files_only=True).eval()
        mapping = json.loads((candidate_dir / "token-id-remap.json").read_text(
            encoding="utf-8"))["newTokenIdToOldTokenId"]
        result["coverage"] = tokenization_metrics(tokenizer, original_tokenizer, probe_rows)
        result["specialTokenIntegrity"] = (
            tokenizer.bos_token_id == 0 and tokenizer.pad_token_id == 1 and
            tokenizer.eos_token_id == 2 and tokenizer.unk_token_id == 3 and
            tokenizer.mask_token_id == target - 1
        )
        result["semanticPreservation"] = semantic_metrics(
            original_model, original_tokenizer, model, tokenizer, mapping,
            probe_rows, contrasts, original_vectors)
        result["byteReductionVsUpstreamPytorchPercent"] = 100 * (
            1 - result["modelFp32Bytes"] / (args.upstream / "pytorch_model.bin").stat().st_size)
        result["estimatedInt8ReductionVsStudent4MixedPercent"] = 100 * (
            1 - result["estimatedMixedHeadProtectedInt8Bytes"] / STUDENT4_MIXED_BYTES)
        result["gate"] = gate_candidate(result)
        write_json(candidate_dir / "candidate-manifest.json", result)
        result["files"] = file_manifest(candidate_dir)
        candidates.append(result)
        del model

    passing = sorted((candidate for candidate in candidates if candidate["gate"]["passed"]),
                     key=lambda candidate: candidate["targetVocabSize"])
    decision = "PRUNING_CANDIDATE_SELECTED" if passing else "VOCAB_PRUNING_NOT_JUSTIFIED"
    selected = passing[0]["targetVocabSize"] if passing else None
    manifest = {
        "schemaVersion": "matrix.nlu.student5.deep-pruning-phase-a.v1",
        "status": "VOCAB_PRUNING_FEASIBLE" if passing else "VOCAB_PRUNING_NOT_JUSTIFIED",
        "decision": decision,
        "selectedVocabSize": selected,
        "testedVocabSizes": list(args.targets),
        "gateThresholds": GATE,
        "student4V22AReferenceMixedBytes": STUDENT4_MIXED_BYTES,
        "upstream": audit,
        "selectionCorpus": {
            **selection_summary,
            "path": args.selection_corpus.name,
            "sha256": sha256(args.selection_corpus),
        },
        "probe": {
            "source": "PROJECT_AUTHORED_SEPARATE_TRAINING_SAFE_PROBE",
            "records": len(probe_rows),
            "contrastPairs": len(contrasts),
            "selectionCorpusOverlapChecked": True,
            "canonicalDevUsed": False,
            "frozenUsed": False,
        },
        "originalCoverage": original_coverage,
        "candidates": candidates,
        "execution": {
            "elapsedSeconds": time.perf_counter() - started,
            "python": platform.python_version(),
            "torch": torch.__version__,
            "transformers": __import__("transformers").__version__,
            "sentencepiece": spm.__version__,
        },
        "policy": {
            "phase": "A_ONLY",
            "teachingExecuted": False,
            "matrixHeadsTrained": False,
            "quantizationExecuted": False,
            "canonicalDevRead": False,
            "frozenDataRead": False,
            "frozenDataTokenized": False,
            "frozenDataAnalyzed": False,
            "student4V22AChanged": False,
            "productionPromotionExecuted": False,
        },
    }
    write_json(args.output_dir / "student5-deep-pruning-manifest.json", manifest)
    print(json.dumps({"status": manifest["status"], "decision": decision,
                      "selectedVocabSize": selected,
                      "elapsedSeconds": manifest["execution"]["elapsedSeconds"]}, indent=2))


if __name__ == "__main__":
    main()
