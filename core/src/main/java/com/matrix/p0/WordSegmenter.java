package com.matrix.p0;

import com.matrix.p0.Domain.Language;
import java.util.List;

public interface WordSegmenter {
    record Token(String text, int startInclusive, int endExclusive) {}
    List<Token> segment(Language language, String text);
    String implementation();
}

