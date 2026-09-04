"""
Chargeback Evidence AI - Stripe & Linear Inspired Fintech Design System
Provides custom CSS, glassmorphism, responsive cards, micro-animations, and typography.
"""

FINTECH_CSS = """
<style>
/* Import Inter & JetBrains Mono Fonts */
@import url('https://fonts.googleapis.com/css2?family=Inter:wght@300;400;500;600;700;800&family=JetBrains+Mono:wght@400;500;600&display=swap');

:root {
    --bg-primary: #0A0D14;
    --bg-surface: #111522;
    --bg-card: rgba(18, 24, 38, 0.7);
    --bg-glass: rgba(255, 255, 255, 0.03);
    --border-color: rgba(255, 255, 255, 0.08);
    --border-hover: rgba(59, 130, 246, 0.4);
    --text-primary: #F8FAFC;
    --text-secondary: #94A3B8;
    --text-muted: #64748B;
    --brand-primary: #3B82F6;
    --brand-gradient: linear-gradient(135deg, #3B82F6 0%, #6366F1 50%, #8B5CF6 100%);
    --card-gradient: linear-gradient(180deg, rgba(30, 41, 59, 0.5) 0%, rgba(15, 23, 42, 0.8) 100%);
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

/* Hide Streamlit default decorations */
#MainMenu {visibility: hidden;}
footer {visibility: hidden;}
header {
    background: transparent !important;
}
[data-testid="stHeader"] {
    background: transparent !important;
}
[data-testid="stSidebarCollapsedControl"], [data-testid="collapsedControl"] {
    visibility: visible !important;
    display: flex !important;
    z-index: 999999 !important;
    color: #F8FAFC !important;
}

/* Top Navigation Banner */
.app-header-container {
    display: flex;
    justify-content: space-between;
    align-items: center;
    padding: 14px 24px;
    background: rgba(15, 23, 42, 0.75);
    backdrop-filter: blur(12px);
    border-bottom: 1px solid var(--border-color);
    border-radius: var(--radius-md);
    margin-bottom: 24px;
}

.brand-badge {
    display: inline-flex;
    align-items: center;
    gap: 8px;
    font-weight: 700;
    font-size: 1.15rem;
    letter-spacing: -0.02em;
    background: linear-gradient(90deg, #60A5FA, #A78BFA);
    -webkit-background-clip: text;
    -webkit-text-fill-color: transparent;
}

.sub-tag {
    font-size: 0.72rem;
    background: rgba(59, 130, 246, 0.15);
    border: 1px solid rgba(59, 130, 246, 0.3);
    color: #93C5FD;
    padding: 3px 8px;
    border-radius: 999px;
    font-weight: 600;
    letter-spacing: 0.04em;
    text-transform: uppercase;
}

/* Dual Portal Cards */
.portal-card {
    background: linear-gradient(180deg, rgba(30, 41, 59, 0.6) 0%, rgba(15, 23, 42, 0.9) 100%);
    border: 1px solid var(--border-color);
    border-radius: var(--radius-lg);
    padding: 28px;
    text-align: center;
    transition: all 0.3s cubic-bezier(0.4, 0, 0.2, 1);
    box-shadow: 0 10px 30px -5px rgba(0, 0, 0, 0.5);
}

.portal-card:hover {
    border-color: #60A5FA;
    transform: translateY(-4px);
    box-shadow: 0 16px 40px -10px rgba(59, 130, 246, 0.25);
}

.portal-icon {
    font-size: 2.8rem;
    margin-bottom: 16px;
    display: inline-block;
}

.portal-title {
    font-size: 1.3rem;
    font-weight: 700;
    color: #F8FAFC;
    margin-bottom: 8px;
}

.portal-desc {
    font-size: 0.88rem;
    color: #94A3B8;
    line-height: 1.5;
    margin-bottom: 20px;
}

/* Horizontal Case Status Lifecycle Tracker */
.lifecycle-tracker {
    display: flex;
    align-items: center;
    justify-content: space-between;
    background: rgba(15, 23, 42, 0.7);
    border: 1px solid var(--border-color);
    border-radius: var(--radius-md);
    padding: 14px 20px;
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
    background: #3B82F6;
    color: #FFFFFF;
    box-shadow: 0 0 12px rgba(59, 130, 246, 0.6);
    border-color: #60A5FA;
}

.lifecycle-step.completed .lifecycle-dot {
    background: rgba(16, 185, 129, 0.2);
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

/* Glassmorphic Cards */
.fintech-card {
    background: var(--card-gradient);
    border: 1px solid var(--border-color);
    border-radius: var(--radius-md);
    padding: 20px;
    margin-bottom: 16px;
    box-shadow: 0 4px 20px -2px rgba(0, 0, 0, 0.4);
    backdrop-filter: blur(16px);
    transition: all 0.25s cubic-bezier(0.4, 0, 0.2, 1);
}

.fintech-card:hover {
    border-color: var(--border-hover);
    box-shadow: 0 8px 30px -4px rgba(59, 130, 246, 0.15);
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
    font-size: 0.8rem;
    color: var(--text-muted);
    line-height: 1.4;
}

/* KPI Metric Cards */
.metric-container {
    display: flex;
    flex-direction: column;
    padding: 16px 20px;
    background: rgba(18, 24, 38, 0.6);
    border: 1px solid var(--border-color);
    border-radius: var(--radius-md);
    transition: border-color 0.2s ease;
}

.metric-container:hover {
    border-color: rgba(99, 102, 241, 0.4);
}

.metric-label {
    font-size: 0.75rem;
    font-weight: 600;
    text-transform: uppercase;
    letter-spacing: 0.05em;
    color: var(--text-muted);
}

.metric-value {
    font-size: 1.9rem;
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

/* 10-Step Live Investigation Timeline */
.timeline-10-step {
    display: flex;
    flex-direction: column;
    gap: 12px;
    margin: 16px 0;
}

.step-card {
    background: rgba(15, 23, 42, 0.75);
    border: 1px solid var(--border-color);
    border-radius: var(--radius-md);
    padding: 14px 18px;
    display: flex;
    align-items: flex-start;
    gap: 16px;
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
    background: rgba(59, 130, 246, 0.2);
    border: 1px solid rgba(59, 130, 246, 0.4);
    color: #93C5FD;
    font-weight: 700;
    font-size: 0.85rem;
    display: flex;
    align-items: center;
    justify-content: center;
    flex-shrink: 0;
}

.step-badge-num.complete {
    background: rgba(16, 185, 129, 0.2);
    border-color: #10B981;
    color: #34D399;
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
    font-size: 0.92rem;
    font-weight: 600;
    color: #F8FAFC;
}

.step-agent {
    font-size: 0.72rem;
    color: #A78BFA;
    background: rgba(139, 92, 246, 0.15);
    padding: 2px 8px;
    border-radius: 999px;
    font-weight: 600;
}

.step-desc {
    font-size: 0.82rem;
    color: #94A3B8;
    line-height: 1.4;
}

.step-meta {
    display: flex;
    gap: 14px;
    font-size: 0.75rem;
    color: #64748B;
    margin-top: 6px;
    font-family: 'JetBrains Mono', monospace;
}

/* Explainable Score Drivers Card */
.score-breakdown-container {
    background: rgba(15, 23, 42, 0.8);
    border: 1px solid var(--border-color);
    border-radius: var(--radius-md);
    padding: 18px;
    margin-top: 14px;
}

.score-item {
    display: flex;
    justify-content: space-between;
    align-items: center;
    padding: 8px 0;
    border-bottom: 1px solid rgba(255, 255, 255, 0.04);
    font-size: 0.85rem;
}

.score-item:last-child {
    border-bottom: none;
}

.score-pts-positive {
    color: #34D399;
    font-weight: 700;
    font-family: 'JetBrains Mono', monospace;
}

.score-pts-negative {
    color: #F87171;
    font-weight: 700;
    font-family: 'JetBrains Mono', monospace;
}

/* Recommended Next Evidence Banner */
.uplift-banner {
    background: linear-gradient(90deg, rgba(16, 185, 129, 0.15) 0%, rgba(59, 130, 246, 0.15) 100%);
    border: 1px solid rgba(16, 185, 129, 0.35);
    border-radius: var(--radius-md);
    padding: 16px 20px;
    margin: 16px 0;
    display: flex;
    align-items: center;
    justify-content: space-between;
}

.uplift-badge {
    background: #10B981;
    color: #FFFFFF;
    font-weight: 800;
    font-size: 1.1rem;
    padding: 6px 14px;
    border-radius: var(--radius-sm);
    box-shadow: 0 0 15px rgba(16, 185, 129, 0.4);
}

/* Traceable Claim Popover / Box */
.traceable-claim {
    background: rgba(30, 41, 59, 0.6);
    border: 1px solid rgba(59, 130, 246, 0.25);
    border-radius: var(--radius-sm);
    padding: 10px 14px;
    margin-bottom: 8px;
    font-size: 0.85rem;
    display: flex;
    justify-content: space-between;
    align-items: center;
    cursor: pointer;
    transition: all 0.2s ease;
}

.traceable-claim:hover {
    border-color: #60A5FA;
    background: rgba(59, 130, 246, 0.12);
}

.source-badge {
    font-size: 0.72rem;
    color: #93C5FD;
    background: rgba(59, 130, 246, 0.2);
    padding: 2px 8px;
    border-radius: 4px;
    font-family: 'JetBrains Mono', monospace;
}

/* AI Chat Assistant Widget */
.chat-container {
    background: rgba(15, 23, 42, 0.9);
    border: 1px solid var(--border-color);
    border-radius: var(--radius-md);
    padding: 16px;
    margin-top: 16px;
}

.chat-bubble-user {
    background: rgba(59, 130, 246, 0.2);
    border: 1px solid rgba(59, 130, 246, 0.4);
    border-radius: 12px 12px 0 12px;
    padding: 10px 14px;
    margin: 8px 0;
    color: #F8FAFC;
    font-size: 0.88rem;
    max-width: 85%;
    margin-left: auto;
}

.chat-bubble-ai {
    background: rgba(30, 41, 59, 0.7);
    border: 1px solid var(--border-color);
    border-radius: 12px 12px 12px 0;
    padding: 12px 16px;
    margin: 8px 0;
    color: #E2E8F0;
    font-size: 0.88rem;
    max-width: 90%;
    line-height: 1.5;
}

.citation-box {
    margin-top: 8px;
    padding: 6px 10px;
    background: rgba(0, 0, 0, 0.3);
    border-left: 3px solid #3B82F6;
    border-radius: 0 4px 4px 0;
    font-size: 0.75rem;
    color: #94A3B8;
    font-family: 'JetBrains Mono', monospace;
}

/* Tag / Badge Chips */
.tag-chip {
    display: inline-flex;
    align-items: center;
    padding: 3px 9px;
    border-radius: 6px;
    font-size: 0.75rem;
    font-weight: 500;
    margin-right: 6px;
    margin-bottom: 6px;
    border: 1px solid rgba(255, 255, 255, 0.1);
}

.tag-blue { background: rgba(59, 130, 246, 0.15); color: #93C5FD; border-color: rgba(59, 130, 246, 0.3); }
.tag-green { background: rgba(16, 185, 129, 0.15); color: #6EE7B7; border-color: rgba(16, 185, 129, 0.3); }
.tag-purple { background: rgba(139, 92, 246, 0.15); color: #C4B5FD; border-color: rgba(139, 92, 246, 0.3); }
.tag-amber { background: rgba(245, 158, 11, 0.15); color: #FCD34D; border-color: rgba(245, 158, 11, 0.3); }
.tag-rose { background: rgba(244, 63, 94, 0.15); color: #FDA4AF; border-color: rgba(244, 63, 94, 0.3); }

/* Score Gauge Box */
.score-badge-huge {
    font-size: 3.2rem;
    font-weight: 900;
    background: linear-gradient(135deg, #10B981, #3B82F6);
    -webkit-background-clip: text;
    -webkit-text-fill-color: transparent;
    line-height: 1;
}

/* Sidebar Custom Styling */
[data-testid="stSidebar"] {
    background-color: #0A0D14 !important;
    border-right: 1px solid var(--border-color);
}
</style>
"""
