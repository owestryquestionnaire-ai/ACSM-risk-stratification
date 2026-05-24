import streamlit as st

# ---------- 1. Initialization & Config ----------
# 設定 layout="wide" 以使用全螢幕寬度
st.set_page_config(page_title="運動準備度和風險評估", layout="wide")

def inject_custom_css():
    st.markdown(
        """
        <style>
        /* Global Base Font and Black Color */
        html, body, [data-testid="stMarkdownContainer"] {
            font-size: 20px !important; 
            color: #000000 !important;
            font-weight: 400 !important;
            line-height: 1.4 !important; 
        }

        /* --- SAFE SPACING (Fixing Overlaps) --- */
        div[data-testid="stVerticalBlock"] {
            gap: 0.5rem !important; 
        }
        .element-container {
            margin-bottom: 0px !important;
        }
        hr {
            margin-top: 0.5rem !important;
            margin-bottom: 0.5rem !important;
            padding: 0px !important;
        }

        /* Headers - BOLD (Added Safe Bottom Margins) */
        h1 { font-size: 34px !important; color: #000000 !important; font-weight: bold !important; line-height: 1.4 !important; margin-bottom: 10px !important;}
        
        h2 { font-size: 30px !important; color: #000000 !important; font-weight: bold !important; border-bottom: 2px solid #000; padding-bottom: 8px !important; line-height: 1.4 !important; margin-top: 10px !important; margin-bottom: 15px !important;}
        
        h3 { font-size: 26px !important; color: #000000 !important; font-weight: bold !important; line-height: 1.4 !important; margin-bottom: 10px !important;}
        h4 { font-size: 22px !important; color: #444 !important; font-weight: bold !important; line-height: 1.4 !important; margin-bottom: 10px !important;}

        /* Radio Buttons & Checkbox Labels - REGULAR */
        div[data-testid="stRadio"] label p, 
        div[data-testid="stCheckbox"] label p {
            font-size: 22px !important; 
            font-weight: 400 !important;
            color: #000000 !important;
            line-height: 1.4 !important; 
        }
        
        /* Reduce gap between radio button items (Keeps options tight) */
        .stRadio > div { gap: 0rem !important; } 
        .stCheckbox > div { margin-bottom: 0rem !important; }

        /* Standard Text - REGULAR */
        .stMarkdown p {
            font-size: 20px !important; 
            color: #000000 !important;
            font-weight: 400 !important;
            line-height: 1.4 !important; 
            margin-bottom: 10px !important; 
        }

        /* Input Box Labels - BOLD */
        label[data-testid="stWidgetLabel"] p {
            font-size: 22px !important; 
            font-weight: bold !important;
            color: #000000 !important;
            line-height: 1.4 !important;
            margin-bottom: 5px !important;
        }

        /* Combined Result Box Styling */
        .final-result-box {
            border: 3px solid #000000;
            border-radius: 10px;
            overflow: hidden;
            box-shadow: 2px 2px 10px rgba(0,0,0,0.1);
            margin-bottom: 15px !important;
        }
        .final-thr-part {
            font-size: 32px !important; 
            color: #000000 !important;
            font-weight: bold !important;
            line-height: 1.4 !important;
            padding: 15px 20px !important; 
            background-color: #ffffff;
        }
        .final-rec-part {
            background-color: #f8f9fa;
            padding: 15px 20px !important; 
            border-top: 3px dashed #000000;
        }
        .final-rec-part p {
            margin-bottom: 5px !important; 
            line-height: 1.4 !important; 
        }
        
        /* Vertical alignment for side-by-side columns */
        .question-text {
            margin-top: 0px !important; 
            font-size: 22px !important; 
            line-height: 1.4 !important; 
        }

        /* ----- CUSTOM RED BUTTON STYLING ----- */
        button[kind="primary"], [data-testid="baseButton-primary"] {
            background-color: #ef5350 !important; 
            color: white !important;
            border-color: #ef5350 !important; 
            font-size: 22px !important;
            padding: 8px 16px !important; 
            font-weight: bold !important;
            line-height: 1.4 !important;
        }
        button[kind="primary"]:hover, [data-testid="baseButton-primary"]:hover {
            background-color: #e53935 !important; 
            border-color: #e53935 !important;
            color: white !important;
        }
        button[kind="secondary"], [data-testid="baseButton-secondary"] {
            font-size: 22px !important;
            padding: 8px 16px !important; 
            font-weight: bold !important;
            line-height: 1.4 !important;
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
        st.session_state["current_tab"] = "1. 運動風險評估 (表格 B)"

def update_val(key):
    st.session_state.data[key] = st.session_state[key]

init_session_states()


# ---------- 2. Logic Functions ----------
def evaluate_b_only():
    # 檢查表格 B 是否所有題目都已作答
    b_keys = [f"s_{i}" for i in range(1, 10)] + ["d_cardio", "d_metabolic", "d_renal", "is_active"]
    if any(st.session_state.data.get(k) is None for k in b_keys):
        return "Pending"

    symptoms = sum(1 for i in range(1, 10) if st.session_state.data.get(f"s_{i}") == "有")
    has_disease = any([
        st.session_state.data.get("d_cardio") == "有", 
        st.session_state.data.get("d_metabolic") == "有", 
        st.session_state.data.get("d_renal") == "有"
    ])
    is_active = st.session_state.data.get("is_active") == "是"
    
    if (has_disease and not is_active) or (symptoms > 0):
        return "Class III"
    if has_disease and is_active and symptoms == 0:
        return "Class II"
    return "Class I"

def calculate_current_class():
    b_class = evaluate_b_only()
    
    # 如果表格 B 已經是 II, III，或者是 Pending（未完成），直接返回
    if b_class in ["Class III", "Class II", "Pending"]:
        return b_class
        
    # 如果表格 B 是 Class I，則繼續檢查表格 A 是否已作答完成
    a_keys = [f"parq_{i}" for i in range(1, 8)]
    if any(st.session_state.data.get(k) is None for k in a_keys):
        return "Pending"

    parq_score = sum(1 for i in range(1, 8) if st.session_state.data.get(f"parq_{i}") == "有")
    if parq_score > 0:
        return "Class II"
        
    return "Class I"

def calculate_thr(age, rhr, risk_level):
    mhr = 220 - age
    if rhr >= mhr: return None, "Abnormal Resting Heart Rate (>= Maximum HR)"
    hrr = mhr - rhr

    details_html = f'<div style="font-size: 18px; font-weight: normal; margin-top: 5px; color: #444;">Maximum HR: {mhr} | Standing HR at rest: {rhr} | HR Reserve: {hrr}</div>'

    if risk_level == "Class III":
        limit = int((hrr * 0.40) + rhr)
        thr_main = f"Training HR: &lt; {limit} bpm"
        return thr_main + details_html, None
    elif risk_level == "Class II":
        limit = int((hrr * 0.60) + rhr)
        thr_main = f"Training HR: &lt; {limit} bpm"
        return thr_main + details_html, None
    else:
        upper = int((hrr * 0.84) + rhr)
        thr_main = f"Training HR: ≤ {upper} bpm"
        return thr_main + details_html, None


# ---------- 3. Callbacks & Helpers ----------
def go_to_tab(tab_name):
    st.session_state["current_tab"] = tab_name

def enable_all_tabs_and_go():
    st.session_state["force_show_all"] = True
    st.session_state["current_tab"] = "2. 體能活動準備問卷 (表格 A)"

def render_inline_question(label, key, options=("否", "有")):
    col1, col2 = st.columns([7, 3]) 
    with col1:
        st.markdown(f'<div class="question-text">{label}</div>', unsafe_allow_html=True)
    with col2:
        saved_val = st.session_state.data.get(key)
        idx = options.index(saved_val) if saved_val in options else None
        st.radio("", options, key=key, index=idx, horizontal=True, label_visibility="collapsed", on_change=update_val, args=(key,))


# ---------- 4. Tab Functions ----------
def tab_b_acsm(b_class, show_all_tabs):
    st.header("表格 B：心血管、呼吸系統及代謝性疾病之主要徵狀")
    st.write("請在合適選擇上選擇「有」或「否」：")
    
    s_items = [
        "1. 因心臟缺血而引致的胸口、頸、下顎、上臂 或其他部位痛楚或不適",
        "2. 靜止或輕鬆活動時感到氣喘",
        "3. 暈眩或失去知覺",
        "4. 平臥時或晚間不時氣喘",
        "5. 足踝腫",
        "6. 心悸或心跳過快",
        "7. 間歇肌肉疼痛、抽筋",
        "8. 心雜音",
        "9. 一般活動感到不尋常的疲倦或氣喘"
    ]
    for i, q in enumerate(s_items, 1):
        render_inline_question(q, f"s_{i}")
        
    st.info("*注意：如有以上徵狀，可能不適合進行強度中度或以上的心肺體能訓練。詳情請向醫生或物理治療師查詢")
    
    st.markdown("---")
    st.subheader("已知醫療狀況 (Known Diseases)")
    render_inline_question("已知心血管疾病 (例如：冠心病、心臟病、中風、心臟衰竭、心律不正
