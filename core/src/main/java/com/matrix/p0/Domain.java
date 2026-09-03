package com.matrix.p0;

import java.util.List;
import java.util.Map;

public final class Domain {
    private Domain() {}

    public enum Language { IT, EN, ES }
    public enum DialogueAct { ASSERT, CORRECT, QUESTION, REQUEST, HYPOTHESIS, UNKNOWN }
    public enum Polarity { POSITIVE, NEGATIVE, UNKNOWN }
    public enum TemporalRelation { ATEMPORAL, CURRENT, PAST, FUTURE, UNKNOWN }
    public enum ClaimKind { EXPLICIT, HYPOTHESIS }

    public record SourceSpan(int startInclusive, int endExclusive, String text) {
        public SourceSpan {
            if (startInclusive < 0 || endExclusive < startInclusive) {
                throw new IllegalArgumentException("invalid source span");
            }
        }
    }

    public record EntityResolution(
        String mention,
        String type,
        String link,
        String method,
        double confidence,
        SourceSpan sourceSpan
    ) {}

    public record Claim(
        String speaker,
        String subject,
        String target,
        String owner,
        String perspective,
        DialogueAct dialogueAct,
        String predicate,
        String objectValue,
        Polarity polarity,
        SourceSpan negationScope,
        TemporalRelation temporalRelation,
        String temporalExpression,
        List<EntityResolution> entities,
        ClaimKind claimKind,
        double confidence,
        List<SourceSpan> sourceSpans,
        List<String> sourceIds,
        boolean worldTruth
    ) {}

    public record Context(
        String speaker,
        String observer,
        Map<String, String> knownEntities,
        List<String> recentEntityRefs
    ) {}

    public record GoldCase(
        String id,
        String scenarioId,
        String split,
        List<String> families,
        Language language,
        String text,
        Context context,
        List<Claim> expected
    ) {}

    public record Interpretation(String engine, String status, List<Claim> claims, List<String> diagnostics) {}
}

