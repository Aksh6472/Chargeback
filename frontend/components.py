"""
Chargeback Evidence AI - Reusable UI Components
Stripe & Linear inspired HTML/CSS components with rich fintech aesthetic.
All HTML is safely unindented to prevent Markdown code block escaping.
"""

import streamlit as st
import plotly.graph_objects as go
import textwrap
from typing import Dict, Any, List, Optional


def render_html(html_code: str):
    """
    Renders HTML cleanly without Markdown code-block indentation bugs.
    Uses st.html for native HTML injection without CommonMark code-block escaping.
    """
    if hasattr(st, "html"):
        st.html(html_code)
    else:
        st.markdown(textwrap.dedent(html_code).strip(), unsafe_allow_html=True)


def render_app_header(current_merchant: Dict[str, Any], active_order_id: str = "", active_portal: str = "Merchant"):
    portal_color = "#3B82F6" if active_portal == "Merchant" else "#10B981"
    merchant_name = current_merchant.get("name", "Apex Retailers Pvt Ltd") if current_merchant else "Apex Retailers Pvt Ltd"
    
    html = f"""
<div class="app-header-container">
    <div style="display: flex; align-items: center; gap: 14px;">
        <div style="width: 38px; height: 38px; border-radius: 10px; background: linear-gradient(135deg, {portal_color}, #6366F1); display: flex; align-items: center; justify-content: center; font-weight: 800; font-size: 1.2rem; color: white;">
            ⚡
        </div>
        <div>
            <div class="brand-badge">CHARGEBACK EVIDENCE AI</div>
            <div style="font-size: 0.76rem; color: #94A3B8;">Autonomous Multi-Agent Dispute Operating System</div>
        </div>
    </div>
    <div style="display: flex; align-items: center; gap: 12px;">
        <span class="sub-tag" style="background: rgba(59, 130, 246, 0.2); border-color: {portal_color}; color: #93C5FD;">{active_portal.upper()} PORTAL</span>
        <div style="background: rgba(255,255,255,0.06); padding: 5px 12px; border-radius: 8px; border: 1px solid rgba(255,255,255,0.08); font-size: 0.78rem; color: #E2E8F0;">
            🏢 <b>{merchant_name}</b>
        </div>
    </div>
</div>
"""
    render_html(html)


def render_case_status_tracker(current_status: str):
    """
    Renders horizontal 6-step lifecycle tracker:
    New -> Investigating -> Evidence Ready -> Submitted -> Won / Lost
    """
    lifecycle = [
        ("new", "1. New"),
        ("investigating", "2. Investigating"),
        ("evidence_ready", "3. Evidence Ready"),
        ("submitted", "4. Submitted"),
        ("won", "5. Won")
    ]
    
    status_lower = current_status.lower() if current_status else "new"
    status_order = ["new", "investigating", "evidence_ready", "submitted", "won"]
    current_idx = status_order.index(status_lower) if status_lower in status_order else 0
    if status_lower == "lost":
        lifecycle[4] = ("lost", "5. Lost")
        current_idx = 4

    html_steps = []
    for i, (key, label) in enumerate(lifecycle):
        if i < current_idx:
            step_class = "lifecycle-step completed"
            icon = "✓"
        elif i == current_idx:
            step_class = "lifecycle-step active"
            icon = "●"
        else:
            step_class = "lifecycle-step"
            icon = str(i + 1)

        html_steps.append(
            f'<div class="{step_class}"><div class="lifecycle-dot">{icon}</div><span>{label}</span></div>'
        )
        if i < len(lifecycle) - 1:
            div_class = "lifecycle-divider active" if i < current_idx else "lifecycle-divider"
            html_steps.append(f'<div class="{div_class}"></div>')

    tracker_html = f'<div class="lifecycle-tracker">{"".join(html_steps)}</div>'
    render_html(tracker_html)


def render_kpi_card(title: str, value: str, trend: str, is_up: bool = True):
    trend_class = "trend-up" if is_up else "trend-neutral"
    arrow = "↑" if is_up else "→"
    html = f"""
<div class="metric-container">
    <div class="metric-label">{title}</div>
    <div class="metric-value">{value}</div>
    <div class="metric-trend {trend_class}">
        <span>{arrow} {trend}</span>
    </div>
</div>
"""
    render_html(html)


def render_agent_card(agent_name: str, status: str, progress: int, exec_time: float, confidence: float, preview: str):
    icon_map = {
        "Document Agent": "🗂️",
        "OCR Agent": "📄",
        "NLP Agent": "🧠",
        "Verification Agent": "⚖️",
        "ML Scoring Agent": "🎯",
        "RAG Agent": "📚",
        "Narrative Agent": "✍️",
        "Gemini Report Agent": "✨"
    }
    icon = icon_map.get(agent_name, "🤖")
    pill_class = "complete" if status.lower() == "complete" else ("running" if status.lower() == "running" else "queued")

    html = f"""
<div class="agent-card {pill_class}">
    <div class="agent-card-header">
        <div class="agent-title">
            <span style="font-size: 1.2rem;">{icon}</span>
            <span>{agent_name}</span>
        </div>
        <span class="status-pill {pill_class}">{status}</span>
    </div>
    <div style="height: 4px; background: rgba(255,255,255,0.06); border-radius: 2px; overflow: hidden; margin: 8px 0 12px 0;">
        <div style="width: {progress}%; height: 100%; background: linear-gradient(90deg, #3B82F6, #10B981); border-radius: 2px;"></div>
    </div>
    <div class="agent-meta-row">
        <span>⏱️ Latency: <b>{exec_time:.2f}s</b></span>
        <span>🎯 Confidence: <b>{int(confidence*100)}%</b></span>
        <span>📊 Status: <b>{progress}% Done</b></span>
    </div>
    <div class="agent-output-box">
        {preview}
    </div>
</div>
"""
    render_html(html)


def render_explainable_score_card(ml_score: Dict[str, Any]):
    score = ml_score.get("evidence_strength_score", ml_score.get("evidence_score", 85))
    win_prob = ml_score.get("win_probability", 0.88)
    dispute_type = ml_score.get("dispute_classification", "Product Not Received")
    breakdown = ml_score.get("score_breakdown", [])
    label = ml_score.get("score_label", "Strong Evidence" if score >= 80 else "Moderate Strength")

    items_html = []
    for item in breakdown:
        pts = item.get("points", 0)
        pts_str = f"+{pts} pts" if pts > 0 else f"{pts} pts"
        pts_class = "score-pts-positive" if pts > 0 else "score-pts-negative"
        icon = "✅" if pts > 0 else "⚠️"
        items_html.append(f"""
<div class="score-item">
    <div>
        <span>{icon} <b>{item.get('name', '')}</b></span>
        <div style="font-size: 0.76rem; color: #94A3B8;">{item.get('explanation', '')}</div>
    </div>
    <span class="{pts_class}">{pts_str}</span>
</div>
""")

    html = f"""
<div class="score-breakdown-container">
    <div style="display: flex; justify-content: space-between; align-items: center; margin-bottom: 12px;">
        <div>
            <span style="font-size: 0.8rem; text-transform: uppercase; color: #94A3B8; font-weight: 700;">Dispute Classification</span>
            <div style="font-size: 1.1rem; font-weight: 700; color: #60A5FA;">🏷️ {dispute_type}</div>
        </div>
        <div style="text-align: right;">
            <span style="font-size: 0.8rem; text-transform: uppercase; color: #94A3B8; font-weight: 700;">Predicted Win Rate</span>
            <div style="font-size: 1.1rem; font-weight: 800; color: #34D399;">{int(win_prob*100)}%</div>
        </div>
    </div>
    <div style="display: flex; align-items: center; justify-content: space-between; background: rgba(255,255,255,0.04); padding: 8px 12px; border-radius: 8px; margin-bottom: 12px;">
        <span style="font-size: 0.85rem; color: #CBD5E1;">Overall Score: <b style="color: #10B981;">{score}/100</b></span>
        <span class="sub-tag" style="background: rgba(16, 185, 129, 0.15); color: #6EE7B7; border-color: rgba(16, 185, 129, 0.3);">{label}</span>
    </div>
    <div style="font-size: 0.82rem; font-weight: 600; color: #CBD5E1; margin: 12px 0 8px 0;">Explainable AI Score Drivers:</div>
    {''.join(items_html)}
</div>
"""
    render_html(html)


def render_recommended_next_evidence(rec: Dict[str, Any]):
    doc = rec.get("recommended_document", "Courier Proof of Delivery (POD)")
    uplift = rec.get("win_probability_uplift_pct", 14)
    reason = rec.get("reason", "Proves physical doorstep handover under card network compelling evidence rules.")
    alt = rec.get("suggested_alternative", "Customer Delivery Confirmation Email")

    html = f"""
<div class="uplift-banner">
    <div>
        <div style="font-size: 0.76rem; text-transform: uppercase; letter-spacing: 0.05em; color: #34D399; font-weight: 700;">🚀 Recommended Next Evidence</div>
        <div style="font-size: 1.05rem; font-weight: 700; color: #F8FAFC; margin: 2px 0;">{doc}</div>
        <div style="font-size: 0.82rem; color: #94A3B8;">{reason} &bull; <span style="color: #93C5FD;">Alternative: {alt}</span></div>
    </div>
    <div style="text-align: right;">
        <div class="uplift-badge">+{uplift}%</div>
        <div style="font-size: 0.72rem; color: #94A3B8; margin-top: 4px;">Win Rate Uplift</div>
    </div>
</div>
"""
    render_html(html)


def render_traceable_claim(claim_title: str, entity_type: str, source_doc: str, page_num: int, ocr_conf: float, ent_conf: float):
    html = f"""
<div class="traceable-claim">
    <div>
        <span style="font-weight: 600; color: #F8FAFC;">{claim_title}</span>
        <div style="font-size: 0.76rem; color: #94A3B8;">Entity: <code>{entity_type}</code> &bull; OCR Conf: <b>{int(ocr_conf*100)}%</b> &bull; NLP Conf: <b>{int(ent_conf*100)}%</b></div>
    </div>
    <span class="source-badge">📄 {source_doc} (p.{page_num})</span>
</div>
"""
    render_html(html)


def render_score_radial(score: int, win_prob: float):
    fig = go.Figure(go.Indicator(
        mode="gauge+number",
        value=score,
        domain={'x': [0, 1], 'y': [0, 1]},
        title={'text': "EVIDENCE STRENGTH SCORE", 'font': {'size': 13, 'color': '#94A3B8'}},
        gauge={
            'axis': {'range': [0, 100], 'tickwidth': 1, 'tickcolor': "#475569"},
            'bar': {'color': "#10B981" if score >= 80 else "#3B82F6"},
            'bgcolor': "rgba(255, 255, 255, 0.05)",
            'borderwidth': 1,
            'bordercolor': "rgba(255, 255, 255, 0.1)",
            'steps': [
                {'range': [0, 50], 'color': 'rgba(239, 68, 68, 0.15)'},
                {'range': [50, 80], 'color': 'rgba(245, 158, 11, 0.15)'},
                {'range': [80, 100], 'color': 'rgba(16, 185, 129, 0.15)'}
            ],
            'threshold': {
                'line': {'color': "#34D399", 'width': 3},
                'thickness': 0.8,
                'value': score
            }
        }
    ))
    fig.update_layout(
        paper_bgcolor='rgba(0,0,0,0)',
        plot_bgcolor='rgba(0,0,0,0)',
        font={'color': "#F8FAFC", 'family': "Inter"},
        height=220,
        margin=dict(l=20, r=20, t=30, b=10)
    )
    st.plotly_chart(fig, use_container_width=True)
