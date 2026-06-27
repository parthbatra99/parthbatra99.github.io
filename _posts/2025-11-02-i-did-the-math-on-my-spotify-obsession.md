---
layout: post
kind: built
recommended: true
recommended_order: 4
title: "I Did the Math on My Spotify Obsession. I'm Spotify's Problem."
subtitle: "A proper cost model for Indian subscribers — marginal royalty, fully-loaded overhead, break-even analysis, and what 100k+ minutes/year actually means for Spotify's P&L."
date: 2025-11-02
hero_art: /assets/images/spotify.png
tags:
  - i-did-the-math
  - tiny-reps
---

For three years running, my Spotify Wrapped has clocked in at over 100,000 minutes. That's more than two full months of non-stop audio — not a flex, more a confession, and also the thing that made me want to actually run the numbers.

<figure class="diagram">
<svg viewBox="0 0 380 150" width="100%" height="auto" role="img" aria-label="A tipped balance scale: one tiny coin on the high side, a mountain of listening minutes crushing the low side." stroke-linecap="round" stroke-linejoin="round">
  <g fill="none" stroke="currentColor" stroke-width="2">
    <!-- Fulcrum triangle -->
    <polygon points="190,95 183,115 197,115"/>
    <!-- Tipped scale beam -->
    <line x1="60" y1="60" x2="310" y2="100"/>
    <!-- Left pan (high side — the tiny pay coin) -->
    <line x1="60" y1="60" x2="46" y2="75"/>
    <line x1="60" y1="60" x2="74" y2="75"/>
    <!-- Right pan (low side — the listening mountain) -->
    <line x1="310" y1="100" x2="296" y2="115"/>
    <line x1="310" y1="100" x2="324" y2="115"/>
    <!-- Tiny coin on the left pan -->
    <circle cx="60" cy="82" r="6"/>
    <circle cx="60" cy="82" r="4"/>
    <!-- Tower of sound-burst / play-minutes on the right -->
    <path d="M296,112 Q290,88 300,72 Q310,58 306,42" stroke-width="1.8"/>
    <path d="M304,112 Q300,94 308,78 Q316,64 312,46" stroke-width="1.8"/>
    <path d="M312,112 Q318,100 314,86 Q310,74 320,60" stroke-width="1.8"/>
    <!-- Extra little bursts piling up -->
    <path d="M288,105 Q284,98 290,92" stroke-width="1.5"/>
    <path d="M322,108 Q328,100 324,94" stroke-width="1.5"/>
    <path d="M300,105 Q306,96 302,88" stroke-width="1.5"/>
  </g>
  <g fill="currentColor" stroke="none" font-family="-apple-system, BlinkMacSystemFont, 'Segoe UI', sans-serif" font-size="13">
    <text x="60" y="100" text-anchor="middle">pay</text>
    <text x="310" y="128" text-anchor="middle">cost</text>
  </g>
</svg>
<figcaption>I take out a lot more than the subscription puts in. I'm Spotify's problem.</figcaption>
</figure>

The question was simple: at what point does a subscriber like me become a money pit for Spotify?

I'm in India, where subscription prices are among the lowest in the world. If I was going to be a freeloader anywhere, it would be here. So I built a cost model.

---

## The Revenue Side

Indian Spotify pricing is aggressive by design. A Premium Individual plan is ₹139/month — roughly $1.40, compared to $10.99 in the US. Here's what each tier actually nets Spotify per user:[^1]

| Plan Tier | Monthly Price (INR) | Users | Effective Revenue Per User (INR) |
| :--- | :--- | :--- | :--- |
| **Premium Individual** | ₹139 | 1 | **₹139.00** |
| **Premium Student** | ₹69 | 1 | **₹69.00** |
| **Premium Duo** | ₹179 | 2 | **₹89.50** |
| **Premium Family** | ₹229 | 6 | **₹38.17** |

The Family plan maxed out at six people nets Spotify ₹38 per person. That's a cup of chai at a decent place. And then there are promotional deals — Diwali 2025 had a full year of Premium for ₹499,[^2] which drops the monthly revenue per user to ₹41.58 (about 50 cents).

---

## The Cost Side: Marginal

Spotify doesn't pay artists a flat fee. They use a pro-rata model: all Indian subscription and ad revenue goes into a pool, Spotify takes ~30%, and the remaining 70% gets distributed proportionally to stream counts. Because the Indian revenue pool is smaller, the per-stream payout is smaller.

The most solid estimate for India: **$0.0008 per stream**, or at $1 = ₹87.5, that's **₹0.07 per stream**.[^3]

This is the *marginal cost* — the direct royalty expense for one additional stream.

### First break-even: royalties only

`Break-Even Streams = Monthly Revenue ÷ Royalty Cost Per Stream`

Assuming average song length of ~3.5 minutes:

| Plan Tier | Break-Even Streams/Month | Daily Listening to Break Even |
| :--- | :--- | :--- |
| **Premium Individual** | ~1,986 streams | **~4.0 hours/day** |
| **Premium Student** | ~986 streams | **~2.0 hours/day** |
| **Premium Duo** | ~1,279 streams | **~2.6 hours/day** |
| **Premium Family** | ~545 streams | **~1.1 hours/day** |

Family plan: just over an hour of daily listening and you're costing Spotify money on royalties alone.

---

## The Cost Side: Fully-Loaded

Royalties are just the variable cost. Spotify is a company with enormous fixed overhead — engineers, infrastructure, R&D, marketing. In Q2 2025, they spent €779 million combined on R&D and Sales & Marketing.[^4]

Allocating that across 602 million global subscribers over 3 months: **₹38.60 per subscriber per month** in overhead.

With an average user streaming ~600 songs/month, overhead cost per stream = ₹38.60 ÷ 600 = **₹0.064 per stream**.[^5]

Total fully-loaded cost per stream: ₹0.07 (royalty) + ₹0.064 (overhead) = **₹0.134 per stream**

### Second break-even: fully-loaded

| Plan Tier | Daily Listening to Break Even (Fully-Loaded) |
| :--- | :--- |
| **Premium Individual** | **~2.6 hours/day** |
| **Premium Student** | **~1.3 hours/day** |
| **Premium Duo** | **~1.7 hours/day** |
| **Premium Family** | **~0.7 hours/day (42 minutes)** |

Family plan subscribers cross into the red at 42 minutes of daily listening. That's barely a commute.

---

## Sensitivity Analysis

The India per-stream rate is an estimate — the actual number could reasonably be 25% higher or lower. Here's how break-even hours change for a Premium Individual subscriber across that range:

| Per-Stream Royalty (INR) | Scenario | Fully-Loaded Cost/Stream | Break-Even (hrs/day) |
| :--- | :--- | :--- | :--- |
| ₹0.053 | -25% (optimistic for Spotify) | ₹0.117 | ~2.3 hrs/day |
| **₹0.070** | **Base estimate** | **₹0.134** | **~2.6 hrs/day** |
| ₹0.088 | +25% (pessimistic for Spotify) | ₹0.152 | ~2.9 hrs/day |

The break-even range is roughly 2.3–2.9 hours/day for an individual plan. Not wildly sensitive to the royalty estimate — the conclusion holds across the range.

---

## Listener Profile Model

Let me put actual listener profiles against the cost model — across all plan tiers, at base royalty estimate:

| Listener Profile | Daily Streaming | Monthly Streams | Cost to Spotify/Month (INR) | Revenue from Individual Plan (INR) | Net (Individual) |
| :--- | :--- | :--- | :--- | :--- | :--- |
| Casual | 30 min | ~257 | **₹34.40** | ₹139 | **+₹104.60** |
| Normal | 1.5 hrs | ~771 | **₹103.31** | ₹139 | **+₹35.69** |
| Heavy | 3 hrs | ~1,543 | **₹206.76** | ₹139 | **-₹67.76** |
| Me (100k+ min/yr) | ~5.5 hrs | ~2,829 | **₹378.79** | ₹139 | **-₹239.79** |

So: on a straight per-user accounting basis, I cost Spotify about ₹240 a month on an Individual plan. The casual listener subsidizes that gap.

This is by design. Spotify's unit economics only work if the distribution of listening is heavily skewed — most users casual, a minority heavy. They need the 30-minute commuters to fund the people who treat Spotify like a utility.

---

## What This Actually Means

The 100k+ minutes number I always half-brag about in Wrapped — on a fully-loaded individual plan in India, I'm a net loss of roughly ₹240/month to Spotify. About ₹2,880 a year. That's not a company-threatening number; Spotify has 230+ million premium subscribers. But it's real.

The thing that makes this work as a business isn't clever pricing. It's that most people don't listen the way I do. The median Indian user probably listens 45 minutes a day, sits comfortably in the profitable zone, and has no idea they're covering for someone's unhinged Wrapped stats.

Spotify's bet on India isn't to extract maximum value per user. It's to capture maximum share now — at ₹139/month — and count on pricing power, podcast revenue, and audiobooks to shift the unit economics later. ₹139 today is a land-grab, not a sustainable margin.

Whether that bet pays off is a different model entirely.

### Sources
[^1]: All subscription pricing data from Spotify's official website for the Indian market as of October 2025.
[^2]: Based on a promotional offer reported by The Times of India for Diwali 2025.
[^3]: Per-stream payout rate estimate for the Indian market from industry analysis by Lost Stories Academy. Currency conversion uses $1 = ₹87.5 (approximate 2025 rate).
[^4]: Combined R&D and Sales & Marketing expenses from Spotify's official Q2 2025 earnings release. Overhead allocation: €779M ÷ 602M global subscribers ÷ 3 months = ₹38.60/subscriber/month.
[^5]: Average user streaming estimate based on industry data (~20 songs/day = 600 songs/month). Overhead cost per stream: ₹38.60 ÷ 600 = ₹0.064.
