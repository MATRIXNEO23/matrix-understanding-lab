package com.matrix.p0;

import com.matrix.p0.Domain.Language;
import opennlp.tools.postag.POSModel;
import opennlp.tools.postag.POSTaggerME;

import java.io.InputStream;
import java.util.EnumMap;
import java.util.List;
import java.util.Map;

public final class OpenNlpPosService {
    private static final Map<Language,String> RESOURCES=Map.of(
        Language.IT,"opennlp-it-ud-vit-pos-1.3-2.5.4.bin",
        Language.EN,"opennlp-en-ud-ewt-pos-1.3-2.5.4.bin",
        Language.ES,"opennlp-es-ud-gsd-pos-1.3-2.5.4.bin"
    );
    private final Map<Language,POSTaggerME> taggers=new EnumMap<>(Language.class);

    public OpenNlpPosService(){
        for(var e:RESOURCES.entrySet()){
            try(InputStream in=OpenNlpPosService.class.getClassLoader().getResourceAsStream(e.getValue())){
                if(in==null)throw new IllegalStateException("missing OpenNLP model resource "+e.getValue());
                taggers.put(e.getKey(),new POSTaggerME(new POSModel(in)));
            }catch(Exception ex){throw new IllegalStateException("cannot load "+e.getKey()+" POS model",ex);}
        }
    }

    public synchronized List<String> tag(Language language,List<WordSegmenter.Token> tokens){
        String[] values=tokens.stream().map(WordSegmenter.Token::text).toArray(String[]::new);
        return List.of(taggers.get(language).tag(values));
    }

    public Map<Language,String> resources(){return RESOURCES;}
}

