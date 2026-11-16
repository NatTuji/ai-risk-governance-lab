# Publication workflow

Destination: [NatTuji/ai-risk-governance-lab](https://github.com/NatTuji/ai-risk-governance-lab). The owner created this public repository and explicitly approved Apache-2.0. Publication within this project is authorized; do not request those approvals again. No other repository is in scope.

## Access verification

Account authorization initially succeeded without a repository installation, and a LICENSE write returned HTTP 403. After the owner installed ChatGPT Codex Connector for NatTuji and selected this project, installation/repository listings updated and the same authorized write succeeded. The LICENSE readback matched the local text. No token or credential was shared in chat.

Repository setup uses GitHub connector APIs because local CLI credentials were invalid. The connector exposes no repository-creation or milestone-creation action. The owner completed repository creation; actual milestones remain pending a supported route. Milestone definitions live in ROADMAP.md and backlog issue bodies.

## Initial remote history

- Approved license: `e8b3ab392872d7826bdf474f75cf322f7d9e9e40`.
- Initial charter: `edddbe2d62dad00c884c21f673d52856b28227af`.
- Feature branch: `feat/assessment-cli`, created from the charter commit.

## Verified publication result

The first implementation commit `75a6c528fb57a4d814b60e99266f4a0eb4eee594` contains tree `3bfb7662c416804dd3849b33190c55b5c2b14c69`. All 33 blobs matched the reviewed local snapshot. [PR #1](https://github.com/NatTuji/ai-risk-governance-lab/pull/1) merged at `4bb17f710ffb180e81ac032779d141caf4b68fd8` after a separate review and successful [hosted CI](https://github.com/NatTuji/ai-risk-governance-lab/actions/runs/43805777964). The four Python jobs (3.11–3.14) and their test/report steps all succeeded.

Eleven Issues (#2–#12) were created. #2–#4 closed with the implementation merge; #5–#12 remain open. Native milestones and main protection are still unconfigured, tracked in #11 and #12. A minor documentation follow-up records these observed results on `main`; it does not change runtime behavior. Subsequent substantive changes should continue through feature branches and PRs.

API publication creates a different remote commit history from the preserved local Git history. Compare file contents/tree hashes explicitly and record remote commit references. Do not claim an upload, Issue, PR, milestone, or CI run exists before verifying it.
