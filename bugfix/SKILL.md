---
name: bugfix
description: Use when fixing, reviewing, or delivering a bug in D:\work\fv-web2 or D:\work\fx-data-web, including Feishu bug comments, Bitbucket PRs, reviewer checks, or a user saying submit/提交 for those repositories.
---

# Bugfix

Use this skill as the repo-specific bug-fix conductor for `D:\work\fv-web2` and `D:\work\fx-data-web`.

**REQUIRED SUB-SKILLS:** Use `bug-memory-workflow` before code edits, `bug-des` for Chinese Feishu/PR content, and `worklog` after a submitted bug-fix PR.

## Core Rules

- Keep the first pass code-only: fix the bug, verify, then stop for user review.
- Do not stage, commit, push, comment on Feishu, create a PR, or log work before the user approves delivery or asks to `submit` / `提交`.
- Create Bitbucket PRs with `bkt` first. Do not automatically open Bitbucket in a browser; any non-`bkt` fallback requires explicit user approval after a `bkt` failure.
- When the user says `submit` / `提交` after a reviewable diff exists, treat it as approval for commit + Feishu comment + push + PR + reviewer verification + worklog unless they narrow the scope.
- Preserve unrelated local changes. Confirm the intended file set before delivery.
- Use repository scripts from `package.json`; prefer focused commands such as `pnpm eslint:files <path>`.
- When modifying a bug, run a `ponytail:ponytail` pass for each touched or directly involved source file and apply only scoped simplifications that keep the bug fix narrow.

## Stage Routing

| User intent | Stage | Stop point |
| --- | --- | --- |
| Fix / investigate / review a bug | Fix stage | After code changes and verification summary |
| `submit`, `提交`, create PR, deliver after review | Delivery stage | After PR reviewer verification and worklog |
| Commit only / no PR | Commit-only stage | After commit and optional Feishu comment |
| Comment / PR description only | Description stage | After Chinese text is prepared |

If the stage is ambiguous, infer conservatively from the latest user message and current git state. Ask one concise question only when the next action could publish or submit something unintended.

## Fix Stage

1. Confirm the working repo is `D:\work\fv-web2` or `D:\work\fx-data-web`.
2. Use `bug-memory-workflow` before editing:
   - Search `D:\Claire\memory\MEMORY.md` and `D:\Claire\memory\extensions\ad_hoc\notes\`.
   - Use repo, package, page, component, API, error text, symptom, data key, and touched file names as search terms.
3. Diagnose with evidence:
   - Read relevant code before editing.
   - Identify the root cause or the narrow behavior gap.
   - Avoid broad refactors unless required to fix the bug.
4. Patch narrowly:
   - Follow existing local patterns.
   - Add purpose comments for new types, methods, or non-obvious branching.
   - Avoid touching generated files or unrelated modules.
5. Run Ponytail on involved files:
   - For every changed or directly relevant source file, invoke `ponytail:ponytail` to look for YAGNI, existing-code reuse, standard-library/native alternatives, unnecessary abstractions, boilerplate, and dependency bloat.
   - Apply only simplifications that preserve the diagnosed root-cause fix and do not broaden the bug scope.
   - Skip style-only churn and record any useful simplification that was intentionally left out.
6. Verify:
   - Run focused lint/test/build checks when practical.
   - If a check cannot run, record the exact blocker.
7. Stop for review:
   - Summarize changed files, behavior, verification, residual risk.
   - Do not commit yet.

## Delivery Stage

Run only after user approval or `submit` / `提交`.

1. Recheck local state:
   - `git status`
   - current branch
   - intended changed files
   - target remote/repository
2. Resolve issue metadata:
   - Feishu issue URL/id
   - exact issue title
   - issue type, usually `缺陷`
3. Build description content:
   - Use `bug-des`.
   - Base it on the issue context and scoped git diff.
   - Reuse the same Chinese text for Feishu comment and PR description unless the user asks otherwise.
4. Commit:
   - Use `fix: <feishu issue title> #<feishu issue id>` for Feishu bug fixes.
   - Include only intended files.
5. Feishu comment:
   - Post or prepare the `bug-des` output.
   - Preserve the required spacing exactly.
6. Push the source branch.
7. Create the Bitbucket PR through `bkt`:
   - Target branch defaults: `release-x` -> `release`, `feature-x` -> `feature`.
   - PR title defaults to the commit message.
   - PR description defaults to the Feishu bug comment text.
   - Run `bkt pr create --title "<PR title>" --target <target branch> --description "<PR description>" --with-default-reviewers` from the repository after the source branch is pushed.
   - Use the Feishu bug comment text as `<PR description>`; do not silently omit the description or switch tools.
   - `--with-default-reviewers` is required on initial creation. Do not create first and rely on later reviewer recovery when default reviewers are available.
8. Verify PR metadata:
   - PR URL
   - source branch
   - target branch
   - title
   - description
   - non-empty reviewers
9. Run `worklog` automatically after the PR is opened/submitted.
10. Final response:
   - commit hash and message
   - Feishu comment status
   - pushed branch
   - PR URL and target branch
   - reviewer verification result
   - worklog result
   - verification that could not run

## Commit-Only Stage

Use only when the user explicitly says commit only, no PR, or otherwise narrows delivery.

1. Recheck `git status` and intended files.
2. Create the bug-fix commit.
3. Post or prepare the Feishu bug comment only if requested or clearly part of the narrowed scope.
4. Stop and state that PR/worklog were intentionally skipped.

## Description Stage

Use `bug-des` for the current Feishu comment and PR-description template. It owns the required headings, spacing, and evidence rules, so do not maintain a second local format here.

## Bitbucket Reviewer Recovery

If reviewers are empty after PR creation:

1. Reopen or fetch the PR metadata.
2. Check target-repository default reviewer rules when accessible.
3. Otherwise copy reviewers from a recent comparable PR or a PR the user mentioned in the same repository.
4. Add reviewers manually.
5. Verify the reviewer list is non-empty before reporting PR completion.

Do not report PR completion if reviewers remain empty and no reviewer source can be resolved.

## BKT Failure Policy

- Use `bkt` for Bitbucket PR creation. Check `bkt pr create --help` when command details are needed.
- If `bkt` is absent, unauthenticated, or exits non-zero, report the exact command and error, then ask for explicit approval before using Bitbucket web, API, browser automation, `git`, or `curl` as a fallback.
- Do not choose a browser fallback for convenience, because `bkt` needs login, or because its description flag needs verification.
- An approved fallback must still apply default reviewers and verify the reviewer list is non-empty.
- If Bitbucket or Feishu requires login, tell the user the exact page/action needed and pause that step.
- If worklog cannot be submitted because of login/tool blockers, report the blocker and the prepared values.

## Common Failure Modes

- Commit created too early: stop after verified code changes until the user approves delivery.
- `submit` only creates a commit: after the review gate, run the full delivery stage unless narrowed.
- Feishu comment has extra blank lines: use the spacing rules above exactly.
- PR targets the wrong branch: apply `release-x` -> `release` and `feature-x` -> `feature` unless overridden.
- Browser opened instead of `bkt`: stop and use `bkt pr create` unless the user explicitly approved a fallback after a recorded `bkt` failure.
- `bkt` unavailable: report the exact error and request fallback approval; do not create the PR through another path automatically.
- PR has no reviewers: recover reviewers and verify metadata before reporting completion.
- Worklog omitted after PR: run `worklog` automatically after PR creation.

## Final Review Checklist

- Bug memory searched before code editing.
- Root cause and fix are evidence-based.
- `ponytail:ponytail` was applied to touched or directly involved source files, with only scoped simplifications kept.
- Patch is narrow and preserves unrelated changes.
- Focused verification ran or a blocker is documented.
- User reviewed code before delivery actions, unless they explicitly overrode that order.
- Bitbucket PR was created with `bkt pr create` and `--with-default-reviewers`, or the recorded `bkt` failure has explicit user-approved fallback.
- Commit message, Feishu comment, PR title, PR description, target branch, reviewers, and worklog all match the rules for the active stage.
