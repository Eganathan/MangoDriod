---
date: '2025-03-14T15:28:28+05:30'
draft: true
title: 'Compose Multiplatform: Project Setup & Dependency Walkthrough'
tags: ["Kotlin", "Compose Multiplatform", "KMP"]
categories: ["Compose Multiplatform"]
---

## Getting Started

### 1. Project Initialization

Start by creating your project using the [Kotlin Multiplatform wizard](https://kmp.jetbrains.com/). This will generate a starter template with the basic project structure.

### 2. Initial Setup

Run the example code to ensure everything works correctly, then initialize Git and push your initial working commit.

### 3. Essential Dependencies

To build a production-ready application, we need to set up the following dependencies:
- **Logging** - For debug and error tracking
- **Resource Management** - For assets, strings, and fonts
- **Navigation** - For app navigation (to be covered later)

---

## Logging with Kermit

For logging, I'm using [Kermit](https://kermit.touchlab.co/docs/), a multiplatform logging library from Touchlab.

### Installation

Add the dependency to your app module's `commonMain` block:

```kotlin
commonMain {
    dependencies {
        // ... other dependencies
        implementation("co.touchlab:kermit:2.0.4")
    }
}
```

Check [Maven Central](https://central.sonatype.com/artifact/co.touchlab/kermit) for the latest version.

### Usage

Using Kermit is straightforward:

```kotlin
Logger.w("MyTag") { "Hello World $someData" } // Log Warning
Logger.i { "Info LogTesting" } // Log Info
```

**Note:** By default, Kermit logs don't include tags. I've created some helper functions to simplify logging with tags.


---

## Compose Resources

For managing resources (images, fonts, strings, etc.) across platforms, we'll use the official Compose Multiplatform resources library.

### Installation

Add the dependency to your `commonMain` block:

```kotlin
commonMain {
    dependencies {
        // ... other dependencies
        implementation("org.jetbrains.compose.components:components-resources:1.10.0-beta01")
    }
}
```

Check [Maven Central](https://central.sonatype.com/artifact/org.jetbrains.compose.components/components-resources) for the latest version.

### Setting Up Resource Directories

Create a new folder called `composeResources` under the `composeApp` directory.

Inside `composeResources`, you can create the following subdirectories as needed:

- **`drawable`** - For images. Supports rasterized images (JPEG, PNG, bitmap, WebP) and vector Android XML images.
  - **Important:** Vector drawables should not reference Android-specific resources like `@color/red`

- **`font`** - For `.ttf` or `.otf` font files (note: singular "font", not "fonts")

- **`strings`** - For string values, organized by localization (similar to Android's strings folder)

- **`files`** - For any other files not covered above

**Note:** Only create the directories you actually need. Don't create empty folders.

For more advanced usage, see the [official documentation on custom resource directories](https://kotlinlang.org/docs/multiplatform/compose-multiplatform-resources-setup.html#custom-resource-directories).

### Example: Setting Up Custom Typography

Let's test the resource system by adding custom fonts:

1. **Download fonts** from [Google Fonts](https://fonts.google.com/)

2. **Rename font files** to lowercase with underscores instead of spaces:
   - Example: `NotoSans-Light.ttf` → `noto_sans_light.ttf`

3. **Create a custom typography file** and set up a `FontFamily`

4. **Import required dependencies:**
   - `androidx.compose.ui.text.font.FontFamily`
   - `org.jetbrains.compose.resources.Font`

5. **Add fonts to the FontFamily** as shown below:
```kotlin
@Composable
private fun customTypography(): Typography {
    val ubuntuFonts = FontFamily(
        Font(Res.font.ubuntu_sans_light, FontWeight.Light, FontStyle.Normal),
        Font(Res.font.ubuntu_sans_medium, FontWeight.Medium, FontStyle.Normal),
        Font(Res.font.ubuntu_sans_regular, FontWeight.Normal, FontStyle.Normal),
        Font(Res.font.ubuntu_sans_semi_bold, FontWeight.SemiBold, FontStyle.Normal),
        Font(Res.font.ubuntu_sans_bold, FontWeight.Bold, FontStyle.Normal),
        Font(Res.font.ubuntu_sans_italic, FontWeight.Normal, FontStyle.Italic)
    )

    return with(MaterialTheme.typography) {
        copy(
            displayLarge = displayLarge.copy(fontFamily = ubuntuFonts),
            displayMedium = displayMedium.copy(fontFamily = ubuntuFonts),
            displaySmall = displaySmall.copy(fontFamily = ubuntuFonts),

            headlineLarge = headlineLarge.copy(fontFamily = ubuntuFonts),
            headlineMedium = headlineMedium.copy(fontFamily = ubuntuFonts),
            headlineSmall = headlineSmall.copy(fontFamily = ubuntuFonts),

            titleLarge = titleLarge.copy(fontFamily = ubuntuFonts),
            titleMedium = titleMedium.copy(fontFamily = ubuntuFonts),
            titleSmall = titleSmall.copy(fontFamily = ubuntuFonts),

            bodyLarge = bodyLarge.copy(fontFamily = ubuntuFonts),
            bodyMedium = bodyMedium.copy(fontFamily = ubuntuFonts),
            bodySmall = bodySmall.copy(fontFamily = ubuntuFonts),

            labelLarge = labelLarge.copy(fontFamily = ubuntuFonts),
            labelMedium = labelMedium.copy(fontFamily = ubuntuFonts),
            labelSmall = labelSmall.copy(fontFamily = ubuntuFonts),
        )
    }
}
```

### Applying Custom Typography

Apply your custom typography to the Material Theme:

```kotlin
@Composable
@Preview
fun App() {
    MaterialTheme(
        typography = customTypography()
    ) {
        // Your app content here
    }
}
```

### String Respource

This [Documentation](https://developer.android.com/develop/ui/compose/resources) will help you 

---

## Navigation

### Installation

```kotlin
commonMain {
    dependencies {
        // ... other dependencies
        implementation("org.jetbrains.androidx.navigation:navigation-compose:2.9.1")
    }
}
```
Check [Maven Central](https://central.sonatype.com/artifact/org.jetbrains.androidx.navigation/navigation-compose) for the latest version.

Now we need Serialization plugin so lets add that 

```kotlin
commonMain {
    dependencies {
        // ... other dependencies
        implementation("org.jetbrains.kotlinx:kotlinx-serialization-json:1.9.0")
    }
}
```
Now, lets apply the plugin in the project build.gralde 
```
plugins {
    ...
    kotlin("plugin.serialization") version "your-kotlin-verion" apply false
}
```

now in the composeApp modules build.gradle file
```
plugins {
    ...
    kotlin("plugin.serialization")
}
```
now sync the project and create a AppNavComponent for example like this

```@Serializable
object Home

@Serializable
data class Screen2(val name: String)

@Composable
fun AppNavigation() {
    val navController = rememberNavController()
    NavHost(navController = navController, startDestination = Home) {

        composable<Home> {
            Column { Text("Home") }
        }

        composable<Screen2> {
            Column { Text("Screen 2") }
        }

    }
}

```

## ViewModel
```

implementation("org.jetbrains.androidx.lifecycle:lifecycle-viewmodel-compose":2.9.0")

```

## DI
```
...
    implementation(project.dependencies.platform("io.insert-koin:koin-bom:$koin_version"))
    implementation("io.insert-koin:koin-core")
    implementation("io.insert-koin:koin-compose")
    implementation("io.insert-koin:koin-compose-viewmodel")
    implementation("io.insert-koin:koin-compose-viewmodel-navigation")
```

