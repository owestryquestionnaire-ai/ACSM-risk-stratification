import streamlit as st

# ---------- 1. Initialization & Config ----------
# 設定 layout="wide" 以使用全螢幕寬度
st.set_page_config(page_title="運動準備度和風險評估", layout="wide")

def inject_custom_css():
    st.markdown(
        """
        <style>
        /* Global Base Font and Black Color (Desktop/iPad) */
        html, body, [data-testid="stMarkdownContainer"] {
            font-size: 20px !important; 
            color: #000000 !important;
            font-weight: 400 !important;
            line-height: 1.4 !important; 
        }

        /* --- SAFE SPACING (Desktop/iPad) --- */
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

        /* Headers - BOLD */
        h1 { font-size: 34px !important; color: #000000 !important; font-weight: bold !important; line-height: 1.4 !important; margin-bottom: 10px !important;}
        h2 { font-size: 30px !important; color: #000000 !important; font-weight: bold !important; border-bottom: 2px solid #000; padding-bottom: 8px !important; line-height: 1.4 !important; margin-top: 10px !important; margin-bottom: 15px !important;}
        h3 { font-size: 26px !important; color: #000000 !important; font-weight: bold !important; line-height: 1.4 !important; margin-bottom: 10px !important;}
        h4 { font-size: 22px !important; color: #444 !important; font-weight: bold !important; line-height: 1.4 !important; margin-bottom: 10px !important;}

        /* Radio Buttons & Checkbox Labels */
        div[data-testid="stRadio"] label p, 
        div[data-testid="stCheckbox"] label p {
            font-size: 22px !important; 
            font-weight: 400 !important;
            color: #000000 !important;
            line-height: 1.4 !important; 
        }
        
        .stRadio > div { gap: 0rem !important; } 
        .stCheckbox > div { margin-bottom: 0rem !important; }

        /* Standard Text */
        .stMarkdown p {
            font-size: 20px !important; 
            color: #000000 !important;
            font-weight: 400 !important;
            line-height: 1.4 !important; 
            margin-bottom: 10px !important; 
        }

        /* Input Box Labels */
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
        
        .question-text {
            margin-top: 0px !important; 
            font-size: 22px !important; 
            line-height: 1.4 !important; 
        }

        /* ----- CUSTOM RED BUTTON STYLING ----- */
        button[kind="primary"], [data-testid="baseButton-primary"],
        button[kind="secondary"], [data-testid="baseButton-secondary"] {
            font-size: 22px !important;
            padding: 8px 16px !important; 
            font-weight: bold !important;
            line-height: 1.4 !important;
        }
        button[kind="primary"], [data-testid="baseButton-primary"] {
            background-color: #ef5350 !important; 
            color: white !important;
            border-color: #ef5350 !important; 
        }
        button[kind="primary"]:hover, [data-testid="baseButton-primary"]:hover {
            background-color: #e53935 !important; 
            border-color: #e53935 !important;
            color: white !important;
        }

        /* =========================================================
           📱 MOBILE RESPONSIVE PATCH (iPhone View Only)
           將斷點從 768px 下修至 600px，釋放平板的螢幕空間
           ========================================================= */
        @media (max-width: 600px) {
            /* 1. Reduce Global Font Sizes */
            html, body, [data-testid="stMarkdownContainer"] { font-size: 16px !important; }
            h1 { font-size: 26px !important; }
            h2 { font-size: 22px !important; }
            h3 { font-size: 20px !important; }
            h4 { font-size: 18px !important; }
            
            .stMarkdown p { font-size: 16px !important; margin-bottom: 5px !important;}
            .question-text { font-size: 18px !important; margin-bottom: 10px !important; }
            
            /* 2. Adjust Radio Buttons for Touch */
            div[data-testid="stRadio"] label p, 
            div[data-testid="stCheckbox"] label p {
                font-size: 18px !important; 
            }
            .stRadio > div { gap: 1rem !important; padding-bottom: 10px !important;} 
            
            /* 3. Make Buttons Mobile Friendly (Wrap text if too long) */
            button[kind="primary"], [data-testid="baseButton-primary"],
            button[kind="secondary"], [data-testid="baseButton-secondary"] {
                font-size: 18px !important;
                padding: 12px 10px !important; 
                white-space: normal !important; 
                height: auto !important;
            }

            /* 4. Relax vertical spacing so stacked elements don't crush */
            div[data-testid="stVerticalBlock"] {
                gap: 1rem !important; 
            }
            
            /* 5. Scale down the final result box */
            .final-thr-part { font-size: 24px !important; padding: 12px 15px !important; }
            .final-rec-part { padding: 12px 15px !important; }
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
    
    if (has_disease and not is_active) or (symptoms > 0):
        return "Class III"
    if has_disease and is_active and symptoms == 0:
