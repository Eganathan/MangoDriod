---
date: '2026-03-07T21:47:13+05:30'
title: 'To or Not to Use AI Tools - A Self Reflection'
categories: ["AI/ML","Thoughts"]
tags: ["AI","reflections"]
---

This is more of a self-reflection than some AI-generated slop I wish to shove in your face. Less than 5% of my friend circle has enough patience to read an article, let alone debate the topic. I’m trying to spend more time around people who have clarity on these topics. Thankfully, at work I was blessed with a friend who shares and discusses these ideas. I mostly find myself defending the values and lessons shared in those articles (Thanks Aditya!). One such article is the catalyst for these thoughts.

Before we go further, I humbly request you to read this piece: ["You Don't Have To"](https://www.scottsmitelli.com/articles/you-dont-have-to/) by Scott Smitelli. Don't stop after the first few paragraphs—keep reading till the end for the twists and turns, then come back here.

Scott's article really makes you think about how we might slowly be losing our edge due to heavy reliance on Large Language Models (LLMs). It’s like how I stopped memorizing phone numbers because they’re stored in my phone book (except my own!), or how calculating large numbers in my head has become hard compared to a local shopkeeper doing it in seconds.

With AI, there are so many techniques I continuously experiment with. Using AI to brainstorm, validate, or debate your thoughts is great—but don't let it run the show. If you do, you'll slowly vanish into the background.

Reading that article—and later debating it with my manager—sent me down a rabbit hole of self-reflection. Is AI destroying the art of coding, or is it simply the next step in our evolution? Here are my honest reflections on where I stand today.

## The "Zero to One" Myth

There's a romanticized idea in our industry that we build things "from zero." The truth is, that hasn't been true for years. We went from machine code to assembly, to C, to Java and Kotlin. Today, 95% of developers rely heavily on layers of abstractions—frameworks, APIs, and libraries—that they didn't build and often don't fully understand under the hood.

AI isn't an alien invasion; it is merely the newest layer of abstraction in this ongoing shift.

At the same time, AI isn't a "magic button." Unless you are cloning a well-documented repository, AI cannot build a full-fledged, custom solution from start to finish with a single prompt. Real engineering still requires architecture, logic, and deep orchestration—all of which must come from a human.

## Value over "The Craft"

Many developers treat coding purely as an art form, priding themselves on writing perfect, zero-dependency code. But practically speaking, in a professional setting, we aren't here just to write poetry in code. We are here to solve problems, deliver value, and earn a living.

All I care about are the humans using the tools I build. The exact ingredients or purity of the code don't matter as much as the end-user's experience. Getting bogged down in purism feels counterproductive if it stands in the way of delivering a valuable product.

## The Danger of "AI Slop"

That being said, my manager raised a very valid point: the sheer ease of generating content with AI easily leads to garbage. Generative AI can produce 10x more content in a single day than humans have produced in a lifetime. When people publish content without personal input, refinement, or real intent, we get what he accurately called "AI slop."

I agree completely. Outputting anything publicly without personal meaning—just creating for the sake of output—pollutes human conversation. The tool is only as good as the intent behind it.

## The Axe and the Chainsaw

Think of AI as an electric chainsaw, and traditional coding as an axe. 

Knowing how to use an axe remains essential even when a chainsaw is available. The chainsaw can break or fail. More importantly, **a lumberjack who has cut down trees with an axe a thousand times knows exactly how to angle the cut so the tree falls right where he wants it to.**

Using AI tools doesn't turn your brain to mush—*provided* you actually understand the changes it makes. Let me be real: **this is extremely hard!** The dangerous thing about AI code isn't when it fails obviously with syntax errors; it's the **illusion of correctness**. AI code often formats nicely and compiles on the first try, while subtly hiding edge-case bugs, race conditions, or security oversights underneath.

That's why I'm actually thankful for Claude's token limitations sometimes—they force me to stay involved. AI shifts your role from pure execution to orchestration. You cannot outsource your **judgment**, **experience**, or **personality**. If you rely entirely on AI without applying these human traits, the quality of your work drops and you risk becoming redundant.

## The Trap of "Vibe Coding"

I'll admit it: I fell into the trap of "vibe coding" for a short period. I regret it because I lost the chance to learn what was actually happening in that block of code. 

I thought skipping that understanding was okay at the time, but reflecting on it opened my eyes. Blind vibe coding might be fine for prototyping quick personal hacks or silly productivity experiments, but doing it on real products or projects you truly care about is a big no-no.

## The Watermark Dilemma: A Forcing Function for Mastery

Like many of you, I feel perplexed by recent discussions around AI providers (like Anthropic) introducing watermarks on model-generated content. 

On a professional level, it can feel frustrating—almost like being flabbergasted. When the core thought, architecture, design, and final approval all originate from your mind, having a watermark stamped on your work forces you to ask: *Do I really want to carry a watermark on my creations?*

At the same time, I acknowledge the clear societal need for it. Watermarking is an essential guardrail against academic fraud in schools and the endless ocean of AI slop flooding social media. 

Ironically, I see this dilemma as a hidden boon. If carrying an AI watermark bothers you, it becomes a powerful forcing function. It pushes you to step up, master the codebase, understand the underlying architecture, and manually drive the development process. In a way, watermarking might be the exact boundary that forces us to keep our human edge sharp.

## An Equalizer for Communication

Beyond writing code, AI is an incredible equalizer for communication. Not everyone is a natural wordsmith. For those who are less vocal or struggle to find the right phrasing, AI helps communicate technical intent clearly. It's not about faking a voice; it's about polishing it. 

That said, getting it to match what's in your head isn't easy. Due to model limitations, AI often summarizes too quickly or gets overly verbose, rarely landing on the exact right proportion without iteration.

## Wielding the Future

My philosophy in this rapidly changing landscape is simple:
- When we only had machine code, we coded in assembly.
- When we got high-level languages like Java and Kotlin, we used them.
- Now we have AI, and we should use it extensively.
- If AI becomes inaccessible or too expensive tomorrow, we go back to coding in Kotlin. We should be prepared for that.

To ensure I stay sharp, I've started **"AI fasting."** Spending three days coding completely without AI is a healthy practice that forces me to build and think independently. 

Recently, I saw a developer in an Instagram reel make a great point: *"Before AI, you delivered a project in a week. Now, even with AI, it still takes a week—why is that?"* His answer: while AI generates code quickly, reviewing it, tweaking it, and fixing its subtle bugs has become much harder.

The underlying reason comes down to **cognitive architecture**. When you write code manually from scratch, you build a mental 3D blueprint of the system in your head—you know every edge case because you built it line by line. When AI generates 300 lines of clean code in seconds, you get the output, but you miss out on building that mental map. When a bug strikes, you have to build that mental map from scratch under pressure.

Finding the right balance is key. Keeping AI away won't help; instead, I intend to embrace it tightly, understand its strengths and weaknesses, and use it to my advantage. 

Coding like a "caveman" shouldn't be a badge of honor. Utilizing tools like MCP (Model Context Protocol), plugins, and advanced prompting is how we stay effective in this new era. Machines should take the drudgery out of life—it's up to us to orchestrate them responsibly and add real value rather than adding to the noise.

---

### A Final Personal Note

Every single idea, experience, dilemma, and angle in this article came from my own human mind and real-world experiences. I used AI as an assistant to help translate my raw, unrefined sentences into clear, well-phrased prose. 

Writing isn't my strongest skill, but I'm learning as I go. Seeing my thoughts translated into clear writing gives me the voice and confidence to keep thinking, writing, and posting more reflections like this.
