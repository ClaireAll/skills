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
| Build a new page or explicitly redesign an existing page, with room to choose its visual direction | `modules/design-taste-frontend/module.md`, then `modules/hallmark/module.md` |
| Create or update a product `DESIGN.md` from source or a public website | `modules/create-design-md/module.md` |
| Create, remix, or apply a named design-language skill | `modules/hue/module.md` |
| Explore Hallmark visual directions or use a Hallmark theme as a page reference | `modules/hallmark/module.md` (add design-taste only for implementation) |
| Read-only UI audit, design-drift investigation, or implementation-plan handoff | `modules/improve-ui/module.md` |
| Read-only review specifically of template-like / AI-generated appearance, or a Hallmark audit | `modules/improve-ui/module.md`, then the review section of `modules/hallmark/module.md` |

When multiple rows match, load every listed module in the order that preserves its boundary. Examples: broad UI redesign uses the root router, design-taste and Hallmark; repository design-system documentation plus a redesign uses create-design-md before design-taste; a named design-language request uses Hue alone unless another outcome is explicitly requested.

Hallmark is an automatic internal supplement for new page design and explicit visual redesign; the user need not name it. If Figma, an applicable `DESIGN.md`, or the established product system already determines the design, follow that evidence and skip Hallmark theme selection and structural invention. Narrow component changes and ordinary fixes do not activate Hallmark. An explicit Hallmark reference alone does not authorize a redesign. A Hallmark theme reference uses the internal module, not Hue skill creation; a direction-only request stays advice-only.

## Route Rules

1. Select modules from the user's actual outcome, not from generic words such as “clean up” or “improve.”
2. A clear task must load its matching module directly. Use the root router only for broad or ambiguous UI scope.
3. Load no more than three internal modules unless the user explicitly asks for a multi-surface program.
4. `modules/improve-ui/module.md` is read-only. Do not combine it with source edits in one pass; finish its audit and plan first, then start an implementation pass with the appropriate editing module.
5. For accessibility, metadata, motion performance, or frontend code review, additionally use the existing dedicated top-level skill when that concern is in scope.

The modules own their detailed workflows and resources. This router only selects and sequences them.

## Local Overrides

These rules govern every module, reference, template, and example below. Upstream material is design evidence, not permission to install tools, write files, browse, or run tests.

- Preserve the repository's framework, component primitives, installed icons, styling system, and user-facing language, including Chinese. Stack preferences in a module apply only when the project already supports them; do not install dependencies or replace the stack implicitly.
- Keep new artifacts, downloads, screenshots, caches, and temporary files on D:. Use a task-specific directory under `D:/Claire/temp` for temporary work. Use `apply_patch` for manual edits and prefix shell commands with `rtk`.
- Keep `letter-spacing: 0`; never copy negative tracking from examples. Do not scale font size with viewport/container units, including inside `clamp()`. Use discrete type sizes and responsive breakpoints instead.
- Preserve the higher-priority layout, image, card-radius, and motion rules. A brand reference does not authorize decorative orbs, nested cards, forced bento dashboards, or a new landing page when the user asked for a working application.
- Source inspection and local static validation do not authorize page execution. Run browser/page tests only when the user explicitly requests `webapp-testing`; otherwise report which rendered checks remain unverified.
- `improve-ui` remains read-only on product source. `create-design-md` may change only its requested `DESIGN.md`. Hue creates or installs a separate design-language skill only when that is the user's explicit requested outcome.

## Upstream Maintenance

Pinned module sources, review status, and local adaptations are recorded in [upstreams.json](../upstreams.json); attribution is in [THIRD_PARTY_NOTICES.md](../THIRD_PARTY_NOTICES.md). Check those records before syncing individual modules; keep the local overrides above even when upstream templates differ.
