---
date: '2025-02-15T10:25:15+05:30' 
draft: false
title: 'Static App Shortcuts in Android: A Simple Implementation Guide'
categories: ["Android"]
---
Have you ever long-pressed an app icon and seen quick actions like **"Search"** or **"New Message"**?  
These are **App Shortcuts**, a powerful feature that allows users to interact with your app **faster** and **more efficiently**.  

In this guide, we'll explore how to implement **static app shortcuts** in Android to enhance user experience.  

## What Are App Shortcuts?  

**App shortcuts provide quick access to common app features when the user long-presses your app icon.**  
Along with system options like **App Info** and **Pause App**, you can define your own **custom shortcuts** for essential actions.  

📌 **Example use cases:**  
✔ **"Create Note"** in a notes app (bypasses unnecessary navigation)  
✔ **"Search"** shortcut (instantly opens search with keyboard focused)  

Users can also **pin shortcuts to their home screen** for even faster access!  

### **How It Looks on a Device**  
![Static App Shortcut example](/img/static-app-short-cut.jpg#center)  

---  

## 🚧 Limitations of Static App Shortcuts  

🔹 **Requires API level 25+ (Android 7.1 and above)**  
🔹 **Maximum of 4 static shortcuts per app** (to prevent misuse)  

Since shortcuts are limited, **choose only essential ones that improve UX!**  

---  

## 🛠 Implementation Guide  

The best part? **Static shortcuts don’t require any dependencies**—we just define them in XML.  

### **1️⃣ Creating Shortcut Values**  

1. Switch to **Project View** in Android Studio.  
2. Create a new folder in `res/` named **`xml-v25`**.  
3. Inside `res/xml-v25/`, create a new file named **`shortcuts.xml`**.  
4. Add the following shortcut definition:  

```xml
<?xml version="1.0" encoding="utf-8"?>
<shortcuts xmlns:android="http://schemas.android.com/apk/res/android">

    <shortcut
        android:shortcutId="create_note_shortcut"
        android:enabled="true"
        android:shortcutShortLabel="@string/create_note"
        android:shortcutLongLabel="@string/create_note_description_for_shortcut"
        android:icon="@drawable/ic_shortcut_create_note">

        <intent
            android:action="android.intent.action.VIEW"
            android:targetPackage="com.example.myapp"
            android:targetClass="com.example.myapp.MainActivity">

            <!-- Extra key to identify the shortcut action -->
            <extra android:name="content_key" android:value="_ssKey_create_note"/>
        </intent>

    </shortcut>
</shortcuts>
```  

🔹 The `content_key` extra helps identify **which shortcut was used**, so we can handle it later.  

⚠️ Since my app's minimum supported version is API 24, i have to add it on the **`xml-v25`** if your app's minimum supported version is 25 or above you can add the **`shortcuts.xml`**  directly to **`xml`** folder.

---  

### **2️⃣ Adding to AndroidManifest.xml**  

Add the following inside your **`AndroidManifest.xml`**, **before** the closing `</activity>` tag:  

```xml
<meta-data
    android:name="android.app.shortcuts"
    android:resource="@xml/shortcuts"/>
```  

After adding this, your manifest should look like this:  

```xml
<manifest xmlns:android="http://schemas.android.com/apk/res/android">
    <application
        android:allowBackup="false"
        android:icon="@drawable/ic_launcher_round"
        android:label="@string/app_name">

        <activity android:name=".MainActivity">
            <intent-filter>
                <action android:name="android.intent.action.MAIN" />
                <category android:name="android.intent.category.LAUNCHER" />
            </intent-filter>

            <!-- Registering the shortcut -->
            <meta-data
                android:name="android.app.shortcuts"
                android:resource="@xml/shortcuts"/>
        </activity>

    </application>
</manifest>
```  

---  

### **3️⃣ Handling Shortcut Logic in Code**  

When the user taps a shortcut, it launches the **MainActivity** with an extra `content_key`.  
We can handle this in Kotlin:  

```kotlin
val activity = LocalContext.current as MainActivity

// Check which shortcut was used
val shortcutCode = when {
    activity.intent.getStringExtra("content_key")?.contains("create_note") == true -> 1
    else -> 0  // Default: No shortcut used
}

// Handle shortcut action
LaunchedEffect(shortcutCode) {
    if (shortcutCode == 1) {
        navigateToNoteCreationScreen()
    }
}
```  

📌 **Shortcut Flow:**  
1️⃣ User **long-presses** the app icon and selects "Create Note".  
2️⃣ App opens **directly in note creation mode** (keyboard preloaded).  
3️⃣ Saves **3+ clicks** compared to manual navigation! 🚀  

---  

## ✅ Key Takeaways  

✔ **App Shortcuts improve UX** by reducing navigation steps.  
✔ **Maximum of 4 static shortcuts per app** (API 25+ required).  
✔ **Define shortcuts in `res/xml-v25/shortcuts.xml`**.  
✔ **Use `content_key` in the intent** to determine the shortcut action.  

### **🔗 Implementation in My App**  
[📌 Commit with Static App Shortcuts on Jot Notes](https://github.com/Eganathan/jotters-space-android/commit/6f0070aef1c0cd53b0d72450121c77a2edf38482)  

Hope this guide helps! Feel free to share your thoughts via my social handles. 😊  

---  

**Thank you for reading!** 🎉