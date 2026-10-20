---
name: bugfix
description: Use when a task in D:\work\fv-web2 or D:\work\fx-data-web contains a Feishu Project issue/detail URL or work item key, or when fixing, investigating, reviewing, commenting on, committing, or delivering a bug in those repositories.
---

# Bugfix

Use this skill as the repository-specific Bug-fix conductor for `D:\work\fv-web2` and `D:\work\fx-data-web`.

**变更隔离依赖：** `D:\Claire\chrome-plugin\change-groups` 插件支持 VS Code UI 和仓库 Git 目录中的 `change-groups.json` 文档协议。UI 或工具不可调用时，先读插件 `README.md` 和现有 JSON；只要文档协议可用，就用它创建分组并精确归组。仅当 UI/工具与文档协议都不可用时，才记录具体限制并回退到 Git 基线、精确路径和 hunk 对比。

Fix and validate in the current checkout on its current branch. Keep Bug edits in a dedicated change group so existing and unrelated user changes remain separate and visible. If neither the plugin UI/tools nor its documented JSON protocol is usable, continue with the recorded dirty-file baseline and exact Bug diff; do not block the work or overwrite protected changes. Commit and deliver the Bug from a dedicated PR branch, then clean the Bug edits and change group, when present, from the original checkout after the PR is verified.

**REQUIRED SUB-SKILLS:** Use `bug-memory-workflow` before code edits and `bug-des` for Chinese Feishu/PR content.

## Immediate Issue-Link Gate

Run this gate before stage routing, other business skills, repository reads, memory search, or substantive analysis.

When the latest user message introduces a primary Feishu Project `issue/detail` URL or exact work item key:

1. Treat it as the current primary issue and call Feishu Project `get_workitem_brief` immediately.
2. As soon as the exact work item `name` is returned, call `set_thread_title` with that exact name as the entire title. If that tool is unavailable, safely assign the exact title to the PowerShell variable `$taskTitle`, then run `rtk pwsh -NoProfile -File 'D:\Claire\tools\codex-thread-title\Set-CodexThreadTitle.ps1' -Name $taskTitle` when PowerShell 7 (`pwsh`) is available. Use Windows PowerShell only when `pwsh` is unavailable. Pass the title through the variable; do not interpolate it into executable command text. The script uses `CODEX_THREAD_ID` by default.
3. Do not add the key, URL, stage, action, repository, or an invented summary to the title.
4. Repeat the gate for every distinct primary issue introduced later.
5. Verify the rename. For the CLI fallback, require exit code `0` and success output containing the exact thread ID and title. On failure, inspect the error and retry once with the alternate available PowerShell host (`pwsh` or Windows PowerShell); do not repeat an invocation that failed with a parse or encoding error. If reading or renaming still fails, record the exact failure and continue without blocking the Bug work.
6. Retain the work item key for the task: use an exact key supplied by the user; otherwise use `f-<numeric issue ID>` from the URL/id.

## Core Rules

- Fix and validate in the current checkout on its currently checked-out branch. Do not switch, stash, reset, or clean the user's checkout.
- Before analysis or edits, record the current branch, `HEAD`, dirty-file list, and listening-port baseline. Treat all pre-existing changes as protected user state.
- Create or select one Codex change group from `D:\Claire\chrome-plugin\change-groups` for the active Bug before editing. Put every Bug code edit in that group and keep pre-existing, unrelated, generated, and other-Bug changes outside it.
- If change-group UI/tools are unavailable, use the plugin's documented `change-groups.json` protocol when its README and repository Git directory are accessible. Fall back to baseline-based isolation only when both UI/tools and that protocol are unavailable; record the exact blocker. Protect every pre-existing dirty path and hunk; do not substitute a branch or worktree during Fix or Validation.
- One task has one primary Bug and, when supported, one active Bug change group. A new primary Bug uses a separate task and, when supported, a separate change group.
- Commit and PR delivery must use a dedicated source branch named `codex/bugfix/<work-item-key>`; add a short collision suffix only when that branch already exists for another change.
- Create the delivery branch in a temporary worktree on the D drive so the original checkout and protected user changes stay in place. A delivery worktree is allowed only for Commit or Delivery stages.
- Keep the active change group, when present, until the PR is created and verified. Then remove only this Bug's edits from the original checkout, delete the group if present, remove the temporary worktree, and delete the local delivery branch after confirming the remote branch and PR contain its commit.
- A change group is not active merely because it exists. After every Bug edit batch and before validation or reporting, compare each full hunk from `git diff HEAD --unified=3` with the repository Git directory's `change-groups.json`; every Bug hunk must belong to the active group. If the UI cannot assign it, follow the plugin README's JSON protocol: preserve other groups, write the complete hunk, and atomically replace the JSON file. Refresh and recheck. Leave protected baseline changes, unrelated changes, and explicitly generated files outside the group. UI/tool absence alone is not grounds to skip the documented protocol.
- Inspect callers before changing shared behavior; move the fix to a shared point only when that change is necessary for the confirmed Bug, not merely because a sibling path has another defect.
- Before editing code, explain the evidenced cause, approach, and scope. Obtain direction confirmation if it has not already been given; a reply such as “修复” or “继续修复” after that explanation confirms the described direction. Do not ask again unless a new choice materially changes behavior, risk, or cost.
- Do not stage, commit, push, comment on Feishu, or create a PR before the user approves that delivery action.
- If Bug edits overlap protected user changes and cannot be separated safely into the Bug change group or exact ungrouped diff, stop before overwriting them.
- Use repository scripts from `package.json` and prefer focused checks such as `pnpm eslint:files <path>`.
- Run `ponytail:ponytail` for every touched or directly involved source file, keeping only scoped simplifications.
- Pass the Runtime Cleanup Gate before every stage stop.

## 修复范围与展示依据

适用于分析后的修复方案、代码修改和用户纠正范围后的继续修复；只读分析不自动授权修改。

- 修改前锁定三个边界：本次要恢复的用户可观察行为、已确认的展示依据、必要的修改位置。说明哪些信息已证实、哪些仍是候选；静态构造出的异常路径不能冒充实际接口响应或页面复现。
- 没有产品或设计依据时，保留现有展示。仓库有现成组件、团队偏好使用某组件，都不等于允许新增错误图标、提示文案、Toast、重试入口或空白内容分支。“弹窗保持打开”只授权修复异常关闭，不自动授权设计失败界面。
- 修改范围可以因新证据调整，但每项业务调整必须能解释“删掉它，会怎样使本次已确认行为仍然失败”。关联缺陷、类型整理、生命周期重构、分页配置和新增抽象，不能因顺手、同类问题或更规范而并入。必要的类型修正、共享修复和请求清理仍可保留，但必须通过同一个必要性判断；配套测试和注释按是否直接支持本次修复的验证或理解判断，不要求每行都独立影响运行结果。
- 若最小修法会沿用无数据态、显示旧数据或持续 loading，先如实说明实际后果；不要把加载失败包装成成功，也不要为了消除这个取舍自行增加设计。能保留既有行为并安全推进时继续；不同选择实质影响验收、风险或成本时才询问。
- 测试直接验证本次故障与成功路径，按实际风险选边界；不要为被撤回的扩展继续保留测试，也不要用“测试通过”证明无依据的新界面正确。

### 收窄改动与完成前复核

用户指出“不是最小修改”“自行设计”等问题后，重新审查**本次完整 diff**，一次撤回所有违反该边界的自有改动；不要只撤用户点名的组件，再用新的状态或分支替代它。保护用户后续修改，无法安全分离时再请求处理。

完成前对每个自有 hunk 检查验收对应关系与必要性；检查新增状态、渲染分支、组件、文案和接口是否有依据。删除无关改动后更新变更分组，重跑受影响的定向检查，并同步评论、PR 描述和已有记忆中的最终行为。不要仅凭行数少就宣称“最简”，也不要为了行数最少省掉必要的错误处理。

## Stage Routing

| User intent | Stage | Stop point |
| --- | --- | --- |
| Fix / investigate / review | Fix | Current-branch changes and automated verification complete |
| `应用`, `Apply`, local validation | Validation | Grouped changes confirmed in the current checkout |
| `提交 commit` | Commit | Active Bug committed on its dedicated PR branch; group retained until PR delivery when present |
| `submit`, create PR, deliver | Delivery | PR verified; original Bug edits, optional change group, delivery worktree, and local delivery branch cleaned |
| Comment / PR description only | Description | Chinese text prepared |

Use the confirmed scope above. Ask one concise question only when the direction is still unconfirmed or a new consequential choice remains unresolved.

## Fix Stage

1. Complete the Immediate Issue-Link Gate and confirm the repo is supported.
2. Record the current branch, `HEAD`, `git status`, dirty paths, and listening-port baseline without altering them.
3. Create or select the active Bug change group and record its name or identifier. If UI/tools are unavailable, use the documented JSON protocol; use baseline and exact-diff isolation only if that protocol is also unavailable.
4. Use `bug-memory-workflow`: search `D:\Claire\memory\bug-fix.md` by work item, repo, package, page, component, API, error, symptom, data key, and likely file names; read only matching entries.
5. Read relevant code, inspect callers, and identify the root cause or narrow behavior gap.
6. 向用户说明 **Bug 原因**、**修改思路** 和 **修改方向**，按「修复范围与展示依据」锁定边界。复用已有确认；仅在方向尚未确认或存在新的实质选择时询问并等待，不重复要求确认。
7. 用户确认后，才在当前分支小范围修改，遵循现有模式，并将每个 Bug 代码改动放入 active change group。若 UI/tools 不可用，按插件 JSON 协议归组；只有协议也不可用时，才持续对照已记录基线并避开受保护路径和 hunk。
8. 修改每一批代码后，立即执行 Change Group Closure Gate：用 `git diff HEAD` 列出新增或变化的 Bug hunk，读取并核对 `change-groups.json`，补齐漏分组的 hunk；未完成分组核对前不得进入测试或汇报。
9. Add Chinese purpose comments for new methods and Chinese comments for non-obvious branching. Avoid generated files and unrelated modules.
10. Run `ponytail:ponytail` on touched or directly relevant source files, then perform the full-diff necessity and design review above; do not broaden the patch to resolve unrelated findings.
11. Run focused lint, test, or build checks. Record the exact blocker when a check cannot run.
12. 修改完成后，向用户汇报实际的 **Bug 原因** 和 **修改思路**；如实际实现与确认方案有差异，明确说明差异。
13. Run the Runtime Cleanup Gate, then report the current branch, change-group status, Bug files, behavior, verification, and residual risk.

## Validation Stage

The Bug changes already live in the current checkout; do not transfer or reapply a diff.

1. Confirm the current branch and active Bug change group, or the recorded baseline and exact Bug diff when no group is available.
2. Run the Change Group Closure Gate again. Confirm every Bug hunk is assigned to the active group when present; without a group, compare the exact Bug diff with the recorded baseline and confirm unrelated changes remain untouched.
3. Run focused verification in the current checkout.
4. Run the Runtime Cleanup Gate and report the branch, change-group status, files, preserved user changes, and result.
5. Once verified, update the existing entry in `D:\Claire\memory\bug-fix.md` rather than creating a duplicate.

## Concurrent Bugs

- Each Bug uses a separate task and, when supported, a separate change group, even on the same current branch.
- Use unique dev-server ports and keep each Bug's edits in its own group when present; otherwise isolate them by exact paths or hunks against each task's baseline.
- Surface overlapping-file or overlapping-hunk conflicts instead of mixing task diffs.
- Do not create branches or worktrees during Fix or Validation. Use one temporary worktree only when committing or delivering that Bug.

## Runtime Cleanup Gate

1. Before starting Trae, a debugger, development server, preview service, test watcher, or listener, record existing matching PIDs and ports as the protected baseline.
2. Record every task-owned launch command, parent PID, identifiable descendants, and ports.
3. Stop only recorded task-owned processes by PID or verified process tree. Never terminate all `Trae`, `node`, `java`, or similar processes by name.
4. Confirm every recorded PID exited and port was released. Report any remainder instead of claiming completion.
5. Keep runtime only when explicitly requested and report its PID, command, and port.

## Commit Stage

Run only after explicit commit approval.

1. Recheck the original branch, recorded pre-Bug `HEAD`, active Bug change group or baseline-based isolation, protected changes, Bug file list, and `git status`.
2. Resolve the work item key: explicit user key first, otherwise `f-<numeric issue ID>`.
3. Create `codex/bugfix/<work-item-key>` from the recorded pre-Bug `HEAD` in a temporary D-drive worktree. Do not switch the original checkout.
4. Apply only the active Bug change group to the delivery worktree. Without a group, transfer only verified Bug paths or hunks relative to the recorded baseline; stop if they overlap protected or unrelated changes.
5. Stage and commit only the Bug files with `fix: <Feishu issue title> #<work-item-key>` and verify the key exactly.
6. Run focused verification and confirm the commit contains only intended Bug changes.
7. Keep the original Bug edits and active change group, when present, until PR delivery succeeds. Do not push, create a PR, or perform post-delivery cleanup when the user requested only a commit.

## Delivery Stage

Run only after `submit`, `提交`, or equivalent delivery approval.

1. Recheck the original branch, recorded pre-Bug `HEAD`, active Bug change group or baseline-based isolation, intended files, protected changes, `git status`, and remote.
2. Resolve the exact issue title and work item key; an explicit key wins, otherwise use `f-<numeric issue ID>`.
3. Create or reuse the Commit-stage temporary worktree and dedicated `codex/bugfix/<work-item-key>` source branch. Apply and commit only the active Bug change group if present; otherwise transfer only the verified Bug paths or hunks relative to the recorded baseline.
4. Use `bug-des` to build the Chinese Feishu comment and PR description from issue context and the dedicated branch diff.
5. Post the Feishu comment and push the dedicated source branch.
6. Resolve the PR destination separately from the active `bkt` context. Inspect `git remote -v` and `bkt context list`, then confirm the source and destination repositories with `bkt repo view`. Never assume the active context is the destination: it may point to a personal fork. In the current `D:\work\fv-web2` setup, `origin` is `~CLAIRE.TANG/fx-web2`, while the upstream destination is `FXDATA/fx-data-web`; create a cross-repository PR with explicit `--project FXDATA --repo fx-data-web --source-project '~CLAIRE.TANG' --source-repo fx-web2`. Verify this mapping against the live remotes and contexts each time. Do not create a PR from the personal repository back into itself.
7. Resolve the target branch from the rules below (`release-x` -> `release`; `feature-x` -> `feature`). Before PR creation, read [references/bitbucket-reviewers.md](references/bitbucket-reviewers.md), query effective reviewers with the real source/target repository IDs and refs, and exclude the authenticated PR author. Do not substitute an unrelated branch pair or reviewer-group list for the actual PR conditions.
8. Create the PR through `bkt` with explicit source and destination repository arguments and repeatable `--reviewer <username>` flags for the verified set. On Data Center, do not rely on `--with-default-reviewers`: fork refs may be resolved in the destination and the author may not be excluded. Verify the PR URL, source project/repository/branch, destination project/repository/target, title, description, reviewer list, and remote commit using `bkt pr view` with explicit destination arguments.
9. The final PR must have at least one verified reviewer other than its author. Refetch first to account for server-side additions, then add missing verified reviewers with `bkt pr edit <id> --project <destination-project> --repo <destination-repo> --reviewer <username>` without replacing existing reviewers. If no valid reviewer set can be established, stop before cleanup and ask the user; never report delivery as complete or recreate an existing PR merely to repair reviewers.
10. Only after verification succeeds, remove this Bug's edits from the original checkout through its change group when present. Without a group, revert only the verified Bug paths or hunks relative to the recorded baseline. Preserve every protected or unrelated hunk, then delete the change group if present.
11. Remove the temporary delivery worktree and delete the local delivery branch after confirming the remote branch still backs the PR. Verify the original branch, `HEAD`, and protected changes match the pre-delivery state.
12. Run the Runtime Cleanup Gate. Prefix the existing task title with `✅` without otherwise rewriting it, using the same native-tool-or-CLI fallback from the Immediate Issue-Link Gate.
13. Report the commit, Feishu comment, remote source branch, PR, reviewers, verification, original-checkout cleanup, group deletion when applicable, and runtime cleanup.

If push, PR creation, or verification fails, keep the original Bug edits, change group when present, delivery worktree, and local branch for a safe retry; do not claim cleanup.

## Description Stage

Use `bug-des` and base the text on the issue context and the active change group's scoped diff, or the verified ungrouped Bug diff.

## Bitbucket Rules

- Resolve the destination from the repository's upstream remote/context, not from whichever `bkt` context happens to be active. For fork workflows, set source and destination project/repository explicitly in `bkt pr create` and verify both in the resulting PR metadata.
- Follow [references/bitbucket-reviewers.md](references/bitbucket-reviewers.md) for repository-aware default-reviewer queries, author exclusion, explicit assignment, and final verification. A successful empty result is not a failed query; reviewers from a recent comparable PR are candidates, not automatically applicable defaults.
- Require a non-author reviewer in the final PR before cleanup. If the effective set is empty after filtering or cannot be verified, inspect the destination conditions and ask the user when no applicable set can be established; do not borrow defaults from arbitrary branches.
- Use `bkt` first. If it is absent, unauthenticated, or fails, report the exact command and error and obtain explicit approval before another web/API/browser/git/curl method.
- Never treat PR creation success as delivery verification. Wrong destination, missing reviewers, or unverified remote commit means delivery is incomplete; preserve the original Bug edits, change group, delivery worktree, and local branch for correction.
- If Bitbucket or Feishu requires login, state the exact page or action and pause that step.

## Common Failures

- A Bug branch or worktree is created during Fix or Validation: stop; dedicated branches and temporary worktrees are only for Commit or Delivery.
- Bug edits are mixed with existing changes or cannot be isolated against the recorded baseline: stop and restore isolation without discarding user work.
- `Apply` tries to transfer a diff: no transfer is needed in the current checkout.
- Delivery uses the original/current branch as the PR source: stop and create the dedicated Bug source branch.
- Delivery uses the active personal Bitbucket context as the destination without checking the upstream remote: stop and recreate the PR in the verified upstream repository; decline the mistaken personal-to-personal PR after the correct PR is verified.
- Reviewers are empty, contain only the author, or destination metadata cannot be verified: do not clean up the original Bug state or claim delivery completion.
- Post-delivery cleanup resets whole files or touches protected changes: stop and clean only through the active Bug change group or verified ungrouped paths and hunks.
- Unrelated changes are staged or overwritten: stop and restore separation without discarding user work.
- Sibling callers were not inspected: check them to establish impact, but do not automatically fix unrelated sibling defects. Use the shared point only when necessary for the confirmed Bug.
- An existing component is treated as design authorization, or a removed UI is replaced by an unapproved state/render branch: return to the confirmed display behavior and review the entire Bug diff.
- Delivery starts without approval, `bkt` is bypassed without approval, reviewers are empty, or task-owned runtime remains: stop and complete the corresponding gate.

## Final Review Checklist

- Task title is the exact issue name, with only the required `✅` prefix after confirmed PR creation.
- Fix and Validation stayed in the original checkout; Commit and Delivery used the dedicated Bug branch and temporary D-drive worktree.
- Before delivery, every Bug code edit was isolated in the active change group when available; authorized ungrouped work was verified against the recorded baseline and unrelated changes remained untouched.
- After each edit batch and before validation, the Change Group Closure Gate confirmed that no Bug hunk was left ungrouped.
- `D:\Claire\memory\bug-fix.md` was searched before editing and updated after verification.
- Root cause and callers were checked; the patch stayed narrow; `ponytail:ponytail` ran on involved source files.
- Every Bug hunk is necessary for the confirmed behavior; new presentation has an explicit basis. Scope corrections were applied to the full Bug diff, with removed extensions also removed from tests and delivery descriptions.
- 修改前已向用户说明 Bug 原因、修改思路和修改方向，并获得需求与方向确认。
- 修改完成后已再次说明实际 Bug 原因和修改思路，并区分已确认信息与待确认项。
- Focused verification ran or its exact blocker was documented.
- No staging or external delivery happened without approval, and the dedicated PR branch included only the verified Bug changes.
- After verified PR creation, the original Bug edits, change group when present, temporary worktree, and local delivery branch were removed without touching protected changes.
- PR metadata/reviewers, remote source branch, original-checkout cleanup, and runtime cleanup were verified when applicable.
