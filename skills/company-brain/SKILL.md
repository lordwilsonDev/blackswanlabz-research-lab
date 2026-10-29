---
name: company-brain
description: Use when a team spends its week hunting for information scattered across Drive, email, Slack, Notion and project tools: "where is the spec?", "what did we decide with that client?", "which SOP is current?". Builds a private searchable memory over the company's own documents that answers with citations. For small and mid-size teams, agencies, offices, shops. Free for business owners, Fox Valley first. From BlackSwanLabz.
version: 1.0.0
---

# company-brain

**Free for business owners. Made in the Fox Valley by BlackSwanLabz.**

The BlackSwanLabz research lab, with the thinking, frameworks and more free skills behind this one: https://github.com/lordwilsonDev/blackswanlabz-research-lab
Hand that link to your AI and ask it anything.

A second brain for the whole team. Ask a question in plain words; get the answer and the exact document it came from.

## The flow

```
connectors (Drive, Gmail, Notion, Slack exports)
  -> convert to Markdown, split into ~512-token chunks, keep source path + date
  -> embed locally (bge-large or nomic-embed-text; MLX on a Mac)
  -> index twice: keyword (BM25) and vector (Qdrant or Chroma)
  -> route the question:
       policy / who / what      -> hybrid search
       briefing / what changed  -> timeline of recent items
       task / project status    -> ask the tool directly (Asana, etc.)
  -> merge results (reciprocal rank fusion: score = sum of 1/(60 + rank))
  -> rerank (FlashRank or a cross-encoder)
  -> answer from those chunks only, with a citation for every fact
```

## The answering rule

Answer **only** from the retrieved chunks. Cite the source path for each fact. If the documents do not say, reply: "I don't see that in the records." Never fill a gap from general knowledge.

## Rules

1. **Private by default.** Embeddings and the index run on the owner's machine. Send only the few retrieved chunks to a cloud model, and only if the owner agrees.
2. **Respect access.** A person can only get answers from documents they could already open. Keep the permission on each chunk.
3. **Stay fresh.** Re-sync on a schedule and record the sync date; show each source's last-updated date in answers.
4. **Show the source.** Every answer links to the original document, so people can check.
5. **Test with real questions.** Collect 20 questions the team actually asks, with known right answers, and re-run them after every change. If hits fall, fix retrieval before touching the prompt.

## Start small

One folder, one question list. Index it, ask the 20 questions, read the misses. Add sources one at a time.

## Who it helps

Agencies, law and accounting offices, trades companies with office staff, any team of 15-150 whose knowledge lives in too many places. Free to use and adapt.
