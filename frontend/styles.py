"""
Chargeback Evidence AI - Stitch Minimalist Corporate Fintech Design System
Institutional, high-contrast, clean off-white canvas with dark slate shell,
crystalline typography (Inter + JetBrains Mono), and Material Symbols Outlined icons.
"""

FINTECH_CSS = """
<style>
/* Import Inter, JetBrains Mono, and Material Symbols Outlined */
@import url('https://fonts.googleapis.com/css2?family=Inter:wght@300;400;500;600;700;800&family=JetBrains+Mono:wght@400;500;600;700&display=swap');
@import url('https://fonts.googleapis.com/css2?family=Material+Symbols+Outlined:wght,FILL@100..700,0..1&display=swap');

:root {
    --surface-canvas: #F8F9FB;
    --surface-card: #FFFFFF;
    --surface-container-low: #F2F4F6;
    --surface-container: #EDEEF0;
    --surface-container-high: #E7E8EA;
    --surface-container-highest: #E1E2E4;
    
    --shell-sidebar: #2D3948;
    --shell-sidebar-active: #1A242C;
    --shell-sidebar-hover: #374758;
    --shell-sidebar-text: #98A4AD;
    --shell-sidebar-text-active: #FFFFFF;
    
    --primary: #1A242C;
    --primary-container: #2F3A42;
    --primary-hover: #121D24;
    --on-primary: #FFFFFF;
    
    --secondary: #535F70;
    --secondary-slate: #64748B;
    --outline: #74777B;
    --outline-variant: #C4C7CB;
    --border-hairline: #E5E7EB;
    --border-subtle: #E2E8F0;
    
    --on-surface: #191C1E;
    --on-surface-variant: #43474B;
    
    /* Functional Status Indicators */
    --status-success: #10B981;
    --status-success-bg: #ECFDF5;
    --status-success-border: #A7F3D0;
    --status-success-text: #065F46;
    
    --status-warning: #F59E0B;
    --status-warning-bg: #FFFBEB;
    --status-warning-border: #FDE68A;
    --status-warning-text: #92400E;
    
    --status-error: #EF4444;
    --status-error-bg: #FEF2F2;
    --status-error-border: #FECACA;
    --status-error-text: #991B1B;

    --status-info: #3B82F6;
    --status-info-bg: #EFF6FF;
    --status-info-border: #BFDBFE;
    --status-info-text: #1E40AF;
    
    --radius-sm: 6px;
    --radius-md: 10px;
    --radius-lg: 14px;
    --radius-xl: 18px;
    --radius-full: 9999px;
    
    --shadow-sm: 0 1px 2px 0 rgba(0, 0, 0, 0.04);
    --shadow-md: 0 4px 12px -2px rgba(47, 58, 66, 0.06), 0 2px 6px -1px rgba(47, 58, 66, 0.03);
    --shadow-lg: 0 12px 24px -4px rgba(47, 58, 66, 0.08), 0 4px 8px -2px rgba(47, 58, 66, 0.03);
}

/* Global Reset & Typography */
html, body, [class*="css"], .stApp {
    font-family: 'Inter', -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, sans-serif !important;
    background-color: var(--surface-canvas) !important;
    color: var(--on-surface) !important;
}

code, kbd, samp, pre, .font-mono {
    font-family: 'JetBrains Mono', monospace !important;
}

/* Material Symbols Icon Utility */
.material-symbols-outlined {
    font-family: 'Material Symbols Outlined' !important;
    font-weight: normal;
    font-style: normal;
    font-size: 20px;
    line-height: 1;
    letter-spacing: normal;
    text-transform: none;
    display: inline-block;
    white-space: nowrap;
    word-wrap: normal;
    direction: ltr;
    -webkit-font-feature-settings: 'liga';
    -webkit-font-smoothing: antialiased;
    vertical-align: middle;
}

/* Streamlit Native Header & Footer Resets */
#MainMenu {visibility: hidden;}
footer {visibility: hidden;}
header[data-testid="stHeader"] {
    background: transparent !important;
    height: 0 !important;
}

/* Main Container Spacing */
.main .block-container {
    max-width: 1540px !important;
    padding: 1.5rem 2.5rem 3.5rem 2.5rem !important;
}

/* Sidebar Custom Styling (Dark Slate #2D3948 Shell) */
[data-testid="stSidebar"] {
    background-color: var(--shell-sidebar) !important;
    border-right: 1px solid rgba(0, 0, 0, 0.1) !important;
    box-shadow: 2px 0 12px rgba(0, 0, 0, 0.06) !important;
}

[data-testid="stSidebar"] [data-testid="stSidebarContent"] {
    padding: 1.25rem 1rem !important;
}

[data-testid="stSidebar"] hr {
    border-color: rgba(255, 255, 255, 0.1) !important;
    margin: 1rem 0 !important;
}

[data-testid="stSidebar"] .stCaption,
[data-testid="stSidebar"] [data-testid="stCaptionContainer"] {
    color: #8A9CAE !important;
    font-size: 0.68rem !important;
    font-weight: 700 !important;
    letter-spacing: 0.08em !important;
    text-transform: uppercase !important;
    margin-top: 0.75rem !important;
    margin-bottom: 0.25rem !important;
}

/* Sidebar Navigation Buttons */
[data-testid="stSidebar"] .stButton > button {
    background-color: transparent !important;
    color: var(--shell-sidebar-text) !important;
    border: 1px solid transparent !important;
    border-radius: var(--radius-md) !important;
    text-align: left !important;
    justify-content: flex-start !important;
    padding: 0.55rem 0.85rem !important;
    font-size: 0.85rem !important;
    font-weight: 500 !important;
    transition: all 0.15s ease-in-out !important;
    box-shadow: none !important;
    margin-bottom: 2px !important;
}

[data-testid="stSidebar"] .stButton > button:hover {
    background-color: var(--shell-sidebar-hover) !important;
    color: #FFFFFF !important;
    border-color: transparent !important;
    transform: none !important;
}

[data-testid="stSidebar"] .stButton > button[kind="primary"] {
    background-color: var(--shell-sidebar-active) !important;
    color: var(--shell-sidebar-text-active) !important;
    font-weight: 600 !important;
    border: 1px solid rgba(255, 255, 255, 0.12) !important;
    box-shadow: 0 2px 6px rgba(0, 0, 0, 0.2) !important;
}

/* Global Button Styles */
.stButton > button {
    border-radius: var(--radius-md) !important;
    font-weight: 600 !important;
    font-size: 0.86rem !important;
    letter-spacing: -0.01em !important;
    padding: 0.55rem 1.15rem !important;
    transition: all 0.15s cubic-bezier(0.16, 1, 0.3, 1) !important;
    border: 1px solid var(--border-hairline) !important;
    background-color: #FFFFFF !important;
    color: var(--primary) !important;
    box-shadow: var(--shadow-sm) !important;
}

.stButton > button:hover {
    background-color: var(--surface-container-low) !important;
    border-color: var(--outline-variant) !important;
    color: var(--primary) !important;
    box-shadow: var(--shadow-md) !important;
    transform: translateY(-1px) !important;
}

.stButton > button:active {
    transform: translateY(0) !important;
}

.stButton > button[kind="primary"] {
    background-color: var(--primary) !important;
    color: var(--on-primary) !important;
    border: 1px solid var(--primary) !important;
    box-shadow: 0 2px 6px rgba(26, 36, 44, 0.2) !important;
}

.stButton > button[kind="primary"]:hover {
    background-color: var(--primary-container) !important;
    border-color: var(--primary-container) !important;
    color: #FFFFFF !important;
    box-shadow: 0 4px 14px rgba(26, 36, 44, 0.3) !important;
}

/* Global Form Controls (Inputs, Selects, Textareas) */
.stTextInput input, 
.stNumberInput input, 
.stSelectbox [data-baseweb="select"] > div,
.stTextArea textarea {
    background-color: #FFFFFF !important;
    border: 1px solid var(--border-hairline) !important;
    border-radius: var(--radius-md) !important;
    color: var(--on-surface) !important;
    font-size: 0.88rem !important;
    box-shadow: var(--shadow-sm) !important;
    transition: all 0.15s ease !important;
}

.stTextInput input:focus, 
.stNumberInput input:focus, 
.stTextArea textarea:focus,
.stSelectbox [data-baseweb="select"] > div:focus-within {
    border-color: var(--primary-container) !important;
    box-shadow: 0 0 0 3px rgba(47, 58, 66, 0.08) !important;
    outline: none !important;
}

/* Custom Stitch UI Cards */
.stitch-card {
    background: #FFFFFF;
    border: 1px solid var(--border-hairline);
    border-radius: var(--radius-lg);
    padding: 1.5rem;
    box-shadow: var(--shadow-sm);
    transition: box-shadow 0.2s ease, border-color 0.2s ease;
    margin-bottom: 1.25rem;
}

.stitch-card:hover {
    box-shadow: var(--shadow-md);
    border-color: var(--outline-variant);
}

.stitch-card-header {
    display: flex;
    justify-content: space-between;
    align-items: center;
    margin-bottom: 0.75rem;
}

.stitch-card-title {
    font-size: 1.05rem;
    font-weight: 700;
    color: var(--on-surface);
    letter-spacing: -0.015em;
    margin: 0;
}

.stitch-card-subtitle {
    font-size: 0.82rem;
    color: var(--secondary-slate);
    margin: 0.25rem 0 0 0;
}

/* Top App Header / Bar */
.stitch-topbar {
    display: flex;
    justify-content: space-between;
    align-items: center;
    background: #FFFFFF;
    border: 1px solid var(--border-hairline);
    border-radius: var(--radius-lg);
    padding: 0.75rem 1.25rem;
    margin-bottom: 1.5rem;
    box-shadow: var(--shadow-sm);
}

/* Status Badges & Pills */
.stitch-pill {
    display: inline-flex;
    align-items: center;
    gap: 5px;
    font-size: 0.72rem;
    font-weight: 700;
    letter-spacing: 0.04em;
    text-transform: uppercase;
    padding: 3px 9px;
    border-radius: var(--radius-full);
}

.stitch-pill-dot {
    width: 6px;
    height: 6px;
    border-radius: 50%;
}

.stitch-pill-success {
    background-color: var(--status-success-bg);
    color: var(--status-success-text);
    border: 1px solid var(--status-success-border);
}
.stitch-pill-success .stitch-pill-dot { background-color: var(--status-success); }

.stitch-pill-warning {
    background-color: var(--status-warning-bg);
    color: var(--status-warning-text);
    border: 1px solid var(--status-warning-border);
}
.stitch-pill-warning .stitch-pill-dot { background-color: var(--status-warning); }

.stitch-pill-error {
    background-color: var(--status-error-bg);
    color: var(--status-error-text);
    border: 1px solid var(--status-error-border);
}
.stitch-pill-error .stitch-pill-dot { background-color: var(--status-error); }

.stitch-pill-info {
    background-color: var(--status-info-bg);
    color: var(--status-info-text);
    border: 1px solid var(--status-info-border);
}
.stitch-pill-info .stitch-pill-dot { background-color: var(--status-info); }

.stitch-pill-neutral {
    background-color: var(--surface-container-low);
    color: var(--secondary-slate);
    border: 1px solid var(--border-hairline);
}
.stitch-pill-neutral .stitch-pill-dot { background-color: var(--outline); }

/* Data Tables */
.stitch-table-wrapper {
    background: #FFFFFF;
    border: 1px solid var(--border-hairline);
    border-radius: var(--radius-lg);
    overflow: hidden;
    box-shadow: var(--shadow-sm);
    margin-bottom: 1.25rem;
}

.stitch-table {
    width: 100%;
    border-collapse: collapse;
    text-align: left;
    font-size: 0.85rem;
}

.stitch-table th {
    background: var(--surface-container-low);
    color: var(--secondary-slate);
    font-size: 0.72rem;
    font-weight: 700;
    text-transform: uppercase;
    letter-spacing: 0.06em;
    padding: 0.75rem 1rem;
    border-bottom: 1px solid var(--border-hairline);
}

.stitch-table td {
    padding: 0.85rem 1rem;
    border-bottom: 1px solid var(--border-hairline);
    color: var(--on-surface);
    vertical-align: middle;
}

.stitch-table tr:last-child td {
    border-bottom: none;
}

.stitch-table tr:hover td {
    background-color: rgba(248, 249, 251, 0.8);
}

/* Metric Cards (KPI 4-strip) */
.stitch-kpi-card {
    background: #FFFFFF;
    border: 1px solid var(--border-hairline);
    border-radius: var(--radius-lg);
    padding: 1.25rem;
    box-shadow: var(--shadow-sm);
    display: flex;
    flex-direction: column;
    justify-content: space-between;
    transition: box-shadow 0.2s ease;
}

.stitch-kpi-card:hover {
    box-shadow: var(--shadow-md);
}

.stitch-kpi-header {
    display: flex;
    justify-content: space-between;
    align-items: center;
    color: var(--secondary-slate);
    font-size: 0.82rem;
    font-weight: 600;
}

.stitch-kpi-icon {
    width: 32px;
    height: 32px;
    border-radius: var(--radius-md);
    background: var(--surface-container-low);
    color: var(--primary-container);
    display: flex;
    align-items: center;
    justify-content: center;
}

.stitch-kpi-value {
    font-size: 1.9rem;
    font-weight: 800;
    color: var(--on-surface);
    letter-spacing: -0.03em;
    line-height: 1.15;
    margin: 0.5rem 0 0.2rem 0;
}

.stitch-kpi-footer {
    display: flex;
    justify-content: space-between;
    align-items: center;
    font-size: 0.76rem;
    color: var(--secondary-slate);
    border-top: 1px solid var(--border-hairline);
    padding-top: 0.6rem;
    margin-top: 0.75rem;
}

/* Tabs Styling */
.stTabs [data-baseweb="tab-list"] {
    background-color: #FFFFFF !important;
    border: 1px solid var(--border-hairline) !important;
    border-radius: var(--radius-md) !important;
    padding: 4px !important;
    gap: 4px !important;
    box-shadow: var(--shadow-sm) !important;
    margin-bottom: 1.25rem !important;
}

.stTabs [data-baseweb="tab"] {
    border-radius: var(--radius-sm) !important;
    padding: 6px 14px !important;
    font-size: 0.84rem !important;
    font-weight: 600 !important;
    color: var(--secondary-slate) !important;
    border: none !important;
    background: transparent !important;
    transition: all 0.15s ease !important;
}

.stTabs [aria-selected="true"] {
    background-color: var(--primary) !important;
    color: #FFFFFF !important;
    box-shadow: var(--shadow-sm) !important;
}

/* Simulated PDF Canvas Sheet */
.stitch-pdf-sheet {
    background: #FFFFFF;
    border: 1px solid var(--border-hairline);
    border-radius: 4px;
    padding: 2.5rem;
    box-shadow: 0 10px 25px -5px rgba(47, 58, 66, 0.1), 0 8px 10px -6px rgba(47, 58, 66, 0.04);
    max-width: 680px;
    margin: 0 auto;
    font-size: 0.86rem;
    color: var(--on-surface);
}

/* Horizontal Case Lifecycle Tracker */
.stitch-lifecycle {
    display: flex;
    align-items: center;
    justify-content: space-between;
    background: #FFFFFF;
    border: 1px solid var(--border-hairline);
    border-radius: var(--radius-lg);
    padding: 0.85rem 1.5rem;
    margin-bottom: 1.25rem;
    box-shadow: var(--shadow-sm);
    overflow-x: auto;
}

.stitch-step {
    display: flex;
    align-items: center;
    gap: 8px;
    font-size: 0.82rem;
    font-weight: 600;
    color: var(--secondary-slate);
    white-space: nowrap;
}

.stitch-step.active {
    color: var(--primary);
    font-weight: 700;
}

.stitch-step.completed {
    color: var(--status-success-text);
}

.stitch-step-num {
    width: 24px;
    height: 24px;
    border-radius: 50%;
    display: flex;
    align-items: center;
    justify-content: center;
    font-size: 0.72rem;
    font-weight: 700;
    background: var(--surface-container-low);
    border: 1px solid var(--border-hairline);
    color: var(--secondary-slate);
}

.stitch-step.active .stitch-step-num {
    background: var(--primary);
    color: #FFFFFF;
    border-color: var(--primary);
    box-shadow: 0 0 0 3px rgba(26, 36, 44, 0.1);
}

.stitch-step.completed .stitch-step-num {
    background: var(--status-success-bg);
    color: var(--status-success);
    border-color: var(--status-success-border);
}

.stitch-divider {
    flex: 1;
    height: 2px;
    background: var(--border-hairline);
    margin: 0 12px;
    min-width: 20px;
}

.stitch-divider.completed {
    background: var(--status-success);
}

/* Chat Assistant Bubbles */
.chat-bubble-user {
    background: var(--primary);
    color: #FFFFFF;
    padding: 10px 16px;
    border-radius: 14px 14px 2px 14px;
    max-width: 78%;
    margin-left: auto;
    margin-bottom: 10px;
    font-size: 0.86rem;
    line-height: 1.45;
    box-shadow: var(--shadow-sm);
}

.chat-bubble-ai {
    background: #FFFFFF;
    color: var(--on-surface);
    border: 1px solid var(--border-hairline);
    padding: 12px 18px;
    border-radius: 14px 14px 14px 2px;
    max-width: 82%;
    margin-right: auto;
    margin-bottom: 10px;
    font-size: 0.86rem;
    line-height: 1.5;
    box-shadow: var(--shadow-sm);
}

.citation-box {
    background: var(--surface-container-low);
    border: 1px solid var(--border-hairline);
    border-left: 3px solid var(--status-info);
    border-radius: var(--radius-sm);
    padding: 6px 12px;
    font-size: 0.76rem;
    color: var(--secondary-slate);
    margin: 4px 0 10px 0;
}

/* Expander Overrides */
.streamlit-expanderHeader {
    background-color: #FFFFFF !important;
    border: 1px solid var(--border-hairline) !important;
    border-radius: var(--radius-md) !important;
    font-weight: 600 !important;
    font-size: 0.86rem !important;
    color: var(--on-surface) !important;
}

.streamlit-expanderContent {
    background-color: #FFFFFF !important;
    border: 1px solid var(--border-hairline) !important;
    border-top: none !important;
    border-radius: 0 0 var(--radius-md) var(--radius-md) !important;
    padding: 1rem !important;
}

/* Custom Split-Screen Auth Container */
.auth-split-layout {
    display: flex;
    min-height: calc(100vh - 4rem);
    border-radius: var(--radius-xl);
    overflow: hidden;
    box-shadow: var(--shadow-lg);
    border: 1px solid var(--border-hairline);
    background: #FFFFFF;
}

.auth-left-pane {
    background-color: var(--primary);
    color: #FFFFFF;
    padding: 3rem 2.5rem;
    display: flex;
    flex-direction: column;
    justify-content: space-between;
    position: relative;
    overflow: hidden;
}

.auth-right-pane {
    background-color: var(--surface-canvas);
    padding: 2.5rem 2rem;
    display: flex;
    flex-direction: column;
    justify-content: center;
    align-items: center;
}

.auth-card-inner {
    background: #FFFFFF;
    border: 1px solid var(--border-hairline);
    border-radius: var(--radius-lg);
    padding: 2rem 2.25rem;
    width: 100%;
    max-width: 440px;
    box-shadow: var(--shadow-md);
}

.portal-choice-card {
    background: var(--surface-container-low);
    border: 1px solid var(--border-hairline);
    border-radius: var(--radius-md);
    padding: 1.1rem 1.25rem;
    display: flex;
    align-items: center;
    justify-content: space-between;
    margin-bottom: 0.85rem;
    cursor: pointer;
    transition: all 0.15s ease;
}

.portal-choice-card:hover {
    background: #FFFFFF;
    border-color: var(--primary-container);
    box-shadow: var(--shadow-md);
    transform: translateY(-1px);
}
</style>
"""
