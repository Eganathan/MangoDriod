---
date: '2025-06-17T22:46:54+05:30' 
draft: false
title: 'Recommended Command Line Tools'
categories: ["Bash","Terminal"]
---
Terminal is lit already but these are some must have commandline tools that i use and i think you must have too.

## HomeBrew

Homebrew is a package manager for macOS (and Linux) that lets you easily install, update, and manage software and developer tools from the command line.

```bash
# Installation command
/bin/bash -c "$(curl -fsSL https://raw.githubusercontent.com/Homebrew/install/HEAD/install.sh)"
```

After running the above command, just restart the terminal and you are good to go, before we start installing stuff lets understand what is formula and cask in brew context.

**Formula:**  They are Command-line tools, libraries, languages (Kotlin, Go etc) this does not need any decorators while handling any brew operations. [AllFormulas](https://formulae.brew.sh/formula/)

**Cask:** Casks are UI applications like chrome, vscode etc and need a `--cask decorator` for operations with it.[CaskDirectory](https://formulae.brew.sh/cask/)

```bash
brew install git             # installing  formula example
brew install --cask firefox  # installing cask example

brew uninstall foo           # remove it
brew upgrade foo             # upgrade it
brew list                    # see installed packages
brew search foo              # find packages
brew info foo                # details about a package
brew update                  # update Homebrew itself
brew upgrade                 # upgrade everything
```

🔗 [HomeBrew-Official](https://brew.sh/)

## Ollama - Local and OpenSource LLMs

This is an incredibly useful tool — I find myself using it almost every other hour.
Local models are fantastic for answering generic or timeless questions where accuracy matters and you don’t need up-to-the-minute data. They’re fast, private, work offline, and come with another big advantage: 🌱 reduced environmental impact.

**Instructions:**

1. run the following command to download via terminal ```bash curl -fsSL https://ollama.com/install.sh | sh``` or if you like to download manually [https://ollama.com/download)](https://ollama.com/download) and install it.
2. navigate to the downloaded folder and unzip the file, `unzip Ollama-darwin.zip`.
3. Now `ls` and you will see a new file called `Ollama.app`.
4. run the open command `open Ollama.app` and agree and allow everything it asks(don't worry its safe).
5. Browse a model form the [ModelLIbrary](https://ollama.com/search), keep an eye on the size some models are like 500 GB 🫢
6. Once you have picked you model then run `ollama run model_name` ie `ollama run deepseek-r1`
7. After the download is complete you can serve it `ollama serve deepseek-r1`.
8. You can interact with the model now, to exit just type `/bye` and you are out.

That was a long process i know, but now anytime you have a question you can just run `ollama run deepseek-r1` and you can interact without any hassle.

| Command                          | Description |
|-----------------------------------|-------------|
| `ollama serve`                   | Starts Ollama on your local system. |
| `ollama create <new_model>`       | Creates a new model from an existing one for customization or training. |
| `ollama show <model>`             | Displays details about a specific model, such as its configuration and release date. |
| `ollama run <model>`              | Runs the specified model, making it ready for interaction. |
| `ollama pull <model>`             | Downloads the specified model to your system. |
| `ollama list`                     | Lists all the downloaded models. |
| `ollama ps`                       | Shows the currently running models. |
| `ollama stop <model>`             | Stops the specified running model. |
| `ollama rm <model>`               | Removes the specified model from your system. |

Here is an example how you can download and run other models

```bash
ollama pull mistral && ollama run mistral
```

🔗 [Ollama](https://ollama.com/)

## Gemini-cli

Gemini CLI, an open-source AI agent (Only agent not the **modal**) that brings the power of Gemini directly into your terminal. It provides lightweight access to Gemini, giving you the most direct path from your prompt to our model. While it excels at coding, we built Gemini CLI to do so much more. It’s a versatile, local utility you can use for a wide range of tasks, from content generation and problem solving to deep research and task management.

### installation

Before you start there is a bug at login, so stick with me on setting this up.

- Ensure you have nodeJs by running `node -v` if your version is greater than `18` you are good to go otherwise upgrade it by running `brew upgrade node`
- in case you don't have node then just install it by running`brew install node@22`
- run `npm install -g @google/gemini-cli` (wait for this to complete)
- run `gemini`
- choose your theme
- pick the google login
- now on some devices the app stops abruptly so open your default browser
- you might see the auth login page
- now run the `gemini` command again and go to your default browser and authenticate on the latest tab.

⚠️ Unlike ollama her only the tool is open source, not the model which means your data will be passed around.
⚠️ 60 request/ min is the current limit, but you can upgrade to paid plan to avoid this.

### Common Commands

- `/chat save any_name_you_want` this saves your current chat into this tag
- `/chat list` lists all the saved chats
- `/chat resume saved_chat_tag_name` to resume the saved chat
- `/compress` replace the entire chat context with a summary. This saves on tokens used for future tasks while retaining a high level summary of what has happened.
- `/auth` if you want to change your auth
- `/quit` or `/exit` to exit from the tool

### switching to shell mode and back

You can input `!` to toggle to shell mode, ie in middle of the chat you want to see which directory you currently are just input `!pwd` the terminal will print the current dir and the theme will change to indicate you are in shell mode once you are done with shell commands just input `!` again and you can start using the gemini as normal mode.

### Providing context

`@<path_to_file_or_directory>` the `@` can you used to provide context to the inference ie `@path/to/your/file.txt Explain this text file.` or `@src/my_project/ Summarize` the code in this directory.

There are more commands and you can find theme here [All Commands of Gemini cli tool](https://github.com/google-gemini/gemini-cli/blob/main/docs/cli/commands.md)


[Gemini CLI-Github repo](https://github.com/google-gemini/gemini-cli?tab=readme-ov-file)

## DuckDuckGo

Search engine is not going away, some times you need to verify things quickly so here comes the DuckDuckGo search engine in cli, you just run `ddgr whats the latest news about ai` and you get a list faster than a bullet(Most of the time).

```bash
# Installation
brew install ddgr
```

### Common Commands

These are the commands you will mostly need

| Command                          | Description |
|-----------------------------------|-------------|
| `ddgr <query>`                   | Perform a search using DuckDuckGo. |
| `ddgr -n <number> <query>`        | Limit the number of search results. |
| `ddgr -j <query>`                 | Search and open the first result automatically in the browser. |
| `ddgr -w <site> <query>`          | Restrict the search to a specific site (site:). |
| `ddgr -s <region> <query>`        | Set region for search (e.g., `-s us-en`). |
| `ddgr -x <query>`                 | Search without opening a browser (display URLs only). |
| `ddgr -C <query>`                 | Colorize the output for easier reading. |
| `ddgr -l`                         | List search history. |
| `ddgr -c`                         | Clear search history. |
| `ddgr --disable-safe`             | Disable safe search filtering. |
| `ddgr -h`                         | Show help information. |

### navigation Commands

When the results are displayed interactively you can use this to navigate
| Shortcut / Action | What it does |
|------------------|--------------|
| `[number]`        | Open the result with that number in your browser. |
| `n` or `N`        | Show the next page of results. |
| `p` or `P`        | Show the previous page of results. |
| `o [number]`      | Open multiple results by space-separated numbers, e.g. `o 1 3 5`. |
| `q`               | Quit ddgr. |

There is so much you can do which you can explore but here is one that i use extensively:

```bash
ddgr -n 5 -w github.com "awesome shell scripts"
# Shows 5 results from GitHub for your query.
```

### Profile Configuration

You can also configure the behavior my modifying the `.ddgrrc` file, you can update it via terminal by running the `vi ~/.ddgrrc` command, here are the options you can configure:

| Option                  | Description |
|-------------------------|-------------|
| `-n <number>`            | Set the number of search results per page. |
| `-C`                     | Enable colorized output for better readability. |
| `--disable-safe`         | Disable safe search filtering. |
| `-x`                     | Show URLs only (do not open in browser). |
| `-r <browser>`           | Set the browser to use for opening results (e.g., `firefox`, `chromium`). |
| `-s <region>`            | Set the search region (e.g., `us-en`, `in-en`). |
| `-w <site>`              | Restrict search to a specific site (site search). |
| `--noua`                 | Disable sending a User-Agent in requests. |
| `--np`                   | Disable search suggestions (don't use POST requests). |
| `--no-completion`        | Disable interactive result selection (just print URLs). |
| `-k <keywords>`          | Set default search keywords (these will always be included in your searches). |
| `-j`                     | Automatically open the first result in your browser. |
| `--json`                 | Output results in JSON format (useful for scripts). |

🔗 [ddgr-Repo](https://github.com/jarun/ddgr)

## Git CLI

```bash
brew install git
```

Im sure you know the git commands so im skipping them, but the profile configuration is really cool so instead of `git status` you can just run `gs` command and here is how.

1. find where your system wide git profile is stored by running `git config --list --show-origin`
2. open that file in vim and and your aliases and other profiles and save for re-open the terminal.

Here is an example file at `~/.gitconfig`

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
        proxy = http://127.1.1.2:xxxx
[alias]
        st = status
        co = checkout
        br = branch
        ci = commit
        lg = log --oneline --graph --decorate
```

I am certain this helps you, There are many such commandline tools that are really intreating but i think of them as a decorators so i have not added them but check out starship, podman cli, tmux and many others.

Thanks for reading and have a great day ☺️