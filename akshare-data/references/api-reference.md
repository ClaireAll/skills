> 官方文档：`https://akshare.akfamily.xyz/`
> 下列签名如与实际不符，以官方文档为准（接口频繁更新）。

## Contents
- A股历史K线（stock_zh_a_hist）
- A股实时行情（全市场 & 分市场）
- A股分钟线（stock_zh_a_hist_min_em）
- 个股详情（盘口/基本信息）
- A股指数历史与成分
- 板块分析（列表/成分/历史/资金流）
- 资金流向
- 选股工具（涨停/跌停/龙虎榜/融资融券）
- 财务数据（三大报表/业绩/摘要）
- 股东与公司（股东/机构/解禁）
- 市场估值
- 港股
- 美股
- 期货
- ETF
- 基金
- 宏观经济（中国）
- 宏观经济（美国）
- 可转债
- 期权
- 加密货币与外汇

---

## A股历史K线

```python
ak.stock_zh_a_hist(
    symbol: str = "000001",        # 6位纯数字
    period: str = "daily",         # "daily" / "weekly" / "monthly"
    start_date: str = "19700101",  # YYYYMMDD
    end_date: str = "20500101",
    adjust: str = "",              # "" 不复权 | "qfq" 前复权 | "hfq" 后复权
    timeout: float = None,
) -> pd.DataFrame
```

**返回字段（12列）：** 日期、股票代码、开盘、收盘、最高、最低、成交量（手）、成交额（元）、振幅(%)、涨跌幅(%)、涨跌额、换手率(%)

---

## A股实时行情

### 全市场（慢，约 70s）
```python
ak.stock_zh_a_spot_em() -> pd.DataFrame
# 沪深京全 A 股 5800+ 行，无参数
```

### 分市场（推荐）
```python
ak.stock_sh_a_spot_em()   # 沪A股 ~28s
ak.stock_sz_a_spot_em()   # 深A股
ak.stock_bj_a_spot_em()   # 北证A股
ak.stock_cy_a_spot_em()   # 创业板
ak.stock_kc_a_spot_em()   # 科创板
ak.stock_new_a_spot_em()  # 新股
```

**返回字段（23列）：** 序号、代码、名称、最新价、涨跌幅(%)、涨跌额、成交量（手）、成交额（元）、振幅(%)、最高、最低、今开、昨收、量比、换手率(%)、市盈率-动态、市净率、总市值（元）、流通市值（元）、涨速、5分钟涨跌(%)、60日涨跌幅(%)、年初至今涨跌幅(%)

---

## A股分钟线

```python
ak.stock_zh_a_hist_min_em(
    symbol: str = "000001",
    period: str = "5",                          # "1"/"5"/"15"/"30"/"60"
    start_date: str = "1979-09-01 09:32:00",    # 日期格式：YYYY-MM-DD HH:MM:SS（非 YYYYMMDD）
    end_date: str = "2222-01-01 09:32:00",
    adjust: str = "",                           # period="1" 时 adjust 无效
) -> pd.DataFrame
```

- `period="1"`：仅近 5 个交易日，无复权，返回 8 列（含均价）
- `period="5/15/30/60"`：近 120 个交易日，返回 11 列（含涨跌幅、振幅、换手率）

---

## 个股详情

```python
ak.stock_individual_info_em(symbol: str = "000001") -> pd.DataFrame
# 返回 item/value 两列，含股票简称、行业、总市值、流通市值、总股本、上市时间等

ak.stock_bid_ask_em(symbol: str = "000001") -> pd.DataFrame
# 五档盘口（买一~买五、卖一~卖五），约 3s

ak.stock_individual_spot_xq(symbol: str = "000001") -> pd.DataFrame
# 雪球个股行情（实时价格、涨跌幅等）
```

---

## A股指数历史与成分

```python
ak.index_zh_a_hist(
    symbol: str = "000001",   # 上证 000001，沪深300 000300，中证500 000905
    period: str = "daily",    # "daily"/"weekly"/"monthly"
    start_date: str = "19700101",
    end_date: str = "22220101",
) -> pd.DataFrame
# 返回（11列）：日期、开盘、收盘、最高、最低、成交量（手）、成交额（元）、振幅(%)、涨跌幅(%)、涨跌额、换手率(%)
```

**指数实时：**
```python
ak.stock_zh_index_spot_em() -> pd.DataFrame    # A股指数实时列表
ak.stock_zh_index_daily_em(symbol="sh000001")  # 指数日线（另一数据源）
```

**指数成分（推荐用 csindex 版）：**
```python
ak.index_stock_cons_csindex(symbol: str = "000300") -> pd.DataFrame
# 返回：成分券代码、成分券名称、交易所、纳入日期

ak.index_stock_cons_weight_csindex(symbol: str = "000300") -> pd.DataFrame
# 返回：成分券代码、成分券名称、权重（%）

ak.index_stock_cons_sina(symbol: str = "000300") -> pd.DataFrame
# 新浪版成分股（作为备选数据源）
```

常用指数代码：000001（上证）、399001（深证）、000300（沪深300）、000905（中证500）、000852（中证1000）、399006（创业板指）、000688（科创50）

---

## 板块分析

### 板块列表
```python
ak.stock_board_industry_name_em() -> pd.DataFrame
# 返回（12列）：排名、板块名称、板块代码(BK开头)、最新价、涨跌额、涨跌幅(%)、成交量、换手率、上涨家数、下跌家数、领涨股票、领涨股票涨跌幅

ak.stock_board_concept_name_em() -> pd.DataFrame   # 概念板块，同上格式
```

### 板块成分股
```python
ak.stock_board_industry_cons_em(symbol: str) -> pd.DataFrame
# symbol 传板块名称（如 "银行"）或板块代码（如 "BK1027"）
# 返回（16列）：序号、代码、名称、最新价、涨跌幅(%)、涨跌额、成交量、成交额、振幅、最高、最低、今开、昨收、换手率(%)、市盈率-动态、市净率

ak.stock_board_concept_cons_em(symbol: str) -> pd.DataFrame   # 概念，同上
```

### 板块历史K线
```python
ak.stock_board_industry_hist_em(
    symbol: str,               # 板块名称，如 "银行"
    period: str = "daily",     # "daily"/"weekly"/"monthly"
    start_date: str = "20240101",
    end_date: str = "20241231",
    adjust: str = "",
) -> pd.DataFrame

ak.stock_board_concept_hist_em(symbol, period, start_date, end_date, adjust)  # 概念，同上
```

### 板块资金流向
```python
ak.stock_fund_flow_industry(indicator: str = "今日") -> pd.DataFrame
# indicator："今日" / "3日" / "5日" / "10日" / "20日"
# 返回行业资金净流入排名

ak.stock_fund_flow_concept(indicator: str = "今日") -> pd.DataFrame   # 概念，同上

ak.stock_sector_fund_flow_rank(indicator: str, sector_type: str) -> pd.DataFrame
# sector_type："行业资金流" / "概念资金流"
```

---

## 资金流向

### 个股资金流
```python
ak.stock_individual_fund_flow(
    stock: str = "000001",
    market: str = "sh",        # "sh" 沪市 | "sz" 深市/创业板/科创板
) -> pd.DataFrame
# 返回今日主力/超大单/大单/中单/小单净流入

ak.stock_fund_flow_individual(stock: str, market: str) -> pd.DataFrame
# 历史资金流数据（近60天）

ak.stock_individual_fund_flow_rank(indicator: str = "今日") -> pd.DataFrame
# 全市场个股资金流排名，indicator："今日"/"3日"/"5日"/"10日"
```

market 参数：沪市主板 `"sh"`，深市主板/创业板/科创板 `"sz"`

### 大盘资金流
```python
ak.stock_market_fund_flow() -> pd.DataFrame     # 大盘资金流向（主力/散户）
ak.stock_main_fund_flow() -> pd.DataFrame       # 主力资金流向分析
```

### 沪深港通
```python
ak.stock_hsgt_hist_em(symbol: str = "沪股通") -> pd.DataFrame
# symbol："沪股通" / "深股通"
# 返回：日期、当日净买入（亿）、累计净买入（亿）

ak.stock_hsgt_sh_hk_spot_em(symbol: str = "沪股通") -> pd.DataFrame
# 实时沪深港通数据

ak.stock_hsgt_fund_flow_summary_em() -> pd.DataFrame   # 资金汇总
ak.stock_hsgt_board_rank_em() -> pd.DataFrame          # 北向板块排名
```

---

## 选股工具

### 涨停/跌停池
```python
ak.stock_zt_pool_em(date: str = "20250327") -> pd.DataFrame          # 涨停池
ak.stock_zt_pool_dtgc_em(date: str = "20250327") -> pd.DataFrame     # 跌停池（近30个交易日）
ak.stock_zt_pool_strong_em(date: str = "20250327") -> pd.DataFrame   # 强势股池
ak.stock_zt_pool_previous_em(date: str = "20250327") -> pd.DataFrame # 昨日涨停
ak.stock_zt_pool_sub_new_em(date: str = "20250327") -> pd.DataFrame  # 次新股涨停
ak.stock_zt_pool_zbgc_em(date: str = "20250327") -> pd.DataFrame     # 涨停不打开
```

### 龙虎榜
```python
ak.stock_lhb_detail_em(
    start_date: str = "20250320",
    end_date: str = "20250327",
) -> pd.DataFrame
# 每日龙虎榜明细（营业部买卖）

ak.stock_lhb_stock_detail_em(symbol: str = "000001") -> pd.DataFrame  # 个股龙虎榜
ak.stock_lhb_stock_statistic_em() -> pd.DataFrame                      # 龙虎榜统计
ak.stock_lhb_jgstatistic_em() -> pd.DataFrame                          # 机构席位统计
ak.stock_lhb_yybph_em() -> pd.DataFrame                                # 营业部排行
```

### 融资融券
```python
ak.stock_margin_sse(
    start_date: str = "20250301",
    end_date: str = "20250328",
) -> pd.DataFrame   # 沪市融资融券汇总

ak.stock_margin_szse(date: str = "20250301") -> pd.DataFrame          # 深市融资融券
ak.stock_margin_detail_sse(date: str = "20250301") -> pd.DataFrame    # 沪市个股明细
ak.stock_margin_detail_szse(date: str = "20250301") -> pd.DataFrame   # 深市个股明细
ak.stock_margin_ratio_pa() -> pd.DataFrame                             # 两融余额占比
```

---

## 财务数据

### 财务摘要（同花顺）
```python
ak.stock_financial_abstract_ths(
    symbol: str = "000001",
    indicator: str = "按报告期",   # "按报告期" / "按年度" / "按单季度"
) -> pd.DataFrame
```

### 三大报表（东财）
```python
ak.stock_profit_sheet_by_report_em(symbol: str = "000001") -> pd.DataFrame    # 利润表
ak.stock_balance_sheet_by_report_em(symbol: str = "000001") -> pd.DataFrame   # 资产负债表
ak.stock_cash_flow_sheet_by_report_em(symbol: str = "000001") -> pd.DataFrame # 现金流量表
```

### 财务指标
```python
ak.stock_financial_analysis_indicator(symbol: str = "000001") -> pd.DataFrame
# 主要财务指标；可能超时

ak.stock_financial_analysis_indicator_em(
    symbol: str = "000001.SZ",    # 需加市场后缀 .SZ/.SH
    indicator: str = "按报告期",
) -> pd.DataFrame   # 东财版，推荐
```

### 业绩与分配
```python
ak.stock_yjbb_em(date: str = "20240930") -> pd.DataFrame    # 业绩报表
ak.stock_yjyg_em(date: str = "20240930") -> pd.DataFrame    # 业绩预告
ak.stock_yjkb_em(date: str = "20240930") -> pd.DataFrame    # 业绩快报
ak.stock_fhps_em(symbol: str = "000001") -> pd.DataFrame    # 分红配送
ak.stock_sy_em(symbol: str = "000001") -> pd.DataFrame      # 收益指标
ak.stock_yysj_em(symbol: str = "000001") -> pd.DataFrame    # 营收数据
```

---

## 股东与公司

### 股东数据
```python
ak.stock_gdfx_free_top_10_em(symbol: str = "000001") -> pd.DataFrame  # 十大流通股东
ak.stock_gdfx_top_10_em(symbol: str = "000001") -> pd.DataFrame       # 十大股东
ak.stock_zh_a_gdhs(symbol: str = "000001") -> pd.DataFrame            # 股东户数变化
ak.stock_main_stock_holder(symbol: str = "000001") -> pd.DataFrame    # 主要股东
```

### 机构与高管
```python
ak.stock_institute_hold(symbol: str = "000001") -> pd.DataFrame    # 机构持仓
ak.stock_institute_recommend() -> pd.DataFrame                      # 机构推荐
ak.stock_hold_management_detail_em(symbol: str) -> pd.DataFrame    # 高管持股
ak.stock_analyst_rank_em() -> pd.DataFrame                         # 分析师排名
```

### 公司动态
```python
ak.stock_repurchase_em(symbol: str = "000001") -> pd.DataFrame     # 股票回购
ak.stock_changes_em(symbol: str = "000001") -> pd.DataFrame        # 公司变动
```

### 限售解禁
```python
ak.stock_restricted_release_queue_em() -> pd.DataFrame            # 限售解禁队列
ak.stock_restricted_release_summary_em() -> pd.DataFrame          # 解禁汇总
ak.stock_restricted_release_detail_em(symbol: str) -> pd.DataFrame # 个股解禁详情
```

---

## 市场估值

```python
ak.stock_a_all_pb() -> pd.DataFrame              # 全A市净率（历史分位）
ak.stock_a_ttm_lyr() -> pd.DataFrame             # 全A市盈率（历史分位），无参数

ak.stock_zh_valuation_baidu(
    symbol: str = "000001",
    indicator: str = "总市值",   # "总市值" / "市盈率" / "市净率" / "市销率" 等
) -> pd.DataFrame

ak.stock_zh_valuation_comparison_em(symbol: str = "000001") -> pd.DataFrame  # 同行业估值对比
ak.stock_dxsyl_em() -> pd.DataFrame   # 全市场股息率；较慢
```

---

## 港股

```python
ak.stock_hk_spot_em() -> pd.DataFrame    # 港股实时；较慢

ak.stock_hk_hist(
    symbol: str = "00700",     # 5位数字，腾讯：00700
    period: str = "daily",
    start_date: str = "20240101",
    end_date: str = "20241231",
    adjust: str = "",
) -> pd.DataFrame

ak.stock_hk_hist_min_em(
    symbol: str = "00700",
    period: str = "1",                         # "1"/"5"/"15"/"30"/"60"
    start_date: str = "2025-03-27 09:30:00",   # YYYY-MM-DD HH:MM:SS
    end_date: str = "2025-03-27 16:00:00",
) -> pd.DataFrame

ak.stock_zh_ah_spot_em() -> pd.DataFrame   # AH股价格对比
```

---

## 美股

```python
ak.stock_us_spot_em() -> pd.DataFrame   # 美股实时；较慢

ak.stock_us_hist(
    symbol: str = "AAPL",      # 大写 Ticker
    period: str = "daily",
    start_date: str = "20240101",
    end_date: str = "20241231",
    adjust: str = "qfq",
) -> pd.DataFrame

ak.stock_us_hist_min_em(
    symbol: str = "AAPL",
    period: str = "1",                         # "1"/"5"/"15"/"30"/"60"
    start_date: str = "2025-03-27 09:30:00",
    end_date: str = "2025-03-27 16:00:00",
) -> pd.DataFrame
```

---

## 期货

```python
ak.futures_display_main_sina() -> pd.DataFrame
# 返回：symbol（如 "RB"）, exchange（如 "SHFE"）, name（如 "螺纹钢"）

ak.futures_main_sina(
    symbol: str = "RB",        # Sina 命名，先用 futures_display_main_sina() 查映射
    start_date: str = "20200101",
    end_date: str = "20241231",
) -> pd.DataFrame
# 返回（8列）：日期、开盘价、最高价、最低价、收盘价、成交量、持仓量、动态结算价
```

常用期货代码：RB（螺纹钢）、CU（铜）、AU（黄金）、AG（白银）、C0（玉米）、M0（豆粕）、IF（沪深300）、IC（中证500）、T（10年国债）

---

## ETF

ETF 代码：6位纯数字，无市场前缀。沪市 `51xxxx`（如 `510300`），深市 `15xxxx`（如 `159919`）。

### ETF 实时行情

```python
ak.fund_etf_spot_em() -> pd.DataFrame
# 全市场 ETF 实时行情，无参数
```

**返回字段（37列，精选常用）：**

| 列名 | 说明 |
|------|------|
| 代码 | 6位纯数字 |
| 名称 | ETF简称 |
| 最新价 | 实时价格 |
| IOPV实时估值 | 盘中参考净值 |
| 基金折价率 | 折溢价率（%）|
| 涨跌幅 | % |
| 成交量 | 份额 |
| 成交额 | 元 |
| 主力净流入-净额 | 主力资金净流入 |
| 最新份额 | 最新份额（申赎变化）|
| 总市值 | 元 |
| 数据日期 | 交易日期 |

### ETF 历史K线

```python
ak.fund_etf_hist_em(
    symbol: str = "510300",    # 6位数字，无前缀
    period: str = "daily",     # "daily" / "weekly" / "monthly"
    start_date: str = "20200101",
    end_date: str = "20261231",
    adjust: str = "",          # "" 不复权 | "qfq" 前复权 | "hfq" 后复权
) -> pd.DataFrame
# 返回（11列）：日期、开盘、收盘、最高、最低、成交量、成交额、振幅(%)、涨跌幅(%)、涨跌额、换手率(%)
```

### ETF 分钟线

```python
ak.fund_etf_hist_min_em(
    symbol: str = "510300",
    period: str = "5",                         # "1"/"5"/"15"/"30"/"60"
    start_date: str = "2025-01-01 09:30:00",   # YYYY-MM-DD HH:MM:SS
    end_date: str = "2025-12-31 15:00:00",
    adjust: str = "",                          # period="1" 时 adjust 无效
) -> pd.DataFrame
```

### ETF 列表与净值

```python
ak.fund_etf_category_sina(symbol: str = "ETF基金") -> pd.DataFrame
# 新浪数据源 ETF 列表（含实时市价）
# symbol："ETF基金" / "LOF基金" / "封闭式基金"
# 注意：返回的代码列含市场前缀，如 "sh510300"

ak.fund_name_em() -> pd.DataFrame
# 全部基金列表（~10000+），字段：基金代码、基金简称、基金类型
# 筛选 ETF：df[df["基金类型"].str.contains("ETF", na=False)]

ak.fund_etf_fund_info_em(
    fund: str = "510300",
    start_date: str = "20200101",
    end_date: str = "20261231",
) -> pd.DataFrame
# 单只 ETF 历史净值（日频）
# 返回字段：净值日期、单位净值、累计净值、日增长率、申购状态、赎回状态
```

### 常用 ETF 代码参考

| 代码 | 名称 | 跟踪标的 |
|------|------|---------|
| 510300 | 华泰柏瑞沪深300ETF | 沪深300 |
| 159919 | 嘉实沪深300ETF | 沪深300 |
| 510500 | 南方中证500ETF | 中证500 |
| 512100 | 南方中证1000ETF | 中证1000 |
| 510050 | 华夏上证50ETF | 上证50 |
| 159949 | 华夏创业板ETF | 创业板指 |
| 588000 | 华夏科创50ETF | 科创50 |
| 513500 | 南方标普500ETF | 标普500 |
| 511010 | 华夏国债ETF | 国债 |
| 518880 | 华安黄金ETF | 黄金现货 |

---

## 基金

```python
ak.fund_open_fund_daily_em() -> pd.DataFrame   # 开放式基金列表（含基金代码）

ak.fund_open_fund_info_em(
    symbol: str = "000478",
    indicator: str = "单位净值走势",
    period: str = "成立来",    # 仅 indicator="累计收益率走势" 时有效
) -> pd.DataFrame
```

indicator 可选值：`"单位净值走势"`（净值日期/单位净值/日增长率）、`"累计净值走势"`、`"累计收益率走势"`、`"同类排名走势"`、`"分红送配详情"`、`"拆分详情"`

period 可选值（累计收益率走势时）：`"1月"` / `"3月"` / `"6月"` / `"1年"` / `"3年"` / `"5年"` / `"今年来"` / `"成立来"`

---

## 宏观经济（中国）

> Jin10 系列函数（`_yearly`/`_monthly`）均无参数，返回 5 列：商品、日期、今值、预测值、前值。

```python
# ── 物价 ────────────────────────────────────
ak.macro_china_cpi()              # NBS 月度详细 CPI（2008 年起），含城市/农村分类
ak.macro_china_cpi_yearly()       # Jin10 CPI 同比（1986 年起）
ak.macro_china_cpi_monthly()      # Jin10 CPI 环比（1996 年起）
ak.macro_china_ppi()              # NBS 月度 PPI（生产者价格指数）
ak.macro_china_ppi_yearly()       # Jin10 PPI 同比

# ── 景气 ────────────────────────────────────
ak.macro_china_pmi_yearly()       # 官方制造业 PMI（2005 年起）
ak.macro_china_cx_pmi_yearly()    # 财新制造业 PMI 终值（2012 年起）

# ── 货币与信贷 ───────────────────────────────
ak.macro_china_m2_yearly()        # M2 同比（1998 年起）
ak.macro_china_lpr()              # LPR 贷款基础利率（历史序列）
ak.macro_china_shibor_all()       # SHIBOR 各期限历史利率

# ── 增长 ────────────────────────────────────
ak.macro_china_gdp()              # NBS 季度 GDP 分产业（2006 Q1 起）
ak.macro_china_gdp_yearly()       # Jin10 GDP 季度同比（2011 年起）
ak.macro_china_industrial_production_yoy()   # 工业增加值（月度同比）
ak.macro_china_fixed_asset_investment_yoy()  # 固定资产投资（月度同比）
ak.macro_china_retail_sales_yoy()            # 社会消费品零售额（月度同比）

# ── 外贸与外汇 ───────────────────────────────
ak.macro_china_trade_all()        # 进出口月度数据（含贸易差额）
ak.macro_china_fx_reserves_yearly()  # 外汇储备（月度，亿美元）
```

---

## 宏观经济（美国）

```python
ak.macro_usa_cpi_monthly()        # 美国 CPI 月度
ak.macro_usa_pmi()                # 美国 PMI（制造业）
ak.macro_usa_gdp_monthly()        # 美国 GDP
ak.macro_usa_non_farm()           # 美国非农就业人数（月度）
ak.macro_usa_interest_rate()      # 美联储利率决议历史
ak.macro_usa_unemployment_rate()  # 美国失业率
```

---

## 可转债

```python
ak.bond_zh_cov() -> pd.DataFrame
# 可转债实时行情列表（代码、名称、最新价、涨跌幅、转股价、溢价率等）

ak.bond_zh_cov_daily(symbol: str = "113008") -> pd.DataFrame
# 单只可转债历史日线（6位数字代码，与正股代码格式相同）
# 返回字段：日期、开盘、收盘、最高、最低、成交量

ak.bond_cov_comparison() -> pd.DataFrame
# 可转债与正股价格对比（溢价率分析辅助）
```

---

## 期权

```python
ak.option_current_em(symbol: str = "沪深300ETF期权") -> pd.DataFrame
# A股期权实时行情（ETF期权/指数期权）
# symbol 示例："沪深300ETF期权"、"上证50ETF期权"

ak.option_finance_board() -> pd.DataFrame
# 期权市场总览（PCR、成交量、持仓量等）
```

---

## 加密货币与外汇

```python
# 加密货币（币安数据源）
ak.crypto_binance_btc_usdt_spot() -> pd.DataFrame           # BTC/USDT 实时
ak.crypto_binance_btc_usdt_kline(period: str = "daily")     # BTC K线
ak.crypto_binance_symbols() -> pd.DataFrame                 # 所有交易对列表

# 外汇与贵金属
ak.forex_usd_cny() -> pd.DataFrame    # 美元兑人民币历史汇率
ak.metals_gold() -> pd.DataFrame      # 国际金价历史
```
