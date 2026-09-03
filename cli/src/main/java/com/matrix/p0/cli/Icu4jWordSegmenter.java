package com.matrix.p0.cli;

import com.ibm.icu.text.BreakIterator;
import com.matrix.p0.Domain.Language;
import com.matrix.p0.WordSegmenter;

import java.util.ArrayList;
import java.util.List;
import java.util.Locale;

public final class Icu4jWordSegmenter implements WordSegmenter {
    @Override public List<Token> segment(Language language,String text){
        Locale locale=Locale.forLanguageTag(language.name().toLowerCase(Locale.ROOT));
        BreakIterator it=BreakIterator.getWordInstance(locale);it.setText(text);List<Token> out=new ArrayList<>();
        int start=it.first();for(int end=it.next();end!=BreakIterator.DONE;start=end,end=it.next()){
            String value=text.substring(start,end);if(value.codePoints().anyMatch(Character::isLetterOrDigit))out.add(new Token(value,start,end));
        }return List.copyOf(out);
    }
    @Override public String implementation(){return "ICU4J_78.1_JVM_PARITY";}
}

