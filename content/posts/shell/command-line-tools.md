---
date: '2025-06-17T22:46:54+05:30' 
draft: false
title: 'Recommended Command Line Tools'
categories: ["Bash","Terminal"]
---
The terminal is already a powerful tool, but the right command-line utilities can make it even better. Here are a few essential tools I use daily that you might find helpful too.

## HomeBrew

Homebrew is a package manager for macOS (and Linux) that lets you easily install, update, and manage software and developer tools from the command line.

```bash
# Installation command
/bin/bash -c "$(curl -fsSL https://raw.githubusercontent.com/Homebrew/install/HEAD/install.sh)"
```

After running the command, restart your terminal, and you're good to go. Before we start installing, let's understand the difference between a "formula" and a "cask" in Homebrew.

**Formula:** Command-line tools, libraries, and languages (e.g., Kotlin, Go). No special flags are needed when using `brew` commands with formulas. [All Formulas](https://formulae.brew.sh/formula/)

**Cask:** GUI applications like Chrome, VSCode, etc. These require a `--cask` flag for `brew` operations. [Cask Directory](https://formulae.brew.sh/cask/)

```bash
brew install git             # Installing a formula
brew install --cask firefox  # Installing a cask

brew uninstall foo           # Remove a package
brew upgrade foo             # Upgrade a specific package
brew list                    # See all installed packages
brew search foo              # Find available packages
brew info foo                # Get details about a package
brew update                  # Update Homebrew's package list
brew upgrade                 # Upgrade all outdated packages
```

🔗 [HomeBrew-Official](https://brew.sh/)

## Ollama - Local and OpenSource LLMs

This is an incredibly useful tool that I find myself using constantly. Local models are fantastic for answering general or timeless questions where you need accuracy without requiring up-to-the-minute data. They’re fast, private, work offline, and have another big advantage: 🌱 a reduced environmental impact.

**Instructions:**

1.  Install Ollama by running the official script in your terminal. If you prefer, you can also download it manually from the [official site](https://ollama.com/download).
    ```bash
    curl -fsSL https://ollama.com/install.sh | sh
    ```
2.  Browse the [Model Library](https://ollama.com/search) to find a model. Keep an eye on the size, as some models can be several gigabytes.
3.  Once you've picked a model, pull it using the `pull` command. For example, to get the Llama 3 model:
    ```bash
    ollama pull llama3
    ```
4.  After the download is complete, you can run the model to start a chat session. To exit, just type `/bye`.
    ```bash
    ollama run llama3
    ```

That's it! Now, anytime you have a question, you can just run `ollama run <model_name>` to interact with your local LLM.

| Command                 | Description                                                               |
| ----------------------- | ------------------------------------------------------------------------- |
| `ollama serve`          | Starts the Ollama server (for API access).                                |
| `ollama create <model>` | Creates a new model from a Modelfile.                                     |
| `ollama show <model>`   | Displays details about a model.                                           |
| `ollama run <model>`    | Runs a model for interactive chat.                                        |
| `ollama pull <model>`   | Downloads a model from the library.                                       |
| `ollama list`           | Lists all downloaded models.                                              |
| `ollama ps`             | Shows currently running models.                                           |
| `ollama stop <model>`   | Stops a running model.                                                    |
| `ollama rm <model>`     | Removes a model from your system.                                         |

Here is an example of how you can download and run another model in one line:

```bash
ollama pull mistral && ollama run mistral
```

🔗 [Ollama](https://ollama.com/)

## Gemini-cli

Gemini CLI is an open-source tool that brings the power of Google's Gemini models directly into your terminal. It provides lightweight, direct access to the API, making it a versatile utility for a wide range of tasks, from coding and content generation to problem-solving and research.

### Installation

1.  Ensure you have Node.js (version 18+). You can check with `node -v`. If you don't have it, install it with Homebrew:
    ```bash
    brew install node
    ```
2.  Install the Gemini CLI globally using npm:
    ```bash
    npm install -g @google/gemini-cli
    ```
3.  Run the setup and authentication command:
    ```bash
    gemini
    ```
    Follow the prompts to choose a theme and log in with your Google account.

**Troubleshooting Tip:** On some systems, the authentication flow in the terminal might not complete. If this happens, run `gemini` again, and then check your default web browser for the Google authentication page to complete the login.

⚠️ Unlike Ollama, only the *tool* is open-source, not the model. Your prompts and data will be processed by Google's servers.

⚠️ The free tier has a rate limit (e.g., 60 requests per minute). You can upgrade to a paid plan to overcome this.

### Common Commands

-   `/chat save <name>`: Saves your current chat with a memorable name.
-   `/chat list`: Lists all your saved chats.
-   `/chat resume <name>`: Resumes a saved chat session.
-   `/compress`: Replaces the current chat context with a summary to save tokens.
-   `/auth`: Manages your authentication settings.
-   `/quit` or `/exit`: Exits the tool.

### Switching to Shell Mode

You can input `!` to toggle shell mode. For example, type `!pwd` to see your current directory. The theme will change to indicate you're in shell mode. To return to the chat, just input `!` again.

### Providing Context

Use the `@` symbol to provide file or directory context for your prompts.
-   `@path/to/your/file.txt Explain this text file.`
-   `@src/my_project/ Summarize the code in this directory.`

You can find more commands in the [official documentation](https://github.com/google-gemini/gemini-cli/blob/main/docs/cli/commands.md).


[Gemini CLI-Github repo](https://github.com/google-gemini/gemini-cli?tab=readme-ov-file)

## DuckDuckGo

Sometimes you just need to verify things quickly with a search engine. `ddgr` brings the DuckDuckGo search engine to your CLI, delivering fast results.

```bash
# Installation
brew install ddgr
```

### Common Commands

These are the commands you'll likely use most often:

| Command                    | Description                                           |
| -------------------------- | ----------------------------------------------------- |
| `ddgr <query>`             | Perform a search.                                     |
| `ddgr -n <num> <query>`    | Limit the number of search results.                   |
| `ddgr -j <query>`          | Open the first result directly in the browser.        |
| `ddgr -w <site> <query>`   | Restrict the search to a specific site.               |
| `ddgr -s <region> <query>` | Set the search region (e.g., `us-en`).                |
| `ddgr -x <query>`          | Display URLs only, without opening a browser.         |
| `ddgr -C <query>`          | Colorize the output for easier reading.               |
| `ddgr -l`                  | List your search history.                             |
| `ddgr -c`                  | Clear your search history.                            |
| `ddgr --disable-safe`      | Disable safe search filtering.                        |
| `ddgr -h`                  | Show the help menu.                                   |

### navigation Commands

When results are displayed, you can use these keys to navigate:

| Shortcut / Action | What it does                                                  |
| ----------------- | ------------------------------------------------------------- |
| `[number]`        | Open the result with that number in your browser.             |
| `n` or `N`        | Show the next page of results.                                |
| `p` or `P`        | Show the previous page of results.                            |
| `o [numbers]`     | Open multiple results (e.g., `o 1 3 5`).                      |
| `q`               | Quit ddgr.                                                    |

Here’s an example I use extensively:

```bash
# Shows 5 results from GitHub for "awesome shell scripts"
ddgr -n 5 -w github.com "awesome shell scripts"
```

### Profile Configuration

You can customize `ddgr`'s default behavior by editing the `~/.ddgrrc` file (`vi ~/.ddgrrc`). Here are some of the options you can configure:

| Option            | Description                                           |
| ----------------- | ----------------------------------------------------- |
| `-n <number>`     | Set the default number of search results per page.    |
| `-C`              | Enable colorized output.                              |
| `--disable-safe`  | Disable safe search.                                  |
| `-x`              | Show URLs only by default.                            |
| `-r <browser>`    | Set the browser for opening results (e.g., `firefox`). |
| `-s <region>`     | Set the default search region (e.g., `us-en`).        |
| `-w <site>`       | Restrict searches to a specific site by default.      |
| `--json`          | Output results in JSON format (useful for scripting). |

🔗 [ddgr-Repo](https://github.com/jarun/ddgr)

## Git CLI

```bash
brew install git
```

I'm sure you're familiar with the basic git commands, but you can create powerful aliases to make your workflow faster. For example, you can run `git st` instead of `git status`.

1.  Find your global git config file by running `git config --list --show-origin`.
2.  Open that file (e.g., `vi ~/.gitconfig`) and add your aliases.

Here is an example `~/.gitconfig` file:

```ini
[credential]
    helper = store
[user]
    name = Eganathan R
    email = md-email@gmail.com
[filter "lfs"]
    smudge = git-lfs smudge -- %f
    process = git-lfs filter-process
    required = true
    clean = git-lfs clean -- %f
[init]
    defaultBranch = master
[http]
    proxy = http://127.0.0.1:xxxx
[alias]
    st = status
    co = checkout
    br = branch
    ci = commit
    lg = log --oneline --graph --decorate # Pretty and compact log view
```

## Podman

Podman is a powerful, daemonless container engine for developing, managing, and running OCI containers. It provides a command-line interface that is compatible with Docker, making it an excellent alternative for container management without requiring a central daemon.

### Installation

```bash
brew install podman
```

After installation, you may need to initialize a Podman machine, which is a lightweight virtual machine for running containers on macOS.

```bash
podman machine init
podman machine start
```

### Common Commands

Many Podman commands are identical to their Docker counterparts, so you can often use `podman` as a drop-in replacement for `docker`.

| Command                 | Description                                         |
| ----------------------- | --------------------------------------------------- |
| `podman pull <image>`   | Pull an image from a container registry.            |
| `podman push <image>`   | Push an image to a container registry.              |
| `podman build -t <tag> .`| Build an image from a Dockerfile.                  |
| `podman images`         | List all local images.                              |
| `podman run <image>`    | Run a command in a new container.                   |
| `podman ps`             | List all running containers.                        |
| `podman ps -a`          | List all containers (running and stopped).          |
| `podman stop <container>`| Stop one or more running containers.               |
| `podman rm <container>` | Remove one or more containers.                      |
| `podman rmi <image>`    | Remove one or more images.                          |
| `podman machine list`   | List available Podman virtual machines.             |
| `podman machine stop`   | Stop the Podman virtual machine.                    |

🔗 [Podman-Official](https://podman.io/)

I'm certain this will help you. There are many other interesting command-line tools out there (like `starship`, `tmux`), but I consider them more for customization.

Thanks for reading, and have a great day ☺️