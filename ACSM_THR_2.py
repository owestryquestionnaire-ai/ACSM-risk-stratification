import streamlit as st

# ---------- 1. Initialization & Config ----------
st.set_page_config(page_title="Risk Stratification of Cardiopulmonary Fitness Training", layout="wide", initial_sidebar_state="collapsed")

def inject_custom_css():
    st.markdown(
        """
        <style>
        /* =========================================================
           🖥️ REDUCE TOP MARGIN
           ========================================================= */
        .block-container {
            padding-top: 2.5rem !important; 
            padding-bottom: 1.5rem !important;
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
    
    s
