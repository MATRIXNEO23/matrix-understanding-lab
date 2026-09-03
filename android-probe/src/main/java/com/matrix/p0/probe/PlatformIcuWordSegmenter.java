package com.matrix.p0.probe;

import android.icu.text.BreakIterator;

import com.matrix.p0.Domain.Language;
import com.matrix.p0.WordSegmenter;

import java.util.ArrayList;
import java.util.List;
import java.util.Locale;

/** Uses Android's platform ICU; no ICU4J payload is packaged in the probe. */
public final class PlatformIcuWordSegmenter implements WordSegmenter {
    @Override
    public List<Token> segment(Language language, String text) {
        BreakIterator iterator = BreakIterator.getWordInstance(locale(language));
        iterator.setText(text);
        List<Token> tokens = new ArrayList<>();
        int start = iterator.first();
        for (int end = iterator.next(); end != BreakIterator.DONE; start = end, end = iterator.next()) {
            String value = text.substring(start, end);
            if (value.codePoints().anyMatch(Character::isLetterOrDigit)) {
                tokens.add(new Token(value, start, end));
            }
        }
        return List.copyOf(tokens);
    }

    @Override
    public String implementation() {
        return "ANDROID_PLATFORM_ICU";
    }

    private static Locale locale(Language language) {
        return switch (language) {
            case IT -> Locale.ITALIAN;
            case EN -> Locale.ENGLISH;
            case ES -> Locale.forLanguageTag("es");
        };
    }
}
