# Project status

Last updated: 2026-11-15 America/Edmonton (host date 2026-11-16 UTC). Remote default branch: `main`; active local handoff branch: `docs/publication-status`. Working project: `/workspace/ai-risk-governance-lab`. Earlier November 16 entries use the host's UTC date for this same local-date session.

## Current state

The working MVP is published on [NatTuji/ai-risk-governance-lab](https://github.com/NatTuji/ai-risk-governance-lab), licensed Apache-2.0. [PR #1](https://github.com/NatTuji/ai-risk-governance-lab/pull/1) merged the reviewed implementation into `main` at `4bb17f710ffb180e81ac032779d141caf4b68fd8`. All 33 uploaded file blobs matched the reviewed local snapshot. [Hosted CI](https://github.com/NatTuji/ai-risk-governance-lab/actions/runs/43805777964) passed on Python 3.11, 3.12, 3.13, and 3.14, including tests and both report formats. Eleven Issues were created (#2–#12); #2–#4 closed with the merge. Actual milestones and main-branch protection remain pending.

## Completed locally

- Compared three bounded concepts and selected an inspectable deployment assessment CLI.
- Created the charter, architecture diagram, versioned input contract, assessment method, lab threat model, roadmap, contribution guidance, and prioritized issue-ready backlog.
- Implemented strict JSON loading, directed flow graph analysis, five candidate-risk rules, Markdown/JSON output, evidence questions, adoption/inaction questions, and mandatory human review.
- Added a synthetic support-assistant example and exactly reproducible report: four matched categories, three boundary crossings.
- Added 54 automated tests with positive and negative behavioral baselines, malformed-input checks, graph cycles/disconnections, output protection, and report-display checks.
- Built a Python wheel and verified its console script in an isolated environment outside the source checkout. See `docs/verification.md` for scope and limits.
- Verified hosted CI for Python 3.11–3.14, with all four jobs and their steps successful.
- Added the approved full Apache-2.0 license and SPDX package metadata; verified the standard license is included in built package metadata.
- Established local commit history: `3229122` charter/plan; `ed5a582` working CLI/tests; later commits record reference uncertainty and session handoff. Use `git log --oneline` for final hashes.

## Active milestone

M1 working implementation and publication are complete, with native milestone setup tracked separately. Selected primary-source sections, metadata, and upstream tool introductions have been checked. Next functional milestone: a reviewed multi-scenario evaluation set ([#5](https://github.com/NatTuji/ai-risk-governance-lab/issues/5)), followed by actor/incentive and evidence-record extensions. Detailed mapping applicability remains provisional.

## Blockers and owner decisions

1. **GitHub App authorization:** resolved. Installation/repository listings now include NatTuji and this project, and the LICENSE write succeeded. The earlier HTTP 403 is historical. API publication is available; local CLI credentials were previously invalid, so remote commits may differ from the preserved local Git history. Do not request or paste tokens into chat.
2. **Source review and scope:** NIST AI RMF 1.0/CSF 2.0 selected sections, OWASP 2025 headings/introductions, MITRE Data README, ISO public metadata, agentic publication metadata, and upstream tool introductions are checked. Detailed mappings, full ISO text, ATLAS techniques, agentic controls, and real-world evaluation remain outside this initial check. OWASP has a newer 2026 LLM edition; MVP references deliberately stay pinned to the reviewed 2025 baseline pending migration review.
3. **Publication approval:** resolved for public `NatTuji/ai-risk-governance-lab`, created by the owner after the public-creation instructions. Publishing the prepared project there is authorized. Do not ask again.
4. **License:** resolved; Apache-2.0 explicitly approved and added locally. Do not ask again.

## Verification summary

54 tests pass locally on Python 3.12.14/Linux. Hosted CI passed the suite and both report formats on Python 3.11–3.14. The synthetic case yields ARGL-001–004 and three declared crossings. License text and built-package license metadata are verified. No claim is made about real-world assessment completeness, fully validated mappings, control effectiveness, macOS execution, or production readiness.

## Next concrete tasks

1. Build the manually reviewed multi-scenario evaluation set in [#5](https://github.com/NatTuji/ai-risk-governance-lab/issues/5) before adding rule breadth or agent integration.
2. Review pinned OWASP 2025 mappings and the newer 2026 edition in [#8](https://github.com/NatTuji/ai-risk-governance-lab/issues/8); do not silently migrate identifiers.
3. Configure native milestones ([#11](https://github.com/NatTuji/ai-risk-governance-lab/issues/11)) and main protection ([#12](https://github.com/NatTuji/ai-risk-governance-lab/issues/12)) when a supported administration route is available. Current connector actions cannot create milestones or change branch rules. Protection has not been enabled.
4. Continue actor/incentive ([#6](https://github.com/NatTuji/ai-risk-governance-lab/issues/6)) and evidence-record ([#7](https://github.com/NatTuji/ai-risk-governance-lab/issues/7)) design after evaluation baselines are reviewed.

## Continuity and execution

Read this file, DECISIONS.md, LEARNING_LOG.md, ROADMAP.md, and the remote backlog at the next session's start. GitHub is now the persistent source of truth. Local Git history is preserved and differs from the API-created remote history; compare tree contents explicitly. Do not modify other repositories.

Scheduling tools are available in this session, but no task schedule or background worker has been configured. Recommended future workflow: a weekly status-review task after repository access is stable, with explicit scope and the existing approval boundaries. Execution is currently on demand; no unattended progress is promised.
