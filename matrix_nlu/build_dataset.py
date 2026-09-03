#!/usr/bin/env python3
"""Build deterministic, disjoint Matrix-NLU supervision and frozen benchmark.

Templates exist only in this auditable lab data builder. They are never shipped
as runtime language rules. The trained encoder/heads must generalize across
split-specific template and lexicon families.
"""

from __future__ import annotations

import argparse
import dataclasses
import hashlib
import json
import pathlib
import random
from collections import Counter, defaultdict


LANGUAGES = ("it", "en", "es")
SPLITS = ("train", "dev", "test")
SEED = 810923
SCHEMA = "matrix.nlu.dataset.v1"


LEXICONS = {
    "train": {
        "name": {"it": ["Alberto", "Chiara", "Davide", "Elena"], "en": ["Albert", "Clara", "David", "Helen"], "es": ["Alberto", "Clara", "David", "Elena"]},
        "place": {"it": ["Roma", "San Vendemiano", "New York", "La Spezia"], "en": ["Rome", "San Vendemiano", "New York", "La Spezia"], "es": ["Roma", "San Vendemiano", "Nueva York", "La Spezia"]},
        "thing": {"it": ["il blu", "il jazz", "i locali affollati", "la pioggia"], "en": ["blue", "jazz", "crowded venues", "rain"], "es": ["el azul", "el jazz", "los locales llenos", "la lluvia"]},
        "role": {"it": ["cuoco", "tecnica", "docente"], "en": ["a cook", "a technician", "a teacher"], "es": ["cocinero", "técnica", "profesor"]},
    },
    "dev": {
        "name": {"it": ["Marco", "Sofia"], "en": ["Mark", "Sophia"], "es": ["Marco", "Sofía"]},
        "place": {"it": ["Bologna", "Café Central", "Porto"], "en": ["Bologna", "Café Central", "Porto"], "es": ["Bolonia", "Café Central", "Oporto"]},
        "thing": {"it": ["il verde", "le code lunghe", "il teatro"], "en": ["green", "long queues", "theatre"], "es": ["el verde", "las colas largas", "el teatro"]},
        "role": {"it": ["infermiera", "guida"], "en": ["a nurse", "a guide"], "es": ["enfermera", "guía"]},
    },
    "test": {
        "name": {"it": ["Nadia", "Pietro", "Lucía"], "en": ["Nadia", "Peter", "Lucia"], "es": ["Nadia", "Pedro", "Lucía"]},
        "place": {"it": ["Monte Carlo", "Buenos Aires", "San Sebastián", "Castel San Pietro"], "en": ["Monte Carlo", "Buenos Aires", "San Sebastian", "Castel San Pietro"], "es": ["Montecarlo", "Buenos Aires", "San Sebastián", "Castel San Pietro"]},
        "thing": {"it": ["le stanze rumorose", "il tè alla menta", "le luci forti"], "en": ["noisy rooms", "mint tea", "bright lights"], "es": ["las habitaciones ruidosas", "el té de menta", "las luces fuertes"]},
        "role": {"it": ["restauratrice", "astronomo"], "en": ["a restorer", "an astronomer"], "es": ["restauradora", "astrónomo"]},
    },
}


TEMPLATES = {
    "train": {
        "name": {"it": "mi chiamo {object}", "en": "my name is {object}", "es": "me llamo {object}"},
        "age": {"it": "ho {object} anni", "en": "I am {object} years old", "es": "tengo {object} años"},
        "residence": {"it": "vivo a {object}", "en": "I live in {object}", "es": "vivo en {object}"},
        "like": {"it": "amo {object}", "en": "I love {object}", "es": "amo {object}"},
        "dislike": {"it": "non amo {object}", "en": "I do not like {object}", "es": "no me gusta {object}"},
        "work": {"it": "{subject} lavora come {object}", "en": "{subject} works as {object}", "es": "{subject} trabaja como {object}"},
        "future_goal": {"it": "domani vorrei visitare {object}", "en": "tomorrow I would like to visit {object}", "es": "mañana me gustaría visitar {object}"},
        "hypothesis": {"it": "forse {subject} vive a {object}", "en": "maybe {subject} lives in {object}", "es": "quizá {subject} vive en {object}"},
        "question": {"it": "dove vive {subject}?", "en": "where does {subject} live?", "es": "¿dónde vive {subject}?"},
    },
    "dev": {
        "name": {"it": "il mio nome è {object}", "en": "people call me {object}", "es": "mi nombre es {object}"},
        "age": {"it": "la mia età è {object}", "en": "my age is {object}", "es": "mi edad es {object}"},
        "residence": {"it": "abito in zona {object}", "en": "my home is in {object}", "es": "resido en {object}"},
        "like": {"it": "mi piace davvero {object}", "en": "I really enjoy {object}", "es": "disfruto mucho {object}"},
        "dislike": {"it": "detesto {object}", "en": "I dislike {object}", "es": "detesto {object}"},
        "work": {"it": "{subject} fa la professione di {object}", "en": "{subject} has a job as {object}", "es": "{subject} tiene el oficio de {object}"},
        "future_goal": {"it": "più avanti voglio andare a {object}", "en": "later I want to go to {object}", "es": "más adelante quiero ir a {object}"},
        "hypothesis": {"it": "può darsi che {subject} abiti a {object}", "en": "perhaps {subject} resides in {object}", "es": "puede que {subject} resida en {object}"},
        "question": {"it": "in quale città abita {subject}?", "en": "which city is {subject} based in?", "es": "¿en qué ciudad reside {subject}?"},
    },
    "test": {
        "name": {"it": "per presentarmi: sono {object}", "en": "to introduce myself, I'm {object}", "es": "para presentarme, soy {object}"},
        "age": {"it": "sono arrivato a {object} anni", "en": "I've reached the age of {object}", "es": "he cumplido {object} años"},
        "residence": {"it": "casa mia si trova a {object}", "en": "I make my home in {object}", "es": "tengo mi hogar en {object}"},
        "like": {"it": "quanto mi entusiasma {object}", "en": "I'm fond of {object}", "es": "me encanta {object}"},
        "dislike": {"it": "{object} proprio non fa per me", "en": "{object} is really not for me", "es": "{object} definitivamente no es para mí"},
        "work": {"it": "di mestiere {subject} è {object}", "en": "professionally, {subject} is {object}", "es": "de profesión, {subject} es {object}"},
        "future_goal": {"it": "ho in programma di raggiungere {object}", "en": "I plan on travelling to {object}", "es": "planeo viajar hasta {object}"},
        "hypothesis": {"it": "non escludo che {subject} risieda a {object}", "en": "it could be that {subject} calls {object} home", "es": "no descarto que {subject} tenga casa en {object}"},
        "question": {"it": "qual è il posto in cui risiede {subject}?", "en": "what place does {subject} call home?", "es": "¿qué lugar considera {subject} su hogar?"},
    },
}


# Project-authored TRAIN-only paraphrases.  Dev and frozen-test surfaces remain
# byte-stable and are never copied into this bank.  These are supervision data,
# not runtime language rules.
TRAIN_PARAPHRASES = {
    "name": {
        "it": ("mi chiamo {object}", "per gli amici sono {object}",
               "puoi chiamarmi {object}", "mi presento come {object}",
               "il nome che uso è {object}"),
        "en": ("my name is {object}", "friends know me as {object}",
               "you can call me {object}", "I introduce myself as {object}",
               "the name I use is {object}"),
        "es": ("me llamo {object}", "mis amigos me conocen como {object}",
               "puedes llamarme {object}", "me presento como {object}",
               "el nombre que uso es {object}"),
    },
    "age": {
        "it": ("ho {object} anni", "i miei anni sono {object}",
               "compio {object} anni", "sono una persona di {object} anni",
               "la mia età anagrafica ammonta a {object}"),
        "en": ("I am {object} years old", "I have lived for {object} years",
               "I turn {object}", "I am a {object}-year-old person",
               "my current age amounts to {object}"),
        "es": ("tengo {object} años", "mis años son {object}",
               "cumplo {object} años", "soy una persona de {object} años",
               "mi edad actual asciende a {object}"),
    },
    "residence": {
        "it": ("vivo a {object}", "risiedo nei pressi di {object}",
               "la mia residenza si trova a {object}", "casa mia è a {object}",
               "sono residente a {object}"),
        "en": ("I live in {object}", "I reside near {object}",
               "my residence is located in {object}", "my house is in {object}",
               "I am resident in {object}"),
        "es": ("vivo en {object}", "resido cerca de {object}",
               "mi residencia está en {object}", "mi casa está en {object}",
               "soy residente en {object}"),
    },
    "like": {
        "it": ("amo {object}", "adoro {object}", "apprezzo molto {object}",
               "{object} mi piace", "ho una preferenza per {object}"),
        "en": ("I love {object}", "I adore {object}", "I greatly appreciate {object}",
               "{object} appeals to me", "I have a preference for {object}"),
        "es": ("amo {object}", "adoro {object}", "aprecio mucho {object}",
               "{object} me gusta", "tengo preferencia por {object}"),
    },
    "dislike": {
        "it": ("non amo {object}", "odio {object}", "non sopporto {object}",
               "{object} non mi piace", "evito volentieri {object}"),
        "en": ("I do not like {object}", "I hate {object}", "I cannot stand {object}",
               "{object} does not appeal to me", "I prefer to avoid {object}"),
        "es": ("no me gusta {object}", "odio {object}", "no soporto {object}",
               "{object} no me agrada", "prefiero evitar {object}"),
    },
    "work": {
        "it": ("{subject} lavora come {object}", "{subject} di mestiere fa {object}",
               "{subject} è impiegato come {object}", "il lavoro di {subject} è {object}",
               "{subject} svolge il ruolo di {object}"),
        "en": ("{subject} works as {object}", "{subject} earns a living as {object}",
               "{subject} is employed as {object}", "{subject}'s occupation is {object}",
               "{subject} performs the role of {object}"),
        "es": ("{subject} trabaja como {object}", "{subject} se gana la vida como {object}",
               "{subject} está empleado como {object}", "el trabajo de {subject} es {object}",
               "{subject} desempeña el papel de {object}"),
    },
    "future_goal": {
        "it": ("domani vorrei visitare {object}", "in futuro desidero raggiungere {object}",
               "ho intenzione di recarmi a {object}", "prevedo di visitare {object}",
               "il mio obiettivo è andare a {object}"),
        "en": ("tomorrow I would like to visit {object}", "in future I want to reach {object}",
               "I intend to travel to {object}", "I expect to visit {object}",
               "my goal is to go to {object}"),
        "es": ("mañana me gustaría visitar {object}", "en el futuro deseo llegar a {object}",
               "tengo intención de ir a {object}", "preveo visitar {object}",
               "mi objetivo es ir a {object}"),
    },
    "hypothesis": {
        "it": ("forse {subject} vive a {object}", "probabilmente {subject} risiede a {object}",
               "immagino che {subject} viva a {object}", "{subject} potrebbe abitare a {object}",
               "è possibile che {subject} abbia casa a {object}"),
        "en": ("maybe {subject} lives in {object}", "probably {subject} resides in {object}",
               "I imagine {subject} lives in {object}", "{subject} might dwell in {object}",
               "it is possible that {subject} has a home in {object}"),
        "es": ("quizá {subject} vive en {object}", "probablemente {subject} reside en {object}",
               "imagino que {subject} vive en {object}", "{subject} podría vivir en {object}",
               "es posible que {subject} tenga casa en {object}"),
    },
    "question": {
        "it": ("dove vive {subject}?", "qual è la residenza di {subject}?",
               "sai dove abita {subject}?", "in che luogo risiede {subject}?",
               "dove ha casa {subject}?"),
        "en": ("where does {subject} live?", "what is {subject}'s residence?",
               "do you know where {subject} lives?", "in what place does {subject} reside?",
               "where is {subject}'s home?"),
        "es": ("¿dónde vive {subject}?", "¿cuál es la residencia de {subject}?",
               "¿sabes dónde vive {subject}?", "¿en qué lugar reside {subject}?",
               "¿dónde tiene casa {subject}?"),
    },
}


@dataclasses.dataclass(frozen=True)
class RenderedClaim:
    text: str
    labels: dict
    spans: dict
    family: str
    adult_only: bool = False


def span_of(text: str, value: str | None) -> list[int] | None:
    if not value:
        return None
    start = text.index(value)
    return [start, start + len(value)]


def make_claim(split: str, language: str, family: str, *, object_value: str = "",
               subject_value: str = "", context_subject: str = "SPEAKER",
               variant: int = 0) -> RenderedClaim:
    template = (TRAIN_PARAPHRASES[family][language][
        variant % len(TRAIN_PARAPHRASES[family][language])]
        if split == "train" else TEMPLATES[split][family][language])
    text = template.format(object=object_value, subject=subject_value)
    predicate = {
        "name": "identity.name", "age": "identity.age",
        "residence": "residence.place", "like": "preference.like",
        "dislike": "preference.like", "work": "work.role",
        "future_goal": "goal.object", "hypothesis": "residence.place",
        "question": "residence.place",
    }[family]
    act = "HYPOTHESIS" if family == "hypothesis" else "QUESTION" if family == "question" else "ASSERT"
    polarity = "UNKNOWN" if family == "question" else "NEGATIVE" if family == "dislike" else "POSITIVE"
    temporal = "FUTURE" if family == "future_goal" else "ATEMPORAL" if family in {"name", "like", "dislike"} else "CURRENT"
    kind = "HYPOTHESIS" if family == "hypothesis" else "EXPLICIT"
    entity_type = "LOCATION" if family in {"residence", "future_goal", "hypothesis"} else "PERSON" if family in {"name", "work", "question"} else None
    entity_value = object_value if entity_type == "LOCATION" else subject_value if family in {"work", "question"} else object_value if family == "name" else None
    negation_value = {
        "it": "non" if "non" in text.lower() else None,
        "en": "not" if "not" in text.lower() else None,
        "es": "no" if " no " in f" {text.lower()} " else None,
    }[language]
    temporal_value = {
        "it": "domani" if "domani" in text else None,
        "en": "tomorrow" if "tomorrow" in text else None,
        "es": "mañana" if "mañana" in text else None,
    }[language]
    labels = {
        "dialogueAct": act, "predicate": predicate, "subjectReferent": context_subject,
        "targetReferent": "SELF" if act == "REQUEST" else "NONE",
        "ownerReferent": "SUBJECT", "perspectiveReferent": "SPEAKER",
        "polarity": polarity, "temporalRelation": temporal, "claimKind": kind,
        "worldTruth": False,
    }
    spans = {
        "source": [0, len(text)], "object": span_of(text, object_value),
        "subject": span_of(text, subject_value), "negation": span_of(text.lower(), negation_value),
        "temporal": span_of(text, temporal_value),
        "entities": [] if not entity_type or not entity_value else [{
            "span": span_of(text, entity_value), "type": entity_type,
            "referent": context_subject if entity_type == "PERSON" else "LOCATION",
        }],
    }
    return RenderedClaim(text, labels, spans, family)


def adult_claim(language: str, grant: bool, split: str) -> RenderedClaim:
    variants = {
        "train": {
            "it": ("acconsento a essere baciato", "non acconsento a essere toccato"),
            "en": ("I consent to being kissed", "I do not consent to being touched"),
            "es": ("consiento que me besen", "no consiento que me toquen"),
        },
        "dev": {
            "it": ("questo bacio mi sta bene", "preferisco che tu non mi tocchi"),
            "en": ("this kiss is okay with me", "I prefer that you do not touch me"),
            "es": ("este beso me parece bien", "prefiero que no me toques"),
        },
        "test": {
            "it": ("hai il mio consenso per baciarmi", "fermati, non voglio contatto fisico"),
            "en": ("you have my consent to kiss me", "stop, I don't want physical contact"),
            "es": ("tienes mi consentimiento para besarme", "para, no quiero contacto físico"),
        },
    }
    text = variants[split][language][0 if grant else 1]
    neg = None
    for marker in ("non", "not", "don't", "no"):
        if marker in text.lower().split() or marker == "don't" and marker in text.lower():
            neg = marker
            break
    labels = {
        "dialogueAct": "ASSERT", "predicate": "consent.grant" if grant else "consent.refuse",
        "subjectReferent": "SPEAKER", "targetReferent": "OBSERVER",
        "ownerReferent": "SUBJECT", "perspectiveReferent": "SPEAKER",
        "polarity": "POSITIVE" if grant else "NEGATIVE", "temporalRelation": "CURRENT",
        "claimKind": "EXPLICIT", "worldTruth": False,
    }
    spans = {"source": [0, len(text)], "object": [0, len(text)], "subject": None,
             "negation": span_of(text.lower(), neg), "temporal": None, "entities": []}
    return RenderedClaim(text, labels, spans, "adult_consent", True)


def shift_span(value, offset):
    if value is None:
        return None
    return [value[0] + offset, value[1] + offset]


def record(record_id: str, split: str, language: str, claims: list[RenderedClaim], joiner: str,
           known_entity: tuple[str, str] | None = None) -> dict:
    text = joiner.join(claim.text for claim in claims)
    offset = 0
    rendered = []
    for claim in claims:
        spans = claim.spans
        rendered.append({
            "labels": claim.labels,
            "spans": {
                "source": shift_span(spans["source"], offset),
                "object": shift_span(spans["object"], offset),
                "subject": shift_span(spans["subject"], offset),
                "negation": shift_span(spans["negation"], offset),
                "temporal": shift_span(spans["temporal"], offset),
                "entities": [{**e, "span": shift_span(e["span"], offset)} for e in spans["entities"]],
            },
            "sourceId": f"matrix-generated:{record_id}:{len(rendered)}",
            "family": claim.family,
        })
        offset += len(claim.text) + len(joiner)
    known = {} if known_entity is None else {known_entity[0]: known_entity[1]}
    return {
        "schemaVersion": SCHEMA, "id": record_id, "split": split,
        "language": language, "text": text,
        "context": {"speaker": "PLAYER", "observer": "luna", "knownEntities": known,
                    "recentEntityRefs": []},
        "claims": rendered, "adultOnly": any(x.adult_only for x in claims),
        "provenance": {"kind": "MATRIX_GENERATED", "generatorSeed": SEED,
                       "templateSplit": split, "license": "PROJECT_AUTHORED"},
    }


def recent_reference_records() -> list[dict]:
    """TRAIN-only pronoun evidence for the existing RECENT_ENTITY contract."""
    specs = {
        "it": (("lei svolge il lavoro di {role}", "work.role", "CURRENT", "EXPLICIT"),
               ("forse lei ha casa a {place}", "residence.place", "CURRENT", "HYPOTHESIS"),
               ("lei si trova ora a {place}", "presence.reported", "CURRENT", "EXPLICIT")),
        "en": (("she has an occupation as {role}", "work.role", "CURRENT", "EXPLICIT"),
               ("maybe she has a home in {place}", "residence.place", "CURRENT", "HYPOTHESIS"),
               ("she is currently present in {place}", "presence.reported", "CURRENT", "EXPLICIT")),
        "es": (("ella ejerce el oficio de {role}", "work.role", "CURRENT", "EXPLICIT"),
               ("quizá ella tiene su casa en {place}", "residence.place", "CURRENT", "HYPOTHESIS"),
               ("ella se encuentra ahora en {place}", "presence.reported", "CURRENT", "EXPLICIT")),
    }
    pronoun = {"it": "lei", "en": "she", "es": "ella"}
    output = []
    for language, patterns in specs.items():
        lex = LEXICONS["train"]
        for index in range(36):
            template, predicate, temporal, kind = patterns[index % len(patterns)]
            role = lex["role"][language][index % len(lex["role"][language])]
            place = lex["place"][language][index % len(lex["place"][language])]
            text = template.format(role=role, place=place)
            mention = pronoun[language]
            object_value = role if predicate == "work.role" else place
            entities = [{"span": span_of(text, mention), "type": "PERSON",
                         "referent": "RECENT_ENTITY"}]
            if predicate != "work.role":
                entities.append({"span": span_of(text, place), "type": "LOCATION",
                                 "referent": "LOCATION"})
            claim = {"labels": {
                "dialogueAct": "HYPOTHESIS" if kind == "HYPOTHESIS" else "ASSERT",
                "predicate": predicate, "subjectReferent": "RECENT_ENTITY",
                "targetReferent": "NONE", "ownerReferent": "SUBJECT",
                "perspectiveReferent": "SPEAKER", "polarity": "POSITIVE",
                "temporalRelation": temporal, "claimKind": kind, "worldTruth": False,
            }, "spans": {"source": [0, len(text)], "object": span_of(text, object_value),
                           "subject": span_of(text, mention), "negation": None,
                           "temporal": None, "entities": entities},
                     "sourceId": f"matrix-authored:recent-{language}-{index:03d}:0",
                     "family": f"recent_{predicate}"}
            output.append({"schemaVersion": SCHEMA,
                "id": f"mx-train-{language}-recent-{index:03d}", "split": "train",
                "language": language, "text": text,
                "context": {"speaker": "PLAYER", "observer": "luna",
                            "knownEntities": {}, "recentEntityRefs": ["npc:recent"]},
                "claims": [claim], "adultOnly": False,
                "provenance": {"kind": "MATRIX_AUTHORED_TRAIN_AUGMENTATION",
                               "generatorSeed": SEED, "templateSplit": "train",
                               "license": "PROJECT_AUTHORED"}})
    return output


def build_records() -> list[dict]:
    rng = random.Random(SEED)
    counts = {"train": 700, "dev": 180, "test": 360}
    output = []
    for split in SPLITS:
        for language in LANGUAGES:
            lex = LEXICONS[split]
            singles = []
            for index in range(counts[split]):
                family = ("name", "age", "residence", "like", "dislike", "work",
                          "future_goal", "hypothesis", "question")[index % 9]
                name = lex["name"][language][index % len(lex["name"][language])]
                place = lex["place"][language][(index * 3 + 1) % len(lex["place"][language])]
                thing = lex["thing"][language][(index * 5 + 2) % len(lex["thing"][language])]
                role = lex["role"][language][(index * 7 + 1) % len(lex["role"][language])]
                obj = name if family == "name" else str(20 + index % 57) if family == "age" else place if family in {"residence", "future_goal", "hypothesis"} else thing if family in {"like", "dislike"} else role if family == "work" else ""
                subject = name if family in {"work", "hypothesis", "question"} else ""
                referent = "KNOWN_ENTITY" if subject else "SPEAKER"
                claim = make_claim(split, language, family, object_value=obj,
                                   subject_value=subject, context_subject=referent,
                                   variant=index // 9)
                known = (subject, f"npc:{index % len(lex['name'][language])}") if subject else None
                rid = f"mx-{split}-{language}-{index:05d}"
                singles.append((claim, known, rid))
                output.append(record(rid, split, language, [claim], "", known))

            # Multi-claim observations use separately generated facts and a
            # split-specific joiner. No full multi-claim surface appears across splits.
            joiners = {"train": {"it": (" e ", "; in più ", ". Inoltre ", "; poi "),
                                  "en": (" and ", "; moreover ", ". Additionally ", "; then "),
                                  "es": (" y ", "; también ", ". Asimismo ", "; luego ")},
                       "dev": {"it": "; inoltre ", "en": "; also ", "es": "; además "},
                       "test": {"it": ", però ", "en": ", while ", "es": ", aunque "}}
            multi_count = counts[split] // 3
            candidates = [x for x in singles if x[1] is None]
            for index in range(multi_count):
                width = 3 if index % 5 == 0 else 2
                chosen = [candidates[(index * 11 + j * 37) % len(candidates)][0] for j in range(width)]
                rid = f"mx-{split}-{language}-multi-{index:04d}"
                joiner = joiners[split][language]
                if isinstance(joiner, tuple):
                    joiner = joiner[index % len(joiner)]
                output.append(record(rid, split, language, chosen, joiner))

            for index in range(max(12, counts[split] // 25)):
                claim = adult_claim(language, index % 2 == 0, split)
                rid = f"mx-{split}-{language}-adult-{index:04d}"
                output.append(record(rid, split, language, [claim], ""))

    output.extend(recent_reference_records())
    rng.shuffle(output)
    return output


def find_span(text: str, value: str | None) -> list[int] | None:
    if not value:
        return None
    start = text.casefold().find(value.casefold())
    if start < 0:
        raise ValueError(f"cannot locate {value!r} in {text!r}")
    return [start, start + len(value)]


def optional_span(text: str, value: str | None) -> list[int] | None:
    if not value:
        return None
    start = text.casefold().find(value.casefold())
    return None if start < 0 else [start, start + len(value)]


def referent(value: str | None, context: dict, *, owner_subject: str | None = None) -> str:
    if value is None:
        return "NONE"
    if owner_subject is not None and value == owner_subject:
        return "SUBJECT"
    if value in {"SELF", context["speaker"]}:
        return "SPEAKER" if value != "SELF" else "SELF"
    if value == context["observer"]:
        return "OBSERVER"
    if value in context["knownEntities"].values():
        return "KNOWN_ENTITY"
    if value in context["recentEntityRefs"]:
        return "RECENT_ENTITY"
    return "UNKNOWN"


def load_p05(path: pathlib.Path) -> list[dict]:
    """Adapt frozen P0.5 gold without changing or copying its test into train."""
    root = json.loads(path.read_text(encoding="utf-8"))
    if root["schemaVersion"] != "p0.gold.v1":
        raise ValueError("unsupported P0.5 schema")
    output = []
    for scenario in root["scenarios"]:
        for language in LANGUAGES:
            text = scenario["variants"][language]
            context = scenario["context"]
            claims = []
            for index, source_claim in enumerate(scenario["claims"]):
                local = source_claim["localized"][language]
                source_text = local["sourceText"]
                source = find_span(text, source_text)
                entities = []
                for entity in local.get("entities", []):
                    link = entity["link"]
                    entity_ref = "LOCATION" if entity["type"] == "LOCATION" else referent(link, context)
                    entities.append({"span": find_span(text, entity["mention"]),
                                     "type": entity["type"], "referent": entity_ref})
                subject = source_claim["subject"]
                labels = {
                    "dialogueAct": source_claim["dialogueAct"],
                    "predicate": source_claim["predicate"],
                    "subjectReferent": referent(subject, context),
                    "targetReferent": referent(source_claim.get("target"), context),
                    "ownerReferent": referent(source_claim["owner"], context, owner_subject=subject),
                    "perspectiveReferent": referent(source_claim["perspective"], context),
                    "polarity": source_claim["polarity"],
                    "temporalRelation": source_claim["temporalRelation"],
                    "claimKind": source_claim["claimKind"], "worldTruth": False,
                }
                object_value = local.get("object")
                subject_mention = next((e["mention"] for e in local.get("entities", [])
                                        if e["type"] == "PERSON" and e["link"] == subject), None)
                object_span = optional_span(text, object_value)
                if object_span is None and entities:
                    # Gold objects may contain a normalized article that is
                    # contracted in the surface form (e.g. "il bar" vs "al
                    # bar"). Entity spans remain exact supervision.
                    object_span = entities[-1]["span"]
                claims.append({
                    "labels": labels,
                    "spans": {"source": source, "object": object_span,
                              "subject": find_span(text, subject_mention),
                              "negation": find_span(text, local.get("negationScope")),
                              "temporal": optional_span(text, local.get("temporalExpression")),
                              "entities": entities},
                    "sourceId": f"p05-gold:{scenario['id']}:{language}:{index}",
                    "family": "+".join(scenario["families"]),
                })
            output.append({
                "schemaVersion": SCHEMA, "id": f"p05-{scenario['id']}-{language}",
                "split": scenario["split"], "language": language, "text": text,
                "context": context, "claims": claims, "adultOnly": False,
                "provenance": {"kind": "P05_FROZEN_GOLD", "sourceScenario": scenario["id"],
                               "license": "PROJECT_AUTHORED"},
            })
    return output


def validate(records: list[dict], require_generated_coverage: bool = True) -> None:
    ids = set()
    split_templates = defaultdict(set)
    split_lexemes = defaultdict(set)
    for row in records:
        assert row["schemaVersion"] == SCHEMA
        assert row["id"] not in ids
        ids.add(row["id"])
        assert row["language"] in LANGUAGES and row["split"] in SPLITS
        assert row["claims"]
        for claim in row["claims"]:
            assert claim["labels"]["worldTruth"] is False
            split_templates[row["split"]].add(claim["family"])
            for name, span in claim["spans"].items():
                values = [entity["span"] for entity in span] if name == "entities" else [span]
                for value in values:
                    if value is None:
                        continue
                    assert 0 <= value[0] < value[1] <= len(row["text"]), (row["id"], name, value)
            source = claim["spans"]["source"]
            assert row["text"][source[0]:source[1]].strip()
        if row["adultOnly"]:
            lower = row["text"].lower()
            assert not any(term in lower for term in ("minor", "minore", "menor", "child", "bambin", "niñ"))
    if require_generated_coverage:
        for split in SPLITS:
            assert {"name", "age", "residence", "like", "dislike", "work", "future_goal",
                    "hypothesis", "question", "adult_consent"} <= split_templates[split]


def digest(path: pathlib.Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def write(records: list[dict], output_dir: pathlib.Path, prefix: str = "matrix") -> dict:
    output_dir.mkdir(parents=True, exist_ok=True)
    files = {}
    for split in SPLITS:
        path = output_dir / f"{prefix}-{split}.jsonl"
        rows = sorted((r for r in records if r["split"] == split), key=lambda x: x["id"])
        path.write_text("".join(json.dumps(r, ensure_ascii=False, sort_keys=True) + "\n" for r in rows), encoding="utf-8")
        files[split] = {"path": str(path), "records": len(rows), "sha256": digest(path),
                        "languages": dict(Counter(r["language"] for r in rows)),
                        "claims": sum(len(r["claims"]) for r in rows)}
    manifest = {
        "schemaVersion": "matrix.nlu.dataset-manifest.v1", "seed": SEED,
        "generator": "matrix_nlu/build_dataset.py", "prefix": prefix, "files": files,
        "separation": "template families and lexicon values are split-specific; frozen test is evaluation-only",
        "worldTruthExpected": 0,
    }
    manifest_path = output_dir / f"{prefix}-manifest.json"
    manifest_path.write_text(json.dumps(manifest, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    return manifest


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--output-dir", type=pathlib.Path, default=pathlib.Path("build/matrix-nlu/data"))
    parser.add_argument("--p05-gold", type=pathlib.Path, default=pathlib.Path("gold/p05-gold-v1.json"))
    args = parser.parse_args()
    rows = build_records()
    validate(rows)
    matrix_manifest = write(rows, args.output_dir)
    p05 = load_p05(args.p05_gold)
    validate(p05, require_generated_coverage=False)
    p05_manifest = write(p05, args.output_dir, "p05")
    print(json.dumps({"matrix": matrix_manifest, "p05": p05_manifest}, indent=2))


if __name__ == "__main__":
    main()
