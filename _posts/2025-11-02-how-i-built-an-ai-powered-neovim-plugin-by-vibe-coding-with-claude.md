---
layout: post
title: "I Built a Neovim Plugin in a Language I Don't Know. Here's the Story."
subtitle: "How I shipped a high-quality Lua plugin with 2,800+ lines of code without knowing Lua, by treating AI as a specialist I could direct."
date: 2025-11-02 12:00:00 +0530
---

I have a confession to make.

I don’t know Lua. I’ve never written it, I’ve never studied it, and I don’t even have the interpreter installed on my machine.

Yet, over a single weekend, I shipped a Neovim plugin with over 2,800 lines of Lua code, 89% test coverage, and a feature set which a hardcore minimalist neovim guy will appreciate. It’s called [hexwitch.nvim](https://github.com/parthbatra99/hexwitch.nvim), and it lets you generate your editor’s colorscheme from plain English.

This isn’t some 10x developer fairytale. It’s a story about a new way of building software I’m calling “vibe-driven development.” It’s about pairing years of programming fundamentals with an AI to build high-quality projects in languages you’ve never touched. It’s the story of how I used an AI as my product guy and my code monkey - Claude Code, and then had to step in as the adult in the room to make it safe for the public.

![My current neovim theme](/assets/images/theme-showcase.jpeg)

## Phase 1: The Idea Guy (and the AI)

It all started with the classic developer addiction: endlessly tweaking my colorscheme. I had a vague idea: “What if I could just *describe* a theme?” But the vision was fuzzy. So, before writing a single line of code, I opened a chat with Claude and treated it as my product guy.

We just spitballed. I threw out half-baked ideas, and it threw back refined concepts. We debated features, user flows, and what would make this thing actually cool. What started as a simple “generate a theme” command evolved into a full-fledged vision:

-   Generate themes from a prompt, obviously.
-   *Refine* existing themes with ease (the real magic).
-   Save and manage a whole library of your creations.
-   Browse themes with a proper UI (because who wants to remember filenames?).
-   Support for multiple AI providers, so you’re not locked in.

After a few hours, we had a rock-solid plan. The AI didn't just help me think; it helped me design a better product before a single line of code existed.

## Phase 2: The Code Monkey - Claude Code (Also the AI)

With a plan in hand, I switched hats. I was now the architect, and Claude was my specialist Lua contractor who only does exactly what they’re told.

I opened a new chat and started directing the work, module by module. The entire plugin was built in a series of 15-20 small, focused conversations.

**Me (The Architect):** “Okay, build me a storage module. It needs to save themes as JSON. Give me `save_theme` and `load_theme` functions. Oh, and sanitize the theme name before you write it to disk.”

**Claude (The Lua Specialist):** *spits out a perfect little Lua module with everything I asked for.*

I’d grab the code, run a quick test, and move on.

**Me:** “Nice. Now, let’s build a UI. Use Telescope to browse the themes we just saved. Read the JSON files and show them in a list.”

This loop was ridiculously fast. We built the AI provider module, the theme applier, the command registration—each piece in its own little sandbox. I didn’t need to know Lua syntax; I just needed to know how to structure a program and delegate.

## Phase 3: The Adult in the Room (Me)

After a weekend of this, I had a pile of working modules. I stitched them together, debugged the flow, and… it worked. The magic moment of generating a theme from a prompt was real. I had a functional prototype.

<video src="/assets/images/demo-vid.mp4" controls style="max-width: 100%; height: auto; border-radius: 8px; box-shadow: 0 4px 6px rgba(0, 0, 0, 0.1);">
  <p>Your browser doesn't support HTML video. Here's a <a href="/assets/images/demo-vid.mp4">link to the video</a> instead.</p>
</video>
*It’s alive! A live demo of generating a theme from scratch.*

But here’s the catch: a functional prototype is **not** a secure product. This is where the AI’s job ended and my job as an experienced engineer began.

I put the plugin through a rigorous security audit, and what I found was a glorious, functional, and deeply insecure mess. The AI-generated code was riddled with the exact kind of vulnerabilities you’d expect from a system that just pattern-matches without understanding the consequences. It was time to clean up the mess.

Here’s a summary of the critical fixes I had to implement myself, line by line:

1.  **Command Injection:** The AI was building system calls with simple string concatenation. A malicious theme name could have run any command on my machine. I ripped it out and replaced it with parameterized calls.
2.  **Path Traversal:** The AI didn’t sanitize theme names properly, leaving the front door open for an attacker to use `../../..` to read or write files anywhere on my system. Fixed.
3.  **Malicious Theme Data:** The plugin blindly trusted the theme data from the AI. A malformed theme could have crashed the editor or worse. I added a strict validation layer to sanitize the data before applying it.
4.  **API Key Leakage:** The AI was happily logging my full API key in debug messages. I scrubbed all the logs to make sure no secrets ever saw the light of day.

To prove the fixes were solid, I built a security test suite from scratch. The difference was night and day.

### Security Posture: Before vs. After

| Issue                | AI-Generated Code (The Intern) | My Hardening (The Senior Dev) | Status      |
|----------------------|--------------------------------|-------------------------------|-------------|
| Command Injection    | ❌ Wide Open                   | ✅ Locked Down                 | **Fixed**   |
| Path Traversal       | ❌ Vulnerable                  | ✅ Protected                   | **Fixed**   |
| Theme Validation     | ❌ YOLO                        | ✅ Comprehensive               | **Added**   |
| API Key Exposure     | ❌ Leaking Secrets             | ✅ Sanitized                   | **Fixed**   |
| Security Tests       | ❌ 0%                          | ✅ 100% Coverage               | **Added**   |

Only after this manual, expert-led hardening was I confident enough to post `hexwitch.nvim` on Reddit and not get roasted.

## The Result: Meet `hexwitch.nvim`

This whole process—AI for vision, AI for code, human for quality—produced a plugin I’m genuinely proud of.

-   **Generate Themes with Plain English:** `:Hexwitch "a moody, high-contrast sci-fi theme with neon green accents"`
-   **Iterate and Refine on the Fly:** `:Hexwitch refine`
-   **Browse Your Creations:** A slick, built-in [Telescope](https://github.com/nvim-telescope/telescope.nvim) UI to browse, search, and apply your saved themes.
-   **Full History with Undo/Redo:** Because creativity needs an escape hatch.
-   **Bring Your Own AI:** Supports OpenAI, OpenRouter, and custom endpoints out of the box.

![The built-in Telescope UI for browsing your theme library.](/assets/images/saved-themes.jpeg)
![The refine window showing various tweaking configurations.](/assets/images/refine.jpeg)

It’s a robust tool, and you can install it today:

```lua
-- With lazy.nvim
{
  "parthbatra99/hexwitch.nvim",
  dependencies = {
    "nvim-lua/plenary.nvim",
    "nvim-telescope/telescope.nvim",
  },
  config = function()
    -- Don't forget to set your OPENAI_API_KEY or OPENROUTER_API_KEY!
    require("hexwitch").setup({
      ai_provider = "openrouter",
      model = "anthropic/claude-3-haiku",
    })
  end,
}
```

## The Scorecard

Because I'm a data scientist at heart, here's the final tally from my weekend experiment:

| Metric                      | Value                                  |
| --------------------------- | -------------------------------------- |
| Lines of Lua Written by Me  | 0                                      |
| Lines of Lua Code Generated | 2,847                                  |
| Test Coverage               | 89%                                    |
| Time Spent                  | ~48 hours                              |
| Sanity Remaining            | Questionable                           |
| My Personal Theme Count     | 47 (current favorite: "autumn rain in Tokyo") |

## My New Hot Take: AI is a Superpower for People Who Already Know Their Stuff

This experiment fundamentally changed how I see software development. It’s a two-part process:

1.  **AI-Accelerated Prototyping:** Use AI as a hyper-fast intern to turn your architectural vision into code, letting you skip the boring syntax-learning phase.
2.  **Expert-Led Hardening:** Apply your deep human expertise to the critical last 10%—security, performance, and reliability—to turn the prototype into a real product.

This is a superpower. It means your value as a developer isn’t just knowing a language; it’s your deep understanding of programming fundamentals that work everywhere. The AI handles the syntax; you handle the safety, quality, and taste.

### Your Turn

You have years of experience. What could you build this weekend if you could instantly get a functional-but-insecure v0.9 of any idea? Go try it. The future of development isn’t about replacing us; it’s about amplifying our expertise to ship better, safer products, faster than ever before.

---

*Check out the project on [GitHub](https://github.com/parthbatra99/hexwitch.nvim). The source code is completely open, and I'd love to see what themes you create!*