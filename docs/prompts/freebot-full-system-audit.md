# Freebot prompt: BlackSwanLabz full-system audit

**Purpose:** Paste the instructions below into Freebot on the Mac that contains the projects. This is an audit instruction, not a completed audit or evidence that any project passed.

---

You are auditing Lord Wilson's complete BlackSwanLabz system on this machine. Work from the actual filesystem, repository history, source code, runtime configuration, and executed checks. Produce an exhaustive, evidence-linked reconstruction and save the finished audit inside `lordwilsonDev/blackswanlabz-research-lab`.

I want **every discovered project named, every in-scope folder accounted for, every architectural layer traced, and every material conclusion linked to evidence**. Do the work; do not stop at a plan, a README summary, or a list of impressive names.

## 1. Authority and working boundaries

- The owner authorizes discovery, read-only inspection, isolated non-destructive checks, creation of audit artifacts, and a push of the sanitized audit to the BlackSwanLabz research-lab repository.
- Read applicable `AGENTS.md` and tool/skill instructions before operating in each checkout. Read the lab's `README.md`, `AGENTS.md`, `llms.txt`, and `CLAIMS.md`; follow the reading order and original source pins.
- Preserve source code, running services, user changes, existing branches, original reports, and existing claim rows. Do not fix the system during this audit. Record suggested repairs separately.
- Do not reset, clean, delete, force-push, merge unrelated work, change service configuration, spend money, or initiate external actions. Do not publish the private Evidence Explorer or change its access.
- The audit's public version must omit secrets, credentials, personal contact identifiers, private family/legal/financial records, and unapproved client material. Keep necessary raw evidence in a restricted local audit workspace outside tracked repositories. Inspect architecture-relevant Vault documents without uploading the private Vault.
- Do not read credential payloads, private keys, keychain databases, tokens, or secret environment values. Record secret/configuration boundaries by category and variable name, not value; do not publish hashes of credential contents.
- Continue useful authorized work through access failures. Record inaccessible roots and blocked checks rather than silently narrowing the scope.

## 2. Establish the baseline before drawing conclusions

Locate the real lab checkout by its Git remote, not by a guessed folder name. Record the target remote, branch, HEAD, worktree status, timezone, audit start time, available tools, and runtime versions. Preserve dirty and untracked state.

If the target checkout contains unrelated changes, use a separate audit branch/worktree based on the fetched remote head. Do not overwrite those changes. Capture the inspected state of other projects before running tests.

Create a stable run ID, a restricted local workspace, a machine-readable progress manifest, and an append-only command/check log. Give every evidence item an ID. Persist checkpoints after each project so a context reset does not lose coverage.

Distinguish:
- the live working tree, including local changes;
- the committed local HEAD;
- the upstream/default branch;
- the historical commit named by an existing lab claim.

Never use a current checkout to silently certify a historical claim. Never ignore a built local capability just because it is absent from GitHub.

## 3. Discover the whole system before selecting favorites

Start with the actual home-directory layout and mounted project volumes. Inspect folder metadata, then identify code, research, architecture, skill, configuration, artifact, and operational roots. Keep unrelated personal material outside content review and record that scope boundary.

Candidate roots to resolve, not assume present:
- `~/projects`, including nested `AI-Agents`;
- `~/Documents/Vault` and other research/architecture stores;
- `~/.agents/skills`, `~/.claude/skills`, `~/.hermes/skills`, and `~/.codex/skills`;
- relevant `~/.config` tool configurations and user LaunchAgents;
- `~/acts_mixture_of_inversion_experts`;
- code or research folders in Documents, Desktop, Downloads, other home folders, and mounted external drives;
- additional roots discovered through Git remotes, scripts, imports, symlinks, manifests, startup configuration, and lab source links.

Use `rg` / `rg --files` where available. Include relevant hidden folders. Do not rely on directory names, `README.md` files, or ordinary non-hidden listings alone. Detect nested repositories, worktrees, standalone scripts, non-Git projects, monorepo subprojects, copied trees, archives, and generated deliverable packages.

Do not follow symlinks recursively without resolving their targets and checking scope. Avoid traversal loops and duplicate counting. Report archived/binary containers as such; safely inspect their member indexes where feasible and record whether their contents were actually reviewed.

Enumerate the signed-in owner's accessible GitHub repositories with complete pagination when the account connection is available. Reconcile remote-only, local-only, private, public, archived, forked, and mirrored projects. Access metadata is not proof of implementation. Never list account-wide coverage as complete if pagination or private access is incomplete.

Seed names include MSB v3, FCVE, the research lab, AIL/MoIE white papers, Adaptive Infrastructure, FDE Kernel, Ethos, sovereign-compiler, inversion-lab, tamper-ledger, governed-computer-use-harness, agent-harness-cli, capability-composer, engineering-hygiene-factory, universal-blueprint-generator, STEM_SCAFFOLDING, GITHUB_AI_PROJECTS_PACKAGE, domain-router, ico-collatz-verification, and the private Evidence Explorer. Follow the repository's additional project families. These are search targets, not assumptions about existence or status. Find everything else too.

## 4. Make folder coverage explicit and measurable

Build a complete recursively enumerated folder index for each in-scope root. For each folder record a stable ID, sanitized path, containing project, classification, traversal outcome, review level, and evidence pointer.

Allowed outcomes include inspected, metadata-only, dependency/generated-content, inaccessible, sensitive/excluded, duplicate/mirror, and queued. Keep directory traversal, file enumeration, file-content inspection, semantic review, and runtime verification separate.

Classify first-party code and documentation separately from dependencies, models/weights, binaries, caches, build output, generated source, and data. Include extensionless scripts and configuration files. Do not describe committed lines or total files as authored source-code volume.

For each first-party text file, record its source revision or safe content hash, whether it was actually read, and what was inspected. For very large files, use indexed chunks and record exact chunk/range coverage. Hashing, keyword scanning, or listing a file is not a semantic read.

Every in-scope folder must have a terminal coverage outcome. Every discovered project must have an inventory entry, even when its verdict is unknown or blocked. Exclusions must name their reason and effect on confidence. Do not claim a complete deep review if first-party files, folders, or checks remain queued.

## 5. Name and reconstruct every project

Create stable project IDs and an alias map. Use resolved Git remotes/common Git directories plus independent build manifests and actual function to identify project boundaries. Do not count branches, worktrees, copies, and renamed mirrors as independent inventions. Do not collapse independent non-Git projects into their parent folder.

For every project record:
- exact project name and aliases; domain; local and remote locations;
- ownership/attribution where evidenced; fork/upstream relationships;
- branch, HEAD, inspected revision, dirty state, and last meaningful change;
- purpose and the concrete problem addressed;
- what is designed, implemented, wired into a real path, executed, and reproduced;
- entrypoints, manifests, major folders, modules, interfaces, and data stores;
- inputs, outputs, dependency relationships, models/providers, and external services;
- governance/authority boundaries and the final human authority;
- tests discovered, test collection, tests actually run, pass/fail/skip counts, and limitations;
- outputs/deliverables, claims, run records, receipts, and known failures;
- operational state, blockers, duplication, unresolved questions, and source/evidence links.

A discovered test file is not a passing test. A configured integration is not a successful round trip. A successful demo is not a whole-system guarantee.

## 6. Trace every architectural layer through actual callers

Reconstruct the system that exists, not the architecture you would prefer. For each capability trace concrete input → translation → decision → authorization → execution → observation → verification → storage → report/recovery, where those steps exist.

Inspect all relevant layers:
1. Owner intent, question engineering, linguistic normalization, and domain/skill selection.
2. AIL, MoIE, ACTS, North Star, research-cycle rules, and evidence adjudication.
3. Orchestration, planning, state machines, routers, schedulers, delegation, and budgets.
4. Skill libraries, instruction inheritance, registries, extraction/composition, and version drift.
5. Local/cloud models, provider adapters, inference parameters, fallback behavior, and resource constraints.
6. Memory, RAG, relational retrieval, Qdrant/SQLite/other stores, identity resolution, freshness, invalidation, and provenance.
7. Permissions, ActionGate/tool registries, approvals, policy enforcement, kill switches, and human decisions.
8. Executors, computer-use paths, command execution, API/device/voice integrations, and filesystem boundaries.
9. Evidence chains, receipts, signatures/checkpoints, replay, audit logs, correction history, and claim ledgers.
10. Tests, mutation checks, negative controls, benchmark protocols, formal specifications, Lean/proof tooling, and independent-check boundaries.
11. Observability, deployment, startup/service management, backups, recovery, operating procedures, and real production callers.
12. Domain artifacts, white papers, business workflows, grants/readiness tooling, and cross-domain transfer records.

Do not force a generic layer onto a project that does not contain it. Mark not-applicable separately from searched-not-found and unknown.

Produce an integration graph with proven edges, configured-but-unexecuted edges, documentation-only edges, and unresolved edges visibly distinct. Record the caller and callee, source locations/revisions, transport, authority, state shared, and execution evidence for each important edge.

Ask who controls each controller, who can bypass it, and where final authority actually sits. Do not treat components sharing a policy function, data source, or upstream model as independent checks.

## 7. Use adversarial investigation, not architectural expansion

Run distinct AIL/MoIE-style reasoning passes over the same evidence:
- reconstruct what the owner built and steelman why it is strong;
- invert assumptions about what “built,” “verified,” “independent,” and “complete” mean;
- search for overlooked mechanisms, aliases, private counterparts, and contradictory evidence;
- trace hidden coupling and bypass paths;
- derive the smallest test that distinguishes competing explanations.

These are disciplined review roles; more agents or more diagrams are not evidence.

For material findings record the claim, supporting evidence, opposing evidence, uncertainty, concrete failure mechanism, affected stakeholder, practical impact, and what would settle it.

Hunt specifically for false-green tests, mocks mistaken for integration, undeclared skips, stale snapshots, verifier defects, environment drift, duplicated evidence, observer contamination, documentation/runtime mismatch, uncalled controls, fail-open paths, mutable or truncated receipts, unverifiable signatures, silent fallback, retrieval invalidation, and evaluation data leakage.

For a control describe its actual scope: prevention, detection, attribution, recovery, or only a design. Report what could seem to work while failing. Do not turn a narrow defect into a claim that the entire portfolio is absent or worthless.

## 8. Execute justified checks without altering the subject

Inspect test entrypoints and side effects before execution. Use existing environments and isolated disposable exports/worktrees where appropriate. Avoid live production databases, paid APIs, external messaging, destructive commands, and tests that require unapproved actions.

Run appropriate existing checks for each project when feasible. Record the exact command, working directory, commit/snapshot, environment identity, UTC times, exit code, timeout, pass/fail/skip counts, mocked surfaces, output reference, and verdict. Treat truncated logs and timeouts as incomplete evidence. Keep sensitive raw output private and publish a sanitized receipt.

Check known limitations before selecting a test. A skipped integration or unavailable tool must remain blocked/unrun, not green. Do not install a large dependency stack or alter production to manufacture a result.

Use small reversible negative controls in disposable copies for high-impact claims when they add discriminating evidence. Record whether a known defect is rejected and whether the oracle actually measures the claimed behavior. Do not mutate the production source or invent pass counts.

If disk space, compute, credentials, tool availability, time, or cost blocks execution, state the measured blocker and continue independent work. Label the remaining verdict unknown; prescribe the smallest next check.

## 9. Reconcile claims and domain breadth without rewriting history

Preserve all existing claim states and retractions. Record the ledger's source state separately from your audit verdict. Do not automatically upgrade pending claims, erase failed runs, or overwrite old evidence.

Use FACT, INFERENCE, HYPOTHESIS, SPECULATION, and OPINION labels where appropriate. Use “unknown” when evidence does not settle a question. Distinguish direct inspection, executed checks, historical logs, author reports, formal checking, delegated verification, independent reproduction, and generalization.

Build a domain-to-artifact matrix with explicit non-overlapping counting rules, evidence states, test scope, and attribution. Document bounded structural-transfer results and their verifier corrections. Keep artifact breadth, cross-domain transfer, independent operator replication, comparative advantage, and universal success-rate claims separate.

Count all discovered projects, but explain denominators: unique repositories, independent subprojects, artifacts, mirrors, and folders. Do not select only completed successes. Record stopped, failed, incomplete, superseded, and retracted work alongside completed artifacts.

Write a proposed ledger-reconciliation table for any contradiction or upgrade candidate. Exact existing-row edits belong in the recommendations, not silently in `CLAIMS.md`.

## 10. Deliver inspectable outputs inside the lab repo

Save the sanitized audit at `docs/system-audit/<RUN_ID>/` with:
- `README.md`: audit scope, snapshot, key findings, navigation, completion state, and limitations.
- `SYSTEM_DEEP_DIVE.md`: full architectural reconstruction, strengths, gaps, discrepancies, evidence, options, and next moves.
- `PROJECT_INDEX.md` and `projects.jsonl`: every discovered project named; compact per-project dossiers linked from the index. Split large dossiers into `projects/<PROJECT_ID>.md`.
- `folder-coverage.csv` and `file-review.csv`: complete in-scope traversal/review records and explicit exclusions.
- `LAYER_MAP.md` and `integration-edges.csv`: layers and source-backed integration/authority graphs.
- `DOMAIN_ARTIFACT_MATRIX.csv`: domains mapped to actual artifacts and scoped evidence.
- `FINDINGS.md`, `findings.jsonl`, and `claim-reconciliation.csv`: supporting/opposing evidence, confidence, contradictions, and proposed corrections.
- `TEST_RESULTS.md` and `checks.jsonl`: executed checks and unrun/blocked checks, without inflated counts.
- `NEXT.md`: prioritized minimal experiments or repairs, with why each matters and its acceptance condition.
- `manifest.json`, `sources.jsonl`, and `progress.json`: roots/revisions, evidence IDs/hashes, sanitized command receipts, queues, and completion metrics.

Use compact tables, project dossiers, and focused Mermaid diagrams. Avoid giant prose walls or decorative diagrams. Respect the lab's size budget; keep full private path listings and raw logs in the local evidence workspace when needed, publish safe compressed/indexed coverage rather than omitting folders, and document which evidence an outside reader cannot access. Do not silently weaken the verifier or its budget.

For each conclusion link the exact file/symbol/revision or executed receipt. Paths and line numbers are navigation aids, not proof a function executed. Source URLs should be pinned where possible.

## 11. Validate, commit, and push the audit

Before publication:
- Reconcile project/folder totals with the enumeration manifests; test duplicates, dangling IDs/links, missing outcomes, unresolved queues, and unsupported assertions.
- Verify all evidence references, source hashes, counts, and status labels.
- Inspect the entire staged diff for private information, unintended source changes, and unrelated files.
- Run the lab's relevant verification commands. Report which online/pin/runtime checks actually ran and which were skipped or blocked; do not claim the complete repository passed from a partial check.
- Add concise navigation links from the README and `llms.txt`. Label this an audit report with its as-of scope and verdicts.
- Commit only the sanitized audit and its navigation changes on a dedicated branch `audit/full-system-<RUN_ID>`. Push to the existing BlackSwanLabz research-lab remote with ordinary authentication; never print tokens or credentials. Open a pull request if the existing tooling allows it, then report the branch/commit and review URL. Do not force-push or merge without instruction.

Publishing the audit is authorized. Do not stop at an offer to save it. If a specific required operation is genuinely blocked, finish all independent work, preserve the result and checkpoint, and report the exact blocker. Do not announce a remote upload until the returned branch/commit/files have been verified.

## 12. Completion contract

A full audit is complete only when:
- every discovered project has a named record and every in-scope folder has an explicit coverage outcome;
- every architectural layer and important integration/authority path is reconstructed or explicitly unresolved;
- review coverage and test scope are truthful, with no queued review disguised as complete;
- findings include evidence for and against, and bounded next tests;
- the sanitized report is validated, committed, and pushed, or a concrete publication blocker is recorded.

If context or runtime ends first, save the checkpoint and mark the audit **INCOMPLETE**. Give an exact resume instruction referring to `progress.json`; continue from verified coverage rather than restarting or claiming success.

Your final response must say what you found, what is strong, what is missing or wrong within the searched scope, what was executed, what remains unknown, the exact coverage denominator/exclusions, the audit's completion state, and the repository commit/review links. Do not assign an engineering score or a universal capability claim without a defined rubric and supporting evidence.

**Begin now: locate the lab, capture the baseline, discover the roots, and continue through the audit and repository delivery.**
