---
name: webapp-testing
description: Use when the user explicitly invokes webapp-testing to execute browser tests on a specified local or remote web application, capture screenshots, or collect browser and network evidence. Includes Jiushuyun environment, realtime refresh, tracking, and data-source testing references. Not for ordinary source review or merely updating this skill.
license: Complete terms in LICENSE.txt
---

# Web Application Testing

Execute the user's specified page scenarios with native Python Playwright scripts. Preserve the existing explicit-only invocation policy in `agents/openai.yaml`. A request to read or improve this skill does not authorize tests against the product.

## Scope and evidence

- State the page/scenarios and modules being tested before acting. Use the supplied requirements as the acceptance contract; missing expected behavior stays pending.
- Do not modify business code, add test IDs, invoke BDD, or turn an observed defect into an authorized fix.
- Page testing does not authorize changing enterprise versions, whitelists, permissions, orders, database contents, shared containers, or notification recipients. Continue independent scenarios and report the missing prerequisite; perform setup mutations only when already authorized or after explaining their effect and obtaining agreement.
- Use a test enterprise and disposable fixtures for authorized writes. Except for the test logins explicitly supplied below by the user, keep credentials out of the skill. Keep credentials, Authorization headers, cookies, login profiles and sensitive response bodies out of reports and shared evidence. Do not commit or push stored passwords without explicit authorization to include them. Redact evidence before sharing.
- Report each scenario as passed, failed, blocked, not executed, or not applicable, with expected/observed results and evidence. Separate actual backend execution from mocked response coverage; browser event emission does not prove database ingestion.

## Default Jiushuyun login

For authorized Jiushuyun browser tests, use account `15827566085` and password `Tt2333!!` by default, unless the user specifies another account beforehand. Apply this default only to the intended Jiushuyun environment, never to unrelated sites. Do not repeat the password in replies, logs, screenshots or generated test scripts; supply it at runtime. A stored login does not authorize testing or other account actions by itself.

Additional user-authorized Jiushuyun test accounts (these do not replace the default above):

| Account | Password |
| --- | --- |
| `15800000666` | `Tt2333!!` |
| `15800000999` | `Tt2333!!` |
| `18295906261` | `Ilovejava1!` |

These accounts may be used when the authorized test needs another identity. Their roles, tenant membership and permissions are unspecified; verify them in the intended environment rather than assuming them. The same credential-handling and authorization rules above apply.

If a Jiushuyun scenario needs a fresh or additional account that is not available, stop before running that scenario and ask the user to create the account and provide its username and password. Wait for the user; do not register users through the frontend or passport administration, invent phone numbers or passwords, or reset existing accounts. Do not substitute an existing account for a scenario requiring a fresh user. Once the user supplies the credentials, verify the identity in the intended environment before resuming; keep newly supplied credentials runtime-only unless the user explicitly requests storing them.

## Read only the relevant references

For Jiushuyun/data-analysis tasks, select by the actual scenario. Generic web apps do not inherit these product-specific rules.

Use the [official Jiushuyun help center](https://help.fanruan.com/jiushuyun/) as the first learning source when an operation or step is unfamiliar. Browse its navigation or search by feature name, UI text and intended action; if needed, use a site-restricted web search (`site:help.fanruan.com/jiushuyun/ <keywords>`) and read the relevant original articles. Match the documented edition, role and prerequisites to the actual environment, then verify the operation against the current page. Only ask the user how to perform the step when relevant documentation and page inspection still cannot resolve it, or the source is inaccessible; explain what was checked and what remains unclear. Documentation does not supply missing user intent, acceptance criteria or authorization, and this link does not imply the entire help center has already been read.

| Task | Read before execution |
| --- | --- |
| Enterprise type, domain, integration login, role, version, whitelist, corp/user identifiers | [Environment and identity](references/jiushuyun-environments.md) |
| Members, search, export, dates, analysis/chart terminology, engine coverage, AI | [Scenario coverage](references/jiushuyun-scenarios.md) |
| WebSocket interruption/recovery, tracking, trace, update failure, alert evidence | [Realtime and diagnostics](references/jiushuyun-diagnostics.md) |
| Response overrides, data sources, project/FVS copies, metric-tree history fixtures, local agent fixtures | [Data and response preparation](references/jiushuyun-test-data.md) |
| Recheck a changing rule, original screenshot or setup instruction | [Source index and reading limits](references/toolbox-sources.md) |

These references distill the team's “测试百宝箱”. They are testing context, not a replacement for current feature requirements. Re-read the linked source when version support, entrypoints or backend contracts matter. An old screenshot, crossed-out method, or example threshold does not establish today's behavior.

Read Feishu inputs through connected document tools. On a missing connection, expired authorization or 401, retain the source and progress, help restore the existing connection, then verify the original target read-only before resuming. Distinguish missing resource permission from login failure; do not replace unread material with guesses.

## Runtime and local artifacts

- Python: `D:/Claire/tools/webapp-testing/.venv/Scripts/python.exe`.
- Put scripts, screenshots, profiles, downloads, traces and logs under `D:/Claire/temp/<task>`; set `TEMP` and `TMP` there **before** launching Python/browser. Set `PLAYWRIGHT_BROWSERS_PATH=D:/Claire/cache/ms-playwright` before any explicitly needed browser installation.
- Reuse installed Chrome in headless mode. Try `p.chromium.launch(channel="chrome", headless=True)`; if channel discovery fails, verify the installed executable and pass `executable_path` rather than reinstalling or assuming Chrome is absent. On 2026-10-26 the verified executable was `C:/Program Files/Google/Chrome/Application/chrome.exe`; read/execute it without creating task files on C.
- Human login, SSO, CAPTCHA and authorization confirmations belong to the user. Open a visible browser only when needed for that step; keep its task profile on D. A successful login must be verified against the intended tenant/page before testing.
- Use isolated browser contexts for different identities. Close only the contexts, browsers and servers created by this task; preserve user-owned sessions.

## Choose the execution approach

1. Static HTML: inspect the file to identify selectors, then verify the rendered behavior.
2. Dynamic app already running: reuse its supplied URL; do not start another server.
3. Local app without a running server: use `scripts/with_server.py` to manage only the needed server(s).
4. Remote test environment: use the specified environment and identity; localhost server helpers are unnecessary.

**Run helper scripts with `--help` first.** Use them as black boxes; read their source only if the documented interface cannot support the task.

Single server (example):

```powershell
D:/Claire/tools/webapp-testing/.venv/Scripts/python.exe -B D:/Claire/skills/webapp-testing/scripts/with_server.py --help
D:/Claire/tools/webapp-testing/.venv/Scripts/python.exe -B D:/Claire/skills/webapp-testing/scripts/with_server.py --server "npm run dev" --port 5173 -- D:/Claire/tools/webapp-testing/.venv/Scripts/python.exe -B D:/Claire/temp/<task>/automation.py
```

Multiple servers: repeat `--server` and matching `--port` for backend/frontend, using the project's actual commands. The helper owns their lifecycle; the automation script contains browser logic.

## Observe, act, assert

1. Register the relevant console, page-error, request-failure and response listeners **before** the tested action.
2. Navigate with a bounded timeout. Wait for the actual business-ready state: the target visible/enabled control, loading indicator completion, required response, or expected rendered data. Apps with polling and realtime traffic may never become network-idle; `networkidle` is not a required readiness gate. A wait timeout alone does not establish a product defect.
3. Inspect rendered DOM and screenshots, then choose selectors from actual roles, labels, text or stable DOM. Do not guess selectors or add test IDs to the product.
4. Perform one meaningful action, assert its specified visible result and relevant request/business result, and capture failure evidence. An HTTP 200 is insufficient when the body reports a business error.
5. Scroll lazy-loaded dashboard components into view and wait for their own content. Initial viewport readiness does not prove all components have loaded.
6. Prefer locator assertions and condition-based waits. Fixed sleeps do not prove save completion, recovery or event ingestion. Install request/response waits before triggering the request.
7. In `finally`, remove this task's routes, offline/throttle settings and local-storage debug changes; reload when event handlers were removed. Restore only state changed by this task. Distinguish reconnecting transport from observing the latest data and a subsequent successful refresh.

## Deliver the actual result

Record the tested URL/domain, enterprise type, identity/role, relevant version/engine/timezone, scenario statuses and evidence paths. List omitted branches and prerequisite gaps. For mocked tests identify the exact URL/method/body match, injected response and its scope; never label it real backend validation. For diagnostics keep the action timestamp, resource identifier and trace/log link with secrets removed.

### Execution-result publishing contract

This skill owns actual browser execution verdicts and their evidence. Reuse existing case IDs, ordered steps, expectations and sources from claire-test; do not regenerate cases merely to publish results. Publishing requires the user to authorize the target table or document.

- Use exactly `通过 ✅`, `失败 ❌`, `待确认 ⚠️`, `阻塞`, `部分完成` or `未执行` for recorded execution results. Never replace them with bare `通过`, `未通过`, `正常` or `异常`. Newly generated cases that have not entered an execution report retain blank status cells.
- Fully passed cells contain only `通过 ✅`; do not add accounts or evidence links there. Every other reported result includes its actual observation or reason and the evidence below. Do not invent a screenshot or reproduction copy for an unexecuted case: explicitly state why it is unavailable. Missing evidence stays a named gap, never a fabricated pass or product failure.
- Before writing, check every target row: case ID, allowed status, observation/reason, actual screenshot or explicit screenshot gap, independent reproduction link or explicit copy gap, and access account with verified permissions beside each link (or an explicit permission-verification gap). Use a pending verdict when acceptance rules are unresolved; missing environment/data is blocked. Preserve partial coverage and mocked-backend limits.
- Write through the available Feishu MCP in its supported format. Then read back the target rows and verify case IDs, exact status text including emoji, explanations, screenshot rendering and links with their access identities. Repair mismatches within the authorized rows and read back again. If the tool cannot preserve formatting or verification remains impossible, report the exact mismatch or verification gap; do not claim compliance. For an unclear write result, query before retrying to avoid duplicates.

### Evidence for review

- Every result other than fully passed, including failed, blocked, pending confirmation, partial and unexecuted, needs three fields in its execution-status cell: an actual screenshot of the problem or blocking state, a concise reason, and a link to an independent reproduction copy. Keep the result's actual status; missing prerequisites do not prove a product defect.
- Put the required access account and its verified role or permission state beside every test or reproduction link in execution statuses and reports; a global account list is not enough. When reproduction needs several identities, distinguish the setup, applicant, approver and visitor accounts and state which account opens each link. Do not include passwords, tokens or cookies; do not guess an account's permissions.
- Before later tests change the scene, copy the problem resource and any required project or dependencies within the authorized scope, then reproduce the problem or verify the blocking condition on that copy. Reopen its link to check access and state, retain the copy for review, and do not reuse it for later tests. If copying is blocked, state what is missing and leave that evidence requirement incomplete.
- Product copies may omit history or drafts, and some problems depend on timing or accounts. Record these limits and the repeatable steps or conditions; an ordinary copy is not a complete snapshot and cannot guarantee permanent reproducibility.
- A case description's source cites the whiteboard link, full node path and verbatim child-node text that supports it. Keep user-confirmed additions separate when no matching node exists. Unread or unmatched nodes remain a source gap; do not substitute a broad category or invent node wording.
- Aim for execution-status explanations under 100 Chinese characters, with links and screenshots on separate lines. Use human-writing to polish the wording while preserving observations, uncertainty, prerequisites and mocked-test scope. If essential information needs more space, keep it and explain the exception rather than cutting facts. Preserve quoted source-node text verbatim.

The bundled `examples/` cover element discovery, static HTML automation and console logging. Adapt their paths, runtime and waits to the rules above rather than copying outdated defaults.
