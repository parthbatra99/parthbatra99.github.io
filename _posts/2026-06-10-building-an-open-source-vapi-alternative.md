---
layout: post
title: "I Built a Voice AI Platform. 90% of It Is Plumbing."
subtitle: "The real engineering journal: Pipecat, WebRTC hell, a recording desync that took three days, and the four-line filter that saved every single call."
date: 2026-06-10 09:00:00 +0530
hero_art: /assets/images/voice-ai.png
tags:
  - voice-ai
  - webrtc
  - infrastructure
  - open-source
---

Here's something nobody tells you about building voice AI systems: the "AI" part is the easy 10%.

The other 90% is plumbing. It's WebSocket connections that timeout silently at 3am. It's a recording bug where bot audio packs itself tight with no silence between turns, so your mixed recording sounds like the AI is talking over itself. It's an LLM that leaks `<function>call_api()</function>` into its output, and your TTS reads it aloud to the user as "less than function call api greater than." It's race conditions between pipeline startup and client connection that drop the first message every other call.

I spent a month building openVAPI, an open-source, self-hosted alternative to Vapi and Retell. About 30 days. 4,600 lines of core pipeline code. One very long 3:35 AM commit. And I wrote every line of it.

This is the engineering journal. The wins, the disasters, and what the git log actually says.

### The Setup

On May 11, 2026, I committed the entire scaffold in one shot: FastAPI backend with assistants, phone numbers, and call logs CRUD. Next.js UI with a dark theme. Postgres, Redis, Docker. 57 files, 3,261 lines. The architecture was deliberate from day one: one FastAPI process, no workers, no threads. Every incoming WebSocket is an asyncio Task. All IO is awaited. A semaphore caps concurrent calls at 50. You scale by running more pods.

Three days later, the voice pipeline landed. I built it on top of **Pipecat**, a Python framework for real-time voice AI from the folks at Daily. Pipecat handles the hard distributed systems problems: media transport, frame plumbing, processor pipelines, turn management. What I built on top was the production layer that Pipecat doesn't give you: Twilio and Plivo telephony with a plugin registry pattern, Deepgram STT with custom echo suppression and interim promotion (more on that later), ElevenLabs TTS, OpenAI and Groq for the LLM. Event handlers with per-turn millisecond timing. A pipeline builder. A service factory. Cost calculation with `pricing.toml`.

That commit was 69 files, 14,521 lines. The first phone call actually connected.

Around May 18, I added the WebRTC pipeline for browser calls. `webrtc_pipeline.py`, using SmallWebRTCTransport with aiortc under the hood, running at 16kHz instead of the 8kHz mulaw that telephony speaks. Different sample rate, different transport, same pipeline. I also built a cost calculator so I'd know exactly what each call cost down to the token and character level.

### 1 AM, `docker compose up`, Again

The git log for May 20 is telling. Between 01:13 and 02:04, there are 28 commits, all in under an hour. What was I actually doing? Trying to get a single outbound phone call to connect end to end.

Telephony providers do not agree on anything. Twilio's WebSocket protocol expects JSON with base64-encoded mulaw. Plivo uses a slightly different framing format. The serializer has to abstract both so the pipeline just sees `InputAudioRawFrame` and `OutputAudioRawFrame` uniformly. And the handshake is a dance: the provider answers, calls your webhook, you return TwiML that opens a WebSocket, then the provider connects back with audio. Getting that right took many attempts.

That's what those 28 commits are. Not a clean, beautiful git history. One person at 1 AM, running `docker compose up` again and again, reading logs, fixing one framing issue at a time.

### "wholesale improvements"

On May 27, I made my biggest single commit and titled it "wholesale improvements" because I genuinely couldn't think of a better name. 47 files, 1,913 insertions, 312 deletions. Here's what was in it:

**The webhook service.** Outbound delivery for call events. HMAC-SHA256 signing following the Standard Webhooks spec. Exponential backoff retry with delays at [0, 5, 30, 300, 1800] seconds. A reconciliation loop that finds unsent webhooks on startup and fires them. Every attempt logged with status code, response body, and error.

**The Vapi compatibility layer.** `vapi_compat.py` exposes a REST shape matching Vapi's API. Existing Vapi clients, any tool built against the Vapi API, can point at openVAPI by changing one URL. That one decision probably saved more adoption friction than any feature I could build.

**The background scheduler with orphan cleanup.** An asyncio task running every 60 seconds. It dials `QUEUED` calls whose `scheduled_at` is due. And on startup it resolves orphans: every call stuck in a non-terminal state from a previous crash gets hung up via the provider REST API, its partial transcript flushed from Redis to Postgres, its phone number returned to the pool.

**S3 storage, consolidated migrations, and rewritten event handlers** with a `TurnMetrics` dataclass tracking VAD start, transcript finalization, LLM start, first token, LLM completion, TTS start, bot speaking start, and bot speaking end. Every turn, every call, in milliseconds.

That's the thing about voice AI. The "intelligence" is an API call. The work is everything around it.

### The Disaster Section

Four bugs. Each one cost me days. Each one taught me something I couldn't have learned from a tutorial.

**Bug 1: The recording desync (3 days)**

This was the hardest bug I fixed in the entire project. It took three days to even understand. Once the math finally clicked, the actual fix landed in a 40-minute burst of commits on the evening of May 28.

The symptom: mixed call recordings were broken. Bot audio was packed tight with no silence between turns. When the mixer combined bot audio with user audio, all the bot's turns landed at position 0. The mixed recording sounded like [bot1, bot2, bot3... user1... user2] instead of interleaving naturally. Two people having a conversation where one person lives in the past.

The root cause was subtle. `BotAudioCaptureProcessor` was storing audio bytes without wall-clock offsets. The mixer had no idea *when* each TTS burst happened. It just concatenated them. User audio spanned the full call timeline because `UserAudioCaptureProcessor` was placed before the LLMUserAggregator's mute gate, so it saw all frames regardless of mute state. But bot audio was positionless.

The fix: store `(wall_clock_offset, audio_bytes)` tuples, then reconstruct the full-length track by placing each TTS burst at its real-time position with silence filling the gaps.

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

The tricky part: within a single turn, TTS frames stream faster than real-time, so consecutive frames land at `wall_pos < write_pos` and append sequentially. Between turns, `wall_pos` jumps ahead of `write_pos`, inserting the correct silence gap. Getting this wrong by even a few samples means the entire recording desyncs. I rewrote it three times before the math clicked.

Two minutes after the recording fix, at 19:18, I pushed a commit titled "made pipeline complete." 93 insertions across 9 files. The scheduler, the event handlers, the pipeline builder, the service factory, and the WebRTC pipeline all wired together and talking to each other for the first time. The quiet follow-up that made everything actually work.

**Bug 2: The race condition between pipeline startup and client connection**

The first message was getting dropped every other call. Here's why: the pipeline needs two things to happen before it can speak. The pipeline has to be started *and* the client has to be connected. If the pipeline starts first and queues the greeting before the client is ready, the frames get dropped. If the client connects first, the pipeline hasn't booted yet.

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

Two events, one gate. Whichever fires second triggers the greeting. It looks simple now. It took me a day to figure out why the first message was disappearing.

**Bug 3: The XML function tag leak**

LLMs emit `<function>call_api()</function>` in their output during tool calls. That's expected. The problem is when these tags bleed into the TTS stream. The user hears "less than function call api greater than." On every single call that triggers a tool.

I wrote a filter that strips these before TTS with a regex:

```python
class XMLFunctionTagFilter(BaseTextFilter):
    _PATTERN = re.compile(
        r"<function[^>]*>.*?</function>",
        flags=re.DOTALL | re.IGNORECASE,
    )
    async def filter(self, text: str) -> str:
        return self._PATTERN.sub("", text)
```

Four lines. Zero dependencies. Saved every single call from sounding like someone reading HTML aloud.

**Bug 4: Deepgram empty final transcripts**

Deepgram returns a great interim transcript like "Okay." Then it returns an empty final. Pipecat only creates `TranscriptionFrame` for non-empty finals, so the turn-stop strategy stalls. The VAD says the user stopped talking, but there's no transcript to act on. The pipeline just... waits. Forever.

The fix lives inside a custom `DeepgramSTTWithLogging` class I wrote (886 lines in `service_factory.py` alone). When a final comes back empty but I have a cached interim, the interim gets promoted as the real transcript. Deepgram's API documentation does not mention this edge case. I found it by dumping per-turn WAV files and realizing the STT was hearing audio, producing a transcript, then throwing it away.

### The Echo Suppression Problem

When the AI speaks, its voice comes out of the user's speaker, bounces around the room, enters the microphone, and Deepgram transcribes it. The AI hears its own voice, generates a response to *that*, speaks it, which gets picked up again. Infinite loop of the AI talking to itself.

The standard solution is AEC (Acoustic Echo Cancellation). The correct solution involves subtracting the reference signal (what the AI is playing) from the input signal, accounting for room acoustics, speaker placement, and mic sensitivity. All of which change with every single call.

I landed on a different approach. Pipecat's `LLMUserAggregator` has mute strategies that broadcast `UserMuteStartedFrame` and `UserMuteStoppedFrame` when the bot is speaking. The problem: these frames only broadcast the mute state. They do NOT emit `STTMuteFrame`, so the STT service never actually stops listening.

I wrote a custom `EchoSuppressionMuteStrategy` that responds to these frames in the STT layer itself, combined with a `DebouncedExternalUserTurnStartStrategy` that adds a cooldown window. The VAD might fire from echo, but the debounce prevents it from triggering a new turn unless 1 second has passed since the last one. Two signals, one confirmation. False positives dropped by roughly 90%.

### The Voicemail Detector

Indian phone networks have their own voicemail greetings. Some in English, some in Hindi. A voicemail detector that only understands English patterns is useless for calls in India.

```python
_PATTERNS = [
    r"please (leave|record) (a|your) message",
    r"not (available|here)",
    r"after the (beep|tone)",
    r"beep ke baad",       # Hindi: "after the beep"
    r"sandesh chhodiye",   # Hindi: "please leave a message"
]
```

It also has a fallback: if VAD stays active for more than 8 seconds before the first transcription arrives, the other end is almost certainly a voicemail greeting, not a person. The bot hangs up before it leaves a message on someone's answering machine.

### The LLM Empty Response Fallback

Sometimes the LLM returns absolutely nothing. No text, no tool call, no interruption flag. Just silence. Maybe the prompt was confusing. Maybe the provider hiccuped. Maybe a server somewhere sneezed.

Without a fallback, the pipeline sits in dead air. The user says "hello?" again. Still nothing. They hang up. You just lost a call to literally nothing.

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

Three boolean checks. One apology. `append_to_context=True` so the LLM remembers it said this and doesn't get confused on the next turn. This fallback fires on roughly 3% of calls. Without it, every one of those calls would have been a silent failure.

### The Webhook Race Condition

At 19:54 the same evening, I pushed the webhook dedupe fix. The race: when a call ends, the pipeline's `finally` block fires and tries to deliver the call-ended webhook. But the scheduler's reconciliation loop might also find that same unsent webhook and try to deliver it. Two workers, same payload, hitting the client's server twice.

The fix: lease-based dispatch backed by Redis. Before sending, a worker claims the dispatch with a TTL. `claim_webhook_dispatch()` atomically checks and sets a `webhook_sent` flag. If someone else claimed it first, you skip. After delivery, `mark_webhook_sent()`. If all retries exhaust, `mark_webhook_exhausted()` so it never gets retried forever.

Three commits in 40 minutes on a Tuesday evening: the recording fix, the pipeline wiring, and the race condition. That's what voice infrastructure engineering actually looks like.

### The 3:35 AM Commit

On June 8, at 3:35 AM, I pushed my biggest feature drop. Realtime voice pipelines for OpenAI and Azure OpenAI Realtime APIs, the new approach where STT, LLM, and TTS are one service. This meant a completely different pipeline topology: no separate STT or TTS processors, just a single realtime LLM service handling audio in and audio out. I had to write `build_realtime_pipeline()` as a separate builder because the frame graph is fundamentally different.

New providers: Google Vertex LLM, Google TTS and STT, Sarvam STT for Indian language support, Cartesia TTS. The `XMLFunctionTagFilter`. In-memory audio buffering with background S3 uploads using fire-and-forget tasks with strong refs (prevents GC cancellation mid-upload). `PipelineMetricsAggregator` tracking prompt tokens, completion tokens, TTS characters, and processing time across every processor. A `PipelineEngineCallbacksProcessor` for post-processing hooks. And an independent max-duration watchdog as a backstop: if the pipeline somehow doesn't end the call, an async task forces it after the timeout.

Then I kept going. Most people sleep after a 3 AM commit. That same day I shipped production configs (a `docker-compose.prod.yml` that removes host port bindings from Redis and Postgres so they aren't exposed on the network, plus a Caddyfile for reverse proxy routing) and post-call summary generation (when an assistant has a `summary_prompt` configured, the transcript goes to OpenAI after hang-up and the summary lands in the database). The 3 AM commit was the headline. The production configs are what turned it from a prototype into a product.

### Production Hardening and the UI Revamp

June 9 was cleanup day. Webhook retry triggers reworked. The transcript generation got a major overhaul, 214 lines added to `call_transcript.py`. Provider columns changed from enum to string so adding a new provider no longer requires a database migration. Bug fixes across both telephony providers.

On June 10 at 23:14, I pushed "complete ui revamp." 52 files changed. 3,512 insertions, 4,229 deletions, net negative because I deleted the old component structure and rebuilt it. Dashboard, analytics, and settings pages. A real component library: cards, modals, toggles, status dots, empty states, page headers. Every page got its own full component instead of being split across a dialog, a table, and an edit page. The thing finally looks like a product.

### The Architecture (What Actually Runs)

Pipecat does the heavy lifting. One pipeline per call, running as an asyncio Task inside FastAPI. No workers, no threads. Each WebSocket is a Task. A semaphore caps concurrent calls at 50.

- **Telephony**: Twilio + Plivo with a plugin registry pattern. Adding a new provider means three files: `provider.py`, `transport.py`, `config.py`. Register at import time.
- **STT**: Deepgram with custom `DeepgramSTTWithLogging` (interim promotion, echo suppression via mute frame handling, per-turn WAV dumps for debugging)
- **LLM**: OpenAI, Groq, Google Vertex, Together AI via factory pattern. Plus OpenAI Realtime API where STT, LLM, and TTS collapse into one service.
- **TTS**: ElevenLabs, OpenAI TTS, Deepgram TTS, Cartesia, Google TTS, Sarvam (Indian language support)
- **WebRTC**: SmallWebRTCTransport at 16kHz for browser calls
- **VAD**: Silero VAD with tuned params (stop_secs=0.8, start_secs=0.3)
- **Recording**: Dual-processor approach. `UserAudioCaptureProcessor` placed before the mute gate so it sees all frames. `BotAudioCaptureProcessor` with wall-clock offsets for proper timeline reconstruction. Mixed to mono, uploaded to S3.
- **State**: Redis for call state, transcript buffer (RPUSH mid-call, zero DB writes during active calls), number pool (atomic SPOP/SADD)
- **Persistence**: Postgres (SQLAlchemy async) + S3
- **Webhooks**: HMAC-SHA256 signing, retry with exponential backoff, Redis lease-based deduplication (prevents double-sends on server restart)
- **Crash recovery**: Background scheduler resolves orphaned calls on startup. Flushes partial transcripts, returns phone numbers to pool.

The Vapi compatibility layer is a separate router that matches Vapi's REST API shape. Existing Vapi clients change one URL. That one decision probably saved more adoption friction than any feature I could build.

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

### The Insight

Building a voice AI platform is an exercise in managing complexity at every single layer. The "AI", the part that sounds impressive in a pitch deck, is a few API calls. The other 90% is the plumbing.

But here's what I actually learned: the hard problems aren't where you expect them. The recording desync took three days and required understanding PCM audio, sample rates, and wall-clock time. The race condition between pipeline startup and client connection took a day and required understanding Pipecat's frame lifecycle. The XML function tag leak took an hour but affected every single call. The empty LLM response fallback fires on 3% of calls and without it, those are all silent failures.

The best code I wrote was four lines that strip XML tags from TTS output. The bug that took the longest was wall-clock offsets in a recording mixer. The feature I'm most proud of is a Hindi voicemail pattern that took one line.

This is what real voice infrastructure looks like. It's not glamorous. But it works.

---

*The commit messages are vague but the code tells the real story.*
