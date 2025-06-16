---
date: '2025-06-11T20:46:54+05:30' 
draft: false
title: 'Basic Bash commands for terminal'
categories: ["Bash","Scripting"]
---

A growing list of Bash commands i use on mac(some only work on mac and its marked with [M]), tips, and tricks to help me stay sharp on the terminal. This is my personal cheat sheet.

## Basics

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
cp file1.txt file2.txt      # Copy file
mv file1.txt file2.txt      # Rename or move file
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
```

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
Ctrl + R        # Reverse search history
Ctrl + L        # Clear screen (same as `clear`)
Ctrl + A / E    # Move to beginning / end of line
```


## Others

- Use alias to create shortcuts:

```bash
alias gs="git status" # hope you have git installed
alias ..="cd .." # this have saved a quite a lot of time for me
```

- Combine commands:

```bash
command1 && command2  # Run command2 only if command1 succeeds
command1 || command2  # Run command2 only if command1 fails
```

- Use .bashrc or .bash_profile to persist aliases or environment variables. (Really useful, we can use same settings on work and other laptops)

- copy file contents [M]:

```bash
cat file.txt | pbcopy
```

- Cleaning

```bash
df -h           # Disk usage
du -sh *        # Folder sizes
top             # Real-time process list
ps aux | grep xyz  # Check if a process is running
```

- Common Tools
    -- gpt - gpt cli tool
    -- ddgr - search from the commandline
    -- curl – Fetch from URL
    -- wget – Download files
    -- tar -xzvf file.tar.gz – Extract tar.gz
    -- zip/unzip – Compress/uncompress