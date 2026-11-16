# Learning log

## 2026-11-15 — Initial implementation

### Concepts introduced

- **Input contract:** a versioned description of valid data. Rejecting an unknown field catches a typo such as `untrustd` rather than ignoring a security-relevant fact.
- **Directed graph:** components are nodes and data flows are edges. Direction matters: a model receiving text from a tool does not automatically imply it can operate that tool.
- **Trust boundary:** a transition between declared trust assumptions. It does not establish an exploitable weakness or prove the data is leaving the organization.
- **Breadth-first search:** explore neighboring nodes in layers. A visited set prevents looping through cycles.
- **Deterministic rule:** the same normalized input produces the same report. Reproducibility lets a reviewer inspect why a finding appeared.
- **Evidence versus assertion:** claiming human review exists is different from demonstrating that an unauthorized action is blocked.
- **Behavioral test:** state what must happen in a known situation, including when a rule should not trigger. Passing tests does not prove complete real-world coverage.
- **Framework mapping:** a reference helps organize reasoning; it does not establish conformity, legal compliance, or certification.

### Lessons from implementation and review

Checking only direct untrusted → model edges misses indirect paths. Checking every tool in the inventory creates false conclusions about disconnected tools. Both mistakes are covered by graph tests. Duplicate JSON keys are rejected because the default parser silently keeps the last value. File writes use exclusive creation to protect existing work. Markdown escaping prevents declared content from becoming trusted report markup.

Independent review found that escaped lone Unicode surrogates can be valid parser input but cannot be written as normal UTF-8 report text. The validator rejects them explicitly; a regression test covers the correction.

Focused display tests also reproduced a quote-escaping bug and accepted direction-control characters that could disguise report text. Text-node HTML escaping now preserves ordinary quotes; the validator rejects direction overrides/isolates and terminal controls while allowing ordinary multilingual text. These fixes concern report integrity, not a demonstrated target-system vulnerability.

GitHub authentication failure was confirmed by HTTP 401 rather than inferred from a missing tool. The project can advance locally, but remote inspection, publishing, and hosted CI remain unverified.

Primary-source fetching also failed to complete because network permission remained pending and the request was aborted. Known reference names are useful starting points, but they are not evidence of a current source review. Framework mappings remain visibly provisional; existing-tool comparisons are hypotheses to verify, not a completed code audit.

### Optional experiment

Copy the synthetic example outside the checkout. Remove the flow from `portal` to `ticket_tool`, leaving the tool component in the inventory. Generate a new report. ARGL-003 should disappear because the model no longer has a declared path to a tool. ARGL-004 should remain. Explain why neither result tells us whether the real system is secure.

### Questions to revisit

How could a reviewer discover a deliberately omitted flow? What evidence would demonstrate that human review actually constrains tool execution? When does a representative path hide important branching behavior? What would justify a residual-risk rating rather than simply a review priority?

Owner mastery has not yet been assessed. These are introduced concepts and suggested exercises, not a claim that learning outcomes have already been achieved.

## 2026-11-16 — Connection verification

The connector now verifies the authenticated GitHub identity as `NatTuji`, but no owned or owner-filtered repositories were returned. The sole reported app installation belongs to another account with selected-repository access. No remote changes were made.

Authentication answers who is connected. Authorization determines which repositories an app can access. A successful identity check does not prove repository permission, and an empty scoped listing does not prove that no repository exists. The remaining connection task is to authorize the intended account/repository, then repeat the read-only repository check. No code changed; the previous 54-test result remains the last code verification, not a new test run.

The owner clarified that this will be their first repository. That explains the empty lists; it should not be treated as a connection failure. We will verify permissions after creation. The available connector has no repository-creation action, so the documented fallback is a one-time GitHub UI step with explicit visibility selection. No remote action or new code verification occurred.

## 2026-11-16 — Repository discovery and licensed publication attempt

The owner created the public project repository and approved Apache-2.0. Direct lookup found it even though list endpoints returned empty. The repository metadata reports the user's push permissions, but the app's LICENSE write failed with HTTP 403 Resource not accessible by integration. No content was uploaded. The next access step is app authorization for the intended repository, rather than repeated public/license approval.

Added the exact standard license and verified SPDX metadata and license inclusion in a package build. License selection changes reuse rights; build metadata makes those rights visible to package tooling. A prepublication review ran all 54 tests successfully and found no apparent secrets or sensitive examples. No runtime logic changed in this step.

Read-only GitHub access also enabled a bounded primary-source check: OWASP's 2025 preface and selected vulnerability introductions confirm the identifiers and concepts used by the rules, while MITRE's Data README confirms ATLAS's role. Verified reference labels are different from validated local risk mappings. NIST and ISO source verification remain unfinished.

## 2026-11-15 America/Edmonton — App installation and publication

The account authorization and repository installation are separate. After the owner installed the app for NatTuji and selected this repository, installation/repository listings updated and the LICENSE write succeeded. Its readback matched the local text. Earlier November 16 entries use the host UTC date for this same local-date session.

The public repository now has a licensed charter on `main` and a feature branch. An API-created commit records the same source files through a different remote history; local Git history is preserved and content must be compared explicitly rather than assuming hashes match.

Primary web sources now confirm NIST framework function names and publication editions, ISO public metadata, and agentic publication metadata. Upstream README introductions support the project-selection comparison. OWASP's newer 2026 LLM edition is a maintenance consideration; the application remains pinned to its reviewed 2025 references until a separate migration review. Source verification does not validate every local mapping or prove control effectiveness.

Publication completed: PR #1 merged after all four hosted Python jobs and both CLI report commands passed. Exact blob matching confirmed the uploaded files matched the reviewed local snapshot. Issues #2–#4 closed as completed; #5–#12 retain evaluation, threat-modeling, governance, demonstration, and repository-hardening work.

The owner asked about the "main branch isn't protected" banner. Tests running and branch protection are different: CI produces results, while a branch rule can require those results before merging and block force pushes/deletion. Public visibility does not give strangers write access. For a solo project, required CI and pull requests are useful without requiring another person's approval. Protection remains unconfigured and is tracked in #12; the current connector lacks administration write actions.

The owner then authorized enforcement. Prepared an active main-only importable ruleset, using the four exact observed check names and GitHub Actions integration ID 15368. An independent review checked the schema and solo-maintainer semantics against primary GitHub documentation. No bypass actors are configured; zero approvals requires a PR record without requiring a second reviewer. The prepared file is a policy artifact, not evidence of active enforcement. API readback still shows no rulesets; installation requires the owner's final UI import because administration writes and browser control are unavailable.
