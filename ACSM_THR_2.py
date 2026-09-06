import streamlit as st

# ---------- 1. Initialization & Config ----------
st.set_page_config(
    page_title="Risk Stratification of Cardiopulmonary Fitness Training", 
    layout="wide", 
    initial_sidebar_state="collapsed"
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

a_key_names = {f"parq_{i}": f"問題 {i}" for i in range(1, 8)}

def get_missing_b():
    return [name for k, name in b_key_names.items() if st.session_state.data.get(k) is None]

def get_missing_a():
    return [name for k, name in a_key_names.items() if st.session_state.data.get(k) is None]

def evaluate_b_only():
    if get_missing_b():
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
        
    if get_missing_a():
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
    if rhr >= mhr: 
        return None, None, "Abnormal Resting Heart Rate (>= Maximum HR)"
    hrr = mhr - rhr

    details_str = f"Maximum HR: {mhr} bpm | Standing HR at rest: {rhr} bpm | HR Reserve: {hrr} bpm"

    if risk_level == "Class III":
        limit = int((hrr * 0.40) + rhr)
        return f"Training HR: < {limit} bpm", details_str, None
    elif risk_level == "Class II":
        limit = int((hrr * 0.60) + rhr)
        return f"Training HR: < {limit} bpm", details_str, None
    else:
        upper = int((hrr * 0.84) + rhr)
        return f"Training HR: ≤ {upper} bpm", details_str, None

# ---------- 3. Callbacks & Helpers ----------
def go_to_tab(tab_name):
    st.session_state["current_tab"] = tab_name
    st.session_state["show_b_errors"] = False
    st.session_state["show_a_errors"] = False

def enable_all_tabs_and_go():
    st.session_state["force_show_all"] = True
    go_to_tab("2. 體能活動適應能力問卷\n(表格 A)")

def try_complete_b(target_tab):
    if get_missing_b():
        st.session_state["show_b_errors"] = True
    else:
        st.session_state["show_b_errors"] = False
        go_to_tab(target_tab)

def try_complete_a(target_tab):
    if get_missing_a():
        st.session_state["show_a_errors"] = True
    else:
        st.session_state["show_a_errors"] = False
        go_to_tab(target_tab)

def render_inline_question(label, key, options=("否", "有"), check_error=False):
    is_missing = check_error and st.session_state.data.get(key) is None
    
    col1, col2 = st.columns([3, 1]) 
    with col1:
        if is_missing:
            st.error(f"請回答: {label}")
        else:
            st.markdown(f"**{label}**")
    with col2:
        saved_val = st.session_state.data.get(key)
        idx = options.index(saved_val) if saved_val in options else None
        st.radio(" ", options, key=key, index=idx, horizontal=True, label_visibility="collapsed", on_change=update_val, args=(key,))

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
        
    st.info("*注意：如有以上徵狀，可能不適合進行強度中度或以上的心肺體能訓練。詳情請向醫生或物理治療師查詢")
    st.divider()
    
    st.subheader("已知醫療狀況 (Known Diseases)")
    render_inline_question("已知心血管疾病 (例如：冠心病、心臟病、中風、心臟衰竭、心律不正)", "d_cardio", check_error=check_err)
    render_inline_question("已知代謝疾病 (例如：糖尿病、甲狀腺疾病)", "d_metabolic", check_error=check_err)
    render_inline_question("已知腎臟疾病", "d_renal", check_error=check_err)
    st.divider()

    st.subheader("當前運動習慣")
    activity_question = "您目前是否定期進行體能活動？(過去 3 個月內，每週至少 3 天，每次 30 分鐘中等強度活動)"
    render_inline_question(activity_question, "is_active", options=("否", "是"), check_error=check_err)
    st.divider()
    
    if check_err and get_missing_b():
        st.error(f"⚠️ 還有 **{len(get_missing_b())}** 個問題尚未填寫。")

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

    st.divider()
    
    if check_err and get_missing_a():
        st.error(f"⚠️ 還有 **{len(get_missing_a())}** 個問題尚未填寫。")

    st.button("✅ 完成運動風險判別（請交給職員）", type="primary", use_container_width=True, on_click=try_complete_a, args=("3. Target HR &\nClinical Guidelines",))


def tab_d_thr(current_class):
    st.header("Target Heart Rate Calculator")
    
    if current_class == "Pending":
        st.info("💡 The system evaluation is currently **Incomplete**. Please manually select the Risk Class below:")
    else:
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
                if symptoms >= 1: reasons.append("Form B ≥ 1")
                if has_disease and not is_active: reasons.append("Known disease without regular exercise")
            elif current_class == "Class II":
                if has_disease and is_active and symptoms == 0: reasons.append("Known disease with regular exercise & Form B = 0")
                if parq_score > 0: reasons.append("Form A (PAR-Q) ≥ 1")
            elif current_class == "Class I":
                reasons.append("No known disease & Form A = 0 & Form B = 0")
                
            if reasons:
                reason_str = " AND/OR ".join(reasons) if current_class != "Class I" else reasons[0]
                
                if current_class == "Class I": st.success(f"✅ **Reason for {current_class}:** {reason_str}")
                elif current_class == "Class II": st.warning(f"⚠️ **Reason for {current_class}:** {reason_str}")
                elif current_class == "Class III": st.error(f"🚨 **Reason for {current_class}:** {reason_str}")
    
    options = ["Class I", "Class II", "Class III"]
    default_idx = options.index(current_class) if current_class in options else None
    selected_class = st.radio("Manual Override", options, index=default_idx, horizontal=True)
    
    st.divider()

    c1, c2 = st.columns(2)
    age = c1.number_input("2. Patient Age", min_value=10, max_value=120, value=None, step=1, key="thr_age")
    rhr = c2.number_input("3. Standing Resting Heart Rate (bpm)", min_value=30, max_value=220, value=None, step=1, key="thr_rhr")

    if st.button("Calculate Guidelines", type="primary", use_container_width=True):
        if selected_class is None:
            st.warning("⚠️ Please select a Risk Class before calculating.")
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
                        "supervision": "Not required: light to moderate intensity | Required: vigorous intensity",
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
                
                # --- PURE NATIVE STREAMLIT RESULT BOX ---
                with st.container(border=True):
                    st.subheader(thr_main)
                    st.caption(thr_details)
                    st.divider()
                    st.subheader(f"📋 {selected_class} Clinical Guidelines")
                    st.markdown(f"**Recommended Intensity:** {rec['intensity']}")
                    st.markdown(f"**Safe exercise zone:** {rec['hrr']}")
                    st.markdown(f"**RPE during Exercise:** {rec['rpe']}")
                    st.markdown(f"**Medical clearance:** {rec['medical']}")
                    st.markdown(f"**Supervision:** {rec['supervision']}")
                    st.markdown(f"**Monitoring:** {rec['monitor']}")
                    st.write("")
                    st.caption("_#Adjustment to target HR zone should be made on individual basis (keep increment of progress ≤ 5%HRR per week)_")
            else:
                st.error(err)
        else:
            st.warning("⚠️ Please input valid Age and Standing Resting HR values before calculating.")
    else:
        st.info("💡 Please input the patient's **Age** and **Standing Resting HR** above, then click 'Calculate Guidelines' to generate the report.")

# ---------- 5. Main Application ----------
def main():
    current_class = calculate_current_class()
    b_class_only = evaluate_b_only()
    
    display_text = "Incomplete" if "Pending" in current_class else current_class
    
    st.title("🏃‍♂️ Risk Stratification of Cardiopulmonary Fitness Training")
    st.info(f"**Risk Stratification: {display_text}**")
    
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

    # --- Render Selected Tab ---
    if st.session_state["current_tab"] == "1. 運動風險評估\n(表格 B)":
        tab_b_acsm(b_class_only, show_all_tabs)
    elif st.session_state["current_tab"] == "2. 體能活動適應能力問卷\n(表格 A)":
        tab_a_parq()
    elif st.session_state["current_tab"] == "3. Target HR &\nClinical Guidelines":
        tab_d_thr(current_class)
        
if __name__ == "__main__":
    main()
