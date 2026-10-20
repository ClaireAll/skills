## Contents
- 批量下载多只股票（含限速与异常处理）
- 全市场实时行情筛选
- 行业板块筛选并批量下载K线
- 获取指数成分股K线（沪深300）
- A股分钟线获取
- 资金流向分析（个股 + 板块）
- 涨停池分析
- 龙虎榜分析
- 财务报表分析（三大报表）
- 股东数据分析
- 期货主力连续批量下载
- 基金净值历史查询
- 宏观数据综合查询
- ETF 分析（实时筛选/历史K线/折溢价监控）
- 宏观大盘仪表板（15+ 指标合并）
- 可转债分析
- 增量更新（Parquet 本地存储）
- 完整技术指标计算（MA/MACD/KDJ/RSI/BOLL）

---

## 批量下载多只股票（含限速与异常处理）

```python
import akshare as ak
import pandas as pd
import time

codes = ["000001", "600519", "300750", "002594"]
frames = []

for code in codes:
    try:
        df = ak.stock_zh_a_hist(
            symbol=code,
            period="daily",
            start_date="20240101",
            end_date="20241231",
            adjust="qfq"
        )
        if not df.empty:
            frames.append(df)
        else:
            print(f"{code}: 返回空（退市或日期范围无数据）")
    except Exception as e:
        print(f"{code} 下载失败: {e}")

    time.sleep(0.5)   # 防东财 IP 封锁

result = pd.concat(frames, ignore_index=True) if frames else pd.DataFrame()
print(f"共获取 {len(result):,} 条记录")
```

---

## 全市场实时行情筛选

```python
import akshare as ak
import pandas as pd

# 用分市场接口更快（沪 ~28s，各市场分别调用）
df_sh = ak.stock_sh_a_spot_em()
df_sz = ak.stock_sz_a_spot_em()
df = pd.concat([df_sh, df_sz], ignore_index=True)

# 筛选：涨幅超过 5%，成交量大于 10 万手，市盈率合理
strong = df[
    (df["涨跌幅"] > 5) &
    (df["成交量"] > 100_000) &
    (df["市盈率-动态"] > 0) & (df["市盈率-动态"] < 100)
][["代码", "名称", "最新价", "涨跌幅", "成交量", "换手率", "总市值", "市盈率-动态"]]

strong = strong.sort_values("涨跌幅", ascending=False)
print(strong.head(20))
```

---

## 行业板块筛选并批量下载K线

```python
import akshare as ak
import pandas as pd
import time

# 第1步：查看行业板块涨跌排名
df_boards = ak.stock_board_industry_name_em()
print(df_boards[["板块名称", "涨跌幅", "上涨家数", "下跌家数"]]
      .sort_values("涨跌幅", ascending=False).head(10))

# 第2步：获取目标板块成分股
target_board = "银行"
df_members = ak.stock_board_industry_cons_em(symbol=target_board)
codes = df_members["代码"].tolist()
print(f"{target_board}板块共 {len(codes)} 只股票")

# 第3步：获取板块整体历史K线（比逐股下载快）
df_board_hist = ak.stock_board_industry_hist_em(
    symbol=target_board,
    period="daily",
    start_date="20240101",
    end_date="20241231",
)
print(df_board_hist.tail())

# 第4步：批量下载个股K线
frames = []
for code in codes:
    try:
        df = ak.stock_zh_a_hist(
            symbol=code, period="daily",
            start_date="20240101", end_date="20241231",
            adjust="qfq"
        )
        if not df.empty:
            df["板块"] = target_board
            frames.append(df)
    except Exception as e:
        print(f"{code} 失败: {e}")
    time.sleep(0.5)

sector_df = pd.concat(frames, ignore_index=True) if frames else pd.DataFrame()
```

---

## 获取指数成分股K线（沪深300）

```python
import akshare as ak
import pandas as pd
import time

# index_stock_cons_csindex 比 index_stock_cons 更精确，含纳入日期
cons = ak.index_stock_cons_csindex(symbol="000300")
codes = cons["成分券代码"].tolist()
print(f"沪深300共 {len(codes)} 只成分股")

# 获取指数本身（基准）
index_df = ak.index_zh_a_hist(
    symbol="000300", period="daily",
    start_date="20240101", end_date="20241231"
)
index_df["日期"] = pd.to_datetime(index_df["日期"])

# 批量下载成分股K线
frames = []
for code in codes:
    try:
        df = ak.stock_zh_a_hist(
            symbol=code, period="daily",
            start_date="20240101", end_date="20241231",
            adjust="qfq"
        )
        if not df.empty:
            frames.append(df)
    except Exception as e:
        print(f"{code} 失败: {e}")
    time.sleep(0.5)

hs300_df = pd.concat(frames, ignore_index=True)
hs300_df["日期"] = pd.to_datetime(hs300_df["日期"])
print(f"沪深300成分股共 {len(hs300_df):,} 条")
```

---

## A股分钟线获取

```python
import akshare as ak
import pandas as pd

# 分钟线日期格式为 YYYY-MM-DD HH:MM:SS，不是 YYYYMMDD
df_5min = ak.stock_zh_a_hist_min_em(
    symbol="000001",
    period="5",
    start_date="2024-12-01 09:30:00",
    end_date="2024-12-31 15:00:00",
    adjust="qfq"
)

df_5min["时间"] = pd.to_datetime(df_5min["时间"])
df_5min = df_5min.rename(columns={
    "时间": "datetime", "开盘": "open", "收盘": "close",
    "最高": "high", "最低": "low", "成交量": "volume"
})
print(f"5分钟线共 {len(df_5min)} 条")

# 1分钟线（只有近5个交易日，无复权）
df_1min = ak.stock_zh_a_hist_min_em(
    symbol="000001",
    period="1",
    start_date="2024-12-27 09:30:00",
    end_date="2024-12-31 15:00:00",
)
```

---

## 资金流向分析（个股 + 板块）

```python
import akshare as ak
import pandas as pd

# ── 个股资金流（今日）────────────────────────
# market：沪市主板 "sh"，深市/创业板/科创板 "sz"
df_flow = ak.stock_individual_fund_flow(stock="000001", market="sz")
print(df_flow)

# ── 个股历史资金流（近60天）────────────────
df_flow_hist = ak.stock_fund_flow_individual(stock="000001", market="sz")
df_flow_hist["日期"] = pd.to_datetime(df_flow_hist["日期"])
print(df_flow_hist.tail(10))

# ── 全市场个股资金流排名────────────────────
df_rank = ak.stock_individual_fund_flow_rank(indicator="今日")
# 筛选主力净流入 Top20
top20 = df_rank.sort_values("主力净流入-净额", ascending=False).head(20)
print(top20[["代码", "名称", "最新价", "涨跌幅", "主力净流入-净额", "主力净流入-净占比"]])

# ── 行业板块资金流排名────────────────────
df_ind_flow = ak.stock_fund_flow_industry(indicator="今日")
print(df_ind_flow.sort_values("主力净流入-净额", ascending=False).head(10))

# ── 概念板块资金流排名────────────────────
df_con_flow = ak.stock_fund_flow_concept(indicator="今日")
print(df_con_flow.sort_values("主力净流入-净额", ascending=False).head(10))
```

---

## 涨停池分析

```python
import akshare as ak
import pandas as pd
import datetime

# 获取最近交易日（手动指定，或从实时行情反推）
today = datetime.date.today().strftime("%Y%m%d")

# ── 当日涨停池────────────────────────────
df_zt = ak.stock_zt_pool_em(date=today)
print(f"今日涨停股 {len(df_zt)} 只")
print(df_zt[["代码", "名称", "涨跌幅", "最终涨停时间", "涨停统计", "连板数", "所属行业"]].head(20))

# ── 强势股池（包含近期连板）────────────────
df_strong = ak.stock_zt_pool_strong_em(date=today)
print(f"强势股 {len(df_strong)} 只")

# ── 昨日涨停跟踪（观察次日表现）────────────
df_prev_zt = ak.stock_zt_pool_previous_em(date=today)
print(f"昨日涨停 {len(df_prev_zt)} 只")

# ── 当日跌停池（近30个交易日内有效）────────
df_dt = ak.stock_zt_pool_dtgc_em(date=today)
print(f"今日跌停股 {len(df_dt)} 只")

# 连板统计
if not df_zt.empty and "连板数" in df_zt.columns:
    df_zt["连板数"] = pd.to_numeric(df_zt["连板数"], errors="coerce")
    lianban = df_zt[df_zt["连板数"] >= 2].sort_values("连板数", ascending=False)
    print(f"\n连板股（2板+）共 {len(lianban)} 只：")
    print(lianban[["代码", "名称", "连板数", "所属行业"]])
```

---

## 龙虎榜分析

```python
import akshare as ak
import pandas as pd

# ── 龙虎榜明细（指定日期范围）────────────────
df_lhb = ak.stock_lhb_detail_em(
    start_date="20241201",
    end_date="20241231"
)
print(f"龙虎榜记录 {len(df_lhb)} 条")
print(df_lhb.columns.tolist())

# ── 个股龙虎榜历史────────────────────────
df_lhb_stock = ak.stock_lhb_stock_detail_em(symbol="000001")
print(df_lhb_stock)

# ── 机构席位统计────────────────────────
df_jg = ak.stock_lhb_jgstatistic_em()
print(df_jg.head(10))   # 机构净买入最多的标的

# ── 营业部排行────────────────────────
df_yyb = ak.stock_lhb_yybph_em()
print(df_yyb.head(10))
```

---

## 财务报表分析（三大报表）

```python
import akshare as ak
import pandas as pd

symbol = "000001"

# ── 财务摘要（同花顺，数据较全）────────────
df_abs = ak.stock_financial_abstract_ths(
    symbol=symbol,
    indicator="按报告期"   # "按报告期" / "按年度" / "按单季度"
)
print(df_abs.columns.tolist())
print(df_abs.head())

# ── 利润表────────────────────────────
df_profit = ak.stock_profit_sheet_by_report_em(symbol=symbol)
print(df_profit.columns.tolist())

# ── 资产负债表────────────────────────
df_balance = ak.stock_balance_sheet_by_report_em(symbol=symbol)

# ── 现金流量表────────────────────────
df_cf = ak.stock_cash_flow_sheet_by_report_em(symbol=symbol)

# ── 业绩报表（全市场某季度）────────────────
df_yjbb = ak.stock_yjbb_em(date="20240930")
print(f"业绩报表共 {len(df_yjbb)} 条")

# ── 主要财务指标（东财版，推荐）────────────
# symbol 需加市场后缀：沪市/科创板 .SH，深市/创业板 .SZ
df_fi = ak.stock_financial_analysis_indicator_em(
    symbol="000001.SZ",
    indicator="按报告期"
)
print(df_fi.head())
```

---

## 股东数据分析

```python
import akshare as ak
import pandas as pd

symbol = "600519"   # 贵州茅台

# ── 十大流通股东────────────────────────
df_top10_free = ak.stock_gdfx_free_top_10_em(symbol=symbol)
print("十大流通股东：")
print(df_top10_free)

# ── 十大股东────────────────────────
df_top10 = ak.stock_gdfx_top_10_em(symbol=symbol)

# ── 股东户数（观察集中度变化）────────────
df_gdhs = ak.stock_zh_a_gdhs(symbol=symbol)
df_gdhs["截止日期"] = pd.to_datetime(df_gdhs["截止日期"])
print("\n股东户数趋势（近8期）：")
print(df_gdhs[["截止日期", "股东户数", "股东户数增减"]].tail(8))

# ── 机构持仓────────────────────────
df_inst = ak.stock_institute_hold(symbol=symbol)
print("\n机构持仓：")
print(df_inst.head())

# ── 限售解禁（全市场近期）────────────────
df_unlock = ak.stock_restricted_release_queue_em()
# 筛选未来1个月解禁
df_unlock["解禁日期"] = pd.to_datetime(df_unlock["解禁日期"])
import datetime
upcoming = df_unlock[
    df_unlock["解禁日期"] > pd.Timestamp.now()
].sort_values("解禁日期").head(20)
print("\n即将解禁：")
print(upcoming[["解禁日期", "股票代码", "股票简称", "解禁数量（万股）", "解禁市值（亿元）"]])
```

---

## 期货主力连续批量下载

```python
import akshare as ak
import pandas as pd
import time

# 获取品种映射（Sina 代码 → 品种名称）
symbol_map = ak.futures_display_main_sina()
print(symbol_map.head(20))

# 批量下载指定品种
target_symbols = ["RB", "CU", "AU", "IF", "IC", "M0"]
frames = {}

for sym in target_symbols:
    try:
        df = ak.futures_main_sina(
            symbol=sym,
            start_date="20200101",
            end_date="20241231"
        )
        if not df.empty:
            df["日期"] = pd.to_datetime(df["日期"])
            for col in ["开盘价", "最高价", "最低价", "收盘价"]:
                df[col] = pd.to_numeric(df[col], errors="coerce")
            frames[sym] = df
            print(f"{sym}: {len(df)} 条")
    except Exception as e:
        print(f"{sym} 失败: {e}")
    time.sleep(0.3)

result = pd.concat(
    [df.assign(symbol=sym) for sym, df in frames.items()],
    ignore_index=True
)
```

---

## 基金净值历史查询

```python
import akshare as ak
import pandas as pd

# 获取基金列表
fund_list = ak.fund_open_fund_daily_em()
target = fund_list[fund_list["基金简称"].str.contains("中证500")]
print(target[["基金代码", "基金简称"]].head())

fund_code = "000478"   # 建信中证500

# 单位净值历史
df_nav = ak.fund_open_fund_info_em(symbol=fund_code, indicator="单位净值走势")
df_nav["净值日期"] = pd.to_datetime(df_nav["净值日期"])
df_nav["单位净值"] = pd.to_numeric(df_nav["单位净值"], errors="coerce")
print(df_nav.tail())

# 近1年累计收益率
df_ret = ak.fund_open_fund_info_em(
    symbol=fund_code,
    indicator="累计收益率走势",
    period="1年"
)

# 分红送配历史
df_div = ak.fund_open_fund_info_em(symbol=fund_code, indicator="分红送配详情")
print(df_div)
```

---

## 宏观数据综合查询

```python
import akshare as ak
import pandas as pd

# CPI 月度同比（NBS 版，字段最全）
cpi = ak.macro_china_cpi()
print(cpi[["月份", "全国-当月", "全国-同比增长", "全国-环比增长"]].tail(12))

# PMI 官方制造业
pmi = ak.macro_china_pmi_yearly()
pmi["日期"] = pd.to_datetime(pmi["日期"])
pmi = pmi.rename(columns={"今值": "PMI"})

# M2 同比
m2 = ak.macro_china_m2_yearly()
m2["日期"] = pd.to_datetime(m2["日期"])
m2 = m2.rename(columns={"今值": "M2_yoy"})

# GDP 分产业（NBS 版）
gdp = ak.macro_china_gdp()
print(gdp[["季度", "国内生产总值-绝对值", "国内生产总值-同比增长"]].tail(8))

# 合并 PMI + M2 到季频 DataFrame
pmi_q = pmi.set_index("日期")["PMI"].resample("QE").last()
m2_q  = m2.set_index("日期")["M2_yoy"].resample("QE").last()
macro_df = pd.concat([pmi_q, m2_q], axis=1).dropna()
print(macro_df.tail(8))
```

---

## ETF 分析（实时筛选/历史K线/折溢价监控）

```python
import akshare as ak
import pandas as pd
import time

# ── 全市场 ETF 实时行情（含 IOPV、折溢价、主力资金流）──
df_etf = ak.fund_etf_spot_em()
print(f"全市场 ETF 共 {len(df_etf)} 只")

# 筛选观察样本：折价不等于买入机会，先核对口径、更新时间和流动性
discount = df_etf[
    pd.to_numeric(df_etf["基金折价率"], errors="coerce") < -1
][["代码", "名称", "最新价", "IOPV实时估值", "基金折价率", "涨跌幅", "成交额"]]
print(f"\n折价超过 1% 的 ETF：{len(discount)} 只")
print(discount.sort_values("基金折价率").head(10))

# 按主力净流入排名（ETF 资金吸引力）
inflow = df_etf.sort_values("主力净流入-净额", ascending=False)
print("\n主力净流入 Top10：")
print(inflow[["代码", "名称", "主力净流入-净额", "涨跌幅"]].head(10))

# ── ETF 历史K线（日线，前复权）────────────────────
# 常用宽基 ETF 批量下载
etf_codes = {
    "510300": "沪深300ETF",
    "510500": "中证500ETF",
    "512100": "中证1000ETF",
    "513500": "标普500ETF",
    "518880": "黄金ETF",
}

frames = {}
for code, name in etf_codes.items():
    try:
        df = ak.fund_etf_hist_em(
            symbol=code,
            period="daily",
            start_date="20200101",
            end_date="20261231",
            adjust="qfq"
        )
        if not df.empty:
            df["日期"] = pd.to_datetime(df["日期"])
            df["名称"] = name
            frames[code] = df
            print(f"{name}({code}): {len(df)} 条")
    except Exception as e:
        print(f"{code} 失败: {e}")
    time.sleep(0.3)

# ── 计算各 ETF 的累计收益率对比 ────────────────────
returns = {}
for code, df in frames.items():
    df_sorted = df.sort_values("日期")
    base = df_sorted["收盘"].iloc[0]
    returns[code] = (df_sorted.set_index("日期")["收盘"] / base - 1) * 100

df_returns = pd.DataFrame(returns)
df_returns.columns = [etf_codes[c] for c in df_returns.columns]
print("\n各 ETF 累计收益率（最近5个交易日）：")
print(df_returns.tail())

# ── ETF 净值查询（场外份额变化）──────────────────
df_nav = ak.fund_etf_fund_info_em(
    fund="510300",
    start_date="20240101",
    end_date="20261231"
)
df_nav["净值日期"] = pd.to_datetime(df_nav["净值日期"])
df_nav["单位净值"] = pd.to_numeric(df_nav["单位净值"], errors="coerce")
print(f"\n510300 净值历史 {len(df_nav)} 条：")
print(df_nav.tail())
```

---

## 宏观大盘仪表板（15+ 指标合并）

```python
import akshare as ak
import pandas as pd

def safe_fetch(func, *args, **kwargs):
    """统一异常处理，返回空 DataFrame 而非崩溃。"""
    try:
        df = func(*args, **kwargs)
        return df if not df.empty else pd.DataFrame()
    except Exception as e:
        print(f"{func.__name__} 获取失败: {e}")
        return pd.DataFrame()

# ── 中国宏观 ──────────────────────────────────

# CPI（同比）
cpi = safe_fetch(ak.macro_china_cpi_yearly)
if not cpi.empty:
    cpi["日期"] = pd.to_datetime(cpi["日期"])
    print("最新CPI同比:", cpi.sort_values("日期").iloc[-1][["日期", "今值"]].to_dict())

# PPI（同比）
ppi = safe_fetch(ak.macro_china_ppi_yearly)
if not ppi.empty:
    ppi["日期"] = pd.to_datetime(ppi["日期"])
    print("最新PPI同比:", ppi.sort_values("日期").iloc[-1][["日期", "今值"]].to_dict())

# PMI
pmi = safe_fetch(ak.macro_china_pmi_yearly)
if not pmi.empty:
    pmi["日期"] = pd.to_datetime(pmi["日期"])
    print("最新PMI:", pmi.sort_values("日期").iloc[-1][["日期", "今值"]].to_dict())

# M2
m2 = safe_fetch(ak.macro_china_m2_yearly)
if not m2.empty:
    m2["日期"] = pd.to_datetime(m2["日期"])
    print("最新M2同比:", m2.sort_values("日期").iloc[-1][["日期", "今值"]].to_dict())

# GDP
gdp = safe_fetch(ak.macro_china_gdp)
if not gdp.empty:
    print("最新GDP:", gdp.iloc[-1][["季度", "国内生产总值-同比增长"]].to_dict())

# LPR
lpr = safe_fetch(ak.macro_china_lpr)
if not lpr.empty:
    print("最新LPR:\n", lpr.tail(2))

# SHIBOR
shibor = safe_fetch(ak.macro_china_shibor_all)
if not shibor.empty:
    print("最新SHIBOR:\n", shibor.tail(1))

# ── 合并时序 DataFrame（对齐到月频）─────────────

def to_monthly_series(df, date_col, value_col, name):
    if df.empty or date_col not in df.columns:
        return pd.Series(name=name, dtype=float)
    df = df.copy()
    df[date_col] = pd.to_datetime(df[date_col], errors="coerce")
    return (df.set_index(date_col)[value_col]
              .dropna()
              .resample("ME").last()
              .rename(name))

macro_monthly = pd.concat([
    to_monthly_series(cpi, "日期", "今值", "CPI同比(%)"),
    to_monthly_series(ppi, "日期", "今值", "PPI同比(%)"),
    to_monthly_series(pmi, "日期", "今值", "PMI"),
    to_monthly_series(m2,  "日期", "今值", "M2同比(%)"),
], axis=1)

print("\n宏观月频仪表板（最近12期）：")
print(macro_monthly.dropna(how="all").tail(12).to_string())
```

---

## 可转债分析

```python
import akshare as ak
import pandas as pd

# ── 获取全市场可转债实时行情 ──────────────────
df_cov = ak.bond_zh_cov()
print(f"可转债共 {len(df_cov)} 只")
print(df_cov.columns.tolist())
print(df_cov.head())

# 按溢价率筛选（低溢价可转债，接近纯债）
# 具体列名以实际返回为准，常见字段：转债代码、转债名称、最新价、涨跌幅、转股价、转股溢价率
if "转股溢价率" in df_cov.columns:
    low_prem = df_cov[
        pd.to_numeric(df_cov["转股溢价率"], errors="coerce") < 10
    ].sort_values("转股溢价率")
    print(f"\n低溢价率（<10%）可转债 {len(low_prem)} 只：")
    print(low_prem.head(10))

# ── 获取单只可转债历史K线 ──────────────────
# 可转债代码为 6 位数字（如 113008 = 转债代码，非股票代码）
df_cov_hist = ak.bond_zh_cov_daily(symbol="113008")
if not df_cov_hist.empty:
    df_cov_hist["日期"] = pd.to_datetime(df_cov_hist["日期"])
    df_cov_hist["收盘"] = pd.to_numeric(df_cov_hist["收盘"], errors="coerce")
    print(f"\n历史K线 {len(df_cov_hist)} 条：")
    print(df_cov_hist.tail(5))

# ── 可转债与正股对比（溢价率变化）────────────
# 先从 bond_zh_cov() 中找到对应正股代码，再获取正股K线对比
```

---

## 增量更新（Parquet 本地存储）

```python
import akshare as ak
import pandas as pd
from pathlib import Path
import time
import datetime

PARQUET_PATH = "data/akshare_daily.parquet"

def get_last_date(code: str) -> str:
    if not Path(PARQUET_PATH).exists():
        return "20100101"
    df = pd.read_parquet(PARQUET_PATH, filters=[("股票代码", "=", code)])
    if df.empty:
        return "20100101"
    return df["日期"].max().strftime("%Y%m%d")

def incremental_update(codes: list):
    today = datetime.date.today().strftime("%Y%m%d")
    new_frames = []

    for code in codes:
        last = get_last_date(code)
        if last >= today:
            continue

        try:
            df = ak.stock_zh_a_hist(
                symbol=code, period="daily",
                start_date=last, end_date=today,
                adjust="qfq"
            )
            if not df.empty:
                df["日期"] = pd.to_datetime(df["日期"])
                new_frames.append(df)
        except Exception as e:
            print(f"{code} 更新失败: {e}")
        time.sleep(0.5)

    if not new_frames:
        print("无新数据")
        return

    new_df = pd.concat(new_frames, ignore_index=True)

    if Path(PARQUET_PATH).exists():
        old_df = pd.read_parquet(PARQUET_PATH)
        combined = (pd.concat([old_df, new_df])
                    .drop_duplicates(subset=["日期", "股票代码"])
                    .reset_index(drop=True))
    else:
        Path("data").mkdir(exist_ok=True)
        combined = new_df

    combined.to_parquet(PARQUET_PATH, index=False, compression="snappy")
    print(f"更新完成，新增 {len(new_df):,} 条")

incremental_update(["000001", "600519", "300750"])
```

---

## 完整技术指标计算（MA/MACD/KDJ/RSI/BOLL）

```python
import akshare as ak
import pandas as pd
import numpy as np

df = ak.stock_zh_a_hist(
    symbol="000001",
    period="daily",
    start_date="20230101",
    end_date="20241231",
    adjust="qfq"
)
df = df.rename(columns={
    "日期": "date", "开盘": "open", "收盘": "close",
    "最高": "high", "最低": "low", "成交量": "volume"
})
df["date"] = pd.to_datetime(df["date"])
df = df.dropna(subset=["close"]).reset_index(drop=True)

# ── 均线系统 ──────────────────────────────
for n in [5, 10, 20, 60, 120, 250]:
    df[f"ma{n}"] = df["close"].rolling(n).mean()

# ── MACD（DIF/DEA/柱状线）────────────────
ema12 = df["close"].ewm(span=12, adjust=False).mean()
ema26 = df["close"].ewm(span=26, adjust=False).mean()
df["macd_dif"] = ema12 - ema26
df["macd_dea"] = df["macd_dif"].ewm(span=9, adjust=False).mean()
df["macd"]     = 2 * (df["macd_dif"] - df["macd_dea"])

# ── KDJ（9日随机指标）────────────────────
low9  = df["low"].rolling(9).min()
high9 = df["high"].rolling(9).max()
rsv   = (df["close"] - low9) / (high9 - low9).replace(0, np.nan) * 100
df["kdj_k"] = rsv.ewm(com=2, adjust=False).mean()
df["kdj_d"] = df["kdj_k"].ewm(com=2, adjust=False).mean()
df["kdj_j"] = 3 * df["kdj_k"] - 2 * df["kdj_d"]

# ── RSI（6/12/24日）──────────────────────
def calc_rsi(series, period):
    delta = series.diff()
    gain  = delta.clip(lower=0).ewm(com=period - 1, adjust=False).mean()
    loss  = (-delta.clip(upper=0)).ewm(com=period - 1, adjust=False).mean()
    return 100 - 100 / (1 + gain / loss.replace(0, np.nan))

df["rsi_6"]  = calc_rsi(df["close"], 6)
df["rsi_12"] = calc_rsi(df["close"], 12)
df["rsi_24"] = calc_rsi(df["close"], 24)

# ── 布林带（20日，2倍标准差）──────────────
df["boll_mid"] = df["close"].rolling(20).mean()
std20 = df["close"].rolling(20).std()
df["boll_upper"] = df["boll_mid"] + 2 * std20
df["boll_lower"] = df["boll_mid"] - 2 * std20

print(df[["date", "close", "ma20", "macd_dif", "kdj_k", "rsi_12", "boll_upper"]].tail())
```
