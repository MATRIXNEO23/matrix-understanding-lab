package com.matrix.p0.cli;

import com.matrix.p0.*;
import com.matrix.p0.Domain.GoldCase;

import java.nio.file.Path;
import java.util.List;
import java.util.Map;

public final class Main {
    public static void main(String[] args) throws Exception {
        Path gold = Path.of(args.length > 0 ? args[0] : "gold/p0-gold-v1.json");
        Path out = Path.of(args.length > 1 ? args[1] : "build/results/baseline-a.json");
        List<GoldCase> cases = GoldDataset.load(gold);
        Map<String,Object> result = Evaluator.evaluate(new BaselineAEngine(), cases);
        Evaluator.writeJson(out,result);
        System.out.printf("engine=%s cases=%s claimCountExact=%.4f fieldExact=%.4f ownership=%s worldTruth=%s%n",
            result.get("engine"),result.get("cases"),result.get("claimCountExact"),result.get("fieldExact"),
            result.get("ownershipViolations"),result.get("inventedWorldTruth"));
    }
}

