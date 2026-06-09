"""
styles.py
Semua CSS global untuk SmartBudget AI — design system terpusat.
"""

GLOBAL_CSS = """
<style>
/* ═══════════════════════════════════════════════════
   FONTS & BASE
═══════════════════════════════════════════════════ */
@import url('https://fonts.googleapis.com/css2?family=DM+Sans:ital,opsz,wght@0,9..40,400;0,9..40,500;0,9..40,600;0,9..40,700;1,9..40,400&family=DM+Mono:wght@400;500&display=swap');

html, body, [class*="css"] {
    font-family: 'DM Sans', -apple-system, BlinkMacSystemFont, sans-serif !important;
}

/* ═══════════════════════════════════════════════════
   COLOR TOKENS
═══════════════════════════════════════════════════ */
:root {
    --navy-950:  #060d1c;
    --navy-900:  #0a1628;
    --navy-800:  #0d1f38;
    --navy-700:  #0f2d4f;
    --blue-600:  #0f4c81;
    --blue-500:  #1e6ab3;
    --blue-400:  #3b82f6;
    --blue-100:  #dbeafe;
    --blue-50:   #eff6ff;
    --green-500: #22c55e;
    --green-400: #4ade80;
    --green-100: #dcfce7;
    --red-500:   #ef4444;
    --red-100:   #fee2e2;
    --amber-500: #f59e0b;
    --amber-100: #fef3c7;
    --slate-700: #334155;
    --slate-500: #64748b;
    --slate-300: #cbd5e1;
    --slate-200: #e2e8f0;
    --slate-100: #f1f5f9;
    --slate-50:  #f8fafc;
    --white:     #ffffff;
    --radius-sm: 6px;
    --radius-md: 10px;
    --radius-lg: 14px;
    --shadow-sm: 0 1px 3px rgba(0,0,0,0.06), 0 1px 2px rgba(0,0,0,0.04);
    --shadow-md: 0 4px 12px rgba(0,0,0,0.08), 0 2px 4px rgba(0,0,0,0.04);
}

/* ═══════════════════════════════════════════════════
   HIDE STREAMLIT DEFAULTS
═══════════════════════════════════════════════════ */
#MainMenu {visibility: hidden;}
footer {visibility: hidden;}
.stDeployButton {display: none;}
header[data-testid="stHeader"] {background: transparent;}

/* ═══════════════════════════════════════════════════
   PAGE BACKGROUND
═══════════════════════════════════════════════════ */
.stApp {
    background: var(--slate-50) !important;
}
.stApp > header {background: transparent !important;}
[data-testid="stAppViewContainer"] > .main {
    background: var(--slate-50) !important;
}
[data-testid="stAppViewContainer"] {
    background: var(--slate-50) !important;
}

/* ═══════════════════════════════════════════════════
   SIDEBAR
═══════════════════════════════════════════════════ */
[data-testid="stSidebar"] {
    background: var(--navy-900) !important;
    border-right: none !important;
}
[data-testid="stSidebar"] * {color: rgba(255,255,255,0.75) !important;}
[data-testid="stSidebar"] h1,
[data-testid="stSidebar"] h2,
[data-testid="stSidebar"] h3 {
    color: #ffffff !important;
}
[data-testid="stSidebar"] [data-testid="stMarkdownContainer"] a {
    color: var(--blue-400) !important;
}
[data-testid="stSidebar"] hr {
    border-color: rgba(255,255,255,0.1) !important;
    margin: 12px 0 !important;
}
[data-testid="stSidebarNav"] {display: none !important;}

/* ═══════════════════════════════════════════════════
   METRIC CARDS
═══════════════════════════════════════════════════ */
[data-testid="metric-container"] {
    background: var(--white) !important;
    border: 1px solid var(--slate-200) !important;
    border-radius: var(--radius-md) !important;
    padding: 1.1rem 1.2rem !important;
    box-shadow: var(--shadow-sm) !important;
    transition: box-shadow 0.2s, transform 0.2s;
}
[data-testid="metric-container"]:hover {
    box-shadow: var(--shadow-md) !important;
    transform: translateY(-1px);
}
[data-testid="stMetricLabel"] {
    font-size: 0.75rem !important;
    font-weight: 500 !important;
    color: var(--slate-500) !important;
    text-transform: uppercase !important;
    letter-spacing: 0.04em !important;
}
[data-testid="stMetricValue"] {
    font-size: 1.5rem !important;
    font-weight: 700 !important;
    color: var(--navy-900) !important;
}
[data-testid="stMetricDelta"] {font-size: 0.75rem !important;}

/* ═══════════════════════════════════════════════════
   BUTTONS
═══════════════════════════════════════════════════ */
.stButton > button {
    border-radius: var(--radius-sm) !important;
    font-weight: 600 !important;
    font-size: 0.875rem !important;
    letter-spacing: 0.01em !important;
    transition: all 0.15s !important;
    border: 1px solid var(--slate-300) !important;
}
.stButton > button:hover {
    transform: translateY(-1px) !important;
    box-shadow: var(--shadow-sm) !important;
}
.stButton > button[kind="primary"] {
    background: var(--blue-600) !important;
    border-color: var(--blue-600) !important;
    color: var(--white) !important;
}
.stButton > button[kind="primary"]:hover {
    background: var(--blue-500) !important;
    border-color: var(--blue-500) !important;
}

/* ═══════════════════════════════════════════════════
   FORM INPUTS
═══════════════════════════════════════════════════ */
.stTextInput > div > div > input,
.stNumberInput > div > div > input,
.stDateInput > div > div > input,
.stSelectbox > div > div,
.stTextArea textarea {
    border-radius: var(--radius-sm) !important;
    border: 1px solid var(--slate-300) !important;
    background: var(--white) !important;
    font-family: 'DM Sans', sans-serif !important;
    font-size: 0.9rem !important;
    transition: border-color 0.15s, box-shadow 0.15s !important;
}
.stTextInput > div > div > input:focus,
.stNumberInput > div > div > input:focus,
.stTextArea textarea:focus {
    border-color: var(--blue-500) !important;
    box-shadow: 0 0 0 3px rgba(30,106,179,0.12) !important;
    outline: none !important;
}

/* ═══════════════════════════════════════════════════
   SELECTBOX & RADIO
═══════════════════════════════════════════════════ */
.stRadio > div {
    gap: 8px !important;
    flex-direction: row !important;
}
.stRadio label {
    background: var(--slate-100) !important;
    border: 1px solid var(--slate-200) !important;
    border-radius: var(--radius-sm) !important;
    padding: 6px 14px !important;
    cursor: pointer !important;
    transition: all 0.15s !important;
    font-size: 0.875rem !important;
}
.stRadio label:has(input:checked) {
    background: var(--blue-100) !important;
    border-color: var(--blue-400) !important;
    color: var(--blue-600) !important;
    font-weight: 600 !important;
}

/* ═══════════════════════════════════════════════════
   DATAFRAME / TABLE
═══════════════════════════════════════════════════ */
[data-testid="stDataFrame"] {
    border-radius: var(--radius-md) !important;
    overflow: hidden !important;
    border: 1px solid var(--slate-200) !important;
    box-shadow: var(--shadow-sm) !important;
}
[data-testid="stDataFrame"] table {
    border-collapse: collapse !important;
}
[data-testid="stDataFrame"] th {
    background: var(--slate-50) !important;
    font-size: 0.72rem !important;
    font-weight: 600 !important;
    color: var(--slate-500) !important;
    text-transform: uppercase !important;
    letter-spacing: 0.05em !important;
    padding: 10px 14px !important;
    border-bottom: 1px solid var(--slate-200) !important;
}
[data-testid="stDataFrame"] td {
    padding: 9px 14px !important;
    font-size: 0.875rem !important;
    border-bottom: 1px solid var(--slate-100) !important;
}

/* ═══════════════════════════════════════════════════
   EXPANDER
═══════════════════════════════════════════════════ */
[data-testid="stExpander"] {
    border: 1px solid var(--slate-200) !important;
    border-radius: var(--radius-md) !important;
    background: var(--white) !important;
    box-shadow: var(--shadow-sm) !important;
    margin-bottom: 1rem !important;
    overflow: hidden !important;
}
[data-testid="stExpander"] > div:first-child {
    padding: 1rem 1.25rem !important;
    font-weight: 600 !important;
    font-size: 0.9rem !important;
    background: var(--white) !important;
}

/* ═══════════════════════════════════════════════════
   TABS
═══════════════════════════════════════════════════ */
[data-testid="stTabs"] [data-baseweb="tab-list"] {
    background: transparent !important;
    border-bottom: 2px solid var(--slate-200) !important;
    gap: 0 !important;
    padding: 0 !important;
}
[data-testid="stTabs"] [data-baseweb="tab"] {
    border-radius: 0 !important;
    padding: 10px 20px !important;
    font-size: 0.875rem !important;
    font-weight: 500 !important;
    color: var(--slate-500) !important;
    border-bottom: 2px solid transparent !important;
    margin-bottom: -2px !important;
    background: transparent !important;
}
[data-testid="stTabs"] [data-baseweb="tab"][aria-selected="true"] {
    color: var(--blue-600) !important;
    border-bottom-color: var(--blue-600) !important;
    font-weight: 600 !important;
}
[data-testid="stTabs"] [data-baseweb="tab-panel"] {
    padding-top: 1.25rem !important;
}

/* ═══════════════════════════════════════════════════
   ALERTS / INFO BOXES
═══════════════════════════════════════════════════ */
[data-testid="stAlert"] {
    border-radius: var(--radius-md) !important;
    border-left-width: 4px !important;
    font-size: 0.875rem !important;
}

/* ═══════════════════════════════════════════════════
   DIVIDER
═══════════════════════════════════════════════════ */
hr {
    border: none !important;
    border-top: 1px solid var(--slate-200) !important;
    margin: 1.5rem 0 !important;
}

/* ═══════════════════════════════════════════════════
   PLOTLY CHARTS
═══════════════════════════════════════════════════ */
.js-plotly-plot {
    border-radius: var(--radius-md) !important;
}

/* ═══════════════════════════════════════════════════
   CUSTOM COMPONENTS
═══════════════════════════════════════════════════ */
.sb-card {
    background: var(--white);
    border: 1px solid var(--slate-200);
    border-radius: var(--radius-md);
    padding: 1.25rem;
    box-shadow: var(--shadow-sm);
    margin-bottom: 1rem;
}
.sb-page-header {
    margin-bottom: 1.5rem;
}
.sb-page-header h1 {
    font-size: 1.6rem;
    font-weight: 700;
    color: var(--navy-900);
    margin-bottom: 0.25rem;
}
.sb-page-header p {
    color: var(--slate-500);
    font-size: 0.9rem;
}
.sb-badge {
    display: inline-block;
    padding: 3px 10px;
    border-radius: 20px;
    font-size: 0.75rem;
    font-weight: 600;
}
.sb-badge-in {
    background: var(--green-100);
    color: #166534;
}
.sb-badge-out {
    background: var(--red-100);
    color: #991b1b;
}
.sb-section-title {
    font-size: 0.95rem;
    font-weight: 600;
    color: var(--navy-900);
    margin-bottom: 0.75rem;
    display: flex;
    align-items: center;
    gap: 6px;
}
</style>
"""

PLOTLY_THEME = {
    "paper_bgcolor": "white",
    "plot_bgcolor": "#f8fafc",
    "font": {
        "family": "DM Sans, sans-serif",
        "color": "#334155",
    },
    "title_font_size": 14,
    "title_font_color": "#0a1628",
    "colorway": ["#1e6ab3", "#22c55e", "#f59e0b", "#ef4444", "#8b5cf6", "#06b6d4", "#ec4899"],
    "margin": dict(l=12, r=12, t=36, b=12),
}