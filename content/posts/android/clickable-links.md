---
date: '2025-11-11T22:30:28+05:30'
draft: false
title: 'Clickable Links in Jetpack Compose: AnnotatedString with Custom URL Handler'
categories: ["Android"]
tags: ["Android", "Jetpack Compose", "AnnotatedString"]
---

While building the onboarding screen for my app, I needed a simple text that read something like this:

![Example of the Implementation](/img/android/clickable-text-android-example.jpeg)
*The green hyperlinks are clickable*

Pretty straightforward, right? Just a bit of text with two clickable links — `Privacy Policy` and `Terms of Service`.

But as I started implementing it, I realized: **there isn't a single complete guide** explaining how to make part of a text clickable using `AnnotatedString` in Jetpack Compose — especially with the new **LinkAnnotation API** and a **custom URL handler** for better control.

So I'm writing this as both a reference for myself and for anyone else struggling with this tiny, under-documented detail.

---

## Why Custom URL Handling?

By default, Compose can open links using the system browser. But what if you want:

- **Better UX with Chrome Custom Tabs** (opens links in-app with smooth transitions)
- **Graceful fallbacks** (handle cases where browsers aren't installed)
- **Full control** over how URLs are opened (analytics, deep links, etc.)

That's exactly what we'll implement.

---

## Step-by-Step Implementation

### 1. Add the Browser Library

We'll use **Android Browser Library** to implement Chrome Custom Tabs for a better link-opening experience.

Add this to your `libs.versions.toml`:

```toml
[versions]
browser = "1.8.0"

[libraries]
androidx-browser = { group = "androidx.browser", name = "browser", version.ref = "browser" }
```

Then add the dependency to your app's `build.gradle.kts`:

```kotlin
dependencies {
    implementation(libs.androidx.browser)
}
```

**Why Chrome Custom Tabs?**
Custom Tabs open web content **inside your app** with a smooth transition, pre-loaded browser engine, and shared cookies/sessions — all without leaving your app's context.

---

### 2. Create a Custom URL Handler

This function handles opening URLs with **three layers of fallback**:

```kotlin
fun urlHandler(url: String, context: Context) {
    try {
        // First: Try Chrome Custom Tabs (best UX)
        val customTabsIntent = CustomTabsIntent.Builder().build()
        customTabsIntent.launchUrl(context, Uri.parse(url))
    } catch (e: ActivityNotFoundException) {
        try {
            // Second: Fallback to system browser
            val intent = Intent(Intent.ACTION_VIEW, Uri.parse(url))
            context.startActivity(intent)
        } catch (e: Exception) {
            // Third: Show toast if no browser exists
            Toast.makeText(
                context,
                "Browser not installed! visit: $url",
                Toast.LENGTH_LONG
            ).show()
        }
    } catch (e: Exception) {
        e.printStackTrace()
        Toast.makeText(
            context,
            "Unable to open link! visit: $url",
            Toast.LENGTH_SHORT
        ).show()
    }
}
```

**How it works:**
1. **Chrome Custom Tabs** (preferred): Opens in-app with native feel
2. **System Browser** (fallback): Opens in the default browser if Custom Tabs fail
3. **Toast Message** (last resort): Shows URL if no browser is available

This ensures **your app never crashes** when opening links, even on devices without browsers.

---

### 3. Building the Clickable Text Component

Now let's create the actual composable with clickable links.

```kotlin
@OptIn(ExperimentalTextApi::class)
@Composable
internal fun TermsAndCondition() {
    val context = LocalContext.current

    // Define how links should behave when clicked
    val linkInteractionListener = LinkInteractionListener {
        urlHandler((it as LinkAnnotation.Url).url, context)
    }

    // Define link styling (color + underline)
    val linkStyle = TextLinkStyles(
        SpanStyle(
            color = DGreen,
            textDecoration = TextDecoration.Underline
        )
    )

    // Create Privacy Policy link annotation
    val privacyPolicy = LinkAnnotation.Url(
        url = URLS.PRIVACY,
        styles = linkStyle,
        linkInteractionListener = linkInteractionListener
    )

    // Create Terms of Service link annotation
    val toc = LinkAnnotation.Url(
        url = URLS.TOC,
        styles = linkStyle,
        linkInteractionListener = linkInteractionListener
    )

    // Helper functions for reusable link text (supports localization!)
    @Composable
    fun AnnotatedString.Builder.privacyLink() {
        withLink(privacyPolicy) {
            append(stringResource(id = R.string.privacy_policy))
        }
    }

    @Composable
    fun AnnotatedString.Builder.tocLink() {
        withLink(toc) {
            append(stringResource(id = R.string.terms_of_service))
        }
    }

    // Build the complete annotated string with mixed text + links
    val annotatedString = buildAnnotatedString {
        append("Read ")
        privacyLink()  // Clickable Privacy Policy
        append(" and tap on `")
        withStyle(style = SpanStyle(fontWeight = FontWeight.Bold)) {
            append("Agree and Continue")
        }
        append("` to accept the ")
        tocLink()  // Clickable Terms of Service
    }

    Text(
        text = annotatedString,
        style = PannaiTheme.typography.semiBold12.copy(
            color = LGray,
            textAlign = TextAlign.Center
        ),
        modifier = Modifier.fillMaxWidth(0.8f),
    )
}
```

---

## Breaking Down the Code

### LinkInteractionListener
```kotlin
val linkInteractionListener = LinkInteractionListener {
    urlHandler((it as LinkAnnotation.Url).url, context)
}
```
- This listener gets triggered when **any link is clicked**
- It extracts the URL from the `LinkAnnotation.Url` object
- Passes it to our custom `urlHandler()` for controlled opening

---

### LinkAnnotation.Url
```kotlin
val privacyPolicy = LinkAnnotation.Url(
    url = URLS.PRIVACY,
    styles = linkStyle,
    linkInteractionListener = linkInteractionListener
)
```
- **url**: The actual link destination
- **styles**: How the link looks (color, underline, etc.)
- **linkInteractionListener**: What happens when clicked

This is the **new Compose way** of handling links (replaces older `pushStringAnnotation` approach).

---

### Helper Functions for Localization
```kotlin
@Composable
fun AnnotatedString.Builder.privacyLink() {
    withLink(privacyPolicy) {
        append(stringResource(id = R.string.privacy_policy))
    }
}
```
**Why helper functions?**
By using `stringResource()`, the link text **automatically updates** based on user's language. This makes your code cleaner, reusable, and supports multi-language apps without duplicating logic.

---

### Building the Final Text
```kotlin
val annotatedString = buildAnnotatedString {
    append("Read ")
    privacyLink()  // This part is clickable!
    append(" and tap on `")
    withStyle(style = SpanStyle(fontWeight = FontWeight.Bold)) {
        append("Agree and Continue")
    }
    append("` to accept the ")
    tocLink()  // This part is also clickable!
}
```
This combines **regular text** + **clickable links** + **styled text** in one component. `withLink()` wraps text and makes it interactive, while `withStyle()` applies visual formatting without making it clickable.

---

## Key Takeaways

- **LinkAnnotation API** is the modern way to create clickable links in Compose
- **Custom URL handler** gives you full control over how links open
- **Chrome Custom Tabs** provides better UX than default browser
- **Graceful fallbacks** prevent app crashes on edge cases
- **Helper functions + stringResource** make your code localization-ready

---

## Why This Approach is Better

Compared to older methods using `pushStringAnnotation`, this approach:

- **Type-safe**: LinkAnnotation is strongly typed
- **Easier styling**: Direct style application per link
- **Better separation**: Link logic separate from text building
- **Localization-friendly**: Works seamlessly with multi-language apps

---

## Related Resources

- [AnnotatedString Documentation](https://developer.android.com/jetpack/compose/text#click-with-annotation)
- [Chrome Custom Tabs Guide](https://developer.chrome.com/docs/android/custom-tabs/)

---

**Thanks for reading!** If you found this helpful, feel free to reach out via my social handles.

