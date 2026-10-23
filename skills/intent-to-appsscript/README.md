# intent-to-appsscript (v0.4.0)

BlackSwanLabz skill: use AI to understand and compile a routine once, then use ordinary code to repeat it. The AI and the user work through it together: the skill supplies the baseline every automation needs, the person decides everything that depends on their situation, and the AI recommends and explains. The result is a bounded Apps Script design with a checked contract, tests, a dry-run default and an honest execution receipt.

## Install

Copy this directory to `.claude/skills/intent-to-appsscript/` in your Claude Code project, or to `.agents/skills/intent-to-appsscript/` for compatible Codex environments. Do not assume linked tools or Google credentials are configured.

## First invocation

"Use intent-to-appsscript and work through this with me. Explain the basics every automation needs, ask me about my situation one thing at a time, recommend and give your reasons, let me decide, and only deploy when I say so."

## Check a contract

    python3 scripts/validate_contract.py examples/contract.json          # validate
    python3 scripts/validate_contract.py --hash examples/contract.json   # hash a receipt must carry
    python3 -m unittest discover -s tests -v                             # run the tests

The validator checks structure, consistency and the status ladder. It does not execute Apps Script, verify OAuth scopes, or prove anything ran: a receipt is a self-reported file.

## What changed in v0.2.0

See the Changelog in `SKILL.md`. Contracts written for earlier versions need the new `decisions` record (and a user `deployment` decision if deployed); six formerly mandatory fields became situational and may be marked `{"not_applicable": "<reason>"}`.

## Status

Drafted and unit-tested. Not yet evaluated against a baseline with a model, and no contract has been deployed or verified. Results are in `evals/results.md`.
