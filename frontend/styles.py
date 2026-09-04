"""
Chargeback Evidence AI - Stripe & Linear Inspired Fintech Design System
Provides custom CSS, glassmorphism, responsive cards, micro-animations, and typography.
"""

FINTECH_CSS = """
<style>
/* Import Inter & JetBrains Mono Fonts */
@import url('https://fonts.googleapis.com/css2?family=Inter:wght@300;400;500;600;700;800&family=JetBrains+Mono:wght@400;500;600&display=swap');

:root {
    --bg-primary: #090D16;
    --bg-surface: #0F1626;
    --bg-card: rgba(18, 24, 38, 0.75);
    --bg-card-hover: rgba(24, 33, 53, 0.85);
    --border-color: rgba(255, 255, 255, 0.08);
    --border-hover: rgba(59, 130, 246, 0.35);
    --text-primary: #F8FAFC;
    --text-secondary: #94A3B8;
    --text-muted: #64748B;
    --brand-primary: #3B82F6;
    --brand-gradient: linear-gradient(135deg, #3B82F6 0%, #6366F1 50%, #8B5CF6 100%);
    --card-gradient: linear-gradient(180deg, rgba(20, 28, 45, 0.7) 0%, rgba(12, 17, 29, 0.9) 100%);
    --success: #10B981;
    --warning: #F59E0B;
    --danger: #EF4444;
    --radius-sm: 8px;
    --radius-md: 12px;
    --radius-lg: 16px;
}

/* Global resets & typography */
html, body, [class*="css"] {
    font-family: 'Inter', -apple-system, BlinkMacSystemFont, sans-serif !important;
}

.stApp {
    background-color: var(--bg-primary) !important;
    background-image: 
        radial-gradient(at 0% 0%, rgba(59, 130, 246, 0.08) 0px, transparent 50%),
        radial-gradient(at 100% 0%, rgba(139, 92, 246, 0.06) 0px, transparent 50%) !important;
}

/* Hide Streamlit default decorations */
#MainMenu {visibility: hidden;}
footer {visibility: hidden;}
header {background: transparent !important;}
[data-testid="stHeader"] {background: transparent !important;}

/* Streamlit button overrides for fintech aesthetics */
.stButton > button {
    border-radius: var(--radius-sm) !important;
    font-weight: 600 !important;
    font-size: 0.86rem !important;
    letter-spacing: -0.01em !important;
    transition: all 0.2s ease !important;
    border: 1px solid var(--border-color) !important;
}

.stButton > button:hover {
    border-color: var(--brand-primary) !important;
    box-shadow: 0 4px 14px rgba(59, 130, 246, 0.2) !important;
    transform: translateY(-1px) !important;
}

.stButton > button[kind="primary"] {
    background: linear-gradient(135deg, #2563EB 0%, #3B82F6 100%) !important;
    border: none !important;
    color: white !important;
    box-shadow: 0 4px 12px rgba(37, 99, 235, 0.3) !important;
}

.stButton > button[kind="primary"]:hover {
    background: linear-gradient(135deg, #1D4ED8 0%, #2563EB 100%) !important;
    box-shadow: 0 6px 20px rgba(37, 99, 235, 0.45) !important;
}

/* Top App Header Container */
.app-header-container {
    display: flex;
    justify-content: space-between;
    align-items: center;
    padding: 14px 24px;
    background: rgba(15, 22, 38, 0.8);
    backdrop-filter: blur(12px);
    border: 1px solid var(--border-color);
    border-radius: var(--radius-md);
    margin-bottom: 20px;
}

.brand-badge {
    font-weight: 800;
    font-size: 1.15rem;
    letter-spacing: -0.02em;
    background: linear-gradient(90deg, #60A5FA, #A78BFA);
    -webkit-background-clip: text;
    -webkit-text-fill-color: transparent;
}

.sub-tag {
    font-size: 0.72rem;
    background: rgba(59, 130, 246, 0.12);
    border: 1px solid rgba(59, 130, 246, 0.25);
    color: #93C5FD;
    padding: 3px 9px;
    border-radius: 999px;
    font-weight: 600;
    letter-spacing: 0.04em;
    text-transform: uppercase;
    display: inline-flex;
    align-items: center;
    gap: 5px;
}

/* Fintech Cards */
.fintech-card {
    background: var(--card-gradient);
    border: 1px solid var(--border-color);
    border-radius: var(--radius-md);
    padding: 20px;
    margin-bottom: 16px;
    box-shadow: 0 4px 20px -2px rgba(0, 0, 0, 0.4);
    backdrop-filter: blur(16px);
    transition: all 0.2s ease;
}

.fintech-card:hover {
    border-color: var(--border-hover);
}

.card-title {
    font-size: 0.95rem;
    font-weight: 600;
    color: var(--text-primary);
    margin-bottom: 6px;
    display: flex;
    align-items: center;
    justify-content: space-between;
}

.card-subtitle {
    font-size: 0.82rem;
    color: var(--text-muted);
    line-height: 1.4;
    margin-bottom: 0;
}

/* Dual Portal & Landing Page Styling */
.landing-brand-header {
    display: flex;
    justify-content: space-between;
    align-items: center;
    margin-bottom: 28px;
}

.landing-brand-logo {
    display: inline-flex;
    align-items: center;
    gap: 10px;
}

.landing-logo-icon {
    width: 36px;
    height: 36px;
    background: linear-gradient(135deg, #2563EB 0%, #7C3AED 100%);
    border-radius: 10px;
    display: flex;
    align-items: center;
    justify-content: center;
    color: white;
    font-size: 1.2rem;
    box-shadow: 0 4px 14px rgba(37, 99, 235, 0.4);
}

.landing-brand-name {
    font-weight: 800;
    font-size: 1.2rem;
    letter-spacing: -0.025em;
    color: #F8FAFC;
}

.landing-tagline {
    font-size: 0.78rem;
    color: #64748B;
    font-weight: 500;
}

.landing-badge {
    display: inline-flex;
    align-items: center;
    gap: 6px;
    background: rgba(30, 41, 59, 0.65);
    border: 1px solid rgba(59, 130, 246, 0.3);
    color: #93C5FD;
    padding: 4px 12px;
    border-radius: 9999px;
    font-size: 0.72rem;
    font-weight: 700;
    letter-spacing: 0.06em;
    text-transform: uppercase;
    margin-bottom: 18px;
    box-shadow: 0 0 16px rgba(59, 130, 246, 0.12);
}

.landing-headline {
    font-size: 3rem;
    font-weight: 800;
    letter-spacing: -0.035em;
    line-height: 1.15;
    color: #F8FAFC;
    margin-bottom: 16px;
}

.landing-headline .gradient-text {
    background: linear-gradient(90deg, #60A5FA 0%, #818CF8 50%, #A78BFA 100%);
    -webkit-background-clip: text;
    -webkit-text-fill-color: transparent;
}

.landing-subtitle {
    font-size: 1.02rem;
    color: #94A3B8;
    line-height: 1.6;
    max-width: 520px;
    margin-bottom: 28px;
}

.trust-grid {
    display: grid;
    grid-template-columns: 1fr 1fr;
    gap: 14px;
    max-width: 500px;
    margin-bottom: 36px;
}

.trust-item {
    display: flex;
    align-items: center;
    gap: 12px;
    background: rgba(15, 23, 42, 0.5);
    border: 1px solid rgba(255, 255, 255, 0.06);
    border-radius: 12px;
    padding: 12px 14px;
    transition: all 0.2s ease;
}

.trust-item:hover {
    border-color: rgba(59, 130, 246, 0.25);
    background: rgba(30, 41, 59, 0.5);
}

.trust-icon {
    width: 34px;
    height: 34px;
    border-radius: 8px;
    display: flex;
    align-items: center;
    justify-content: center;
    flex-shrink: 0;
    font-size: 1rem;
}

.trust-icon.investigation {
    background: rgba(59, 130, 246, 0.15);
    border: 1px solid rgba(59, 130, 246, 0.3);
    color: #60A5FA;
}

.trust-icon.verification {
    background: rgba(14, 165, 233, 0.15);
    border: 1px solid rgba(14, 165, 233, 0.3);
    color: #38BDF8;
}

.trust-icon.traceability {
    background: rgba(99, 102, 241, 0.15);
    border: 1px solid rgba(99, 102, 241, 0.3);
    color: #818CF8;
}

.trust-icon.vault {
    background: rgba(16, 185, 129, 0.15);
    border: 1px solid rgba(16, 185, 129, 0.3);
    color: #34D399;
}

.trust-item-title {
    font-size: 0.86rem;
    font-weight: 700;
    color: #F1F5F9;
    margin-bottom: 2px;
}

.trust-item-desc {
    font-size: 0.74rem;
    color: #64748B;
}

.partners-section {
    border-top: 1px solid rgba(255, 255, 255, 0.06);
    padding-top: 18px;
    max-width: 500px;
}

.partners-label {
    font-size: 0.7rem;
    font-weight: 600;
    text-transform: uppercase;
    letter-spacing: 0.08em;
    color: #64748B;
    margin-bottom: 10px;
}

.partners-row {
    display: flex;
    align-items: center;
    gap: 22px;
}

.partner-logo {
    font-size: 1rem;
    font-weight: 800;
    color: #475569;
    letter-spacing: -0.02em;
    transition: color 0.2s ease;
}

.partner-logo:hover {
    color: #94A3B8;
}

/* Glassmorphism Auth Card */
.st-key-auth_card_container,
.auth-card-outer {
    background: rgba(15, 23, 42, 0.88) !important;
    border: 1px solid rgba(255, 255, 255, 0.08) !important;
    border-radius: 24px !important;
    padding: 36px 30px !important;
    box-shadow: 0 25px 50px -12px rgba(0, 0, 0, 0.8), 0 0 35px rgba(37, 99, 235, 0.06) !important;
    backdrop-filter: blur(24px) !important;
    max-width: 500px !important;
    margin: 0 auto !important;
}

.auth-card-heading {
    font-size: 1.8rem;
    font-weight: 800;
    color: #F8FAFC;
    letter-spacing: -0.025em;
    margin: 0 0 6px 0;
}

.auth-card-subheading {
    font-size: 0.88rem;
    color: #94A3B8;
    margin: 0 0 24px 0;
    line-height: 1.45;
}

/* Portal Card Box */
.portal-card-box {
    background: rgba(255, 255, 255, 0.025);
    border: 1px solid rgba(255, 255, 255, 0.08);
    border-radius: 18px;
    padding: 18px 20px;
    display: flex;
    align-items: center;
    justify-content: space-between;
    gap: 16px;
    transition: all 0.25s cubic-bezier(0.16, 1, 0.3, 1);
    box-shadow: 0 4px 20px rgba(0, 0, 0, 0.25);
    cursor: pointer;
    margin-bottom: 14px;
    position: relative;
}

.portal-card-box:hover {
    background: rgba(37, 99, 235, 0.08);
    border-color: rgba(96, 165, 250, 0.45);
    transform: translateY(-2px);
    box-shadow: 0 12px 30px -5px rgba(37, 99, 235, 0.25);
}

.portal-card-left {
    display: flex;
    align-items: center;
    gap: 14px;
    flex: 1;
}

.portal-card-icon {
    width: 48px;
    height: 48px;
    border-radius: 14px;
    display: flex;
    align-items: center;
    justify-content: center;
    flex-shrink: 0;
}

.portal-card-icon.merchant {
    background: linear-gradient(135deg, #4F46E5 0%, #3B82F6 100%);
    color: #FFFFFF;
    box-shadow: 0 6px 18px rgba(59, 130, 246, 0.35);
}

.portal-card-icon.customer {
    background: linear-gradient(135deg, #059669 0%, #10B981 50%, #06B6D4 100%);
    color: #FFFFFF;
    box-shadow: 0 6px 18px rgba(16, 185, 129, 0.35);
}

.portal-card-title {
    font-size: 1.1rem;
    font-weight: 700;
    color: #F8FAFC;
    letter-spacing: -0.01em;
    margin-bottom: 4px;
}

.portal-card-desc {
    font-size: 0.8rem;
    color: #94A3B8;
    line-height: 1.45;
}

.portal-card-arrow {
    width: 36px;
    height: 36px;
    border-radius: 50%;
    background: rgba(255, 255, 255, 0.04);
    border: 1px solid rgba(255, 255, 255, 0.1);
    display: flex;
    align-items: center;
    justify-content: center;
    color: #94A3B8;
    flex-shrink: 0;
    transition: all 0.2s ease;
}

.portal-card-box:hover .portal-card-arrow {
    background: rgba(59, 130, 246, 0.3);
    border-color: #60A5FA;
    color: #FFFFFF;
    transform: translateX(3px);
}

/* Card Footer */
.auth-card-footer {
    border-top: 1px solid rgba(255, 255, 255, 0.06);
    padding-top: 18px;
    margin-top: 22px;
    text-align: center;
}

.auth-card-footer-item {
    display: inline-flex;
    align-items: center;
    gap: 6px;
    font-size: 0.78rem;
    color: #64748B;
    font-weight: 500;
    margin-bottom: 3px;
}

.auth-card-footer-sub {
    font-size: 0.72rem;
    color: #475569;
}

/* Overlay buttons for Streamlit click binding */
.st-key-btn_portal_merchant {
    margin-top: -108px !important;
    height: 94px !important;
    position: relative !important;
    z-index: 10 !important;
}

.st-key-btn_portal_merchant button {
    height: 94px !important;
    width: 100% !important;
    opacity: 0 !important;
    cursor: pointer !important;
}

.st-key-btn_portal_customer {
    margin-top: -108px !important;
    height: 94px !important;
    position: relative !important;
    z-index: 10 !important;
}

.st-key-btn_portal_customer button {
    height: 94px !important;
    width: 100% !important;
    opacity: 0 !important;
    cursor: pointer !important;
}

/* OTP Code input field */
input[aria-label="6-Digit Verification Code"] {
    text-align: center !important;
    font-size: 1.5rem !important;
    letter-spacing: 0.35em !important;
    font-weight: 700 !important;
    font-family: 'JetBrains Mono', monospace !important;
    color: #60A5FA !important;
    background: rgba(15, 23, 42, 0.8) !important;
    border: 1px solid rgba(59, 130, 246, 0.4) !important;
    border-radius: 12px !important;
    padding: 12px 14px !important;
}

input[aria-label="6-Digit Verification Code"]:focus {
    border-color: #3B82F6 !important;
    box-shadow: 0 0 20px rgba(59, 130, 246, 0.3) !important;
}

/* Horizontal Case Status Lifecycle Tracker */
.lifecycle-tracker {
    display: flex;
    align-items: center;
    justify-content: space-between;
    background: rgba(15, 22, 36, 0.8);
    border: 1px solid var(--border-color);
    border-radius: var(--radius-md);
    padding: 12px 20px;
    margin-bottom: 20px;
    overflow-x: auto;
}

.lifecycle-step {
    display: flex;
    align-items: center;
    gap: 8px;
    font-size: 0.82rem;
    font-weight: 600;
    color: #64748B;
    position: relative;
    white-space: nowrap;
}

.lifecycle-step.active {
    color: #60A5FA;
}

.lifecycle-step.completed {
    color: #34D399;
}

.lifecycle-dot {
    width: 22px;
    height: 22px;
    border-radius: 50%;
    display: flex;
    align-items: center;
    justify-content: center;
    font-size: 0.72rem;
    font-weight: 700;
    background: rgba(255, 255, 255, 0.05);
    border: 1px solid rgba(255, 255, 255, 0.1);
}

.lifecycle-step.active .lifecycle-dot {
    background: #2563EB;
    color: #FFFFFF;
    box-shadow: 0 0 12px rgba(37, 99, 235, 0.6);
    border-color: #60A5FA;
}

.lifecycle-step.completed .lifecycle-dot {
    background: rgba(16, 185, 129, 0.18);
    color: #34D399;
    border-color: #10B981;
}

.lifecycle-divider {
    flex: 1;
    height: 2px;
    background: rgba(255, 255, 255, 0.06);
    margin: 0 12px;
    min-width: 24px;
}

.lifecycle-divider.active {
    background: linear-gradient(90deg, #10B981, #3B82F6);
}

/* KPI Metric Cards */
.metric-container {
    display: flex;
    flex-direction: column;
    padding: 18px 20px;
    background: rgba(18, 24, 38, 0.65);
    border: 1px solid var(--border-color);
    border-radius: var(--radius-md);
    transition: border-color 0.2s ease;
}

.metric-container:hover {
    border-color: rgba(99, 102, 241, 0.4);
}

.metric-label {
    font-size: 0.74rem;
    font-weight: 600;
    text-transform: uppercase;
    letter-spacing: 0.05em;
    color: var(--text-muted);
}

.metric-value {
    font-size: 1.85rem;
    font-weight: 800;
    color: var(--text-primary);
    margin: 4px 0;
    letter-spacing: -0.03em;
}

.metric-trend {
    font-size: 0.78rem;
    font-weight: 500;
    display: inline-flex;
    align-items: center;
    gap: 4px;
}

.trend-up { color: var(--success); }
.trend-neutral { color: #60A5FA; }

/* 10-Step Timeline */
.step-card {
    background: rgba(15, 22, 36, 0.75);
    border: 1px solid var(--border-color);
    border-radius: var(--radius-md);
    padding: 14px 18px;
    display: flex;
    align-items: flex-start;
    gap: 16px;
    margin-bottom: 10px;
    transition: all 0.2s ease;
}

.step-card.active {
    border-color: #3B82F6;
    background: rgba(30, 58, 138, 0.18);
    box-shadow: 0 0 20px rgba(59, 130, 246, 0.2);
}

.step-card.complete {
    border-color: rgba(16, 185, 129, 0.3);
}

.step-badge-num {
    width: 28px;
    height: 28px;
    border-radius: 50%;
    display: flex;
    align-items: center;
    justify-content: center;
    font-size: 0.75rem;
    font-weight: 700;
    flex-shrink: 0;
}

.step-badge-num.complete {
    background: rgba(16, 185, 129, 0.2);
    color: #34D399;
    border: 1px solid rgba(16, 185, 129, 0.4);
}

.step-content {
    flex: 1;
}

.step-header {
    display: flex;
    justify-content: space-between;
    align-items: center;
    margin-bottom: 4px;
}

.step-name {
    font-weight: 600;
    font-size: 0.92rem;
    color: #F8FAFC;
}

.step-agent {
    font-size: 0.72rem;
    color: #60A5FA;
    background: rgba(59, 130, 246, 0.12);
    padding: 2px 7px;
    border-radius: 4px;
    font-weight: 600;
}

.step-desc {
    font-size: 0.82rem;
    color: #94A3B8;
    line-height: 1.4;
    margin-bottom: 8px;
}

.step-meta {
    display: flex;
    gap: 16px;
    font-size: 0.74rem;
    color: #64748B;
}

/* Status Pills */
.status-pill {
    font-size: 0.72rem;
    font-weight: 700;
    padding: 3px 8px;
    border-radius: 999px;
    text-transform: uppercase;
    letter-spacing: 0.04em;
    display: inline-flex;
    align-items: center;
    gap: 4px;
}

.status-pill.complete, .status-pill.won {
    background: rgba(16, 185, 129, 0.15);
    color: #34D399;
    border: 1px solid rgba(16, 185, 129, 0.3);
}

.status-pill.running, .status-pill.investigating {
    background: rgba(59, 130, 246, 0.15);
    color: #60A5FA;
    border: 1px solid rgba(59, 130, 246, 0.3);
}

.status-pill.new {
    background: rgba(148, 163, 184, 0.15);
    color: #94A3B8;
    border: 1px solid rgba(148, 163, 184, 0.25);
}

/* Score Breakdown & Uplift */
.score-breakdown-container {
    background: rgba(15, 22, 36, 0.75);
    border: 1px solid var(--border-color);
    border-radius: var(--radius-md);
    padding: 16px;
    margin-top: 14px;
}

.score-item {
    display: flex;
    justify-content: space-between;
    align-items: center;
    padding: 7px 0;
    border-bottom: 1px solid rgba(255, 255, 255, 0.04);
}

.score-pts-positive {
    font-size: 0.86rem;
    font-weight: 700;
    color: #34D399;
}

.score-pts-negative {
    font-size: 0.86rem;
    font-weight: 700;
    color: #F87171;
}

.uplift-banner {
    background: linear-gradient(90deg, rgba(16, 185, 129, 0.12) 0%, rgba(59, 130, 246, 0.08) 100%);
    border: 1px solid rgba(16, 185, 129, 0.25);
    border-radius: var(--radius-md);
    padding: 14px 18px;
    margin: 14px 0;
    display: flex;
    justify-content: space-between;
    align-items: center;
}

.uplift-badge {
    font-size: 1.25rem;
    font-weight: 900;
    color: #34D399;
}

/* Clickable Traceable Claim */
.traceable-claim {
    background: rgba(18, 26, 44, 0.7);
    border: 1px solid rgba(59, 130, 246, 0.25);
    border-radius: var(--radius-sm);
    padding: 12px 16px;
    margin-bottom: 10px;
    display: flex;
    justify-content: space-between;
    align-items: center;
    transition: all 0.2s ease;
}

.traceable-claim:hover {
    border-color: #3B82F6;
    background: rgba(30, 58, 138, 0.15);
}

.source-badge {
    font-size: 0.74rem;
    color: #93C5FD;
    background: rgba(59, 130, 246, 0.15);
    padding: 3px 8px;
    border-radius: 4px;
    border: 1px solid rgba(59, 130, 246, 0.3);
}

/* Chat Assistant Bubbles */
.chat-bubble-user {
    background: rgba(37, 99, 235, 0.25);
    border: 1px solid rgba(59, 130, 246, 0.4);
    border-radius: 12px 12px 2px 12px;
    padding: 12px 16px;
    margin: 8px 0 8px auto;
    max-width: 80%;
    color: #F8FAFC;
    font-size: 0.88rem;
}

.chat-bubble-ai {
    background: rgba(18, 26, 44, 0.8);
    border: 1px solid rgba(255, 255, 255, 0.08);
    border-radius: 12px 12px 12px 2px;
    padding: 14px 18px;
    margin: 8px auto 8px 0;
    max-width: 85%;
    color: #E2E8F0;
    font-size: 0.88rem;
    line-height: 1.5;
}

.citation-box {
    background: rgba(0, 0, 0, 0.35);
    border-left: 3px solid #3B82F6;
    padding: 6px 12px;
    border-radius: 0 6px 6px 0;
    font-size: 0.78rem;
    color: #94A3B8;
    margin-top: 6px;
}
</style>
"""
