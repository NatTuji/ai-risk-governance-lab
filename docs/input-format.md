# Input format 1.0

Copy `examples/support-assistant.json` and use synthetic data while learning. All top-level fields below are required. Unknown fields at every level are rejected so a typo cannot silently omit a risk condition.

| Field | Meaning |
| --- | --- |
| `schema_version` | Exactly the string `"1.0"` |
| `name`, `purpose`, `business_value`, `owner` | Nonempty strings, maximum 4,000 characters each; owner can be a role |
| `components` | 1–50 objects: `id`, `name`, `kind`, `trust_zone` |
| `data_flows` | 0–200 objects: `source`, `target`, `data_classification`, `untrusted`, `description` |
| `consequential_decisions` | JSON boolean; true if decisions materially affect people, rights, safety, or significant interests |
| `controls` | 0–7 declared control objects: `id`, `status`, optional `evidence` |

Component IDs must match `[a-z][a-z0-9_-]{0,63}` and be unique. Kinds are `user`, `application`, `model`, `data_store`, or `tool`. A component can represent a person, process endpoint, or service; it need not be a deployed resource. Trust zones are nonempty names chosen by the author. Components with the same zone are assumed to share trust assumptions; the engine cannot validate this choice.

Each flow is directed: `source` and `target` must reference component IDs. Classification is one of `public`, `internal`, `confidential`, or `personal`. If data is both personal and confidential, use `personal`; both classifications trigger the sensitive-boundary rule. These labels are a lab convention, not a legal classification. `untrusted` must be `true` or `false`, not `0`, `1`, or a string. Treat externally supplied prompts and retrieved documents as untrusted unless you can justify otherwise. Classifications and trust are not automatically propagated; describe each edge honestly.

Controls have unique IDs from `human_review`, `access_control`, `data_minimization`, `output_validation`, `monitoring`, `incident_response`, and `supplier_review`. Status is `planned` or `implemented`. Evidence is an optional text reference; it is never opened. An implemented claim does not mean tested, effective, or independently verified.

Files must be UTF-8 JSON, at most 1 MiB. Duplicate JSON keys, NaN, Infinity, unsupported control characters, Unicode direction overrides/isolates, lone surrogates, and excessive parser nesting are rejected. Ordinary non-ASCII text remains supported. Newlines in text are allowed but collapsed and escaped in Markdown output. The format intentionally omits many real-world details; capture those in a human-reviewed threat model rather than assuming the tool covered them.

## CLI contract

`python3 -m ai_risk_lab assess INPUT [--format markdown|json] [--output NEW_FILE]`

Exit 0 means report generation succeeded, **not** that deployment is acceptable. Exit 2 means arguments, input, or file operations failed. Errors go to stderr. Output defaults to Markdown on stdout. Existing output files are protected by exclusive creation; choose a new filename to regenerate.

JSON reports contain the complete normalized input, cross-zone flows, findings, evidence gates, limitations, and value/inaction questions. Each finding carries its rule ID and framework URLs. `decision` remains `human_review_required` and `review_required` remains true. There is no aggregate risk score or approval exit code.
