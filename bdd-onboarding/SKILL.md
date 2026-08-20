---
name: bdd-onboarding
description: 接入或诊断 FXDATA 跨仓库 BDD 流水线；用于安装依赖插件、准备 bdd-harness 与产品仓归档，并在运行前执行 doctor，不用于日常编写单个 BDD 用例。
---

# BDD Onboarding

将具体的 BDD 编排交给官方 `$fx-bdd:bdd`。本 skill 只处理接入时容易被忽略的跨仓库约束和停止条件。

## 先确认插件与会话

依赖顺序固定：先安装并启用 `fx-data-test-skills`，再安装并启用 `fx-bdd`。用下面两条命令复核，二者都必须是 `installed, enabled`：

```powershell
codex plugin list -m fx-data-test-skills
codex plugin list -m skill-manager
```

插件安装或更新后，要求用户新开 Codex 会话；当前会话不会重新发现新 skill。新会话以 `$fx-bdd:bdd` 调用，不能简写为 `$fx-bdd` 或 `$bdd`。

## 准备 Harness

`bdd-harness` 必须是用户 Bitbucket 空间中由网页 Fork 建立的仓库，不能直接克隆上游。让用户选择本地绝对路径；不要擅自决定磁盘位置。克隆后核验：`origin` 指向个人空间、`upstream` 指向 `fxdata/bdd-harness`，并且存在 `release` 与 `feature` 分支。

在用户指定的 harness 路径中安装依赖与 Chromium，再运行 `pnpm type:check`、`pnpm eslint`。复制 `.env.example` 为 `.env`，仅由用户提供或确认必要的 URL、项目路径和凭据；`.env` 不能提交。平台端口未监听时，要求用户先启动平台，不运行场景。

## 初始化产品仓

先让 `$fx-bdd:bdd` 初始化产品仓归档，生成并跟踪：

- `docs/bdd/profile.md`
- `docs/bdd/domain-dimensions.md`

`docs/bdd/local.json` 只存当前机器的 harness 绝对路径。只写入产品仓的 `.git/info/exclude`，不要改共享 `.gitignore`。初始化阶段只建立领域维度骨架，不预先扩写完整用例库。

确认 harness 与产品仓在同一发布线后再继续：harness `release` 对应产品仓发布线，`feature` 对应产品仓开发线。分支偏离时先报告，不要混线运行来制造假失败。

## 先 Doctor，再执行

使用 `$fx-bdd:bdd` 执行 `doctor`。它只能检查归档、跨仓路径、分支、浏览器、端口、`.env`、MCP 和依赖能力，不能运行测试或修改业务流程。只要有 `❌`，停止后续 BDD 流水线，明确列出需要用户处理的项。

飞书或 Figma MCP 仅“工具可见”并不代表用户授权可用。无法读取时标注对应来源待确认，不能把未读到的交互事实当作已确认信息。

## 交付边界

- `.feature`、step、helper 和 Playwright 配置只留在 harness；产品仓不新增测试框架依赖。
- 跨仓改动分开提交；除非用户明确要求，不提交、不推送、不创建 PR。
- 需求执行会自动上传测试计划到飞书时，若用户仅需要本地草稿，必须显式传达“仅生成本地草稿、不要回填”。
