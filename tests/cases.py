"""Small synthetic cases, authored independently of the rule implementation."""


def basic_case():
    """A declared internal document assistant, without sensitive data or tools."""
    return {
        "schema_version": "1.0",
        "name": "Synthetic document assistant",
        "purpose": "Draft answers from public reference documents.",
        "business_value": "Reduce time spent locating published procedures.",
        "owner": "Synthetic review team",
        "components": [
            {"id": "app", "name": "Assistant", "kind": "application", "trust_zone": "internal"},
            {"id": "model", "name": "Model", "kind": "model", "trust_zone": "internal"},
        ],
        "data_flows": [
            {
                "source": "app",
                "target": "model",
                "data_classification": "public",
                "untrusted": False,
                "description": "Reviewed reference text and question",
            }
        ],
        "consequential_decisions": False,
        "controls": [],
    }


def add_component(case, component_id, kind, zone="internal"):
    case["components"].append(
        {"id": component_id, "name": component_id, "kind": kind, "trust_zone": zone}
    )


def add_flow(case, source, target, classification="public", untrusted=False):
    case["data_flows"].append(
        {
            "source": source,
            "target": target,
            "data_classification": classification,
            "untrusted": untrusted,
            "description": f"Synthetic transfer from {source} to {target}",
        }
    )
