# Publication workflow

Destination: [NatTuji/ai-risk-governance-lab](https://github.com/NatTuji/ai-risk-governance-lab). The owner created this public repository and explicitly approved Apache-2.0. Publication within this project is authorized; do not request those approvals again. No other repository is in scope.

## Access verification

Account authorization initially succeeded without a repository installation, and a LICENSE write returned HTTP 403. After the owner installed ChatGPT Codex Connector for NatTuji and selected this project, installation/repository listings updated and the same authorized write succeeded. The LICENSE readback matched the local text. No token or credential was shared in chat.

Repository setup uses GitHub connector APIs because local CLI credentials were invalid. The connector exposes no repository-creation or milestone-creation action. The owner completed repository creation; actual milestones remain pending a supported route. Milestone definitions live in ROADMAP.md and backlog issue bodies.

## Initial remote history

- Approved license: `e8b3ab392872d7826bdf474f75cf322f7d9e9e40`.
- Initial charter: `edddbe2d62dad00c884c21f673d52856b28227af`.
- Feature branch: `feat/assessment-cli`, created from the charter commit.

## Remaining publication sequence

1. Upload the reviewed tree as a logical feature commit and verify every blob against the local snapshot. Use expected branch-head checks and never force-update an unexpectedly changed ref.
2. Open the implementation PR and create Issues from the prepared backlog.
3. Verify actual hosted CI, including supported Python versions and both report formats. A workflow configuration is not proof of passing checks.
4. Record actual PR, Issue, commit, and check URLs. Keep PROJECT_STATUS.md current.

API publication creates a different remote commit history from the preserved local Git history. Compare file contents/tree hashes explicitly and record remote commit references. Do not claim an upload, Issue, PR, milestone, or CI run exists before verifying it.
