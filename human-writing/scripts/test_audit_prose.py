"""Regression tests for the deterministic prose-audit helper."""

from __future__ import annotations

import importlib.util
import json
import os
import subprocess
import sys
import tempfile
import unittest
from pathlib import Path


SCRIPT_PATH = Path(__file__).with_name("audit_prose.py")


def load_auditor():
    spec = importlib.util.spec_from_file_location("audit_prose", SCRIPT_PATH)
    if spec is None or spec.loader is None:
        raise RuntimeError("Could not load audit_prose.py")

    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


class AuditProseTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls) -> None:
        cls.auditor = load_auditor()

    def test_detects_chinese_reversal_and_prompt_colon(self) -> None:
        findings = self.auditor.audit_text(
            "这不是一次普通更新，而是一次系统性重构。\n一句话总结：先做审计。",
            language="zh",
        )

        self.assertEqual(
            {finding["code"] for finding in findings},
            {"zh_reversal", "zh_prompt_colon"},
        )

    def test_detects_english_ai_patterns(self) -> None:
        findings = self.auditor.audit_text(
            "This pivotal release showcases a vibrant new landscape. "
            "It is not just faster, but more reliable.",
            language="en",
        )

        self.assertEqual(
            {finding["code"] for finding in findings},
            {"en_ai_vocabulary", "en_negative_parallelism"},
        )

    def test_detects_humanizer_inspired_chinese_patterns(self) -> None:
        findings = self.auditor.audit_text(
            "这标志着产品创新的重要转变。行业报告显示它提供无缝体验。"
            "希望这对您有帮助，未来可期。",
            language="zh",
        )

        self.assertEqual(
            {finding["code"] for finding in findings},
            {
                "zh_empty_significance",
                "zh_promotional_language",
                "zh_vague_attribution",
                "zh_chatbot_residue",
                "zh_generic_positive_ending",
            },
        )

    def test_detects_chat_residue_and_generic_english_ending(self) -> None:
        findings = self.auditor.audit_text(
            "I hope this helps. The future looks bright, and this could potentially help.",
            language="en",
        )

        self.assertEqual(
            {finding["code"] for finding in findings},
            {
                "en_chatbot_residue",
                "en_generic_positive_ending",
                "en_excessive_hedging",
            },
        )

    def test_auto_mode_checks_mixed_chinese_and_english_text(self) -> None:
        findings = self.auditor.audit_text(
            "看似很简单，实则非常复杂。 This is a testament to progress.",
            language="auto",
        )

        self.assertEqual(
            {finding["code"] for finding in findings},
            {"zh_reversal", "en_ai_vocabulary"},
        )

    def test_does_not_flag_plain_technical_text(self) -> None:
        findings = self.auditor.audit_text(
            "The API returns the selected record.\n接口返回当前选中的记录。",
            language="auto",
        )

        self.assertEqual(findings, [])

    def test_cli_emits_json_for_a_utf8_file(self) -> None:
        with tempfile.TemporaryDirectory() as temp_dir:
            draft_path = Path(temp_dir) / "draft.md"
            draft_path.write_text("说白了，这不是功能，而是姿势。", encoding="utf-8")

            environment = os.environ.copy()
            environment.pop("PYTHONUTF8", None)
            environment.pop("PYTHONIOENCODING", None)
            result = subprocess.run(
                [sys.executable, str(SCRIPT_PATH), str(draft_path), "--format", "json"],
                check=True,
                capture_output=True,
                text=True,
                encoding="utf-8",
                env=environment,
            )

        report = json.loads(result.stdout)
        self.assertEqual(report["language"], "auto")
        self.assertEqual(
            {finding["code"] for finding in report["findings"]},
            {"zh_reversal", "zh_signpost"},
        )


if __name__ == "__main__":
    unittest.main()
