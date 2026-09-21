# Codex Skills

更新日期：2026-09-16

个人 skill 根目录：`D:\Claire\skills`。Codex 默认发现路径 `C:\Users\Claire\.codex\skills` 是指向这里的 junction，因此本仓库是本地 skill 的唯一维护入口。

这里维护本地 personal 与 `.system` skills，并记录当前会话可用 skill 的名称快照。插件提供的 skills 会随 Codex 会话和插件版本变化；实际调用以前，以当前会话的可用 skill 列表为准。

## 当前会话可用 Skill 名称

以 2026-09-04 的会话快照为基础，当前新增本地 `interaction-guide`、`test-skill`、`21-day-self-interview` 与 `life-design`，并安装 `fx-workflow` 插件，索引合计 **82** 个 skill；插件部分以安装状态为准，实际调用项以新会话发现结果为准。

| 来源 | 数量 | Skill 名称 |
| --- | ---: | --- |
| 本地 personal | 21 | `21-day-self-interview`、`archify`、`bdd-onboarding`、`bug-des`、`bug-memory-workflow`、`bugfix`、`feishu-doc-writer`、`find-skills`<br>`fixing-accessibility`、`fixing-metadata`、`fixing-motion-performance`、`frontend-code-review`、`human-writing`、`i18n-helper`、`interaction-guide`、`life-design`<br>`require-understand`、`resolving-merge-conflicts`、`test-skill`、`to-questionnaire`、`ui` |
| 本地 `.system` | 5 | `imagegen`、`openai-docs`、`plugin-creator`、`skill-creator`、`skill-installer` |
| FXDATA BDD 插件 | 3 | `fx-bdd:bdd`、`fx-data-test-skills:read-feature-input`、`fx-data-test-skills:test-plan-generator` |
| FX Workflow 插件 | 4 | `fx-workflow:dev-doc-writer`、`fx-workflow:feishu-mcp-reauth`、`fx-workflow:reading-kms-confluence-pages`、`fx-workflow:work-log` |
| Figma 插件 | 12 | `figma:figma-code-connect`、`figma:figma-create-new-file`、`figma:figma-design-to-code`、`figma:figma-generate-design`、`figma:figma-generate-diagram`、`figma:figma-generate-library`、`figma:figma-implement-motion`、`figma:figma-swiftui`<br>`figma:figma-use`、`figma:figma-use-figjam`、`figma:figma-use-motion`、`figma:figma-use-slides` |
| OpenAI 开发者插件 | 5 | `openai-developers:agents-sdk`、`openai-developers:build-chatgpt-app`、`openai-developers:chatgpt-app-submission`、`openai-developers:openai-api-troubleshooting`、`openai-developers:openai-platform-api-key` |
| 文档与表格能力 | 6 | `documents:documents`、`pdf:pdf`、`presentations:Presentations`、`spreadsheets:Spreadsheets`、`spreadsheets:excel-live-control`、`template-creator:template-creator` |
| 插件管理 | 1 | `plugin-management:plugin-management` |
| Ponytail 插件 | 6 | `ponytail:ponytail`、`ponytail:ponytail-audit`、`ponytail:ponytail-debt`、`ponytail:ponytail-gain`、`ponytail:ponytail-help`、`ponytail:ponytail-review` |
| Product Design 插件 | 5 | `product-design:audit`、`product-design:ideate`、`product-design:image-to-code`、`product-design:index`、`product-design:url-to-code` |
| Superpowers 插件 | 14 | `superpowers:brainstorming`、`superpowers:dispatching-parallel-agents`、`superpowers:executing-plans`、`superpowers:finishing-a-development-branch`、`superpowers:receiving-code-review`、`superpowers:requesting-code-review`、`superpowers:subagent-driven-development`、`superpowers:systematic-debugging`<br>`superpowers:test-driven-development`、`superpowers:using-git-worktrees`、`superpowers:using-superpowers`、`superpowers:verification-before-completion`、`superpowers:writing-plans`、`superpowers:writing-skills` |

`review-agent` 未计入上述索引；系统技能是否存在及是否可调用，以本机目录和会话发现结果为准。

## 使用原则

- 优先选择职责清晰、覆盖完整任务的最小入口。
- `require-understand` 会按目标自动加载需求理解模块；需要把他人掌握的需求缺口整理成问卷时调用 `to-questionnaire`，生成测试计划时自动追加测试计划模块。
- `interaction-guide` 是源码交互 HTML 说明的入口，配合 `require-understand` 核对行为、配合 `archify` 展示流程；默认独立子流程、右侧详情和悬浮关联线高亮，内容覆盖与页面验证分开验收。
- `test-skill` 用于根据当前迭代、需求、分支或 PR 生成转测前的开发自测、手动自查用例和提测检查清单。
- `ui` 会按目标自动加载一个或多个 UI 内部模块；明确的小任务不必加载宽泛路由上下文。
- `bugfix` 是 `fv-web2 / fx-data-web` 的唯一缺陷交付编排器；它取代已移除的 `fx-data-web-bugfix-workflow`，并调用 `bug-memory-workflow` 与 `bug-des`，这些 skill 仍可独立使用。
- 只有脚本产生的缓存、报告和构建输出应被忽略；skill 源码、模板和验证脚本应留在版本控制中。

## 需求、文档与计划

| Skill | 适用场景 |
| --- | --- |
| `find-skills` | 本地没有合适能力时，发现和安装可复用 skill。 |
| [`interaction-guide`](interaction-guide/SKILL.md) | 根据指定源码逐动作整理可点击 HTML 交互说明；覆盖实际文案、环境权限、置灰 tooltip、异步状态及字段级分支，支持分块补充现有文档和核对遗漏。 |
| `require-understand` | 读取、对齐飞书、Figma、本地文档或混合需求输入；可将指定源码与交互文档逐项对照并就地标注矛盾或遗漏；需要时将他人掌握的需求缺口转成交付问卷，或串联测试场景、脑图与回填流程。 |
| `to-questionnaire` | 将只有产品、测试、开发或其他特定人员能回答的需求缺口整理为结构化 Markdown 问卷；普通澄清问题不会触发。 |
| `feishu-doc-writer` | 创建、更新或核验飞书/Lark 文档和 wiki 页面。 |

## BDD 流水线

| Skill | 适用场景 |
| --- | --- |
| `bdd-onboarding` | 接入或巡检 FXDATA 跨仓库 BDD 流水线：校验插件依赖、准备 harness 与产品仓归档，并在执行前完成 `doctor`。 |
| `fx-bdd:bdd`（Codex 插件） | 官方 BDD 流水线执行入口，负责初始化、`doctor`、需求到可执行场景的完整编排。首次安装或更新插件后必须新开 Codex 会话，再以 `$fx-bdd:bdd` 调用。 |

本机已接入 `fx-data-test-skills` 与 `fx-bdd` 两个插件，二者必须同时保持 `installed, enabled`。`fx-data-test-skills` 是前置依赖；不要只安装 `fx-bdd`。用 `codex plugin list -m fx-data-test-skills` 和 `codex plugin list -m skill-manager` 复核状态。

## 飞书与内部工作流

| Skill | 适用场景 | 调用示例 |
| --- | --- | --- |
| `fx-workflow:feishu-mcp-reauth` | 检查或续期飞书文档 MCP 链接；默认无头执行，登录态失效时才打开 Chrome。 | `$fx-workflow:feishu-mcp-reauth 检查飞书 MCP 有效期` 或 `$fx-workflow:feishu-mcp-reauth 重新授权飞书 MCP`。 |
| `fx-workflow:work-log` | 从 Bitbucket 已合并 PR 汇总每日工作内容与工时，并提交到飞书项目。首次使用需要配置空间 ID、用户 ID 和兜底工作项。 | `$fx-workflow:work-log 记录本周工作日志`。 |

`fx-workflow` 以插件形式安装，因此同时提供 `fx-workflow:dev-doc-writer` 与 `fx-workflow:reading-kms-confluence-pages`；新安装的插件 skill 需要在新会话中加载。

## 产品与界面设计

| Skill | 适用场景 |
| --- | --- |
| `ui` | 统一入口：自动选择 UI 路由、快速视觉整理、前端设计、`DESIGN.md`、设计语言或只读 UI 审查模块，并可组合需要的模块。 |

## 架构与图表

| Skill | 适用场景 |
| --- | --- |
| `archify` | 将系统说明、仓库代码或 Mermaid 转为经过校验的独立 HTML 架构图、流程图、时序图、数据流图或生命周期图；适合技术方案梳理、代码架构盘点、接口调用链和部署边界说明。 |

## 写作与内容

| Skill | 适用场景 |
| --- | --- |
| `human-writing` | 新写、改写或审计中文优先的内容；保留作者声音，不编造事实，并检查中英文常见 AI 写作痕迹。 |

## 自我探索与人生设计

| Skill | 适用场景 | 调用示例 |
| --- | --- | --- |
| `21-day-self-interview` | 连续 21 天、每天三个问题的渐进式自我访谈；第 7、14、21 天回顾此前回答。记录默认保存在 `D:\Claire\memory\self-interview`。 | `$21-day-self-interview 开始 21 天自我访谈，使用中文`；之后说“继续今晚的自我访谈”或“查看访谈进度”。 |
| `life-design` | 针对职业、生活重心或未来方向进行 6–9 轮访谈，形成三条五年路径及低成本验证行动。仅在明确调用时使用。 | `$life-design 帮我做一次人生设计，重点梳理未来五年的职业方向`。 |

## 前端质量

| Skill | 适用场景 |
| --- | --- |
| `frontend-code-review` | 审查前端代码中的缺陷、回归和交互风险。 |
| `fixing-accessibility` | 修复 ARIA、键盘、焦点、对比度和表单可访问性问题。 |
| `fixing-metadata` | 完善 SEO、Open Graph、canonical、结构化数据和 robots 元数据。 |
| `fixing-motion-performance` | 排查和修复动画、滚动联动和模糊效果的性能问题。 |
| `i18n-helper` | 检查 JS/TS i18n JSON 的未使用 key、重复值和误报风险。 |

## 测试协作

| Skill | 适用场景 |
| --- | --- |
| `test-skill` | 根据当前迭代、需求、分支或 PR 生成转测前的开发自测、手动自查用例或提测检查清单；默认不执行测试、不编写 BDD 用例、不修改业务代码。 |

## 缺陷协作与交付

| Skill | 适用场景 |
| --- | --- |
| `bug-memory-workflow` | Bug 修复、调查或 review 前检索已确认的历史经验。 |
| `bugfix` | `fv-web2 / fx-data-web` 的修复、review gate、Feishu、Bitbucket PR 与交付流程。 |
| `bug-des` | 基于 issue 与 diff 生成中文 Feishu 缺陷评论或 PR 描述。 |

## Git 协作

| Skill | 适用场景 |
| --- | --- |
| `resolving-merge-conflicts` | 处理正在进行的 Git merge 或 rebase 冲突：追溯双方提交、PR 或工单意图，逐段合并并完成项目校验，而不是机械保留某一侧。 |

## 系统 Skills

`.system` 下的安装和平台能力保持独立：`imagegen`、`openai-docs`、`plugin-creator`、`review-agent`、`skill-creator`、`skill-installer`。除非明确维护平台能力，不要删除或合并它们。

## 预选 Skill

| Skill | 后续可能使用的能力 | 当前状态 |
| --- | --- | --- |
| `diagram-design` | 生成 editorial 风格的 HTML/SVG/PNG 图表；支持流程图、用户旅程、泳道图、状态图，并可导入 Mermaid、draw.io 和 Excalidraw。 | 尚未安装；需要高质量静态图表或飞书文档配图时使用 |
| `interaction-guide` | 根据源码生成详细交互说明、HTML 模拟页面预览、流程节点与页面状态联动，以及权限、空状态、加载和失败场景。 | 已安装；交互文档和页面预览 |
| `archify` | 生成经过校验的架构图、流程图、时序图、数据流图和生命周期图，并输出独立 HTML。 | 已安装；技术流程和结构图 |
| `feishu-doc-writer` | 根据 Markdown 创建、更新和回读验证飞书文档或 Wiki；后续可接入图表图片插入。 | 已安装；飞书文档交付 |
| `figma:figma-generate-diagram` | 将 Mermaid 生成可编辑的 FigJam 流程图、架构图、时序图、状态图或 ER 图。 | 已安装插件；需要 FigJam 协作时使用 |
| `fx-bdd:bdd` | 根据产品和交互文档生成 Gherkin 用例，并接入 FXDATA BDD 执行流程。 | 已安装插件；需要可执行验收场景时使用 |
