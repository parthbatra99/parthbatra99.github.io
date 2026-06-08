# Setup

## Ruby

System macOS Ruby is too old. Use Homebrew:

```bash
brew install ruby
```

Add to `~/.zshrc`:

```bash
export PATH="/opt/homebrew/opt/ruby@4.0/bin:$PATH"
```

Then:

```bash
source ~/.zshrc
gem install bundler
bundle install
```

## Start server

```bash
export PATH="/opt/homebrew/opt/ruby@4.0/bin:$PATH"
bundle exec jekyll serve
# http://localhost:4000 — live reload on save
```

Different port:

```bash
bundle exec jekyll serve --port 4001
```

## Stop server

`Ctrl+C` in the terminal, or if backgrounded:

```bash
pkill -f "jekyll serve"
```

## Build

```bash
export PATH="/opt/homebrew/opt/ruby@4.0/bin:$PATH"
bundle exec jekyll build
# output → _site/
```

## Deploy (build + push)

`_site/` is committed. GitHub Pages serves from `main`.

```bash
export PATH="/opt/homebrew/opt/ruby@4.0/bin:$PATH"
bundle exec jekyll build
git add -A
git commit -m "rebuild"
git push origin main
# live at fromparth.blog within ~1 min
```

## Structure

| Path | Purpose |
|---|---|
| `_posts/` | Blog posts (`YYYY-MM-DD-title.md`) |
| `_layouts/` | Page templates |
| `_includes/` | Shared partials (header, footer, head) |
| `_data/navigation.yml` | Nav links |
| `assets/main.scss` | All styles |
| `index.html` | Homepage |
| `cv.md` | CV page |
| `_config.yml` | Site config, email, social handles |
| `_site/` | Built output — commit after every build |
