"""Render input as text, never as trusted HTML or executable Markdown."""

import html
import re


def escape(value):
    # Values are text nodes, never HTML attributes. Keeping quotes literal also
    # avoids escaping the '#' in numeric HTML entities during Markdown escaping.
    text = html.escape(str(value), quote=False)
    # Collapse line breaks so supplied text cannot inject a new Markdown section.
    text = " ".join(text.split())
    return re.sub(r"([\\`*_{}\[\]()#+!|>~])", r"\\\1", text)


def render_markdown(report):
    case = report["use_case"]
    lines = [
        f"# AI deployment assessment: {escape(case['name'])}",
        "",
        "**Decision: human review required. This report does not approve deployment.**",
        "",
        f"Engine: {escape(report['engine_version'])}; report schema: {escape(report['report_schema_version'])}.",
        "",
        "## Purpose and value",
        "",
        f"- Purpose: {escape(case['purpose'])}",
        f"- Expected business value (declared, not verified): {escape(case['business_value'])}",
        f"- Accountable owner (declared): {escape(case['owner'])}",
        "",
        "## Declared system and assets",
        "",
        "Components and classifications are supplied by the author. They have not been discovered or verified.",
        "",
    ]
    for component in case["components"]:
        lines.append(f"- {escape(component['id'])}: {escape(component['name'])}; kind {escape(component['kind'])}; trust zone {escape(component['trust_zone'])}.")
    lines += ["", "### Data flows", ""]
    for flow in case["data_flows"]:
        lines.append(f"- {escape(flow['source'])} → {escape(flow['target'])}: {escape(flow['description'])}; classification {escape(flow['data_classification'])}; untrusted input: {str(flow['untrusted']).lower()}.")
    if not case["data_flows"]:
        lines.append("No flows declared; completeness requires review.")
    lines += ["", "## Trust boundaries", ""]
    for boundary in report["trust_boundaries"]:
        lines.append(f"- {escape(boundary['source'])} ({escape(boundary['source_zone'])}) → {escape(boundary['target'])} ({escape(boundary['target_zone'])}): {escape(boundary['data_classification'])}.")
    if not report["trust_boundaries"]:
        lines.append("No cross-zone flows declared. This does not establish that no boundaries exist.")
    lines += ["", "## Candidate risks", "", "Priorities are rule-based review order, not measured likelihood or residual risk. All scenarios are hypotheses.", ""]
    for finding in report["findings"]:
        lines += [f"### {finding['id']}: {escape(finding['title'])}", "", f"Priority: **{finding['priority']}**. {escape(finding['priority_rationale'])}", "", escape(finding["scenario"]), "", "Declared facts that triggered this rule:", ""]
        lines.extend(f"- {escape(fact)}" for fact in finding["trigger_facts"])
        if finding["attack_path"]:
            lines += ["", "Representative candidate path through declared components: " + " → ".join(escape(part) for part in finding["attack_path"]) + "."]
        lines += ["", "Recommended controls: " + ", ".join(escape(item) for item in finding["recommended_controls"]) + ".", "", "Evidence to request:", ""]
        lines.extend(f"- {escape(item)}" for item in finding["evidence_required"])
        lines += ["", "Provisional conceptual framework references (applicability review pending; not compliance findings):", ""]
        for reference in finding["framework_references"]:
            # URLs come from the local rule catalogue, never from a supplied use case.
            lines.append(f"- {escape(reference['framework'])}: {escape(reference['reference'])} — {reference['url']}")
        lines += ["", "Residual risk: **not assessed**. Control effectiveness and risk acceptance require a human decision.", ""]
    if not report["findings"]:
        lines += ["No catalogue rules matched. Coverage is limited; this is not evidence of safety.", ""]
    lines += ["## Declared safeguards", "", "Statuses and evidence references are claims. The tool neither opens references nor verifies effectiveness.", ""]
    for control in case["controls"]:
        lines.append(f"- {escape(control['id'])}: {escape(control['status'])}; evidence reference: {escape(control.get('evidence') or 'not supplied')}.")
    if not case["controls"]:
        lines.append("No safeguards declared.")
    lines += ["", "## Risk of inaction and value evidence", ""]
    lines.extend(f"- {escape(item)}" for item in report["inaction_review"])
    lines += ["", "## Evidence gates and outstanding decisions", ""]
    lines.extend(f"- {escape(item)}" for item in report["evidence_gates"])
    lines += ["", "## Limitations", ""]
    lines.extend(f"- {escape(item)}" for item in report["limitations"])
    return "\n".join(lines).rstrip() + "\n"
