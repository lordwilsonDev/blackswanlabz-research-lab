# Starter interview

Ask one question at a time. Accept yes, no, unknown, a number, a choice, or a sentence. Record every answer. A "no" is information, not failure. Do not explain the framework while asking. Do not fill in missing answers.

## Core eight (start here)

1. What are you trying to build or improve, in one sentence?
2. Who is it for, and what problem do they have today?
3. What would success look like in 12 months, in your own words?
4. Ask these as three separate questions, one at a time:
   a. Who does this work today, and how much of their time does it take?
   b. What do they use (paper, spreadsheet, email, software), and are past records kept anywhere?
   c. Baseline: how many per week, how long does each take, how many are lost? Also: what does an average job pay? "Unknown" is fine; write "measure first".
5. What can you not afford to lose or break (money, reputation, people, health, legal standing)?
6. How many hours a week can you put in, and how much money can you risk?
7. Who must approve decisions, and who will actually do the work?
8. What would make you stop or change direction?

## Interview rules (from the machine-shop dry run)

- **Read back.** If an answer is garbled, voice-transcribed, or surprising, restate it in one line and ask "did I get that right?" before recording it.
- **Probe absolutes.** "24/7", "never miss a customer", "better": ask what would be true in the first few minutes, then turn it into something measurable.
- **Declared is not verified.** When the person says X causes Y ("customers leave because of the wait"), record it as declared, ask "how do you know?", and add it to the to-test list.
- **Tag provenance.** Mark each answer: *real* (from the person's own business) or *imagined* (role-play, or a guess at how an owner would think). Imagined answers are hypotheses, never evidence.
- **Ask for the last real example early:** "Walk me through the last job, from first call to done." Do not assume the business model (shop floor, site visits, remote).
- **Split bundled questions.** If half an answer is missing, ask the missing half smaller. Do not fill it in.
- **Ask what a word means** before judging it (for example "leverage"). Do not assume a motive behind a question.

## Intent state

For each answer, keep one tag: confirmed, inferred, provisional, unknown, conflicted, superseded. Ask next about the item that is most uncertain, most costly if wrong, and blocking other answers. Language to probe: vague words ("grow", "better", "soon"), absolutes ("always", "never"), hidden obligations, unnamed people, and unstated deadlines.

## Escalate to the longer bootstrap only when needed

If the person wants depth, use the lab's 50-question bootstrap (`08-operations/50-question-os-bootstrap-v1.md` in the BlackSwanLabz research-lab repo). Its groups: identity and objective, scope and constraints, current state, people and authority, evidence and truth, AI and verification, workflow and capability, governance and safety, measurement and learning, self-building system. It compiles answers into: known capabilities, missing capabilities, unknowns, risks, skills and SOPs to load, metrics needed, first executable task. That compiler is a specification in the repo, not running code; this skill performs it by hand.

## Output of the interview

A one-page `intent.md`: goal, customer, constraints, resources, authority, stop conditions, a list of unknowns with who or what could resolve each, and a **to-test list** of declared or imagined claims, each turned into a question to ask a real person. End with the single most useful next question.
