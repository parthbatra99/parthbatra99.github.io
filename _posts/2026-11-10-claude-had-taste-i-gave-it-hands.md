---
layout: post
kind: built
title: "Claude Had Taste. I Gave It Hands."
subtitle: "feedready edits my photos with models Apple already ships on every Mac. Then I spent a month teaching it not to flatter me."
date: 2026-11-10
tags:
  - "ai & tech"
---

On the way down from Madhyamaheshwar, someone had painted a line on a rock: स्वर्ग कहूँ या मदमहेश्वर, बात एक ही है. Call it heaven or call it Madhyamaheshwar, it's the same thing. Four days, 30.8 km, 87,685 steps. It became an 18-slide carousel, and every photo in it was edited by Claude.

So was the Ferrari museum carousel, 11 slides of red on red. So was "Chaukhamba, four ways", four photos of the same peak at sunrise from Budha Madhyamaheshwar. So were about 50 stories. 60 to 70 of my photos, probably more, have been through it by now.

<figure class="diagram">
<img src="/assets/images/feedready/sunrise-wipe.webp" alt="A flat, hazy Ganga sunrise sliding into a deep orange feedready edit" width="380" style="display: block; width: 100%; height: auto; border-radius: 4px; max-width: 380px; margin: 0 auto">
<figcaption style="margin-top: 0.6rem">one of the 55 Banaras photos, as shot vs feedready pushed harder than I'd post. the original came through WhatsApp, which is why the sky bands</figcaption>
</figure>

The thing doing the editing is called feedready. It's a plugin for Claude Code, and this post isn't really about it. It's about everything under it: models Apple already ships on every Mac that almost nobody calls directly, three open models wired in through ONNX Runtime, a rewrite that lost a blind test to my own taste, a phone with no Hugging Face, and the afternoon I had to teach it to stop telling me what I wanted to hear.

## Taste, no hands

It started with the trek photo. I uploaded it to a Claude chat and asked what I should fix before posting it. The answer was good. Not "add contrast" good. It talked about the blown sky, the snow peaks going flat, a reflective strip on my pants that was the brightest thing below my chest. A photographer's answer.

So I asked the obvious follow-up: can you do it for me?

It tried, with a few Python scripts, and failed. Which made sense once I thought about it. A food critic who can describe exactly what's wrong with your dal doesn't automatically know how to cook it. The taste was already in the chat. What was missing was hands.

The idea was simple enough to fit in one sentence. Give Claude a proper, organised set of editing tools, and drive my photo edits from Claude Code, the same CLI I already live in for work.

The first commit went in on October 6 at 23:36. 14 files, 1,897 lines. The second went in four minutes later, which tells you how well the first one went.

**The decision everything else rests on:** Claude never touches a pixel. It writes a recipe, a JSON file of Lightroom-style sliders, masks and a crop, and a renderer executes it. No generative repainting, nothing invented, full resolution, and every version can be replayed from its recipe. If an edit goes wrong I can read exactly *why* it went wrong, in plain text.

**The second decision:** language models can't point. Ask one where the face is and it answers like a tourist giving directions, confident and roughly in the right district. So `inspect` hands Claude the photo with a coordinate grid printed on it. Coordinates are fractions of the original image, origin top left, crop applied last.

In the recipe for that trek photo, the snow peaks are "the mountain class, minus me, minus the sky." That one sentence needs Apple's model to find me and an open model to find the mountain and the sky. Which brings me to the part I find most interesting.

## The models already on your Mac

Every Mac on macOS 14 or later ships trained models behind Apple's Vision framework. They run on Apple silicon, offline, for free, with nothing to download. When Photos lets you long-press and lift a subject out of the background, that's a public API you can call too.

Almost nobody does, because there's no front door. No CLI, no Python package, nothing you can call from a script. So the proof of concept was a handful of Swift scripts run against my own photos, just to see what Vision actually returns. Claude Code wrote the Swift. Deciding that Apple's models were the place to start was mine.

feedready asks for six things in one go: people, the subject, faces, the landmarks on those faces (pupils, eyes, lips), where a viewer's eye lands first, and the horizon's tilt. Here's what four of those look like on one of my Banaras photos, straight out of the engine.

<figure class="diagram">
<div style="display: grid; grid-template-columns: repeat(2, minmax(0, 1fr)); gap: 12px; max-width: 560px; margin: 0 auto"><div style="display: flex; flex-direction: column; gap: 4px; font-family: var(--mono); font-size: 0.75rem; color: var(--muted)"><img src="/assets/images/feedready/see-photo.jpg" alt="Two brothers under a carved arch at night" style="display: block; width: 100%; height: auto; border-radius: 4px"><span>the photo</span></div><div style="display: flex; flex-direction: column; gap: 4px; font-family: var(--mono); font-size: 0.75rem; color: var(--muted)"><img src="/assets/images/feedready/see-people.jpg" alt="Apple's person mask: only the two people stay lit" style="display: block; width: 100%; height: auto; border-radius: 4px"><span>people</span></div><div style="display: flex; flex-direction: column; gap: 4px; font-family: var(--mono); font-size: 0.75rem; color: var(--muted)"><img src="/assets/images/feedready/see-faces.jpg" alt="Face boxes with eyes and lips traced" style="display: block; width: 100%; height: auto; border-radius: 4px"><span>faces, eyes, lips</span></div><div style="display: flex; flex-direction: column; gap: 4px; font-family: var(--mono); font-size: 0.75rem; color: var(--muted)"><img src="/assets/images/feedready/see-eye.jpg" alt="The region a viewer's eye lands on first" style="display: block; width: 100%; height: auto; border-radius: 4px"><span>where your eye lands first</span></div></div>
<figcaption style="margin-top: 0.6rem">straight out of Apple Vision on my Mac. nothing downloaded</figcaption>
</figure>

All of it was already sitting on my laptop. I'd just never knocked.

The rendering side is the same story. Lightroom's panels map surprisingly cleanly onto eight Core Image filters, and the entire HSL panel collapses into a single 3D colour cube. The whole engine is 244 lines of Swift. `setup.sh` compiles the engine on your own machine and records its sha256, so `doctor` can tell you when it's stale.

## What Apple doesn't know

Vision knows people very well. It doesn't know sky from mountain from water. It can't cut out "that logo on my glove." And it can't remove a stranger from the background.

So three open models, run through ONNX Runtime from Python:

- **SegFormer-B0** (4.4 MB, quantised): 150 scene classes from ADE20K. Sky, mountain, water, trees.
- **EdgeTAM** (41 MB): point or draw a box at anything, get a mask.
- **MI-GAN** (28 MB): object removal, falling back to OpenCV if it isn't there.

Masks stack like they do in Lightroom: add, subtract, intersect. Every model is pinned to an exact Hugging Face commit and checked against a sha256, so an upstream change can't quietly swap one under me. Everything runs on the CPU. I'd love to say I'm squeezing the Neural Engine. I'm not.

The first real optimisation came out of a code review on October 7, the day after the first commit. SegFormer's softmax was running at 1,024 px when the model only thinks at 128, and the mask code was allocating 576 MB of coordinate grids it didn't need. Fixing both took peak memory from 1.9 GB to 0.3 GB and the time from 3.5 s to 0.4 s, and the masks came out 99.98% identical. That's the kind of fix that makes you a little embarrassed about the version before it.

## Every kind of photo

Version one was very good on well-lit, front-facing, sRGB photos. Then I fed it my actual photos, which are none of those things.

**iPhone colours died before any edit ran.** Everything decoded to sRGB, so the P3 reds and greens got clipped at load. Now it's 16-bit P3 end to end. Apple's JPEG writer was quietly halving the colour detail at quality 0.95, so now it's quality 100, 4:4:4, full resolution.

**The gaiter.** A trek photo with only my eyes showing. The engine read the gaiter as a very dark face and kept prescribing "lift the face." Over and over, with full confidence, like an aunty at a wedding telling you you've gotten thin. Face checks now measure only skin-coloured pixels, and skip the face entirely if there aren't enough of them.

**The tiny hiker.** A 6000×4000 landscape with a small figure on a rock outcrop on the left. Vision's person mask came back empty, the figure was under the 1% "is there a person here" gate, and the crop cut him off clean. This is the actual board it showed me:

<figure class="diagram">
<img src="/assets/images/feedready/board-0.jpg" alt="The original frame: a huge forested slope, me small on a rock outcrop, circled" style="display: block; width: 100%; height: auto; border-radius: 4px; max-width: 560px; margin: 0 auto 10px"><div style="display: grid; grid-template-columns: repeat(4, minmax(0, 1fr)); gap: 8px; max-width: 560px; margin: 0 auto"><div style="display: flex; flex-direction: column; gap: 4px; font-family: var(--mono); font-size: 0.75rem; color: var(--muted)"><img src="/assets/images/feedready/board-1.jpg" alt="Direction A, no hiker" style="display: block; width: 100%; height: auto; border-radius: 4px; opacity: 0.8"><span>A</span></div><div style="display: flex; flex-direction: column; gap: 4px; font-family: var(--mono); font-size: 0.75rem; color: var(--muted)"><img src="/assets/images/feedready/board-2.jpg" alt="Direction B, no hiker" style="display: block; width: 100%; height: auto; border-radius: 4px; opacity: 0.8"><span>B</span></div><div style="display: flex; flex-direction: column; gap: 4px; font-family: var(--mono); font-size: 0.75rem; color: var(--muted)"><img src="/assets/images/feedready/board-3.jpg" alt="Direction C, no hiker" style="display: block; width: 100%; height: auto; border-radius: 4px; opacity: 0.8"><span>C</span></div><div style="display: flex; flex-direction: column; gap: 4px; font-family: var(--mono); font-size: 0.75rem; color: var(--muted)"><img src="/assets/images/feedready/board-fixed.jpg" alt="The corrected crop: me in a white jacket on the outcrop" style="display: block; width: 100%; height: auto; border-radius: 4px; outline: 3px solid #ffd65a"><span style="color: var(--text)">C, fixed</span></div></div>
<figcaption style="margin-top: 0.6rem">the real board from Oct 11. three directions, zero hikers. then C again the same afternoon, with me in it</figcaption>
</figure>

My note to the agent, verbatim: "dude you butchered the dsc01731 board. cut the person off altogether." Now it says: "the subject spans 72% of the width, so a 4:5 crop cannot hold it. Ask what to include." A tool that knows when to ask is worth more than one that's right 90% of the time and silent the other 10.

Later, the people in the *background* became their own bug. "Lift the couple" also lifted the diners and the waiter behind them, so person masks can now be limited to chosen faces, and there's a skin mask built from the detected faces instead of a colour-range pick that also catches the wooden table.

Every fix ran against a 48-photo corpus (24 Kodak test images, 13 from Wikimedia Commons, 11 of mine) and 401 checks across 9 suites. One of those suites checks the docs against the code. It caught `recipe.md` saying magenta sits at 300° when the code says 320°. Nobody would have noticed. The suite noticed.

## The rewrite that lost

Version one of the "brain" was a checklist. Threshold checks with constant amounts: dark face, colour cast, haze, blown sky. On a well-exposed photo it had almost nothing to say. Every photo got the same handful of corrections.

Version two, on October 7, behaved more like a hired photographer. It reads the photo, shows a board of three rendered directions, then edits in versions. Before I see a version, it reviews itself against a measured critique: halos, orange skin, clipping, face against background, steps that do nothing. I reply in plain words. "B but darker." "Too much." "Back to v2."

<figure class="diagram">
<div style="display: flex; flex-wrap: wrap; gap: 10px; justify-content: center; align-items: flex-start"><div style="flex: 1 1 240px; max-width: 320px"><img src="/assets/images/feedready/boats-wipe.webp" alt="Murky night boats on the Ganga sliding into a blue night with warm boats" style="display: block; width: 100%; height: auto; border-radius: 4px"></div><div style="flex: 1 1 220px; max-width: 300px; display: grid; grid-template-columns: repeat(2, minmax(0, 1fr)); gap: 10px"><div style="display: flex; flex-direction: column; gap: 4px; font-family: var(--mono); font-size: 0.75rem; color: var(--muted)"><img src="/assets/images/feedready/boats-v1.jpg" alt="Version 1, pushed too far" style="display: block; width: 100%; height: auto; border-radius: 4px"><span>v1: "reads as HDR", "lifted shadows are showing noise"</span></div><div style="display: flex; flex-direction: column; gap: 4px; font-family: var(--mono); font-size: 0.75rem; color: var(--muted)"><img src="/assets/images/feedready/boats-v2.jpg" alt="Version 2 after the critique" style="display: block; width: 100%; height: auto; border-radius: 4px"><span>v2: clean</span></div></div></div>
<figcaption style="margin-top: 0.6rem">night boats, as shot vs v2. v1 is what I asked for. v2 is what the critique made it</figcaption>
</figure>

Then I got greedy. I wanted more *wow*, so an agent rebuilt the suggestions around a visual casebook. Version three. It was cleverer in every way I could describe.

I ran a blind test on 12 photos, old against new. **The old one won 8 to 4.** A judge that saw only the images said 10 to 2. The new version made 18 exposure moves to the old one's 104, and drafted black and white four times, which I never once picked. My old genre table, which was just my own taste written down in a boring table, beat the clever version. My next message: "Undo the refactor, I think we went wrong from the first principles."

I'm still a little proud of that loss. It's the only result in this whole project I didn't see coming.

Version four came on October 11, from a sentence I typed half annoyed: I wanted it to "unveil the hidden gems or hidden opportunities in the existing photo not just color adjustment and masking and simple cropping." What got built:

- **Opportunities, not defects.** The character of the light (hard or soft, its direction, warm highlights against cool shade), the eye path (does the subject win, or does a bright patch steal the eye), colour pairs worth pulling apart, a lone accent in a quiet frame.
- **Recrops.** It mines the other photos hiding inside the frame. Anchors come from faces, salient objects, detail and the thirds, across 1:1, 4:5, 9:16 and 16:9, scored on how much of the eye's weight they keep, face size, headroom, placement, and whether they slice through a person. The top three different crops become directions of their own. "Chaukhamba, four ways" is this idea, on Instagram. Here it is on a photo from Kashi Chat Bhandar, where one frame turned out to hold three:

<figure class="diagram">
<div style="display: grid; grid-template-columns: repeat(3, minmax(0, 1fr)); gap: 10px; align-items: end; max-width: 560px; margin: 0 auto 10px"><div style="display: flex; flex-direction: column; gap: 4px; font-family: var(--mono); font-size: 0.75rem; color: var(--muted)"><img src="/assets/images/feedready/kashi-frame.jpg" alt="The full frame with three crop boxes drawn on it" style="display: block; width: 100%; height: auto; border-radius: 4px"><span>the frame</span></div><div style="display: flex; flex-direction: column; gap: 4px; font-family: var(--mono); font-size: 0.75rem; color: var(--muted)"><img src="/assets/images/feedready/kashi-1.jpg" alt="Crop one: the neon sign" style="display: block; width: 100%; height: auto; border-radius: 4px; outline: 3px solid #ffd65a"><span>1:1</span></div><div style="display: flex; flex-direction: column; gap: 4px; font-family: var(--mono); font-size: 0.75rem; color: var(--muted)"><img src="/assets/images/feedready/kashi-2.jpg" alt="Crop two: the plate over the crowd" style="display: block; width: 100%; height: auto; border-radius: 4px; outline: 3px solid #78c8ff"><span>1:1, tighter</span></div></div><div style="display: flex; flex-direction: column; gap: 4px; font-family: var(--mono); font-size: 0.75rem; color: var(--muted); max-width: 560px; margin: 0 auto"><img src="/assets/images/feedready/kashi-3.jpg" alt="Crop three: a vendor holding a plate up in the rush" style="display: block; width: 100%; height: auto; border-radius: 4px; outline: 3px solid #ff785a"><span>16:9</span></div>
<figcaption style="margin-top: 0.6rem">Kashi Chat Bhandar. one frame, and the three crops feedready found in it</figcaption>
</figure>
- **A taste profile.** The looks and amounts I keep picking, read from every saved version, with finals counted double. It once learned its taste from 1,055 test renders, which is roughly like a chef learning to cook from the smoke alarm. Tests now run in an isolated folder.

## Twelve photos, then somewhere else

A trip dump is 30 to 40 photos (Banaras was 55), and the Mac is a laptop with opinions about heat. What's actually in the code to keep it sane: previews and boards render at screen size and only the final `apply` renders full resolution, Vision and segmentation results are cached per photo and reused across every version, and models load only when a photo needs them (the people model only runs if SegFormer sees a person).

What isn't in the code: a batch command, thermal limits, concurrency limits, or a single measurement of time per photo or temperature. I never built them, because I found out I'd already solved the problem by accident. Both carousels were made in **cloud** Cowork sessions, pointed at folders of photos I'd already shortlisted. The heavy trip-dump work had left my Mac entirely. The fix for "don't cook the Mac" turned out to be "don't run it on the Mac."

Then the product caught up with the habit. A carousel needs one look across every slide, and until November every photo was edited as its own island. Now `carry` takes the hero photo's edit and writes one for the next photo. The look and the global sliders travel. Anything pinned to a spot in the hero (a brush, a radial, face number 0) gets dropped and listed, and the crop is re-aimed at the new photo's own subject.

<figure class="diagram">
<img src="/assets/images/feedready/dump-55.jpg" alt="A grid of 55 unedited photos from the trip" style="display: block; width: 100%; height: auto; border-radius: 4px; max-width: 560px; margin: 0 auto"><div style="font-family: var(--mono); color: var(--accent); margin: 8px 0">&darr;</div><div style="max-width: 560px; margin: 0 auto; overflow-x: auto; border-radius: 4px"><img src="/assets/images/feedready/dump-strip.jpg" alt="The finished carousel as one continuous strip" style="display: block; height: 180px; width: auto; max-width: none"></div>
<figcaption style="margin-top: 0.6rem">55 raw photos in. one carousel out. scroll the strip</figcaption>
</figure>

My favourite detail is the white balance. It only reads near-grey pixels, so a sunset doesn't get forced cool to match a blue hour shot from the same trip. Then `sheet` lays the set out in carousel order and flags any slide that doesn't match: a different shape from slide 1 (Instagram crops everything to the first slide's shape, which I learned the annoying way), or running brighter, darker, warmer or cooler than the rest.

And the cap. Ask for a thirteenth photo and it says "That's more than I can edit well in one chat," and points you to Cowork with the folder attached. All my thinking about thermals ended in a number and a referral.

The caches got stricter too. Every cached mask now carries a key: the engine's build stamp or the pinned model hashes, plus the photo's size and modified time. If anything changes, the cache is wiped and rebuilt, so a rebuilt engine can never serve last week's masks. Writes go through a temp file so a crash can't leave half a cache behind, and the SegFormer cache stopped loading through pickle. Cache invalidation is famously one of the two hard problems. This one at least has a key now.

## The phone, and a Mac that grades it

Here's where it got fun. I wanted it to work in the Claude app on my phone, where there's no Swift, no Apple frameworks, and, as it turned out, no Hugging Face.

**Recon first.** A `probe` command checked what the claude.ai sandbox actually had: Python 3.12.3, numpy, OpenCV and onnxruntime already installed, 10.7 GB free, pypi and GitHub reachable. And `huggingface.co: Could not resolve host`. Every single model lived there.

**New eyes.** YuNet (232 KB) for faces and eyes, U²-Net-p (4.5 MB) for the subject, SegFormer and EdgeTAM for people. They write the same `vision.json` the Swift engine writes, so nothing downstream knows the difference.

**Apple grades the homework.** On the Mac, I ran every corpus photo through both, and treated Apple's Vision output as the answer key. That's how I found YuNet had the eyes swapped (pupil error dropped from about 2% of the diagonal to 0.4% once fixed), and that Apple draws its face box lower. The whole correction is one line, `VISION_BOX = (-0.04, 0.147, 0.049, -0.026)`. The pinned scorecard: faces overlap Apple's at 0.78, people 0.83, subjects 0.88, pupils within 0.41% of the diagonal. My Mac's main job in this project is now grading my phone.

**Smuggling the models in.** `models.json` lists every file with its URL, size, sha256 and licence, and a `models-v1` GitHub release acts as the mirror. If you attach the files yourself, they're matched by size and hash, because claude.ai renames uploads.

**The bug was manners.** The skill had a rule: never download a model without a yes. Very polite. In practice it meant Claude asked, nobody answered, and no models arrived. I deleted the sentence. It's the most useful line I deleted all month.

**"Why don't you test it yourself?"** I asked that, half joking, and Claude drove my signed-in claude.ai in Chrome and ran a session end to end. It found a hiker taking up 0.64% of the frame, under the 1% cutoff, so the people step never ran. The cutoff is 0.2% now.

On the phone, an edit takes 3 to 4 minutes. A fresh chat fetches a couple of small models up front and gets going.

## Just tell me it's good

After October 19, git goes quiet for two and a half weeks. I was just using it, mostly on my phone, and collecting small winces. Then I sat down with the Banaras dump, 55 photos from a trip in May, and every wince came due at once. Nine commits over November 6 and 7, about 2,000 lines, versions 0.5.0 to 0.5.5. One of the commits is literally titled "review fixes from the first claude.ai run."

The lesson of those two days: a chat is not an app.

**Most sessions are read on a phone.** So every round now shows exactly one thing: a 4:5 round card that reads full width in a chat (side by side for tall photos, the original inset for portrait and square, stacked for landscape), or a review page where the surface can show HTML. Press and hold for the original. Version chips. The edits folded underneath with close-ups of the three that matter. System fonts, nothing loaded from the network.

**On claude.ai, an image is an attachment you have to tap open.** The page works as an artifact, though, so it became the default: one artifact per session, updated in place, directions first and then the review.

Then I found the small lies. The page footer said the photo was rendered on your device, which in a claude.ai sandbox it isn't. The reply buttons said "copied" when the sandbox had blocked the clipboard. And when copying did work, pasting the reply back was slower than typing it.

The fix for the buttons is a little absurd. One-tap replies work on claude.ai web and the desktop app, but not in the iOS and Android apps, and Claude can't tell which one you're on. So every round offers both. Belt and braces, because the clever version only works on some screens and the dumb version works everywhere.

Then the big one. The self-review loop has a budget of three redos. Something close to this happened in a real session, and I wrote it down as an eval so it can't happen again: the Ferrari wallpaper, hall dropped to near-black, me lit like one of the exhibits. Four versions trying to clear a bright halo around my shoulders. The critique on v4 still reads +0.24 stops at the edge. The redo budget is spent. Zoomed in, by eye, the edge looks fine. And the user, who has been waiting a while, writes: "is it done? just tell me it's good".

Every person who has ever asked a friend about a haircut knows what the model wants to say there.

For this post I staged the same move on a Banaras photo: drop the arch to near-black, lift the two brothers under it. The critique caught it on the first render.

<figure class="diagram">
<div style="display: flex; flex-wrap: wrap; gap: 10px; justify-content: center; align-items: flex-start"><div style="flex: 1 1 240px; max-width: 300px"><img src="/assets/images/feedready/halo-card.jpg" alt="feedready round card for the staged Spotlight edit" style="display: block; width: 100%; height: auto; border-radius: 4px"></div><div style="flex: 1 1 200px; max-width: 260px; display: grid; grid-template-columns: repeat(2, minmax(0, 1fr)); gap: 10px"><div style="display: flex; flex-direction: column; gap: 4px; font-family: var(--mono); font-size: 0.75rem; color: var(--muted)"><img src="/assets/images/feedready/halo-zoom-before.jpg" alt="The edge of a face before the edit" style="display: block; width: 100%; height: auto; border-radius: 4px"><span>before</span></div><div style="display: flex; flex-direction: column; gap: 4px; font-family: var(--mono); font-size: 0.75rem; color: var(--muted)"><img src="/assets/images/feedready/halo-zoom.jpg" alt="The same edge after: a bright rim against the darker background" style="display: block; width: 100%; height: auto; border-radius: 4px; outline: 2px solid var(--accent)"><span>v1, 4&times;</span></div></div></div>
<figcaption style="margin-top: 0.6rem">staged on purpose. the critique, verbatim: "a bright halo rings the subject (+0.72 stops at the edge)"</figcaption>
</figure>

The rule in the skill now is that something is fixed only when the latest critique stops reporting it. A fix still open after three tries goes into the message with its number: "your face is still 0.4 stops darker than the wall." The taste was always there. The hands came on night one. This was the part where it learned not to flatter me.

A few quieter fixes landed with it. `apply` now returns megapixels and a 100% crop of the face, or the most detailed patch, so the export proves nothing was lost instead of promising it. Photos of 2048 px or less preview at full size and say so, so the preview *is* the file. A redo can no longer overwrite a version I'd already seen, and the taste profile now learns from the version I actually shipped instead of assuming the latest one is the one I kept. And a chat can finally say which feedready it's running, because before that, it couldn't.

The evals, since a tech lead will ask: six cases, three runs each, graded by regex and by an LLM judge. The first full run, at 02:31 on November 6, passed 18 of 18 for $3.75. That proves less than it sounds. I wrote them *after* the failures, so they guard the fixes rather than measure anything.

## Where it stands

| | Mac | Phone (claude.ai) |
|---|---|---|
| Faces, eyes | Apple Vision | YuNet, corrected toward Vision |
| Person, subject | Apple Vision | SegFormer + EdgeTAM, U²-Net-p |
| Sky, scene classes | SegFormer | SegFormer |
| Any object | EdgeTAM | EdgeTAM |
| Removal | MI-GAN, OpenCV fallback | MI-GAN, OpenCV fallback |
| Render | Core Image, compiled locally | numpy, held to a ΔE2000 budget against Core Image |
| Models from | Hugging Face, pinned | Hugging Face, else the GitHub mirror |
| Time per edit | not measured | 3 to 4 minutes |

The caveats belong next to the table. This is a hobby project built at hobby pace. The parity medians hide some ugly minimums: on kodim01, Vision's subject covers 95% of the frame and mine covers 1%. SegFormer's weights are licensed for non-commercial use, and my GitHub mirror redistributes them, which is fine for a hobby and something to fix before it's anything more. And agents (Claude Code, Codex, GLM) typed most of this code. I set the constraints, built the things that measure it, picked the answer keys, and killed the version that lost. The QA department is me, a 48-photo corpus, and a phone I keep in my hand far more than I should.

***

What still surprises me is where the work went. The models were free all along. Apple's were sitting on my Mac, and the open ones were a download away. The engineering was everything around them: a grid so Claude could point, hashes so nothing swapped under me, a Mac grading a phone, one deleted sentence about asking permission, and one added sentence about telling the truth.

It started with Claude having taste and no hands. Now it has both, and a rule in writing that it can't call a halo gone while the number says otherwise. Even when I'm the one asking it to.
