# Bitbucket Reviewer Resolution

Use this reference only during approved Bitbucket PR delivery. It changes reviewer handling, not the Bug's confirmation, change-group, worktree, or cleanup rules. Keep the original checkout untouched; do not adopt an upstream script's stash/rebase workflow.

## Query the Actual PR

1. Confirm the destination and source with `bkt repo view --project <project> --repo <repo> --json`; record each repository's numeric ID. Verify the pushed source ref exists in the source repository and the target ref exists in the destination. Do not assume a fork branch also exists upstream.
2. Get the authenticated username from the selected host/context in `bkt auth status`. The API caller becomes the new PR's author; do not infer this from `git config user.name` or the fork owner's name. If the identity cannot be established, resolve it before assigning reviewers.
3. On Data Center, call the destination's effective-reviewer endpoint through `bkt` with **both repository IDs** and full refs:

```text
bkt api /rest/default-reviewers/latest/projects/<destination-project>/repos/<destination-repo>/reviewers --param sourceRepoId=<source-repo-id> --param targetRepoId=<destination-repo-id> --param sourceRefId=refs/heads/<source-branch> --param targetRefId=refs/heads/<target-branch> --json
```

Compare reviewer identities to the authenticated author, exclude the author, and deduplicate the remaining usernames. Prefer stable user IDs where available; compare Data Center usernames case-insensitively. Do not compare display names. Pass each remaining reviewer via `--reviewer <username>` in `bkt pr create`, with explicit source/destination arguments.

`bkt repo default-reviewers list` may resolve both refs in the destination; do not use it for a fork-only source branch. `bkt pr reviewer-group list` lists groups, not this PR's effective reviewers. For Data Center, explicit reviewers also avoid relying on the Cloud-only author-exclusion promise of `--with-default-reviewers`.

## Empty or Failed Queries

- A 404 is not an empty default-reviewer result. Recheck host/context, repository IDs, source push, refs, permissions, and the exact error before retrying. Do not change the query to an arbitrary branch pair to make it succeed.
- A successful empty list can mean no condition matches this PR, or filtering removed the only reviewer. Inspect the destination conditions:

```text
bkt api /rest/default-reviewers/latest/projects/<destination-project>/repos/<destination-repo>/conditions --json
```

- Check source/target matchers against the actual PR. A recent PR with the same repository pair and relevant target may suggest candidates, but does not prove they apply; ask the user if no applicable independent reviewer can be established. Preserve the Bug edits and delivery worktree while this step waits.

## Verify the Existing PR

- Parse the actual response shape: `bkt pr create --json` may return `id/title/url`; `bkt pr view --json` may wrap the object in `pull_request`. A missing `links` property alone does not prove creation failed. Reuse the returned ID/URL and refetch with explicit destination arguments before retrying a write whose result is unclear.
- Read the final PR author and reviewers with `bkt pr view <id> --project <destination-project> --repo <destination-repo> --json`. Allow a brief bounded refetch for server automation; do not recreate the PR when reviewers have not appeared yet.
- Verify at least one actual reviewer is not the author. An author-only list fails the delivery gate even though it is non-empty. Remove an erroneous author assignment and add missing verified reviewers through explicit `bkt pr edit` flags, then refetch.
- Prefer `bkt pr edit --reviewer` / `--remove-reviewer`; a hand-written raw PUT may replace the entire reviewer list and erase existing assignments. Reviewer repair must preserve unrelated reviewers.
- Only after PR metadata, remote commit, and independent reviewers are verified may the existing Delivery Stage perform cleanup. If verification is blocked, preserve the recoverable state and report the exact pending action.

Reference: [upstream PR rules](https://code.fineres.com/projects/FXDATA/repos/skill-manager/browse/plugins/dev-toolkit/skills/open-bitbucket-pr/SKILL.md).
