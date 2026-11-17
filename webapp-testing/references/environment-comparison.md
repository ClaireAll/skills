# A/B environment acceptance

Use this mode only for an explicitly invoked `webapp-testing` task that asks to compare environments. A is the environment under acceptance; B is the baseline. A typical input is:

```text
$webapp-testing A:<待验收环境 URL> B:<基准环境 URL> 飞书链接:<测试文档 URL>
```

The user supplies the actual A, B and Feishu URLs for each task. The sample addresses and document in the request that established this mode are examples, not standing test targets. If a required URL is missing, ask for it before dependent testing. Use the Jiushuyun account authorized in the main skill unless the user supplies a different authorized test account; verify its environment, identity and role before use. Keep passwords runtime-only. Test all existing case IDs in the supplied document unless the user narrows the scope. Put scripts and evidence under `D:/Claire/temp/<task>`.

## Acceptance rules

1. Read the existing cases, expectations and sources from the supplied test document. Preserve their IDs and wording; do not regenerate or rewrite cases.
2. For each case, observe B's actual behavior first, then run A under the same relevant conditions. Compare A against B's observed behavior. If the document's expectation conflicts with B, mark `待确认 ⚠️`, record the conflict, and do not automatically fail A.
3. Distinguish real backend execution from mocked responses. Missing account permission, data or environment is `阻塞`; do not infer a pass.
4. Use only authorized test accounts and disposable data for writes. Do not change permissions, enterprise configuration or shared data without separate authorization.

## Repeatable, low-token execution

1. Verify entry points and selectors against the current pages before writing a batch script. Follow applicable guidance in `../../playwright-best-practices/SKILL.md` while retaining this skill's native Python Playwright runtime. Let independent cases continue after one fails.
2. Have the script record each case's B and A observed behavior and assertions, necessary component screenshots, console errors and request failures. Fix controllable data, viewport, language and theme where the application permits, to avoid meaningless visual differences.
3. Read compact machine-generated results for passed cases. Expand logs, screenshots and difference images only for failed, pending or blocked cases. Correct script errors and rerun affected cases before assigning product verdicts.
4. Do not add project dependencies or change business code. Keep scripts, profiles and evidence in the task's D-drive directory.

## Feishu writeback

An explicit request to execute this A/B workflow with a specified test document authorizes updating only the `执行状态` cells of existing in-scope case rows in that document. Preserve IDs, descriptions, expectations, sources and other people's content. Apply the main skill's exact status vocabulary and evidence contract: fully passed cells contain only `✅`; other cells state the observed behavior or blocker and include real screenshots, independent reproduction links, and verified access account and permission beside each link, or explicitly name each evidence gap. Never fabricate evidence or label a case fully passed when required evidence is missing.

After writing, read back every target row and verify its ID, status, explanation, rendered image and link. If a write result is unclear, query the original document before retrying. Report any unresolved mismatch or verification gap.

## Final response

Report only the tested environments, scope, counts by status, failed/pending/blocked details, evidence gaps and Feishu readback result, with a link to the test document. Do not paste all passed steps or long browser logs into the conversation.
