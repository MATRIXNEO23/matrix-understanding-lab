# Gate 10 — Android/Moto G56 footprint probe

## Scope and status

`android-probe` is an isolated, offline debug APK for measuring the frozen A/B
benchmark on a physical Moto G56. It does not integrate anything into Matrix
production. Candidate B uses Android platform ICU plus the same OpenNLP tools,
POS artifacts and mapper measured by the JVM runner; ICU4J is not packaged.

The APK declares no network permission. It embeds `p0-gold-v1.json`, performs
three warm-up loops and twenty measured loops over all 66 cases, then exports:

- Candidate-B cold constructor wall/thread-CPU time;
- warm per-turn wall and thread-CPU p50/p95 for A and B;
- process PSS before engines, after B initialization, and sampled peak;
- thermal status at loop start/end and maximum;
- device/API/ABI metadata and Candidate-B quality output.

The in-process PSS delta is diagnostic: a later isolated-process run or Android
Studio profiler capture may refine it. APK/model bytes come from the CI-built
artifact, not from runtime PSS. No Moto value is claimed until the JSON from a
real phone is returned.

## Verified build evidence

CI run `33745451037` at commit
`de377a7549d2eb58971f362c6e750b4f12a8647a` completed unit tests, the unified
A/B runner and `:android-probe:assembleDebug` successfully.

| Build item | Measured value |
|---|---:|
| APK | 5,636,633 bytes |
| APK SHA-256 | `5f117c38c2d263d9848ee11054404e318c608d386618a63cc368047fa8bff506` |
| Three POS model files, uncompressed total | 4,068,644 bytes |
| English model | 1,164,974 bytes |
| Spanish model | 1,754,275 bytes |
| Italian model | 1,149,395 bytes |
| GitHub artifact archive | 5,628,343 bytes |
| Artifact id/digest | `9889461911` / `sha256:089490176715e3c507c5c2d95f70e524995c5b60c517d3359bb5ab63c813a050` |

These are package/file sizes, not memory usage. A subsequent CI gate inspects
the built manifest with `aapt` and fails if `android.permission.INTERNET` is
present.

## Reproducible build

The lab pins AGP `8.9.2`, Gradle `8.11.1`, JDK 17, compile SDK 35 and min SDK 26.
API 26 is required because OpenNLP 2.5.11 contains `MethodHandle.invoke` usage;
D8 rejects it below Android O even though platform ICU itself starts at API 24.
AGP/Gradle/JDK/SDK is the compatibility set published for AGP 8.9. Build locally with:

```text
gradle --no-daemon :core:test :cli:run :android-probe:assembleDebug
```

CI uploads `p0-android-probe/android-probe-debug.apk`. The package is
`com.matrix.p0.probe`; it is intentionally separate from Neon Tides.

## Physical Moto G56 procedure

1. Charge above 50%, disable battery saver, let the phone cool to a stable idle
   state, close unrelated foreground apps, and keep the screen on.
2. Install with `adb install -r android-probe-debug.apk` and launch **Matrix P0
   Probe**. Keep it in the foreground until `PASS` appears.
3. Record Android build, room/device starting condition and whether charging was
   connected. Repeat at least three cold app starts; force-stop between runs.
4. Export the JSON shown on screen. The normal command is:

```text
adb pull /sdcard/Android/data/com.matrix.p0.probe/files/p0-mobile-probe.json
```

If scoped-storage policy blocks that path, use Android Studio Device Explorer
for the app-specific external-files directory. Do not report hand-copied UI
numbers as the canonical result; retain each raw JSON.

## Acceptance interpretation

- ownership/perspective violations and invented World Truth remain zero-tolerance;
- Candidate B's initial supervision target is delta PSS `<= 40 MB`;
- CPU, p50/p95 and thermal drift are compared against A on the same device;
- a quality win does not waive the Italian model license stop;
- a successful APK build is **instrumentation ready**, not a completed Moto
  measurement.

Primary Android references:

- https://developer.android.com/build/releases/agp-8-9-0-release-notes
- https://developer.android.com/reference/android/os/Debug
- https://developer.android.com/reference/android/os/PowerManager#getCurrentThermalStatus()
- https://developer.android.com/reference/android/icu/text/BreakIterator
