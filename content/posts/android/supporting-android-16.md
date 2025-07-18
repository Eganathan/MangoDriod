---
date: '2025-06-20T19:47:13+05:30' 
draft: true
title: 'Supporting API 15+'
categories: ["Android"]
tags: ["Android"]
---

## Updating Icon Colors

```kotlin
import android.os.Build
import android.view.View
import android.view.Window
import android.view.WindowInsetsController

/*
    * Utility function to set the status bar icons color to light or dark.
 */
fun setLightStatusBar(window: Window, isLight: Boolean = true) {
    if (Build.VERSION.SDK_INT >= Build.VERSION_CODES.R) {
        val controller = window.insetsController
        if (controller != null) {
            if (isLight) {
                controller.setSystemBarsAppearance(
                    WindowInsetsController.APPEARANCE_LIGHT_STATUS_BARS,
                    WindowInsetsController.APPEARANCE_LIGHT_STATUS_BARS
                )
            } else {
                controller.setSystemBarsAppearance(
                    0,
                    WindowInsetsController.APPEARANCE_LIGHT_STATUS_BARS
                )
            }
        }
    } else {
        val decorView = window.decorView
        var flags = decorView.systemUiVisibility
        flags = if (isLight) {
            flags or View.SYSTEM_UI_FLAG_LIGHT_STATUS_BAR
        } else {
            flags and View.SYSTEM_UI_FLAG_LIGHT_STATUS_BAR.inv()
        }
        decorView.systemUiVisibility = flags
    }
}
```

