package com.matrix.p05.train;

import opennlp.tools.postag.POSSample;
import org.junit.jupiter.api.Test;

import java.nio.charset.StandardCharsets;
import java.util.List;

import static org.junit.jupiter.api.Assertions.assertArrayEquals;
import static org.junit.jupiter.api.Assertions.assertEquals;
import static org.junit.jupiter.api.Assertions.assertThrows;

class ConlluCorpusTest {
    @Test void parsesUpostagsAndSkipsMultiwordAndEmptyNodes() {
        String input = "# sent_id = x\n"
            + "1-2\tNel\t_\t_\t_\t_\t_\t_\t_\t_\n"
            + "1\tIn\tin\tADP\t_\t_\t0\troot\t_\t_\n"
            + "2\til\til\tDET\t_\t_\t1\tdet\t_\t_\n"
            + "2.1\tx\tx\tX\t_\t_\t_\t_\t_\t_\n"
            + "3\tparco\tparco\tNOUN\t_\t_\t1\tobl\t_\t_\n\n";
        List<POSSample> samples = ConlluCorpus.parse(input.getBytes(StandardCharsets.UTF_8));
        assertEquals(1, samples.size());
        assertArrayEquals(new String[]{"In", "il", "parco"}, samples.get(0).getSentence());
        assertArrayEquals(new String[]{"ADP", "DET", "NOUN"}, samples.get(0).getTags());
    }

    @Test void rejectsMalformedRows() {
        assertThrows(IllegalArgumentException.class,
            () -> ConlluCorpus.parse("1\tciao\n".getBytes(StandardCharsets.UTF_8)));
    }
}
