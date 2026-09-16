---
name: bugfix
description: Use when a task in D:\work\fv-web2 or D:\work\fx-data-web contains a Feishu Project issue/detail URL or work item key, or when fixing, investigating, reviewing, commenting on, committing, or delivering a bug in those repositories.
---

# Bugfix

Use this skill as the repository-specific Bug-fix conductor for `D:\work\fv-web2` and `D:\work\fx-data-web`.

Work directly in the current checkout on its current branch. Keep each Bug's code changes in its own Codex change group so existing and unrelated user changes remain separate and visible.

**REQUIRED SUB-SKILLS:** Use `bug-memory-workflow` before code edits and `bug-des` for Chinese Feishu/PR content.

## Immediate Issue-Link Gate

Run this gate before stage routing, other business skills, repository reads, memory search, or substantive analysis.

When the latest user message introduces a primary Feishu Project `issue/detail` URL or exact work item key:

1. Treat it as the current primary issue and call Feishu Project `get_workitem_brief` immediately.
2. As soon as the exact work item `name` is returned, call `set_thread_title` with that exact name as the entire title.
3. Do not add the key, URL, stage, action, repository, or an invented summary to the title.
4. Repeat the gate for every distinct primary issue introduced later.
5. Verify the rename. Retry once on failure; if reading or renaming still fails, state the exact blocker and retry after it is resolved.
6. Retain the work item key for the task: use an exact key supplied by the user; otherwise use `f-<numeric issue ID>` from the URL/id.

## Core Rules

- Modify the current checkout on its currently checked-out branch. Do not create a Bug branch or worktree, and do not switch branches, stash, reset, or clean the user's checkout.
- Before analysis or edits, record the current branch, `HEAD`, dirty-file list, and listening-port baseline. Treat all pre-existing changes as protected user state.
- Create or select one Codex change group for the active Bug before editing. Put every Bug code edit in that group and keep pre-existing, unrelated, generated, and other-Bug changes outside it.
- Change groups are mandatory for Bug code edits. If unavailable, report the blocker instead of substituting a branch/worktree workflow.
- One task has one primary Bug and one active Bug change group. A new primary Bug uses a separate task and change group.
- Inspect callers before changing shared behavior and fix the root cause at their shared routing point when possible.
- Do not stage, commit, push, comment on Feishu, or create a PR before the user approves that delivery action.
- If Bug edits overlap protected user changes and cannot be separated safely into the Bug change group, stop before overwriting them.
- Use repository scripts from `package.json` and prefer focused checks such as `pnpm eslint:files <path>`.
- Run `ponytail:ponytail` for every touched or directly involved source file, keeping only scoped simplifications.
- Pass the Runtime Cleanup Gate before every stage stop.

## Stage Routing

| User intent | Stage | Stop point |
| --- | --- | --- |
| Fix / investigate / review | Fix | Current-branch changes and automated verification complete |
| `应用`, `Apply`, local validation | Validation | Grouped changes confirmed in the current checkout |
| `提交 commit` or commit to the current branch | Commit | Only the active Bug change group committed |
| `submit`, create PR, deliver | Delivery | PR metadata and reviewers verified |
| Commit to another branch | Ask the user to switch to it | Do not create a worktree or move user state |
| Comment / PR description only | Description | Chinese text prepared |

Ask one concise question only when the next action could publish or submit something unintended.

## Fix Stage

1. Complete the Immediate Issue-Link Gate and confirm the repo is supported.
2. Record the current branch, `HEAD`, `git status`, dirty paths, and listening-port baseline without altering them.
3. Create or select the active Bug change group and record its name or identifier.
4. Use `bug-memory-workflow`: search `D:\Claire\memory\bug-fix.md` by work item, repo, package, page, component, API, error, symptom, data key, and likely file names; read only matching entries.
5. Read relevant code, inspect callers, and identify the root cause or narrow behavior gap.
6. Patch narrowly on the current branch, following existing patterns and putting every Bug code edit into the active change group as it is made.
7. Add Chinese purpose comments for new methods and Chinese comments for non-obvious branching. Avoid generated files and unrelated modules.
8. Run `ponytail:ponytail` on touched or directly relevant source files.
9. Run focused lint, test, or build checks. Record the exact blocker when a check cannot run.
10. Run the Runtime Cleanup Gate, then report the current branch, change group, Bug files, behavior, verification, and residual risk.

## Validation Stage

The Bug changes already live in the current checkout; do not transfer or reapply a diff.

1. Confirm the current branch and active Bug change group.
2. Confirm all Bug code edits are in that group and unrelated changes remain outside it.
3. Run focused verification in the current checkout.
4. Run the Runtime Cleanup Gate and report the branch, group, files, preserved user changes, and result.
5. Once verified, update the existing entry in `D:\Claire\memory\bug-fix.md` rather than creating a duplicate.

## Concurrent Bugs

- Each Bug uses a separate task and change group, even on the same current branch.
- Use unique dev-server ports and keep each Bug's edits in its own group.
- Surface overlapping-file or overlapping-hunk conflicts instead of mixing groups.
- Never create a branch or worktree as a concurrency fallback.

## Runtime Cleanup Gate

1. Before starting Trae, a debugger, development server, preview service, test watcher, or listener, record existing matching PIDs and ports as the protected baseline.
2. Record every task-owned launch command, parent PID, identifiable descendants, and ports.
3. Stop only recorded task-owned processes by PID or verified process tree. Never terminate all `Trae`, `node`, `java`, or similar processes by name.
4. Confirm every recorded PID exited and port was released. Report any remainder instead of claiming completion.
5. Keep runtime only when explicitly requested and report its PID, command, and port.

## Commit Stage

Run only after explicit commit approval.

1. If a named target is not the current branch, ask the user to switch to it and stop. Do not create a worktree or switch/stash/reset automatically.
2. Recheck the current branch, active Bug change group, protected changes, Bug file list, and `git status`.
3. Resolve the work item key: explicit user key first, otherwise `f-<numeric issue ID>`.
4. Stage and commit only the active Bug change group; never stage protected or unrelated changes.
5. Use `fix: <Feishu issue title> #<work-item-key>` and verify the key exactly.
6. Run focused verification, confirm the commit contains only intended Bug changes, run cleanup, and report the result.

If the user says only `提交 commit`, use the current branch.

## Delivery Stage

Run only after `submit`, `提交`, or equivalent delivery approval.

1. Recheck the current branch, active Bug change group, intended files, protected changes, `git status`, and remote.
2. Resolve the exact issue title and work item key; an explicit key wins, otherwise use `f-<numeric issue ID>`.
3. Use `bug-des` to build the Chinese Feishu comment and PR description from issue context and the active group's diff.
4. Commit only the active Bug change group if needed, post the Feishu comment, and push the current branch.
5. Create the PR through `bkt` with target defaults `release-x` -> `release` and `feature-x` -> `feature`:
   `bkt pr create --title "<PR title>" --target <target branch> --description "<PR description>" --with-default-reviewers`
6. Verify the PR URL, source, target, title, description, and non-empty reviewers.
7. Run the Runtime Cleanup Gate. After PR creation is confirmed, prefix the existing task title with `✅` without otherwise rewriting it.
8. Report the commit, Feishu comment, pushed branch, PR, reviewers, verification, and cleanup.

## Description Stage

Use `bug-des` and base the text on the issue context and active change group's scoped diff.

## Bitbucket Rules

- If reviewers are empty, refetch PR metadata, check default reviewer rules, or copy reviewers from a recent comparable PR, then verify the list is non-empty.
- Use `bkt` first. If it is absent, unauthenticated, or fails, report the exact command and error and obtain explicit approval before another web/API/browser/git/curl method.
- An approved fallback must still apply and verify non-empty reviewers.
- If Bitbucket or Feishu requires login, state the exact page or action and pause that step.

## Common Failures

- A Bug branch or worktree is created: stop and continue only in the current checkout on its current branch.
- Bug edits are ungrouped or mixed with existing changes: separate only the Bug edits into its change group.
- `Apply` tries to transfer a diff: no transfer is needed in the current checkout.
- A different target branch is requested: ask the user to check it out; do not switch, stash, or create a worktree.
- Unrelated changes are staged or overwritten: stop and restore separation without discarding user work.
- Only the reported symptom path is patched: inspect sibling callers and fix the shared root cause.
- Delivery starts without approval, `bkt` is bypassed without approval, reviewers are empty, or task-owned runtime remains: stop and complete the corresponding gate.

## Final Review Checklist

- Task title is the exact issue name, with only the required `✅` prefix after confirmed PR creation.
- Work stayed in the original checkout on its current branch; no Bug branch or worktree was created.
- Every Bug code edit is in the active change group and unrelated changes remain outside it.
- `D:\Claire\memory\bug-fix.md` was searched before editing and updated after verification.
- Root cause and callers were checked; the patch stayed narrow; `ponytail:ponytail` ran on involved source files.
- Focused verification ran or its exact blocker was documented.
- No staging or external delivery happened without approval, and delivery included only the active Bug change group.
- PR metadata/reviewers and runtime cleanup were verified when applicable.
