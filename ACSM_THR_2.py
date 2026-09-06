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
        [data-testid="stSidebar"] p, [data-testid="stSidebar"] div, [data-testid="stSidebar"] span
