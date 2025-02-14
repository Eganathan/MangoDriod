---
date: '2025-02-13T10:25:22+05:30' 
draft: false
title: 'Implementing Static App Shortcuts on Android(Draft)'
---
App shortcuts enable the user to interact with you app quickly without any complex navigation's from users part, it simplifies and encourages the user to interact with the app more swiftly.

## What is an app short cut?

**They are some custom options that pop's up when the user long presses your app icon** along with some system provided short app-specific cuts`App Info` and `Pause App`, This provides a better UX for users by providing a fastest way to interact with most common app-specific operations.

Users could also choose to pin these shortcuts on their home screens so the long press can also be avoided, basically it provides a single click action that user will otherwise not be able to perform that quickly.

Here is how it looks on the actual device:
![Static App Shortcut example](/img/static-app-short-cut.jpg#center)

## Limitations

This is supported only from API 25+ and since the developer might misuse this the developer team has constrained to a maximum of 4, so make sure you add only what could ease the user experience.

1️⃣ You can only create a maximum of 4 static shortcuts in your app.    
2️⃣ Supported only from API level 25+

### Considerations

Since we are limited to maximum of 4, we must ensure the shortcut are absolutely essential and solves a common user problem because the user will get used to it and might even pin the shortcut to their home screen.

An example for a best use case for a shortcut will be   

1️⃣ **Creation in a note app**    
*This allows the user to avoid navigating to notes screen, click a button and click for focus.*

2️⃣ **Search Option**    
*User can swiftly navigate to search screen with a focused textfield with keyboard loaded already.*

So ensure you abide by these points:

✅ Add only essential shortcuts.   
✅ Ensure it provides value for the user.   
✅ Once added it must not be removed later.  

Since we are are clear on this, let's get our hands dirty;

## Implementation

The nice thing about Static App Shortcuts are that, it does not require any dependency we can get started by defining the shortcuts first, but before you have to create a new resource folder:

### 1️⃣ Creating the Shortcut values

1. Switch your project File View to Project from Android
2. Create a new folder in the `res` folder named `xml-v25`
3. Inside the `res/xml-v25/` create a new file xml resource file named `shortcuts.xml` with root element `shortcuts`
4. add your shortcuts to the file, like the example below

```xml
<?xml version="1.0" encoding="utf-8"?>
<shortcuts xmlns:android="http://schemas.android.com/apk/res/android">
    <shortcut
        android:shortcutId="custom-unique-short-cut-identifier"
        android:enabled="true"
        android:shortcutShortLabel="@string/create_note"
        android:shortcutLongLabel="@string/create_note_description_for_short_cut"
        android:icon="@drawable/ic_short_cut_creation">
        <intent
            android:action="android.intent.action.VIEW"
            android:targetPackage="dev.eknath.jottersspace"
            android:targetClass="dev.eknath.jottersspace.MainActivity">

            <extra android:name="content_key" android:value="_ssKey_create_note"/>
        </intent>
    </shortcut>
</shortcuts>
```

The intent extra `content_key` enables us to understand what shortcut was applied, here i have added a prefix:`_ssKey_` this enables me to map the shortcut keys much better, so on the above example i know this shortcuts intention is to create a note, so on the activity i know what to do to implement logic of the shortcut, we will talk about this again on step 3 so lets add this to manifest.

### 2️⃣ Adding it to Manifest

Ensure you add this to your apps `AndroidManifest.xml` file, it must be right before the ending `</activity>` tag

```xml
 <meta-data
 android:name="android.app.shortcuts"
 android:resource="@xml/shortcuts"/>
 ```

after adding the above code your app's `AndroidManifest.xml` will look something like this:

```xml
<?xml version="1.0" encoding="utf-8"?>
<manifest xmlns:android="http://schemas.android.com/apk/res/android"
    xmlns:tools="http://schemas.android.com/tools">

    <uses-permission android:name="android.permission.ACCESS_NETWORK_STATE"/>
    <uses-permission android:name="android.permission.INTERNET"/>

    <application
        android:allowBackup="false"
        android:dataExtractionRules="@xml/data_extraction_rules"
        android:fullBackupContent="@xml/backup_rules"
        android:icon="@drawable/ic_launcher_round"
        android:label="@string/app_name"
        android:roundIcon="@drawable/ic_app_icon"
        android:supportsRtl="true"
        android:name=".AppName"
        android:theme="@style/Theme.AppTheme"
        tools:targetApi="31">
        <activity
            android:name=".MainActivity"
            android:exported="false"
            android:label="@string/app_name"
            android:theme="@style/Theme.AppTheme">
            <intent-filter>
                <action android:name="android.intent.action.MAIN" />

                <category android:name="android.intent.category.LAUNCHER" />
            </intent-filter>
            <meta-data
                android:name="android.app.shortcuts"
                android:resource="@xml/shortcuts"/>
        </activity>
    </application>

</manifest>
```

### 3️⃣ Handling Business Logic for the shortcuts

Now the app has the defined shortcuts and the system will take care of the UI, next handling the business logic.

The *Activity's* intent will have the provided `content-key` so on the launched effect we can get the value of `content-key` and decide on what to do next, this is what i have done to one of my app:

#### Example of Logic Handling

I have added a prefix `_ssKey_` on all my shortcut intent's extras, just like the example shared earlier and i have also associated each key with a number for ease of logic handling:

```kotlin
val activity = (LocalContext.current as MainActivity)
val shortCutCode = (if(activity.intent.getStringExtra("content_key")?.contains("create_note") == true) 1 else 0)`
```

on the example above 0 is the default value so i know its not any of the shortcuts, on the other hand if the value is 1 then i navigate them to an appropriate screen and in my case open a new note creation screen focused and keyboard at the bottom, if user had to do the same operation otherwise a minimum of 3 clicks are to be required `Launch the app -> Navigate to note screen -> Create NewButton -> Request Focus` instead the with the shortcut the user will now directly be at the creation screen on a single click if they have pinned the shortcut.

### Changeset of implementation on my app

[Commit with Static App Shortcuts on Jot-Android-app](https://github.com/Eganathan/jotters-space-android/commit/6f0070aef1c0cd53b0d72450121c77a2edf38482)

Hope you were able to implement the static app shortcuts easily, if you have any feedbacks or inputs please do share it via any of my social handles.

Thank you for reading :)
