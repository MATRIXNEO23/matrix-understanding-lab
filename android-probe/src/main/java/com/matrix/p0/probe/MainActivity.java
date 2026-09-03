package com.matrix.p0.probe;

import android.app.Activity;
import android.os.Build;
import android.os.Bundle;
import android.os.Debug;
import android.os.PowerManager;
import android.os.SystemClock;
import android.view.ViewGroup;
import android.widget.ScrollView;
import android.widget.TextView;

import com.fasterxml.jackson.databind.ObjectMapper;
import com.matrix.p0.BaselineAEngine;
import com.matrix.p0.CandidateBEngine;
import com.matrix.p0.Domain.GoldCase;
import com.matrix.p0.Evaluator;
import com.matrix.p0.GoldDataset;
import com.matrix.p0.UnderstandingEngine;

import java.io.File;
import java.io.InputStream;
import java.util.ArrayList;
import java.util.Collections;
import java.util.LinkedHashMap;
import java.util.List;
import java.util.Map;
import java.util.concurrent.Executors;

/** Manual, offline-only footprint probe for a physical Moto G56. */
public final class MainActivity extends Activity {
    private static final int WARMUP_LOOPS = 3;
    private static final int MEASURED_LOOPS = 20;
    private TextView output;

    @Override
    protected void onCreate(Bundle state) {
        super.onCreate(state);
        output = new TextView(this);
        output.setPadding(24, 24, 24, 24);
        output.setText("Matrix P0 probe in esecuzione. Tenere l'app in primo piano…");
        ScrollView scroll = new ScrollView(this);
        scroll.addView(output, new ScrollView.LayoutParams(
            ViewGroup.LayoutParams.MATCH_PARENT, ViewGroup.LayoutParams.WRAP_CONTENT));
        setContentView(scroll);
        Executors.newSingleThreadExecutor().execute(this::runProbe);
    }

    private void runProbe() {
        try {
            List<GoldCase> cases;
            try (InputStream input = getAssets().open("p0-gold-v1.json")) {
                cases = GoldDataset.load(input);
            }

            long pssBeforeKb = Debug.getPss();
            ProbeResult baseline = measure(new BaselineAEngine(), cases, false);

            long initWallStart = SystemClock.elapsedRealtimeNanos();
            long initCpuStart = Debug.threadCpuTimeNanos();
            CandidateBEngine candidate = new CandidateBEngine(new PlatformIcuWordSegmenter());
            long initCpuNs = Debug.threadCpuTimeNanos() - initCpuStart;
            long initWallNs = SystemClock.elapsedRealtimeNanos() - initWallStart;
            long pssAfterInitKb = Debug.getPss();
            ProbeResult candidateResult = measure(candidate, cases, true);

            Map<String, Object> report = new LinkedHashMap<>();
            report.put("schemaVersion", "p0.mobile.probe.v1");
            report.put("gold", "p0.gold.v1");
            report.put("device", Map.of(
                "manufacturer", Build.MANUFACTURER,
                "model", Build.MODEL,
                "device", Build.DEVICE,
                "sdk", Build.VERSION.SDK_INT,
                "abis", List.of(Build.SUPPORTED_ABIS)
            ));
            report.put("offline", true);
            report.put("networkPermissionDeclared", false);
            report.put("loops", Map.of("warmup", WARMUP_LOOPS, "measured", MEASURED_LOOPS,
                "casesPerLoop", cases.size()));
            report.put("processPssKbBeforeEngines", pssBeforeKb);
            report.put("candidateBInitWallNs", initWallNs);
            report.put("candidateBInitThreadCpuNs", initCpuNs);
            report.put("candidateBPssKbAfterInit", pssAfterInitKb);
            report.put("candidateBInitDeltaPssKb", pssAfterInitKb - pssBeforeKb);
            report.put("baselineA", baseline.toMap());
            report.put("candidateB", candidateResult.toMap());
            report.put("candidateBQuality", Evaluator.evaluate(candidate, cases));
            report.put("measurementNotes", List.of(
                "PSS is process PSS sampled with android.os.Debug.getPss().",
                "CPU is worker-thread CPU time; wall latency uses elapsedRealtimeNanos().",
                "The baseline and Candidate B run in one process; B delta is diagnostic, not isolated-process PSS.",
                "Confidence scores are not calibrated probabilities."
            ));

            File dir = getExternalFilesDir(null);
            if (dir == null) dir = getFilesDir();
            File file = new File(dir, "p0-mobile-probe.json");
            new ObjectMapper().writerWithDefaultPrettyPrinter().writeValue(file, report);
            String message = "PASS — probe completato\n\n" +
                "Output: " + file.getAbsolutePath() + "\n" +
                "B init wall: " + initWallNs + " ns\n" +
                "B init delta PSS: " + (pssAfterInitKb - pssBeforeKb) + " KB\n" +
                "B warm p50/p95: " + candidateResult.wallP50Ns + " / " + candidateResult.wallP95Ns + " ns\n" +
                "B peak PSS: " + candidateResult.peakPssKb + " KB\n" +
                "Thermal start/end/max: " + candidateResult.thermalStart + " / " +
                candidateResult.thermalEnd + " / " + candidateResult.thermalMax + "\n\n" +
                "Estrarre il JSON con adb come descritto in docs/MOBILE_PROBE.md.";
            runOnUiThread(() -> output.setText(message));
        } catch (Throwable failure) {
            runOnUiThread(() -> output.setText("FAIL — " + failure.getClass().getName() + ": " + failure.getMessage()));
        }
    }

    private ProbeResult measure(UnderstandingEngine engine, List<GoldCase> cases, boolean samplePss) {
        for (int loop = 0; loop < WARMUP_LOOPS; loop++) runLoop(engine, cases, null, null);
        List<Long> wall = new ArrayList<>(MEASURED_LOOPS * cases.size());
        List<Long> cpu = new ArrayList<>(MEASURED_LOOPS * cases.size());
        long peakPssKb = Debug.getPss();
        int thermalStart = thermalStatus();
        int thermalMax = thermalStart;
        for (int loop = 0; loop < MEASURED_LOOPS; loop++) {
            runLoop(engine, cases, wall, cpu);
            if (samplePss) peakPssKb = Math.max(peakPssKb, Debug.getPss());
            thermalMax = Math.max(thermalMax, thermalStatus());
        }
        return new ProbeResult(percentile(wall, 0.50), percentile(wall, 0.95),
            percentile(cpu, 0.50), percentile(cpu, 0.95), peakPssKb,
            thermalStart, thermalStatus(), thermalMax);
    }

    private static void runLoop(UnderstandingEngine engine, List<GoldCase> cases,
                                List<Long> wall, List<Long> cpu) {
        for (GoldCase item : cases) {
            long wallStart = SystemClock.elapsedRealtimeNanos();
            long cpuStart = Debug.threadCpuTimeNanos();
            engine.interpret(item.id(), item.language(), item.text(), item.context());
            long cpuNs = Debug.threadCpuTimeNanos() - cpuStart;
            long wallNs = SystemClock.elapsedRealtimeNanos() - wallStart;
            if (wall != null) wall.add(wallNs);
            if (cpu != null) cpu.add(cpuNs);
        }
    }

    private int thermalStatus() {
        if (Build.VERSION.SDK_INT < 29) return -1;
        PowerManager manager = getSystemService(PowerManager.class);
        return manager == null ? -1 : manager.getCurrentThermalStatus();
    }

    private static long percentile(List<Long> values, double quantile) {
        if (values.isEmpty()) return 0;
        List<Long> sorted = new ArrayList<>(values);
        Collections.sort(sorted);
        int index = (int) Math.ceil(quantile * sorted.size()) - 1;
        return sorted.get(Math.max(0, Math.min(index, sorted.size() - 1)));
    }

    private record ProbeResult(long wallP50Ns, long wallP95Ns, long cpuP50Ns, long cpuP95Ns,
                               long peakPssKb, int thermalStart, int thermalEnd, int thermalMax) {
        Map<String, Object> toMap() {
            Map<String, Object> out = new LinkedHashMap<>();
            out.put("wallLatencyP50Ns", wallP50Ns);
            out.put("wallLatencyP95Ns", wallP95Ns);
            out.put("threadCpuP50Ns", cpuP50Ns);
            out.put("threadCpuP95Ns", cpuP95Ns);
            out.put("peakProcessPssKb", peakPssKb);
            out.put("thermalStatusStart", thermalStart);
            out.put("thermalStatusEnd", thermalEnd);
            out.put("thermalStatusMax", thermalMax);
            return out;
        }
    }
}
