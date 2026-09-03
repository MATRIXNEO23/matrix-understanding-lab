package com.matrix.p05.train;

import opennlp.tools.postag.POSSample;

import java.io.IOException;
import java.nio.charset.StandardCharsets;
import java.nio.file.Files;
import java.nio.file.Path;
import java.util.ArrayList;
import java.util.List;

final class ConlluCorpus {
    private ConlluCorpus() {}

    static List<POSSample> parse(byte[] bytes) {
        String text = new String(bytes, StandardCharsets.UTF_8).replace("\r\n", "\n");
        List<POSSample> samples = new ArrayList<>();
        List<String> tokens = new ArrayList<>();
        List<String> tags = new ArrayList<>();
        for (String line : text.split("\n", -1)) {
            if (line.isBlank()) {
                flush(samples, tokens, tags);
                continue;
            }
            if (line.startsWith("#")) continue;
            String[] columns = line.split("\t", -1);
            if (columns.length < 4) {
                throw new IllegalArgumentException("invalid CoNLL-U row: " + line);
            }
            if (columns[0].contains("-") || columns[0].contains(".")) continue;
            if (columns[1].isBlank() || columns[3].isBlank() || "_".equals(columns[3])) {
                throw new IllegalArgumentException("missing token/UPOS: " + line);
            }
            tokens.add(columns[1]);
            tags.add(columns[3]);
        }
        flush(samples, tokens, tags);
        return List.copyOf(samples);
    }

    static void writeNormalized(Path path, List<POSSample> samples) throws IOException {
        Files.createDirectories(path.getParent());
        StringBuilder out = new StringBuilder();
        for (POSSample sample : samples) {
            String[] sentence = sample.getSentence();
            String[] tags = sample.getTags();
            for (int i = 0; i < sentence.length; i++) {
                out.append(sentence[i].replace("\t", " ")).append('\t').append(tags[i]).append('\n');
            }
            out.append('\n');
        }
        Files.writeString(path, out, StandardCharsets.UTF_8);
    }

    static long tokenCount(List<POSSample> samples) {
        return samples.stream().mapToLong(s -> s.getSentence().length).sum();
    }

    private static void flush(List<POSSample> samples, List<String> tokens, List<String> tags) {
        if (tokens.isEmpty()) return;
        samples.add(new POSSample(tokens.toArray(String[]::new), tags.toArray(String[]::new)));
        tokens.clear();
        tags.clear();
    }
}
