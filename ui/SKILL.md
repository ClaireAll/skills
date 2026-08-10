---
name: ui
description: Use when implementing, polishing, auditing, documenting, or creating a UI or design system, and the task may need one or more specialized UI workflows.
---

# UI

Route a UI task to the smallest internal module set without asking the user to choose modules manually.

## Automatic Routing

| User intent | Modules to read before acting |
| --- | --- |
| UI goal is broad, unclear, or spans multiple surfaces | `modules/ui-skills-root/module.md`, then the matching modules below |
| Fast cleanup of spacing, hierarchy, typography, or small layout problems | `modules/baseline-ui/module.md` |
| Build or materially rework a frontend experience with a deliberate visual direction | `modules/design-taste-frontend/module.md` |
| Create or update a product `DESIGN.md` from source or a public website | `modules/create-design-md/module.md` |
| Create, remix, or apply a named design-language skill | `modules/hue/module.md` |
| Read-only UI audit, design-drift investigation, or implementation-plan handoff | `modules/improve-ui/module.md` |

When multiple rows match, load every listed module in the order that preserves its boundary. Examples: broad UI redesign uses the root router plus design-taste; repository design-system documentation plus a redesign uses create-design-md before design-taste; a named design-language request uses Hue alone unless another outcome is explicitly requested.

## Route Rules

1. Select modules from the user's actual outcome, not from generic words such as “clean up” or “improve.”
2. A clear task must load its matching module directly. Use the root router only for broad or ambiguous UI scope.
3. Load no more than three internal modules unless the user explicitly asks for a multi-surface program.
4. `modules/improve-ui/module.md` is read-only. Do not combine it with source edits in one pass; finish its audit and plan first, then start an implementation pass with the appropriate editing module.
5. For accessibility, metadata, motion performance, or frontend code review, additionally use the existing dedicated top-level skill when that concern is in scope.

The modules own their detailed workflows and resources. This router only selects and sequences them.
