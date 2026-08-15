---
title: "Blog Help & Quick Reference"
date: 2026-08-15
draft: false
description: "Personal reference for managing this Hugo blog — creating posts, pages, front matter, and common commands."
ShowToc: true
TocOpen: true
---

## Project Structure

```
mangoDriod/
├── content/
│   ├── posts/          ← all blog posts live here
│   │   ├── ai-ml/
│   │   ├── android/
│   │   ├── cmp/
│   │   ├── drafts/     ← WIP posts (draft: true)
│   │   ├── DSA/
│   │   ├── iot/
│   │   ├── shell/
│   │   └── software-development/
│   ├── archives.md     ← special page (layout: archives)
│   ├── search.md       ← special page (layout: search)
│   └── doc.md          ← this file
├── archetypes/
│   └── default.md      ← template used by `hugo new`
├── static/             ← images, files served as-is
├── themes/PaperMod/
└── hugo.yaml           ← site config (nav, params, etc.)
```

---

## Creating a New Post

### Option A — Hugo CLI (recommended)

```bash
# Creates content/posts/my-new-post.md with front matter filled in
hugo new posts/my-new-post.md

# Under a category subfolder
hugo new posts/android/my-android-post.md
hugo new posts/shell/my-shell-tip.md
```

The file is created from `archetypes/default.md`. It starts with `draft: true` so it won't appear on the live site until you flip it.

### Option B — Copy an existing post

Duplicate any `.md` file inside `content/posts/`, update the front matter, and start writing.

---

## Front Matter Reference

Every post starts with a YAML block between `---` fences.

```yaml
---
title: "My Post Title"
date: 2026-08-15T10:00:00+05:30   # ISO 8601, include timezone
draft: false                        # true = hidden from build output
categories: ["Android"]            # shown as category links
tags: ["kotlin", "compose"]        # shown as tag chips
description: "One-liner shown in list views and SEO meta."
cover:
  image: "images/cover.png"        # relative to static/ or post bundle
  alt: "Cover image alt text"
weight: 1                          # lower = listed first (optional)
---
```

**Minimal working front matter:**

```yaml
---
title: "Title Here"
date: 2026-08-15
draft: false
---
```

---

## Drafts

- Set `draft: true` to hide a post from `hugo build` and production.
- To preview drafts locally: `hugo server -D`
- To publish: change `draft: true` → `draft: false`
- The `content/posts/drafts/` folder is just a naming convention — `draft:` in the front matter is what actually controls visibility.

---

## Categories & Tags

Both are free-form arrays in front matter.

```yaml
categories: ["AI/ML", "AI-Tools"]
tags: ["claude", "android", "kotlin"]
```

- Categories are broader topics; tags are specific keywords.
- Both auto-generate listing pages at `/categories/` and `/tags/`.
- Existing categories in this blog: `Android`, `AI/ML`, `AI-Tools`, `Shell`, `Software Development`, `IoT`, `DSA`, `CMP`.

---

## Creating a Standalone Page

A standalone page (not a post) goes directly under `content/`.

```bash
hugo new about.md
```

Then in its front matter, don't set a category — just give it a `title`. It'll be available at `/about/`.

Special layouts PaperMod supports:

| `layout` value | What it renders |
|---|---|
| `archives` | Monthly/yearly post archive |
| `search` | Full-text search UI |
| *(none/default)* | Plain content page |

Example (like `archives.md`):
```yaml
---
title: "Archive"
layout: "archives"
url: "/archives/"
summary: archives
---
```

---

## Local Dev Server

```bash
# Start local server with live reload
hugo server

# Include draft posts
hugo server -D

# Custom port
hugo server -p 1314
```

Site is available at `http://localhost:1313` by default.

---

## Build & Deploy

```bash
# Build static files into public/
hugo

# Build including drafts (for review only, don't deploy)
hugo -D
```

The `public/` folder is the deployable output.

---

## Adding to the Nav Menu

Edit `hugo.yaml` — add an entry under `menu.main`:

```yaml
menu:
  main:
    - identifier: "doc"
      name: Doc
      url: /doc/
      weight: 5      # controls order; lower = further left
```

---

## Images & Static Files

Put images in `static/images/` — they're served from the site root.

```markdown
![Alt text](/images/my-image.png)
```

Or reference in front matter:

```yaml
cover:
  image: "/images/my-image.png"
  alt: "Alt text"
```

---

## Useful Hugo Commands

| Command | What it does |
|---|---|
| `hugo new posts/name.md` | Create a new post from archetype |
| `hugo server -D` | Dev server with drafts |
| `hugo` | Build to `public/` |
| `hugo list drafts` | List all draft posts |
| `hugo list future` | List posts with future dates |
| `hugo --minify` | Build with minified output |

---

## Resources Section

Lives at `content/resources/`. Not shown on the home page (controlled by `mainSections: ["posts"]` in `hugo.yaml`). Accessible at `/resources/`.

Current topic pages:

| File | URL |
|---|---|
| `resources/kotlin.md` | `/resources/kotlin/` |
| `resources/android.md` | `/resources/android/` |
| `resources/kmp.md` | `/resources/kmp/` |
| `resources/dsa.md` | `/resources/dsa/` |

To add a new topic, create `content/resources/my-topic.md` with the same front matter pattern.

### `linkcard` shortcode

Renders a styled link card. Use it inside any resource page (or any post).

```
{{</* linkcard url="https://..." title="Title" desc="Optional description" type="article" */>}}
```

**`type` values and their colours:**

| type | colour |
|---|---|
| `article` | blue |
| `video` | yellow |
| `playlist` | green |
| `doc` | purple |
| `tool` | orange |
| `repo` | teal |
| `link` | default (no colour) |

For YouTube playlists use the built-in Hugo shortcode:
```
{{</* youtube VIDEO_OR_PLAYLIST_ID */>}}
```

---

## Archetype (default template)

Located at `archetypes/default.md`. Edit this to change what `hugo new` generates:

```yaml
---
date: '{{ .Date }}'
draft: true
title: '{{ replace .File.ContentBaseName "-" " " | title }}'
categories: ["default"]
tags: ["default","default1"]
---
```
