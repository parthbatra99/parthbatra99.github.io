# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Project Overview

This is a personal Jekyll blog for Parth Batra (batra.blog) built with the Minima theme. The site includes blog posts, various content sections (quick-wits, the-good-stuff, workbench), and is deployed to GitHub Pages at `https://parthbatra99.github.io`.

## Architecture

### Jekyll Structure
- **Posts**: Located in `_posts/` with Jekyll naming convention `YYYY-MM-DD-title.md`
- **Layouts**: Custom layouts in `_layouts/` for different page types:
  - `default.html` - Base layout with header/footer
  - `blog.html` - Blog post listing layout
  - `post.html` - Individual blog post layout
  - Custom layouts for special sections: `workbench.html`, `the-good-stuff.html`, `quick-wits.html`
- **Includes**: Shared components in `_includes/`:
  - `head.html` - HTML head section
  - `header.html` - Navigation header
- **Data**: Navigation menu defined in `_data/navigation.yml`
- **Styling**: Custom SCSS in `assets/main.scss` extending Minima theme

### Content Sections
- **Blog**: Traditional blog posts in `_posts/`
- **Quick-wits**: Short thoughts/ideas (`quick-wits.md` → `/quick-wits/`)
- **The Good Stuff**: Curated content highlights (`the-good-stuff.md` → `/the-good-stuff/`)
- **Workbench**: Projects/experiments (`workbench.md` → `/workbench/`)
- **List 16.4**: Special list content (`list-100.md` → `/list-16-4/`)

## Development Commands

### Build and Serve
```bash
# Install dependencies
bundle install

# Serve locally at http://localhost:4000
bundle exec jekyll serve

# Build for production
bundle exec jekyll build
```

### Common Tasks
- **New blog post**: Create file in `_posts/` with format `YYYY-MM-DD-title.md`
- **Update navigation**: Edit `_data/navigation.yml`
- **Modify styling**: Edit `assets/main.scss`
- **Layout changes**: Modify files in `_layouts/` or `_includes/`

## Configuration

- **Site config**: `_config.yml` contains site metadata, author info, social links
- **Theme**: Uses Minima theme with jekyll-toc plugin for table of contents
- **Deployment**: Configured for GitHub Pages deployment from main branch

## File Naming Conventions

- Blog posts: `YYYY-MM-DD-title.md` (Jekyll standard)
- Layout files: `{section-name}.html` (e.g., `blog.html`, `workbench.html`)
- Section pages: `{section-name}.md` with front matter specifying layout and permalink