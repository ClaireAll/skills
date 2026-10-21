# DESIGN.md Schema and Validation

## Evidence Contract

Use the same normalization pipeline in every mode:

```text
role -> value -> source -> scope -> recurrence -> confidence
```

In repository mode, inspect existing DESIGN.md and explicit guidance first, then tokens/themes/global styles, shared primitives, representative routes, and only then surface-local code. A source is usable only when the selected product imports, references, inherits, or renders it.

In URL mode, sample colors, type, spacing, borders, radii, elevation, navigation, inputs, cards, and repeated structures at desktop and mobile widths. Prefer computed values and loaded CSS over visual estimates. A value becomes a system rule only when:

1. It is visible or computed on a rendered page.
2. Its value is measured or recurs for the same role across the required samples.
3. It changes a concrete implementation decision.

For exact URL values, require either a matching rendered value plus loaded declaration/custom property, or recurring computed values for the same role. Do not invent semantic aliases from raw CSS values. Keep URL-mode YAML sparse but non-empty whenever measured evidence survives.

Keep a private ledger by page and viewport, with element role, computed property/value, and matching loaded declaration or public custom property. A public property name is usable only when both its declaration and rendered use are observable. A site-wide prose rule must recur across at least two sampled templates; otherwise scope it to the inspected page. A component rule needs the same treatment on at least two sampled pages and a concrete implementation consequence.

## Frontmatter Shape

Start with:

```yaml
---
version: alpha
name: <string>
description: <string>
---
```

Only `name` is required. Add `colors`, `typography`, `rounded`, `spacing`, or `components` only when a governing source defines that system or contract.

- `colors`, `rounded`, and `spacing` are flat mappings with valid token names.
- `typography` is a mapping of named scales. Each scale contains only `fontFamily`, `fontSize`, `lineHeight`, `fontWeight`, and `letterSpacing` as applicable.
- `components` may refer to canonical token paths but may not create a parallel token schema.
- Use mappings, never sequences, for token groups. Preserve source token names where they exist; do not derive convenience scales from utilities or repeated literals.
- Token references use `{path.to.token}`.

Resolve framework utilities through the selected product's active theme before recording exact values. If the source has a single group-level `--radius`, normalize it to `rounded.base`; do not invent a radius scale from utility classes. A typography child must be a field mapping, not a scalar font name. Inspect the parsed frontmatter before saving, not just the rendered Markdown.

For URL reconstruction, use flat names such as `background-primary`, `foreground-secondary`, and `border-muted`, matching `^[a-zA-Z0-9][a-zA-Z0-9-]*$`. Do not emit nested color groups or URL-specific typography field aliases.

Identify the export target before writing:

- Tailwind v4: `css-tailwind`
- Tailwind v3: `json-tailwind`
- Other projects: `dtcg`

URL-only reconstruction defaults to `css-tailwind` unless the user selects another target.

Read the already installed DESIGN.md tool's `spec` output before encoding theme modes. Use theme-aware syntax only when that specification supports it; otherwise retain alternate values in a `## Themes` table and keep the default value under the canonical token. Do not invent parallel light/dark token names or describe the fallback table as machine-readable theme support.

## Markdown Contract

Start with `## Overview`, limited to product purpose and evidenced design direction. Include only supported sections, in this order:

1. Colors
2. Themes
3. Typography
4. Layout
5. Elevation & Depth
6. Shapes
7. Components
8. Do's and Don'ts

Outside the optional Themes table, Markdown records rationale and application guidance, not token inventories, source syntax, audit notes, rejected evidence, or documentation methodology. Every sentence outside the Overview must change an implementation decision. Add a Don't only when an explicit governing source states the prohibition.

Keep citations, conflicting sources, and unresolved questions in the surrounding report, not in `DESIGN.md`. Preserve the product's existing language.

Before saving, remove unsupported YAML tokens, page-local behavior presented as product-wide rules, invented product character, duplicate schema, and vague advice.

## Validation Gate

Use an already installed DESIGN.md executable or the repository's existing script. The commands below use a placeholder for that executable, not a request to download it. Do not invoke `npx` in a way that fetches a missing package. If no tool is available, report lint/export as blocked and ask before installation; do not claim successful validation.

Run with the existing tool:

```bash
rtk proxy <installed-design-md-command> lint DESIGN.md
rtk proxy <installed-design-md-command> export --format <format> DESIGN.md
```

Inspect the export. Every populated category supported by the target must emit its corresponding output family. For `css-tailwind`, verify:

- `colors` -> `--color-*`
- `typography.<name>.fontFamily` -> `--font-*`
- `typography.<name>.fontSize` -> `--text-*`
- `rounded` -> `--radius-*`
- `spacing` -> `--spacing-*`

If an existing DESIGN.md is updated, preserve the original in memory or in the task's D: temporary directory and run:

```bash
rtk proxy <installed-design-md-command> diff <previous-file> DESIGN.md
```

Restore any accepted decision unless current governing evidence or the user explicitly replaces it. Inspect exports in memory; do not retain generated export files. Do not report success while lint or export fails, or while a populated supported category fails to emit. If the target cannot represent supported design information, retain that information and report the exporter limitation rather than deleting it to force a pass.
