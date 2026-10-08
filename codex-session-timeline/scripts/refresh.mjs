import { createReadStream, existsSync, mkdirSync, readFileSync, readdirSync, renameSync, statSync, writeFileSync } from "node:fs";
import { homedir } from "node:os";
import { dirname, join, relative, resolve } from "node:path";
import { createInterface } from "node:readline";
import { fileURLToPath } from "node:url";

const skillDir = dirname(dirname(fileURLToPath(import.meta.url)));
const codexHome = process.env.CODEX_HOME || join(homedir(), ".codex");
const sessionRoots = [join(codexHome, "sessions"), join(codexHome, "archived_sessions")];
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

function topLevelType(line) {
  return /"type"\s*:\s*"([^"]+)"/.exec(line)?.[1] || "";
}

function readSessionMetadata(line) {
  try {
    const entry = JSON.parse(line);
    const payload = entry.payload || {};
    return {
      id: payload.id || "",
      session_id: payload.session_id || payload.id || "",
      timestamp: entry.timestamp || payload.timestamp || "",
    };
  } catch {
    return { id: "", session_id: "", timestamp: "" };
  }
}

function tokenValue(usage) {
  if (Number.isSafeInteger(usage?.total_tokens) && usage.total_tokens >= 0) return usage.total_tokens;
  if (Number.isSafeInteger(usage?.input_tokens) && usage.input_tokens >= 0
    && Number.isSafeInteger(usage?.output_tokens) && usage.output_tokens >= 0) {
    return usage.input_tokens + usage.output_tokens;
  }
  return null;
}

function readUsageSnapshot(line) {
  try {
    const entry = JSON.parse(line);
    const info = entry.payload?.info;
    const timestamp = entry.timestamp;
    if (!timestamp || !Number.isFinite(Date.parse(timestamp))) return null;
    return {
      timestamp,
      total_tokens: tokenValue(info?.total_token_usage),
      last_tokens: tokenValue(info?.last_token_usage),
    };
  } catch {
    // Ignore malformed or incomplete usage lines.
  }
  return null;
}

function buildDailySessions(rollouts, summaries, previousSummaryById) {
  const threads = new Map();
  for (const rollout of rollouts) {
    let thread = threads.get(rollout.codex_thread_id);
    if (!thread) {
      thread = { id: rollout.codex_thread_id, created_at: rollout.created_at, root_created_at: "", rolloutStartDates: new Map(), snapshots: [] };
      threads.set(thread.id, thread);
    } else if (rollout.created_at < thread.created_at) {
      thread.created_at = rollout.created_at;
    }
    if (rollout.rollout_id === rollout.codex_thread_id
      && (!thread.root_created_at || rollout.created_at < thread.root_created_at)) {
      thread.root_created_at = rollout.created_at;
    }
    if (!thread.rolloutStartDates.has(rollout.rollout_id)
      || rollout.created_at < thread.rolloutStartDates.get(rollout.rollout_id)) {
      thread.rolloutStartDates.set(rollout.rollout_id, dateInShanghai(rollout.created_at));
    }
    thread.snapshots.push(...rollout.usage_snapshots.map((snapshot) => ({ ...snapshot, rollout_id: rollout.rollout_id })));
  }

  const sessions = [];
  for (const thread of threads.values()) {
    if (thread.root_created_at) thread.created_at = thread.root_created_at;
    const startDate = dateInShanghai(thread.created_at);
    const snapshots = [...new Map(thread.snapshots.map((snapshot) => [
      `${snapshot.rollout_id}|${snapshot.timestamp}|${snapshot.total_tokens ?? ""}|${snapshot.last_tokens ?? ""}`,
      snapshot,
    ])).values()].sort((a, b) => a.timestamp.localeCompare(b.timestamp));
    const daily = new Map();
    const previousTotals = new Map();
    for (const snapshot of snapshots) {
      const date = dateInShanghai(snapshot.timestamp);
      if (!date) continue;
      let day = daily.get(date);
      if (!day) {
        day = { first_at: snapshot.timestamp, total: 0, has_usage: false, unknown: false };
        daily.set(date, day);
      }
      if (snapshot.timestamp < day.first_at) day.first_at = snapshot.timestamp;

      if (snapshot.last_tokens !== null) {
        day.total += snapshot.last_tokens;
        day.has_usage = true;
      } else if (snapshot.total_tokens !== null) {
        const previousTotal = previousTotals.get(snapshot.rollout_id);
        if (previousTotal !== undefined && snapshot.total_tokens >= previousTotal) {
          day.total += snapshot.total_tokens - previousTotal;
          day.has_usage = true;
        } else if (previousTotal === undefined && date === thread.rolloutStartDates.get(snapshot.rollout_id)) {
          day.total += snapshot.total_tokens;
          day.has_usage = true;
        } else {
          day.unknown = true;
        }
        previousTotals.set(snapshot.rollout_id, snapshot.total_tokens);
      } else {
        day.unknown = true;
      }
    }

    if (startDate && !daily.has(startDate)) {
      daily.set(startDate, { first_at: thread.created_at, total: 0, has_usage: false, unknown: false });
    }
    for (const [date, day] of daily) {
      sessions.push({
        codex_thread_id: thread.id,
        date,
        created_at: date === startDate ? thread.created_at : day.first_at,
        summary: summaries[thread.id]?.trim() || previousSummaryById.get(thread.id) || "",
        category: null,
        token_count: day.unknown || !day.has_usage ? null : day.total,
      });
    }
  }
  return sessions;
}

function readImportedSessions(path, date) {
  const entries = JSON.parse(readFileSync(path, "utf8"));
  if (!Array.isArray(entries) || entries.length === 0) {
    throw new Error("--records 文件必须是非空会话数组");
  }
  const ids = new Set();
  return entries.map((entry) => {
    const id = typeof entry?.codex_thread_id === "string" ? entry.codex_thread_id.trim() : "";
    const createdAt = typeof entry?.created_at === "string" ? entry.created_at : "";
    const tokens = entry?.token_count;
    if (!id || ids.has(id) || dateInShanghai(createdAt) !== date
      || !(tokens === null || (Number.isSafeInteger(tokens) && tokens >= 0))) {
      throw new Error("--records 中的会话 ID、日期或 Token 数无效，或会话 ID 重复");
    }
    ids.add(id);
    return {
      codex_thread_id: id,
      date,
      created_at: createdAt,
      summary: typeof entry.summary === "string" ? entry.summary.trim() : "",
      category: null,
      token_count: tokens,
    };
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

async function readRollout(path) {
  const metadata = { id: "", session_id: "", timestamp: "" };
  const usageSnapshots = [];
  const input = createInterface({ input: createReadStream(path), crlfDelay: Infinity });
  for await (const line of input) {
    const type = topLevelType(line);
    if (type === "session_meta" && !metadata.id) {
      Object.assign(metadata, readSessionMetadata(line));
    } else if (type === "event_msg" && /"payload"\s*:\s*\{\s*"type"\s*:\s*"token_count"/.test(line)) {
      const usage = readUsageSnapshot(line);
      if (usage) usageSnapshots.push(usage);
    }
  }

  if (!metadata.id || !metadata.timestamp) return null;
  const session = {
    codex_thread_id: metadata.session_id,
    rollout_id: metadata.id,
    created_at: metadata.timestamp,
    usage_snapshots: usageSnapshots,
  };
  return dateInShanghai(session.created_at) ? session : null;
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
  const summaryIndex = process.argv.indexOf("--summaries");
  const summaryPath = summaryIndex < 0 ? "" : process.argv[summaryIndex + 1] || "";
  const recordsIndex = process.argv.indexOf("--records");
  const recordsPath = recordsIndex < 0 ? "" : process.argv[recordsIndex + 1] || "";
  if (recordsPath && !snapshotDate) throw new Error("--records 必须与 --date 一起使用");
  if (!sessionRoots.some(existsSync)) throw new Error(`找不到 Codex 会话目录：${codexHome}`);

  let summaries = {};
  if (summaryPath) summaries = JSON.parse(readFileSync(summaryPath, "utf8"));
  if (!summaries || typeof summaries !== "object" || Array.isArray(summaries)) {
    throw new Error("--summaries 文件必须是以会话 ID 为键、摘要文本为值的 JSON 对象");
  }
  const previousIndex = readPreviousIndex();
  const previousSummaryById = new Map(previousIndex.sessions
    .filter((session) => session.codex_thread_id && typeof session.summary === "string" && session.summary)
    .map((session) => [session.codex_thread_id, session.summary]));
  const previousSources = previousIndex.source_cache || {};
  const sourceCache = {};
  const rollouts = [];
  let failedFiles = 0;
  for (const path of sessionRoots.flatMap((root) => existsSync(root) ? listRollouts(root) : [])) {
    try {
      const stats = statSync(path);
      const sourcePath = relative(codexHome, path).replaceAll("\\", "/");
      const cached = previousSources[sourcePath];
      if (cached?.size === stats.size && cached?.mtime_ms === stats.mtimeMs
        && cached.session_id && cached.rollout_id && cached.created_at && Array.isArray(cached.usage_snapshots)) {
        rollouts.push({
          codex_thread_id: cached.session_id,
          rollout_id: cached.rollout_id,
          created_at: cached.created_at,
          usage_snapshots: cached.usage_snapshots,
        });
        sourceCache[sourcePath] = cached;
        continue;
      }

      const rollout = await readRollout(path);
      if (rollout) {
        rollouts.push(rollout);
        sourceCache[sourcePath] = {
          size: stats.size,
          mtime_ms: stats.mtimeMs,
          session_id: rollout.codex_thread_id,
          rollout_id: rollout.rollout_id,
          created_at: rollout.created_at,
          usage_snapshots: rollout.usage_snapshots,
        };
      }
    } catch {
      failedFiles += 1;
    }
  }
  if (!rollouts.length) throw new Error("没有找到可读取的 Codex 会话记录；现有页面和 JSON 未更改");

  const generatedSessions = buildDailySessions(rollouts, summaries, previousSummaryById);
  const authoritativeDates = new Set(Array.isArray(previousIndex.authoritative_dates) ? previousIndex.authoritative_dates : []);
  const authoritativeSessions = previousIndex.sessions.filter((session) => authoritativeDates.has(session.date));
  if (recordsPath) {
    authoritativeDates.add(snapshotDate);
    for (let index = authoritativeSessions.length - 1; index >= 0; index -= 1) {
      if (authoritativeSessions[index].date === snapshotDate) authoritativeSessions.splice(index, 1);
    }
    authoritativeSessions.push(...readImportedSessions(recordsPath, snapshotDate));
  }
  const sessions = generatedSessions.filter((session) => !authoritativeDates.has(session.date));
  sessions.push(...authoritativeSessions);
  sessions.sort((a, b) => a.created_at.localeCompare(b.created_at) || a.codex_thread_id.localeCompare(b.codex_thread_id));
  const index = { schema_version: 6, updated_at: new Date().toISOString(), sessions, source_cache: sourceCache, authoritative_dates: [...authoritativeDates].sort() };
  const pageIndex = { schema_version: index.schema_version, updated_at: index.updated_at, sessions };
  const template = readFileSync(join(skillDir, "assets", "index.html"), "utf8");
  if (!template.includes("__SESSION_INDEX_JSON__") || !template.includes("__DEFAULT_DATE__")) {
    throw new Error("HTML 模板缺少索引或日期占位符；现有页面和 JSON 未更改");
  }

  mkdirSync(outputDir, { recursive: true });
  writeAtomically(indexPath, JSON.stringify(index));
  writeAtomically(htmlPath, renderHtml(template, pageIndex));
  console.log(`已读取 ${sessions.length} 条本地会话日记录。`);
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
