---
date: '{{ .Date | time.Format ":date_medium" }}' 
draft: true
title: '{{ replace .File.ContentBaseName "-" " " | title }}'
---
