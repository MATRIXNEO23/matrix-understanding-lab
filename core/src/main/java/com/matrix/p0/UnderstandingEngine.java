package com.matrix.p0;

import com.matrix.p0.Domain.Context;
import com.matrix.p0.Domain.Interpretation;
import com.matrix.p0.Domain.Language;

public interface UnderstandingEngine {
    String id();
    String status();
    Interpretation interpret(String caseId, Language language, String text, Context context);
}

