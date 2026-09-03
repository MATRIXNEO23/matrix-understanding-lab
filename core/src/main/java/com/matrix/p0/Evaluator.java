package com.matrix.p0;

import com.fasterxml.jackson.databind.ObjectMapper;
import com.fasterxml.jackson.databind.SerializationFeature;
import com.matrix.p0.Domain.*;

import java.io.IOException;
import java.nio.file.Files;
import java.nio.file.Path;
import java.util.*;
import java.util.function.Function;

public final class Evaluator {
    private Evaluator() {}

    public static Map<String, Object> evaluate(UnderstandingEngine engine, List<GoldCase> cases) {
        List<Map<String, Object>> rows = new ArrayList<>();
        List<Long> latencies = new ArrayList<>();
        int expectedClaims=0, predictedClaims=0, countExact=0, fields=0, fieldsCorrect=0;
        int spanExpected=0, spanPredicted=0, spanMatched=0, entityExpected=0, entityPredicted=0, entityMatched=0;
        int negExpected=0, negPredicted=0, negMatched=0, unknown=0, falseStructured=0, ownershipViolations=0, worldTruth=0;
        // cases, caseExact, fieldErrors, fields, fieldsCorrect, claimCountExact,
        // predictedClaims, unknownClaims, ownershipViolations, worldTruth
        Map<String, int[]> languageTotals = new LinkedHashMap<>();
        Map<String, int[]> splitTotals = new LinkedHashMap<>();
        Map<String, Integer> errorFamilies = new TreeMap<>();
        for (GoldCase c : cases) {
            long t0=System.nanoTime();
            Interpretation actual=engine.interpret(c.id(),c.language(),c.text(),c.context());
            latencies.add(System.nanoTime()-t0);
            expectedClaims+=c.expected().size(); predictedClaims+=actual.claims().size();
            if(c.expected().size()==actual.claims().size()) countExact++;
            int[] lt=languageTotals.computeIfAbsent(c.language().name().toLowerCase(Locale.ROOT),k->new int[10]);
            int[] st=splitTotals.computeIfAbsent(c.split(),k->new int[5]);
            lt[0]++;st[0]++;
            boolean rowExact=c.expected().size()==actual.claims().size();
            if(rowExact){lt[5]++;st[3]++;}
            int n=Math.min(c.expected().size(),actual.claims().size());
            List<String> errors=new ArrayList<>();
            for(int i=0;i<n;i++){
                Claim e=c.expected().get(i), a=actual.claims().get(i);
                List<Function<Claim,Object>> accessors=List.of(Claim::speaker,Claim::subject,Claim::target,Claim::owner,
                    Claim::perspective,Claim::dialogueAct,Claim::predicate,Claim::objectValue,Claim::polarity,
                    Claim::temporalRelation,Claim::claimKind);
                String[] names={"speaker","subject","target","owner","perspective","act","predicate","object","polarity","temporal","kind"};
                for(int f=0;f<accessors.size();f++){
                    fields++;lt[3]++;st[1]++; Object ev=accessors.get(f).apply(e), av=accessors.get(f).apply(a);
                    if(Objects.equals(norm(ev),norm(av))){fieldsCorrect++;lt[4]++;st[2]++;} else {rowExact=false;errors.add(names[f]+":"+ev+"!="+av);errorFamilies.merge(errorFamily(names[f]),1,Integer::sum);}
                }
                Set<String> es=spanKeys(e.sourceSpans()), as=spanKeys(a.sourceSpans());
                spanExpected+=es.size();spanPredicted+=as.size();spanMatched+=intersection(es,as);
                Set<String> ee=entityKeys(e.entities()),ae=entityKeys(a.entities());
                entityExpected+=ee.size();entityPredicted+=ae.size();entityMatched+=intersection(ee,ae);
                Set<String> en=tokenSet(e.negationScope()),an=tokenSet(a.negationScope());
                negExpected+=en.size();negPredicted+=an.size();negMatched+=intersection(en,an);
                if(!Objects.equals(e.owner(),a.owner())||!Objects.equals(e.perspective(),a.perspective())) {ownershipViolations++;lt[8]++;}
                if(a.worldTruth()) {worldTruth++;lt[9]++;}
                if(a.predicate().equals("speech.unresolved")) {unknown++;lt[7]++;}
                if(e.predicate().equals("speech.unresolved")&&!a.predicate().equals("speech.unresolved")) falseStructured++;
            }
            if(c.expected().size()!=actual.claims().size())errorFamilies.merge("segmentation",1,Integer::sum);
            if(rowExact){lt[1]++;st[4]++;} lt[2]+=errors.size();lt[6]+=actual.claims().size();
            Map<String,Object> row=new LinkedHashMap<>(); row.put("caseId",c.id());row.put("split",c.split());row.put("language",c.language().name().toLowerCase(Locale.ROOT));
            row.put("exact",rowExact);row.put("errors",errors);row.put("expectedClaims",c.expected().size());row.put("predictedClaims",actual.claims().size());
            row.put("prediction",actual); rows.add(row);
        }
        latencies.sort(Long::compare);
        Map<String,Object> metrics=new LinkedHashMap<>();
        metrics.put("engine",engine.id());metrics.put("status",engine.status());metrics.put("cases",cases.size());
        metrics.put("claimCountExact",ratio(countExact,cases.size()));metrics.put("fieldExact",ratio(fieldsCorrect,fields));
        metrics.put("spanF1",f1(spanMatched,spanPredicted,spanExpected));metrics.put("negationScopeF1",f1(negMatched,negPredicted,negExpected));
        metrics.put("entityTypeLinkF1",f1(entityMatched,entityPredicted,entityExpected));
        metrics.put("unknownRate",ratio(unknown,Math.max(1,predictedClaims)));metrics.put("falseStructuredClaimRate",ratio(falseStructured,Math.max(1,expectedClaims)));
        metrics.put("ownershipViolations",ownershipViolations);metrics.put("inventedWorldTruth",worldTruth);
        metrics.put("latencyNsP50",percentile(latencies,0.50));metrics.put("latencyNsP95",percentile(latencies,0.95));
        Map<String,Object> langs=new LinkedHashMap<>();
        String worstLanguage=null;double worstFieldExact=Double.POSITIVE_INFINITY;
        for(var entry:languageTotals.entrySet()){
            int[] v=entry.getValue();double languageFieldExact=ratio(v[4],v[3]);
            Map<String,Object> lm=new LinkedHashMap<>();lm.put("cases",v[0]);lm.put("caseExact",ratio(v[1],v[0]));
            lm.put("claimCountExact",ratio(v[5],v[0]));lm.put("fieldExact",languageFieldExact);lm.put("fieldErrors",v[2]);
            lm.put("unknownRate",ratio(v[7],Math.max(1,v[6])));lm.put("ownershipViolations",v[8]);lm.put("inventedWorldTruth",v[9]);
            langs.put(entry.getKey(),lm);if(languageFieldExact<worstFieldExact){worstFieldExact=languageFieldExact;worstLanguage=entry.getKey();}
        }
        metrics.put("languages",langs);metrics.put("worstLanguage",Map.of("language",worstLanguage,"fieldExact",worstFieldExact));
        Map<String,Object> splits=new LinkedHashMap<>();splitTotals.forEach((k,v)->splits.put(k,Map.of("cases",v[0],"fieldExact",ratio(v[2],v[1]),"claimCountExact",ratio(v[3],v[0]),"caseExact",ratio(v[4],v[0]))));
        metrics.put("splits",splits);metrics.put("errorFamilies",errorFamilies);
        metrics.put("criticalGate",Map.of("pass",ownershipViolations==0&&worldTruth==0,"ownershipTolerance",0,"worldTruthTolerance",0));
        metrics.put("rows",rows);return metrics;
    }

    public static void writeJson(Path path,Object value)throws IOException{
        Files.createDirectories(path.getParent());new ObjectMapper().enable(SerializationFeature.INDENT_OUTPUT).writeValue(path.toFile(),value);
    }
    private static Object norm(Object x){return x instanceof String s?s.trim().toLowerCase(Locale.ROOT):x;}
    private static Set<String> spanKeys(List<SourceSpan> spans){Set<String>s=new HashSet<>();for(SourceSpan x:spans)s.add(BaselineAEngine.normalize(x.text()));return s;}
    private static Set<String> entityKeys(List<EntityResolution> entities){Set<String>s=new HashSet<>();for(EntityResolution e:entities)s.add(BaselineAEngine.normalize(e.mention())+"|"+e.type()+"|"+e.link());return s;}
    private static Set<String> tokenSet(SourceSpan span){if(span==null)return Set.of();return new HashSet<>(Arrays.asList(BaselineAEngine.normalize(span.text()).split(" ")));}
    private static int intersection(Set<String>a,Set<String>b){Set<String>x=new HashSet<>(a);x.retainAll(b);return x.size();}
    private static double ratio(int n,int d){return d==0?1.0:(double)n/d;}
    private static double f1(int match,int predicted,int expected){if(predicted+expected==0)return 1.0;return (2.0*match)/(predicted+expected);}
    private static long percentile(List<Long>x,double p){if(x.isEmpty())return 0;return x.get(Math.min(x.size()-1,(int)Math.ceil(p*x.size())-1));}
    private static String errorFamily(String field){return switch(field){
        case "owner","perspective","speaker","subject","target" -> "ownership";
        case "predicate","object" -> "predicate_mapping";
        case "polarity" -> "negation";
        case "temporal" -> "temporality";
        case "act","kind" -> "dialogue_act";
        default -> "other";
    };}
}
