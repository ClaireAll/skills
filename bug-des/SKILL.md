---
name: bug-des
description: Ask for 问题描述、问题原因、修复方法, then ask where the diff lives (package path) and require git diff context to complete the full bug template by inferring remaining fields from the fx-data-web repo (D:\work\fx-data-web) and the user's changes. Expand brief原因/修复方法 into fuller, concrete descriptions. Omit 问题描述 in the final output. Use when the user wants this project-aware template completion.
---

# Bug Template Filler (fx-data-web)

Use `assets/template.txt` as the base template.

## Workflow

1. Load `assets/template.txt` (UTF-8).
2. Collect user-provided fields (ask if missing):
   - 问题描述
   - 问题原因
   - 修复方法
3. Ask for diff location (required):
   - “改动的 diff 在哪个包/路径？请给出相对 D:\\work\\fx-data-web 的路径（例如 packages/jsy-web）。”
4. Require git diff context:
   - Prefer running `git status` and `git diff` scoped to the provided path.
   - If git diff cannot be accessed, ask the user to paste the diff (or a file list + key snippets). Do not guess without diff evidence.
5. Inspect repo context in `D:\\work\\fx-data-web` scoped to the diff location to infer remaining fields:
   - Use `rg` to locate touched modules, routes, APIs, and components referenced by the diff.
   - Use `readme.md` and routing/config files to map changes to pages and entry points.
   - Identify tests near the changed code (e.g., `vitest`, `__tests__`, `*.spec.*`, `*.test.*`).
   - Treat comments, screenshots, attachments, and linked docs as first-class bug evidence when the user provides them; do not rely on the title/description alone.
6. Expand brief原因/修复方法 into fuller, concrete descriptions:
   - 根因: explain the mechanism (what code path + why it failed) using diff evidence.
   - 修复方法: describe the code change in terms of behavior (what was changed, where, and why it fixes the issue).
   - Keep it accurate and avoid inventing details not supported by the diff or repo context.
7. Fill the template:
   - If a label line exists (e.g., `【问题原因】：`), insert the user value after the label.
   - If a label line lacks `：`, add `：` before inserting the value.
   - If the template does not contain `【问题描述】`, prepend a new line `【问题描述】：<value>` at the top.
   - Preserve all other lines and their order.
8. Field completion rules (project-aware + diff-scoped):
   - 影响范围: list impacted modules/pages/routes/roles/environments based on changed files, call sites, and data-flow evidence within the diff scope; do not write “no impact” from intuition alone.
   - 功能: summarize user-visible behavior changes (features, flows, UI states) based on affected modules/pages.
   - 性能: note any performance implications; if no evidence, write “无明显影响”.
   - 测试范围: list affected tests; if none exist, provide minimal manual checks with concrete URLs from the repo (or mark as “待补充”). Write checks as operation + expected result; for bug fixes with automated tests, mention base-red/fix-green evidence when available.
9. Output rules:
   - Output only the completed full template, no extra commentary.
   - Do NOT include 问题描述 in the final output; omit that line even if the template contains it.
   - Ensure 测试范围 is the last item in the output.

## Notes

- If repo evidence is insufficient to complete a field, ask a concise follow-up question and mark that field as “待确认”.
- Prefer concrete file paths and routes over generic descriptions.
- If the diff path is outside the repo or unclear, ask the user to re-enter it.
