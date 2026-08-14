# Codex Skills

更新日期：2026-08-14

个人 skill 根目录：`D:\Claire\skills`。Codex 默认发现路径 `C:\Users\Claire\.codex\skills` 是指向这里的 junction，因此本仓库是本地 skill 的唯一维护入口。

这里只维护本地 personal 与 `.system` skills。插件提供的 skills 会随 Codex 会话和插件版本变化，以当前会话的可用 skill 列表为准，不在这里复制一份易过期的清单。

## 使用原则

- 优先选择职责清晰、覆盖完整任务的最小入口。
- `require-understand` 会按目标自动加载需求理解模块，生成测试计划时自动追加测试计划模块。
- `ui` 会按目标自动加载一个或多个 UI 内部模块；明确的小任务不必加载宽泛路由上下文。
- `bugfix` 是 `fv-web2 / fx-data-web` 的唯一缺陷交付编排器；它取代已移除的 `fx-data-web-bugfix-workflow`，并调用 `bug-memory-workflow`、`bug-des` 与 `worklog`，这些 skill 仍可独立使用。
- 只有脚本产生的缓存、报告和构建输出应被忽略；skill 源码、模板和验证脚本应留在版本控制中。

## 需求、文档与计划

| Skill | 适用场景 |
| --- | --- |
| `find-skills` | 本地没有合适能力时，发现和安装可复用 skill。 |
| `require-understand` | 读取、对齐飞书、Figma、本地文档或混合需求输入；需要测试计划时自动串联测试场景、脑图与回填流程。 |
| `feishu-doc-writer` | 创建、更新或核验飞书/Lark 文档和 wiki 页面。 |

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

## 前端质量

| Skill | 适用场景 |
| --- | --- |
| `frontend-code-review` | 审查前端代码中的缺陷、回归和交互风险。 |
| `fixing-accessibility` | 修复 ARIA、键盘、焦点、对比度和表单可访问性问题。 |
| `fixing-metadata` | 完善 SEO、Open Graph、canonical、结构化数据和 robots 元数据。 |
| `fixing-motion-performance` | 排查和修复动画、滚动联动和模糊效果的性能问题。 |
| `i18n-helper` | 检查 JS/TS i18n JSON 的未使用 key、重复值和误报风险。 |

## 缺陷协作与交付

| Skill | 适用场景 |
| --- | --- |
| `bug-memory-workflow` | Bug 修复、调查或 review 前检索已确认的历史经验。 |
| `bugfix` | `fv-web2 / fx-data-web` 的修复、review gate、Feishu、Bitbucket PR 与交付流程。 |
| `bug-des` | 基于 issue 与 diff 生成中文 Feishu 缺陷评论或 PR 描述。 |
| `worklog` | 已提交 Feishu 缺陷 PR 后登记或准备项目工时。 |

## 系统 Skills

`.system` 下的安装和平台能力保持独立：`imagegen`、`openai-docs`、`plugin-creator`、`review-agent`、`skill-creator`、`skill-installer`。除非明确维护平台能力，不要删除或合并它们。
