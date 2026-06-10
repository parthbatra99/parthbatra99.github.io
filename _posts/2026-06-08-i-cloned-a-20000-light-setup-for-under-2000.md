---
layout: post
title: "I Cloned a ₹20,000 Light Setup for Under ₹2,000"
subtitle: "How I built a real-time TV backlight that syncs colors with what's on screen, for less than the cost of a decent dinner."
date: 2026-06-08 14:00:00 +0530
hero_art: /assets/images/ambilight.png
tags:
  - diy
  - hardware
  - raspberry-pi
  - embedded
---

Philips wants **₹20,000** for the Hue Play Gradient Lightstrip. Twenty. Thousand. Rupees. For LEDs.

Let that sink in.

The Hue Play does something genuinely cool — it reads what's on your TV and projects matching colors onto the wall behind it, creating an ambient glow that makes everything feel more *immersive*. It's the kind of thing you see in a tech reviewer's setup video and immediately want.

But ₹20k? For *colored lights*? That's more than some phones. I refused on principle.

So I built my own. For under ₹2,000.

### The Plan (Or: What Philips Is Actually Charging You For)

The core idea is almost insultingly simple:

1. **Read** what's on the TV screen
2. **Sample** the dominant colors from different regions — top, bottom, left, right, center
3. **Send** those colors to an LED strip mounted on the back of the TV
4. **Repeat** fast enough that it feels real-time

That's it. That's the *entire product*. Philips wraps it in a polished app and a fancy brand name, but the engineering underneath is straightforward. Here's what I needed:

### The Bill of Materials

| Component | What It Does | Cost (₹) |
|:---|:---|:---|
| **Raspberry Pi Zero 2W** | The brain. Runs the sampling software. | 750 |
| **WS2812B LED Strip** (3m, 60 LEDs/m) | Individually addressable RGB LEDs. The actual lights. | 450 |
| **HDMI Splitter** (1-in, 2-out) | Taps the TV signal without interrupting it. | 300 |
| **USB HDMI Capture Card** | Converts the tapped HDMI into frames the Pi can read. | 250 |
| **5V 10A Power Supply** | Powers the LED strip (these things are *hungry*). | 250 |
| **Jumper Wires + Connectors** | Wiring everything together. | 100 |
| | | **Total: ₹2,100** |

Less than a tenth of the commercial price. And I'm being *generous* with the rounding.

For reference:

| | **My Build** | **Philips Hue Play Gradient** |
|:---|:---|:---|
| **Cost** | ~₹2,100 | ~₹20,000 |
| **Customizable** | ✅ Completely — it's your code | ❌ Limited to app settings |
| **Open Source** | ✅ Yes | ❌ No |
| **Works with Any TV** | ✅ Yes (anything with HDMI) | ❌ Specific TV sizes |
| **Extendable** | ✅ Add more strips, go wild | ❌ Proprietary connectors |

### The Architecture

Here's how the data flows, because understanding the pipeline is understanding where things go wrong:

```
TV HDMI Out → HDMI Splitter ──┬── [Split 1] → TV (untouched, as if nothing happened)
                               │
                               └── [Split 2] → USB Capture Card → Raspberry Pi
                                                                    │
                                                              OpenCV reads frames
                                                              Samples colors per region
                                                              Averages & smooths
                                                                    │
                                                              GPIO → WS2812B Strip → Glowing Wall
```

The HDMI splitter is the unsung hero. It lets me tap the video signal without the TV even knowing. The capture card turns that tapped signal into a video stream the Pi can process. Then a Python script — about 200 lines — does the actual work:

1. **Grab a frame** from the capture card via OpenCV
2. **Divide the frame into regions** that map to where the LEDs physically sit on the back of the TV
3. **Average the colors** in each region (with perceptual weighting — naïve averaging looks *muddy*)
4. **Smooth the transitions** using a rolling average so the colors don't seizure-inducingly flicker
5. **Push the colors** to the WS2812B strip via the Pi's GPIO using the `rpi_ws281x` library

Clean. Elegant. In theory.

### The Build: Where Things Went Sideways

The theory is clean. The practice? *Less so.*

#### The Latency Problem

The first prototype worked. The colors were... *mostly* right. But the latency was **brutal** — nearly **500ms**. The TV would show an explosion, and half a second later the wall behind it would finally, sheepishly, turn orange. It was like watching a badly dubbed movie, but for *lights*.

The bottleneck was the capture card. USB 2.0 capture cards are cheap (₹250 cheap), but they add significant latency. And processing every single frame at 30fps on a Pi Zero 2W was... *optimistic*.

**The fix:** I stopped trying to process every frame. Instead, I sample at **10fps** — fast enough to feel responsive, slow enough to let the Pi actually keep up. Combined with a ring buffer for color smoothing (weighted average of the last 5 samples), the perceived latency dropped to under **50ms**.

Still not instant. But your brain genuinely cannot tell the difference.

#### Power Injection (Or: Why My LEDs Were Dying at the Edges)

WS2812B LEDs are power-hungry little monsters. At full white, each LED draws about **60mA**. With 180 LEDs (3m × 60/m), that's **10.8A** at full brightness. The Pi *cannot* supply that. I cannot stress this enough.

The first time I turned everything on full white, the LEDs near the power supply were *blindingly* bright, and the ones at the far end of the strip were a sad, dim orange. Voltage drop along the strip was murdering my color accuracy.

**The fix:** Power injection. I ran additional power lines from the supply to the strip at **every 1-meter interval** (three injection points for a 3m strip). The difference was night and day — uniform brightness across the entire strip and no more color shift at the edges.

This is one of those things that seems obvious in retrospect but absolutely *wasn't* when I was staring at dim LEDs wondering what went wrong.

#### Signal Integrity

The WS2812B data signal is timing-sensitive. It uses a single data line with very specific pulse widths — we're talking *nanosecond-level* precision. On a Raspberry Pi, the GPIO timing can be jittery because Linux isn't a real-time OS. Other processes can interrupt and mess with your signal timing.

I was seeing random color flickers. A single LED occasionally flashing white or green in the middle of an otherwise smooth transition. It was subtle, but once you notice it, you can't *un-notice* it.

**The fix:** The `rpi_ws281x` library uses the Pi's **PWM hardware** (via DMA) to drive the data line, which sidesteps the OS jitter problem entirely. The key was making sure no other process was competing for the PWM hardware. I disabled the Pi's audio output (which also uses PWM) in `/boot/config.txt`:

```bash
dtparam=audio=off
```

Clean signal. No more flickers. A one-line fix for a problem I spent an entire evening diagnosing.

#### Color Calibration

This one snuck up on me. The colors on the wall didn't match the colors on the TV. A bright red on screen would look more like an orange-ish *pink* on the LEDs. The WS2812B color reproduction isn't perfect, and the white wall behind the TV shifts the color temperature.

**The fix:** A gamma correction table. I apply a per-channel gamma curve to the output values before sending them to the strip:

```python
GAMMA = 2.2

def gamma_correct(color):
    """Apply perceptual gamma correction to RGB tuple."""
    return tuple(int((c / 255) ** GAMMA * 255) for c in color)
```

This alone made the colors feel *significantly* more accurate. I also clamped the maximum brightness to **80%** — not because of power concerns (the injection points handled that), but because at 100% the color reproduction degrades and the strip runs hot enough to *damage the adhesive backing*. Ask me how I know.

### The Result

After a month of weekends and more than a few late nights, it works. *Really* well.

The wall behind my TV now glows with the same colors on screen. Action scenes feel more immersive. The ambient mode during movies is genuinely cinematic — warm oranges during candle-lit scenes, cool blues during underwater shots, pitch black during... well, pitch black scenes.

And the whole thing cost less than what Philips charges for a *single replacement power supply*.

### What I'd Do Differently

A few things I learned the hard way:

- **Start with power injection.** Don't wait for the dim edges to appear. Just do it from day one. Run thick wires. You'll thank yourself.
- **The capture card matters more than you think.** Spend the extra ₹100 on a USB 3.0 card if your Pi supports it. The latency improvement is worth every rupee.
- **Heat management.** The Pi Zero 2W gets warm during continuous frame processing. A ₹30 heatsink is a *very* good investment.
- **Diffusion.** Raw LED light is harsh and creates visible hotspots on the wall. A strip of frosted tape or a cheap diffuser channel softens the light beautifully. ₹50 well spent.

### The Code

The entire sampling pipeline runs on about **200 lines of Python**. It's clean, well-commented, and handles all the edge cases I discovered during the build. I'll be open-sourcing it soon — keep an eye on [my GitHub](https://github.com/parthbatra99).

---

*Sometimes the best tech isn't the most expensive. It's the one you build yourself, learn from, and can actually fix when it breaks at 2am.*
