package com.matrix.p05.train;

import com.fasterxml.jackson.databind.ObjectMapper;
import com.fasterxml.jackson.databind.SerializationFeature;
import opennlp.tools.postag.POSModel;
import opennlp.tools.postag.POSSample;
import opennlp.tools.postag.POSTaggerFactory;
import opennlp.tools.postag.POSTaggerME;
import opennlp.tools.util.ObjectStream;
import opennlp.tools.util.Parameters;
import opennlp.tools.util.TrainingParameters;
import opennlp.tools.util.model.ModelType;

import java.io.ByteArrayOutputStream;
import java.io.IOException;
import java.net.HttpURLConnection;
import java.nio.charset.StandardCharsets;
import java.nio.file.Files;
import java.nio.file.Path;
import java.security.MessageDigest;
import java.time.Instant;
import java.util.ArrayList;
import java.util.Comparator;
import java.util.LinkedHashMap;
import java.util.List;
import java.util.Locale;
import java.util.Map;

/** Reproducible source-to-model pipeline for the clean Italian P0.5 POS artifact. */
public final class TrainItalianPos {
    static final String SELECTED_RESOURCE = "opennlp-it-ud-markit-pos-p05.bin";
    static final long ORDER_SEED = 20260903L;

    private TrainItalianPos() {}

    public static void main(String[] args) throws Exception {
        if (args.length != 1) throw new IllegalArgumentException("usage: TrainItalianPos <output-dir>");
        Path root = Path.of(args[0]).toAbsolutePath().normalize();
        Path sourceDir = root.resolve("sources");
        Path normalizedDir = root.resolve("normalized");
        Path modelDir = root.resolve("models");
        Path generatedDir = root.resolve("generated-resources");
        Files.createDirectories(sourceDir);
        Files.createDirectories(normalizedDir);
        Files.createDirectories(modelDir);
        Files.createDirectories(generatedDir);

        Map<String, byte[]> sourceBytes = new LinkedHashMap<>();
        List<Map<String, Object>> sourceRecords = new ArrayList<>();
        for (SourceManifest.Source source : SourceManifest.SOURCES) {
            byte[] bytes = fetch(source);
            sourceBytes.put(source.role(), bytes);
            Files.write(sourceDir.resolve(source.fileName()), bytes);
            sourceRecords.add(sourceRecord(source, bytes));
        }

        Map<String, List<POSSample>> splits = new LinkedHashMap<>();
        List<Map<String, Object>> splitRecords = new ArrayList<>();
        for (String split : List.of("train", "dev", "test")) {
            List<POSSample> samples = ConlluCorpus.parse(sourceBytes.get(split));
            splits.put(split, samples);
            Path normalized = normalizedDir.resolve("it_markit-" + split + ".pos.tsv");
            ConlluCorpus.writeNormalized(normalized, samples);
            splitRecords.add(Map.of(
                "split", split,
                "sentences", samples.size(),
                "tokens", ConlluCorpus.tokenCount(samples),
                "normalizedSha256", sha256(Files.readAllBytes(normalized))
            ));
        }

        List<VariantSpec> specs = List.of(
            new VariantSpec("maxent-i100-c1", ModelType.MAXENT, 100, 1),
            new VariantSpec("maxent-i200-c1", ModelType.MAXENT, 200, 1),
            new VariantSpec("perceptron-i100-c1", ModelType.PERCEPTRON, 100, 1)
        );
        List<TrainedVariant> variants = new ArrayList<>();
        for (VariantSpec spec : specs) {
            POSModel model = train(splits.get("train"), spec);
            byte[] bytes = serialize(model);
            Path modelPath = modelDir.resolve("opennlp-it-markit-" + spec.id() + ".bin");
            Files.write(modelPath, bytes);
            variants.add(new TrainedVariant(spec, model, bytes, accuracy(model, splits.get("dev"))));
        }
        variants.sort(Comparator.comparingDouble(TrainedVariant::devAccuracy).reversed()
            .thenComparingInt(v -> v.bytes().length).thenComparing(v -> v.spec().id()));
        TrainedVariant selected = variants.get(0);
        double testAccuracy = accuracy(selected.model(), splits.get("test"));
        Path selectedPath = generatedDir.resolve(SELECTED_RESOURCE);
        Files.write(selectedPath, selected.bytes());
        Files.writeString(generatedDir.resolve("MARKIT-CC-BY-4.0.txt"),
            new String(sourceBytes.get("license"), StandardCharsets.UTF_8), StandardCharsets.UTF_8);

        List<Map<String, Object>> experimentRecords = new ArrayList<>();
        for (TrainedVariant variant : variants) {
            experimentRecords.add(Map.of(
                "id", variant.spec().id(),
                "algorithm", variant.spec().type().name(),
                "iterations", variant.spec().iterations(),
                "cutoff", variant.spec().cutoff(),
                "devTokenAccuracy", variant.devAccuracy(),
                "bytes", variant.bytes().length,
                "sha256", sha256(variant.bytes()),
                "selected", variant == selected
            ));
        }
        Map<String, Object> manifest = new LinkedHashMap<>();
        manifest.put("schemaVersion", "p05.training.v1");
        manifest.put("generatedAt", Instant.now().toString());
        manifest.put("pipeline", "pinned-download -> git-blob-verify -> conllu-normalize -> OpenNLP-train -> dev-select -> frozen-test");
        manifest.put("tool", Map.of("java", System.getProperty("java.version"), "opennlp", "2.5.11"));
        manifest.put("dataset", Map.of(
            "name", "UD Italian MarkIT",
            "upstreamCommit", SourceManifest.UPSTREAM_COMMIT,
            "license", "CC BY 4.0",
            "attribution", "Teresa Paccosi; Alessio Palmero Aprosio; Sara Tonelli"
        ));
        manifest.put("sources", sourceRecords);
        manifest.put("splits", splitRecords);
        manifest.put("trainingOrder", "upstream order; no shuffle");
        manifest.put("seed", ORDER_SEED);
        manifest.put("experiments", experimentRecords);
        manifest.put("selectionRule", "highest dev token accuracy; then smaller bytes; then lexical id");
        manifest.put("selected", Map.of(
            "id", selected.spec().id(),
            "resource", SELECTED_RESOURCE,
            "sha256", sha256(selected.bytes()),
            "bytes", selected.bytes().length,
            "devTokenAccuracy", selected.devAccuracy(),
            "testTokenAccuracy", testAccuracy
        ));
        new ObjectMapper().enable(SerializationFeature.INDENT_OUTPUT)
            .writeValue(root.resolve("training-manifest.json").toFile(), manifest);

        System.out.printf(Locale.ROOT,
            "P05_TRAINING_OK selected=%s dev=%.6f test=%.6f bytes=%d sha256=%s%n",
            selected.spec().id(), selected.devAccuracy(), testAccuracy, selected.bytes().length,
            sha256(selected.bytes()));
    }

    static POSModel train(List<POSSample> samples, VariantSpec spec) throws IOException {
        TrainingParameters params = new TrainingParameters();
        params.put(Parameters.ALGORITHM_PARAM, spec.type().name());
        params.put(Parameters.ITERATIONS_PARAM, spec.iterations());
        params.put(Parameters.CUTOFF_PARAM, spec.cutoff());
        return POSTaggerME.train("ita", new ListObjectStream<>(samples), params, new POSTaggerFactory());
    }

    static double accuracy(POSModel model, List<POSSample> samples) {
        POSTaggerME tagger = new POSTaggerME(model);
        long correct = 0, total = 0;
        for (POSSample sample : samples) {
            String[] predicted = tagger.tag(sample.getSentence());
            String[] expected = sample.getTags();
            for (int i = 0; i < expected.length; i++) {
                if (expected[i].equals(predicted[i])) correct++;
                total++;
            }
        }
        return total == 0 ? 1.0 : (double) correct / total;
    }

    private static byte[] fetch(SourceManifest.Source source) throws Exception {
        HttpURLConnection connection = (HttpURLConnection) source.uri().toURL().openConnection();
        connection.setConnectTimeout(30_000);
        connection.setReadTimeout(60_000);
        connection.setRequestProperty("User-Agent", "matrix-understanding-lab-p05");
        if (connection.getResponseCode() != 200) {
            throw new IOException("download failed " + connection.getResponseCode() + " for " + source.uri());
        }
        byte[] bytes;
        try (var input = connection.getInputStream()) {
            bytes = input.readAllBytes();
        } finally {
            connection.disconnect();
        }
        if (bytes.length != source.bytes()) {
            throw new IllegalStateException("byte size mismatch for " + source.fileName());
        }
        String blob = gitBlobSha1(bytes);
        if (!blob.equals(source.gitBlobSha1())) {
            throw new IllegalStateException("Git blob mismatch for " + source.fileName() + ": " + blob);
        }
        return bytes;
    }

    private static Map<String, Object> sourceRecord(SourceManifest.Source source, byte[] bytes) throws Exception {
        Map<String, Object> record = new LinkedHashMap<>();
        record.put("role", source.role());
        record.put("url", source.uri().toString());
        record.put("bytes", bytes.length);
        record.put("gitBlobSha1", gitBlobSha1(bytes));
        record.put("sha256", sha256(bytes));
        record.put("trainingInput", "train".equals(source.role()));
        return record;
    }

    static String gitBlobSha1(byte[] bytes) throws Exception {
        MessageDigest digest = MessageDigest.getInstance("SHA-1");
        digest.update(("blob " + bytes.length + "\0").getBytes(StandardCharsets.UTF_8));
        return hex(digest.digest(bytes));
    }

    static String sha256(byte[] bytes) throws Exception {
        return hex(MessageDigest.getInstance("SHA-256").digest(bytes));
    }

    private static String hex(byte[] bytes) {
        StringBuilder out = new StringBuilder(bytes.length * 2);
        for (byte value : bytes) out.append(String.format(Locale.ROOT, "%02x", value & 0xff));
        return out.toString();
    }

    private static byte[] serialize(POSModel model) throws IOException {
        ByteArrayOutputStream output = new ByteArrayOutputStream();
        model.serialize(output);
        return output.toByteArray();
    }

    record VariantSpec(String id, ModelType type, int iterations, int cutoff) {}
    private record TrainedVariant(VariantSpec spec, POSModel model, byte[] bytes, double devAccuracy) {}

    private static final class ListObjectStream<T> implements ObjectStream<T> {
        private final List<T> values;
        private int index;
        private ListObjectStream(List<T> values) { this.values = values; }
        @Override public T read() { return index < values.size() ? values.get(index++) : null; }
        @Override public void reset() { index = 0; }
        @Override public void close() {}
    }
}
