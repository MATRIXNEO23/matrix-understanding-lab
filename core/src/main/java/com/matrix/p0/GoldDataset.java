package com.matrix.p0;

import com.fasterxml.jackson.databind.JsonNode;
import com.fasterxml.jackson.databind.ObjectMapper;
import com.matrix.p0.Domain.*;

import java.io.IOException;
import java.nio.file.Path;
import java.util.ArrayList;
import java.util.Iterator;
import java.util.LinkedHashMap;
import java.util.List;
import java.util.Map;

public final class GoldDataset {
    private GoldDataset() {}

    public static List<GoldCase> load(Path path) throws IOException {
        JsonNode root = new ObjectMapper().readTree(path.toFile());
        if (!"p0.gold.v1".equals(root.path("schemaVersion").asText())) {
            throw new IllegalArgumentException("unsupported gold schema");
        }
        List<GoldCase> out = new ArrayList<>();
        for (JsonNode scenario : root.withArray("scenarios")) {
            for (Language language : Language.values()) {
                String lang = language.name().toLowerCase();
                String text = scenario.path("variants").path(lang).asText();
                Context context = parseContext(scenario.path("context"));
                List<Claim> claims = new ArrayList<>();
                for (JsonNode claim : scenario.withArray("claims")) {
                    claims.add(parseClaim(claim, claim.path("localized").path(lang), text,
                        "gold:" + scenario.path("id").asText() + "-" + lang));
                }
                List<String> families = new ArrayList<>();
                scenario.withArray("families").forEach(n -> families.add(n.asText()));
                String sid = scenario.path("id").asText();
                out.add(new GoldCase(sid + "-" + lang, sid, scenario.path("split").asText(),
                    List.copyOf(families), language, text, context, List.copyOf(claims)));
            }
        }
        return List.copyOf(out);
    }

    private static Context parseContext(JsonNode node) {
        Map<String, String> known = new LinkedHashMap<>();
        Iterator<Map.Entry<String, JsonNode>> fields = node.path("knownEntities").fields();
        fields.forEachRemaining(e -> known.put(e.getKey(), e.getValue().asText()));
        List<String> recent = new ArrayList<>();
        node.withArray("recentEntityRefs").forEach(n -> recent.add(n.asText()));
        return new Context(node.path("speaker").asText(), node.path("observer").asText(),
            Map.copyOf(known), List.copyOf(recent));
    }

    private static Claim parseClaim(JsonNode common, JsonNode local, String fullText, String sourceId) {
        String sourceText = local.path("sourceText").asText();
        int start = Math.max(0, indexOfIgnoreCase(fullText, sourceText));
        List<EntityResolution> entities = new ArrayList<>();
        for (JsonNode entity : local.withArray("entities")) {
            String mention = entity.path("mention").asText();
            int entityStart = Math.max(0, indexOfIgnoreCase(fullText, mention));
            entities.add(new EntityResolution(mention, entity.path("type").asText(),
                entity.path("link").asText(), "gold", 1.0,
                new SourceSpan(entityStart, entityStart + mention.length(), mention)));
        }
        SourceSpan negation = null;
        if (local.hasNonNull("negationScope")) {
            String value = local.path("negationScope").asText();
            int n = Math.max(0, indexOfIgnoreCase(fullText, value));
            negation = new SourceSpan(n, n + value.length(), value);
        }
        return new Claim(
            common.path("speaker").asText(), common.path("subject").asText(),
            common.path("target").isNull() ? null : common.path("target").asText(),
            common.path("owner").asText(), common.path("perspective").asText(),
            DialogueAct.valueOf(common.path("dialogueAct").asText()),
            common.path("predicate").asText(), local.path("object").asText(),
            Polarity.valueOf(common.path("polarity").asText()), negation,
            TemporalRelation.valueOf(common.path("temporalRelation").asText()),
            local.hasNonNull("temporalExpression") ? local.path("temporalExpression").asText() : null,
            List.copyOf(entities), ClaimKind.valueOf(common.path("claimKind").asText()), 1.0,
            List.of(new SourceSpan(start, start + sourceText.length(), sourceText)),
            List.of(sourceId), false
        );
    }

    static int indexOfIgnoreCase(String source, String part) {
        return source.toLowerCase(java.util.Locale.ROOT).indexOf(part.toLowerCase(java.util.Locale.ROOT));
    }
}

