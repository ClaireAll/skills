---
name: akshare-data
description: Use when obtaining financial data with AKShare or analyzing A-share stocks, domestic ETFs, Chinese mutual funds, existing holdings, or investment candidates for short-term and multi-week/month horizons. Not for executing trades, guaranteed predictions, or unrelated professional tasks.
---

# AKShare 多市场金融数据获取

使用 `akshare` 获取多市场金融数据。AKShare 不需要登录，直接调用函数返回 pandas DataFrame；多数 A 股接口使用中文列名，且上游数据源变化较频繁，脚本必须检查空结果和实际字段。

**不适用于**：高可靠生产行情源、逐笔级 tick 数据、需要强 SLA 的实时交易系统。纯 A 股历史行情或季频财务指标也可评估 `baostock-data`。

## 本机入口与投资研究

- 已安装 AKShare `1.19.1`；运行环境固定为 `D:\Claire\tools\investment-research\.venv`，不要用系统 Python 或全局 pip 安装依赖。
- 使用共享启动器执行 Python 脚本，自动把进程内配置、缓存和临时目录放到 D 盘：

```powershell
rtk proxy D:\Claire\tools\investment-research\.venv\Scripts\python.exe -B D:\Claire\skills\agent-reach\scripts\run.py python -c "import akshare as ak; print(ak.__version__)"
```

- 脚本与输出放在 `D:\Claire\temp\<任务名>`；完成后清理本次无需保留的文件，不把持仓和账户信息写入本仓库。
- 分析已有持仓、主动筛选标的或给操作建议时，先读 [投资研究规则](references/investment-research.md)。按用户需要区分几天以内的短线与几周到几个月的波段；结合讨论时调用 `agent-reach`，不把社交热度当作行情证据。
- 本地参考文档已经修正 `fund_open_fund_info_em(symbol=...)`；不确定的接口仍以当前安装签名和官方文档为准，不机械复制旧示例。
- 2026-10-15 的安装验收中，东方财富股票/ETF日线接口连接中断；新浪备用接口 `stock_zh_a_daily(symbol="sh600519", ...)`、`fund_etf_hist_sina(symbol="sh510300")` 和基金净值 `fund_open_fund_info_em(symbol="000001", ...)` 均返回非空数据，最新日期为 2026-10-14。这是一次连通性快照，不代表永久可用或盘中实时。日后先检查数据日期和字段，失败再按实际来源降级；新浪 ETF 日线无复权参数，不直接用于未经分红/拆分核验的收益计算。

## 安装与验证

本机环境已配置。更新前说明版本变动并取得对应授权，仅在共享 D 盘虚拟环境更新，并重新验证实际需要的股票、ETF 与基金接口。用户要求离线或只读检查时不联网、不升级。

遇到 `JSONDecodeError`、`KeyError`、字段缺失、返回结构变化时，先核对当前安装版本、函数签名、实际列名和数据源，再查 `references/api-reference.md` 与允许访问的官方文档：`https://akshare.akfamily.xyz/`。必要时提出升级方案，不自行修改运行环境。

## 工作流

**复制此 checklist 追踪进度：**

```
AKShare 进度:
- [ ] 步骤 1: 选择最窄 API 和数据源
- [ ] 步骤 2: 规范代码、市场、日期、周期和复权参数
- [ ] 步骤 3: 单标的任务优先使用个股接口
- [ ] 步骤 4: 调用 API 并检查 df.empty 和 df.columns
- [ ] 步骤 5: 按需重命名中文列并验证字段
- [ ] 步骤 6: 批量任务加入限速、重试和缓存
- [ ] 步骤 7: 运行质量检查并修正问题
```

**步骤 1: 选择最窄 API 和数据源**

根据市场和数据类型选择精确函数。函数签名、数据源变体和返回字段不确定时，加载 `references/api-reference.md`。

常用 API 速查：

| 需求 | API |
|------|-----|
| A 股日/周/月 K 线 | `stock_zh_a_hist()` |
| A 股分钟线 | `stock_zh_a_hist_min_em()` |
| A 股实时行情 | `stock_sh_a_spot_em()` / `stock_sz_a_spot_em()` / `stock_bj_a_spot_em()` / `stock_zh_a_spot_em()` |
| 个股盘口/基本信息 | `stock_bid_ask_em()` / `stock_individual_info_em()` |
| 个股/市场资金流 | `stock_individual_fund_flow()` / `stock_individual_fund_flow_rank()` / `stock_market_fund_flow()` |
| 行业/概念板块 | `stock_board_industry_*` / `stock_board_concept_*` |
| 涨停池/龙虎榜 | `stock_zt_pool_em()` / `stock_lhb_detail_em()` |
| 三大财务报表 | `stock_profit_sheet_by_report_em()` / `stock_balance_sheet_by_report_em()` / `stock_cash_flow_sheet_by_report_em()` |
| 股东与公司数据 | `stock_gdfx_top_10_em()` / `stock_gdfx_free_top_10_em()` / `stock_zh_a_gdhs()` |
| 港股/美股历史行情 | `stock_hk_hist()` / `stock_us_hist()` |
| 期货主力连续 | `futures_display_main_sina()` / `futures_main_sina()` |
| ETF/基金/可转债 | `fund_etf_*` / `fund_open_fund_*` / `bond_zh_cov*` |
| 中国/美国宏观 | `macro_china_*` / `macro_usa_*` |

**步骤 2: 规范代码、市场、日期、周期和复权参数**

使用 AKShare 的代码约定，不要混用 BaoStock 格式：

| 项目 | AKShare 约定 |
|------|--------------|
| A 股代码 | 6 位纯数字，例如 `"000001"` |
| 资金流等市场参数 | 通常沪市/科创板用 `"sh"`，深市/创业板用 `"sz"` |
| A 股日线日期 | `YYYYMMDD`，例如 `"20240101"` |
| 分钟线日期 | `YYYY-MM-DD HH:MM:SS` |
| 复权参数 | 通常 `""` 不复权，`"qfq"` 前复权，`"hfq"` 后复权 |
| 返回列名 | 多数为中文，如 `日期`、`收盘`、`成交量`、`换手率` |

与 BaoStock 的关键差异：

| 特性 | AKShare | BaoStock |
|------|---------|----------|
| 登录 | 不需要 | 需要 `login()` / `logout()` |
| A 股代码 | `"000001"` | `"sz.000001"` |
| 日线日期 | `"20240101"` | `"2024-01-01"` |
| 列名 | 中文为主 | 英文为主 |
| 数值类型 | 多数已转换 | 多数为字符串 |
| 市场覆盖 | A 股、港股、美股、期货、基金、宏观等 | 主要 A 股 |

**步骤 3: 单标的任务优先使用个股接口**

单只股票任务使用个股接口，例如 `stock_zh_a_hist()`、`stock_individual_info_em()`、`stock_bid_ask_em()`、`stock_individual_fund_flow()`。只有真正需要全市场筛选、排名或扫描时才使用全市场接口。

全市场接口通常更慢、更容易被上游限流，返回列也更容易变化。

**步骤 4: 调用 API 并检查 df.empty 和 df.columns**

```python
import akshare as ak
import pandas as pd


df = ak.stock_zh_a_hist(
    symbol="000001",
    period="daily",
    start_date="20240101",
    end_date="20241231",
    adjust="qfq",
)

if df.empty:
    raise ValueError("AKShare returned no rows; check symbol, date format, period, adjustment, and source coverage")

print(df.columns.tolist())
```

**步骤 5: 按需重命名中文列并验证字段**

只重命名任务需要的字段，并保留原始 DataFrame 便于排查数据源差异。

```python
df = df.rename(columns={
    "日期": "date",
    "股票代码": "symbol",
    "开盘": "open",
    "收盘": "close",
    "最高": "high",
    "最低": "low",
    "成交量": "volume",
    "成交额": "amount",
    "涨跌幅": "pct_chg",
    "换手率": "turnover",
})

required = {"date", "close", "volume"}
missing = required - set(df.columns)
if missing:
    raise KeyError(f"Missing expected AKShare columns: {sorted(missing)}")

df["date"] = pd.to_datetime(df["date"])
```

**步骤 6: 批量任务加入限速、重试和缓存**

加载 `references/common-recipes.md` 获取批量下载、行业筛选、指数成分、分钟线、资金流、涨停池、龙虎榜、财务报表、股东数据、期货、基金、ETF、宏观仪表板、可转债、增量存储和技术指标模板。

批量调用时加入 `time.sleep()`、异常重试、中间结果落盘和跳过日志。遇到上游限流、空响应或畸形 JSON 时，增加等待时间或切换同类数据源后缀。

**步骤 7: 运行质量检查并修正问题**

运行下方质量 checklist。若检查失败，回到对应步骤修正后重新验证。

## 数据源后缀选择

AKShare 常见函数后缀反映不同上游来源。字段、覆盖范围和稳定性不能视为完全一致。

| 后缀 | 常见来源 | 使用建议 |
|------|----------|----------|
| `_em` | 东方财富 | A 股行情、资金流、板块数据常用，字段较全，但可能限流 |
| `_ths` | 同花顺 | 财务和个股资料的替代来源 |
| `_xq` | 雪球 | 公司概况、持仓和部分实时数据 |
| `_sina` | 新浪 | 期货、部分历史数据较常见 |

遇到 `_em` 接口失败时，优先查 `references/api-reference.md` 中是否有同类 `_ths`、`_xq` 或 `_sina` 函数。

## 常见陷阱

- 日线、指数、期货等接口常用 `YYYYMMDD`；分钟线常用 `YYYY-MM-DD HH:MM:SS`。
- A 股函数通常传 6 位纯数字，不传 `sh.` / `sz.` 前缀。
- 资金流向接口常需要 `market="sh"` 或 `market="sz"`。
- 中文列名必须以实际 `df.columns` 为准，不要假设一定存在英文列。
- 单股查询不要用 `stock_zh_a_spot_em()` 再筛选，优先用个股接口。
- 退市股、非交易日、未覆盖标的可能静默返回空 DataFrame。
- `period="1"` 的分钟线通常不支持复权，历史深度也有限。
- 期货主力连续常用新浪品种代码，例如先用 `futures_display_main_sina()` 查映射。
- 可转债、基金、ETF 的代码格式类似 6 位数字，但含义和市场前缀规则不同。
- AKShare 上游接口变化较快，先核对签名和列名、查当前文档、评估同类数据源；需要升级时先说明并取得对应授权。

## 约束

- 优先选择最窄 API，不为单标的任务调用全市场接口。
- 明确设置 `adjust`，不要依赖默认不复权。
- 在任何分析、筛选、绘图或存储前检查 `df.empty` 和 `df.columns`。
- 下游代码依赖字段前先验证字段存在。
- 批量任务必须加入限速、重试、日志和可恢复存储。
- 将实时行情视为第三方网页数据抓取结果，不承诺交易级稳定性。

## 质量检查

- [ ] `name` 与目录名一致，frontmatter 只保留必要元数据。
- [ ] API 选择与市场和数据类型匹配。
- [ ] A 股代码使用 6 位纯数字。
- [ ] 日期格式匹配具体接口。
- [ ] 价格序列已明确设置 `adjust`。
- [ ] 单标的任务未滥用全市场接口。
- [ ] 调用后检查 `df.empty`。
- [ ] 调用后打印或验证 `df.columns`。
- [ ] 中文列名重命名前已确认存在。
- [ ] 批量任务包含限速、重试、日志和缓存。
- [ ] 接口异常时已考虑升级 AKShare 或切换同类数据源。

## 参考资料（按需加载）

- `references/api-reference.md` - API 签名、数据源变体、参数、返回字段和市场覆盖。
- `references/common-recipes.md` - 批量下载、筛选器、资金流、涨停池、龙虎榜、财务报表、股东、期货、基金、ETF、宏观、可转债、增量存储、技术指标。
- 官方文档：`https://akshare.akfamily.xyz/`
- GitHub Issues：`https://github.com/akfamily/akshare`
