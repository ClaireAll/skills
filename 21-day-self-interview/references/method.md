# 方法论 / Methodology

> 这 21 天不是随便凑的题。它把几条成熟的心理学传统编织在一起，
> 折叠进一个普通人能坚持的节奏里。
> These 21 nights aren't a random pile of prompts. They braid several mature
> psychological traditions into a rhythm an ordinary person can actually keep.

## 为什么是「访谈」而不是「打卡」/ Why "interview", not "habit tracker"

打卡问"做到了吗"，访谈问"你是谁、你在往哪走"。前者改变行为，后者改变
**关系**——你和你自己的关系。行为的改变，往往是看清自己之后自然发生的副产品。

A tracker asks "did you do it?" An interview asks "who are you, and where are
you headed?" The first changes behavior; the second changes your *relationship*
with yourself. Behavioral change tends to follow, as a byproduct of seeing
clearly.

## 三阶段的逻辑 / The three-phase arc

```
看见 See (1-7)  →  理解 Understand (8-14)  →  选择 Choose (15-21)
观察当下           追溯成因                  夺回主动权
observe present    trace the causes          reclaim agency
```

顺序是刻意的。**先看见，再理解，最后才谈选择。** 跳过"看见"直接谈"你想成为
谁"，会得到一堆漂亮的空话；只有先诚实地看清现状、理解它从哪来，"选择"才有
重量。这也是为什么题目不能打乱顺序、不能由 AI 即兴发挥。

The order is deliberate. **See first, then understand, only then choose.**
Skip straight to "who do you want to be" and you get pretty, hollow answers.
Only after honestly seeing the present and understanding its origins does
"choice" carry weight. This is why the questions must not be reordered or
improvised.

## 借鉴的传统 / Traditions it draws on

- **存在主义心理学 / Existential psychology** (Yalom, Frankl, May)：自由与
  责任、有限性（死亡觉察）、意义、真实性。Day 16/17/18/20 直接来自这一脉。
  Freedom & responsibility, finitude, meaning, authenticity.

- **苏格拉底式提问 / Socratic questioning**：不给答案，用问题把人带到他自己
  早已知道、却没敢看的地方。整个 skill 的提问姿态。
  Never hand answers; use questions to lead people to what they already know
  but haven't dared look at.

- **正念式观察 / Mindful observation**：第一阶段"看见"不评判、只观察当下
  （时间、能量、注意力、身体），借自正念与接纳承诺疗法（ACT）的去融合。
  Phase one observes without judging — borrowed from mindfulness and ACT.

- **叙事疗法 / Narrative therapy**：Day 10「剧本」、Day 11「重复」——把人从
  "我就是这样"重写成"我继承了一个故事，而故事可以改写"。
  Rewriting "this is just who I am" into "I inherited a story, and stories can
  be rewritten."

- **习惯科学 / Habit science**：为什么是 21 天的*夜间仪式*而非一次性问卷——
  固定的时间锚点、低门槛（只是回答）、累积的可见进度，让人能坚持下来。
  A fixed nightly anchor, low friction, visible accumulation — so it sticks.

## 「镜子机制」是核心创新 / The "mirror mechanism" is the core idea

大多数自省工具的失败，在于它们**没有记忆**——你今天写的东西，明天就沉进
日记本里再没人看。这个 skill 把每晚的回答存进 `journal.json`，并在第 7/14/21
天强制 `recap`：AI 读回用户自己过去的原话，把碎片拼成一张画像还给他。

**被长时间地看见**，是人很少获得、却极其渴望的体验。这正是这个项目想给的东西。

Most self-reflection tools fail because they have **no memory** — what you
write today sinks into a notebook and is never seen again. This skill stores
every night in `journal.json` and forces a `recap` on Days 7/14/21: the AI
reads the user's *own past words* back to them and weaves the fragments into a
portrait. **Being seen over time** is something people rarely get and deeply
crave. That's what this project is built to give.

## 改编它 / Make it yours

题库是纯 JSON（`questions.zh.json` / `questions.en.json`），结构简单：每天一个
`theme`、一句 `opening`、三个 `questions`、一条给 AI 的 `mirror`。
你可以改问题、换语言、甚至改成 7 天 / 30 天的版本——只要保持"看见→理解→选择"
的递进，它就立得住。欢迎 PR 你的题库变体。

The question banks are plain JSON with a simple shape. Edit the questions,
add a language, fork it into a 7-day or 30-day version — as long as you keep
the "See → Understand → Choose" progression, it holds. PRs with your own
variants are welcome.
