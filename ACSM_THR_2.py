import streamlit as st


# --- Helper Functions (The Logic) ---
def calculate_risk(is_active, has_disease, has_symptoms):
    """Calculates exercise risk based on 2015 ACSM Algorithm."""
    if not is_active:
        if has_symptoms:
            return "High Risk: Medical clearance recommended before starting any exercise.", "high"
        elif has_disease:
            return "Moderate Risk: Medical clearance recommended before starting exercise. Following clearance, start with light-to-moderate intensity.", "moderate"
        else:
            return "Low Risk: Medical clearance not necessary. You can start with light-to-moderate intensity exercise.", "low"
    else:
        if has_symptoms:
            return "High Risk: Discontinue exercise and seek medical clearance before resuming.", "high"
        elif has_disease:
            return "Moderate Risk: Medical clearance not necessary for moderate intensity, but recommended before engaging in vigorous intensity exercise.", "moderate"
        else:
            return "Low Risk: Medical clearance not necessary. You can continue moderate or vigorous intensity exercise.", "low"


def calculate_thr(age, rhr, risk_level_str):
    """Calculates Target Heart Rate (THR) range using Karvonen Formula."""
    mhr = 220 - age
    if rhr >= mhr:
        return None, "Resting Heart Rate cannot be greater than or equal to estimated Maximum Heart Rate (220 - age)."

    hrr = mhr - rhr

    # Set intensity percentages based on risk level (as % of HRR)
    if risk_level_str == "low":
        lower_percent, upper_percent = 0.50, 0.85
        advice = "對於**低風險**人士，中等至高強度範圍通常是合適的。請從較低強度開始，逐步增加。"  # Translated
    elif risk_level_str == "moderate":
        lower_percent, upper_percent = 0.40, 0.60
        advice = "對於**中等風險**人士，建議從輕度到中等強度開始，尤其是在初期或未經醫生批准進行劇烈運動之前。"  # Translated
    elif risk_level_str == "high":
        # Adjusted: upper limit now 39% HRR to be strictly "less than 40% HRR".
        # Lower percent is included for calculation consistency but not displayed as a lower bound.
        lower_percent, upper_percent = 0.30, 0.39
        advice = "對於**高風險**人士，**任何運動都必須在徹底的醫療許可後才能進行**。如果獲得許可，建議將運動強度保持在最高心率限制以下，進行非常輕度到輕度的運動（低於 40% HRR）。"  # Translated and adjusted advice
    else:
        return None, "風險等級尚未確定。"  # Translated

    # Apply Karvonen Formula
    lower_bound = int((hrr * lower_percent) + rhr)  # Calculated, but not always displayed as a range
    upper_bound = int((hrr * upper_percent) + rhr)

    # Conditional output string for high risk (emphasizing max, not a range)
    if risk_level_str == "high":
        thr_zone_display = f"您的建議目標心率 (THR) 應為 **最高 {upper_bound} bpm**。"
    else:
        thr_zone_display = f"建議的目標心率 (THR) 區間為 **{lower_bound} - {upper_bound} bpm**。"

    output = f"您的估計最大心率 (MHR) 為 **{mhr} bpm**。\n" \
             f"您的靜息心率 (RHR) 為 **{rhr} bpm**。\n" \
             f"您的心率儲備 (HRR) 為 **{hrr} bpm**。\n\n" \
             f"{thr_zone_display}\n\n" \
             f"{advice}"
    return output, None


# --- Streamlit App Layout ---
st.set_page_config(page_title="運動準備度和風險評估", layout="centered")

st.title("🏃‍♂️ 運動準備度和風險評估")
st.write("請填寫以下問卷以評估您的體能活動準備度。")

# Create two tabs for the two different questionnaires
tab1, tab2 = st.tabs(["1. PAR-Q 評估", "2. ACSM 風險與心率"])

# ==========================================
# TAB 1: PAR-Q
# ==========================================
with tab1:
    st.header("體能活動準備問卷 (PAR-Q)")
    st.write("請回答以下 7 個一般健康問題：")

    q1 = st.radio("1. 醫生是否曾說過您有心臟疾病，並且只能在醫生建議下進行體能活動？", ("否", "是"), horizontal=True,
                  key="parq_q1")
    q2 = st.radio("2. 當您進行體能活動時，胸部會感到疼痛嗎？", ("否", "是"), horizontal=True, key="parq_q2")
    q3 = st.radio("3. 在過去一個月內，當您沒有進行體能活動時，是否曾感到胸痛？", ("否", "是"), horizontal=True,
                  key="parq_q3")
    q4 = st.radio("4. 您是否會因頭暈而失去平衡，或者曾經失去知覺？", ("否", "是"), horizontal=True, key="parq_q4")
    q5 = st.radio("5. 你的骨骼或關節（例如脊骨、膝蓋或髖關節）是否有毛病，且會因改變體能活動而惡化？", ("否", "是"),
                  horizontal=True, key="parq_q5")
    q6 = st.radio("6. 您的醫生目前是否正在為您的血壓或心臟疾病開處方藥物（例如利尿劑）？", ("否", "是"), horizontal=True,
                  key="parq_q6")
    q7 = st.radio("7. 您是否知道有任何其他原因導致您不應該進行體能活動？", ("否", "是"), horizontal=True, key="parq_q7")

    st.markdown("---")
    if st.button("評估 PAR-Q", key="evaluate_parq_button"):
        answers = [q1, q2, q3, q4, q5, q6, q7]
        if "是" in answers:
            st.error(
                "🛑 **停止：需要醫療許可。**\n\n因為您回答了一個或多個問題為「是」，在開始大幅增加體能活動或進行體能評估之前，您應該諮詢您的醫生。")
        else:
            st.success(
                "✅ **已獲准運動。**\n\n因為您回答所有問題為「否」，您可以合理地確定開始增加體能活動是安全的。請慢慢開始，逐步增加。")
            st.info("👉 *現在，請前往第二個分頁 (ACSM 風險與心率) 進行更詳細的風險分層。*")
# ==========================================
# TAB 2: ACSM & Heart Rate - INPUTS
# ==========================================
with tab2:
    st.header("ACSM 運動風險評估")
    st.write("根據 2015 年 ACSM 算法，確定您的詳細運動風險類別。")

    st.subheader("選填：目標心率計算器")
    age = st.number_input("輸入您的年齡（歲）：", min_value=1, max_value=120, value=None, placeholder="例如：30",
                          key="age_input")
    rhr = st.number_input("輸入您的靜息心率（bpm）：", min_value=30, max_value=120, value=None, placeholder="例如：60",
                          key="rhr_input")

    st.markdown("---")
    st.header("1. 體徵和症狀")
    st.write("在過去 12 個月內，您是否經歷過以下任何情況？")
    col1, col2 = st.columns(2)
    with col1:
        symptom_chest_pain = st.checkbox("因心臟缺血而引致的胸口、頸、下顎、上臂或其他部位痛楚或不適", key="s_chest_pain")
        symptom_shortness_breath = st.checkbox("靜止時或輕微活動時呼吸急促", key="s_short_breath")
        symptom_dizziness = st.checkbox("頭暈或頭昏眼花", key="s_dizziness")
    with col2:
        symptom_fatigue = st.checkbox("異常疲勞", key="s_fatigue")
        symptom_palpitations = st.checkbox("心悸（心跳不規律）", key="s_palpitations")
        symptom_swelling = st.checkbox("腿部、腳踝或足部腫脹", key="s_swelling")

    has_symptoms = any(
        [symptom_chest_pain, symptom_shortness_breath, symptom_dizziness, symptom_fatigue, symptom_palpitations,
         symptom_swelling])

    st.markdown("---")
    st.header("2. 已知醫療狀況")
    st.write("您是否有以下任何已知醫療狀況？")
    col3, col4 = st.columns(2)
    with col3:
        disease_cardiovascular = st.checkbox("已知心血管疾病 (例如：心臟病發作、中風)", key="d_cardio")
        disease_metabolic = st.checkbox("已知代謝疾病 (例如：糖尿病、甲狀腺疾病)", key="d_metabolic")
    with col4:
        disease_renal = st.checkbox("已知腎臟（腎）疾病", key="d_renal")

    has_disease = any([disease_cardiovascular, disease_metabolic, disease_renal])

    st.markdown("---")
    st.header("3. 當前運動習慣")
    is_active = st.radio("您目前是否定期進行體能活動？ (過去 3 個月內，每週至少 3 天，每次 30 分鐘中等強度活動)",
                         ("是", "否"), key="is_active_radio") == "是"
    # ==========================================
    # TAB 2: ACSM & Heart Rate - RESULTS
    # ==========================================
    st.markdown("---")
    if st.button("計算 ACSM 風險", key="calculate_acsm_button"):

        # 1. Show ACSM Risk Level
        recommendation, risk_level_str = calculate_risk(is_active, has_disease, has_symptoms)
        st.subheader("您的運動風險評估：")
        if risk_level_str == "low":
            st.success(f"**風險類別：低風險**\n\n{recommendation}")
        elif risk_level_str == "moderate":
            st.warning(f"**風險類別：中等風險**\n\n{recommendation}")
        else:
            st.error(f"**風險類別：高風險**\n\n{recommendation}")

        st.markdown("---")

        # 2. Show Target Heart Rate (Only if age and rhr are filled out)
        if age is not None and rhr is not None:
            st.subheader("目標心率區間估計：")
            thr_output, thr_error = calculate_thr(age, rhr, risk_level_str)

            if thr_error:
                st.error(thr_error)
            else:
                st.markdown(thr_output)
            st.markdown("---")
        else:
            st.info("💡 *由於年齡或靜息心率留空，因此未計算目標心率。*")

        # This is completely un-indented, so it shows up at the bottom of the whole page, outside the tabs.
st.markdown("---")
st.caption("免責聲明：此工具僅供參考，不能替代專業醫療建議。")
