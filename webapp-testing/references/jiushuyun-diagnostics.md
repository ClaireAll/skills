# 实时刷新、埋点与诊断证据

仅在用户要求的对应测试中使用。来源为测试百宝箱的 WS、埋点、trace 与告警文档，详见 [来源索引](toolbox-sources.md)。保存诊断资料前脱敏。

## WebSocket：两个页面、两类恢复

准备同一测试资源的两个独立页面 A/B，A 写入数据，B 观测刷新。文档中的断连语句只影响执行它的标签页。先观察正常刷新和实际 `BI.socket` 对象，记录 B 原始数据及连接状态。只有任务已授权这些测试写入和故障注入时执行下列操作。

### 完全断开，手动重连

在 B 依次执行：

```javascript
BI.socket.off("disconnect");
BI.socket.disconnect();
```

确认 B 的 `BI.socket.connected` 为 false，并在约定观测窗口内没有自动恢复。A 改数据时 B 不自动刷新；随后 B 执行 `BI.socket.connect()`，等待连接恢复，断言 B 补上 A 刚才的最新数据。A 再改一次，B 应继续自动更新。连接变 true 只证明传输恢复，不证明补数和持续刷新均通过。

### 断开一次，自动重连

若上一场景移除了 disconnect 监听，先刷新 B 恢复应用自己的监听逻辑。不要自己手写一份处理器“修好”被测行为。

按当前工具能力只对 B 设置可控慢网，然后执行 `BI.socket.disconnect()`，保留原有 disconnect 监听。A 在重连间隙改数据；等待 B 自动重连及补最新数据，再让 A 改一次确认后续刷新。记录重连/数据可见时间及超时。整上下文 offline 会同时阻断 HTTP，不能冒充 WS 独立断连。

结束后恢复本次设置的网络条件并刷新 B。慢网、断连、恢复和断言分别记录，未触发预期故障时不能把恢复场景记通过。

## 一体化埋点：发送与入库分开

- 先确认事件的当前设计契约及前端/后端类型。新链路不能默认套旧 WS honeypot 结构。
- 前端文档截图的 `evt` 是对象（name/type，过程事件可带 p_s/p_d）；后端为字符串。字段、实体及自定义参数都与本事件开发文档核对，不把截图中的示例结构强制套给全部事件。
- 先注册监听再触发动作，关联事件 ID/名称、用户/企业、资源 ID、动作时间和次数。实际请求可在 `log/v1` 的 payload 查询参数；按实际编码在本地解析，文档示例为 `JSON.parse(decodeURIComponent(atob(payload)))`。不要把包含用户/令牌的完整载荷贴入外部解析站点或报告。
- 控制台 point content 可辅助观察。确有必要且获准时，可临时设置 localStorage 的 `__DEV__` 为 true；记录并恢复原有值，不将调试输出当成入库证据。
- 一体化文档列出 MongoDB `fx-track`：前端 `dh_track_logs`、后端 `dh_back_track_logs`、性能 `dh_performance_back_track_logs`；数据同步服务是另一套库。旧 PG 表和旧 WS 方法只在明确仍使用旧链路时采用。
- 入库核验需要对应环境 VPN/数据库只读权限。按当前事件字段、资源标识和本次触发时间窗口查询，排除历史记录；UTC 存储与本地时区显示可能相差 8 小时，不能直接判时间错误。
- 缺少入库权限时可继续浏览器发送侧测试，报告“发送侧已验证，入库待权限”，不能写“一体化埋点全部通过”。
- 源文描述编辑埋点验收/自动化覆盖字段以同步统一监控；这属于外部写入，只在用户明确要求回填时执行。“无需另写埋点用例”是该团队流程，不禁止保存本次执行证据。

## Trace 与更新失败

- 请求响应头可带 `Traceid`。记录请求方法/脱敏路径、发生时间、资源 ID、响应码/业务错误及 trace ID，避免只留一张报错截图。
- 源文测试地址为 `https://signoz.jsydevelop.com/trace/<trace-id>`，正式地址多一层 `work`。访问当次核实环境；读了生产诊断链接不代表允许生产写操作。
- 没有 trace ID 时按资源、接口和时间窗口检索。源文示例 `tableId = '<id>'`、`name in ['POST /decision/v1/conf/analysis/operators/fields']`、`selectIndex = 2`；组合条件在实际查询界面核对语法，不能盲抄原文缺分隔符的拼接。
- 架构识别优先按源文“最新方法”搜索 `polarsNode EXISTS` 并看实际属性；被划掉的 execute/metric 方法不作为默认流程。
- 底表更新失败：以 tableId 和 update 操作定位记录，`rowCount = -1` 是该指南的失败线索；比较 `rootErrorId` 与 `tableId`，不一致则沿根错误标识继续查，直到找到匹配的根表并查看错误/Logs。
- 遇到缺标识、无权限、无对应时间记录或重复 ID 环路即停止追查并保留已走路径；不能无限循环，也不能只凭下游报错就断言下游表是根因。
- 数据库辅助定位（获准只读时）：`fx_asset` 资产、`fx_asset_draft` 草稿、`fx_resource_permission` 权限、`fx_lineage` 血缘、`fx_mirror_report` 镜像来源、`fx_recycle` 回收站、`fx_operation_record` 最近操作、`hi_parameter` 参数；权益相关有 `fx_corp_version`、`fx_capacity`、订单表和 `fx_ai_entitlement_period`。以当前结构为准，不为测试直接改库。
- `fx_capacity` 截图区分 capacity 总量、current 已用量、effectivetime 生效时间和 expirationtime 失效时间；版本缓冲期与界面显示不能仅按某个数据库日期相等断言。

## 异常告警与日志

- 测试异常告警已接入类型可从 SigNoz Alerts 核对；文档录屏展示复制规则、修改异常类/环境/时间窗口/阈值及通知通道。配置或 Test Notification 会产生共享变更/消息，本 Skill 不自动执行。
- 日志巡检文档当时聚焦 NPE 和 IndexOutOfBounds，并用 body 去重、日志 URL 和 exception.message 生成【日志告警】缺陷。它是巡检口径，不应让普通页面测试忽略其他错误，也不自动创建缺陷或指定经办人。
- 该文档排除 `JSY-Developer` 本地前端、python-requests 来源及 root span 为 complex 的部分告警；当次适用性需确认。自动化请求本身可能制造 Python 来源日志，应与产品用户链路区分。
- 附件浏览器扩展只提供异常列表/日志定位的快捷入口，可直接只读查询 SigNoz，不为验证强制安装扩展。
- “一段时间无日志”只支持“在此环境、窗口和过滤条件下未再观察到”；不能泛化为功能修复通过。功能回归仍须按研发给出的影响范围实际执行。
