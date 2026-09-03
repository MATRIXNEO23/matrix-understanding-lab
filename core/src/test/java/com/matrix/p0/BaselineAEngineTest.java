package com.matrix.p0;

import com.matrix.p0.Domain.*;
import org.junit.jupiter.api.Test;

import java.util.List;
import java.util.Map;

import static org.junit.jupiter.api.Assertions.*;

class BaselineAEngineTest {
    private final BaselineAEngine engine=new BaselineAEngine();
    private final Context context=new Context("PLAYER","luna",Map.of(),List.of());

    @Test void frozenItalianRegressionIsTyped() {
        Claim c=engine.interpret("r1",Language.IT,"non amo i locali affollati",context).claims().get(0);
        assertEquals("preference.like",c.predicate());assertEquals(Polarity.NEGATIVE,c.polarity());assertFalse(c.worldTruth());
    }

    @Test void splitsTwoSupportedItalianClaims() {
        var claims=engine.interpret("r2",Language.IT,"Ho 44 anni e vivo a San Vendemiano",context).claims();
        assertEquals(List.of("identity.age","residence.place"),claims.stream().map(Claim::predicate).toList());
    }

    @Test void otherLanguagesRemainObservableUnknown() {
        assertEquals("speech.unresolved",engine.interpret("r3",Language.EN,"My name is Albert",context).claims().get(0).predicate());
        assertEquals("speech.unresolved",engine.interpret("r4",Language.ES,"Me llamo Alberto",context).claims().get(0).predicate());
    }
}

