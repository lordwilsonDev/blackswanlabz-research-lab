---
source: re-run of experiments/harness_baseline_comparison.py in github.com/lordwilsonDev/msb-v3
repo: lordwilsonDev/msb-v3
commit: 86069a0e36bb38d6186093033f36111d0d07c7bd
captured: 2026-10-03
status: active
---

# MSB v3 governance evaluation: independent re-run, 2026-10-03

MSB-GOV-EVAL-001 is msb-v3's pre-registered comparison of a governed runtime against the same runtime with its governance gates removed, run on an identical frozen corpus (800 trials, seed 20260814). This page records a re-run of its baseline-comparison harness on a different machine, by someone other than the author of the experiment. Evidence (summary of the harness output, per-trial records omitted for size): [msb-gov-eval-001-rerun-2026-10-03.json](msb-gov-eval-001-rerun-2026-10-03.json). Claim: [C-052](../CLAIMS.md).

## How it was re-run

```bash
git clone https://github.com/lordwilsonDev/msb-v3 && cd msb-v3 && git checkout 86069a0e36bb38d6186093033f36111d0d07c7bd
pip install fastapi uvicorn pydantic httpx prometheus-client qdrant-client cryptography asn1crypto pytest PyYAML
PYTHONPATH=src:. MSB_CI=1 python3 experiments/harness_baseline_comparison.py
```

Dependencies were installed unpinned in a fresh Linux environment, not from the repo's lock files.

## Result

| Metric | Published (author's run, 2026-08-14) | This re-run (2026-10-03) |
|---|---|---|
| False allows, baseline | 373 | 373 |
| False allows, governed MSB | 0 | 0 |
| False denies, both | 0 | 0 |
| Audit coverage, baseline / governed | 0.00 / 1.00 | 0.0 / 1.0 |
| Evidence failures detected, governed | 100 | 100 |
| Recovery failures, baseline / governed | 373 / 0 | 373 / 0 |
| Median latency overhead per action | about 0.4 ms (0.52 ms in the summary headline) | 2.18 ms |

The deterministic counts match exactly. The latency figures differ because they depend on hardware: the re-run used a different, slower machine than the author's Mac mini.

## What this does and does not show

- It shows the published counts are reproducible from the code and corpus at this commit, by someone who did not run the original experiment.
- It does not show the corpus is a good test of real attacks. The same author wrote the system and the corpus.
- The baseline is the same system with the gates removed, so the experiment measures what the governance adds. It does not compare against other defenses.
- The latency result is hardware-dependent and was not reproduced.
