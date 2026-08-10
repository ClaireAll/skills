import argparse
import html
import http.server
import json
import os
import pathlib
import re
import secrets
import socket
import subprocess
import sys
import webbrowser
from typing import Any

import i18n_report


SKILL_DIR = pathlib.Path(__file__).resolve().parents[1]
DEFAULT_OUTPUT = SKILL_DIR / "i18n-helper-report.html"


def collect_report(config_path: pathlib.Path, scan_root: pathlib.Path, prefix: str) -> dict[str, Any]:
    project_root, i18n_file, patterns = i18n_report.read_config(config_path)
    project_root = project_root.resolve()
    i18n_path = (i18n_file if i18n_file.is_absolute() else project_root / i18n_file).resolve()
    scan_root = scan_root.resolve()
    compiled_patterns = tuple(re.compile(pattern) for pattern in patterns)
    entries = i18n_report._load_i18n_entries(i18n_path)
    entry_by_key = {entry.key: entry for entry in entries}
    known_keys = frozenset(entry_by_key)
    value_to_keys: dict[str, list[str]] = {}
    for entry in entries:
        normalized = i18n_report._normalize_value(entry.value)
        if normalized:
            value_to_keys.setdefault(normalized, []).append(entry.key)

    used: dict[str, list[str]] = {}
    scanned_files = 0
    seen_call_positions: set[tuple[pathlib.Path, int]] = set()

    def record(key: str, source_path: pathlib.Path, line: int | None = None) -> None:
        if not key.startswith(prefix):
            return
        location = i18n_report._relative_display_path(source_path, project_root)
        if line is not None:
            location = f"{location}:{line}"
        bucket = used.setdefault(key, [])
        if location not in bucket:
            bucket.append(location)

    for source_path in _iter_scoped_source_files(scan_root, i18n_path):
        text = i18n_report._read_text(source_path)
        scanned_files += 1
        for key in i18n_report._find_quoted_key_literals(text, known_keys):
            record(key, source_path)
        for pattern in compiled_patterns:
            for match in pattern.finditer(text):
                call_start = match.start()
                open_paren = text.find("(", call_start)
                seen_key = (source_path, open_paren if open_paren != -1 else call_start)
                if seen_key in seen_call_positions:
                    continue
                seen_call_positions.add(seen_key)
                parsed = i18n_report._parse_first_argument(text, call_start)
                if not parsed.static_keys:
                    continue
                line_number = text.count("\n", 0, call_start) + 1
                for key in parsed.static_keys:
                    record(key, source_path, line_number)

    rows = []
    for key in sorted(used):
        entry = entry_by_key.get(key)
        if entry is None:
            continue
        normalized = i18n_report._normalize_value(entry.value)
        candidates = [candidate for candidate in value_to_keys.get(normalized or "", []) if candidate != key]
        rows.append(
            {
                "key": key,
                "value": i18n_report._display_value(entry.value),
                "usage_count": len(used[key]),
                "examples": used[key][:8],
                "candidate_keys": candidates,
                "target_keys": [candidate for candidate in candidates if not candidate.startswith(prefix)],
            }
        )

    return {
        "project_root": str(project_root),
        "scan_root": str(scan_root),
        "i18n_file": str(i18n_path),
        "prefix": prefix,
        "scanned_files": scanned_files,
        "hd_key_count": len(rows),
        "replaceable_key_count": sum(1 for row in rows if row["target_keys"]),
        "rows": rows,
    }


def write_report(
    config_path: pathlib.Path,
    scan_root: pathlib.Path,
    prefix: str,
    output_path: pathlib.Path,
    api_base: str | None = None,
    token: str | None = None,
    open_report: bool = True,
) -> pathlib.Path:
    report = collect_report(config_path, scan_root, prefix)
    output_path = output_path.resolve()
    output_path.write_text(render_html(report, api_base, token), encoding="utf-8")
    if open_report:
        webbrowser.open(output_path.as_uri())
    return output_path


def render_html(report: dict[str, Any], api_base: str | None, token: str | None) -> str:
    grouped: dict[str, list[dict[str, Any]]] = {}
    for row in report["rows"]:
        grouped.setdefault(row["value"], []).append(row)

    body_rows: list[str] = []
    group_index = 0
    for value, rows in grouped.items():
        group_index += 1
        targets = sorted({target for row in rows for target in row["target_keys"]})
        target_html = "".join(
            f'<label><input type="radio" name="target-{group_index}" value="{_e(target)}"> <code>{_e(target)}</code></label>'
            for target in targets
        )
        if not target_html:
            target_html = '<span class="muted">没有非 HD 同 value 候选</span>'
        for row_index, row in enumerate(rows):
            other_hd = [key for key in row["candidate_keys"] if key.startswith(report["prefix"])]
            body_rows.append(
                "<tr>"
                + (
                    f'<td rowspan="{len(rows)}" class="value-cell">{_e(value)}</td>'
                    if row_index == 0
                    else ""
                )
                + f'<td><input type="checkbox" class="source-check" data-group="{group_index}" value="{_e(row["key"])}" {"disabled" if not targets else ""}></td>'
                + f'<td><code>{_e(row["key"])}</code><div class="meta">使用 {row["usage_count"]} 处</div><div class="examples">{_e("; ".join(row["examples"]))}</div></td>'
                + f'<td>{_e(", ".join(other_hd)) if other_hd else "<span class=\"muted\">无</span>"}</td>'
                + (
                    f'<td rowspan="{len(rows)}" class="targets">{target_html}</td>'
                    if row_index == 0
                    else ""
                )
                + "</tr>"
            )

    if not body_rows:
        body_rows.append('<tr><td colspan="5" class="empty">没有找到目录下以指定前缀开头的已使用 key。</td></tr>')

    api_config = json.dumps({"base": api_base, "token": token}, ensure_ascii=False)
    return f"""<!doctype html>
<html lang="zh-CN">
<head>
  <meta charset="utf-8">
  <title>HD 国际化替换候选</title>
  <style>
    :root {{ color-scheme: light; --line: #d8dee8; --muted: #667085; --bg: #f6f8fb; --primary: #1f65d6; }}
    * {{ box-sizing: border-box; }}
    body {{ margin: 0; padding: 24px; font-family: -apple-system, BlinkMacSystemFont, "Segoe UI", sans-serif; color: #18202f; background: var(--bg); }}
    h1 {{ margin: 0 0 10px; font-size: 22px; }}
    code {{ font-family: "Cascadia Mono", Consolas, monospace; font-size: 12px; }}
    .panel {{ background: #fff; border: 1px solid var(--line); border-radius: 8px; padding: 18px; box-shadow: 0 8px 24px rgba(22, 34, 51, 0.06); }}
    .head {{ display: flex; justify-content: space-between; gap: 16px; align-items: flex-start; margin-bottom: 16px; }}
    .path {{ color: var(--muted); font-size: 12px; line-height: 1.7; overflow-wrap: anywhere; }}
    .metrics {{ display: flex; gap: 10px; flex-wrap: wrap; margin: 12px 0 18px; }}
    .metric {{ border: 1px solid var(--line); border-radius: 6px; padding: 8px 12px; background: #fbfcff; }}
    .metric strong {{ display: block; font-size: 18px; }}
    .metric span, .muted, .meta, .examples {{ color: var(--muted); font-size: 12px; }}
    .actions {{ display: flex; gap: 8px; align-items: center; }}
    button {{ border: 1px solid var(--line); background: #fff; border-radius: 6px; padding: 8px 12px; cursor: pointer; }}
    button.primary {{ color: #fff; background: var(--primary); border-color: var(--primary); }}
    button:disabled {{ opacity: .55; cursor: not-allowed; }}
    table {{ width: 100%; border-collapse: collapse; background: #fff; }}
    th, td {{ border-bottom: 1px solid var(--line); padding: 10px; vertical-align: top; text-align: left; }}
    th {{ position: sticky; top: 0; background: #eef3fb; z-index: 1; }}
    tbody tr:nth-child(even) {{ background: #fafcff; }}
    .table-wrap {{ max-height: calc(100vh - 260px); overflow: auto; border: 1px solid var(--line); border-radius: 8px; }}
    .value-cell {{ width: 220px; font-weight: 600; }}
    .targets label {{ display: block; margin-bottom: 6px; }}
    .examples {{ margin-top: 5px; line-height: 1.5; overflow-wrap: anywhere; }}
    .status {{ min-height: 20px; margin-top: 10px; color: var(--muted); }}
    .empty {{ text-align: center; color: var(--muted); padding: 30px; }}
  </style>
</head>
<body>
  <div class="panel">
    <div class="head">
      <div>
        <h1>HD 国际化替换候选</h1>
        <div class="path">扫描目录：<code>{_e(report["scan_root"])}</code></div>
        <div class="path">国际化 JSON：<code>{_e(report["i18n_file"])}</code></div>
        <div class="path">规则：只列出源码中已使用且 key 以 <code>{_e(report["prefix"])}</code> 开头的项；候选来自同 value 的非 HD key。</div>
      </div>
      <div class="actions">
        <button id="refreshBtn">刷新</button>
        <button id="replaceBtn" class="primary">执行勾选替换</button>
      </div>
    </div>
    <div class="metrics">
      <div class="metric"><strong>{report["scanned_files"]}</strong><span>扫描源码文件</span></div>
      <div class="metric"><strong>{report["hd_key_count"]}</strong><span>HD key</span></div>
      <div class="metric"><strong>{report["replaceable_key_count"]}</strong><span>有非 HD 候选</span></div>
    </div>
    <div class="table-wrap">
      <table>
        <thead><tr><th>Value</th><th>替换</th><th>HD Key</th><th>同 value 的其它 HD</th><th>替换为</th></tr></thead>
        <tbody>{"".join(body_rows)}</tbody>
      </table>
    </div>
    <div class="status" id="status">替换只修改扫描目录内源码字符串字面量，不删除 zh_CN/en_US/zh_TW JSON。</div>
  </div>
  <script>
    const api = {api_config};
    const statusEl = document.getElementById('status');
    function setStatus(text) {{ statusEl.textContent = text; }}
    function reloadReport() {{
      const url = new URL(window.location.href);
      url.searchParams.set('t', Date.now().toString());
      window.location.href = url.toString();
    }}
    async function post(path, payload) {{
      if (!api.base) throw new Error('本报告没有启动替换服务，请重新运行脚本。');
      const response = await fetch(api.base + path, {{
        method: 'POST',
        headers: {{ 'Content-Type': 'application/json' }},
        body: JSON.stringify({{ ...payload, token: api.token }})
      }});
      const result = await response.json();
      if (!response.ok) throw new Error(result.error || '请求失败');
      return result;
    }}
    document.getElementById('replaceBtn').addEventListener('click', async () => {{
      const replacements = {{}};
      document.querySelectorAll('.source-check:checked').forEach((checkbox) => {{
        const group = checkbox.dataset.group;
        const target = document.querySelector(`input[name="target-${{group}}"]:checked`);
        if (target) replacements[checkbox.value] = target.value;
      }});
      const count = Object.keys(replacements).length;
      if (!count) {{ setStatus('请先勾选要替换的 HD key，并选择替换目标。'); return; }}
      if (!window.confirm(`将替换 ${{count}} 个 HD key，范围仅限当前扫描目录。是否继续？`)) return;
      try {{
        setStatus('正在替换...');
        const result = await post('/replace', {{ replacements }});
        setStatus(`替换完成：${{result.changedFiles}} 个文件，${{result.replacedOccurrences}} 处。正在刷新...`);
        window.setTimeout(reloadReport, 700);
      }} catch (error) {{
        setStatus(error.message);
      }}
    }});
    document.getElementById('refreshBtn').addEventListener('click', async () => {{
      try {{
        setStatus('正在刷新...');
        await post('/refresh', {{}});
        reloadReport();
      }} catch (error) {{
        setStatus(error.message);
      }}
    }});
  </script>
</body>
</html>"""


def serve_api(config_path: pathlib.Path, scan_root: pathlib.Path, prefix: str, output_path: pathlib.Path, port: int, token: str) -> int:
    class Handler(http.server.BaseHTTPRequestHandler):
        def do_OPTIONS(self) -> None:
            self._send_json({"ok": True})

        def do_POST(self) -> None:
            if self.path not in {"/replace", "/refresh"}:
                self._send_json({"error": "not found"}, 404)
                return
            try:
                length = int(self.headers.get("Content-Length", "0"))
                payload = json.loads(self.rfile.read(length).decode("utf-8") or "{}")
                if payload.get("token") != token:
                    self._send_json({"error": "invalid token"}, 403)
                    return
                changed_files = 0
                replaced_occurrences = 0
                replaced_keys: tuple[str, ...] = ()
                if self.path == "/replace":
                    replacements = payload.get("replacements")
                    if not isinstance(replacements, dict):
                        self._send_json({"error": "replacements must be an object"}, 400)
                        return
                    clean = _validate_replacements(config_path, scan_root, prefix, replacements)
                    changed_files, replaced_occurrences, replaced_keys = _replace_in_scope(config_path, scan_root, clean)
                write_report(config_path, scan_root, prefix, output_path, f"http://127.0.0.1:{port}", token, open_report=False)
                self._send_json(
                    {
                        "ok": True,
                        "changedFiles": changed_files,
                        "replacedOccurrences": replaced_occurrences,
                        "replacedKeys": replaced_keys,
                        "reportPath": str(output_path.resolve()),
                    }
                )
            except Exception as error:
                self._send_json({"error": str(error)}, 500)

        def log_message(self, _format: str, *_args: Any) -> None:
            return

        def _send_json(self, payload: dict[str, Any], status: int = 200) -> None:
            body = json.dumps(payload, ensure_ascii=False).encode("utf-8")
            self.send_response(status)
            self.send_header("Content-Type", "application/json; charset=utf-8")
            self.send_header("Access-Control-Allow-Origin", "*")
            self.send_header("Access-Control-Allow-Headers", "Content-Type")
            self.send_header("Access-Control-Allow-Methods", "POST, OPTIONS")
            self.send_header("Content-Length", str(len(body)))
            self.end_headers()
            self.wfile.write(body)

    with http.server.ThreadingHTTPServer(("127.0.0.1", port), Handler) as server:
        server.serve_forever()
    return 0


def _replace_in_scope(config_path: pathlib.Path, scan_root: pathlib.Path, replacements: dict[str, str]) -> tuple[int, int, tuple[str, ...]]:
    project_root, i18n_file, _patterns = i18n_report.read_config(config_path)
    project_root = project_root.resolve()
    i18n_path = (i18n_file if i18n_file.is_absolute() else project_root / i18n_file).resolve()
    changed_files = 0
    replaced_occurrences = 0
    replaced_keys: set[str] = set()
    for source_path in _iter_scoped_source_files(scan_root.resolve(), i18n_path):
        text, encoding = i18n_report._read_text_with_encoding(source_path)
        updated, count, file_replaced_keys = i18n_report._replace_key_literals_in_text(text, replacements)
        if not count:
            continue
        i18n_report._write_text_with_encoding(source_path, updated, encoding)
        changed_files += 1
        replaced_occurrences += count
        replaced_keys.update(file_replaced_keys)
    return changed_files, replaced_occurrences, tuple(sorted(replaced_keys))


def _validate_replacements(config_path: pathlib.Path, scan_root: pathlib.Path, prefix: str, raw: dict[Any, Any]) -> dict[str, str]:
    report = collect_report(config_path, scan_root, prefix)
    allowed: dict[str, set[str]] = {
        row["key"]: set(row["target_keys"])
        for row in report["rows"]
        if row["target_keys"]
    }
    clean: dict[str, str] = {}
    for source, target in raw.items():
        if not isinstance(source, str) or not isinstance(target, str):
            continue
        if target not in allowed.get(source, set()):
            raise ValueError(f"{source} cannot be replaced by {target}")
        clean[source] = target
    if not clean:
        raise ValueError("no valid replacements selected")
    return clean


def _iter_scoped_source_files(scan_root: pathlib.Path, i18n_path: pathlib.Path):
    i18n_dir = i18n_path.parent.resolve()
    for current_root, dir_names, file_names in os.walk(scan_root):
        current_path = pathlib.Path(current_root)
        resolved_current_path = current_path.resolve()
        if i18n_report._is_relative_to(resolved_current_path, i18n_dir):
            dir_names[:] = []
            continue
        dir_names[:] = [
            name
            for name in dir_names
            if name.lower() not in i18n_report.EXCLUDED_DIR_NAMES
            and not i18n_report._is_relative_to((current_path / name).resolve(), i18n_dir)
        ]
        for file_name in file_names:
            if file_name in i18n_report.EXCLUDED_FILE_NAMES:
                continue
            path = current_path / file_name
            if path.suffix.lower() not in i18n_report.SOURCE_EXTENSIONS:
                continue
            yield path


def _start_server(config_path: pathlib.Path, scan_root: pathlib.Path, prefix: str, output_path: pathlib.Path, port: int, token: str) -> None:
    command = [
        sys.executable,
        str(pathlib.Path(__file__).resolve()),
        "--serve",
        "--config",
        str(config_path.resolve()),
        "--scan-root",
        str(scan_root.resolve()),
        "--prefix",
        prefix,
        "--output",
        str(output_path.resolve()),
        "--port",
        str(port),
        "--token",
        token,
    ]
    kwargs: dict[str, Any] = {
        "stdout": subprocess.DEVNULL,
        "stderr": subprocess.DEVNULL,
        "stdin": subprocess.DEVNULL,
        "cwd": str(SKILL_DIR),
    }
    if os.name == "nt":
        kwargs["creationflags"] = subprocess.CREATE_NO_WINDOW
    subprocess.Popen(command, **kwargs)


def _find_free_port() -> int:
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as sock:
        sock.bind(("127.0.0.1", 0))
        return int(sock.getsockname()[1])


def _e(value: Any) -> str:
    return html.escape(str(value), quote=True)


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description="Generate scoped HD-prefix i18n replacement report.")
    parser.add_argument("--config", type=pathlib.Path, default=SKILL_DIR / "config.md")
    parser.add_argument("--scan-root", type=pathlib.Path, required=True)
    parser.add_argument("--prefix", default="HD")
    parser.add_argument("--output", type=pathlib.Path, default=DEFAULT_OUTPUT)
    parser.add_argument("--no-open", action="store_true")
    parser.add_argument("--no-server", action="store_true")
    parser.add_argument("--serve", action="store_true", help=argparse.SUPPRESS)
    parser.add_argument("--port", type=int, help=argparse.SUPPRESS)
    parser.add_argument("--token", help=argparse.SUPPRESS)
    args = parser.parse_args(argv)

    output_path = args.output.resolve()
    if args.serve:
        if not args.port or not args.token:
            raise ValueError("--serve requires --port and --token")
        return serve_api(args.config, args.scan_root, args.prefix, output_path, args.port, args.token)

    api_base = None
    token = None
    if not args.no_server:
        port = _find_free_port()
        token = secrets.token_urlsafe(24)
        _start_server(args.config, args.scan_root, args.prefix, output_path, port, token)
        api_base = f"http://127.0.0.1:{port}"

    write_report(args.config, args.scan_root, args.prefix, output_path, api_base, token, open_report=not args.no_open)
    report = collect_report(args.config, args.scan_root, args.prefix)
    print(f"报告已生成：{output_path}")
    print(f"扫描目录：{report['scan_root']}")
    print(f"扫描源码文件数：{report['scanned_files']}")
    print(f"{args.prefix} key：{report['hd_key_count']}")
    print(f"有非 {args.prefix} 候选：{report['replaceable_key_count']}")
    if api_base:
        print(f"替换服务：{api_base}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
