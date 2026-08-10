---
name: design-taste-frontend
description: Use when designing or materially reworking a frontend experience that needs a deliberate visual direction, strong hierarchy, and non-generic execution. Do not use for a narrow UI fix, code-only review, or read-only UX audit.
---

# Intentional Frontend Design

Use this as a design-direction overlay for an implementation task. For a narrow UI repair, use `../baseline-ui/module.md`; for an evidence-only critique, use `../improve-ui/module.md`.

## Calibrate Before Building

- Inspect the existing product, design evidence, and active stack before choosing a visual direction.
- Preserve the product's existing language for user-facing copy. Do not translate working Chinese content into English or replace specific domain language with generic filler.
- Set three dials deliberately: visual variance, visual density, and motion. Derive them from product type, evidence, and the user's request; there is no universal default.
- Name the dominant hierarchy, color strategy, image/media strategy, and one memorable composition choice before writing UI.
- Respect a utilitarian product surface. A dashboard, editor, CRM, or settings workflow should optimize scanning and repeated action rather than behave like a marketing page.

## Work With the Codebase

- Reuse the current framework, component library, styling system, and installed icon set. Check `package.json` before importing a dependency.
- In React or Next.js, isolate client-only interaction in the smallest leaf component that needs it. Keep static layout and data work outside that boundary.
- Use local state for local interaction. Add global state only when it removes real cross-tree coordination.
- Match the installed Tailwind version and project conventions. Do not introduce v4 syntax into a v3 project.
- Use a stable layout system: constrained page widths, CSS Grid for multi-column composition, and explicit responsive collapse. Full-height scenes need `min-height: 100dvh`, not brittle viewport-height assumptions.

## Compose With Evidence

- Give every color a role: canvas, surface, text, border, action, and status. Keep contrast adequate and avoid arbitrary palette drift.
- Keep existing brand typography when it is established. When a new type choice is justified, pick it for a concrete reason; do not default to the same fashionable font pair across projects.
- Establish hierarchy with scale, weight, spacing, and placement before using color or decoration.
- Use cards only when a frame clarifies ownership, elevation, or a repeated item. Do not turn every section into a rounded container.
- Choose a composition that fits the content: asymmetric editorial rhythm for narrative work, dense aligned bands for operational work, and a genuine image or product state when a hero is warranted.
- Use real domain-specific copy, states, and data. Avoid placeholder people, implausibly perfect metrics, generic startup names, and abstract marketing verbs.

## Complete the Interaction

- Build loading, empty, error, disabled, focus, hover, active, and selected states where the surface needs them.
- Forms have visible labels, helpful constraints, and errors adjacent to the field that needs attention.
- Use icons from the installed library instead of emoji or hand-drawn substitutes.
- Add motion only when it explains state, hierarchy, or direct manipulation. Choose one animation system per interaction boundary; do not add perpetual movement merely to make a screen feel busy.

## Protect Performance and Accessibility

- Animate `transform` and `opacity`; avoid animating layout properties and expensive effects inside scrolling containers.
- Keep high-cost visual effects, canvas work, and scroll choreography isolated, cancellable, and optional. Respect reduced-motion preferences.
- Maintain keyboard access, visible focus, readable contrast, and touch-safe targets as part of the composition, not as a later cleanup.
- Do not create arbitrary z-index layers. Use an intentional layer scale for sticky UI, popovers, dialogs, and overlays.

## Avoid Default-Looking Output

- Do not default to centered headline plus decorative gradient, three identical feature cards, violet glow on a dark canvas, generic bento tiles, or a stock-like image that hides the product.
- Do not make a visually loud choice without a source-based reason. A bento grid, glass surface, serif display, canvas background, magnetic button, or 3D scene is a tool, not a default.
- Do not combine several motion libraries or ship an effect whose cleanup, mobile behavior, or accessibility state is unclear.

## Preflight

- The visual direction matches the evidence and product type.
- Copy, icons, responsive behavior, and interaction states are coherent.
- No layout relies on accidental overflow, unbounded text, or viewport quirks.
- The implementation remains small enough to maintain and uses no dependency that the project does not already support.
