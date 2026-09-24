import { createReadStream, existsSync, mkdirSync, readFileSync, readdirSync, renameSync, statSync, writeFileSync } from "node:fs";
import { homedir } from "node:os";
import { dirname, join, relative, resolve } from "node:path";
import { createInterface } from "node:readline";
import { fileURLToPath } from "node:url";

const skillDir = dirname(dirname(fileURLToPath(import.meta.url)));
const codexHome = process.env.CODEX_HOME || join(homedir(), ".codex");
const sessionsDir = join(codexHome, "sessions");
const outputDir = process.env.CODEX_SESSION_TIMELINE_DIR || join(codexHome, "codex-session-timeline");
const indexPath = join(outputDir, "sessions.json");
const htmlPath = join(outputDir, "index.html");

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

export function buildSession(metadata, usageSnapshots, titleById) {
  const id = metadata.id || metadata.session_id || "";
  const createdAt = metadata.timestamp || "";
  const tokenCount = [...usageSnapshots].reverse().find((value) => Number.isSafeInteger(value) && value >= 0);
  return {
    codex_thread_id: id,
    date: dateInShanghai(createdAt),
    created_at: createdAt,
    thread_title: titleById.get(id) || "未命名会话",
    category: null,
    token_count: tokenCount ?? null,
  };
}

function topLevelType(line) {
  const timestampFirst = /^\s*\{\s*"timestamp"\s*:\s*"(?:\\.|[^"\\])*"\s*,\s*"type"\s*:\s*"([^"]+)"/.exec(line);
  if (timestampFirst) return timestampFirst[1];
  return /^\s*\{\s*"type"\s*:\s*"([^"]+)"/.exec(line)?.[1] || "";
}

function readSessionMetadata(line) {
  const id = /"payload"\s*:\s*\{\s*"id"\s*:\s*"([^"]+)"/.exec(line)?.[1] || "";
  const timestamp = /^\s*\{\s*"timestamp"\s*:\s*"((?:\\.|[^"\\])*)"/.exec(line)?.[1] || "";
  return { id, timestamp };
}

function readUsage(line) {
  try {
    const usage = JSON.parse(line).payload?.info?.total_token_usage;
    if (Number.isSafeInteger(usage?.total_tokens) && usage.total_tokens >= 0) return usage.total_tokens;
    if (Number.isSafeInteger(usage?.input_tokens) && Number.isSafeInteger(usage?.output_tokens)) {
      return usage.input_tokens + usage.output_tokens;
    }
  } catch {
    // Ignore malformed or incomplete usage lines.
  }
  return null;
}

function readTitleIndex(path) {
  const titleById = new Map();
  if (!existsSync(path)) return titleById;
  const stream = createReadStream(path);
  const input = createInterface({ input: stream, crlfDelay: Infinity });
  return new Promise((resolvePromise, reject) => {
    input.on("line", (line) => {
      try {
        const entry = JSON.parse(line);
        if (entry.id && entry.thread_name) titleById.set(entry.id, entry.thread_name);
      } catch {
        // Keep other valid title-index entries when one line is malformed.
      }
    });
    input.on("close", () => resolvePromise(titleById));
    stream.on("error", reject);
  });
}

function listRollouts(directory) {
  const files = [];
  for (const entry of readdirSync(directory, { withFileTypes: true })) {
    const path = join(directory, entry.name);
    if (entry.isDirectory()) files.push(...listRollouts(path));
    else if (entry.isFile() && /^rollout-.*\.jsonl$/i.test(entry.name)) files.push(path);
  }
  return files;
}

function readPreviousIndex() {
  try {
    const index = JSON.parse(readFileSync(indexPath, "utf8"));
    if (Array.isArray(index.sessions)) return index;
  } catch {
    // Start a fresh local index when no usable cache exists.
  }
  return { sessions: [], source_cache: {} };
}

async function readRollout(path, titleById) {
  const metadata = { id: "", timestamp: "" };
  const usageSnapshots = [];
  const input = createInterface({ input: createReadStream(path), crlfDelay: Infinity });
  for await (const line of input) {
    const type = topLevelType(line);
    if (type === "session_meta" && !metadata.id) {
      Object.assign(metadata, readSessionMetadata(line));
    } else if (type === "event_msg" && /"payload"\s*:\s*\{\s*"type"\s*:\s*"token_count"/.test(line)) {
      const usage = readUsage(line);
      if (usage !== null) usageSnapshots.push(usage);
    }
  }

  if (!metadata.id || !metadata.timestamp) return null;
  const session = buildSession(metadata, usageSnapshots, titleById);
  return session.date ? session : null;
}

function writeAtomically(path, content) {
  const temporaryPath = `${path}.${process.pid}.tmp`;
  writeFileSync(temporaryPath, content, "utf8");
  renameSync(temporaryPath, path);
}

function renderHtml(template, index, defaultDate = "") {
  const embeddedIndex = JSON.stringify(index)
    .replaceAll("<", "\\u003c")
    .replaceAll(">", "\\u003e")
    .replaceAll("&", "\\u0026");
  return template
    .replace("__SESSION_INDEX_JSON__", embeddedIndex)
    .replace("__DEFAULT_DATE__", defaultDate);
}

function getRequestedDate(args) {
  const dateIndex = args.indexOf("--date");
  if (dateIndex < 0) return "";
  const value = args[dateIndex + 1] || "";
  const timestamp = Date.parse(`${value}T00:00:00Z`);
  if (!/^\d{4}-\d{2}-\d{2}$/.test(value)
    || !Number.isFinite(timestamp)
    || new Date(timestamp).toISOString().slice(0, 10) !== value) {
    throw new Error("--date 必须使用有效的 YYYY-MM-DD 日期");
  }
  return value;
}

async function refresh() {
  const snapshotDate = getRequestedDate(process.argv.slice(2));
  if (!existsSync(sessionsDir)) throw new Error(`找不到 Codex 会话目录：${sessionsDir}`);

  const titleById = await readTitleIndex(join(codexHome, "session_index.jsonl"));
  const previousIndex = readPreviousIndex();
  const previousSessions = new Map(previousIndex.sessions
    .filter((session) => session.codex_thread_id)
    .map((session) => [session.codex_thread_id, session]));
  const previousSources = previousIndex.source_cache || {};
  const sourceCache = {};
  const sessions = [];
  let failedFiles = 0;
  for (const path of listRollouts(sessionsDir)) {
    try {
      const stats = statSync(path);
      const sourcePath = relative(sessionsDir, path).replaceAll("\\", "/");
      const cached = previousSources[sourcePath];
      if (cached?.size === stats.size && cached?.mtime_ms === stats.mtimeMs) {
        const previous = previousSessions.get(cached.session_id);
        if (previous) {
          const session = {
            ...previous,
            thread_title: titleById.get(previous.codex_thread_id) || previous.thread_title,
          };
          if (session.date && session.created_at) {
            sessions.push(session);
            sourceCache[sourcePath] = cached;
            continue;
          }
        }
      }

      const session = await readRollout(path, titleById);
      if (session) {
        sessions.push(session);
        sourceCache[sourcePath] = { size: stats.size, mtime_ms: stats.mtimeMs, session_id: session.codex_thread_id };
      }
    } catch {
      failedFiles += 1;
    }
  }
  if (!sessions.length) throw new Error("没有找到可读取的 Codex 会话记录；现有页面和 JSON 未更改");

  sessions.sort((a, b) => a.created_at.localeCompare(b.created_at) || a.codex_thread_id.localeCompare(b.codex_thread_id));
  const index = { schema_version: 3, updated_at: new Date().toISOString(), sessions, source_cache: sourceCache };
  const pageIndex = { schema_version: index.schema_version, updated_at: index.updated_at, sessions };
  const template = readFileSync(join(skillDir, "assets", "index.html"), "utf8");
  if (!template.includes("__SESSION_INDEX_JSON__") || !template.includes("__DEFAULT_DATE__")) {
    throw new Error("HTML 模板缺少索引或日期占位符；现有页面和 JSON 未更改");
  }

  mkdirSync(outputDir, { recursive: true });
  writeAtomically(indexPath, JSON.stringify(index));
  writeAtomically(htmlPath, renderHtml(template, pageIndex));
  console.log(`已读取 ${sessions.length} 条本地会话记录。`);
  console.log(`JSON：${indexPath}`);
  console.log(`HTML：${htmlPath}`);
  if (failedFiles) console.warn(`有 ${failedFiles} 个会话文件无法读取，已跳过。`);

  if (snapshotDate) {
    const snapshotPath = join(outputDir, `${snapshotDate}.html`);
    writeAtomically(snapshotPath, renderHtml(template, pageIndex, snapshotDate));
    console.log(`日期页面：${snapshotPath}`);
  }
}

if (process.argv[1] && resolve(process.argv[1]) === fileURLToPath(import.meta.url)) {
  refresh().catch((error) => {
    console.error(error instanceof Error ? error.message : error);
    process.exitCode = 1;
  });
}
