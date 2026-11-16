# Threat model: the assessment tool

This is a preliminary threat model of the lab itself, separate from the systems users describe. All scenarios here are hypotheses unless an automated test is named as evidence of a narrower behavior.

## Assets and boundaries

Assets include assessment integrity, input confidentiality, local files, framework provenance, and reviewer trust. Boundaries are JSON author → parser, validated data → rule engine, structured report → Markdown viewer, and local checkout → future public repository/CI. The tool inherits the local user's filesystem permissions. It is not a sandbox for malicious local programs or a multi-user service.

| Actor and incentive | Surface and possible path | Current safeguard and evidence | Remaining uncertainty |
| --- | --- | --- | --- |
| Submitter seeking easy approval | Omit flows, label data public, or claim controls are implemented | Reports preserve declarations, always require review, never lower priority from claims; behavioral tests | Cannot detect dishonest or incomplete inventories |
| Malicious input author | Duplicate JSON keys or wrong types hide a risk flag | Strict parser, exact booleans, unknown-field rejection; negative tests | Schema validation cannot prove facts |
| Malicious input author | Insert HTML or Markdown that disguises report content | Escape user text, collapse newlines, never follow evidence references; CLI HTML test | Viewer-specific rendering behavior is not exhaustively tested |
| Malicious input author | Oversized input, excessive nesting, or cyclic flows exhaust resources | 1 MiB file cap, field/list limits, cycle-safe graph traversal; size and cycle tests | File input must be a normal trusted local file; special devices/FIFOs could block; no execution time sandbox |
| Accidental operator error | Save a report over input or another local file | Exclusive output creation, tested against existing and input paths | Caller still chooses destination and local access permissions |
| Contributor or compromised dependency | Alter rule logic or CI to fabricate assurance or expose data | No runtime dependencies; small reviewed changes, verified hosted CI on Python 3.11–3.14, read-only CI permissions, synthetic examples | Action tags are not immutable pins; main-branch protection not configured (tracked in issue #12) |
| Reviewer under time pressure | Interpret no findings or framework references as approval/compliance | Repeated limitations, explicit human-review decision and unassessed residual risk | Warnings alone cannot ensure a disciplined review process |

## Sensitive data handling

The program makes no network requests and does not resolve URLs in evidence references. Reports contain the full input and may be sensitive. `.gitignore` is convenience, not a security boundary: keep real input and output outside the repository, review staged files, and never rely on ignore rules to remove already tracked material. Error messages may reveal local file paths. No secret scanning service has been enabled.

## Before agent augmentation

Treat retrieved documents and tool outputs as untrusted data. Keep evidence references separate from instructions. Restrict permissions and network destinations, require human approval for material actions, log evidence provenance, and evaluate prompt-injection behavior against reviewed scenarios. No agent permissions or external actions are implemented in this milestone.
