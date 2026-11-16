# Roadmap

Use this file for direction and GitHub Issues for day-to-day work once connected. Initial issue bodies are in `docs/backlog.md`. Priorities are P0 (next/blocking), P1 (next milestone), and P2 (later).

| Milestone | Outcome | Exit evidence | State |
| --- | --- | --- | --- |
| M0 — Select and design | Bounded concept, source research, architecture, assumptions | Decision records and primary-source notes | Selected source sections/metadata and upstream introductions checked; mapping review remains iterative |
| M1 — Traceable assessment | Local JSON → rules → Markdown/JSON | Synthetic demo, negative tests, reproducible sample report, continuity docs | Implemented locally; final verification recorded in PROJECT_STATUS |
| M1 publication | Authorized portfolio repository and issue backlog | Approved account/visibility/license; verified remote, CI, Issues/milestones | App access resolved; license/charter published; feature PR and CI verification in progress |
| M2 — Structured adversarial review | Actors, incentives, assets, prerequisites, misuse cases, evidence records | Reviewed scenario set, explicit rejected hypotheses, control/evidence provenance | Next implementation milestone |
| M3 — Evaluated agent assistance | Limited research or evidence assistance without autonomous acceptance | Baseline comparison, error analysis, injection/permission tests | Deferred until M2 establishes evaluation data |
| M4 — Professional demonstration | Coherent portfolio narrative and repeatable realistic example | Walkthrough, sample artifacts, limitations, independent review | Planned |

## Immediate sequence

1. Finish local verification and commit the MVP.
2. Verify primary framework sources and existing-tool scope when network access is available. Establish GitHub access; inspect repository metadata only to find a suitable destination. Do not modify other repositories.
3. Public-repository/account, Apache-2.0, and app authorization are resolved. Publish only this project and verify the resulting files.
4. Create milestones and Issues from the prepared backlog. Push a feature branch and open a PR for the working implementation; verify hosted CI.
5. Expand the reviewed baseline with at least five distinct organizational use cases before adding rules or agent-generated suggestions.

## Learning checkpoints

After M1, explain the input contract, graph traversal, why a path is only a hypothesis, and why control claims do not establish acceptable risk. After M2, distinguish an observed test result from a proposed attack and explain residual-risk decisions. After M3, evaluate agent errors and permission boundaries against a manual baseline.

## Session workflow

Start by reading PROJECT_STATUS, DECISIONS, LEARNING_LOG, ROADMAP, and the remote issue backlog when accessible. Choose one bounded next issue. Build → Explain → Verify → Reflect. End with current tests, committed status, unresolved decisions, and the next concrete task. Do not promise unattended execution: no schedule is configured.
