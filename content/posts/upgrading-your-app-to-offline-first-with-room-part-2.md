---
date: '2025-02-05T13:02:29+05:30' 
draft: false
title: 'Setting up Room and exploring its Key components (#OFR-02)'
tags: ["Room","Android","Offline-First-App"]
categories: ["Android","KMP"]
---

Previously we discussed about the strategies and picked Google's Room Library,so now lets get started with setting up the library and discuss about the key components of room.

## Setup

Since Google has the best article for setting up, I will be skipping the setup up
Dependency setup: [Official Guide on Setting up Room Dependencies and plugins](https://developer.android.com/jetpack/androidx/releases/room)

Please do ensure you follow the above guide and then sync and build your project successfully, as it will help you to try out the components yourself. In this article, my intention is to explore the key components of Room, a bare minimum you need to know to implement a simple offline-first app. For a detailed and more complex use case, check out my upcoming article.

## Key Components

Primarily, there are three important components: Entity, DAO's, and Database, The entity represent a table. Dao's are an interface to write queries and define your operations. The database is where you associate your entities and include the dao's you would like to access from outside; hence, it's the entry point of your database. Let's check it out one by one:

### Entity

Any class annotated with @Entity is an entity, and those classes represent a table in the database. Here is an example of what a simple entity would look like:

```kotlin
@Entity
data class LocalHabitTracker(
    @PrimaryKey(autoGenerate = true) val id: Long,
    val associatedHabitId: Long,
    val positionX: Int,
    val positionY: Int,
    val note: String
)
```

An entity must have a minimum of one parameter that is annotated with @PrimaryKey(), and it would be the primary key for uniquely identifying a single row; the value of the parameter must be unique; otherwise the app will crash.

You can set the autogenerate to true just like the above code snippet. Ensure the type is primitive; I prefer Long, but if you are expecting very few entries, you can use Short; otherwise, you decide it according to your needs. If you have no clue, then stick with Long.

The entity can be further modified with a custom name for the table, indexing, custom column names, etc. We can discuss those in the upcoming articles.

### DAOs

Short for Data Access Object, as the name suggests, this is the interface between the developer and Room for accessing the tables in a safe and simplified way. It's basically an interface with an annotation with @Dao; inside you can use Room query annotations to access and modify the tables as per your requirements. Here is a sample code snippet of how a DAO for our case will look like:

```kotlin
@Dao
interface HabitTrackerDao {

    //Query to get all the habit trackers
    @Query("SELECT * FROM LocalHabitTracker")
    suspend fun getAll(): List<LocalHabitTracker>

    //Query to get a habit tracker by id
    @Query("SELECT * FROM LocalHabitTracker WHERE id = :id")
    suspend fun getById(id: Long): LocalHabitTracker

    //Insert's the row into a table, if the data already exists, it will crash
    @Insert
    suspend fun insert(habitTracker: LocalHabitTracker)

    //Update's the row if the data already exists
    @Update
    suspend fun update(habitTracker: LocalHabitTracker)

    // Upsert's the row, if the data already exists, it will update, else it will insert
    @Upsert
    suspend fun upsert(habitTracker: LocalHabitTracker)

    // Deletes the row from the table
    @Delete
    suspend fun delete(habitTracker: LocalHabitTracker)
}
```

As you can see in the above snippet, Room simplifies the process of implementing an offline-first app. Though it looks simple, don't assume that Room is only for simple use cases; I have kept it minimal to not overcompensate it. We will definitely go through the complex use cases in the upcoming articles.

The interface annotated with @Dao is typically called Dao's; here our Dao is called HabitTrackerDao.''It is preferred to name your Dao with a postfix 'Dao.'.

I would highly recommend you access only one entity (table) in a single DAO, but Room does not restrict you from accessing multiple entities (tables) in the same DAO, but trust me, this will be helpful as your product grows. We will talk about how to handle the complex cases in the next article on Room.

 Do note There is no restriction on the number of Dao's you can have; just ensure the names don't conflict with each other, and the minimum target can handle it (no need to worry if your entities are less than 50).

### Database

Now we have tables or entities and the DAOs that enable us to access and interact with the tables. Now, there can be multiple databases in an Android app, so how does Room know that the entity and DAO are part of which database? That's exactly what we are going to define next.

Take a look at the following code snippet of our simple database:

```kotlin
@Database(
    entities = [LocalHabitTracker::class], // Add all your entities here
    version = 1,//version of the database,update this once you make changes to the schema(Entity) of the database
)
abstract class HabitTrackerDataBase() : RoomDatabase() {

    //Room will implement this funtion and return the implementation of this dao
    abstract fun habitTrackerDao(): HabitTrackerDao
   
    //Add all your Dao's here that you want to access

    
}
```

This might be a little tricky, but it's pretty simple. We are creating an abstract class that extends the RoomDatabase and also annotating it with @Database to represent the class as a database and letting the room compiler know that this is one of the databases and the declared entities inside the array are to be associated with this database, and this serves as an entry point to the database.

The entities array as of now has only one entity for simplicity, so don't forget to add all the entities in this array. Another thing to note is that whenever you are modifying the entities, ensure you upgrade the version of the database to avoid a crash. The reason for this crash is that Room does not know how to handle the schema changes unless a migration strategy is provided; we will talk about this in the next article. In a real-world application, the table could contain user data, and we usually want to preserve this data during schema updates, making migrations a crucial part of database version management.

Manually Creating a Database and Interacting
Hooray! Finally, we are here. You can build it for accessing the database and interacting with it easily. Do check out the code below; it shows a simple manual creation of the database. 

```kotlin
class MainActivity : AppCompatActivity() {

    override fun onCreate(savedInstanceState: Bundle?) {
        super.onCreate(savedInstanceState)

        // Manually Creating the Database
        val habitTrackerData = Room.databaseBuilder(
            context = this, // ApplicationContext
            klass = HabitTrackerDataBase::class.java, // Database abstract class
            name = "your_custom_database_name" // custom name for the table
        ).build() 
        
        // You can receive the implementation of the Dao class from the database object
        val habitTrackerDao = habitTrackerDB.habitTrackerDao()
        
       
        setContent {
            AppTheme {
                AppNav(activity = this, habitLocalService = habitTrackerDao)
            }
        }
    }
}
```

We are using the DatabaseBuilder function from the Room Companion object to build our database; the result of the build is our own implementation of the requested database, with which we can get the implementation of our DAO's from Room and do our interactions... 

Do ensure you don't use the UI thread for accessing the database, as it can cause issues; otherwise, you should not have any other issue, but if you face any issue, feel free to start a discussion below:

This is a simple implementation, but a typical app developer would use a DI. Whether to use DI or not is your decision,, depending on the scale of your project. but I will be using it in the final project after this series of articles.

Thanks for reading so far. While this already feels like a lot, these could be enough for your first simple projects, but there are a lot of other interesting cases we have not yet talked about, like @RawQuery, Junctions, TableViews, and many more, which we shall discuss in the next article.

feel free to share your feedbacks and suggestions below.