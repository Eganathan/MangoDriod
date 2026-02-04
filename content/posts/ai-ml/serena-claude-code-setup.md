---
date: '2026-02-04T10:00:00+05:30'
title: 'Supercharging Claude Code with Serena - Save 70% on Tokens'
categories: ["AI/ML", "AI-Tools"]
tags: ["AI", "Claude", "Tools", "MCP", "Developer-Productivity"]
---

## A Quick Note

This is a continuation of my [Claude Code notes](https://md.eknath.dev/posts/ai-ml/claude-code-notes/). If you haven't read that yet, I recommend starting there for the fundamentals. This article focuses on a specific optimization that has dramatically improved my Claude Code experience.

---

## The Problem: Token Costs Add Up Fast

If you've been using Claude Code for a while, you've probably noticed that **token costs can spiral quickly** - especially on large codebases. Here's why:

When you ask Claude something like *"Where is the authentication logic?"*, it often:
1. Reads entire files to understand context
2. Scans through multiple modules looking for patterns
3. Sometimes re-reads files it already looked at

For a medium-sized project (50k+ lines of code), a single exploration session can consume **thousands of tokens** just reading files. Multiply that across a day's work, and you're looking at serious costs.

Worse, when the context window fills up, Claude can start **hallucinating** - referencing functions that don't exist or suggesting patterns that don't match your codebase.

---

## Enter Serena: Semantic Code Navigation

**Serena** is an open-source MCP (Model Context Protocol) server that gives Claude Code **semantic understanding** of your codebase. Instead of reading entire files, Claude can now:

- **Jump directly to function definitions**
- **Find all usages of a class or method**
- **Navigate imports and dependencies**
- **Understand type hierarchies**

It does this by leveraging **LSP (Language Server Protocol)** - the same technology that powers your IDE's "Go to Definition" and "Find All References" features.

### The Results?

In my testing on a ~100k line Android/KMP project:

| Metric | Without Serena | With Serena |
|--------|---------------|-------------|
| Tokens for "Find auth logic" | ~15,000 | ~4,500 |
| Context preservation | Poor | Excellent |
| Navigation accuracy | File-based guessing | Semantic precision |
| Estimated cost savings | Baseline | **~70%** |

That 70% isn't marketing fluff - it's real savings from not reading entire files when you only need specific symbols.

---

## How Serena Works Under the Hood

If you've read my [MCP article](#), you know that MCP servers extend Claude's capabilities through a standardized protocol. Serena specifically provides:

1. **Code Indexing**: When you run `serena project create`, it builds an index of your codebase's symbols, types, and relationships.

2. **LSP Integration**: Serena wraps language servers (for Kotlin, TypeScript, Python, etc.) to provide semantic navigation.

3. **Smart Querying**: When Claude asks "Where is `UserRepository`?", Serena returns the exact file and line number - not a file dump.

4. **Live Updates**: The index updates as you modify code, staying in sync with your project.

```
┌─────────────────┐      MCP Protocol      ┌─────────────────┐
│   Claude Code   │ ◄──────────────────────► │     Serena      │
│    (Client)     │                          │   (MCP Server)  │
└─────────────────┘                          └────────┬────────┘
                                                      │
                                                      │ LSP
                                                      ▼
                                             ┌─────────────────┐
                                             │  Language Server │
                                             │  (kotlin-ls,    │
                                             │   tsserver, etc) │
                                             └─────────────────┘
```

---

## One-Time Setup

### Prerequisites

- Claude Code CLI installed ([see my setup guide](https://md.eknath.dev/posts/ai-ml/claude-code-notes/))
- A supported project (Kotlin, TypeScript, Python, Go, Rust, and more)

### Step 1: Install `uv` Package Manager

Serena uses `uv` for installation. If you don't have it:

```bash
# macOS/Linux
curl -LsSf https://astral.sh/uv/install.sh | sh

# Reload your shell
source ~/.zshrc  # or ~/.bashrc
```

Why `uv`? It's a fast Python package manager that handles Serena's dependencies cleanly.

### Step 2: Install Serena Tools

Install the CLI tools globally:

```bash
uv tool install git+https://github.com/oraios/serena
```

This gives you two commands:
- `serena` - Project management CLI
- `serena-mcp-server` - The MCP server that Claude connects to

### Step 3: Initialize Your Project Index

Navigate to your project root and create the index:

```bash
cd /path/to/your/project

# Create the Serena index
serena project create --name your-project-name --index .
```

**What this does:**
- Creates a `.serena/` folder in your project
- Scans your codebase for symbols, types, and relationships
- Builds a searchable index for Claude to query

**Initial indexing time** depends on project size:
| Project Size | Approximate Time |
|-------------|------------------|
| Small (< 10k lines) | 10-30 seconds |
| Medium (10k-50k lines) | 1-3 minutes |
| Large (50k-200k lines) | 3-10 minutes |
| Very Large (200k+ lines) | 10-20 minutes |

You can monitor progress at `http://localhost:24282` during indexing.

> **Important**: Add `.serena/` to your `.gitignore`. This folder is local cache and shouldn't be committed.

```bash
# Add to .gitignore
echo ".serena/" >> .gitignore
```

### Step 4: Restart Your Terminal

> **Important**: After installing `uv` and Serena, **close all terminal windows and open a fresh one**. This ensures your shell recognizes the new commands.

I spent time debugging "command not found" errors only to realize a terminal restart fixed everything. Save yourself the frustration.

```bash
# Close all terminals, then open a new one and verify
which serena
which serena-mcp-server
```

Both should return valid paths. If not, try running `source ~/.zshrc` (or `~/.bashrc`).

### Step 5: Connect Serena to Claude Code

Register Serena as an MCP server:

```bash
# Add the server (run from your project root)
claude mcp add serena -- serena-mcp-server --project $(pwd)
```

Verify it's connected:

```bash
# Check MCP server status
claude mcp list
```

You should see `serena` in the list with a green status.

---

## Handling Permission Prompts

When you start using Serena with Claude Code, you'll encounter **multiple permission prompts**. Claude asks for approval each time Serena wants to:
- Read files
- Navigate to definitions
- Search for symbols
- Access the index

This is good for security, but can get tedious during intensive coding sessions.

### Option 1: Approve Permissions Individually (Recommended for Learning)

When starting out, approve each permission manually. This helps you understand what Serena is doing and builds trust in the tool.

### Option 2: Auto-Accept Permissions for Serena

If you trust Serena and want a smoother experience, you can configure Claude to auto-accept its tool calls:

```bash
# Start Claude with auto-accept for the current session
claude --allowedTools "mcp__serena*"
```

This allows all Serena MCP tools without prompting, while still prompting for other potentially dangerous operations.

### Option 3: Dangerously Skip All Permissions (Use with Caution)

For experienced users who understand the risks:

```bash
# Skip ALL permission prompts (not just Serena)
claude --dangerously-skip-permissions
```

> **Warning**: This flag bypasses ALL safety prompts - file writes, shell commands, everything. Only use this if:
> - You're on a development machine (not production)
> - You understand Claude can modify/delete files without asking
> - You're working in a git-tracked project (easy to revert mistakes)
> - You trust your judgment to review changes before committing

For most users, Option 2 (`--allowedTools "mcp__serena*"`) is the sweet spot - smooth Serena experience while keeping other safeguards in place.

---

## Using Serena with Claude Code

### Starting a Session

```bash
# Navigate to your project
cd /path/to/your/project

# Start Claude with Serena connected
claude
```

### Onboarding Claude to Your Project

The first time you use Serena on a project, run this prompt:

```
Use Serena to onboard this project. Understand the architecture,
main modules, and key entry points.
```

Claude will use Serena's semantic capabilities to build a mental model of your codebase - without reading every file.

### Practical Examples

**Finding specific implementations:**
```
Where is the UserRepository interface implemented?
```

Without Serena: Claude reads multiple files guessing where implementations might be.
With Serena: Claude jumps directly to the concrete class.

**Understanding call hierarchies:**
```
What functions call the `syncUserData()` method?
```

Serena traces all callers semantically, giving Claude precise context.

**Navigating multi-module projects:**
```
How does the :feature:auth module communicate with :core:network?
```

Serena understands module boundaries and can trace cross-module dependencies.

---

## Monitoring and Debugging

### Live Dashboard

Serena provides a local web dashboard for monitoring and debugging:

```
http://localhost:24282
```

Open this URL in your browser while Serena is running. You'll see:

**Index Status Panel**
- Total symbols indexed (classes, functions, variables)
- Indexing progress percentage
- Last index update timestamp
- Any indexing errors or warnings

**Query Logs**
- Real-time log of Claude's queries to Serena
- Which symbols were requested
- Response times for each query
- Helps you understand what Claude is "thinking"

**Language Server Status**
- Connected language servers (kotlin-ls, tsserver, etc.)
- Server health and memory usage
- Restart buttons if a server becomes unresponsive

**Cache Statistics**
- Hit/miss ratios
- Memory usage
- Option to clear cache if things get stale

> **Tip**: Keep the dashboard open in a browser tab during intensive coding sessions. If Claude seems confused or slow, check the dashboard - you might spot a language server that crashed or an indexing error.

### Serena Tools Available to Claude

When connected, Claude gains access to these MCP tools (you can see these with `claude mcp list`):

| Tool | Purpose |
|------|---------|
| `serena_get_definition` | Jump to where a symbol is defined |
| `serena_get_references` | Find all usages of a symbol |
| `serena_get_symbols` | List all symbols in a file |
| `serena_search_symbols` | Search for symbols by name pattern |
| `serena_get_hover` | Get type info and documentation |
| `serena_get_diagnostics` | Get compiler errors/warnings |

Claude automatically chooses the right tool based on your question.

### Troubleshooting Common Issues

**"command not found: serena" after installation:**

This is the most common issue. Your terminal doesn't know about the new commands yet.

```bash
# Option 1: Reload shell config
source ~/.zshrc  # or ~/.bashrc

# Option 2 (recommended): Close ALL terminal windows and open a fresh one
# This ensures a clean shell environment
```

**"1 MCP server failed" error:**

```bash
# Remove and re-add the server
claude mcp remove serena
claude mcp add serena -- serena-mcp-server --project $(pwd)
```

**Index out of sync:**

```bash
# Rebuild the index
serena project update --name your-project-name
```

**Server not starting:**

Make sure you're in the correct project root where you ran `serena project create`.

**Language not supported:**

Check [Serena's supported languages](https://github.com/oraios/serena#supported-languages). For Android/KMP projects, Kotlin support works out of the box.

---

## Tip: Simplify with Aliases

These Serena commands are verbose. If you find yourself typing them often, consider setting up shell aliases or using a tool like [Aliasly](https://github.com/Eganathan/aliasly) to manage shortcuts across projects.

---



### 1. Keep Your Index Updated

After major refactors or pulling new changes:

```bash
serena project update --name your-project-name
```

### 2. Use Specific Queries

Instead of:
```
How does authentication work?
```

Try:
```
Show me the AuthViewModel and its dependencies using Serena.
```

The more specific your query, the better Serena can target the exact symbols.

### 3. Combine with CLAUDE.md

Your `CLAUDE.md` file complements Serena perfectly. Use CLAUDE.md for:
- Project conventions and coding standards
- Build commands and configuration
- Architecture overview

Use Serena for:
- Navigating actual code
- Finding implementations
- Tracing dependencies

### 4. Monitor Your Savings

Use `/cost` in Claude Code to track your token usage. Compare sessions before and after Serena to see the actual savings.

---

## Comparison: Claude Code vs. Claude Code + Serena

Here's a side-by-side breakdown of how Serena transforms Claude Code's capabilities:

| Feature | Claude Code (Standard) | Claude Code + Serena |
|---------|------------------------|---------------------|
| **Search Method** | Text-based / Full file reads | Symbolic / LSP-powered |
| **Code Retrieval** | Reads entire files | Extracts specific symbols/blocks |
| **Token Usage** | High (linear to file size) | Low (targeted retrieval) |
| **Memory** | Session-based | Persistent project indexing |
| **Navigation** | File path guessing | Precise symbol jumping |
| **Cross-references** | Manual grep patterns | Semantic "Find All References" |
| **Type Understanding** | Inferred from context | Actual type hierarchy |
| **Multi-module Support** | Reads each module separately | Understands module relationships |
| **Context Preservation** | Fills up quickly | Stays efficient longer |
| **Setup Required** | None | One-time indexing |

### Practical Scenario Comparison

| Scenario | Raw Reading | With Serena |
|----------|-------------|-------------|
| "Find function X" | Reads entire files, guesses locations | Direct jump to definition |
| "Who calls function Y?" | Manual grep through codebase | Semantic reference finding |
| "Show class hierarchy" | Reads all related files | Type hierarchy navigation |
| Large codebase exploration | Context window overflow | Targeted symbol queries |
| Token efficiency | Baseline | ~70% reduction |

---

## Supported Languages

Serena works with any language that has LSP support. Here's the current status:

| Language | Support Level | Language Server |
|----------|--------------|-----------------|
| **Kotlin** | Excellent | kotlin-language-server |
| **TypeScript/JavaScript** | Excellent | tsserver |
| **Python** | Excellent | pylsp / pyright |
| **Go** | Excellent | gopls |
| **Rust** | Excellent | rust-analyzer |
| **Java** | Good | eclipse.jdt.ls |
| **C/C++** | Good | clangd |
| **Swift** | Experimental | sourcekit-lsp |

For **Android/KMP projects**, Kotlin support is what matters most - and it works great.

> **Note**: Serena auto-detects your project's languages and starts the appropriate language servers. You don't need to configure this manually.

---

## Updating and Managing Serena

### Update Serena to Latest Version

```bash
uv tool upgrade serena
```

### Rebuild Project Index

After major refactors, dependency updates, or pulling large changes:

```bash
serena project update --name your-project-name
```

### Remove Serena from a Project

```bash
# Remove MCP server from Claude
claude mcp remove serena

# Delete the local index (optional)
rm -rf .serena/
```

### Working with Multiple Projects

Serena indexes are project-specific. To switch between projects:

```bash
# Project A
cd /path/to/project-a
claude mcp add serena -- serena-mcp-server --project $(pwd)

# Project B (in a different terminal/session)
cd /path/to/project-b
claude mcp add serena -- serena-mcp-server --project $(pwd)
```

Each project maintains its own `.serena/` index.

---

## When NOT to Use Serena

Serena isn't always the best choice:

- **Small scripts or single-file projects**: The overhead of indexing doesn't pay off
- **Heavily dynamic languages**: LSP works best with typed languages
- **Quick one-off questions**: Sometimes just asking Claude directly is faster
- **Non-code tasks**: Documentation, git operations, etc. don't benefit from Serena

Use judgment - Serena is a tool for **navigating complex codebases**, not a universal solution.

---

## Integration with My Workflow

Here's how Serena fits into my daily Claude Code usage:

1. **Morning context building**: "Use Serena to show me what I worked on yesterday in the :feature:dashboard module"

2. **Feature development**: "Using Serena, find all places where we handle network errors and show me the patterns"

3. **Code review**: "Navigate to the UserService implementation and review it for potential issues"

4. **Debugging**: "Trace all callers of `processPayment()` and identify where the null check might be failing"

5. **Onboarding teammates**: "Use Serena to explain the data flow from API response to UI state"

---

## Cost Analysis

Let's break down the real savings. With Claude Sonnet at ~$3/1M input tokens:

| Session Type | Without Serena | With Serena | Savings |
|--------------|---------------|-------------|---------|
| Quick exploration | 10k tokens | 3k tokens | $0.02 |
| Feature implementation | 50k tokens | 15k tokens | $0.10 |
| Full-day coding | 200k tokens | 60k tokens | $0.42 |
| Monthly usage (20 days) | 4M tokens | 1.2M tokens | **$8.40** |

These are conservative estimates. For larger codebases or Opus usage, savings multiply significantly.

---

## Setup Checklist

Quick reference for new projects:

- [ ] Install `uv`: `curl -LsSf https://astral.sh/uv/install.sh | sh`
- [ ] Install Serena: `uv tool install git+https://github.com/oraios/serena`
- [ ] **Restart terminal** (close all windows, open fresh)
- [ ] Verify install: `which serena && which serena-mcp-server`
- [ ] Create index: `serena project create --name PROJECT_NAME --index .`
- [ ] Add to .gitignore: `echo ".serena/" >> .gitignore`
- [ ] Connect to Claude: `claude mcp add serena -- serena-mcp-server --project $(pwd)`
- [ ] Test connection: `claude mcp list`
- [ ] Start Claude: `claude` (or `claude --allowedTools "mcp__serena*"` to auto-accept Serena permissions)
- [ ] Onboard Claude: "Use Serena to onboard this project"

---

## Resources

- [Serena GitHub Repository](https://github.com/oraios/serena)
- [Model Context Protocol Documentation](https://modelcontextprotocol.io/)
- [My Claude Code Notes](https://md.eknath.dev/posts/ai-ml/claude-code-notes/)
- [LSP Specification](https://microsoft.github.io/language-server-protocol/)

---

## Final Thoughts

Serena has become an essential part of my Claude Code setup. The token savings are nice, but the real value is **better context preservation**. Claude makes fewer mistakes when it has precise semantic information instead of guessing from partial file reads.

If you're working on any non-trivial codebase - especially multi-module Android/KMP projects - give Serena a try. The 10-minute setup pays for itself within the first session.

As always, remember: **AI is a copilot, not a pilot**. Serena makes the copilot more efficient, but you're still in control.

---

*This article is a living document. Last updated: February 2026*

---

## Glossary

New to some of these terms? Here's a quick reference:

### MCP (Model Context Protocol)

**Model Context Protocol** is an open standard created by Anthropic that allows AI assistants (like Claude) to connect to external tools and data sources. Think of it as a "USB port" for AI - any tool that implements MCP can plug into Claude and extend its capabilities.

**Example**: Serena is an MCP server. When you run `claude mcp add serena`, you're telling Claude "hey, there's a new tool you can use."

[Learn more](https://modelcontextprotocol.io/)

---

### LSP (Language Server Protocol)

**Language Server Protocol** is a standard created by Microsoft that powers IDE features like:
- "Go to Definition" (Ctrl/Cmd + Click)
- "Find All References"
- Auto-completion
- Syntax errors and warnings

Instead of each IDE implementing these features separately for every language, LSP provides a common interface. Your IDE talks to a "language server" that understands the specific language.

**Example**: When you Ctrl+Click a function in VS Code and it jumps to the definition - that's LSP in action. Serena uses this same technology to give Claude semantic code navigation.

[Learn more](https://microsoft.github.io/language-server-protocol/)

---

### uv

**uv** is a fast Python package and project manager created by [Astral](https://astral.sh/). It's like npm for Python, but significantly faster (written in Rust).

**Why Serena uses it**: Serena is a Python project. `uv tool install` installs CLI tools globally, similar to `npm install -g`.

**Key commands**:
```bash
# Install a tool globally
uv tool install package-name

# Install from git repository
uv tool install git+https://github.com/user/repo

# Update a tool
uv tool upgrade package-name
```

[Learn more](https://docs.astral.sh/uv/)

---

### Tokens

**Tokens** are the fundamental units that AI models process. Roughly:
- 1 token ≈ 4 characters in English
- 1 token ≈ 0.75 words
- 100 tokens ≈ 75 words

When you send a prompt to Claude, it counts tokens. When Claude responds, it generates tokens. Both cost money with the API.

**Why this matters**: If Claude reads a 1000-line file to answer a simple question, that's a lot of tokens wasted. Serena helps Claude read only what it needs.

---

### Context Window

The **context window** is the maximum amount of text (in tokens) that an AI model can "remember" during a conversation. Think of it as the AI's working memory.

| Model | Context Window |
|-------|---------------|
| Claude Sonnet | 200k tokens |
| Claude Sonnet 4.5 | 500k tokens |
| GPT-4 | 128k tokens |

**Why this matters**: When the context window fills up, older information gets "forgotten" or summarized. With large codebases, this can cause Claude to lose track of important details. Serena's efficient queries help preserve context.

---

### Semantic vs. Syntactic

- **Syntactic**: Understanding code as text/patterns (like grep searching for "function")
- **Semantic**: Understanding code's meaning and relationships (knowing that `UserRepository implements Repository<User>`)

Serena provides **semantic** navigation - it understands your code's structure, not just the text.

---

### Index / Indexing

When Serena "indexes" your project, it's building a searchable database of your code's structure:
- All classes, functions, and variables
- Their locations (file + line number)
- Their relationships (what calls what, what implements what)

This is similar to how search engines index websites - they pre-process content so searches are fast.

---

### CLI (Command Line Interface)

A **CLI** is a text-based interface for interacting with software. Instead of clicking buttons in a GUI, you type commands.

**Examples**:
- `git` - Version control CLI
- `npm` - Node.js package manager CLI
- `claude` - Claude Code's CLI

---

### MCP Server vs. Client

In the MCP architecture:
- **Client**: The AI assistant (Claude Code) that uses tools
- **Server**: The tool that provides capabilities (Serena, file system access, etc.)

When you run `claude mcp add serena`, you're registering Serena as a server that Claude (the client) can connect to.

---

Questions or feedback? Reach out:
- [Email](mailto:mail@eknath.dev)
- [Website](https://eknath.dev)
