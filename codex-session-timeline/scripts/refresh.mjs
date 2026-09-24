import { existsSync, mkdirSync, readFileSync, renameSync, writeFileSync } from "node:fs";
import { dirname, join } from "node:path";
import { fileURLToPath } from "node:url";

const skillDir = dirname(dirname(fileURLToPath(import.meta.url)));
const outputDir = process.env.CODEX_SESSION_TIMELINE_DIR || "D:\\Claire\\codex-session-timeline";
const envPath = process.env.CODEX_SESSION_TIMELINE_ENV || "D:\\Claire\\storage\\.env.local";
const indexPath = join(outputDir, "sessions.json");
const htmlPath = join(outputDir, "index.html");
const fields = "codex_thread_id,date,created_at,thread_title,category,token_count";
const pageSize = 1000;

function loadEnv() {
  if (!existsSync(envPath)) throw new Error(`找不到日报数据库配置：${envPath}`);
  for (const line of readFileSync(envPath, "utf8").split(/\r?\n/)) {
    const match = line.match(/^\s*(?:export\s+)?([A-Za-z0-9_]+)\s*=\s*(.*)\s*$/);
    if (!match || process.env[match[1]]) continue;
    let value = match[2].trim();
    if (value.length > 1 && ((value[0] === '"' && value.at(-1) === '"') || (value[0] === "'" && value.at(-1) === "'"))) {
      value = value.slice(1, -1);
    }
    process.env[match[1]] = value;
  }
}

function getDatabaseConfig() {
  const baseUrl = process.env.NEXT_PUBLIC_SUPABASE_URL?.trim().replace(/\/+$/, "");
  const apiKey = process.env.SUPABASE_SERVICE_ROLE_KEY?.trim();
  if (!baseUrl || !apiKey) throw new Error("日报数据库配置缺少 Supabase URL 或服务密钥");
  return { apiKey, baseUrl, userId: process.env.CODEX_DAILY_USER_ID?.trim() };
}

async function queryRest(config, table, params, range) {
  const url = new URL(`${config.baseUrl}/rest/v1/${table}`);
  for (const [key, value] of Object.entries(params)) url.searchParams.set(key, value);
  const response = await fetch(url, {
    headers: {
      apikey: config.apiKey,
      Authorization: `Bearer ${config.apiKey}`,
      ...(range ? { "Range-Unit": "items", Range: range } : {}),
    },
  });
  if (!response.ok) throw new Error(`读取日报元数据失败（HTTP ${response.status}）`);
  return response.json();
}

async function getUserId(config) {
  if (config.userId) return config.userId;
  const users = await queryRest(config, "users", { select: "id", limit: "2" });
  if (users.length !== 1 || !users[0]?.id) throw new Error("无法唯一确认日报用户，请配置 CODEX_DAILY_USER_ID");
  return users[0].id;
}

async function readSessions(config, userId) {
  const sessions = [];
  for (let offset = 0; ; offset += pageSize) {
    const rows = await queryRest(config, "codex_log", {
      select: fields,
      id: `eq.${userId}`,
      order: "date.asc,created_at.asc",
    }, `${offset}-${offset + pageSize - 1}`);
    for (const row of rows) {
      if (!/^\d{4}-\d{2}-\d{2}$/.test(row.date || "") || /^Automation:/i.test(row.thread_title || "")) continue;
      const tokenCount = row.token_count == null ? null : Number(row.token_count);
      sessions.push({
        codex_thread_id: row.codex_thread_id || "",
        date: row.date,
        created_at: row.created_at,
        thread_title: row.thread_title || "未命名会话",
        category: Number.isInteger(Number(row.category)) ? Number(row.category) : 10000,
        token_count: Number.isFinite(tokenCount) && tokenCount >= 0 ? tokenCount : null,
      });
    }
    if (rows.length < pageSize) break;
  }
  return sessions;
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

async function refresh() {
  const dateIndex = process.argv.indexOf("--date");
  const snapshotDate = dateIndex >= 0 ? process.argv[dateIndex + 1] : "";
  const snapshotTimestamp = snapshotDate ? Date.parse(`${snapshotDate}T00:00:00Z`) : NaN;
  if (snapshotDate && (!/^\d{4}-\d{2}-\d{2}$/.test(snapshotDate)
    || !Number.isFinite(snapshotTimestamp)
    || new Date(snapshotTimestamp).toISOString().slice(0, 10) !== snapshotDate)) {
    throw new Error("--date 必须使用 YYYY-MM-DD");
  }

  loadEnv();
  const config = getDatabaseConfig();
  const userId = await getUserId(config);
  const sessions = await readSessions(config, userId);
  const index = { schema_version: 2, updated_at: new Date().toISOString(), sessions };
  const template = readFileSync(join(skillDir, "assets", "index.html"), "utf8");
  if (!template.includes("__SESSION_INDEX_JSON__") || !template.includes("__DEFAULT_DATE__")) {
    throw new Error("HTML 模板缺少索引或日期占位符");
  }

  mkdirSync(outputDir, { recursive: true });
  writeAtomically(indexPath, JSON.stringify(index));
  writeAtomically(htmlPath, renderHtml(template, index));
  console.log(`索引已更新：${sessions.length} 条日报会话记录。`);
  console.log(`JSON：${indexPath}`);
  console.log(`HTML：${htmlPath}`);

  if (snapshotDate) {
    const snapshotPath = join(outputDir, `${snapshotDate}.html`);
    writeAtomically(snapshotPath, renderHtml(template, index, snapshotDate));
    console.log(`日期页面：${snapshotPath}`);
  }
}

refresh().catch((error) => {
  console.error(error instanceof Error ? error.message : error);
  process.exitCode = 1;
});
