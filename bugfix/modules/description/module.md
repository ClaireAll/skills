# Bug Description Writer

Use `template.txt` as the only output structure for Feishu bug comments and matching bug-fix PR descriptions. Facts control wording.

**REQUIRED SUB-SKILL:** After the factual draft is complete, use `human-writing` in rewrite mode to make the Chinese read naturally. It may improve expression only; it must not add, remove, or reinterpret facts.

## Final Output Contract

Start every draft by copying the structure in `template.txt`. Do not draft headings from memory or borrow another bug/PR template.

Keep `原因` and `改动内容` as the first two section headings, in that order. Select the final section from the evidence:

- Concrete residual risk: use `可能导致的问题`.
- No concrete residual risk, but directly affected flows are known: use `影响的场景`.
- Neither is supported: omit the final section.

Use at most one final section; do not retain an empty section or fill it with `略`. The template below shows the affected-scenarios branch:

```markdown
## 原因
**Bug 原因：** <evidence-backed root cause, or 原因待确认。>

**可能导致问题的来源提交：**
- **来源提交：** `<short-sha>`（<author>，<YYYY-MM-DD>，<behavior summary>）。其中对 <affected behavior> 的改动可能导致 <bug symptom>。关联事项：<linked references>。

## 改动内容
- <confirmed user-facing change>

## 影响的场景
- <directly affected operation, flow, or feature supported by the change>
```

User-facing prose must not contain source file paths, file names, extensions, directories, component file names, or diff-hunk identifiers. Use those only to establish the internal facts, then describe the affected feature, flow, interaction, or business behavior instead. Include a source artifact only when the user explicitly asks for it.

Do not substitute or add headings such as `疑似原因`, `变更描述`, `测试情况`, `简要描述`, `问题描述`, `问题原因`, `修复内容`, `修改方案`, `验证结果`, `关联Issue`, or `Checklist`.

## Concise Output Rules

Keep the final comment short while preserving every independently meaningful user-visible change:

- `原因` 用 1～2 句说明故障机制；不写排查过程、背景介绍或实现细节。
- 来源提交每项只保留“提交信息 + 改动行为 + 可能造成的现象 + 关联链接”，合并重复候选，不重复解释同一因果链。
- `改动内容` 按独立改动逐条列出；多个内部改动不能合并成一条，每个 bullet 尽量只写一句话，直接说明用户可见结果。完整性通过逐条覆盖有意义的改动保证，不逐行复述 diff、调用链或文件改动。
- `可能导致的问题` 每个场景只写一句“触发条件 + 可能结果”，不追加分析、验证、处理建议或保护措施。
- `影响的场景` 只列本次改动直接涉及的操作、流程或功能范围，不把尚未验证的恢复结果写成已通过。
- 删除重复主语、套话、过程连接词和同义改写；不要为了显得完整而补充源码中没有的背景。

先在内部保留完整的行为清单，再将同一用户结果合并到最终评论。内部清单不能直接整段复制到评论中。

### External Comment Filter

The completed template contains only the following information:

- `原因`：解释当前现象所需的最短因果链。
- `来源提交`：能够说明当前现象由何种改动引入的最少提交；只有中间修复本身造成了当前现象时，才把它列为来源提交。
- `改动内容`：最终产生的用户可见变化；提交哈希、PR 链接、测试结果、工时和交付状态留在交付汇报中。
- `可能导致的问题` / `影响的场景`：有具体风险时写证据支持的风险场景；没有具体风险时写有依据的直接影响范围。

输出前为每句话匹配上述一个位置；无法匹配的内容不进入评论。排查过程、尝试过但未引入当前现象的失败方案，以及同一因果链的重复解释只保留在内部证据中。

## Feishu MCP Publishing

Publish or update authorized Feishu bug comments directly through available Feishu Project MCP comment tools. Use plain text or tool-supported Markdown, preserving template section order, bullets and links. Do not apply custom colors, font sizes or rich-text clipboard formatting, or open a browser merely to style a comment.

Create one comment or update the specified existing comment, then verify the saved content through MCP. If a write times out or its result is unclear, query the original target before retrying to avoid duplicates. If MCP is unavailable or authorization expires, help restore the existing connection and retain the draft; do not automatically switch to browser publishing. A browser may be used for required human login or authorization; verify MCP recovery separately. Publishing still requires user authorization. Chat drafts and PR descriptions remain Markdown.

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
   - For each residual risk, record one concrete scenario and the possible user-visible result. If none is supported, record the operations, flows, or features directly affected by the change.
3. Fill the template:

| Section | Fill rule |
| --- | --- |
| `原因` | Write `Bug 原因` first, followed by `可能导致问题的来源提交`. Keep the cause behavior-focused and evidence-backed. Use `原因待确认。` when the cause is not established. Use one complete bullet per independently supported source commit; when none is supported, write `**可能导致问题的来源提交：** 略`. |
| `改动内容` | Provide a complete behavior-level inventory of the final diff. Keep each independently meaningful feature, flow, interaction, business rule, state guard or recovery, validation or error-handling behavior, and API or data-contract behavior as a separate concise bullet. Do not merge distinct changes. Do not list diff lines, call chains, or implementation steps. Pure formatting or comment-only changes may be omitted. Do not use checkboxes. |
| `可能导致的问题` | Use only for evidence-backed residual risks. Write one sentence per bullet combining the condition or user action with its possible result. Do not add field labels, analysis, mitigation, verification status, or follow-up actions, or present a possible result as an observed fact. |
| `影响的场景` | When no concrete residual risk is supported, list only the operations, flows, or features directly affected by the change. Do not invent a risk or imply that unverified scenarios have passed. |

   Use this shape for each supported scenario:

   ```markdown
   - <具体条件或用户操作>时，可能<具体结果>。
   ```

   If reviewed evidence supports no concrete risk, omit `可能导致的问题` and use `影响的场景` for the direct affected flows supported by the final diff or requirements. If neither is supported, omit the final section instead of leaving an empty section or writing `略`.

   If evidence supports a concrete potential failure but its outcome is not sufficiently verified, use:

   ```markdown
   - <具体场景>待验证。
   ```

   Do not invent a risk or use generic labels such as `逻辑问题`, `交互问题`, or `性能问题` merely to fill the section.
4. Humanize the factual draft with `human-writing`:
   - Treat it as Chinese technical rewrite work with compression, not expansion.
   - Give it only the completed body text after source-artifact references have been removed. The selected headings, cause/source order, bullets, links, and spacing remain under this module’s control.
   - Keep the tone concise, professional, and direct. Prefer one sentence per change, risk, or affected-scenario bullet and natural sentence rhythm.
   - Preserve every fact, uncertainty, negation, commit detail, Markdown link, complete change item, and risk or affected scenario.
   - Remove repetition, background, causal claims not in the facts, verification claims, reassurance, personal voice, marketing language, source-file information, and unnecessary transition phrases without changing the certainty level.
5. Run the final evidence gate:
   - Check the heading branch against `template.txt`: `原因` then `改动内容`, followed by at most one of `可能导致的问题` or `影响的场景` according to the evidence.
   - Remove every HTML comment and placeholder.
   - Confirm `原因` states the Bug cause before source commits and uses the exact pending wording when evidence is missing.
   - Confirm every recognized item id in source attribution is linked correctly.
   - Confirm the completed prose contains no source path, file name, extension, directory, component file name, or diff-hunk identifier unless explicitly requested.
   - Compare the internal final-diff behavior list with `改动内容`; every independently meaningful behavior change must have a corresponding bullet.
   - Confirm `可能导致的问题` is present only for concrete supported risks, and contains one-sentence possible-result or pending-scenario bullets. Otherwise use `影响的场景` for supported direct effects, or omit the final section; never leave an empty final section or use `略` as its content.
   - Confirm each sentence is supported by the diff, issue context, history, verification output, or user-provided evidence.
6. Output only the completed template. Use the same completed content for the Feishu comment and PR description unless the user asks for different wording.

## Missing Evidence

- Ask one concise follow-up only when missing information prevents an accurate completed template.
- Use `原因待确认。` when the root cause is not established; do not invent one.
- Use `**可能导致问题的来源提交：** 略` when history cannot identify a supported candidate; do not ask for more history solely to fill this field.
- When no concrete risk is supported, use `影响的场景` for direct affected flows supported by the available evidence; if neither is supported, omit the final section. Lack of verification alone is not a risk scenario.
- If the diff path is outside the repo or cannot be inferred, ask for the relevant path, file list, or diff snippet.
