---
date: '2025-02-28T08:36:06+05:30' 
draft: true
title: 'Making Sense of Deep Seek Open Source Week'
categories: ["Ai/ML"]
tags: ["AI","ML","DeepSeek","OpenSource"]
---
This is my attempt of understanding the DeepSeeks OpenSource week releasing exciting things for the AI/ML community, as we are part of this incredible 


## Flash MLA - Makes AI Responses Faster

FlashMLA(Mixed Low-rank Attention)is an efficient Mixed Low-rank Attention decoding kernel(*A specialized piece of software*) for Hopper GPUs which is optimized to handle texts of different lengths efficiently without wasting memory or slowing down. Whether it’s a short sentence or a long paragraph, it processes them swiftly.

Most Models used to allocate Fixed Memory Allocation, and when processing large sequence of data the it slows down the inference(*generate texts or making predictions*) due to higher memory and compute requirements and finally in-efficiency in storing KV(keyValue)Cache in a fixed way which causes fragmentation when the text length is long.

### Paged Key Value Cache
AI text generation in chats involves predicting the next word based on previous words, for this to happen swiftly each of the following operation need to happen in a sequence:

 `Fetching past words (or tokens) from memory` ➡️ `Processing them with mathematical operations`(matrix multiplications, attention mechanisms, etc.) ➡️ `Generating the next word` ➡️ `Repeating this process for each new word`.

To ensure this works as expected the tokens must be easily accessible, typically this is stored in a `Key-Value(KV)cache`, instead of using this,The Flash MLA incorporates the `Paged KV Cache` for enhancing the memory and processing speed.

Let's checkout an analogy to understand this further:

**❌ Without Paged KV Cache**

📝 Prompt:“Tell me about black holes.”    
🤖 The AI stores all the info in one big memory block.

📝 Next Prompt: “Now explain their effects on time.”    
🤖 The AI scans the entire memory block (even the parts it doesn’t need), slowing things down.

**✅ With Paged KV Cache**

📝 Prompt: “Tell me about black holes.”    
📂 The AI stores data in small pages (like folders).

📝 Next Prompt: “Now explain their effects on time.”    
📂 The AI quickly grabs just the “black hole” page without searching everything, making responses faster and more efficient.



