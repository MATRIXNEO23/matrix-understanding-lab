#!/usr/bin/env python3
"""Build Student-4-v2.2A train-only repair dataset.

This script preserves the immutable v2 dev/test partitions and appends only
project-authored TRAIN rows targeted at the v2.1 dev failure modes:
negation, predicate selection, claim spans, Italian ownership/referents and
question/request/report/correction separation.

It intentionally keeps ``schemaVersion == matrix.nlu.dataset.v2`` and the
``matrix-v2-*.jsonl`` filenames because the existing trainer is hard-bound to
the v2 contract when frozen access is deferred. The variant distinction lives in
``train_config_v22a.json`` and the generated mapping/manifest evidence.
"""

from __future__ import annotations

import argparse
import hashlib
import json
import pathlib
from collections import Counter

import build_dataset_v2 as v2

SCHEMA = v2.SCHEMA
REPAIR_SCHEMA = "matrix.nlu.dataset.v2.2a.repair.v1"
LANGUAGES = ("it", "en", "es")


def sha256(path: pathlib.Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def _span(text: str, surface: str | None) -> list[int] | None:
    if surface is None:
        return None
    start = text.index(surface)
    return [start, start + len(surface)]


def _entities(text: str, people: tuple[str, ...] = (), locations: tuple[str, ...] = ()) -> list[dict]:
    entities: list[dict] = []
    for person in people:
        span = _span(text, person)
        entities.append({"span": span, "type": "PERSON", "referent": "PERSON"})
    for location in locations:
        span = _span(text, location)
        entities.append({"span": span, "type": "LOCATION", "referent": "LOCATION"})
    return sorted(entities, key=lambda item: (item["span"][0], item["type"]))


def _context(people: tuple[str, ...] = (), locations: tuple[str, ...] = ()) -> dict:
    known = {}
    for person in people:
        known[person] = {"type": "PERSON"}
    for location in locations:
        known[location] = {"type": "LOCATION"}
    return {
        "speaker": "PLAYER",
        "observer": "luna",
        "knownEntities": known,
        "recentEntityRefs": [],
    }


def _row(
    *,
    language: str,
    row_id: str,
    text: str,
    dialogue_act: str,
    predicate: str,
    subject_referent: str,
    target_referent: str = "NONE",
    owner_referent: str = "SUBJECT",
    perspective_referent: str = "SPEAKER",
    polarity: str = "POSITIVE",
    temporal_relation: str = "CURRENT",
    claim_kind: str = "EXPLICIT",
    object_text: str | None = None,
    subject_text: str | None = None,
    temporal_text: str | None = None,
    people: tuple[str, ...] = (),
    locations: tuple[str, ...] = (),
    family: str = "v22a_repair",
) -> dict:
    source = [0, len(text)]
    object_span = _span(text, object_text)
    subject_span = _span(text, subject_text)
    temporal_span = _span(text, temporal_text)
    negation_span = list(source) if polarity == "NEGATIVE" else None
    claim = {
        "labels": {
            "dialogueAct": dialogue_act,
            "predicate": predicate,
            "subjectReferent": subject_referent,
            "targetReferent": target_referent,
            "ownerReferent": owner_referent,
            "perspectiveReferent": perspective_referent,
            "polarity": polarity,
            "temporalRelation": temporal_relation,
            "claimKind": claim_kind,
            "worldTruth": False,
        },
        "spans": {
            "source": source,
            "object": object_span,
            "subject": subject_span,
            "negation": negation_span,
            "temporal": temporal_span,
            "entities": _entities(text, people=people, locations=locations),
        },
        "sourceId": f"matrix-v22a-authored:{row_id}:0",
        "family": family,
        "annotationPolicy": {
            "version": SCHEMA,
            "negationSurface": "SEMANTIC_SCOPE" if negation_span else "NONE",
            "subjectSurface": "IMPLICIT" if subject_referent == "SPEAKER" else (
                "EXPLICIT" if subject_span else "NONE"
            ),
            "temporalSurface": "EXPLICIT" if temporal_span else (
                "IMPLICIT" if temporal_relation != "ATEMPORAL" else "NONE"
            ),
            "temporalExpression": temporal_text,
        },
    }
    return {
        "schemaVersion": SCHEMA,
        "id": row_id,
        "split": "train",
        "language": language,
        "text": text,
        "context": _context(people=people, locations=locations),
        "claims": [claim],
        "adultOnly": False,
        "provenance": {
            "kind": "MATRIX_AUTHORED_V2_AUGMENTATION",
            "createdInVersion": SCHEMA,
            "parentSchema": "matrix.nlu.dataset.v1",
            "migrationPolicy": "SUPERVISOR_OPTION_A",
            "annotationContract": SCHEMA,
            "repairContract": REPAIR_SCHEMA,
            "leakageFamily": f"matrix:train:{row_id}",
            "generatorSeed": 810924,
            "license": "PROJECT_AUTHORED",
        },
    }


def build_repair_rows() -> tuple[list[dict], list[dict]]:
    rows: list[dict] = []

    def add(**kwargs) -> None:
        row = _row(**kwargs)
        rows.append(row)

    # Italian: negation + ownership/referent safety + predicate contrast.
    add(language="it", row_id="mx-v22a-it-neg-00", text="Non mi piace Marco",
        dialogue_act="ASSERT", predicate="preference.like", subject_referent="SPEAKER",
        target_referent="KNOWN_ENTITY", polarity="NEGATIVE", object_text="Marco",
        people=("Marco",), family="v22a_it_negation_preference")
    add(language="it", row_id="mx-v22a-it-neg-01", text="Non vivo più a Roma",
        dialogue_act="ASSERT", predicate="residence.place", subject_referent="SPEAKER",
        polarity="NEGATIVE", object_text="Roma", locations=("Roma",),
        family="v22a_it_negation_residence")
    add(language="it", row_id="mx-v22a-it-neg-02", text="Non sono arrabbiato con Luna",
        dialogue_act="ASSERT", predicate="attribute.is", subject_referent="SPEAKER",
        target_referent="OBSERVER", polarity="NEGATIVE", object_text="arrabbiato",
        people=("Luna",), family="v22a_it_negation_attribute")
    add(language="it", row_id="mx-v22a-it-neg-03", text="Marco non lavora come medico",
        dialogue_act="ASSERT", predicate="work.role", subject_referent="KNOWN_ENTITY",
        polarity="NEGATIVE", subject_text="Marco", object_text="medico",
        people=("Marco",), family="v22a_it_negation_known_subject")
    add(language="it", row_id="mx-v22a-it-neg-04", text="Giulia non vuole uscire con Marco",
        dialogue_act="ASSERT", predicate="goal.object", subject_referent="KNOWN_ENTITY",
        target_referent="KNOWN_ENTITY", polarity="NEGATIVE", subject_text="Giulia",
        object_text="uscire con Marco", people=("Giulia", "Marco"),
        family="v22a_it_negation_goal")
    add(language="it", row_id="mx-v22a-it-neg-05", text="Non è mio, è di Luca",
        dialogue_act="CORRECT", predicate="possession.has", subject_referent="KNOWN_ENTITY",
        owner_referent="KNOWN_ENTITY", perspective_referent="SPEAKER",
        polarity="NEGATIVE", object_text="mio", people=("Luca",),
        family="v22a_it_ownership_correction")

    add(language="it", row_id="mx-v22a-it-pred-00", text="Lavoro come meccanico",
        dialogue_act="ASSERT", predicate="work.role", subject_referent="SPEAKER",
        object_text="meccanico", family="v22a_it_predicate_work")
    add(language="it", row_id="mx-v22a-it-pred-01", text="Ho una macchina",
        dialogue_act="ASSERT", predicate="possession.has", subject_referent="SPEAKER",
        object_text="una macchina", family="v22a_it_predicate_possession")
    add(language="it", row_id="mx-v22a-it-pred-02", text="Voglio andare al bar",
        dialogue_act="ASSERT", predicate="goal.object", subject_referent="SPEAKER",
        object_text="andare al bar", family="v22a_it_predicate_goal")
    add(language="it", row_id="mx-v22a-it-pred-03", text="Mi chiamo Alberto",
        dialogue_act="ASSERT", predicate="identity.name", subject_referent="SPEAKER",
        object_text="Alberto", family="v22a_it_predicate_identity")
    add(language="it", row_id="mx-v22a-it-act-00", text="Ti piace Marco?",
        dialogue_act="QUESTION", predicate="preference.like", subject_referent="OBSERVER",
        target_referent="KNOWN_ENTITY", subject_text="Ti", object_text="Marco",
        people=("Marco",), family="v22a_it_dialogue_question")
    add(language="it", row_id="mx-v22a-it-act-01", text="Vieni al bar con me?",
        dialogue_act="REQUEST", predicate="goal.object", subject_referent="OBSERVER",
        target_referent="SPEAKER", object_text="bar", family="v22a_it_dialogue_request")

    # English: predicate and P0.5 style claim structure, with controlled negation pairs.
    add(language="en", row_id="mx-v22a-en-neg-00", text="I do not like Marco",
        dialogue_act="ASSERT", predicate="preference.like", subject_referent="SPEAKER",
        target_referent="KNOWN_ENTITY", polarity="NEGATIVE", object_text="Marco",
        people=("Marco",), family="v22a_en_negation_preference")
    add(language="en", row_id="mx-v22a-en-neg-01", text="I do not live in Rome anymore",
        dialogue_act="ASSERT", predicate="residence.place", subject_referent="SPEAKER",
        polarity="NEGATIVE", object_text="Rome", locations=("Rome",),
        family="v22a_en_negation_residence")
    add(language="en", row_id="mx-v22a-en-neg-02", text="Marco does not work as a doctor",
        dialogue_act="ASSERT", predicate="work.role", subject_referent="KNOWN_ENTITY",
        polarity="NEGATIVE", subject_text="Marco", object_text="a doctor",
        people=("Marco",), family="v22a_en_negation_known_subject")
    add(language="en", row_id="mx-v22a-en-neg-03", text="This is not mine, it is Luca's",
        dialogue_act="CORRECT", predicate="possession.has", subject_referent="KNOWN_ENTITY",
        owner_referent="KNOWN_ENTITY", perspective_referent="SPEAKER",
        polarity="NEGATIVE", object_text="mine", people=("Luca",),
        family="v22a_en_ownership_correction")
    add(language="en", row_id="mx-v22a-en-pred-00", text="I work as a mechanic",
        dialogue_act="ASSERT", predicate="work.role", subject_referent="SPEAKER",
        object_text="a mechanic", family="v22a_en_predicate_work")
    add(language="en", row_id="mx-v22a-en-pred-01", text="I have a car",
        dialogue_act="ASSERT", predicate="possession.has", subject_referent="SPEAKER",
        object_text="a car", family="v22a_en_predicate_possession")
    add(language="en", row_id="mx-v22a-en-pred-02", text="I want to go to the bar",
        dialogue_act="ASSERT", predicate="goal.object", subject_referent="SPEAKER",
        object_text="go to the bar", family="v22a_en_predicate_goal")
    add(language="en", row_id="mx-v22a-en-pred-03", text="My name is Alberto",
        dialogue_act="ASSERT", predicate="identity.name", subject_referent="SPEAKER",
        object_text="Alberto", family="v22a_en_predicate_identity")
    add(language="en", row_id="mx-v22a-en-pred-04", text="I am a patient person",
        dialogue_act="ASSERT", predicate="attribute.is", subject_referent="SPEAKER",
        object_text="a patient person", family="v22a_en_predicate_attribute")
    add(language="en", row_id="mx-v22a-en-pred-05", text="I can come tonight",
        dialogue_act="ASSERT", predicate="consent.grant", subject_referent="SPEAKER",
        temporal_relation="FUTURE", object_text="come tonight", temporal_text="tonight",
        family="v22a_en_predicate_consent")
    add(language="en", row_id="mx-v22a-en-act-00", text="Do you like Marco?",
        dialogue_act="QUESTION", predicate="preference.like", subject_referent="OBSERVER",
        target_referent="KNOWN_ENTITY", subject_text="you", object_text="Marco",
        people=("Marco",), family="v22a_en_dialogue_question")
    add(language="en", row_id="mx-v22a-en-act-01", text="Come to the bar with me",
        dialogue_act="REQUEST", predicate="goal.object", subject_referent="OBSERVER",
        target_referent="SPEAKER", object_text="bar", family="v22a_en_dialogue_request")

    # Spanish: negation repair first, then predicate contrast.
    add(language="es", row_id="mx-v22a-es-neg-00", text="No me gusta Marco",
        dialogue_act="ASSERT", predicate="preference.like", subject_referent="SPEAKER",
        target_referent="KNOWN_ENTITY", polarity="NEGATIVE", object_text="Marco",
        people=("Marco",), family="v22a_es_negation_preference")
    add(language="es", row_id="mx-v22a-es-neg-01", text="Ya no vivo en Roma",
        dialogue_act="ASSERT", predicate="residence.place", subject_referent="SPEAKER",
        polarity="NEGATIVE", object_text="Roma", locations=("Roma",),
        family="v22a_es_negation_residence")
    add(language="es", row_id="mx-v22a-es-neg-02", text="No estoy enfadado con Luna",
        dialogue_act="ASSERT", predicate="attribute.is", subject_referent="SPEAKER",
        target_referent="OBSERVER", polarity="NEGATIVE", object_text="enfadado",
        people=("Luna",), family="v22a_es_negation_attribute")
    add(language="es", row_id="mx-v22a-es-neg-03", text="Marco no trabaja como médico",
        dialogue_act="ASSERT", predicate="work.role", subject_referent="KNOWN_ENTITY",
        polarity="NEGATIVE", subject_text="Marco", object_text="médico",
        people=("Marco",), family="v22a_es_negation_known_subject")
    add(language="es", row_id="mx-v22a-es-neg-04", text="Giulia no quiere salir con Marco",
        dialogue_act="ASSERT", predicate="goal.object", subject_referent="KNOWN_ENTITY",
        target_referent="KNOWN_ENTITY", polarity="NEGATIVE", subject_text="Giulia",
        object_text="salir con Marco", people=("Giulia", "Marco"),
        family="v22a_es_negation_goal")
    add(language="es", row_id="mx-v22a-es-neg-05", text="No es mío, es de Luca",
        dialogue_act="CORRECT", predicate="possession.has", subject_referent="KNOWN_ENTITY",
        owner_referent="KNOWN_ENTITY", perspective_referent="SPEAKER",
        polarity="NEGATIVE", object_text="mío", people=("Luca",),
        family="v22a_es_ownership_correction")

    add(language="es", row_id="mx-v22a-es-pred-00", text="Trabajo como mecánico",
        dialogue_act="ASSERT", predicate="work.role", subject_referent="SPEAKER",
        object_text="mecánico", family="v22a_es_predicate_work")
    add(language="es", row_id="mx-v22a-es-pred-01", text="Tengo un coche",
        dialogue_act="ASSERT", predicate="possession.has", subject_referent="SPEAKER",
        object_text="un coche", family="v22a_es_predicate_possession")
    add(language="es", row_id="mx-v22a-es-pred-02", text="Quiero ir al bar",
        dialogue_act="ASSERT", predicate="goal.object", subject_referent="SPEAKER",
        object_text="ir al bar", family="v22a_es_predicate_goal")
    add(language="es", row_id="mx-v22a-es-pred-03", text="Me llamo Alberto",
        dialogue_act="ASSERT", predicate="identity.name", subject_referent="SPEAKER",
        object_text="Alberto", family="v22a_es_predicate_identity")
    add(language="es", row_id="mx-v22a-es-act-00", text="¿Te gusta Marco?",
        dialogue_act="QUESTION", predicate="preference.like", subject_referent="OBSERVER",
        target_referent="KNOWN_ENTITY", subject_text="Te", object_text="Marco",
        people=("Marco",), family="v22a_es_dialogue_question")
    add(language="es", row_id="mx-v22a-es-act-01", text="Ven al bar conmigo",
        dialogue_act="REQUEST", predicate="goal.object", subject_referent="OBSERVER",
        target_referent="SPEAKER", object_text="bar", family="v22a_es_dialogue_request")

    additions = []
    for row in rows:
        claim = row["claims"][0]
        additions.append({
            "dataset": "matrix",
            "rowId": row["id"],
            "split": "train",
            "language": row["language"],
            "reason": "STUDENT_4_V22A_TARGETED_REPAIR_TRAIN_ONLY",
            "family": claim["family"],
            "predicate": claim["labels"]["predicate"],
            "polarity": claim["labels"]["polarity"],
            "dialogueAct": claim["labels"]["dialogueAct"],
        })
    return rows, additions


def build(p05_gold: pathlib.Path) -> tuple[dict[str, list[dict]], dict]:
    records, mapping = v2.build(p05_gold)
    repair_rows, repair_additions = build_repair_rows()
    records["matrix"].extend(repair_rows)

    counts = Counter(row["language"] for row in repair_rows)
    if set(counts) != set(LANGUAGES) or len(set(counts.values())) != 1:
        raise RuntimeError(f"v2.2A repair rows must stay language-balanced: {dict(counts)}")

    mapping = dict(mapping)
    mapping["schemaVersion"] = "matrix.nlu.dataset-v22a-repair-mapping.v1"
    mapping["baseMappingSchema"] = "matrix.nlu.dataset-v1-to-v2-mapping.v1"
    mapping["repairContract"] = REPAIR_SCHEMA
    mapping["repairPolicy"] = {
        "splitsModified": ["train"],
        "devModified": False,
        "frozenModified": False,
        "frozenPredictionsRead": False,
        "frozenDataUsedForTuning": False,
        "targetFailures": [
            "it/es Matrix negation F1 collapse",
            "it/en/es P0.5 predicate collapse",
            "span decoding exact-set cascade",
            "Italian ownership corruption guard",
            "question/request/report/correction separation",
        ],
    }
    mapping["counts"] = {**mapping.get("counts", {}), "v22aTrainRepairAdditions": len(repair_additions)}
    mapping["trainAdditions"] = sorted(
        list(mapping.get("trainAdditions", [])) + repair_additions,
        key=lambda item: (item.get("language", ""), item.get("rowId", "")),
    )
    return records, mapping


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--output-dir", type=pathlib.Path, default=pathlib.Path("build/matrix-nlu/data-v22a"))
    parser.add_argument("--p05-gold", type=pathlib.Path, default=pathlib.Path("gold/p05-gold-v1.json"))
    args = parser.parse_args()

    records, mapping = build(args.p05_gold)
    manifests = {
        source: v2.write_dataset(records[source], args.output_dir, f"{source}-v2", v2.V1_HASHES[source])
        for source in ("matrix", "p05")
    }
    mapping["v2Files"] = {source: manifests[source]["files"] for source in manifests}
    mapping_path = args.output_dir / "v1-to-v2-corrections.json"
    mapping_path.write_text(json.dumps(mapping, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")

    print(json.dumps({
        "schemaVersion": REPAIR_SCHEMA,
        "datasetSchema": SCHEMA,
        "outputDir": str(args.output_dir),
        "repairRows": mapping["counts"]["v22aTrainRepairAdditions"],
        "languageCounts": dict(sorted(Counter(row["language"] for row in build_repair_rows()[0]).items())),
        "manifests": manifests,
        "mapping": {"path": str(mapping_path), "sha256": sha256(mapping_path), **mapping["counts"]},
        "frozenModified": False,
        "devModified": False,
    }, indent=2, ensure_ascii=False))


if __name__ == "__main__":
    main()
