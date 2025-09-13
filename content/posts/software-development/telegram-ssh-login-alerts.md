---
title: "How to Set Up Telegram Alerts for SSH Logins on Debian"
date: 2025-09-13T10:00:00+05:30
draft: false
tags: ["debian", "vps", "security", "telegram", "ssh", "automation"]
---

Securing your Virtual Private Server (VPS) is critical. A simple and effective way to monitor access is to receive real-time notifications for every successful SSH login. This guide provides a step-by-step walkthrough for setting up instant Telegram alerts on a Debian-based server, giving you immediate awareness of all shell access.

## 1. Prerequisites

Before you begin, ensure you have the following:

- A server running a Debian-based Linux distribution.
- `sudo` or `root` access to the server.
- A Telegram account.
- `curl` and `jq` installed on your server. If you don't have them, install them now:
  ```bash
  sudo apt-get update && sudo apt-get install -y curl jq
  ```

## 2. Create a Telegram Bot

Your alerts will be sent by a Telegram Bot.

### Step 1: Talk to BotFather
In your Telegram app, search for the verified **BotFather** account and start a chat.

### Step 2: Create the Bot
Send the `/newbot` command. Follow the prompts to give your bot a display name and a unique username, which must end in `bot`.

### Step 3: Save the API Token
Once created, BotFather will provide a secret **API token**. Copy this token and keep it secure; you will need it in the next steps.

## 3. Get Your Personal Chat ID

The bot needs to know where to send the alerts. This will be your personal Telegram chat.

### Step 1: Start a Chat with Your Bot
Search for your new bot in Telegram and send it any message (e.g., `/start`). This initializes the chat.

### Step 2: Retrieve the Chat ID
In your server's terminal, run the following command. Replace `<YOUR_BOT_TOKEN>` with the token you saved from BotFather.

```bash
curl -s "https://api.telegram.org/bot<YOUR_BOT_TOKEN>/getUpdates" | jq '.result[0].message.chat.id'
```

This command will output a long number, which is your **Chat ID**. Copy it.

## 4. Create the Notification Script

This shell script will be triggered on login, gather information, and send the alert.

### Step 1: Create the Script File
Using a text editor, create a new file for the script:

```bash
sudo nano /usr/local/bin/ssh-login-alert.sh
```

### Step 2: Add the Script Content
Paste the following code into the file. **Remember to replace the placeholder values for `BOT_TOKEN` and `CHAT_ID` with your actual credentials.**

```bash
#!/bin/bash

# --- Replace with your details ---
BOT_TOKEN="<YOUR_BOT_TOKEN>"
CHAT_ID="<YOUR_CHAT_ID>"
#----------------------------------

# Do nothing if not an interactive session
if [ -z "$PAM_TYPE" ] || [ "$PAM_TYPE" != "open_session" ]; then
    exit 0
fi

# Gather login information
HOSTNAME=$(hostname)
USER=$PAM_USER
IP_ADDRESS=$PAM_RHOST
TIMESTAMP=$(date +"%Y-%m-%d %H:%M:%S")

# Format the message using Markdown
MESSAGE=$(cat <<EOF
🔔 *New SSH Login Detected* 🔔

*Server:* \`$HOSTNAME\`
*User:* \`$USER\`
*From IP:* \`$IP_ADDRESS\`
*Time:* \`$TIMESTAMP\`
EOF
)

# Send the message via the Telegram API
curl -s --max-time 10 -X POST "https://api.telegram.org/bot$BOT_TOKEN/sendMessage" \
     -d chat_id="$CHAT_ID" \
     -d text="$MESSAGE" \
     -d parse_mode="Markdown" > /dev/null
```

### Step 3: Make the Script Executable
Save the file and make it executable so the system can run it.

```bash
sudo chmod +x /usr/local/bin/ssh-login-alert.sh
```

## 5. Configure PAM to Trigger the Script

We'll use the Pluggable Authentication Module (PAM) framework to execute our script whenever a user opens a new SSH session.

### Step 1: Edit the SSHD PAM Configuration
Open the PAM configuration file for the SSH daemon:

```bash
sudo nano /etc/pam.d/sshd
```

### Step 2: Add the Execution Rule
Add the following line at the very **end** of the file. This tells PAM to run our script for every session, but our script is smart enough to only act on SSH logins.

```
# Run script for SSH login notification
session optional pam_exec.so /usr/local/bin/ssh-login-alert.sh
```

Save and close the file.

## 6. Test the Setup

You're all set! To test the notification, log out of your server and log back in via SSH.

```bash
exit
```

```bash
ssh your_user@your_server_ip
```

Within seconds, you should receive a neatly formatted notification on Telegram from your bot. If you don't, double-check that the `BOT_TOKEN` and `CHAT_ID` in your script are correct and that the script is executable.

```