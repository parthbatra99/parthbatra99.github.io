---
layout: workbench
title: Workbench
description: Active learning logs, side project builds, and professional highlights. Where theory hits the terminal and ideas get their hands dirty with code and data.
permalink: /workbench/
---

### hexwitch.nvim — AI Colorscheme Generator

**[2025-11-01]** Had a vague idea while tweaking my Neovim theme for the 400th time: *"What if I could just describe a vibe and get a colorscheme?"* Opened a chat with Claude and started spitballing.

**[2025-11-02]** Shipped it. 2,800 lines of Lua — a language I'd never written — in a single weekend. Claude was the product guy and the code monkey; I was the adult who caught command injection, path traversal, and API key leakage before they went public.

> **Summary:** A Neovim plugin that generates colorschemes from plain English prompts. Supports multiple AI providers, Telescope UI for browsing your library, and a full undo/redo history. Vibe-driven development at its finest.
>
> `lua · neovim · telescope · openai/openrouter`
>
> ✅ Shipped — [Read the full story](/blog/how-i-built-an-ai-powered-neovim-plugin-by-vibe-coding-with-claude/) · [GitHub](https://github.com/parthbatra99/hexwitch.nvim)

---

### DIY Ambilight — Real-time TV Backlight Sync

**[2026-03-15]** Saw the Philips Hue Play Gradient Lightstrip. ₹20,000 for colored LEDs behind a TV. Absolutely not.

**[2026-03-22]** Parts arrived. HDMI splitter, USB capture card, WS2812B strip, Raspberry Pi Zero 2W. Total out of pocket: **₹2,100**. Less than a tenth of the commercial price.

**[2026-04-05]** First light. Colors are roughly right but the latency is brutal — nearly 500ms. The TV shows a sunset and the wall behind it is still rendering the previous scene.

**[2026-04-20]** Fixed the latency. Dropped from 500ms to under 50ms. The trick was sampling screen regions at 10fps instead of processing every frame, plus a ring buffer for color smoothing. Your brain genuinely can't tell the difference.

**[2026-05-01]** Spent the weekend on power injection. WS2812B LEDs at full white draw ~60mA *each* — 180 LEDs means 10.8A. Without injection points every meter, the far end of the strip was a sad, dim orange. Fixed. Now uniform brightness edge to edge.

**[2026-05-10]** Signal integrity nightmare solved. Disabled the Pi's audio output (it competes for PWM hardware) and the random color flickers disappeared. Added gamma correction for color accuracy. Also clamped brightness to 80% — not for power, but because at 100% the color reproduction degrades and the adhesive backing starts peeling.

> **Summary:** A homemade bias lighting system that reads TV content in real-time and syncs matching colors to a LED strip on the back. ~200 lines of Python, entirely open hardware, and the whole thing costs less than a decent dinner.
>
> `python · opencv · raspberry-pi · ws2812b · gpio`
>
> 🔨 In Progress — Blog post coming soon

---

### Open-Source Voice AI Platform — A Vapi Alternative

**[2026-04-01]** Started building a self-hosted voice AI platform at work. The motivation was simple: Vapi and Retell are proprietary black boxes. We needed something we could own, modify, and deploy on our own infrastructure.

**[2026-04-15]** Two weeks in. The WebRTC bridge is working — bidirectional audio streaming, ICE candidate handling, the works. The first time I heard my own voice loop back through the system was genuinely unsettling.

**[2026-05-01]** STT→LLM→TTS pipeline is functional but the latency is a disaster. Streaming tokens from the LLM helps, but TTS needs complete sentences. Built a sentence buffer that accumulates tokens until it hits a sentence boundary, then flushes to TTS. The AI's first sentence reaches the user while the LLM is still generating the second one.

**[2026-05-15]** Spent a full week on **echo detection**. When the AI speaks, its voice comes out of the user's speaker, bounces into the mic, and the STT transcribes it. The AI ends up having a conversation with itself. Implemented AEC combined with a playback state tracker that tells the pipeline exactly when AI audio is being played.

**[2026-05-25]** Barge-in support. Allowing users to interrupt the AI mid-sentence. The timing window is brutal — too sensitive and ambient noise cuts off the AI mid-word, too slow and the user has already repeated themselves. Landed on a two-signal confirmation: VAD *and* echo cancellation must both agree the user is speaking.

**[2026-06-01]** Fallback provider chains. When Deepgram goes down mid-call, transparently switch to Whisper. When OpenAI is slow, try Anthropic. Built a health monitor that tracks provider latency and error rates in real-time. The switch is invisible to the user.

**[2026-06-05]** The WebSocket situation is... a lot. Each active call maintains 4-5 concurrent WebSocket connections. Wrote a ConnectionManager that handles heartbeat timeouts, message ordering, and session isolation. With 50 concurrent calls, that's 250 connections. It's the single most valuable piece of infrastructure in the entire stack.

**[2026-06-08]** User unmute frames. When a user unmutes, the pipeline receives stale buffered audio. Implemented a frame sequence counter — on unmute, discard any frame with a sequence number lower than the current. Clean sync, no hallucinated transcriptions.

**[2026-06-10]** Docker-first packaging done. `docker compose up` and the entire stack is running — media server, orchestration API, workflow builder, Redis, reverse proxy. Open `localhost:3010`, describe your use case, and you're talking to your first voice bot.

> **Summary:** A self-hosted, open-source voice AI platform. BYOK across LLM/STT/TTS providers, visual workflow builder, real-time telephony, MCP-native tool calling, and Docker-first deployment. 90% plumbing, 10% intelligence. Open-sourcing soon.
>
> `python · fastapi · webrtc · docker · websockets · twilio · openai · deepgram`
>
> 🔨 Nearing Completion — [Follow on GitHub](https://github.com/dograh-hq/dograh)

---

_Last Updated: June 10, 2026_
