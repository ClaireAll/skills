## 2. WORKFLOW

> Paths beginning with `references/` are relative to the Hue skill root unless a generated skill folder is explicitly named.

Follow this sequence. No shortcuts.

### Phase 1: Deep Analysis
Gather information from the input. Don't just extract tokens — understand the *system*:
- Colors (background, surface, text, accent, semantic)
- Fonts (display, body, mono) + why they fit
- Spacing feel + density level
- Corner radii + philosophy
- Surface depth + elevation approach
- Motion character
- Overall attitude + primary tension
- What's ABSENT that you'd expect? (Absence = design decision)

**Classify the brand type.** This changes your strategy for the entire generation:

| Type | Signal | Differentiation lives in... | Examples |
|------|--------|---------------------------|----------|
| **UI-rich** | Many visible components, distinctive shapes, strong color system, unique interactions | Components, colors, craft effects | Linear, Notion, Spotify, mymind, Nothing |
| **Content-rich** | Full-bleed photography, minimal UI chrome, few distinctive components, identity lives in imagery | Typography, spacing, surface temperature, restraint | Tesla, Nike, Porsche, luxury brands |

For **UI-rich brands**: lean into component distinctiveness — pill shapes, glows, colored indicators, dense grids, signature interactions. These translate well to Bento Grid widgets.

For **content-rich brands**: the UI is intentionally invisible — the differentiating levers shift from components to subtler choices. But these are LEVERS, not rules — the direction still comes from the brand:
- **Typography** becomes the primary visual tool. Study the brand's exact type choices — size, weight, spacing. Reproduce faithfully, don't impose a direction.
- **Spacing** carries more identity weight when there are fewer visual elements. Match the brand's actual density.
- **Surface temperature** matters more when there's less color. Warm blacks ≠ cool blacks ≠ pure blacks.
- **Accent restraint** — reproduce how sparingly the brand uses color. Don't add color that isn't there.
- **Domain-specific widget content** — "396 mi range" feels authentic, "12 tasks" feels generic. Specificity compensates for visual simplicity.

Tell the user which type you identified: "This is a content-rich brand — the design language is more about typography and restraint than about distinctive UI components. The preview will be subtler."

Document your findings. These will feed into the Design Model in Phase 7.

### Phase 2: Component Inventory

**This is the critical step.** Before generating anything, inventory which UI components the brand actually has on their site/product:

For each standard component type, check: does the brand have it? What does it look like?

| Component | Check for | Where to look |
|-----------|-----------|---------------|
| Buttons | Primary, secondary, ghost variants | CTAs, forms, nav |
| Cards | Content cards, feature cards | Homepage, features page |
| Inputs | Text fields, search bars | Login, search, forms |
| Toggles/Switches | Settings, filters | Product UI, settings |
| Tags/Badges | Status indicators, categories | Product UI, blog |
| Lists | Data lists, nav lists | Product UI, pricing |
| Progress | Bars, rings, gauges | Product UI, onboarding |
| Navigation | Header, sidebar, tabs | All pages |
| Overlays | Modals, dropdowns, tooltips | Product interactions |

For each component the brand HAS, create a **Tear-Down Sheet** — extract CSS properties as precisely as possible (exact from source code when available via WebFetch, estimated from visual appearance otherwise):

> **Tear-Down: Button (Primary)**
> - **Source:** `brand.com` CTA button
> - **Observed:** `background: #5E5CE6`, `color: #FFF`, `font-size: 15px`, `font-weight: 500`, `padding: 10px 16px`, `border-radius: 8px`, `box-shadow: none`
> - **Hover:** `background: #4E4CD5` (slightly darker)
> - **Conclusion:** Generated primary button will use these exact values as baseline.

This creates a traceable link between what the brand actually does and what the skill generates.

For components the brand DOESN'T have, create a **Derived Design** with explicit justification:

> **Derived: Toggle Switch**
> - **Source:** Not found on `brand.com`
> - **Derived Design:** Flat, rectangular switch with sharp corners, no shadow
> - **Justified by:** Principle 1 ("Flat, not deep") + Principle 3 ("Geometric forms only"). Consistent with the brand's existing input fields which use 0px radius and border-only depth.

Name the specific principles from the analysis that justify the derivation. No guessing — reason from the system.

### Phase 3: Icon Kit Selection

**We cannot copy a brand's proprietary icons into generated skills.** Instead, we maintain a pool of freely-licensed icon kits in `references/icon-kits.md` and pick the closest fit as a best-match fallback.

Follow this sequence exactly — no shortcuts, no defaulting to Phosphor because it's familiar.

1. **Observe the brand's actual icons.** Pull 4–6 distinct glyphs from the brand's site (nav, feature sections, product UI). For each, describe in prose what you see. Example: *"nav icons: ~1.75px stroke, rounded terminals, slightly irregular curves, outline-only, humanist."*

2. **Score the brand on the five matching criteria** from `icon-kits.md`:
   - `stroke_weight`: thin / regular / medium / bold / filled
   - `corner_treatment`: sharp / soft / fully-round
   - `fill_style`: outline / solid / duotone / mixed
   - `form_language`: geometric / humanist / hand-drawn
   - `visual_density`: minimal / balanced / detailed

3. **Read `references/icon-kits.md`** and compare the brand's scores against each kit's match profile. Use the Decision Matrix as a quick-pick, but justify your pick with the criteria — don't just pick a row.

4. **Pick ONE kit** (never mix). If multiple kits match, pick the one with closer stroke weight and form language over other factors — those are the most visually load-bearing.

5. **Write `match_reasoning`** — 2–3 sentences naming what matches, what doesn't, and why this kit beats the second-best option. If the gap is large (e.g. brand is hand-drawn but no kit is truly hand-drawn), say so explicitly.

6. **Never claim the brand uses the kit.** The YAML fields are `observed_style` (what the brand actually does, as prose) and `fallback_kit` (what we rendered with). The `disclaimer` field makes this explicit for anyone reading the skill later.

This step gets its own YAML block — see Phase 7 for the schema.

### Phase 4: Hero Stage Analysis (MANDATORY)

**This step is mandatory.** Every brand gets a `hero_stage` block, even if it collapses to `subject: none` + `medium: absent`. The slot is never skipped — it is a major identity signal.

A **hero stage** is the composed visual behind the landing hero: a *background field*, optionally a *hero subject* sitting in front of it, and a defined *relation* between them (how light bleeds, how shadows fall). Thinking only in "backgrounds" misses half the brands. Raycast isn't a gradient — it's a glowing orb *on* a gradient. Linear is a device mockup on a mesh. mymind *is* just the painterly field (no subject).

Read `references/hero-stage.md` for the full dial reference and preset library. Follow this sequence:

1. **Observe the brand's hero stage as a whole.** Look at hero sections and feature areas. Describe in prose: background field + hero subject (if any) + how they relate. Examples:
   - *"A glowing light-ball centered on a soft radial gradient in brand reds and purples; the ball bleeds warm light into the field behind it"* (Raycast-era)
   - *"A floating app-window mockup offset to the right of a muted purple mesh; subject is flat, no light interaction"* (Linear-style)
   - *"A machined aluminum cylinder sits on a dark stage under a tight top spotlight, grounded by a soft contact shadow"* (B&O-style)
   - *"Diagonal 3D glass bars fill the viewport. No centered subject — the geometric mass is the hero"* (current Raycast, sculptural field)
   - *"Hand-painted warm landscape scenes; no foreground subject — the background IS the hero"* (mymind)
   - *"Faint dot grid on dark with a code panel centered, subject has a drop shadow, no glow"* (Vercel-style)

2. **Pick a starting preset** from the 9 in `hero-stage.md`:
   - `luminous-on-gradient`, `device-on-mesh`, `painterly-no-hero`, `grid-on-dark`, `object-on-spotlight`, `editorial-photo`, `shader-ambient`, `flat-blank`, `sculptural-field`

   Or set `preset: null` and fill every dial manually. Presets are starting points, not constraints.

3. **Tune the four dial groups** (background / hero / relation / form). Defaults must stay `subtle` unless the brand is genuinely loud.

   **Background dials:** `medium` (`gradient` / `mesh` / `painterly` / `shader` / `pattern` / `bokeh` / `sculptural` / `noise` / `photo` / `absent`), `color_mode`, `saturation`, `light_source`, `falloff`, `vignette`, `texture`, `motion`, `intensity`, `safe_zone`, `color_palette` (3–5 hues).

   **Hero dials:** `subject` chosen **by intent, not form** — `none` / `luminous` (light-emitter, CSS-rendered) / `object` (concrete physical product → generic warm metallic form as a decorative placeholder, user swaps it for their own 3D render before shipping) / `device` (product window, CSS-rendered) / `composition` (arranged elements, CSS-rendered) / `photo-cutout` (prose placeholder). Plus `form` (per-subject: geometry enum for `luminous`, layout label for `composition`, ignored otherwise — canonical definition in `hero-stage.md`), `placement`, `scale`, `tint`.

   **Relation dials:** `type` (`flat` / `glow` / `halo` / `reflection` / `emissive` / `shadow-only`), `bleed` (0–100).

4. **Sanity-check using the subject × relation compat matrix in `hero-stage.md`.** A `device` with `emissive` relation makes no physical sense. A `luminous` with `shadow-only` contradicts its own physics. An `object` with `emissive` turns it into a lightbulb. Match the relation to the subject's intent.

   **Honesty rule for `object`:** We never CSS-simulate a concrete physical product. `subject: object` renders as a **generic warm metallic form** (vertical pill, horizontal disc, or soft capsule) that holds the slot on the stage as a decorative element. The form makes no attempt to represent the actual product — it's a placeholder the user swaps for their real 3D render or product photography before shipping. The surrounding stage (spotlight, vignette, floor, contact shadow) is fully composed so the swap is trivial. Same honesty principle as `medium: photo` and `subject: photo-cutout` — don't fake what you can't render.

5. **Decide motion** on the background: `static` / `drift` / `pulse` / `reactive`. Default `static`. Only `drift` or `pulse` if the brand's own site visibly animates.

6. **Opt into `medium: shader`** only if the brand clearly uses animated WebGL as primary identity and one of the shader presets fits. See `background-shaders.md`. Default to CSS/SVG mediums. Shader defaults must also be `subtle`.

7. **Write the `hero_stage` YAML block** — see Phase 7 schema. Include `observed_style` (prose), the three dial groups, and a `disclaimer` when real-brand assets are proprietary.

**Photo-hero rule.** `medium: photo` or `subject: photo-cutout` renders a labeled prose placeholder, never fake stock imagery. Honest is better than fake.

**Subtle-by-default rule.** Every dial defaults to its calmest value. `intensity: subtle`, `vignette: off`, `bleed: ≤ 30`. Brands that look maximalist on their own site still read as `subtle` in our fallback, because hero copy sits on top and legibility is non-negotiable.

### Phase 5: Confirm Direction
Summarize the aesthetic direction in 2-3 sentences. Include the primary tension or trade-off that defines this language (e.g., "Industrial precision softened by warm grays" or "Playful shapes with serious typography"). Present this to the user and wait for confirmation before generating files.

Example:
> **Direction:** Swiss-industrial with a single accent color as a signal device. Monochrome palette, tight grids, mechanical motion. The contrast between clinical precision and one moment of color creates visual tension. Type-driven hierarchy using a geometric sans + monospace pair.
>
> Proceed?

### Phase 6: Token Preview
After the user approves the direction, present the core foundational tokens for a final check before full generation:

> **Proposed Core Tokens:**
> - **Background:** `#FAF8F5` (warm paper)
> - **Accent:** `#8E3D6E` (deep plum)
> - **Body Font:** Hanken Grotesk, 15px, weight 400
> - **Display Font:** Spectral, 34px, weight 500
> - **Base Radius:** 6px
> - **Base Spacing:** 8px grid
> - **Elevation:** Subtle (1-2px diffused shadows)
>
> Confirm or adjust?

This gives the user a low-cost opportunity to correct a foundational value that would otherwise cascade incorrectly through all generated files.

### Phase 7: Build Design Model
Create a `design-model.yaml` in the skill folder as the **Single Source of Truth**. If the skill folder doesn't exist yet, create it now (default location from Phase 9) — don't wait until Phase 9 to make the directory. This file captures every design decision in a structured, machine-readable format. All subsequent files (tokens.md, components.md, platform-mapping.md, previews) are generated FROM this model.

The YAML has two token layers: **Primitives** (raw ramps) and **Semantic** (role-based tokens referencing primitives).

```yaml
name: "Aster"
philosophy: "A quiet reading room for research. Warm paper, ink text, one plum accent."
primary_mode: "light"
brand_domain: "research notes / citation management"
brand_type: "ui-rich"    # or "content-rich"
mono_for_code: true      # code blocks, file paths, shell commands, inline technical tokens
mono_for_metrics: false  # pricing, counts, timestamps, percentages, ID strings
# locked_weight: 400     # OPTIONAL. Set only when the brand genuinely uses a single font weight across all text. Most brands do not — leave unset. If set, ALL type scale rows use this weight; the `weight` column becomes "—" in the scale table (or a single row at the top of the table).
# Backwards-compat: older skills may have `mono_for_data: true/false`. Treat `mono_for_data: true` as `mono_for_code: true + mono_for_metrics: true`, and `false` as both false.

# ── PRIMITIVES ── Raw scales derived from brand analysis
primitives:
  colors:
    neutral:    # Temperature matches the brand (warm/cool/pure)
      50: "#FAF8F5"
      100: "#F3F0EA"
      200: "#E6E1D8"
      300: "#D4CEC2"
      400: "#A8A193"
      500: "#7E776A"
      600: "#5F594E"
      700: "#48433A"
      800: "#322E27"
      900: "#211E19"
      950: "#14120E"
    brand:      # Accent hue, 500 = primary
      50: "#FBF1F7"
      100: "#F6E0EC"
      200: "#ECC2DA"
      300: "#DA97BE"
      400: "#BC6597"
      500: "#8E3D6E"
      600: "#76305B"
      700: "#5E2649"
      800: "#471C37"
      900: "#321326"
      950: "#1F0A17"
    red:   { 50: "#FEF2F2", 500: "#E5484D", 900: "#7F1D1D" }
    green: { 50: "#F0FDF4", 500: "#4AB66A", 900: "#14532D" }
    amber: { 50: "#FFFBEB", 500: "#E5A73B", 900: "#78350F" }
  spacing: [0, 1, 2, 4, 6, 8, 12, 16, 20, 24, 32, 40, 48, 64, 96]
  radii: [0, 2, 4, 6, 8, 12, 16, 24, 999]
  # NOTE: The default radii scale above is a SUPERSET — trim unused values for the brand.
  #   Pill-first brands (Cursor, Stripe pill CTAs)    → radii: [0, 4, 8, 999]
  #   Sharp / hard-edge brands (Linear, Nothing)      → radii: [0, 2, 4]
  #   Soft-but-not-round brands (Notion, Apple)       → radii: [0, 4, 8, 12, 16]
  # RULE: Radii primitives should only contain values the brand actually uses. A scale
  # with 9 values but only 2 referenced is a signal that you over-sampled. After generating
  # semantic tokens, audit the primitives — any primitive value not referenced by a semantic
  # token must be removed.

# ── SEMANTIC TOKENS ── Roles that reference primitives
tokens:
  colors:
    light:
      background: "{neutral.50}"
      surface1: "{neutral.100}"
      surface2: "{neutral.200}"
      surface3: "{neutral.300}"
      border: "{neutral.200}"
      border_visible: "{neutral.300}"
      text1: "{neutral.900}"
      text2: "{neutral.600}"
      text3: "{neutral.500}"
      text4: "{neutral.400}"
      accent: "{brand.500}"
      accent_subtle: "{brand.50}"
    dark:
      background: "{neutral.950}"
      surface1: "{neutral.900}"
      surface2: "{neutral.800}"
      surface3: "{neutral.700}"
      border: "{neutral.800}"
      border_visible: "{neutral.700}"
      text1: "{neutral.50}"
      text2: "{neutral.400}"
      text3: "{neutral.500}"
      text4: "{neutral.600}"
      accent: "{brand.400}"
      accent_subtle: "{brand.950}"
    success: "{green.500}"
    warning: "{amber.500}"
    error: "{red.500}"
    # Status tints — backgrounds behind status text/badges (foreground stays the 500 step).
    # Derivation rule: light mode = lightest ramp step (50), dark mode = darkest (900).
    success_bg: { light: "{green.50}", dark: "{green.900}" }
    warning_bg: { light: "{amber.50}", dark: "{amber.900}" }
    error_bg:   { light: "{red.50}",   dark: "{red.900}" }

  spacing:
    2xs: 2
    xs: 4
    sm: 8
    md: 16
    lg: 24
    xl: 32
    2xl: 48
    3xl: 64
    4xl: 96

  radii:
    element: 4      # small controls, checkboxes
    control: 6      # buttons, inputs
    component: 8    # cards, panels
    container: 12   # modals, sheets
    pill: 999       # pills, tags (if brand uses them)

  typography:
    # Families + base sizes. tokens.md derives the full 7-token type scale from these:
    # --display, --heading, --subheading, --body, --body-sm, --caption, --label (canonical names,
    # identical in tokens-template.md and platform-mapping-template.md).
    display: { family: "Spectral", size: "34px", weight: 500, line_height: 1.15 }
    body: { family: "Hanken Grotesk", size: "15px", weight: 400, line_height: 1.5 }
    mono: { family: "IBM Plex Mono", size: "12px", weight: 400 }

  elevation:
    strategy: "subtle"
    # ...

  motion:
    personality: "smooth"
    easing: "ease-in-out"
    duration_fast: "120ms"
    duration_normal: "220ms"

  # Hero stage — composed background + optional hero subject + relation.
  # Mandatory. Replaces the older `background_graphics` block.
  # See references/hero-stage.md for the full dial reference.
  hero_stage:
    preset: "painterly-no-hero"   # or null for fully manual
    observed_style:
      description: "Soft ink-wash fields in plum and paper tones; no foreground subject — the wash IS the hero."
      where_used: ["hero", "feature sections"]
    background:
      medium: "painterly"         # gradient / mesh / painterly / shader / pattern / bokeh / sculptural / noise / photo / absent
      color_mode: "palette"       # monochrome / dual-tone / palette / brand-tinted-neutral
      saturation: "muted"         # flat / muted / vibrant / neon
      light_source: "ambient"     # top / bottom / top-l..br / center / ambient / none
      falloff: "soft"             # hard / soft / radial / linear
      vignette: "off"             # off / subtle / strong
      texture: "paper"            # clean / grain / paper / paint / pixel
      motion: "static"            # static / drift / pulse / reactive
      intensity: "subtle"         # subtle / bold / blown-out  ← default subtle
      safe_zone: "full-bleed"     # full-bleed / masked-for-text / edge-only
      color_palette: ["#DA97BE", "#8E3D6E", "#E6E1D8", "#A8A193", "#FAF8F5"]
    hero:
      subject: "none"             # none / luminous / object / device / composition / photo-cutout  ← intent, not form
      # form: "sphere"            # sphere / disc / ring / torus — ONLY for luminous. Ignored for everything else.
      # placement, scale, tint ignored when subject: none
      # NOTE for `object`: concrete physical products render as a generic warm metallic
      #                    form (decorative placeholder). The user swaps it for their
      #                    own 3D render / product photo before shipping. The form
      #                    doesn't resemble the product — it just holds the slot.
    relation:
      type: "flat"                # flat / glow / halo / reflection / emissive / shadow-only
      bleed: 0                    # 0-100, how much subject light spills into background
      # Compat: see subject × relation matrix in references/hero-stage.md.
      # Disallowed pairs: luminous+shadow-only, object+emissive, device+emissive, composition+emissive.
    disclaimer: "Approximated with SVG + CSS. The real brand uses commissioned illustrations not redistributed with this skill."

  # Dual-track iconography — brand reality + our fallback.
  # The skill renders `fallback_kit`; `observed_style` documents truth.
  iconography:
    observed_style:
      description: "Custom 1.75px outline icons with rounded terminals. Humanist with slight irregularity. Not from any standard kit."
      stroke_weight: "regular"
      corner_treatment: "soft"
      fill_style: "outline"
      form_language: "humanist"
      visual_density: "balanced"
    fallback_kit:
      name: "Phosphor"
      weight: "regular"        # thin / light / regular / bold / fill / duotone
      match_score: "high"      # high / medium / low
      match_reasoning: "Phosphor regular matches the observed stroke weight (~1.5px), rounded terminals, and humanist form language. Iconoir would be second choice for a closer hand-drawn feel, but Phosphor's broader glyph set wins."
      cdn: "https://unpkg.com/@phosphor-icons/web@2/src/regular/style.css"
      icon_class_prefix: "ph ph-"
    disclaimer: "Icons in the generated preview are a best-match fallback from the Phosphor kit. The brand's actual icons are proprietary and not redistributed with this skill."

components:
  button_primary:
    source: "observed"
    background: "{brand.500}"
    color: "#FFFFFF"
    padding: "10px 16px"
    radius: "{radii.control}"
    font_weight: 500
    hover: { background: "{brand.600}" }
  # ...

# App screen — product UI rendered inside a device frame.
# Required for Phase 13 generation.
app_screen:
  archetype: "list-detail"  # dashboard / editor / list-detail / feed / conversational / canvas
  frame: "browser"          # browser / phone / desktop / tablet
  frame_params:
    url: "app.aster.ink/library"     # browser only — fictional domain
    title: "Aster — Library"
  content_seed: "citation library for a climate-paper draft"   # one-line description of what the screen shows
  required_tokens_checklist:
    - "background, surface1, surface2, surface3, border, border_visible"
    - "text1, text2, text3, text4"
    - "accent, accent_subtle, success, warning, error"
    - "all typography scale tokens"
    - "all spacing tokens used in components"
```

**How to generate the primitives:**
- **Neutral ramp:** Extract the brand's gray temperature (warm/cool/pure) from the analysis. Generate a 50-950 ramp that matches. Warm brand → warm-tinted grays. Cool brand → cool-tinted.
- **Brand ramp:** The accent color becomes 500. Generate lighter (50-400) and darker (600-950) variants around it.
- **Status colors:** Minimal ramps (50, 500, 900) for red/green/amber. Enough for bg-tint + foreground + dark-mode.
- **Spacing/radii primitives:** A superset scale. Semantic tokens pick from this scale.

**Avoid the AI default look.** Left unconstrained, language models converge on the same handful of "tasteful" choices — which is exactly what makes generated design systems look generated. Two ban lists apply whenever YOU are inventing or deriving a choice:

- **Banned as invented display/heading faces:** Space Grotesk, Playfair Display, Fraunces, Instrument Serif, DM Serif Display, DM Serif Text — and Inter used as a display/heading face. These are the statistical defaults, not decisions. Pick from a wider pool instead: Geist, Satoshi, Cabinet Grotesk, General Sans, Hanken Grotesk, Manrope, Bricolage Grotesque, Newsreader, Spectral, IBM Plex Serif, Source Serif 4, Libre Caslon Text, Zodiak — or anything else that's genuinely motivated by the brand. (Satoshi, Cabinet Grotesk, General Sans and Zodiak load from Fontshare; the rest are on Google Fonts.)
- **Banned as invented genre palettes:** premium → beige + brass + oxblood; tech/SaaS → violet glow on near-black (the `#5E6AD2` family); fintech → navy + teal; wellness → sage + cream. If your palette for a fictional brand lands on one of these, you didn't derive it — you defaulted to it. Go back to the brief and find what's specific.

**The nuance that matters:** these bans apply ONLY to invented or derived decisions — fallback kits, fictional brands, description-only briefs. If the real analyzed brand demonstrably uses Inter as its headline face or ships a sage-and-cream palette, the skill documents reality. `observed_style` always wins over the ban list. The bans exist to stop YOU from defaulting, not to overrule a brand.

`scripts/validate.mjs` cross-checks this: it emits a WARN when a banned font heads the display stack of a generated skill. The WARN is a prompt to justify, not an automatic failure.

Write the YAML first. Then generate all other files by reading from it. This ensures tokens.md, components.md, platform-mapping.md, and preview.html all use the exact same values.
