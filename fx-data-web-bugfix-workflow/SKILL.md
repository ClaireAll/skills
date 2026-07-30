---
name: fx-data-web-bugfix-workflow
description: Follow the stored D:\work\fv-web2 / fx-data-web bug-fix workflow when the user asks to fix a bug, prepare a Feishu issue comment, or create a PR with repo-specific defaults.
argument-hint: "[feishu_issue_id_or_context]"
user-invocable: false
allowed-tools:
  - Read
  - Grep
  - Bash
---

# fx-data-web bugfix workflow

## When to use

Use this skill when work is happening in `D:\work\fv-web2 / fx-data-web` and the task includes one or more of:

- fixing a bug that may need a later commit
- the user says `submit` and expects the full post-review delivery flow
- preparing the standard four-section Feishu bug comment
- creating a PR after a bug-fix commit

Do not use this skill for unrelated repositories, non-bug-fix tasks, or when the user gives more specific instructions that replace the stored defaults.

## Inputs / context to gather

1. Confirm the repository is `D:\work\fv-web2 / fx-data-web`.
2. Identify whether the current task is still in the "code changes for review" stage or has already moved to "approved, ready to commit".
3. If a Feishu issue is involved, capture its title and issue number for the commit-message template.
4. Check whether the user explicitly said `submit` or otherwise asked for submit/delivery, because in this repo that means commit plus PR unless they narrow it.
5. If creating a PR, inspect the local branch name and the final commit message.

## Procedure

1. Make the code changes first and stop there for review.
   - Default behavior is "First modify the code only and let the user review the changes."
   - Keep the patch as compact and narrowly scoped as possible; avoid unrelated cleanup or broad refactors unless the user asks for them.
   - If you add a new type or a new method, include a concise comment explaining its purpose.
   - Do not create the commit yet unless the user explicitly approves or asks for the commit now.
2. After approval, create the commit for a Feishu bug fix using:
   - `fix: <feishu issue title> #<feishu issue id>`
3. At the same time, prepare or post the Feishu bug comment with exactly these four sections:
   - `problem cause`
   - `impact scope`
   - `test scope`
   - `fix method`
4. Format the Feishu comment strictly:
   - no empty line between a section title and its content
   - exactly one empty line between content blocks
5. Decide PR behavior from the user's wording:
   - if the user said `submit`, treat that as commit + PR by default after the review gate
   - if the user explicitly narrowed the request to commit only or said not to create a PR, stop after commit/comment
   - otherwise, after the commit and Feishu comment are done, ask whether the user wants a PR
6. If a PR should be created, apply the repo defaults unless the user overrides them:
   - branch `release-x` targets `release`
   - branch `feature-x` targets `feature`
   - PR title defaults to the commit message
   - PR description copies the same four-section content from the Feishu bug comment with the same spacing rules
7. After the Feishu bug-fix PR is submitted/opened, run the `worklog` skill automatically.
   - Do not ask whether to record Feishu Project work hours.
   - Use the worklog skill's default time rule when the user did not supply a time.
8. Verify PR completion metadata before reporting completion.
   - Fetch the created PR's metadata and confirm the reviewer list is not empty.
   - If reviewers were not specified, use a recent comparable PR or a PR the user mentioned in this repository as the reference when appropriate.

## Efficiency plan

1. Check the branch name once and reuse it for PR target selection.
2. Draft the four-section Feishu comment once, then reuse the same text for the PR description if a PR is requested.
3. Keep code edits narrow so review stays focused and the user can validate the intended fix quickly.
4. Stop before commit creation if the user has not reviewed the code yet; this avoids rework and matches the stored workflow.
5. If the user already said `submit`, do not spend another turn asking whether to create a PR unless they also narrowed the request.
6. After a PR is opened, hand the already-known Feishu issue and verified fix context directly to `worklog`; do not re-ask about time unless its required non-time context is missing.

## Pitfalls and fixes

- Symptom: commit created too early.
  - Likely cause: skipped the review gate.
  - Fix: pause after code changes and wait for explicit approval before committing.
- Symptom: the patch grows beyond the requested fix.
  - Likely cause: bundled refactors or opportunistic cleanup.
  - Fix: trim the change back to the smallest targeted edit that solves the requested bug.
- Symptom: new types or methods are added without comments.
  - Likely cause: repo-specific comment expectations were missed.
  - Fix: add concise purpose comments for each new type and method before handing the code over for review.
- Symptom: user says `submit` but the workflow stops after commit or asks again about PR creation.
  - Likely cause: the newer `submit` clarification was missed.
  - Fix: after the review gate, treat `submit` as commit plus PR unless the user explicitly says commit only or no PR.
- Symptom: Feishu comment or PR description has extra blank lines.
  - Likely cause: generic markdown habits.
  - Fix: keep each title directly attached to its content and leave only one blank line between blocks.
- Symptom: PR targets the wrong base branch.
  - Likely cause: branch-to-target mapping was not checked.
  - Fix: map `release-x` to `release` and `feature-x` to `feature` unless the user says otherwise.
- Symptom: PR is reported complete with no reviewers.
  - Likely cause: post-create metadata was not checked.
  - Fix: fetch PR metadata and confirm reviewers are non-empty before reporting completion.
- Symptom: bug-fix PR handoff omits Feishu Project work hours.
  - Likely cause: `worklog` was treated as an optional follow-up.
  - Fix: invoke `worklog` automatically after the PR is submitted/opened; use its default time rule when no time is supplied.

## Verification checklist

- The repo is `D:\work\fv-web2 / fx-data-web`.
- The code patch stays compact and narrowly scoped to the requested fix.
- Any new types or methods added in the change include purpose comments.
- Code changes were shown for review before commit creation unless the user explicitly changed that order.
- Feishu bug-fix commit messages use `fix: <feishu issue title> #<feishu issue id>` when applicable.
- The four Feishu sections are present and spaced correctly.
- If the user said `submit`, the workflow included PR creation unless they explicitly narrowed the request.
- If a PR was created, its target branch, title, and description follow the stored defaults or the user's override.
- A created PR has a non-empty reviewer list confirmed from post-create metadata.
- After a Feishu bug-fix PR was submitted/opened, the `worklog` follow-up was run automatically, or any required user/login blocker was reported.
