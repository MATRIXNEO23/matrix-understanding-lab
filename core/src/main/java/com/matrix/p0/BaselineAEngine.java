package com.matrix.p0;

import com.matrix.p0.Domain.*;

import java.text.Normalizer;
import java.util.ArrayList;
import java.util.List;
import java.util.Locale;
import java.util.regex.Matcher;
import java.util.regex.Pattern;

/** Reproducibility control for the bounded, Italian-first Matrix parser. */
public final class BaselineAEngine implements UnderstandingEngine {
    private static final Pattern AGE = Pattern.compile("(?iu)\\bho\\s+(\\d{1,3})\\s+anni\\b");
    private static final Pattern NAME = Pattern.compile("(?u)\\b(?:mi\\s+chiamo|sono)\\s+([A-ZÀ-Ý][\\p{L}'-]*(?:\\s+[A-ZÀ-Ý][\\p{L}'-]*)?)");

    @Override public String id() { return "A_BASELINE_FROZEN"; }
    @Override public String status() { return "READY"; }

    @Override
    public Interpretation interpret(String caseId, Language language, String text, Context context) {
        if (language != Language.IT) {
            return new Interpretation(id(), status(), List.of(unresolved(caseId, text, context)),
                List.of("language_not_supported_by_frozen_baseline"));
        }
        List<Slice> slices = split(text);
        List<Claim> claims = new ArrayList<>();
        for (Slice slice : slices) claims.add(parse(caseId, text, slice, context));
        return new Interpretation(id(), status(), List.copyOf(claims), List.of("frozen_matrix_semantics=" +
            "ae82d5cf843d52b3d60caadd161e4a5516fc5d0d"));
    }

    private Claim parse(String caseId, String full, Slice slice, Context context) {
        String raw = slice.text.trim();
        String n = normalize(raw);
        DialogueAct act = raw.endsWith("?") || n.startsWith("dove ") ? DialogueAct.QUESTION
            : n.startsWith("apri ") ? DialogueAct.REQUEST
            : n.startsWith("in realta ") || n.startsWith("anzi ") ? DialogueAct.CORRECT
            : n.startsWith("forse ") ? DialogueAct.HYPOTHESIS : DialogueAct.ASSERT;
        String predicate = "speech.unresolved";
        String object = raw;
        Polarity polarity = Polarity.UNKNOWN;
        Matcher age = AGE.matcher(raw);
        Matcher name = NAME.matcher(raw);
        if (name.find()) { predicate = "identity.name"; object = name.group(1); polarity = Polarity.POSITIVE; }
        else if (age.find()) { predicate = "identity.age"; object = age.group(1); polarity = Polarity.POSITIVE; }
        else if (n.matches(".*\\b(?:lavoro|lavora) come .+")) { predicate = "work.role"; object = after(raw, "come"); polarity = Polarity.POSITIVE; }
        else if (n.matches(".*\\b(?:vivo|vive|vivevo|abitavo|abito) a .+")) { predicate = "residence.place"; object = afterAny(raw, List.of(" a ")); polarity = n.contains("non vivo") ? Polarity.NEGATIVE : Polarity.POSITIVE; }
        else if (n.matches(".*\\bsono (?:al|alla|a) .+")) { predicate = "presence.reported"; object = afterAny(raw, List.of(" al ", " alla ", " a ")); polarity = Polarity.POSITIVE; }
        else if (n.matches(".*\\b(?:mi piace|amo|odio|detesto|non sopporto) .+")) {
            predicate = "preference.like";
            String marker = n.contains("mi piace") ? "mi piace" : n.contains("non sopporto") ? "non sopporto" :
                n.contains("detesto") ? "detesto" : n.contains("odio") ? "odio" : "amo";
            object = after(raw, marker);
            polarity = n.contains("non ") || n.contains("odio") || n.contains("detesto") ? Polarity.NEGATIVE : Polarity.POSITIVE;
        } else if (n.contains("vorrei ")) { predicate = "goal.object"; object = after(raw, "vorrei"); polarity = Polarity.POSITIVE; }

        String subject = resolveSubject(raw, context);
        SourceSpan span = absoluteSpan(full, raw, slice.start);
        SourceSpan neg = polarity == Polarity.NEGATIVE ? span : null;
        TemporalRelation temporal = n.contains("prima ") || n.contains("vivevo") || n.contains("abitavo") ? TemporalRelation.PAST
            : n.contains("domani ") ? TemporalRelation.FUTURE
            : predicate.equals("speech.unresolved") || predicate.startsWith("preference") || predicate.equals("identity.name")
                ? TemporalRelation.ATEMPORAL : TemporalRelation.CURRENT;
        String expression = n.contains("prima ") ? "Prima" : n.contains("domani ") ? "Domani" : null;
        ClaimKind kind = act == DialogueAct.HYPOTHESIS ? ClaimKind.HYPOTHESIS : ClaimKind.EXPLICIT;
        List<EntityResolution> entities = entities(full, raw, slice.start, predicate, object, subject, context);
        String target = act == DialogueAct.REQUEST ? "SELF" : null;
        return new Claim(context.speaker(), subject, target, subject, context.speaker(), act, predicate,
            object.trim(), polarity, neg, temporal, expression, entities, kind,
            predicate.equals("speech.unresolved") ? 0.5 : 0.94, List.of(span),
            List.of("observation:" + caseId), false);
    }

    private static String resolveSubject(String raw, Context context) {
        for (var entry : context.knownEntities().entrySet()) {
            if (containsWord(raw, entry.getKey())) return entry.getValue();
        }
        String n = normalize(raw);
        if ((n.startsWith("lei ") || n.startsWith("lui ")) && !context.recentEntityRefs().isEmpty()) {
            return context.recentEntityRefs().get(0);
        }
        return context.speaker();
    }

    private static List<EntityResolution> entities(String full, String raw, int offset, String predicate,
                                                    String object, String subject, Context context) {
        List<EntityResolution> out = new ArrayList<>();
        for (var e : context.knownEntities().entrySet()) {
            int p = indexOfIgnoreCase(raw, e.getKey());
            if (p >= 0) out.add(entity(e.getKey(), "PERSON", e.getValue(), "known_entity", full, offset + p));
        }
        if (predicate.equals("identity.name")) {
            int p = Math.max(0, indexOfIgnoreCase(raw, object));
            out.add(entity(object, "PERSON", context.speaker(), "predicate_identity_object", full, offset + p));
        } else if (predicate.equals("residence.place") || predicate.equals("presence.reported")) {
            int p = Math.max(0, indexOfIgnoreCase(raw, object));
            out.add(entity(object, "LOCATION", "LOCATION:" + slug(object), "predicate_location_object", full, offset + p));
        }
        return List.copyOf(out);
    }

    private static EntityResolution entity(String mention, String type, String link, String method, String full, int start) {
        return new EntityResolution(mention, type, link, method, 0.99,
            new SourceSpan(start, Math.min(full.length(), start + mention.length()), mention));
    }

    private static Claim unresolved(String caseId, String text, Context c) {
        return new Claim(c.speaker(), c.speaker(), null, c.speaker(), c.speaker(),
            text.trim().endsWith("?") ? DialogueAct.QUESTION : DialogueAct.ASSERT,
            "speech.unresolved", text, Polarity.UNKNOWN, null, TemporalRelation.ATEMPORAL,
            null, List.of(), ClaimKind.EXPLICIT, 0.5,
            List.of(new SourceSpan(0, text.length(), text)), List.of("observation:" + caseId), false);
    }

    private static List<Slice> split(String text) {
        List<Slice> out = new ArrayList<>();
        int start = 0;
        Matcher m = Pattern.compile("(?iu)\\s+(?:e|,|;)+\\s+").matcher(text);
        while (m.find()) {
            String left = text.substring(start, m.start()).trim();
            String right = text.substring(m.end()).trim();
            if (hasPredicate(left) && hasPredicate(right)) {
                int actual = text.indexOf(left, start);
                out.add(new Slice(left, actual));
                start = m.end();
            }
        }
        String tail = text.substring(start).trim();
        if (!tail.isEmpty()) out.add(new Slice(tail, text.indexOf(tail, start)));
        return out;
    }

    private static boolean hasPredicate(String s) {
        String n = normalize(s);
        return NAME.matcher(s).find() || AGE.matcher(s).find() || n.matches(".*\\b(?:vivo|vive|vivevo|abitavo|abito) a .+")
            || n.matches(".*\\b(?:mi piace|amo|odio|detesto|non sopporto) .+") || n.matches(".*\\b(?:lavoro|lavora) come .+");
    }

    static String normalize(String s) {
        return Normalizer.normalize(s, Normalizer.Form.NFD).replaceAll("\\p{M}+", "")
            .toLowerCase(Locale.ROOT).replaceAll("[^\\p{L}\\p{N}']+", " ").trim();
    }
    static String slug(String s) { return normalize(s).replace(' ', '_'); }
    static int indexOfIgnoreCase(String source, String part) { return source.toLowerCase(Locale.ROOT).indexOf(part.toLowerCase(Locale.ROOT)); }
    static boolean containsWord(String source, String word) { return Pattern.compile("(?iu)(?<!\\p{L})" + Pattern.quote(word) + "(?!\\p{L})").matcher(source).find(); }
    static String after(String raw, String marker) { int p=indexOfIgnoreCase(raw, marker); return p<0?raw:raw.substring(p+marker.length()).trim(); }
    static String afterAny(String raw, List<String> markers) { for(String m:markers){int p=indexOfIgnoreCase(raw,m);if(p>=0)return raw.substring(p+m.length()).trim();}return raw; }
    static SourceSpan absoluteSpan(String full, String text, int hint) { int p=full.indexOf(text, Math.max(0,hint)); if(p<0)p=Math.max(0,hint); return new SourceSpan(p,Math.min(full.length(),p+text.length()),text); }
    private record Slice(String text, int start) {}
}

