"""Load and validate the small, explicit use-case format.

The input describes a system; validation does not prove that description is true.
We reject unknown fields so that a spelling mistake cannot silently remove a
security-relevant fact. Everything returned is a new, ordinary Python object.
"""

import json
import re
import unicodedata
from pathlib import Path


MAX_INPUT_BYTES = 1_048_576
MAX_TEXT_LENGTH = 4_000
COMPONENT_KINDS = frozenset({"user", "application", "model", "data_store", "tool"})
DATA_CLASSIFICATIONS = frozenset({"public", "internal", "confidential", "personal"})
CONTROL_IDS = frozenset({
    "human_review", "access_control", "data_minimization", "output_validation",
    "monitoring", "incident_response", "supplier_review",
})
CONTROL_STATUSES = frozenset({"planned", "implemented"})
COMPONENT_ID = re.compile(r"[a-z][a-z0-9_-]{0,63}\Z")


class ValidationError(ValueError):
    """The input cannot be interpreted safely using the supported format."""


def _object(value, path, required, optional=frozenset()):
    if not isinstance(value, dict):
        raise ValidationError(f"{path} must be an object")
    if any(not isinstance(key, str) for key in value):
        raise ValidationError(f"{path} field names must be strings")
    missing = required - value.keys()
    unknown = value.keys() - required - optional
    if missing:
        raise ValidationError(f"{path} is missing fields: {', '.join(sorted(missing))}")
    if unknown:
        # Unknown keys are themselves untrusted; keep control characters out of
        # terminal diagnostics as well as successful assessment reports.
        raise ValidationError(f"{path} has unknown fields: {', '.join(ascii(key) for key in sorted(unknown))}")
    return value


def _text(value, path, allow_empty=False):
    if not isinstance(value, str):
        raise ValidationError(f"{path} must be a string")
    if len(value) > MAX_TEXT_LENGTH:
        raise ValidationError(f"{path} must contain at most {MAX_TEXT_LENGTH} characters")
    clean = value.strip()
    if not clean and not allow_empty:
        raise ValidationError(f"{path} must not be empty")
    # Newlines and tabs are useful in descriptions; other control characters are
    # not useful here and can obscure terminal/report content.
    if any(unicodedata.category(char) == "Cc" and char not in "\n\r\t" for char in clean):
        raise ValidationError(f"{path} contains unsupported control characters")
    if any(unicodedata.bidirectional(char) in {"LRE", "RLE", "LRO", "RLO", "PDF", "LRI", "RLI", "FSI", "PDI"} for char in clean):
        raise ValidationError(f"{path} contains unsupported direction-control characters")
    # JSON escape sequences can encode isolated UTF-16 surrogates, which are
    # not Unicode scalar values and cannot be written as UTF-8 report text.
    if any(0xD800 <= ord(char) <= 0xDFFF for char in clean):
        raise ValidationError(f"{path} contains an invalid Unicode surrogate")
    return clean


def _choice(value, choices, path):
    if not isinstance(value, str) or value not in choices:
        raise ValidationError(f"{path} must be one of: {', '.join(sorted(choices))}")
    return value


def _boolean(value, path):
    # bool is a subclass of int in Python; accepting 0/1 here hides bad inputs.
    if type(value) is not bool:
        raise ValidationError(f"{path} must be true or false")
    return value


def _list(value, path, maximum, minimum=0):
    if not isinstance(value, list):
        raise ValidationError(f"{path} must be an array")
    if not minimum <= len(value) <= maximum:
        raise ValidationError(f"{path} must contain {minimum} to {maximum} items")
    return value


def validate_use_case(data):
    """Return a validated copy, or raise ValidationError with a field path.

    Component IDs link data-flow endpoints. A trust zone is a user-declared
    grouping of components with shared trust assumptions; names such as
    ``vendor`` have no special meaning to the engine.
    """
    required = {
        "schema_version", "name", "purpose", "business_value", "owner",
        "components", "data_flows", "consequential_decisions", "controls",
    }
    _object(data, "use_case", required)
    if data["schema_version"] != "1.0":
        raise ValidationError("schema_version must be the string '1.0'")

    result = {"schema_version": "1.0"}
    for field in ("name", "purpose", "business_value", "owner"):
        result[field] = _text(data[field], field)

    components = []
    component_ids = set()
    for index, component in enumerate(_list(data["components"], "components", 50, 1)):
        path = f"components[{index}]"
        _object(component, path, {"id", "name", "kind", "trust_zone"})
        component_id = component["id"]
        if not isinstance(component_id, str) or not COMPONENT_ID.fullmatch(component_id):
            raise ValidationError(f"{path}.id must match [a-z][a-z0-9_-]{{0,63}}")
        if component_id in component_ids:
            raise ValidationError(f"{path}.id duplicates another component ID")
        component_ids.add(component_id)
        components.append({
            "id": component_id,
            "name": _text(component["name"], f"{path}.name"),
            "kind": _choice(component["kind"], COMPONENT_KINDS, f"{path}.kind"),
            "trust_zone": _text(component["trust_zone"], f"{path}.trust_zone"),
        })
    result["components"] = components

    flows = []
    for index, flow in enumerate(_list(data["data_flows"], "data_flows", 200)):
        path = f"data_flows[{index}]"
        _object(flow, path, {
            "source", "target", "data_classification", "untrusted", "description",
        })
        for endpoint in ("source", "target"):
            if not isinstance(flow[endpoint], str) or flow[endpoint] not in component_ids:
                raise ValidationError(f"{path}.{endpoint} must reference a component ID")
        flows.append({
            "source": flow["source"],
            "target": flow["target"],
            "data_classification": _choice(
                flow["data_classification"], DATA_CLASSIFICATIONS,
                f"{path}.data_classification",
            ),
            "untrusted": _boolean(flow["untrusted"], f"{path}.untrusted"),
            "description": _text(flow["description"], f"{path}.description"),
        })
    result["data_flows"] = flows
    result["consequential_decisions"] = _boolean(
        data["consequential_decisions"], "consequential_decisions",
    )

    controls = []
    control_ids = set()
    for index, control in enumerate(_list(data["controls"], "controls", len(CONTROL_IDS))):
        path = f"controls[{index}]"
        _object(control, path, {"id", "status"}, {"evidence"})
        control_id = _choice(control["id"], CONTROL_IDS, f"{path}.id")
        if control_id in control_ids:
            raise ValidationError(f"{path}.id duplicates another control ID")
        control_ids.add(control_id)
        controls.append({
            "id": control_id,
            "status": _choice(control["status"], CONTROL_STATUSES, f"{path}.status"),
            "evidence": _text(control.get("evidence", ""), f"{path}.evidence", allow_empty=True),
        })
    result["controls"] = controls
    return result


def _unique_object(pairs):
    result = {}
    for key, value in pairs:
        if key in result:
            raise ValidationError("JSON contains a duplicate object field")
        result[key] = value
    return result


def _reject_constant(value):
    raise ValidationError(f"JSON constant {value} is not supported")


def load_use_case(path):
    """Read at most 1 MiB of UTF-8 JSON and validate it.

    Input is data only: we never execute it or follow evidence references.
    File-system errors propagate to the CLI so it can report the operation that
    failed. Malformed content is reported as ValidationError.
    """
    with Path(path).open("rb") as source:
        raw = source.read(MAX_INPUT_BYTES + 1)
    if len(raw) > MAX_INPUT_BYTES:
        raise ValidationError(f"input file exceeds {MAX_INPUT_BYTES} bytes")
    try:
        text = raw.decode("utf-8")
        data = json.loads(
            text, object_pairs_hook=_unique_object, parse_constant=_reject_constant,
        )
    except UnicodeDecodeError as error:
        raise ValidationError("input file must contain UTF-8 text") from error
    except ValidationError:
        raise
    except (ValueError, RecursionError) as error:
        raise ValidationError("input file must contain valid, reasonably nested JSON") from error
    return validate_use_case(data)
