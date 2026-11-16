"""Small, inspectable risk-screening rules over a declared deployment graph.

The rules generate hypotheses for a human reviewer. A graph path is a declared
data flow, not evidence that an attacker can execute the path successfully.
"""

from collections import deque
from copy import deepcopy


ENGINE_VERSION = "0.1.0"

_NIST_URL = "https://www.nist.gov/itl/ai-risk-management-framework"
_OWASP_URL = "https://genai.owasp.org/llm-top-10/"


def _nist(function):
    return {"framework": "NIST AI RMF 1.0", "reference": function, "url": _NIST_URL}


def _owasp(identifier):
    return {"framework": "OWASP Top 10 for LLM Applications 2025", "reference": identifier, "url": _OWASP_URL}


def _path_to_kind(start, desired_kind, components, adjacency):
    """Return one shortest directed path, including start, or None.

    A visited set makes this breadth-first search terminate even if declared
    flows contain cycles. Input order breaks ties deterministically.
    """
    pending = deque([[start]])
    visited = {start}
    while pending:
        path = pending.popleft()
        current = path[-1]
        if components[current]["kind"] == desired_kind:
            return path
        for target in adjacency[current]:
            if target not in visited:
                visited.add(target)
                pending.append(path + [target])
    return None


def _finding(identifier, title, priority, rationale, scenario, facts, path, references, controls, evidence):
    return {
        "id": identifier,
        "title": title,
        "priority": priority,
        "priority_rationale": rationale,
        "scenario": scenario,
        "trigger_facts": facts,
        "attack_path": path,
        "framework_references": references,
        "recommended_controls": controls,
        "evidence_required": evidence,
        "scenario_status": "hypothesis",
        "residual_risk": "not_assessed",
    }


def assess(use_case):
    """Assess a validated use case without network calls, execution, or mutation.

    One finding is emitted per matching rule. Priorities are this lab's triage
    heuristics; neither claimed controls nor framework mappings prove safety.
    """
    components = {component["id"]: component for component in use_case["components"]}
    adjacency = {identifier: [] for identifier in components}
    for flow in use_case["data_flows"]:
        adjacency[flow["source"]].append(flow["target"])

    boundaries = []
    for flow in use_case["data_flows"]:
        source_zone = components[flow["source"]]["trust_zone"]
        target_zone = components[flow["target"]]["trust_zone"]
        if source_zone != target_zone:
            boundaries.append({
                "source": flow["source"],
                "target": flow["target"],
                "source_zone": source_zone,
                "target_zone": target_zone,
                "data_classification": flow["data_classification"],
                "description": flow["description"],
            })

    findings = []

    # ARGL-001: untrusted material may reach a model indirectly through an app
    # or retrieval store. Matching only direct edges would miss that boundary.
    injection_paths = []
    injection_facts = []
    for index, flow in enumerate(use_case["data_flows"], start=1):
        if not flow["untrusted"]:
            continue
        continuation = _path_to_kind(flow["target"], "model", components, adjacency)
        if continuation is not None:
            path = [flow["source"]] + continuation
            injection_paths.append(path)
            injection_facts.append(
                f"Declared flow {index} ({flow['source']} -> {flow['target']}) is marked untrusted; "
                f"a declared path reaches a model: {' -> '.join(path)}."
            )
    if injection_paths:
        findings.append(_finding(
            "ARGL-001", "Untrusted content reaches a model", "high",
            "Investigate early because untrusted content can influence model behavior; exploitability is untested.",
            "An adversary could place instructions in untrusted content and attempt to redirect model behavior or disclose context.",
            injection_facts, injection_paths[0], [_owasp("LLM01:2025"), _nist("MAP"), _nist("MEASURE")],
            ["access_control", "output_validation", "monitoring"],
            ["Document which content is untrusted and how instructions are separated from it.",
             "Run safe prompt-injection evaluations with representative inputs and record failures.",
             "Verify authorization independently of model-generated instructions."],
        ))

    sensitive_boundaries = [boundary for boundary in boundaries
                            if boundary["data_classification"] in {"confidential", "personal"}]
    if sensitive_boundaries:
        facts = [
            f"Declared {boundary['data_classification']} flow {boundary['source']} -> {boundary['target']} "
            f"crosses trust zones {boundary['source_zone']} -> {boundary['target_zone']}."
            for boundary in sensitive_boundaries
        ]
        first = sensitive_boundaries[0]
        findings.append(_finding(
            "ARGL-002", "Sensitive data crosses a declared trust boundary", "high",
            "Review handling and authorization before deployment because sensitive data crosses a declared boundary; disclosure is unproven.",
            "Sensitive information could be exposed through inappropriate access, retention, logging, or downstream reuse across this boundary.",
            facts, [first["source"], first["target"]], [_owasp("LLM02:2025"), _nist("MAP"), _nist("MANAGE")],
            ["data_minimization", "access_control", "supplier_review"],
            ["Verify data classification, permitted recipients, retention, and deletion for each crossing.",
             "Test authorization and minimization using synthetic sensitive records.",
             "Determine whether any recipient is a supplier; a different trust zone alone does not establish this."],
        ))

    models = [identifier for identifier, component in components.items() if component["kind"] == "model"]
    tool_paths = []
    for model in models:
        path = _path_to_kind(model, "tool", components, adjacency)
        if path is not None:
            tool_paths.append(path)
    if tool_paths:
        findings.append(_finding(
            "ARGL-003", "A model has a declared path to a tool", "high",
            "Prioritize permission and action review because model output may reach an action-capable tool; execution authority is unknown.",
            "Manipulated or incorrect model output could induce an excessive or unauthorized tool action if downstream checks fail.",
            [f"Declared model-to-tool path: {' -> '.join(path)}." for path in tool_paths], tool_paths[0],
            [_owasp("LLM06:2025"), _nist("MANAGE")],
            ["access_control", "human_review", "output_validation", "monitoring"],
            ["Document tool permissions, action types, and the identity used for execution.",
             "Test independent authorization, argument validation, and human approval for material actions.",
             "Demonstrate denied actions and bounded recovery in a safe test environment."],
        ))

    if models:
        findings.append(_finding(
            "ARGL-004", "Model output requires task-specific evaluation", "medium",
            "Evaluate reliability for every declared model; consequences depend on the task and downstream use, which this rule does not quantify.",
            "A model could produce incorrect or misleading output that users treat as reliable, harming the intended business process.",
            [f"Declared model component: {identifier}." for identifier in models], [],
            [_owasp("LLM09:2025"), _nist("MEASURE")],
            ["output_validation", "human_review", "monitoring"],
            ["Create a manually reviewed evaluation set with task-specific acceptance criteria.",
             "Measure error rates, limitations, and affected user groups against the existing process.",
             "Test how uncertainty, corrections, and escalation are presented to users."],
        ))

    if use_case["consequential_decisions"]:
        findings.append(_finding(
            "ARGL-005", "Consequential decisions require accountable oversight", "high",
            "Review before deployment because the submitter declares consequential decisions; the tool does not determine legal obligations.",
            "An incorrect, unfair, or unreviewable decision could materially affect people or the organization without effective recourse.",
            ["The submitter declared consequential_decisions=true."], [], [_nist("GOVERN"), _nist("MAP"), _nist("MEASURE")],
            ["human_review", "monitoring", "incident_response"],
            ["Name an accountable decision owner and define which decisions require human review.",
             "Document affected stakeholders, appeal routes, and impact and fairness evaluation.",
             "Have an appropriate reviewer determine applicable legal and contractual duties."],
        ))

    return {
        "report_schema_version": "1.0",
        "engine_version": ENGINE_VERSION,
        "use_case": deepcopy(use_case),
        "trust_boundaries": boundaries,
        "findings": findings,
        "review_required": True,
        "decision": "human_review_required",
        "limitations": [
            "Inputs, control statuses, and evidence descriptions are submitter declarations, not independently verified facts.",
            "Findings are candidate scenarios, not demonstrated vulnerabilities; no finding does not establish safety.",
            "Graph traversal returns representative declared paths, not an exhaustive attack-path analysis or proof of execution authority.",
            "Priorities are lab-defined triage heuristics, not likelihood estimates, risk scores, or framework requirements.",
            "Claimed or planned controls do not remove findings; control effectiveness and residual risk remain unassessed.",
            "Framework references are selective conceptual mappings, not compliance, certification, or complete framework coverage.",
            "Reference labels and selected source sections have been checked; local applicability and safeguard mappings remain provisional pending reviewer assessment.",
            "The report does not approve deployment or determine applicable law; material decisions remain with accountable human reviewers.",
        ],
        "inaction_review": [
            "What evidence supports the declared business value, compared with the current process?",
            "What productivity, service, or strategic opportunity might be lost by delaying deployment, and how could that be measured?",
            "Could a bounded pilot, a simpler non-AI alternative, or added safeguards preserve value while evidence is collected?",
            "Who owns the decision, and when will the adoption and inaction assumptions be reviewed?",
        ],
        "evidence_gates": [
            "A human owner validates the system inventory, trust boundaries, data flows, and intended use.",
            "Reviewers evaluate each candidate scenario, record control effectiveness, and assess residual risk.",
            "Task performance and business-value evidence are compared with a documented non-AI baseline.",
            "Accountable humans record outstanding decisions, risk acceptance, and deployment conditions; this report grants no approval.",
        ],
    }
