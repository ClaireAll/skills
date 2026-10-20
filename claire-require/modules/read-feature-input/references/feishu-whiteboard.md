# 飞书画板读取

仅在需求来源包含飞书原生画板时读取本参考。目标是拿到节点文字、脑图层级和流程连线；普通图片与 Figma 不走本流程。

## 选择读取方式

1. 从已读取的文档正文确认目标画板 token，例如 `<whiteboard token="..."/>`。token 只用于内部定位。
2. 当前工具能返回完整节点数据时，优先使用只读接口。已安装且已授权的 `lark-cli` 可用 `lark-cli whiteboard +export --as user --whiteboard-token <token> --output-type raw`；未安装不自动安装。
3. 接口只返回缩略图时，可在已登录的浏览器中复制画板，取得剪贴板 `text/html`。浏览器不可用或用户无法完成登录时，保留目标及未读范围，继续不依赖该画板的工作。

数据优先在内存中解析。需要保存原始数据供核对时，放任务专属的 `D:/Claire/temp` 目录，结束时只清理本次创建且无需保留的文件。

## 浏览器复制

- 先确认目标画板顶部在视口内，从文档态双击画板块的空白区域一次。不要双击节点文字、连线或评论按钮。
- 进入画板后只单击空白处聚焦，用 Windows 的 `Ctrl+A`、`Ctrl+C` 复制。**不要在已打开的画布上再次双击**，这可能创建节点；不要为定位画板而展开会持久化的折叠标题。
- 用当前浏览器工具的剪贴板能力或页面内 `copy` 事件取得 `text/html`；需要剪贴板授权时让用户确认。先清空本次捕获值，再执行复制，避免误用上次数据。`text/plain` 只有逐行文字，不能用于还原层级。
- 解码后必须将 payload 的 `token` 与目标画板 token 比对；不一致、缺少 `data-info` 或复制无数据都不是读取成功。允许一次重新定位/复制，仍失败就记录具体缺口。
- 用 `Escape` 退出并确认回到文档态。若出现未保存提示，先核对是否误改了节点；只放弃本次产生且确认不需保留的视图状态，不保存或丢弃用户已有内容改动。

## 解码与完整性核对

使用结构化解析，不凭剪贴板行数推断层级：

- HTML 用 DOM 解析器取 `data-info` 属性，校验包裹格式 `--%whiteboard-x--<payload>--whiteboard-x%--`；payload 依次 Base64 解码、URI 解码、JSON 解析。格式变化或解析失败时保留原始数据，不声称解码成功。
- JSON 顶层包含 `token` 与 `data`。递归展平 `data` 中节点的 `children`，不能只查看容器顶层。
- 脑图节点 `type=24`：文字在 `info.textV2.text`，父节点在 `info.mindMap.parentId`；按父子关系重建树，同级按 `info.baseV2.y` 对照视觉顺序。缺失父节点、循环关系、无文字或游离节点要单独核对，不能静默丢弃。
- OpenAPI raw 导出格式与剪贴板不同，按实际节点 schema 解析类型及文字，不能直接套数字类型字段。若已安装插件包含适配该格式的 `decode-whiteboard.mjs`，可核实脚本路径后复用；没有脚本也可按结构化数据读取，不必调用 BDD Skill。

脑图之外的文字和关系也必须检查：

| 剪贴板节点 | 读取内容 |
| --- | --- |
| `type=20` 容器 | 递归读取 `children` |
| `type=3/13` 文本框、形状 | `info.textV2.text` |
| `type=17` 表格 | `info.table.tableRowInfo.data` 中的格子文字，保留 `rowSpan/colSpan` 合并含义 |
| `type=15` 连线 | `info.connectorV2` 的起止对象及 `captions` 文案；端点未挂对象时用坐标和截图核实，不擅自归属 |
| `type=1/14` 贴图、图标 | 节点数据不含图片内文字；影响需求时另取图片/截图阅读 |

对照可见内容核对节点数、根/叶节点、游离文字、表格、连线及贴图。流程图的空间分区不能只靠坐标猜含义，必要时用截图对照；未知类型要记录，不忽略。

节点数据未取全时可用缩略图辅助，输出中明确哪些内容来自图片辨认、哪些结构仍未核实。只拿到缩略图不报告“完整读取”。

参考：[上游画板读取规则](https://code.fineres.com/projects/FXDATA/repos/skill-manager/browse/plugins/dev-toolkit/skills/read-feature-input/references/feishu-whiteboard.md)。
