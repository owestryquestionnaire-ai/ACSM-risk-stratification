import streamlit as st

# --- MUST BE THE VERY FIRST STREAMLIT COMMAND ---
st.set_page_config(page_title="運動準備度和風險評估", layout="centered") 

# --- Helper Functions (The Logic) ---
def calculate_risk(is_active, has_disease, form_a_score, form_b_score):
    """Calculates exercise risk based strictly on the provided Form A, Form B, and disease/activity rules."""
    
    # Class III Logic:
    if (has_disease and not is_active) or (form_b_score > 0):
        return "Class III. Seek medical clearance prior to exercise. Following medical clearance, light intensity exercise recommended. Continuous heart rate and RPE monitoring together with close supervision.", "high" 
    
    # Class II Logic:
    if has_disease and is_active and form_b_score == 0:
        return "Class II. Continue with moderate intensity exercise. Medical clearance recommended before engaging in vigorous intensity exercise.", "moderate" 
    
    if not has_disease and form_a_score > 0 and form_b_score == 0:
        return "Class II. You answered 'Yes' to PAR-Q question(s). Following medical clearance, light to moderate intensity exercise recommended.", "moderate"

    # Class I Logic:
    if not has_disease and form_a_score == 0 and form_b_score == 0:
        if not is_active:
            return "Class I. Light to moderate intensity exercise recommended. May gradually progress to vigorous intensity exercise following ACSM guidelines.", "low" 
        else:
            return "Class I. Continue with moderate or vigorous intensity exercise.", "low" 
            
    # Fallback
    return "Class III. Seek medical clearance prior to exercise.", "high"

def calculate_thr(age, rhr, risk_level_str):
    """Calculates Target Heart Rate (THR) upper limits using Karvonen Formula with structured output."""
    mhr = 220 - age 
    if rhr >= mhr: 
        return None, "靜息心率不能大於或等於估計最大心率 (220 - 年齡)。請檢查您的輸入。" 

    hrr = mhr - rhr 
    
    # Double spaces at the end of lines force a single line break in Markdown
    if risk_level_str == "low":
        upper_bound = int((hrr * 0.84) + rhr)
        thr_zone_display = f"Target Heart Rate **≤ {upper_bound} bpm**." 
        advice = (
            "<u>**Class I**</u>\n\n"
            "Safe Exercise Zone: ≤ 84% HRR  \n"
            "RPE: <17  \n"
            "Recommended Exercise Intensity: Moderate to Vigorous Intensity ✔️  \n"
            "Medical Clearance: Not necessary  \n"
            "Supervision: Not required  \n"
            "Monitoring: Monitor HR in first session (to facilitate teaching but it is not compulsory)"
        )
        
    elif risk_level_str == "moderate":
        upper_bound = int((hrr * 0.60) + rhr)
        thr_zone_display = f"Target Heart Rate **< {upper_bound} bpm**." 
        advice = (
            "<u>**Class II**</u>\n\n"
            "Safe Exercise Zone: < 60% HRR  \n"
            "RPE: <14  \n"
            "Recommended Exercise Intensity: Light to Moderate Intensity  \n"
            "Medical Clearance: Recommended before engaging in vigorous intensity exercise  \n"
            "Supervision: Not strictly required  \n"
            "Monitoring: Recommended to monitor HR and RPE"
        )
        
    elif risk_level_str == "high":
        upper_bound = int((hrr * 0.40) + rhr)
        thr_zone_display = f"Target Heart Rate **< {upper_bound} bpm**." 
        advice = (
            "<u>**Class III**</u>\n\n"
            "Safe Exercise Zone: < 40% HRR  \n"
            "RPE: <12  \n"
            "Recommended Exercise Intensity: Light Intensity  \n"
            "Medical Clearance: **Required prior to exercise 🛑**  \n"
            "Supervision: Close supervision required  \n"
            "Monitoring: Continuous heart rate and RPE monitoring"
        )
        
    else:
        return None, "風險等級尚未確定。" 

    # Final formatted output block
    output = (
        f"Maximum Heart Rate= **{mhr} bpm**.  \n"
        f"Resting Heart Rate= **{rhr} bpm**.  \n"
        f"Heart Rate Reserve= **{hrr} bpm**.  \n\n"
        f"{thr_zone_display}\n\n"
        f"{advice}"
    )
    
    return output, None

# --- Custom CSS for larger font size ---
st.markdown("""
<style>
    p, .stMarkdown { font-size: 1.4rem !important; line-height: 1.6 !important; }
    h1 { font-size: 3rem !important; }
    h2 { font-size: 2.5rem !important; }
    h3 { font-size: 2rem !important; }
    label { font-size: 1.4rem !important; line-height: 1.6 !important; }
    .stCheckbox > label > div, .stRadio > label > div { font-size: 1.4rem !important; line-height: 1.6 !important; }
    .stCheckbox > label > div > p, .stRadio > label > div > p { font-size: 1.4rem !important; line-height: 1.6 !important; }
    .stNumberInput input { font-size: 1.4rem !important; }
    div.stButton > button { font-size: 1.4rem !important; height: auto !important; padding: 0.8em 1.5em !important; }
    .stAlert p { font-size: 1.3rem !important; }
    .stAlert.info p { font-size: 1.25rem !important; }
    .stTabs [data-baseweb="tab"] { font-size: 1.4rem !important; }
    .stCaption { font-size: 1.4rem !important; }
</style>
""", unsafe_allow_html=True)
# --- End Custom CSS ---

st.title("🏃‍♂️ 運動準備度和風險評估") 
st.write("請填寫以下問卷以評估您的體能活動準備度。") 

# Create three tabs
tab1, tab2, tab3 = st.tabs(["1.體能活動適應力問卷（PAR-Q）", "2.ACSM運動風險評估", "3.目標心率計算器"]) 

# ==========================================
# TAB 1: PAR-Q (FORM A)
# ==========================================
with tab1:
    st.header("Form A: 體能活動準備問卷 (PAR-Q)") 
    st.write("請回答以下 7 個一般健康問題：") 
    
    q1 = st.radio("1. 過往醫生有否說你有心臟病或高血壓?", ("否", "是"), horizontal=True, key="parq_q1")
    q2 = st.radio("2. 當你靜止或做運動時有否感覺胸口痛？", ("否", "是"), horizontal=True, key="parq_q2")
    q3 = st.radio("3. 在過去十二個月內，你有否因頭暈而跌倒或失去知覺？", ("否", "是"), horizontal=True, key="parq_q3")
    q4 = st.radio("4. 您是否曾被診斷出患有慢性疾病？", ("否", "是"), horizontal=True, key="parq_q4")
    q5 = st.radio("5. 你是否正在服用治療慢性疾病的處方藥？", ("否", "是"), horizontal=True, key="parq_q5")
    q6 = st.radio("6. 做運動有否可能加重你骨骼，關節或軟組織的痛楚？", ("否", "是"), horizontal=True, key="parq_q6")
    q7 = st.radio("7. 過往醫生有否說你只應進行醫生建議或監察的運動？", ("否", "是"), horizontal=True, key="parq_q7")

    # Score calculation for Form A
    parq_answers = [q1, q2, q3, q4, q5, q6, q7]
    form_a_score = parq_answers.count("是")

    st.markdown("---")
    if st.button("評估 PAR-Q", key="evaluate_parq_button"): 
        if form_a_score > 0: 
            st.error("""🛑 **停止：需要醫療許可。**
因為您回答了一個或多個問題為「是」，在開始增加運動量或進行體能評估前，請先致電或親身與醫生商談，告知醫生這份問卷，以及您回答「是」。
""")
        else:
            st.success("✅ **已獲准運動。**\n\n因為您回答所有問題為「否」，您可以合理地確定開始增加體能活動是安全的。請慢慢開始，逐步增加。") 
            st.info("👉 *現在，請前往第二個分頁 (ACSM 風險與心率) 進行更詳細的風險分層。*") 

# ==========================================
# TAB 2: ACSM & Heart Rate - INPUTS & RESULTS
# ==========================================
with tab2:
    st.header("ACSM 運動風險評估") 
    st.write("根據 2015 年 ACSM 算法，確定您的詳細運動風險類別。") 
    
    st.subheader("選填：目標心率計算器") 
    age_tab2 = st.number_input("輸入您的年齡（歲）：", min_value=1, max_value=120, value=None, placeholder="例如：30", key="age_input_tab2") 
    rhr_tab2 = st.number_input("輸入您的靜息心率（bpm）：", min_value=30, max_value=120, value=None, placeholder="例如：60", key="rhr_input_tab2") 

    st.markdown("---")
    st.header("Form B: 體徵和症狀") 
    st.write("在過去 12 個月內，您是否經歷過以下任何情況？") 
    
    s_1 = st.checkbox("因心臟缺血而引致的胸口、頸、下顎、上臂或其他部位痛楚或不適", key="s_chest_pain") 
    s_2 = st.checkbox("靜止時或輕微活動時呼吸急促", key="s_short_breath") 
    s_3 = st.checkbox("暈眩或失去知覺", key="s_dizziness") 
    s_4 = st.checkbox("平臥時或晚間不時氣喘", key="s_orthopnea")
    s_5 = st.checkbox("足踝腫", key="s_swelling") 
    s_6 = st.checkbox("心悸或心跳過快", key="s_palpitations") 
    s_7 = st.checkbox("間歇肌肉疼痛、抽筋", key="s_claudications") 
    s_8 = st.checkbox("心雜音", key="s_murmur")
    s_9 = st.checkbox("一般活動感到不尋常的疲倦或氣喘", key="s_fatigue") 
    
    # Score calculation for Form B
    symptoms_list = [s_1, s_2, s_3, s_4, s_5, s_6, s_7, s_8, s_9]
    form_b_score = sum(symptoms_list) # True = 1, False = 0

    st.markdown("---")
    st.header("已知醫療狀況") 
    st.write("您是否有以下任何已知醫療狀況？") 
    
    disease_cardiovascular = st.checkbox("已知心血管疾病 (例如：冠心病、心臟病、中風、心臟衰竭、心律不正)", key="d_cardio") 
    disease_metabolic = st.checkbox("已知代謝疾病 (例如：糖尿病、甲狀腺疾病)", key="d_metabolic") 
    disease_renal = st.checkbox("已知腎臟疾病", key="d_renal") 

    has_disease = any([disease_cardiovascular, disease_metabolic, disease_renal])

    st.markdown("---")
    st.header("當前運動習慣") 
    is_active = st.radio("您目前是否定期進行體能活動？ (過去 3 個月內，每週至少 3 天，每次 30 分鐘中等強度活動)", ("是", "否"), key="is_active_radio") == "是" 

    st.markdown("---")
    if st.button("Calculate Exercise Risk", key="calculate_acsm_button"): 
        
        # Calculate Risk passing the specific scores
        recommendation, risk_level_str = calculate_risk(is_active, has_disease, form_a_score, form_b_score)
        
        st.subheader("Class Stratification for Cardiopulmonary Fitness Training:") 
        if risk_level_str == "low":
            st.success(f"**Class I**\n\n{recommendation}") 
        elif risk_level_str == "moderate":
            st.warning(f"**Class II**\n\n{recommendation}") 
        else: 
            st.error(f"**Class III **\n\n{recommendation}") 

        st.markdown("---")
        
        if age_tab2 is not None and rhr_tab2 is not None:
            st.subheader("Training Heart Rate:") 
            thr_output, thr_error = calculate_thr(age_tab2, rhr_tab2, risk_level_str) 
            
            if thr_error:
                st.error(thr_error)
            else:
                st.markdown(thr_output, unsafe_allow_html=True) # Enabled HTML for underline
            st.markdown("---")
        else:
            st.info("💡 *由於年齡或靜息心率留空，因此未計算目標心率。*") 

# ==========================================
# TAB 3: Direct THR Calculator
# ==========================================
with tab3:
    st.header("目標心率計算器 (直接輸入分類)")
    st.write("如果您已經知道您的 ACSM 運動風險分類，可以直接在此輸入，並計算您的目標心率。")

    selected_class = st.radio(
        "請選擇您的運動風險分類：",
        ["Class I", "Class II", "Class III"],
        horizontal=True,
        key="direct_thr_class_select"
    )

    age_tab3 = st.number_input("輸入您的年齡（歲）：", min_value=1, max_value=120, value=None, placeholder="例如：30", key="age_input_tab3")
    rhr_tab3 = st.number_input("輸入您的靜息心率（bpm）：", min_value=30, max_value=120, value=None, placeholder="例如：60", key="rhr_input_tab3")

    st.markdown("---")

    if st.button("計算目標心率", key="calculate_thr_tab3_button"):
        if age_tab3 is None or rhr_tab3 is None:
            st.error("請輸入年齡和靜息心率以計算目標心率。")
        else:
            # Map selected Class string to risk_level_str used by calculate_thr
            risk_map = {"Class I": "low", "Class II": "moderate", "Class III": "high"}
            risk_level_for_thr = risk_map[selected_class]

            st.subheader(f"根據 {selected_class} 的目標心率：")
            thr_output, thr_error = calculate_thr(age_tab3, rhr_tab3, risk_level_for_thr)

            if thr_error:
                st.error(thr_error)
            else:
                st.markdown(thr_output, unsafe_allow_html=True) # Enabled HTML for underline

# --- Footer (Un-indented, applies to whole page) ---
st.markdown("---")
st.caption("Disclaimer: This tool is for reference purpose and cannot replace professional medical advice. Adjustment to target HR zone should also be made on individual basis.")
