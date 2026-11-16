# Initial issue backlog

Prepared issue bodies for GitHub; issue URLs will be recorded here and in PROJECT_STATUS.md after creation. Public `NatTuji/ai-risk-governance-lab` and Apache-2.0 are approved, app authorization is verified, and the initial license/charter are published. Milestone names below are planning definitions until actual GitHub milestone creation is verified.

## Milestones to create

- **M1 — Traceable assessment and publication:** local working capability plus verified repository, license, CI, and issue management.
- **M2 — Structured adversarial review:** reviewed scenarios, actors, control evidence, and reproducible evaluation.
- **M3 — Evaluated agent assistance:** constrained assistance benchmarked against human-reviewed cases.

## B01 — Establish the approved GitHub repository

Priority: P0. Milestone: M1. Labels: project-management, blocked.

The owner-created public repository and app authorization are verified; license and charter are published. Upload the implementation as logical branches/commits and create the initial PR. Do not change any other repository.

Acceptance: verified remote URL, account and visibility; approved license; initial commits and PR visible; no unrelated repo writes. Account, visibility, license, and app authorization decisions are resolved.

## B02 — Deliver the local deterministic MVP

Priority: P0. Milestone: M1. Labels: enhancement, testing. Local state: implemented and tested; close remotely only after the code is published and checks are verified.

Implement strict JSON validation, declared boundaries, five explainable rules, Markdown/JSON reporting, and a synthetic example. Retain uncertainty, human accountability, and inaction questions.

Acceptance: CLI completes both formats; independent positive/negative baselines pass; output is protected; sample report is reproducible; no runtime model/network dependency.

## B03 — Verify hosted CI and contribution workflow

Priority: P0. Milestone: M1. Labels: ci, testing.

Run the prepared workflow in the authorized repository, verify supported Python versions, and review the first PR. Consider immutable action pins and branch protection after the repository exists.

Acceptance: actual hosted CI run URLs and successful supported-version results; branch/PR instructions match the repository. Local tests do not satisfy hosted-CI acceptance.

## B04 — Build a reviewed multi-scenario evaluation set

Priority: P1. Milestone: M2. Labels: evaluation, research.

Add at least five distinct synthetic organizational use cases: internal knowledge assistant, customer support tool, consequential HR workflow, code assistant, and bounded security triage. Define expected findings and limitations manually before running the engine. Include negative cases and plausible missing risks.

Acceptance: reviewer rationale for each expected finding and deliberate nonfinding; rule-level false-positive/false-negative analysis on the reviewed set; explicit gaps. Do not claim general accuracy from a small synthetic dataset.

## B05 — Model actors, incentives, prerequisites, and misuse

Priority: P1. Milestone: M2. Labels: threat-modeling, enhancement.

Design a versioned extension for actors, assets, action permissions, prerequisites, and misuse scenarios. Compare selected scenarios with primary MITRE ATLAS and OWASP agentic guidance. Avoid treating a data-flow path as proven execution authority.

Acceptance: documented schema trade-offs; direct and indirect attack scenarios; evidence-backed versus hypothetical distinction; reference applicability reviewed; backwards compatibility decision recorded.

## B06 — Add human-reviewed evidence and residual-risk records

Priority: P1. Milestone: M2. Labels: governance, enhancement.

Design evidence metadata with reviewer, date, source, scope, result, and limitations. Keep declarations, observations, proposed mitigations, and authorized risk acceptance distinct. Do not fetch arbitrary URLs or make automatic approval decisions.

Acceptance: example of accepted and rejected hypotheses, failed control evidence, outstanding decisions, and human-owned residual-risk rationale. Record evidence provenance without committing sensitive material.

## B07 — Review framework applicability and catalogue coverage

Priority: P1. Milestone: M2. Labels: research, documentation.

Review conceptual mappings against primary sources and document exclusions. Initial source-label/metadata checks are complete, but local applicability remains provisional. Compare the newer OWASP 2026 LLM edition with the pinned 2025 baseline before migration. Evaluate NIST CSF, ATLAS, ISO/IEC 42001, and agentic guidance for specific additions; do not add references merely for breadth. Have a qualified reviewer assess the interpretation before stronger organizational claims.

Acceptance: source/version/access log, rationale for each mapping, normative-status distinction, and explicit limits where full text or expertise is unavailable.

## B08 — Evaluate a constrained agent-assistance experiment

Priority: P2. Milestone: M3. Labels: agents, evaluation. Dependency: B04–B07.

Prototype one bounded function, such as proposing evidence questions from approved documents. Compare it with the manual baseline and deterministic engine. Evaluate hallucinated references, missed risks, prompt injection, and action boundaries.

Acceptance: recorded evaluation design/results and error analysis; untrusted content separation; least privilege; human approval for material actions; costs approved before paid API use.

## B09 — Produce a professional walkthrough

Priority: P2. Milestone: M2. Labels: documentation, portfolio.

Create a concise realistic demonstration showing the input, architecture, risk reasoning, evidence gaps, verification, and owner decisions. Explain what the artifact demonstrates and what remains a prototype.

Acceptance: reproducible walkthrough with synthetic data; clear scope and uncertainty; owner can explain the main components and at least one meaningful limitation in their own words. Do not assert mastery without participation.
