import json
import pathlib
import subprocess
import sys
import tempfile
import time
import unittest
import urllib.error
import urllib.request

import i18n_report


class I18nReportTests(unittest.TestCase):
    def make_project(self):
        workspace = tempfile.TemporaryDirectory()
        root = pathlib.Path(workspace.name)
        (root / "src").mkdir()
        (root / "i18n").mkdir()
        (root / "i18n" / "zh_CN.json").write_text(
            json.dumps(
                {
                    "fxp.data.data_center.specified_o'clock.opt": "Clock option",
                    "HD-Basic_Edit_Connection": "Edit connection",
                    "HD-Basic_Add_Connect": "Add connect",
                    "used.quoted.single": "Single quoted",
                    "used.quoted.double": "Double quoted",
                    "used.simple": "Simple",
                    "unused.key": "Unused",
                    "duplicate.a": " A  B ",
                    "duplicate.b": "A B",
                    "HD-Duplicate": "A B",
                    "BI.legacy.unused": "Ignored BI prefix",
                    "nested": {"unused": "Nested unused"},
                },
                ensure_ascii=False,
            ),
            encoding="utf-8",
        )
        return workspace, root

    def write_used_duplicate_keys(self, root):
        (root / "src" / "duplicates.ts").write_text(
            "const a = 'duplicate.a';\n"
            "const b = 'duplicate.b';\n"
            "const hd = 'HD-Duplicate';\n",
            encoding="utf-8",
        )

    def test_default_report_path_lives_in_skill_directory(self):
        skill_dir = pathlib.Path(i18n_report.__file__).resolve().parents[1]
        self.assertEqual(i18n_report.DEFAULT_REPORT_PATH, skill_dir / "i18n-helper-report.html")

    def test_static_key_with_inner_apostrophe_is_not_truncated(self):
        workspace, root = self.make_project()
        self.addCleanup(workspace.cleanup)
        (root / "src" / "page.tsx").write_text(
            "BI.i18nText(\"fxp.data.data_center.specified_o'clock.opt\", index);\n"
            "t('used.simple');\n",
            encoding="utf-8",
        )

        report = i18n_report.analyze_project(
            root,
            pathlib.Path("i18n/zh_CN.json"),
            [r"BI\.i18nText\s*\(", r"(?:t|i18n\.t|\$t)\s*\("],
        )

        self.assertIn("fxp.data.data_center.specified_o'clock.opt", report.used_keys)
        self.assertNotIn("fxp.data.data_center.specified_o", report.used_keys)
        self.assertIn("unused.key", {item.key for item in report.unused_keys})

    def test_static_keys_in_conditional_first_argument_are_used(self):
        workspace, root = self.make_project()
        self.addCleanup(workspace.cleanup)
        (root / "src" / "conditional.tsx").write_text(
            "BI.i18nText(mode === 'edit' ? 'HD-Basic_Edit_Connection' : 'HD-Basic_Add_Connect');\n",
            encoding="utf-8",
        )

        report = i18n_report.analyze_project(
            root,
            pathlib.Path("i18n/zh_CN.json"),
            [r"BI\.i18nText\s*\(", r"(?:t|i18n\.t|\$t)\s*\("],
        )

        self.assertIn("HD-Basic_Edit_Connection", report.used_keys)
        self.assertIn("HD-Basic_Add_Connect", report.used_keys)
        self.assertNotIn("edit", report.used_keys)
        self.assertNotIn("HD-Basic_Edit_Connection", {item.key for item in report.unused_keys})
        self.assertNotIn("HD-Basic_Add_Connect", {item.key for item in report.unused_keys})

    def test_complete_keys_in_single_or_double_quoted_literals_are_used(self):
        workspace, root = self.make_project()
        self.addCleanup(workspace.cleanup)
        (root / "src" / "quoted.ts").write_text(
            "const single = 'used.quoted.single';\n"
            "const double = \"used.quoted.double\";\n"
            "// 'unused.key' in a comment is not a source string literal.\n",
            encoding="utf-8",
        )

        report = i18n_report.analyze_project(
            root,
            pathlib.Path("i18n/zh_CN.json"),
            [r"BI\.i18nText\s*\(", r"(?:t|i18n\.t|\$t)\s*\("],
        )

        unused_keys = {item.key for item in report.unused_keys}
        self.assertIn("used.quoted.single", report.used_keys)
        self.assertIn("used.quoted.double", report.used_keys)
        self.assertNotIn("used.quoted.single", unused_keys)
        self.assertNotIn("used.quoted.double", unused_keys)
        self.assertIn("unused.key", unused_keys)

    def test_dynamic_calls_are_reported_separately(self):
        workspace, root = self.make_project()
        self.addCleanup(workspace.cleanup)
        (root / "src" / "dynamic.ts").write_text(
            "const key = 'used.simple';\n"
            "BI.i18nText(key);\n"
            "i18n.t(`prefix.${name}`);\n",
            encoding="utf-8",
        )

        report = i18n_report.analyze_project(
            root,
            pathlib.Path("i18n/zh_CN.json"),
            [r"BI\.i18nText\s*\(", r"(?:t|i18n\.t|\$t)\s*\("],
        )

        reasons = {item.reason for item in report.dynamic_calls}
        self.assertIn("first argument is not a string literal", reasons)
        self.assertIn("template literal contains interpolation", reasons)

    def test_static_call_key_missing_from_json_is_reported(self):
        workspace, root = self.make_project()
        self.addCleanup(workspace.cleanup)
        (root / "src" / "missing.tsx").write_text(
            "BI.i18nText('HD-Basic_Cancel');\n"
            "t('HD-Basic_Cancel');\n",
            encoding="utf-8",
        )

        report = i18n_report.analyze_project(
            root,
            pathlib.Path("i18n/zh_CN.json"),
            [r"BI\.i18nText\s*\(", r"(?:t|i18n\.t|\$t)\s*\("],
        )

        missing = {item.key: item for item in report.missing_used_keys}
        self.assertIn("HD-Basic_Cancel", missing)
        self.assertEqual(missing["HD-Basic_Cancel"].usage_count, 2)
        self.assertIn("missing.tsx:1", missing["HD-Basic_Cancel"].examples[0])

    def test_duplicate_values_are_grouped_after_width_and_space_normalization(self):
        workspace, root = self.make_project()
        self.addCleanup(workspace.cleanup)
        self.write_used_duplicate_keys(root)

        report = i18n_report.analyze_project(
            root,
            pathlib.Path("i18n/zh_CN.json"),
            [r"BI\.i18nText\s*\(", r"(?:t|i18n\.t|\$t)\s*\("],
        )

        duplicate_groups = [group for group in report.duplicate_value_groups if "duplicate.a" in group.keys]
        self.assertEqual(len(duplicate_groups), 1)
        self.assertEqual(set(duplicate_groups[0].keys), {"duplicate.a", "duplicate.b", "HD-Duplicate"})

    def test_unused_keys_are_excluded_from_duplicate_value_groups(self):
        workspace, root = self.make_project()
        self.addCleanup(workspace.cleanup)
        (root / "src" / "duplicates.ts").write_text(
            "const a = 'duplicate.a';\n"
            "const b = 'duplicate.b';\n",
            encoding="utf-8",
        )

        report = i18n_report.analyze_project(
            root,
            pathlib.Path("i18n/zh_CN.json"),
            [r"BI\.i18nText\s*\(", r"(?:t|i18n\.t|\$t)\s*\("],
        )

        duplicate_groups = [group for group in report.duplicate_value_groups if "duplicate.a" in group.keys]
        self.assertEqual(len(duplicate_groups), 1)
        self.assertEqual(set(duplicate_groups[0].keys), {"duplicate.a", "duplicate.b"})
        self.assertNotIn("HD-Duplicate", duplicate_groups[0].keys)
        self.assertIn("HD-Duplicate", {item.key for item in report.unused_keys})

    def test_html_report_contains_required_sections(self):
        workspace, root = self.make_project()
        self.addCleanup(workspace.cleanup)
        (root / "src" / "dynamic.ts").write_text("BI.i18nText(key);\n", encoding="utf-8")
        report = i18n_report.analyze_project(
            root,
            pathlib.Path("i18n/zh_CN.json"),
            [r"BI\.i18nText\s*\(", r"(?:t|i18n\.t|\$t)\s*\("],
        )

        html = i18n_report.render_html(report)

        self.assertIn("未使用 key", html)
        self.assertIn("相同 value", html)
        self.assertIn("unused.key", html)
        self.assertNotIn("疑似动态使用", html)
        self.assertNotIn("疑似动态调用", html)
        self.assertNotIn("dynamic", html)

    def test_bi_prefix_keys_are_excluded_from_unused_and_duplicate_checks(self):
        workspace, root = self.make_project()
        self.addCleanup(workspace.cleanup)
        (root / "src" / "empty.ts").write_text("", encoding="utf-8")

        report = i18n_report.analyze_project(
            root,
            pathlib.Path("i18n/zh_CN.json"),
            [r"BI\.i18nText\s*\(", r"(?:t|i18n\.t|\$t)\s*\("],
        )

        all_unused_keys = {item.key for item in report.unused_keys}
        duplicate_keys = {key for group in report.duplicate_value_groups for key in group.keys}
        self.assertNotIn("BI.legacy.unused", all_unused_keys)
        self.assertNotIn("BI.legacy.unused", duplicate_keys)

    def test_duplicate_value_table_renders_one_key_per_row_with_merged_value(self):
        workspace, root = self.make_project()
        self.addCleanup(workspace.cleanup)
        self.write_used_duplicate_keys(root)
        report = i18n_report.analyze_project(
            root,
            pathlib.Path("i18n/zh_CN.json"),
            [r"BI\.i18nText\s*\(", r"(?:t|i18n\.t|\$t)\s*\("],
        )

        html = i18n_report.render_html(report)

        self.assertIn('rowspan="3"', html)
        self.assertIn("<td><code>HD-Duplicate</code></td>", html)
        self.assertIn("<td><code>duplicate.a</code></td>", html)
        self.assertIn("<td><code>duplicate.b</code></td>", html)

    def test_duplicate_value_table_has_replace_controls(self):
        workspace, root = self.make_project()
        self.addCleanup(workspace.cleanup)
        self.write_used_duplicate_keys(root)
        report = i18n_report.analyze_project(
            root,
            pathlib.Path("i18n/zh_CN.json"),
            [r"BI\.i18nText\s*\(", r"(?:t|i18n\.t|\$t)\s*\("],
        )

        html = i18n_report.render_html(
            report,
            api_endpoint="http://127.0.0.1:8765/replace",
            api_token="test-token",
        )

        self.assertIn("替换", html)
        self.assertIn("替换为", html)
        self.assertIn("执行替换", html)
        self.assertIn('data-role="source"', html)
        self.assertIn('data-role="target"', html)
        self.assertIn('data-key="duplicate.a"', html)
        self.assertIn('data-key="duplicate.b"', html)
        self.assertIn("function refreshReportHtml", html)
        self.assertIn("refreshReportHtml(result.reportPath)", html)
        self.assertIn("i18n-helper-refresh", html)
        self.assertNotIn("window.location.reload()", html)

    def test_replace_controls_collect_all_checked_rows_as_map(self):
        workspace, root = self.make_project()
        self.addCleanup(workspace.cleanup)
        self.write_used_duplicate_keys(root)
        report = i18n_report.analyze_project(
            root,
            pathlib.Path("i18n/zh_CN.json"),
            [r"BI\.i18nText\s*\(", r"(?:t|i18n\.t|\$t)\s*\("],
        )

        html = i18n_report.render_html(report)

        self.assertIn("function collectReplacementMap()", html)
        self.assertIn('document.querySelectorAll(\'input[data-role="target"]:checked\')', html)
        self.assertIn("for (const target of targets)", html)
        self.assertIn("replacementMap[sourceKey] = targetKey", html)
        self.assertIn("const replacements = collectReplacementMap();", html)
        self.assertNotIn("const target = document.querySelector(`input[data-role=\"target\"", html)

    def test_replace_controls_show_actual_many_source_replacement_preview(self):
        workspace, root = self.make_project()
        self.addCleanup(workspace.cleanup)
        self.write_used_duplicate_keys(root)
        report = i18n_report.analyze_project(
            root,
            pathlib.Path("i18n/zh_CN.json"),
            [r"BI\.i18nText\s*\(", r"(?:t|i18n\.t|\$t)\s*\("],
        )

        html = i18n_report.render_html(report)

        self.assertIn("function formatReplacementPreview(replacements", html)
        self.assertIn("Object.entries(replacements)", html)
        self.assertIn("formatReplacementPreview(replacements)", html)
        self.assertIn("${formatReplacementPreview(replacements)}", html)

    def test_header_has_manual_refresh_control(self):
        workspace, root = self.make_project()
        self.addCleanup(workspace.cleanup)
        (root / "src" / "empty.ts").write_text("", encoding="utf-8")
        report = i18n_report.analyze_project(
            root,
            pathlib.Path("i18n/zh_CN.json"),
            [r"BI\.i18nText\s*\(", r"(?:t|i18n\.t|\$t)\s*\("],
        )

        html = i18n_report.render_html(
            report,
            api_endpoint="http://127.0.0.1:8765/replace",
            api_token="test-token",
        )

        self.assertIn('class="title-row"', html)
        self.assertIn('id="execute-refresh-report"', html)
        self.assertIn('aria-describedby="refresh-status"', html)
        self.assertIn('id="refresh-status"', html)
        self.assertIn(">刷新<", html)
        self.assertIn("fetch(apiUrl('/refresh')", html)
        self.assertIn("refreshReportHtml(result.reportPath)", html)

    def test_tables_use_zebra_striping(self):
        workspace, root = self.make_project()
        self.addCleanup(workspace.cleanup)
        self.write_used_duplicate_keys(root)
        report = i18n_report.analyze_project(
            root,
            pathlib.Path("i18n/zh_CN.json"),
            [r"BI\.i18nText\s*\(", r"(?:t|i18n\.t|\$t)\s*\("],
        )

        html = i18n_report.render_html(report)

        self.assertIn("--stripe:", html)
        self.assertIn("tbody tr:nth-child(even)", html)

    def test_refresh_endpoint_reruns_report_without_source_changes(self):
        workspace, root = self.make_project()
        self.addCleanup(workspace.cleanup)
        source_path = root / "src" / "page.ts"
        source_path.write_text("const key = 'used.simple';\n", encoding="utf-8")
        original_i18n = (root / "i18n" / "zh_CN.json").read_text(encoding="utf-8")
        config_path = root / "config.md"
        config_path.write_text(
            "\n".join(
                [
                    str(root),
                    "i18n/zh_CN.json",
                    json.dumps([r"BI\.i18nText\s*\(", r"(?:t|i18n\.t|\$t)\s*\("]),
                ]
            ),
            encoding="utf-8",
        )
        output_path = root / "report.html"
        port = i18n_report._find_free_port()
        token = "test-token"
        process = subprocess.Popen(
            [
                sys.executable,
                str(pathlib.Path(i18n_report.__file__).resolve()),
                "--serve",
                "--config",
                str(config_path),
                "--output",
                str(output_path),
                "--port",
                str(port),
                "--token",
                token,
            ],
            stdout=subprocess.DEVNULL,
            stderr=subprocess.DEVNULL,
        )

        def stop_server():
            process.terminate()
            try:
                process.wait(timeout=5)
            except subprocess.TimeoutExpired:
                process.kill()

        self.addCleanup(stop_server)
        deadline = time.time() + 5
        while time.time() < deadline:
            try:
                request = urllib.request.Request(
                    f"http://127.0.0.1:{port}/ready",
                    method="OPTIONS",
                )
                urllib.request.urlopen(request, timeout=0.5).close()
                break
            except (OSError, urllib.error.URLError):
                time.sleep(0.05)
        else:
            self.fail("refresh service did not start")

        request = urllib.request.Request(
            f"http://127.0.0.1:{port}/refresh",
            data=json.dumps({"token": token}).encode("utf-8"),
            headers={"Content-Type": "application/json"},
            method="POST",
        )
        with urllib.request.urlopen(request, timeout=5) as response:
            payload = json.loads(response.read().decode("utf-8"))

        self.assertTrue(payload["ok"])
        self.assertEqual(payload["changedFiles"], 0)
        self.assertEqual(payload["replacedOccurrences"], 0)
        self.assertEqual(payload["deletedKeys"], 0)
        self.assertEqual(payload["reportPath"], str(output_path))
        self.assertTrue(output_path.exists())
        self.assertIn("unused.key", output_path.read_text(encoding="utf-8"))
        self.assertEqual((root / "i18n" / "zh_CN.json").read_text(encoding="utf-8"), original_i18n)

    def test_hd_keys_cannot_be_selected_as_replacement_target(self):
        workspace, root = self.make_project()
        self.addCleanup(workspace.cleanup)
        self.write_used_duplicate_keys(root)
        report = i18n_report.analyze_project(
            root,
            pathlib.Path("i18n/zh_CN.json"),
            [r"BI\.i18nText\s*\(", r"(?:t|i18n\.t|\$t)\s*\("],
        )

        html = i18n_report.render_html(report)

        self.assertIn('data-role="source" data-group="g0" data-key="HD-Duplicate"', html)
        self.assertNotIn('data-role="target" data-group="g0" data-key="HD-Duplicate"', html)
        self.assertIn('class="check-cell target-cell empty-target"', html)

    def test_duplicate_target_selection_is_limited_to_one_per_group(self):
        workspace, root = self.make_project()
        self.addCleanup(workspace.cleanup)
        self.write_used_duplicate_keys(root)
        report = i18n_report.analyze_project(
            root,
            pathlib.Path("i18n/zh_CN.json"),
            [r"BI\.i18nText\s*\(", r"(?:t|i18n\.t|\$t)\s*\("],
        )

        html = i18n_report.render_html(report)

        self.assertIn('item.dataset.role === "target"', html)
        self.assertIn('input[data-role="target"][data-group="${group}"]', html)

    def test_unused_key_table_has_delete_controls(self):
        workspace, root = self.make_project()
        self.addCleanup(workspace.cleanup)
        (root / "src" / "empty.ts").write_text("", encoding="utf-8")
        report = i18n_report.analyze_project(
            root,
            pathlib.Path("i18n/zh_CN.json"),
            [r"BI\.i18nText\s*\(", r"(?:t|i18n\.t|\$t)\s*\("],
        )

        html = i18n_report.render_html(
            report,
            api_endpoint="http://127.0.0.1:8765",
            api_token="test-token",
        )

        self.assertIn('id="execute-delete-unused"', html)
        self.assertIn('data-role="unused-delete"', html)
        self.assertIn('data-key="unused.key"', html)
        self.assertIn("/delete-unused", html)

    def test_delete_unused_keys_updates_locale_jsons(self):
        workspace, root = self.make_project()
        self.addCleanup(workspace.cleanup)
        source_data = json.loads((root / "i18n" / "zh_CN.json").read_text(encoding="utf-8"))
        for locale_name in ("en_US.json", "zh_TW.json"):
            (root / "i18n" / locale_name).write_text(
                json.dumps(source_data, ensure_ascii=False),
                encoding="utf-8",
            )

        result = i18n_report.delete_keys_from_i18n_json(
            root / "i18n" / "zh_CN.json",
            ["unused.key", "nested.unused", "missing.key"],
        )

        self.assertEqual(result.deleted_keys, 2)
        self.assertEqual(result.deleted_entries, 6)
        self.assertEqual(result.changed_files, 3)
        for locale_name in ("zh_CN.json", "en_US.json", "zh_TW.json"):
            data = json.loads((root / "i18n" / locale_name).read_text(encoding="utf-8"))
            self.assertNotIn("unused.key", data)
            self.assertNotIn("unused", data["nested"])

    def test_replace_keys_updates_source_literals_only(self):
        workspace, root = self.make_project()
        self.addCleanup(workspace.cleanup)
        source_path = root / "src" / "replace.ts"
        source_path.write_text(
            "BI.i18nText('duplicate.a');\n"
            "const key = \"duplicate.a\";\n"
            "// duplicate.a in comment should stay\n",
            encoding="utf-8",
        )
        original_i18n = (root / "i18n" / "zh_CN.json").read_text(encoding="utf-8")

        result = i18n_report.replace_keys_in_project(
            root,
            root / "i18n" / "zh_CN.json",
            {"duplicate.a": "duplicate.b"},
        )

        updated_source = source_path.read_text(encoding="utf-8")
        self.assertEqual(result.replaced_occurrences, 2)
        self.assertIn("BI.i18nText('duplicate.b');", updated_source)
        self.assertIn('const key = "duplicate.b";', updated_source)
        self.assertIn("// duplicate.a in comment should stay", updated_source)
        self.assertEqual((root / "i18n" / "zh_CN.json").read_text(encoding="utf-8"), original_i18n)

    def test_replace_keys_does_not_add_utf8_bom_to_source_file(self):
        workspace, root = self.make_project()
        self.addCleanup(workspace.cleanup)
        source_path = root / "src" / "replace.ts"
        source_path.write_bytes(b"BI.i18nText('duplicate.a');\n")

        i18n_report.replace_keys_in_project(
            root,
            root / "i18n" / "zh_CN.json",
            {"duplicate.a": "duplicate.b"},
        )

        updated_bytes = source_path.read_bytes()
        self.assertFalse(updated_bytes.startswith(b"\xef\xbb\xbf"))
        self.assertIn(b"BI.i18nText('duplicate.b');", updated_bytes)

    def test_replace_keys_preserves_crlf_without_extra_carriage_returns(self):
        workspace, root = self.make_project()
        self.addCleanup(workspace.cleanup)
        source_path = root / "src" / "replace.ts"
        source_path.write_bytes(
            b"BI.i18nText('duplicate.a');\r\n"
            b"const key = 'duplicate.a';\r\n"
        )

        i18n_report.replace_keys_in_project(
            root,
            root / "i18n" / "zh_CN.json",
            {"duplicate.a": "duplicate.b"},
        )

        updated_bytes = source_path.read_bytes()
        self.assertNotIn(b"\r\r\n", updated_bytes)
        self.assertIn(b"BI.i18nText('duplicate.b');\r\n", updated_bytes)
        self.assertIn(b"const key = 'duplicate.b';\r\n", updated_bytes)

    def test_keys_still_used_after_replace_are_not_safe_to_delete(self):
        workspace, root = self.make_project()
        self.addCleanup(workspace.cleanup)
        (root / "src" / "remaining.ts").write_text(
            "BI.i18nText('duplicate.a');\n",
            encoding="utf-8",
        )

        safe_keys, skipped_keys = i18n_report.filter_keys_safe_to_delete(
            root,
            pathlib.Path("i18n/zh_CN.json"),
            [r"BI\.i18nText\s*\(", r"(?:t|i18n\.t|\$t)\s*\("],
            ["duplicate.a", "unused.key"],
        )

        self.assertEqual(safe_keys, ("unused.key",))
        self.assertEqual(skipped_keys, ("duplicate.a",))

    def test_replace_keys_matches_only_complete_quoted_literals(self):
        workspace, root = self.make_project()
        self.addCleanup(workspace.cleanup)
        source_path = root / "src" / "replace.ts"
        source_path.write_text(
            "BI.i18nText('A');\n"
            "BI.i18nText('A_B');\n"
            'const double = "A_B";\n'
            "const template = `A_B`;\n",
            encoding="utf-8",
        )

        result = i18n_report.replace_keys_in_project(
            root,
            root / "i18n" / "zh_CN.json",
            {"A": "C"},
        )

        updated_source = source_path.read_text(encoding="utf-8")
        self.assertEqual(result.replaced_occurrences, 1)
        self.assertIn("BI.i18nText('C');", updated_source)
        self.assertIn("BI.i18nText('A_B');", updated_source)
        self.assertIn('const double = "A_B";', updated_source)
        self.assertIn("const template = `A_B`;", updated_source)

    def test_replace_endpoint_deletes_replaced_keys_from_locale_jsons(self):
        workspace, root = self.make_project()
        self.addCleanup(workspace.cleanup)
        source_data = json.loads((root / "i18n" / "zh_CN.json").read_text(encoding="utf-8"))
        for locale_name in ("en_US.json", "zh_TW.json"):
            (root / "i18n" / locale_name).write_text(
                json.dumps(source_data, ensure_ascii=False),
                encoding="utf-8",
            )
        source_path = root / "src" / "replace.ts"
        source_path.write_text("BI.i18nText('duplicate.a');\n", encoding="utf-8")
        config_path = root / "config.md"
        config_path.write_text(
            "\n".join(
                [
                    str(root),
                    "i18n/zh_CN.json",
                    json.dumps([r"BI\.i18nText\s*\(", r"(?:t|i18n\.t|\$t)\s*\("]),
                ]
            ),
            encoding="utf-8",
        )
        output_path = root / "report.html"
        port = i18n_report._find_free_port()
        token = "test-token"
        process = subprocess.Popen(
            [
                sys.executable,
                str(pathlib.Path(i18n_report.__file__).resolve()),
                "--serve",
                "--config",
                str(config_path),
                "--output",
                str(output_path),
                "--port",
                str(port),
                "--token",
                token,
            ],
            stdout=subprocess.DEVNULL,
            stderr=subprocess.DEVNULL,
        )

        def stop_server():
            process.terminate()
            try:
                process.wait(timeout=5)
            except subprocess.TimeoutExpired:
                process.kill()

        self.addCleanup(stop_server)
        deadline = time.time() + 5
        while time.time() < deadline:
            try:
                request = urllib.request.Request(
                    f"http://127.0.0.1:{port}/ready",
                    method="OPTIONS",
                )
                urllib.request.urlopen(request, timeout=0.5).close()
                break
            except (OSError, urllib.error.URLError):
                time.sleep(0.05)
        else:
            self.fail("replacement service did not start")

        request = urllib.request.Request(
            f"http://127.0.0.1:{port}/replace",
            data=json.dumps(
                {"token": token, "replacements": {"duplicate.a": "duplicate.b"}}
            ).encode("utf-8"),
            headers={"Content-Type": "application/json"},
            method="POST",
        )
        with urllib.request.urlopen(request, timeout=5) as response:
            payload = json.loads(response.read().decode("utf-8"))

        self.assertTrue(payload["ok"])
        self.assertEqual(payload["replacedOccurrences"], 1)
        self.assertEqual(payload["deletedKeys"], 1)
        self.assertEqual(payload["deletedEntries"], 3)
        self.assertEqual(len(payload["deletedFiles"]), 3)
        self.assertIn("BI.i18nText('duplicate.b');", source_path.read_text(encoding="utf-8"))
        for locale_name in ("zh_CN.json", "en_US.json", "zh_TW.json"):
            data = json.loads((root / "i18n" / locale_name).read_text(encoding="utf-8"))
            self.assertNotIn("duplicate.a", data)
            self.assertIn("duplicate.b", data)

    def test_replace_endpoint_applies_whole_replacement_map(self):
        workspace, root = self.make_project()
        self.addCleanup(workspace.cleanup)
        source_data = json.loads((root / "i18n" / "zh_CN.json").read_text(encoding="utf-8"))
        source_data.update(
            {
                "duplicate.c": "C D",
                "duplicate.d": "C  D",
            }
        )
        for locale_name in ("zh_CN.json", "en_US.json", "zh_TW.json"):
            (root / "i18n" / locale_name).write_text(
                json.dumps(source_data, ensure_ascii=False),
                encoding="utf-8",
            )
        source_path = root / "src" / "replace.ts"
        source_path.write_text(
            "BI.i18nText('duplicate.a');\n"
            "BI.i18nText('duplicate.c');\n",
            encoding="utf-8",
        )
        config_path = root / "config.md"
        config_path.write_text(
            "\n".join(
                [
                    str(root),
                    "i18n/zh_CN.json",
                    json.dumps([r"BI\.i18nText\s*\(", r"(?:t|i18n\.t|\$t)\s*\("]),
                ]
            ),
            encoding="utf-8",
        )
        output_path = root / "report.html"
        port = i18n_report._find_free_port()
        token = "test-token"
        process = subprocess.Popen(
            [
                sys.executable,
                str(pathlib.Path(i18n_report.__file__).resolve()),
                "--serve",
                "--config",
                str(config_path),
                "--output",
                str(output_path),
                "--port",
                str(port),
                "--token",
                token,
            ],
            stdout=subprocess.DEVNULL,
            stderr=subprocess.DEVNULL,
        )

        def stop_server():
            process.terminate()
            try:
                process.wait(timeout=5)
            except subprocess.TimeoutExpired:
                process.kill()

        self.addCleanup(stop_server)
        deadline = time.time() + 5
        while time.time() < deadline:
            try:
                request = urllib.request.Request(
                    f"http://127.0.0.1:{port}/ready",
                    method="OPTIONS",
                )
                urllib.request.urlopen(request, timeout=0.5).close()
                break
            except (OSError, urllib.error.URLError):
                time.sleep(0.05)
        else:
            self.fail("replacement service did not start")

        request = urllib.request.Request(
            f"http://127.0.0.1:{port}/replace",
            data=json.dumps(
                {
                    "token": token,
                    "replacements": {
                        "duplicate.a": "duplicate.b",
                        "duplicate.c": "duplicate.d",
                    },
                }
            ).encode("utf-8"),
            headers={"Content-Type": "application/json"},
            method="POST",
        )
        with urllib.request.urlopen(request, timeout=5) as response:
            payload = json.loads(response.read().decode("utf-8"))

        self.assertTrue(payload["ok"])
        self.assertEqual(payload["replacedOccurrences"], 2)
        self.assertEqual(payload["deletedKeys"], 2)
        self.assertEqual(payload["deletedEntries"], 6)
        updated_source = source_path.read_text(encoding="utf-8")
        self.assertIn("BI.i18nText('duplicate.b');", updated_source)
        self.assertIn("BI.i18nText('duplicate.d');", updated_source)
        for locale_name in ("zh_CN.json", "en_US.json", "zh_TW.json"):
            data = json.loads((root / "i18n" / locale_name).read_text(encoding="utf-8"))
            self.assertNotIn("duplicate.a", data)
            self.assertNotIn("duplicate.c", data)
            self.assertIn("duplicate.b", data)
            self.assertIn("duplicate.d", data)


if __name__ == "__main__":
    unittest.main()
