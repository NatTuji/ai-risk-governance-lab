# Assessment method

## Evidence and claims

This tool performs a preliminary screening of a declared deployment. It is not a completed threat model or a risk acceptance process.

Keep four levels distinct:

1. **Declaration:** an author says that a component, flow, owner, or safeguard exists.
2. **Hypothesis:** a rule suggests a failure or misuse scenario based on that declaration.
3. **Observed evidence:** a reviewer inspects a test, configuration, or other artifact and records what it actually demonstrates. This milestone requests such evidence but does not validate it.
4. **Decision:** an authorized human records how uncertainty and remaining risk will be handled. The CLI does not make this decision.

All generated findings have `scenario_status: hypothesis` and `residual_risk: not_assessed`. Controls are `planned` or `implemented` declarations; neither status reduces a rule's priority. A future evidence workflow must preserve who reviewed what, when, under which assumptions, and with which limitations.

## Rule catalogue 0.1.0

| Rule | Trigger | Priority and reasoning | Selected conceptual references |
| --- | --- | --- | --- |
| ARGL-001 | An untrusted edge has a directed continuation to a model | High: investigate possible instruction manipulation early | OWASP LLM01:2025; NIST AI RMF MAP, MEASURE |
| ARGL-002 | A confidential or personal flow crosses different declared trust zones | High: review recipients and handling before exposure | OWASP LLM02:2025; NIST AI RMF MAP, MANAGE |
| ARGL-003 | A model has a directed path to a tool | High: review permissions and downstream action checks | OWASP LLM06:2025; NIST AI RMF MANAGE |
| ARGL-004 | Any model is declared | Medium: task-specific performance evidence is needed | OWASP LLM09:2025; NIST AI RMF MEASURE |
| ARGL-005 | The author declares consequential decisions | High: review material impacts, recourse, and accountability | NIST AI RMF GOVERN, MAP, MEASURE |

These are this project's rules and priorities, not requirements extracted from a standard. Selected primary-source sections confirm the referenced labels and concepts; local applicability and safeguard mappings remain provisional pending reviewer assessment. OWASP references are explicitly pinned to the reviewed 2025 edition; a 2026 migration requires a separate review. High and medium indicate review order; they do not quantify probability, severity, financial exposure, or acceptable residual risk. LLM references are most applicable to LLM deployments; the input's generic `model` kind does not verify model type. Sensitive flows and consequential decisions can trigger without a model, so reviewers must assess reference applicability.

The rules intentionally omit many categories: training-data poisoning, model theft, denial of service, model-specific safety behavior, most bias analysis, and jurisdiction-specific duties. No matching rules means limited catalogue coverage, not low risk.

## Review workflow

1. Confirm the intended use, business-value hypothesis, affected people, data inventory, and accountable owner.
2. Check that the declared system includes relevant dependencies, ingress points, identities, and downstream actions.
3. For each candidate, record relevant actors, incentives, prerequisites, plausible harm, and existing safeguards. Reject inapplicable hypotheses with a rationale rather than deleting their history.
4. Collect evidence appropriate to the claim: authorization denial tests, synthetic prompt-injection evaluations, retention configuration, reviewed task performance, and approval enforcement tests.
5. Assess residual risk in context. Record an authorized decision, conditions, review date, and escalation/rollback owner. This decision belongs outside the automatic CLI output.

The initial report does not capture a full actor/incentive model or structured review decisions. Those are the next threat-modeling milestone.

## Adoption and inaction

Business value is a hypothesis to test, not an automatic justification for accepting harm. Compare the current process with a bounded pilot: task completion time, error rates, review effort, affected groups, operating cost, and reversibility. Record what delay could cost and what a simpler non-AI alternative could achieve. This milestone generates review questions, not an ROI estimate.

## Verification strategy

Behavioral baselines are hand-authored rather than generated from the engine. A sensitive, untrusted, consequential model-to-tool workflow should trigger all five categories. An internal model used without declared untrusted flows, sensitive boundaries, or tools should trigger only output evaluation. A nonmodel workflow may have no findings but must still require review.

Negative cases matter: a disconnected tool should not imply model authority, and a cycle disconnected from a model should not imply prompt injection. Input tests protect the contract; CLI tests verify the actual user interface. Passing these tests shows the programmed rules behave as specified. It does not validate real-world completeness or control effectiveness. A future domain-expert review and larger scenario set are needed before organizational use.
