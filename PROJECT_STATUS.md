# Project status

Last updated: 2026-11-15 America/Edmonton (host date 2026-11-16 UTC). Active local/remote feature branch: `feat/assessment-cli`. Working project: `/workspace/ai-risk-governance-lab`. Earlier November 16 entries use the host's UTC date for this same local-date session.

## Current state

The first end-to-end capability is implemented and verified locally. The public repository [NatTuji/ai-risk-governance-lab](https://github.com/NatTuji/ai-risk-governance-lab) is approved and its GitHub App installation now grants project access. An Apache-2.0 LICENSE write succeeded and readback matched local text. `main` contains the license and initial charter; `feat/assessment-cli` was created for the working implementation. Feature upload, PR, Issues, and hosted CI verification are in progress. Actual milestones have not been created.

## Completed locally

- Compared three bounded concepts and selected an inspectable deployment assessment CLI.
- Created the charter, architecture diagram, versioned input contract, assessment method, lab threat model, roadmap, contribution guidance, and prioritized issue-ready backlog.
- Implemented strict JSON loading, directed flow graph analysis, five candidate-risk rules, Markdown/JSON output, evidence questions, adoption/inaction questions, and mandatory human review.
- Added a synthetic support-assistant example and exactly reproducible report: four matched categories, three boundary crossings.
- Added 54 automated tests with positive and negative behavioral baselines, malformed-input checks, graph cycles/disconnections, output protection, and report-display checks.
- Built a Python wheel and verified its console script in an isolated environment outside the source checkout. See `docs/verification.md` for scope and limits.
- Prepared CI for Python 3.11–3.14; hosted runs remain unverified.
- Added the approved full Apache-2.0 license and SPDX package metadata; verified the standard license is included in built package metadata.
- Established local commit history: `3229122` charter/plan; `ed5a582` working CLI/tests; later commits record reference uncertainty and session handoff. Use `git log --oneline` for final hashes.

## Active milestone

M1 local demonstration is working and repository bootstrap is verified. Selected primary-source sections, metadata, and upstream tool introductions have been checked. Complete the feature upload, Issues, and hosted CI verification; detailed mapping applicability/evaluation remains follow-up work. See `docs/backlog.md` B01/B03/B07.

## Blockers and owner decisions

1. **GitHub App authorization:** resolved. Installation/repository listings now include NatTuji and this project, and the LICENSE write succeeded. The earlier HTTP 403 is historical. API publication is available; local CLI credentials were previously invalid, so remote commits may differ from the preserved local Git history. Do not request or paste tokens into chat.
2. **Source review and scope:** NIST AI RMF 1.0/CSF 2.0 selected sections, OWASP 2025 headings/introductions, MITRE Data README, ISO public metadata, agentic publication metadata, and upstream tool introductions are checked. Detailed mappings, full ISO text, ATLAS techniques, agentic controls, and real-world evaluation remain outside this initial check. OWASP has a newer 2026 LLM edition; MVP references deliberately stay pinned to the reviewed 2025 baseline pending migration review.
3. **Publication approval:** resolved for public `NatTuji/ai-risk-governance-lab`, created by the owner after the public-creation instructions. Publishing the prepared project there is authorized. Do not ask again.
4. **License:** resolved; Apache-2.0 explicitly approved and added locally. Do not ask again.

## Verification summary

54 tests pass on Python 3.12.14/Linux, including a November 16 prepublication rerun. The synthetic case yields ARGL-001–004 and three declared crossings. Both report formats generate successfully. Approved license text and built-package license metadata are verified. No claim is made about real-world assessment completeness, fully source-verified mappings, hosted CI, macOS execution, or the other Python versions. Mac compatibility is a design target, not a completed test result.

## Next concrete tasks

1. Upload the reviewed tree to the authorized feature branch, verify its contents, and open the implementation PR.
2. Create Issues from the prepared backlog and verify actual hosted CI. Milestone creation has no currently exposed connector action; retain milestone definitions locally until a supported route is available.
3. Record actual PR/Issue/check URLs and reconcile local/remote tree state. Do not claim CI passed merely because a workflow file exists.
4. Extend manually reviewed scenarios (B04) before new rule breadth or agent integration. Then design actor/incentive and evidence-record extensions.

## Continuity and execution

Read this file, DECISIONS.md, LEARNING_LOG.md, ROADMAP.md, and the remote backlog when available at the next session's start. The code and local Git history are the temporary source of truth until GitHub is established. Do not modify other repositories.

Scheduling tools are available in this session, but no task schedule or background worker has been configured. Recommended future workflow: a weekly status-review task after repository access is stable, with explicit scope and the existing approval boundaries. Execution is currently on demand; no unattended progress is promised.
