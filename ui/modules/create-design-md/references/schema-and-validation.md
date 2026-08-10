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

For URL reconstruction, use flat names such as `background-primary`, `foreground-secondary`, and `border-muted`, matching `^[a-zA-Z0-9][a-zA-Z0-9-]*$`. Do not emit nested color groups or URL-specific typography field aliases.

Identify the export target before writing:

- Tailwind v4: `css-tailwind`
- Tailwind v3: `json-tailwind`
- Other projects: `dtcg`

Run `npx @google/design.md spec` before encoding theme modes. Use theme-aware syntax only when the installed specification supports it; otherwise retain alternate values in a `## Themes` table and keep the default value under the canonical token.

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

Before saving, remove unsupported YAML tokens, page-local behavior presented as product-wide rules, invented product character, duplicate schema, and vague advice.

## Validation Gate

Run:

```bash
npx @google/design.md lint DESIGN.md
npx @google/design.md export --format <format> DESIGN.md
```

Inspect the export. Every populated category supported by the target must emit its corresponding output family. For `css-tailwind`, verify:

- `colors` -> `--color-*`
- `typography.<name>.fontFamily` -> `--font-*`
- `typography.<name>.fontSize` -> `--text-*`
- `rounded` -> `--radius-*`
- `spacing` -> `--spacing-*`

If an existing DESIGN.md is updated, preserve the original temporarily and run:

```bash
npx @google/design.md diff <previous-file> DESIGN.md
```

Restore any accepted decision unless current governing evidence or the user explicitly replaces it. Do not retain generated export files. Do not report success while lint or export fails, or while a populated supported category fails to emit.
