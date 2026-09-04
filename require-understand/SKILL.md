---
name: require-understand
description: Use when understanding feature or interaction requirements from Feishu, Figma, local files, or text; comparing specified source code with an interaction document; turning unresolved stakeholder-owned gaps into a questionnaire; or producing a test plan, scenario mindmap, or Feishu test document.
---

# Understand Requirements

Route requirement work to the correct internal module without asking the user to choose one.

## Automatic Routing

| User intent | Modules to read before acting |
| --- | --- |
| Read, summarize, clarify, or reconcile a feature document, interaction spec, Feishu page, Figma file, local requirement file, or mixed input | `modules/read-feature-input/module.md` |
| Generate a test plan, test scenarios, Mermaid mindmap, completeness checklist, or Feishu test-plan document | `modules/read-feature-input/module.md`, then `modules/test-plan-generator/module.md` |
| Compare a Feishu, Figma, or local interaction document with specified source code; identify contradictions or missing documentation | `modules/read-feature-input/module.md`, then `modules/interaction-spec-sync/module.md` |
| Update a specified interaction document from that comparison | `modules/read-feature-input/module.md`, then `modules/interaction-spec-sync/module.md`; load `feishu-doc-writer` before writing to Feishu |
| Turn requirement gaps that only a specific stakeholder can answer into a questionnaire | `modules/read-feature-input/module.md`, then **REQUIRED SUB-SKILL:** use `to-questionnaire` |
| Both understand a requirement and produce a test-plan artifact | Read both modules in the same order |

When more than one row matches, load the union of its modules. A test-plan request always requires the input-reading module first, even when the user supplies only a short text description.

## Route Rules

1. Identify every input source before selecting modules. Do not let a single link hide related Figma, Feishu, local-file, or pasted-text inputs.
2. Load every module named by the selected route before interpreting the requirement or writing an output.
3. The input module owns source handling, evidence alignment, Figma discipline, and clarification of missing facts.
4. The test-plan module owns scenario design, review-before-Feishu-backfill, and the final test-plan artifact.
5. The interaction-spec-sync module owns code-to-spec comparison and in-place document annotations. It does not modify application code or replace the document-writing skill.
6. For code-to-spec comparison, require a source directory or file scope. Ask one focused clarification only when it is unavailable after inspecting all provided sources.
7. Default to a read-only audit. Update a Feishu document only when the user explicitly requests a write or sync operation.
8. Ask one focused clarification only when a required fact is unavailable after the selected modules have inspected all provided sources.
9. Use `to-questionnaire` only when the user requests a questionnaire or equivalent artifact and the unresolved facts belong to a named or identifiable stakeholder. Ordinary clarification stays in the current conversation.

Keep the responsibilities separate: understanding is reusable on its own; questionnaires and test plans are additional output paths, not automatic side effects of every requirement-reading request.
