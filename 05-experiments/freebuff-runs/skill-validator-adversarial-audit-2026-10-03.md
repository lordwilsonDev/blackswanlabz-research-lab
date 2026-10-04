---
source: FreeBuff (Buffy) run record from the PZS notebook, 06_ARCHITECTURE/skill-validator-adversarial-audit-2026-10-03.md; body copied unchanged except that links to other notebook files are written as plain references
captured: 2026-10-03
status: pending
---

# Skill Validator Adversarial Audit — 2026-10-03

Date: 2026-10-03
Status: TESTED / FINDINGS OPEN
Scope: `~/.agents/skills` (69 directories containing `SKILL.md`), gates:
`skill-normalizer/scripts/verify-skill.mjs` and
`skill-creator/scripts/validate-skill.mjs`.

No installed skill, validator, or mutator was modified. Mutations ran in temp
copies and temporary fixtures were removed. This is a same-author, same-session
instrument test; it is **not** an independent audit.

---

## Headline

The shipped mutation engine reports **95.6%** (680/711 applicable mutants
caught; 31 survived, all `drop-version`). That is a raw mutation-run statistic,
**not a valid estimate of incremental detection power**, for two reasons:

1. Baseline validators disagree substantially: `verify-skill.mjs` passes only
   **32/69** installed skills; `validate-skill.mjs` passes **56/69**. The
   mutator does not first record each gate's baseline result for each skill.
   Any mutant that fails an already-failing gate is counted as “caught,” even
   if the mutation had no causal effect.
2. A deliberately syntax-broken gate, and a gate subprocess that cannot spawn
   `node`, both produce a **100% catch score and exit 0** on a one-skill corpus.
   Non-zero child outcomes are treated as gate verdicts rather than requiring
   evidence that the gate ran and evaluated the mutant.

Six adversarial probes were executed against throwaway fixtures. **Six behaviors reproduced** (five failure modes plus one valid-YAML contract disagreement).
The run and summarized records are in
`state/repair/test-skill-gate-blindspots.mjs` (FreeBuff notebook file `../state/repair/test-skill-gate-blindspots.mjs`)
and `state/repair/SKILL_GATE_PROBES_2026-10-03.txt` (FreeBuff notebook file `../state/repair/SKILL_GATE_PROBES_2026-10-03.txt`).

## Exact full-corpus mutation run

Command (equivalent):

```bash
node ~/.agents/skills/mutating-skill/scripts/mutate-and-score.mjs \
  --corpus ~/.agents/skills \
  --gate-verify ~/.agents/skills/skill-normalizer/scripts/verify-skill.mjs \
  --gate-env ~/.agents/skills/skill-creator/scripts/validate-skill.mjs
```

Observed:

```text
69 skills discovered
711 applicable mutants
680 caught
31 survived
95.6% raw catch rate
```

| Operator | Caught / applicable | Result |
|---|---:|---|
| abs-link | 21/21 | 100% |
| angle-desc | 39/39 | 100% |
| bad-name | 69/69 | 100% |
| bloat-body | 69/69 | 100% |
| break-link | 21/21 | 100% |
| drop-desc | 69/69 | 100% |
| drop-frontmatter | 69/69 | 100% |
| drop-name | 69/69 | 100% |
| drop-skill-md | 69/69 | 100% |
| drop-version | 8/39 | 21% |
| gut-workflow | 69/69 | 100% |
| stray-file | 69/69 | 100% |
| unquote-desc | 39/39 | 100% |

31 survivors = `drop-version` on skills whose removal of version was accepted
by both gates. The mutator's own documentation explicitly says version is
warning-only by design; these are **known equivalents by the declared gate
contract**, not defects by themselves. The 30 `drop-version` N/A rows are skills
without a version field.

The operator set omits critical contracts: `name == containing directory`,
actual YAML parse validity, and mutation causality against per-gate baseline.

## Installed-corpus baseline, before mutation

The two validators were independently run against every skill directory (69):

```text
verify-skill.mjs    32/69 pass; 37 fail
validate-skill.mjs  56/69 pass; 13 fail
```

These gates intentionally implement different subsets and have different
contracts, but the mutator aggregates them with OR (`either non-zero = caught`)
and does not preserve which gate caught which condition or whether that gate
already failed before mutation. So “95.6%” is not “95.6% of defects newly
caught.”

A static skill-corpus audit was also run on frontmatter, L1 quality, body budget,
links, and safety:

```text
checks_run: frontmatter, l1-quality, l2-budget, links, safety
counts: high 0, medium 45, low 1136, info 28
```

These include findings across installed authored/vendor material. They are
routing/hygiene signals, not validator correctness or security verdicts. The
skill-corpus-audit self-test passed **79/79 assertions**. It tests its fixtures;
it does not establish perfect recall on this real corpus.

## Reproduced gaps and contract disagreement

### 1. Folder/name identity accepted by both gates

Fixture directory: `wrong-folder-name/`
Frontmatter: `name: fixture-skill`

```text
verify-skill exit 0
validate-skill exit 0
```

The verify gate checks kebab-case, not `name == directory basename`. The
environment gate also checks shape, not identity. If downstream tooling binds
skill identity to folder name, this can create ambiguous or silently ignored
skills. Severity depends on the consuming harness; not every deployment may
require equality. The gate contract should say whether mismatch is prohibited.

### 2. Malformed YAML accepted by both gates

Fixture description:

```yaml
description: "Use this skill when: "trigger" is described here"
```

Both gates exit 0. Ruby Psych's actual YAML parser rejects the same frontmatter:
`did not find expected key while parsing a block mapping`. Both validators use
regex extraction/brace heuristics, not YAML parsing. Therefore the comment
claim “frontmatter parses as YAML” in `verify-skill.mjs` is stronger than what
its implementation establishes.

### 3. Valid YAML single-quote disagreement

The environment validator accepts single- or double-quoted YAML scalars. The
normalizer validator requires double quotes. A fixture with a valid single-
quoted `description` therefore produced:

```text
verify-skill exit 1
validate-skill exit 0
```

This is a **contract disagreement**, not necessarily a defect: if the normalizer
intentionally requires a stricter style than YAML or the environment validator,
that requirement should be explicit. The mutator does not include a single-quote
operator, so the disagreement is outside its reported score.

### 4. Pre-existing failure credited to unrelated mutation

One-skill baseline fixture had an unquoted description:

```text
baseline verify exit=1
baseline environment gate exit=0
```

Applying `drop-version` (warning-only and unrelated) still yields:

```text
drop-version 1/1 (100%)
```

because the already-failing verify gate makes the mutator's OR condition report
“caught.” This is a causal attribution flaw. Catch credit should require a
baseline-pass gate to transition to a mutation-specific failure, with the
failure attributable to the injected condition.

### 5. Syntax-crashed validator counted as an ordinary catch

A temporary gate file existed but contained invalid JavaScript. The mutator's
preflight only checked file existence. It then ran that gate 13 times; Node's
syntax error was a non-zero status, which `runGate` treated as `fail` / “gate
caught mutant.” Result:

```text
13/13 caught — 100.0%
mutator exit 0
```

The code has a guard for `e.code.startsWith('ERR_')`, but `execFileSync`'s
syntax-error child process failure surfaced as a status, not such an error code.
The guard therefore does not protect this case.

### 6. ENOENT when spawning a gate counted as an ordinary catch

Both gate script files existed. The mutator was launched with an absolute Node
runtime, but child `PATH` contained no `node`; each `runGate` attempted
`execFileSync('node', ...)` and received `ENOENT`. The mutator again returned:

```text
13/13 caught — 100.0%
mutator exit 0
```

This directly falsifies the mutator docstring's assertion that “Any gate that
cannot run must fail the whole run loudly.” It only preflights gate file
existence; it does not establish successful gate execution.

## Interpretation

- `drop-version` survivors are intentional under the current warning-only
  contract; retain them as the known-equivalent class unless the contract
  changes.
- The 95.6% raw score is useful as a snapshot of this operator/corpus pair,
  but is **not fit to be quoted as gate effectiveness** because baseline
  failures and tool errors are credited as catches.
- The two validators are not equivalent: one enforces body size/content/links;
  the other focuses on required metadata and selected compatibility concerns.
  Reports must remain per-gate, not only OR-aggregated.
- Structural mismatch and invalid YAML are real contract gaps if validators
  are intended to guarantee canonical skill identity and parseable YAML. The
  fixtures prove acceptance; a policy owner should confirm those requirements
  before modifying the validators.
- The skill-corpus-audit self-test's 79/79 is encouraging fixture coverage, but
  the same principle applies: self-tests do not prove independent correctness.

## Second pass: skill-corpus-audit itself

Ran `skill-corpus-audit/scripts/self_test.py`: **79/79**. Then ran additional
temporary-corpus probes against the actual imported audit implementation. Results
are preserved in `state/repair/SKILL_CORPUS_AUDIT_PROBES_2026-10-03.txt` and the
repeatable fixture driver `state/repair/test-skill-corpus-audit-blindspots.py`.

### Confirmed behavior and findings

- **Malformed YAML is not detected by `check_frontmatter`.** A skill with matching
  folder/name and a sufficiently long description containing unescaped internal
  quotes was rejected by PyYAML but produced no frontmatter finding. This is
  consistent with the script's stated “deliberately not a YAML parser” design,
  so classify as a declared limitation / contract boundary—not a hidden bug.
- **Path traversal and symlink escapes are accepted by the link check.**
  `scripts/../../outside.md` resolved to an existing file outside the skill root
  and emitted no containment finding. A `scripts/` symlink to an external
  directory likewise resolved outside and emitted no finding. The auditor checks
  existence and basenames, not containment after resolution. Whether this is a
  defect depends on intended scope: skill references may intentionally point to
  external resources, but such a link is not safely contained by this skill.
- **Closed-fence and inline-code links are not promoted to medium broken-link
  findings, but they still produce low “looks illustrative” findings.** Therefore
  the user-facing guide's stronger wording (“links in a fence or inline code span
  are not links, so neither is scanned”) is not literally true of the current
  behavior. This is a noise/documentation mismatch, not a false medium breakage.
- **The unclosed-fence case is explicitly documented as a known limitation.** The
  probe observed a low illustrative finding for it. This is not counted as a
  surprise defect; the boundary is already disclosed.
- **The reasoned safety suppression behaves as documented:** code-line marker
  becomes an info receipt and suppresses the medium network finding. This is a
  trust boundary (skill author supplies the reason), not a verification that the
  reason is substantively valid. It is transparent but not an independent review.

### Second-pass conclusion

The 79/79 self-test demonstrates the named fixtures, not general correctness.
This additional pass found two unannounced containment/parse limitations (YAML
parser intentionally minimal; path containment not checked) and one wording
mismatch on code-span filtering. It did **not** reproduce a false medium finding
for closed fences, nor did it show the safety suppression being silent.

## Repair priority — proposal only

1. **Fix mutation accounting first:** establish a baseline per gate/per skill;
   count only a baseline-pass → post-mutation-fail transition; distinguish
   `GATE_ERROR`/spawn error from `GATE_REJECTED`; fail closed if either gate
   could not execute.
2. **Use a real YAML parser** in validation, or narrow the claim to a clearly
   documented syntactic subset and mutation-test that exact grammar.
3. **Decide and encode folder/name identity** in the gate contract, then add
   matching and mismatching controls.
4. Re-run the full suite only after baseline behavior is stable, report each
   gate's score separately, and keep `N/A`/known-equivalent rows separate from
   defect survivors.

No validator or mutator repair was applied. This is a findings report, not
approval to change installed gates.

## Related

- Probe source (FreeBuff notebook file `../state/repair/test-skill-gate-blindspots.mjs`)
- Probe output (FreeBuff notebook file `../state/repair/SKILL_GATE_PROBES_2026-10-03.txt`)
- Corpus-audit probe source (FreeBuff notebook file `../state/repair/test-skill-corpus-audit-blindspots.py`)
- Corpus-audit probe output (FreeBuff notebook file `../state/repair/SKILL_CORPUS_AUDIT_PROBES_2026-10-03.txt`)
- Epistemic substrate promotion filter (FreeBuff notebook file `epistemic-substrate-promotion-filter-v1-0.md`)
- Governor v1.0 pointer (FreeBuff notebook file `epistemic-governor-substrate-v1-0.md`)
- Domain-crossing benchmark (FreeBuff notebook file `domain-crossing-depth-benchmark-v1-0.md`)
- Verify the mutation landed (FreeBuff notebook file `../39_LESSONS/verify-the-mutation-landed.md`)
- Duplicated guards hide mutations (FreeBuff notebook file `../39_LESSONS/duplicated-guards-hide-mutations.md`)