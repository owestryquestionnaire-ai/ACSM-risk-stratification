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
        return "Class II"
    return "Class I"

def calculate_current_class():
    b_class = evaluate_b_only()
    
    if b_class in ["Class III", "Class II", "Pending"]:
        return b_class
        
    missing_a = get_missing_a()
    if missing_a:
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
    st.session_state["show_b_errors"] = False
    st.session_state["show_a_errors"] = False

def enable_all_tabs_and_go():
    st.session_state["force_show_all"] = True
    go_to_tab("2. 體能活動準備問卷 (表格 A)")

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
    
    col1, col2 = st.columns([7, 3]) 
    with col1:
        if is_missing:
            # 移除了 ❌ 符號，保留紅色粗體與背景高光
            st.markdown(f'<div class="question-text" style="color: #c62828; font-weight: bold; background-color: #ffebee; border-left: 4px solid #c62828; padding-left: 8px;">{label}</div>', unsafe_allow_html=True)
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
        "5. 足踝腫",
        "6. 心悸或心跳過快",
        "7. 間歇肌肉疼痛、抽筋",
        "8. 心雜音",
        "9. 一般活動感到不尋常的疲倦或氣喘"
    ]
    for i, q in enumerate(s_items, 1):
        render_inline_question(q, f"s_{i}", check_error=check_err)
        
    st.info("*注意：如有以上徵狀，可能不適合進行強度中度或以上的心肺體能訓練。詳情請向醫生或物理治療師查詢")
    
    st.markdown("---")
    st.subheader("已知醫療狀況 (Known Diseases)")
    render_inline_question("已知心血管疾病 (例如：冠心病、心臟病、中風、心臟衰竭、心律不正)", "d_cardio", check_error=check_err)
    render_inline_question("已知代謝疾病 (例如：糖尿病、甲狀腺疾病)", "d_metabolic", check_error=check_err)
    render_inline_question("已知腎臟疾病", "d_renal", check_error=check_err)

    st.markdown("---")
    st.subheader("當前運動習慣")
    activity_question = "您目前是否定期進行體能活動？<br><span style='font-size: 18px; color: #555;'>(過去 3 個月內，每週至少 3 天，每次 30 分鐘中等強度活動)</span>"
    
    render_inline_question(activity_question, "is_active", options=("否", "是"), check_error=check_err)

    st.markdown("---")
    
    if check_err:
        missing = get_missing_b()
        if missing:
            st.error(f"⚠️ 還有 **{len(missing)}** 個問題尚未填寫，請檢查上方標示為紅色的項目。")

    if b_class == "Pending":
        st.button("➡️ 儲存並前往下一步", type="primary", use_container_width=True, on_click=try_complete_b, args=("3. Target HR & Clinical Guidelines",))
    elif b_class in ["Class II", "Class III"]:
        if not show_all_tabs:
            st.warning(f"🚨 根據表格 B，運動風險類別為 **{b_class}**。系統已自動隱藏表格 A。")
            c1, c2 = st.columns(2)
            with c1:
                st.button("✅ 完成運動風險判別（請交給職員）", type="primary", use_container_width=True, on_click=try_complete_b, args=("3. Target HR & Clinical Guidelines",))
            with c2:
                st.button("📝 顯示隱藏的表單 (前往表格 A)", use_container_width=True, on_click=enable_all_tabs_and_go)
        else:
            st.warning(f"🚨 根據表格 B，運動風險類別為 **{b_class}**。您選擇繼續填寫表格 A。")
            st.button("➡️ 儲存並前往「2. 體能活動準備問卷」", type="primary", use_container_width=True, on_click=try_complete_b, args=("2. 體能活動準備問卷 (表格 A)",))
    else:
        st.button("➡️ 儲存並前往「2. 體能活動準備問卷」", type="primary", use_container_width=True, on_click=try_complete_b, args=("2. 體能活動準備問卷 (表格 A)",))


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

    st.button("✅ 完成運動風險判別（請交給職員）", type="primary", use_container_width=True, on_click=try_complete_a, args=("3. Target HR & Clinical Guidelines",))


def tab_d_thr(current_class):
    st.header("Target Heart Rate & Clinical Recommendations")
    
    st.subheader("⚙️ Select Risk Class")
    
    if current_class == "Pending":
        st.markdown("💡 The system evaluation is currently **Incomplete**. Please manually select the Risk Class below:")
    else:
        st.markdown(f"💡 The system evaluates the patient as **{current_class}**. You can manually override this below:")
    
    options = ["Class I", "Class II", "Class III"]
    default_idx = options.index(current_class) if current_class in options else None
    selected_class = st.radio("Manual Override", options, index=default_idx, horizontal=True, label_visibility="collapsed")
    
    result_container = st.container()
    
    st.markdown("---")
    st.subheader("🎯 Input Data")

    c1, c2 = st.columns(2)
    age = c1.number_input("Age", min_value=10, max_value=120, value=None, step=1, key="thr_age")
    rhr = c2.number_input("Standing Resting HR", min_value=30, max_value=220, value=None, step=1, key="thr_rhr")

    if st.button("Calculate", type="primary", use_container_width=True):
        if selected_class is None:
            result_container.warning("⚠️ Please select a Risk Class before calculating.")
        elif age is not None and rhr is not None:
            thr_string, err = calculate_thr(int(age), int(rhr), selected_class)
            
            if not err:
                recs = {
                    "Class I": {
                        "intensity": "Moderate: ✔️ Vigorous: ✔️",
                        "hrr": "≤ 84% HRR",
                        "rpe": "&lt; 17",
                        "medical": "Not necessary",
                        "supervision": "Not required",
                        "monitor": "Monitor HR in First session (to facilitate teaching but it is not compulsory)"
                    },
                    "Class II": {
                        "intensity": "Moderate: ✔️ Vigorous: ❌",
                        "hrr": "&lt; 60% HRR",
                        "rpe": "&lt; 14",
                        "medical": "Recommended for vigorous intensity exercise",
                        "supervision": "Not required (unless patient is working for vigorous exercise)",
                        "monitor": "Continuous HR or RPE monitoring"
                    },
                    "Class III": {
                        "intensity": "Moderate: ❌ Vigorous: ❌",
                        "hrr": "&lt; 40% HRR",
                        "rpe": "&lt; 12",
                        "medical": "Recommended",
                        "supervision": "Required (for both moderate and vigorous exercise)",
                        "monitor": "Continuous HR and RPE monitoring together with close supervision"
                    }
                }
                rec = recs[selected_class]
                
                result_container.markdown(f"""
                <div class="final-result-box">
                    <div class="final-thr-part">
                        {thr_string}
                    </div>
                    <div class="final-rec-part">
                        <h3 style="margin-top: 0; border-bottom: 2px solid #ccc; padding-bottom: 10px;">📋 {selected_class} Clinical Guidelines</h3>
                        <p><b>Recommended Exercise Intensity:</b><br>{rec['intensity']}</p>
                        <p><b>Safe exercise zone:</b> {rec['hrr']}</p>
                        <p><b>RPE during Exercise:</b> {rec['rpe']}</p>
                        <p><b>Medical Clearance:</b><br>{rec['medical']}</p>
                        <p><b>Supervision:</b><br>{rec['supervision']}</p>
                        <p><b>Monitoring:</b><br>{rec['monitor']}</p>
                    </div>
                </div>
                """, unsafe_allow_html=True)
            else:
                result_container.error(err)
        else:
            result_container.warning("⚠️ Please input valid Age and Standing Resting HR values before calculating.")
    else:
        result_container.info("💡 Please input the patient's **Age** and **Standing Resting HR** above, then click 'Calculate' to generate the report.")


def main():
    inject_custom_css()
    
    current_class = calculate_current_class()
    b_class_only = evaluate_b_only()
    
    class_colors = {
        "Pending": {"bg": "#f8f9fa", "border": "#6c757d", "text": "#495057"},
        "Class I": {"bg": "#e8f5e9", "border": "#2e7d32", "text": "#1b5e20"},
        "Class II": {"bg": "#fff3e0", "border": "#ef6c00", "text": "#e65100"},
        "Class III": {"bg": "#ffebee", "border": "#c62828", "text": "#b71c1c"}
    }
    theme = class_colors[current_class]
    
    display_text = "Incomplete" if current_class == "Pending" else current_class
    
    st.title("🏃‍♂️ Risk Class stratification for cardiopulmonary fitness training")
    
    st.markdown(f"""
    <div style="background-color: {theme['bg']}; border: 2px solid {theme['border']}; border-radius: 8px; padding: 10px; text-align: center; margin-bottom: 15px;">
        <span style="margin: 0; color: {theme['text']}; font-size: 26px; font-weight: bold;">Risk Stratification: {display_text}</span>
    </div>
    """, unsafe_allow_html=True)
    
    show_all_tabs = st.session_state.get("force_show_all", False)
    should_hide_a = (b_class_only in ["Class II", "Class III"]) and not show_all_tabs
    
    if should_hide_a:
        available_tabs = ["1. 運動風險評估 (表格 B)", "3. Target HR & Clinical Guidelines"]
    else:
        available_tabs = ["1. 運動風險評估 (表格 B)", "2. 體能活動準備問卷 (表格 A)", "3. Target HR & Clinical Guidelines"]
        
    if st.session_state["current_tab"] not in available_tabs:
        st.session_state["current_tab"] = available_tabs[0]
        
    cols = st.columns(len(available_tabs))
    for i, tab_name in enumerate(available_tabs):
        btn_type = "primary" if st.session_state["current_tab"] == tab_name else "secondary"
        if cols[i].button(tab_name, type=btn_type, key=f"nav_{i}", use_container_width=True):
            go_to_tab(tab_name)
            st.rerun()

    st.markdown("---")

    if st.session_state["current_tab"] == "1. 運動風險評估 (表格 B)":
        tab_b_acsm(b_class_only, show_all_tabs)
    elif st.session_state["current_tab"] == "2. 體能活動準備問卷 (表格 A)":
        tab_a_parq()
    elif st.session_state["current_tab"] == "3. Target HR & Clinical Guidelines":
        tab_d_thr(current_class)
        
    st.markdown("---")
    st.caption("#Adjustment to target HR zone should be made on individual basis (keep increment of progress ≤ 5%HRR per week)")

if __name__ == "__main__":
    main()
