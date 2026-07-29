---
name: worklog
description: "Use when the user asks Codex to log or prepare Feishu Project/Meego work hours for a fixed bug, such as 录工时, 登记工时, 填工时, 工时录入, worklog, or when Codex has finished fixing a Feishu issue/缺陷 and submitted/opened the PR."
---

# Worklog

## Overview

Use this skill after bug-fix work when Feishu Project hours should be recorded for that bug. After Codex submits/opens a PR for a fixed Feishu issue/缺陷, run this skill automatically as the final follow-up without asking whether to log hours. Prefer live browser automation when a logged-in Feishu session and browser-control tool are available; if login is required, notify the user to log in manually and resume after they finish.

## Worklog Information

- Page: `https://project.feishu.cn/b2rl2h/meegoPlg/MII_686B6DA98EC9C002_board_f3d5nl`
- Work item type: `缺陷`
- Work item instance: exact Feishu issue id/title from the fixed bug.
- Duration/start time: explicit values when supplied; otherwise use the default random non-overlapping 1-3h slot starting after 09:00 and before 20:00 local time.
- Log body: `问题描述：...` and `修复方案：...`.
- Submit button: `提交工时`.

## Required Context

Collect these values before submitting:

- Bug instance: Feishu bug URL/id/title, or an exact searchable title from the just-fixed bug.
- Time block: selected calendar slot or explicit start time and duration. If neither is supplied, default to a random/free slot that does not overlap existing worklogs, lasts 1-3 hours, and starts after 09:00 and before 20:00 local time.
- Log text: bug description and fix plan.

If any missing value other than time would change what gets submitted and cannot be recovered from the current thread, ask one concise question before submitting. Missing time uses the default random/free-slot rule. Never choose a similar bug instance by guess.

## Workflow

1. Read [references/worklog-fields.md](references/worklog-fields.md) for the page URL, field mapping, and log format.
2. Extract the bug description and fix plan from the current bug context: Feishu issue, issue comments, user-provided bug notes, bug template, git diff, commit message, PR description, or the verified fix summary. If the issue body lacks a fix plan, inspect comments/remarks for a confirmed `问题描述` and `修复方法/修复方案`.
3. Compose `登记日志` with only the confirmed description and fix plan. Keep it concise and factual.
4. If invoked after a bug-fix PR was submitted/opened, treat that completed PR as permission to submit the worklog. Do not ask the user whether to run this skill.
5. Open the Feishu Project worklog page. If a login page or expired-session prompt appears, notify the user to manually log in in the browser, pause, and continue after login succeeds. If browser-control tools are not loaded, use the available tool discovery/browser tooling; if live automation is unavailable, return the exact field values for the user to paste.
6. Resolve the time block. Use the selected time block if the page already opened the modal. If no modal is open and the user supplied a time range, select that range on the calendar first. If the user did not supply time values, apply the default random/free-slot rule: query existing worklogs for the target local day and choose a non-overlapping slot lasting 1-3 hours with a start time after 09:00 and before 20:00 local time.
7. Immediately normalize the visible modal values: set `记录工时` and `开始时间` to the requested or selected values before working on dropdowns. Calendar drag may open the modal with the wrong range.
8. Set `工作项类型` to `缺陷`. For Semi-style dropdowns, if clicking the visible option text does not select it, type/filter the option and use keyboard navigation (`ArrowDown`, `Enter`) until the combobox value changes.
9. Search `工作项实例` by exact bug id, issue key, and exact title.
10. If UI search returns `暂无数据` for an exact Feishu issue URL/id, use the API fallback in [references/worklog-fields.md](references/worklog-fields.md). Do this only when the issue detail API confirms the same project, type `issue`, exact `work_item_id`, and exact title.
11. Fill `登记日志`.
12. Submit only when the user explicitly asked to record/submit work hours or this skill is running automatically after a bug-fix PR was submitted/opened, and the bug and log are exact. Treat the default random/free-slot rule as user-approved when time is missing; do not ask for confirmation solely because the time was selected by that rule. If the bug or log was inferred, summarize the fields and ask for confirmation before submitting.
13. Verify by querying or reloading the worklog page. If refresh opens month view, switch to week view. Confirm total time, date cell time, work item display, and log snippet.

## Guardrails

- When login, CAPTCHA, permission, or page-loading steps require user action, tell the user exactly what manual action is needed and pause. For login, ask the user to complete login in the browser; never ask for or handle account credentials yourself.
- Do not invent bug descriptions or fix plans. Use `待确认` only in drafts, never in a submitted log.
- Do not derive the worklog duration from issue status/elapsed fields such as `已进行 8 小时`; use only the user's requested values, the selected calendar range, or an allowed random/free-slot rule.
- Do not choose a similar work item. UI search failure is not permission to guess; either use the exact API fallback or ask the user.
- Do not auto-submit before the bug-fix PR is submitted/opened unless the user explicitly asks to record work hours earlier.
- Do not hardcode session secrets such as `x-worklog-key`; read them from current network traffic when API fallback is needed.
- Preserve existing repo-specific bug workflows. This skill runs after the bug context is available; it does not replace debugging, verification, commits, PRs, or bug-memory recording.
- If the user asks only for a draft, prepare the worklog text and stop before live submission.
