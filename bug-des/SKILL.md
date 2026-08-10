---
name: bug-des
description: Create Chinese Feishu bug comments or PR descriptions for fx-data-web/fv-web2 from issue context plus git diff evidence. Use when the user asks to comment on a Feishu bug, prepare a bug-fix PR description, fill the team's bug template, or summarize change description, linked issue, changed content, testing, and checklist items.
---

# Bug Description Writer (fx-data-web)

Use `assets/template.txt` as the default template for Feishu bug comments and bug-fix PR descriptions.

## Workflow

1. Collect issue context when available:
   - 问题描述
   - 问题原因
   - 修复方案
   - Feishu/JIRA/工单 title, id, or URL
2. Ask for diff location only when it cannot be inferred from the current repo state:
   - `改动的 diff 在哪个包/路径？请给出相对 D:\work\fx-data-web 或 D:\work\fv-web2 的路径，例如 packages/jsy-web。`
3. Require git diff context:
   - Prefer running `git status` and `git diff` scoped to the provided path.
   - If git diff cannot be accessed, ask the user to paste the diff or a file list plus key snippets. Do not guess without diff evidence.
4. Inspect repo context in `D:\work\fx-data-web` or `D:\work\fv-web2` scoped to the diff location:
   - Use `rg` to locate touched modules, routes, APIs, and components referenced by the diff.
   - Use README and routing/config files to map changes to pages and entry points.
   - Identify tests near the changed code, such as `vitest`, `__tests__`, `*.spec.*`, or `*.test.*`.
   - Treat comments, screenshots, attachments, and linked docs as bug evidence when the user provides them.
5. Fill `assets/template.txt` and preserve its section order:
   - `变更描述`: replace the HTML comment with a concise evidence-backed summary of the change. Include the bug symptom, root cause, fix, and known impact/risk when the evidence supports them.
   - `关联Issue`: replace `#12345` with the Feishu/JIRA/工单 id or URL from the issue context. If no id is available, use `- 待补充`.
   - `改动内容`: replace the sample checkbox items with concrete changed files/modules/behaviors from the diff. Check only items that are confirmed by evidence.
   - `测试情况`: replace the sample checkbox items with concrete verification results. Check only tests or manual checks that were actually run or explicitly provided.
   - `Checklist`: keep the checklist section, checking only items supported by evidence. Leave unchecked when not confirmed.
6. Output only the completed template for comments or PR descriptions, with no extra commentary.
7. Keep it accurate and avoid inventing details not supported by the diff, issue context, or repo evidence.

## Notes

- If repo evidence is insufficient to complete a field, ask a concise follow-up question or mark that field as `待补充`.
- Prefer concrete file paths and routes over generic descriptions.
- If the diff path is outside the repo or unclear, ask the user to re-enter it.
