---
name: human-writing
description: Use when drafting, rewriting, or auditing Chinese-first prose that must sound natural and human-written without inventing facts, especially when removing AI-style filler, inflated claims, promotional language, formulaic structure, or chatbot residue.
---

# Human Writing

Write Chinese-first prose with a believable human voice, or revise Chinese and English text without flattening its meaning or inventing detail. Natural writing starts with material, voice, and purpose; AI-pattern removal is a selective editorial pass, never a license to add facts, attitudes, or personality.

## Route The Task

| Request | Read | Do |
| --- | --- | --- |
| New Chinese narrative, essay, post, script, or long answer | `references/chinese-writing.md` | Classify it as non-fiction or fiction before drafting. |
| Rewrite or humanize existing text | `references/humanization.md` | Preserve information, then revise for voice and clarity. |
| English or mixed-language copy | `references/humanization.md` | Use the same no-fabrication and voice-calibration rules. |
| Audit only | `references/humanization.md` | Report patterns; do not rewrite unless asked. |
| User supplies their own writing sample | `references/humanization.md` | Match the sample's habits ahead of default style preferences. |
| Technical, legal, reference, or structured text | `references/humanization.md` | Use minimum intervention; preserve terms, evidence, and required structure. |

## Non-Negotiable Boundaries

- Obey the user's requested format, audience, language, and tone.
- Do not add non-fiction facts, names, dates, quotes, numbers, sources, or personal experience. Fiction may create details only when the user has asked for fiction.
- Keep technical, legal, and reference writing neutral unless the user requests a different voice.
- Do not manufacture personality with slang, typos, fake memories, generic disagreement, or decorative formatting.
- Preserve required Markdown, headings, lists, links, code, identifiers, quotations, placeholders, and exact wording that the user marks as fixed.
- When the source is abstract or thin, shorten it or retain a plain statement. Do not compensate by inventing examples, causes, outcomes, or a first-person perspective.

## Two-Pass Workflow

1. Lock the contract: classify the request, audience, format, factual status, and text that cannot change.
2. Calibrate the voice from user instructions and any supplied sample. For technical writing, clarity and restraint are the intended voice.
3. Diagnose only actual problems: inflated importance, promotional language, vague attribution, formulaic contrast/list/ending, unnecessary signposts, chatbot residue, or mechanical rhythm.
4. Revise locally and concretely. Prefer direct subjects, ordinary words, and source-supported detail already present in the material.
5. Check the result: facts, certainty, terminology, formatting, links, and required structure must remain intact; every remaining stylistic change must fit the target voice.
6. Deliver the requested artifact without exposing internal checklists unless the user asked for an audit.

## Pattern Judgment

The patterns in `references/humanization.md` and the audit script are review signals, not word bans. A detected term, a three-item list, or an em dash may be appropriate in context. Remove a pattern only when it makes the prose vaguer, more promotional, more formulaic, or less like the requested voice.

For factual work, replace unsupported grandeur with the supplied facts or delete it. For personal work, preserve the author's real opinions and uncertainty; do not add a performative "human" voice. For technical work, simple wording is enough: do not force jokes, first person, casual asides, or uneven structure.

## Audit Tool

Run the deterministic helper after a prose draft, or when the user requests a pattern audit:

```powershell
py .\scripts\audit_prose.py .\draft.md --language auto
py .\scripts\audit_prose.py .\draft.md --language zh --format json
```

The report identifies patterns to review. It never proves that a sentence is bad and never edits the file.

## Resources

- `references/chinese-writing.md`: Chinese material boundaries, fiction/non-fiction routing, and prose rhythm.
- `references/humanization.md`: no-fabrication rewriting, author-sample calibration, pattern judgment, and cross-language review.
- `scripts/audit_prose.py`: UTF-8 text/Markdown audit helper; its findings require human judgment.
