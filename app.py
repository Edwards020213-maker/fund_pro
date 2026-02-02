import streamlit as st
import pandas as pd
import requests
import akshare as ak
import datetime
import time
import math
import json
from streamlit_local_storage import LocalStorage

# ==========================================
# 🔐 商家后台配置区
# ==========================================
VALID_VIP_CODES = [
    "LIHWQY","GO75ON","DXPIOA","SAMRUO","SGUGKB","K88CTV","I354RX", "K9IJMS","4ZF59V","27DP9A","U0CALN","1XVK1D","G6AW46","Q9TXDU","HH4FDG",
    "LGYUB6", "2S55MK","82GJKA","7RI4IN","YE9SEZ","VLBGKG","4VKIWT","Q7SL9J","6QEBLO","P1OHJR","59L0A3","L1OTDE","8LH0D3","BMTQSN","F7NKNF",
    "0MJ0RD","TFLKK3","AKBODE","SC87DP","G3WJAG","N3XX4X","AN09RU", "I1A2Z3", "RH1C5B", "Y6RMG9", "ZH3G5O", "GTCAPG", "PZE1LX", "WT7Z8O", "EO6LXU", 
    "BYK569", "84IDLA","ETCTZG","P6YI7G","QZGDLB"
]
UNLOCK_HINT = "请输入您的专属 VIP 兑换码"
BUY_GUIDE = "如需获取，请在购买平台（闲鱼/小红书）私信联系发货"
CONTACT_TIP = "💡 遇到问题？欢迎在 闲鱼/小红书 私信联系"
# ==========================================

# --- 0. 核心配置 ---
# --- 0. 核心配置：全行业代理映射表 (超级扩容版 V26.3) ---
PROXY_MAP = {
    # === A股宽基 ===
    "沪深300": "510300", "300": "510300",
    "上证50": "510050",  "中证500": "510500", "500": "510500",
    "中证1000": "512100", "1000": "512100",
    "中证2000": "563300", "2000": "563300", "微盘": "563300",
    "科创50": "588000",  "科创100": "588190", "科创": "588000",
    "创业板": "159915",  "创50": "159949",
    "北证50": "589905",

    # === 科技与成长 ===
    "半导体": "512480", "芯片": "159995", "集成电路": "512480",
    "人工智能": "159819", "AI": "159819", "算力": "512480",
    "计算机": "512720", "软件": "515290", "信创": "562030",
    "游戏": "159869", "动漫": "159869", "传媒": "512980",
    "通信": "515050", "5G": "515050",
    "消费电子": "159732", "苹果": "159732",
    "机器人": "562500", "机床": "159663",

    # === 新能源与车 ===
    "新能源": "515030", "光伏": "515790", "绿电": "562550",
    "电池": "159755",   "锂电": "561160",
    "汽车": "515700",   "智能汽车": "515250",

    # === 医药与医疗 ===
    "医药": "512010", "医疗": "512170", "生物": "516500",
    "创新药": "159992", "中药": "560080", "疫苗": "159643",

    # === 大消费 ===
    "白酒": "161725", "酒": "512690", "食品": "515710",
    "家电": "159996", "电器": "159996",
    "养殖": "159865", "猪": "159865", "农牧": "159865",
    "农业": "516110", "种业": "516110",
    "旅游": "159766",

    # === 周期与资源 ===
    "煤炭": "515220", "能源": "515220",
    "有色": "512400", "稀土": "516150",
    "钢铁": "515210", 
    "化工": "516020", "石化": "516020",
    "石油": "561360", "油气": "513350",
    "黄金": "518880", "上海金": "518600",
    "豆粕": "159985", # 商品期货ETF

    # === 金融与地产 ===
    "证券": "512000", "券商": "512000",
    "银行": "512800",
    "保险": "515070", # 通常用金融地产或证券暂代，或300非银
    "地产": "512200", "房地产": "512200",
    "基建": "516970",

    # === 策略与红利 ===
    "红利": "515080", "高股息": "515080",
    "央企": "560068", "国企": "517090",

    # === 军工 ===
    "军工": "512660", "国防": "512660",

    # === 跨境/QDII (重要) ===
    "纳斯达克": "513100", "纳指": "513100", "QQQ": "513100",
    "标普500": "513500", "标普": "513500", "SPX": "513500",
    "恒生科技": "513180", "恒科": "513180", "港股通互联网": "159792",
    "恒生互联网": "513330", "中概互联": "513050", "中概": "513050",
    "恒生指数": "159920", "恒指": "159920",
    "日经": "513520", "日本": "513520",
    "越南": "513280", 
    "印度": "164824", # 印度LOF
    "德国": "513030", "法兰克福": "513030",
    "法国": "513080",
    "美股生物": "513290", "美股医药": "513290",
    "东南亚": "513910", "泛东南亚": "513910",
    "沙特": "159329", # 沙特ETF
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
    
    try:
        safe_amount = float(holding_amount)
        if math.isnan(safe_amount): safe_amount = 0.0
    except:
        safe_amount = 0.0
        
    profit = safe_amount * (est_change / 100)
    
    return {"code": fund_code, "name": fund_name, "change_pct": est_change, "profit": profit, "amount": safe_amount, "method": method, "detail": detail}

# --- 3. Streamlit 界面 ---
st.set_page_config(page_title="基金估值Pro", page_icon="💰", layout="wide")

ls = LocalStorage()

if "fund_data" not in st.session_state:
    st.session_state.fund_data = pd.DataFrame([
        {"代码": "013403", "持仓金额": 10000.50, "备注": "演示持仓"},
        {"代码": "005827", "持仓金额": 0.00, "备注": "演示观察"},
    ])
if "vip_unlocked" not in st.session_state:
    st.session_state.vip_unlocked = False

st.markdown("### 💰 基金实盘估值 V26.2 (顺序修复版)")
st.caption("🚀 极速计算 | 💾 支持保存持仓到浏览器 | 无广告")

with st.sidebar:
    st.info(CONTACT_TIP, icon="📩")
    st.markdown("---")
    if st.button("🧹 强制清除缓存", help="如果读取报错，请点此重置"):
        ls.deleteAll()
        st.toast("缓存已清空", icon="🧹")
        time.sleep(1)
        st.rerun()

# === 编辑与存储控制区 ===
with st.expander("📝 编辑持仓 (支持粘贴Excel)", expanded=True):
    
    # 【关键修复】步骤1：先渲染表格，获取最新的 edited_df
    # 只有先运行这一步，edited_df 里才会有你刚刚输入的数据
    edited_df = st.data_editor(
        st.session_state.fund_data,
        num_rows="dynamic",
        column_config={
            "代码": st.column_config.TextColumn(help="6位代码"),
            "持仓金额": st.column_config.NumberColumn(
                min_value=0.0, format="%.2f", step=0.01, help="输入本金"
            ),
            "备注": st.column_config.TextColumn(),
        },
        use_container_width=True
    )
    
    st.divider() # 加个分割线，视觉上分层

    col_a, col_b, col_c = st.columns([2, 1, 1])
    
    # 【关键修复】步骤2：再渲染保存按钮，并使用上面的 edited_df 进行保存
    with col_b:
        if st.button("💾 保存配置", use_container_width=True):
            # 这里用 edited_df (用户改过的)，而不是 session_state (旧的)
            current_json = edited_df.to_json(orient="records")
            ls.setItem("my_fund_config_v26", current_json)
            st.toast("✅ 已保存！下次请点击右侧【读取配置】恢复", icon="💾")
    
    with col_c:
        if st.button("📥 读取配置", use_container_width=True):
            saved_data = ls.getItem("my_fund_config_v26")
            if saved_data is not None:
                try:
                    if isinstance(saved_data, str):
                        data_obj = json.loads(saved_data)
                    else:
                        data_obj = saved_data
                    
                    st.session_state.fund_data = pd.DataFrame(data_obj)
                    st.toast("✅ 读取成功", icon="📥")
                    time.sleep(0.5)
                    st.rerun()
                except Exception as e:
                    st.error(f"❌ 读取失败: {e}")
                    st.caption("请尝试点击左侧边栏的【强制清除缓存】")
            else:
                st.warning("⚠️ 本地暂无存档")

# =========================================================

start_calc = st.button("🚀 开始估值", type="primary", use_container_width=True)

if start_calc or st.session_state.get('show_results', False):
    st.session_state.show_results = True
    
    mask_has_code = edited_df["代码"].astype(str).str.strip() != ""
    valid_rows = edited_df[mask_has_code].copy()
    valid_rows["持仓金额"] = pd.to_numeric(valid_rows["持仓金额"], errors='coerce').fillna(0.0)
    
    if valid_rows.empty:
        st.warning("请至少输入一行基金代码")
        st.stop()

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
                        st.success("✅ 验证成功！")
                        time.sleep(1)
                        st.rerun()
                    else:
                        st.error("❌ 无效的兑换码")
            st.caption(f"💡 {BUY_GUIDE}")
        
        st.markdown("---")
        st.subheader("📊 基础涨跌幅 (免费预览)")
        for index, row in valid_rows.iterrows():
            code = str(row["代码"]).strip()
            res = analyze_fund_profit_by_amount(code, 0.0)
            val = res['change_pct']
            icon = "🔴" if val > 0 else "🟢"
            with st.container():
                c1, c2 = st.columns([2, 1])
                with c1:
                    st.markdown(f"**{res['name']}**")
                    st.caption(f"{res['code']} | {res['method']}")
                with c2:
                    st.markdown(f"**{icon} {val:+.2f}%**")
                    st.caption("🔒 收益隐藏")
                st.divider()
    else:
        results = []
        progress_bar = st.progress(0)
        total_profit = 0.0
        
        for index, row in valid_rows.iterrows():
            code = str(row["代码"]).strip()
            amount = float(row["持仓金额"])
            res = analyze_fund_profit_by_amount(code, amount)
            res['user_remark'] = row.get("备注", "")
            results.append(res)
            
            if not math.isnan(res['profit']):
                total_profit += res['profit']
            progress_bar.progress((index + 1) / len(valid_rows))
        
        progress_bar.empty()
        
        st.markdown("---")
        if math.isnan(total_profit): total_profit = 0.0
        bg_color = "#ffebee" if total_profit > 0 else "#e8f5e9"
        border_color = "red" if total_profit > 0 else "green"
        sign = "+" if total_profit > 0 else ""
        
        st.markdown(
            f"""
            <div style="background-color:{bg_color}; padding:15px; border-radius:10px; border-left: 5px solid {border_color}; text-align:center;">
                <h4 style="margin:0; color:#666;">今日预估总盈亏 (Pro)</h4>
                <h2 style="margin:5px 0; color:{border_color};">{sign}{total_profit:,.2f} 元</h2>
            </div>
            """, unsafe_allow_html=True)
        
        st.markdown("### 📋 详细数据")
        for res in results:
            val = res['change_pct']
            profit = res['profit']
            amount = res['amount']
            color = "gray"; icon = "⚪"
            if val > 0: color = "red"; icon = "🔴"
            elif val < 0: color = "green"; icon = "🟢"
            
            with st.container():
                c1, c2 = st.columns([1.5, 1])
                with c1:
                    st.markdown(f"**{res['name']}**")
                    st.caption(f"{res['code']} | {res['method']}")
                    if res['user_remark']: st.caption(f"备注: {res['user_remark']}")
                with c2:
                    st.markdown(f"**{icon} {val:+.2f}%**")
                    if amount > 0:
                        p_sign = "+" if profit > 0 else ""
                        st.markdown(f":{color}[**{p_sign}{profit:.2f} 元**]")
                    else: st.caption("👀 观察中")
                st.text(res['detail'])
                st.divider()
