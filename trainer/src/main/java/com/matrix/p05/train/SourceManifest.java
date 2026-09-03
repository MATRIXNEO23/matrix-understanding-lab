package com.matrix.p05.train;

import java.net.URI;
import java.util.List;

final class SourceManifest {
    static final String UPSTREAM_COMMIT = "e210079df0aea331ec1dcaa90648d815ce94c3ce";
    static final String BASE = "https://raw.githubusercontent.com/UniversalDependencies/UD_Italian-MarkIT/"
        + UPSTREAM_COMMIT + "/";

    static final List<Source> SOURCES = List.of(
        new Source("train", "it_markit-ud-train.conllu", 1_266_080L,
            "b616889012c62e56e991d14ea3653d798d29b74c", true),
        new Source("dev", "it_markit-ud-dev.conllu", 665_430L,
            "f138df1ee75d0e0b35de5856c4b3f6cebca6bbff", true),
        new Source("test", "it_markit-ud-test.conllu", 658_412L,
            "fe41f81cf242a022ed814c3684ecc37f5951cddf", true),
        new Source("license", "LICENSE.txt", 188L,
            "a7b465577bca288b1eb6f7eed92d83558e038d68", false),
        new Source("card", "README.md", 1_968L,
            "87bbd5801727c1de536b1eb57c0e81ac992c5fe3", false)
    );

    private SourceManifest() {}

    record Source(String role, String fileName, long bytes, String gitBlobSha1, boolean corpus) {
        URI uri() {
            return URI.create(BASE + fileName);
        }
    }
}
