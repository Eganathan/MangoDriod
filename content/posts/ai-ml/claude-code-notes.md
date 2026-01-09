---
date: '2026-01-09T21:47:13+05:30'
title: 'Staying Relevant with Claude Code - A Self-Note for Android & KMP Developers'
categories: ["AI/ML","AI-Tools"]
tags: ["AI","ML","Claude","Tools","Android","KMP"]
---

## A Quick Disclaimer

This article is primarily a **self-note** that I keep updating as I learn more about Claude Code. The AI tooling landscape evolves rapidly, so some information might be outdated by the time you read this. If you find something that needs updating, feel free to reach out!

Whether you're a **junior developer** just getting started or a **senior developer** looking to boost your workflow, Claude Code has something for everyone.

---

## Why Should You Care?

If you've read my [Solutionist Mindset talk](https://md.eknath.dev/posts/software-development/devfest2025-solutionist-mindset-talk/), you know I believe in **using AI as a copilot, not a pilot**. Claude Code embodies this philosophy perfectly—it's a CLI tool that sits alongside your existing workflow, helping you move faster while keeping you in control.

For Android and **Compose Multiplatform (KMP)** developers like us, having a tool that understands our codebase context is game-changing. Gradle configurations, multi-module architectures, platform-specific implementations—Claude Code can navigate all of this.

---

## What is Claude Code?

Claude Code is Anthropic's **official CLI tool** that brings Claude directly into your terminal. Unlike the web interface, it:

- **Has full access to your codebase** (with your permission)
- **Can read, write, and edit files** directly
- **Runs shell commands** for you
- **Understands project context** across multiple files
- **Integrates with Git** for version control operations

Think of it as having a senior developer sitting next to you who can:
- Explore your codebase instantly
- Write and refactor code
- Debug issues by reading logs and stack traces
- Create commits and PRs
- Explain complex code sections

---

## Latest Updates (January 2026)

**Update available for Claude Code users (v: 2.1.2)!**

### Model Selection

Opus 4.5 is now available in model selection. While **Sonnet is superior for general coding tasks**, **Opus is amazing for complex features and crazy bugs**. You can use `-m` flag for selecting a specific model for particular task sessions.

| Model ID | Description | Context Window | Relative Cost |
|----------|-------------|----------------|---------------|
| `claude-sonnet-4-20250514` | Sonnet 4 (default, most balanced) | 200K | $$ (Moderate) |
| `claude-opus-4-20250514` | Opus 4 (most capable, slower) | 200K | $$$$ (Very High) |
| `claude-sonnet-4-5-20250929` | Sonnet 4.5 (smartest, efficient) | 500K | $$$ (High) |
| `claude-haiku-4-5-20251001` | Haiku 4.5 (fastest, most economical) | 200K | $ (Low) |

> [!WARNING]
> **Token Usage Warning**: Continuous usage of **Opus** models will consume your rate limits and quota significantly faster (approx. 5-10x) than Sonnet. Use Opus only for complex debugging or architectural tasks.

```bash
# Run with a specific model
claude -m claude-opus-4-20250514
```

### Official Plugins

Check out the official plugins:
- [All Plugins](https://github.com/anthropics/claude-code/tree/main/plugins)
- [Code Review Plugin](https://github.com/anthropics/claude-code/tree/main/plugins/code-review)

---

## Getting Started

### Installation

```bash
# Using npm
npm install -g @anthropic-ai/claude-code

# Using Homebrew (macOS)
brew install claude-code
```

After installation, run `claude` in your terminal to start an interactive session. You'll need to authenticate with your Anthropic API key or use the `claude --login` command to login via the browser.

### Basic Usage

Navigate to your project directory and simply run:

```bash
claude
```

This starts an interactive session where you can ask questions, request code changes, or explore your codebase.

---

## Essential Commands Every Developer Should Know

### 1️⃣ Slash Commands

Claude Code has built-in slash commands that trigger specific workflows:

| Command | What It Does |
|---------|-------------|
| `/help` | Shows available commands and usage tips |
| `/clear` | Clears conversation history (starts fresh) |
| `/compact` | Compresses the conversation to save context |
| `/cost` | Shows token usage and estimated costs |
| `/doctor` | Diagnoses installation and configuration issues |
| `/init` | Creates a CLAUDE.md file with project context |
| `/review` | Triggers code review for recent changes |
| `/commit` | Creates a git commit with meaningful message |

### 2️⃣ The CLAUDE.md File

One of the most powerful features for **multi-module Android/KMP projects** is the `CLAUDE.md` file. Create this at your project root:

```markdown
# Project: MyKMPApp

## Architecture
- Multi-module KMP project
- Shared module: commonMain, androidMain, iosMain
- Android app module with Jetpack Compose UI
- iOS app using SwiftUI

## Key Conventions
- Use Koin for dependency injection
- Room for local database (Android), SQLDelight for shared
- Ktor for networking
- Kotlin Coroutines + Flow for async operations

## Build Commands
- `./gradlew assembleDebug` - Build Android debug
- `./gradlew :shared:build` - Build shared module only
- `./gradlew connectedAndroidTest` - Run instrumented tests

## Module Structure
- :app - Android application entry point
- :shared - KMP shared code
- :feature:home - Home feature module
- :feature:settings - Settings feature module
- :core:network - Networking utilities
- :core:database - Database layer
```

Claude reads this file and uses it as **persistent context** for every conversation. This is incredibly useful for:
- **Multi-module navigation** - Claude knows your module structure
- **Consistent coding patterns** - Follows your conventions
- **Faster builds** - Knows the right Gradle commands

### 3️⃣ Vim-Style Keybindings

For terminal enthusiasts, Claude Code supports vim keybindings:

| Key | Action |
|-----|--------|
| `Escape` | Enter command mode |
| `i` | Return to insert mode |
| `Ctrl+C` | Cancel current operation |
| `Ctrl+D` | Exit Claude Code |

---

## Practical Use Cases for Android/KMP Developers

### Use Case 1: Exploring Unfamiliar Codebases

When you join a new project or inherit legacy code:

```
You: How is the authentication flow implemented in this app?
     Show me the key files involved.
```

Claude will search through your codebase, identify relevant files (ViewModels, Repositories, API services), and explain the flow.

### Use Case 2: Writing Compose UI Components

```
You: Create a bottom sheet component for filtering products.
     It should have checkboxes for categories and a price range slider.
     Follow our existing design system in :core:designsystem module.
```

Claude will:
1. Look at your existing design system
2. Match the patterns and naming conventions
3. Create the component following your architecture

### Use Case 3: Debugging Build Issues

```
You: I'm getting this Gradle error when building the shared module:
     [paste error here]

     Help me understand and fix it.
```

Claude can read your `build.gradle.kts` files, understand the dependency graph, and suggest fixes.

### Use Case 4: Writing Platform-Specific Implementations

```
You: I need to implement biometric authentication.
     Create the expect/actual declarations for Android and iOS
     in the :core:auth module.
```

Claude understands KMP's expect/actual mechanism and generates appropriate platform-specific code.

### Use Case 5: Creating Git Commits

```
You: /commit
```

Claude will:
1. Analyze your staged changes
2. Understand the context of modifications
3. Generate a meaningful commit message
4. Create the commit

### Use Case 6: Room Database Migrations

```
You: I need to add a 'lastSyncedAt' column to the UserEntity.
     Create the migration and update the entity.
```

Claude handles the boilerplate of Room migrations, which can be error-prone manually.

---

## Best Practices for Effective Usage

### ✅ DO

1. **Be specific with context** - Instead of "fix this bug", say "fix the crash in `UserRepository.kt` when the token expires" make sure you add the file and line-number of the function or scope.

2. **Review generated code** - Always understand what Claude writes. Don't blindly accept suggestions.

3. **Use it for exploration** - Ask Claude to explain complex parts of your codebase or third-party libraries

4. **Leverage for boilerplate** - Let Claude handle repetitive tasks like:
   - Creating data classes from API responses
   - Writing Room entities and DAOs
   - Setting up Hilt/Koin modules
   - Creating navigation graphs
   - Writing unit test boilerplate

5. **Maintain your CLAUDE.md** - Keep it updated as your project evolves

6. **Use the right model for the task** - Haiku for quick questions, Sonnet for general coding, Opus for complex debugging

### ❌ DON'T

1. **Don't share sensitive data** - Avoid passing API keys, secrets, or user data through Claude

2. **Don't skip the review** - Especially for security-critical code (authentication, payment processing, encryption etc)

3. **Don't use it as a crutch** - You should still understand the fundamentals. AI is a multiplier, not a replacement.

4. **Don't expect perfection** - Claude can make mistakes. Treat its output as a starting point.

5. **Don't ignore Gradle sync** - After Claude modifies `build.gradle.kts`, sync manually in Android Studio

---

## Cost Management Tips

Claude Code uses API tokens, which cost money. Here's how to optimize:

### 1️⃣ Choose the Right Model

| Task Type | Recommended Model |
|-----------|-------------------|
| Quick questions, simple edits | Haiku 4.5 |
| General development | Sonnet 4/4.5 |
| Complex debugging, architecture | Opus 4/4.5 |

### 2️⃣ Use `/compact` Regularly

Long conversations consume more tokens. Use `/compact` to summarize and reduce context.

### 3️⃣ Start Fresh for New Tasks

Use `/clear` when switching to unrelated tasks. No need to carry previous context.

### 4️⃣ Be Concise

Instead of:
```
"Hey Claude, I was wondering if you could maybe help me
understand how the user authentication works in this app,
like when someone logs in, what happens step by step?"
```

Try:
```
"Explain the login flow. Start from LoginViewModel."
```

### 6️⃣ Offload Tasks to Other Models/Tools (Save those Tokens!)

Not everything requires Claude Code's deep context awareness. Save your tokens by routing tasks to the right tool:

*   **Use Gemini for Quick Concepts**: Need to understand "How `LruCache` works internally" or "Explain the Builder pattern"? Use **Gemini**. It's fast, free/cheap, and great for general knowledge that doesn't need your private codebase context.
*   **Use ChatGPT for High-Level Project Questions**: If you need advice on "Best practices for modularizing a KMP project" or architecture discussions where providing full code access isn't necessary, **ChatGPT** is a great option.
*   **Use CLI Tools for Quick Answers**: If you're a terminal power user (using `tmux`, `dia`, etc.), tools like **ddgr** (DuckDuckGo from terminal) or **Ollama** (local models) are fantastic for quick lookups without leaving your flow.

> [!TIP]
> **Pro Tip**: Reserve Claude Code for tasks that *specifically* need to read your files, understand your project structure, or perform edits. For everything else, cheaper (or free) alternatives often work just as well!

### 7️⃣ Check Costs with `/cost`

Regularly run `/cost` to monitor your usage.

---

## Integration with Development Workflow

### IDE Integration

Claude Code works alongside your IDE, not inside it. A typical workflow:

1. **Have your IDE open** (Android Studio / Fleet / IntelliJ)
2. **Run Claude in a terminal** (split screen works great)
3. **Ask Claude to make changes**
4. **Review changes in IDE** (they appear instantly)
5. **Test and iterate**

### Git Workflow Integration

Claude Code integrates nicely with Git:

```bash
# Start a session
claude

# Create meaningful commits
You: /commit

# Create a pull request
You: Create a PR for these changes. The target branch is develop.

# Review code before pushing
You: Review the changes in the last commit for any issues.
```

---

## Common Gotchas for Android/KMP Projects

### 1️⃣ Gradle Sync After Changes

When Claude modifies `build.gradle.kts` files, you'll need to sync in Android Studio manually. Claude can't trigger this for you.

### 2️⃣ Resource Files

Claude can create/modify XML resources (layouts, strings, drawables), but be careful with:
- **Generated resources** (R class) - These regenerate on build
- **Vector drawables** - Complex paths might need manual tweaking

### 3️⃣ Compose Preview

Claude-generated Compose components might need `@Preview` annotations added for visibility in Android Studio's preview pane.

### 4️⃣ iOS-Specific Code

For KMP projects, Claude can write Swift/Objective-C code for iOS implementations, but:
- You'll need Xcode to verify it compiles
- Swift interop with Kotlin can be tricky

### 5️⃣ Version Catalog

If you use `libs.versions.toml`, make sure Claude knows about it in your `CLAUDE.md`. Otherwise, it might use hardcoded versions.

---

## My Personal Workflow

Here's how I typically use Claude Code for Android development:

1. **Morning exploration** - "What did I work on yesterday? Show me recent changes."

2. **Feature development** - Start with asking Claude to explore existing patterns, then implement following those patterns

3. **Code review helper** - "Review this ViewModel for potential memory leaks or coroutine issues"

4. **Documentation** - "Generate KDoc comments for the public methods in NetworkClient.kt"

5. **Refactoring** - "Migrate this callback-based API to use Kotlin Coroutines with Flow"

6. **Test writing** - "Write unit tests for UserRepository using MockK"

---

## Advanced: MCP Servers

Claude Code supports **Model Context Protocol (MCP)** servers, which extend its capabilities. For Android developers, interesting MCPs include:

- **File system access** - Already built-in
- **Git operations** - Built-in
- **Web search** - For documentation lookups
- **Custom tools** - You can create your own MCP servers

Check out the [MCP Documentation](https://modelcontextprotocol.io/) for more details.

---

## Useful One-Liners

Quick commands I use frequently:

```bash
# Start with a specific model for complex tasks
claude -m claude-opus-4-20250514

# Resume last conversation
claude --resume

# Check installation health
claude /doctor

# Quick code review
claude "Review my staged changes for issues"
```

---

## What's Next?

This article covers the fundamentals, but Claude Code is constantly evolving. I plan to update this note as I discover:
- New features and capabilities
- Better workflows for KMP development
- Integration patterns with CI/CD
- Team collaboration strategies

---

## Final Thoughts

Claude Code is a **powerful addition to the Android/KMP developer toolkit**. It's not about replacing your skills—it's about **amplifying** them. Use it to handle boilerplate, explore unfamiliar code, and move faster on repetitive tasks.

But remember: **You are still the pilot**. Claude is your copilot. Understand what it generates, review its suggestions, and keep learning the fundamentals.

The developers who thrive in the AI age won't be those who code the fastest—they'll be the ones who **solve problems thoughtfully** while leveraging every tool at their disposal.

---

## Resources

- [Official Claude Code Documentation](https://docs.anthropic.com/claude-code)
- [Claude Code GitHub](https://github.com/anthropics/claude-code)
- [Official Plugins](https://github.com/anthropics/claude-code/tree/main/plugins)
- [Model Context Protocol](https://modelcontextprotocol.io/)
- [My Solutionist Mindset Talk](https://md.eknath.dev/posts/software-development/devfest2025-solutionist-mindset-talk/)

---

Feel free to connect with me on:
📩 **[Email](mailto:mail@eknath.dev)**
🌍 **[Website](https://eknath.dev)**

*I wish to keep this article as a living document. Last updated: January 2026*
