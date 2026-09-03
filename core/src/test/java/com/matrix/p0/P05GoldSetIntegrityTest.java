package com.matrix.p0;

import com.matrix.p0.Domain.GoldCase;
import org.junit.jupiter.api.Test;

import java.util.List;
import java.util.Map;
import java.util.Set;
import java.util.stream.Collectors;

import static org.junit.jupiter.api.Assertions.*;

class P05GoldSetIntegrityTest {
    private final List<GoldCase> cases = load();

    @Test void expandedShapeIsFrozenAndParallel() {
        assertEquals(264, cases.size());
        assertEquals(Map.of("train", 87L, "dev", 84L, "test", 93L),
            cases.stream().collect(Collectors.groupingBy(GoldCase::split, Collectors.counting())));
        assertEquals(Set.of("IT", "EN", "ES"),
            cases.stream().map(c -> c.language().name()).collect(Collectors.toSet()));
        assertEquals(264, cases.stream().map(GoldCase::id).distinct().count());
    }

    @Test void requiredAdversarialFamiliesArePresent() {
        Set<String> families = cases.stream().flatMap(c -> c.families().stream()).collect(Collectors.toSet());
        assertTrue(families.containsAll(Set.of(
            "multi_claim", "coordination", "negation_local", "imperative", "modal_goal",
            "person_location_collision", "composite_location", "explicit_unknown",
            "ownership", "perspective", "provenance", "code_switch", "colloquial",
            "malformed", "temporality", "location_cooccurrence")));
    }

    @Test void safetyAndProvenanceInvariantsHold() {
        assertTrue(cases.stream().flatMap(c -> c.expected().stream()).noneMatch(c -> c.worldTruth()));
        assertTrue(cases.stream().flatMap(c -> c.expected().stream())
            .allMatch(c -> !c.sourceIds().isEmpty() && !c.sourceSpans().isEmpty()
                && c.speaker() != null && c.subject() != null && c.owner() != null && c.perspective() != null));
    }

    private static List<GoldCase> load() {
        try (var input = P05GoldSetIntegrityTest.class.getResourceAsStream("/p05-gold-v1.json")) {
            assertNotNull(input, "expanded gold set must be packaged as a test resource");
            return GoldDataset.load(input);
        } catch (Exception e) {
            throw new RuntimeException(e);
        }
    }
}
