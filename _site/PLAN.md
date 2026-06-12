# Plan: Download YouTube Transcripts & Generate Blog Posts for fromparth.blog

## Context
Your brother has a YouTube channel with 24 videos (all full-length, 3–35 min each). We need to:
1. Download transcripts from all 24 videos
2. Generate blog posts in your personal Jekyll blog style (fromparth.blog)

## Key Findings

### Video Classification
- **All 24 videos are FULL videos** (none are Shorts — shortest is 3m 16s, longest is 35m 5s)
- All videos have auto-generated English captions available via `youtube-transcript-api`

### Your Blog Style (from `.skills/blog-writing.md`)
- First-person, conversational, like explaining to a smart friend over drinks
- Confident but not arrogant, self-deprecating humor, honest emotions
- Specific numbers, not vague quantifiers
- Delhi-Indian cultural seasoning when natural
- No corporate jargon, no "let's dive in", no em dashes
- Paragraphs ≤4 sentences, varied sentence length
- Jekyll format with `layout: post`, title, subtitle, date, tags
- Files named `YYYY-MM-DD-slug.md` in `_posts/`

### Tooling
| Tool | Status | Purpose |
|------|--------|---------|
| `youtube-transcript-api` | ✅ Working | Fetch auto-generated English transcripts |
| `yt-dlp` | ✅ Working | Get video metadata (title, duration, description) |
| Blog AI generation | ✅ This conversation's AI | Generate blog posts matching your voice |

## Approach

### Phase 1: Batch Download All Transcripts
1. Use `youtube_transcript_api` to fetch English transcripts for all 24 videos
2. Use `yt-dlp` to get metadata (publish date, description, duration) for proper Jekyll naming
3. Save each as a clean text file in `transcripts/` directory
4. Format: `transcripts/{video_id}_{slug}.txt` with title + transcript

### Phase 2: Generate Blog Posts
For each video transcript, generate a Jekyll blog post that:
- Follows the `.skills/blog-writing.md` voice guide exactly
- Uses `layout: post` with proper front matter
- Named `YYYY-MM-DD-{slug}.md` using the video's publish date
- Has a catchy title matching your title formula (first-person, specific, surprising)
- Opens with a strong hook (contradiction, confession, staggering fact, etc.)
- Structured body with headers, humor beats every 2-3 paragraphs
- Ends with a sharp closing insight (never summarizes)
- Includes 3-5 tags relevant to the content
- References the YouTube video link at the bottom (minimal byline)
- Saved in `_posts/` directory

### Directory Structure
```
transcripts/              # 24 raw transcript files
_posts/                   # 24 new blog posts (alongside existing 6)
```

## 24 Videos to Process

| # | Title | Duration | YouTube ID |
|---|-------|----------|------------|
| 1 | I Tried this 2-Minute Rule: My Output Jumped by 40% | 9m 52s | RKvOngBTrcc |
| 2 | The 4 KEY TAKEAWAYS That Changed My Everyday Life | 12m 48s | Kz663aIOSLg |
| 3 | Why Having Less Money Makes You More Creative! | 14m 58s | M-oyHqRgi0c |
| 4 | Say Goodbye to Reading Anxiety Forever! | 10m 31s | IdFz5SJKo-A |
| 5 | I Spent 107 Days Studying My Stupid Decisions | 9m 23s | DPUb7A2SjS4 |
| 6 | 9 Fundamentals to Build an Extraordinary Career | 14m 28s | 8AY0N7HOxdo |
| 7 | Multitasking vs Task Switching | 19m 58s | ZiJAI4rl3KY |
| 8 | Does 5 AM Make You Smarter or Just Tired? | 13m 34s | xnPA1Rz7BaI |
| 9 | Surprising Way to Boost Your Productivity Starting Today | 6m 29s | U2uPm-W1TPY |
| 10 | Let's Solve 80% of Your Problems in 20 Minutes | 20m 53s | qLBPTY35OXs |
| 11 | 7 Fun Lessons I learnt Last Month | 35m 5s | LGmWZLfnMv4 |
| 12 | Why Are So Many Men Lonely? | 21m 57s | U-rBK560cLE |
| 13 | 9 Life-Changing Lessons I Learned This Month | 18m 35s | SizjR8CcyP4 |
| 14 | 37 Pages That Changed My Thinking Forever | 11m 44s | yba6wFdI5aI |
| 15 | I Found The BOOK That SAVED Me From BRAINROT | 8m 38s | ulyX4HTWISA |
| 16 | What Happens When You Read at 5AM for a Week? | 17m 52s | pe-ApiTZrUc |
| 17 | Why Jealousy Might Be Your Hidden Superpower! | 4m 42s | a4AoVCPQvbk |
| 18 | How Reading Transformed My Life (Mind Unlocked) | 8m 13s | i1J5uZ0cwwg |
| 19 | How to Optimize Your 20s for Maximum Growth | 3m 16s | rOY13NzT-cU |
| 20 | I Was Reading Books WRONG for 2 Years | 8m 25s | Y8p5xpHLFqY |
| 21 | PhD Researcher's PROVEN Method to Solve Any Problem | 9m 5s | xfpebxTN3KA |
| 22 | I Finally Found the Blueprint to GENIUS | 7m 2s | X95iivX8Szg |
| 23 | I Forced Myself to Read Books for 3 Years | 7m 14s | Lqvlpn4nL7Y |
| 24 | I made Stoic Videos for 30 Days Straight | 7m 19s | bzZ7plDqxm0 |

## Steps
- [ ] Create `transcripts/` directory
- [ ] Write and run batch transcript download script (fetch all 24 via youtube_transcript_api)
- [ ] Fetch video metadata (publish dates) via yt-dlp for Jekyll naming
- [ ] Verify all 24 transcripts downloaded correctly
- [ ] Generate blog post for each transcript, following `.skills/blog-writing.md` voice
- [ ] Save as `_posts/YYYY-MM-DD-slug.md` with proper Jekyll front matter
- [ ] Final quality check on a few sample posts

## Verification
- All 24 transcript files in `transcripts/` are non-empty
- All 24 blog posts in `_posts/` have valid Jekyll front matter
- Blog posts match the voice/style guide (no tone killers, proper hooks, strong closings)
- `bundle exec jekyll build` succeeds with no errors
