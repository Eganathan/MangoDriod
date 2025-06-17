---
date: '2025-06-11T20:46:54+05:30' 
draft: false
title: 'Basic Bash Commands'
categories: ["Bash","Scripting"]
---

One of my mentors, [RWX-Rob](https://linktr.ee/rwxrob), runs online bootcamps called Boost, where he shares tech industry standards. A key lesson he emphasizes is the importance of learning Linux and working with its Bash command-line. Mastering the terminal has helped me save time and stay focused. These are my quick reference notes — not an exhaustive list, but the commands I use most often and im sure it will be useful for you too.

btw BASH is short for Bourne Again SHell, just in case some one asks, so lets move it:

## Mac Switching between Zsh and Bash

As a software developer, choose **Bash** if you're new to shell scripting due to its familiarity and abundance of online resources, while opting for **Zsh** for improved performance, customization, and
security features, keeping in mind that switching to Zsh might require adapting to some differences when working with Linux distributions.

```bash
chsh -s /bin/bash  # switch to bash
chsh -s /bin/zsh   # Switch to zsh
```

## Identity

```bash
pwd             # Print current working directory
whoami          # Show current user
clear           # Clear the terminal screen
history         # Show command history
```

## File & Directory Navigation

```bash
ls              # List files
ls -la          # List all files with details
cd /path/to/dir # Change directory
cd ..           # Go up one directory
cd -            # Go to previous directory
```

## File Operations

```bash
touch file.txt              # Create a new empty file
mkdir folder                # Create a new directory
cp file1.txt file2.txt      # Copy file or dir
mv file1.txt file2.txt      # Rename or move file or dir
rm file.txt                 # Delete file 
rm -r folder                # Delete directory recursively
```

## Searching & Finding

```bash
grep "text" file.txt        # Search for text in a file
grep -r "text" .            # Recursive search in directory
find . -name "*.sh"         # Find all .sh files
```

## Editing Files

```bash
vi file.txt                 # Open file in Vim editor (i don't like nano sorry!) 
cat file.txt                # Print file content
less file.txt               # Scroll through file
head file.txt               # First 10 lines
tail file.txt               # Last 10 lines
```

- Vim Editor has its own commands and pallets, will add my reference here.

## Permissions

```bash
chmod +x script.sh          # Make script executable
chmod 755 file              # Set permissions (owner rwx, others rx)
chown user:group file       # Change ownership
ls -l file                  # Get info of file permissions and owner etc
ls -ld folder               # Get info of folder permissions and owner etc
```

### Permissions String Quick Reference

```bash
-rw-r--r-- 1 user group 1234 Jun 16 19:00 myfile.txt # Example output for ls -l file check the table for ref
drwxr-xr-x 2 user group 4096 Jun 16 19:00 mydir # Example output for ls -ld folder check the table for ref
```

| Position  | Meaning                                | Example                          |
|-----------|----------------------------------------|----------------------------------|
| 1st char  | File type (`-` file, `d` directory, `l` symlink) | `-` = file, `d` = directory        |
| 2-4       | Owner permissions (read `r`, write `w`, execute `x`) | `rwx` = owner can read, write, execute |
| 5-7       | Group permissions                      | `r-x` = group can read, execute  |
| 8-10      | Others permissions                     | `r--` = others can only read     |


## Scripts & Variables

```bash
#!/bin/bash
echo "Hello, $USER"         # Sample Bash script

# Variables
name="Eganathan"
echo "Hi, $name"
```

## Loops & Conditions

```bash
# If
if [ -f "file.txt" ]; then
  echo "Exists"
fi

# For loop
for f in *.txt; do
  echo "$f"
done
```

## Time Savers

```bash
!!              # Repeat last command
!abc            # Run last command starting with 'abc'
Ctrl + R        # Reverse search command history
Ctrl + L        # Clear screen (same as `clear`)
Ctrl + A / E    # Move to beginning / end of line
```

## Date Time

```bash
date # Print current date and time
date +"%T"        # Print current time in 24-hour format (HH:MM:SS)
date +"%r"        # Print current time in 12-hour format with AM/PM
date +"%F"        # Print current date in YYYY-MM-DD format
date +"%d-%m-%Y"  # Print current date in custom format: Day Month Year
date -u           # Print current UTC time
```

## Use alias to create shortcuts

```bash
alias gs="git status" # hope you have git installed
alias ..="cd .." # this have saved a quite a lot of time for me
```

## Combine commands

```bash
command1 && command2  # Run command2 only if command1 succeeds
command1 || command2  # Run command2 only if command1 fails
```

## copy file contents

```bash
cat file.txt | pbcopy
```

## Cleaning

```bash
df -h           # Disk usage
du -sh *        # Folder sizes
top             # Real-time process list
ps aux | grep xyz  # Check if a process is running
```

## Configuration Files

```bash
# Bash
cat ~/.bash_profile   # Main configuration file
cat ~/.bashrc         # Profile configuration file

# Zsh (Mac)
cat ~/.zshrc          # Main configuration file
cat ~/.zprofile       # Profile configuration file
```

These files persist aliases or environment variables and your personal scripts, this is really helpful to customize the shell for your taste

✅ Use the Main configuration file for environment variables like JAVA PATH and others.
✅ Use the Profile Configuration File for aliases and other similar settings.

⚠️ Once you add your alias or update the profile configuration, you will need to re-start the terminal for the new configuration to come into effect.

I keep a copy of the profile configuration in git so i have access to my configurations both on my work and other systems if i need em.

## Common commandline tool that is used often by me

- homebrew - package manager like npm
- ddgr - search from the commandline (DuckDuckGo)
- ollama - for local offline AI models for simple tasks and quires.
- zip/unzip – Compress/uncompress
- curl - API testing and others

> "Warning: Terminal use may cause excessive productivity and happiness." - Ollama 3.5