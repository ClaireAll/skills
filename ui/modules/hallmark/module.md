---
name: hallmark
description: Internal ui supplement for new page design, explicit visual redesign, and requested reviews of template-like appearance. Preserve established design evidence and skip narrow fixes.
---

# Material-led Page Design

Selectively adapted from Nutlope/Hallmark v2. Use with `design-taste-frontend` for implementation; this module adds content structure, theme selection and a review lens, not a second implementation workflow. The public `ui` entrypoint and its local overrides govern every reference here.

## Establish the design boundary

- For a broad new intention with no clear goal or deliverable, ask the most consequential question and wait before inspecting the project. Otherwise inspect the relevant project and supplied evidence before asking for information already available.
- An applicable Figma design, `DESIGN.md`, brand specification or established component system takes precedence. When it settles the visual design, skip theme exploration and structural changes; implement that design using the normal `ui` route.
- Keep the requested scope: a new app screen remains an app screen; a small component edit does not become a page redesign. An audit goes directly to **Review**, without running the design steps below.
- A request for visual directions or theme advice ends with the recommendation; it does not authorize implementation, files or a separate design-language skill. Hallmark theme references use this module rather than the Hue creation workflow.
- Before an authorized redesign, identify the affected files and existing content, routes, controls and handlers that must remain. Visual redesign does not authorize changing APIs, permissions, business behavior or removing functionality.

## Build from the visitor's task

Establish the audience, primary task and available material from the request and project. Separate supplied facts and usable assets from missing information. Never invent customers, prices, dates, testimonials, logos or product screenshots. Ask only for missing information that blocks the task; an unanswered question is not permission to choose a user-facing default.

Choose content and action placement for the task, not a recurring sequence of hero, metrics, three cards and a newsletter. These are examples to adapt, not required sections or permission to add functionality:

| Visitor task | Useful content and action placement |
| --- | --- |
| Book a class or service | Show the real offer and available schedule; put booking beside the relevant choice; close with practical details when supplied. |
| Visit a place | Prioritize what is there, the supplied opening hours, location and directions. Do not invent hours or an address. |
| Buy or attend | Place the product or event, verified price/date, options and purchase/ticket action together; include only supplied terms and proof. |
| Try software | Show the actual product or supplied screenshots and a supported trial/download action; use concrete tasks rather than generic feature tiles. |
| Subscribe or listen | Let a real sample, issue or episode explain the offer; subscription/playback belongs near it, if that action is in scope. |
| Hire a person or studio | Let actual work and capabilities lead to the supplied contact route; no fabricated client wall or case studies. |
| Work in an application | Preserve navigation, data density, task controls and states. Do not add a marketing hero, promotional sections or a closing CTA. |

Use the strongest real material as the visual focus: a workshop photograph, a product state, an actual offer, or informative typography. Section count and text length follow content and language; do not apply English word budgets or force a thin brief into a long page. If an image is missing, use a clearly identified placeholder only when the requested prototype needs one; do not present it as the real product or quietly source/download replacements.

## Choose a direction when the design is open

Read [references/directions.md](references/directions.md) only when visual exploration or a named Hallmark theme is relevant. The local selection offers six adapted directions, not the full upstream theme library or exact reproductions.

Choose based on the material, task and requested tone. Reuse existing tokens and available fonts, including suitable Chinese glyphs; theme names do not authorize fonts, packages or assets to be installed. A theme describes color roles, type hierarchy and surfaces, not the order or number of sections.

If the user delegated visual choices, choose the fitting direction and briefly explain why. Otherwise ask when a material design decision has no basis; do not treat examples or your recommendation as user approval. If the user asks for a bespoke direction, derive it from their actual subject instead of forcing a catalog choice. No random deal, rotation log or automatic theme switching.

Before implementing, briefly state the primary task, selected direction and real material carrying the page. Fold this into the normal design-taste update rather than producing another approval ceremony or mandatory document. For example: a supplied pottery schedule and classroom photos can support a course timetable with booking beside each class; the theme changes its visual treatment, not the booking contract.

## Review

For a newly built page or an authorized redesign, review only the work in scope. For a read-only audit, use `improve-ui`'s contract, runtime and correction evidence gates and its report format; do not edit product files or turn aesthetic preferences into verified defects.

Distinguish three kinds of observations:

1. **Contract or correctness issue:** unsupported factual claims, lost content or actions in a redesign, divergence from the binding design, or broken focus/reduced-motion behavior introduced by this work. Establish evidence and correct only within the authorized implementation scope. Findings outside it are reports, not repair authorization.
2. **Possible template reflex:** repetitive heading labels, decorative status dots, one colored word in every headline, identical card rows, generic slogans, or an unrelated newsletter ending. Ask what useful job it does here. These are prompts for judgment, not universal bans; retain a pattern supported by the content or design system. In an audit, discard unsupported candidates rather than manufacture a contract from Hallmark's preferences.
3. **Visual finish:** hierarchy, rhythm, image crop, density and first-screen action visibility. Judge these from supplied visual evidence or an explicitly authorized browser test; source inspection alone cannot certify their rendered appearance.

Try the specificity check: if replacing the business name leaves the same page equally convincing, look for actual material or tasks the design has failed to express. This is a design question, not a numerical score or an automatic requirement to rebuild.

Use the repository's existing static checks when relevant. Browser execution, screenshots and viewport checks require an explicit `webapp-testing` request; a screenshot supplied by the user may be inspected without starting the page. Report unverified rendering and interactions plainly. Do not claim Hallmark lint or visual gates passed: no upstream linter is bundled here.

## Integration limits

This adaptation supplies design guidance and a small reference selection. It does not install Hallmark, run `npx`, add Puppeteer, hooks or API integrations, invoke reviewers automatically, or write `.hallmark` logs, CSS stamps, generated token files or `DESIGN.md`. Use existing project owners for styles. Do not copy upstream global overflow rules, fixed word/section limits, font-loading snippets, animations or negative tracking into the product.

Pinned sources and attribution are maintained in [upstreams.json](../../../upstreams.json) and [THIRD_PARTY_NOTICES.md](../../../THIRD_PARTY_NOTICES.md).
