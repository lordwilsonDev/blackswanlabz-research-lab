---
source: vault:10_Projects/BlackSwanLabz-OS.md
vault-date: 2026-09-25
captured: 2026-09-28
status: pending
---

# BlackSwanLabz OS (roadmap)

**Not built yet.** This page describes a plan. No image, installer or repository exists, and nothing here has been tested.

## What it is

A planned rebranded fork of Omarchy, the keyboard-first Arch Linux distribution built on the Hyprland compositor, with the Hermes agent included and controllable by voice, and with the North Star method built in (see [North Star](../02-frameworks/north-star.md)). The stated reason for starting from Omarchy is that a keyboard-driven desktop is a better fit for an agent driving the machine than a mouse-driven one. That is a design judgement, not a measured result.

## Decision on what is given away

On 2026-09-25 the decision was that Axiom Inversion Logic and the Mixture of Inversion Experts are given away free, alongside the rest of the setup ([Axiom Inversion Logic](../02-frameworks/axiom-inversion-logic.md), [MoIE](../02-frameworks/moie.md)). This replaced an earlier plan, made on 2026-09-13, to hold those two back. "Free" is a statement of intent, and it is not yet literally true: the repository holding the method has no public remote, and the benchmark meant to test it has a validated harness but has not been run ([C-004](../CLAIMS.md), pending; [Hermes12 benchmark](../05-experiments/hermes12-benchmark.md)).

## Licensing research (2026-09-13)

Three research passes were run for the fork question. They are working notes from a private vault, not legal advice, and this summary is no firmer than they are.

- **Code.** Omarchy's own code is MIT-licensed and Hyprland is BSD-3-Clause. Both permit modification and redistribution, so forking is permitted.
- **Name.** The real constraint is the trademark on "Omarchy", held by a separate foundation. Rebranding avoids it. A plain-text credit such as "Powered by Omarchy" is judged low-risk under general trademark principles, but the foundation's public brand page says nothing either way, and its actual stance was not verified.
- **Third-party AI command-line tools.** Omarchy does not ship these in its image. It installs each one on first use from the vendor's own channel, and the notes treat keeping that pattern as a design constraint. Bundling the binaries instead would change the analysis: some of these tools carry permissive licenses, while Claude Code is proprietary and Anthropic's published policy governs pre-installation, so bundling it without an agreement is a real risk.

## Stated as gray, not settled

- Whether the "not a primary product" condition in one vendor's CLI license would be met by an OS image.
- Whether Anthropic's terms permit repackaging its desktop app. Omarchy already does this in its own package repository. The terms neither clearly allow nor forbid it. Reusing Omarchy's existing package without mirroring the binaries keeps the exposure with Omarchy rather than the fork, which lowers the risk without making it clearly permitted.

The notes found no outright blocker, and also did not survey every bundled app or Arch packaging terms.

## Open decisions

- How it is distributed: a virtual-machine trial, a bootable image, or something else.
- Which skills make up the free setup.
- Which Hermes instance is the reference for what ships.
- How much further licensing research is needed before engineering starts.
