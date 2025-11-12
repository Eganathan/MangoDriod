---
date: '2025-11-11T22:30:28+05:30' 
draft: true
title: 'Clickable Links in Jetpack Compose AnnotatedString also with Custom URL Handler'
---

While building the onboarding screen for my app, I needed a simple text in that read something like this:

![Example of the Implementation](/img/devfest_2025/speaking-at-the-platform-01.JPG)
*The green hyperlinks are clickable*

Pretty straightforward, right? Just a bit of text with two clickable links — `Privacy Policy` and `Terms of Service`.

But as I started implementing it, I realized: there isn’t a single complete guide explaining how to make part of a text clickable using AnnotatedString in Jetpack Compose — especially with the new LinkAnnotation API and a custom URL handler for backward compatability.

So I’m writing this as both a reference for myself and for anyone else struggling with this tiny, under-documented detail.


```toml
browser = "1.8.0"

[libraries]
androidx-browser = { group = "androidx.browser", name = "browser", version.ref = "browser" }

```

```gradle
    implementation libs.androidx.browser
```

### URL Handler
```kotlin
fun urlHandler(url: String, context: Context) {

    try {
        val customTabsIntent = CustomTabsIntent.Builder().build()
        customTabsIntent.launchUrl(context, Uri.parse(url))
    } catch (e: ActivityNotFoundException) {
        try {
            val intent = Intent(Intent.ACTION_VIEW, Uri.parse(url))
            context.startActivity(intent)
        } catch (e: Exception) {
            Toast.makeText(context, "Browser not installed! visit: $url", Toast.LENGTH_LONG).show()
        }
    } catch (e: Exception) {
        e.printStackTrace()
        Toast.makeText(context, "Unable to open link! visit: $url", Toast.LENGTH_SHORT).show()
    }
}
```

```kotlin
@OptIn(ExperimentalTextApi::class)
@Composable
internal fun TermsAndCondition() {
    val context = LocalContext.current
    
    val linkInteractionListener = LinkInteractionListener {
        urlHandler((it as LinkAnnotation.Url).url, context)
    }

    val linkStyle = TextLinkStyles(SpanStyle(color = DGreen, textDecoration = TextDecoration.Underline))

    val privacyPolicy = LinkAnnotation.Url(
        url = URLS.PRIVACY,
        styles = linkStyle,
        linkInteractionListener = linkInteractionListener
    )
    val toc = LinkAnnotation.Url(
        url = URLS.TOC,
        styles = linkStyle,
        linkInteractionListener = linkInteractionListener
    )

    //This helps us to re-use it while supporting multiple locale
    @Composable
    fun AnnotatedString.Builder.privacyLink() {
        withLink(privacyPolicy) {
            append(stringResource(id = R.string.privacy_policy))
        }
    }

    //This helps us to re-use it while supporting multiple locale
    @Composable
    fun AnnotatedString.Builder.tocLink() {
        withLink(toc) {
            append(stringResource(id = R.string.terms_of_service))
        }
    }


    val annotatedString = buildAnnotatedString {
        append("Read ")
        privacyLink()//Clickable Privacy Policy
        append(" and tap on `")
        withStyle(style = SpanStyle(fontWeight = FontWeight.Bold)) {
            append(
                "Agree and Continue"
            )
        }
        append("` to accept the ")
        tocLink() //Clickable Terms and Conditions
    }

    Text(
        text = annotatedString,
        style = PannaiTheme.typography.semiBold12.copy(color = LGray, textAlign = TextAlign.Center),
        modifier = Modifier.fillMaxWidth(0.8f),
    )
}
```

