from __future__ import annotations

import argparse
import http.server
import html
import json
import os
import pathlib
import re
import secrets
import socket
import subprocess
import sys
import time
import unicodedata
import webbrowser
from dataclasses import dataclass
from typing import Any, Iterable


SOURCE_EXTENSIONS = {
    ".cjs",
    ".cts",
    ".htm",
    ".html",
    ".js",
    ".jsx",
    ".mjs",
    ".mts",
    ".svelte",
    ".ts",
    ".tsx",
    ".vue",
}

EXCLUDED_DIR_NAMES = {
    ".git",
    ".next",
    "build",
    "coverage",
    "dist",
    "node_modules",
    "out",
}

EXCLUDED_FILE_NAMES = {
    "bun.lockb",
    "package-lock.json",
    "pnpm-lock.yaml",
    "yarn.lock",
}

IGNORED_KEY_PREFIXES = ("BI",)
DELETE_LOCALE_FILE_NAMES = ("zh_CN.json", "en_US.json", "zh_TW.json")

SKILL_DIR = pathlib.Path(__file__).resolve().parents[1]
DEFAULT_REPORT_PATH = SKILL_DIR / "i18n-helper-report.html"


@dataclass(frozen=True)
class I18nEntry:
    key: str
    value: Any


@dataclass(frozen=True)
class DynamicCall:
    path: str
    line: int
    snippet: str
    reason: str


@dataclass(frozen=True)
class DuplicateValueGroup:
    normalized_value: str
    sample_value: str
    keys: tuple[str, ...]


@dataclass(frozen=True)
class MissingUsedKey:
    key: str
    usage_count: int
    examples: tuple[str, ...]


@dataclass(frozen=True)
class AnalysisReport:
    project_root: pathlib.Path
    i18n_file: pathlib.Path
    patterns: tuple[str, ...]
    total_keys: int
    used_keys: frozenset[str]
    unused_keys: tuple[I18nEntry, ...]
    missing_used_keys: tuple[MissingUsedKey, ...]
    duplicate_value_groups: tuple[DuplicateValueGroup, ...]
    dynamic_calls: tuple[DynamicCall, ...]
    scanned_files: int


@dataclass(frozen=True)
class ParsedArgument:
    static_keys: tuple[str, ...]
    reason: str | None


@dataclass(frozen=True)
class ReplacementResult:
    changed_files: int
    replaced_occurrences: int
    replaced_keys: tuple[str, ...] = ()


@dataclass(frozen=True)
class DeleteResult:
    deleted_keys: int
    deleted_entries: int
    changed_files: int
    changed_paths: tuple[pathlib.Path, ...]


def read_config(config_path: pathlib.Path) -> tuple[pathlib.Path, pathlib.Path, list[str]]:
    lines = config_path.read_text(encoding="utf-8-sig").splitlines()
    if len(lines) < 3:
        raise ValueError(f"{config_path} must contain project path, i18n JSON path, and regex patterns")

    project_root = pathlib.Path(_strip_optional_quotes(lines[0].strip()))
    i18n_file = pathlib.Path(_strip_optional_quotes(lines[1].strip()))
    patterns = json.loads(lines[2].strip())

    if not isinstance(patterns, list) or not all(isinstance(item, str) for item in patterns):
        raise ValueError("config line 3 must be a JSON array of regex strings")

    return project_root, i18n_file, patterns


def analyze_project(
    project_root: pathlib.Path,
    i18n_file: pathlib.Path,
    patterns: Iterable[str],
) -> AnalysisReport:
    project_root = project_root.resolve()
    i18n_path = i18n_file if i18n_file.is_absolute() else project_root / i18n_file
    i18n_path = i18n_path.resolve()
    pattern_list = tuple(patterns)
    compiled_patterns = tuple(re.compile(pattern) for pattern in pattern_list)

    entries = _load_i18n_entries(i18n_path)
    known_keys = frozenset(entry.key for entry in entries)
    used_keys: set[str] = set()
    used_key_counts: dict[str, int] = {}
    used_key_examples: dict[str, list[str]] = {}
    dynamic_calls: list[DynamicCall] = []
    seen_call_positions: set[tuple[pathlib.Path, int]] = set()
    scanned_files = 0

    def record_used(keys: Iterable[str], source_path: pathlib.Path, line: int | None = None) -> None:
        location = _relative_display_path(source_path, project_root)
        if line is not None:
            location = f"{location}:{line}"
        for key in keys:
            used_keys.add(key)
            used_key_counts[key] = used_key_counts.get(key, 0) + 1
            examples = used_key_examples.setdefault(key, [])
            if len(examples) < 3 and location not in examples:
                examples.append(location)

    for source_path in _iter_source_files(project_root, i18n_path):
        text = _read_text(source_path)
        scanned_files += 1
        record_used(_find_quoted_key_literals(text, known_keys), source_path)
        for pattern in compiled_patterns:
            for match in pattern.finditer(text):
                call_start = match.start()
                open_paren = text.find("(", call_start)
                seen_key = (source_path, open_paren if open_paren != -1 else call_start)
                if seen_key in seen_call_positions:
                    continue
                seen_call_positions.add(seen_key)

                line_number = text.count("\n", 0, call_start) + 1
                parsed = _parse_first_argument(text, call_start)
                if parsed.static_keys:
                    record_used(parsed.static_keys, source_path, line_number)
                    continue

                dynamic_calls.append(
                    DynamicCall(
                        path=_relative_display_path(source_path, project_root),
                        line=line_number,
                        snippet=_call_snippet(text, call_start),
                        reason=parsed.reason or "unable to parse first argument",
                    )
                )

    unused = tuple(entry for entry in entries if entry.key not in used_keys)
    used_entries = tuple(entry for entry in entries if entry.key in used_keys)
    missing_used = tuple(
        MissingUsedKey(
            key=key,
            usage_count=used_key_counts.get(key, 0),
            examples=tuple(used_key_examples.get(key, ())),
        )
        for key in sorted(used_keys)
        if key not in known_keys and not _is_ignored_key(key)
    )
    duplicates = _find_duplicate_value_groups(used_entries)

    return AnalysisReport(
        project_root=project_root,
        i18n_file=i18n_path,
        patterns=pattern_list,
        total_keys=len(entries),
        used_keys=frozenset(used_keys),
        unused_keys=unused,
        missing_used_keys=missing_used,
        duplicate_value_groups=duplicates,
        dynamic_calls=tuple(dynamic_calls),
        scanned_files=scanned_files,
    )


def replace_keys_in_project(
    project_root: pathlib.Path,
    i18n_file: pathlib.Path,
    replacements: dict[str, str],
) -> ReplacementResult:
    project_root = project_root.resolve()
    i18n_path = i18n_file if i18n_file.is_absolute() else project_root / i18n_file
    i18n_path = i18n_path.resolve()
    clean_replacements = _clean_replacement_map(replacements)
    if not clean_replacements:
        return ReplacementResult(changed_files=0, replaced_occurrences=0)

    changed_files = 0
    replaced_occurrences = 0
    replaced_keys: set[str] = set()
    for source_path in _iter_source_files(project_root, i18n_path):
        text, encoding = _read_text_with_encoding(source_path)
        updated, count, file_replaced_keys = _replace_key_literals_in_text(text, clean_replacements)
        if count == 0:
            continue
        _write_text_with_encoding(source_path, updated, encoding)
        changed_files += 1
        replaced_occurrences += count
        replaced_keys.update(file_replaced_keys)

    return ReplacementResult(
        changed_files=changed_files,
        replaced_occurrences=replaced_occurrences,
        replaced_keys=tuple(sorted(replaced_keys)),
    )


def filter_keys_safe_to_delete(
    project_root: pathlib.Path,
    i18n_file: pathlib.Path,
    patterns: Iterable[str],
    keys: Iterable[str],
) -> tuple[tuple[str, ...], tuple[str, ...]]:
    report = analyze_project(project_root, i18n_file, patterns)
    unique_keys = tuple(dict.fromkeys(keys))
    safe_keys = tuple(key for key in unique_keys if key not in report.used_keys)
    skipped_keys = tuple(key for key in unique_keys if key in report.used_keys)
    return safe_keys, skipped_keys


def _clean_replacement_map(replacements: dict[Any, Any]) -> dict[str, str]:
    return {
        source: target
        for source, target in replacements.items()
        if isinstance(source, str)
        and isinstance(target, str)
        and source
        and target
        and source != target
    }


def delete_keys_from_i18n_json(i18n_file: pathlib.Path, keys: Iterable[str]) -> DeleteResult:
    i18n_path = i18n_file.resolve()
    clean_keys = tuple(dict.fromkeys(key for key in keys if isinstance(key, str) and key))
    if not clean_keys:
        return DeleteResult(deleted_keys=0, deleted_entries=0, changed_files=0, changed_paths=())

    deleted_key_set: set[str] = set()
    deleted_entries = 0
    changed_paths: list[pathlib.Path] = []
    for locale_path in _iter_delete_locale_paths(i18n_path):
        if not locale_path.exists():
            continue
        data = json.loads(locale_path.read_text(encoding="utf-8-sig"))
        if not isinstance(data, dict):
            raise ValueError(f"{locale_path} root must be an object")

        file_deleted = 0
        for key in clean_keys:
            if _delete_i18n_key(data, key):
                file_deleted += 1
                deleted_key_set.add(key)

        if file_deleted:
            locale_path.write_text(
                json.dumps(data, ensure_ascii=False, indent=2) + "\n",
                encoding="utf-8",
            )
            deleted_entries += file_deleted
            changed_paths.append(locale_path)

    return DeleteResult(
        deleted_keys=len(deleted_key_set),
        deleted_entries=deleted_entries,
        changed_files=len(changed_paths),
        changed_paths=tuple(changed_paths),
    )


def _iter_delete_locale_paths(i18n_path: pathlib.Path) -> tuple[pathlib.Path, ...]:
    paths = [i18n_path.parent / file_name for file_name in DELETE_LOCALE_FILE_NAMES]
    if i18n_path.name not in DELETE_LOCALE_FILE_NAMES:
        paths.insert(0, i18n_path)
    return tuple(dict.fromkeys(path.resolve() for path in paths))


def _delete_i18n_key(data: dict[str, Any], key: str) -> bool:
    if key in data:
        del data[key]
        return True

    parts = key.split(".")
    current: Any = data
    for part in parts[:-1]:
        if not isinstance(current, dict) or part not in current:
            return False
        current = current[part]
    if isinstance(current, dict) and parts[-1] in current:
        del current[parts[-1]]
        return True
    return False


def render_html(
    report: AnalysisReport,
    api_endpoint: str | None = None,
    api_token: str | None = None,
) -> str:
    duplicate_rows = "\n".join(
        _duplicate_rows(group, group_index)
        for group_index, group in enumerate(report.duplicate_value_groups)
    )
    unused_rows = "\n".join(
        "<tr>"
        f'<td class="check-cell unused-check-cell"><input type="checkbox" data-role="unused-delete" '
        f'data-key="{_e(entry.key)}" aria-label="删除未使用 key {_e(entry.key)}"></td>'
        f"<td><code>{_e(entry.key)}</code></td>"
        f"<td>{_e(_display_value(entry.value))}</td>"
        "</tr>"
        for entry in report.unused_keys
    )
    missing_rows = "\n".join(
        "<tr>"
        f"<td><code>{_e(item.key)}</code></td>"
        f"<td>{item.usage_count}</td>"
        f"<td>{_e('; '.join(item.examples))}</td>"
        "</tr>"
        for item in report.missing_used_keys
    )
    api_base = _api_base_from_endpoint(api_endpoint)
    api_config = json.dumps({"base": api_base, "token": api_token}, ensure_ascii=False)

    if not unused_rows:
        unused_rows = '<tr><td colspan="3" class="empty">没有发现未使用 key。</td></tr>'
    if not missing_rows:
        missing_rows = '<tr><td colspan="3" class="empty">没有发现源码仍在使用但 JSON 缺失的 key。</td></tr>'
    if not duplicate_rows:
        duplicate_rows = '<tr><td colspan="5" class="empty">没有发现相同 value。</td></tr>'

    css = """
    :root { color-scheme: light; --ink: #1f2937; --muted: #667085; --line: #d9dee8; --bg: #f5f7fb; --panel: #ffffff; --stripe: #f8fafc; --accent: #1b6ca8; --warn: #9a5b13; }
    * { box-sizing: border-box; }
    body { margin: 0; background: var(--bg); color: var(--ink); font: 14px/1.5 "Segoe UI", Arial, sans-serif; }
    header { padding: 22px 28px 16px; border-bottom: 1px solid var(--line); background: var(--panel); }
    h1 { margin: 0; font-size: 22px; font-weight: 650; letter-spacing: 0; }
    h2 { margin: 28px 0 10px; font-size: 17px; font-weight: 650; letter-spacing: 0; }
    button { font: inherit; }
    button:focus-visible, input:focus-visible { outline: 2px solid var(--accent); outline-offset: 2px; }
    code { font-family: Consolas, "SFMono-Regular", Menlo, monospace; font-size: 13px; }
    main { max-width: 1440px; margin: 0 auto; padding: 0 24px 32px; }
    .meta { display: grid; grid-template-columns: repeat(5, minmax(120px, 1fr)); gap: 8px; margin-top: 12px; }
    .metric { border: 1px solid var(--line); background: #fbfcff; border-radius: 6px; padding: 10px 12px; min-width: 0; }
    .metric strong { display: block; font-size: 19px; line-height: 1.15; }
    .metric span, .pathline { color: var(--muted); font-size: 12px; overflow-wrap: anywhere; }
    .title-row { display: flex; align-items: center; justify-content: space-between; gap: 14px; flex-wrap: wrap; margin-bottom: 10px; }
    .header-actions { display: flex; align-items: center; justify-content: flex-end; gap: 10px; color: var(--muted); font-size: 12px; }
    .secondary-button { background: #fff; color: var(--accent); }
    .table-wrap { overflow: auto; border: 1px solid var(--line); background: var(--panel); border-radius: 6px; }
    table { width: 100%; border-collapse: collapse; table-layout: fixed; }
    th, td { border-bottom: 1px solid var(--line); padding: 8px 10px; vertical-align: top; text-align: left; overflow-wrap: anywhere; }
    th { position: sticky; top: 0; background: #eef3f8; color: #26364a; font-size: 12px; font-weight: 650; }
    tbody tr:nth-child(even) { background: var(--stripe); }
    tr:last-child td { border-bottom: 0; }
    .unused th:nth-child(1) { width: 72px; text-align: center; }
    .unused th:nth-child(2) { width: 36%; }
    .unused td:nth-child(1) { text-align: center; }
    .missing th:nth-child(1) { width: 42%; }
    .missing th:nth-child(2) { width: 110px; }
    .duplicate th:nth-child(1) { width: 34%; }
    .duplicate th:nth-child(2) { width: 80px; }
    .duplicate th:nth-child(3), .duplicate th:nth-child(5) { width: 72px; text-align: center; }
    .duplicate th:nth-child(4) { width: 42%; }
    .duplicate td:nth-child(3), .duplicate td:nth-child(5) { text-align: center; }
    .duplicate .merged { font-weight: 500; }
    .section-head { display: flex; align-items: flex-end; justify-content: space-between; gap: 16px; margin-top: 28px; }
    .section-head h2 { margin: 0 0 10px; }
    .action-panel { display: flex; align-items: center; justify-content: flex-end; gap: 10px; flex-wrap: wrap; margin-bottom: 8px; color: var(--muted); font-size: 12px; text-align: right; }
    .action-button { border: 1px solid #1b6ca8; background: #1b6ca8; color: #fff; border-radius: 6px; padding: 7px 12px; cursor: pointer; }
    .danger-button { border-color: #b42318; background: #b42318; }
    .action-button:disabled { border-color: #b7c0cc; background: #d8dee8; color: #617082; cursor: not-allowed; }
    .status { min-width: 180px; }
    .check-cell { text-align: center; vertical-align: middle; }
    .check-cell input { width: 16px; height: 16px; margin: 0 auto; display: block; }
    .empty-target { color: var(--muted); }
    .empty { color: var(--muted); text-align: center; padding: 16px; }
    .warn { color: var(--warn); }
    @media (max-width: 760px) { header { padding: 18px 16px; } main { padding: 0 12px 24px; } .meta { grid-template-columns: repeat(2, minmax(120px, 1fr)); } .title-row { align-items: flex-start; flex-direction: column; } .header-actions, .section-head { align-items: flex-start; } .section-head { flex-direction: column; } .action-panel { justify-content: flex-start; text-align: left; } th, td { padding: 7px 8px; } }
    """

    return f"""<!doctype html>
<html lang="zh-CN">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<title>国际化检查报告</title>
<style>{css}</style>
</head>
<body>
<header>
  <div class="title-row">
    <h1>国际化检查报告</h1>
    <div class="header-actions" aria-live="polite">
      <span id="refresh-status">本地服务启动后可刷新。</span>
      <button id="execute-refresh-report" class="action-button secondary-button" type="button" aria-describedby="refresh-status" disabled>刷新</button>
    </div>
  </div>
  <div class="pathline">工程位置：<code>{_e(str(report.project_root))}</code></div>
  <div class="pathline">国际化 JSON：<code>{_e(str(report.i18n_file))}</code></div>
  <div class="meta">
    <div class="metric"><strong>{report.total_keys}</strong><span>参与判断的 key</span></div>
    <div class="metric"><strong>{len(report.used_keys)}</strong><span>静态使用 key</span></div>
    <div class="metric"><strong>{len(report.unused_keys)}</strong><span>未使用 key</span></div>
    <div class="metric"><strong>{len(report.duplicate_value_groups)}</strong><span>相同 value 组</span></div>
    <div class="metric"><strong>{len(report.missing_used_keys)}</strong><span>源码仍使用但 JSON 缺失 key</span></div>
  </div>
</header>
<main>
  <div class="section-head">
    <h2>未使用 key</h2>
    <div class="action-panel" aria-live="polite">
      <span id="delete-status" class="status">勾选未使用 key 后可删除。</span>
      <button id="execute-delete-unused" class="action-button danger-button" type="button" disabled>删除勾选</button>
    </div>
  </div>
  <div class="table-wrap">
    <table class="unused">
      <thead><tr><th>删除</th><th>Key</th><th>Value</th></tr></thead>
      <tbody>{unused_rows}</tbody>
    </table>
  </div>

  <h2>源码仍使用但 JSON 缺失 key</h2>
  <div class="table-wrap">
    <table class="missing">
      <thead><tr><th>Key</th><th>引用次数</th><th>示例位置</th></tr></thead>
      <tbody>{missing_rows}</tbody>
    </table>
  </div>

  <div class="section-head">
    <h2>相同 value</h2>
    <div class="action-panel" aria-live="polite">
      <span id="replace-status" class="status">勾选左侧“替换”的 key，并在同组右侧勾选一个“替换为”的 key。</span>
      <button id="execute-replace" class="action-button" type="button" disabled>执行替换</button>
    </div>
  </div>
  <div class="table-wrap">
    <table class="duplicate">
      <thead><tr><th>Value</th><th>数量</th><th>替换</th><th>Key</th><th>替换为</th></tr></thead>
      <tbody>{duplicate_rows}</tbody>
    </table>
  </div>
</main>
<script>
const i18nHelperApi = {api_config};

function apiUrl(path) {{
  if (!i18nHelperApi.base) return null;
  return `${{i18nHelperApi.base}}${{path}}`;
}}

function refreshReportHtml(_reportPath) {{
  const url = new URL(window.location.href);
  url.searchParams.set('i18n-helper-refresh', Date.now().toString());
  window.location.replace(url.toString());
}}

function collectReplacementMap() {{
  const replacementMap = {{}};
  const targets = document.querySelectorAll('input[data-role="target"]:checked');
  for (const target of targets) {{
    const groupId = target.dataset.group;
    const targetKey = target.dataset.key;
    const sources = document.querySelectorAll(`input[data-role="source"][data-group="${{groupId}}"]:checked`);
    for (const source of sources) {{
      const sourceKey = source.dataset.key;
      if (sourceKey && targetKey && sourceKey !== targetKey) replacementMap[sourceKey] = targetKey;
    }}
  }}
  return replacementMap;
}}

function formatReplacementPreview(replacements, limit = 10) {{
  const entries = Object.entries(replacements);
  if (entries.length === 0) return '';
  const visible = entries
    .slice(0, limit)
    .map(([source, target]) => `${{source}} -> ${{target}}`);
  const hidden = entries.length - visible.length;
  return hidden > 0
    ? `${{visible.join('; ')}}; ... 另有 ${{hidden}} 条`
    : visible.join('; ');
}}

function updateReplaceState() {{
  const button = document.getElementById('execute-replace');
  const status = document.getElementById('replace-status');
  const replacements = collectReplacementMap();
  const count = Object.keys(replacements).length;
  const apiReady = Boolean(i18nHelperApi.base && i18nHelperApi.token);
  button.disabled = !apiReady || count === 0;
  if (!apiReady) {{
    status.textContent = '本地替换服务未启动，请重新运行报告脚本。';
  }} else if (count === 0) {{
    status.textContent = '勾选左侧“替换”的 key，并在同组右侧勾选一个“替换为”的 key。';
  }} else {{
    status.textContent = `已生成 ${{count}} 条替换映射：${{formatReplacementPreview(replacements)}}`;
  }}
}}

function collectUnusedDeletes() {{
  return Array.from(document.querySelectorAll('input[data-role="unused-delete"]:checked'))
    .map((item) => item.dataset.key)
    .filter(Boolean);
}}

function updateDeleteState() {{
  const button = document.getElementById('execute-delete-unused');
  const status = document.getElementById('delete-status');
  const keys = collectUnusedDeletes();
  const apiReady = Boolean(i18nHelperApi.base && i18nHelperApi.token);
  button.disabled = !apiReady || keys.length === 0;
  if (!apiReady) {{
    status.textContent = '本地删除服务未启动，请重新运行报告脚本。';
  }} else if (keys.length === 0) {{
    status.textContent = '勾选未使用 key 后可删除。';
  }} else {{
    status.textContent = `已选择 ${{keys.length}} 个未使用 key。`;
  }}
}}

function updateRefreshState() {{
  const button = document.getElementById('execute-refresh-report');
  const status = document.getElementById('refresh-status');
  const apiReady = Boolean(i18nHelperApi.base && i18nHelperApi.token);
  button.disabled = !apiReady;
  if (!apiReady) {{
    status.textContent = '本地服务未启动，请重新运行报告脚本。';
  }} else {{
    status.textContent = '点击刷新重新扫描。';
  }}
}}

document.querySelectorAll('.duplicate input[type="checkbox"]').forEach((checkbox) => {{
  checkbox.addEventListener('change', (event) => {{
    const current = event.currentTarget;
    const group = current.dataset.group;
    const key = current.dataset.key;
    if (current.checked && current.dataset.role === "target") {{
      document.querySelectorAll(`input[data-role="target"][data-group="${{group}}"]`).forEach((item) => {{
        if (item.dataset.role === "target" && item !== current) item.checked = false;
      }});
      const sameSource = document.querySelector(`input[data-role="source"][data-group="${{group}}"][data-key="${{CSS.escape(key)}}"]`);
      if (sameSource) sameSource.checked = false;
    }}
    if (current.checked && current.dataset.role === 'source') {{
      const sameTarget = document.querySelector(`input[data-role="target"][data-group="${{group}}"][data-key="${{CSS.escape(key)}}"]`);
      if (sameTarget) sameTarget.checked = false;
    }}
    updateReplaceState();
  }});
}});

document.getElementById('execute-replace').addEventListener('click', async () => {{
  const button = document.getElementById('execute-replace');
  const status = document.getElementById('replace-status');
  const replacements = collectReplacementMap();
  const count = Object.keys(replacements).length;
  if (count === 0) return;
  if (!window.confirm(`将执行 ${{count}} 条替换映射：\n${{formatReplacementPreview(replacements)}}\n并重新生成报告。是否继续？`)) return;
  button.disabled = true;
  button.setAttribute('aria-busy', 'true');
  status.textContent = '正在替换并重新排查...';
  try {{
    const response = await fetch(apiUrl('/replace'), {{
      method: 'POST',
      headers: {{ 'Content-Type': 'application/json' }},
      body: JSON.stringify({{ token: i18nHelperApi.token, replacements }})
    }});
    const result = await response.json();
    if (!response.ok) throw new Error(result.error || '替换失败');
    status.textContent = `已替换 ${{result.replacedOccurrences}} 处，删除 ${{result.deletedKeys}} 个旧 key，正在刷新报告...`;
    window.setTimeout(() => refreshReportHtml(result.reportPath), 700);
  }} catch (error) {{
    status.textContent = error.message || '替换失败';
    button.removeAttribute('aria-busy');
    updateReplaceState();
  }}
}});

document.querySelectorAll('input[data-role="unused-delete"]').forEach((checkbox) => {{
  checkbox.addEventListener('change', updateDeleteState);
}});

document.getElementById('execute-delete-unused').addEventListener('click', async () => {{
  const button = document.getElementById('execute-delete-unused');
  const status = document.getElementById('delete-status');
  const keys = collectUnusedDeletes();
  if (keys.length === 0) return;
  if (!window.confirm(`将从 zh_CN.json、en_US.json、zh_TW.json 中删除 ${{keys.length}} 个未使用 key，并重新生成报告。是否继续？`)) return;
  button.disabled = true;
  button.setAttribute('aria-busy', 'true');
  status.textContent = '正在删除并重新排查...';
  try {{
    const response = await fetch(apiUrl('/delete-unused'), {{
      method: 'POST',
      headers: {{ 'Content-Type': 'application/json' }},
      body: JSON.stringify({{ token: i18nHelperApi.token, keys }})
    }});
    const result = await response.json();
    if (!response.ok) throw new Error(result.error || '删除失败');
    status.textContent = `已删除 ${{result.deletedKeys}} 个 key，更新 ${{result.changedFiles}} 个语言文件，正在刷新报告...`;
    window.setTimeout(() => refreshReportHtml(result.reportPath), 700);
  }} catch (error) {{
    status.textContent = error.message || '删除失败';
    button.removeAttribute('aria-busy');
    updateDeleteState();
  }}
}});

document.getElementById('execute-refresh-report').addEventListener('click', async () => {{
  const button = document.getElementById('execute-refresh-report');
  const status = document.getElementById('refresh-status');
  if (!i18nHelperApi.base || !i18nHelperApi.token) {{
    updateRefreshState();
    return;
  }}
  button.disabled = true;
  button.setAttribute('aria-busy', 'true');
  status.textContent = '正在重新执行检查...';
  try {{
    const response = await fetch(apiUrl('/refresh'), {{
      method: 'POST',
      headers: {{ 'Content-Type': 'application/json' }},
      body: JSON.stringify({{ token: i18nHelperApi.token }})
    }});
    const result = await response.json();
    if (!response.ok) throw new Error(result.error || '刷新失败');
    status.textContent = '已重新生成报告，正在刷新页面...';
    window.setTimeout(() => refreshReportHtml(result.reportPath), 700);
  }} catch (error) {{
    status.textContent = error.message || '刷新失败';
    button.removeAttribute('aria-busy');
    updateRefreshState();
  }}
}});

updateReplaceState();
updateDeleteState();
updateRefreshState();
</script>
</body>
</html>"""


def write_report_html(
    report: AnalysisReport,
    output_path: pathlib.Path | None = None,
    open_report: bool = True,
    api_endpoint: str | None = None,
    api_token: str | None = None,
) -> pathlib.Path:
    if output_path is None:
        output_path = DEFAULT_REPORT_PATH
    output_path = output_path.resolve()
    output_path.write_text(
        render_html(report, api_endpoint=api_endpoint, api_token=api_token),
        encoding="utf-8",
    )
    if open_report:
        webbrowser.open(output_path.as_uri())
    return output_path


def serve_replacement_api(
    config_path: pathlib.Path,
    output_path: pathlib.Path,
    port: int,
    token: str,
) -> int:
    endpoint = f"http://127.0.0.1:{port}/replace"

    class Handler(http.server.BaseHTTPRequestHandler):
        def do_OPTIONS(self) -> None:
            self._send_json({"ok": True})

        def do_POST(self) -> None:
            if self.path not in {"/replace", "/delete-unused", "/refresh"}:
                self._send_json({"error": "not found"}, status=404)
                return

            try:
                length = int(self.headers.get("Content-Length", "0"))
                payload = json.loads(self.rfile.read(length).decode("utf-8") or "{}")
                if payload.get("token") != token:
                    self._send_json({"error": "invalid token"}, status=403)
                    return

                project_root, i18n_file, patterns = read_config(config_path)
                i18n_path = i18n_file if i18n_file.is_absolute() else project_root / i18n_file
                changed_files = 0
                replaced_occurrences = 0
                deleted_keys = 0
                deleted_entries = 0
                deleted_files: list[str] = []
                skipped_delete_keys: tuple[str, ...] = ()
                if self.path == "/replace":
                    replacements = payload.get("replacements")
                    if not isinstance(replacements, dict):
                        self._send_json({"error": "replacements must be an object"}, status=400)
                        return
                    replace_result = replace_keys_in_project(project_root, i18n_path, replacements)
                    changed_files = replace_result.changed_files
                    replaced_occurrences = replace_result.replaced_occurrences
                    safe_delete_keys, skipped_delete_keys = filter_keys_safe_to_delete(
                        project_root,
                        i18n_file,
                        patterns,
                        replace_result.replaced_keys,
                    )
                    delete_result = delete_keys_from_i18n_json(i18n_path, safe_delete_keys)
                    deleted_keys = delete_result.deleted_keys
                    deleted_entries = delete_result.deleted_entries
                    deleted_files = [str(path) for path in delete_result.changed_paths]
                elif self.path == "/delete-unused":
                    keys = payload.get("keys")
                    if not isinstance(keys, list):
                        self._send_json({"error": "keys must be an array"}, status=400)
                        return
                    delete_result = delete_keys_from_i18n_json(i18n_path, keys)
                    changed_files = delete_result.changed_files
                    deleted_keys = delete_result.deleted_keys
                    deleted_entries = delete_result.deleted_entries
                    deleted_files = [str(path) for path in delete_result.changed_paths]

                report = analyze_project(project_root, i18n_file, patterns)
                write_report_html(
                    report,
                    output_path,
                    open_report=False,
                    api_endpoint=endpoint,
                    api_token=token,
                )
                self._send_json(
                    {
                        "ok": True,
                        "changedFiles": changed_files,
                        "replacedOccurrences": replaced_occurrences,
                        "deletedKeys": deleted_keys,
                        "deletedEntries": deleted_entries,
                        "deletedFiles": deleted_files,
                        "skippedDeleteKeys": list(skipped_delete_keys),
                        "reportPath": str(output_path),
                        "unusedKeys": len(report.unused_keys),
                        "missingUsedKeys": len(report.missing_used_keys),
                        "duplicateValueGroups": len(report.duplicate_value_groups),
                    }
                )
            except Exception as error:  # pragma: no cover - exercised through browser usage.
                self._send_json({"error": str(error)}, status=500)

        def log_message(self, _format: str, *_args: Any) -> None:
            return

        def _send_json(self, payload: dict[str, Any], status: int = 200) -> None:
            body = json.dumps(payload, ensure_ascii=False).encode("utf-8")
            self.send_response(status)
            self.send_header("Content-Type", "application/json; charset=utf-8")
            self.send_header("Content-Length", str(len(body)))
            self.send_header("Access-Control-Allow-Origin", "*")
            self.send_header("Access-Control-Allow-Headers", "Content-Type")
            self.send_header("Access-Control-Allow-Methods", "POST, OPTIONS")
            self.end_headers()
            self.wfile.write(body)

    server = http.server.ThreadingHTTPServer(("127.0.0.1", port), Handler)
    server.timeout = 2
    deadline = time.time() + 7200
    while time.time() < deadline:
        server.handle_request()
    return 0


def _find_free_port() -> int:
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as sock:
        sock.bind(("127.0.0.1", 0))
        return int(sock.getsockname()[1])


def _start_replacement_server(
    config_path: pathlib.Path,
    output_path: pathlib.Path,
    port: int,
    token: str,
) -> None:
    command = [
        sys.executable,
        str(pathlib.Path(__file__).resolve()),
        "--serve",
        "--config",
        str(config_path.resolve()),
        "--output",
        str(output_path.resolve()),
        "--port",
        str(port),
        "--token",
        token,
    ]
    creationflags = subprocess.CREATE_NO_WINDOW if os.name == "nt" else 0
    subprocess.Popen(
        command,
        stdin=subprocess.DEVNULL,
        stdout=subprocess.DEVNULL,
        stderr=subprocess.DEVNULL,
        close_fds=True,
        creationflags=creationflags,
    )


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description="Generate an i18n usage report.")
    parser.add_argument(
        "--config",
        type=pathlib.Path,
        default=pathlib.Path(__file__).resolve().parents[1] / "config.md",
        help="Path to config.md. The first three lines are project path, i18n JSON path, and regex JSON array.",
    )
    parser.add_argument(
        "--output",
        type=pathlib.Path,
        help="HTML output path. Defaults to the i18n-helper skill directory.",
    )
    parser.add_argument("--no-open", action="store_true", help="Write the report without opening it.")
    parser.add_argument("--no-server", action="store_true", help="Do not start the local replacement service.")
    parser.add_argument("--serve", action="store_true", help=argparse.SUPPRESS)
    parser.add_argument("--port", type=int, help=argparse.SUPPRESS)
    parser.add_argument("--token", help=argparse.SUPPRESS)
    args = parser.parse_args(argv)

    output_path = (args.output or DEFAULT_REPORT_PATH).resolve()

    if args.serve:
        if not args.port or not args.token:
            raise ValueError("--serve requires --port and --token")
        return serve_replacement_api(args.config, output_path, args.port, args.token)

    project_root, i18n_file, patterns = read_config(args.config)
    api_endpoint = None
    api_token = None
    if not args.no_server:
        port = _find_free_port()
        api_token = secrets.token_urlsafe(24)
        _start_replacement_server(args.config, output_path, port, api_token)
        api_endpoint = f"http://127.0.0.1:{port}/replace"

    report = analyze_project(project_root, i18n_file, patterns)
    output_path = write_report_html(
        report,
        output_path,
        open_report=not args.no_open,
        api_endpoint=api_endpoint,
        api_token=api_token,
    )

    print(f"报告已生成：{output_path}")
    print(f"工程位置：{report.project_root}")
    print(f"国际化 JSON：{report.i18n_file}")
    print(f"扫描源码文件数：{report.scanned_files}")
    print(f"参与判断的 key：{report.total_keys}")
    print(f"静态使用 key：{len(report.used_keys)}")
    print(f"未使用 key：{len(report.unused_keys)}")
    print(f"相同 value 组：{len(report.duplicate_value_groups)}")
    print(f"源码仍使用但 JSON 缺失 key：{len(report.missing_used_keys)}")
    if api_endpoint:
        print(f"替换服务：{api_endpoint}")
    return 0


def _strip_optional_quotes(value: str) -> str:
    if len(value) >= 2 and value[0] == value[-1] and value[0] in {"'", '"'}:
        return value[1:-1]
    return value


def _load_i18n_entries(i18n_path: pathlib.Path) -> tuple[I18nEntry, ...]:
    data = json.loads(i18n_path.read_text(encoding="utf-8-sig"))
    entries: list[I18nEntry] = []
    _flatten_entries(data, "", entries)
    return tuple(entry for entry in entries if not _is_ignored_key(entry.key))


def _is_ignored_key(key: str) -> bool:
    return key.startswith(IGNORED_KEY_PREFIXES)


def _flatten_entries(value: Any, prefix: str, entries: list[I18nEntry]) -> None:
    if isinstance(value, dict):
        for child_key, child_value in value.items():
            key = str(child_key) if not prefix else f"{prefix}.{child_key}"
            _flatten_entries(child_value, key, entries)
        return
    entries.append(I18nEntry(prefix, value))


def _iter_source_files(project_root: pathlib.Path, i18n_path: pathlib.Path) -> Iterable[pathlib.Path]:
    i18n_dir = i18n_path.parent.resolve()
    for current_root, dir_names, file_names in os.walk(project_root):
        current_path = pathlib.Path(current_root)
        resolved_current_path = current_path.resolve()
        if _is_relative_to(resolved_current_path, i18n_dir):
            dir_names[:] = []
            continue

        dir_names[:] = [
            name
            for name in dir_names
            if name.lower() not in EXCLUDED_DIR_NAMES
            and not _is_relative_to((current_path / name).resolve(), i18n_dir)
        ]

        for file_name in file_names:
            if file_name in EXCLUDED_FILE_NAMES:
                continue
            path = current_path / file_name
            if path.suffix.lower() not in SOURCE_EXTENSIONS:
                continue
            yield path


def _is_relative_to(path: pathlib.Path, parent: pathlib.Path) -> bool:
    try:
        path.relative_to(parent)
        return True
    except ValueError:
        return False


def _read_text(path: pathlib.Path) -> str:
    text, _encoding = _read_text_with_encoding(path)
    return text


def _read_text_with_encoding(path: pathlib.Path) -> tuple[str, str]:
    raw = path.read_bytes()
    if raw.startswith(b"\xef\xbb\xbf"):
        return raw.decode("utf-8-sig"), "utf-8-sig"

    for encoding in ("utf-8", "gb18030"):
        try:
            return raw.decode(encoding), encoding
        except UnicodeDecodeError:
            continue
    return raw.decode("utf-8", errors="replace"), "utf-8"


def _write_text_with_encoding(path: pathlib.Path, text: str, encoding: str) -> None:
    path.write_bytes(text.encode(encoding))


def _replace_key_literals_in_text(text: str, replacements: dict[str, str]) -> tuple[str, int, set[str]]:
    pieces: list[str] = []
    last_emit = 0
    index = 0
    count = 0
    replaced_keys: set[str] = set()

    while index < len(text):
        if text.startswith("//", index):
            next_line = text.find("\n", index + 2)
            index = len(text) if next_line == -1 else next_line + 1
            continue
        if text.startswith("/*", index):
            close = text.find("*/", index + 2)
            index = len(text) if close == -1 else close + 2
            continue

        marker = text[index]
        if marker in {"'", '"'}:
            value, end, reason = _parse_quoted_string_with_end(text, index, marker)
            if reason is None and value in replacements:
                pieces.append(text[last_emit:index])
                pieces.append(marker)
                pieces.append(_encode_string_literal_content(replacements[value], marker))
                pieces.append(marker)
                last_emit = end
                count += 1
                replaced_keys.add(value)
            index = max(end, index + 1)
            continue

        if marker == "`":
            value, end, reason = _parse_template_literal_with_end(text, index)
            if reason is None and value in replacements:
                pieces.append(text[last_emit:index])
                pieces.append("`")
                pieces.append(_encode_string_literal_content(replacements[value], "`"))
                pieces.append("`")
                last_emit = end
                count += 1
                replaced_keys.add(value)
            index = max(end, index + 1)
            continue

        index += 1

    if count == 0:
        return text, 0, set()
    pieces.append(text[last_emit:])
    return "".join(pieces), count, replaced_keys


def _encode_string_literal_content(value: str, quote: str) -> str:
    escaped = value.replace("\\", "\\\\")
    escaped = escaped.replace("\r", "\\r").replace("\n", "\\n")
    if quote == "`":
        return escaped.replace("`", "\\`").replace("${", "\\${")
    return escaped.replace(quote, "\\" + quote)


def _parse_first_argument(source: str, call_start: int) -> ParsedArgument:
    open_paren = source.find("(", call_start)
    if open_paren == -1:
        return ParsedArgument((), "call opening parenthesis was not found")

    arg_start = _skip_space_and_comments(source, open_paren + 1)
    if arg_start >= len(source):
        return ParsedArgument((), "missing first argument")

    marker = source[arg_start]
    if marker in {"'", '"'}:
        value, reason = _parse_quoted_string(source, arg_start, marker)
        return ParsedArgument((value,) if value is not None else (), reason)
    if marker == "`":
        value, reason = _parse_template_literal(source, arg_start)
        return ParsedArgument((value,) if value is not None else (), reason)

    conditional_keys, reason = _parse_static_conditional_argument(source, arg_start)
    if conditional_keys:
        return ParsedArgument(conditional_keys, None)
    return ParsedArgument((), reason or "first argument is not a string literal")


def _find_quoted_key_literals(source: str, known_keys: frozenset[str]) -> set[str]:
    used: set[str] = set()
    index = 0
    while index < len(source):
        if source.startswith("//", index):
            next_line = source.find("\n", index + 2)
            index = len(source) if next_line == -1 else next_line + 1
            continue
        if source.startswith("/*", index):
            close = source.find("*/", index + 2)
            index = len(source) if close == -1 else close + 2
            continue

        marker = source[index]
        if marker in {"'", '"'}:
            value, end, reason = _parse_quoted_string_with_end(source, index, marker)
            if reason is None and value in known_keys:
                used.add(value)
            index = max(end, index + 1)
            continue

        if marker == "`":
            index = _skip_string_like(source, index, marker)
            continue
        index += 1
    return used


def _parse_static_conditional_argument(source: str, arg_start: int) -> tuple[tuple[str, ...], str | None]:
    arg_end = _find_first_argument_end(source, arg_start)
    expression = source[arg_start:arg_end].strip()
    if not expression:
        return (), "missing first argument"
    question_index = _find_top_level_conditional_question(expression)
    if question_index == -1:
        return (), None
    return _collect_static_conditional_branch_keys(expression)


def _find_first_argument_end(source: str, start: int) -> int:
    depth = 0
    index = start
    while index < len(source):
        char = source[index]
        if char in {"'", '"', "`"}:
            index = _skip_string_like(source, index, char)
            continue
        if char in "([{":
            depth += 1
            index += 1
            continue
        if char in ")]}":
            if depth == 0 and char == ")":
                return index
            depth = max(0, depth - 1)
            index += 1
            continue
        if char == "," and depth == 0:
            return index
        index += 1
    return len(source)


def _collect_static_conditional_branch_keys(expression: str) -> tuple[tuple[str, ...], str | None]:
    expression = _strip_wrapping_parentheses(expression.strip())
    question_index = _find_top_level_conditional_question(expression)
    if question_index == -1:
        key = _parse_static_string_expression(expression)
        if key is None:
            return (), "conditional branch is not a static string literal"
        return (key,), None

    colon_index = _find_matching_conditional_colon(expression, question_index)
    if colon_index == -1:
        return (), "conditional expression is missing a false branch"

    true_keys, true_reason = _collect_static_conditional_branch_keys(expression[question_index + 1 : colon_index])
    false_keys, false_reason = _collect_static_conditional_branch_keys(expression[colon_index + 1 :])
    if true_keys and false_keys:
        return true_keys + false_keys, None
    return (), true_reason or false_reason or "conditional branches are not static string literals"


def _find_top_level_conditional_question(expression: str) -> int:
    depth = 0
    index = 0
    while index < len(expression):
        char = expression[index]
        if char in {"'", '"', "`"}:
            index = _skip_string_like(expression, index, char)
            continue
        if char in "([{":
            depth += 1
        elif char in ")]}":
            depth = max(0, depth - 1)
        elif char == "?" and depth == 0:
            return index
        index += 1
    return -1


def _find_matching_conditional_colon(expression: str, question_index: int) -> int:
    depth = 0
    nested_conditionals = 0
    index = question_index + 1
    while index < len(expression):
        char = expression[index]
        if char in {"'", '"', "`"}:
            index = _skip_string_like(expression, index, char)
            continue
        if char in "([{":
            depth += 1
        elif char in ")]}":
            depth = max(0, depth - 1)
        elif depth == 0 and char == "?":
            nested_conditionals += 1
        elif depth == 0 and char == ":":
            if nested_conditionals == 0:
                return index
            nested_conditionals -= 1
        index += 1
    return -1


def _parse_static_string_expression(expression: str) -> str | None:
    expression = _strip_wrapping_parentheses(expression.strip())
    if not expression:
        return None
    marker = expression[0]
    if marker in {"'", '"'}:
        value, end, reason = _parse_quoted_string_with_end(expression, 0, marker)
    elif marker == "`":
        value, end, reason = _parse_template_literal_with_end(expression, 0)
    else:
        return None
    if reason is not None or value is None:
        return None
    return value if expression[end:].strip() == "" else None


def _strip_wrapping_parentheses(expression: str) -> str:
    while _outer_parentheses_wrap_expression(expression):
        expression = expression[1:-1].strip()
    return expression


def _outer_parentheses_wrap_expression(expression: str) -> bool:
    expression = expression.strip()
    if len(expression) < 2 or expression[0] != "(" or expression[-1] != ")":
        return False

    depth = 0
    index = 0
    while index < len(expression):
        char = expression[index]
        if char in {"'", '"', "`"}:
            index = _skip_string_like(expression, index, char)
            continue
        if char == "(":
            depth += 1
        elif char == ")":
            depth -= 1
            if depth == 0 and index != len(expression) - 1:
                return False
        index += 1
    return depth == 0


def _skip_string_like(source: str, start: int, quote: str) -> int:
    index = start + 1
    while index < len(source):
        char = source[index]
        if char == "\\":
            index += 2
            continue
        if char == quote:
            return index + 1
        index += 1
    return len(source)


def _skip_space_and_comments(source: str, index: int) -> int:
    while index < len(source):
        char = source[index]
        if char.isspace():
            index += 1
            continue
        if source.startswith("//", index):
            next_line = source.find("\n", index + 2)
            index = len(source) if next_line == -1 else next_line + 1
            continue
        if source.startswith("/*", index):
            close = source.find("*/", index + 2)
            index = len(source) if close == -1 else close + 2
            continue
        break
    return index


def _parse_quoted_string(source: str, start: int, quote: str) -> tuple[str | None, str | None]:
    value, _end, reason = _parse_quoted_string_with_end(source, start, quote)
    return value, reason


def _parse_quoted_string_with_end(source: str, start: int, quote: str) -> tuple[str | None, int, str | None]:
    index = start + 1
    chars: list[str] = []
    while index < len(source):
        char = source[index]
        if char == "\\":
            decoded, index = _decode_escape(source, index)
            chars.append(decoded)
            continue
        if char == quote:
            return "".join(chars), index + 1, None
        chars.append(char)
        index += 1
    return None, index, "unterminated string literal"


def _parse_template_literal(source: str, start: int) -> tuple[str | None, str | None]:
    value, _end, reason = _parse_template_literal_with_end(source, start)
    return value, reason


def _parse_template_literal_with_end(source: str, start: int) -> tuple[str | None, int, str | None]:
    index = start + 1
    chars: list[str] = []
    while index < len(source):
        char = source[index]
        if char == "\\":
            decoded, index = _decode_escape(source, index)
            chars.append(decoded)
            continue
        if char == "`":
            return "".join(chars), index + 1, None
        if char == "$" and index + 1 < len(source) and source[index + 1] == "{":
            return None, index, "template literal contains interpolation"
        chars.append(char)
        index += 1
    return None, index, "unterminated template literal"


def _decode_escape(source: str, slash_index: int) -> tuple[str, int]:
    if slash_index + 1 >= len(source):
        return "\\", slash_index + 1

    escaped = source[slash_index + 1]
    simple = {
        "\\": "\\",
        "'": "'",
        '"': '"',
        "`": "`",
        "b": "\b",
        "f": "\f",
        "n": "\n",
        "r": "\r",
        "t": "\t",
        "v": "\v",
    }
    if escaped in simple:
        return simple[escaped], slash_index + 2
    if escaped in {"\n", "\r"}:
        next_index = slash_index + 2
        if escaped == "\r" and next_index < len(source) and source[next_index] == "\n":
            next_index += 1
        return "", next_index
    if escaped == "x" and slash_index + 3 < len(source):
        digits = source[slash_index + 2 : slash_index + 4]
        if _is_hex(digits):
            return chr(int(digits, 16)), slash_index + 4
    if escaped == "u":
        decoded = _decode_unicode_escape(source, slash_index + 2)
        if decoded is not None:
            return decoded
    return escaped, slash_index + 2


def _decode_unicode_escape(source: str, start: int) -> tuple[str, int] | None:
    if start < len(source) and source[start] == "{":
        close = source.find("}", start + 1)
        if close != -1:
            digits = source[start + 1 : close]
            if digits and _is_hex(digits):
                return chr(int(digits, 16)), close + 1
        return None

    if start + 3 < len(source):
        digits = source[start : start + 4]
        if _is_hex(digits):
            return chr(int(digits, 16)), start + 4
    return None


def _is_hex(value: str) -> bool:
    return bool(value) and all(char in "0123456789abcdefABCDEF" for char in value)


def _call_snippet(source: str, call_start: int) -> str:
    snippet = re.sub(r"\s+", " ", source[call_start : call_start + 240]).strip()
    if len(snippet) > 220:
        return snippet[:217] + "..."
    return snippet


def _find_duplicate_value_groups(entries: tuple[I18nEntry, ...]) -> tuple[DuplicateValueGroup, ...]:
    grouped: dict[str, list[I18nEntry]] = {}
    for entry in entries:
        normalized = _normalize_value(entry.value)
        if normalized is None:
            continue
        grouped.setdefault(normalized, []).append(entry)

    groups = [
        DuplicateValueGroup(
            normalized_value=normalized,
            sample_value=_display_value(items[0].value),
            keys=tuple(sorted(item.key for item in items)),
        )
        for normalized, items in grouped.items()
        if len(items) > 1
    ]
    groups.sort(key=lambda group: (-len(group.keys), group.normalized_value))
    return tuple(groups)


def _normalize_value(value: Any) -> str | None:
    if not isinstance(value, str):
        return None
    normalized = unicodedata.normalize("NFKC", value)
    normalized = re.sub(r"\s+", " ", normalized).strip()
    return normalized or None


def _display_value(value: Any) -> str:
    if isinstance(value, str):
        return value
    return json.dumps(value, ensure_ascii=False)


def _duplicate_rows(group: DuplicateValueGroup, group_index: int) -> str:
    rows: list[str] = []
    row_count = len(group.keys)
    for index, key in enumerate(group.keys):
        source_checkbox = (
            f'<input type="checkbox" data-role="source" data-group="g{group_index}" '
            f'data-key="{_e(key)}" aria-label="将 {_e(key)} 替换为同组右侧勾选的 key">'
        )
        target_checkbox = (
            f'<input type="checkbox" data-role="target" data-group="g{group_index}" '
            f'data-key="{_e(key)}" aria-label="使用 {_e(key)} 作为替换目标">'
        )
        target_cell = (
            '<td class="check-cell target-cell empty-target" aria-label="HD 开头的 key 不可作为替换目标"></td>'
            if key.startswith("HD")
            else f'<td class="check-cell target-cell">{target_checkbox}</td>'
        )
        if index == 0:
            rows.append(
                "<tr>"
                f'<td class="merged" rowspan="{row_count}">{_e(group.normalized_value)}</td>'
                f'<td class="merged" rowspan="{row_count}">{row_count}</td>'
                f'<td class="check-cell">{source_checkbox}</td>'
                f"<td><code>{_e(key)}</code></td>"
                f"{target_cell}"
                "</tr>"
            )
            continue
        rows.append(
            "<tr>"
            f'<td class="check-cell">{source_checkbox}</td>'
            f"<td><code>{_e(key)}</code></td>"
            f"{target_cell}"
            "</tr>"
        )
    return "\n".join(rows)


def _relative_display_path(path: pathlib.Path, project_root: pathlib.Path) -> str:
    try:
        return str(path.relative_to(project_root))
    except ValueError:
        return str(path)


def _api_base_from_endpoint(api_endpoint: str | None) -> str | None:
    if not api_endpoint:
        return None
    return api_endpoint[:-8] if api_endpoint.endswith("/replace") else api_endpoint.rstrip("/")


def _e(value: str) -> str:
    return html.escape(value, quote=True)


if __name__ == "__main__":
    raise SystemExit(main())
