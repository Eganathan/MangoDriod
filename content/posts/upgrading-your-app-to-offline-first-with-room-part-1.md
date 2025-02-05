---
date: '2025-02-05T09:23:57+05:30' 
draft: false
title: 'Upgrading Your App to Offline First With Room Part 1'
---

Making your app Offline first is extremely essential if you intend to provide a better user experience for your users, but not just that it makes your app faster by reduce the number of network call which in turn also reduces the running cost of servers significantly, i can yap more about why this is must but since you have already decided to invest in this lets skip it for now.

The whole idea of offline-first application is to persist the remote fetched data on device so if and when the user requests the same data again we can provide it much faster skipping the remote call process again until the validity expires, there are many other complexities we will discuss later but this is the gist of what it means to be offline first app.

### Offline Strategies

Primarily there are two strategies for implementing this one is Partial-Offline-first(ReadOnly Offline First) and the other is Fully-Offline-First, the only difference between them is weather you want to allow user to modify their data offline, if the answer is yes then you promise the user a full offline Create,Read,Update and Delete(CRUD) Operations while this sounds really nice to have the complexities involved in implementing this is pretty hectic, painful and the percentage of errors data will be significantly high, sorry if the previous statement made you re-thing the decision but wait we can also implement a simpler Partially Offline method which significantly reduces the complexities and pain involved in achieving offline-first.

### Partial Offline First(or ReadOnly)

Like i mentioned above this is a much simpler approach with much less complexities and errors,the core concept of this is to allow user to do write operations(Create,Update,Delete) only when the user is online and the response from the server is used to update the local entity which ensure that the entity is same as whats in the server, i hope i have not complicated this, Simply further the user will be allowed to do any write operations (Create,Update,Delete) they have to be online.

Restricting the write operations(CUD) when the user is offline, We can effectively keep our local data clean and up-to-date with server changes, and this will significantly reduce the complexities we have to deal with and the user is happy  and aware that he can access the app offline but can view only the previous accessed entity, its a win win situation for users and developers in the starting stage of app development.

### What Library to choose ?

Yes!,there are wide verity of options to choose from but we are going to stick with Google Room's Persistence Library as its most preferred option for most Android and KMP projects as its extremely powerful yet simple to learn and implement.

## Intro to Google Room's Persistence Library

 Google Room's Persistence Library is built on top of SQLite that provides a more convenient and structured way to manage your app's local database. It lets you work with your data as Kotlin objects (data classes) instead of manually formulating them using SQL queries, which itself is a tedious task prone to many errors.

 Room also simplifies interactions with the database with many great features like validating the queries, seamless integration with Kotlin Flow, paging, LiveData, and many more. These features make Room the most preferred option for offline-first apps, as it expedites the process and helps us to avoid issues early in the development cycle, lets just begin by setting up: