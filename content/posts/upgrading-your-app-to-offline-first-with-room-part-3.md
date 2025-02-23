---
date: '2025-02-22T11:23:17+05:30' 
draft: false
title: 'Quickly Exploring Key Components of Room (#OF03)'
---
## 👋 Intro

On the [previous article](https://md.eknath.dev/posts/upgrading-your-app-to-offline-first-with-room-part-2/) we have set-up the Room dependencies and plugins, Now lets get into the primary key components of a room library.

There are three important components: **Entity**, **DAO**'s, and **Database**.  

- **Entity** represents a single row of a table. (Table structure)
- **DAO**'s (Data Access Objects) are interfaces to write queries and define operations.
- **Database** is where you associate entities and include the DAO's you'd like to access from outside.  

Let's check it out one by one! 🔍

---

## 🏗️ Entities: Defining Your Data Structure

Any class annotated with `@Entity` is an entity, which represents a table in a database,ensure you follow [Normal Forms](https://www.geeksforgeeks.org/normal-forms-in-dbms/) while creating a perfect schema, lets look how an entity/table is represented here.

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

**Key Points:**
✅ An entity **must have** at least one parameter annotated with @PrimaryKey().
✅ The **primary key** must be unique, or your app will crash.
✅ If you want Room to **auto-generate** the primary key, set autoGenerate = true.
✅ Stick to **primitive types** like Long, but if you’re expecting very few entries, you can use Short.

The entity can be further customized with **table names, indexing, and custom column names**, which we’ll cover in later articles. 🎯

### 🔗 DAOs: Your Data Gateway

DAOs serve as the interface between your app and the database, providing an abstraction layer. This is a bridge between you the developer and the Database all your interactions happen here,

**✍️ Example:**

```kotlin
@Dao
interface HabitTrackerDao {

    // Query to get all habit trackers
    @Query("SELECT * FROM LocalHabitTracker")
    suspend fun getAll(): List<LocalHabitTracker>

    // Query to get a habit tracker by ID
    @Query("SELECT * FROM LocalHabitTracker WHERE id = :id")
    suspend fun getById(id: Long): LocalHabitTracker

    // Insert a new row into the table (fails if duplicate)
    @Insert
    suspend fun insert(habitTracker: LocalHabitTracker)

    // Update an existing row
    @Update
    suspend fun update(habitTracker: LocalHabitTracker)

    // Upsert: If exists, update; otherwise, insert
    @Upsert
    suspend fun upsert(habitTracker: LocalHabitTracker)

    // Delete a row from the table
    @Delete
    suspend fun delete(habitTracker: LocalHabitTracker)
}
```

**Best Practices:**

✅ **One entity per DAO:** It’s best to separate each table into its own DAO for maintainability.
✅ **No limit** on the number of DAOs, but make sure they have unique names.
✅ **Keep queries optimized** to avoid performance issues as your app scales.

We’ll cover complex cases like @RawQuery, Junctions, and TableViews in later articles! 🔮

### 🏛️ Database: The Central Hub

Now that we have entities and DAOs, we need to connect them through a database class so it can generate the table and Dao's for us to interact with and it also manages integrity validation, migrations and works as a central hub for our interactions with tables.

**✍️ Example:**

```kotlin
@Database(
    entities = [LocalHabitTracker::class], // Add all your entities here
    version = 1 // Update this when modifying the schema
)
abstract class HabitTrackerDataBase : RoomDatabase() {

    // Room will auto-implement this function and return the DAO implementation
    abstract fun habitTrackerDao(): HabitTrackerDao

}
```

**Important Notes:**

✅ Always increase the version when modifying entities to prevent crashes.
✅ Room doesn’t know how to handle schema changes unless you define a migration strategy.
✅ Multiple databases can exist in an app, so this class serves as an entry point for Room.

Migrations and schema updates are crucial for real-world apps to prevent data loss. We’ll cover that soon. 🔄

🎛️ Manually Creating and Using the Database

Now, let’s see how to manually create and interact with the database in our app.

**✍️ Example:**

```kotlin
class MainActivity : AppCompatActivity() {

    override fun onCreate(savedInstanceState: Bundle?) {
        super.onCreate(savedInstanceState)

        // Creating the database manually
        val habitTrackerDB = Room.databaseBuilder(
            context = this, // ApplicationContext
            klass = HabitTrackerDataBase::class.java, // Database abstract class
            name = "habbit_tracker" // Custom database name
        ).build() 
        
        // Get the DAO implementation
        val habitTrackerDao = habitTrackerDB.habitTrackerDao()

        setContent {
            AppTheme {
                AppNav(activity = this, habitLocalService = habitTrackerDao)
            }
        }
    }
}
```

**⚡ Pro Tips:**

✅ Don’t use the UI thread for database operations; always use coroutines or background threads.
✅ In real-world apps, use Dependency Injection (DI) for managing database instances efficiently.
✅ Avoid creating multiple database instances, as it can lead to memory leaks and performance issues.


Mostly this is enough for creating simple CRUD apps, though it looks simple the entities will be converted into a query to create tables, A concrete classes will be created for each Dao's and other essential tasks will be carried by room it self easing our development and debug process.

#### 🚀 What’s Next?

This was a quick summary on each of the key components, on the next article we will dive a little deeper into **@Entity** its keys and customizations, the purpose of this series to learn each one of them in detail.

I’d love to hear your feedbacks and suggestion.
Thanks for reading! 🚀