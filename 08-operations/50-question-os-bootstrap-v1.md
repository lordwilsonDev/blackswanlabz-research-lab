# 50-Question OS Bootstrap

**Status:** Core bootstrap interface

## Purpose

This is the initial ignition sequence for the BlackSwanLabz capability/SOP compiler. A new user does not need to understand the architecture first. Claude, Codex, or another capable agent asks these questions one at a time, records the answers, and compiles the resulting state into the next required questions, skills, harnesses, SOPs, metrics, and executable task.

## Agent instruction

Ask these questions **one at a time**. The user should answer **YES or NO**. Do not explain the architecture while asking. Record every answer. Do not assume that NO means failure. After all 50 answers, compile the answers into an initial OS state and identify the next smallest set of questions required to move forward.

If YES/NO is not legitimately knowable, the agent may record **UNKNOWN** rather than forcing a false binary answer.

## 50 Questions

### Identity & objective

1. Do you know what you are trying to accomplish?
2. Can you describe the desired end state?
3. Is there a real problem or opportunity driving this?
4. Do you know who the intended beneficiary or customer is?
5. Do you know what success would look like?

### Scope & constraints

6. Have you defined what is inside the scope of this effort?
7. Have you defined what is outside the scope?
8. Are there constraints that cannot be violated?
9. Are there deadlines that materially affect the solution?
10. Are there resources you must work within?

### Current state

11. Do you know what already exists?
12. Do you know what has already been tried?
13. Do you have existing documents, data, code, procedures, or other evidence?
14. Do you know what is currently working?
15. Do you know what is currently failing?

### People & authority

16. Do you know who is responsible for the outcome?
17. Do you know who has authority to make the relevant decisions?
18. Do you know who will actually use the resulting system or procedure?
19. Have the affected people been represented in the problem definition?
20. Do you know who can approve the final result?

### Evidence & truth

21. Do you have evidence supporting your current understanding of the problem?
22. Can you distinguish facts from assumptions?
23. Can you identify which claims are still uncertain?
24. Do you know what evidence would prove your current explanation wrong?
25. Can another person independently inspect the evidence?

### AI & verification

26. Are you willing to have AI challenge your assumptions instead of merely confirming them?
27. Can you use more than one model or independent reasoning path when the issue matters?
28. Are you willing to treat model agreement as insufficient proof?
29. Can you test an AI-generated conclusion against independent evidence?
30. Do you have a way to record AI failures and corrections?

### Workflow & capability

31. Can the problem be broken into smaller tasks?
32. Can those tasks be turned into repeatable procedures?
33. Would a successful procedure be useful again in the future?
34. Can you define what a competent performance of the task looks like?
35. Can you test that competence on a new example rather than the example used for training?

### Governance & safety

36. Are there actions the system must never take without human approval?
37. Are there privacy, security, legal, financial, safety, or ethical constraints?
38. Do you know what should happen when the system encounters uncertainty?
39. Do you know when the system must stop and escalate to a human?
40. Can you preserve an audit trail of important decisions and changes?

### Measurement & learning

41. Do you have a measurable way to determine whether the system improved?
42. Do you know which failures matter most?
43. Can you measure the time or resources required to perform the work?
44. Can you distinguish a successful outcome from a merely plausible answer?
45. Can successful procedures be converted into reusable organizational knowledge?

### Self-building system

46. Are you willing to let the system identify capabilities you have not yet designed?
47. Are you willing to create a new skill when repeated work reveals a reusable pattern?
48. Are you willing to create a new harness or test when a failure reveals a missing control?
49. Are you willing to revise the system when evidence shows that an existing assumption is wrong?
50. Do you want the system to continuously turn verified solutions into reusable capabilities?

## Post-bootstrap compilation

The 50 answers are not the product. They are the initial state.

The agent should compile:

**Answers → Initial State → Known Capabilities → Missing Capabilities → Unknowns → Dependencies → Risks → Skills to Load → Harnesses to Load → SOPs Required → Metrics Required → Next Questions → First Executable Task**

Rules:

- A **NO** is information, not automatically failure.
- An **UNKNOWN** is not true or false; it identifies missing knowledge.
- Contradictions become diagnostic signals.
- Do not invent missing information merely to complete the bootstrap.
- Model agreement is not proof.
- Independent evidence and testing outrank plausible answers.
- Failed tests are information and should be preserved.
- Human decisions remain explicit.
- The system should build/compile the next needed capability from the discovered state rather than requiring a fixed curriculum in advance.

## Core operating idea

**The user answers questions. The OS figures out what it needs to build next.**
