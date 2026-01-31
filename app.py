import streamlit as st
import pandas as pd
import requests
import akshare as ak
import datetime
import time
import math # 引入数学库处理 NaN

# ==========================================
# 🔐 商家后台配置区
# ==========================================
# 你的 VIP 码列表
VALID_VIP_CODES = [

    
    "LIHWQY",
    "GO75ON",
    "DXPIOA",
    "SAMRUO",
    "SGUGKB",
    "K88CTV",
    "I354RX",
    "K9IJMS",
    "4ZF59V",
    "27DP9A",
    "U0CALN",
    "1XVK1D",
    "G6AW46",
    "Q9TXDU",
    "HH4FDG",
    "LGYUB6",
    "2S55MK",
    "82GJKA",
    "7RI4IN",
    "YE9SEZ",
    "VLBGKG",
    "4VKIWT",
    "Q7SL9J",
    "6QEBLO",
    "P1OHJR",
    "59L0A3",
    "L1OTDE",
    "8LH0D3",
    "BMTQSN",
    "F7NKNF",
    "0MJ0RD",
    "TFLKK3",
    "AKBODE",
    "SC87DP",
    "G3WJAG",
    "N3XX4X",
    "AN09RU",
    "I1A2Z3",
    "RH1C5B",
    "Y6RMG9",
    "ZH3G5O",
    "GTCAPG",
    "PZE1LX",
    "WT7Z8O",
    "EO6LXU",
    "BYK569",
    "84IDLA",
    "ETCTZG",
    "P6YI7G",
    "QZGDLB",
    "840423",
    "TWGP8H",
    "15I2DP",
    "HRMRKV",
    "3WY5JH",
    "YJKYFZ",
    "F3M8B4",
    "HVY1W4",
    "AL6ZVQ",
    "QG4QBX",
    "SQV628",
    "258DZZ",
    "1OGV7B",
    "48QEKO",
    "BL6O63",
    "Y6N9IS",
    "MYTEAI",
    "9S53FV",
    "5CPE8K",
    "K5SIFM",
    "95IMWC",
    "YGS2NA",
    "XWP0A4",
    "P451MY",
    "GEX87J",
    "95X7O4",
    "S9MQ6O",
    "J5AFI3",
    "DXYIEQ",
    "Y66CHG",
    "D9V8FH",
    "H12O4L",
    "65WEGJ",
    "6LGBDW",
    "80DKD7",
    "A4RDFR",
    "00QRGW",
    "13QHNJ",
    "44WMQO",
    "9W4NZC",
    "H0GBQ2",
    "Y6VTGA",
    "KN3OF6",
    "H6KA3G",
    "J3YTXA",
    "JORYF5",
    "P96A2L",
    "3YJWVQ",
    "X0X15R",
    "MMGJSH",
    "G7GJZT",
    "CJSHXK",
    "QOCJBF",
    "6KX2C7",
    "OGSS2I",
    "L58E68",
    "0ASVGK",
    "0T1ZNQ",
    "GI5G7T",
    "E7M97K",
    "YL88HE",
    "6VCC9Z",
    "GKKBNX",
    "EWSA8O",
    "XBI78Q",
    "43LBFW",
    "YGG58F",
    "KD3V51",
    "9S779H",
    "C8U703",
    "3F1GC4",
    "FYPW3E",
    "86VG6C",
    "V8QBPS",
    "9VP23J",
    "O12BM6",
    "T272DM",
    "S3YOFJ",
    "653NID",
    "SRXNFS",
    "G7ABM1",
    "PFA1H8",
    "6EMH1M",
    "ZSI3XO",
    "PJL3QC",
    "TU5E4L",
    "80XKAV",
    "V080DA",
    "GP0SKK",
    "T88DUY",
    "CGZ3Y9",
    "G50E47",
    "F8T0KO",
    "2KCFZM",
    "IY2ATM",
    "N0E71I",
    "0UF3GK",
    "NZBL5L",
    "43ZMAX",
    "QNETBH",
    "7D8EX8",
    "V56BPD",
    "2B8TIN",
    "7TFMTB",
    "AH3TFE",
    "QNEBW3",
    "A8BI1R",
    "DVGKT0",
    "XIYVJ1",
    "M9SFAX",
    "XNGA3H",
    "ZDBP7G",
    "WEUXB4",
    "RZW6PZ",
    "3FYY7O",
    "LX2EDJ",
    "8LUHO7",
    "L13NBA",
    "OAYKE2",
    "8IEVEV",
    "OBR9RI",
    "3572CC",
    "P9TL6R",
    "6Z0H88",
    "Z9S6TL",
    "9530N3",
    "APOUVP",
    "3709HV",
    "U16QG5",
    "3N8ONH",
    "4ZOMSV",
    "C2VE7O",
    "9FYUIN",
    "23JB00",
    "9OXVTK",
    "36AUYP",
    "RUJOSV",
    "VN4Z2A",
    "HONT8G",
    "XPYTER",
    "QO73WD",
    "AELK10",
    "DIMHW8",
    "M1UASQ",
    "NYTSB1",
    "LIDHKH",
    "Q7GHEG",
    "7MH9OJ",
    "X0R1F7",
    "Y0EZ9M",
    "07C334",
    "AAX8O6",
    "WO8327",
    "DAUAVQ",
    "38QEQK",
    "JQIPHP",
    "R1GH9B",
    "EOHT0G",
    "KR2N4Z",
    "EM06CT",
    "DK0Z6H",
    "LJODG0",
    "TY0JO0",
    "AKXUOO",
    "RX0CT0",
    "6FGH08",
    "RUCH70",
    "9YK0T8",
    "LQDLU2",
    "ISEE51",
    "88YMAW",
    "COH12C",
    "HDUJD2",
    "2BC43I",
    "JSBYON",
    "ZEKSTU",
    "PQ87U9",
    "PCYBQM",
    "KXAXXB",
    "EN3A42",
    "SI3FDH",
    "HOHFW4",
    "XPSD57",
    "DRRR8B",
    "XU0GOO",
    "UR1TY8",
    "5FF8FK",
    "2GRPJ1",
    "2O9RTZ",
    "4J5GNI",
    "0R2OG9",
    "NLJ2NA",
    "1AUSGT",
    "QW4E37",
    "HO46NH",
    "4ZPY5H",
    "WKHRSX",
    "GI42HT",
    "M6QW91",
    "7L8CU5",
    "BH1Q1C",
    "EMMHCB",
    "6XRE2E",
    "ES3CWD",
    "QHH9D4",
    "N1CPNN",
    "HC4GLH",
    "QJ7VEG",
    "5MQKMA",
    "49QQ4H",
    "8T0N4Z",
    "6ZEYCN",
    "Z6IH77",
    "0CXNYY",
    "GLJ4BU",
    "Q67MM8",
    "FH4T7Y",
    "MQYN28",
    "21CXDN",
    "DVM9AW",
    "TME2E2",
    "1LT52O",
    "J8KU6K",
    "4HI71X",
    "0FE2E5",
    "Y0YIUE",
    "9TZXLN",
    "ZLUIP5",
    "MH88DG",
    "LORK69",
    "6N22F4",
    "Q8WW0B",
    "YH6ZAJ",
    "2N2WZ1",
    "8HEIWZ",
    "Q2BNWC",
    "U5L38M",
    "FHRO69",
    "UKLZHZ",
    "F5XKKW",
    "8JUG4H",
    "QY6EOZ",
    "5JPR7W",
    "Z4WI4T",
    "287KLF",
    "DNLYKH",
    "NIG714",
    "JZK9FY",
    "TEWZPC",
    "2XL8X1",
    "AA9ACG",
    "S3UACW",
    "0MCET6",
    "PFLYYV",
    "PBLX9M",
    "1563I1",
    "PVF13A",
    "U1U8IT",
    "SF0KJZ",
    "UXFLTC",
    "X48VO8",
    "KX0ESO",
    "YEAT8T",
    "HOIDZY",
    "CJ1RL3",
    "49FFL4",
    "R8J3FC",
    "OO8TL8",
    "FOD7HK",
    "2KMDHY",
    "62F4CR",
    "REZAFZ",
    "PON1L4",
    "VCI4GO",
    "UA83U4",
    "BTSERZ",
    "86GFVV",
    "8420CW",
    "CTJIKU",
    "UNQZ9W",
    "BELYI9",
    "SKSA4A",
    "R2WALM",
    "1LD2BH",
    "WRS8OJ",
    "OT13HC",
    "BIZS3T",
    "MHV9OM",
    "Q0O83E",
    "8F3ZZ7",
    "Y66ABO",
    "LJA6Y5",
    "X0RL3F",
    "4Q9UEF",
    "XUMX55",
    "BML70R",
    "1HHV30",
    "0JCVQ3",
    "9A4TPV",
    "2YQ9SC",
    "FVETTK",
    "PA574K",
    "C7VSJ7",
    "UY509L",
    "KK1NHD",
    "WV6S8C",
    "0LLSBZ",
    "W65QK3",
    "KRZYOC",
    "URU82K",
    "23I8S2",
    "M6H908",
    "FFCGH8",
    "HOYV0E",
    "BU76TR",
    "V4DF5Y",
    "M2NNUU",
    "C6T6VT",
    "9HUV22",
    "9JJBSB",
    "WOZWO5",
    "I1B3CC",
    "MIVVBY",
    "A6QAPO",
    "XE4QXN",
    "2WZC9Z",
    "1K6SIP",
    "DEQJCQ",
    "54WT62",
    "NFJV8T",
    "78W5I6",
    "S9U4YW",
    "HJEZ5G",
    "UIIPA1",
    "MWFU2K",
    "2P7OLR",
    "E0PO6V",
    "8068IS",
    "03U9M6",
    "NTH21Z",
    "1O2O9C",
    "INBX55",
    "KIU8R0",
    "19Z98P",
    "4G7OZP",
    "2QRFGF",
    "C886DI",
    "N0O35F",
    "23N2ZJ",
    "B02H58",
    "B1U5DX",
    "LD7LAT",
    "1KZBGF",
    "AEIU5Z",
    "B5YWR9",
    "C4XYDL",
    "FHF04B",
    "HKWU78",
    "GVX0IL",
    "25B3IA",
    "CVVCX8",
    "NVV2U0",
    "V56CSS",
    "OUZ78P",
    "G2OPEG",
    "YFIH4J",
    "11OAUU",
    "W3XAOI",
    "5JGVO5",
    "9O2MGU",
    "074XG6",
    "1WFQLM",
    "CTR33Y",
    "F1MMZP",
    "TA1RFF",
    "F0RGVN",
    "GVFH4F",
    "6QGULC",
    "R3MXF8",
    "57S5SL",
    "8MQJ7D",
    "5MHM7N",
    "OS44DQ",
    "XNXK24",
    "KLME53",
    "3RVS78",
    "XMYVD9",
    "ZFANIN",
    "LB008X",
    "ERCXAV",
    "B8BXFN",
    "VREDKA",
    "SNK0A5",
    "SVORSV",
    "TDF09Z",
    "P71KJK",
    "2NS5BE",
    "KCCW35",
    "04AS8X",
    "0UPTJ0",
    "ZCWRD2",
    "KXG3RK",
    "SDRUL7",
    "RQDI1A",
    "WRM6Q5",
    "48124W",
    "1O78R0",
    "15D2O2",
    "08WYKW",
    "VPG3US",
    "LJ76MP",
    "NKN2SK",
    "U6GSWC",
    "XSMZIT",
    "U8YVN9",
    "WYJI6B",
    "6DYIG0",
    "LLGYWC",
    "WKQVPR",
    "HAJJG9",
    "VSZ0L1",
    "08N4SQ",
    "RGTSX5",
    "TQR0IR",
    "ITKC0P",
    "SJ5IFA",
    "TE56EF",
    "WA87LZ",
    "CBS8A4",
    "L80ET4",
    "AFDCJZ",
    "7U97HN",
    "F2GTG6",
    "TAY1TW",
    "GS93TE",
    "MRS4IN",
    "UV0JGN",
    "0UE3OW",
    "VYFYRL",
    "BB8DFL",
    "LR0DVW",
    "D83AZD",
    "GZWGVN",
    "K467TM",
    "B9SX1D",
    "JEB8CZ",
    "FWF9A5",
    "4VJPOI",
    "R5SS0L",
    "BNKKMO",
 
]

UNLOCK_HINT = "请输入您的专属 VIP 兑换码"
BUY_GUIDE = "如需获取，请在购买平台（闲鱼/小红书）私信联系发货"
# ==========================================

# --- 0. 核心配置：全行业代理映射表 ---
PROXY_MAP = {
    "黄金": "518880", "上海金": "518600", "豆粕": "159985",
    "有色": "512400", "化工": "516020", "石化": "516020",
    "石油": "561360", "油气": "513350", "煤炭": "515220",
    "沪深300": "510300", "上证50": "510050", "中证500": "510500",
    "科创50": "588000", "创业板": "159915", "微盘": "563300",
    "半导体": "512480", "芯片": "159995", "人工智能": "159819",
    "游戏": "159869", "传媒": "512980", "光伏": "515790",
    "新能源": "515030", "白酒": "161725", "医疗": "512170",
    "医药": "512010", "证券": "512000", "银行": "512800",
    "纳斯达克": "513100", "纳指": "513100", "标普500": "513500",
    "恒生科技": "513180", "恒生互联网": "513330", "中概互联": "513050",
    "恒生指数": "159920", "日经": "513520", "港股通互联网": "159792",
}

# --- 1. 基础工具函数 ---
def get_tencent_code(symbol):
    s = str(symbol).strip().upper()
    if s.isalpha(): return f"us{s}"
    if len(s) == 5 and s.isdigit(): return f"hk{s}"
    if len(s) == 6 and s.isdigit():
        if s.startswith(('5','6','9')): return f"sh{s}"
        if s.startswith(('0','1','2','3')): return f"sz{s}"
    return None

def fetch_quotes_universal(code_list):
    if not code_list: return {}, 0.0
    unique_codes = list(set(code_list))
    t_codes = []
    map_ref = {}
    need_fx = False
    
    for c in unique_codes:
        tc = get_tencent_code(c)
        if tc:
            key = f"s_{tc}"
            t_codes.append(key)
            map_ref[key] = c
            if "us" in tc: need_fx = True
    
    if need_fx: t_codes.append("s_usUSDCNH")
    
    res_dict = {}
    fx_change = 0.0
    
    try:
        rand_param = int(time.time() * 1000)
        url = f"http://qt.gtimg.cn/q={','.join(t_codes)}&_={rand_param}"
        r = requests.get(url, timeout=3)
        r.encoding = 'gbk'
        for line in r.text.split(';'):
            if '=' not in line: continue
            k, v = line.split('=', 1)
            data = v.strip('"').split('~')
            if len(data) < 6: continue
            
            if "s_usUSDCNH" in k:
                try: fx_change = float(data[5])
                except: pass
            else:
                key_clean = k.split('v_')[-1]
                raw = map_ref.get(key_clean)
                if raw:
                    try: res_dict[raw] = float(data[5])
                    except: pass
    except: pass
    return res_dict, fx_change

def get_fund_name_only(fund_code):
    try:
        ts = int(time.time() * 1000)
        url = f"http://qt.gtimg.cn/q=jj{fund_code}&t={ts}"
        r = requests.get(url, timeout=2)
        r.encoding = 'gbk'
        if '="' in r.text:
            data = r.text.split('="')[1].split('~')
            if len(data) > 1:
                return data[1]
    except: pass
    return f"基金{fund_code}"

# --- 2. 核心分析逻辑 ---
def analyze_fund_profit_by_amount(fund_code, holding_amount):
    fund_name = get_fund_name_only(fund_code)
    est_change = 0.0
    method = "❌ 未知"
    detail = "无数据"
    
    if "债" in fund_name and "可转债" not in fund_name:
        est_change = 0.0
        method = "🛡️ 债券基金"
        detail = "忽略波动"
    
    elif not method.startswith("🛡️"):
        found_proxy = False
        for kw, proxy in PROXY_MAP.items():
            if kw in fund_name:
                q, _ = fetch_quotes_universal([proxy])
                est_change = q.get(proxy, 0.0)
                method = "⚡ 行业锚定"
                detail = f"追踪 {kw}({proxy})"
                found_proxy = True
                break
        
        if not found_proxy:
            holdings_df = pd.DataFrame()
            try:
                cur_year = datetime.datetime.now().year
                for y in [cur_year, cur_year-1]:
                    df = ak.fund_portfolio_hold_em(symbol=fund_code, date=str(y))
                    if not df.empty:
                        holdings_df = df[df['季度'] == df['季度'].max()].copy()
                        break
            except: pass
            
            if not holdings_df.empty:
                stocks = holdings_df['股票代码'].astype(str).tolist()
                weights = pd.to_numeric(holdings_df['占净值比例'], errors='coerce') / 100
                quotes, fx = fetch_quotes_universal(stocks)
                
                total_w = 0; total_c = 0; us_count = 0
                for i, s in enumerate(stocks):
                    if s in quotes:
                        w = weights.iloc[i]
                        c = quotes[s]
                        if s.isalpha(): c += fx; us_count += 1
                        total_c += w * c; total_w += w
                        
                if total_w > 0.05:
                    est_change = total_c / total_w
                    if us_count > 3: method = "🇺🇸 美股穿透"; detail = f"昨收+汇率({fx:+.2f}%)"
                    else: method = "📈 持仓穿透"; detail = f"基于 {len(stocks)} 只持仓"
    
    # [V16.0 修复] 确保 holding_amount 是有效数字
    try:
        safe_amount = float(holding_amount)
        if math.isnan(safe_amount): safe_amount = 0.0
    except:
        safe_amount = 0.0
        
    profit = safe_amount * (est_change / 100)
    
    return {"code": fund_code, "name": fund_name, "change_pct": est_change, "profit": profit, "amount": safe_amount, "method": method, "detail": detail}

# --- 3. Streamlit 界面 ---
st.set_page_config(page_title="基金估值Pro", page_icon="💰", layout="wide")

if "fund_data" not in st.session_state:
    st.session_state.fund_data = pd.DataFrame([
        {"代码": "013403", "持仓金额": 10000.0, "备注": "演示持仓"},
        {"代码": "005827", "持仓金额": 0.0, "备注": "演示观察"},
    ])
if "vip_unlocked" not in st.session_state:
    st.session_state.vip_unlocked = False

st.markdown("### 💰 基金实盘估值")
st.caption("全能版：支持股票/ETF/QDII | 🚀 输入本金，一键计算今日盈亏")

with st.expander("📝 编辑持仓 (支持粘贴Excel)", expanded=True):
    col1, col2 = st.columns([4, 1])
    with col2:
        if st.button("🗑️ 清空表格"):
            st.session_state.fund_data = pd.DataFrame([{"代码": "", "持仓金额": 0.0, "备注": ""}])
            st.rerun()
            
    edited_df = st.data_editor(
        st.session_state.fund_data,
        num_rows="dynamic",
        column_config={
            "代码": st.column_config.TextColumn(help="6位代码"),
            "持仓金额": st.column_config.NumberColumn(min_value=0, format="%.2f", help="输入本金"),
            "备注": st.column_config.TextColumn(),
        },
        use_container_width=True
    )

start_calc = st.button("🚀 开始估值", type="primary", use_container_width=True)

if start_calc or st.session_state.get('show_results', False):
    st.session_state.show_results = True
    
    # ================= [V16.0 核心修复] 数据清洗逻辑 =================
    # 1. 过滤掉代码为空的行 (防止空行干扰)
    mask_has_code = edited_df["代码"].astype(str).str.strip() != ""
    # 2. 拷贝一份数据，避免报警
    valid_rows = edited_df[mask_has_code].copy()
    
    # 3. 强制清洗金额列：把 NaN, None, 空字符串 全部变成 0.0
    valid_rows["持仓金额"] = pd.to_numeric(valid_rows["持仓金额"], errors='coerce').fillna(0.0)
    # =================================================================
    
    if valid_rows.empty:
        st.warning("请至少输入一行基金代码")
        st.stop()

    # --- A. 验证逻辑：是否为有效VIP ---
    if not st.session_state.vip_unlocked:
        st.divider()
        with st.container():
            st.warning("🔒 正在计算收益... (高级功能已锁定)")
            
            c1, c2 = st.columns([3, 1])
            with c1:
                pwd_input = st.text_input(UNLOCK_HINT, key="pwd_try", placeholder="请输入闲鱼/小红书获取的卡密").strip()
            with c2:
                st.write("") 
                st.write("") 
                if st.button("🔓 立即验证"):
                    if pwd_input in VALID_VIP_CODES:
                        st.session_state.vip_unlocked = True
                        st.success("✅ 验证成功！欢迎尊贵的 Pro 会员")
                        time.sleep(1)
                        st.rerun()
                    else:
                        st.error("❌ 无效的兑换码")
            
            st.caption(f"💡 {BUY_GUIDE}")
        
        st.markdown("---")
        st.subheader("📊 基础涨跌幅 (预览模式)")
        
        for index, row in valid_rows.iterrows():
            code = str(row["代码"]).strip()
            # 即使免费版，传入清洗过的 0.0 也比传入 NaN 安全
            res = analyze_fund_profit_by_amount(code, 0.0)
            
            val = res['change_pct']
            color = "gray"; icon = "⚪"
            if val > 0: color = "red"; icon = "🔴"
            elif val < 0: color = "green"; icon = "🟢"
            
            with st.container():
                c1, c2 = st.columns([2, 1])
                with c1:
                    st.markdown(f"**{res['name']}**")
                    st.caption(f"{res['code']} | {res['method']}")
                with c2:
                    st.markdown(f"**{icon} {val:+.2f}%**")
                    st.caption("🔒 收益隐藏")
                st.divider()

    # --- B. 验证通过：显示完整版 ---
    else:
        results = []
        progress_bar = st.progress(0)
        total_profit = 0.0; total_principal = 0.0
        
        for index, row in valid_rows.iterrows():
            code = str(row["代码"]).strip()
            amount = float(row["持仓金额"]) # 这里已经是清洗过的安全数字了
            
            res = analyze_fund_profit_by_amount(code, amount)
            res['user_remark'] = row.get("备注", "")
            results.append(res)
            
            # 双重保险，防止 res['profit'] 是 NaN
            safe_profit = 0.0
            if not math.isnan(res['profit']):
                safe_profit = res['profit']
                
            total_profit += safe_profit
            total_principal += amount
            progress_bar.progress((index + 1) / len(valid_rows))
            
        progress_bar.empty()
        
        st.markdown("---")
        
        # 处理总盈亏也可能出现 NaN 的极端情况
        if math.isnan(total_profit): total_profit = 0.0
        
        bg_color = "#ffebee" if total_profit > 0 else "#e8f5e9"
        border_color = "red" if total_profit > 0 else "green"
        sign = "+" if total_profit > 0 else ""
        
        st.markdown(
            f"""
            <div style="background-color:{bg_color}; padding:15px; border-radius:10px; border-left: 5px solid {border_color}; text-align:center;">
                <h4 style="margin:0; color:#666;">今日预估总盈亏 (Pro)</h4>
                <h2 style="margin:5px 0; color:{border_color};">{sign}{total_profit:,.2f} 元</h2>
                <small>持仓本金: {total_principal:,.2f} 元</small>
            </div>
            """, unsafe_allow_html=True)
        
        st.markdown("### 📋 详细数据")
        for res in results:
            val = res['change_pct']; profit = res['profit']; amount = res['amount']
            color = "gray"; icon = "⚪"
            if val > 0: color = "red"; icon = "🔴"
            elif val < 0: color = "green"; icon = "🟢"
            
            # 显示修复：如果算出来是 NaN，强制显示为 0.00
            display_profit = profit if not math.isnan(profit) else 0.0
            
            with st.container():
                c1, c2 = st.columns([1.5, 1])
                with c1:
                    st.markdown(f"**{res['name']}**")
                    st.caption(f"{res['code']} | {res['method']}")
                    if res['user_remark']: st.caption(f"备注: {res['user_remark']}")
                with c2:
                    st.markdown(f"**{icon} {val:+.2f}%**")
                    if amount > 0:
                        p_sign = "+" if display_profit > 0 else ""
                        st.markdown(f":{color}[**{p_sign}{display_profit:.2f} 元**]")
                    else: st.caption("👀 观察中")
                st.text(res['detail'])
                st.divider()