"""Project-authored train-only diversity for Matrix-NLU dataset v2.

These examples are development-driven at the semantic-family level, but use
new surfaces and entities.  They are dataset supervision, never runtime rules.
"""

from __future__ import annotations


def _span(text: str, value: str | None):
    if value is None:
        return None
    start = text.index(value)
    return [start, start + len(value)]


def _row(schema: str, parent_schema: str, seed: int, *, language: str,
         category: str, index: int, text: str, predicate: str,
         dialogue_act: str = "ASSERT", polarity: str = "POSITIVE",
         temporal_relation: str = "ATEMPORAL", object_text: str | None = None,
         subject_text: str | None = None, subject_referent: str = "SPEAKER",
         target_referent: str = "NONE", claim_kind: str = "EXPLICIT",
         temporal_text: str | None = None, entities: tuple[tuple[str, str, str], ...] = (),
         known_entities: dict[str, str] | None = None) -> tuple[dict, dict]:
    row_id = f"mx-v2-train-{language}-generalization-{category}-{index:03d}"
    source = [0, len(text)]
    negative = polarity == "NEGATIVE"
    entity_rows = [{"span": _span(text, mention), "type": kind, "referent": referent}
                   for mention, kind, referent in entities]
    claim = {
        "labels": {
            "dialogueAct": dialogue_act, "predicate": predicate,
            "subjectReferent": subject_referent,
            "targetReferent": target_referent,
            "ownerReferent": "SUBJECT", "perspectiveReferent": "SPEAKER",
            "polarity": polarity, "temporalRelation": temporal_relation,
            "claimKind": claim_kind, "worldTruth": False,
        },
        "spans": {
            "source": source, "object": _span(text, object_text),
            "subject": None if subject_referent == "SPEAKER" else _span(text, subject_text),
            "negation": source if negative else None,
            "temporal": _span(text, temporal_text), "entities": entity_rows,
        },
        "sourceId": f"matrix-v2-authored:{row_id}:0",
        "family": f"{category}_v2_train_generalization",
        "annotationPolicy": {
            "version": schema,
            "negationSurface": "SEMANTIC_SCOPE" if negative else "NONE",
            "subjectSurface": "IMPLICIT" if subject_referent == "SPEAKER" else "EXPLICIT",
            "temporalSurface": "EXPLICIT" if temporal_text else (
                "IMPLICIT" if temporal_relation != "ATEMPORAL" else "NONE"),
            "temporalExpression": temporal_text,
        },
    }
    row = {
        "schemaVersion": schema, "id": row_id, "split": "train",
        "language": language, "text": text,
        "context": {"speaker": "PLAYER", "observer": "luna",
                    "knownEntities": known_entities or {}, "recentEntityRefs": []},
        "claims": [claim], "adultOnly": category.startswith("consent"),
        "provenance": {
            "kind": "MATRIX_AUTHORED_V2_AUGMENTATION",
            "createdInVersion": schema, "parentSchema": parent_schema,
            "migrationPolicy": "SUPERVISOR_OPTION_A",
            "annotationContract": schema,
            "leakageFamily": f"matrix:train:{row_id}",
            "generatorSeed": seed, "license": "PROJECT_AUTHORED",
            "rationale": "DEV_FAMILY_GENERALIZATION_WITH_DISTINCT_SURFACE",
        },
    }
    addition = {"dataset": "matrix", "rowId": row_id, "split": "train",
                "language": language, "reason": "DEV_FAMILY_GENERALIZATION",
                "family": category}
    return row, addition


def build_generalization_rows(schema: str, parent_schema: str, seed: int):
    rows, additions = [], []

    negative = {
        "it": (("trovo davvero sgradevole {object}", "il rumore"),
               ("non gradisco affatto {object}", "la confusione"),
               ("provo avversione per {object}", "l'attesa"),
               ("mi infastidisce molto {object}", "il traffico"),
               ("non riesco ad apprezzare {object}", "la nebbia"),
               ("considero insopportabile {object}", "il disordine"),
               ("preferisco evitare del tutto {object}", "la folla"),
               ("mi disgusta sinceramente {object}", "la maleducazione"),
               ("non è di mio gusto {object}", "il viola"),
               ("ho una forte antipatia per {object}", "le attese"),
               ("faccio volentieri a meno di {object}", "la musica alta"),
               ("non provo alcun piacere per {object}", "la grandine")),
        "en": (("I find {object} deeply unpleasant", "loud chatter"),
               ("I do not enjoy {object} at all", "heavy traffic"),
               ("I feel a strong aversion to {object}", "waiting around"),
               ("{object} bothers me a great deal", "dense fog"),
               ("I cannot appreciate {object}", "untidy rooms"),
               ("I consider {object} unbearable", "constant noise"),
               ("I would rather avoid {object} entirely", "large crowds"),
               ("I genuinely loathe {object}", "rude behaviour"),
               ("{object} is not to my taste", "purple decor"),
               ("I have a strong dislike of {object}", "long delays"),
               ("I am happier without {object}", "blaring music"),
               ("I take no pleasure in {object}", "hail storms")),
        "es": (("considero muy desagradable {object}", "el ruido"),
               ("no disfruto nada de {object}", "el tráfico"),
               ("siento una fuerte aversión por {object}", "la espera"),
               ("me molesta muchísimo {object}", "la niebla"),
               ("no consigo apreciar {object}", "el desorden"),
               ("me resulta insoportable {object}", "el bullicio"),
               ("prefiero evitar por completo {object}", "la multitud"),
               ("me disgusta sinceramente {object}", "la grosería"),
               ("{object} no es de mi gusto", "el color morado"),
               ("siento mucha antipatía por {object}", "las demoras"),
               ("prescindo con gusto de {object}", "la música fuerte"),
               ("no siento ningún placer con {object}", "el granizo")),
    }
    for language, examples in negative.items():
        for index, (template, object_text) in enumerate(examples):
            text = template.format(object=object_text)
            row, addition = _row(schema, parent_schema, seed, language=language,
                category="negative_preference", index=index, text=text,
                predicate="preference.like", polarity="NEGATIVE",
                object_text=object_text)
            rows.append(row); additions.append(addition)

    future = {
        "it": (("fra qualche tempo desidero raggiungere {object}", "Verona", "fra qualche tempo"),
               ("un giorno vorrei recarmi a {object}", "Genova", "un giorno"),
               ("nelle prossime settimane conto di visitare {object}", "Ravenna", "nelle prossime settimane"),
               ("a breve spero di andare a {object}", "Parma", "a breve"),
               ("entro l'anno voglio vedere {object}", "Siena", "entro l'anno"),
               ("nel prossimo futuro intendo esplorare {object}", "Matera", "nel prossimo futuro")),
        "en": (("in due course I want to reach {object}", "Brighton", "in due course"),
               ("one day I would like to travel to {object}", "Cambridge", "one day"),
               ("over the coming weeks I plan to visit {object}", "Durham", "over the coming weeks"),
               ("before long I hope to go to {object}", "Exeter", "before long"),
               ("within the year I want to see {object}", "Norwich", "within the year"),
               ("in the near future I intend to explore {object}", "Bath", "in the near future")),
        "es": (("con el tiempo deseo llegar a {object}", "Valencia", "con el tiempo"),
               ("algún día me gustaría viajar a {object}", "Granada", "algún día"),
               ("durante las próximas semanas pienso visitar {object}", "Salamanca", "durante las próximas semanas"),
               ("dentro de poco espero ir a {object}", "Málaga", "dentro de poco"),
               ("antes de fin de año quiero ver {object}", "Sevilla", "antes de fin de año"),
               ("en un futuro cercano pretendo explorar {object}", "Córdoba", "en un futuro cercano")),
    }
    for language, examples in future.items():
        for index, (template, place, temporal_text) in enumerate(examples):
            text = template.format(object=place)
            row, addition = _row(schema, parent_schema, seed, language=language,
                category="explicit_future_goal", index=index, text=text,
                predicate="goal.object", temporal_relation="FUTURE",
                object_text=place, temporal_text=temporal_text,
                entities=((place, "LOCATION", "LOCATION"),))
            rows.append(row); additions.append(addition)

    consent = {
        "it": ((True, "per me va bene ricevere un abbraccio"),
               (True, "sono d'accordo con questo contatto"),
               (True, "ti autorizzo a prendermi la mano"),
               (True, "questo gesto ha il mio assenso"),
               (False, "non voglio essere abbracciato adesso"),
               (False, "rifiuto qualunque contatto in questo momento"),
               (False, "non hai il permesso di toccarmi"),
               (False, "preferisco che tu mantenga le distanze")),
        "en": ((True, "I am comfortable receiving a hug"),
               (True, "I agree to this physical contact"),
               (True, "you may hold my hand"),
               (True, "this gesture has my approval"),
               (False, "I do not want to be hugged now"),
               (False, "I refuse any contact at this moment"),
               (False, "you do not have permission to touch me"),
               (False, "I would prefer you to keep your distance")),
        "es": ((True, "me parece bien recibir un abrazo"),
               (True, "estoy de acuerdo con este contacto"),
               (True, "puedes tomarme de la mano"),
               (True, "este gesto cuenta con mi aprobación"),
               (False, "no quiero que me abracen ahora"),
               (False, "rechazo cualquier contacto en este momento"),
               (False, "no tienes permiso para tocarme"),
               (False, "prefiero que mantengas la distancia")),
    }
    for language, examples in consent.items():
        for index, (grant, text) in enumerate(examples):
            row, addition = _row(schema, parent_schema, seed, language=language,
                category="consent_grant" if grant else "consent_refuse",
                index=index, text=text,
                predicate="consent.grant" if grant else "consent.refuse",
                polarity="POSITIVE" if grant else "NEGATIVE",
                temporal_relation="CURRENT", object_text=text,
                target_referent="OBSERVER")
            rows.append(row); additions.append(addition)

    acts = {
        "it": (("REQUEST", "potresti ricordarmi il mio colore preferito?", "preference.like", "il mio colore preferito", "POSITIVE"),
               ("REQUEST", "dimmi per favore dove abito", "residence.place", "dove abito", "UNKNOWN"),
               ("REQUEST", "puoi verificare quale lavoro svolgo?", "work.role", "quale lavoro svolgo", "UNKNOWN"),
               ("CORRECT", "mi correggo: il mio nome è Giulio", "identity.name", "Giulio", "POSITIVE"),
               ("CORRECT", "rettifico quanto detto: ho trentadue anni", "identity.age", "trentadue", "POSITIVE"),
               ("CORRECT", "no, la mia residenza corretta è Udine", "residence.place", "Udine", "POSITIVE")),
        "en": (("REQUEST", "could you remind me of my favourite colour?", "preference.like", "my favourite colour", "POSITIVE"),
               ("REQUEST", "please tell me where I live", "residence.place", "where I live", "UNKNOWN"),
               ("REQUEST", "can you check which job I perform?", "work.role", "which job I perform", "UNKNOWN"),
               ("CORRECT", "let me correct that: my name is Julian", "identity.name", "Julian", "POSITIVE"),
               ("CORRECT", "to amend what I said, I am thirty-two", "identity.age", "thirty-two", "POSITIVE"),
               ("CORRECT", "no, my correct residence is Reading", "residence.place", "Reading", "POSITIVE")),
        "es": (("REQUEST", "¿podrías recordarme mi color favorito?", "preference.like", "mi color favorito", "POSITIVE"),
               ("REQUEST", "dime por favor dónde vivo", "residence.place", "dónde vivo", "UNKNOWN"),
               ("REQUEST", "¿puedes comprobar qué trabajo desempeño?", "work.role", "qué trabajo desempeño", "UNKNOWN"),
               ("CORRECT", "me corrijo: mi nombre es Julián", "identity.name", "Julián", "POSITIVE"),
               ("CORRECT", "rectifico lo dicho: tengo treinta y dos años", "identity.age", "treinta y dos", "POSITIVE"),
               ("CORRECT", "no, mi residencia correcta es Alicante", "residence.place", "Alicante", "POSITIVE")),
    }
    for language, examples in acts.items():
        for index, (act, text, predicate, object_text, polarity) in enumerate(examples):
            row, addition = _row(schema, parent_schema, seed, language=language,
                category=f"dialogue_{act.lower()}", index=index, text=text,
                predicate=predicate, dialogue_act=act, polarity=polarity,
                temporal_relation="CURRENT", object_text=object_text,
                target_referent="SELF" if act == "REQUEST" else "NONE")
            rows.append(row); additions.append(addition)

    third_party = {
        "it": (("Lorenzo", "Lorenzo esercita la professione di architetto", "architetto", "work.role"),
               ("Marta", "Marta risiede stabilmente a Perugia", "Perugia", "residence.place"),
               ("Irene", "Irene si trova attualmente a Lecce", "Lecce", "presence.reported")),
        "en": (("Lawrence", "Lawrence works professionally as an architect", "an architect", "work.role"),
               ("Martha", "Martha resides permanently in Plymouth", "Plymouth", "residence.place"),
               ("Irene", "Irene is currently present in Lancaster", "Lancaster", "presence.reported")),
        "es": (("Lorenzo", "Lorenzo ejerce profesionalmente como arquitecto", "arquitecto", "work.role"),
               ("Marta", "Marta reside permanentemente en Zaragoza", "Zaragoza", "residence.place"),
               ("Irene", "Irene está actualmente presente en León", "León", "presence.reported")),
    }
    for language, examples in third_party.items():
        for index, (person, text, object_text, predicate) in enumerate(examples):
            location = predicate != "work.role"
            entities = [(person, "PERSON", "KNOWN_ENTITY")]
            if location:
                entities.append((object_text, "LOCATION", "LOCATION"))
            row, addition = _row(schema, parent_schema, seed, language=language,
                category="known_third_party", index=index, text=text,
                predicate=predicate, temporal_relation="CURRENT",
                object_text=object_text, subject_text=person,
                subject_referent="KNOWN_ENTITY", entities=tuple(entities),
                known_entities={person: f"npc:{person.casefold()}"})
            rows.append(row); additions.append(addition)

    return rows, additions
