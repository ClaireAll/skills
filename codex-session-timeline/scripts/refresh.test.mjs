import assert from "node:assert/strict";
import { spawnSync } from "node:child_process";
import { mkdtempSync, mkdirSync, readFileSync, rmSync, statSync, utimesSync, writeFileSync } from "node:fs";
import { tmpdir } from "node:os";
import { join } from "node:path";
import { fileURLToPath } from "node:url";
const tempBase = process.env.CODEX_SESSION_TIMELINE_TEST_TMP || tmpdir();
mkdirSync(tempBase, { recursive: true });
const tempRoot = mkdtempSync(join(tempBase, "codex-session-timeline-"));
try {
  const codexHome = join(tempRoot, "codex-home");
  const dayDir = join(codexHome, "sessions", "2026", "09", "24");
  const archivedDir = join(codexHome, "archived_sessions", "2026", "09", "25");
  const outputDir = join(tempRoot, "output");
  const summariesPath = join(tempRoot, "summaries.json");
  const recordsPath = join(tempRoot, "stored-report.json");
  const rolloutPath = join(dayDir, "rollout-example.jsonl");
  const continuationPath = join(dayDir, "rollout-continuation.jsonl");
  const workerPath = join(dayDir, "rollout-worker.jsonl");
  const archivedPath = join(archivedDir, "rollout-archived.jsonl");
  mkdirSync(dayDir, { recursive: true });
  mkdirSync(archivedDir, { recursive: true });
  writeFileSync(summariesPath, JSON.stringify({ "thread-1": "修复分类赋值校验并补充 BDD 用例" }));
  writeFileSync(rolloutPath, [
    JSON.stringify({ timestamp: "2026-09-23T15:00:00.000Z", ordinal: 0, type: "session_meta", payload: { session_id: "thread-1", id: "thread-1", timestamp: "2026-09-23T15:00:00.000Z" } }),
    JSON.stringify({ type: "response_item", payload: { type: "message", role: "user", content: [{ type: "input_text", text: "<recommended_plugins>ignored context</recommended_plugins>\n# AGENTS.md instructions\n## My request:\n请修复分类赋值错误" }] } }),
    JSON.stringify({ type: "response_item", payload: { type: "message", role: "developer", content: [{ type: "input_text", text: "internal context" }] } }),
    JSON.stringify({ type: "response_item", payload: { type: "message", role: "assistant", phase: "final_answer", content: [{ type: "output_text", text: "已修复分类赋值校验" }] } }),
    JSON.stringify({ timestamp: "2026-09-23T15:10:00.000Z", type: "event_msg", payload: { type: "token_count", info: { total_token_usage: { total_tokens: 50 } } } }),
    JSON.stringify({ timestamp: "2026-09-23T15:59:00.000Z", type: "event_msg", payload: { type: "token_count", info: { total_token_usage: { total_tokens: 80 } } } }),
    JSON.stringify({ timestamp: "2026-09-23T16:01:00.000Z", type: "event_msg", payload: { type: "token_count", info: { total_token_usage: { total_tokens: 110 }, last_token_usage: { total_tokens: 30 } } } }),
    JSON.stringify({ timestamp: "2026-09-23T17:10:00.000Z", type: "event_msg", payload: { type: "token_count", info: { total_token_usage: { total_tokens: 120 }, last_token_usage: { total_tokens: 10 } } } }),
    JSON.stringify({ timestamp: "2026-09-23T17:20:00.000Z", type: "event_msg", payload: { type: "token_count", info: { total_token_usage: { total_tokens: 345 }, last_token_usage: { total_tokens: 225 } } } }),
  ].join("\n"));
  writeFileSync(continuationPath, [
    JSON.stringify({ timestamp: "2026-09-23T17:20:00.000Z", ordinal: 0, type: "session_meta", payload: { session_id: "thread-1", id: "thread-1", timestamp: "2026-09-23T15:00:00.000Z" } }),
    JSON.stringify({ timestamp: "2026-09-23T17:20:00.000Z", type: "event_msg", payload: { type: "token_count", info: { total_token_usage: { total_tokens: 345 }, last_token_usage: { total_tokens: 225 } } } }),
    JSON.stringify({ timestamp: "2026-09-23T17:30:00.000Z", type: "event_msg", payload: { type: "token_count", info: { total_token_usage: { total_tokens: 400 }, last_token_usage: { total_tokens: 55 } } } }),
  ].join("\n"));
  writeFileSync(workerPath, [
    JSON.stringify({ timestamp: "2026-09-24T00:30:00.000Z", ordinal: 0, type: "session_meta", payload: { session_id: "thread-1", id: "worker-1", timestamp: "2026-09-24T00:30:00.000Z" } }),
    JSON.stringify({ timestamp: "2026-09-24T00:35:00.000Z", type: "event_msg", payload: { type: "token_count", info: { total_token_usage: { total_tokens: 200 } } } }),
    JSON.stringify({ timestamp: "2026-09-24T00:40:00.000Z", type: "event_msg", payload: { type: "token_count", info: { total_token_usage: { total_tokens: 260 } } } }),
  ].join("\n"));
  writeFileSync(archivedPath, [
    JSON.stringify({ timestamp: "2026-09-24T16:10:00.000Z", ordinal: 0, type: "session_meta", payload: { session_id: "archived-thread", id: "archived-thread", timestamp: "2026-09-24T16:10:00.000Z" } }),
    JSON.stringify({ timestamp: "2026-09-24T16:11:00.000Z", type: "event_msg", payload: { type: "token_count", info: { last_token_usage: { total_tokens: 7 } } } }),
  ].join("\n"));

  const scriptPath = fileURLToPath(new URL("./refresh.mjs", import.meta.url));
  const result = spawnSync(process.execPath, [scriptPath, "--date", "2026-09-24", "--summaries", summariesPath], {
    encoding: "utf8",
    env: { ...process.env, CODEX_HOME: codexHome, CODEX_SESSION_TIMELINE_DIR: outputDir },
  });
  assert.equal(result.status, 0, result.stderr || result.stdout);
  const index = JSON.parse(readFileSync(join(outputDir, "sessions.json"), "utf8"));
  const yesterday = index.sessions.filter((session) => session.date === "2026-09-23");
  const today = index.sessions.filter((session) => session.date === "2026-09-24");
  assert.equal(yesterday.length, 1);
  assert.equal(yesterday[0].token_count, 80);
  assert.equal(today.length, 1);
  assert.equal(today[0].token_count, 580);
  assert.equal(today[0].summary, "修复分类赋值校验并补充 BDD 用例");
  assert.ok(index.sessions.every((session) => !("thread_title" in session)));
  assert.equal(Object.keys(index.source_cache).length, 4);
  assert.ok(index.source_cache[Object.keys(index.source_cache)[0]].usage_snapshots.length > 0);
  assert.ok(!JSON.stringify(index).includes(codexHome));
  const page = readFileSync(join(outputDir, "2026-09-24.html"), "utf8");
  assert.ok(page.includes('const snapshotDefaultDate = "2026-09-24";'));
  assert.ok(page.includes("修复分类赋值校验并补充 BDD 用例"));
  assert.ok(!page.includes("source_cache"));

  const extractPath = fileURLToPath(new URL("./extract-session-context.mjs", import.meta.url));
  const extracted = spawnSync(process.execPath, [extractPath, "--date", "2026-09-24"], {
    encoding: "utf8",
    env: { ...process.env, CODEX_HOME: codexHome, CODEX_SESSION_TIMELINE_DIR: outputDir },
  });
  assert.equal(extracted.status, 0, extracted.stderr || extracted.stdout);
  const context = JSON.parse(extracted.stdout);
  assert.deepEqual(context.sessions[0].user_messages, ["请修复分类赋值错误"]);
  assert.deepEqual(context.sessions[0].final_answers, ["已修复分类赋值校验"]);
  assert.ok(!extracted.stdout.includes("internal context"));

  const cacheKey = Object.keys(index.source_cache).find((path) => path.endsWith("rollout-example.jsonl"));
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
  const cachedIndex = JSON.parse(readFileSync(join(outputDir, "sessions.json"), "utf8"));
  assert.equal(cachedIndex.sessions.find((session) => session.date === "2026-09-24").summary, "修复分类赋值校验并补充 BDD 用例");

  writeFileSync(recordsPath, JSON.stringify([
    { codex_thread_id: "stored-1", created_at: "2026-09-24T01:00:00.000Z", summary: "从已保存日报导入", token_count: 700 },
    { codex_thread_id: "stored-2", created_at: "2026-09-24T02:00:00.000Z", summary: "核对历史会话", token_count: 300 },
  ]));
  const importedRun = spawnSync(process.execPath, [scriptPath, "--date", "2026-09-24", "--records", recordsPath], {
    encoding: "utf8",
    env: { ...process.env, CODEX_HOME: codexHome, CODEX_SESSION_TIMELINE_DIR: outputDir },
  });
  assert.equal(importedRun.status, 0, importedRun.stderr || importedRun.stdout);
  const importedIndex = JSON.parse(readFileSync(join(outputDir, "sessions.json"), "utf8"));
  const importedDay = importedIndex.sessions.filter((session) => session.date === "2026-09-24");
  assert.deepEqual(importedDay.map((session) => session.codex_thread_id), ["stored-1", "stored-2"]);
  assert.equal(importedDay.reduce((sum, session) => sum + session.token_count, 0), 1000);
  assert.ok(importedIndex.authoritative_dates.includes("2026-09-24"));

  const laterRun = spawnSync(process.execPath, [scriptPath, "--date", "2026-09-23"], {
    encoding: "utf8",
    env: { ...process.env, CODEX_HOME: codexHome, CODEX_SESSION_TIMELINE_DIR: outputDir },
  });
  assert.equal(laterRun.status, 0, laterRun.stderr || laterRun.stdout);
  const laterIndex = JSON.parse(readFileSync(join(outputDir, "sessions.json"), "utf8"));
  assert.equal(laterIndex.sessions.filter((session) => session.date === "2026-09-24").length, 2);
} finally {
  rmSync(tempRoot, { recursive: true, force: true });
}

console.log("refresh checks passed");
