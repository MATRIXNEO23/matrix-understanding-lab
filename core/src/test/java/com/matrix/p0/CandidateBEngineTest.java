package com.matrix.p0;

import com.matrix.p0.Domain.*;
import org.junit.jupiter.api.Test;

import java.text.BreakIterator;
import java.util.*;

import static org.junit.jupiter.api.Assertions.*;

class CandidateBEngineTest {
    private final CandidateBEngine engine=new CandidateBEngine(new JdkUnicodeSegmenter());
    private final Context context=new Context("PLAYER","luna",Map.of(),List.of());

    @Test void loadsAllThreeOpenNlpModelsAndKeepsWorldGuard(){
        for(Language language:Language.values()){
            String text=language==Language.IT?"Mi chiamo Alberto":language==Language.EN?"My name is Albert":"Me llamo Alberto";
            Claim claim=engine.interpret("smoke-"+language,language,text,context).claims().get(0);
            assertEquals("identity.name",claim.predicate());assertFalse(claim.worldTruth());assertFalse(claim.sourceIds().isEmpty());
        }
    }

    @Test void registryOutranksCapitalizationAndLocationStaysLocation(){
        Context c=new Context("PLAYER","luna",Map.of("Marco","OTHER:marco"),List.of());
        var claim=engine.interpret("entity",Language.EN,"Marco lives in New York",c).claims().get(0);
        assertEquals("OTHER:marco",claim.subject());
        assertTrue(claim.entities().stream().anyMatch(e->e.type().equals("LOCATION")&&e.mention().equals("New York")));
    }

    @Test void sameMapperHandlesLocalNegationAcrossLanguages(){
        var it=engine.interpret("n1",Language.IT,"Amo il jazz e non vivo a Roma",context).claims();
        var en=engine.interpret("n2",Language.EN,"I like jazz and I do not live in Rome",context).claims();
        var es=engine.interpret("n3",Language.ES,"Me gusta el jazz y no vivo en Roma",context).claims();
        for(var claims:List.of(it,en,es)){assertEquals(2,claims.size());assertEquals(Polarity.POSITIVE,claims.get(0).polarity());assertEquals(Polarity.NEGATIVE,claims.get(1).polarity());}
    }

    static final class JdkUnicodeSegmenter implements WordSegmenter {
        public List<Token> segment(Language language,String text){BreakIterator i=BreakIterator.getWordInstance(Locale.forLanguageTag(language.name().toLowerCase(Locale.ROOT)));i.setText(text);List<Token>o=new ArrayList<>();int s=i.first();for(int e=i.next();e!=BreakIterator.DONE;s=e,e=i.next()){String v=text.substring(s,e);if(v.codePoints().anyMatch(Character::isLetterOrDigit))o.add(new Token(v,s,e));}return o;}
        public String implementation(){return "JDK_TEST_PROXY";}
    }
}

