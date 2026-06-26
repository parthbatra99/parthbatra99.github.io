# Blog Writing Skill: Parth Batra's Voice

A practical guide for drafting and reviewing posts for fromparth.blog. The benchmark posts are "I Built a Voice AI in 30 Days. Its Hardest Bug Took Three." (a technical build journal) and "I Wrote 15 Postcards Nobody Asked For. They Weren't for My Friends." (a reflective personal essay). Everything below should pull a draft toward those two, across technical deep-dives, data analysis, DIY builds, and reflective essays.

The single biggest shift from earlier posts: the writing got more vulnerable and more personal. That's the spine now. Competence is the table stakes; what makes a post unmistakably Parth's is what he's willing to admit about himself on the page.

---

## Voice and Tone Checklist

### The Core Voice

Write like you're explaining something cool to a smart friend over drinks. Not like you're presenting at a conference.

**Vulnerability is the spine (read this first):** This is the trait that does the most work, and the one a generic tech blog can't fake. Risk something real on the page. Admit the thing you'd rather keep behind your competence. The post should leave the reader knowing something true about you that you didn't have to tell them.
- Identity honesty: "I wrote 15 postcards... They weren't for my friends. They were for the version of me I'm trying to become."
- Admit uncertainty out loud, mid-thought: "I'm still figuring out which is which." / "as far as I can tell" / "I default to yes because I haven't earned the right to say no yet."
- Emotional exposure without flinching, then no walk-back: "I felt proud. Not of the postcards. Of the version of me who chose to do it that way."
- In technical posts vulnerability shows up as the failure made specific: "this is the one that fixes it" on attempt 14 of 14, the 3:35 AM commit, "the QA department is me, my phone, and a 1 AM docker compose habit."
- DON'T: hint at a struggle and then resolve it in the same sentence so it costs nothing. If it was hard, sit in the hard part before you fix it.

**Confident but not arrogant:** You know your stuff but don't need to announce it.
- DO: "This is the workflow I used. Not a story, not a hot take - a methodology I think you can replicate if you have a few years of engineering behind you."
- DONT: "I've developed a proprietary methodology that will revolutionize your workflow."

**Self-deprecating without fishing for reassurance:**
- DO: "I did something I'm not entirely proud of: I grabbed a syringe and reached for the silicone lube I use on my Rubik's cubes."
- DONT: "I know this might not be perfect, but please be kind."

**Accessible technical depth:** No gatekeeping, no oversimplifying.
- Explain VAD, STT, AEC by showing why they matter, not by defining acronyms.
- DO: "The rpi_ws281x library uses the Pi's PWM hardware (via DMA) to drive the data line, which sidesteps the OS jitter problem entirely."
- DONT: "As we all know, PWM stands for Pulse Width Modulation."

**Honest emotions on the page:**
- DO: "It was funny for about 30 seconds. Then it was terrifying."
- DO: "I was crouched over my sink for longer than I want to admit, and somewhere around keycap 70 I had a very clear thought: I could just buy a new keyboard. I kept going anyway."
- DONT: "I encountered some challenges during the process."

**Delhi-Indian cultural seasoning (not forced, just natural):**
- DO: "If you know any emotionally unavailable mid-20s Indian men, you know that's the highest compliment physically possible. We are a nonchalant final boss. 'Love you bro' from us is a Nobel acceptance speech."
- DO: "That's a cup of chai at a decent place."
- DO: "Diwali 2025 had a full year of Premium for Rs. 499"
- DO: The AI had a conversation with itself about the weather in Bangalore
- DO: Hindi voicemail patterns ("beep ke baad", "sandesh chhodiye") treated as a normal part of the problem, not an exotic aside
- DO: Rupee pricing (Rs.), Indian market context
- DO: Casual references to local food, prices, and context
- DONT: "Namaste, fellow desis!" or forced Hindi
- Keep it organic. If the post is about something global (Neovim, voice AI), the Indian context comes from you, not from signaling.

### Tone Killers (Zero Tolerance)

| Tone Killer | Why It's Bad | Replace With |
|---|---|---|
| "In today's world..." | Filler. Says nothing. | Just state the thing |
| "It goes without saying..." | Then don't say it | Cut the line |
| "Let's dive in" | Listicle energy | Nothing. Start. |
| Corporate jargon (leverage, utilize, facilitate, streamline) | Press release voice | Plain words: use, start, help, simplify |
| "I'd be happy to..." | Chatbot voice | Just do it |
| "Please don't hesitate..." | CYA corporate speak | Remove entirely |
| Em dashes or en dashes | Punctuation crutch | Use commas, periods, or line breaks |

### Sentence-Level Voice Rules

1. Vary sentence length. Short ones hit harder. Longer ones build rhythm.
2. Paragraphs are ≤4 sentences. One-sentence paragraphs are for deliberate emphasis, not laziness, not filler.
3. No consecutive same-word sentence starts. If two sentences in a row start with "The", rewrite one.
4. Use contractions naturally. "don't" not "do not". "it's" not "it is". "that's" not "that is".
5. Plain words always. "Help" not "facilitate". "Use" not "utilize". "Start" not "commence".
6. Specific numbers, not vague quantifiers. "100,000 minutes" not "a lot of listening". "Rs. 38 per person" not "very little money". "2,800 lines" not "a bunch of code".
7. Single-word italics for emphasis, used sparingly. Italicize the one word the sentence turns on, not phrases: "I felt *proud*." / "arguing *for* my betterment." / "Perfectionism says *it's not ready*." If more than one word per paragraph is italicized, you're leaning on it too hard.
8. No em dashes or en dashes anywhere in prose. Both benchmarks honor this absolutely. Use commas, periods, or line breaks. (The structural dashes in this skill doc are doc scaffolding, not blog voice, don't copy them into a post.)

### Structure & Break Conventions
- `## Heading` for real sections.
- `***` (horizontal rule) for a *tonal pivot* inside a reflective piece, the moment the essay turns from observation to confession, or from the pattern to the caveat. The last-5% post uses it exactly twice, at its two hardest turns. It's a held breath, not a section divider. Use it only when the temperature of the writing changes.
- `---` closes a post above the small italic sign-off line ("*The commit messages are vague but the code tells the real story.*").

### Humor Cadence Rule (conditional on post type)

Humor is the warmth driver for **built / DIY / analysis** posts. For those, hit a humor beat every 2-3 paragraphs. Not every paragraph (exhausting), not less (the post loses warmth and reads like documentation). Three types, use at least two per post:
- **Situational/observational**: the absurdity of the situation is the joke. "It was funny for about 30 seconds. Then it was terrifying."
- **Hyperbolic comparison**: scale inversion or absurd equivalence. "It's not really open-source. It's a hostage situation." / "The last retry fires half an hour later, which in webhook time is a formal apology letter."
- **Self-deprecation**: always pair with a competence signal immediately after. "I kept going anyway." / "I didn't care." / "The QA department is me, my phone, and a 1 AM docker compose habit."

**For reflective (`kind: theory`) posts, do NOT force this cadence.** Vulnerability and honesty carry the warmth instead. The last-5% essay lands exactly one joke (the "Love you bro" / Nobel line) in the whole piece and is stronger for it. A reflective post can go many paragraphs with no joke at all if the honesty is doing the work. One well-placed beat early buys goodwill; after that, get out of the way and be sincere. Forcing jokes into a reflective piece breaks the spell.

### Imagery & Metaphor Density Rule

A defining feature of the new voice: abstract mechanisms become physical scenes. In built/analysis posts, land one fresh, concrete image roughly every 2-3 paragraphs. The image must be specific to *this* subject, invented for the thing you're describing, never pulled off the shelf.

Mined from the voice AI post (study these):
- "The last retry fires half an hour later, which in webhook time is a formal apology letter."
- "Leave it longer and every reply feels like a long-distance call from 1991."
- A dropped transcript is "a waiter who takes your order, reads it back to you, and bins it on the way to the kitchen."
- The echo loop is "a robot arguing with its own echo."
- A double-fired webhook announces the call ended twice, "which is one more ending than most calls have."
- Mis-timed bot audio "lives in the past": "two people in a conversation where one of them lives in the past."

How to build one: name the abstract failure, then ask "what would this be if a human did it?" Answer in one concrete sentence and stop. Don't explain the metaphor after landing it.

**Banned:** dead/generic metaphors that fit anything, "game-changer", "Swiss-army-knife", "the secret sauce", "moving the needle", "a different beast". If the image would survive a find-and-replace of your topic with any other topic, it's not specific enough. Cut it.

### Voice Self-Check

Read any paragraph aloud. Does it sound like you? If it sounds like it could come from any tech blog, rewrite it.

---

## Title Formula

### Structure Options (Pick One)

1. **"I [did impressive thing]. I [humble admission]."**
   - *Example:* "I Shipped a Neovim Plugin in Lua. I Don't Know Lua."
   - *Example:* "I Built a Voice AI Platform. 90% of It Is Plumbing."

2. **"I [did thing in a timeframe]. The [unexpected truth / hardest part]."**
   - *Example:* "I Built a Voice AI in 30 Days. Its Hardest Bug Took Three."
   - *Example:* "I Did the Math on My Spotify Obsession. I'm Spotify's Problem."
   - *Example:* "I Cloned a 20,000 Rupee Light Setup for Under 2,000"

3. **Question with wild implied answer**
   - *Example:* "What a Rubik's Cube and Car Wax Have to Do With My Keyboard Setup"
   - *Example:* "When Does Your Streaming Habit Actually Cost Spotify Money?"

4. **Numbers + contrast**
   - *Example:* "2,800 Lines of Lua, 89% Coverage, Zero Prior Experience"

5. **"I [did thing nobody asked for]. [The confession that subverts why]."** (reflective)
   - *Example:* "I Wrote 15 Postcards Nobody Asked For. They Weren't for My Friends."
   - The first half is the odd, concrete act. The second half admits the real, more vulnerable reason.

### Title Checklist
- [ ] First-person perspective ("I" not "How to")
- [ ] Specific, not abstract ("20,000 Rupee Light Setup" not "Expensive Tech")
- [ ] Implies surprising insight
- [ ] Under 70 characters ideally
- [ ] Subtitle adds context without repeating

### Subtitle Rules
- [ ] Specific context the title doesn't give
- [ ] Mention methodology, timeframe, or scope
- [ ] Tone matches title
- *Example:* Title: "I Shipped a Neovim Plugin in Lua. I Don't Know Lua." Subtitle: "The actual workflow: use AI as the specialist, yourself as the architect."

---

## Opening Hook (First 3 Paragraphs)

### Hook Types (Pick One)

1. **The Contradiction**
   - "I don't know Lua. I've never written it... Over a single weekend, I shipped a Neovim plugin with over 2,800 lines of Lua code."

2. **The Absurd Premise**
   - "I have a Rubik's cube in my desk drawer and a bottle of ceramic car wax under my sink. Neither should have anything to do with keyboards."

3. **The Staggering Fact**
   - "Philips wants 20,000 rupees for the Hue Play Gradient Lightstrip. Twenty. Thousand. For LEDs."

4. **The Confession**
   - "For three years running, my Spotify Wrapped has clocked in at over 100,000 minutes. That's more than two full months of non-stop audio, not a flex, more a confession."

5. **The Unexpected Percentage**
   - "Here's something nobody tells you about building voice AI systems: the 'AI' part is the easy 10%."

6. **The Vulnerable Confession-Scene** (reflective posts)
   - Open inside a specific, slightly exposing real moment, not a thesis. "I wrote 15 postcards from the highest post office in the world. It's in Hikkim, Spiti, somewhere around 15000 feet. I spent a full day writing to the people close to me. By hand, each one different."
   - Then surface the quiet, honest observation underneath it: "The extra effort wasn't what earned the reactions. They would have come anyway. But here's the part I didn't expect."
   - Let the scene do the work. No abstract framing before the reader is in the moment with you.

### Hook Checklist
- [ ] Opens with strong, specific claim
- [ ] Creates curiosity gap
- [ ] Establishes personal stakes
- [ ] Natural transition to body

---

## Body Structure by Post Type

### Architecture/Technical Posts (e.g., voice AI, neovim plugin)
1. **The Hook**: Why this matters, personal stake
2. **The Setup**: What you set out to build, constraints
3. **Phase-by-phase breakdown**: Week 1, Step 1, etc.
4. **The Disaster Section**: What went wrong (specific numbers, emotions, failed attempts)
5. **The Solution**: How you fixed it, with code/architecture
6. **Results**: Honest status of what shipped
7. **The Insight**: What this means beyond this project

### Analysis Posts (e.g., Spotify economics)
1. **The Hook**: Personal behavior sparking the question
2. **The Question**: Clear, specific hypothesis
3. **Data Presentation**: Tables, calculations, sources (gradual complexity: marginal → fully-loaded → sensitivity)
4. **The Model**: Apply to real scenarios/listener profiles
5. **The Insight**: What data reveals about behavior or strategy
6. **Sources**: Inline footnotes, not bibliography

### DIY/Build Posts (e.g., keyboard, ambilight)
1. **The Hook**: Absurd premise or cost comparison
2. **The Discovery**: How you found the project
3. **Step-by-step**: Images, setbacks, "I almost gave up" moments
4. **The Hack**: Unconventional solution (Rubik's cube lube, car wax)
5. **Results**: Before/after with sensory details
6. **The Lesson**: What random thing taught you

### Reflective / Personal Essay Posts (`kind: theory`, e.g. the last 5%)

No code, no tables, no spec sheet. The engine is honesty, not information. Structure derived from the last-5% post:

1. **The concrete moment**: open inside one specific, slightly vulnerable real scene (15 postcards in Hikkim). Not an abstract claim. The reader should be standing somewhere before they're being told anything.
2. **The pattern**: "I've started noticing..." Name the recurring thing, then ground it in two or three small, real, mildly unflattering-to-you examples (the dead-deal travel agent you almost ghosted, the homestay reviews nobody connects to you). Concrete every time; never a hypothetical.
3. **What I think is actually happening**: the interpretive turn. Reframe the mundane act as identity-level ("Each one casts a vote... A hundred is a different person"). Hedge honestly: "as far as I can tell", "Here's the thing I keep turning over."
4. **The honest caveat**: distinguish the idea from its evil twin so it can't be misread (the last 5% is *not* perfectionism: "Perfectionism says *it's not ready*. The last 5% says *it's ready, I did it right, next*."). Admit what you still haven't figured out.
5. **The reframe ending**: often borrowed wisdom recast against its old meaning ("*How you do anything is how you do everything.* It used to sound like a threat. Now it sounds like the most generous thing I've ever read."). Tie back to the opening moment so the postcard from paragraph one closes the loop.

Use `***` for the two tonal pivots: into the caveat, and into the closing. See the Structure & Break Conventions above.

### Body Writing Checklist
- [ ] Clear section transitions
- [ ] Every technical detail answers "so what?"
- [ ] Tables for comparisons (before/after, cost, features)
- [ ] Specific numbers, not "a lot" or "very fast"
- [ ] Honest emotions (frustration, surprise, terror, pride)
- [ ] Anticipate reader questions
- [ ] Code blocks max 200 lines, well-commented
- [ ] Images at key moments (before disaster, after fix, final result)
- [ ] Italicized thoughts: *"I could just buy a new keyboard"*

---

## Closing Insight

### Rules
- [ ] Never summarize what reader just read
- [ ] One sharp insight that reframes the whole post
- [ ] Personal reflection, not advice to reader
- [ ] Thematic tie to opening
- [ ] CTA only if organic

### Examples of Strong Closings
- "Years of shipping things that broke at inconvenient times had taught me something more transferable than syntax."
- "Sometimes the best tech isn't the most expensive. It's the one you build yourself, learn from, and can actually fix when it breaks at 2am."
- (Built, effort-vs-impact reframe) "What still surprises me is that effort and impact refuse to correlate. My best code is four lines that strip XML tags from a voice stream. The bug that took the longest was a recording mixer that didn't know what time it was."
- (Reflective, borrowed-wisdom recast) "*How you do anything is how you do everything.* It used to sound like a threat. Now it sounds like the most generous thing I've ever read." Take a line the reader has heard before and flip what it means to you. The reframe is the insight.

---

## Self-Evaluation Rubric

Rate your draft 1-5 on each criterion:

### Voice & Authenticity (out of 30)
| Criterion | 1 (Poor) | 3 (Okay) | 5 (Excellent) |
|---|---|---|---|
| **Vulnerability / exposure** | Stays safe behind competence | Admits a struggle | Risks something real; reader learns something true about you |
| Authentic voice | Could be anyone | Some personality | Unmistakably Parth |
| Self-deprecating humor (built/DIY/analysis) | None/forced | Occasional | Natural, disarming, *or deliberately sparse on a reflective post* |
| Fresh imagery / metaphor | Generic or none | One or two | A specific, invented image every 2-3 paragraphs |
| Technical accessibility | Too shallow/deep | Mostly accessible | Deep but inviting |
| Cultural references | None/awkward | Some | Natural seasoning |

### Structure & Flow (out of 20)
| Criterion | 1 (Poor) | 3 (Okay) | 5 (Excellent) |
|---|---|---|---|
| Opening hook | Boring/generic | Interesting | Can't stop reading |
| Section transitions | Abrupt/missing | Functional | Invisible/seamless |
| Pacing | Rushed or drags | Decent | Good rhythm |
| Closing insight | Summary/weak | Okay | Reframes everything |

### Technical Quality (out of 20)
| Criterion | 1 (Poor) | 3 (Okay) | 5 (Excellent) |
|---|---|---|---|
| Specific numbers/data | Vague/absent | Some specifics | Rich with specifics |
| Table formatting | Messy/missing | Basic | Clear, informative |
| Code/examples | None/broken | Works | Elegant, well-explained |
| Source credibility | Unsourced/weak | Some sources | Solid, inline footnotes |

**Total Score: ___ / 70**

**Below 40:** Major rewrite needed
**40-58:** Good draft, polish weak sections
**58-70:** Ready to publish, minor line-edits only

**Reflective (`kind: theory`) posts:** the Technical Quality table mostly won't apply (no tables, code, or sources). Score Voice & Authenticity and Structure & Flow normally, and replace Technical Quality with a single judgment out of 20: *did the essay earn its reframe, or just assert it?* A reflective post lives or dies on whether the closing insight feels paid for by the honesty that came before it.

---

## AI Self-Evaluation Prompts

After drafting, ask:

1. **The Generic Test**: If I changed the author name to "Tech Blogger," would anyone notice?
2. **The Exposure Test**: Did I risk something real, or stay safe behind competence? Find the one sentence the reader will remember about *me*, not the project. If there isn't one, the post isn't done.
3. **The So What Test**: Every technical section answers: Why does this matter?
4. **The Humor Check**: built/DIY/analysis: one genuine smile moment? Reflective: is the honesty carrying the warmth without a forced joke?
5. **The Imagery Audit**: Find every metaphor. Is each one invented for this subject, or would it survive find-and-replacing my topic? Cut the survivors.
6. **The Numbers Audit**: Replace every "a lot," "very," "fast," "slow" with specifics
7. **The Opening-Closing Swap**: Do they feel like the same post? Does the closing tie back to the opening scene?
8. **The Honesty Check**: Did you include failures and uncertainty, and admit something at the identity level, not just "this bug was hard"?

---

## Quick Reference

### Do
- Risk something real about yourself, vulnerability is the spine
- Start sentences with "I"
- Use contractions (don't, can't, it's)
- Include specific numbers and dates
- Describe failures before successes; sit in the hard part before the fix
- Turn abstract mechanisms into concrete, invented images
- Admit uncertainty out loud ("I'm still figuring out which is which")
- Single-word italics for the word a sentence turns on
- Short-medium paragraphs (2-5 sentences)
- Use tables for comparisons (built/analysis)
- End with insight, not summary

### Don't
- Stay safe behind competence, that's the generic-blog default
- Generic advice ("Always remember to...")
- Off-the-shelf metaphors ("game-changer", "Swiss-army-knife", "a different beast")
- Force jokes into a reflective post
- Resolve a struggle in the same sentence you raise it
- Buzzwords (leverage, synergy, disruptive)
- Excessive humility disclaimers
- Unexplained jargon
- Perfection narratives
- Em dashes or en dashes
- Corporate/LinkedIn voice
- Listicles without narrative
- "In conclusion..."

---

## Frontmatter, Tags & Media

### Frontmatter Fields
```yaml
layout: post
kind: built          # the post type, drives voice & structure (see below)
title: "..."         # follow the Title Formula
subtitle: "..."      # specific context the title doesn't give
date: YYYY-MM-DD
hero_art: /assets/images/name.png   # optional hero image
recommended: true                   # optional: feature on the homepage
recommended_order: 1                # optional: ordering among recommended
tags:
  - ...
```

**The `kind:` field** sets which body structure and voice rules apply:
- `built`: technical build journals (voice AI post). Humor + imagery on, full disaster section.
- `theory`: reflective / personal essays (last 5%). Vulnerability carries the warmth, humor sparse, no code/tables.
- Use the existing analysis/DIY structures even where the `kind` tag differs; match the structure to the actual content.

### Tagging Guide
Tags are **topic-only** and rendered as `#tag` chips on the blog list and post pages. Content *type* is already carried by `kind:` — never duplicate it in tags. Use a **controlled vocabulary**; do not invent new tags or one-off specifics (no `neovim`, `spotify`, `spiti`, `vapi` — fold them into the closest tag below).

Tags carry the blog's **playful voice**, not dry topic labels. Use **2–4 tags per post**, drawn only from these 12:

| tag | covers |
|---|---|
| `note-to-self` | growth, identity, mental models, self-improvement |
| `just-a-thought` | philosophy, stoicism, free will, meaning, critical thinking |
| `brain-glitch` | psychology, cognitive biases, how the brain works |
| `get-shit-done` | productivity, focus, time, output |
| `tiny-reps` | habits, routines, behavior change |
| `book-brain` | book-driven posts |
| `bio-hacking` | health, fitness, body, energy |
| `the-day-job` | career, work, money, skills |
| `made-this-up` | creativity, making, constraints |
| `nomading` | travel, trips |
| `ai & tech` | software, hardware, DIY, AI, any build (quoted in YAML for the `&`) |
| `i-did-the-math` | quantified / "did the math" posts |

Adding a 13th tag is a deliberate taxonomy change — update this list, then backfill existing posts. Keep the voice consistent (witty, lowercase, kebab-case).

### Media Guidelines
- Hero image: `/assets/images/[name].png` (1200x630)
- Inline images: `/assets/images/[post]-[step].jpeg`
- Descriptive alt text (not just "image")
- Videos: MP4 with fallback link
- Audio: `<audio controls>` with m4a/mp3

---

*Remember: Your reader is smart and busy. Respect their intelligence, entertain them, teach them something new, and tell them something true about yourself they didn't have to be told. That last part is what they'll remember. That's the fromparth.blog promise.*