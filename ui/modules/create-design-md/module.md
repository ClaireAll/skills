---
name: create-design-md
description: Use when creating or updating a DESIGN.md from a product repository or public website, especially when coding agents need evidence-based UI tokens and design guidance.
---

# Create DESIGN.md

Capture the intentional design system for one product or coherent website. Do not turn every repeated implementation value into a design decision.

## Boundaries

- Modify only `DESIGN.md`; do not change product source, dependencies, configuration, or generated files.
- Keep the document evidence-based, implementation-relevant, and compact.
- Preserve accepted decisions in an existing `DESIGN.md` unless the user or stronger current evidence replaces them.

## Choose the Evidence Mode

**Repository mode** is the default whenever source is available. Write `DESIGN.md` at the selected product root. If a repository has multiple deployable products and ownership is unclear, ask which product is in scope.

**URL mode** applies only when a public URL is the sole source. It requires rendered browser inspection at desktop and mobile widths. Inspect computed styles, loaded stylesheets, and up to three representative same-origin pages. If rendered inspection is unavailable, ask for source or screenshots; do not infer a design system from page copy or raw HTML alone.

## Required Route

1. Collect evidence in the chosen mode, then **MUST READ** `references/schema-and-validation.md` before drafting frontmatter.
2. Record each candidate as `role -> value -> source -> scope -> recurrence -> confidence`.
3. Admit only values that are shared, observable, and consequential to implementation. Omit local styling, guesses, migration artifacts, generated output, and undocumented preference.
4. Normalize admitted evidence into the DESIGN.md schema before writing Markdown. Do not draft prose and retrofit invalid YAML later.
5. Write the smallest document that represents supported design intent: overview first, then only the standard sections that have evidence.
6. Run the required lint and compatibility export. Do not return a draft, summary, or success claim until both pass and the populated categories actually emit.

## Evidence Discipline

- Repository evidence may establish canonical token names, component ownership, and documented rationale, but only if the selected product consumes it.
- URL evidence may establish rendered patterns and measured values, not private intent or source ownership.
- In URL mode, a claim needs an observation, a measured or recurring basis, and a concrete implementation consequence. Otherwise omit it.
- When sources conflict, document the governing guidance and report the conflict outside `DESIGN.md`.

## Report

Return the mode, audited product or URL, output path, governing sources, omitted or conflicting areas, and fresh lint/export results. Label URL-mode output as a reconstructed draft.
