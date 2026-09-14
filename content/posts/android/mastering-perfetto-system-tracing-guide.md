---
date: '2026-09-01T15:10:00+05:30'
title: 'A Practical Guide to Google Perfetto: Why, Setup, Recording, and Deep Trace Analysis'
categories: ["Android", "Performance"]
tags: ["Android", "Perfetto", "Performance", "Profiling", "Systrace", "Kotlin", "Trace Processor", "DevTools"]
---

If you have ever spent hours debugging a mysterious UI frame drop, an unpredictable app startup delay, or high CPU utilization, you know that log statements and simple timers only tell half the story. 

Modern operating systems and apps are deeply asynchronous. A lag spike in your app's main thread could be caused by garbage collection, lock contention, CPU frequency throttling, or another background process starving your app of CPU cycles.

Enter **[Perfetto](https://github.com/google/perfetto)** — Google's open-source, next-generation system profiling, app tracing, and metrics analysis platform.

In this guide, we'll walk through what Perfetto is, why it completely supersedes legacy tools like Systrace, how to set it up, various ways to record traces, and how to analyze them like a pro (including querying trace data with SQL!).

---

## TL;DR - Quick Start

Want to capture a trace right now?

1. Connect your Android device via USB with USB Debugging enabled.
2. Open **[ui.perfetto.dev](https://ui.perfetto.dev)** in Chrome.
3. Click **Record new trace** in the left sidebar.
4. Select **Recording mode: Stop when full**, choose **UI & Rendering** preset, select your device, and click **Start Recording**.
5. Reproduce your app workflow. The trace will open automatically in the web visualizer.

---

## 1. What is Perfetto & Why Should You Care?

### The Evolution: Why Legacy Systrace Was Retired

For years, Android developers relied on `systrace` and `atrace`. While useful, Systrace had significant limitations:
- High performance overhead when capturing high-frequency events.
- Fixed in-memory buffer constraints leading to lost events.
- Heavy HTML trace viewers that crashed browser tabs when opening files larger than a few hundred megabytes.
- Limited cross-platform extensibility.

Google engineered **Perfetto** from the ground up to unify tracing across the entire stack — Android OS (from Android 9/10+), Linux, Chrome, and native/userspace applications.

```
+-------------------------------------------------------------------------+
|                              Perfetto Stack                             |
+-------------------------------------------------------------------------+
|  Data Sources: Kernel ftrace | App Trace points | heapprofd | GPU/Power |
+-------------------------------------------------------------------------+
|  Collection:   traced daemon (Lock-free Shared Memory Ring Buffers)      |
+-------------------------------------------------------------------------+
|  Storage:      Compact, streaming Protobuf format (.perfetto-trace)     |
+-------------------------------------------------------------------------+
|  Analysis:     Trace Processor (SQL engine) + ui.perfetto.dev (Canvas)  |
+-------------------------------------------------------------------------+
```

### Why Perfetto Stands Out

1. **Near-Zero Overhead**: Uses a shared-memory IPC architecture (`traced` daemon) where data is written directly to shared ring buffers without heavy kernel context switches.
2. **Unified Data Sources**: Correlates kernel events (CPU scheduling, thread states, CPU frequencies, disk I/O, IRQs) with app-level custom slices (`Trace.beginSection`), memory allocations, and battery counters.
3. **No App Instrumentation Required for System Insights**: You can see which CPU core ran your thread, when it got preempted, and what other process took over the core.
4. **Trace Processor (SQL Analysis Engine)**: Every trace is essentially an in-memory SQLite database. You can query your trace using SQL to calculate 99th percentile frame times, lock wait times, or memory spikes.
5. **Blazing-Fast Web UI**: [ui.perfetto.dev](https://ui.perfetto.dev) uses WebAssembly and HTML5 Canvas to smoothly pan and zoom through gigabytes of trace data at 60 FPS.

---

## 2. Setting Up Perfetto

### Prerequisites & Device Compatibility

- **Android 10 (API 29) or higher**: Perfetto daemons are built into the OS and enabled by default.
- **Android 9 (Pie)**: Perfetto is available but must be enabled via adb properties.
- **Host PC**: macOS, Linux, or Windows with `adb` installed.

### Preparing Your Android App for Production-Accurate Tracing

> **Warning**: Never profile an app with `debuggable = true` in production performance tests. Debug builds disable ART compiler optimizations (like inline functions and Ahead-of-Time compilation) and add significant JIT overhead.

Instead, use the `<profileable>` tag introduced in Android 10 (API 29) to allow Perfetto to capture detailed app-level traces without debug overhead:

In your `AndroidManifest.xml`:

```xml
<manifest xmlns:android="http://schemas.android.com/apk/res/android">
    <application
        android:allowBackup="true"
        android:icon="@mipmap/ic_launcher"
        android:label="@string/app_name"
        android:theme="@style/Theme.MyApp">

        <!-- Allows Perfetto & Android Studio to profile non-debuggable release builds -->
        <profileable 
            android:shell="true" 
            android:enabled="true" />

        <activity android:name=".MainActivity" android:exported="true">
            ...
        </activity>
    </application>
</manifest>
```

### Adding Custom Application Trace Markers (Kotlin / Jetpack Compose)

Add the Jetpack Tracing library to your `app/build.gradle.kts`:

```kotlin
dependencies {
    // Official AndroidX Tracing library
    implementation("androidx.tracing:tracing-ktx:1.3.0")
}
```

#### Tracing Standard Kotlin Functions

Use the `trace` inline function to wrap critical sections (e.g. database queries, network JSON parsing, complex transformations):

```kotlin
import androidx.tracing.trace

fun loadFeedData(): List<FeedItem> {
    return trace("FeedRepository:loadFeedData") {
        val rawData = fetchFromDatabase()
        trace("FeedRepository:mapItems") {
            rawData.map { it.toUiModel() }
        }
    }
}
```

#### Tracing Jetpack Compose Recompositions

If you want Compose to automatically generate trace slices for every composable during recomposition, add the Compose runtime tracing dependency:

```kotlin
dependencies {
    implementation("androidx.compose.runtime:runtime-tracing:1.7.8")
}
```

This annotates the trace with composable names, source file names, and recomposition counts directly in the Perfetto timeline.

---

## 3. How to Record Traces

There are 4 popular ways to record Perfetto traces depending on your workflow.

### Method 1: The Perfetto Web UI (Recommended for Quick Visual Debugging)

1. Open **[ui.perfetto.dev](https://ui.perfetto.dev)** in Google Chrome or any Chromium browser.
2. Click **Record new trace** on the left menu.
3. Select **Add ADB device** (or WebUSB). Approve the USB debugging prompt on your phone.
4. Customize your probe selections:
   - **CPU**: Cores, CPU Frequency, Syscalls, Scheduling details (`sched_switch`).
   - **Android apps & jank**: App startup, Choreographer, SurfaceFlinger, Frame timeline.
   - **Target App**: Enter your package name (e.g., `com.example.myapp`).
5. Set buffer size (e.g., `64 MB`) and duration (e.g., `10s`).
6. Click **Start Recording**, perform your user action, and watch the trace automatically parse and open.

---

### Method 2: Command Line with `record_android_trace`

If you prefer the terminal or want to automate trace collection, Google provides a standalone Python helper script:

#### Download the script:
```bash
curl -O https://raw.githubusercontent.com/google/perfetto/main/tools/record_android_trace
chmod +x record_android_trace
```

#### Record a 10-second trace:
```bash
./record_android_trace \
  -o app_jank.perfetto-trace \
  -t 10s \
  -b 64mb \
  -a com.example.myapp \
  sched freq idle am wm gfx view binder_driver hal dalvik camera
```

#### Breakdown of flags:
- `-o <file>`: Output file path.
- `-t <time>`: Tracing duration (e.g. `10s`, `1m`).
- `-b <size>`: In-memory buffer size.
- `-a <package>`: Enables app-level `atrace` / `androidx.tracing` categories for this specific package.
- `sched freq am wm gfx view binder_driver`: Key kernel and OS tracing categories.

Once finished, open the output `.perfetto-trace` file directly at [ui.perfetto.dev](https://ui.perfetto.dev) by clicking **Open trace file**.

---

### Method 3: System Tracing Quick Settings Tile (On-Device)

For capturing real-world bugs in the wild without a PC connected:

1. On your Android phone, go to **Settings > System > Developer options > System Tracing**.
2. Toggle on **Show Quick Settings tile**.
3. Pull down your phone's notification shade and tap the **System Tracing** tile to start recording.
4. Reproduce the bug or jank.
5. Tap the tile again to stop.
6. Share or pull the generated trace from `/data/local/traces/` via ADB:
   ```bash
   adb pull /data/local/traces/ .
   ```

---

### Method 4: Automated Tracing with Jetpack Macrobenchmark

If you want traces captured automatically during CI/CD regression tests, use Jetpack Macrobenchmark:

```kotlin
@RunWith(AndroidJUnit4::class)
class ScrollBenchmark {
    @get:Rule
    val benchmarkRule = MacrobenchmarkRule()

    @Test
    fun scrollFeedCompilationMode() = benchmarkRule.measureRepeated(
        packageName = "com.example.myapp",
        metrics = listOf(FrameTimingMetric(), StartupTimingMetric()),
        compilationMode = CompilationMode.Full(),
        iterations = 5,
        startupMode = StartupMode.COLD
    ) {
        pressHome()
        startActivityAndWait()

        val feedList = device.findObject(By.res("feed_list"))
        feedList.setGestureMargin(device.displayWidth / 5)
        feedList.fling(Direction.DOWN)
    }
}
```

Every benchmark run generates a direct link to a Perfetto trace file in Android Studio’s test results window.

---

## 4. How to Navigate and Read a Trace in Perfetto UI

When you open a trace in [ui.perfetto.dev](https://ui.perfetto.dev), the interface might look intimidating at first. Here is how to navigate it smoothly:

### Essential Keyboard Shortcuts

| Key | Action |
|---|---|
| `W` | Zoom in on timeline (centered at cursor) |
| `S` | Zoom out |
| `A` | Pan left |
| `D` | Pan right |
| `M` | Mark selected range (measure time delta) |
| `F` | Focus / zoom to fit selected slice |
| `?` | Show all keyboard shortcuts |

```
+--------------------------------------------------------------------------------+
|  Time: 0s               2s               4s               6s               8s  |
+--------------------------------------------------------------------------------+
| CPU 0-7:  [|||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||]  |
|                                                                                |
| Process: com.example.myapp (PID: 14203)                                        |
|   ├─ Main Thread (14203)                                                       |
|   │    [Choreographer#doFrame] -> [inflate] -> [bindViewHolder]                |
|   ├─ RenderThread (14220)                                                      |
|   │    [DrawFrame] -> [syncFrameState] -> [eglSwapBuffers]                     |
|   └─ DefaultDispatcher-worker-1                                                |
|        [FeedRepository:loadFeedData]                                           |
+--------------------------------------------------------------------------------+
```

### Key Tracks to Inspect

1. **CPU Usage & Scheduling Tracks (`sched`)**:
   - Each thread bar has colored blocks representing thread states:
     - **Green (Running)**: The thread is actively executing on a CPU core.
     - **Blue (Runnable)**: The thread is ready to run, but waiting for an available CPU core (**CPU contention** or CPU starvation!).
     - **Red/Orange (Sleeping/Blocked)**: The thread is waiting on an I/O operation, a lock, a mutex, or `Thread.sleep()`.
2. **App Main Thread**:
   - Shows your app's UI message loop. Look for `Choreographer#doFrame` slices.
   - On a 60Hz display, a frame slice must complete in under **16.6ms**; on 120Hz, under **8.3ms**. If `doFrame` exceeds this, you have dropped frames (jank).
3. **RenderThread**:
   - Handles the hardware acceleration commands sent from the main thread and syncs with the GPU via OpenGL/Vulkan (`eglSwapBuffersWithDamageKHR`).
4. **Android Frame Timeline (Jank Detection Track)**:
   - Colored markers indicate whether each frame was:
     - **Green**: On-time.
     - **Yellow/Red**: Delayed / Dropped frame with the root cause (e.g. `App Deadline Missed` or `Display HAL Deadline Missed`).

---

## 5. What Not: Advanced Power Features

### Querying Traces with SQL (Trace Processor)

One of Perfetto's greatest strengths is the **Trace Processor**. Instead of manually panning around a massive trace looking for spikes, you can write SQL queries directly in the UI query console (or in a Python script).

Click the **Query (SQL)** tab in the left sidebar of the Perfetto UI:

#### 1. Find the 10 longest slices in your app:
```sql
SELECT 
    name, 
    CAST(dur / 1e6 AS INT) AS duration_ms,
    track.name AS thread_name
FROM slice
JOIN track ON slice.track_id = track.id
WHERE dur > 10000000 -- greater than 10ms
ORDER BY dur DESC
LIMIT 10;
```

#### 2. Calculate time spent in `Runnable` state (CPU Starvation):
```sql
SELECT 
    thread.name,
    SUM(dur) / 1e6 AS total_runnable_delay_ms
FROM thread_state
JOIN thread USING (utid)
WHERE state = 'R' -- Runnable (waiting for CPU)
GROUP BY thread.name
ORDER BY total_runnable_delay_ms DESC
LIMIT 5;
```

#### 3. Analyze Lock Contention:
```sql
SELECT 
    name,
    COUNT(*) AS contention_count,
    SUM(dur) / 1e6 AS total_wait_time_ms
FROM slice
WHERE name LIKE 'monitor contention%'
GROUP BY name
ORDER BY total_wait_time_ms DESC;
```

---

### Memory Profiling with `heapprofd`

Perfetto includes a native heap profiler called **`heapprofd`** that samples allocations with zero code modifications:

```bash
# Capture native memory allocations of your app
./record_android_trace \
  -o heap_trace.perfetto-trace \
  -t 20s \
  -b 128mb \
  heapprofd \
  -a com.example.myapp
```

When opened in [ui.perfetto.dev](https://ui.perfetto.dev), it displays flame graphs and allocation breakdown trees showing exact callstacks that allocated native memory.

---

## Common Pitfalls & Best Practices

| Do's | Don'ts |
|---|---|
| Use `<profileable android:shell="true" />` on Release builds. | Never run benchmarks or record traces on `debuggable=true` builds. |
| Use specific categories to keep buffer usage manageable. | Don't enable every single data source unless you're diagnosing kernel-level bugs. |
| Use `trace("SectionName") { ... }` around suspect blocks. | Don't put trace sections inside micro-loops (e.g. iterating 100,000 items). |
| Look at thread states (`Runnable` vs `Sleeping`) to understand *why* code was slow. | Don't assume slow function execution is always bad code; it could be CPU frequency throttling or lock contention. |

---

## Summary

Perfetto is the gold standard for performance engineering on Android and Linux systems. Whether you are hunting down a 100ms frame drop during a Compose scroll gesture, profiling memory leaks with `heapprofd`, or automating performance regressions in CI using SQL metrics, Perfetto provides unprecedented observability.

### Useful Links & Further Reading

- [Official Perfetto GitHub Repository](https://github.com/google/perfetto)
- [Perfetto Documentation & Reference Guides](https://perfetto.dev/docs/)
- [Perfetto Web UI Visualizer](https://ui.perfetto.dev)
- [Android Developers Guide on System Tracing](https://developer.android.com/topic/performance/tracing)
- [Jetpack Tracing Guide](https://developer.android.com/topic/performance/tracing/custom-events)

---

*Found this guide helpful? Have questions or favorite Perfetto SQL queries? Feel free to reach out via my social handles!*
