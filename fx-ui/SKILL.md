---
name: fx-ui
description: Use when implementing, planning, or auditing frontend interaction behavior in fx-data-web or fv-web2, especially Title, Tooltip, validation, search, disabled actions, export, Popconfirm, batch selection, loading, InputNumber, Select, field errors, hierarchy, or guidance. Load only the relevant rules, compare expected behavior with current source, and report audit findings before making fixes.
metadata:
  short-description: FXDATA 前端交互规范与代码审查
---

# FX UI

面向 `fx-data-web` / `fv-web2` 前端代码的交互规范与代码审查 skill。它负责：

1. 编写功能或开发计划时，约束交互行为、状态、反馈、文案和组件选择。
2. 完成代码后，依据规范核查实际代码，报告不符合项和证据。
3. 仅在用户确认审查结论或修改方向后，处理审查发现的问题。

## 使用边界

- 只处理两个目标仓库的前端代码；后端、纯业务逻辑和其他仓库不套用本规范。
- 先确认当前功能涉及的页面、组件、状态和交互路径，再读取相关参考文件。
- 只读取当前流程需要的参考文件，不把无关页面的规则强行套入当前功能。
- 文档规则不完整、存在讨论稿或状态冲突时，标记为“待确认”，不能自行补写颜色、尺寸、文案或行为。
- 以当前源码为实际行为依据，同时保留文档期望行为；两者不一致时报告差异，不静默选择一方。

## 参考文件选择

按当前流程读取：

- 通用层级、导出、Popconfirm、批量选择、Loading、InputNumber、Select、字段报错：读取 [references/interaction-style.md](references/interaction-style.md)。
- 截断文本、Title、Tooltip、校验、悬浮延时和定位：读取 [references/tooltip-validation.md](references/tooltip-validation.md)。
- 前端本地过滤、拼音匹配和高亮：读取 [references/search.md](references/search.md)。远端搜索跳过，不把接口匹配能力当成前端规范问题。
- 隐藏、禁用、权限、复杂可用性判断和点击反馈：读取 [references/disabled-actions.md](references/disabled-actions.md)。
- 说明图标、Pop 尺寸和 Loading 效果：读取 [references/common-feedback.md](references/common-feedback.md)。
- 只有用户明确要求生成或更新飞书审查文档时，才读取 [references/feishu-output.md](references/feishu-output.md)。

专用参考文件与 `interaction-style.md` 有重叠时，专用参考文件对对应场景优先；没有明确证据的精确颜色、尺寸、间距和动画参数不得自行补充。

## 工作流程

### 1. 编码前或开发计划阶段

- 识别受影响的触发对象、容器、组件 API、状态管理、事件处理和请求链路。
- 查找现有 FD 组件、设计 token、统一封装、通用校验和同类页面，优先复用已有实现。
- 明确正常、hover、focus、点击、禁用、错误、加载、空值、边界值和恢复状态。
- 先区分 `Title`、`Tooltip`、`Pop`，不能因它们都表现为悬浮提示就混用规则。
- 发现需求或文档信息不足时，提出最小必要问题；不凭经验补规则。

### 2. 编码中

- 按适用规则实现，不改变无关交互。
- 文档只给出原则而没有精确值时，沿用项目现有 token、组件和统一封装。
- 交互文案保持来源文案；需要改写时说明依据。
- 对无法确认的规则保留可审查的实现边界，并在结果中列出待确认项。

### 3. 完成后审查

完成初步代码后，自动先做一次 `fx-ui` 审查并报告，审查范围按以下优先级确定：

1. 优先审查已暂存差异；没有暂存内容时审查用户指定的工作区范围，并明确说明范围。
2. 从变更代码、组件默认行为、测试、调用方和相邻实现推导运行时行为，不能只凭组件名称或 CSS 类名判断。
3. 将实际行为与适用规则逐项对照，区分“明确不符合”“文档与源码冲突”“证据不足”。
4. 每个问题只报一个独立改动点，不把多个内部问题合并成一句。
5. 审查阶段只报告，不自行暂存、修改、提交或创建 PR。

至少检查这些适用项：

- 交互层级、组件选择和状态完整性。
- Title、Tooltip、Pop 的用途、触发、延时、定位、箭头、颜色和消失行为。
- 文本输入、字段报错、校验时机、恢复值和错误文案。
- 前端本地搜索的触发、大小写、拼音、高亮和已选状态保持。
- 隐藏、禁用、权限提示、复杂判断和未就绪状态的区分。
- 导出加载、并行任务、按钮状态、Toast、下载和失败反馈。
- Popconfirm 与 Alert 的使用边界及确认按钮文案。
- 列表单选、Shift 范围选择和选中状态覆盖规则。
- Loading、InputNumber、Select、引导、层级结构和拖拽占位。

审查完成后停止，等待用户确认。用户确认后才处理发现项；修改后重新审查受影响流程。

## 发现分类与报告

每个发现包含：位置、触发场景、当前行为、规范期望、规范定位、直接影响和最小修改方向。规范定位必须引用具体章节和条款，不能只写“违反 Tooltip 规范”。

```md
## 审查结论
- 范围：
- 结论：符合 / 存在问题 / 规则待确认

## 明确违反规范
### [P1] 问题标题
- 场景：用户如何触发
- 实际：源码当前行为
- 期望：对应交互规则
- 规范：规范名称 > 章节 — 具体条款
- 证据：文件:行号、相关调用或运行时依据
- 建议：最小修改方向

## 待确认
- 当前行为、缺失证据或文档冲突：
- 需要用户或产品确认：

## 其他审查发现
- 仅记录业务逻辑、通用代码质量或其他非交互规范问题，不能冒充规范违规。

## 已检查通过
- 只记录实际检查过且有源码、组件、测试或运行时证据的行为。
```

严重级别只表示交互影响：

- `P1`：阻断核心操作、造成错误数据或明显违反关键交互规则。
- `P2`：功能可继续，但状态、反馈或操作路径不符合规范。
- `P3`：文案、视觉状态或一致性问题，不影响主要流程。

没有发现项时，报告 `交互规范检查通过`，并说明实际检查过的行为。没有运行时证据时，不声称已经完成视觉或运行时验证。

## 修改规则

- 审查完成后不自动修复；只有用户明确确认审查结论或修改方向后才改代码。
- 修改前保护用户已有改动，保持变更范围最小。
- 修改后重新审查受影响流程，并说明仍未验证的部分。
- `fx-ui` 负责交互规范，不代替业务正确性、无障碍、安全或通用代码质量审查；需要时分别调用对应 skill。

## 参考来源

规则整理自交互规范知识库节点 `交互组件规则定稿`，并吸收 `skill-manager` PR 33 中 `interaction-spec-review` 的审查组织方式。页面中标记为讨论、草稿、缺少正文或存在冲突的内容，只能作为补充证据，不能直接升级为强制规则。
