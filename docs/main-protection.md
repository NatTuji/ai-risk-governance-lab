# Enforce safeguards on main

The owner authorized these settings on 2026-11-15 America/Edmonton. The importable configuration is [.github/rulesets/main.json](../.github/rulesets/main.json). **Committing that file does not activate repository settings.** Import and save it in GitHub, then verify effective rules. Issue [#12](https://github.com/NatTuji/ai-risk-governance-lab/issues/12) remains open until enforcement is verified.

## Prepared policy

| Setting | Prepared behavior |
| --- | --- |
| Target | Exactly `refs/heads/main` |
| Enforcement | Active when saved in GitHub |
| Bypass actors | Empty; no administrator, app, team, or user exception |
| Pull requests | Required; zero independent approvals so a solo maintainer can merge |
| Review conversations | Must be resolved |
| Status checks | All four `test (3.11)` through `test (3.14)` contexts must satisfy GitHub's required-check policy |
| Check source | GitHub Actions, integration ID 15368, verified from this repository's actual check runs |
| Up-to-date requirement | Strict: changes are tested against the current main branch |
| History rewriting/deletion | Blocked by `non_fast_forward` and `deletion` rules |

No `update` rule is included: that rule would block ordinary updates for everyone without bypass permission, including the intended merge workflow. No paid service, deployment requirement, or extra reviewer is introduced. Repository administrators can still edit or disable the ruleset; this is a workflow safeguard, not protection against the repository owner changing policy. GitHub treats some skipped/neutral check conclusions as satisfying required checks; this rule uses GitHub's native semantics.

## Apply once through GitHub

The current connector has no administration-write action, local CLI credentials are invalid, and Chrome control is unavailable. GitHub's ruleset creation API requires repository Administration (write), which the managed connection does not provide. Do not share credentials or grant unrelated repository access.

1. Download the JSON file to the computer where GitHub is open.
2. Open [this repository's ruleset settings](https://github.com/NatTuji/ai-risk-governance-lab/settings/rules).
3. Select **New ruleset → Import a ruleset** and choose the JSON file.
4. Review the imported form: enforcement **Active**, target **main**, bypass list empty, all four checks with GitHub Actions as their source, and required approvals zero. Click **Create**.

This final UI action applies the prepared configuration. It is needed because the available connection lacks the required capability; the owner has already authorized the policy. No new approval is being requested.

## Verification after saving

Read the actual rulesets and effective main rules:

- `GET /repos/NatTuji/ai-risk-governance-lab/rulesets`
- `GET /repos/NatTuji/ai-risk-governance-lab/rules/branches/main`

Confirm active main-targeted PR, required-check, deletion, and non-fast-forward rules. Verify each check context/source and strict mode. Inspect the bypass list in the saved UI: the API may omit that field for a connection without write access to the ruleset, and omission does not prove the list is empty.

A later safe verification can use a temporary failing PR and inspect that merge is blocked. Do not attempt a real force push, branch deletion, or merge of a failing PR to test protection. Close issue #12 only after observed enforcement; otherwise keep the precise incomplete step recorded. Subsequent main changes should go through branches and checked PRs, including assistant changes.

Sources: [GitHub ruleset import instructions](https://docs.github.com/en/repositories/configuring-branches-and-merges-in-your-repository/managing-rulesets/managing-rulesets-for-a-repository#importing-a-ruleset), [GitHub REST rules schema and permissions](https://docs.github.com/en/rest/repos/rules#create-a-repository-ruleset).
