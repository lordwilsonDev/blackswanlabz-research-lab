---
source: draft evidence-class rule for human adjudication, written by the assistant after part 1 of IA-1 returned INCONCLUSIVE, 2026-10-05
captured: 2026-10-05
status: pending
---

# Draft adjudication rule (not frozen; the owner decides)

Part 1 of [IA-1](../../06-proofs/integrated-assessment-ia-1.md) was INCONCLUSIVE because two scorers could not agree on what counts as execution or reconstruction. This draft fixes the classes before any person scores the 15 domains, so the person applies a rule instead of deciding each domain from scratch. Part 1's recorded result is not changed by it. If adopted, it is benchmark v1.1 and the person's scores are a new run.

## Three evidence classes

| Class | Means | Ladder level it can support |
|---|---|---|
| Artifact | A file, design or analysis exists. Nobody has run it. | up to L6 |
| Execution | Someone ran it and a record exists: command, inputs and environment, output, exit status. The runner may be the author. | L7, and L8 if the run was an attack on the result |
| Reconstruction | A party other than the original author, using only the repository and pinned commit (no conversational state), re-ran the method and the record compares the new result with the original published one, including where they differ. | L9 |

## Rules

1. **A re-run is execution until it meets the reconstruction test.** An assistant re-running a pinned harness this session meets it only if the run used the repo's own instructions, a pinned commit, and a recorded comparison with the original. The MSB v3 and FCVE re-runs in `CLAIMS.md` (C-052, C-057 to C-061) have those records; whether they count as "a party other than the author" is the open question below.
2. **Claim status does not set the level.** A pending row is not a reason to score an executed run as unexecuted. The level reflects what was run; the claim row says whether the statement is established.
3. **One run, one domain.** An execution record counts toward L7 or higher in a single named domain. Other domains may cite it only up to L6. This stops one strong artifact (the MSB v3 re-run) from creating breadth.
4. **Reading is not running.** A document read with `unzip` or a viewer is an artifact (Rule F). The antitrust L7 in scorer A fails this rule.
5. **Synthetic data stays synthetic.** It can support L5 to L8. It cannot support L10.

## Open questions only the owner can answer

1. Does a re-run by the assistant, or by a different model, count as "a party other than the original author" for L9? If yes, say so; if only a human or an unrelated team counts, L9 is unreachable by this session's re-runs and the domains drop to L7 or L8.
2. Is the author's own reproduction of their own harness after a clean checkout (no re-run by anyone else) execution only, or reconstruction?
3. Who adjudicates? The owner scoring their own domains is the same-author problem the ladder names; a second person is the check.

## Why not average the two scorers

Averaging mixes two different readings of the rule and produces a number neither reading supports. The floor in [RESULT.md](runs/2026-10-05/RESULT.md) is a conservative bound, not a measurement.
