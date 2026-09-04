#!/usr/bin/env python3
"""Build the Student-5 vocabulary-selection corpus from TRAIN-only sources.

This module deliberately has no argument for canonical dev/test/frozen data.
The v2 correction manifest is used only as control metadata to remove the
already-authorized TRAIN row IDs that were excluded by the canonical v2 build.
"""

from __future__ import annotations

import argparse
import hashlib
import json
import pathlib
import random
import re
import tarfile
import urllib.request
from collections import Counter

import build_dataset as v1
import build_dataset_v2 as v2
from prepare_massive import LANGUAGE, parse_annotated, select
from v2_train_generalization import build_generalization_rows


SEED = 810925
EXPECTED_MATRIX_V1_TRAIN = 2991
EXPECTED_MATRIX_V2_TRAIN = 2775
EXPECTED_REPAIR_TRAIN = 375
EXPECTED_MASSIVE_PER_LANGUAGE = 3000
TRAIN_MARKER = re.compile(rb'"partition"\s*:\s*"train"')


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


def write_jsonl(path: pathlib.Path, rows: list[dict]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text("".join(json.dumps(row, ensure_ascii=False, sort_keys=True) + "\n"
                            for row in rows), encoding="utf-8")


def build_matrix_v1_train_only() -> list[dict]:
    """Reproduce only the v1 TRAIN partition without invoking held-out builders."""
    split = "train"
    count = 700
    output = []
    for language in v1.LANGUAGES:
        lex = v1.LEXICONS[split]
        singles = []
        for index in range(count):
            family = ("name", "age", "residence", "like", "dislike", "work",
                      "future_goal", "hypothesis", "question")[index % 9]
            name = lex["name"][language][index % len(lex["name"][language])]
            place = lex["place"][language][(index * 3 + 1) % len(lex["place"][language])]
            thing = lex["thing"][language][(index * 5 + 2) % len(lex["thing"][language])]
            role = lex["role"][language][(index * 7 + 1) % len(lex["role"][language])]
            obj = (name if family == "name" else str(20 + index % 57)
                   if family == "age" else place
                   if family in {"residence", "future_goal", "hypothesis"} else thing
                   if family in {"like", "dislike"} else role if family == "work" else "")
            subject = name if family in {"work", "hypothesis", "question"} else ""
            referent = "KNOWN_ENTITY" if subject else "SPEAKER"
            claim = v1.make_claim(split, language, family, object_value=obj,
                                  subject_value=subject, context_subject=referent,
                                  variant=index // 9)
            known = (subject, f"npc:{index % len(lex['name'][language])}") if subject else None
            row_id = f"mx-train-{language}-{index:05d}"
            singles.append((claim, known, row_id))
            output.append(v1.record(row_id, split, language, [claim], "", known))

        joiners = {
            "it": (" e ", "; in più ", ". Inoltre ", "; poi "),
            "en": (" and ", "; moreover ", ". Additionally ", "; then "),
            "es": (" y ", "; también ", ". Asimismo ", "; luego "),
        }
        candidates = [item for item in singles if item[1] is None]
        for index in range(count // 3):
            width = 3 if index % 5 == 0 else 2
            chosen = [candidates[(index * 11 + offset * 37) % len(candidates)][0]
                      for offset in range(width)]
            row_id = f"mx-train-{language}-multi-{index:04d}"
            output.append(v1.record(row_id, split, language, chosen,
                                    joiners[language][index % len(joiners[language])]))

        for index in range(max(12, count // 25)):
            claim = v1.adult_claim(language, index % 2 == 0, split)
            row_id = f"mx-train-{language}-adult-{index:04d}"
            output.append(v1.record(row_id, split, language, [claim], ""))

    output.extend(v1.recent_reference_records())
    if len(output) != EXPECTED_MATRIX_V1_TRAIN:
        raise RuntimeError(f"Matrix v1 TRAIN count {len(output)} != {EXPECTED_MATRIX_V1_TRAIN}")
    if any(row["split"] != "train" for row in output):
        raise RuntimeError("non-TRAIN Matrix row entered the selection corpus")
    return output


def build_matrix_v2_train_only(matrix_v1: list[dict], mapping_path: pathlib.Path) -> list[dict]:
    """Apply v2 semantics/additions and canonical TRAIN drop IDs only."""
    migrated, _ = v2._migrate(matrix_v1, "matrix")
    additions, _ = v2.v2_train_augmentations()
    generalization, _ = build_generalization_rows(v2.SCHEMA, v1.SCHEMA, v1.SEED)
    mapping = json.loads(mapping_path.read_text(encoding="utf-8"))
    drops = {
        entry["rowId"] for entry in mapping["partitionDrops"]
        if entry.get("dataset") == "matrix" and entry.get("split") == "train"
    }
    if len(drops) != 345:
        raise RuntimeError(f"unexpected canonical TRAIN drop count: {len(drops)}")
    rows = [row for row in migrated + additions + generalization if row["id"] not in drops]
    if len(rows) != EXPECTED_MATRIX_V2_TRAIN:
        raise RuntimeError(f"Matrix v2 TRAIN count {len(rows)} != {EXPECTED_MATRIX_V2_TRAIN}")
    if any(row["split"] != "train" for row in rows):
        raise RuntimeError("non-TRAIN Matrix v2 row entered the selection corpus")
    return rows


def read_repair_train(path: pathlib.Path, manifest_path: pathlib.Path) -> list[dict]:
    manifest = json.loads(manifest_path.read_text(encoding="utf-8"))
    if manifest["records"] != EXPECTED_REPAIR_TRAIN or manifest["sha256"] != sha256(path):
        raise RuntimeError("v2.2A repair TRAIN manifest mismatch")
    rows = [json.loads(line) for line in path.read_text(encoding="utf-8").splitlines()]
    if len(rows) != EXPECTED_REPAIR_TRAIN or any(row["split"] != "train" for row in rows):
        raise RuntimeError("v2.2A repair is not exactly 375 TRAIN rows")
    return rows


def download_massive_train(source_path: pathlib.Path, cache_dir: pathlib.Path) -> tuple[list[dict], dict]:
    """Download the pinned archive and decode only lines marked TRAIN.

    Non-TRAIN lines are rejected at the byte-marker boundary before JSON decode;
    their utterance fields are never inspected, tokenized, or retained.
    """
    spec = json.loads(source_path.read_text(encoding="utf-8"))
    cache_dir.mkdir(parents=True, exist_ok=True)
    archive_path = cache_dir / "amazon-massive-dataset-1.0.tar.gz"
    if not archive_path.exists():
        with urllib.request.urlopen(spec["url"], timeout=300) as response, \
                archive_path.open("wb") as output:
            while True:
                block = response.read(1024 * 1024)
                if not block:
                    break
                output.write(block)
    actual = sha256(archive_path)
    if actual != spec["expectedSha256"]:
        raise RuntimeError(f"MASSIVE archive hash mismatch: {actual}")

    all_selected = []
    raw_train_counts = {}
    license_bytes = None
    with tarfile.open(archive_path, "r:gz") as archive:
        members = archive.getmembers()
        license_member = next(member for member in members if member.name.endswith("/LICENSE"))
        license_bytes = archive.extractfile(license_member).read()
        for locale_index, locale in enumerate(spec["locales"]):
            member = next(member for member in members
                          if member.name.endswith(f"/data/{locale}.jsonl"))
            candidates = []
            with archive.extractfile(member) as handle:
                for raw_line in handle:
                    if not TRAIN_MARKER.search(raw_line):
                        continue
                    row = json.loads(raw_line)
                    if row["partition"] != "train":
                        raise RuntimeError("MASSIVE byte marker/parser disagreement")
                    candidates.append(row)
            raw_train_counts[locale] = len(candidates)
            chosen = select(candidates, EXPECTED_MASSIVE_PER_LANGUAGE,
                            SEED + locale_index * 101)
            for row in chosen:
                text, _ = parse_annotated(row["annot_utt"])
                all_selected.append({
                    "source": "massive-1.0-train",
                    "sourceId": f"massive-1.0:{locale}:{row['id']}",
                    "language": LANGUAGE[locale],
                    "domain": "general",
                    "category": "massive_request_intent",
                    "text": text,
                    "license": "CC-BY-4.0",
                })
    counts = Counter(row["language"] for row in all_selected)
    if counts != Counter({"it": 3000, "en": 3000, "es": 3000}):
        raise RuntimeError(f"MASSIVE TRAIN sample mismatch: {counts}")
    return all_selected, {
        "source": spec,
        "archivePath": str(archive_path),
        "archiveSha256": actual,
        "licenseSha256": hashlib.sha256(license_bytes).hexdigest(),
        "rawTrainCounts": raw_train_counts,
        "selectedCounts": dict(sorted(counts.items())),
        "nonTrainJsonDecoded": False,
    }


GENERAL = {
    "it": {
        "names": ["Alessandro", "Beatrice", "Camilla", "Dario", "Eleonora", "Federico",
                  "Giorgia", "Ilaria", "Jacopo", "Lorenzo", "Marta", "Niccolò", "Noemi",
                  "Riccardo", "Sofía", "José", "François", "Zoë"],
        "places": ["Milano", "Napoli", "Venezia", "Firenze", "Palermo", "Cagliari",
                   "Buenos Aires", "Città del Messico", "San Sebastián", "New York"],
        "slang": ["boh", "mah", "raga", "tipo", "cioè", "vabbè", "cmq", "nn", "xké",
                  "tutto ok?", "ci becchiamo", "mi sa", "un casino", "che figata"],
        "times": ["ieri sera", "stamattina", "adesso", "più tardi", "domani",
                  "la prossima settimana", "nel 2027", "fra tre ore"],
    },
    "en": {
        "names": ["Alexander", "Beatrice", "Camila", "Darius", "Eleanor", "Frederick",
                  "Georgia", "Iris", "Jacob", "Liam", "Martha", "Nicholas", "Noemi",
                  "Richard", "Sofía", "José", "François", "Zoë"],
        "places": ["London", "Manchester", "Bristol", "Edinburgh", "Dublin", "Austin",
                   "Buenos Aires", "Mexico City", "San Sebastián", "New York"],
        "slang": ["dunno", "kinda", "gonna", "wanna", "lemme", "yep", "nope", "btw",
                  "idk", "what's up?", "hang out", "my bad", "awesome", "low-key"],
        "times": ["last night", "this morning", "right now", "later", "tomorrow",
                  "next week", "in 2027", "in three hours"],
    },
    "es": {
        "names": ["Alejandro", "Beatriz", "Camila", "Darío", "Elena", "Federico",
                  "Georgia", "Inés", "Jacobo", "Luis", "Marta", "Nicolás", "Noemí",
                  "Ricardo", "Sofía", "José", "François", "Zoë"],
        "places": ["Madrid", "Barcelona", "Sevilla", "Valencia", "Málaga", "Cádiz",
                   "Buenos Aires", "Ciudad de México", "San Sebastián", "Nueva York"],
        "slang": ["no sé", "bueno", "tío", "rollo", "o sea", "vale", "q", "xq", "tb",
                  "¿qué tal?", "quedamos", "me parece", "un lío", "qué guay"],
        "times": ["anoche", "esta mañana", "ahora mismo", "más tarde", "mañana",
                  "la próxima semana", "en 2027", "dentro de tres horas"],
    },
}


ADULT = {
    "it": {
        "desire": ["desiderio", "attrazione", "eccitazione", "intimità", "voglia", "fantasia",
                   "flirt", "seduzione", "bacio", "carezza"],
        "anatomy": ["pene", "vagina", "vulva", "clitoride", "seno", "capezzoli", "testicoli",
                    "ano", "sedere", "corpo"],
        "practice": ["sesso", "sesso orale", "sesso anale", "masturbazione", "petting",
                     "preliminari", "penetrazione", "dirty talk", "roleplay", "sexting",
                     "blowjob", "handjob"],
        "slang": ["scopare", "cazzo", "figa", "venire", "fare l'amore", "andare a letto"],
        "health": ["preservativo", "contraccezione", "protezione", "lubrificante", "test STI"],
    },
    "en": {
        "desire": ["desire", "attraction", "arousal", "intimacy", "lust", "fantasy",
                   "flirting", "seduction", "kiss", "caress"],
        "anatomy": ["penis", "vagina", "vulva", "clitoris", "breasts", "nipples", "testicles",
                    "anus", "butt", "body"],
        "practice": ["sex", "oral sex", "anal sex", "masturbation", "petting", "foreplay",
                     "penetration", "dirty talk", "roleplay", "sexting", "blowjob", "handjob"],
        "slang": ["fuck", "cock", "pussy", "come", "make love", "sleep together"],
        "health": ["condom", "contraception", "protection", "lubricant", "STI test"],
    },
    "es": {
        "desire": ["deseo", "atracción", "excitación", "intimidad", "ganas", "fantasía",
                   "coqueteo", "seducción", "beso", "caricia"],
        "anatomy": ["pene", "vagina", "vulva", "clítoris", "pechos", "pezones", "testículos",
                    "ano", "culo", "cuerpo"],
        "practice": ["sexo", "sexo oral", "sexo anal", "masturbación", "petting", "preliminares",
                     "penetración", "dirty talk", "roleplay", "sexting", "blowjob", "handjob"],
        "slang": ["follar", "polla", "coño", "correrse", "hacer el amor", "acostarse"],
        "health": ["preservativo", "anticoncepción", "protección", "lubricante", "prueba de ITS"],
    },
}


def authored_coverage_rows() -> list[dict]:
    rows = []
    general_templates = {
        "it": ["{name} vive a {place} {time}", "Non credo che {name} sia a {place}",
               "Puoi chiamare {name} più tardi?", "No, correggo: {name} è a {place}",
               "La macchina di {name} è a {place}", "Messaggio informale: {slang}"],
        "en": ["{name} lives in {place} {time}", "I don't think {name} is in {place}",
               "Can you call {name} later?", "No, correction: {name} is in {place}",
               "{name}'s car is in {place}", "Informal message: {slang}"],
        "es": ["{name} vive en {place} {time}", "No creo que {name} esté en {place}",
               "¿Puedes llamar a {name} más tarde?", "No, corrijo: {name} está en {place}",
               "El coche de {name} está en {place}", "Mensaje informal: {slang}"],
    }
    for language, values in GENERAL.items():
        for index in range(240):
            template = general_templates[language][index % len(general_templates[language])]
            text = template.format(
                name=values["names"][index % len(values["names"])],
                place=values["places"][(index * 3) % len(values["places"])],
                time=values["times"][(index * 5) % len(values["times"])],
                slang=values["slang"][(index * 7) % len(values["slang"])],
            )
            rows.append({"source": "matrix-student5-authored-coverage", "language": language,
                         "domain": "general", "category": "authored_daily_language",
                         "text": text, "license": "PROJECT_AUTHORED"})

    adult_templates = {
        "it": ["Tra adulti parliamo di {term} con consenso", "Mi interessa {term} con te",
               "Ti chiedo se vuoi {term}", "Non voglio {term}, fermati",
               "Prima desideravo {term}, domani forse no", "Luna dice che Marco preferisce {term}"],
        "en": ["Adults discuss {term} with consent", "I am interested in {term} with you",
               "I am asking whether you want {term}", "I do not want {term}, stop",
               "I wanted {term} before, maybe not tomorrow", "Luna says Marco prefers {term}"],
        "es": ["Los adultos hablan de {term} con consentimiento", "Me interesa {term} contigo",
               "Te pregunto si quieres {term}", "No quiero {term}, para",
               "Antes deseaba {term}, quizá mañana no", "Luna dice que Marco prefiere {term}"],
    }
    for language, categories in ADULT.items():
        for category, terms in categories.items():
            for index, term in enumerate(terms):
                for template in adult_templates[language]:
                    rows.append({"source": "matrix-student5-authored-adult-coverage",
                                 "language": language, "domain": "adult_intimacy",
                                 "category": category, "text": template.format(term=term),
                                 "adultOnly": True, "license": "PROJECT_AUTHORED"})

    code_switch = [
        ("it", "Mi piace il dirty talk, pero solo con consenso explícito"),
        ("it", "No quiero sex adesso, please fermati"),
        ("es", "Quiero fare l'amore contigo, but only if you agree"),
        ("en", "I want intimità contigo, pero no ahora"),
        ("it", "Possiamo fare sexting mañana, if you still want it"),
        ("es", "El roleplay mi piace, ma possiamo stop whenever we want"),
    ]
    for repeat in range(30):
        for language, text in code_switch:
            rows.append({"source": "matrix-student5-authored-code-switch",
                         "language": language, "domain": "adult_intimacy",
                         "category": "code_switch", "text": f"{text} #{repeat + 1}",
                         "adultOnly": True, "license": "PROJECT_AUTHORED"})

    controls = (
        "0123456789 .,!?:;-'’\"()[]{} / \\ @ # % & + = _ € $",
        "abcdefghijklmnopqrstuvwxyz ABCDEFGHIJKLMNOPQRSTUVWXYZ",
        "àèéìíîòóùúüñç ÀÈÉÌÍÎÒÓÙÚÜÑÇ",
        "https://example.com user@example.com @utente #argomento :-) ❤️ 😊 😂 😘",
    )
    for text in controls:
        rows.append({"source": "matrix-student5-authored-controls", "language": "multi",
                     "domain": "controls", "category": "mandatory_characters",
                     "text": text, "license": "PROJECT_AUTHORED"})
    return rows


def source_rows(rows: list[dict], source: str) -> list[dict]:
    return [{"source": source, "sourceId": row["id"], "language": row["language"],
             "domain": "adult_intimacy" if row.get("adultOnly") else "general",
             "category": "matrix_train", "text": row["text"],
             "license": "PROJECT_AUTHORED"} for row in rows]


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--output-dir", type=pathlib.Path, required=True)
    parser.add_argument("--mapping", type=pathlib.Path, required=True)
    parser.add_argument("--repair", type=pathlib.Path, required=True)
    parser.add_argument("--repair-manifest", type=pathlib.Path, required=True)
    parser.add_argument("--massive-source", type=pathlib.Path, required=True)
    parser.add_argument("--source-cache", type=pathlib.Path, required=True)
    args = parser.parse_args()

    matrix_v1 = build_matrix_v1_train_only()
    matrix_v2 = build_matrix_v2_train_only(matrix_v1, args.mapping)
    repair = read_repair_train(args.repair, args.repair_manifest)
    massive, massive_manifest = download_massive_train(args.massive_source, args.source_cache)
    authored = authored_coverage_rows()

    rows = (source_rows(matrix_v1, "matrix-v1-train") +
            source_rows(matrix_v2, "matrix-v2-train") +
            source_rows(repair, "matrix-v22a-repair-train-only") +
            massive + authored)
    random.Random(SEED).shuffle(rows)
    output_path = args.output_dir / "student5-vocab-selection-corpus.jsonl"
    write_jsonl(output_path, rows)
    counts_by_source = Counter(row["source"] for row in rows)
    counts_by_language = Counter(row["language"] for row in rows)
    counts_by_domain = Counter(row["domain"] for row in rows)
    manifest = {
        "schemaVersion": "matrix.nlu.student5.vocab-selection-corpus.v1",
        "seed": SEED,
        "file": output_path.name,
        "sha256": sha256(output_path),
        "records": len(rows),
        "countsBySource": dict(sorted(counts_by_source.items())),
        "countsByLanguage": dict(sorted(counts_by_language.items())),
        "countsByDomain": dict(sorted(counts_by_domain.items())),
        "matrixV1TrainRecords": len(matrix_v1),
        "matrixV2TrainRecords": len(matrix_v2),
        "repairTrainOnlyRecords": len(repair),
        "massive": massive_manifest,
        "policy": {
            "canonicalDevRead": False,
            "canonicalDevTokenized": False,
            "frozenDataRead": False,
            "frozenDataTokenized": False,
            "frozenDataAnalyzed": False,
            "v2MappingUse": "TRAIN_DROP_IDS_ONLY_CONTROL_METADATA",
            "nonTrainMassiveJsonDecoded": False,
            "adultMaterial": "ADULT_ONLY_PROJECT_AUTHORED_NLU_COVERAGE",
            "moderationLabels": False,
        },
    }
    write_json(args.output_dir / "student5-vocab-selection-corpus-manifest.json", manifest)
    print(json.dumps(manifest, indent=2, ensure_ascii=False))


if __name__ == "__main__":
    main()
