# 安装与定时任务 / Setup & Scheduling

这个 skill 的精髓是**每晚自动来问你**。下面是把它接上定时任务的方法。
The magic is that it comes to you each night. Here's how to wire up the schedule.

## 1. 装上 skill / Install the skill

把这个仓库作为一个 Hermes skill 安装。最简单的方式是直接从仓库里的
`SKILL.md` 安装：
Install this repo as a Hermes skill — easiest via the `SKILL.md` URL:

```bash
hermes skills install https://raw.githubusercontent.com/Forlives/21-day-self-interview/main/SKILL.md
```

或者克隆到你的 skills 目录 / or clone into your skills dir:

```bash
git clone https://github.com/Forlives/21-day-self-interview.git \
  ~/.hermes/skills/21-day-self-interview
```

## 2. 开始旅程 / Start the journey

```bash
cd ~/.hermes/skills/21-day-self-interview   # 或你克隆的位置
python si.py init --lang zh                 # 或 --lang en
```

## 3. 设每晚的定时任务 / Set the nightly cron

最简单：直接在 Hermes 里用自然语言说。
Easiest: just tell Hermes in plain language.

```
每晚 22:00 加载 21-day-self-interview 这个 skill，
帮我做今天的自我访谈。
```

Hermes 会创建一个 cron job，每晚触发、加载本 skill、按当天的进度问你问题。
等价的显式命令：
Hermes creates a cron job that fires nightly, loads this skill, and runs the
day's prompt. The explicit equivalent:

```bash
hermes cron create "0 22 * * *" \
  --skills 21-day-self-interview \
  --prompt "现在是今晚的自我访谈时间。按 SKILL.md 的流程：先 python si.py prompt 取今天的问题（回映日先 recap），扮演存在主义心理咨询师一个个问我，结束时用 si.py record 记录我的回答。"
```

> ⏰ 时间锚点很重要。固定在你睡前的某个时刻，21 天才容易坚持下来。

## 4. 进度查看 / Check progress

```bash
python si.py status      # 进度条
python si.py recap        # 至今所有回答（你自己的私人记录）
```

## 状态存哪 / Where state lives

默认在 `~/.self-interview/`（可用环境变量 `SI_HOME` 改）：
- `state.json` — 语言、开始日期、进度
- `journal.json` — 你每晚的回答，**永久保留，只在本地**

这些文件已被 `.gitignore` 排除，**绝不会**被提交到仓库。你的回答只属于你。
These are gitignored and **never** committed. Your answers are yours alone.

## 常见问题 / FAQ

**Q：错过了一晚怎么办？**
天数按日历日推进。错过当晚不影响——下次 `prompt` 会给你当前日历对应的那天。
想补答某一天，用 `python si.py record --day N ...`。

**Q：能改成 7 天或 30 天吗？**
能。题库是 JSON，复制 `questions.zh.json` 改成你要的天数与主题即可，
保持「看见→理解→选择」的递进。欢迎 PR。

**Q：可以重新开始吗？**
`python si.py reset --yes`。会清空进度，但 `journal.json` 会自动备份。
