---
name: claire-require
description: Read and understand Feishu, Figma, local, or pasted requirements; clarify acceptance criteria and important gaps for development and testing; compare or synchronize an interaction document with specified source code. Use claire-test for formal code findings and self-check cases.
---

# Claire Requirements

Route requirement work to the correct internal module without asking the user to choose one.

## Automatic Routing

| User intent | Modules to read before acting |
| --- | --- |
| Read, summarize, clarify, or reconcile a feature document, interaction spec, Feishu page, Figma file, local requirement file, or mixed input | `modules/read-feature-input/module.md` |
| Generate self-check cases or formally audit source code against requirements | Hand off to `../claire-test/SKILL.md`; share sources already read instead of interpreting them again |
| Compare a Feishu, Figma, or local interaction document with specified source code; identify contradictions or missing documentation | `modules/read-feature-input/module.md`, then `modules/interaction-spec-sync/module.md` |
| Update a specified interaction document from that comparison | `modules/read-feature-input/module.md`, then `modules/interaction-spec-sync/module.md`; load `feishu-doc-writer` before writing to Feishu |
| Requirement is materially ambiguous, the user asks to be questioned, or the user invokes a grill-me/deep-questioning mode | `modules/read-feature-input/module.md`, then use the clarification loop below |
| Understand a requirement and then review its implementation | Read the input module, then hand off to `../claire-test/SKILL.md` with confirmed rules and open questions |

When more than one row matches, load the relevant modules. Ordinary requirement reading does not generate test plans or launch tests.

Use interaction-spec-sync when the goal is to explain or maintain the interaction document. If the user asks for code defects, fix proposals, or an implementation audit, `claire-test` takes precedence even when document discrepancies are part of the request; do not run two full audits.

## Route Rules

1. Identify every input source before selecting modules. Do not let a single link hide related Figma, Feishu, local-file, or pasted-text inputs.
2. Load every module named by the selected route before interpreting the requirement or writing an output.
3. The input module owns source handling, evidence alignment, Figma discipline, and clarification of missing facts.
4. `claire-test` owns code-problem reports, proposed fixes, and requested self-check cases. Do not retain a second test-plan generator here.
5. The interaction-spec-sync module owns code-to-spec comparison and in-place document annotations. It does not modify application code or replace the document-writing skill.
6. For code-to-spec comparison, require a source directory or file scope. Ask one focused clarification only when it is unavailable after inspecting all provided sources.
7. Default to a read-only audit. Update a Feishu document only when the user explicitly requests a write or sync operation.
8. Ask one focused clarification only when a required fact is unavailable after the selected modules have inspected all provided sources. When the user explicitly asks for deep questioning, or the ambiguity would change the implementation, use the clarification loop below instead of guessing.
9. Keep ordinary clarification in the current conversation. When an unresolved fact belongs to a named stakeholder, record it explicitly as an open question instead of inventing an answer.
10. Do not invoke `fx-bdd:*` or `fx-data-test-skills:*` for ordinary requirement, development, or testing work. Those plugins are reserved for an explicit BDD request.

## Requirement Handoff

Return a concise understanding grounded in the sources: purpose and scope, entries and roles, defaults and state changes, validation and async behavior, acceptance criteria, development considerations, and unresolved questions. Include only the parts relevant to the request.

Give confirmed rules stable source references so a later `claire-test` audit can trace them to the original text, annotation, or image. Distinguish stated requirements, user-confirmed decisions, implementation observations, and assumptions. Never use the current implementation alone to decide intended behavior.

Keep the result in the conversation unless the user requests an artifact. Temporary input copies belong in a task-specific directory under `D:/Claire/temp`. A supplied but unread document must be named as unread; do not present its contents as known.

## Clarification Loop

Use this as the built-in grill-me capability; do not create a separate Skill.

1. Map the material decisions as a design tree: record what each decision depends on and what its answer would change. Keep this working map internal unless the user asks to see it; do not expand it into unrelated product design.
2. Separate discoverable facts from user decisions. Inspect supplied documents, the scoped repository, or available read-only tools for facts instead of asking the user to look them up. An unread source or unfinished lookup remains an unsettled prerequisite; do not treat it as evidence or block independent questions on it.
3. Identify the current frontier: decisions whose prerequisites are already settled. Choose the most consequential unanswered decision from that frontier. A question that depends on another unanswered question belongs to a later round.
4. Ask one question at a time by default. State the concrete uncertainty, why it matters, your recommended answer, and the main tradeoff when there is enough evidence to recommend one. Use observable examples or choices; a recommendation is not a confirmed requirement. If the user explicitly asks for a batch, group only independent frontier questions and keep their answers separately identifiable.
5. After each answer, record the confirmed decision and recompute the frontier. Revisit downstream decisions when a prerequisite changes; do not repeat settled questions or silently keep an invalid assumption.
6. Stop when no material decision remains, the user ends the interview, or the remaining decisions belong to named stakeholders and have been recorded as open questions. Do not interrogate every conceivable branch or require answers to facts that can be safely verified.
7. Summarize confirmed requirements, assumptions, rejected directions, and remaining questions. In an explicit deep-questioning session, ask whether this captures the shared understanding before moving into implementation; ordinary reading does not require an extra approval round. Continue only within the user's requested scope, and do not turn interview completion into permission to modify code or publish a document.

Understanding remains useful on its own. Formal audits and self-check cases belong to `claire-test`; page execution belongs to explicitly requested `webapp-testing`.

## Upstream Maintenance

The clarification loop adapts `mattpocock/skills`'s `grill-me` and its shared `grilling` dependency. Pinned sources and local adaptations are recorded in [upstreams.json](../upstreams.json); attribution is in [THIRD_PARTY_NOTICES.md](../THIRD_PARTY_NOTICES.md). Preserve one-question-at-a-time routing, read-only defaults, and the explicit BDD boundary when syncing.
