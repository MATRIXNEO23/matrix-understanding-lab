#!/usr/bin/env python3
"""Build the frozen P0.5 parallel semantic benchmark before mapper fixes."""

from __future__ import annotations

import copy
import hashlib
import json
import pathlib
import unicodedata

ROOT = pathlib.Path(__file__).resolve().parents[1]
LANGS = ("it", "en", "es")
SPLITS = ("train", "dev", "test")


def slug(value: str) -> str:
    normalized = "".join(
        c for c in unicodedata.normalize("NFD", value.lower())
        if unicodedata.category(c) != "Mn"
    )
    return "_".join("".join(c if c.isalnum() else " " for c in normalized).split())


def location(mentions: tuple[str, str, str], canonical: str | None = None):
    key = canonical or slug(mentions[1])
    return tuple([{"mention": m, "type": "LOCATION", "link": f"LOCATION:{key}"}] for m in mentions)


def person(mentions: tuple[str, str, str], link: str):
    return tuple([{"mention": m, "type": "PERSON", "link": link}] for m in mentions)


def merged(*entity_sets):
    return tuple(sum((list(group[i]) for group in entity_sets), []) for i in range(3))


def context(speaker="PLAYER", observer="luna", known=None, recent=None):
    return {
        "speaker": speaker,
        "observer": observer,
        "knownEntities": known or {},
        "recentEntityRefs": recent or [],
    }


def claim(predicate, objects, sources, *, speaker="PLAYER", subject="PLAYER",
          target=None, owner=None, perspective=None, act="ASSERT",
          polarity="POSITIVE", temporal=None, temporal_expression=(None, None, None),
          kind="EXPLICIT", entities=((), (), ())):
    if temporal is None:
        temporal = "ATEMPORAL" if predicate in {"identity.name", "preference.like", "speech.unresolved"} else "CURRENT"
    localized = {}
    for i, lang in enumerate(LANGS):
        item = {"object": objects[i], "sourceText": sources[i], "entities": list(entities[i])}
        if temporal_expression[i] is not None:
            item["temporalExpression"] = temporal_expression[i]
        if polarity == "NEGATIVE":
            item["negationScope"] = sources[i]
        localized[lang] = item
    return {
        "speaker": speaker,
        "subject": subject,
        "target": target,
        "owner": owner or subject,
        "perspective": perspective or speaker,
        "dialogueAct": act,
        "predicate": predicate,
        "polarity": polarity,
        "temporalRelation": temporal,
        "claimKind": kind,
        "localized": localized,
    }


EXTRAS = []


def add(families, variants, claims, ctx=None):
    number = len(EXTRAS) + 1
    EXTRAS.append({
        "id": f"P05-{number:03d}",
        "split": SPLITS[(number - 1) % len(SPLITS)],
        "families": families,
        "context": ctx or context(),
        "claims": claims,
        "variants": dict(zip(LANGS, variants)),
    })


def single(families, variants, predicate, objects, **kwargs):
    add(families, variants, [claim(predicate, objects, variants, **kwargs)], kwargs.pop("ctx", None) if "ctx" in kwargs else None)


# Preference and local negation: varied objects, articles and code-switching.
for variants, objects, polarity in [
    (("Amo il tè verde", "I love green tea", "Amo el té verde"), ("il tè verde", "green tea", "el té verde"), "POSITIVE"),
    (("Non mi piace la pioggia", "I do not like rain", "No me gusta la lluvia"), ("la pioggia", "rain", "la lluvia"), "NEGATIVE"),
    (("Odio i rumori forti", "I hate loud noises", "Odio los ruidos fuertes"), ("i rumori forti", "loud noises", "los ruidos fuertes"), "POSITIVE"),
    (("Mi piace molto il cinema", "I like cinema a lot", "Me gusta mucho el cine"), ("molto il cinema", "cinema a lot", "mucho el cine"), "POSITIVE"),
    (("Non sopporto le code lunghe", "I don't like long queues", "No me gustan las colas largas"), ("le code lunghe", "long queues", "las colas largas"), "NEGATIVE"),
    (("Mi piace la musica live", "I like musica live", "Me gusta la musica live"), ("la musica live", "musica live", "la musica live"), "POSITIVE"),
]:
    add(["preference", "negation_local" if polarity == "NEGATIVE" else "lexical_variation"], variants,
        [claim("preference.like", objects, variants, polarity=polarity)])

# Residence/presence and capitalized person/location collisions.
residence_rows = [
    (("Abito a Bologna", "I live in Bologna", "Vivo en Bolonia"), ("Bologna", "Bologna", "Bolonia"), ("Bologna", "Bologna", "Bolonia"), "bologna", "residence.place"),
    (("Vivo a New York", "I live in New York", "Vivo en Nueva York"), ("New York", "New York", "Nueva York"), ("New York", "New York", "Nueva York"), "new_york", "residence.place"),
    (("Sono alla stazione centrale", "I am at the central station", "Estoy en la estación central"), ("stazione centrale", "central station", "estación central"), ("stazione centrale", "central station", "estación central"), None, "presence.reported"),
    (("Sono al Café Central", "I am at Café Central", "Estoy en Café Central"), ("Café Central", "Café Central", "Café Central"), ("Café Central", "Café Central", "Café Central"), "cafe_central", "presence.reported"),
]
for variants, objects, mentions, canonical, predicate in residence_rows:
    add(["location", "composite_location"], variants,
        [claim(predicate, objects, variants, entities=location(mentions, canonical))])
known_marco = context(known={"Marco": "npc:marco"})
variants = ("Marco vive a Porto", "Marco lives in Porto", "Marco vive en Oporto")
add(["third_person", "person_location_collision"], variants,
    [claim("residence.place", ("Porto", "Porto", "Oporto"), variants, subject="npc:marco",
           owner="npc:marco", entities=merged(person(("Marco", "Marco", "Marco"), "npc:marco"),
                                                location(("Porto", "Porto", "Oporto"), "porto")))], known_marco)
known_roma = context(known={"Roma": "npc:roma"})
variants = ("Roma vive a Madrid", "Roma lives in Madrid", "Roma vive en Madrid")
add(["third_person", "person_location_collision"], variants,
    [claim("residence.place", ("Madrid", "Madrid", "Madrid"), variants, subject="npc:roma",
           owner="npc:roma", entities=merged(person(("Roma", "Roma", "Roma"), "npc:roma"),
                                               location(("Madrid", "Madrid", "Madrid"), "madrid")))], known_roma)

# Identity, work, pronoun and current-NPC ownership.
for variants, predicate, objects, entities, ctx, subject in [
    (("Io mi chiamo Chiara", "My name is Clara", "Yo me llamo Clara"), "identity.name", ("Chiara", "Clara", "Clara"), person(("Chiara", "Clara", "Clara"), "PLAYER"), context(), "PLAYER"),
    (("Sono Davide", "I am David", "Soy David"), "identity.name", ("Davide", "David", "David"), person(("Davide", "David", "David"), "PLAYER"), context(), "PLAYER"),
    (("Ho 52 anni", "I am 52 years old", "Tengo 52 años"), "identity.age", ("52", "52", "52"), ((), (), ()), context(), "PLAYER"),
    (("Marco lavora come infermiere", "Marco works as a nurse", "Marco trabaja como enfermero"), "work.role", ("infermiere", "a nurse", "enfermero"), person(("Marco", "Marco", "Marco"), "npc:marco"), known_marco, "npc:marco"),
    (("Lei lavora come architetta", "She works as an architect", "Ella trabaja como arquitecta"), "work.role", ("architetta", "an architect", "arquitecta"), person(("Lei", "She", "Ella"), "npc:sofia"), context(recent=["npc:sofia"]), "npc:sofia"),
    (("Mi chiamo Luna", "My name is Luna", "Me llamo Luna"), "identity.name", ("Luna", "Luna", "Luna"), person(("Luna", "Luna", "Luna"), "luna"), context(speaker="luna", observer="npc:nia"), "luna"),
]:
    add(["ownership", "perspective", "provenance"], variants,
        [claim(predicate, objects, variants, speaker=ctx["speaker"], subject=subject,
               owner=subject, perspective=ctx["speaker"], entities=entities)], ctx)

# Twelve two-/three-claim observations. Source spans are proposition-local.
multi_rows = [
    (("Ho 30 anni e vivo a Roma", "I am 30 years old and I live in Rome", "Tengo 30 años y vivo en Roma"),
     [("identity.age", ("30", "30", "30"), ("Ho 30 anni", "I am 30 years old", "Tengo 30 años"), {}),
      ("residence.place", ("Roma", "Rome", "Roma"), ("vivo a Roma", "I live in Rome", "vivo en Roma"), {"entities": location(("Roma", "Rome", "Roma"), "rome")})]),
    (("Amo il mare e non vivo a Genova", "I love the sea and I do not live in Genoa", "Amo el mar y no vivo en Génova"),
     [("preference.like", ("il mare", "the sea", "el mar"), ("Amo il mare", "I love the sea", "Amo el mar"), {}),
      ("residence.place", ("Genova", "Genoa", "Génova"), ("non vivo a Genova", "I do not live in Genoa", "no vivo en Génova"), {"polarity": "NEGATIVE", "entities": location(("Genova", "Genoa", "Génova"), "genoa")})]),
    (("Lavoro come guida e vivo a Firenze", "I work as a guide and I live in Florence", "Trabajo como guía y vivo en Florencia"),
     [("work.role", ("guida", "a guide", "guía"), ("Lavoro come guida", "I work as a guide", "Trabajo como guía"), {}),
      ("residence.place", ("Firenze", "Florence", "Florencia"), ("vivo a Firenze", "I live in Florence", "vivo en Florencia"), {"entities": location(("Firenze", "Florence", "Florencia"), "florence")})]),
    (("Ho una bici e amo le colline", "I own a bike and I love hills", "Tengo una bici y amo las colinas"),
     [("possession.has", ("una bici", "a bike", "una bici"), ("Ho una bici", "I own a bike", "Tengo una bici"), {}),
      ("preference.like", ("le colline", "hills", "las colinas"), ("amo le colline", "I love hills", "amo las colinas"), {})]),
    (("Mi chiamo Paolo e lavoro come docente", "My name is Paul and I work as a teacher", "Me llamo Pablo y trabajo como profesor"),
     [("identity.name", ("Paolo", "Paul", "Pablo"), ("Mi chiamo Paolo", "My name is Paul", "Me llamo Pablo"), {"entities": person(("Paolo", "Paul", "Pablo"), "PLAYER")}),
      ("work.role", ("docente", "a teacher", "profesor"), ("lavoro come docente", "I work as a teacher", "trabajo como profesor"), {})]),
    (("Ho 41 anni e non amo il traffico", "I am 41 years old and I do not like traffic", "Tengo 41 años y no me gusta el tráfico"),
     [("identity.age", ("41", "41", "41"), ("Ho 41 anni", "I am 41 years old", "Tengo 41 años"), {}),
      ("preference.like", ("il traffico", "traffic", "el tráfico"), ("non amo il traffico", "I do not like traffic", "no me gusta el tráfico"), {"polarity": "NEGATIVE"})]),
    (("Ho 36 anni e vivo a Torino e amo il jazz", "I am 36 years old and I live in Turin and I love jazz", "Tengo 36 años y vivo en Turín y amo el jazz"),
     [("identity.age", ("36", "36", "36"), ("Ho 36 anni", "I am 36 years old", "Tengo 36 años"), {}),
      ("residence.place", ("Torino", "Turin", "Turín"), ("vivo a Torino", "I live in Turin", "vivo en Turín"), {"entities": location(("Torino", "Turin", "Turín"), "turin")}),
      ("preference.like", ("il jazz", "jazz", "el jazz"), ("amo il jazz", "I love jazz", "amo el jazz"), {})]),
    (("Mi chiamo Sara e lavoro come cuoca e vivo a Padova", "My name is Sarah and I work as a cook and I live in Padua", "Me llamo Sara y trabajo como cocinera y vivo en Padua"),
     [("identity.name", ("Sara", "Sarah", "Sara"), ("Mi chiamo Sara", "My name is Sarah", "Me llamo Sara"), {"entities": person(("Sara", "Sarah", "Sara"), "PLAYER")}),
      ("work.role", ("cuoca", "a cook", "cocinera"), ("lavoro come cuoca", "I work as a cook", "trabajo como cocinera"), {}),
      ("residence.place", ("Padova", "Padua", "Padua"), ("vivo a Padova", "I live in Padua", "vivo en Padua"), {"entities": location(("Padova", "Padua", "Padua"), "padua")})]),
    (("Non amo il freddo e ho un cane e vivo a Bari", "I do not like cold weather and I own a dog and I live in Bari", "No me gusta el frío y tengo un perro y vivo en Bari"),
     [("preference.like", ("il freddo", "cold weather", "el frío"), ("Non amo il freddo", "I do not like cold weather", "No me gusta el frío"), {"polarity": "NEGATIVE"}),
      ("possession.has", ("un cane", "a dog", "un perro"), ("ho un cane", "I own a dog", "tengo un perro"), {}),
      ("residence.place", ("Bari", "Bari", "Bari"), ("vivo a Bari", "I live in Bari", "vivo en Bari"), {"entities": location(("Bari", "Bari", "Bari"), "bari")})]),
    (("Lavoro come artista e amo il blu e non vivo a Pisa", "I work as an artist and I love blue and I do not live in Pisa", "Trabajo como artista y amo el azul y no vivo en Pisa"),
     [("work.role", ("artista", "an artist", "artista"), ("Lavoro come artista", "I work as an artist", "Trabajo como artista"), {}),
      ("preference.like", ("il blu", "blue", "el azul"), ("amo il blu", "I love blue", "amo el azul"), {}),
      ("residence.place", ("Pisa", "Pisa", "Pisa"), ("non vivo a Pisa", "I do not live in Pisa", "no vivo en Pisa"), {"polarity": "NEGATIVE", "entities": location(("Pisa", "Pisa", "Pisa"), "pisa")})]),
    (("Ho 28 anni e lavoro come tecnico e ho una moto", "I am 28 years old and I work as a technician and I own a motorcycle", "Tengo 28 años y trabajo como técnico y tengo una moto"),
     [("identity.age", ("28", "28", "28"), ("Ho 28 anni", "I am 28 years old", "Tengo 28 años"), {}),
      ("work.role", ("tecnico", "a technician", "técnico"), ("lavoro come tecnico", "I work as a technician", "trabajo como técnico"), {}),
      ("possession.has", ("una moto", "a motorcycle", "una moto"), ("ho una moto", "I own a motorcycle", "tengo una moto"), {})]),
    (("Mi piace il teatro e abito a Parma e ho 47 anni", "I like theatre and I live in Parma and I am 47 years old", "Me gusta el teatro y vivo en Parma y tengo 47 años"),
     [("preference.like", ("il teatro", "theatre", "el teatro"), ("Mi piace il teatro", "I like theatre", "Me gusta el teatro"), {}),
      ("residence.place", ("Parma", "Parma", "Parma"), ("abito a Parma", "I live in Parma", "vivo en Parma"), {"entities": location(("Parma", "Parma", "Parma"), "parma")}),
      ("identity.age", ("47", "47", "47"), ("ho 47 anni", "I am 47 years old", "tengo 47 años"), {})]),
]
for variants, specs in multi_rows:
    claims = [claim(pred, obj, src, **opts) for pred, obj, src, opts in specs]
    add(["multi_claim", "coordination", "mixed_types"], variants, claims)

# Corrections/supersession.
for variants, objects, mentions, marker_family in [
    (("In realtà vivo a Napoli", "Actually, I live in Naples", "En realidad vivo en Nápoles"), ("Napoli", "Naples", "Nápoles"), ("Napoli", "Naples", "Nápoles"), "correction"),
    (("Anzi, vivo a Lecce", "In fact, I live in Lecce", "De hecho vivo en Lecce"), ("Lecce", "Lecce", "Lecce"), ("Lecce", "Lecce", "Lecce"), "correction"),
    (("In realtà lavoro come sarta", "Actually, I work as a tailor", "En realidad trabajo como sastre"), ("sarta", "a tailor", "sastre"), (None, None, None), "correction"),
    (("Anzi, ho 45 anni", "In fact, I am 45 years old", "De hecho tengo 45 años"), ("45", "45", "45"), (None, None, None), "correction"),
    (("In realtà amo il verde", "Actually, I love green", "En realidad amo el verde"), ("il verde", "green", "el verde"), (None, None, None), "correction"),
    (("Anzi, mi chiamo Elena", "In fact, my name is Helen", "De hecho me llamo Elena"), ("Elena", "Helen", "Elena"), (None, None, None), "correction"),
]:
    predicate = "residence.place" if mentions[0] else ("work.role" if "lavor" in variants[0] or "work" in variants[1] else ("identity.age" if "anni" in variants[0] else ("identity.name" if "chiamo" in variants[0] else "preference.like")))
    entities = location(mentions) if mentions[0] else (person(objects, "PLAYER") if predicate == "identity.name" else ((), (), ()))
    add([marker_family, "supersession"], variants,
        [claim(predicate, objects, variants, act="CORRECT", entities=entities)])

# Future goals and past/current temporal-location co-occurrence.
temporal_rows = [
    (("Domani vorrei trasferirmi a Verona", "Tomorrow I would like to move to Verona", "Mañana me gustaría mudarme a Verona"), "goal.object", ("trasferirmi a Verona", "to move to Verona", "mudarme a Verona"), "FUTURE", ("Domani", "Tomorrow", "Mañana"), location(("Verona", "Verona", "Verona"), "verona")),
    (("Domani vorrei visitare Barcellona", "Tomorrow I would like to visit Barcelona", "Mañana me gustaría visitar Barcelona"), "goal.object", ("visitare Barcellona", "to visit Barcelona", "visitar Barcelona"), "FUTURE", ("Domani", "Tomorrow", "Mañana"), location(("Barcellona", "Barcelona", "Barcelona"), "barcelona")),
    (("Prima vivevo a Como", "I used to live in Como", "Antes vivía en Como"), "residence.place", ("Como", "Como", "Como"), "PAST", ("Prima", "Previously", "Antes"), location(("Como", "Como", "Como"), "como")),
    (("Prima abitavo a La Spezia", "Previously I lived in La Spezia", "Antes vivía en La Spezia"), "residence.place", ("La Spezia", "La Spezia", "La Spezia"), "PAST", ("Prima", "Previously", "Antes"), location(("La Spezia", "La Spezia", "La Spezia"), "la_spezia")),
    (("Domani sono a Roma", "Tomorrow I am in Rome", "Mañana estoy en Roma"), "presence.reported", ("Roma", "Rome", "Roma"), "FUTURE", ("Domani", "Tomorrow", "Mañana"), location(("Roma", "Rome", "Roma"), "rome")),
    (("Prima ero a Milano", "Previously I was in Milan", "Antes estaba en Milán"), "presence.reported", ("Milano", "Milan", "Milán"), "PAST", ("Prima", "Previously", "Antes"), location(("Milano", "Milan", "Milán"), "milan")),
]
for variants, pred, objects, relation, expressions, entities in temporal_rows:
    add(["temporality", "location_cooccurrence", "modal_goal" if pred == "goal.object" else "time_relation"], variants,
        [claim(pred, objects, variants, temporal=relation, temporal_expression=expressions, entities=entities)])

# Imperatives: independent verbs; request detection must not be a verb-list lookup.
for variants in [
    ("Chiudi la finestra", "Close the window", "Cierra la ventana"),
    ("Porta qui il libro", "Bring the book here", "Trae aquí el libro"),
    ("Aspetta un momento", "Wait a moment", "Espera un momento"),
    ("Spegni la luce", "Turn off the light", "Apaga la luz"),
    ("Mostrami la mappa", "Show me the map", "Muéstrame el mapa"),
    ("Ricorda questo nome", "Remember this name", "Recuerda este nombre"),
]:
    add(["imperative", "dialogue_act", "independent_paraphrase"], variants,
        [claim("speech.unresolved", variants, variants, target="SELF", act="REQUEST", polarity="UNKNOWN")])

# Questions and hypotheses retain speaker ownership and never become world truth.
for variants, subject, ctx, act, kind, polarity, objects, entities in [
    (("Dove vive Marco?", "Where does Marco live?", "¿Dónde vive Marco?"), "npc:marco", known_marco, "QUESTION", "EXPLICIT", "UNKNOWN", ("", "", ""), person(("Marco", "Marco", "Marco"), "npc:marco")),
    (("Dove vive Sofia?", "Where does Sofia live?", "¿Dónde vive Sofia?"), "npc:sofia", context(known={"Sofia": "npc:sofia"}), "QUESTION", "EXPLICIT", "UNKNOWN", ("", "", ""), person(("Sofia", "Sofia", "Sofia"), "npc:sofia")),
    (("Forse Marco vive a Siena", "Maybe Marco lives in Siena", "Quizá Marco vive en Siena"), "npc:marco", known_marco, "HYPOTHESIS", "HYPOTHESIS", "POSITIVE", ("Siena", "Siena", "Siena"), merged(person(("Marco", "Marco", "Marco"), "npc:marco"), location(("Siena", "Siena", "Siena"), "siena"))),
    (("Credo che Marco viva a Lucca", "I think Marco lives in Lucca", "Tal vez Marco vive en Lucca"), "npc:marco", known_marco, "HYPOTHESIS", "HYPOTHESIS", "POSITIVE", ("Lucca", "Lucca", "Lucca"), merged(person(("Marco", "Marco", "Marco"), "npc:marco"), location(("Lucca", "Lucca", "Lucca"), "lucca"))),
    (("Forse lei vive a Trento", "Perhaps she lives in Trento", "Quizás ella vive en Trento"), "npc:sofia", context(recent=["npc:sofia"]), "HYPOTHESIS", "HYPOTHESIS", "POSITIVE", ("Trento", "Trento", "Trento"), merged(person(("lei", "she", "ella"), "npc:sofia"), location(("Trento", "Trento", "Trento"), "trento"))),
    (("Dove vive lei?", "Where does she live?", "¿Dónde vive ella?"), "npc:sofia", context(recent=["npc:sofia"]), "QUESTION", "EXPLICIT", "UNKNOWN", ("", "", ""), person(("lei", "she", "ella"), "npc:sofia")),
]:
    add(["question" if act == "QUESTION" else "hypothesis", "ownership", "world_truth_guard"], variants,
        [claim("residence.place", objects, variants, subject=subject, owner=subject, act=act,
               kind=kind, polarity=polarity, entities=entities)], ctx)

# Possession, explicit unknown and colloquial/malformed inputs.
for variants, predicate, objects, families in [
    (("Ho uno zaino nero", "I own a black backpack", "Tengo una mochila negra"), "possession.has", ("uno zaino nero", "a black backpack", "una mochila negra"), ["possession"]),
    (("Ho due gatti", "I have two cats", "Tengo dos gatos"), "possession.has", ("due gatti", "two cats", "dos gatos"), ["possession", "number"]),
    (("boh forse così", "uh maybe so", "pues quizá así"), "speech.unresolved", ("boh forse così", "uh maybe so", "pues quizá así"), ["explicit_unknown", "colloquial"]),
    (("???", "???", "???"), "speech.unresolved", ("???", "???", "???"), ["explicit_unknown", "malformed"]),
    (("io 29 anni", "me 29 years old", "yo 29 años"), "identity.age", ("29", "29", "29"), ["colloquial", "imperfect_grammar"]),
    (("vivo a berlin", "i live in berlin", "vivo en berlín"), "residence.place", ("berlin", "berlin", "berlín"), ["lowercase_entity", "location"]),
]:
    entities = location(objects, "berlin") if predicate == "residence.place" else ((), (), ())
    add(families, variants, [claim(predicate, objects, variants, entities=entities)])

# Person and place in one proposition, including composite locations.
for variants, role_objects, location_mentions, canonical in [
    (("Marco lavora come guida a Roma", "Marco works as a guide in Rome", "Marco trabaja como guía en Roma"), ("guida a Roma", "a guide in Rome", "guía en Roma"), ("Roma", "Rome", "Roma"), "rome"),
    (("Marco lavora come cuoco a New York", "Marco works as a cook in New York", "Marco trabaja como cocinero en Nueva York"), ("cuoco a New York", "a cook in New York", "cocinero en Nueva York"), ("New York", "New York", "Nueva York"), "new_york"),
    (("Sofia lavora come medica a Sanremo", "Sofia works as a doctor in Sanremo", "Sofia trabaja como médica en Sanremo"), ("medica a Sanremo", "a doctor in Sanremo", "médica en Sanremo"), ("Sanremo", "Sanremo", "Sanremo"), "sanremo"),
    (("Sofia vive a Città del Messico", "Sofia lives in Mexico City", "Sofia vive en Ciudad de México"), ("Città del Messico", "Mexico City", "Ciudad de México"), ("Città del Messico", "Mexico City", "Ciudad de México"), "mexico_city"),
    (("Marco vive a San Pietro", "Marco lives in Saint Peter", "Marco vive en San Pedro"), ("San Pietro", "Saint Peter", "San Pedro"), ("San Pietro", "Saint Peter", "San Pedro"), "san_pietro"),
    (("Sofia lavora come guida a Buenos Aires", "Sofia works as a guide in Buenos Aires", "Sofia trabaja como guía en Buenos Aires"), ("guida a Buenos Aires", "a guide in Buenos Aires", "guía en Buenos Aires"), ("Buenos Aires", "Buenos Aires", "Buenos Aires"), "buenos_aires"),
]:
    name = "Sofia" if variants[0].startswith("Sofia") else "Marco"
    link = "npc:sofia" if name == "Sofia" else "npc:marco"
    ctx = context(known={name: link})
    predicate = "residence.place" if " vive " in f" {variants[0]} " else "work.role"
    entities = merged(person((name, name, name), link), location(location_mentions, canonical))
    add(["named_entities", "person_location_collision", "composite_location"], variants,
        [claim(predicate, role_objects, variants, subject=link, owner=link, entities=entities)], ctx)


def main():
    if len(EXTRAS) != 66:
        raise SystemExit(f"expected 66 new scenarios, got {len(EXTRAS)}")
    original_path = ROOT / "gold" / "p0-gold-v1.json"
    output_path = ROOT / "gold" / "p05-gold-v1.json"
    original = json.loads(original_path.read_text(encoding="utf-8"))
    output = copy.deepcopy(original)
    output["frozenAt"] = "2026-09-03T17:00:00Z"
    output["benchmarkId"] = "P0.5-expanded-v1"
    output["parentGoldSha256"] = hashlib.sha256(original_path.read_bytes()).hexdigest()
    output["rules"]["expandedBeforeMapperFixes"] = True
    output["rules"]["newScenarioCount"] = len(EXTRAS)
    output["scenarios"].extend(EXTRAS)
    rendered = json.dumps(output, ensure_ascii=False, indent=2) + "\n"
    output_path.write_text(rendered, encoding="utf-8")
    print(f"wrote {output_path} scenarios={len(output['scenarios'])} variants={len(output['scenarios']) * 3} sha256={hashlib.sha256(rendered.encode()).hexdigest()}")


if __name__ == "__main__":
    main()
