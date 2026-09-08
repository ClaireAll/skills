---
name: bug-des
description: Use when writing, publishing, or updating a Chinese Feishu bug comment, bug description, or bug-fix PR description for fx-data-web or fv-web2, including colored rich-text comments.
---

# Bug Description Writer

Use `assets/template.txt` as the only output structure for Feishu bug comments and matching bug-fix PR descriptions. Facts control wording.

**REQUIRED SUB-SKILL:** After the factual draft is complete, use `human-writing` in rewrite mode to make the Chinese read naturally. It may improve expression only; it must not add, remove, or reinterpret facts.

## Final Output Contract

Start every draft by copying the structure in `assets/template.txt`. Do not draft headings from memory or borrow another bug/PR template.

Output exactly these three Feishu rich-text H2 headings, in this order, with no renamed, omitted, or additional headings:

```markdown
## 原因
**Bug 原因：** <evidence-backed root cause, or 原因待确认。>

**可能导致问题的来源提交：**
- **来源提交：** `<short-sha>`（<author>，<YYYY-MM-DD>，<behavior summary>）。其中对 <affected behavior> 的改动可能导致 <bug symptom>。关联事项：<linked references>。

## 改动内容
- <confirmed user-facing change>

## 可能导致的问题
- <concrete scenario and its possible result>
```

User-facing prose must not contain source file paths, file names, extensions, directories, component file names, or diff-hunk identifiers. Use those only to establish the internal facts, then describe the affected feature, flow, interaction, or business behavior instead. Include a source artifact only when the user explicitly asks for it.

Do not substitute or add headings such as `疑似原因`, `变更描述`, `测试情况`, `简要描述`, `问题描述`, `问题原因`, `修复内容`, `修改方案`, `验证结果`, `关联Issue`, or `Checklist`.

## Feishu Rich-Text Publishing

When publishing or updating a Feishu bug comment, colored rich text is the default. Keep `assets/template.txt` as the content source, then apply this presentation:

| Content | Style |
| --- | --- |
| `原因` | 20px, bold, `#B42318` |
| `改动内容` | 20px, bold, `#067647` |
| `可能导致的问题` | 20px, bold, `#B54708` |
| `Bug 原因：` | 14px, normal, `#B42318` |
| `可能导致问题的来源提交：` | 14px, normal, `#175CD3` |
| Body and list items | 14px, normal, default text color |

Use the Feishu API to create one plain-text fallback comment first. Then use browser automation to edit that same comment and paste rendered rich text through the system clipboard; copying HTML source text is not sufficient. Never create a second comment for the colored version.

Before sending the edited comment, verify that the three headings have the required colors and size, body text and list items render at 14px with normal weight, links still work, no unexpected emoji or blank heading was inserted, and only one comment will remain. Do not use `!important`; Feishu strips it. If rich-text paste or verification fails, cancel the edit, preserve the plain fallback comment, and tell the user that color formatting was not applied.

This publishing workflow applies only when writing to Feishu. A draft returned in chat and a PR description remain Markdown.

## Cause And Source Commit Attribution

Write the evidence-backed Bug cause first. Explain the faulty behavior or state transition that produces the symptom without naming source artifacts. When the available evidence cannot establish the cause, write exactly:

```markdown
**Bug 原因：** 原因待确认。
```

After the cause, list only history-backed commits that may have introduced the problem. Each candidate must identify the behavior changed by that commit and connect it to the current symptom. Use `可能` unless causality is proven. Do not select a commit from message similarity alone.

When no history-backed candidate can be located, write exactly:

```markdown
**可能导致问题的来源提交：** 略
```

Replace every recognized standalone item id found in a source commit or its context with a Markdown link. Preserve the original label and id exactly; do not invent links for unrecognized ids.

| Item id | Markdown link rule |
| --- | --- |
| `f-<id>` | `[f-<id>](https://project.feishu.cn/b2rl2h/issue/detail/<id>)` |
| `m-<id>` | `[m-<id>](https://project.feishu.cn/b2rl2h/story/detail/<id>)` |
| `g-<id>` | `[g-<id>](https://project.feishu.cn/b2rl2h/assignment/detail/<id>)` |
| `s-<id>` | `[s-<id>](https://project.feishu.cn/b2rl2h/s/detail/<id>)` |
| `JSY-<id>` | `[JSY-<id>](https://work.fineres.com/browse/JSY-<id>)` |
| `REPORT-<id>` | `[REPORT-<id>](https://work.fineres.com/browse/REPORT-<id>)` |
| `KERNEL-<id>` | `[KERNEL-<id>](https://work.fineres.com/browse/KERNEL-<id>)` |

## Workflow

1. Collect evidence:
   - Issue symptom, confirmed root cause, repair approach, title, id, or URL when available.
   - Scoped `git status` and `git diff` from `D:\work\fx-data-web` or `D:\work\fv-web2`.
   - Candidate source commits from targeted `git log`, `git show`, and, when useful, `git blame` or history search.
   - Nearby routes, APIs, components, actual verification output, screenshots, attachments, comments, and linked documents when they explain the change or residual risk.
2. Lock the facts before drafting:
   - Record source paths and implementation details only in the internal fact set.
   - Record the confirmed cause or mark it pending. Never infer a cause from a file name alone.
   - For each source-commit candidate, record its short hash, author, date, subject, linked item ids, changed behavior, and evidence connecting it to the symptom.
   - Record every independently meaningful behavior-level change in the final diff.
   - For each residual risk, record one concrete scenario and the possible user-visible result.
3. Fill the template:

| Section | Fill rule |
| --- | --- |
| `原因` | Write `Bug 原因` first, followed by `可能导致问题的来源提交`. Keep the cause behavior-focused and evidence-backed. Use `原因待确认。` when the cause is not established. Use one complete bullet per independently supported source commit; when none is supported, write `**可能导致问题的来源提交：** 略`. |
| `改动内容` | Provide a complete behavior-level inventory of the final diff. Use one bullet for each independently meaningful feature, flow, interaction, business rule, state guard or recovery, validation or error-handling behavior, and API or data-contract behavior that changed. Do not merge distinct changes merely to shorten the comment. Pure formatting or comment-only changes may be omitted. Do not use checkboxes. |
| `可能导致的问题` | Write only concrete scenarios. Use one natural sentence per bullet that combines the relevant condition or user action with its possible result. Do not add field labels, analysis, mitigation, verification status, or follow-up actions. A scenario must not be presented as observed fact unless evidence confirms it. |

   Use this shape for each supported scenario:

   ```markdown
   - <具体条件或用户操作>时，可能<具体结果>。
   ```

   If reviewed evidence supports no specific scenario, write exactly:

   ```markdown
   略
   ```

   If a concrete scenario is known but its outcome is not sufficiently verified, use:

   ```markdown
   - <具体场景>待验证。
   ```

   Do not invent a risk or use generic labels such as `逻辑问题`, `交互问题`, or `性能问题` merely to fill the section.
4. Humanize the factual draft with `human-writing`:
   - Treat it as Chinese technical rewrite work and use minimum intervention.
   - Give it only the completed body text after source-artifact references have been removed. The three headings, cause/source order, bullets, links, and spacing remain under `bug-des` control.
   - Keep the tone concise, professional, and direct. Prefer clear subjects and natural sentence rhythm.
   - Preserve every fact, uncertainty, negation, commit detail, Markdown link, complete change item, and risk scenario.
   - Do not add background, causal claims, verification claims, reassurance, personal voice, marketing language, source-file information, or a stronger or weaker certainty level.
5. Run the final evidence gate:
   - Compare every `##` heading with `assets/template.txt`; exactly three headings must appear in the same order.
   - Remove every HTML comment and placeholder.
   - Confirm `原因` states the Bug cause before source commits and uses the exact pending wording when evidence is missing.
   - Confirm every recognized item id in source attribution is linked correctly.
   - Confirm the completed prose contains no source path, file name, extension, directory, component file name, or diff-hunk identifier unless explicitly requested.
   - Compare the internal final-diff behavior list with `改动内容`; every independently meaningful behavior change must have a corresponding bullet.
   - Confirm `可能导致的问题` contains only one-sentence scenario bullets with a possible result, a one-sentence pending scenario, or exactly `略`.
   - Confirm each sentence is supported by the diff, issue context, history, verification output, or user-provided evidence.
6. Output only the completed template. Use the same completed content for the Feishu comment and PR description unless the user asks for different wording.

## Missing Evidence

- Ask one concise follow-up only when missing information prevents an accurate completed template.
- Use `原因待确认。` when the root cause is not established; do not invent one.
- Use `**可能导致问题的来源提交：** 略` when history cannot identify a supported candidate; do not ask for more history solely to fill this field.
- Use `略` when no supported risk scenario can be identified; use the pending scenario form when only the result remains unverified.
- If the diff path is outside the repo or cannot be inferred, ask for the relevant path, file list, or diff snippet.
