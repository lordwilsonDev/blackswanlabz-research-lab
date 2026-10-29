---
name: creator-content-os
description: Use when someone has ideas in their head, a recording, or rough notes and wants a week of content in their own voice: a short video script, a newsletter, a social thread and an email, without the "AI sound". For course creators, founders, teachers, owners who write or speak for their business. Free for business owners, Fox Valley first. From BlackSwanLabz.
version: 1.0.0
---

# creator-content-os

**Free for business owners. Made in the Fox Valley by BlackSwanLabz.**

The BlackSwanLabz research lab, with the thinking, frameworks and more free skills behind this one: https://github.com/lordwilsonDev/blackswanlabz-research-lab
Hand that link to your AI and ask it anything.

You already have the ideas. The slow part is turning one idea into four formats that still sound like you. This skill does that and keeps your voice.

## The flow

```
one raw input (a 30-minute talk, bullet notes, a voice dump)
  -> transcribe and chunk it
  -> learn the voice from 3-5 things the person wrote or said themselves
  -> draft four pieces from the same idea:
       1. short video script (hook, beats, call to action)
       2. newsletter, the long version
       3. social carousel or thread, about 5 posts
       4. one email for a nurture sequence
  -> quality gate (below)
  -> the person approves, then it goes out (Ghost, Substack, Buffer, or by hand)
```

## Voice profile

Save one small file per person and reuse it:

```yaml
voice_profile:
  creator: "<name>"
  sentence_length: { mean: 11, max: 22, rhythm: "mix short and long" }
  avoid_words: [delve, game-changer, in conclusion, supercharge, testament to, unlocking, "in today's fast-paced world"]
  opens_with: "a surprising observation"
  argues_by: "claim -> what goes wrong -> a real example"
  closes_with: "one concrete thing to do next"
```

Build it from their real words, then show it to them and let them edit it.

## Quality gate

- No banned words; no filler openers ("In today's world...").
- Every claim and number comes from the person's input. Nothing invented to sound impressive.
- Read each piece against two samples of their writing: would they say this?
- Four pieces, one message: same core point, different shape for each channel.

## Rules

1. The person's words come first. Quote them; do not paraphrase them into mush.
2. Draft only. The person approves before anything is published.
3. Keep their stories theirs. Do not add examples about other people or results they did not share.

## Who it helps

Course creators, coaches, newsletter writers, founders, teachers. Free to use and adapt.
