---
date: '2025-02-19T19:47:13+05:30' 
draft: false
title: 'What is an RNN? An explanation for simpletons'
categories: ["Ai/ML"]
---

## Understanding the Evolution of AI Models

When diving into AI/ML, we constantly hear about **transformers** and their revolutionary impact. But how did we get here? The journey started from `Traditional Neural Networks` ➡ `Recurrent Neural Networks (RNNs)` ➡ `Attention Mechanisms` and finally to `Transformers`.  

RNNs were a **significant milestone** because they addressed sequential data processing but had major limitations. These limitations led to the birth of attention mechanisms and transformers. Interestingly, before **GPT** became a household name, **Google extensively used RNNs** in their products, including predictive text, speech recognition, and early recommendation systems.

## What is a Recurrent Neural Network (RNN)?

Have you ever wondered how your keyboard **predicts the next word** while typing? Before transformers took over, **RNNs were the secret behind word suggestions** and other sequential tasks.

### **Definition:**
An **RNN (Recurrent Neural Network)** is a type of artificial neural network designed specifically for **processing sequential data**. Unlike traditional feed-forward networks, RNNs have **loops that allow information to persist**, making them well-suited for tasks where **context and order matter**.

### **Common Use Cases of RNNs:**
👉 **Natural Language Processing (NLP)** (e.g., speech recognition, text generation, machine translation)  
👉 **Time Series Prediction** (e.g., stock price forecasting, weather prediction)  
👉 **Sequence Modeling** (e.g., handwriting recognition, music composition)  

## How Does an RNN Work?  

Let’s use the **word prediction** example to understand the key stages of an RNN. When you type a sentence, the RNN processes it in three key stages:  

### **1️⃣ Input Processing Stage**  

This is the **data collection stage**, where the model gathers input to make predictions.  

🔹 When you **first start using a social media app**, its recommendations may seem random or inaccurate. Over time, as you interact more, the app starts to understand your preferences. This happens because it continuously **collects data from you** to make better predictions.  

🔹 In the **keyboard analogy**, as you type more, the model **stores your words** in memory, helping it predict what you might type next.  

### **2️⃣ Hidden State Update (Memory Stage)**  

At this stage, the RNN **updates its hidden state** based on the new input and previous memory.  

🔹 In **social media**, the model remembers what you’ve previously engaged with and **adjusts recommendations** accordingly. If you keep watching **travel vlogs**, it will prioritize showing more similar content.  

🔹 In **keyboard predictions**, the model updates its memory with each word you type, continuously refining its **contextual understanding**.  

### **3️⃣ Output Generation Stage**  

Now, the model **makes a decision** and produces an output based on its learning.  

🔹 In **social media**, this means recommending the **next video or post** that best matches your interests.  
🔹 In **typing**, this means predicting and suggesting the **next word** in your sentence.  

### **4️⃣ Backpropagation Through Time (BPTT) – Training Stage**  

This is where the model **learns from past mistakes** and improves over time. Think of it like a **student reviewing mistakes from past exams** to perform better in the next test.  

🔹 In **social media**, if you suddenly stop engaging with travel vlogs and switch to fitness videos, the model realizes its past predictions were wrong and **adjusts itself** to reflect your new interests.  

🔹 In **keyboard predictions**, if you frequently **delete a suggested word and type something else**, the model **adapts** to improve its future suggestions.  

### **How Does BPTT Work?**  
1️⃣ The model **compares its predictions** to actual user behavior.  
2️⃣ If there’s an **error**, it **adjusts its internal weights** to improve accuracy.  
3️⃣ This process repeats across **multiple iterations**, constantly fine-tuning the model.  

This stage is **crucial** because it ensures that the model **evolves and adapts** based on real-world interactions.

---

## **Final Thoughts**  

RNNs played a critical role in AI’s evolution, **powering early NLP applications, recommendations, and predictive text systems**. However, due to **limitations like vanishing gradients and slow processing**, they were eventually replaced by **transformers** and **attention-based models**.  

Yet, understanding RNNs is essential because they paved the way for **modern AI breakthroughs**. Without RNNs, we wouldn’t have reached **the transformer era of GPT**! 🚀  

---
Your feedbacks are welcome, Thanks for Reading.