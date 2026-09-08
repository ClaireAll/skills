---
name: bugfix
description: Use when a task in D:\work\fv-web2 or D:\work\fx-data-web contains a Feishu Project issue/detail URL or work item key, or when fixing, investigating, reviewing, commenting on, committing, or delivering a bug in those repositories.
---

# Bugfix

Use this skill as the repo-specific bug-fix conductor for `D:\work\fv-web2` and `D:\work\fx-data-web`.

The same isolated-worktree lifecycle applies to both repositories. Each active Bug task owns one branch and one worktree while the fix is developed; manual validation happens after only the Bug diff is applied to the original checkout's current branch.

**REQUIRED SUB-SKILLS:** Use `using-git-worktrees` for isolated Bug workspaces, `bug-memory-workflow` before code edits, `bug-des` for Chinese Feishu/PR content, and `worklog` after a submitted bug-fix PR.

## Immediate Issue-Link Gate

Run this gate before stage routing and before loading requirement/design skills, reading repository files, searching memory, or starting substantive analysis. Do not defer it because another workflow already started or because the task is now in commit or delivery stage.

When the latest user message introduces a primary Feishu Project `issue/detail` URL or exact work item key:

1. Treat the latest user-provided issue as the current primary issue. Do not select a suspected-cause link, related issue, or commit reference instead.
2. Call Feishu Project `get_workitem_brief` immediately with the issue URL or ID. The fixed basic fields are sufficient when they include the exact work item `name`; do not fetch comments or all custom fields first merely to rename the task.
3. As soon as the exact work item `name` is returned, immediately call `set_thread_title` for the current Codex task.
4. Use the exact work item `name` as the entire task title. Do not include the work item key, URL, stage, action, repository, or an invented summary such as “分析/修复/评估……”.
5. Run the gate once for every distinct primary issue introduced in the task. If the user switches to another issue link later, rename the task again to the new issue name.
6. Verify that `set_thread_title` completed successfully before continuing. If the call fails, retry it once; if the work item cannot be read or the retry fails, state the exact blocker in the first user update and retry after the blocker is resolved. Never silently leave an automatic URL title or a placeholder such as `1`.
7. Resolve and retain the work item key for the whole task: use an exact key explicitly supplied by the user; otherwise use `f-<numeric issue ID>` from the Feishu issue URL/id.

## Core Rules

- Keep each Bug in its own task, branch, and worktree. A task may have only one primary Bug; process simultaneous Bugs in separate tasks.
- Create the Bug branch and worktree immediately after the issue-link gate. Perform analysis, edits, and automated verification inside that worktree, then apply only the Bug diff to the original checkout's current branch for manual validation.
- Do not create a pre-validation commit. Leave the reviewed Bug changes uncommitted until the user explicitly requests `提交 commit 到 <目标分支>`.
- Do not stage, commit, push, comment on Feishu, create a PR, or log work before the user approves delivery. `提交 commit 到 <目标分支>` is the commit-to-target flow described below; `submit` or an explicit PR request uses the full delivery flow.
- Create Bitbucket PRs with `bkt` first. Do not automatically open Bitbucket in a browser; any non-`bkt` fallback requires explicit user approval after a `bkt` failure.
- When the user says `submit` or explicitly asks to create a PR after a reviewable diff exists, treat it as approval for commit + Feishu comment + push + PR + reviewer verification + worklog unless they narrow the scope.
- When the user says `提交 commit 到 <目标分支>`, perform only the commit-to-target flow: commit the verified changes, transfer them to the named target branch, verify the target branch, remove the Bug worktree, and delete the exact Bug branch. Do not push, create a PR, comment on Feishu, or log work unless separately requested.
- Preserve unrelated local changes. Confirm the intended file set before delivery.
- Use repository scripts from `package.json`; prefer focused commands such as `pnpm eslint:files <path>`.
- When modifying a bug, run a `ponytail:ponytail` pass for each touched or directly involved source file and apply only scoped simplifications that keep the bug fix narrow.
- Treat every Trae/debug process, development server, preview service, test watcher, or other listener started by Codex for the current task as task-owned runtime. Record it at launch and pass the Runtime Cleanup Gate before any stage stop or final response.

## Stage Routing

| User intent | Stage | Stop point |
| --- | --- | --- |
| Fix / investigate / review a bug | Fix stage | After isolated code changes and automated verification |
| `应用`, `Apply`, switch to local validation | Validation-apply stage | After the Bug diff is applied and verified on the original checkout's current branch |
| `提交 commit 到 <目标分支>` | Commit-to-target stage | After target-branch commit and worktree/branch cleanup |
| `submit`, create PR, deliver after review | Delivery stage | After PR reviewer verification and worklog |
| Commit only / no PR without a target branch | Ask for the target branch | Do not mutate Git state |
| Comment / PR description only | Description stage | After Chinese text is prepared |

If the stage is ambiguous, infer conservatively from the latest user message and current git state. Ask one concise question only when the next action could publish or submit something unintended.

## Fix Stage

Create the isolated worktree before substantive repository analysis or code edits. Before starting Trae, a debugger, a development server, a preview service, a test watcher, or another listener, perform steps 1-2 of the Runtime Cleanup Gate so ownership can be proved later.

1. Confirm the working repo is `D:\work\fv-web2` or `D:\work\fx-data-web`.
2. Establish the Bug workspace immediately:
   - Capture the current branch, `HEAD`, dirty-file list, existing worktrees, and listening-port baseline.
   - Use the current branch's `HEAD` as the default base. Create the worktree from committed state without stashing, resetting, or otherwise mutating the original checkout.
   - Create a unique branch named `codex/bug-<numeric-issue-id>-<short-slug>` and a sibling worktree at `D:\work\<repo-name>-worktrees\<numeric-issue-id>-<short-slug>`.
   - If the branch or path already exists, do not reuse it silently; inspect its recorded state and ask before changing it.
   - Verify the new worktree is on the new branch and record the exact branch, path, base commit, and task-owned runtime baseline.
   - Keep the original checkout's modified tracked files, untracked files, account data, and local environment configuration in place. Never copy them into the Bug worktree merely to prepare validation.
   - Record the original dirty paths as protected user state. All remaining diagnosis, edits, automated tests, and runtime launches before Apply happen inside the new worktree.
3. Use `bug-memory-workflow` before editing:
   - Search `D:\Claire\memory\bug-fix.md` first by work item, repo, package, page, component, API, error text, symptom, data key, and touched file names.
   - Read only the matching entries. Use fallback paths from `bug-memory-workflow/references/bug-memory-notes.md` only when the unified file has no relevant match.
4. Diagnose with evidence:
   - Read relevant code before editing.
   - Identify the root cause or the narrow behavior gap.
   - Avoid broad refactors unless required to fix the bug.
5. Patch narrowly:
   - Follow existing local patterns.
   - Add purpose comments for new types, methods, or non-obvious branching.
   - Avoid touching generated files or unrelated modules.
6. Run Ponytail on involved files:
   - For every changed or directly relevant source file, invoke `ponytail:ponytail` to look for YAGNI, existing-code reuse, standard-library/native alternatives, unnecessary abstractions, boilerplate, and dependency bloat.
   - Apply only simplifications that preserve the diagnosed root-cause fix and do not broaden the bug scope.
   - Skip style-only churn and record any useful simplification that was intentionally left out.
7. Verify:
   - Run focused lint/test/build checks when practical.
   - If a check cannot run, record the exact blocker.
8. Run the Runtime Cleanup Gate. Keep the Bug worktree as the isolated source diff until Apply or explicit abandonment.
9. Stop for review and report the explicit Bug file list, behavior, automated verification, residual risk, Bug branch, and worktree path. Do not tell the user to validate in the worktree.

## Validation-Apply Stage

Run when the user clicks or requests `应用` / `Apply`, or asks to switch to local validation.

1. Resolve the original checkout's current branch at Apply time and report it. Do not switch branches, stash, reset, or disturb its existing local changes.
2. Recheck the explicit Bug file list against the original checkout. Unrelated dirty files are expected and must remain untouched; if a Bug file has user edits that were not part of the recorded baseline, stop on that file rather than overwrite it.
3. Apply only the Bug diff from the isolated worktree to the original checkout's current branch. Do not copy account/configuration files into the worktree, and do not stage or commit during Apply.
4. Run focused verification from the original checkout so the checks use the same local account and environment state as manual validation.
5. Run the Runtime Cleanup Gate, then report the validation branch, original checkout path, applied Bug files, preserved user changes, and verification result. The user validates on this current branch.
6. Keep the Bug worktree until validation is complete and the fix is committed or explicitly abandoned. Once verified, update the existing Bug entry in `D:\Claire\memory\bug-fix.md` rather than creating a duplicate.

### Parallel Bug Rules

- Each distinct Feishu Bug link starts or continues a separate task. Each task has one issue title, one branch, and one worktree.
- Use separate worktree directories and unique dev-server ports for concurrent Bugs. Apply only the selected Bug diff to the original checkout's current branch; never combine worktree diffs implicitly.
- A Bug worktree remains until its verified changes are committed to the target branch or the user explicitly abandons the work. Do not delete a worktree merely because its conversation was archived.
- If two Bugs need overlapping files, keep their worktrees isolated and surface any target-branch conflict during commit-to-target instead of merging them implicitly.

## Runtime Cleanup Gate

Apply this gate after successful or failed debugging and verification, before every stage stop or final response, and when abandoning a runtime-assisted attempt.

1. Establish ownership before launch:
   - Before starting Trae, a debugger, development server, preview service, test watcher, or other listener, record matching existing process IDs and listening ports as the protected baseline.
   - A process that existed before the task or was started by the user is not task-owned and must not be closed.
2. Record each launch:
   - Record the launch command, parent PID, identifiable descendant PIDs, and listening ports immediately after startup.
   - A Trae instance started by Codex and its debugging descendants are task-owned. When Codex uses an already-running user Trae instance, only positively identified child runtimes launched for this task are task-owned.
3. Clean up only task-owned runtime:
   - Stop the recorded descendant processes and parent process by PID or verified process tree. Never terminate all `Trae`, `node`, `java`, or similarly named processes by name.
   - Cleanup remains required after failed checks, tool errors, or interrupted debugging, not only after a successful fix.
4. Verify cleanup:
   - Confirm every recorded task-owned PID has exited and every recorded port no longer has a listener.
   - If cleanup fails, report the exact remaining PID and port; do not report the stage as complete.
5. Preserve an explicit exception:
   - Leave runtime running only when the user explicitly asks. Report the retained PID, command, and port in the final response.

## Delivery Stage

Run only after user approval or `submit` / `提交`.

1. Recheck local state:
   - After Apply, run the checks from the original checkout and its validated current branch. Otherwise use the recorded Bug worktree.
   - `git status`
   - current branch
   - intended changed files
   - target remote/repository
2. Resolve issue metadata:
   - Feishu issue URL/id and its numeric issue ID
   - exact issue title
   - resolved `工作项 Key`
   - issue type, usually `缺陷`
   - Resolve the key in this order: copy an exact key explicitly supplied by the user; otherwise compose `f-<numeric issue ID>` from the Feishu issue URL/id.
   - An explicit user key may use `f-`, `m-`, `g-`, or another prefix and always overrides the default `f-` prefix.
   - Reuse the resolved key throughout the task. Do not look it up again or ask the user again during commit, PR, comment, or worklog steps.
   - Ask the user only when neither an explicit key nor an identifiable numeric issue ID is available.
3. Build description content:
   - Use `bug-des`.
   - Base it on the issue context and scoped git diff.
   - Reuse the same Chinese text for Feishu comment and PR description unless the user asks otherwise.
4. Commit:
   - Use `fix: <feishu issue title> #<工作项 Key>` for Feishu bug fixes.
   - Before committing, verify that the value after `#` exactly matches the key resolved above, including its prefix and punctuation.
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
10. Run the Runtime Cleanup Gate.
11. Final response:
   - commit hash and message
   - Feishu comment status
   - pushed branch
   - PR URL and target branch
   - reviewer verification result
   - worklog result
   - runtime cleanup result and released ports
   - verification that could not run

## Commit-to-Target Stage

Run this stage only after the user confirms manual validation is complete and explicitly names the target branch, for example `提交 commit 到 <target-branch>`. This is a local commit-and-transfer flow; do not push or create a PR unless the user separately requests it.

1. Recheck the recorded Bug worktree, validation checkout, target branch, explicit Bug file list, protected user-dirty paths, and current status.
2. Unrelated user changes on the target branch are allowed. Stop only if the target is missing or ambiguous, or a Bug file contains unrecognized overlapping edits; never stash, reset, or overwrite user changes automatically.
3. Resolve the work item key using the same priority as Delivery Stage: explicit user key first; otherwise `f-<numeric issue ID>` from the Feishu issue URL/id.
4. If the named target is the branch used for validation, stage only the explicit Bug file list there and create the formal bug-fix commit using `<type>: <subject> #<task-id>`; do not stage protected user-dirty paths.
5. If the named target differs from the validation branch, use a separate clean target worktree and transfer only the Bug commit there; never switch or clean the user's original checkout.
6. Run focused verification on the target branch and confirm the commit contains only the intended Bug files.
7. Only after target-branch verification succeeds, remove the exact Bug worktree and delete the exact Bug branch. Do not remove any other worktree or branch.
8. Run the Runtime Cleanup Gate and report the target branch commit, source branch deletion, removed worktree, and any verification that could not run.

## Commit-Only Stage

For a Bug task, `提交 commit 到 <target-branch>` is handled by Commit-to-Target Stage above. Do not infer the target branch from the current checkout or from a default.

If the user says only `提交 commit` without a target branch, ask for the exact target branch before creating a commit. A commit-only request without a PR still follows the target-branch transfer and cleanup rules above.

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
- Worktree created too late: create the Bug branch and worktree immediately after the issue-link gate, before substantive repository analysis or edits.
- Local account/configuration files are copied into the Bug worktree: this is the wrong direction; leave user state in the original checkout and apply only the Bug diff back to its current branch.
- User is told to validate in the Bug worktree: run Validation-Apply first and validate in the original checkout on its current branch.
- Multiple Bugs share one checkout: use one Codex task, branch, and worktree per Bug; surface overlapping-file conflicts instead of silently mixing changes.
- Original checkout is switched, stashed, or reset for validation: Apply must preserve its current branch and existing local state.
- Bug worktree removed before validation: retain it until the user confirms validation complete or explicitly abandons the Bug.
- Target branch omitted for commit: ask for the exact target branch; never infer it from the current checkout.
- Target branch has unrelated local changes: preserve them and continue with the explicit Bug files; stop only on an overlapping Bug-file conflict.
- Wrong commit reference: an explicit user key always wins; when none was supplied, use `f-<numeric issue ID>` from the Feishu issue URL/id.
- Unnecessary work-key question: do not ask when the user supplied a Feishu issue URL/id containing a numeric issue ID; apply the default `f-` prefix.
- Issue link or `1` remains as the task title: the Immediate Issue-Link Gate was skipped or deferred; run it immediately and use only the exact Feishu work item name.
- `submit` only creates a commit: after the review gate, run the full delivery stage unless narrowed.
- Feishu comment has extra blank lines: use the spacing rules above exactly.
- PR targets the wrong branch: apply `release-x` -> `release` and `feature-x` -> `feature` unless overridden.
- Browser opened instead of `bkt`: stop and use `bkt pr create` unless the user explicitly approved a fallback after a recorded `bkt` failure.
- `bkt` unavailable: report the exact error and request fallback approval; do not create the PR through another path automatically.
- PR has no reviewers: recover reviewers and verify metadata before reporting completion.
- Worklog omitted after PR: run `worklog` automatically after PR creation.
- Trae or listener left running: close only the recorded task-owned PID tree, verify its ports are released, and preserve baseline/user-owned processes.

## Final Review Checklist

- `D:\Claire\memory\bug-fix.md` was searched before code editing; fallback memory paths were used only when needed.
- Current task title exactly matches the current primary Feishu issue name and contains no work item key, URL, stage, or invented summary.
- Root cause and fix are evidence-based.
- `ponytail:ponytail` was applied to touched or directly involved source files, with only scoped simplifications kept.
- Patch is narrow and preserves unrelated changes.
- Focused verification ran or a blocker is documented.
- User reviewed code before delivery actions, unless they explicitly overrode that order.
- Every active Bug has its own recorded branch and worktree, including in both supported repositories.
- Validation-Apply transferred only the explicit Bug diff to the original checkout's current branch and preserved all unrelated local changes.
- Commit-to-target committed only the Bug files on the validated target branch, verified it, then removed only the exact Bug worktree and branch.
- Commit reference exactly matches the explicitly supplied key, or defaults to `f-<numeric issue ID>` when the user did not supply one.
- Bitbucket PR was created with `bkt pr create` and `--with-default-reviewers`, or the recorded `bkt` failure has explicit user-approved fallback.
- Every task-owned Trae/debug process, development server, watcher, and listener is stopped and its ports are released, unless the user explicitly requested retention and the retained runtime details were reported.
- Commit message, Feishu comment, PR title, PR description, target branch, reviewers, and worklog all match the rules for the active stage.
