import assert from "node:assert/strict";
import { spawnSync } from "node:child_process";
import { mkdtempSync, mkdirSync, readFileSync, rmSync, statSync, utimesSync, writeFileSync } from "node:fs";
import { tmpdir } from "node:os";
import { join } from "node:path";
import { fileURLToPath } from "node:url";
import { buildSession } from "./refresh.mjs";

const session = buildSession({
  id: "thread-1",
  timestamp: "2026-09-23T17:00:00.000Z",
}, [120, 345], new Map([["thread-1", "Example session"]]));

assert.deepEqual(session, {
  codex_thread_id: "thread-1",
  date: "2026-09-24",
  created_at: "2026-09-23T17:00:00.000Z",
  thread_title: "Example session",
  category: null,
  token_count: 345,
});

assert.equal(buildSession({ id: "thread-2", timestamp: "2026-09-24T00:00:00Z" }, [], new Map()).token_count, null);

const tempBase = process.env.CODEX_SESSION_TIMELINE_TEST_TMP || tmpdir();
mkdirSync(tempBase, { recursive: true });
const tempRoot = mkdtempSync(join(tempBase, "codex-session-timeline-"));
try {
  const codexHome = join(tempRoot, "codex-home");
  const dayDir = join(codexHome, "sessions", "2026", "09", "24");
  const outputDir = join(tempRoot, "output");
  const rolloutPath = join(dayDir, "rollout-example.jsonl");
  mkdirSync(dayDir, { recursive: true });
  writeFileSync(join(codexHome, "session_index.jsonl"), `${JSON.stringify({ id: "thread-1", thread_name: "Example session" })}\n`);
  writeFileSync(rolloutPath, [
    JSON.stringify({ timestamp: "2026-09-23T17:00:00.000Z", type: "session_meta", payload: { id: "thread-1", timestamp: "2026-09-23T17:00:00.000Z" } }),
    JSON.stringify({ timestamp: "2026-09-23T17:10:00.000Z", type: "event_msg", payload: { type: "token_count", info: { total_token_usage: { total_tokens: 120 } } } }),
    JSON.stringify({ timestamp: "2026-09-23T17:20:00.000Z", type: "event_msg", payload: { type: "token_count", info: { total_token_usage: { total_tokens: 345 } } } }),
  ].join("\n"));

  const scriptPath = fileURLToPath(new URL("./refresh.mjs", import.meta.url));
  const result = spawnSync(process.execPath, [scriptPath, "--date", "2026-09-24"], {
    encoding: "utf8",
    env: { ...process.env, CODEX_HOME: codexHome, CODEX_SESSION_TIMELINE_DIR: outputDir },
  });
  assert.equal(result.status, 0, result.stderr || result.stdout);
  const index = JSON.parse(readFileSync(join(outputDir, "sessions.json"), "utf8"));
  assert.equal(index.sessions.length, 1);
  assert.equal(index.sessions[0].thread_title, "Example session");
  assert.equal(index.sessions[0].date, "2026-09-24");
  assert.equal(index.sessions[0].token_count, 345);
  assert.equal(Object.keys(index.source_cache).length, 1);
  assert.ok(!JSON.stringify(index).includes(codexHome));
  const page = readFileSync(join(outputDir, "2026-09-24.html"), "utf8");
  assert.ok(page.includes('const snapshotDefaultDate = "2026-09-24";'));
  assert.ok(!page.includes("source_cache"));

  const cacheKey = Object.keys(index.source_cache)[0];
  const cachedSource = index.source_cache[cacheKey];
  writeFileSync(rolloutPath, "x".repeat(statSync(rolloutPath).size));
  utimesSync(rolloutPath, cachedSource.mtime_ms / 1000, cachedSource.mtime_ms / 1000);
  assert.equal(statSync(rolloutPath).size, cachedSource.size);
  index.source_cache[cacheKey].mtime_ms = statSync(rolloutPath).mtimeMs;
  writeFileSync(join(outputDir, "sessions.json"), JSON.stringify(index));
  const cachedRun = spawnSync(process.execPath, [scriptPath, "--date", "2026-09-24"], {
    encoding: "utf8",
    env: { ...process.env, CODEX_HOME: codexHome, CODEX_SESSION_TIMELINE_DIR: outputDir },
  });
  assert.equal(cachedRun.status, 0, cachedRun.stderr || cachedRun.stdout);
} finally {
  rmSync(tempRoot, { recursive: true, force: true });
}

console.log("refresh checks passed");
