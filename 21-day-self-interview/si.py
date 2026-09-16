#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
si.py — 21 Days of Self-Interview / 21 天自我访谈
A tiny, dependency-free state machine for a 21-night guided self-inquiry.

The AI agent (Hermes, or any agent that can run a shell command + read JSON)
calls this script each night to fetch the day's prompt, and after the
conversation, records the user's answers. Everything is plain stdlib so the
repo runs anywhere Python 3.8+ exists.

Usage:
  python si.py init [--lang zh|en] [--start YYYY-MM-DD]
  python si.py prompt            # what to ask tonight (JSON for the agent)
  python si.py status            # human-readable progress
  python si.py record --day N --file answers.txt   # save the night's answers
  python si.py record --day N --text "..."
  python si.py recap [--day N]   # past answers + mirror notes for reflection
  python si.py reset --yes       # wipe local state (keeps the journal backup)

State lives in $SI_HOME or D:/Claire/memory/self-interview/ :
  state.json     progress + config
  journal.json   every night's answers, kept forever
"""
import argparse, datetime, json, os, sys, pathlib

VERSION = "1.0.0"

def repo_root() -> pathlib.Path:
    return pathlib.Path(__file__).resolve().parent

def home() -> pathlib.Path:
    env = os.environ.get("SI_HOME")
    base = pathlib.Path(env) if env else repo_root().parent.parent / "memory" / "self-interview"
    base.mkdir(parents=True, exist_ok=True)
    return base

def load_questions(lang: str) -> dict:
    f = repo_root() / f"questions.{lang}.json"
    if not f.exists():
        f = repo_root() / "questions.zh.json"
    return json.loads(f.read_text(encoding="utf-8"))

def state_path() -> pathlib.Path:
    return home() / "state.json"

def journal_path() -> pathlib.Path:
    return home() / "journal.json"

def load_state():
    p = state_path()
    if not p.exists():
        return None
    return json.loads(p.read_text(encoding="utf-8"))

def save_state(st: dict):
    state_path().write_text(json.dumps(st, ensure_ascii=False, indent=2), encoding="utf-8")

def load_journal() -> dict:
    p = journal_path()
    if not p.exists():
        return {}
    return json.loads(p.read_text(encoding="utf-8"))

def save_journal(j: dict):
    journal_path().write_text(json.dumps(j, ensure_ascii=False, indent=2), encoding="utf-8")

def today() -> datetime.date:
    return datetime.date.today()

def current_day(st: dict) -> int:
    """Day number 1..21 based on calendar days since start. Capped at 21."""
    start = datetime.date.fromisoformat(st["start_date"])
    delta = (today() - start).days
    return max(1, min(21, delta + 1))

# ---------- commands ----------

def cmd_init(args):
    existing = load_state()
    if existing and not args.force:
        print(json.dumps({
            "ok": False,
            "msg": "已存在进行中的自我访谈。用 `si.py status` 查看，或 `si.py reset --yes` 重新开始。"
                   " / A journey is already in progress. Use status, or reset --yes to restart.",
            "state": existing,
        }, ensure_ascii=False))
        return
    start = args.start or today().isoformat()
    st = {
        "version": VERSION,
        "lang": args.lang,
        "start_date": start,
        "created_at": datetime.datetime.now().isoformat(timespec="seconds"),
        "completed_days": [],
    }
    save_state(st)
    if not journal_path().exists():
        save_journal({})
    q = load_questions(args.lang)
    print(json.dumps({
        "ok": True,
        "msg": f"已开始《{q['title']}》。第一晚从 {start} 起。 / Started '{q['title']}'. Day 1 begins {start}.",
        "state": st,
    }, ensure_ascii=False))

def _day_block(q, n):
    for d in q["days"]:
        if d["day"] == n:
            return d
    return None

def _phase_for(q, n):
    for ph in q["phases"]:
        lo, hi = ph["range"]
        if lo <= n <= hi:
            return ph
    return None

def cmd_prompt(args):
    st = load_state()
    if not st:
        print(json.dumps({"ok": False, "msg": "尚未开始。先运行 init。 / Not started. Run init first."}, ensure_ascii=False))
        return
    n = current_day(st)
    q = load_questions(st["lang"])
    day = _day_block(q, n)
    phase = _phase_for(q, n)
    journal = load_journal()
    done = str(n) in journal
    out = {
        "ok": True,
        "day": n,
        "total": 21,
        "already_answered_today": done,
        "lang": st["lang"],
        "title": q["title"],
        "phase": {"id": phase["id"], "name": phase["name"], "intent": phase["intent"]},
        "theme": day["theme"],
        "opening": day["opening"],
        "questions": day["questions"],
        "mirror_note_for_agent": day["mirror"],
        "recap_available": [int(k) for k in journal.keys()],
    }
    print(json.dumps(out, ensure_ascii=False))

def cmd_status(args):
    st = load_state()
    if not st:
        print("尚未开始任何自我访谈。运行：python si.py init / No journey yet. Run: python si.py init")
        return
    n = current_day(st)
    q = load_questions(st["lang"])
    journal = load_journal()
    phase = _phase_for(q, n)
    answered = sorted(int(k) for k in journal.keys())
    bar = "".join("●" if (i+1) in answered else ("◐" if (i+1)==n else "○") for i in range(21))
    print(f"《{q['title']}》  v{st['version']}  [{st['lang']}]")
    print(f"开始 / Start: {st['start_date']}   今天 / Today: Day {n}/21   阶段 / Phase: {phase['name']}")
    print(f"进度 / Progress: {bar}  ({len(answered)}/21 答过 answered)")
    if answered:
        print(f"已记录 / Recorded days: {answered}")

def cmd_record(args):
    st = load_state()
    if not st:
        print(json.dumps({"ok": False, "msg": "尚未开始。 / Not started."}, ensure_ascii=False)); return
    n = args.day or current_day(st)
    if args.file:
        text = pathlib.Path(args.file).read_text(encoding="utf-8")
    else:
        text = args.text or ""
    if not text.strip():
        print(json.dumps({"ok": False, "msg": "没有内容可记录。 / Nothing to record."}, ensure_ascii=False)); return
    q = load_questions(st["lang"])
    day = _day_block(q, n)
    journal = load_journal()
    journal[str(n)] = {
        "day": n,
        "theme": day["theme"],
        "date": today().isoformat(),
        "recorded_at": datetime.datetime.now().isoformat(timespec="seconds"),
        "questions": day["questions"],
        "answers": text.strip(),
    }
    save_journal(journal)
    if n not in st["completed_days"]:
        st["completed_days"].append(n)
        st["completed_days"].sort()
    save_state(st)
    print(json.dumps({"ok": True, "msg": f"已记录 Day {n}（{day['theme']}）。 / Recorded Day {n}.", "completed": st["completed_days"]}, ensure_ascii=False))

def cmd_recap(args):
    st = load_state()
    if not st:
        print(json.dumps({"ok": False, "msg": "尚未开始。 / Not started."}, ensure_ascii=False)); return
    journal = load_journal()
    if args.day:
        entries = [journal[str(args.day)]] if str(args.day) in journal else []
    else:
        entries = [journal[k] for k in sorted(journal, key=lambda x: int(x))]
    print(json.dumps({"ok": True, "count": len(entries), "entries": entries}, ensure_ascii=False))

def cmd_reset(args):
    if not args.yes:
        print(json.dumps({"ok": False, "msg": "需要 --yes 确认。这会清空进度（journal 会备份）。 / Pass --yes. Clears progress (journal is backed up)."}, ensure_ascii=False)); return
    # back up journal before wiping
    jp = journal_path()
    if jp.exists():
        ts = datetime.datetime.now().strftime("%Y%m%d_%H%M%S")
        backup = home() / f"journal.backup.{ts}.json"
        backup.write_text(jp.read_text(encoding="utf-8"), encoding="utf-8")
    if state_path().exists():
        state_path().unlink()
    print(json.dumps({"ok": True, "msg": "已重置。journal 已备份。 / Reset done. Journal backed up."}, ensure_ascii=False))

def main():
    ap = argparse.ArgumentParser(prog="si.py", description="21 Days of Self-Interview state machine")
    ap.add_argument("--version", action="version", version=f"si.py {VERSION}")
    sub = ap.add_subparsers(dest="cmd", required=True)

    p = sub.add_parser("init", help="start a new 21-day journey")
    p.add_argument("--lang", choices=["zh", "en"], default="zh")
    p.add_argument("--start", help="start date YYYY-MM-DD (default: today)")
    p.add_argument("--force", action="store_true", help="overwrite existing state")
    p.set_defaults(func=cmd_init)

    p = sub.add_parser("prompt", help="tonight's prompt as JSON (for the agent)")
    p.set_defaults(func=cmd_prompt)

    p = sub.add_parser("status", help="human-readable progress")
    p.set_defaults(func=cmd_status)

    p = sub.add_parser("record", help="save tonight's answers")
    p.add_argument("--day", type=int)
    p.add_argument("--file")
    p.add_argument("--text")
    p.set_defaults(func=cmd_record)

    p = sub.add_parser("recap", help="dump past answers for reflection")
    p.add_argument("--day", type=int)
    p.set_defaults(func=cmd_recap)

    p = sub.add_parser("reset", help="wipe local state")
    p.add_argument("--yes", action="store_true")
    p.set_defaults(func=cmd_reset)

    args = ap.parse_args()
    args.func(args)

if __name__ == "__main__":
    main()
