# Roadmap

Use this file for direction and GitHub Issues for day-to-day work once connected. Initial issue bodies are in `docs/backlog.md`. Priorities are P0 (next/blocking), P1 (next milestone), and P2 (later).

| Milestone | Outcome | Exit evidence | State |
| --- | --- | --- | --- |
| M0 — Select and design | Bounded concept, source research, architecture, assumptions | Decision records and primary-source notes | Selected source sections/metadata and upstream introductions checked; mapping review remains iterative |
| M1 — Traceable assessment | Local JSON → rules → Markdown/JSON | Synthetic demo, negative tests, reproducible sample report, continuity docs | Implemented locally; final verification recorded in PROJECT_STATUS |
| M1 publication | Authorized portfolio repository and issue backlog | Approved account/visibility/license; verified remote, CI, Issues/milestones | Implementation merged via PR #1; hosted CI verified; Issues created; native milestones pending #11 |
| M2 — Structured adversarial review | Actors, incentives, assets, prerequisites, misuse cases, evidence records | Reviewed scenario set, explicit rejected hypotheses, control/evidence provenance | Next implementation milestone |
| M3 — Evaluated agent assistance | Limited research or evidence assistance without autonomous acceptance | Baseline comparison, error analysis, injection/permission tests | Deferred until M2 establishes evaluation data |
| M4 — Professional demonstration | Coherent portfolio narrative and repeatable realistic example | Walkthrough, sample artifacts, limitations, independent review | Planned |

## Immediate sequence

1. Expand the reviewed baseline with at least five distinct organizational use cases ([#5](https://github.com/NatTuji/ai-risk-governance-lab/issues/5)) before adding rules or agent-generated suggestions.
2. Review local framework mapping applicability and the OWASP 2026 edition ([#8](https://github.com/NatTuji/ai-risk-governance-lab/issues/8)).
3. Configure native milestones and main-branch protection when administration tooling is available (#11 and #12).
4. Develop structured actors, incentives, prerequisites, and human-reviewed evidence records (#6 and #7).

## Learning checkpoints

After M1, explain the input contract, graph traversal, why a path is only a hypothesis, and why control claims do not establish acceptable risk. After M2, distinguish an observed test result from a proposed attack and explain residual-risk decisions. After M3, evaluate agent errors and permission boundaries against a manual baseline.

## Session workflow

Start by reading PROJECT_STATUS, DECISIONS, LEARNING_LOG, ROADMAP, and the remote issue backlog when accessible. Choose one bounded next issue. Build → Explain → Verify → Reflect. End with current tests, committed status, unresolved decisions, and the next concrete task. Do not promise unattended execution: no schedule is configured.
