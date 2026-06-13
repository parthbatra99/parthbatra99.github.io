---
layout: post
title: "What Actually Happens in the Second After You Say Hello to an AI"
subtitle: "Telephony, WebRTC, voice detection, transcription. A month building it from scratch, and where that second actually goes."
date: 2026-05-24
hero_art: /assets/images/voice-ai.png
tags:
  - ai
  - software
  - open-source
  - vapi
---

You call a number, an AI picks up, you say "hello," and it says "hello" back. Feels instant. Feels simple. It is neither.

In the second after you speak, your voice leaves your phone, crosses a telephony network that still speaks a protocol older than the web, lands on a server that has to decide you're actually talking and not just breathing, gets transcribed into text, gets sent to a large language model that thinks up a reply, gets turned back into a human-sounding voice, and gets pushed back down the same line to your ear. If any one of those steps takes too long, the AI talks over you, or sits in dead silence, or answers a question you didn't ask. All of it has to happen in under a second, every turn, on every call, forever.

Here's the part nobody tells you: the "AI" in that chain is the easy 10%. The model is a single API call. The other 90% is plumbing. It's the WebSocket that times out silently at 3am. It's a recording bug where the bot's audio packs itself tight with no silence between turns, so the saved call sounds like the AI is talking over itself. It's an LLM that leaks `<function>call_api()</function>` into its output, and the voice engine reads it aloud as "less than function call api greater than." It's a race condition that drops the very first thing the AI says on every other call.

I spent a month building openVAPI, an open-source, self-hosted alternative to Vapi and Retell. About 30 days. Around 4,600 lines of core pipeline code. One very long 3:35 AM commit. And I wrote every line of it.

This is the engineering journal. The wins, the disasters, and what the git log actually says.

### The Anatomy of That Second

Before the war stories, here's where the second actually goes. These aren't marketing numbers. The first row is a value I chose myself, the rest are typical figures for the providers in my stack, and later you'll meet the `TurnMetrics` dataclass that stamps every one of these stages on every real turn.

| Stage | Typical time | Where the number comes from |
| :--- | :--- | :--- |
| Confirming you've actually stopped talking | 800 ms | Configured: Silero VAD `stop_secs=0.8` |
| Final transcript from STT | 100-300 ms | Typical for Deepgram streaming |
| First token from the LLM | 200-400 ms | Typical for Groq and OpenAI |
| First audio byte from TTS | 75-150 ms | Typical for ElevenLabs Flash |
| Audio back down the line | 50-100 ms | 20 ms chunks plus the carrier network |

Add it up and the full path from your last syllable runs somewhere between 1.2 and 1.7 seconds. The sub-second figure everyone quotes starts at row two, after the silence check. Which is fair, because that 800 ms is not the AI being slow. It's the pipeline being polite.

Cut the silence window shorter and the bot interrupts you every time you pause to think. Leave it longer and every reply feels like a long-distance call from 1991. The single biggest lever in voice AI latency has nothing to do with the AI. It's deciding how long a human silence has to last before it counts as a turn.

### The Setup

On May 11, 2026, I committed the entire scaffold in one shot: a FastAPI backend (Python's async web framework) with CRUD for assistants, phone numbers, and call logs. A Next.js UI with a dark theme, because I already knew what hours I'd be keeping. Postgres for durable storage, Redis for fast in-memory state, Docker to run it all. 57 files, 3,261 lines. The architecture was deliberate from day one: one process, no worker pool, no threads. Every incoming call rides on an asyncio Task. All IO is awaited. A semaphore caps concurrent calls at 50. You scale by running more pods.

Three days later, the voice pipeline landed. I built it on top of **Pipecat**, a Python framework for real-time voice AI from the folks at Daily. Pipecat handles the hard distributed-systems problems: moving audio around, passing it between processing stages as "frames," and managing whose turn it is to speak. What I built on top was the production layer Pipecat doesn't give you.

That layer is a tour of the modern voice stack. **Twilio and Plivo** for telephony (the actual phone carriers that own the numbers and ring the call). **Deepgram** for STT, speech-to-text, turning what the caller says into words on the wire. **ElevenLabs** for TTS, text-to-speech, turning the AI's reply back into a voice that sounds human. **OpenAI and Groq** as the LLM, the brain that decides what to say. I wired them together with a plugin registry for the carriers, a service factory, a pipeline builder, event handlers with per-turn millisecond timing, and cost calculation in a `pricing.toml`. Four vendors, four billing models, one TOML file to keep them all honest.

One detail that trips up everyone: phone audio is bad on purpose. The telephony pipeline runs at 8kHz mulaw, a low-fidelity, narrow-band format designed in an era when bandwidth was precious. It's why every phone call sounds slightly muffled. That commit was 69 files, 14,521 lines. The first phone call actually connected.

Around May 18, I added browser calls. For those I used **WebRTC**, the same peer-to-peer audio and video tech that powers Google Meet and Discord. Getting a server to speak WebRTC (browsers do it natively, servers don't) means **aiortc**, the Python library that implements the protocol, wrapped here by Pipecat's `SmallWebRTCTransport`. Browser audio comes in at a cleaner 16kHz instead of the phone's 8kHz, so the same pipeline now has to juggle two sample rates depending on where the call came from. I also built a cost calculator so I'd know exactly what each call cost, down to the token and the character. On the cheapest stack (Groq for the brain, Deepgram for the ears, ElevenLabs for the voice, Twilio for the line), a 3-minute call comes out to roughly $0.10. About 8 rupees. Less than the chai you'd drink while debugging it.

### 1 AM, `docker compose up`, Again

The git log for May 20 is telling. Between 01:13 and 02:04, there are 28 commits, all in under an hour. What was I actually doing? Trying to get a single outbound phone call to connect end to end.

Telephony providers do not agree on anything. The handshake itself is a little dance: the carrier answers the call, pings your server over the internet, you hand back a set of instructions that tells it to open a live audio socket, and then it streams the call's raw audio to you in real time. Twilio sends that audio as JSON with base64-encoded mulaw. Plivo uses a slightly different framing. A serializer has to abstract both so the rest of the pipeline just sees a uniform `InputAudioRawFrame` and `OutputAudioRawFrame` and never has to care which carrier is on the line. Getting that right took 14 attempts in 51 minutes.

That's what those 28 commits are: each attempt left a pair of snapshots. Not a clean, beautiful git history. One person at 1 AM, running `docker compose up` again and again, reading logs, fixing one framing issue at a time. Every run started with the same thought, *this is the one that fixes it*, and run 14 finally was.

### "wholesale improvements"

On May 27, I made my biggest single commit and titled it "wholesale improvements" because I genuinely couldn't think of a better name. 47 files, 1,913 insertions, 312 deletions. Here's what was in it:

**The webhook service.** When a call ends, you often need to tell some other server about it. That's a webhook, an HTTP call your system makes outward. Mine signs every payload with HMAC-SHA256 (so the receiver can prove it really came from me) and retries on failure with exponential backoff at [0, 5, 30, 300, 1800] seconds. The last retry fires half an hour later, which in webhook time is a formal apology letter. A reconciliation loop finds unsent webhooks on startup and fires them. Every attempt is logged with status code, response body, and error.

**The Vapi compatibility layer.** `vapi_compat.py` exposes a REST shape that matches Vapi's API exactly. Any tool already built against Vapi can point at openVAPI by changing one URL. That single decision probably removed more adoption friction than any feature I could build.

**The background scheduler with crash recovery.** An asyncio task that wakes every 60 seconds, dials any call that was queued for a future time, and cleans up orphans: if the server crashed mid-call, on restart it finds every call stuck in limbo, hangs it up through the carrier's API, flushes the half-finished transcript from Redis to Postgres, and returns the phone number to the pool.

**S3 storage, consolidated database migrations, and rewritten event handlers** with a `TurnMetrics` dataclass that times every stage of every turn: when speech was detected, when the transcript finalized, when the LLM started, when its first token arrived, when it finished, when the voice started speaking, and when it stopped. Every turn, every call, in milliseconds.

That's the thing about voice AI. The intelligence is an API call. The work is everything around it.

### The Disaster Section

Four bugs. Each one cost me days. Each one taught me something no tutorial covers.

**Bug 1: The recording desync (3 days)**

This was the hardest bug in the whole project. It took three days just to understand. Once the math finally clicked, the fix itself landed in a 40-minute burst of commits on the evening of May 28.

The symptom: saved call recordings were broken. The system records both sides of a call, the human and the AI, then mixes them into one audio file. But the bot's audio was packed tight with no silence between its turns. When the mixer combined the two tracks, all of the bot's turns landed at the very start. The recording sounded like [bot1, bot2, bot3... then user1... user2], two people in a conversation where one of them lives in the past.

The root cause was subtle. The processor capturing bot audio stored raw bytes with no timestamps. The mixer had no idea *when* each burst of speech actually happened, so it just concatenated them. The human's audio, meanwhile, spanned the real call timeline correctly, because its capture processor sat earlier in the pipeline and saw every frame. The bot's audio was positionless.

The fix: store each chunk as a `(wall_clock_offset, audio_bytes)` pair, then rebuild the full track by dropping each burst at its real-time position, with silence filling the gaps between.

```python
def _build_bot_track(chunks: list[tuple[float, bytes]], sample_rate: int) -> bytes:
    """Reconstruct bot audio track with silence gaps between turns preserved."""
    track = bytearray()
    write_pos = 0  # bytes
    for offset_secs, audio_bytes in chunks:
        wall_pos = int(offset_secs * sample_rate) * 2
        if wall_pos > write_pos:
            if wall_pos > len(track):
                track.extend(b"\x00" * (wall_pos - len(track)))
            write_pos = wall_pos
        end_pos = write_pos + len(audio_bytes)
        if end_pos > len(track):
            track.extend(b"\x00" * (end_pos - len(track)))
        track[write_pos:end_pos] = audio_bytes
        write_pos = end_pos
    return bytes(track)
```

The tricky part: within a single turn, the voice engine streams audio faster than real-time, so consecutive frames land at `wall_pos < write_pos` and just append in sequence. Between turns, `wall_pos` jumps ahead, inserting exactly the right amount of silence. Get this wrong by a few samples and the entire recording drifts out of sync. I rewrote it three times before the math held.

Two minutes after the recording fix, at 19:18, I pushed a commit titled "made pipeline complete." 93 insertions across 9 files: the scheduler, the event handlers, the pipeline builder, the service factory, and the WebRTC pipeline all wired together and talking to each other for the first time. The quiet follow-up that made everything actually work.

**Bug 2: The race condition that ate the first message**

The AI's opening line was vanishing on every other call. Half the time the bot was a stand-up comedian delivering the opener before the doors opened. Here's why. Before the AI can speak, two things have to be true: the pipeline has to be booted *and* the caller has to be connected. If the pipeline boots first and queues the greeting before the caller is on the line, the audio goes nowhere. If the caller connects first, the pipeline isn't ready yet.

```python
ready_state = {
    "pipeline_started": False,
    "client_connected": False,
    "triggered": False,
}

async def _trigger_initial_response():
    if (
        ready_state["pipeline_started"]
        and ready_state["client_connected"]
        and not ready_state["triggered"]
    ):
        ready_state["triggered"] = True
        if first_message:
            await task.queue_frame(
                TTSSpeakFrame(first_message, append_to_context=True)
            )
```

Two events, one gate. Whichever fires second triggers the greeting. It looks obvious now. It took me a day to figure out why the greeting kept disappearing.

**Bug 3: The XML tag leak**

When an LLM uses a tool, it emits markup like `<function>call_api()</function>` in its output. That's expected and correct. The problem is when those tags slip through to the voice engine, which dutifully reads them aloud: "less than function call api greater than." On every single call that triggers a tool.

I wrote a filter that strips them before they reach TTS:

```python
class XMLFunctionTagFilter(BaseTextFilter):
    _PATTERN = re.compile(
        r"<function[^>]*>.*?</function>",
        flags=re.DOTALL | re.IGNORECASE,
    )
    async def filter(self, text: str) -> str:
        return self._PATTERN.sub("", text)
```

Four lines. Zero dependencies. Saved every call from sounding like someone reading HTML out loud.

**Bug 4: Deepgram's empty final transcripts**

Speech-to-text engines stream their best guess as you talk, refining it word by word. Deepgram would return a perfectly good interim guess like "Okay." Then it would return an empty final. Pipecat only creates a transcript event for non-empty finals, so the logic that decides "the human is done talking, go reply" would stall. Voice Activity Detection said the caller stopped, but there was no transcript to act on. The pipeline just waited. Forever.

The fix lives inside a custom STT wrapper I wrote (886 lines in `service_factory.py` alone). When a final comes back empty but I have a cached interim, I promote the interim as the real transcript. Deepgram's docs don't mention this edge case anywhere. I found it by dumping per-turn WAV files and realizing the engine was hearing audio, producing a transcript, then throwing it away. A waiter who takes your order, reads it back to you, and bins it on the way to the kitchen.

### The Echo Problem

When the AI speaks, its voice comes out of the caller's speaker, bounces around the room, re-enters the microphone, and gets transcribed right back. The AI hears its own voice, treats it as the human talking, generates a reply to itself, speaks that, hears it again. An infinite loop of a robot arguing with its own echo.

The textbook fix is AEC, Acoustic Echo Cancellation: subtract the signal you're playing from the signal you're hearing. Done properly it has to account for room acoustics, speaker placement, and mic sensitivity, all of which change on every call. Heavy machinery.

I went a different way. Pipecat's user aggregator already knows when the bot is speaking and broadcasts mute-start and mute-stop signals. The catch: those signals only announce the mute state, they don't actually tell the STT engine to stop listening. So I wrote a custom `EchoSuppressionMuteStrategy` that acts on them inside the STT layer itself, paired with a `DebouncedExternalUserTurnStartStrategy` that adds a cooldown. Even if echo sneaks past and trips the voice detector, the debounce refuses to start a new turn unless a full second has passed since the last one. Two signals, one confirmation. False positives dropped by roughly 90%.

### The Voicemail Detector

Indian phone networks have their own voicemail greetings, some English, some Hindi. A detector that only knows English patterns is useless for calls in India.

```python
_PATTERNS = [
    r"please (leave|record) (a|your) message",
    r"not (available|here)",
    r"after the (beep|tone)",
    r"beep ke baad",       # Hindi: "after the beep"
    r"sandesh chhodiye",   # Hindi: "please leave a message"
]
```

It also has a fallback that needs no language at all: if the voice detector stays active for more than 8 seconds before the first transcript arrives, the other end is almost certainly a recorded greeting, not a person taking a breath. The bot hangs up before it starts leaving a message on someone's answering machine.

### The Empty Response Fallback

Sometimes the LLM returns absolutely nothing. No text, no tool call, no interruption. Just silence. Maybe the prompt confused it. Maybe the provider hiccuped. Maybe a server somewhere sneezed.

Without a fallback, the pipeline sits in dead air. The caller says "hello?" again. Still nothing. They hang up. You just lost a call to literally nothing.

```python
if (not _llm_turn_text_seen["value"]
        and not _llm_turn_tool_called["value"]
        and not _llm_interrupted["value"]):
    await task.queue_frame(
        TTSSpeakFrame(
            "I'm sorry, I didn't quite get that. Could you repeat yourself?",
            append_to_context=True,
        )
    )
```

Three boolean checks. One apology. `append_to_context=True` so the LLM remembers it said this and doesn't get confused on the next turn. This fires on roughly 3% of calls. Without it, every one of those is a silent failure.

### The Webhook Race Condition

At 19:54 that same evening, I pushed the webhook dedupe fix. The race: when a call ends, the pipeline's cleanup block fires and tries to deliver the call-ended webhook. But the scheduler's reconciliation loop might find that same unsent webhook and try to deliver it too. Two workers, same payload, hitting the customer's server twice. The call gets announced as ended twice, which is one more ending than most calls have.

The fix: lease-based dispatch backed by Redis. Before sending, a worker claims the dispatch with a short-lived lock. `claim_webhook_dispatch()` atomically checks and sets a "sent" flag. If someone else already claimed it, you skip. After delivery, `mark_webhook_sent()`. If all retries exhaust, `mark_webhook_exhausted()` so it never loops forever.

Three commits in 40 minutes on a Tuesday evening: the recording fix, the pipeline wiring, and the race condition. That's what voice infrastructure engineering actually looks like.

### The 3:35 AM Commit

On June 8, at 3:35 AM, I pushed my biggest feature drop. Realtime voice pipelines for the **OpenAI and Azure OpenAI Realtime APIs**, a fundamentally different design where listening, thinking, and speaking all happen inside one model over a single connection, instead of the traditional relay of STT to LLM to TTS. Lower latency, but a completely different shape, so I had to write a separate `build_realtime_pipeline()` because the frame graph isn't the same.

New providers landed in the same commit: **Google Vertex** as another LLM option, **Google TTS and STT**, **Sarvam** STT for Indian languages, **Cartesia** for a faster voice. The `XMLFunctionTagFilter`. In-memory audio buffering with background S3 uploads (fire-and-forget tasks held by a strong reference so the garbage collector doesn't kill an upload mid-flight). A metrics aggregator that tracks prompt tokens, completion tokens, voice characters, and processing time across every stage. And an independent max-duration watchdog as a backstop: if the pipeline somehow never ends a call, a separate task forces it after a timeout.

Then I kept going. Most people sleep after a 3 AM commit. That same day I shipped production configs (a `docker-compose.prod.yml` that stops exposing Redis and Postgres on the network, plus a Caddy reverse proxy) and post-call summaries (when an assistant has a `summary_prompt`, the transcript goes to the LLM after hang-up and the summary lands in the database). The 3 AM commit was the headline. The production configs are what turned it from a prototype into a product.

### Production Hardening and the UI Revamp

June 9 was cleanup day, the kind of day where nothing demos well and everything matters. Webhook retry triggers reworked. The transcript generation got a major overhaul, 214 lines added to `call_transcript.py`. Provider columns changed from a strict enum to a plain string, so adding a new provider no longer requires a database migration. Bug fixes across both carriers.

On June 10 at 23:14, I pushed "complete ui revamp." 52 files changed. 3,512 insertions, 4,229 deletions, net negative because I deleted the old component structure and rebuilt it. Best diff stat of the month. Dashboard, analytics, and settings pages. A real component library: cards, modals, toggles, status dots, empty states, page headers. Every page got its own component instead of being smeared across a dialog, a table, and an edit page. The thing finally looks like a product.

### The Architecture (What Actually Runs)

Pipecat does the heavy lifting. One pipeline per call, running as an asyncio Task inside FastAPI. No workers, no threads. A semaphore caps concurrent calls at 50.

- **Telephony**: Twilio and Plivo via a plugin registry. Adding a carrier means three files and a registration at import time.
- **STT**: Deepgram, wrapped in a custom class: interim promotion, echo suppression, per-turn WAV dumps for debugging.
- **LLM**: OpenAI, Groq, Google Vertex, Together AI via a factory, plus the OpenAI Realtime API where listen-think-speak collapse into one service.
- **TTS**: ElevenLabs, OpenAI, Deepgram, Cartesia, Google, and Sarvam for Indian languages.
- **WebRTC**: SmallWebRTCTransport (aiortc under the hood) at 16kHz for browser calls.
- **VAD**: Silero, tuned to 0.3s to start and 0.8s to confirm a stop.
- **Recording**: dual capture processors with wall-clock offsets, mixed to mono, uploaded to S3.
- **State**: Redis for live call state, the transcript buffer (zero database writes while a call is active), and the phone number pool. Postgres and S3 for everything durable.
- **Webhooks**: HMAC-SHA256 signing, exponential backoff, Redis lease-based deduplication.
- **Crash recovery**: the scheduler resolves orphaned calls on startup, flushes partial transcripts, and returns numbers to the pool.

### Where We Are Now

Here's the honest status:

| Feature | Status |
| :--- | :--- |
| Real-time voice conversations (sub-second latency) | Working |
| BYOK across LLM, STT, TTS providers | Working |
| Recording with proper timeline sync | Working |
| Echo suppression with debounced VAD | Working |
| Voicemail detection (English + Hindi) | Working |
| Vapi-compatible REST API | Working |
| Telephony (Twilio, Plivo) | Working |
| WebRTC browser calls | Working |
| Webhook system with retry and deduplication | Working |
| Realtime voice pipelines (OpenAI/Azure) | Working |
| Docker self-hosting | Working |
| Dashboard, analytics, settings | Working |
| Per-turn millisecond diagnostic metrics | Working |
| Crash recovery with orphan cleanup | Working |
| Post-call summary generation | Working |
| Multi-language STT beyond Hindi | In progress |

One caveat belongs next to that table. This is a one-person, one-month codebase: a single integration test, no CI pipeline, and nothing has pushed it past the 50-call semaphore yet. Every "Working" above means working on real calls, not battle-tested at scale. The QA department is me, my phone, and a 1 AM `docker compose` habit.

### The Insight

Building a voice AI platform is an exercise in managing complexity at every single layer. The intelligence, the part that sounds impressive in a pitch deck, is a few API calls. The other 90% is the plumbing.

What still surprises me is that effort and impact refuse to correlate. My best code is four lines that strip XML tags from a voice stream. The bug that took the longest was a recording mixer that didn't know what time it was. And the feature I'm proudest of is a Hindi voicemail pattern that took one line.

This is what real voice infrastructure looks like. It's not glamorous. But it works.

---

*The commit messages are vague but the code tells the real story.*
