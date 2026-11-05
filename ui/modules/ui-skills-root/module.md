---
name: ui-skills-root
description: Internal selector for the public ui skill. Use it only when a UI request is broad or unclear.
---

# UI Scope Selector

Use this internal module only after `$ui` identifies a broad or unclear UI task. It selects local modules; never call an external registry or CLI.

## Local Selection

| Outcome | Internal module |
| --- | --- |
| Quick spacing, hierarchy, typography, or layout cleanup | `../baseline-ui/module.md` |
| Deliberate visual direction for an implementation or redesign | `../design-taste-frontend/module.md` |
| New page design or explicit visual redesign with an open design direction | `../design-taste-frontend/module.md`, then `../hallmark/module.md` |
| Evidence-based product `DESIGN.md` | `../create-design-md/module.md` |
| Named design language, remix, or brand-derived visual system | `../hue/module.md` |
| Hallmark visual directions or a Hallmark theme reference | `../hallmark/module.md` (advice-only unless implementation is requested) |
| Read-only UI audit and implementation handoff | `../improve-ui/module.md` |
| Read-only template-like / AI-generated appearance review or Hallmark audit | `../improve-ui/module.md`, then the review section of `../hallmark/module.md` |

## Selection Rules

1. Identify the requested outcome, then load its matching module. Do not choose by vague words such as “better” or “polish.”
2. Ask one short clarification only when the outcome cannot be inferred from the provided context.
3. Prefer one module. Use two for clearly combined outcomes and at most three for a broad redesign or multi-surface review.
4. Keep `improve-ui` audit-only. Finish its audit and plan before starting an implementation pass with an editing module.
5. Preserve the existing stack and design evidence; this selector does not add external skills, dependencies, or tools.
6. Within the selected outcome, narrow by topic, then the actual stack, then specificity. Prefer a relevant existing specialized skill over a broad module; do not fetch alternatives from a registry.
7. Hallmark supplements open page design automatically, not narrow fixes. When Figma or the current product system determines the design, preserve it instead of choosing a Hallmark theme or new page structure. A Hallmark audit stays read-only.
