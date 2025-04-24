---
date: '2025-03-09T13:18:39+05:30' 
draft: false
title: 'DAO: The Backbone of Offline-First Apps (#OF05)'
tags: ["Room", "Android", "Offline-First-App"]
categories: ["Android", "KMP"]
---

In our [previous article](https://md.eknath.dev/posts/upgrading-your-app-to-offline-first-with-room-part-4/), we covered **Entities** in Room. Now, let’s explore **DAOs (Data Access Objects)** – the bridge between your app and the database. DAOs allow you to execute queries that allow is to insert, update, and delete records efficiently and thats exactly what we are going to explore today.

---

## What is a DAO?

A DAO is an interface annotated with @Dao that defines methods for interacting with the database. The Room compiler generates the necessary implementation for these interfaces and its methods, which enables us to access the database efficient and type safe. 

A typical DAO will look simar as the code below:

```kotlin
@Dao
interface ProductDao {

 @Query("SELECT * FROM products")
 suspend fun getAllProducts(): List<Product>

 @Query("SELECT * FROM products WHERE id = :productId")
 suspend fun getProductById(productId: Long): Product?

 @Insert
 suspend fun insertProduct(product: Product)

 @Insert
 suspend fun insertProducts(products: List<Product>)
    
 @Update
 suspend fun updateProduct(product: Product)

 @Delete
 suspend fun deleteProduct(product: Product)

 @Upsert
 suspend fun upsertProduct(product: Product)
}
```

While the `@Dao` interface is created by the developer the instance/Implementation of the DAO's are created by the compiler when the Database is created and the generated implementation file can be looked at the following path:

>`app/build/generated/source/kapt/debug/YOUR_PACKAGE_NAME/database/ProductDao_Impl.java` 

The file will contain the instance with `impl` as post fix and all the corresponding functions will have its own implementation accessing the SQLLite Database for example the **select query** annotated with `@Query` on the above **DAO** will generate an implementation code that is shared below, **if you are to use SQLLite Directly this is the code you would have to write manually for each query**:

The implementation of select query will look like this:

```java
@Override
public Object getAllProducts(Continuation<? super List<Product>> continuation) {
    final String _sql = "SELECT * FROM products";
    final RoomSQLiteQuery _statement = RoomSQLiteQuery.acquire(_sql, 0);
    return CoroutinesRoom.execute(__db, false, continuation, new Callable<List<Product>>() {
 @Override
        public List<Product> call() throws Exception {
            Cursor _cursor = DBUtil.query(__db, _statement, false, null);
            try {
                List<Product> _result = new ArrayList<>();
                while (_cursor.moveToNext()) {
                    Product _item = new Product();
                    _item.id = _cursor.getLong(_cursor.getColumnIndexOrThrow("id"));
                    _item.name = _cursor.getString(_cursor.getColumnIndexOrThrow("name"));
                    _item.price = _cursor.getFloat(_cursor.getColumnIndexOrThrow("price"));
                    _result.add(_item);
 }
                return _result;
 } finally {
                _cursor.close();
                _statement.release();
 }
 }
 });
}
```

Isn't it so nice how **instead of writing 24 lines we just have to write 1**  

🙏 **Thank You, Android and Google Team for making this extremely robust and performant.**

Now that we got an intro on **Dao** and what happens behind the scenes, let's go through the supported query annotations.

## Supported Query Annotations

In the previous section of DAO example code, you might have noticed the annotations (`@Insert`,`@Delete`...) on each functions, these annotations help the compiler to generate query object on your behalf so we can smoothly interact with the database, Let's go through each of them to understand how and when to use them effectively.

### @Insert - Insert Data into the Database

Used for **inserting single or multiple entries to a table**, this will **skip validation of checking if a duplicate entry with the same primary id exists**, so it's faster for insertion when you are clear that duplicate entries are impossible. In case **you inset a duplicate entry the app will crash** with the exception primary key already exists.

Here is an example of how the `@Insert` can be used:

```kotlin
...
 //Inserting single item
 @Insert(onConflict = OnConflictStrategy.REPLACE)
 suspend fun insertProduct(product: Product)     
 
 //Inserting multiple items
 @Insert
 suspend fun insertProducts(products: List<Product>)     
...
```

#### Conflict Strategy

Defining the conflict strategy on the query tells the room how to handle the conflict effectively by default it `NONE`:

- `NONE`: Default strategy when you insert duplicate it crashes the app.
- `REPLACE`: Keep the old data and ignore the new data.
- `ABORT`: Aborts the transaction entirely so none of the entries will be updated.
- `IGNORE`: Skip the entry and proceed to next

You can set your preference as per your requirement, but if you want the behavior of `REPLACE` hold on there is another annotation that we will learn about soon that is a better option.

⚠️ Beware: inserting duplicate entries will crash the app if you don't provide a conflict strategy.

### @Update - Modify Existing Data

Used for updating all columns of an existing row where the primary key matches, If the table does not contain a matching primary key, the update fails silently (no error or no exception) but the unmatched entries remain unchanged (they are not inserted or modified).

Like the `@insert` you can `@update` single or multiple entries, a sample code will look something like this:

```kotlin
...
 //Updating single item
 @Update
 suspend fun updateProduct(product: Product)   
 
 //Updating multiple items
 @Update
 suspend fun updateProducts(products: List<Product>)     
...
```

The update overrides the provided value to matched entries so if you accidentally provide a null value, that is exactly what the matched row's column will be, for example, if you want to mark the product as sold-out you will think you have to send only a product object with `id` and the `sold` value but if you do that all other values like name, date, and other values will be set as null so ensure you provide all values.


⚠️ You are overriding all values, so ensure you provide all values in each entry.    
⚠️ Unmatched rows will not be inserted, no errors or exceptions will be thrown

### @Upsert - Insert or Update in One Call

`@Upsert` is a combination of `@Insert` and `@Update`, if the entry matches the **primary-key** it updates them, otherwise it inserts them smoothly, you could use `@Insert` with `REPLACE` if your table has no primary key otherwise this is better.

This is an example of how the ``@Upsert` will be used in a dao

```kotlin
// upsert single item
@Upsert
suspend fun upsertProduct(product: Product)

// upsert bulk Item
@Upsert
suspend fun upsertProducts(products: List<Product>)
```

One thing to note is that the conflict is handled only for the primary key, if your table has other columns that are set as unique the upsert may still fail if that rule is ever broken due to new data.

⚠️ Requires the primary key     
⚠️ If your table has unique constraints on other columns, @Upsert may still fail.

### @Delete - Remove Entries from the Database

Enables you to delete single and multiple entities blissfully, if the row does not exist it fails silently which means that the entries that exist will be deleted and the other will not since it does not exist, here is how typical delete functions will look like:

```kotlin
// delete single item
@Delete
suspend fun deleteProduct(product: Product)

// delete bulk Item
@Delete
suspend fun deleteProducts(products: List<Product>)
```

I don't like to pass the entire entity for deletions so I prefer to use `@Query` for it so I can just pass the primary keys for deletion, but for simplicity, you can use the `@Delete` as well.

### @Query - The Most Powerful Annotation

The `@Query` Swiss knife allows you to write custom SQL queries to interact with your database. It provides more flexibility than other annotations (`@Insert`, `@Update`, `@Delete`) and is essential for performing simple/complex operations depending on our use cases.

```kotlin
...
// bulk get
@Query("SELECT * FROM products")
suspend fun getAllProducts(): List<Product>

// single get 
@Query("SELECT * FROM products WHERE id = :productId")
suspend fun getProductById(productId: Long): Product?

// search Query
@Query("SELECT * FROM products WHERE name LIKE '%' || :searchQuery || '%'")
suspend fun searchProducts(searchQuery: String): List<Product>

// deleting item with ID
@Query("DELETE FROM products WHERE id = :productId")
suspend fun deleteProductById(productId: Long)

// delete multiple items
@Query("DELETE FROM products WHERE id IN (:productIds)")
suspend fun deleteProductById(productIds: List<Long>)

// deleting all entries (truncates)
@Query("DELETE FROM products")
suspend fun deleteAllProducts()
...
```

Swiss Knife it is, you can do all kinds of operations with it, its gives us more flexibility but as we know "With Great Power comes to Great Responsibility". Although `@Query` is powerful, it can fail in various ways due to syntax errors, missing data, type mismatches, database constraints, etc.. so use it cautiously and expect exceptions and app crashes.

### @RawQuery - Fully Dynamic SQL Execution

The `@RawQuery` annotation in Room allows you to write and execute fully dynamic SQL queries, will will explore this later in this series it breaks the simplicity boundary because there is no compile-time safety on this.

## 🚀 Conclusion

Data Access Objects **(DAOs) are the backbone of efficient database operations in Room**. They provide a clean, structured way to interact with your database while leveraging compile-time safety and reducing boilerplate SQL code. With annotations like @Insert, @Update, @Delete, @Upsert, and @Query, DAOs make it easier to perform CRUD operations while maintaining performance and maintainability.

By using DAOs, you ensure that your Offline-First App has a seamless data layer, enabling a smooth and efficient user experience.

**Next, we will discuss about @RawQuery and its pro's and cons...**

## **Final Thoughts**  

This is my journey in **building an offline-first app**. I’d love to hear your feedback, suggestions, or questions!  

Feel free to connect with me on:  
📩 **[Email](mailto:mail@eknath.dev)**  
🌍 **[Website](https://eknath.dev)**   
💫 **[LinkedIn-Post for comments and feedbacks](https://www.linkedin.com/posts/eganathan_offlinefirstandroid-offlinefirst-android-activity-7294912159627546624-TG77?utm_source=share&utm_medium=member_desktop&rcm=ACoAABYcOpgBgvDfy-0uUjfX0HTNqzzLfKZQAQU)** 

🔖 [Previous Article in this Series](https://md.eknath.dev/posts/upgrading-your-app-to-offline-first-with-room-part-4/)
🚀 **Stay tuned for Part 6!** 🚀 

🔖 [Next Article in this Series](https://md.eknath.dev/posts/upgrading-your-app-to-offline-first-with-room-part-5/)