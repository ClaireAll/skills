# Intent and Acceptance

Read this for an ambiguous/new requirement, an explicit interview, or a request to author or materially revise a requirement brief or acceptance contract. It supplements the input reader; it does not replace Feishu/Figma evidence handling or start development. Clear-source summaries and extraction do not need an interview or this full workflow.

## Find the Actual Outcome

Start with a tentative one-sentence understanding and the specific information still missing. Reuse what the sources or user already established; do not ask every question as a fixed questionnaire.

Check the target user, their actual problem, the desired outcome, what observable result would count as success, and any binding constraint. Ask why now only when timing changes the scope or decision. A requested dashboard or button is a candidate solution, not proof of the underlying need; do not substitute a different product without the user's decision.

If the answer is only "modern", "scalable", or "best practice", ask which concrete situation or tradeoff matters. Attach your current hypothesis and its basis when useful, clearly allowing correction. Do not invent an opposing guess to manipulate agreement or treat your recommendation as the user's intent.

Use the main skill's decision-tree/frontier loop: facts come from scoped evidence, decisions come from the user, and dependent questions wait. Stop when remaining unknowns cannot change this deliverable or are explicitly recorded as stakeholder decisions. No subjective confidence percentage proves understanding. If repeated answers do not resolve the same gap, name it and offer to narrow or reframe instead of extending the interview indefinitely. A non-interactive run records blocked decisions; it does not fabricate user answers.

## Write a Reviewable Understanding

Keep it compact and use the user's terms. Include the relevant parts of this contract:

- **Outcome and users:** the problem being solved, for whom, and any reason timing matters.
- **Success:** observable results supported by the sources or explicitly confirmed by the user.
- **Scope and constraints:** what is included and which limits actually bind this task.
- **Not doing:** explicit exclusions and their basis. Do not invent exclusions to make the contract easier; mark a material unknown as unresolved.
- **Decisions and gaps:** source-backed rules, individual user decisions, proposals, rejected directions, and open questions, kept distinguishable.

The assembled understanding is still **pending review** until the user approves that version. Label it accordingly even when each individual answer is known. An unresolved issue that changes the outcome blocks an unconditional "ready" claim; a stakeholder-owned gap can be handed off explicitly without pretending it was settled.

Follow the main skill's strict gate: understanding/draft -> ask for review and stop; a later confirmation -> confirmed handoff and stop; only a subsequent user-selected stage may run. A concrete "confirm this version" is sufficient, in the user's language. Silence, "you decide", and an instruction to hurry do not themselves approve the understanding. If an acknowledgment could refer to something else, ask one focused confirmation rather than rejecting clear approval mechanically.

If the user corrects the scope, update the affected decisions and invalidate dependent assumptions; unchanged rules keep their identifiers and sources. When intent is approved, do not immediately create a spec just because it was requested earlier. If the user later selects drafting, the new draft gets its own review before further stages.

## Make Acceptance Observable

For an authored brief or acceptance contract, turn vague goals into conditions that someone can check without inferring the intended behavior. Extracting already-explicit conditions from a document is not authoring a new contract.

Use stable requirement IDs and source references. A compact row is enough:

| ID | Condition / role / initial state | Action | Observable result and timing | Source | Status |
| --- | --- | --- | --- | --- | --- |
| AC-01 | Conditions stated in the source | The relevant operation | The sourced or user-confirmed result | Source rule / user decision | Confirmed rule / proposed interpretation / unresolved |

Do not fill unknown cells with invented rules. Select applicable boundaries from the actual requirement: entry and permissions, defaults, state transitions, validation, asynchronous success/failure and recovery. An absent button does not prove API authorization; a successful response does not prove persisted state. Document each only when evidence or a user decision establishes it.

"Faster" needs a relevant measurement point, environment, workload and target. Ask which outcome matters, or offer a clearly labeled candidate; do not import upstream sample values such as latency or coverage thresholds. Preserve units, scope, timing and certainty from the source. An unmeasured baseline remains unmeasured, not a new statistic.

When several independently testable capabilities are genuinely bundled, expose their scope and relevant dependencies in a short list so the user can choose the boundary. Do not invent module architecture, build order or a hierarchy for a single capability; those are separate design/planning decisions.

Separate what the requested deliverable can do, what requires another user decision, and what is out of scope. This does not authorize commands, dependencies, schema/API changes, feature flags, automatic tests or code edits. Ordinary requirement work stays read-only, with no BDD invocation.

## Trace Change Impact

Use this when the user asks what a change will affect or when a rule may affect multiple entries and the boundary is unclear. Start from the changed rule and its source. Follow the relevant entry points, shared logic and API calls in scoped code. Record the evidence for each verified impact and mark any unavailable code or untraced path as pending.

| Changed rule and source | Verified impact and evidence | Paths or decisions still open | Observable acceptance |
| --- | --- | --- | --- |
| Rule ID or source section | Affected entry or shared logic, with file or symbol | Path to trace or product decision to confirm | Expected behavior supported by a confirmed rule |

Use the clarification loop for unresolved product decisions that change scope. A read-only impact analysis of confirmed rules needs no new approval. Share the list with `claire-test` when formal findings or self-check cases are requested.

## Keep the Deliverable Proportional

Default to the conversation. Do not create `SPEC.md`, intent files, a project plan, or a new spec system merely because upstream examples use them. If the user has selected the current drafting stage and requests a local requirement draft, use their existing format and D: destination, label unapproved additions and stop for review. A later document named in an earlier chained request does not bypass the intent review gate. A local draft is not permission to publish to Feishu or overwrite an existing document; existing-document edits need the user's applicable authorization.

Include executable commands, code-style examples, project structure or test-framework choices only when requested and verified in the repository; never fill a product requirement brief with invented engineering conventions. An acceptance contract is not a test plan and does not claim execution. Formal source findings/self-check cases remain with `claire-test`; page execution requires an explicit `webapp-testing` request.

When handed off after the review gate, share approved scope, rule/acceptance IDs and sources, non-goals, constraints and remaining gaps. Do not re-read all sources or launch another interview when nothing material has changed. If a later request changes the approved contract, review only the affected requirements before further downstream work.
