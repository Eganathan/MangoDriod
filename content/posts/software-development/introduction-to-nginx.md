---
title: "Introduction to Nginx: Hosting Your First Website"
date: 2025-09-13T12:00:00+05:30
draft: false
tags: ["nginx", "web server", "linux", "vps", "beginner"]
---

So you have a server, and now you want to share your project with the world. To do that, you need a web server. Nginx (pronounced "Engine-X") is one of the most popular, powerful, and efficient web servers available. It's famous for its high performance and its ability to also act as a reverse proxy, but at its core, it's brilliant at serving web pages.

This guide will walk you through the basics of Nginx, explaining its structure and showing you how to set up your very first website.

## 1. Installation

If you haven't already, you can install Nginx on any Debian-based system (like Ubuntu) with a single command. It's also good practice to ensure your firewall allows web traffic.

```bash
# Install Nginx
sudo apt update
sudo apt install nginx -y

# Allow Nginx through the firewall
sudo ufw allow 'Nginx Full'
```

To check that it's running, you can use `systemctl`:

```bash
sudo systemctl status nginx
```

If it's active, you can visit your server's IP address in a web browser, and you should see the default "Welcome to Nginx!" page.

## 2. Understanding the Nginx Directory Structure

Nginx's configuration can seem intimidating, but it's very logical. All the important files live in `/etc/nginx/`.

- `/etc/nginx/nginx.conf`: The main configuration file. You will rarely need to edit this file directly.
- `/etc/nginx/sites-available/`: This is where you will store the configuration files for each of your websites. Think of it as a library of all possible sites you *could* host.
- `/etc/nginx/sites-enabled/`: This directory contains symbolic links (shortcuts) to the files in `sites-available`. Nginx only reads the configurations in this `sites-enabled` directory. This setup allows you to easily turn websites on and off without deleting their configuration.

## 3. Setting Up Your First Site (A Server Block)

Let's host a website for a domain you own, `your-domain.com`. First, ensure you have pointed your domain to your server's IP address using an `A` record at your domain registrar.

### Step 1: Create a Home for Your Website
It's standard practice to store website files in the `/var/www/` directory.

```bash
# Create a directory for your domain
sudo mkdir -p /var/www/your-domain.com/html

# Assign ownership to your current user so you can edit files easily
sudo chown -R $USER:$USER /var/www/your-domain.com/html
```

### Step 2: Create a Sample Page
Let's create a simple `index.html` file for Nginx to serve.

```bash
echo "<h1>Success! The your-domain.com server block is working!</h1>" > /var/www/your-domain.com/html/index.html
```

### Step 3: Create the Nginx Configuration File
Nginx calls the configuration for a single site a "server block". We will create a new file in `sites-available` for our domain.

```bash
sudo nano /etc/nginx/sites-available/your-domain.com
```

Paste in the following configuration. Each line is explained by the comments.

```nginx
# This defines a server
server {
    # Listen on port 80 (standard HTTP) for both IPv4 and IPv6
    listen 80;
    listen [::]:80;

    # The root directory where the website files are stored
    root /var/www/your-domain.com/html;

    # The order of files to look for when a request comes in
    index index.html index.htm;

    # The domain names this server block should respond to
    server_name your-domain.com www.your-domain.com;

    # This block handles how to find files
    location / {
        # Try to serve the requested file, then a directory, or else show a 404 error
        try_files $uri $uri/ =404;
    }
}
```

### Step 4: Enable Your Site
Now, we need to tell Nginx to actually use this configuration. We do this by creating a symbolic link to the file in the `sites-enabled` directory.

```bash
sudo ln -s /etc/nginx/sites-available/your-domain.com /etc/nginx/sites-enabled/
```

### Step 5: Test and Restart Nginx
It's very important to test your configuration file for syntax errors before restarting Nginx.

```bash
sudo nginx -t
```

If you see `syntax is ok` and `test is successful`, you are good to go. Restart Nginx to apply the changes.

```bash
sudo systemctl restart nginx
```

That's it! If you now visit `http://your-domain.com` in your browser, you will see your "Success!" message instead of the default Nginx welcome page.

## 4. What's Next?

You have successfully configured Nginx to host a basic website. This is the foundation for hosting any web project. From here, you can:

- **Host multiple websites** on the same server by creating a new directory and a new server block file for each domain.
- **Set up a reverse proxy** to pass traffic to applications running on different ports (like Node.js or Python apps).
- **Secure your sites with SSL/TLS** using a free tool like Certbot to enable HTTPS.

These more advanced topics are covered in our "Advanced VPS Guide: Mastering Nginx, Subdomains, and Reverse Proxies".
