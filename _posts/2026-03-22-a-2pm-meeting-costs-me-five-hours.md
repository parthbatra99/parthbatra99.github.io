---
layout: post
kind: theory
title: "A 2 p.m. Meeting Costs Me Five Hours"
subtitle: "I run on a maker's schedule and I keep forgetting it. What one badly-placed meeting actually takes from the day."
date: 2026-03-22
tags:
  - get-shit-done
  - note-to-self
---

Are you a maker, or a manager? Not what your business card says. What your calendar says. [Paul Graham](https://www.paulgraham.com/makersschedule.html) drew this line years ago, and once you see it you can't unsee it. I spent last week on the wrong side of it.

I was chasing a race condition in a webhook handler for a client deadline we were already three days behind on. Critical work, my name on it, the kind of bug that only shows itself if you can hold the whole call flow in your head at once. I'd finally gotten it cornered by noon. Then a 2 p.m. review landed on the calendar. One hour, they said.

It cost me five.

The state machine I'd been holding in my head all morning drained out somewhere around the time the reminder fired. I sat through the meeting making the right faces, ran a quiet post-mortem on it in my own head for an hour after, and by the time I reopened the editor the exact shape of the bug was gone. All that scaffolding I'd spent the morning building in my head to hold it up, someone had quietly dismantled it while I sat in a room nodding. The day was over in everything but the clock. One meeting. One hour, on paper. Five hours, in reality.

Here's the part I'm less proud of. For years I'd have looked at that day, a packed calendar and a bug still open, and quietly called it productive. A full calendar used to feel like proof I mattered. I said yes to the sync, yes to the catch-up, yes to the review I had no stake in, because I hadn't earned the right to say no yet, and a full calendar was the easiest way to feel like I had one.

Graham's argument is that there are two kinds of schedules, and they are mutually hostile. The **manager schedule** runs on the hour. Nine to six, back to back, finish one meeting and walk into the next. It is the schedule of people whose job is to talk about the work. The **maker schedule** runs on the half-day. You block the whole morning for one hard thing, or the whole afternoon, because real work, writing code, drafting an essay, working through a proof, doesn't survive being interrupted. It needs a runway to take off.

The trap, for me, is that the manager schedule feels better in the moment. A day of back-to-back calls leaves you tired in a way that reads as important. You were needed, look, the calendar proves it. A maker's day leaves you with one shipped thing and six hours nobody saw, which feels like less even when it's the only thing that mattered. I know which schedule I do my real work on. I still catch myself reaching for the other one, because it's the one that gives you something to point at by 6 p.m.

<figure class="diagram">
<svg viewBox="0 0 380 150" width="100%" height="auto" role="img" aria-label="Manager day split into many small meeting blocks; maker day is one long block broken by a single 2pm meeting." font-family="-apple-system, BlinkMacSystemFont, 'Segoe UI', sans-serif">
  <g fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round">
    <rect x="90" y="22" width="38" height="26" rx="3"/>
    <rect x="132" y="22" width="38" height="26" rx="3"/>
    <rect x="174" y="22" width="38" height="26" rx="3"/>
    <rect x="216" y="22" width="38" height="26" rx="3"/>
    <rect x="258" y="22" width="38" height="26" rx="3"/>
    <rect x="300" y="22" width="38" height="26" rx="3"/>
    <rect x="90" y="92" width="116" height="26" rx="3"/>
    <rect x="210" y="92" width="38" height="26" rx="3" fill="currentColor"/>
    <rect x="252" y="92" width="86" height="26" rx="3" opacity="0.35"/>
  </g>
  <g stroke="none" fill="currentColor" font-size="13">
    <text x="82" y="40" text-anchor="end">manager</text>
    <text x="82" y="110" text-anchor="end">maker</text>
    <text x="229" y="136" text-anchor="middle" opacity="0.6">2pm</text>
  </g>
</svg>
<figcaption>One meeting dropped into a maker's day doesn't cost an hour. It fragments the whole afternoon.</figcaption>
</figure>

A single meeting dropped into a maker's day doesn't cost an hour. It costs the runway. The hour before it, because your brain starts taxiing toward the meeting. The hour of the meeting itself. The hour after it, where you sit and quietly replay what was said. And the rest of the afternoon, because the thread you were holding is gone and you can't find the end of it again.

***

Then I started shipping things I actually cared about again, and that story fell apart fast. You can't finish a feature between two meetings. A hard bug won't stay in your head when part of you is already bracing for the next notification. The maker schedule isn't a preference. It's a precondition. The work doesn't exist without it.

So I did the unglamorous thing. I picked one day, Wednesday, and shoved every meeting I couldn't kill onto it. Standups, syncs, reviews, the lot, all stacked back to back so Wednesday looks like a manager's whole week compressed into eight hours. It's an ugly day. I'm useless for real work by the end of it. But it buys the other four clean, and I guard those like they're the only thing I own, because at work they mostly are.

Saying that out loud cost more than I expected. Nothing in a corporate calendar is ever actually a quick sync. "Bas paanch minute ka kaam hai" is just how a forty-minute call introduces itself before it eats your morning. And the honest reason for saying no, that fifteen minutes on the phone costs me three hours at the desk, sounds precious to someone whose whole job runs on those fifteen-minute calls. So I mostly don't explain. I just move it to Wednesday. The race condition got fixed on a Thursday nobody had booked. Almost everything I'm proud of this year happened on a day the calendar was empty.

***

I still lose the occasional afternoon to a meeting I shouldn't have taken. Last week's was one of them. But I've stopped calling those days productive, and that one honesty has done more for my week than any system I've tried.

Graham wrote that the manager schedule is the one you're *supposed* to want, the one the senior people run. I used to read that as aspiration. I read it as a warning now. The full calendar I once wanted so I'd have something to point at by 6 p.m. turned out to be the clearest sign I'd stopped making the things worth pointing at.

The 2 p.m. meeting was never really the problem. Forgetting what the afternoon was for was.

---

*Most days don't evaporate. You trade them away, one yes at a time.*
