import streamlit as st

# --- MUST BE THE VERY FIRST STREAMLIT COMMAND ---
st.set_page_config(page_title="運動準備度和風險評估", layout="centered") 

# --- Helper Functions (The Logic) ---
def calculate_risk(is_active, has_disease, form_a_score, form_b_score):
    """Calculates exercise risk based strictly on the provided Form A, Form B, and disease/activity rules."""
    
    # Class III Logic:
    # 1. Known disease WITHOUT regular exercise (Form B >= 0)
    # 2. Or if they have ANY signs/symptoms (Form B > 0), they automatically fall into Class III for safety.
    if (has_disease and not is_active) or (form_b_score > 0):
        return "Class III. Seek medical clearance prior to exercise. Following medical clearance, light intensity exercise recommended. Continuous heart rate and RPE monitoring together with close supervision.", "high" 
    
    # Class II Logic:
    # Known disease WITH regular exercise AND Form B = 0
    if has_disease and is_active and form_b_score == 0:
        return "Class II. Continue with moderate intensity exercise. Medical clearance recommended before engaging in vigorous intensity exercise.", "moderate" 
    
    # Also assign to Class II if they failed PAR-Q (Form A > 0) but have no known disease and Form B = 0 
    if not has_disease and form_a_score > 0 and form_b_score == 0:
        return "Class II. You answered 'Yes' to PAR-Q question(s). Following medical clearance, light to moderate intensity exercise recommended.", "moderate"

    # Class I Logic:
    # No known disease AND Form A = 0 AND Form B = 0
    if not has_disease and form_a_score == 0 and form_b_score == 0:
        if not is_active:
            return "Class I. Light to moderate intensity exercise recommended. May gradually progress to vigorous intensity exercise following ACSM guidelines.", "low" 
        else:
            return "Class I. Continue with moderate or vigorous intensity exercise.", "low" 
            
    # Fallback just in case
    return "Class III. Seek medical clearance prior to exercise.", "high"

def calculate_thr(age, rhr, risk_level_str):
    """Calculates Target Heart Rate (THR) range using Karvonen Formula."""
    mhr = 220 - age 
    if rhr >= mhr: 
        return None, "靜息心率不能大於或等於估計最大心率 (220 - 年齡)。請檢查您的輸入。" 

    hrr = mhr - rhr 
    
    if risk_level_str == "low":
        lower_percent, upper_percent = 0.30, 0.84 # Keep upper_percent for calculation consistency
        advice = "**Class I** - Safe Exercise Zone: 30-84%HRR. RPE <17." 
    elif risk_level_str == "moderate":
        lower_percent, upper_percent = 0.30, 0.59
        advice = "**Class II** - Safe Exercise Zone: 30-59%HRR. RPE <14." 
    elif risk_level_str == "high":
        lower_percent, upper_percent = 0.30, 0.39 
        advice = "**Class III** - **Recommend medical clearance prior to exercise.** Safe Exercise Zone: <40% HRR. RPE <12." 
    else:
        return None, "風險等級尚未確定。" 

    lower_bound = int((hrr * lower_percent) + rhr) 
    upper_bound = int((hrr * upper_percent) + rhr)

    # --- MODIFIED THR DISPLAY LOGIC ---
    if risk_level_str == "high":
        thr_zone_display = f"Target Heart Rate **最高 {upper_bound} bpm**." 
    elif risk_level_str == "low": # Display as a range for Class I, with 84% HRR as upper limit
        thr_zone_display = f"Target Heart Rate **{lower_bound} - {upper_bound} bpm**." 
    else: # For Class II
        thr_zone_display = f"Target Heart Rate **{lower_bound} - {upper_bound} bpm**." 

    output = f"Maximum Heart Rate= **{mhr} bpm**.\n" \
             f"Resting Heart Rate= **{rhr} bpm**.\n" \
             f"Heart Rate Reserve= **{hrr} bpm**.\n\n" \
             f"{thr_zone_display}\n\n" \
             f"{advice}"
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

# Create three tabs for the three different questionnaires
tab1, tab2, tab3 = st.tabs(["1.體能活動適應力問卷（PAR-Q）", "2.ACSM運動風險評估", "3.目標心率計算器"]) 

# ==========================================
# TAB 1: PAR-Q (FORM A)
# ==========================================
with tab1:
    st.header("Form A: 體能活動準備問卷 (PAR-Q)") 
    st.write("請回答以下 7 個一般健康問題：") 
    
    q1 = st.radio("1. 醫生是否曾說過您有心臟疾病，並且只能在醫生建議下進行體能活動？", ("否", "是"), horizontal=True, key="parq_q1")
    q2 = st.radio("2. 當您進行體能活動時，胸部會感到疼痛嗎？", ("否", "是"), horizontal=True, key="parq_q2")
    q3 = st.radio("3. 在過去一個月內，當您沒有進行體能活動時，是否曾感到胸痛？", ("否", "是"), horizontal=True, key="parq_q3")
    q4 = st.radio("4. 您是否會因頭暈而失去平衡，或者曾經失去知覺？", ("否", "是"), horizontal=True, key="parq_q4")
    q5 = st.radio("5. 你的骨骼或關節（例如脊骨、膝蓋或髖關節）是否有毛病，且會因改變體能活動而惡化？", ("否", "是"), horizontal=True, key="parq_q5")
    q6 = st.radio("6. 您的醫生目前是否正在為您的血壓或心臟疾病開處方藥物（例如利尿劑）？", ("否", "是"), horizontal=True, key="parq_q6")
    q7 = st.radio("7. 您是否知道有任何其他原因導致您不應該進行體能活動？", ("否", "是"), horizontal=True, key="parq_q7")

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
# TAB 2: ACSM & Heart Rate - INPUTS (FORM B & Disease)
# ==========================================
with tab2:
    st.header("ACSM 運動風險評估") 
    st.write("根據 2015 年 ACSM 算法，確定您的詳細運動風險類別。") 
    
    st.subheader("選填：目標心率計算器") 
    # Unique keys for age and RHR inputs in Tab 2
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
    
    disease_cardiovascular = st.checkbox("已知心血管疾病 (例如：冠心病、心臟病發作、中風、心臟衰竭)", key="d_cardio") 
    disease_metabolic = st.checkbox("已知代謝疾病 (例如：糖尿病、甲狀腺疾病)", key="d_metabolic") 
    disease_renal = st.checkbox("已知腎臟（腎）疾病", key="d_renal") 

    has_disease = any([disease_cardiovascular, disease_metabolic, disease_renal])

    st.markdown("---")
    st.header("當前運動習慣") 
    is_active = st.radio("您目前是否定期進行體能活動？ (過去 3 個月內，每週至少 3 天，每次 30 分鐘中等強度活動)", ("是", "否"), key="is_active_radio") == "是" 
# ==========================================
# TAB 2: ACSM & Heart Rate - RESULTS
# ==========================================
    st.markdown("---")
    if st.button("Calculate Exercise Risk", key="calculate_acsm_button"): 
        
        # Calculate Risk passing the specific scores (from Form A in tab1, and Form B/disease from tab2)
        recommendation, risk_level_str = calculate_risk(is_active, has_disease, form_a_score, form_b_score)
        
        st.subheader("Class Stratification for Cardiopulmonary Fitness Training:") 
        if risk_level_str == "low":
            st.success(f"**Class I**\n\n{recommendation}") 
        elif risk_level_str == "moderate":
            st.warning(f"**Class II**\n\n{recommendation}") 
        else: 
            st.error(f"**Class III **\n\n{recommendation}") 

        st.markdown("---")
        
        # Only show THR if age and rhr are filled out in Tab 2's optional inputs
        if age_tab2 is not None and rhr_tab2 is not None: # Use tab2's age/rhr here
            st.subheader("Training Heart Rate:") 
            thr_output, thr_error = calculate_thr(age_tab2, rhr_tab2, risk_level_str) 
            
            if thr_error:
                st.error(thr_error)
            else:
                st.markdown(thr_output)
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
                st.markdown(thr_output)


# --- Footer (Un-indented, applies to whole page) ---
st.markdown("---")
st.caption("Disclaimer: This tool is for reference purpose and cannot replace professional medical advice. Adjustment to target HR zone should also be made on individual basis.")
