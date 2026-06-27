#!/usr/bin/env bash
# Daily narration: find lowest recommended_order post without narration, generate, commit, push.

set -euo pipefail

REPO="$(cd "$(dirname "$0")/.." && pwd)"
POSTS_DIR="$REPO/_posts"
AUDIO_DIR="$REPO/assets/audio/posts"
LOG="$REPO/scripts/narration.log"

# Load GEMINI_API_KEY from ~/.env.narration (never committed to git)
if [ -f "$HOME/.env.narration" ]; then
  # shellcheck disable=SC1090
  source "$HOME/.env.narration"
fi

if [ -z "${GEMINI_API_KEY:-}" ]; then
  log "ERROR: GEMINI_API_KEY not set. Add it to ~/.env.narration"
  exit 1
fi

log() { echo "[$(date '+%Y-%m-%d %H:%M:%S')] $*" | tee -a "$LOG"; }

log "=== daily_narration.sh start ==="

# Find candidate: recommended: true, no narration: true, pick lowest recommended_order
TARGET=""
BEST_ORDER=9999
TITLE=""

for f in "$POSTS_DIR"/*.md; do
  fm=$(awk '/^---/{c++;next} c==1' "$f")
  recommended=$(echo "$fm" | grep -E '^recommended:\s*true' || true)
  narration=$(echo "$fm" | grep -E '^narration:\s*true' || true)
  [ -z "$recommended" ] && continue
  [ -n "$narration" ] && continue

  order=$(echo "$fm" | grep -E '^recommended_order:' | awk '{print $2}' | tr -d '"'"'" || echo "9999")
  order=${order:-9999}

  if [ "$order" -lt "$BEST_ORDER" ]; then
    BEST_ORDER="$order"
    TARGET="$f"
    TITLE=$(echo "$fm" | grep -E '^title:' | sed 's/^title:\s*//' | tr -d '"'"'")
  fi
done

if [ -z "$TARGET" ]; then
  log "All recommended posts already have narration. Nothing to do."
  exit 0
fi

STEM=$(basename "$TARGET" .md)
MP3="$AUDIO_DIR/${STEM}.mp3"

log "Target: $STEM (order=$BEST_ORDER)"
log "Title : $TITLE"

# Skip generation if MP3 already exists
if [ -f "$MP3" ]; then
  log "MP3 already exists, skipping generation."
else
  log "Installing google-genai..."
  pip3 install -q google-genai

  log "Generating narration..."
  python3 "$REPO/scripts/generate_narration.py" "$TARGET" 2>&1 | tee -a "$LOG"

  if [ ! -f "$MP3" ]; then
    log "ERROR: MP3 not created. Check log above. Exiting."
    exit 1
  fi
fi

# Update front matter if not already done
if ! grep -q 'narration: true' "$TARGET"; then
  log "Updating front matter..."
  # Insert before closing --- of front matter
  python3 - "$TARGET" "$STEM" <<'PYEOF'
import sys, re
path, stem = sys.argv[1], sys.argv[2]
text = open(path).read()
# Find second ---
second = text.index('---', 3)
front = text[:second]
rest = text[second:]
insert = f'narration: true\nnarration_src: "/assets/audio/posts/{stem}.mp3"\n'
open(path, 'w').write(front + insert + rest)
PYEOF
fi

# Commit and push
cd "$REPO"
git config user.email "hi@fromparth.blog"
git config user.name "Parth Batra"
git add "assets/audio/posts/${STEM}.mp3" "_posts/$(basename "$TARGET")"
git commit -m "feat: add narration to ${TITLE}"
git push origin main

log "Done: narration committed and pushed for: $TITLE"
