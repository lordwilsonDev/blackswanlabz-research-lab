# intent-to-appsscript (v0.3.0)

BlackSwanLabz skill: use AI to understand and compile a routine once, then use ordinary code to repeat it. Turns a plain-language Google Workspace automation request into a bounded Apps Script design with a checked contract, tests, a dry-run default and an honest execution receipt.

## Install

Copy this directory to `.claude/skills/intent-to-appsscript/` in your Claude Code project, or to `.agents/skills/intent-to-appsscript/` for compatible Codex environments. Do not assume linked tools or Google credentials are configured.

## First invocation

"Apply intent-to-appsscript to this task. Reuse existing capabilities, route to the right tool, write the contract, invert the hidden assumptions, build with tests, and only deploy with my explicit authorization."

## Check a contract

    python3 scripts/validate_contract.py examples/contract.json          # validate
    python3 scripts/validate_contract.py --hash examples/contract.json   # hash a receipt must carry
    python3 -m unittest discover -s tests -v                             # run the tests

The validator checks structure, consistency and the status ladder. It does not execute Apps Script, verify OAuth scopes, or prove anything ran: a receipt is a self-reported file.

## What changed in v0.2.0

See the Changelog in `SKILL.md`. Contracts written for v0.1 or v0.2 need the new fields (`rollback`, `success_measure`, and for receipts `mode`, `deployed_version` and evidence).

## Status

Drafted and unit-tested. Not yet evaluated against a baseline with a model, and no contract has been deployed or verified. Results are in `evals/results.md`.
