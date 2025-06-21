---
date: '2025-06-20T19:47:13+05:30' 
title: 'Ollama & Goose cli - Offline Agent setup'
categories: ["AI/ML"]
tags: ["AI","ML"]
---

## Fair Warning

Make sure you are using a capable system — ideally with a powerful CPU, GPU, and adequate cooling — before running large language models locally. LLMs can consume significant resources, generate substantial heat, and may cause system instability or damage if your hardware isn’t up to the task. Please proceed with caution!

This guide walks you through setting up Ollama (with deepseek-r1-goose) and Goose CLI. 

## Step 1: Download & Install Ollama

```bash
curl -fsSL https://ollama.com/install.sh | sh
```

Or, if you prefer to download manually then checkout:[https://ollama.com/download](https://ollama.com/download)
[Ollama-SetUpGuide](https://md.eknath.dev/posts/shell/command-line-tools/#ollama---local-and-opensource-llms)

## Step 2:Pull and Run the model

The following model is optimized for the agent we are going to install next so lets pull and run the model:

```bash
ollama run michaelneale/deepseek-r1-goose
```
more info about the model is available here [https://www.ollama.com/michaelneale/deepseek-r1-goose](https://www.ollama.com/michaelneale/deepseek-r1-goose)

## Step 3: Download And configure Goose-cli

Download the goose via HomeBrew if you don't have it installed please check this article [HomeBrew-SetUpGuide](https://md.eknath.dev/posts/shell/command-line-tools/#homebrew)

```bash
brew install block-goose-cli
```

now you can run the goose

```bash
goose 
```

Running after the first installation, the configure menu will be shown, make sure you select `Ollama` as the model provider, you can navigate by up and down arrow and hit return/enter to select the option.

After the model provider, next comes the model selection option, just type `michaelneale/deepseek-r1-goose` and hit return/enter.

Later if you want to change the model you can always run ```bash goose configure```, i would recommend you use this model others are not working as expected this is already slow.

You can stop goose by given `/exit` command.

## Where Offline Agents Work Best

- The task is narrow, well-defined, and focused.
- You want fast, private processing without sending data to the cloud.
- You are working with small to moderate inputs and outputs, as local models may struggle with large contexts or long conversations on limited hardware.
- Context limit required is less than 32K tokens

Again, always monitor your system’s health, and don’t hesitate to stop the model if things heat up!
