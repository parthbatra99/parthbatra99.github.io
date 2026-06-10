# Blog Writing Skill: Parth Batra's Voice

A practical guide for drafting and reviewing posts for fromparth.blog. Based on analysis of 5 published posts covering technical deep-dives, data analysis, and DIY builds.

---

## Voice and Tone Checklist

### The Core Voice

Write like you're explaining something cool to a smart friend over drinks. Not like you're presenting at a conference.

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
- DO: "That's a cup of chai at a decent place."
- DO: "Diwali 2025 had a full year of Premium for Rs. 499"
- DO: The AI had a conversation with itself about the weather in Bangalore
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
2. Paragraphs are ≤4 sentences. One-sentence paragraphs are for deliberate emphasis — not laziness, not filler.
3. No consecutive same-word sentence starts. If two sentences in a row start with "The", rewrite one.
4. Use contractions naturally. "don't" not "do not". "it's" not "it is". "that's" not "that is".
5. Plain words always. "Help" not "facilitate". "Use" not "utilize". "Start" not "commence".
6. Specific numbers, not vague quantifiers. "100,000 minutes" not "a lot of listening". "Rs. 38 per person" not "very little money". "2,800 lines" not "a bunch of code".

### Humor Cadence Rule

Hit a humor beat every 2–3 paragraphs. Not every paragraph (exhausting), not less (the post loses warmth and reads like documentation). Three types — use at least two per post:
- **Situational/observational** — the absurdity of the situation is the joke. "It was funny for about 30 seconds. Then it was terrifying."
- **Hyperbolic comparison** — scale inversion or absurd equivalence. "It's not really open-source. It's a hostage situation."
- **Self-deprecation** — always pair with a competence signal immediately after. "I kept going anyway." / "I didn't care."

### Voice Self-Check

Read any paragraph aloud. Does it sound like you? If it sounds like it could come from any tech blog, rewrite it.

---

## Title Formula

### Structure Options (Pick One)

1. **"I [did impressive thing]. I [humble admission]."**
   - *Example:* "I Shipped a Neovim Plugin in Lua. I Don't Know Lua."
   - *Example:* "I Built a Voice AI Platform. 90% of It Is Plumbing."

2. **"I [did thing]. The [unexpected truth]."**
   - *Example:* "I Did the Math on My Spotify Obsession. I'm Spotify's Problem."
   - *Example:* "I Cloned a 20,000 Rupee Light Setup for Under 2,000"

3. **Question with wild implied answer**
   - *Example:* "What a Rubik's Cube and Car Wax Have to Do With My Keyboard Setup"
   - *Example:* "When Does Your Streaming Habit Actually Cost Spotify Money?"

4. **Numbers + contrast**
   - *Example:* "2,800 Lines of Lua, 89% Coverage, Zero Prior Experience"

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
   - "For three years running, my Spotify Wrapped has clocked in at over 100,000 minutes. That's more than two full months of non-stop audio — not a flex, more a confession."

5. **The Unexpected Percentage**
   - "Here's something nobody tells you about building voice AI systems: the 'AI' part is the easy 10%."

### Hook Checklist
- [ ] Opens with strong, specific claim
- [ ] Creates curiosity gap
- [ ] Establishes personal stakes
- [ ] Natural transition to body

---

## Body Structure by Post Type

### Architecture/Technical Posts (e.g., voice AI, neovim plugin)
1. **The Hook** — Why this matters, personal stake
2. **The Setup** — What you set out to build, constraints
3. **Phase-by-phase breakdown** — Week 1, Step 1, etc.
4. **The Disaster Section** — What went wrong (specific numbers, emotions, failed attempts)
5. **The Solution** — How you fixed it, with code/architecture
6. **Results** — Honest status of what shipped
7. **The Insight** — What this means beyond this project

### Analysis Posts (e.g., Spotify economics)
1. **The Hook** — Personal behavior sparking the question
2. **The Question** — Clear, specific hypothesis
3. **Data Presentation** — Tables, calculations, sources (gradual complexity: marginal → fully-loaded → sensitivity)
4. **The Model** — Apply to real scenarios/listener profiles
5. **The Insight** — What data reveals about behavior or strategy
6. **Sources** — Inline footnotes, not bibliography

### DIY/Build Posts (e.g., keyboard, ambilight)
1. **The Hook** — Absurd premise or cost comparison
2. **The Discovery** — How you found the project
3. **Step-by-step** — Images, setbacks, "I almost gave up" moments
4. **The Hack** — Unconventional solution (Rubik's cube lube, car wax)
5. **Results** — Before/after with sensory details
6. **The Lesson** — What random thing taught you

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

---

## Self-Evaluation Rubric

Rate your draft 1-5 on each criterion:

### Voice & Authenticity (out of 20)
| Criterion | 1 (Poor) | 3 (Okay) | 5 (Excellent) |
|---|---|---|---|
| Authentic voice | Could be anyone | Some personality | Unmistakably Parth |
| Self-deprecating humor | None/forced | Occasional | Natural, disarming |
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

**Total Score: ___ / 60**

**Below 35:** Major rewrite needed
**35-50:** Good draft — polish weak sections
**50-60:** Ready to publish — minor line-edits only

---

## AI Self-Evaluation Prompts

After drafting, ask:

1. **The Generic Test** — If I changed the author name to "Tech Blogger," would anyone notice?
2. **The So What Test** — Every technical section answers: Why does this matter?
3. **The Humor Check** — Is there one genuine smile moment?
4. **The Numbers Audit** — Replace every "a lot," "very," "fast," "slow" with specifics
5. **The Opening-Closing Swap** — Do they feel like the same post?
6. **The Honesty Check** — Did you include failures and uncertainty?

---

## Quick Reference

### Do
- Start sentences with "I"
- Use contractions (don't, can't, it's)
- Include specific numbers and dates
- Describe failures before successes
- Short-medium paragraphs (2-5 sentences)
- Use tables for comparisons
- End with insight, not summary

### Don't
- Generic advice ("Always remember to...")
- Buzzwords (leverage, synergy, disruptive)
- Excessive humility disclaimers
- Unexplained jargon
- Perfection narratives
- Corporate/LinkedIn voice
- Listicles without narrative
- "In conclusion..."

---

## Tags & Media

### Tagging Guide
Use 3-5 tags per post:
- Primary topic (neovim, voice-ai, diy)
- Tech stack (lua, webrtc, raspberry-pi)
- Content type (infrastructure, hardware, analysis)
- Optional: company/product if central

### Media Guidelines
- Hero image: `/assets/images/[name].png` (1200x630)
- Inline images: `/assets/images/[post]-[step].jpeg`
- Descriptive alt text (not just "image")
- Videos: MP4 with fallback link
- Audio: `<audio controls>` with m4a/mp3

---

*Remember: Your reader is smart and busy. Respect their intelligence, entertain them, teach them something new. That's the fromparth.blog promise.*