package com.matrix.p0;

import com.matrix.p0.Domain.*;
import com.matrix.p0.WordSegmenter.Token;

import java.text.Normalizer;
import java.util.*;
import java.util.regex.Matcher;
import java.util.regex.Pattern;

/** ICU boundaries + OpenNLP UD POS evidence + a bounded Matrix semantic mapper. */
public final class CandidateBEngine implements UnderstandingEngine {
    private final WordSegmenter segmenter;
    private final OpenNlpPosService pos;

    public CandidateBEngine(WordSegmenter segmenter){this.segmenter=segmenter;this.pos=new OpenNlpPosService();}
    @Override public String id(){return "B_ICU_OPENNLP_MATRIX";}
    @Override public String status(){return "LAB_ONLY_LICENSE_BLOCKED";}

    @Override public Interpretation interpret(String caseId,Language language,String text,Context context){
        List<Slice> slices=split(language,text);
        List<Claim> claims=new ArrayList<>();List<String> diagnostics=new ArrayList<>();
        for(Slice s:slices){
            List<Token> tokens=segmenter.segment(language,s.text());List<String> tags=pos.tag(language,tokens);
            claims.add(map(caseId,language,text,s,tokens,tags,context));
            diagnostics.add("slice="+s.text()+"; tokens="+tokens.stream().map(Token::text).toList()+"; pos="+tags);
        }
        diagnostics.add("segmenter="+segmenter.implementation());
        return new Interpretation(id(),status(),List.copyOf(claims),List.copyOf(diagnostics));
    }

    private Claim map(String caseId,Language language,String full,Slice slice,List<Token> tokens,List<String> tags,Context context){
        String raw=slice.text().trim(), n=norm(raw);String[] words=n.split(" ");
        DialogueAct act=dialogueAct(language,raw,n,tags);
        ClaimKind kind=act==DialogueAct.HYPOTHESIS?ClaimKind.HYPOTHESIS:ClaimKind.EXPLICIT;
        Predicate p=predicate(language,raw,n,tokens,tags,act);
        String subject=subject(language,raw,context);
        String owner=subject,perspective=context.speaker();
        String target=act==DialogueAct.REQUEST?"SELF":null;
        String object=p.object().trim();
        Polarity polarity=p.predicate().equals("speech.unresolved")||act==DialogueAct.QUESTION||act==DialogueAct.REQUEST?Polarity.UNKNOWN:
            isNegative(language,n,p.marker())?Polarity.NEGATIVE:Polarity.POSITIVE;
        SourceSpan source=span(full,raw,slice.start());
        SourceSpan neg=polarity==Polarity.NEGATIVE?negation(language,full,raw,slice.start(),p):null;
        Temporal temporal=temporal(language,n,p.predicate());
        List<EntityResolution> entities=entities(language,full,raw,slice.start(),tokens,tags,p,object,subject,context);
        return new Claim(context.speaker(),subject,target,owner,perspective,act,p.predicate(),object,polarity,neg,
            temporal.relation(),temporal.expression(),entities,kind,p.predicate().equals("speech.unresolved")?0.45:0.88,
            List.of(source),List.of("observation:"+caseId),false);
    }

    private List<Slice> split(Language language,String text){
        String conjunction=language==Language.IT?"e":language==Language.EN?"and":"y";
        Pattern pattern=Pattern.compile("(?iu)\\s+(?:"+conjunction+"|,|;)\\s+");Matcher m=pattern.matcher(text);
        List<Slice> out=new ArrayList<>();int start=0;
        while(m.find()){
            String left=text.substring(start,m.start()).trim(),right=text.substring(m.end()).trim();
            if(looksLikePredicate(language,left)&&looksLikePredicate(language,right)){
                int at=text.indexOf(left,start);out.add(new Slice(left,at));start=m.end();
            }
        }
        String tail=text.substring(start).trim();if(!tail.isEmpty())out.add(new Slice(tail,text.indexOf(tail,start)));
        return out;
    }

    private boolean looksLikePredicate(Language l,String raw){
        String n=norm(raw);
        return switch(l){
            case IT -> n.matches(".*\\b(mi chiamo|sono|ho|lavoro|lavora|vivo|vive|vivevo|abitavo|abito|amo|mi piace|vorrei)\\b.*")||n.matches(".*\\b\\d{1,3} anni\\b.*");
            case EN -> n.matches(".*\\b(my name is|am|is|have|own|work|works|live|lives|like|love|would like)\\b.*")||n.matches(".*\\b\\d{1,3} years? old\\b.*");
            case ES -> n.matches(".*\\b(me llamo|soy|estoy|tengo|trabajo|trabaja|vivo|vive|vivia|gusta|gustan|amo|gustaria)\\b.*")||n.matches(".*\\b\\d{1,3} anos?\\b.*");
        };
    }

    private Predicate predicate(Language l,String raw,String n,List<Token> tokens,List<String> tags,DialogueAct act){
        if(act==DialogueAct.REQUEST)return new Predicate("speech.unresolved",raw,"");
        if(act==DialogueAct.QUESTION&&containsLiveVerb(l,n))return new Predicate("residence.place","",liveMarker(l,n));
        Matcher age=Pattern.compile("\\b(\\d{1,3})\\s+(?:anni|years? old|anos?)\\b").matcher(n);
        if(age.find())return new Predicate("identity.age",age.group(1),age.group());
        List<String> nameMarkers=switch(l){case IT->List.of("mi chiamo");case EN->List.of("my name is");case ES->List.of("me llamo");};
        for(String m:nameMarkers)if(n.contains(m))return new Predicate("identity.name",after(raw,m),m);
        for(String m:workMarkers(l))if(n.contains(m))return new Predicate("work.role",after(raw,m),m);
        for(String m:residenceMarkers(l))if(containsPhrase(n,m))return new Predicate("residence.place",afterLocation(raw,m,l),m);
        for(String m:presenceMarkers(l))if(containsPhrase(n,m))return new Predicate("presence.reported",after(raw,m),m);
        for(String m:preferenceMarkers(l))if(containsPhrase(n,m))return new Predicate("preference.like",after(raw,m),m);
        for(String m:goalMarkers(l))if(containsPhrase(n,m))return new Predicate("goal.object",after(raw,m),m);
        for(String m:possessionMarkers(l))if(containsPhrase(n,m))return new Predicate("possession.has",after(raw,m),m);
        Copula cop=copula(l,n,tokens,tags);
        if(cop!=null)return new Predicate(cop.proper()?"identity.name":"attribute.is",cop.object(),cop.marker());
        return new Predicate("speech.unresolved",raw,"");
    }

    private Copula copula(Language l,String n,List<Token> tokens,List<String> tags){
        List<String> markers=switch(l){case IT->List.of("sono ");case EN->List.of("i am ");case ES->List.of("soy ");};
        for(String marker:markers){if(n.startsWith(marker)){
            String object=n.substring(marker.length()).trim();int idx=Math.max(0,tokens.size()-1);
            boolean proper=idx<tags.size()&&tags.get(idx).equals("PROPN");
            if(!proper&&!tokens.isEmpty()){String original=tokens.get(idx).text();proper=Character.isUpperCase(original.codePointAt(0));}
            return new Copula(objectFromRawEnd(tokens,idx,object),marker.trim(),proper);
        }}return null;
    }

    private String subject(Language l,String raw,Context c){
        for(var e:c.knownEntities().entrySet())if(BaselineAEngine.containsWord(raw,e.getKey()))return e.getValue();
        String n=norm(raw);Set<String> pronouns=switch(l){case IT->Set.of("lei","lui");case EN->Set.of("she","he","they");case ES->Set.of("ella","el");};
        if(Arrays.stream(n.split(" ")).anyMatch(pronouns::contains)&&!c.recentEntityRefs().isEmpty())return c.recentEntityRefs().get(0);
        return c.speaker();
    }

    private List<EntityResolution> entities(Language l,String full,String raw,int offset,List<Token> tokens,List<String> tags,
                                            Predicate p,String object,String subject,Context c){
        List<EntityResolution> out=new ArrayList<>();
        for(var e:c.knownEntities().entrySet()){int x=idx(raw,e.getKey());if(x>=0)out.add(entity(e.getKey(),"PERSON",e.getValue(),"world_registry",full,offset+x));}
        String first=norm(raw).split(" ")[0];Set<String> pronouns=switch(l){case IT->Set.of("lei","lui");case EN->Set.of("she","he","they");case ES->Set.of("ella","el");};
        if(pronouns.contains(first)&&!c.recentEntityRefs().isEmpty()){int x=idx(raw,raw.split("\\s+")[0]);out.add(entity(raw.split("\\s+")[0],"PERSON",c.recentEntityRefs().get(0),"recent_reference",full,offset+Math.max(0,x)));}
        if(p.predicate().equals("identity.name")){int x=Math.max(0,idx(raw,object));out.add(entity(object,"PERSON",c.speaker(),"identity_argument",full,offset+x));}
        if(p.predicate().equals("residence.place")||p.predicate().equals("presence.reported")){
            String mention=stripLeadingArticle(object,l,true);int x=Math.max(0,idx(raw,mention));out.add(entity(mention,"LOCATION","LOCATION:"+BaselineAEngine.slug(mention),"predicate_location_argument",full,offset+x));
        }
        if(p.predicate().equals("goal.object")){
            for(int i=0;i<tokens.size();i++)if(tags.get(i).equals("PROPN")){String mention=tokens.get(i).text();int x=idx(raw,mention);out.add(entity(mention,"LOCATION","LOCATION:"+BaselineAEngine.slug(mention),"goal_location_hint",full,offset+Math.max(0,x)));}
        }
        return List.copyOf(out);
    }

    private DialogueAct dialogueAct(Language l,String raw,String n,List<String> tags){
        Set<String> questions=switch(l){case IT->Set.of("dove","come","chi","cosa","quando");case EN->Set.of("where","how","who","what","when");case ES->Set.of("donde","como","quien","que","cuando");};
        String first=n.split(" ")[0];if(raw.trim().endsWith("?")||questions.contains(first))return DialogueAct.QUESTION;
        for(String x:correctionMarkers(l))if(n.startsWith(x))return DialogueAct.CORRECT;
        for(String x:hypothesisMarkers(l))if(n.startsWith(x))return DialogueAct.HYPOTHESIS;
        if(!tags.isEmpty()&&tags.get(0).equals("VERB")&&!firstPersonStart(l,n)&&!looksLikePredicate(l,raw))return DialogueAct.REQUEST;
        return DialogueAct.ASSERT;
    }

    private boolean isNegative(Language l,String n,String marker){return switch(l){case IT->n.contains("non ")||marker.equals("odio")||marker.equals("detesto");case EN->n.contains(" not ")||n.startsWith("not ")||n.contains("don't ")||n.contains("do not ");case ES->n.startsWith("no ")||n.contains(" no ");};}
    private SourceSpan negation(Language l,String full,String raw,int offset,Predicate p){String key=l==Language.EN&&norm(raw).contains("not ")?"not":l==Language.IT?"non":"no";int local=idx(raw,key);if(local<0)local=0;int end=raw.length();String value=raw.substring(local,end);return new SourceSpan(offset+local,offset+end,value);}
    private Temporal temporal(Language l,String n,String predicate){
        List<String> past=switch(l){case IT->List.of("prima","vivevo","abitavo");case EN->List.of("used to","previously");case ES->List.of("antes","vivia");};
        for(String x:past)if(n.contains(x))return new Temporal(TemporalRelation.PAST,displayToken(n,x));
        List<String> future=switch(l){case IT->List.of("domani");case EN->List.of("tomorrow");case ES->List.of("manana");};
        for(String x:future)if(n.contains(x))return new Temporal(TemporalRelation.FUTURE,displayToken(n,x));
        if(predicate.equals("identity.name")||predicate.equals("preference.like")||predicate.equals("speech.unresolved"))return new Temporal(TemporalRelation.ATEMPORAL,null);
        return new Temporal(TemporalRelation.CURRENT,null);
    }

    private static List<String> workMarkers(Language l){return switch(l){case IT->List.of("lavoro come","lavora come");case EN->List.of("work as","works as");case ES->List.of("trabajo como","trabaja como");};}
    private static List<String> residenceMarkers(Language l){return switch(l){case IT->List.of("vivo a","vive a","vivevo a","abitavo a","abito a");case EN->List.of("live in","lives in","used to live in");case ES->List.of("vivo en","vive en","vivia en");};}
    private static List<String> presenceMarkers(Language l){return switch(l){case IT->List.of("sono al","sono alla","sono a");case EN->List.of("i am at","is at");case ES->List.of("estoy en","esta en");};}
    private static List<String> preferenceMarkers(Language l){return switch(l){case IT->List.of("non sopporto","mi piace","amo","odio","detesto");case EN->List.of("do not like","don't like","like","love","hate");case ES->List.of("no me gustan","no me gusta","me gustan","me gusta","amo","odio");};}
    private static List<String> goalMarkers(Language l){return switch(l){case IT->List.of("vorrei");case EN->List.of("would like");case ES->List.of("me gustaria");};}
    private static List<String> possessionMarkers(Language l){return switch(l){case IT->List.of("ho");case EN->List.of("i own","i have");case ES->List.of("tengo");};}
    private static List<String> correctionMarkers(Language l){return switch(l){case IT->List.of("in realta","anzi");case EN->List.of("actually","in fact");case ES->List.of("en realidad","de hecho");};}
    private static List<String> hypothesisMarkers(Language l){return switch(l){case IT->List.of("forse","credo che");case EN->List.of("maybe","perhaps","i think");case ES->List.of("quiza","quizas","tal vez");};}
    private static boolean firstPersonStart(Language l,String n){return switch(l){case IT->n.startsWith("io ")||n.startsWith("mi ")||n.startsWith("sono ")||n.startsWith("ho ");case EN->n.startsWith("i ")||n.startsWith("my ");case ES->n.startsWith("yo ")||n.startsWith("me ")||n.startsWith("soy ")||n.startsWith("tengo ");};}
    private static boolean containsLiveVerb(Language l,String n){return switch(l){case IT->n.contains("vive");case EN->n.contains("live");case ES->n.contains("vive");};}
    private static String liveMarker(Language l,String n){return l==Language.IT?"vive":l==Language.EN?"live":"vive";}
    private static String afterLocation(String raw,String marker,Language l){return after(raw,marker);}
    private static String after(String raw,String marker){int p=idx(norm(raw),norm(marker));if(p<0)return raw;String normalizedPrefix=norm(raw).substring(0,p+norm(marker).length());int words=normalizedPrefix.isBlank()?0:normalizedPrefix.split(" ").length;String[] original=raw.trim().split("\\s+");return String.join(" ",Arrays.copyOfRange(original,Math.min(words,original.length),original.length)).replaceAll("^[,;]+|[?.!,;]+$","").trim();}
    private static String stripLeadingArticle(String s,Language l,boolean location){String regex=switch(l){case IT->location?"(?iu)^(?:il|lo|la|i|gli|le)\\s+":"(?iu)^(?:il|lo|la|i|gli|le)\\s+";case EN->"(?iu)^(?:the)\\s+";case ES->"(?iu)^(?:el|la|los|las)\\s+";};return s.replaceFirst(regex,"");}
    private static String objectFromRawEnd(List<Token> tokens,int idx,String fallback){return idx<tokens.size()?tokens.get(idx).text():fallback;}
    private static String displayToken(String n,String x){return x.equals("manana")?"Mañana":Character.toUpperCase(x.charAt(0))+x.substring(1);}
    private static String norm(String s){return Normalizer.normalize(s,Normalizer.Form.NFD).replaceAll("\\p{M}+","").toLowerCase(Locale.ROOT).replaceAll("[^\\p{L}\\p{N}']+"," ").trim();}
    private static boolean containsPhrase(String n,String p){return (" "+n+" ").contains(" "+p+" ");}
    private static int idx(String s,String p){return s.toLowerCase(Locale.ROOT).indexOf(p.toLowerCase(Locale.ROOT));}
    private static SourceSpan span(String full,String raw,int hint){int p=full.indexOf(raw,Math.max(0,hint));if(p<0)p=hint;return new SourceSpan(p,Math.min(full.length(),p+raw.length()),raw);}
    private static EntityResolution entity(String mention,String type,String link,String method,String full,int start){return new EntityResolution(mention,type,link,method,0.95,new SourceSpan(start,Math.min(full.length(),start+mention.length()),mention));}
    private record Slice(String text,int start){}
    private record Predicate(String predicate,String object,String marker){}
    private record Copula(String object,String marker,boolean proper){}
    private record Temporal(TemporalRelation relation,String expression){}
}
