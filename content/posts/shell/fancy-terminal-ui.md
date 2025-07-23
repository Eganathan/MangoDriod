---
title: "Making Your Terminal Fancy on Linux and macOS"
date: 2025-06-23T10:00:00+05:30
draft: false
---

> "My terminal looks really bad, while some people have a really cool CLI starting page with their name etc. What should I do so mine looks cool too?"

If you're spending a lot of time in your terminal, why not make it a pleasant and productive environment? A well-customized terminal can not only look cool but also boost your productivity. This guide will walk you through various ways to transform your bland terminal into a powerful and visually appealing workspace on Linux and macOS.

## 1. The Shell Prompt (PS1)

The shell prompt is the first thing you see. Customizing it can provide useful information at a glance.

### Basic Customization

You can customize your prompt by modifying the `PS1` environment variable in your shell's configuration file (`~/.bashrc` for Bash, `~/.zshrc` for Zsh).

For example, to show your username, hostname, and current working directory, you can add this to your config file:

```bash
export PS1="\u@\h:\w\$ "
```

### Advanced Prompt Customization with Starship

For a more powerful and visually rich prompt, you can use tools like [Starship](https://starship.rs/). Starship is a cross-shell prompt that is fast, customizable, and works on Linux, macOS, and Windows.

**Installation:**

*   **Linux (and macOS with Homebrew):**
    ```bash
    brew install starship
    ```
*   **Other Linux:**
    ```bash
    curl -sS https://starship.rs/install.sh | sh
    ```

**Configuration:**

Add the following to the end of your `~/.bashrc` or `~/.zshrc`:

```bash
eval "$(starship init bash)" # for Bash
eval "$(starship init zsh)"  # for Zsh
```

Starship is highly configurable. You can find more information in the [official documentation](https://starship.rs/config/).

## 2. Terminal Emulators

The terminal emulator is the application you use to interact with the shell. While the default terminal emulators on Linux and macOS are functional, there are better alternatives with more features and customization options.

*   **iTerm2 (macOS):** A powerful replacement for the default Terminal app on macOS. It offers features like split panes, search, and extensive customization.
*   **Alacritty:** A fast, cross-platform, OpenGL terminal emulator.
*   **Kitty:** A feature-rich and hackable GPU-based terminal emulator.

## 3. Color Schemes

A good color scheme can reduce eye strain and make your terminal more readable.

*   **Dracula:** A popular dark theme for many applications, including terminals.
*   **Solarized:** A theme with both light and dark variants, designed for readability.
*   **Nord:** A clean and elegant theme with a focus on clarity.

Most terminal emulators have built-in support for changing color schemes. You can also find collections of themes online, like [iTerm2 Color Schemes](https://iterm2colorschemes.com/).

## 4. Fonts with Ligatures

Using a font designed for programming can improve readability. Fonts with ligatures combine multiple characters into a single symbol, which can make your code look cleaner.

*   **Fira Code:** A popular free monospaced font with programming ligatures.
*   **JetBrains Mono:** A free and open-source font for developers.
*   **Cascadia Code:** A fun, new monospaced font from Microsoft that includes programming ligatures.

After installing a font, you'll need to configure your terminal emulator to use it.

## 5. Cool CLI Tools

Here are some tools that can make your terminal more informative and user-friendly:

*   **Neofetch:** A command-line system information tool that displays a logo of your OS along with system information.

    ```bash
    # macOS
    brew install neofetch

    # Linux (Debian/Ubuntu)
    sudo apt-get install neofetch
    ```
    Add `neofetch` to the end of your `~/.bashrc` or `~/.zshrc` to see it every time you open a new terminal.

*   **lsd or exa:** Modern replacements for the `ls` command with more features and better defaults.

    ```bash
    # lsd (macOS)
    brew install lsd

    # exa (macOS)
    brew install exa

    # lsd (Linux)
    sudo apt-get install lsd

    # exa (Linux)
    sudo apt-get install exa
    ```
    You can alias `ls` to `lsd` or `exa` in your shell's configuration file:
    ```bash
    alias ls='lsd'
    # or
    alias ls='exa'
    ```

*   **bat:** A `cat` clone with syntax highlighting and Git integration.

    ```bash
    # macOS
    brew install bat

    # Linux
    sudo apt-get install bat
    ```
    You can alias `cat` to `bat`:
    ```bash
    alias cat='bat'
    ```

*   **zoxide:** A smarter `cd` command that learns your habits.

    ```bash
    # macOS
    brew install zoxide

    # Linux
    curl -sS https://raw.githubusercontent.com/ajeetdsouza/zoxide/main/install.sh | bash
    ```
    Add the following to your `~/.bashrc` or `~/.zshrc`:
    ```bash
    eval "$(zoxide init bash)" # for Bash
    eval "$(zoxide init zsh)"  # for Zsh
    ```

## Conclusion

By combining these tools and techniques, you can create a terminal environment that is not only beautiful but also tailored to your workflow. Experiment with different tools and configurations to find what works best for you. A personalized terminal can make your command-line experience much more enjoyable and productive.
