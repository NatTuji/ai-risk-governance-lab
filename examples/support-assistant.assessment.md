# AI deployment assessment: Synthetic customer support drafting assistant

**Decision: human review required. This report does not approve deployment.**

Engine: 0.1.0; report schema: 1.0.

## Purpose and value

- Purpose: Draft replies from customer tickets and internal knowledge articles; a support specialist remains responsible for sending replies.
- Expected business value (declared, not verified): Hypothesis: reduce drafting time while preserving accuracy. Compare a limited pilot against manual handling, including review effort and correction rates.
- Accountable owner (declared): Synthetic support operations lead

## Declared system and assets

Components and classifications are supplied by the author. They have not been discovered or verified.

- customer: Customer submitting a support ticket; kind user; trust zone public.
- portal: Support application; kind application; trust zone organization.
- knowledge: Internal knowledge articles; kind data\_store; trust zone organization.
- model: Hosted language model; kind model; trust zone provider.
- ticket\_tool: Ticket update tool; kind tool; trust zone organization.

### Data flows

- customer → portal: Synthetic customer text that may contain adversarial instructions; classification personal; untrusted input: true.
- knowledge → portal: Retrieved internal guidance; trust declaration needs validation against ingestion permissions; classification internal; untrusted input: false.
- portal → model: Prompt containing the ticket and selected guidance; classification personal; untrusted input: true.
- model → portal: Generated draft and suggested ticket actions; classification internal; untrusted input: true.
- portal → ticket\_tool: Apply a ticket update after declared specialist review; enforcement is not verified; classification internal; untrusted input: false.

## Trust boundaries

- customer (public) → portal (organization): personal.
- portal (organization) → model (provider): personal.
- model (provider) → portal (organization): internal.

## Candidate risks

Priorities are rule-based review order, not measured likelihood or residual risk. All scenarios are hypotheses.

### ARGL-001: Untrusted content reaches a model

Priority: **high**. Investigate early because untrusted content can influence model behavior; exploitability is untested.

An adversary could place instructions in untrusted content and attempt to redirect model behavior or disclose context.

Declared facts that triggered this rule:

- Declared flow 1 \(customer -&gt; portal\) is marked untrusted; a declared path reaches a model: customer -&gt; portal -&gt; model.
- Declared flow 3 \(portal -&gt; model\) is marked untrusted; a declared path reaches a model: portal -&gt; model.
- Declared flow 4 \(model -&gt; portal\) is marked untrusted; a declared path reaches a model: model -&gt; portal -&gt; model.

Representative candidate path through declared components: customer → portal → model.

Recommended controls: access\_control, output\_validation, monitoring.

Evidence to request:

- Document which content is untrusted and how instructions are separated from it.
- Run safe prompt-injection evaluations with representative inputs and record failures.
- Verify authorization independently of model-generated instructions.

Provisional conceptual framework references (applicability review pending; not compliance findings):

- OWASP Top 10 for LLM Applications 2025: LLM01:2025 — https://genai.owasp.org/llm-top-10/
- NIST AI RMF 1.0: MAP — https://www.nist.gov/itl/ai-risk-management-framework
- NIST AI RMF 1.0: MEASURE — https://www.nist.gov/itl/ai-risk-management-framework

Residual risk: **not assessed**. Control effectiveness and risk acceptance require a human decision.

### ARGL-002: Sensitive data crosses a declared trust boundary

Priority: **high**. Review handling and authorization before deployment because sensitive data crosses a declared boundary; disclosure is unproven.

Sensitive information could be exposed through inappropriate access, retention, logging, or downstream reuse across this boundary.

Declared facts that triggered this rule:

- Declared personal flow customer -&gt; portal crosses trust zones public -&gt; organization.
- Declared personal flow portal -&gt; model crosses trust zones organization -&gt; provider.

Representative candidate path through declared components: customer → portal.

Recommended controls: data\_minimization, access\_control, supplier\_review.

Evidence to request:

- Verify data classification, permitted recipients, retention, and deletion for each crossing.
- Test authorization and minimization using synthetic sensitive records.
- Determine whether any recipient is a supplier; a different trust zone alone does not establish this.

Provisional conceptual framework references (applicability review pending; not compliance findings):

- OWASP Top 10 for LLM Applications 2025: LLM02:2025 — https://genai.owasp.org/llm-top-10/
- NIST AI RMF 1.0: MAP — https://www.nist.gov/itl/ai-risk-management-framework
- NIST AI RMF 1.0: MANAGE — https://www.nist.gov/itl/ai-risk-management-framework

Residual risk: **not assessed**. Control effectiveness and risk acceptance require a human decision.

### ARGL-003: A model has a declared path to a tool

Priority: **high**. Prioritize permission and action review because model output may reach an action-capable tool; execution authority is unknown.

Manipulated or incorrect model output could induce an excessive or unauthorized tool action if downstream checks fail.

Declared facts that triggered this rule:

- Declared model-to-tool path: model -&gt; portal -&gt; ticket\_tool.

Representative candidate path through declared components: model → portal → ticket\_tool.

Recommended controls: access\_control, human\_review, output\_validation, monitoring.

Evidence to request:

- Document tool permissions, action types, and the identity used for execution.
- Test independent authorization, argument validation, and human approval for material actions.
- Demonstrate denied actions and bounded recovery in a safe test environment.

Provisional conceptual framework references (applicability review pending; not compliance findings):

- OWASP Top 10 for LLM Applications 2025: LLM06:2025 — https://genai.owasp.org/llm-top-10/
- NIST AI RMF 1.0: MANAGE — https://www.nist.gov/itl/ai-risk-management-framework

Residual risk: **not assessed**. Control effectiveness and risk acceptance require a human decision.

### ARGL-004: Model output requires task-specific evaluation

Priority: **medium**. Evaluate reliability for every declared model; consequences depend on the task and downstream use, which this rule does not quantify.

A model could produce incorrect or misleading output that users treat as reliable, harming the intended business process.

Declared facts that triggered this rule:

- Declared model component: model.

Recommended controls: output\_validation, human\_review, monitoring.

Evidence to request:

- Create a manually reviewed evaluation set with task-specific acceptance criteria.
- Measure error rates, limitations, and affected user groups against the existing process.
- Test how uncertainty, corrections, and escalation are presented to users.

Provisional conceptual framework references (applicability review pending; not compliance findings):

- OWASP Top 10 for LLM Applications 2025: LLM09:2025 — https://genai.owasp.org/llm-top-10/
- NIST AI RMF 1.0: MEASURE — https://www.nist.gov/itl/ai-risk-management-framework

Residual risk: **not assessed**. Control effectiveness and risk acceptance require a human decision.

## Declared safeguards

Statuses and evidence references are claims. The tool neither opens references nor verifies effectiveness.

- human\_review: implemented; evidence reference: Synthetic design claim only; no approval enforcement test has been supplied.
- access\_control: planned; evidence reference: Proposed ticket-scoped tool identity.
- monitoring: planned; evidence reference: not supplied.

## Risk of inaction and value evidence

- What evidence supports the declared business value, compared with the current process?
- What productivity, service, or strategic opportunity might be lost by delaying deployment, and how could that be measured?
- Could a bounded pilot, a simpler non-AI alternative, or added safeguards preserve value while evidence is collected?
- Who owns the decision, and when will the adoption and inaction assumptions be reviewed?

## Evidence gates and outstanding decisions

- A human owner validates the system inventory, trust boundaries, data flows, and intended use.
- Reviewers evaluate each candidate scenario, record control effectiveness, and assess residual risk.
- Task performance and business-value evidence are compared with a documented non-AI baseline.
- Accountable humans record outstanding decisions, risk acceptance, and deployment conditions; this report grants no approval.

## Limitations

- Inputs, control statuses, and evidence descriptions are submitter declarations, not independently verified facts.
- Findings are candidate scenarios, not demonstrated vulnerabilities; no finding does not establish safety.
- Graph traversal returns representative declared paths, not an exhaustive attack-path analysis or proof of execution authority.
- Priorities are lab-defined triage heuristics, not likelihood estimates, risk scores, or framework requirements.
- Claimed or planned controls do not remove findings; control effectiveness and residual risk remain unassessed.
- Framework references are selective conceptual mappings, not compliance, certification, or complete framework coverage.
- Reference labels and selected source sections have been checked; local applicability and safeguard mappings remain provisional pending reviewer assessment.
- The report does not approve deployment or determine applicable law; material decisions remain with accountable human reviewers.
