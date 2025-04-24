---
date: '2025-04-22T08:18:39+05:30'
draft: true
title: 'Mastering Raw Queries in Room: Why, When & When Not to Use Them (#OF06)'
tags: ["Room","Android","Offline-First-App"]
categories: ["Android","KMP"]
---

In the [previous article](https://md.eknath.dev/posts/upgrading-your-app-to-offline-first-with-room-part-5/), we explored the power and flexibility of DAOs with Room’s built-in query annotations. But what if your query needs don’t fit into Room’s constraints? Enter @RawQuery – the most flexible and dangerous tool in the Room arsenal.

Let’s dive into what `@RawQuery` is, when it shines and shuns.
---
## What is @RawQuery?

`@RawQuery` allows you to execute **SQL statements that aren’t validated at compile time**. Unlike `@Query`, which Room parses and validates during compilation, raw queries are evaluated at runtime.

You typically use `@RawQuery` with either SupportSQLiteQuery (for fully dynamic queries) or plain String (though the latter is limited and discouraged).

```kotlin
@Dao
interface ProductDao {

    @RawQuery 
    suspend fun getProductsWithRawQuery(query: SupportSQLiteQuery): List<Product>


    // This will be called from the repository
    @Transaction
    suspend fun getProductsAbovePrice(minPrice: Int): List<Product> {
    val query = SimpleSQLiteQuery(
        "SELECT * FROM products WHERE price > ?",
        arrayOf(minPrice)
    )
    return productDao.getProductsWithRawQuery(query)
    }
}
```

### ✅ When Should You Use @RawQuery?

Despite its risks, there are legitimate use cases for `@RawQuery` which come handy when the app is completely offline and need to do operations similar to server with available data for example sorting, filtering and searching.

There are some cases where you need advanced joins, unions, subqueries Room’s `@Query` might fall short an example i can think of are expense list screen where you need to get associated budgets,tags, users who created and approved them etc getting this merged data specific filter and sort type will be extremely hard with conventional methods in cases like these `@RawQuery` are a boon.

This is one of my dao's functions that is triggered when the there applies a filter, since there was no network i apply the filter and show the available data assuming the user already knows he is in offline mode,we have an indicator that should handle conveying of the message. So take a look and the params and tell me can we acheve this using conventional method faster than this ? i don't think so but do share your views.


Lets check out my code for 
```kotlin

 @RawQuery // Query runner
    suspend fun getExpensesWithParamsQueryRunner(query: SupportSQLiteQuery): List<LocalExpenseWithDetails>

 @Transaction // this will be called as a fallback option when offline
    suspend fun getExpensesWithParams(
        type: String?,
        budgetId: Long?,
        sessionId: Long?,
        filterParam: FilterParams,
        sortParam: SortParam,
        searchQuery: String?,
        page: Int
    ): List<LocalExpenseWithDetails> {
        val typeId = if (type != null && type != BaseExpenseType.ALL) getExpenseTypeWithName(type.serverKey) else null
        return getExpensesWithParamsQueryRunner(
            query = getExpenseQuery( // query generator
                typeId = typeId,
                budgetId = budgetId,
                sessionId = sessionId,
                filterParam = filterParam,
                sortParam = sortParam,
                search = searchQuery,
                page = page
            )
        )
    }

```
3. Performance Testing / Debugging
During development, you might want to test different raw SQL statements quickly without baking them into DAOs.

### ⚠️ When NOT to Use @RawQuery

Just because you can doesn’t mean you should. Raw queries come with trade-offs:

- ❌ No Compile-Time Safety

Room won’t validate your SQL. Typos, wrong column names, or invalid SQL will only fail at runtime – often with vague errors.

- ❌ No Type Inference

Unlike @Query, Room won’t know what result type to expect unless you specify it manually and correctly.

- ❌ Risk of SQL Injection
If you’re concatenating SQL strings, you open yourself to SQL injection vulnerabilities. Always use parameterized queries or filter the vulnerable queries.

```kotlin
// Bad ❌
val query = SimpleSQLiteQuery("SELECT * FROM products WHERE name = '$name'")

// Good ✅
val query = SimpleSQLiteQuery("SELECT * FROM products WHERE name = ?", arrayOf(name))
```

### 📋 Tips for Safely Using Raw Queries
- ✅ Always use SimpleSQLiteQuery with parameterized arguments.
- ✅ Keep the query logic isolated and well-documented.
- ✅ Prefer @Query whenever possible.
- ✅ Avoid user-generated input directly in SQL strings.
- ✅ Write tests to validate dynamic query paths.


### 🚫 Anti-Patterns to Avoid
- ❌ Using raw queries as your primary query method.
- ❌ Skipping query reuse – dynamic doesn’t mean you can’t structure it.
- ❌ Using @RawQuery when @Query or DAO methods would suffice.
- ❌ Ignoring test coverage for raw query logic.


## 🚀 Conclusion
`@RawQuery` is the escape hatch when Room’s abstraction becomes a cage. Use it when needed, but use it wisely. Think of it like the goto statement of Room – powerful but potentially dangerous if overused or misused.

In most offline-first app cases, well-structured DAOs using Room’s annotations will suffice. But in edge cases where flexibility is key, `@RawQuery` gives you that last-mile control.

**Next up, we’ll explore Query Optimization Tips to keep your Offline-First App lightning fast, even at scale.**

**Next we will explore Data Access Objects**, Stay tuned for the next article in this series! 🚀

## **Final Thoughts**  
Raw queries are sharp tools — excellent in skilled hands, but risky for the unprepared. If you’ve got a use case or edge case where @RawQuery saved your app or made something possible, I’d love to hear it!

Feel free to connect and share your stories:
📩 **[Email](mailto:mail@eknath.dev)**  
🌍 **[Website](https://eknath.dev)**   
💫 **[LinkedIn-Post for comments and feedbacks](https://www.linkedin.com/posts/eganathan_offlinefirstandroid-offlinefirst-android-activity-7294912159627546624-TG77?utm_source=share&utm_medium=member_desktop&rcm=ACoAABYcOpgBgvDfy-0uUjfX0HTNqzzLfKZQAQU)** 

🔖 [Previous Article in this Series](https://md.eknath.dev/posts/upgrading-your-app-to-offline-first-with-room-part-5/)
🚀 **Stay tuned for Part 7!** 🚀 

<!-- 🔖 [Next Article in this Series](https://md.eknath.dev/posts/upgrading-your-app-to-offline-first-with-room-part-7/) -->