import { createReadStream, readFileSync } from "node:fs";
import { homedir } from "node:os";
import { join } from "node:path";
import { createInterface } from "node:readline";

const codexHome = process.env.CODEX_HOME || join(homedir(), ".codex");
const outputDir = process.env.CODEX_SESSION_TIMELINE_DIR || join(codexHome, "codex-session-timeline");

function dateInShanghai(timestamp) {
  const date = new Date(timestamp);
  if (!Number.isFinite(date.getTime())) return "";
  return new Intl.DateTimeFormat("en-CA", {
    timeZone: "Asia/Shanghai",
    year: "numeric",
    month: "2-digit",
    day: "2-digit",
  }).format(date);
}

function requestedDate(args) {
  const index = args.indexOf("--date");
  const date = index < 0 ? "" : args[index + 1] || "";
  if (!/^\d{4}-\d{2}-\d{2}$/.test(date)) throw new Error("用法：node extract-session-context.mjs --date YYYY-MM-DD");
  return date;
}

function messageText(content) {
  return (content || [])
    .filter((item) => item && ["input_text", "output_text"].includes(item.type) && typeof item.text === "string")
    .map((item) => item.text.trim())
    .filter(Boolean)
    .join("\n");
}

function clipped(text, limit) {
  return text.length > limit ? `${text.slice(0, limit)}…[已截短]` : text;
}

function cleanUserText(text) {
  const requestMarker = "## My request:";
  const requestIndex = text.indexOf(requestMarker);
  if (requestIndex >= 0) return text.slice(requestIndex + requestMarker.length).trim();
  if (/<recommended_plugins>|# AGENTS\.md instructions|<environment_context>/.test(text)) return "";
  return text.trim();
}

async function extract(path, messages, date) {
  const input = createInterface({ input: createReadStream(path), crlfDelay: Infinity });
  for await (const line of input) {
    let entry;
    try { entry = JSON.parse(line); } catch { continue; }
    if (dateInShanghai(entry.timestamp) !== date) continue;
    const payload = entry.type === "response_item" ? entry.payload : null;
    if (payload?.type !== "message") continue;
    if (payload.role !== "user" && !(payload.role === "assistant" && payload.phase === "final_answer")) continue;
    let text = messageText(payload.content);
    if (payload.role === "user") text = cleanUserText(text);
    if (text) messages[payload.role === "user" ? "user" : "assistant"].add(text);
  }
}

async function main() {
  const date = requestedDate(process.argv.slice(2));
  const index = JSON.parse(readFileSync(join(outputDir, "sessions.json"), "utf8"));
  const selected = new Map();
  for (const session of index.sessions) {
    if (session.date === date && session.codex_thread_id && !selected.has(session.codex_thread_id)) {
      selected.set(session.codex_thread_id, { created_at: session.created_at, messages: { user: new Set(), assistant: new Set() } });
    }
  }
  const sources = Object.entries(index.source_cache || {})
    .filter(([relativePath, source]) => selected.has(source.session_id)
      && ((source.usage_snapshots || []).some((snapshot) => dateInShanghai(snapshot.timestamp) === date)
        || dateInShanghai(source.created_at) === date
        || relativePath.startsWith(`${date.replaceAll("-", "/")}/`)
        || relativePath.split("/").slice(1, 4).join("-") === date))
    .sort(([a], [b]) => a.localeCompare(b));
  for (const [relativePath, source] of sources) {
    const session = selected.get(source.session_id);
    const path = relativePath.startsWith("sessions/") || relativePath.startsWith("archived_sessions/")
      ? join(codexHome, relativePath)
      : join(codexHome, "sessions", relativePath);
    await extract(path, session.messages, date);
  }

  const result = [...selected].map(([id, session]) => {
    const user = [...session.messages.user];
    const assistant = [...session.messages.assistant];
    const recentUser = user.length > 6 ? [user[0], ...user.slice(-5)] : user;
    return {
      id,
      created_at: session.created_at,
      user_messages: recentUser.map((text) => clipped(text, 900)),
      final_answers: assistant.slice(-2).map((text) => clipped(text, 700)),
    };
  }).sort((a, b) => a.created_at.localeCompare(b.created_at));
  process.stdout.write(`${JSON.stringify({ date, sessions: result })}\n`);
}

main().catch((error) => {
  console.error(error instanceof Error ? error.message : error);
  process.exitCode = 1;
});
