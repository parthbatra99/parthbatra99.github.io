# Voice examples — annotated passages from the three canonical posts

These are the ground truth. Read them before drafting. Each excerpt is followed by a note on what it demonstrates.

## From "I Wrote 15 Postcards Nobody Asked For. They Weren't for My Friends." (personal essay, kind: theory)

> I wrote 15 postcards from the highest post office in the world. It's in Hikkim, Spiti, somewhere around 15000 feet. I was there some time back, and I spent a full day writing to the people close to me at that time. By hand, each one different, the kind of penmanship I normally save for signing official documents.

*Cold open inside a concrete scene. Specific number, specific place, specific altitude. The joke ("penmanship I normally save for signing official documents") is quiet and true, not performed.*

> Most came back with a "thanks." A few came back with "love you bro." If you know any emotionally unavailable mid-20s Indian men, you know that's the highest compliment physically possible. We are a nonchalant final boss. "Love you bro" from us is a Nobel acceptance speech.

*Humor by precise overstatement of a real observation. "We" places him inside the group being teased. Short sentences stack for rhythm.*

> The extra effort wasn't what earned the reactions. They would have come anyway. But here's the part I didn't expect. Sitting down to write fifteen postcards by hand, one full day, each one actually different, I felt *proud*. Not of the postcards. Of the version of me who chose to do it that way.

*Arguing with himself mid-essay: sets up the obvious reading, then pivots. Italics on the single pivot word. Fragments ("Not of the postcards.") earn their place.*

> Doing things well, as far as I can tell, isn't a quality strategy. It's an identity strategy.

*Theory stated as theory ("as far as I can tell"). The claim is sharp but the hedge stays.*

> I used to think I had separate dials. Work at 90, gym at 40, relationships at 60, dishes at 20. I assumed they were independent. Lately I'm not so sure.

*Numbers even for the metaphor. Revision in real time ("Lately I'm not so sure") instead of arriving pre-convinced.*

> The test I've been running on myself: could I find one more minute to make this better, and would future-me be glad I spent it? Usually yes. Sometimes no, and then I ship. I'm still figuring out which is which. I default to yes because I haven't earned the right to say no yet.

*Unresolved thread left unresolved. Self-deprecation with spine.*

> It means the postcard matters. The gym set matters. The message to the travel agent matters. Google review matters. Not because the world is keeping score, but because you are always, in every one of them, rehearsing and becoming someone. You might as well become someone who does things right!

*Ending: earned reframe, anaphora for the final build, and the one exclamation mark of the whole post.*

## From "Measuring Personal Growth" (personal essay, kind: theory)

> During table tennis practice last year, I caught myself counting imaginary scores. Not the actual rally. The *implied* one.

*Cold open in scene. Italics on the pivot word.*

> Some friends told me this whole exercise is mildly sociopathic. Why measure everything? Life is to be lived, not scored. They're not wrong, they're just asking the wrong person to stop. I'm a mathematician and an athlete at the core. I will always keep score. ... So the question was never whether to measure. It was _what_ to measure. ... It's me trying to mend me.

*He includes the strongest objection to his own premise, concedes half of it, and redirects. Evidence against himself stays in the post.*

> Becoming a new person sounds clean. It isn't. It feels like outgrowing a room you used to love, walking back in years later, and finding the ceiling too low to stand up straight in. ... The growth and the loss are the same event. I haven't figured out how to want one without getting the other.

*Domestic, human-scale metaphor. The contradiction is the point and is left standing.*

> Five years ago the college kid in me panicked about money constantly. Every UPI notification was a small heart attack.

*Indian texture (UPI) native to the material, not decorative.*

> I looked up one day and the fear had moved out without telling me.

*Personification of the abstract. Short punch after longer setup.*

> That's the one metric I trust most. Not the rate, not the problems, not the options. Just this: I can finally lose on purpose. A younger me would have called that losing. He'd have been wrong.

*Ending lands on the smallest, most personal specific instead of a summary.*

## From "I Built a Voice AI in 30 Days. Its Hardest Bug Took Three." (technical build-log, kind: built)

> You call a number, an AI picks up, you say "hello," and it says "hello" back. Feels instant. Feels simple. It is neither.

*Technical post opens cold too. Fragments for rhythm.*

> Here's the part nobody tells you: the "AI" in that chain is the easy 10%. The model is a single API call. The other 90% is plumbing.

*Thesis as plain talk. "Here's the part nobody tells you" is his move for turning the corner.*

> The git log for May 20 is telling. Between 01:13 and 02:04, there are 28 commits, all in under an hour. What was I actually doing? Trying to get a single outbound phone call to connect end to end. ... Not a clean, beautiful git history. One person at 1 AM, running `docker compose up` again and again, reading logs, fixing one framing issue at a time. Every run started with the same thought, *this is the one that fixes it*, and run 14 finally was.

*The specifics ARE the story. Self-aware about the mess, no shame, no bragging.*

> On the cheapest stack ... a 3-minute call comes out to roughly $0.10. About 8 rupees. Less than the chai you'd drink while debugging it.

*Cost made physical. Rupees and chai, because that's his actual frame.*

> The last retry fires half an hour later, which in webhook time is a formal apology letter.

*Technical humor: one clause, then move on.*

> Deepgram's docs don't mention this edge case anywhere. I found it by dumping per-turn WAV files and realizing the engine was hearing audio, producing a transcript, then throwing it away. A waiter who takes your order, reads it back to you, and bins it on the way to the kitchen.

*Bug explained, then personified in one image. The image comes after the real explanation, never instead of it.*

> One caveat belongs next to that table. This is a one-person, one-month codebase: a single integration test, no CI pipeline, and nothing has pushed it past the 50-call semaphore yet. ... The QA department is me, my phone, and a 1 AM `docker compose` habit.

*The honesty section. Every technical post undercuts its own achievement with the true caveat, stated plainly and made funny only by its precision.*

> What still surprises me is that effort and impact refuse to correlate. My best code is four lines that strip XML tags from a voice stream. The bug that took the longest was a recording mixer that didn't know what time it was.

*Closing insight is earned from the material, stated with surprise rather than authority.*

## Register differences at a glance

Personal essays (kind: theory): pure prose, zero bullets and zero tables, `***` break before the closing movement, italics for pivots, more hedging, endings tend toward reframe or admission.

Technical build-logs (kind: built): tables allowed (status, latency), real code blocks with comments in his voice, bold lead-ins for grouped items ("**Bug 1: The recording desync (3 days)**"), dates and diff stats as narrative beats, a mandatory honest-caveat passage, closing insight drawn from the wreckage.

Shared by both: cold opens, specifics over adjectives, humor only where true, no em-dashes, no advice, no summary endings.
