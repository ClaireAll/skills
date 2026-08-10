---
name: require-understand
description: Use when understanding feature or interaction requirements from Feishu, Figma, local files, or text, especially when turning them into a test plan, scenario mindmap, or Feishu test document.
---

# Understand Requirements

Route requirement work to the correct internal module without asking the user to choose one.

## Automatic Routing

| User intent | Modules to read before acting |
| --- | --- |
| Read, summarize, clarify, or reconcile a feature document, interaction spec, Feishu page, Figma file, local requirement file, or mixed input | `modules/read-feature-input/module.md` |
| Generate a test plan, test scenarios, Mermaid mindmap, completeness checklist, or Feishu test-plan document | `modules/read-feature-input/module.md`, then `modules/test-plan-generator/module.md` |
| Both understand a requirement and produce a test-plan artifact | Read both modules in the same order |

When more than one row matches, load the union of its modules. A test-plan request always requires the input-reading module first, even when the user supplies only a short text description.

## Route Rules

1. Identify every input source before selecting modules. Do not let a single link hide related Figma, Feishu, local-file, or pasted-text inputs.
2. Load every module named by the selected route before interpreting the requirement or writing an output.
3. The input module owns source handling, evidence alignment, Figma discipline, and clarification of missing facts.
4. The test-plan module owns scenario design, review-before-Feishu-backfill, and the final test-plan artifact.
5. Ask one focused clarification only when a required fact is unavailable after the selected module has inspected all provided sources.

Keep the two responsibilities separate: understanding is reusable on its own; test-plan generation is an additional output path, not an automatic side effect of every requirement-reading request.
