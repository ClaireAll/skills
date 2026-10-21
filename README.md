# Codex Skills

更新日期：2026-10-21

个人 skill 根目录：`D:\Claire\skills`。Codex 默认发现路径 `C:\Users\Claire\.codex\skills` 是指向这里的 junction，因此本仓库是本地 skill 的唯一维护入口。

这里维护本地 personal 与 `.system` skills，并记录当前会话可用 skill 的名称快照。插件提供的 skills 会随 Codex 会话和插件版本变化；实际调用以前，以当前会话的可用 skill 列表为准。

## Skill 目录与插件索引

下表记录本地目录与插件的历史索引，部分入口尚未在当前会话加载。2026-10-20 核对本地 personal 共 **27** 个：新增 `teach`，移除已不存在的 `21-day-self-interview`；`.system/plugin-creator` 也已移除。插件实际可用入口以当前会话发现结果为准，历史数量不代表当前可调用总数。

| 来源 | 数量 | Skill 名称 |
| --- | ---: | --- |
| 本地 personal | 27 | `agent-reach`、`akshare-data`、`archify`、`bug-des`、`bug-memory-workflow`、`bugfix`、`claire-require`、`claire-test`、`codex-session-timeline`、`feishu-doc-writer`<br>`find-skills`、`fixing-accessibility`、`fixing-motion-performance`、`frontend-code-review`、`fx-ui`、`human-writing`、`i-have-adhd`、`i18n-helper`、`interaction-guide`<br>`life-decision-guide`、`life-design`、`maintaining-windows-health`、`open-code-review-delegate`、`resolving-merge-conflicts`、`teach`、`ui`、`webapp-testing` |
| 本地 `.system` | 4 | `imagegen`、`openai-docs`、`skill-creator`、`skill-installer` |
| Dev Toolkit 插件 | 9 | `dev-toolkit:bkt`、`dev-toolkit:code-figma`、`dev-toolkit:commit`、`dev-toolkit:deploy-app`、`dev-toolkit:fetch-library-docs`、`dev-toolkit:firecrawl`、`dev-toolkit:open-bitbucket-pr`、`dev-toolkit:read-feature-input`、`dev-toolkit:worktree` |
| FXDATA BDD 插件 | 5 | `fx-bdd:bdd`、`fx-bdd:setup`、`fx-bdd:test-scenario-planner`、`fx-data-test-skills:read-feature-input`、`fx-data-test-skills:test-plan-generator` |
| FX Workflow 插件 | 4 | `fx-workflow:dev-doc-writer`、`fx-workflow:feishu-issue-commit`、`fx-workflow:reading-kms-confluence-pages`、`fx-workflow:work-log` |
| Figma 插件 | 14 | `figma:figma-code-connect`、`figma:figma-create-new-file`、`figma:figma-design-to-code`、`figma:figma-generate-design`、`figma:figma-generate-diagram`、`figma:figma-generate-library`、`figma:figma-generative-plugins`<br>`figma:figma-implement-motion`、`figma:figma-shaders`、`figma:figma-swiftui`、`figma:figma-use`、`figma:figma-use-figjam`、`figma:figma-use-motion`、`figma:figma-use-slides` |
| 文档与表格能力 | 6 | `documents:documents`、`pdf:pdf`、`presentations:Presentations`、`spreadsheets:Spreadsheets`、`spreadsheets:excel-live-control`、`template-creator:template-creator` |
| 插件管理 | 1 | `plugin-management:plugin-management` |
| Ponytail 插件 | 6 | `ponytail:ponytail`、`ponytail:ponytail-audit`、`ponytail:ponytail-debt`、`ponytail:ponytail-gain`、`ponytail:ponytail-help`、`ponytail:ponytail-review` |
| 规格对照插件 | 1 | `spec-to-code-compliance:spec-to-code-compliance` |
| Sites 插件 | 1 | `sites:sites` |
| Pages 插件 | 4 | `pages:maintain-space`、`pages:manage-schedules`、`pages:organize-space`、`pages:write-page` |
| Pets 插件 | 3 | `work-pets:create-pet`、`work-pets:pets`、`work-pets:update-pet` |
| 安全插件 | 1 | `defense-factory:open-defense-factory` |
| Superpowers 插件 | 15 | `superpowers:brainstorming`、`superpowers:diagnosing-superpowers`、`superpowers:dispatching-parallel-agents`、`superpowers:executing-plans`、`superpowers:finishing-a-development-branch`、`superpowers:receiving-code-review`、`superpowers:requesting-code-review`、`superpowers:subagent-driven-development`<br>`superpowers:systematic-debugging`、`superpowers:test-driven-development`、`superpowers:using-git-worktrees`、`superpowers:using-superpowers`、`superpowers:verification-before-completion`、`superpowers:writing-plans`、`superpowers:writing-skills` |

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

## 内置开源能力维护

2026-10-21 核对并选择性同步以下三个融合入口。它们保留本地职责和使用边界，不是上游文件的原样镜像；没有更新 BDD、独立插件或仅被调用的 Skill。

| 本地入口 | 上游能力 | 本次同步重点 |
| --- | --- | --- |
| `claire-require` | `mattpocock/skills` 的 `grill-me` 及共享依赖 `grilling` | 按决策依赖组织追问，先核实事实，再问当前可决定的问题；默认仍一次一个问题，不扩大实施授权。 |
| `human-writing` | `KKKKhazix/human-writing`、`blader/humanizer` | 材料充分性、现实与虚构边界、文体适配、跨段模板和读者已有上下文；保留最终稿交付、代码与事实保护，不引入机械禁词。 |
| `ui` | `ibelick/ui-skills`、`dominikmartn/hue`，保留 Taste 本地改写 | 六个模块均已核对；补齐 `DESIGN.md` 证据与导出规则、Hue 安全校验。`baseline-ui`、`improve-ui` 无需改动；Taste 未声明许可证，本次不复制新原文。 |

上游仓库、文件路径、完整提交号、核对结果和本地差异记录在 [upstreams.json](upstreams.json)，版权说明见 [THIRD_PARTY_NOTICES.md](THIRD_PARTY_NOTICES.md)。后续更新先定位真实上游并比较差异，不用安装命令整包覆盖融合入口，也不把“核对过”当成“所有模块都新增了内容”。

本次入口格式、引用和写作审计器 7 项回归测试通过，并做了独立场景试用。未执行页面测试；Hue 的 Atlas 示例仍报告 3 条对比度警告、2 个跳过项，其中工作区缺少 `js-yaml`，不能宣称真实 YAML 解析或完整视觉验证通过。

## 需求、文档与计划

| Skill | 适用场景 |
| --- | --- |
| `find-skills` | 本地没有合适能力时，发现和安装可复用 skill。 |
| [`interaction-guide`](interaction-guide/SKILL.md) | 根据指定源码逐动作整理可点击 HTML 交互说明；覆盖实际文案、环境权限、置灰 tooltip、异步状态及字段级分支，支持分块补充现有文档和核对遗漏。 |
| [`claire-require`](claire-require/SKILL.md) | 读取、对齐飞书、Figma、本地文档或文字需求，整理验收标准、状态、权限、开发注意点和待确认项；保留明确要求时的交互文档对齐及同步，正式代码问题审查交给 `claire-test`。 |
| `feishu-doc-writer` | 创建、更新或核验飞书/Lark 文档和 wiki 页面。 |

## BDD 流水线

| Skill | 适用场景 |
| --- | --- |
| `fx-bdd:bdd`（Codex 插件） | 官方 BDD 流水线执行入口，负责初始化、`doctor`、需求到可执行场景的完整编排。首次安装或更新插件后必须新开 Codex 会话，再以 `$fx-bdd:bdd` 调用。 |
| `fx-bdd:setup` | 初始化或刷新 Codex 的五个 BDD 子代理配置；安装或升级后执行，配置生成后新开会话加载。 |
| `fx-bdd:test-scenario-planner` | BDD 内的测试场景树与覆盖台账生成器，负责来源、需求、经验规则、草稿、反向核对及脚本校验；随 `fx-bdd` 安装，不替代日常 `claire-test`。 |
| `dev-toolkit:read-feature-input` | 新版 BDD Phase 0 的输入读取依赖，负责飞书文档、画板文字层级与 Figma 备注等材料；仅由明确的 BDD 任务调用或用户明确点名时使用。 |

依据[接入 BDD 流水线执行手册](https://fanruan-x.feishu.cn/wiki/PrmZwZyTiihXjpkrBSscytqunZc)及上游源码于 2026-10-12 核对：当前安装的 `fx-bdd` 为 `1.1.10`，配套 `dev-toolkit 1.5.4`。Codex 不会自动解析这项插件间依赖，必须显式安装并确认两个插件都为 `installed, enabled`。

手册中“Codex 不能注册 agent”的说明早于本次插件更新。`fx-bdd 1.1.10` 新增 `setup` 和注册脚本：本机已将五份配置生成到 `D:\Claire\agents`，`C:\Users\Claire\.codex\agents` 是指向该目录的 junction。代理名称为 `fx-bdd-feature-reader`、`fx-bdd-test-planner`、`fx-bdd-coverage-critic`、`fx-bdd-convention-critic`、`fx-bdd-impact-critic`；需要新会话加载。环境支持具名代理时按这些名称调用，否则使用独立通用子代理读取插件中的对应定义，不能由主流程代替独立审计。升级后从实际安装副本重新运行注册脚本。

`fx-data-test-skills 0.4.0` 继续保留，但不再是新版 `fx-bdd` 的输入读取依赖，不要用它替代 `dev-toolkit`。本次三个 BDD 相关插件均已刷新安装副本并逐文件核对上游，旧测试插件仍为 `0.4.0`。安装工具同时刷新了同市场的 `fx-workflow` 到 `4.0.1`，该版本移除了 `feishu-mcp-reauth`。

新版 BDD 输入读取与测试计划回填优先使用已安装的 `lark-cli`，不可用时回退到飞书 MCP；画板读取需要文字和层级。两种工具的图表及提醒语法不同，按对应参考文件执行。本机未安装 `lark-cli`，MCP 连接或授权失效时，按全局连接恢复规则协助用户重连或在浏览器授权，验证后继续原任务。

这两个插件保留，但只在用户明确要求 BDD 流程或点名其 BDD 入口时调用。普通需求读取、辅助开发、源码审查、自查用例生成和页面测试不调用 `fx-bdd:*` 或 `fx-data-test-skills:*`；其通用关键词触发说明不覆盖该偏好。

`dev-toolkit:read-feature-input` 也不增加日常入口，普通需求仍走 `claire-require`。`dev-toolkit` 是完整官方插件，随依赖安装另带八个研发工具，上方索引已逐一列出。

### Codex 安装与更新

更新源是保留 Git remote 的 D 盘本地 clone：`D:\Claire\cache\codex-marketplaces\skill-manager` 与 `D:\Claire\cache\codex-marketplaces\fx-data-test-skills`；Codex 以本地 marketplace 注册它们，避免再次向 C 盘下载快照。当前源码提交分别为 `571481f4f25f84d4a5b78a4edf3f25cb50d9bd9e` 与 `89c190695e4538fba424772392096296512d9d9c`。

插件实际缓存位于 `D:\Claire\cache\codex-plugins\skill-manager` 和 `D:\Claire\cache\codex-plugins\fx-data-test-skills`；对应的 `C:\Users\Claire\.codex\plugins\cache\<marketplace>` 仅为 junction。后续更新先拉源码，再刷新安装副本；本地 marketplace 不通过 `marketplace upgrade` 自动拉取 Git：

```powershell
rtk git -C D:/Claire/cache/codex-marketplaces/skill-manager pull --ff-only
rtk proxy codex plugin add dev-toolkit@skill-manager
rtk proxy codex plugin add fx-bdd@skill-manager
rtk proxy codex plugin list -m skill-manager --json

rtk git -C D:/Claire/cache/codex-marketplaces/fx-data-test-skills pull --ff-only
rtk proxy codex plugin add fx-data-test-skills@fx-data-test-skills
rtk proxy codex plugin list -m fx-data-test-skills --json
```

安装或更新后新开会话，在业务仓库中使用完整名称：

```text
$fx-bdd:bdd 对当前仓库做 doctor 体检
$fx-bdd:bdd 初始化当前仓库的 BDD 档案
$fx-bdd:bdd 按这些需求开展 BDD，先提交用例给我评审
$fx-bdd:setup 刷新本机五个 BDD 子代理配置，文件保存在 D:\Claire\agents
```

不要只写 `$fx-bdd` 或 `$bdd`。本次更新了插件及依赖并完成子代理初始化，没有对业务仓库运行 BDD 初始化、doctor 或业务测试。六个 BDD 相关 Skill 与五份代理配置通过基础校验，注册脚本的四项测试通过；文件生成不代表当前会话已加载新能力。

### 接入与执行边界

- 团队独立 harness 必须先在 Bitbucket 网页 fork `FXDATA/bdd-harness`，再 clone 自己的 fork；`origin` 指向个人空间，`upstream` 指向团队上游。更新上游用 `--ff-only`，用例 PR 源与目标保持同线；已有改动或分支歧义不能直接切分支。
- 产品仓与 harness 的开发线按各仓 `docs/bdd/profile.md` 核对，不把手册的某个项目映射直接套到所有仓库。跨仓路径写入 `docs/bdd/local.json`，必须使用绝对路径，并通过 `.git/info/exclude` 排除。
- 仅在明确要求接入时生成 `profile.md` 与 `domain-dimensions.md`，探测结果交用户确认；领域库先建骨架，不编造规则。`test-plan/`、`design.md`、`fixtures.md` 入库，`progress.md`、`inputs/`、`audits/` 按官方规则排除。
- 独立 harness 的 `.feature`、step、helper 和 Playwright 配置不复制到产品仓。完整 BDD 可能按仓库锚点契约补充测试属性；普通 `claire-test` 与 `webapp-testing` 不因此获得修改业务代码的权限。
- harness 的依赖与 Chromium revision 按其锁定版本安装，浏览器缓存设置在 D 盘；通过 Playwright 报告的安装路径验证实际就位，不能只看安装退出码，也不能为运行成功随意改依赖版本。
- 开跑前确认被测平台、账号与测试数据就绪。doctor 核对档案、跨仓环境及依赖能力，不跑业务用例；MCP 工具可见不等于鉴权有效，必须区分未暴露、已暴露未验证与实际调用失败。
- Phase 2 保留人工评审卡点；默认会把测试计划回填飞书并创建审核待办，不需要回填时提前说明。自主续跑不自行 commit 或 push；跨仓改动分别提交，产品 PR 链接对应的用例 PR。

## 飞书与内部工作流

| Skill | 适用场景 | 调用示例 |
| --- | --- | --- |
| `fx-workflow:work-log` | 从 Bitbucket 已合并 PR 汇总每日工作内容与工时，并提交到飞书项目。首次使用需要配置空间 ID、用户 ID 和兜底工作项。 | `$fx-workflow:work-log 记录本周工作日志`。 |

`fx-workflow 4.0.1` 已移除旧的 `feishu-mcp-reauth`，不再调用其失效路径。需要续期飞书文档 MCP 时，使用当前可用的恢复能力或打开[飞书 MCP 配置平台](https://open.feishu.cn/page/mcp)，由用户完成重新授权；再验证原目标读取，并继续任务。飞书项目 MCP 按自身授权入口处理。

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
| `i-have-adhd` | 日常对话、个人规划、生活决策与学习跟进时自动使用行动优先、短步骤的表达方式；编码、排障、评审、正式文档等工作场景仅在明确调用时使用。 |

## 自我探索与人生设计

| Skill | 适用场景 | 调用示例 |
| --- | --- | --- |
| `life-decision-guide` | 检索《高性价比人生指南》，按成本、收益量级和证据等级回答健康、法律、社保、消费及其他具体人生决策，并注明条目出处。建议按需显式调用。 | `$life-decision-guide 替朋友担保值不值得？` |
| `life-design` | 针对职业、生活重心或未来方向进行 6–9 轮访谈，形成三条五年路径及低成本验证行动。仅在明确调用时使用。 | `$life-design 帮我做一次人生设计，重点梳理未来五年的职业方向`。 |

## 学习辅助

| Skill | 适用场景 |
| --- | --- |
| [`teach`](teach/SKILL.md) | 显式调用时开展持续学习，维护学习目标、课程、参考资料与学习记录。 |

## 投资研究与网络信息

| Skill | 适用场景 | 调用示例 |
| --- | --- | --- |
| [`agent-reach`](agent-reach/SKILL.md) | 读取已接通的社交平台讨论、网页和 RSS；投资研究中补充雪球、小红书等平台的热点与分歧，不代替公告或行情来源。 | `$agent-reach 搜集最近一周与沪深300ETF相关的公开讨论，区分事实、传闻和观点，保留出处。` |
| [`akshare-data`](akshare-data/SKILL.md) | 通过 AKShare 获取 A股、国内ETF和公募基金数据，诊断已有持仓、主动筛选候选，分别进行短线或波段研究并给出条件式建议。 | `$akshare-data 分析我的基金和ETF持仓，结合agent-reach搜集的公开讨论，分别给出短线和波段观察结论、调整条件和风险。` |

### 组合使用

- 默认资产范围是 A股、国内ETF和公募基金，同时支持已有持仓诊断与主动筛选；周期分为几天以内的短线、几周到几个月的波段。用户只要求一种任务或周期时不扩展其范围。
- 投资相关自然语言请求可触发 `akshare-data`；需要市场讨论时再配合 `agent-reach`，不必每次手动串联。纯数据查询不强制搜索社交平台，普通飞书、Figma、代码等工作也不会因有链接而强制调用 Agent-Reach。
- 输出包括倾向、事实依据与反证、数据时间、操作触发条件、判断失效/退出条件、费用和风险。没有足够证据时可以观望；不知道个人资金与风险约束时不擅自给具体调仓金额或比例。
- 行情、净值和基金披露持仓分别标记日期；没有有效最新报价时不报即时进出价格。讨论热度、过去涨幅和回测均不构成收益保证，不自动下单、不连接交易账户、不自动创建监控任务。
- 持仓分析时可提供代码、名称、金额或仓位、成本和预期持有时间；无需账号、密码或验证码。持仓、Cookie、临时报告不提交 Git。

### 本机环境与验收

Skill 文件在本仓库；依赖单独保存在 `D:\Claire\tools\investment-research`，不把虚拟环境或 `node_modules` 放入 Git。已安装 Agent-Reach `1.5.0`、AKShare `1.19.1`、OpenCLI `1.8.8`；OpenCLI 作为读取平台的后端，不另增一个 Skill 入口。

统一通过启动器运行，子进程的用户目录、配置、缓存、临时文件均指向 D 盘，不改系统 PATH 或用户配置：

```powershell
# 检查渠道；只能证明输出中实际通过的项目，不能代表所有平台可用
rtk proxy D:\Claire\tools\investment-research\.venv\Scripts\python.exe -B D:\Claire\skills\agent-reach\scripts\run.py agent-reach doctor --json

# 检查浏览器桥接；若本次启动 daemon，用完后关闭本次启动且无其他任务使用的进程
rtk proxy D:\Claire\tools\investment-research\.venv\Scripts\python.exe -B D:\Claire\skills\agent-reach\scripts\run.py opencli doctor

# 执行放在 D 盘任务目录中的数据分析脚本
rtk proxy D:\Claire\tools\investment-research\.venv\Scripts\python.exe -B D:\Claire\skills\agent-reach\scripts\run.py python D:\Claire\temp\<任务名>\analysis.py
```

Python 依赖版本记录在 [requirements.txt](agent-reach/requirements.txt)，只安装到上述 D 盘虚拟环境；OpenCLI 以 `--ignore-scripts` 安装到 `D:\Claire\tools\investment-research\node`。配置根目录为 `D:\Claire\tools\investment-research\home`，启动器创建的任务临时目录在子进程退出后清理。

2026-10-15 的实际验证：

| 项目 | 结果与边界 |
| --- | --- |
| 股票日线 | `600519` 的新浪备用源成功返回 26 条数据，最新日期 2026-10-14；东方财富日线接口连接中断，保留降级说明。 |
| ETF日线 | `510300` 的新浪备用源成功返回 26 条数据，最新日期 2026-10-14；并非盘中实时行情，也不能直接替代复权收益序列。 |
| 公募基金净值 | `000001` 返回 6022 条净值数据，最新日期 2026-10-14；已修复上游示例中 `fund=` 与当前 `symbol=` 不符的问题。 |
| Agent-Reach 与 OpenCLI | CLI 可运行，OpenCLI 包含雪球、小红书命令；雪球公开接口返回 HTTP 400，OpenCLI 浏览器扩展未连接，社交读取尚待用户连接及登录验证。 |

连接社交平台时，按 [OpenCLI 官方发布页](https://github.com/jackwener/opencli/releases)准备 Browser Bridge 扩展，由用户在 Chrome 中安装并自行登录对应平台，然后执行只读身份与内容验证。不要自动提取 Cookie，不在聊天中粘贴 Cookie；本次安装不意味着已有平台授权。

来源：[Agent-Reach](https://github.com/Panniantong/Agent-Reach/tree/94f06c1969dfc1834001269d79d3ad0972d9dee6/agent_reach/skill)，提交 `94f06c1969dfc1834001269d79d3ad0972d9dee6`；[haomingz/skills 的 akshare-data](https://github.com/haomingz/skills/tree/aabd488de4ab0465117685f6f1af6482e7865e9f/skills/akshare-data)，提交 `aabd488de4ab0465117685f6f1af6482e7865e9f`。均保留上游 MIT 许可证，本地补充了 D 盘运行、触发范围、投资研究规则与接口参数修正。取数验证不代表策略获利或全部接口可用。

## 代码审查与前端质量

| Skill | 适用场景 |
| --- | --- |
| `frontend-code-review` | 审查前端代码中的缺陷、回归和交互风险。 |
| `open-code-review-delegate` | 由 OCR 确定性筛选 Git 改动并匹配审查规则，再由当前 Codex 完成逐文件审查；适合跨文件改动或提交 PR 前检查。调用：`$open-code-review-delegate 审查当前工作区改动`。 |
| `fx-ui` | 规划、实现或审查 `fx-data-web`、`fv-web2` 的前端交互行为。 |
| `fixing-accessibility` | 修复 ARIA、键盘、焦点、对比度和表单可访问性问题。 |
| `fixing-motion-performance` | 排查和修复动画、滚动联动和模糊效果的性能问题。 |
| `i18n-helper` | 检查 JS/TS i18n JSON 的未使用 key、重复值和误报风险。 |

## Windows 维护

| Skill | 适用场景 |
| --- | --- |
| `maintaining-windows-health` | 排查 Windows 11 磁盘、内存压力、异常重启与崩溃转储，并通过分级清理和监控降低开发机故障风险。 |

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

`.system` 下的安装和平台能力保持独立：`imagegen`、`openai-docs`、`review-agent`、`skill-creator`、`skill-installer`。除非明确维护平台能力，不要删除或合并它们。

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
| [`codex-session-timeline`](codex-session-timeline/SKILL.md) | 按上海日期浏览 Codex 会话内容摘要、时间与 Token 用量，并生成可直接打开的 HTML 时间轴。 |
