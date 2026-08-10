### Phase 8: Generate Skill Files from Design Model
> Paths beginning with `references/` are relative to the Hue skill root unless a generated skill folder is explicitly named.

Read the `design-model.yaml` and generate all 4 files. Fill every placeholder. No empty sections, no TODOs. Use the templates from `references/` as the exact structure:

| File | Template | Purpose |
|------|----------|---------|
| `SKILL.md` | `references/skill-template.md` | Philosophy, craft rules, anti-patterns, workflow |
| `references/tokens.md` | `references/tokens-template.md` | Colors, fonts, spacing, motion, iconography |
| `references/components.md` | `references/components-template.md` | Buttons, cards, inputs, lists, navigation, overlays |
| `references/platform-mapping.md` | `references/platform-mapping-template.md` | CSS custom properties, SwiftUI extensions, Tailwind config |

**Every value in these files must come from the Design Model.** If a value isn't in the YAML, add it to the YAML first, then reference it. No hardcoding values that aren't in the model.

**Components must be based on the inventory from Phase 2.** Each component in the YAML has `source: observed` or `source: derived` — this traces back to the Tear-Down Sheets.

### Phase 9: Write Files
Default location depends on the platform:
- **Claude Code:** `~/.claude/skills/{skill-name}-design/`
- **Codex:** `~/.agents/skills/{skill-name}-design/`
- If the user specifies a different path, use that.

Create the directory structure:

```
{skill-name}-design/
  design-model.yaml              ← Single Source of Truth
  SKILL.md
  references/
    tokens.md
    components.md
    platform-mapping.md
```

### Phase 10: Generate Visual Preview
**Generate visual preview.** Create a `preview.html` in the skill folder — a standalone Bento Grid dashboard rendered in the generated design language. Read `references/preview-template.md` for the specification. **All CSS values in the preview must come from `design-model.yaml`** — re-read the YAML before writing CSS to ensure no drift.

Open the preview in a browser (macOS: `open preview.html`, or provide the absolute path). This is the magic moment — the user sees their design language come alive.

### Phase 11: Generate Component Library

After the Bento Grid preview, generate a second visual output: `component-library.html`. Where the Bento Grid shows the language *in use*, the Component Library shows it *dismantled* — every component on its own canvas with its exact token values spelled out in a spec table beside it.

Read `references/component-library-template.md` for the full specification. Key rules:

1. **Two-column layout.** Sticky TOC on the left (~240px), scrollable main area on the right (max-width ~960px). TOC active-state via a passive `scroll` listener on the main area that compares each component group's `offsetTop` against the scroll position (see the scroll-tracking script in the template).
2. **Required sections:** Defined in `references/component-library-template.md` — follow the category tabs and section list there. Skip a section only if the brand genuinely has no concept of it.
3. **Each section has:** heading + one-line description, a Canvas showing live components (variants + states side-by-side, not requiring hover), a Spec table listing the exact token values.
4. **State rendering.** When a component has multiple interactive states (default/hover/active/focus/disabled), render them **all at once** using static `.is-hover`, `.is-focused` etc. classes that reproduce the state's visual. Never rely on actual hover — the user needs to see all states simultaneously.
5. **Round stroke caps everywhere.** Progress rings, bars, dashed elements — `stroke-linecap: round` unless the brand explicitly mandates flat caps (rare).
6. **Same floating Light/Dark bar as the Bento Grid preview** — copy the pattern exactly for consistency across both views.
7. **All values from `design-model.yaml`.** Re-read before writing any CSS. No hardcoded hex values — everything goes through semantic tokens.

Open it in the browser after generating. The Bento Grid answers "what does this language feel like?"; the Component Library answers "what are the exact values?".

### Phase 12: Generate Landing Page

Generate a third visual output: `landing-page.html`. Where the Bento Grid shows density and the Component Library shows specs, the Landing Page shows the brand *telling a story* — editorial typography, narrative rhythm, alternating feature sections.

Read `references/landing-page-template.md` for the full specification. Key rules:

1. **Required sections in order:** Header, Hero, Feature 1, Feature 2, Feature 3, (optional) Pull quote, (optional) Pricing, Final CTA, Footer. Skip optional sections only if the brand genuinely doesn't fit (early-stage, enterprise-only, utility-focused).
2. **No lorem ipsum — ever.** Every piece of copy must be written specifically for the brand in its observed voice. Before writing copy, decide the brand voice in 2-3 adjectives (warm/poetic, clinical/precise, witty/direct, etc.) and commit. Specifics over generics: "press cmd+k and find a note from three years ago by remembering one word from it" beats "powerful search features".
3. **Hero dominance.** Display headline must feel 2-3× larger than any other type on the page. Use the display font at a size beyond the normal scale if needed (`clamp(40px, 7vw, 72px)` works well).
4. **Alternating features.** Text-left / visual-right, then swap. Prevents the eye from falling into a single column.
5. **Visual elements are suggestive, never literal.** Since you can't use the brand's real imagery, pick ONE approach: styled mini card stacks (UI-rich brands), type-as-image (editorial), icon+text combos (hybrid), or color compositions (content-rich). Never stock photos, never fake logos.
6. **Restraint on surface tints.** Body stays on `var(--bg)`. Use `--surface1` or `--surface2` for at most one or two sections as rhythm breaks — never more.
7. **Same floating Light/Dark bar** as the other two views.
8. **All values from `design-model.yaml`.** Re-read before writing CSS.

**Pre-ship verification — run before declaring the landing done.** These three checks catch the most common silent-failure bugs:

1. **Every CSS class-selector must hit at least one element.** If the stylesheet references `.hero h1` but the HTML only has `<section class="lp-hero">` + `<div class="hero-content">`, the rules don't match and the h1 renders with default browser styles. Grep your selector names against your HTML: every class used in CSS should exist in the markup. If you introduce a wrapper like `.hero-content`, update every matching selector too.
2. **Flex parents need explicit child widths.** A hero section using `display: flex; align-items: center` will shrink its inner `.container` down to intrinsic content width — so a 1320px max-width container silently becomes 721px. Always give inner containers inside flex heroes `width: 100%`, or use `display: block` on the hero and center with margin.
3. **Open in the browser and inspect the hero.** Check computed `font-family` and `font-size` on the h1 — if they say `Inter 32px` when you expected `Cormorant Garamond 96px`, your display-font CSS rule didn't match. Fix the selector, don't ship the bug. Also test both light and dark modes — editorial brands often break in one of the two.

Editorial brands often look dramatically different in dark mode — always test both.

### Phase 13: Generate App Screen

Generate the fourth and final visual: `app-screen.html`. Where the landing page shows *what the brand sells* and the component library shows *what the pieces look like*, the app screen shows *what the product actually feels like in use* — tokens applied to a representative screen inside the brand's product, rendered inside a device frame.

This is the step that validates "does the design system survive contact with real product UI?" A language that looks great on a marketing hero but falls apart inside a dense dashboard is a failed language. The app screen is the proof.

Read `references/app-screen-template.md` for the full specification. Key rules:

1. **Archetype first.** Pick one of six: `dashboard`, `editor`, `list-detail`, `feed`, `conversational`, `canvas`. Match to the brand's actual product category via `brand_domain`.
2. **Device frame.** `browser` / `phone` / `desktop` / `tablet`, matched to the brand's primary platform. Default to `browser` for SaaS/platform brands, `phone` for consumer apps, `desktop` for native pro tools.
3. **Content density is non-negotiable.** Sparse screens read as wireframes, not products. Dashboard needs 4–8 metric tiles + a chart + a table. List-detail needs 10+ items. Conversational needs 8+ messages. See the density rules in the template.
4. **Brand voice in the invented content.** No lorem ipsum, no generic placeholders. A fictional SLO tool's dashboard shows `checkout-api` and `auth-worker`, not `service-a` and `service-b`. The content IS the brand voice.
5. **Every token must show up at least once.** Use the required-tokens checklist from the template. If a token doesn't appear, the design system has a coverage gap.
6. **One "mid-use" touch.** A cursor hovering, a hover state, a selected list item — one visual signal that says "this is the product caught mid-use", not a static mockup.
7. **Same floating Light/Dark bar** and click-disabled anchors as the other three views.
8. **Add the new view to the sticky TOC** in the component library so all four views are reachable from each other.

**Current status:** Phase 13 is live with two canonical proofs, both using the `dashboard` archetype inside a `browser` frame.

- `examples/ridge/app-screen.html` — SLO overview for `checkout-api`. 8-service sidebar, 3 KPI tiles with sparklines, a 30-day error-budget burn-down chart, 8 log events, and a fake cursor hovering on the selected service. Dev-platform vocabulary (services, alerts, SLO, incidents).
- `examples/stint/app-screen.html` — stint 07 detail view for the `paper` workspace. Sidebar of 7 recent stints with status dots, 3 KPI tiles (completion / days left / at risk), a 14-day burn-down chart with actual vs dashed ideal line, 8-row activity feed, and a fake cursor hovering on the selected stint. Project-tracker vocabulary (stints, tasks, cycles, carryover).

Both render in light + dark mode, use every required token from the checklist, and serve as patterns to copy for the next brand that adopts Phase 13. A third proof should exercise a *different* archetype (not `dashboard`) to keep the template honest — Halcyon with a `conversational` (reasoning-graph chat) archetype is the best next target because it tests both a new archetype and the `sculptural-field` backdrop in a product context.

### Phase 14: Self-Validation
After generating all outputs, validate every HTML file against the Design Model. This covers `preview.html`, `component-library.html`, `landing-page.html`, and `app-screen.html`.

**Step 1 — run the validation script. This is mandatory, not a suggestion:**

```
node scripts/validate.mjs <path-to-generated-skill-folder>
```

(`scripts/validate.mjs` lives in THIS skill's folder, not in the generated one.) The script checks: YAML syntax, orphan CSS class-selectors, undefined `var(--token)` usages, leftover `{{placeholder}}` / TODO / FIXME / lorem ipsum, em-dashes in visible text, the generated SKILL.md frontmatter contract, WCAG contrast on the core text/background pairs, and AI-default display fonts. Fix every ERROR it reports, re-run, and repeat until the exit code is 0. Do not skip the script. Prose checklists don't hold; the gate does.

**Step 2 — screenshot self-review loop (after EVERY HTML artifact, not just at the end):**

On Claude Code, do this right after generating each HTML file in Phases 10–13:

1. Open the file via Chrome DevTools MCP — `mcp__chrome-devtools__navigate_page` (or `new_page`) with the `file://` URL, then `mcp__chrome-devtools__take_screenshot`.
2. Look at the screenshot yourself and answer four questions:
   - (a) Is the display font actually rendering, or did it fall back to a default?
   - (b) Does any area read as default-LLM aesthetics — violet-glow-on-dark, an Inter headline, empty card grids?
   - (c) Is content stuck at the top with dead whitespace below it?
   - (d) Do the rendered token colors match `design-model.yaml`?
3. Any finding → fix it, re-screenshot, re-answer. Repeat until all four pass. Check both light and dark mode.

On Codex (no browser tools): declare the visual check as an explicit user step — "open `landing-page.html` in a browser and confirm the display font renders and the accent matches the model" — and rely on `validate.mjs` all the more. It is the only automated gate you have there; never skip it.

**Step 3 — manual cross-checks the script cannot cover:**

1. **Accent fidelity** — the accent hex in the YAML matches the interactive elements across all previews.
2. **Spacing rhythm** — spacing values in the outputs trace back to the YAML scale, no invented one-off paddings.
3. **Component completeness** — compare each component in the preview against its Tear-Down Sheet or Derived Design from Phase 2.

If anything doesn't match — fix it before showing to the user.

### Phase 15: Offer Iteration
After writing, tell the user what was created and ask if they want adjustments. Common requests: "more contrast", "warmer tones", "different font", "more playful motion", "add a glow effect", "less padding."

**For iterations:** update `design-model.yaml` first, then regenerate only the affected files from the model. This keeps everything in sync.

### Phase 16: Installation Reminder
After generating, tell the user:
> Restart your AI coding assistant (Claude Code, Codex, etc.) or start a new conversation for the skill to be detected. Activate it by saying "{skill-name} design" or "/{skill-name}-design".

---

## 3. QUALITY STANDARDS

These are non-negotiable. Every generated skill must meet all of them.

### Preview
- The `preview.html` must look like a real app dashboard, not a component library. Use real-looking content, proper hierarchy, proper density.

### Philosophy
- 2-4 sentences that capture the *attitude*, not just the aesthetics. "Subtract, don't add" is a philosophy. "Clean and modern" is not.
- Reference the design lineage — what real-world objects, brands, movements, or eras this draws from.
- Include the primary tension that gives the language its character.

### Design Principles
- 5-7 principles. Each: **Bold Title.** + one sentence.
- Every principle must be falsifiable — you can point at a screen and say "this violates principle 3."
- No platitudes. "User-friendly" is not a principle. "Type does the heavy lifting — hierarchy comes from scale and weight, never from color or icons" is.

### Craft Rules
- 5-6 rules in Section 2 of SKILL.md. Each is a *how-to-compose* instruction.
- Include: visual hierarchy layers, typography discipline (font budget per screen), spacing semantics, color strategy, composition approach.
- Use tables for layer/hierarchy definitions — they're scannable and unambiguous.
- Include the squint test or equivalent quick-validation method.

### Anti-Patterns
- 8-12 specific bans. Each starts with "No" and names the exact thing.
- Be precise: "No border-radius > 16px on cards" not "avoid large corners."
- Include both visual anti-patterns (gradients, shadows) and behavioral ones (toast popups, skeleton screens).
- Anti-patterns are what prevent the skill from producing generic output. They're the immune system.

### Colors
- Coherent palette. Every color must have a *role*, not just a hex code.
- Mentally verify contrast: text on background must exceed 4.5:1 for body, 3:1 for large text.
- Both dark and light mode values. Derive secondary mode from primary — don't just invert. Warm light mode needs warm dark mode.
- Include semantic colors: accent, success, warning, error.
- Token names follow this schema:

| Token | Role |
|-------|------|
| `--background` | Page/canvas background |
| `--bg` | Alias for `--background` (short form used in hero/landing templates) |
| `--surface1` | Primary elevated surface (cards) |
| `--surface2` | Secondary surface (nested, grouped) |
| `--surface3` | Tertiary surface (inputs, wells) |
| `--border` | Subtle/decorative borders |
| `--border-visible` | Intentional borders |
| `--text1` | Primary text (headings, body) |
| `--text2` | Secondary text (descriptions, labels) |
| `--text3` | Tertiary text (placeholders, timestamps) |
| `--text4` | Disabled text |
| `--accent` | Primary interactive color |
| `--accent-subtle` | Tinted backgrounds for accent |
| `--success` | Positive states |
| `--warning` | Caution states |
| `--error` | Destructive/error states |
| `--success-bg` | Tinted background behind success text/badges |
| `--warning-bg` | Tinted background behind warning text/badges |
| `--error-bg` | Tinted background behind error text/badges |

**Status tint derivation rule:** each `--*-bg` comes from the same status ramp as its foreground — light mode uses the lightest ramp step (`{hue.50}`), dark mode the darkest (`{hue.900}`); the foreground stays `{hue.500}` in both. This matches how `tokens-template.md` (status ramp table) and `components-template.md` (tags, alerts) consume them.

**Platform mapping must emit all tokens above.** `--bg` is an alias for `--background` — emit both in the `:root` block. `--border-visible` must be emitted alongside `--border`. `--accent-subtle` must be emitted (not `--accent-bg` — that's a deprecated name). `--success-bg` / `--warning-bg` / `--error-bg` must be emitted in both modes. See `references/platform-mapping-template.md`.

### Fonts
- Display, body, and mono roles. Always three.
- **Google Fonts only** for web skills. Name the exact font and weights needed.
- **System fonts** for SwiftUI skills (SF Pro, SF Rounded, SF Mono, New York).
- Include fallback stacks. Always.
- State *why* the font fits the aesthetic. "Geometric sans with humanist details" tells Claude how to judge edge cases.
- **`mono_for_code` + `mono_for_metrics`:** Two independent flags decide where the mono font applies. `mono_for_code` covers code blocks, file paths, shell commands, inline technical tokens. `mono_for_metrics` covers pricing, counts, timestamps, percentages, ID strings. Many brands use mono for code but NOT for metrics (e.g. Cursor: mono inside IDE screenshots, but `$20` pricing stays in the sans). Decide each flag by checking the brand's actual site.

  | Brand type | Example | `mono_for_code` | `mono_for_metrics` |
  |------------|---------|-----------------|--------------------|
  | Dev-tool / terminal | Linear, Nothing | `true` | `true` |
  | Dev-tool with editorial marketing | Cursor, Vercel, Raycast | `true` | `false` |
  | Consumer / editorial | Apple, mymind, Notion | `false` | `false` |

  **Backwards compat:** older skills may have `mono_for_data: true/false`. Treat `true` as both new flags true, `false` as both false.
- **`locked_weight`** (optional, top-level): Set only when the brand genuinely uses a single font weight across all text (h1 through body all at the same weight). Most brands do not — leave unset. If set, ALL type scale rows use this weight; see Type Scale section below for the table treatment.

### Type Scale
- 7 sizes minimum: display, heading, subheading, body, body-sm, caption, label. These names are canonical — identical in `references/tokens-template.md` and `references/platform-mapping-template.md`. Never invent alternates like `--h1`/`--h2`.
- Every size gets: px value, line-height ratio, letter-spacing, weight, and use case.
- Follow this structure:

| Token | Size | Line Height | Letter Spacing | Weight | Use |
|-------|------|-------------|----------------|--------|-----|
| `--display` | Npx | ratio | em | weight | use case |
| `--heading` | Npx | ratio | em | weight | use case |
| `--subheading` | Npx | ratio | em | weight | use case |
| `--body` | Npx | ratio | em | weight | use case |
| `--body-sm` | Npx | ratio | em | weight | use case |
| `--caption` | Npx | ratio | em | weight | use case |
| `--label` | Npx | ratio | em | weight | use case |

- **Locked-weight variant:** If `locked_weight` is set in the model, the weight column in the type scale table becomes a single row at the top (e.g. "All sizes: weight 400") instead of repeating per row. Drop the `Weight` column from the table or set every cell to `—`. Use this only for brands that genuinely run a single weight across all text (Cursor is one example).

### Spacing
- 8px base grid. Always.
- Scale: `2xs` (2px), `xs` (4px), `sm` (8px), `md` (16px), `lg` (24px), `xl` (32px), `2xl` (48px), `3xl` (64px), `4xl` (96px).
- Every value gets a semantic use case.

### Radii
- Define separately for: cards, buttons, inputs, tags/pills.
- State the corner philosophy — sharp (0-4px), soft (8-16px), round (20-24px), pill (999px).
- If the platform is iOS, note `RoundedRectangle(cornerRadius:, style: .continuous)`.

### Elevation
- Pick one primary elevation strategy:

| Strategy | When | How |
|----------|------|-----|
| **Flat** | Industrial, minimal | No shadows. Borders or background change only. |
| **Subtle** | Warm, friendly | Small y-offset (1-3px), diffused blur, low opacity. |
| **Glow** | Dark-mode-forward, premium | Colored shadow matching accent, no y-offset. |
| **Material** | Glass, depth-heavy | Blur + transparency + saturation. |

### Motion
- Pick one motion personality:

| Personality | Easing | Duration | Behavior |
|-------------|--------|----------|----------|
| **Mechanical** | `ease-out` or linear | 120-200ms | Precise, no overshoot. Click, not swoosh. |
| **Smooth** | `ease-in-out` | 200-350ms | Calm transitions, no bounce. |
| **Playful** | Spring (damping 0.7-0.8) | 300-500ms | Overshoot + settle. Things feel alive. |
| **None** | Instant | 0-100ms | Content appears, no choreography. |

### Platform Mapping
- Generate REAL, valid, copy-paste-ready code. Not pseudocode.
- CSS: `:root` block with all custom properties. Include dark mode via `[data-theme="dark"]` or `@media (prefers-color-scheme: dark)`.
- SwiftUI: `Color` extension with static properties, `Font` extension with static methods, relevant `ViewModifier`s.
- Tailwind: `extend` block for `tailwind.config.js` mapping all tokens.

### Components
- Every component gets: when to use, variants, exact token mapping per variant.
- Minimum components: cards, buttons (4 variants), inputs, lists, navigation, tags/chips, overlays (modal + bottom sheet), state patterns (empty, loading, error, disabled).
- Use tables for variant specifications — scannable, unambiguous.

---

## 4. FRONTMATTER RULES

Every generated SKILL.md must start with this frontmatter structure:

```yaml
---
name: {skill-name}-design
description: "Use when the user explicitly asks to use or apply the {Skill Name} design system, '{Skill Name} style', '{Skill Name} design', or '/{skill-name}-design'. NEVER trigger automatically for generic UI or design tasks."
allowed-tools: [Read, Write, Edit, Glob, Grep]
---
```

Two hard rules, identical in `references/skill-template.md` and enforced by `scripts/validate.mjs`:

1. **`name` must equal the skill's folder name**, format `{brand}-design` (e.g. folder `meadow-design/` → `name: meadow-design`). A mismatch breaks skill discovery.
2. **`description` must contain the explicit trigger phrases AND the literal string "NEVER trigger automatically".** Never allow automatic triggering for generic design tasks.

**Cross-platform note:** `allowed-tools` is a Claude Code field. Codex ignores it but tolerates its presence. Both platforms use `name` and `description` for discovery; do not add a root-level `version` field.

---

## 5. TONE & VOICE

Write generated skills like a senior designer briefing a junior one. Authoritative, specific, opinionated.

**Good:** "Shadows are banned. Depth comes from border + background change. If something needs to float, use a 1px border at 8% opacity, not a shadow."

**Bad:** "Consider using subtle borders instead of heavy shadows for a cleaner look."

**Good:** "Max 2 chromatic colors per screen. The neutral canvas makes each color arrival feel special."

**Bad:** "Try to limit the number of colors for a more cohesive design."

The difference: good instructions are falsifiable, specific, and leave no room for interpretation. Bad instructions are suggestions that the model will interpret inconsistently.

---

## 6. ITERATION

After generating, the user may request adjustments. Common patterns:

| Request | What to change | What NOT to change |
|---------|---------------|-------------------|
| "More contrast" | Text/background delta, accent saturation | Font choices, spacing, components |
| "Warmer" / "Cooler" | Gray palette undertones, accent hue | Structure, typography, motion |
| "Different font" | Font stack + type scale adjustments | Colors, spacing, components |
| "More playful" | Motion personality, corner radii, elevation | Color palette, anti-patterns |
| "More minimal" | Reduce components, increase spacing, flatten elevation | Core philosophy |
| "Add glow/glass" | Elevation strategy, surface treatment | Typography, spacing |

Apply changes to the specific files and sections affected. Never regenerate from scratch unless the user asks for a completely different direction.

---

## 7. REFERENCE TEMPLATES

Use these as the exact structure for generated files. Fill every placeholder, delete every comment block.

- `references/skill-template.md` — SKILL.md structure (philosophy, craft rules, anti-patterns, workflow)
- `references/tokens-template.md` — Token definitions (fonts, type scale, colors, spacing, radii, elevation, motion)
- `references/components-template.md` — Component specifications (cards, buttons, inputs, lists, nav, overlays, states)
- `references/platform-mapping-template.md` — Platform code (CSS custom properties, SwiftUI extensions, Tailwind config)
