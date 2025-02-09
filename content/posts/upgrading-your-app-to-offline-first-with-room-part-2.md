---
date: '2025-02-05T13:02:29+05:30' 
draft: true
title: 'Setting-up Room Library and its dependencies(#OF02)'
tags: ["Room","Android","Offline-First-App"]
categories: ["Android","KMP"]
---

Previously we discussed some important strategies and picked Google's Room Library,now lets get started with setting up the library and a deeper look into the dependencies.

## Official Documentation

The Google team keeps the document up-to-date, and has a simper set-up guide so feel free to check it out. Obviously you might be wondering why write an article if the content is already available, The team at google have to consider all the developers equally i meant the Java and Kotlin users, while most of us have migrated to kotlin, some still are using Java hence the documentation has both dependencies but we don't need all of them hence this article.

So here you go: [Official Guide on Setting up Room Dependencies and plugins](https://developer.android.com/jetpack/androidx/releases/room).


## Setting up Dependencies

Let's first ensure the project's `build.grade` has `google()` and `mavenCentral()` as locations to find our dependencies, this will allow the gradle to search for the dependencies there, some specific organizations might host their dependencies on a different  domain, you can also add them here but for now lets ensure your **projects** `build.gradle` has the `google()` and `mavenCentral()`:

```kotlin
buildscript {
    repositories {
        google()
        mavenCentral()
    }
}
```

Head to your module's `build.grade` file and add following dependencies to your dependencies block and add only the Room dependencies from the below block of code:

```kotlin
dependencies {
    // Other dependencies 
    // ...

    // Room Dependencies (Copy from this line)
    val room_version = "2.6.1"

    //Room-core
    implementation("androidx.room:room-runtime:$room_version")
    
    // Annotation Support
    ksp("androidx.room:room-compiler:$room_version")

    // Kotlin Extensions and Coroutines support for Room (Optional)
    implementation("androidx.room:room-ktx:$room_version")
    
    //(don't copy from this line)
}
```

You can visit [Maven Central](https://mvnrepository.com/artifact/androidx.room/room-runtime) for latest stable version and its details, also you can head to Google's official Doc for the same


Now lets add the plugin to the the project level `build.grade` file:

```kotlin
plugins {
    id("androidx.room") version "$room_version" apply false
    //other plugins here
}
```

Lets add the plugin to our module but adding the following to out module's 'build.gradle' file:

```kotlin
plugins {
    id("androidx.room")
}
```

we also have to add a directory, so the room can save the schema somewhere so lets add that as well:

```kotlin
android {
    ...
    room {
        schemaDirectory("$projectDir/schemas")
    }
}
```
Now you can 'sync` the project and it should work as expected
