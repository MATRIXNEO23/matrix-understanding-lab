package com.matrix.p0.cli;

import com.matrix.p0.*;
import com.matrix.p0.Domain.GoldCase;

import java.nio.file.Path;
import java.nio.file.Files;
import java.nio.charset.StandardCharsets;
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
        report.put("candidateC",Map.of(
            "status","CANDIDATE_C_NOT_READY",
            "gate07","SKIPPED_BY_SPEC",
            "reason","No compact reproducible IT/EN/ES model emits the frozen Matrix claim contract; no metrics fabricated."));
        report.put("candidates",results);
        report.put("jvm",Map.of("java",System.getProperty("java.version"),"maxHeapBytes",Runtime.getRuntime().maxMemory(),"classpathBytes",classpathBytes(),
            "measurementScope","CI JVM wall-clock microbenchmark; not Android PSS/CPU/thermal"));
        Evaluator.writeJson(out,report);
        writeMarkdown(out.resolveSibling("p0-results.md"),results,report);
    }

    private static long classpathBytes(){long total=0;for(String entry:System.getProperty("java.class.path","").split(java.io.File.pathSeparator)){try{Path p=Path.of(entry);if(java.nio.file.Files.isRegularFile(p))total+=java.nio.file.Files.size(p);}catch(Exception ignored){}}return total;}

    @SuppressWarnings("unchecked")
    private static void writeMarkdown(Path path,List<Map<String,Object>> results,Map<String,Object> report)throws Exception{
        StringBuilder s=new StringBuilder("# P0 unified benchmark results\n\n");
        s.append("Gold: `p0.gold.v1` (same frozen 66 variants for every executable candidate).\n\n");
        s.append("| Candidate | Status | Field exact | Worst language | Claim-count exact | Span F1 | Negation F1 | Entity F1 | Ownership violations | World Truth | p50 ns | p95 ns |\n");
        s.append("|---|---|---:|---|---:|---:|---:|---:|---:|---:|---:|---:|\n");
        for(Map<String,Object> r:results){
            Map<String,Object>w=(Map<String,Object>)r.get("worstLanguage");
            s.append(String.format(Locale.ROOT,"| %s | %s | %.4f | %s (%.4f) | %.4f | %.4f | %.4f | %.4f | %s | %s | %s | %s |%n",
                r.get("engine"),r.get("status"),r.get("fieldExact"),w.get("language"),w.get("fieldExact"),r.get("claimCountExact"),r.get("spanF1"),r.get("negationScopeF1"),r.get("entityTypeLinkF1"),r.get("ownershipViolations"),r.get("inventedWorldTruth"),r.get("latencyNsP50"),r.get("latencyNsP95")));
        }
        Map<String,Object> c=(Map<String,Object>)report.get("candidateC");
        s.append("| C_ONNX_COMPACT | ").append(c.get("status")).append(" | — | — | — | — | — | — | — | — | — | — |\n\n");
        s.append("Candidate C has no quality or footprint values because Gate 06 found no valid model; this is not scored as zero.\n\n");
        s.append("Latency is a single CI/JVM wall-clock diagnostic, not a Moto G56 measurement. Confidence values are scores, not calibrated probabilities.\n");
        Files.createDirectories(path.getParent());Files.writeString(path,s.toString(),StandardCharsets.UTF_8);
    }
}
