# Decisions

## ADR-001 — Start with a deterministic deployment assessment CLI

Date: 2026-11-15. Status: selected for the initial local MVP.

Choose the assessment CLI over a standalone adversarial harness or evidence tracker. It integrates system modeling, security scenarios, governance questions, and an inspectable implementation on a modest laptop. Existing harnesses can later supply tests; evidence records can later grow from findings. See `docs/architecture.md` for the comparison.

## ADR-002 — Use Python 3.11+ and the standard library

Date: 2026-11-15. Status: implemented.

Use JSON, dictionaries, breadth-first graph search, argparse, and unittest. Avoid YAML parsers, web frameworks, databases, and model services until there is a demonstrated need. This lowers installation and maintenance effort. Packaging uses setuptools only if the optional install workflow is chosen.

## ADR-003 — Preserve uncertainty and human accountability

Date: 2026-11-15. Status: implemented.

Findings are hypotheses based on declared facts. Priority is a lab heuristic. Safeguards are claims; residual risk is unassessed. No report automatically approves a deployment, including one with zero findings. This sacrifices the appearance of a simple score to avoid unsupported precision.

## ADR-004 — Map a selected subset, do not imply compliance

Date: 2026-11-15. Status: selected source sections and labels verified; local mappings remain provisional at NIST AI RMF function and OWASP LLM category level.

Research wider frameworks but only emit references that can be explained. NIST CSF, MITRE ATLAS, OWASP agentic guidance, and ISO/IEC 42001 inform later work; they are not fully mapped by this release. Do not bundle licensed source text or invent inaccessible ISO clause requirements.

## ADR-005 — Validate strictly and protect report output

Date: 2026-11-15. Status: implemented.

Reject unknown fields, duplicate JSON keys, malformed types, invalid endpoints, and bounded-size violations. Escape user-controlled Markdown/HTML. Never execute input or open evidence links. Refuse overwrites rather than add a destructive default. Strict schemas require versioning for future extensions.

## ADR-006 — Prepare locally while GitHub is blocked

Date: 2026-11-15. Status: temporary limitation.

GitHub CLI returned HTTP 401; no connected GitHub tools became available during the initial check. Do not infer account identity or repository availability. Build in a new isolated local repository, prepare issue bodies, and defer remote creation until access, account, and public visibility are approved. Other user repositories are outside scope. Local commit metadata uses a project identity rather than a discovered personal email.

Update 2026-11-16: connector authentication now succeeds as `NatTuji`. Repository listings returned empty and the sole reported installation belongs to another account with selected-repository access. Keep publication blocked until authorization for the intended repository is established and public creation is approved. Do not infer repository absence from an empty connector result.

Owner clarification 2026-11-16: this will be their first repository, so empty lists are expected. No create-repository action is available in the connector, the CLI reports invalid credentials, and no browser tool is available. Prepare a one-time manual creation step in `docs/publishing.md`; verify actual access after creation rather than diagnosing empty lists as an access failure.

## ADR-007 — License under Apache-2.0

Date: 2026-11-15; approved and applied locally 2026-11-16. Status: implemented.

The owner approved Apache-2.0 for permissive reuse and explicit patent terms. Added the unchanged standard license from the system Apache-2.0 text, with SPDX package metadata and inclusion in the wheel. Build tooling now requires setuptools>=77.0.3 for standardized license metadata; the runtime remains dependency-free. Referenced standards and upstream projects retain their own terms.

## ADR-008 — Publish only after app authorization succeeds

Date: initial host record 2026-11-16 UTC; resolved in the 2026-11-15 America/Edmonton session. Status: access verified.

The owner created public `NatTuji/ai-risk-governance-lab`. Direct metadata lookup verifies its identity and public status even though connector list endpoints still return empty. Empty contents/refs confirm it has no initial commit. A LICENSE creation attempt returned HTTP 403 Resource not accessible by integration. Do not equate the authenticated user's push permission with app authorization. Await the owner granting app access to this repository; retain approved publication and licensing decisions without requesting them again. No other repositories are in scope.

Resolution: after the owner installed ChatGPT Codex Connector for NatTuji, installation/repository listings included the intended account/project. The approved LICENSE write succeeded and readback matched the local standard license. `main` now contains a license and charter; feature publication may proceed. The earlier failure remains an audit record, not a current blocker.

Publication result: feature PR #1 merged at `4bb17f710ffb180e81ac032779d141caf4b68fd8` after exact source-tree verification, a separate review, and successful Python 3.11–3.14 hosted checks. Initial setup Issues #2–#4 closed. API-created remote history differs from the preserved local history; content verification is the continuity mechanism until a normal authenticated Git fetch is available.

## ADR-009 — Keep framework editions explicit

Date: 2026-11-15 America/Edmonton. Status: selected.

Research verified NIST function names, selected OWASP 2025 categories, and public metadata for other sources. OWASP now advertises a 2026 LLM Top 10. Keep the working MVP pinned to its reviewed 2025 references; assess semantic changes in a separate issue before migration. Verified labels do not prove local mapping validity or control effectiveness.
