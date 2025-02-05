---
date: '2025-02-05T09:23:57+05:30' 
draft: false
title: 'Upgrading Your App to Offline First With Room Part 1 (#OFR-1)'
tags: ["Room","Android","Offline-First-App"]
categories: ["Android","KMP"]
---

Making your app Offline first is extremely essential if you intend to provide the best user experience for your users,it makes your app significantly faster by reduce the number of network call which in turn also reduces the running cost of servers, i can still yap a lot more about why this is must but since you have already decided to invest in this lets focus on the core topic.

The whole idea of offline-first application is to persist the remote fetched data on device so if and when the user requests the same data again we can provide it much faster skipping the remote call process again until the validity expires, there are many other complexities we will discuss later but this is the gist of what it means to be offline first app.

### Fair Warning

There are many ways to solve one problem, and what iam discussing here is my approach towards this there may better methods and solutions but since so far nothing has aligned with our/my requirements i had to make one my self, so what iam trying to saying is take my inputs with a pinch of salt, iam more than happy to hear your feedback and suggestions lets talk, discuss and debate this will enrich us both equally but as things progress my views and approach on this may change and i will actively be updating these articles.

that being said,lets just dive in.

### Offline Strategies (Partial or Full)

Primarily there are two strategies for implementing this of which one is Partial-Offline and the other is Fully-Offline, the only difference between these are, That we allow user to modify their data offline or not.

On the Fully-Offline method you promise the user a fully functional offline app with Create,Read,Update and Delete(CRUD) Operations,While the other promises only Read operation when offline and the write operations only when the user is connected to the network.

While Full-Offline approach makes sense, the complexities involved in implementing this is pretty complex, hectic, painful and more error prone and honestly a bad UX if your user has multiple devices connected to same account, imagine the user creates some important data on his tablet without connecting to the network and then forgets to sync and then at work he is puzzled to find the data missing on his personal mobile phone, the user may raise a ticket and might even get frustrated and stop using the app thinking we lost their data, while this might sound like a lame reason to ditch solving problem, i might explore this later in this series.

So the Partial approach  aligned better for our use-case, we decided to go with Partially-Offline as its significantly less complex and workable quick solution with less bux and provides best UX to users, so lets dive a little deeper on this approach:

### Partial Offline First Apps(or ReadOnly)

This is a simplest approach with less complexities and much better error rates,the core concept of this is to allow user to do write operations(that is Create,Update,Delete) only when the user is connected to network and the response from the server is used to update the local data effectively ensuring that the entity is in similar form as server,Simplifying further the user will be allowed to do any write operations (tha t is Create,Update,Delete) only when they are connected to the network, which means when the user is offline they will have access to the data but restricted to only Viewing them until the device is connected to the network.

By restricting the write operations(CUD) when the user is offline, we are ensuring the data we have is clean and up-to-date with server, and this will significantly reduce the complexities in the business logics involved in maintaining the data correctness,and also at the same time providing the best of user experience.

On the previous example of multi-device-logins the user will be able to view the data no matter which device he has created them as its stored ont he cloud, so he can just sync and refresh the data and access his valuable data with ease and we avoided the confusion and the frustration they might have had otherwise.

I hope you are clear on whats Partial and Fully Offline App means, both are just different approaches of implementing offline-first-apps so depending on the use case one might shine brighter than other.

Ok since we are settled on this decision, lets move on to the next one, How we are planing to fetch the data from the server? wether we try to clone remote data-base as is or partially or only keeping the data user has fetched, this is much simpler decision and lets see options we have:

### synchronization Strategy

Primary options here are OnDemand (or Pull-based synchronization) or Mimic(or Push-based synchronization),the OnDemand strategy which fetches the data on user requests like on user navigation to certain screens the invalidation happens on deletion or expiry of data's persistence period set by the developer and the other strategy is to clone and mimic the remote database and keep a carbon copy of the database and invalidation happens once the server sends a signal that the remote database was modified and we re-clone the database again so you must have already guessed the pros and cons of both, the OnDemand is much light weight and User centric and other is more heavy and doing some un-necessary heavy lifting, note im biased due to my requirements so keep that in mind while selected your options depending on your use-cases.

Though i mentioned that i am aligned with the OnDemand strategy i do fetch some initial data after the login so the user has some data to see on initial navigation, after the initial fetch i switch to 100% onDemand, this Hybrid model enables me to ensure the user is not navigated to a loading screen on initial landing screen inside the app thus providing a better ux.

Iam going to stick with mostly OnDemand since my use-case is complex due to apps requirement, former is also accomplishable depending on the requirement and especially if the data set is small and not that complex so pick yours depending on your requirement.

### What Library too choose?

Yes!,there are wide verity of options to choose from but i loved to stick with Google Room's Persistence Library as its most preferred option for most Android and KMP projects as its Simple and also extremely powerful, it expedites the development process 10X(my experience) compared to other options available, Room is your friend in this journey so lets check a bit more about it

### Intro to Google Room's Persistence Library

Google Room's Persistence Library is built on top of SQLite that provides a more convenient and structured way to manage your app's local database. It enables us to work with data as Kotlin Data classes instead of manually formulating them using SQL queries, which itself is a tedious task prone to many errors.

Room also simplifies interactions with the database with many great features like The Compile-time verification of SQL queries,Convenience annotations that minimize repetitive and error-prone boilerplate code, Streamlined database migration paths and seamless integration with Kotlin Flow, paging, LiveData, and many more like raw quires.

These features make Room the most preferred option, as it expedites the process and helps us to avoid issues early in the development cycle by saving time and resources i am in love with this library so Room Library is your friend in this journey so we will discuss more about this in the next article in this series.

### Final Note

As i mentioned initially this is my journey on making our app offline-first, if you have feedbacks or suggestions or Doubts feel free to connect with me on any [social media](httsps://ekanth.dev) or [Email Me](mailto:mail@eknath.dev)

Thank you for taking your time to read this article.
