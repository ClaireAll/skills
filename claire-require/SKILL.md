---
name: claire-require
description: Use proactively when the user describes a desired feature, behavior change, interaction rule, acceptance condition, or a problem with an intended improvement, even in ordinary conversation without naming this skill. Read and clarify requirements from Feishu, Figma, local files, or pasted text; compare or synchronize interaction specs with scoped source code. Do not use solely for how-to questions, bug investigation, casual feedback without a change request, or unambiguous mechanical edits. Use claire-test for formal code findings and self-check cases.
---

# Claire Requirements

Route requirement work to the correct internal module without asking the user to choose one.

## Recognize requirement intent

Judge the user's requested outcome in conversation context, not the presence of the word “需求”, a document link, or an explicit skill invocation. Proactively use this skill for a desired new capability, changed product behavior, business/interaction rules, acceptance conditions, or a request to understand requirement materials. A problem paired with a desired improvement is an incomplete requirement; do not invent its solution.

- “导出时增加一个确认弹窗” and “无权限的人可以查看，但不能编辑” express intended behavior: read the input module and extract the stated rules; clarify only material gaps.
- “用户总找不到入口，希望更容易发现” supplies a problem and goal: inspect available context, then clarify consequential choices rather than assuming a particular UI change.
- “导出怎么操作” is a how-to question; “为什么导出失败” is an investigation. Use the appropriate workflow unless the conversation also asks for a new behavior.
- “这个弹窗好难用” alone is feedback, not authorization to redesign it. Use context to determine the requested help; ask one focused question only if the distinction materially changes the work.
- A precise reversible edit such as “把按钮文案改成保存” can proceed directly within scope without a requirement interview. Explicit requests to use this skill still apply, without adding unnecessary gates.

Inspect provided sources and context before asking whether something is a requirement. When uncertainty would materially affect scope, expected results, risk or cost, ask a focused intent question (for example, whether the user wants an explanation or a behavior change). Otherwise state a safe assumption and continue. Skill selection alone does not trigger an interview, require a new artifact, or grant implementation/testing permission; preserve the existing gate only for active clarification and authored or materially revised requirement contracts.

## Automatic Routing

| User intent | Modules to read before acting |
| --- | --- |
| Describe a desired feature, behavior change, interaction/business rule, or acceptance condition in natural language | `modules/read-feature-input/module.md`; use the clarification route only for material unresolved decisions |
| Read, summarize, clarify, or reconcile a feature document, interaction spec, Feishu page, Figma file, local requirement file, or mixed input | `modules/read-feature-input/module.md` |
| Generate self-check cases or formally audit source code against requirements | Hand off to `../claire-test/SKILL.md`; share sources already read instead of interpreting them again |
| Compare a Feishu, Figma, or local interaction document with specified source code; identify contradictions or missing documentation | `modules/read-feature-input/module.md`, then `modules/interaction-spec-sync/module.md` |
| Update a specified interaction document from that comparison | `modules/read-feature-input/module.md`, then `modules/interaction-spec-sync/module.md`; load `feishu-doc-writer` before writing to Feishu |
| Requirement is materially ambiguous, the user asks to be questioned, or the user invokes a grill-me/interview/deep-questioning mode | `modules/read-feature-input/module.md`, then [intent-and-acceptance](references/intent-and-acceptance.md) and the clarification loop below |
| Draft or revise a requirement brief or acceptance criteria | Read the input module, then [intent-and-acceptance](references/intent-and-acceptance.md); produce only the requested requirement artifact, subject to the strict review gate |
| Understand a requirement and then review its implementation | Read the input module; complete any active clarification/specification review gate before handing off to `../claire-test/SKILL.md` with confirmed rules and open questions |

When more than one row matches, load the relevant modules. Ordinary requirement reading does not generate test plans or launch tests.

The strict review gate below takes precedence over routes that request later work. It applies when actively clarifying or authoring requirements, not when simply extracting clear existing rules or receiving an already-confirmed contract for a direct review.

Use interaction-spec-sync when the goal is to explain or maintain the interaction document. If the user asks for code defects, fix proposals, or an implementation audit, `claire-test` takes precedence even when document discrepancies are part of the request; do not run two full audits.

## Route Rules

1. Identify every input source before selecting modules. Do not let a single link hide related Figma, Feishu, local-file, or pasted-text inputs.
2. Load every module named by the selected route before interpreting the requirement or writing an output.
3. The input module owns source handling, evidence alignment, Figma discipline, and clarification of missing facts.
4. `claire-test` owns code-problem reports, proposed fixes, and requested self-check cases. Do not retain a second test-plan generator here.
5. The interaction-spec-sync module owns code-to-spec comparison and in-place document annotations. It does not modify application code or replace the document-writing skill.
6. For code-to-spec comparison, require a source directory or file scope. Ask one focused clarification only when it is unavailable after inspecting all provided sources.
7. Default to a read-only audit. Update a Feishu document only when the user explicitly requests a write or sync operation.
8. Ask one focused clarification only when a required fact is unavailable after the selected modules have inspected all provided sources. When the user explicitly asks for deep questioning, or the ambiguity would change the implementation, read `references/intent-and-acceptance.md` and use the clarification loop below instead of guessing.
9. Keep ordinary clarification in the current conversation. When an unresolved fact belongs to a named stakeholder, record it explicitly as an open question instead of inventing an answer.
10. Do not invoke `fx-bdd:*` or `fx-data-test-skills:*` for ordinary requirement, development, or testing work. Those plugins are reserved for an explicit BDD request.

## Requirement Handoff

Return a concise understanding grounded in the sources: purpose and scope, entries and roles, defaults and state changes, validation and async behavior, acceptance criteria, development considerations, and unresolved questions. Include only the parts relevant to the request.

Give confirmed rules stable source references so a later `claire-test` audit can trace them to the original text, annotation, or image. Distinguish stated requirements, user-confirmed decisions, implementation observations, and assumptions. Never use the current implementation alone to decide intended behavior.

For authored or materially revised requirements, use `references/intent-and-acceptance.md` to separate the problem from a proposed solution, state explicit non-goals, and translate supported rules into observable acceptance conditions. Label new interpretations and numerical targets as proposals until confirmed; do not quietly promote them into requirements. Extracting already-explicit acceptance conditions from a clear source is still ordinary reading.

Keep the result in the conversation unless the user requests an artifact. Temporary input copies belong in a task-specific directory under `D:/Claire/temp`. A supplied but unread document must be named as unread; do not present its contents as known.

## Clarification Loop

Use this as the built-in grill-me/interview capability; do not create a separate Skill. Before choosing technical solutions, state a tentative one-sentence read of the desired outcome and the material gap. Check who benefits, the problem they face, observable success, binding constraints, and scope against sources already read; ask only about missing information that could change the result. Do not invent a confidence percentage.

1. Map the material decisions as a design tree: record what each decision depends on and what its answer would change. Keep this working map internal unless the user asks to see it; do not expand it into unrelated product design.
2. Separate discoverable facts from user decisions. Inspect supplied documents, the scoped repository, or available read-only tools for facts instead of asking the user to look them up. An unread source or unfinished lookup remains an unsettled prerequisite; do not treat it as evidence or block independent questions on it.
3. Identify the current frontier: decisions whose prerequisites are already settled. Choose the most consequential unanswered decision from that frontier. A question that depends on another unanswered question belongs to a later round.
4. Ask one question at a time by default. State the concrete uncertainty, why it matters, your recommended answer, and the main tradeoff when there is enough evidence to recommend one. Use observable examples or choices; a recommendation is not a confirmed requirement. If the user explicitly asks for a batch, group only independent frontier questions and keep their answers separately identifiable.
5. After each answer, record the confirmed decision and recompute the frontier. Revisit downstream decisions when a prerequisite changes; do not repeat settled questions or silently keep an invalid assumption.
6. Stop when no material decision remains, the user ends the interview, or the remaining decisions belong to named stakeholders and have been recorded as open questions. Do not interrogate every conceivable branch or require answers to facts that can be safely verified.
7. Present the proposed understanding, including confirmed individual decisions, assumptions, non-goals, and remaining questions. Request explicit review and end the turn under the strict review gate; answers to individual questions do not approve the assembled contract. Do not start an audit, implementation, new document-authoring stage, or publication as downstream work in that turn. A local draft explicitly selected as the current stage's review artifact follows gate 1 below, not this downstream prohibition.

## Strict Review Gate (User Choice B)

Apply this gate to active clarification and authored or materially revised requirement contracts, even if an earlier request also asked for downstream work. Existing confirmed rules do not need to be re-approved just because this skill reads them.

1. **Ready for review:** deliver a concrete understanding or requested requirement draft for the current selected stage, explicitly distinguish proposed additions from confirmed facts, ask the user to confirm or correct this version, then **stop the turn**. Do not start downstream work or write an unsolicited artifact. An explicitly requested local draft may be this stage's review artifact; an earlier chained request for a later document is not permission to skip the intent gate. Publishing or changing an existing document is not implied.
2. **Later confirmation:** accept explicit approval of this specific version, not silence, a delegated decision, or an unrelated acknowledgment. Return the confirmed intent/requirements and relevant next-step choices, then **stop this turn too** without invoking downstream tools. Do not automatically resume the earlier chained request.
3. **Corrections or unresolved decisions:** revise affected parts and present the corrected version for review. Decisions awaiting a stakeholder remain open, not approved. If questioning stalls or the user stops it, report the precise gap and current draft rather than assuming agreement.
4. **Next stage:** proceed only after the user selects or authorizes that stage in a subsequent turn. Confirming intent does not approve a new spec, code changes, tests, or publication. A new or materially changed requirement draft has its own review gate; unchanged source reading does not.

See `references/intent-and-acceptance.md` for the compact handoff and acceptance format. Pure explanation, mechanical work, clear-source summarization/extraction, and direct review of already-confirmed requirements do not trigger an interview or extra gate.

Understanding remains useful on its own. Formal audits and self-check cases belong to `claire-test`; page execution belongs to explicitly requested `webapp-testing`.

## Upstream Maintenance

The clarification loop adapts `mattpocock/skills`'s `grill-me` and shared `grilling`, plus selected intent and acceptance practices from `addyosmani/agent-skills`'s `interview-me` and `spec-driven-development`. Pinned sources and local adaptations are recorded in [upstreams.json](../upstreams.json); attribution is in [THIRD_PARTY_NOTICES.md](../THIRD_PARTY_NOTICES.md). Preserve the strict review gate, one-question-at-a-time routing, read-only defaults, and explicit BDD boundary when syncing. The full upstream lifecycle is not installed or invoked.
