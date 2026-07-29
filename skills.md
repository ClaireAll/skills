# Codex Skills 清单

生成日期：2026-07-23

个人 skills 根目录：`D:\Claire\skills`

默认发现路径：`C:\Users\Claire\.codex\skills`，当前是指向 `D:\Claire\skills` 的 junction。

这份清单按当前 Codex 会话暴露出来的 skills 整理。`D:\Claire\skills` 下的是个人/系统 skills；插件提供的 skills 仍来自 Codex 插件缓存目录。

## D 盘个人和系统 Skills

| Skill | 位置 | 用途 |
|---|---|---|
| `bug-des` | `D:\Claire\skills\bug-des` | 生成 `fx-data-web` 项目的缺陷说明模板；会询问问题描述、原因、修复方法，并结合 git diff 推断完整内容。 |
| `find-skills` | `D:\Claire\skills\find-skills` | 帮你发现、筛选、推荐和安装开放生态里的 agent skills。适合问“有没有某某 skill”“帮我找一个能做 X 的 skill”。 |
| `frontend-code-review` | `D:\Claire\skills\frontend-code-review` | 对前端 `.tsx`、`.ts`、`.js` 等文件做代码审查，重点看 bug、回归风险、可访问性、状态和交互问题。 |
| `hue` | `D:\Claire\skills\hue` | 生成新的设计语言 skill。适合创建 design system skill、从截图/产品风格提炼视觉规范、重混已有设计 skill。 |
| `imagegen` | `D:\Claire\skills\.system\imagegen` | 生成或编辑位图图片，比如插画、照片风格图、贴图、sprite、透明背景素材或视觉 mockup。 |
| `openai-docs` | `D:\Claire\skills\.system\openai-docs` | 查询 OpenAI 产品/API/Codex 的最新官方文档，并用官方来源回答模型、接口、提示和迁移相关问题。 |
| `plugin-creator` | `D:\Claire\skills\.system\plugin-creator` | 创建个人 Codex 插件目录、`.codex-plugin/plugin.json`、市场条目和可选插件结构。 |
| `skill-creator` | `D:\Claire\skills\.system\skill-creator` | 创建或更新 Codex skill，帮助设计 `SKILL.md`、目录结构、触发条件和可复用工作流。 |
| `skill-installer` | `D:\Claire\skills\.system\skill-installer` | 从 GitHub 或 curated skills 源安装 Codex skills 到本地 skills 目录。 |

## 文档、表格、演示和 PDF

| Skill | 来源 | 用途 |
|---|---|---|
| `documents:documents` | primary runtime plugin | 创建、编辑、批注、渲染和验证 `.docx`/Word/Google Docs 目标文档。 |
| `pdf:pdf` | primary runtime plugin | 读取、生成、检查、渲染和验证 PDF，适合版式重要的 PDF 工作。 |
| `presentations:Presentations` | primary runtime plugin | 创建或编辑 PowerPoint / Google Slides 风格的演示文稿。 |
| `spreadsheets:Spreadsheets` | primary runtime plugin | 创建、编辑、分析和验证 `.xlsx`、`.csv`、`.tsv` 等独立表格文件。 |
| `spreadsheets:excel-live-control` | primary runtime plugin | 通过已连接的 Excel 会话控制打开的工作簿；不用于普通独立表格文件。 |
| `template-creator:template-creator` | primary runtime plugin | 从 Word、PPT、Excel 样例创建或更新可复用的 artifact-template skill。 |

## Figma Skills

| Skill | 来源 | 用途 |
|---|---|---|
| `figma:figma-code-connect` | Figma plugin | 创建和维护 Figma Code Connect 模板，把 Figma 组件映射到代码片段。 |
| `figma:figma-create-new-file` | Figma plugin | 创建新的 Figma / FigJam / Slides 文件前的必读流程。 |
| `figma:figma-design-to-code` | Figma plugin | 将 Figma 设计实现成代码前的必读流程，适合“按这个 Figma 做页面/组件”。 |
| `figma:figma-generate-design` | Figma plugin | 把应用页面、视图或布局生成到 Figma 里。 |
| `figma:figma-generate-diagram` | Figma plugin | 在 Figma 中生成流程图、架构图、ERD、状态图、时序图等图表前的必读流程。 |
| `figma:figma-generate-library` | Figma plugin | 从代码库创建或更新专业设计系统，包括 tokens、变量、组件库和主题。 |
| `figma:figma-implement-motion` | Figma plugin | 将 Figma 中的动效、动画和 motion 规范实现到生产代码中。 |
| `figma:figma-swiftui` | Figma plugin | 在 SwiftUI 和 Figma 之间双向转换设计、视图、tokens 和 iOS/iPadOS 界面。 |
| `figma:figma-use` | Figma plugin | 调用 Figma 文件上下文执行读写操作前的基础流程。 |
| `figma:figma-use-figjam` | Figma plugin | 在 FigJam 上下文中使用 Figma 工具的补充流程。 |
| `figma:figma-use-motion` | Figma plugin | 在 Figma 中添加、编辑或检查 motion/动画节点时使用。 |
| `figma:figma-use-slides` | Figma plugin | 在 Figma Slides 上下文中使用 Figma 工具的补充流程。 |

## GitHub Skills

| Skill | 来源 | 用途 |
|---|---|---|
| `github:github` | GitHub plugin | 面向 GitHub 仓库、issue、PR 的通用梳理、检索和上下文获取。 |
| `github:gh-address-comments` | GitHub plugin | 查看并处理 PR review comments、requested changes 和未解决 review threads。 |
| `github:gh-fix-ci` | GitHub plugin | 调查并修复 GitHub Actions / PR checks 失败。 |
| `github:yeet` | GitHub plugin | 将本地改动整理、提交、推送，并创建 draft PR。 |

## Gmail Skills

| Skill | 来源 | 用途 |
|---|---|---|
| `gmail:gmail` | Gmail plugin | 搜索、阅读、总结邮件/线程，提取待办，草拟回复、转发或整理邮件。 |
| `gmail:gmail-inbox-triage` | Gmail plugin | 对收件箱做优先级分流，区分紧急、需回复、等待中和 FYI。 |

## Product Design Skills

| Skill | 来源 | 用途 |
|---|---|---|
| `product-design:index` | Product Design plugin | 产品设计任务入口，适合设计探索、UX 审查、视觉克隆、原型检查等。 |
| `product-design:audit` | Product Design plugin | 基于截图审查产品流程、页面、漏斗、设置路径、可用性和可访问性问题。 |
| `product-design:ideate` | Product Design plugin | 根据设计 brief 生成图片化的视觉方向、变体、remix 或探索方案。 |
| `product-design:image-to-code` | Product Design plugin | 将截图、mockup 或图片参考忠实实现成响应式前端。 |
| `product-design:url-to-code` | Product Design plugin | 将线上 URL 克隆为本地可运行的前端页面。 |

## Superpowers 工作流 Skills

| Skill | 来源 | 用途 |
|---|---|---|
| `superpowers:using-superpowers` | Superpowers plugin | 开始任务时判断并加载相关 skills，建立 skill 使用规则。 |
| `superpowers:brainstorming` | Superpowers plugin | 在创建功能、组件或修改行为前澄清意图、需求和设计方向。 |
| `superpowers:systematic-debugging` | Superpowers plugin | 遇到 bug、测试失败或异常行为时，按系统化调试流程定位根因。 |
| `superpowers:test-driven-development` | Superpowers plugin | 实现功能或修 bug 前先设计测试，以 TDD 方式推进。 |
| `superpowers:verification-before-completion` | Superpowers plugin | 在声称完成、修复或通过前先运行验证命令并确认结果。 |
| `superpowers:writing-plans` | Superpowers plugin | 对多步骤开发任务先写实施计划，再动代码。 |
| `superpowers:executing-plans` | Superpowers plugin | 按已有实施计划执行，并在检查点进行 review。 |
| `superpowers:dispatching-parallel-agents` | Superpowers plugin | 面对多个独立任务时拆分并并行派发 sub-agents。 |
| `superpowers:subagent-driven-development` | Superpowers plugin | 用 sub-agents 执行相互独立的开发计划任务。 |
| `superpowers:requesting-code-review` | Superpowers plugin | 完成实现后请求代码审查，合并前检查质量。 |
| `superpowers:receiving-code-review` | Superpowers plugin | 收到代码审查意见后，先验证意见再实现修改。 |
| `superpowers:using-git-worktrees` | Superpowers plugin | 开始需要隔离的开发工作时创建或复用 git worktree。 |
| `superpowers:finishing-a-development-branch` | Superpowers plugin | 实现和验证完成后，决定合并、PR 或清理分支的收尾流程。 |
| `superpowers:writing-skills` | Superpowers plugin | 创建、编辑或验证 skills 时使用的工作流。 |

