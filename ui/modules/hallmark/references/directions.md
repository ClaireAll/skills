# Selected Hallmark directions

Load only when a page has an open visual direction or the user names a Hallmark theme. These are concise local adaptations of six upstream materials, not vendored themes or pixel-exact presets. Theme choice never overrides the project's applicable design or `ui` local rules.

| Direction | Material to draw from | Where it can help | Local adaptation |
| --- | --- | --- | --- |
| Cobalt | Cool near-white, blue-grey text and rules, a cobalt action accent, technical type hierarchy. | Developer tools and product demonstrations with real code or operational states. | Show meaningful code/state; omit the upstream ASCII field, animated effects and keycap mechanics unless independently requested. |
| Studio | Cool white, dark ink, editorial display hierarchy, true-color work photographs and a small orange signal. | Portfolios and studios with actual work to show. | Let work lead; crop marks, dot grids and grain are not required decoration. |
| Vellum | Parchment tones, umber text, ultramarine accent and ledger-like rules. | Coffee, craft and shops whose real material supports a printed trade-ledger treatment. | Use readable available Chinese typography; do not import blackletter fonts or fake age, provenance and founding dates. |
| Werkstatt | Warm putty, near-black text, strong ruled cells and functional blue/red/yellow categories. | Classes and workshops with schedules and course information. | Color categories only when real categories exist. Preserve actual photo meaning; uppercase Latin headings and monochrome photos are not Chinese UI requirements. |
| Almanac | Cool slate and a pale sheet, dark ink, contrasting heading/prose hierarchy, aligned figures and a chart accent. | Reference pages, catalogs and data-rich editorial content. | Use actual figures; existing chart semantics and table primitives win over a new palette. |
| Ribbon | Warm light surfaces or a blue-black night, quiet sans-serif hierarchy and a restrained signal color. | Listening and calm consumer experiences with actual controls and content. | Choose one mode based on the task; no automatic dark-mode switch, generated light canvas or added motion. |

## Apply a material, not a template

- Derive the page's content and structure from its task before choosing the visual treatment. A cafe's visit page needs useful visit information; a class page needs course choices. Neither acquires a newsletter or pricing section because a theme example has one.
- When authorized to choose, select a fitting direction and explain the relationship to the material. Do not ask the user to compare all six or read all upstream files. If none fits, derive a bespoke direction from the subject.
- Translate the material into the project's existing canvas, surface, text, border, action and status tokens. Keep `letter-spacing: 0`, discrete type sizes and the existing font-loading method. Do not introduce font downloads, effects or dependencies from upstream examples.
- This selection has no precise token preset or preview images. When a user requests exact fidelity to one of these themes or names an unlisted theme, read its reference at the pinned upstream revision before describing details. Inspect its preview when visual fidelity matters; do not claim a preview was inspected when it was not. If the source is unavailable, report that limitation and do not substitute an imagined theme.

## Sources

Reviewed revision: `4f6a46c6dc325d40ab268c93e25c7b96676ebccd`, Hallmark v2.0.0. Material summaries come from the [theme index](https://github.com/Nutlope/hallmark/blob/4f6a46c6dc325d40ab268c93e25c7b96676ebccd/skills/hallmark/references/themes/index.json). Exact theme references are under the [pinned theme directory](https://github.com/Nutlope/hallmark/tree/4f6a46c6dc325d40ab268c93e25c7b96676ebccd/skills/hallmark/references/themes), named `<slug>.md` with `<slug>.jpg` previews. Source tokens and preview appearance are reference evidence, not local implementation rules.
