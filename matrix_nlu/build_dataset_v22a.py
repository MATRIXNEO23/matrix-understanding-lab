#!/usr/bin/env python3
"""Build Student-4-v2.2A data.

The immutable v2 Matrix/P0.5 train/dev/test files stay compatible with the
existing v2 audit.  The actual v2.2A repair examples are emitted as a separate
TRAIN-ONLY auxiliary file consumed only by ``train_v22a.py``.

Final repair contract approved for v2.2A:
- IT core: 139
- ES core: 70
- EN core: 69
- Adult/intimacy IT: 60
- Cross-lingual contrast: 37
- Total: 375 train-only examples

No dev/frozen rows are modified here.  No adult/safety/censorship labels are
introduced: intimate/adult language is mapped to ordinary Matrix semantics such
as REQUEST, ASSERT, goal.object, consent.grant, consent.refuse or
speech.unresolved.
"""

from __future__ import annotations

import argparse
import hashlib
import json
import pathlib
from collections import Counter
from itertools import cycle

import build_dataset_v2 as v2

SCHEMA = v2.SCHEMA
REPAIR_SCHEMA = "matrix.nlu.dataset.v2.2a.repair.v2"
REPAIR_FILE = "v22a-repair-train.jsonl"
REPAIR_MANIFEST = "v22a-repair-train-manifest.json"
TARGET_COUNTS = {
    "it_core": 139,
    "es_core": 70,
    "en_core": 69,
    "adult_intimacy_it": 60,
    "cross_lingual": 37,
}

PEOPLE = ["Marco", "Giulia", "Luca", "Sara", "Nico", "Elena", "Marta", "Paolo"]
PLACES_IT = ["Roma", "Milano", "Torino", "Padova", "Napoli", "Bari", "Treviso", "Verona"]
PLACES_ES = ["Roma", "Madrid", "Bilbao", "Sevilla", "Toledo", "Murcia", "Valencia", "Granada"]
PLACES_EN = ["Rome", "London", "Bristol", "Oxford", "Leeds", "York", "Dublin", "Brighton"]
ROLES_IT = ["medico", "meccanico", "barista", "programmatore", "insegnante", "cuoco", "fotografo"]
ROLES_ES = ["médico", "mecánico", "camarero", "programador", "profesor", "cocinero", "fotógrafo"]
ROLES_EN = ["doctor", "mechanic", "barista", "developer", "teacher", "cook", "photographer"]
ITEMS_IT = ["una macchina", "un telefono", "una moto", "un appartamento", "un cane", "una chiave"]
ITEMS_ES = ["un coche", "un teléfono", "una moto", "un piso", "un perro", "una llave"]
ITEMS_EN = ["a car", "a phone", "a motorbike", "an apartment", "a dog", "a key"]
ACTIONS_IT = ["uscire con Marco", "andare al bar", "vedere Luna", "parlare con Giulia", "restare qui", "venire a casa"]
ACTIONS_ES = ["salir con Marco", "ir al bar", "ver a Luna", "hablar con Giulia", "quedarme aquí", "venir a casa"]
ACTIONS_EN = ["go to the bar", "see Luna", "talk to Giulia", "stay here", "come home", "meet Marco"]
ADULT_ACTIONS_IT = [
    "baciarti", "toccarti", "abbracciarti", "fare sesso con te", "spogliarmi con te",
    "stare nudo con te", "fare qualcosa di intimo", "provare qualcosa di più spinto",
    "fare petting", "fare dirty talk", "toccare il tuo corpo", "dormire nudo con te",
]
EN_TERMS_IN_IT = ["sex", "kiss", "dirty talk", "roleplay", "petting", "strip", "hot chat", "blowjob", "handjob", "flirt", "teasing"]
ATTR_IT = ["geloso", "arrabbiato", "sicuro", "pronto", "interessato", "confuso"]
ATTR_ES = ["celoso", "enfadado", "seguro", "listo", "interesado", "confundido"]
ATTR_EN = ["jealous", "angry", "sure", "ready", "interested", "confused"]


def sha256(path: pathlib.Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def _span(text: str, surface: str | None) -> list[int] | None:
    if surface is None:
        return None
    start = text.index(surface)
    return [start, start + len(surface)]


def _entities(text: str, people=(), locations=()) -> list[dict]:
    out = []
    for value in people:
        out.append({"span": _span(text, value), "type": "PERSON", "referent": "PERSON"})
    for value in locations:
        out.append({"span": _span(text, value), "type": "LOCATION", "referent": "LOCATION"})
    return sorted(out, key=lambda e: (e["span"][0], e["type"]))


def _context(people=(), locations=()) -> dict:
    known = {p: {"type": "PERSON"} for p in people}
    known.update({p: {"type": "LOCATION"} for p in locations})
    return {"speaker": "PLAYER", "observer": "luna", "knownEntities": known, "recentEntityRefs": []}


def row(block: str, idx: int, language: str, text: str, dialogue: str, predicate: str,
        subject: str, obj: str | None = None, *, target: str = "NONE",
        owner: str = "SUBJECT", perspective: str = "SPEAKER", polarity: str = "POSITIVE",
        temporal: str = "CURRENT", subject_text: str | None = None,
        temporal_text: str | None = None, people=(), locations=(), adult: bool = False,
        family: str | None = None) -> dict:
    source = [0, len(text)]
    claim = {
        "labels": {
            "dialogueAct": dialogue,
            "predicate": predicate,
            "subjectReferent": subject,
            "targetReferent": target,
            "ownerReferent": owner,
            "perspectiveReferent": perspective,
            "polarity": polarity,
            "temporalRelation": temporal,
            "claimKind": "EXPLICIT",
            "worldTruth": False,
        },
        "spans": {
            "source": source,
            "object": _span(text, obj),
            "subject": _span(text, subject_text),
            "negation": list(source) if polarity == "NEGATIVE" else None,
            "temporal": _span(text, temporal_text),
            "entities": _entities(text, people=people, locations=locations),
        },
        "sourceId": f"matrix-v22a-repair:{block}:{idx}:0",
        "family": family or f"v22a_{block}",
        "annotationPolicy": {
            "version": SCHEMA,
            "negationSurface": "SEMANTIC_SCOPE" if polarity == "NEGATIVE" else "NONE",
            "subjectSurface": "IMPLICIT" if subject == "SPEAKER" else ("EXPLICIT" if subject_text else "NONE"),
            "temporalSurface": "EXPLICIT" if temporal_text else ("IMPLICIT" if temporal != "ATEMPORAL" else "NONE"),
            "temporalExpression": temporal_text,
        },
    }
    return {
        "schemaVersion": SCHEMA,
        "id": f"mx-v22a-{block}-{idx:03d}",
        "split": "train",
        "language": language,
        "text": text,
        "context": _context(people=people, locations=locations),
        "claims": [claim],
        "adultOnly": adult,
        "provenance": {
            "kind": "MATRIX_AUTHORED_V2_AUGMENTATION",
            "createdInVersion": SCHEMA,
            "parentSchema": "matrix.nlu.dataset.v1",
            "migrationPolicy": "SUPERVISOR_OPTION_A",
            "annotationContract": SCHEMA,
            "repairContract": REPAIR_SCHEMA,
            "leakageFamily": f"matrix:train:v22a:{block}:{idx:03d}",
            "generatorSeed": 810924,
            "license": "PROJECT_AUTHORED",
        },
    }


def build_it_core() -> list[dict]:
    rows = []
    specs = []
    for n, place, role, item, action, attr in zip(cycle(PEOPLE), cycle(PLACES_IT), cycle(ROLES_IT), cycle(ITEMS_IT), cycle(ACTIONS_IT), cycle(ATTR_IT)):
        k = len(specs)
        if k >= 139:
            break
        if k < 63:
            pattern = k % 6
            if pattern == 0: specs.append((f"Non mi piace {n} oggi", "preference.like", "SPEAKER", n, "KNOWN_ENTITY", None, (), (n,), ()))
            elif pattern == 1: specs.append((f"Non vivo più vicino a {place} adesso", "residence.place", "SPEAKER", place, "NONE", None, (), (), (place,)))
            elif pattern == 2: specs.append((f"{n} non lavora come {role} in questo periodo", "work.role", "KNOWN_ENTITY", role, "NONE", n, (), (n,), ()))
            elif pattern == 3: specs.append((f"{n} non vuole {action} domani", "goal.object", "KNOWN_ENTITY", action, "NONE", n, (), tuple(x for x in PEOPLE if x in action or x == n), ()))
            elif pattern == 4: specs.append((f"Non sono {attr} con Luna ora", "attribute.is", "SPEAKER", attr, "OBSERVER", None, (), ("Luna",), ()))
            else: specs.append((f"Non ho {item} con me", "possession.has", "SPEAKER", item, "NONE", None, (), (), ()))
        elif k < 91:
            pattern = k % 5
            if pattern == 0: specs.append((f"Lavoro come {role} da poco", "work.role", "SPEAKER", role, "NONE", None, (), (), ()))
            elif pattern == 1: specs.append((f"Ho {item} a casa", "possession.has", "SPEAKER", item, "NONE", None, (), (), ()))
            elif pattern == 2: specs.append((f"Voglio {action} più tardi", "goal.object", "SPEAKER", action, "NONE", None, (), tuple(p for p in PEOPLE if p in action), ()))
            elif pattern == 3: specs.append((f"Mi chiamo Alberto variante {k}", "identity.name", "SPEAKER", "Alberto", "NONE", None, (), (), ()))
            else: specs.append((f"Sono una persona {attr} oggi", "attribute.is", "SPEAKER", attr, "NONE", None, (), (), ()))
        elif k < 113:
            specs.append((f"Non è mio, è di {n} davvero", "possession.has", "KNOWN_ENTITY", "mio", "NONE", None, (), (n,), ()))
        elif k < 128:
            if k % 2 == 0: specs.append((f"Ti sto chiedendo se vuoi {action}, non dicendo che vieni", "goal.object", "OBSERVER", action, "SPEAKER", None, (), tuple(p for p in PEOPLE if p in action), ()))
            else: specs.append((f"{n} dice che non vuole {action}", "goal.object", "KNOWN_ENTITY", action, "NONE", n, (), tuple(set([n] + [p for p in PEOPLE if p in action])), ()))
        else:
            specs.append((f"Da ieri non voglio {action}", "goal.object", "SPEAKER", action, "NONE", None, ("Da ieri", "PAST"), tuple(p for p in PEOPLE if p in action), ()))
    for i, (text, pred, subj, obj, target, subj_text, temp, people, locs) in enumerate(specs):
        temporal_text, temporal_rel = (temp if temp else (None, "CURRENT"))
        rows.append(row("it-core", i, "it", text, "ASSERT", pred, subj, obj, target=target,
                        polarity="NEGATIVE" if "non" in text.casefold() or text.startswith("Non") else "POSITIVE",
                        subject_text=subj_text, temporal=temporal_rel, temporal_text=temporal_text,
                        people=people, locations=locs, family="v22a_it_core"))
    return rows


def build_es_core() -> list[dict]:
    rows = []
    specs = []
    for n, place, role, item, action, attr in zip(cycle(PEOPLE), cycle(PLACES_ES), cycle(ROLES_ES), cycle(ITEMS_ES), cycle(ACTIONS_ES), cycle(ATTR_ES)):
        k = len(specs)
        if k >= 70: break
        if k < 46:
            pattern = k % 5
            if pattern == 0: specs.append((f"No me gusta {n} ahora", "preference.like", "SPEAKER", n, "KNOWN_ENTITY", None, (), (n,), ()))
            elif pattern == 1: specs.append((f"Ya no vivo cerca de {place}", "residence.place", "SPEAKER", place, "NONE", None, (), (), (place,)))
            elif pattern == 2: specs.append((f"{n} no trabaja como {role} hoy", "work.role", "KNOWN_ENTITY", role, "NONE", n, (), (n,), ()))
            elif pattern == 3: specs.append((f"{n} no quiere {action}", "goal.object", "KNOWN_ENTITY", action, "NONE", n, (), tuple(set([n] + [p for p in PEOPLE if p in action])), ()))
            else: specs.append((f"No estoy {attr} con Luna", "attribute.is", "SPEAKER", attr, "OBSERVER", None, (), ("Luna",), ()))
        elif k < 62:
            if k % 3 == 0: specs.append((f"Trabajo como {role} ahora", "work.role", "SPEAKER", role, "NONE", None, (), (), ()))
            elif k % 3 == 1: specs.append((f"Tengo {item} conmigo", "possession.has", "SPEAKER", item, "NONE", None, (), (), ()))
            else: specs.append((f"Quiero {action} luego", "goal.object", "SPEAKER", action, "NONE", None, (), tuple(p for p in PEOPLE if p in action), ()))
        elif k < 68:
            specs.append((f"No es mío, es de {n}", "possession.has", "KNOWN_ENTITY", "mío", "NONE", None, (), (n,), ()))
        else:
            specs.append((f"¿Quieres {action} conmigo?", "goal.object", "OBSERVER", action, "SPEAKER", None, (), tuple(p for p in PEOPLE if p in action), ()))
    for i, (text, pred, subj, obj, target, subj_text, temp, people, locs) in enumerate(specs):
        dialogue = "QUESTION" if text.startswith("¿") else "ASSERT"
        rows.append(row("es-core", i, "es", text, dialogue, pred, subj, obj, target=target,
                        polarity="NEGATIVE" if " no " in f" {text.casefold()} " or text.startswith("No") or text.startswith("Ya no") else "POSITIVE",
                        subject_text=subj_text, people=people, locations=locs, family="v22a_es_core"))
    return rows


def build_en_core() -> list[dict]:
    rows = []
    specs = []
    for n, place, role, item, action, attr in zip(cycle(PEOPLE), cycle(PLACES_EN), cycle(ROLES_EN), cycle(ITEMS_EN), cycle(ACTIONS_EN), cycle(ATTR_EN)):
        k = len(specs)
        if k >= 69: break
        if k < 38:
            pattern = k % 5
            if pattern == 0: specs.append((f"I work as a {role} now", "work.role", "SPEAKER", f"a {role}", "NONE", None, (), (), ()))
            elif pattern == 1: specs.append((f"I have {item} with me", "possession.has", "SPEAKER", item, "NONE", None, (), (), ()))
            elif pattern == 2: specs.append((f"I want to {action} later", "goal.object", "SPEAKER", action, "NONE", None, (), tuple(p for p in PEOPLE if p in action), ()))
            elif pattern == 3: specs.append((f"My name is Alberto case {k}", "identity.name", "SPEAKER", "Alberto", "NONE", None, (), (), ()))
            else: specs.append((f"I feel {attr} today", "attribute.is", "SPEAKER", attr, "NONE", None, (), (), ()))
        elif k < 50:
            specs.append((f"I like {n}, but I do not want to {action}", "preference.like", "SPEAKER", n, "KNOWN_ENTITY", None, (), tuple(set([n] + [p for p in PEOPLE if p in action])), ()))
        elif k < 60:
            specs.append((f"Do you want to {action} with me?", "goal.object", "OBSERVER", action, "SPEAKER", None, (), tuple(p for p in PEOPLE if p in action), ()))
        elif k < 67:
            specs.append((f"I do not like {n} anymore", "preference.like", "SPEAKER", n, "KNOWN_ENTITY", None, (), (n,), ()))
        else:
            specs.append((f"Tonight I can {action}", "consent.grant", "SPEAKER", action, "NONE", None, ("Tonight", "FUTURE"), tuple(p for p in PEOPLE if p in action), ()))
    for i, (text, pred, subj, obj, target, subj_text, temp, people, locs) in enumerate(specs):
        dialogue = "QUESTION" if text.endswith("?") else "ASSERT"
        temporal_text, temporal_rel = (temp if temp else (None, "CURRENT"))
        rows.append(row("en-core", i, "en", text, dialogue, pred, subj, obj, target=target,
                        polarity="NEGATIVE" if " not " in f" {text.casefold()} " else "POSITIVE",
                        subject_text=subj_text, temporal=temporal_rel, temporal_text=temporal_text,
                        people=people, locations=locs, family="v22a_en_core"))
    return rows


def build_adult_it() -> list[dict]:
    rows = []
    idx = 0
    for action in (ADULT_ACTIONS_IT * 2)[:15]:
        text = f"Vorrei {action} con te"
        rows.append(row("adult-it", idx, "it", text, "ASSERT", "goal.object", "SPEAKER", action,
                        target="OBSERVER", adult=True, family="v22a_adult_it_desire")); idx += 1
    for action in (ADULT_ACTIONS_IT * 2)[2:17]:
        text = f"Puoi {action} con me?"
        rows.append(row("adult-it", idx, "it", text, "REQUEST", "goal.object", "OBSERVER", action,
                        target="SPEAKER", adult=True, family="v22a_adult_it_request")); idx += 1
    for action in (ADULT_ACTIONS_IT * 2)[4:15]:
        text = f"Sì, mi va {action}"
        rows.append(row("adult-it", idx, "it", text, "ASSERT", "consent.grant", "SPEAKER", action,
                        target="OBSERVER", adult=True, family="v22a_adult_it_consent")); idx += 1
    refusals = ["Non voglio {a}", "Non adesso", "Non mi va", "Fermati", "Basta così", "Non voglio continuare", "Preferisco fermarmi", "Non mi sento pronto"]
    for template, action in zip(refusals, cycle(ADULT_ACTIONS_IT)):
        text = template.format(a=action)
        obj = action if "{a}" in template else None
        rows.append(row("adult-it", idx, "it", text, "ASSERT", "consent.refuse", "SPEAKER", obj,
                        target="OBSERVER", polarity="NEGATIVE", adult=True,
                        family="v22a_adult_it_refusal_boundary")); idx += 1
    for term in EN_TERMS_IN_IT[:11]:
        text = f"Voglio {term} con te"
        rows.append(row("adult-it", idx, "it", text, "ASSERT", "speech.unresolved", "SPEAKER", term,
                        target="OBSERVER", adult=True, family="v22a_adult_it_english_term")); idx += 1
    assert idx == 60, idx
    return rows


def build_cross() -> list[dict]:
    rows = []
    triplets = [
        ("Non mi piace Marco adesso", "No me gusta Marco ahora", "I do not like Marco now", "preference.like", "Marco"),
        ("Non vivo più a Roma", "Ya no vivo en Roma", "I do not live in Rome anymore", "residence.place", "Roma"),
        ("Lavoro come meccanico", "Trabajo como mecánico", "I work as a mechanic", "work.role", "meccanico"),
        ("Ho una macchina", "Tengo un coche", "I have a car", "possession.has", "una macchina"),
        ("Voglio andare al bar", "Quiero ir al bar", "I want to go to the bar", "goal.object", "andare al bar"),
        ("Non sono geloso", "No estoy celoso", "I am not jealous", "attribute.is", "geloso"),
        ("Vieni con me?", "¿Vienes conmigo?", "Are you coming with me?", "goal.object", "Vieni"),
        ("No, non voglio", "No, no quiero", "No, I do not want to", "consent.refuse", None),
        ("Sì, mi va", "Sí, me apetece", "Yes, I want to", "consent.grant", None),
        ("Non è mio", "No es mío", "It is not mine", "possession.has", "mio"),
        ("Marco non vuole uscire", "Marco no quiere salir", "Marco does not want to go out", "goal.object", "uscire"),
        ("Ti sto chiedendo di restare", "Te pido que te quedes", "I am asking you to stay", "goal.object", "restare"),
    ]
    idx = 0
    for it, es, en, pred, obj in triplets:
        for lang, text in (("it", it), ("es", es), ("en", en)):
            if idx >= 37: break
            actual_obj = obj
            if lang == "es":
                actual_obj = {"Roma":"Roma", "meccanico":"mecánico", "una macchina":"un coche", "andare al bar":"ir al bar", "geloso":"celoso", "Vieni":"Vienes", "mio":"mío", "uscire":"salir", "restare":"quedes"}.get(obj, obj)
            if lang == "en":
                actual_obj = {"Roma":"Rome", "meccanico":"mechanic", "una macchina":"a car", "andare al bar":"go to the bar", "geloso":"jealous", "Vieni":"coming", "mio":"mine", "uscire":"go out", "restare":"stay"}.get(obj, obj)
            dialogue = "QUESTION" if text.endswith("?") else "ASSERT"
            polarity = "NEGATIVE" if any(m in text.casefold() for m in ("non", " no ", "not", " no quiero", "no es")) else "POSITIVE"
            rows.append(row("cross", idx, lang, text, dialogue, pred, "SPEAKER", actual_obj,
                            polarity=polarity, family="v22a_cross_lingual_contrast"))
            idx += 1
    assert len(rows) == 36
    rows.append(row("cross", 36, "it", "Non sto affermando questo, sto facendo una domanda", "CORRECT",
                    "speech.unresolved", "SPEAKER", "questo", polarity="NEGATIVE",
                    family="v22a_cross_lingual_extra_it"))
    return rows


def build_repair_rows() -> list[dict]:
    rows = build_it_core() + build_es_core() + build_en_core() + build_adult_it() + build_cross()
    counts = Counter(r["id"].split("-")[2] for r in rows)
    if len(rows) != sum(TARGET_COUNTS.values()):
        raise RuntimeError(f"repair row count mismatch: {len(rows)}")
    return rows


def write_jsonl(rows: list[dict], path: pathlib.Path) -> None:
    path.write_text("".join(json.dumps(row, ensure_ascii=False, sort_keys=True) + "\n" for row in rows), encoding="utf-8")


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--output-dir", type=pathlib.Path, default=pathlib.Path("build/matrix-nlu/data-v22a"))
    parser.add_argument("--p05-gold", type=pathlib.Path, default=pathlib.Path("gold/p05-gold-v1.json"))
    args = parser.parse_args()
    args.output_dir.mkdir(parents=True, exist_ok=True)

    records, mapping = v2.build(args.p05_gold)
    manifests = {source: v2.write_dataset(records[source], args.output_dir, f"{source}-v2", v2.V1_HASHES[source]) for source in ("matrix", "p05")}

    repair_rows = build_repair_rows()
    repair_path = args.output_dir / REPAIR_FILE
    write_jsonl(repair_rows, repair_path)
    block_counts = Counter(row["id"].split("-", 3)[2] for row in repair_rows)
    language_counts = Counter(row["language"] for row in repair_rows)
    manifest = {
        "schemaVersion": REPAIR_SCHEMA,
        "datasetSchema": SCHEMA,
        "file": REPAIR_FILE,
        "sha256": sha256(repair_path),
        "records": len(repair_rows),
        "claims": sum(len(row["claims"]) for row in repair_rows),
        "targetCounts": TARGET_COUNTS,
        "languageCounts": dict(sorted(language_counts.items())),
        "policy": {
            "split": "train-only auxiliary",
            "devModified": False,
            "frozenModified": False,
            "frozenPredictionsRead": False,
            "adultSafetyLabels": False,
            "censorshipLabels": False,
        },
    }
    (args.output_dir / REPAIR_MANIFEST).write_text(json.dumps(manifest, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")

    mapping["v2Files"] = {source: manifests[source]["files"] for source in manifests}
    mapping["v22aRepair"] = manifest
    mapping_path = args.output_dir / "v1-to-v2-corrections.json"
    mapping_path.write_text(json.dumps(mapping, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")

    print(json.dumps({
        "schemaVersion": REPAIR_SCHEMA,
        "outputDir": str(args.output_dir),
        "baseManifests": manifests,
        "repairManifest": manifest,
        "mapping": {"path": str(mapping_path), "sha256": sha256(mapping_path)},
    }, indent=2, ensure_ascii=False))


if __name__ == "__main__":
    main()
