package com.matrix.p0.cli;

import com.matrix.p0.*;
import com.matrix.p0.Domain.GoldCase;

import java.nio.file.Path;
import java.util.*;

public final class Main {
    public static void main(String[] args) throws Exception {
        Path gold = Path.of(args.length > 0 ? args[0] : "gold/p0-gold-v1.json");
        Path out = Path.of(args.length > 1 ? args[1] : "build/results/p0-results.json");
        List<GoldCase> cases = GoldDataset.load(gold);
        List<UnderstandingEngine> engines=List.of(new BaselineAEngine(),new CandidateBEngine(new Icu4jWordSegmenter()));
        List<Map<String,Object>> results=new ArrayList<>();
        for(UnderstandingEngine engine:engines){
            Map<String,Object> result=Evaluator.evaluate(engine,cases);results.add(result);
            System.out.printf("engine=%s status=%s cases=%s claimCountExact=%.4f fieldExact=%.4f ownership=%s worldTruth=%s%n",
                result.get("engine"),result.get("status"),result.get("cases"),result.get("claimCountExact"),result.get("fieldExact"),
                result.get("ownershipViolations"),result.get("inventedWorldTruth"));
        }
        Map<String,Object> report=new LinkedHashMap<>();report.put("schemaVersion","p0.results.v1");report.put("gold","p0.gold.v1");
        report.put("candidateC",Map.of("status","CANDIDATE_C_RESEARCH_PENDING"));report.put("candidates",results);
        report.put("jvm",Map.of("java",System.getProperty("java.version"),"maxHeapBytes",Runtime.getRuntime().maxMemory(),"classpathBytes",classpathBytes()));
        Evaluator.writeJson(out,report);
    }

    private static long classpathBytes(){long total=0;for(String entry:System.getProperty("java.class.path","").split(java.io.File.pathSeparator)){try{Path p=Path.of(entry);if(java.nio.file.Files.isRegularFile(p))total+=java.nio.file.Files.size(p);}catch(Exception ignored){}}return total;}
}
