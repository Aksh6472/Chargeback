"""
Chargeback Evidence AI - Stripe & Linear Inspired Fintech Design System
Provides custom CSS, glassmorphism, responsive cards, micro-animations, and typography.
"""

FINTECH_CSS = """
<style>
/* Import Inter Font */
@import url('https://fonts.googleapis.com/css2?family=Inter:wght@300;400;500;600;700;800&family=JetBrains+Mono:wght@400;500&display=swap');

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

/* Hide Streamlit default decorations but keep sidebar toggle visible */
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

/* Custom top banner / app header */
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
    font-size: 1.1rem;
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
    transform: translateY(-2px);
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
    font-size: 2rem;
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

/* Multi-Agent Status Cards */
.agent-card {
    background: rgba(15, 23, 42, 0.8);
    border: 1px solid var(--border-color);
    border-radius: var(--radius-md);
    padding: 18px;
    margin-bottom: 14px;
    position: relative;
    overflow: hidden;
}

.agent-card.running {
    border-color: #3B82F6;
    box-shadow: 0 0 15px rgba(59, 130, 246, 0.2);
}

.agent-card.complete {
    border-color: rgba(16, 185, 129, 0.4);
}

.agent-card-header {
    display: flex;
    justify-content: space-between;
    align-items: center;
    margin-bottom: 10px;
}

.agent-title {
    font-size: 0.95rem;
    font-weight: 600;
    color: #F1F5F9;
    display: flex;
    align-items: center;
    gap: 10px;
}

.status-pill {
    font-size: 0.72rem;
    padding: 3px 10px;
    border-radius: 999px;
    font-weight: 600;
    letter-spacing: 0.03em;
    text-transform: uppercase;
}

.status-pill.complete {
    background: rgba(16, 185, 129, 0.15);
    color: #34D399;
    border: 1px solid rgba(16, 185, 129, 0.3);
}

.status-pill.running {
    background: rgba(59, 130, 246, 0.15);
    color: #60A5FA;
    border: 1px solid rgba(59, 130, 246, 0.3);
    animation: pulse 2s infinite;
}

.status-pill.queued {
    background: rgba(148, 163, 184, 0.15);
    color: #94A3B8;
    border: 1px solid rgba(148, 163, 184, 0.2);
}

@keyframes pulse {
    0%, 100% { opacity: 1; }
    50% { opacity: 0.5; }
}

.agent-meta-row {
    display: flex;
    gap: 20px;
    font-size: 0.78rem;
    color: var(--text-muted);
    margin: 8px 0;
}

.agent-output-box {
    background: rgba(0, 0, 0, 0.3);
    border: 1px solid rgba(255, 255, 255, 0.05);
    border-radius: var(--radius-sm);
    padding: 10px 14px;
    font-size: 0.82rem;
    color: #CBD5E1;
    font-family: 'JetBrains Mono', monospace;
    line-height: 1.45;
}

/* Timeline Components */
.timeline-step {
    position: relative;
    padding-left: 36px;
    padding-bottom: 24px;
    border-left: 2px solid rgba(59, 130, 246, 0.3);
}

.timeline-step:last-child {
    border-left: 2px transparent;
    padding-bottom: 0;
}

.timeline-dot {
    position: absolute;
    left: -7px;
    top: 2px;
    width: 12px;
    height: 12px;
    border-radius: 50%;
    background: #3B82F6;
    box-shadow: 0 0 10px #3B82F6;
}

.timeline-title {
    font-size: 0.9rem;
    font-weight: 600;
    color: #F8FAFC;
}

.timeline-time {
    font-size: 0.75rem;
    color: #94A3B8;
    margin-bottom: 4px;
}

.timeline-desc {
    font-size: 0.82rem;
    color: #CBD5E1;
    line-height: 1.4;
}

.timeline-badge {
    display: inline-block;
    background: rgba(255, 255, 255, 0.06);
    border: 1px solid rgba(255, 255, 255, 0.1);
    color: #93C5FD;
    padding: 2px 8px;
    border-radius: 4px;
    font-size: 0.72rem;
    margin-top: 6px;
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
