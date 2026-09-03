package com.matrix.p0;

import com.matrix.p0.Domain.GoldCase;
import org.junit.jupiter.api.Test;

import java.nio.file.Path;
import java.util.List;
import java.util.Map;
import java.util.Set;
import java.util.stream.Collectors;

import static org.junit.jupiter.api.Assertions.*;

class GoldSetIntegrityTest {
    private final List<GoldCase> cases = load();

    @Test void frozenShapeAndParallelLanguages() {
        assertEquals(66,cases.size());
        assertEquals(Map.of("train",21L,"dev",18L,"test",27L),cases.stream().collect(Collectors.groupingBy(GoldCase::split,Collectors.counting())));
        assertEquals(Set.of("IT","EN","ES"),cases.stream().map(c->c.language().name()).collect(Collectors.toSet()));
        assertTrue(cases.stream().allMatch(c->!c.expected().isEmpty()));
    }

    @Test void criticalClaimsNeverExpectWorldTruth() {
        assertTrue(cases.stream().flatMap(c->c.expected().stream()).noneMatch(c->c.worldTruth()));
        assertTrue(cases.stream().flatMap(c->c.expected().stream()).allMatch(c->!c.sourceIds().isEmpty()&&!c.sourceSpans().isEmpty()));
    }

    private static List<GoldCase> load(){try{return GoldDataset.load(Path.of("src/test/resources/p0-gold-v1.json"));}catch(Exception e){throw new RuntimeException(e);}}
}

