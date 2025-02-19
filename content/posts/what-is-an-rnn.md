---
date: '2025-02-19T19:47:13+05:30' 
draft: true
title: 'What is an RNN? An explanation for simpletons'
categories: ["Ai/ML"]
---

On the topics of AI/ML i keep hearing about the importance of transformers, so i dig a little deeper in learning the journey from `Traditional-Neural-networks` ➡ `Recurrent Neural Network (RNN)` ➡ `Attention Mechanism` to finally `Transformers`, the RNN  is significant milestone because the others were born out of `RNN`'s limitations, also it was around for quite a while before we knew the word GPT, it was used by google for most of their products before the `Transformer` advancement.

## What is a Recurrent Neural Network(RNN)?

Have you wondered how the keyboard's word suggestion works perfectly well while typing? the secret behind it was RNN's before the `transformers`, so technically:

An RNN or Recurrent Neural Network is a type of artificial neural network designed for sequential data processing. Unlike traditional feed-forward neural networks, RNNs have loops that allow information to persist, making them well-suited for tasks where  context and order matters.

**here are some more examples which might make it more easier to understand:**

👉 **Natural Language Processing (NLP)** (e.g., speech recognition, text generation, machine translation)
👉 **Time Series Prediction** (e.g., stock price forecasting, weather prediction)
👉 **Sequence Modeling** (e.g., handwriting recognition, music composition)

## Stages of its working

Lets take the previous example of word prediction: Predicting the next word as you type your sentence, there are three states like, `Input Processing Stage` where the model knows what you have already typed, `Hidden State Update (Memory Stage)` is what you are typing now and `Output Generation Stage` is what the model prediction stage where it tries to predict the next word, lets go a little deeper into these:

### 1️⃣ Input Processing Stage

**This is the very first stage where the data is collected**, You might have noticed the first time you used a social media the suggestions are really crappy but as you use it more and more the platform behaves as if it knows you,right? the reason is because they have more **data from you** which is a must for better prediction, hence this is the most crucial stage for the RNN's to work effectively and this continues as you consume the content more.

The data is collected continuously for better prediction, as you type more words into the keyboard this stage ensures the data is added to its memory for the next stage.

### 2️⃣ Hidden State Update (Memory Stage)

If we are to follow the same analogy form the previous stage about social media, This stage is where the model updates its **Hidden/Unknown State** (reality) by takeing the current media/reel that is consumed by the user and previous information from the memory, thanks to stage 1 now the model analyzes what to show next.

### 3️⃣ Output Generation Stage

This is the stage where the model decides and provides an output of what you most likely prefer to watch/consume next, or in the the typing analogy where is here the next work is provided as suggestion.

### 4️⃣ Backpropagation Through Time (BPTT) – Training Stage

At this stage, the model learns from past mistakes and improves its predictions over time. Think of it like a student reviewing mistakes in past exams to score better in the next one.

In the social media analogy, if you suddenly stop engaging with a certain type of content (e.g., you stop watching travel vlogs and start liking fitness videos), the model realizes its past predictions were wrong and adjusts itself to better match your new interests and in the keyboard analogy, if you frequently delete a suggested word and type something else, the model learns that its previous prediction was incorrect. Over time, it improves its word suggestions based on your actual typing patterns.

💡 How does it work?
1️⃣ The model compares its predictions to what actually happened.
2️⃣ If there’s an error, it adjusts its internal weights to improve future predictions.
3️⃣ This process happens over multiple iterations, constantly fine-tuning the model to become more accurate.
