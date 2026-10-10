# Codex Skills

更新日期：2026-10-10

个人 skill 根目录：`D:\Claire\skills`。Codex 默认发现路径 `C:\Users\Claire\.codex\skills` 是指向这里的 junction，因此本仓库是本地 skill 的唯一维护入口。

这里维护本地 personal 与 `.system` skills，并记录当前会话可用 skill 的名称快照。插件提供的 skills 会随 Codex 会话和插件版本变化；实际调用以前，以当前会话的可用 skill 列表为准。

## 当前会话可用 Skill 名称

以已提交索引为基础，本次将需求与测试入口收敛为 claire-require、claire-test，并新增 webapp-testing 和规格对照插件，索引合计 **85** 个 skill；插件部分以安装状态为准，实际调用项以新会话发现结果为准。

| 来源 | 数量 | Skill 名称 |
| --- | ---: | --- |
| 本地 personal | 23 | `21-day-self-interview`、`archify`、`bdd-onboarding`、`bug-des`、`bug-memory-workflow`、`bugfix`、`codex-session-timeline`、`feishu-doc-writer`、`find-skills`<br>`fixing-accessibility`、`fixing-metadata`、`fixing-motion-performance`、`frontend-code-review`、`human-writing`、`i18n-helper`、`interaction-guide`、`life-design`<br>`claire-require`、`resolving-merge-conflicts`、`claire-test`、`to-questionnaire`、`ui`、`webapp-testing` |
| 本地 `.system` | 5 | `imagegen`、`openai-docs`、`plugin-creator`、`skill-creator`、`skill-installer` |
| FXDATA BDD 插件 | 3 | `fx-bdd:bdd`、`fx-data-test-skills:read-feature-input`、`fx-data-test-skills:test-plan-generator` |
| FX Workflow 插件 | 4 | `fx-workflow:dev-doc-writer`、`fx-workflow:feishu-mcp-reauth`、`fx-workflow:reading-kms-confluence-pages`、`fx-workflow:work-log` |
| Figma 插件 | 12 | `figma:figma-code-connect`、`figma:figma-create-new-file`、`figma:figma-design-to-code`、`figma:figma-generate-design`、`figma:figma-generate-diagram`、`figma:figma-generate-library`、`figma:figma-implement-motion`、`figma:figma-swiftui`<br>`figma:figma-use`、`figma:figma-use-figjam`、`figma:figma-use-motion`、`figma:figma-use-slides` |
| OpenAI 开发者插件 | 5 | `openai-developers:agents-sdk`、`openai-developers:build-chatgpt-app`、`openai-developers:chatgpt-app-submission`、`openai-developers:openai-api-troubleshooting`、`openai-developers:openai-platform-api-key` |
| 文档与表格能力 | 6 | `documents:documents`、`pdf:pdf`、`presentations:Presentations`、`spreadsheets:Spreadsheets`、`spreadsheets:excel-live-control`、`template-creator:template-creator` |
| 插件管理 | 1 | `plugin-management:plugin-management` |
| Ponytail 插件 | 6 | `ponytail:ponytail`、`ponytail:ponytail-audit`、`ponytail:ponytail-debt`、`ponytail:ponytail-gain`、`ponytail:ponytail-help`、`ponytail:ponytail-review` |
| Product Design 插件 | 5 | `product-design:audit`、`product-design:ideate`、`product-design:image-to-code`、`product-design:index`、`product-design:url-to-code` |
| 规格对照插件 | 1 | `spec-to-code-compliance:spec-to-code-compliance` |
| Superpowers 插件 | 14 | `superpowers:brainstorming`、`superpowers:dispatching-parallel-agents`、`superpowers:executing-plans`、`superpowers:finishing-a-development-branch`、`superpowers:receiving-code-review`、`superpowers:requesting-code-review`、`superpowers:subagent-driven-development`、`superpowers:systematic-debugging`<br>`superpowers:test-driven-development`、`superpowers:using-git-worktrees`、`superpowers:using-superpowers`、`superpowers:verification-before-completion`、`superpowers:writing-plans`、`superpowers:writing-skills` |

`review-agent` 未计入上述索引；系统技能是否存在及是否可调用，以本机目录和会话发现结果为准。

## 使用原则

- 优先选择职责清晰、覆盖完整任务的最小入口。
- `claire-require` 负责读懂飞书、Figma、本地资料与需求说明，澄清验收规则和开发注意点；不再内置测试计划生成器。
- `claire-test` 默认只读审查需求与源码，结合规格对照与实际边界给出代码问题、修改方案和手动验证步骤；用户自行修改。要求自查用例时才生成完整清单。
- `webapp-testing` 保持独立，仅在明确点名时实测页面；普通审查不自动运行浏览器、不添加 test-id、不修改业务源码。
- `interaction-guide` 是源码交互 HTML 说明的入口，配合 `claire-require` 核对行为、配合 `archify` 展示流程；默认独立子流程、右侧详情和悬浮关联线高亮，内容覆盖与页面验证分开验收。
- `ui` 会按目标自动加载一个或多个 UI 内部模块；明确的小任务不必加载宽泛路由上下文。
- `bugfix` 是 `fv-web2 / fx-data-web` 的唯一缺陷交付编排器；它取代已移除的 `fx-data-web-bugfix-workflow`，并调用 `bug-memory-workflow` 与 `bug-des`，这些 skill 仍可独立使用。
- 只有脚本产生的缓存、报告和构建输出应被忽略；skill 源码、模板和验证脚本应留在版本控制中。

## 需求、文档与计划

| Skill | 适用场景 |
| --- | --- |
| `find-skills` | 本地没有合适能力时，发现和安装可复用 skill。 |
| [`interaction-guide`](interaction-guide/SKILL.md) | 根据指定源码逐动作整理可点击 HTML 交互说明；覆盖实际文案、环境权限、置灰 tooltip、异步状态及字段级分支，支持分块补充现有文档和核对遗漏。 |
| [`claire-require`](claire-require/SKILL.md) | 读取、对齐飞书、Figma、本地文档或文字需求，整理验收标准、状态、权限、开发注意点和待确认项；保留明确要求时的交互文档对齐及同步，正式代码问题审查交给 `claire-test`。 |
| `to-questionnaire` | 将只有产品、测试、开发或其他特定人员能回答的需求缺口整理为结构化 Markdown 问卷；普通澄清问题不会触发。 |
| `feishu-doc-writer` | 创建、更新或核验飞书/Lark 文档和 wiki 页面。 |

## BDD 流水线

| Skill | 适用场景 |
| --- | --- |
| `bdd-onboarding` | 接入或巡检 FXDATA 跨仓库 BDD 流水线：校验插件依赖、准备 harness 与产品仓归档，并在执行前完成 `doctor`。 |
| `fx-bdd:bdd`（Codex 插件） | 官方 BDD 流水线执行入口，负责初始化、`doctor`、需求到可执行场景的完整编排。首次安装或更新插件后必须新开 Codex 会话，再以 `$fx-bdd:bdd` 调用。 |

本机已接入 `fx-data-test-skills` 与 `fx-bdd` 两个插件，二者必须同时保持 `installed, enabled`。`fx-data-test-skills` 是前置依赖；不要只安装 `fx-bdd`。用 `codex plugin list -m fx-data-test-skills` 和 `codex plugin list -m skill-manager` 复核状态。

这两个插件保留，但只在用户明确要求 BDD 流程或点名其 BDD 入口时调用。普通需求读取、辅助开发、源码审查、自查用例生成和页面测试不调用 `fx-bdd:*` 或 `fx-data-test-skills:*`；其通用关键词触发说明不覆盖该偏好。

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
| [`claire-test`](claire-test/SKILL.md) | 默认对照需求与源码，复用 `spec-to-code-compliance`，补查相关边界并给出问题、触发条件、源码证据、修改方案和手动验证步骤；不改代码、不自动运行页面。用户要求时也能生成转测自查用例。 |
| [`webapp-testing`](webapp-testing/SKILL.md) | Anthropic 官方页面测试工具：明确点名时使用 Python Playwright 操作真实页面、截图和收集日志，通过现有文案、角色和 DOM 定位；无需为审查补 test-id。 |
| [`spec-to-code-compliance:spec-to-code-compliance`](.plugins/spec-to-code-compliance/skills/spec-to-code-compliance/SKILL.md) | `claire-test` 的规格判断底层依赖，保留完整上游工作流、checker 和 resources；设为显式调用，避免作为另一个自动审查入口。不负责发现所有文档外缺陷。 |

### 文档驱动的代码与页面检查

`spec-to-code-compliance` 保存在 `.plugins/spec-to-code-compliance`，包含上游 Skill、审查代理、工作流、示例和许可证。版本为 `2.0.2`，来源提交为 `442fc9d6c89b1e937e6f7a477e7071ea75fcbea4`；由本仓库的 `.claude-plugin/marketplace.json` 提供本地 marketplace `claire-page-testing`，并在 Codex 中安装、启用。

源码与缓存均实际位于 D 盘。Codex 所需的 `C:\Users\Claire\.codex\plugins\cache\claire-page-testing` 是指向 `D:\Claire\cache\codex-plugins\claire-page-testing` 的 junction。安装状态可用 `codex plugin list --marketplace claire-page-testing --json` 复核。后续更新上游源码后，使用 `codex plugin add spec-to-code-compliance@claire-page-testing` 刷新安装副本；新会话加载新增插件能力。

`webapp-testing` 的 Python 运行环境为 `D:\Claire\tools\webapp-testing\.venv\Scripts\python.exe`，默认复用已安装的 Chrome。临时脚本、截图、日志、飞书输入副本和规格对照报告放在 `D:\Claire\temp\<任务名>`；为规格对照工作流指定该目录中的 `outDir`。审查不修改业务源码、不添加 test-id、不向业务仓库写入临时测试文件。

三个日常入口的调用示例：

```text
$claire-require 读取这份测试文档，整理已确认规则、验收标准、开发注意点和疑点：
https://fanruan-x.feishu.cn/wiki/B5khwOSp3iBLuWkDZm0chYfJnzp

$claire-test 根据上述文档检查代码问题，结合规格对照与相关边界，
给出代码位置、触发条件、修改方案和手动验证步骤，由我自行修改。
源码范围：D:\work\fv-web2\packages\<目标模块>\src

$claire-test 为本次改动生成转测前手动自查用例，保留未执行状态。

$webapp-testing 在 <实际测试页面地址> 验证我指定的这些场景，
截图和日志放入 D:\Claire\temp 的任务目录，不修改业务代码。
```

飞书文档需要有效授权；只有明确点名页面测试时，才需要可访问的测试环境、账号和适用测试数据。删除、提交等会改变数据的场景使用专门测试数据。当前规格对照工作流默认检查 10 条要求、单次最多 30 条，超过范围应分批检查并保留未检查项；不能把局部通过当成整份文档通过。

Codex 没有上游工作流运行器时，`claire-test` 按上游 checker、分析格式与复核规则使用宿主子代理适配执行；不会把依赖宿主绑定的脚本当作普通 Node 程序运行。报告区分“原生工作流”“Codex 子代理适配”与缺少独立复核的主上下文审查。

来源：[Anthropic webapp-testing](https://github.com/anthropics/skills/tree/main/skills/webapp-testing)、[Trail of Bits spec-to-code-compliance](https://github.com/trailofbits/skills/tree/main/plugins/spec-to-code-compliance)。安装时已验证浏览器运行环境；未对上述飞书文档执行正式业务审查。

本地入口已通过名称、元数据、文件链接及显式调用策略检查。隔离样例中，只读审查指出了另一保存入口的权限缺口，给出共享层修法，没有将已存在的共享名称校验误报；输入文件哈希保持不变。该样例验证的是单上下文降级路径，上游原生工作流和逐项独立反证流程尚未验证。

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

## Codex 会话时间轴

| Skill | 适用场景 |
| --- | --- |
| [`codex-session-timeline`](codex-session-timeline/SKILL.md) | 按上海日期浏览日报中的 Codex 会话标题、分类、时间与 Token 用量，并生成可直接打开的 HTML 时间轴。 |
