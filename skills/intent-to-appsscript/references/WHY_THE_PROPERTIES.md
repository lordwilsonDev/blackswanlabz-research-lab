# Why these properties — causal map

- **Linguistics:** converts phrases such as "every customer" or "on time" into explicit selection and temporal conditions. Without it, code can execute perfectly while fulfilling the wrong intent.
- **Communication theory:** guards against semantic drift at each boundary: human → specification → code → log → human. Preserve original phrase, interpretation and observed result.
- **AIL:** overturns default assumptions ("AI must do it", "a trigger runs exactly once", "sending means delivered") and produces failure cases that normal happy-path testing omits.
- **MoIE:** decomposes one task into genuinely different evaluation functions; requires competing mechanisms and counterexamples, not theatrical agent counts.
- **Control flow:** expresses decisions and side effects in executable state transitions and enforces exactly-once *effects* where feasible via idempotency (not an assumption of exactly-once trigger delivery).
- **Cybernetics:** closes the gap between desired and observed behavior using metrics, feedback, stoppability and adjustment. Controlling actions does not guarantee intended outcomes.
- **Governance/security:** a script uses account authority even after the initiating conversation ends; least privilege, explicit deployment authorization and auditable state matter.
- **Teaching:** makes the created capability understandable and safely operable by the person, not just the authoring model.
- **Intelligence minimization:** LLMs perform uncertain interpretation at design-time; deterministic software carries repeated execution. Invoke intelligence again when data, goals, or rules change materially.

# Three levels of certainty
1. Structural: source code contains named constructs/tests.
2. Behavioral: tests execute and return expected results in controlled fixtures.
3. Operational: actual authorized trigger/action works against intended data with monitoring and rollback.
Never imply 3 from 1 or 2.
