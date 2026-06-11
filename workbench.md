---
layout: workbench
title: Workbench
description: Active learning logs, side project builds, and professional highlights. Where theory hits the terminal and ideas get their hands dirty with code and data.
permalink: /workbench/
---

### openVAPI — Open-Source Voice AI Platform

**[2026-05-11]** Scaffolded the entire project in one commit. FastAPI + Next.js + Postgres + Redis. Assistants, phone numbers, call logs. 57 files, 3,261 lines. Architecture was deliberate from day one: one FastAPI process, asyncio Tasks for concurrency, no workers, no threads.

**[2026-05-14]** Voice pipeline lands. Pipecat-based with Twilio and Plivo telephony via plugin registry, Deepgram STT with custom echo suppression, ElevenLabs TTS, OpenAI/Groq LLM. First phone call connects. 69 files, 14,521 lines.

**[2026-05-18]** WebRTC pipeline for browser calls (SmallWebRTCTransport at 16kHz). Cost calculator, usage accumulator, enhanced provider flows.

**[2026-05-27]** "Wholesale improvements": webhooks with HMAC-SHA256 signing and exponential backoff, Vapi compatibility layer (existing Vapi clients change one URL), background call scheduler with orphan crash recovery, S3 storage, per-turn millisecond diagnostic metrics tracking VAD through TTFB through bot speaking end.

**[2026-05-28]** The evening of the recording desync. Bot audio packed with no silence gaps between turns. Mixed recordings had all bot turns at position 0. Three days of debugging PCM audio and sample rates. Fix: wall-clock offset tracking per chunk, then reconstruct the full-length track by placing each TTS burst at its real-time position. Also: webhook deduplication with Redis lease claims, pipeline race condition fix (dual-event gate for startup + client connection).

**[2026-06-08]** 3:35 AM commit. Realtime voice pipelines (OpenAI/Azure Realtime APIs, completely different pipeline topology where STT+LLM+TTS are one service). Google Vertex, Google TTS/STT, Sarvam STT for Indian languages, Cartesia TTS. XML function tag filter (four lines, saved every call from TTS reading HTML tags aloud). In-memory audio buffering, pipeline metrics aggregator, Deepgram interim-promotion fix, crash recovery with orphan cleanup, max-duration watchdog backstop.

**[2026-06-09]** Production hardening. Docker-compose fixes, Caddy routing, webhook retry logic, bug fixes.

**[2026-06-10]** Complete UI revamp. Dashboard, analytics, settings pages. 52 files changed. 4,600 lines of core pipeline code total.

> **Summary:** Self-hosted, open-source voice AI platform. BYOK across LLM/STT/TTS providers, realtime voice pipelines, telephony via Twilio/Plivo, Vapi-compatible REST API, echo suppression, recording with wall-clock sync, crash recovery, per-turn millisecond metrics. Docker-first deployment. Open-sourcing soon.
>
> `python · fastapi · pipecat · webrtc · docker · deepgram · openai · twilio · plivo`
>
> 🔨 Nearing Completion — [Read the full story](/blog/building-an-open-source-vapi-alternative/)

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

_Last Updated: June 11, 2026_
