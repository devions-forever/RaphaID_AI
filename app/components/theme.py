"""
Clinical Theme — Flat Dark Theme for RaphaID AI
Single accent teal (#64FFDA), safety red (#F87171) for errors/alerts only.
Strictly zero gradients. Medical PACS/workstation density and precision.
"""

import streamlit as st


def get_theme_colors() -> dict:
    """Return the clinical color palette — flat navy + single teal accent."""
    return {
        # Background (locked)
        "bg_primary": "#0A0F1D",
        "bg_secondary": "#0D1528",
        "bg_card": "#111A2E",
        "bg_hover": "#16213E",
        # Text
        "text_primary": "#E8EDF3",
        "text_secondary": "#8A94A6",
        "text_muted": "#5C6779",
        "text_accent": "#64FFDA",
        # Accents — single teal + safety red only
        "accent_teal": "#64FFDA",
        "accent_emerald": "#64FFDA",
        "accent_red": "#F87171",
        "accent_orange": "#64FFDA",
        "accent_yellow": "#64FFDA",
        "accent_purple": "#8A94A6",
        # Borders
        "border_subtle": "#1F2D44",
        "border_accent": "#64FFDA",
        # Status
        "success": "#64FFDA",
        "warning": "#8A94A6",
        "error": "#F87171",
        "info": "#64FFDA",
    }


def apply_theme() -> None:
    """Apply the clinical dark theme via unified CSS injection."""
    colors = get_theme_colors()

    css = f"""
    <style>
    /* ============================================================
       GLOBAL CLINICAL DARK THEME
    ============================================================ */
    html, body, [data-testid="stAppViewContainer"],
    [data-testid="stHeader"], [data-testid="stToolbar"],
    .main, .block-container {{
        background-color: {colors["bg_primary"]} !important;
        color: {colors["text_primary"]} !important;
    }}

    [data-testid="stSidebar"] {{
        background-color: {colors["bg_primary"]} !important;
        border-right: 1px solid {colors["border_subtle"]} !important;
    }}

    [data-testid="stSidebar"] > div {{
        background-color: {colors["bg_primary"]} !important;
    }}

    [data-testid="stSidebar"] .block-container {{
        padding-top: 1.2rem !important;
        padding-bottom: 2rem !important;
    }}

    [data-testid="stSidebar"] [data-testid="stVerticalBlock"] {{
        row-gap: 0.35rem !important;
    }}

    /* Force all headings to crisp clinical white */
    h1, h2, h3, h4, h5, h6 {{
        color: #FFFFFF !important;
        font-weight: 700 !important;
        letter-spacing: -0.01em !important;
    }}

    .main .block-container h2 {{
        margin-top: 1.4rem;
        margin-bottom: 0.6rem;
    }}
    .main .block-container h3 {{
        margin-top: 1.2rem;
        margin-bottom: 0.5rem;
    }}
    .main .block-container h2:first-child,
    .main .block-container h3:first-child {{
        margin-top: 0.2rem;
    }}

    /* Keep Streamlit-native text readable */
    [data-testid="stAppViewContainer"] p,
    [data-testid="stAppViewContainer"] label,
    .block-container p {{
        color: {colors["text_primary"]};
    }}

    /* Input fields */
    .stTextInput input, .stNumberInput input, .stTextArea textarea,
    .stSelectbox > div > div {{
        background-color: {colors["bg_card"]} !important;
        color: {colors["text_primary"]} !important;
        border: 1px solid {colors["border_subtle"]} !important;
        border-radius: 8px !important;
    }}

    .stTextInput input:focus, .stNumberInput input:focus, .stTextArea textarea:focus {{
        border-color: {colors["accent_teal"]} !important;
        box-shadow: 0 0 0 1px {colors["accent_teal"]} !important;
    }}

    /* Selectbox dropdown */
    [data-baseweb="select"] > div {{
        background-color: {colors["bg_card"]} !important;
        color: {colors["text_primary"]} !important;
        border-color: {colors["border_subtle"]} !important;
    }}

    [data-baseweb="popover"], [role="listbox"] {{
        background-color: {colors["bg_card"]} !important;
        border: 1px solid {colors["border_subtle"]} !important;
    }}

    [role="option"] {{
        background-color: {colors["bg_card"]} !important;
        color: {colors["text_primary"]} !important;
    }}

    [role="option"]:hover {{
        background-color: {colors["bg_hover"]} !important;
        color: {colors["accent_teal"]} !important;
    }}

    /* File uploader */
    [data-testid="stFileUploader"] {{
        background-color: rgba(255, 255, 255, 0.02) !important;
        color: {colors["text_primary"]} !important;
    }}

    [data-testid="stFileUploaderDropzone"] {{
        background-color: {colors["bg_card"]} !important;
        border: 1px dashed {colors["border_subtle"]} !important;
        border-radius: 10px !important;
    }}

    [data-testid="stFileUploaderDropzone"]:hover {{
        border-color: {colors["accent_teal"]} !important;
    }}

    /* Expanders */
    [data-testid="stExpander"] {{
        background-color: {colors["bg_card"]} !important;
        border: 1px solid {colors["border_subtle"]} !important;
        border-radius: 10px !important;
        margin-bottom: 0.75rem !important;
    }}

    [data-testid="stExpander"] summary {{
        color: {colors["text_secondary"]} !important;
        background-color: transparent !important;
        font-weight: 600 !important;
    }}

    /* Native Alerts */
    [data-testid="stInfo"] {{
        background-color: rgba(100, 255, 218, 0.06) !important;
        border-left: 3px solid {colors["accent_teal"]} !important;
        border-radius: 0 8px 8px 0 !important;
        color: {colors["text_primary"]} !important;
    }}

    [data-testid="stWarning"] {{
        background-color: rgba(138, 148, 166, 0.08) !important;
        border-left: 3px solid {colors["warning"]} !important;
        border-radius: 0 8px 8px 0 !important;
        color: {colors["text_primary"]} !important;
    }}

    [data-testid="stError"] {{
        background-color: rgba(248, 113, 113, 0.08) !important;
        border-left: 3px solid {colors["error"]} !important;
        border-radius: 0 8px 8px 0 !important;
        color: {colors["text_primary"]} !important;
    }}

    [data-testid="stSuccess"] {{
        background-color: rgba(100, 255, 218, 0.06) !important;
        border-left: 3px solid {colors["accent_teal"]} !important;
        border-radius: 0 8px 8px 0 !important;
        color: {colors["text_primary"]} !important;
    }}

    /* ============================================================
       BUTTONS — FLAT MEDICAL PALETTE (NO RED GRADIENTS)
    ============================================================ */
    .stButton > button {{
        background-color: {colors["bg_card"]} !important;
        background-image: none !important;
        color: {colors["text_primary"]} !important;
        -webkit-text-fill-color: {colors["text_primary"]} !important;
        border: 1px solid {colors["border_subtle"]} !important;
        border-radius: 8px !important;
        padding: 0.6rem 1.4rem !important;
        font-weight: 600 !important;
        font-size: 0.92rem !important;
        letter-spacing: 0.01em !important;
        transition: border-color 0.2s ease, background-color 0.2s ease, color 0.2s ease !important;
        box-shadow: none !important;
    }}

    .stButton > button:hover {{
        background-color: {colors["bg_hover"]} !important;
        border-color: {colors["accent_teal"]} !important;
        color: {colors["accent_teal"]} !important;
        -webkit-text-fill-color: {colors["accent_teal"]} !important;
        transform: none !important;
        box-shadow: none !important;
    }}

    /* Primary CTA buttons — Solid Clinical Teal */
    .stButton > button[kind="primary"],
    .stButton > button[data-testid="baseButton-primary"],
    section.main div[data-testid="stButton"] > button[kind="primary"],
    section.main div[data-testid="stButton"] > button[data-testid="baseButton-primary"] {{
        background-color: {colors["accent_teal"]} !important;
        background-image: none !important;
        color: {colors["bg_primary"]} !important;
        -webkit-text-fill-color: {colors["bg_primary"]} !important;
        border: 1px solid {colors["accent_teal"]} !important;
        border-radius: 8px !important;
        padding: 0.65rem 1.6rem !important;
        font-weight: 700 !important;
        font-size: 0.95rem !important;
        box-shadow: none !important;
        transition: background-color 0.2s ease, opacity 0.2s ease !important;
    }}

    .stButton > button[kind="primary"]:hover,
    .stButton > button[data-testid="baseButton-primary"]:hover,
    section.main div[data-testid="stButton"] > button[kind="primary"]:hover,
    section.main div[data-testid="stButton"] > button[data-testid="baseButton-primary"]:hover {{
        background-color: #52e0be !important;
        border-color: #52e0be !important;
        color: {colors["bg_primary"]} !important;
        -webkit-text-fill-color: {colors["bg_primary"]} !important;
        box-shadow: 0 2px 8px rgba(100, 255, 218, 0.2) !important;
        transform: none !important;
    }}

    /* Disabled buttons */
    .stButton > button:disabled,
    .stButton > button[disabled] {{
        background-color: {colors["bg_secondary"]} !important;
        color: {colors["text_muted"]} !important;
        -webkit-text-fill-color: {colors["text_muted"]} !important;
        border-color: {colors["border_subtle"]} !important;
        cursor: not-allowed !important;
        box-shadow: none !important;
    }}

    /* Sidebar Navigation buttons */
    [data-testid="stSidebar"] div[data-testid="stButton"] > button {{
        background-color: {colors["bg_card"]} !important;
        background-image: none !important;
        color: {colors["text_secondary"]} !important;
        -webkit-text-fill-color: {colors["text_secondary"]} !important;
        border: 1px solid {colors["border_subtle"]} !important;
        border-radius: 8px !important;
        padding: 0.55rem 0.85rem !important;
        font-weight: 600 !important;
        font-size: 0.88rem !important;
        text-align: left !important;
        justify-content: flex-start !important;
        box-shadow: none !important;
        width: 100% !important;
        margin-bottom: 0.35rem !important;
    }}

    [data-testid="stSidebar"] div[data-testid="stButton"] > button:hover {{
        border-color: {colors["accent_teal"]} !important;
        color: {colors["accent_teal"]} !important;
        -webkit-text-fill-color: {colors["accent_teal"]} !important;
        background-color: {colors["bg_hover"]} !important;
    }}

    [data-testid="stSidebar"] div[data-testid="stButton"] > button[kind="primary"],
    [data-testid="stSidebar"] div[data-testid="stButton"] > button[data-testid="baseButton-primary"] {{
        background-color: rgba(100, 255, 218, 0.12) !important;
        background-image: none !important;
        color: {colors["accent_teal"]} !important;
        -webkit-text-fill-color: {colors["accent_teal"]} !important;
        border: 1px solid {colors["accent_teal"]} !important;
        font-weight: 700 !important;
    }}

    /* ============================================================
       SHARED CLINICAL SURFACES (CARDS, BADGES, STEPPERS)
    ============================================================ */
    .rh-hero {{
        background: {colors["bg_card"]};
        border: 1px solid {colors["border_subtle"]};
        border-radius: 12px;
        padding: 1.3rem 1.8rem;
        margin-bottom: 1.2rem;
        text-align: center;
    }}

    .rh-card {{
        background: {colors["bg_card"]};
        border: 1px solid {colors["border_subtle"]};
        border-radius: 10px;
        padding: 1.1rem;
        margin-bottom: 0.75rem;
        transition: border-color 0.2s ease;
    }}

    .rh-card:hover {{
        border-color: rgba(100, 255, 218, 0.3);
    }}

    .rh-badge {{
        display: inline-block;
        border: 1px solid {colors["border_subtle"]};
        background: rgba(255, 255, 255, 0.02);
        border-radius: 999px;
        padding: 3px 10px;
        font-size: 0.72rem;
        color: {colors["text_secondary"]};
        margin: 0 4px 4px 0;
        letter-spacing: 0.04em;
    }}

    .rh-stepper {{
        background: {colors["bg_card"]};
        border: 1px solid {colors["border_subtle"]};
        border-radius: 10px;
        padding: 0.75rem 1rem;
        display: flex;
        flex-wrap: wrap;
        gap: 0.5rem;
        justify-content: space-between;
        align-items: center;
        margin-bottom: 1rem;
    }}

    .rh-step {{
        flex: 1;
        min-width: 105px;
        text-align: center;
        font-size: 0.8rem;
        color: {colors["text_secondary"]};
    }}

    .rh-empty {{
        background: {colors["bg_card"]};
        border: 1px solid {colors["border_subtle"]};
        border-radius: 12px;
        padding: 2.5rem 1.5rem;
        text-align: center;
        color: {colors["text_secondary"]};
        margin-bottom: 1rem;
    }}

    .rh-pending {{
        background: {colors["bg_card"]};
        border: 1px solid {colors["border_subtle"]};
        border-left: 3px solid {colors["accent_teal"]};
        border-radius: 0 10px 10px 0;
        padding: 1rem 1.2rem;
        margin: 1rem 0;
    }}

    /* Metrics */
    [data-testid="stMetric"], .metric-card {{
        background: {colors["bg_card"]} !important;
        border: 1px solid {colors["border_subtle"]} !important;
        border-radius: 10px !important;
        padding: 0.9rem 1rem !important;
        text-align: center !important;
        margin-bottom: 0.75rem !important;
    }}

    [data-testid="stMetric"] [data-testid="stMetricValue"], .metric-value {{
        color: {colors["accent_teal"]} !important;
        font-size: 1.8rem !important;
        font-weight: 800 !important;
        letter-spacing: -0.02em !important;
        line-height: 1.1 !important;
    }}

    [data-testid="stMetric"] [data-testid="stMetricLabel"], .metric-label {{
        color: {colors["text_secondary"]} !important;
        text-transform: uppercase !important;
        font-size: 0.72rem !important;
        letter-spacing: 0.06em !important;
        margin-top: 0.35rem !important;
    }}

    /* Detection table */
    .detection-table {{
        width: 100%;
        border-collapse: collapse;
        border-radius: 8px;
        overflow: hidden;
        border: 1px solid {colors["border_subtle"]};
        margin-bottom: 1rem;
    }}

    .detection-table th {{
        background: {colors["bg_secondary"]};
        color: {colors["accent_teal"]};
        padding: 0.65rem 1rem;
        font-size: 0.8rem;
        text-transform: uppercase;
        letter-spacing: 0.06em;
        font-weight: 700;
        border-bottom: 1px solid {colors["border_subtle"]};
    }}

    .detection-table td {{
        padding: 0.6rem 1rem;
        border-bottom: 1px solid {colors["border_subtle"]};
        color: {colors["text_primary"]};
        font-size: 0.88rem;
        background: {colors["bg_card"]};
    }}

    .detection-table tr:last-child td {{
        border-bottom: none;
    }}

    .detection-table tr:hover td {{
        background: {colors["bg_hover"]};
    }}

    .footer-credit {{
        text-align: center;
        color: {colors["text_muted"]};
        font-size: 0.76rem;
        padding: 1.5rem 0 1rem;
        border-top: 1px solid {colors["border_subtle"]};
        margin-top: 2rem;
        letter-spacing: 0.03em;
        line-height: 1.6;
    }}

    /* Dividers */
    hr {{
        border: none !important;
        border-top: 1px solid {colors["border_subtle"]} !important;
        margin: 1.2rem 0 !important;
    }}

    /* Scrollbars */
    ::-webkit-scrollbar {{
        width: 6px;
        height: 6px;
    }}
    ::-webkit-scrollbar-track {{
        background: {colors["bg_primary"]};
    }}
    ::-webkit-scrollbar-thumb {{
        background: {colors["border_subtle"]};
        border-radius: 3px;
    }}
    ::-webkit-scrollbar-thumb:hover {{
        background: {colors["accent_teal"]};
    }}
    </style>
    """

    st.markdown(css, unsafe_allow_html=True)

    try:
        st.config.set_option("theme.base", "dark")
        st.config.set_option("theme.primaryColor", colors["accent_teal"])
        st.config.set_option("theme.backgroundColor", colors["bg_primary"])
        st.config.set_option("theme.secondaryBackgroundColor", colors["bg_card"])
        st.config.set_option("theme.textColor", colors["text_primary"])
    except Exception:
        pass