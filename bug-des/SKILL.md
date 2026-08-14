---
name: bug-des
description: Create natural, evidence-backed Chinese Feishu bug comments or PR descriptions for fx-data-web/fv-web2 from issue context and git diff evidence. Use when the user asks to write a bug comment, PR description, or the team's bug template.
---

# Bug Description Writer

Use `assets/template.txt` as the only output structure for Feishu bug comments and matching bug-fix PR descriptions. Facts control wording.

**REQUIRED SUB-SKILL:** After the factual draft is complete, use `human-writing` in rewrite mode to make the Chinese read naturally. It may improve expression only; it must not add, remove, or reinterpret facts.

## Final Output Contract

Start every draft by copying the structure in `assets/template.txt`. Do not draft headings from memory or borrow another bug/PR template.

The five section labels are Feishu rich-text H2 headings. Emit each one literally with the Markdown prefix `## `; a plain-text label, bullet label, quotation, bold-only text, HTML heading, or renamed label is invalid.

Output exactly these five headings, in this order, with no renamed, omitted, or additional headings:

```markdown
## 疑似原因
- 来源提交：`<short-sha>`（<author>，<commit date>，<behavior summary>）。其中对 <affected behavior> 的改动可能导致 <bug symptom>。关联事项：<linked references>。

## 变更描述
<evidence-backed summary>

## 改动内容
- <confirmed user-facing change>

## 测试情况
- <actual functional verification result or pending confirmation>

## 可能导致的问题
- <condition-specific supported risk, or a qualified no-risk/pending statement>
```

User-facing prose must not contain source file paths, file names, extensions, directories, component file names, or diff-hunk identifiers. Use those only to establish the internal facts, then describe the affected feature, flow, interaction, or business behavior instead. Include a source artifact only when the user explicitly asks for it.

Do not substitute headings such as `问题描述`, `问题原因`, `修复内容`, `修改方案`, `验证结果`, `关联Issue`, or `Checklist`. Any output containing one of those headings is invalid and must be rewritten from `assets/template.txt`. Always keep `疑似原因` and `可能导致的问题`.

## Source Commit Attribution

Use this output shape when a candidate is available. Keep the explanation behavior-focused so it identifies the code change that may have led to the bug without naming files. When no history-backed candidate can be located, the entire `疑似原因` content must be exactly `略` with no bullet or explanation.

```markdown
- 来源提交：`<short-sha>`（<author>，<YYYY-MM-DD>，<behavior summary>）。其中对 <affected behavior> 的改动可能导致 <bug symptom>。关联事项：[f-123](https://project.feishu.cn/b2rl2h/issue/detail/123)。
```

Replace every recognized standalone item id found in the source commit, its context, or the cause explanation with a Markdown link. Preserve the original label and id exactly; do not invent links for unrecognized ids. When multiple candidates are independently supported, write one complete bullet per candidate; do not list commits based on message similarity alone.

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
   - Issue symptom, confirmed root cause, and repair approach when available.
   - Issue title, id, or URL when the user provides it. Do not add a separate issue section because the template no longer has one.
   - Scoped `git status` and `git diff` from `D:\work\fx-data-web` or `D:\work\fv-web2`.
   - Candidate source commits from targeted `git log`, `git show`, and, when useful, `git blame` or history search. Use changed paths only for investigation; never expose them in the completed comment.
   - Nearby routes, APIs, components, and actual test output when they explain the diff.
   - Screenshots, attachments, comments, and linked documents supplied by the user.
2. Lock the facts before drafting:
   - Record changed files and implementation details only in the internal fact set; do not carry them into the completed comment.
   - For each source-commit candidate, record its short hash, author, date, subject, linked item ids, the behavior it introduced or changed, and why that behavior may explain the symptom.
   - Record confirmed behavior, functional verification, residual risks, and unknowns that must remain qualified.
   - Never infer a root cause, test result, coverage number, user impact, or risk from a file name alone.
3. Fill the template without changing its section order or Markdown shape:

| Section | Fill rule |
| --- | --- |
| `变更描述` | Replace the HTML comment with a concise, evidence-backed summary. Mention symptom, cause, fix, and impact only when each is confirmed. Describe product behavior, not source artifacts. |
| `疑似原因` | Cite only a history-backed source-commit candidate. Include its short hash, known author/date, and a behavior-focused summary; then state which behavior change in that commit may have caused the bug. Use `可能` or `疑似` unless causality is proven. Convert every recognized item id in the entry to the required Markdown link. When no candidate can be established, write only `略`. |
| `改动内容` | Replace the placeholders with one concrete, user-facing feature, flow, interaction, or business-rule change per bullet. Do not mention file paths, file names, extensions, directories, or component file names. Do not use checkboxes. |
| `测试情况` | Replace the placeholders with only functional tests or manual checks that actually ran or were explicitly supplied. State the scenario and observable result, such as a regression scenario, a named test that passed, or a completed user flow. `git diff --cached --check`, `git diff --check`, `git status`, formatting checks, and other source-integrity checks are not functional verification and must never be reported as passing tests. When functional verification is unknown, write `- 功能验证待补充。` instead of claiming success. |
| `可能导致的问题` | Replace the placeholders with evidence-backed residual risks. Each risk must state the trigger condition, affected scope, specific user-visible symptom, and current protection, verification status, or follow-up. Use this form: `- 在 <触发条件> 下，<影响范围> 可能出现 <具体表现>；<当前防护、验证结论或后续动作>。` |

   Do not write generic risk labels such as `逻辑问题`, `交互问题`, or `性能问题`. If reviewed evidence supports no specific residual risk, write `- 已核查 <已验证的范围>，暂未发现明确风险。`; if risk evidence is insufficient, write `- <具体场景> 的影响待验证：尚缺少 <所需测试或证据>。` Do not invent a risk merely to fill the section.

   Do not reintroduce `关联Issue` or `Checklist`. Keep no blank line between a heading and its content, and exactly one blank line between completed sections.
4. Humanize the factual draft with `human-writing`:
   - Treat it as Chinese technical rewrite work and follow its humanization route.
   - Give it only the completed body text after all source-artifact references have been removed. The five headings, bullet structure, item links, and spacing remain under `bug-des` control.
   - Keep the tone concise, professional, and direct. Prefer clear subjects and natural sentence rhythm over template-like wording.
   - Preserve every delivered user-facing fact, uncertainty, negation, source commit hash, author/date, Markdown link, route or API label that is needed for understanding, test result, and risk qualification. Keep the literal `略` unchanged when it is the `疑似原因` content.
   - Do not add background, causal explanation, test coverage, reassurance, personal voice, marketing language, source-file information, or a stronger/weaker certainty level.
   - Do not alter headings, section order, bullet count, Markdown syntax, required spacing, source-commit attribution, item links, or the trigger/scope/symptom/follow-up structure of a risk.
5. Run a final evidence gate:
   - Compare every `##` heading with `assets/template.txt`; they must match exactly, be H2 headings, and appear in the same order.
   - Remove the template HTML comment and every placeholder.
   - Confirm that `疑似原因` contains either a history-backed candidate with short hash, known commit details, a behavior-to-symptom explanation, and correctly linked recognized item ids, or exactly `略`.
   - Confirm that `变更描述` and `改动内容` contain no source file path, file name, extension, directory, or component file name unless the user explicitly requested it.
   - Confirm that `测试情况` contains only actual functional verification or `功能验证待补充。`; do not report a Git diff, status, formatting, or whitespace check as a passing test.
   - Confirm every risk either uses the required trigger/scope/symptom/follow-up form or uses the specific qualified no-risk/pending wording above.
   - Check that each remaining sentence is supported by the diff, issue context, test output, or user-provided evidence.
   - Keep unconfirmed facts explicitly pending rather than fabricating a polished answer.
6. Output only the completed template. Use the same completed content for the Feishu comment and PR description unless the user asks for different wording.

## Missing Evidence

- Ask one concise follow-up only when the missing detail prevents an accurate completed template.
- Otherwise use the template's pending wording for the affected test or risk field.
- When history is insufficient to identify a source commit, write only `略` under `疑似原因` instead of selecting one from commit-message similarity alone. Do not ask for more history solely to fill this section.
- If the diff path is outside the repo or cannot be inferred, ask the user for the relevant path, file list, or diff snippet.
