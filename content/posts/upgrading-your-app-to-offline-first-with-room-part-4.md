---
date: '2025-02-28T19:39:05+05:30' 
draft: true
title: '@Entity() in Room- A Deeper Dive'
tags: ["Room","Android","Offline-First-App"]
categories: ["Android","KMP"]
---

In our [previous article](https://md.eknath.dev/posts/upgrading-your-app-to-offline-first-with-room-part-3/), we explored the key components of Room. Now, let’s take a deep dive into Room Entities, their importance, and the various ways to customize them.

**Entities** are the foundation of Room—they define how your data is stored in the database. Properly structuring your entity ensures efficient querying, maintainability, and scalability. Let's break it down! 🛠️

## 🏗️ What is an Entity?
An **Entity in Room represents a table in the database**. Each instance of the entity corresponds to a row in the table. Room generates the corresponding SQL table schema based on the entity class.

**Defining an Entity:**

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

**Breaking It Down:**

- `@Entity` tells Room that this class is a database table.
- `@PrimaryKey` is used to uniquely identify each row.
- `autoGenerate = true` ensures Room generates unique IDs automatically.
- `@Ignore` → Excludes a field from being stored in the database.

---

## 🔄 Customizing Entities

Room provides several ways to customize entities to fit your data structure requirements. Let's explore these! 🚀

### 1️⃣ Custom Table and Column Names

By default, Room uses the **class name as the table name** and **variable names as column names**. You can override this using annotations:

```kotlin
@Entity(tableName = "habit_tracker")
data class LocalHabitTracker(
    @PrimaryKey(autoGenerate = true) val id: Long,
    @ColumnInfo(name = "habit_id") val associatedHabitId: Long,
    @ColumnInfo(name = "pos_x") val positionX: Int,
    @ColumnInfo(name = "pos_y") val positionY: Int,
    val note: String
)
```

- tableName changes the SQL table name.
- @ColumnInfo(name = "custom_name") changes the column name in the table.

### 2️⃣ Indexing for Faster Queries

Indexes speed up query performance, especially for large datasets. Use @Index for frequently queried columns.

```kotlin
@Entity(
    tableName = "habit_tracker",
    indices = [Index(value = ["habit_id"])]
)
data class LocalHabitTracker(
    @PrimaryKey(autoGenerate = true) val id: Long,
    val associatedHabitId: Long,
    val positionX: Int,
    val positionY: Int,
    val note: String
)
```

- Indexing `habit_id` speeds up lookup queries on this column.

### 3️⃣ Unique Constraints

Prevent duplicate values using `unique = true`.

```kotlin
@Entity(
    tableName = "habit_tracker",
    indices = [Index(value = ["habit_id"], unique = true)]
)
data class LocalHabitTracker(
    @PrimaryKey(autoGenerate = true) val id: Long,
    val associatedHabitId: Long,
    val positionX: Int,
    val positionY: Int,
    val note: String
)
```

- Ensures habit_id remains unique across all rows.

### 4️⃣ Foreign Keys for Relationships

Define relationships between tables using `@ForeignKey`.
```kotlin
@Entity(
    tableName = "habit_tracker",
    foreignKeys = [
        ForeignKey(
            entity = Habit::class,
            parentColumns = ["id"],
            childColumns = ["habit_id"],
            onDelete = ForeignKey.CASCADE
        )
    ]
)
data class LocalHabitTracker(
    @PrimaryKey(autoGenerate = true) val id: Long,
    val habit_id: Long,
    val positionX: Int,
    val positionY: Int,
    val note: String
)
```
- habit_id references id from the Habit table.
- onDelete = CASCADE ensures that deleting a Habit deletes all related LocalHabitTracker records.

### 5️⃣ Embedded Objects

Instead of creating separate tables, you can embed objects inside an entity.

```kotlin
data class Position(
    val x: Int,
    val y: Int
)

@Entity
data class LocalHabitTracker(
    @PrimaryKey(autoGenerate = true) val id: Long,
    val associatedHabitId: Long,
    @Embedded val position: Position,
    val note: String
)
```

- The Position object is embedded as separate columns (x, y) in LocalHabitTracker.

---


## 🔍 Best Practices

✅ Use `autoGenerate = true` for `@PrimaryKey` to avoid conflicts if you don't have a server that provides it.  
✅ Optimize query performance with `@Index`.  
✅ Define `@ForeignKey` relationships to maintain integrity but optional for complex cases.  
✅ Use `@Ignore` for transient fields that shouldn't be stored in the database.  
✅ Keep entity classes small and focused—avoid unnecessary logic inside them.  
✅ Ensure Proper Indexing: Index frequently queried columns to improve performance.
✅ Use Primitive Types: Room doesn’t support custom objects directly. Use `@TypeConverter` if needed.

---

## 🚀 Conclusion

Room Entities form the foundation of Android's database layer, allowing structured and efficient data management. By following best practices, you ensure scalable and maintainable database architectures.

Want to dive deeper? Stay tuned for the next article in this series! 🚀

## **Final Thoughts**  

This is my journey in **building an offline-first app**. I’d love to hear your feedback, suggestions, or questions!  

Feel free to connect with me on:  
📩 **[Email](mailto:mail@eknath.dev)**  
🌍 **[Website](https://eknath.dev)** 
💫 **[LinkedIn-Post for comments and feedbacks](https://www.linkedin.com/posts/eganathan_offlinefirstandroid-offlinefirst-android-activity-7294912159627546624-TG77?utm_source=share&utm_medium=member_desktop&rcm=ACoAABYcOpgBgvDfy-0uUjfX0HTNqzzLfKZQAQU)** 

🔖 [Previous Article in this Series](https://md.eknath.dev/posts/upgrading-your-app-to-offline-first-with-room-part-3/) 
🚀 **Stay tuned for Part 5!** 🚀 

<!-- 🔖 [Next Article in this Series](https://md.eknath.dev/posts/upgrading-your-app-to-offline-first-with-room-part-5/) -->
