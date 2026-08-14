"""Flag common AI-writing patterns without deciding whether they are wrong."""

from __future__ import annotations

import argparse
import json
import re
import sys
from pathlib import Path
from typing import Final


Pattern = tuple[str, str, str, str]

PATTERNS: Final[tuple[Pattern, ...]] = (
    (
        "zh_reversal",
        "zh",
        r"(?:不是|并非|不在于|与其说|看似)[^。！？!?\n]{0,48}(?:而是|而在于|不如说|实则|其实)",
        "Avoid setting up a generic misconception only to overturn it. State the claim and support it directly.",
    ),
    (
        "zh_prompt_colon",
        "zh",
        r"(?:一句话总结|核心是|先说结论)\s*[:：]",
        "Replace prompt-like lead-ins with the actual point.",
    ),
    (
        "zh_signpost",
        "zh",
        r"(?:说白了|说穿了|值得注意的是|更微妙的是|还有一层)",
        "Use the supporting detail instead of announcing that an insight is coming.",
    ),
    (
        "zh_empty_significance",
        "zh",
        r"(?:标志着|体现了|证明了|彰显了|反映了)[^。！？!?\n]{0,36}(?:重要性|意义|价值|转变|进步)",
        "Check whether the claim says more than the available facts. Prefer the concrete change or responsibility.",
    ),
    (
        "zh_promotional_language",
        "zh",
        r"(?:令人叹为观止|必游之地|充满活力的|丰富的文化遗产|无缝(?:的)?|开创性的|卓越的体验)",
        "Check whether this is promotional language. Replace it with supported description or remove it.",
    ),
    (
        "zh_vague_attribution",
        "zh",
        r"(?:专家|行业报告|观察者|一些批评者|有关人士)(?:普遍)?(?:认为|指出|表示|显示|称)",
        "Name a supplied source when one exists; otherwise remove or qualify the unsupported attribution.",
    ),
    (
        "zh_chatbot_residue",
        "zh",
        r"(?:希望这对(?:你|您)有帮助|当然[！!]|当然，|请(?:随时)?告诉我|如果(?:你|您)还(?:需要|想要))",
        "Check whether chat-oriented wording was accidentally carried into the finished text.",
    ),
    (
        "zh_generic_positive_ending",
        "zh",
        r"(?:未来可期|值得期待|令人期待|迈出了?重要一步|开启(?:了)?(?:新的)?篇章|继续(?:向前|前行|追求卓越))",
        "Check whether the ending adds information. End on a concrete fact, decision, or open question when possible.",
    ),
    (
        "en_ai_vocabulary",
        "en",
        r"\b(?:pivotal|testament|vibrant|landscape|showcases?|delve|underscore|crucial)\b",
        "Check whether a plainer, more specific word says the same thing.",
    ),
    (
        "en_negative_parallelism",
        "en",
        r"\bnot\s+(?:just|only|merely)\b[^.!?\n]{0,80}\bbut\b",
        "State the point directly instead of framing it as a correction.",
    ),
    (
        "en_vague_attribution",
        "en",
        r"\b(?:experts|observers|industry reports|some critics)\s+(?:believe|argue|say|suggest)\b",
        "Name a source when one exists; otherwise remove or qualify the unsupported claim.",
    ),
    (
        "en_promotional_language",
        "en",
        r"\b(?:breathtaking|must-visit|groundbreaking|renowned|nestled)\b",
        "Replace promotional language with sourced description or remove it.",
    ),
    (
        "en_chatbot_residue",
        "en",
        r"\b(?:i hope this helps|feel free to (?:ask|reach out)|let me know if)\b",
        "Check whether chat-oriented wording was accidentally carried into the finished text.",
    ),
    (
        "en_generic_positive_ending",
        "en",
        r"\b(?:the future looks bright|exciting times (?:lie|are) ahead|an important step in the right direction)\b",
        "Check whether the ending adds information. End on a concrete fact, decision, or open question when possible.",
    ),
    (
        "en_excessive_hedging",
        "en",
        r"\b(?:could potentially|may possibly|might perhaps)\b",
        "Use one level of uncertainty unless the source requires more precise qualification.",
    ),
    (
        "em_dash",
        "both",
        r"[—–]",
        "Check whether a period, comma, parenthesis, or a simpler sentence reads better for this voice.",
    ),
)


def _line_number(text: str, offset: int) -> int:
    return text.count("\n", 0, offset) + 1


def audit_text(text: str, language: str = "auto") -> list[dict[str, object]]:
    """Return one actionable finding per matched pattern category."""

    if language not in {"auto", "zh", "en"}:
        raise ValueError("language must be one of: auto, zh, en")

    enabled_languages = {"zh", "en"} if language == "auto" else {language}
    findings: list[dict[str, object]] = []

    for code, applies_to, expression, advice in PATTERNS:
        if applies_to != "both" and applies_to not in enabled_languages:
            continue

        match = re.search(expression, text, flags=re.IGNORECASE)
        if match is None:
            continue

        findings.append(
            {
                "code": code,
                "line": _line_number(text, match.start()),
                "match": match.group(0),
                "advice": advice,
            }
        )

    return findings


def _format_text_report(path: Path, findings: list[dict[str, object]]) -> str:
    if not findings:
        return f"{path}: no configured patterns found"

    lines = [f"{path}: {len(findings)} pattern(s) to review"]
    for finding in findings:
        lines.append(
            f"L{finding['line']} [{finding['code']}] {finding['match']}\n"
            f"  {finding['advice']}"
        )
    return "\n".join(lines)


def _configure_utf8_stdout() -> None:
    """Keep JSON and text reports readable when Windows defaults to a legacy code page."""

    reconfigure = getattr(sys.stdout, "reconfigure", None)
    if callable(reconfigure):
        reconfigure(encoding="utf-8")


def main() -> int:
    _configure_utf8_stdout()
    parser = argparse.ArgumentParser(
        description="Flag selected Chinese and English AI-writing patterns for human review."
    )
    parser.add_argument("path", type=Path, help="UTF-8 text or Markdown file to audit")
    parser.add_argument(
        "--language",
        choices=("auto", "zh", "en"),
        default="auto",
        help="Pattern set to use (default: auto, checks both sets)",
    )
    parser.add_argument(
        "--format",
        choices=("text", "json"),
        default="text",
        help="Report format (default: text)",
    )
    args = parser.parse_args()

    text = args.path.read_text(encoding="utf-8-sig")
    findings = audit_text(text, language=args.language)

    if args.format == "json":
        print(
            json.dumps(
                {"path": str(args.path), "language": args.language, "findings": findings},
                ensure_ascii=False,
                indent=2,
            )
        )
    else:
        print(_format_text_report(args.path, findings))

    return 0


if __name__ == "__main__":
    raise SystemExit(main())
