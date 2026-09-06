import streamlit as st

# ---------- 1. Initialization & Config ----------
# Initial_sidebar_state="collapsed" ensures it starts hidden and only expands when pressed
st.set_page_config(page_title="Risk Stratification of Cardiopulmonary Fitness Training", layout="wide", initial_sidebar_state="collapsed")

def inject_custom_css():
    st.markdown(
        """
        <style>
        /* =========================================================
           🖥️ REDUCE TOP MARGIN
           ========================================================= */
        .block-container {
            padding-top: 1.5rem !important;
            padding-bottom: 1.5rem !important;
        }
        
        /* 隱藏頂部預設的裝飾性 header 空間 */
        header[data-testid="stHeader"] {
            height: 0px !important;
        }

        /* =========================================================
           🖥️ DESKTOP & iPAD VIEW (長者友善選項 + 精緻標題排版)
           ========================================================= */
        html, body, [data-testid="stMarkdownContainer"] {
            font-size: 24px !important; 
            font-weight: 400 !important;
            line-height: 1.45 !important; 
        }

        /* --- SAFE SPACING --- */
        div[data-testid="stVerticalBlock"] { gap: 0.6rem !important; }
        .element-container { margin-bottom: 0px !important; }
        hr { margin-top: 0.6rem !important; margin-bottom: 0.6rem !important; padding: 0px !important; }

        /* Headers - BOLD */
        h1 { font-size: 30px !important; font-weight: bold !important; line-height: 1.45 !important; margin-bottom: 12px !important;}
        h2 { font-size: 28px !important; font-weight: bold !important; border-bottom: 2px solid var(--text-color); padding-bottom: 8px !important; line-height: 1.45 !important; margin-top: 12px !important; margin-bottom: 15px !important;}
        h3 { font-size: 26px !important; font-weight: bold !important; line-height: 1.45 !important; margin-bottom: 12px !important;}
        h4 { font-size: 24px !important; font-weight: bold !important; line-height: 1.45 !important; margin-bottom: 12px !important; opacity: 0.8;}

        /* Radio Buttons & Checkbox Labels */
        div[data-testid="stRadio"] label p, div[data-testid="stCheckbox"] label p {
            font-size: 26px !important; 
            font-weight: 400 !important; 
            line-height: 1.45 !important; 
        }
        
        /* 確保選項絕對不會換行 (Force single line for radio buttons) */
        .stRadio > div { 
            gap: 0rem !important; 
            flex-wrap: nowrap !important;
        } 
        
        .stCheckbox > div { margin-bottom: 0rem !important; }

        /* Standard Text */
        .stMarkdown p {
            font-size: 24px !important; 
            line-height: 1.45 !important; 
            margin-bottom: 12px !important; 
        }

        /* Input Box Labels */
        label[data-testid="stWidgetLabel"] p {
            font-size: 26px !important; 
            font-weight: bold !important; 
            margin-bottom: 6px !important;
        }

        .question-text { margin-top: 0px !important; font-size: 26px !important; line-height: 1.45 !important; }

        /* ----- CUSTOM RED BUTTON STYLING ----- */
        button[kind="primary"], [data-testid="baseButton-primary"], button[kind="secondary"], [data-testid="baseButton-secondary"] {
            font-size: 24px !important; 
            padding: 10px 20px !important; 
            font-weight: bold !important; 
            line-height: 1.45 !important;
        }
        button[kind="primary"], [data-testid="baseButton-primary"] { background-color: #ef5350 !important; color: white !important; border-color: #ef5350 !important; }
        button[kind="primary"]:hover, [data-testid="baseButton-primary"]:hover { background-color: #e53935 !important; border-color: #e53935 !important; color: white !important;}

        /* =========================================================
           🖥️ SIDEBAR NAVIGATION PANEL (Smaller Font, Left Aligned, Multiline)
           ========================================================= */
        [data-testid="stSidebar"] p, [data-testid="stSidebar"] div, [data-testid="stSidebar"] span {
            font-size: 18px !important; 
        }
        [data-testid="stSidebar"] h2 {
            font-size: 22px !important;
            margin-bottom: 10px !important;
        }
        [data-testid="stSidebar"] button[kind="primary"], 
        [data-testid="stSidebar"] [data-testid="baseButton-primary"], 
        [data-testid="stSidebar"] button[kind="secondary"], 
        [data-testid="stSidebar"] [data-testid="baseButton-secondary"] {
            font-size: 18px !important; 
            padding: 12px 12px !important; 
            font-weight: bold !important; 
            height: auto !important; /* Allow height to expand for multiline */
            text-align: left !important;
        }
        
        /* 讓按鈕內的內容靠左對齊 */
        [data-testid="stSidebar"] button div {
            justify-content: flex-start !important; 
            width: 100%;
        }
        
        /* 確保可以換行並靠左 */
        [data-testid="stSidebar"] button p {
            white-space: pre-wrap !important; 
            text-align: left !important;
            line-height: 1.3 !important;
        }

        /* --- 頂部狀態提示框 (Desktop/iPad 預設大小) --- */
        .risk-strat-box {
            border-radius: 8px; 
            padding: 12px; 
            text-align: center; 
            margin-bottom: 20px;
        }
        .risk-strat-text {
            font-size: 28px; 
            font-weight: bold;
        }

        /* =========================================================
           📱 MOBILE RESPONSIVE PATCH (iPhone 專屬長者大字版)
           ========================================================= */
        @media (max-width: 767px) {
            html, body, [data-testid="stMarkdownContainer"] { font-size: 20px !important; }
            h1 { font-size: 24px !important; }
            h2 { font-size: 22px !important; }
            h3 { font-size: 20px !important; }
            h4 { font-size: 18px !important; }
            
            .stMarkdown p { font-size: 20px !important; margin-bottom: 8px !important;}
            .question-text { font-size: 22px !important; margin-bottom: 8px !important; }
            
            [data-testid="column"] { margin-bottom: 12px !important; }
            .element-container { margin-bottom: 12px !important; }
            
            div[data-testid="stRadio"] label p, div[data-testid="stCheckbox"] label p {
                font-size: 22px !important; 
            }
            .stRadio > div { 
                gap: 1.5rem !important; 
                padding-bottom: 15px !important;
            } 
            
            button[kind="primary"], [data-testid="baseButton-primary"], button[kind="secondary"], [data-testid="baseButton-secondary"] {
                font-size: 22px !important;
                padding: 14px 12px !important; 
                white-space: normal !important; 
                height: auto !important;
            }

            /* 手機版專屬：頂部狀態提示框自動縮小 */
            .risk-strat-box {
                padding: 8px !important;
            }
            .risk-strat-text {
                font-size: 20px !important;
            }
        }
        </style>
        """,
        unsafe_allow_html=True
    )

def init_session_states():
    if "data" not in st.session_state:
        st.session_state.data = {}
        for i in range(1, 10): st.session_state.data[f"s_{i}"] = None
        for k in ["d_cardio", "d_metabolic", "d_renal", "is_active"]: st.session_state.data[k] = None
        for i in range(1, 8): st.session_state.data[f"parq_{i}"] = None
        st.session_state.data["parq_4_text"] = ""
        st.session_state.data["parq_5_text"] = ""

    if "force_show_all" not in st.session_state:
        st.session_state["force_show_all"] = False
    if "current_tab" not in st.session_state:
        st.session_state["current_tab"] = "1. 運動風險評估\n(表格 B)"
    if "show_b_errors" not in st.session_state:
        st.session_state["show_b_errors"] = False
    if "show_a_errors" not in st.session_state:
        st.session_state["show_a_errors"] = False

def update_val(key):
    st.session_state.data[key] = st.session_state[key]

init_session_states()


# ---------- 2. Logic Functions ----------
b_key_names = {
    "s_1": "徵狀 1 (胸口/頸/下顎痛楚)", "s_2": "徵狀 2 (靜止氣喘)", "s_3": "徵狀 3 (暈眩)",
    "s_4": "徵狀 4 (平臥氣喘)", "s_5": "徵狀 5 (足踝腫)", "s_6": "徵狀 6 (心悸)",
    "s_7": "徵狀 7 (肌肉疼痛/抽筋)", "s_8": "徵狀 8 (心雜音)", "s_9": "徵狀 9 (不尋常疲倦)",
    "d_cardio": "已知心血管疾病", "d_metabolic": "已知代謝疾病", "d_renal": "已知腎臟疾病",
    "is_active": "當前運動習慣"
}

a_key_names = {
    f"parq_{i}": f"問題 {i}" for i in range(1, 8)
}

def get_missing_b():
    missing = []
    for k, name in b_key_names.items():
        if st.session_state.data.get(k) is None:
            missing.append(name)
    return missing

def get_missing_a():
    missing = []
    for k, name in a_key_names.items():
        if st.session_state.data.get(k) is None:
            missing.append(name)
    return missing

def evaluate_b_only():
    missing_b = get_missing_b()
    if missing_b:
        return "Pending"

    symptoms = sum(1 for i in range(1, 10) if st.session_state.data.get(f"s_{i}") == "有")
    has_disease = any([
        st.session_state.data.get("d_cardio") == "有", 
        st.session_state.data.get("d_metabolic") == "有", 
        st.session_state.data.get("d_renal") == "有"
    ])
    is_active = st.session_state.data.get("is_active") == "是"
    
    if (has_disease and not is_active) or (symptoms >= 1):
        return "Class III"
    if has_disease and is_active and symptoms == 0:
        return "Class II"
        
    return "Pending Form A"

def calculate_current_class():
    b_class = evaluate_b_only()
    
    if b_class in ["Class III", "Class II", "Pending"]:
        return b_class
        
    missing_a = get_missing_a()
    if missing_a:
        return "Pending"

    parq_score = sum(1 for i in range(1, 8) if st.session_state.data.get(f"parq_{i}") == "有")
    
    symptoms = sum(1 for i in range(1, 10) if st.session_state.data.get(f"s_{i}") == "有")
    has_disease = any([
        st.session_state.data.get("d_cardio") == "有", 
        st.session_state.data.get("d_metabolic") == "有", 
        st.session_state.data.get("d_renal") == "有"
    ])

    if not has_disease and parq_score == 0 and symptoms == 0:
        return "Class I"
    elif parq_score > 0:
        return "Class II"
        
    return "Class I"

def calculate_thr(age, rhr, risk_level):
    mhr = 220 - age
    if rhr >= mhr: return None, None, "Abnormal Resting Heart Rate (>= Maximum HR)"
    hrr = mhr - rhr

    # Using non-breaking spaces for a cleaner look in HTML
    details_str = f"Maximum HR: {mhr} bpm &nbsp;|&nbsp; Standing HR at rest: {rhr} bpm &nbsp;|&nbsp; HR Reserve: {hrr} bpm"

    if risk_level == "Class III":
        limit = int((hrr * 0.40) + rhr)
        thr_main = f"Training HR: &lt; {limit} bpm"
        return thr_main, details_str, None
    elif risk_level == "Class II":
        limit = int((hrr * 0.60) + rhr)
        thr_main = f"Training HR: &lt; {limit} bpm"
        return thr_main, details_str, None
    else:
        upper = int((hrr * 0.84) + rhr)
        thr_main = f"Training HR: &le; {upper} bpm"
        return thr_main, details_str, None


# ---------- 3. Callbacks & Helpers ----------
def go_to_tab(tab_name):
    st.session_state["current_tab"] = tab_name
    st.session_state["show_b_errors"] = False
    st.session_state["show_a_errors"] = False

def enable_all_tabs_and_go():
    st.session_state["force_show_all"] = True
    go_to_tab("2. 體能活動適應能力問卷\n(表格 A)")

def try_complete_b(target_tab):
    missing = get_missing_b()
    if missing:
        st.session_state["show_b_errors"] = True
    else:
        st.session_state["show_b_errors"] = False
        go_to_tab(target_tab)

def try_complete_a(target_tab):
    missing = get_missing_a()
    if missing:
        st.session_state["show_a_errors"] = True
    else:
        st.session_state["show_a_errors"] = False
        go_to_tab(target_tab)

def render_inline_question(label, key, options=("否", "有"), check_error=False):
    is_missing = check_error and st.session_state.data.get(key) is None
    
    col1, col2 = st.columns([8.2, 1.8]) 
    with col1:
        if is_missing:
            st.markdown(f'<div class="question-text" style="color: #c62828 !important; font-weight: bold; background-color: #ffebee !important; border-left: 5px solid #c62828; padding-left: 10px;">{label}</div>', unsafe_allow_html=True)
        else:
            st.markdown(f'<div class="question-text">{label}</div>', unsafe_allow_html=True)
    with col2:
        saved_val = st.session_state.data.get(key)
        idx = options.index(saved_val) if saved_val in options else None
        st.radio("", options, key=key, index=idx, horizontal=True, label_visibility="collapsed", on_change=update_val, args=(key,))


# ---------- 4. Tab Functions ----------
def tab_b_acsm(b_class, show_all_tabs):
    check_err = st.session_state.get("show_b_errors", False)
    
    st.header("表格 B：心血管、呼吸系統及代謝性疾病之主要徵狀")
    st.write("請在合適選擇上選擇「有」或「否」：")
    
    s_items = [
        "1. 因心臟缺血而引致的胸口、頸、下顎、上臂 或其他部位痛楚或不適",
        "2. 靜止或輕鬆活動時感到氣喘",
        "3. 暈眩或失去知覺",
        "4. 平臥時或晚間不時氣喘",
        "5. 足踝腫 (小腿、腳眼、腳面腫)",
        "6. 心悸或心跳過快",
        "7. 間歇肌肉疼痛、抽筋",
        "8. 心雜音",
        "9. 一般活動感到不尋常的疲倦或氣喘"
    ]
    for i, q in enumerate(s_items, 1):
        render_inline_question(q, f"s_{i}", check_error=check_err)
        # Targeted spacer ONLY after Question 1 for wrapped text spacing
        if i == 1:
            st.markdown("<div style='height: 15px;'></div>", unsafe_allow_html=True)
        
    st.info("*注意：如有以上徵狀，可能不適合進行強度中度或以上的心肺體能訓練。詳情請向醫生或物理治療師查詢")
    
    st.markdown("---")
    st.subheader("已知醫療狀況 (Known Diseases)")
    render_inline_question("已知心血管疾病 (例如：冠心病、心臟病、中風、心臟衰竭、心律不正)", "d_cardio", check_error=check_err)
    
    # Targeted spacer after the first known disease question for wrapped text spacing
    st.markdown("<div style='height: 15px;'></div>", unsafe_allow_html=True)
    
    render_inline_question("已知代謝疾病 (例如：糖尿病、甲狀腺疾病)", "d_metabolic", check_error=check_err)
    render_inline_question("已知腎臟疾病", "d_renal", check_error=check_err)

    st.markdown("---")
    st.subheader("當前運動習慣")
    activity_question = "您目前是否定期進行體能活動？<br><span style='font-size: 20px; opacity: 0.8;'>(過去 3 個月內，每週至少 3 天，每次 30 分鐘中等強度活動)</span>"
    
    render_inline_question(activity_question, "is_active", options=("否", "是"), check_error=check_err)

    st.markdown("---")
    
    if check_err:
        missing = get_missing_b()
        if missing:
            st.error(f"⚠️ 還有 **{len(missing)}** 個問題尚未填寫，請檢查上方標示為紅色的項目。")

    if b_class == "Pending":
        st.button("➡️ 儲存並前往下一步", type="primary", use_container_width=True, on_click=try_complete_b, args=("3. Target HR &\nClinical Guidelines",))
    elif b_class in ["Class II", "Class III"]:
        if not show_all_tabs:
            st.warning(f"🚨 根據表格 B，運動風險類別為 **{b_class}**。系統已自動隱藏表格 A。")
            c1, c2 = st.columns(2)
            with c1:
                st.button("✅ 完成運動風險判別（請交給職員）", type="primary", use_container_width=True, on_click=try_complete_b, args=("3. Target HR &\nClinical Guidelines",))
            with c2:
                st.button("📝 顯示隱藏的表單 (前往表格 A)", use_container_width=True, on_click=enable_all_tabs_and_go)
        else:
            st.warning(f"🚨 根據表格 B，運動風險類別為 **{b_class}**。您選擇繼續填寫表格 A。")
            st.button("➡️ 儲存並前往「2. 體能活動適應能力問卷」", type="primary", use_container_width=True, on_click=try_complete_b, args=("2. 體能活動適應能力問卷\n(表格 A)",))
    else:
        st.button("➡️ 儲存並前往「2. 體能活動適應能力問卷」", type="primary", use_container_width=True, on_click=try_complete_b, args=("2. 體能活動適應能力問卷\n(表格 A)",))


def tab_a_parq():
    check_err = st.session_state.get("show_a_errors", False)
    
    st.header("表格 A：體能活動適應能力問卷")
    st.write("請在合適選擇上選擇「有」或「否」：")
    
    render_inline_question("1. 過往醫生有否說你有心臟病或高血壓?", "parq_1", check_error=check_err)
    render_inline_question("2. 當你靜止或做運動時有否感覺胸口痛？", "parq_2", check_error=check_err)
    render_inline_question("3. 在過去十二個月內，你有否因頭暈而跌倒或失去知覺？", "parq_3", check_error=check_err)
    
    render_inline_question("4. 您是否曾被診斷出患有慢性疾病？", "parq_4", check_error=check_err)
    if st.session_state.data.get("parq_4") == "有":
        st.text_input("如有，請列出：", value=st.session_state.data.get("parq_4_text", ""), key="parq_4_text", on_change=update_val, args=("parq_4_text",))
        
    render_inline_question("5. 你是否正在服用治療慢性疾病的處方藥？", "parq_5", check_error=check_err)
    if st.session_state.data.get("parq_5") == "有":
        st.text_input("如有，請列出：", value=st.session_state.data.get("parq_5_text", ""), key="parq_5_text", on_change=update_val, args=("parq_5_text",))
        
    render_inline_question("6. 做運動有否可能加重你骨骼，關節或軟組織的痛楚？", "parq_6", check_error=check_err)
    render_inline_question("7. 過往醫生有否說你只應進行醫生建議或監察的運動？", "parq_7", check_error=check_err)

    st.markdown("---")
    
    if check_err:
        missing = get_missing_a()
        if missing:
            st.error(f"⚠️ 還有 **{len(missing)}** 個問題尚未填寫，請檢查上方標示為紅色的項目。")

    st.button("✅ 完成運動風險判別（請交給職員）", type="primary", use_container_width=True, on_click=try_complete_a, args=("3. Target HR &\nClinical Guidelines",))


def tab_d_thr(current_class):
    st.header("Target Heart Rate Calculator")
    
    st.subheader("⚙️ Select Risk Class")
    
    if current_class == "Pending":
        st.markdown("💡 The system evaluation is currently **Incomplete**. Please manually select the Risk Class below:")
    else:
        st.markdown(f"💡 The system evaluates the patient as **{current_class}**. You can manually override this below:")
        
        if current_class in ["Class I", "Class II", "Class III"]:
            reasons = []
            symptoms = sum(1 for i in range(1, 10) if st.session_state.data.get(f"s_{i}") == "有")
            has_disease = any([
                st.session_state.data.get("d_cardio") == "有", 
                st.session_state.data.get("d_metabolic") == "有", 
                st.session_state.data.get("d_renal") == "有"
            ])
            is_active = st.session_state.data.get("is_active") == "是"
            parq_score = sum(1 for i in range(1, 8) if st.session_state.data.get(f"parq_{i}") == "有")

            if current_class == "Class III":
                if symptoms >= 1:
                    reasons.append("Form B ≥ 1")
                if has_disease and not is_active:
                    reasons.append("Known disease without regular exercise")
            elif current_class == "Class II":
                if has_disease and is_active and symptoms == 0:
                    reasons.append("Known disease with regular exercise & Form B = 0")
                if parq_score > 0:
                    reasons.append("Form A (PAR-Q) ≥ 1")
            elif current_class == "Class I":
                reasons.append("No known disease & Form A = 0 & Form B = 0")
                
            if reasons:
                reason_str = " AND/OR ".join(reasons) if current_class != "Class I" else reasons[0]
                
                if current_class == "Class I":
                    st.success(f"✅ **Reason for {current_class}:** {reason_str}")
                elif current_class == "Class II":
                    st.warning(f"⚠️ **Reason for {current_class}:** {reason_str}")
                elif current_class == "Class III":
                    st.error(f"🚨 **Reason for {current_class}:** {reason_str}")
    
    options = ["Class I", "Class II", "Class III"]
    default_idx = options.index(current_class) if current_class in options else None
    selected_class = st.radio("Manual Override", options, index=default_idx, horizontal=True, label_visibility="collapsed")
    
    result_container = st.container()
    
    st.markdown("---")

    c1, c2 = st.columns(2)
    age = c1.number_input("2. Patient Age", min_value=10, max_value=120, value=None, step=1, key="thr_age")
    rhr = c2.number_input("3. Standing Resting Heart Rate (bpm)", min_value=30, max_value=220, value=None, step=1, key="thr_rhr")

    if st.button("Calculate Guidelines", type="primary", use_container_width=True):
        if selected_class is None:
            result_container.warning("⚠️ Please select a Risk Class before calculating.")
        elif age is not None and rhr is not None:
            thr_main, thr_details, err = calculate_thr(int(age), int(rhr), selected_class)
            
            if not err:
                recs = {
                    "Class I": {
                        "intensity": "Moderate: ✔️ Vigorous: ✔️",
                        "hrr": "≤ 84% HRR",
                        "rpe": "< 17",
                        "medical": "Not necessary",
                        "supervision": "Not required",
                        "monitor": "Monitor HR in First session (optional)"
                    },
                    "Class II": {
                        "intensity": "Moderate: ✔️ Vigorous: ❌",
                        "hrr": "< 60% HRR",
                        "rpe": "< 14",
                        "medical": "Recommended for vigorous intensity exercise",
                        "supervision": "Not required: light to moderate intensity<br>Required: vigorous intensity",
                        "monitor": "Continuous HR or RPE monitoring"
                    },
                    "Class III": {
                        "intensity": "Moderate: ❌ Vigorous: ❌",
                        "hrr": "< 40% HRR",
                        "rpe": "< 12",
                        "medical": "Recommended",
                        "supervision": "Required",
                        "monitor": "Continuous HR and RPE monitoring together with close supervision"
                    }
                }
                rec = recs[selected_class]
                
                with result_container:
                    # Tighter Banner Box, Larger White Font, Line separator
                    st.markdown(f"""
                    <div style="background-color: #2c3e50; padding: 15px 20px; border-radius: 8px 8px 0 0; text-align: center;">
                        <h2 style="color: #ffffff !important; margin: 0; font-size: 42px; font-weight: bold;">{thr_main}</h2>
                        <hr style="border: 0; border-top: 1px solid rgba(255,255,255,0.4); margin: 12px auto; width: 90%;">
                        <p style="color: #ffffff !important; margin: 0; opacity: 0.85; font-size: 16px;">{thr_details}</p>
                    </div>
                    """, unsafe_allow_html=True)
                    
                    with st.container(border=True):
                        st.subheader(f"📋 {selected_class} Clinical Guidelines")
                        st.markdown("<hr style='margin: 0px 0px 15px 0px;'/>", unsafe_allow_html=True) # Line strictly under Title
                        
                        r_col1, r_col2 = st.columns([1.5, 2.5])
                        
                        r_col1.markdown("**Recommended Intensity:**")
                        r_col2.markdown(rec['intensity'])
                        
                        r_col1.markdown("**Safe exercise zone:**")
                        r_col2.markdown(rec['hrr'])
                        
                        r_col1.markdown("**RPE during Exercise:**")
                        r_col2.markdown(rec['rpe'])
                        
                        r_col1.markdown("**Medical clearance:**")
                        r_col2.markdown(rec['medical'])
                        
                        r_col1.markdown("**Supervision:**")
                        r_col2.markdown(rec['supervision'], unsafe_allow_html=True) 
                        
                        r_col1.markdown("**Monitoring:**")
                        r_col2.markdown(rec['monitor'])
                        
                        st.markdown("<hr style='margin: 15px 0px;'/>", unsafe_allow_html=True) # Line above Remarks
                        # Smaller Remarks
                        st.markdown("<p style='font-size: 14px; font-style: italic; color: #6c757d; margin: 0;'>#Adjustment to target HR zone should be made on individual basis (keep increment of progress ≤ 5%HRR per week)</p>", unsafe_allow_html=True)
            else:
                result_container.error(err)
        else:
            result_container.warning("⚠️ Please input valid Age and Standing Resting HR values before calculating.")
    else:
        result_container.info("💡 Please input the patient's **Age** and **Standing Resting HR** above, then click 'Calculate Guidelines' to generate the report.")


def main():
    inject_custom_css()
    
    current_class = calculate_current_class()
    b_class_only = evaluate_b_only()
    
    class_colors = {
        "Pending": {"bg": "#f8f9fa", "border": "#6c757d", "text": "#495057"},
        "Pending Form A": {"bg": "#f8f9fa", "border": "#6c757d", "text": "#495057"},
        "Class I": {"bg": "#e8f5e9", "border": "#2e7d32", "text": "#1b5e20"},
        "Class II": {"bg": "#fff3e0", "border": "#ef6c00", "text": "#e65100"},
        "Class III": {"bg": "#ffebee", "border": "#c62828", "text": "#b71c1c"}
    }
    
    theme = class_colors[current_class] if current_class in class_colors else class_colors["Pending"]
    display_text = "Incomplete" if "Pending" in current_class else current_class
    
    st.title("🏃‍♂️ Risk Stratification of Cardiopulmonary Fitness Training")
    
    st.markdown(f"""
    <div class="risk-strat-box" style="background-color: {theme['bg']}; border: 2px solid {theme['border']}; margin-bottom: 20px;">
        <span class="risk-strat-text" style="color: {theme['text']};">Risk Stratification: {display_text}</span>
    </div>
    """, unsafe_allow_html=True)
    
    show_all_tabs = st.session_state.get("force_show_all", False)
    should_hide_a = (b_class_only in ["Class II", "Class III"]) and not show_all_tabs
    
    if should_hide_a:
        available_tabs = ["1. 運動風險評估\n(表格 B)", "3. Target HR &\nClinical Guidelines"]
    else:
        available_tabs = ["1. 運動風險評估\n(表格 B)", "2. 體能活動適應能力問卷\n(表格 A)", "3. Target HR &\nClinical Guidelines"]
        
    if st.session_state["current_tab"] not in available_tabs:
        st.session_state["current_tab"] = available_tabs[0]
        
    # --- Navigation Sidebar ---
    with st.sidebar:
        st.header("表單選擇")
        st.markdown("請選擇下方表單：")
        for i, tab_name in enumerate(available_tabs):
            btn_type = "primary" if st.session_state["current_tab"] == tab_name else "secondary"
            if st.button(tab_name, type=btn_type, key=f"nav_{i}", use_container_width=True):
                go_to_tab(tab_name)
                st.rerun()

    if st.session_state["current_tab"] == "1. 運動風險評估\n(表格 B)":
        tab_b_acsm(b_class_only, show_all_tabs)
    elif st.session_state["current_tab"] == "2. 體能活動適應能力問卷\n(表格 A)":
        tab_a_parq()
    elif st.session_state["current_tab"] == "3. Target HR &\nClinical Guidelines":
        tab_d_thr(current_class)
        
    st.markdown("---")
    st.caption("#Adjustment to target HR zone should be made on individual basis (keep increment of progress ≤ 5%HRR per week)")

if __name__ == "__main__":
    main()
