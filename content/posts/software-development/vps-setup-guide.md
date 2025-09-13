---
title: "Advanced VPS Guide: Mastering Nginx, Subdomains, and Reverse Proxies"
date: 2025-09-07T12:00:00+05:30
tags: ["vps", "linux", "server", "nginx", "security", "subdomain", "reverse-proxy"]
draft: false
---

A Virtual Private Server (VPS) is your personal canvas on the internet. While basic setup is straightforward, unlocking its true potential requires mastering the web server. This guide dives deep into using Nginx to host multiple projects, manage subdomains, and route traffic to different services, transforming your single server into a multi-functional powerhouse.

## 1. Initial Server Setup

After acquiring a VPS, you'll get an IP address and root access. Your first steps are to secure the server and create a non-root user for daily operations.

Connect to your server via SSH:
```bash
ssh root@YOUR_SERVER_IP
```

### Create a Sudo User

Operating as `root` is risky. Create a new user and grant administrative privileges.

```bash
# Create the new user (replace 'devuser' with your username)
adduser devuser

# Add the user to the 'sudo' group
usermod -aG sudo devuser
```

Now, set up SSH key authentication for your new user for enhanced security and convenience, then log in as that user.

## 2. Essential Security and Updates

A public server is a constant target. Secure it immediately.

### Configure the Firewall

`ufw` (Uncomplicated Firewall) makes this easy. We'll allow SSH, HTTP, and HTTPS traffic.

```bash
# Allow OpenSSH (so you don't lock yourself out)
sudo ufw allow OpenSSH

# Allow Nginx to handle web traffic on ports 80 and 443
sudo ufw allow 'Nginx Full'

# Enable the firewall
sudo ufw enable
```

After enabling, check its status to ensure it's active and your rules are loaded.
```bash
sudo ufw status
```

### Update Your Server

Keep your system's packages current to patch security vulnerabilities.

```bash
sudo apt update && sudo apt upgrade -y
```

## 3. Installing and Understanding Nginx

Nginx is the heart of our setup. It's a high-performance web server that can also act as a reverse proxy, load balancer, and more.

```bash
# Install Nginx
sudo apt install nginx -y
```

While the package should start and enable Nginx automatically, it's good practice to run the commands explicitly to be sure.

```bash
# Start the Nginx service
sudo systemctl start nginx

# Enable Nginx to start automatically on boot
sudo systemctl enable nginx

# Now, check that it's running and enabled
sudo systemctl status nginx
```
You should see `active (running)` in the output. Visiting your server's IP in a browser should also show the Nginx welcome page.

### Nginx Configuration Structure

Nginx's configuration lives in `/etc/nginx`. The `-p` flag in the commands below ensures that the command does nothing if the directories already exist.

```bash
sudo mkdir -p /etc/nginx/sites-available
sudo mkdir -p /etc/nginx/sites-enabled
```

The key directories are:
*   `/etc/nginx/nginx.conf`: The main configuration file. You rarely edit this.
*   `/etc/nginx/sites-available/`: Where you store the configuration files for each of your sites (called "server blocks").
*   `/etc/nginx/sites-enabled/`: Where you create symbolic links to the configurations in `sites-available` that you want to be active.

This structure lets you easily enable or disable sites without deleting their configuration files.

## 4. Advanced Hosting: Subdomains and Reverse Proxies

This is where the magic happens. A single server can host a blog, a portfolio website, a web app, and several APIs, all neatly organized using subdomains.

The core concept is the **Reverse Proxy**. Your Nginx server listens on the standard web ports (80 for HTTP, 443 for HTTPS) and intelligently forwards incoming requests to the correct internal service based on the requested domain or subdomain.

### Scenario:
Let's say we want to set up the following on our server:
1.  `eknath.dev`: A static HTML/CSS website.
2.  `blog.eknath.dev`: A separate project, maybe a Hugo or Jekyll site.
3.  `api.eknath.dev`: A Node.js application running on port `3000`.

### Step 1: Create Project Directories

Organize your projects in the `/var/www` directory.

```bash
# Create directories for the main site and blog
sudo mkdir -p /var/www/eknath.dev/html
sudo mkdir -p /var/www/blog.eknath.dev/html

# Set correct permissions
sudo chown -R $USER:$USER /var/www/eknath.dev
sudo chown -R $USER:$USER /var/www/blog.eknath.dev
```

Verify that the directories were created with the correct ownership.
```bash
ls -ld /var/www/eknath.dev/
ls -ld /var/www/blog.eknath.dev/
```

Now, place some placeholder files.
```bash
echo "<h1>Welcome to Eknath's Site</h1>" | sudo tee /var/www/eknath.dev/html/index.html
echo "<h1>Welcome to Eknath's Blog</h1>" | sudo tee /var/www/blog.eknath.dev/html/index.html
```

### Step 2: Create Nginx Server Blocks

Now, we create a configuration file for each site in `sites-available`.

**For the main domain (`eknath.dev`):**

```bash
sudo nano /etc/nginx/sites-available/eknath.dev
```

Add the following server block:
```nginx
server {
    listen 80;
    listen [::]:80;

    server_name eknath.dev www.eknath.dev;

    root /var/www/eknath.dev/html;
    index index.html index.php;

    location / {
        try_files $uri $uri/ =404;
    }
}
```

**For the blog subdomain (`blog.eknath.dev`):**

```bash
sudo nano /etc/nginx/sites-available/blog.eknath.dev
```
Add this configuration:
```nginx
server {
    listen 80;
    listen [::]:80;

    server_name blog.eknath.dev;

    root /var/www/blog.eknath.dev/html;
    index index.html;

    location / {
        try_files $uri $uri/ =404;
    }
}
```

### Step 3: Configure the Reverse Proxy for the API

For `api.eknath.dev`, we'll proxy requests to our Node.js app, which we assume is running on `http://127.0.0.1:3000`.

Create the configuration file:
```bash
sudo nano /etc/nginx/sites-available/api.eknath.dev
```
Add the reverse proxy configuration:
```nginx
server {
    listen 80;
    listen [::]:80;

    server_name api.eknath.dev;

    location / {
        proxy_pass http://127.0.0.1:3000;
        proxy_set_header Host $host;
        proxy_set_header X-Real-IP $remote_addr;
        proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
        proxy_set_header X-Forwarded-Proto $scheme;
    }
}
```

### Step 4: Enable the Sites and Test

Now, link these configurations into `sites-enabled` to activate them.

```bash
sudo ln -s /etc/nginx/sites-available/eknath.dev /etc/nginx/sites-enabled/
sudo ln -s /etc/nginx/sites-available/blog.eknath.dev /etc/nginx/sites-enabled/
sudo ln -s /etc/nginx/sites-available/api.eknath.dev /etc/nginx/sites-enabled/
```

Test the Nginx configuration for syntax errors:
```bash
sudo nginx -t
```

If it's successful, restart Nginx to apply the changes:
```bash
sudo systemctl restart nginx
```

Check the status to ensure it restarted correctly.
```bash
sudo systemctl status nginx
```

After setting up your DNS records, you'll be able to access each service through its unique subdomain.

## 5. Securing Your Sites with SSL (HTTPS)

We'll use **Let's Encrypt**, a free and automated Certificate Authority, and **Certbot**, a tool that makes managing SSL/TLS certificates effortless.

### Step 1: Install Certbot

Certbot has a dedicated Nginx plugin that automates the process.

```bash
# Install Certbot and its Nginx plugin
sudo apt install certbot python3-certbot-nginx -y
```

### Step 2: Obtain and Install the SSL Certificates

With your server blocks already configured, running Certbot is incredibly simple.

```bash
# Run Certbot to get certificates for all configured domains
sudo certbot --nginx
```

Certbot will guide you through a few simple steps:
1.  **Enter your email address.**
2.  **Agree to the Terms of Service.**
3.  **Choose domains** from the list Certbot finds.
4.  **Choose to redirect HTTP to HTTPS.** This is highly recommended.

### Step 3: Verify the New Configuration

Certbot automatically modifies your Nginx files to enable HTTPS. You can check the new configuration by running `sudo nginx -t` and then reloading Nginx with `sudo systemctl reload nginx`.

### Step 4: Understanding Automatic Renewal

Let's Encrypt certificates are valid for 90 days. The Certbot package automatically sets up a task to renew them. You can test the renewal process with a dry run:
```bash
sudo certbot renew --dry-run
```
If this command runs without errors, your auto-renewal is set up correctly.

## Conclusion

You have now transformed a basic VPS into a sophisticated, multi-tenant hosting platform. By leveraging Nginx's server blocks and reverse proxy capabilities, you can host and manage numerous projects, each on its own subdomain, from a single server. Happy hosting!