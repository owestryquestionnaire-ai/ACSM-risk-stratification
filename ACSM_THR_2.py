import streamlit as st

# ---------- 1. Initialization & Config ----------
# 設定 layout="wide" 以使用全螢幕寬度，並將網頁標籤改為英文
st.set_page_config(page_title="Risk Stratification of Cardiopulmonary Fitness Training", layout="wide")

def inject_custom_css():
    # 移除所有強制文字顏色 (color)，讓 Streamlit 原生系統自動完美處理深色/淺色模式的文字轉換！
    st.markdown(
        """
        <style>
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
        .stRadio > div { gap: 0rem !important; } 
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

        /* Combined Result Box Styling */
        .final-result-box { border: 3px solid var(--text-color); border-radius: 10px; overflow: hidden; box-shadow: 2px 2px 10px rgba(0,0,0,0.1); margin-bottom: 15px !important; }
        .final-thr-part { font-size: 36px !important; font-weight: bold !important; line-height: 1.45 !important; padding: 15px 20px !important; background-color: var(--background-color); }
        .final-rec-part { background-color: var(--secondary-background-color); padding: 15px 20px !important; border-top: 3px dashed var(--text-color); }
        .final-rec-part p { margin-bottom: 6px !important; line-height: 1.45 !important; }
        
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
            
            .final-thr-part { font-size: 28px !important; padding: 12px 15px !important; }
            .final-rec-part { padding: 12px 15px !important; }
        }
        </style>
        """,
        unsafe_allow_html=True
    )

def init_session_states():
    if "data" not in st.session_state:
        st.session_state.data = {}
        for i in range(1, 10):
