---
layout: post
title: "Building an Open-Source Vapi: 90% Plumbing, 10% Intelligence"
subtitle: "A week-by-week engineering journal of voice pipelines, WebSocket hell, echo detection nightmares, and the last 10% that makes it all actually work."
date: 2026-06-10 09:00:00 +0530
hero_art: /assets/images/voice-ai.png
tags:
  - voice-ai
  - webrtc
  - infrastructure
  - open-source
---

Here's something nobody tells you about building voice AI systems: the "AI" part is the **easy 10%**.

The other 90%? It's plumbing. It's WebSocket connections that timeout silently at 3am. It's echo detection that thinks the AI's own voice is the user speaking. It's latency budgets measured in milliseconds where every component steals a few. It's fallback chains that need to switch providers *mid-call* without the user ever noticing.

I've spent the last ten weeks building a self-hosted, open-source voice AI platform at work — a real alternative to Vapi and Retell. The kind where every line of code is yours, you bring your own LLM/STT/TTS providers, and it runs on your own infrastructure.

This is the engineering journal of how it actually happened. The wins, the disasters, and the 2am realizations.

### Week 1-2: The WebRTC Bridge — Getting Audio In and Out

Everything starts with getting audio to flow in both directions. The user speaks into their phone or browser, and the AI speaks back. In real-time.

I started with **WebRTC** — the same protocol that powers Google Meet and Discord. The browser establishes a peer connection, and audio flows through as a media stream. Simple in theory.

**The problem:** WebRTC is designed for *browser-to-browser* communication. My server isn't a browser. I needed a media server that could act as a WebRTC endpoint — receiving audio from the client, decoding it, and passing it to my processing pipeline.

After evaluating a few options, I went with a custom Python media bridge using `aiortc`. It handles the WebRTC negotiation, receives audio frames, and exposes them as a clean async iterator. On the flip side, it takes generated audio and encodes it back into the outgoing WebRTC stream.

The first time I heard my own voice loop back through the system — delayed by about 2 seconds — was genuinely unsettling. Like talking into a cave that answers back.

**The fix for the delay:** The initial 2-second latency was mostly from *buffering*. I was queuing entire audio chunks before processing them. Switched to a streaming model where audio frames are processed as they arrive, one by one. Round-trip latency dropped to about **800ms**. Still not great, but a start.

### Week 3: The STT Layer — And the Latency Surprise

With audio flowing in, the next step was Speech-to-Text. I integrated **Deepgram** as the primary STT provider (fast, supports streaming transcription) with **OpenAI Whisper** as fallback.

This is where I learned my first hard lesson: **latency isn't just about processing speed. It's about *when* you start processing.**

If you wait for the user to finish speaking before you start transcription, you've already lost. The STT needs to be streaming — processing audio as it arrives and providing partial transcripts. But partial transcripts are *noisy*. The STT might think the user said "I want to" and then correct itself to "I want two" halfway through the next word.

**The solution:** A **Voice Activity Detection (VAD)** layer using Silero's VAD model. It runs on the incoming audio stream and tells me when the user is *actually* speaking versus when there's just background noise. Only when the VAD detects a pause — an endpoint — do I consider the transcript "final" and pass it to the LLM.

This alone cut perceived latency by **~300ms** because we stopped wasting time transcribing silence.

### Week 4: The LLM Orchestration — Streaming Tokens vs. Complete Sentences

The LLM part should be simple. Send text in, get text out. Except:

1. If you wait for the LLM to finish the *entire* response before sending it to TTS, you've added seconds of dead air.
2. If you stream tokens directly to TTS, the TTS receives incomplete sentences and produces *garbled* audio.

**The approach I landed on:** Stream LLM tokens into a **sentence buffer**. The buffer accumulates tokens until it detects a sentence boundary — period, question mark, exclamation mark, or a pause in token generation. Then it sends the complete sentence to TTS.

```python
class SentenceBuffer:
    def __init__(self):
        self.buffer = ""
        self.sentence_endings = {'.', '!', '?', '।'}

    def add_token(self, token: str) -> str | None:
        self.buffer += token
        if any(self.buffer.rstrip().endswith(e) for e in self.sentence_endings):
            sentence = self.buffer.strip()
            self.buffer = ""
            return sentence
        return None
```

The beauty of this: the first sentence of the AI's response reaches the user's ears while the LLM is *still generating the second sentence*. The perceived latency drops dramatically because the user hears *something* almost immediately.

But here's the subtle issue: what if the LLM generates a really long sentence? The buffer waits for a period that might not come for 20 tokens. During that time, the user is sitting in silence wondering if the AI crashed.

**The fix:** A timeout on the buffer. If no sentence boundary is detected within **500ms** of receiving the last token, flush whatever we have as a "best effort" sentence. The TTS handles incomplete text reasonably well — it's not perfect, but it's better than dead air.

### Week 5-6: Echo Detection — The Hardest Problem I Faced This Year

This is where things got *dark*.

When the AI speaks, its voice comes out of the user's speaker or phone earpiece. That audio bounces around the room, enters the microphone, and the STT transcribes it. The AI hears its own voice, thinks the user said something, generates a response to *that*, speaks *that* response, which gets picked up again, and... you get an infinite loop of the AI talking to itself.

The first time I saw this happen in testing, the AI had a full, coherent conversation with itself about the weather in Bangalore. It was funny for about 30 seconds. Then it was *terrifying*.

**Attempt 1: Simple mute gate.** When the AI is speaking, mute the microphone input.

*Problem:* The user can't interrupt. If the AI is rambling, the user is stuck listening to the whole monologue. Not acceptable.

**Attempt 2: Volume threshold.** Only pass audio to the STT if the input volume exceeds the AI's output volume.

*Problem:* In a quiet room, the echo can be louder than the user's actual voice. In a noisy room, background noise triggers false positives. Neither extreme works.

**Attempt 3: Acoustic Echo Cancellation (AEC).** I implemented a reference-based AEC where I subtract the AI's output audio (the reference signal) from the input audio. What's left should be the user's voice plus noise. This is the "correct" solution, but it's *hard*. The echo depends on room acoustics, speaker placement, mic sensitivity, and about a dozen other variables that change with *every single call*.

I ended up using the STT provider's built-in AEC combined with a custom **playback state tracker** — a module that knows *exactly* when the AI's audio is being played and signals the pipeline to be suspicious of incoming audio during those windows.

The combination works. For production, "works" is enough.

### Week 6: Barge-In — Letting the User Interrupt

Once echo detection was working, barge-in was the next puzzle. When the user starts speaking while the AI is mid-sentence, the system needs to:

1. **Detect** the user's speech (not echo — the distinction is critical)
2. **Stop** the TTS playback immediately
3. **Cancel** any queued LLM tokens
4. **Start** processing the user's new input

The timing window is *brutal*. If the detection is too sensitive, ambient noise cuts off the AI mid-word. If it's too slow, the user has already repeated themselves twice before the AI notices.

I landed on a **two-signal confirmation**: both the VAD *and* the echo cancellation must agree that the user is speaking before triggering a barge-in. This reduced false positives by about **90%** without adding noticeable delay to genuine interruptions.

### Week 7: Fallback Providers — When the Cloud Has a Bad Day

Here's a fun fact: LLM providers go down. Not often, but often enough that if you're running a voice platform handling concurrent calls, *someone* is going to hit an outage during business hours.

I built a **provider health monitor** that tracks:

- **Average response latency** — rolling 5-minute window
- **Error rate** — HTTP 5xx, timeouts, malformed responses
- **Time since last successful request** — catches "silent" failures

When a provider's health score drops below a threshold, the system automatically falls back to the next in the chain. For STT: Deepgram → Whisper → AssemblyAI. For LLM: OpenAI → Anthropic → a local model as absolute last resort. For TTS: ElevenLabs → OpenAI TTS → Google TTS.

The switch is **transparent to the user**. The voice might change slightly (different TTS provider), but the conversation doesn't miss a beat.

**The tricky part:** Fallback during an *active* streaming response. If OpenAI returns 3 tokens and then errors out, you can't just switch to Anthropic and start fresh — the user has already heard the beginning of the sentence. The fix: log the partial response and include it as context when retrying with the fallback provider. Seamlessly.

### Week 8: WebSocket Hell

Each active call maintains **4-5 concurrent WebSocket connections**:

1. **Client ↔ Server** — WebRTC signaling + control messages
2. **Server ↔ STT Provider** — streaming audio for transcription
3. **Server ↔ LLM Provider** — streaming chat completion
4. **Server ↔ TTS Provider** — streaming text for audio generation
5. **Server ↔ Telephony Provider** — Twilio/Vonage SIP signaling, if applicable

With 50 concurrent calls, that's **250 WebSocket connections** that all need to stay alive, handle reconnection gracefully, and — critically — *never mix up messages between sessions*.

I wrote a **ConnectionManager** that handles:

- **Heartbeat timeouts:** If a WebSocket doesn't respond to a ping within 10 seconds, consider it dead and reconnect.
- **Message ordering:** Each message has a sequence number. If messages arrive out of order, buffer and reorder before processing.
- **Session isolation:** Each call's connections are tagged with a session ID. When a call ends, *all* associated connections are torn down. No leaking sockets.

The ConnectionManager was probably the single most valuable piece of infrastructure I wrote. Everything else — the STT, the LLM, the TTS — sits on top of it. When your foundation is solid, the layers above it can afford to be a little messy. And oh, they were.

### Week 9: User Unmute Frames

Here's an edge case I didn't see coming.

When a user is muted and then unmutes, the audio pipeline receives a burst of **stale audio** — buffered frames from *before* the unmute event. These frames contain whatever was happening while muted: silence, background noise, or old conversation audio.

If the STT processes these stale frames, it might hallucinate a transcription or, worse, trigger a false VAD detection that kicks off an unnecessary LLM call. The user unmuted to say "hello" and the AI responds to a ghost sentence from 30 seconds ago.

**The fix:** A **frame sequence counter**. Each audio frame is tagged with a monotonically increasing sequence number. When an unmute event occurs, the pipeline records the current sequence number and discards any incoming frame with a lower number. Clean sync. No stale data. No ghost sentences.

### Week 9-10: Docker-First Packaging

The final piece: making the entire stack deployable with a single command.

Because if your open-source project needs a 47-step setup guide with environment variables named `THING_ONE`, `THING_TWO`, and `THING_TWO_BUT_ACTUALLY_THREE`, it's not really open-source. It's a hostage situation.

```bash
docker compose up
```

That's it. One command. The compose file pulls pre-built images and starts:

- **Media Server** — WebRTC bridge
- **Orchestration API** — FastAPI
- **Workflow Builder** — the frontend
- **Redis** — session state and pub/sub
- **NGINX** — reverse proxy with SSL termination

First startup takes 2-3 minutes to pull images. After that, you open `localhost:3010`, describe your use case in a sentence, and you're talking to your first voice bot.

### Where We Are Now

The platform is almost ready for open-source. Here's the honest status:

| Feature | Status |
|:---|:---|
| Real-time voice conversations (sub-second latency) | ✅ Working |
| BYOK across LLM, STT, TTS providers | ✅ Working |
| Echo detection + barge-in | ✅ Working |
| Fallback provider chains | ✅ Working |
| Telephony (Twilio, Vonage) | ✅ Working |
| Visual workflow builder | ✅ Working |
| MCP-native tool calling | ✅ Working |
| Docker-first self-hosting | ✅ Working |
| Python + Node SDKs | ✅ Working |
| Multi-language STT (Hindi, Spanish) | 🔨 In progress |
| Call recording + transcription export | 🔨 In progress |
| Analytics dashboard | 🔨 In progress |

### The Takeaway

Building a voice AI platform is an exercise in managing complexity at *every single layer*. The "AI" — the part that sounds impressive in a pitch deck — is a few API calls. The other 90% is the plumbing: audio routing, latency budgets, error recovery, provider failover, and a hundred edge cases that only surface when real humans start using the thing and doing things you never expected.

But that's also what makes it *interesting*. Anyone can call an API. Building the infrastructure that makes it feel *seamless* — that's engineering.

---

*We're open-sourcing soon. If you're interested in voice AI infrastructure, [follow along on GitHub](https://github.com/dograh-hq/dograh).*
