"""
Chargeback Evidence AI - Reusable Stitch UI Components
Institutional, minimalist fintech components for metrics, status tracking, agent cards,
explainable score factors, source traceability, and evidence preview dockets.
"""

import streamlit as st
import plotly.graph_objects as go
import textwrap
from typing import Dict, Any, List, Optional


def render_html(html_code: str):
    """
    Renders HTML cleanly without Markdown code-block indentation bugs.
    Uses st.html for native HTML injection.
    """
    if hasattr(st, "html"):
        st.html(html_code)
    else:
        st.markdown(textwrap.dedent(html_code).strip(), unsafe_allow_html=True)


def render_app_header(current_merchant: Optional[Dict[str, Any]] = None, active_order_id: str = "", active_portal: str = "Merchant"):
    """
    Renders the Stitch top navigation bar with search context, live production telemetry, and user profile pill.
    """
    m_name = (current_merchant.get("name") if current_merchant else None) or ("Apex Retailers Pvt Ltd" if active_portal == "Merchant" else "Cardholder")
    role_label = active_portal.upper()

    html = f"""
<div class="stitch-topbar">
    <div style="display: flex; align-items: center; gap: 14px;">
        <div style="display: flex; align-items: center; gap: 8px;">
            <div style="width: 32px; height: 32px; border-radius: 8px; background: #1A242C; color: #FFFFFF; display: flex; align-items: center; justify-content: center; font-weight: 800; font-size: 1rem;">
                <span class="material-symbols-outlined" style="font-size: 18px;">shield</span>
            </div>
            <div>
                <div style="font-weight: 800; font-size: 0.98rem; color: #191C1E; letter-spacing: -0.02em;">Evidence AI</div>
                <div style="font-size: 0.72rem; color: #64748B; font-weight: 500;">Dispute Shield &bull; {role_label} Workspace</div>
            </div>
        </div>
    </div>
    <div style="display: flex; align-items: center; gap: 12px;">
        <div class="stitch-pill stitch-pill-success" style="font-size: 0.7rem; padding: 4px 10px;">
            <span class="stitch-pill-dot"></span>
            <span>Production &bull; Live Feed</span>
        </div>
        <div style="background: #F2F4F6; border: 1px solid #E5E7EB; padding: 4px 12px; border-radius: 8px; font-size: 0.8rem; color: #191C1E; font-weight: 600; display: flex; align-items: center; gap: 6px;">
            <span class="material-symbols-outlined" style="font-size: 16px; color: #64748B;">{'store' if active_portal == 'Merchant' else 'person'}</span>
            <span>{m_name}</span>
        </div>
    </div>
</div>
"""
    render_html(html)


def render_case_status_tracker(current_status: str):
    """
    Renders horizontal 5-step lifecycle tracker matching Stitch UI:
    New -> Collecting Evidence -> Ready to Submit -> Submitted -> Closed (Won)
    """
    lifecycle = [
        ("new", "New"),
        ("investigating", "Collecting Evidence"),
        ("evidence_ready", "Ready to Submit"),
        ("submitted", "Submitted"),
        ("won", "Closed (Won)")
    ]
    
    status_lower = (current_status or "new").lower()
    status_order = ["new", "investigating", "evidence_ready", "submitted", "won"]
    current_idx = status_order.index(status_lower) if status_lower in status_order else 0
    if status_lower == "lost":
        lifecycle[4] = ("lost", "Closed (Lost)")
        current_idx = 4

    html_steps = []
    for i, (key, label) in enumerate(lifecycle):
        if i < current_idx:
            step_class = "stitch-step completed"
            icon = '<span class="material-symbols-outlined" style="font-size: 14px;">check</span>'
        elif i == current_idx:
            step_class = "stitch-step active"
            icon = str(i + 1)
        else:
            step_class = "stitch-step"
            icon = str(i + 1)

        html_steps.append(
            f'<div class="{step_class}"><div class="stitch-step-num">{icon}</div><span>{label}</span></div>'
        )
        if i < len(lifecycle) - 1:
            div_class = "stitch-divider completed" if i < current_idx else "stitch-divider"
            html_steps.append(f'<div class="{div_class}"></div>')

    tracker_html = f'<div class="stitch-lifecycle">{"".join(html_steps)}</div>'
    render_html(tracker_html)


def render_kpi_card(title: str, value: str, trend: str, is_up: bool = True, footer_label: str = "Active Rails", footer_val: str = "Auto-Synced", icon_name: str = "account_balance_wallet"):
    """
    Renders clean Stitch KPI card with header icon, primary value, trend badge, and footer status strip.
    """
    pill_class = "stitch-pill-success" if is_up else "stitch-pill-warning"
    arrow = "arrow_upward" if is_up else "schedule"
    
    html = f"""
<div class="stitch-kpi-card">
    <div>
        <div class="stitch-kpi-header">
            <span>{title}</span>
            <div class="stitch-kpi-icon">
                <span class="material-symbols-outlined" style="font-size: 18px;">{icon_name}</span>
            </div>
        </div>
        <div class="stitch-kpi-value">{value}</div>
        <div style="margin-top: 4px;">
            <span class="stitch-pill {pill_class}">
                <span class="material-symbols-outlined" style="font-size: 13px;">{arrow}</span>
                <span>{trend}</span>
            </span>
        </div>
    </div>
    <div class="stitch-kpi-footer">
        <span style="text-transform: uppercase; font-size: 0.7rem; letter-spacing: 0.04em;">{footer_label}</span>
        <span class="font-mono" style="font-weight: 600; color: #191C1E;">{footer_val}</span>
    </div>
</div>
"""
    render_html(html)


def render_agent_card(agent_name: str, status: str, progress: int, exec_time: float, confidence: float, preview: str):
    icon_map = {
        "Document Agent": "folder_open",
        "OCR Agent": "document_scanner",
        "NLP Agent": "psychology",
        "Verification Agent": "verified",
        "ML Scoring Agent": "insights",
        "Dispute Intelligence Agent": "travel_explore",
        "RAG Agent": "travel_explore",
        "Narrative Agent": "edit_note",
        "Report Agent": "picture_as_pdf"
    }
    icon = icon_map.get(agent_name, "smart_toy")
    pill_class = "stitch-pill-success" if status.lower() == "complete" else "stitch-pill-info"

    html = f"""
<div class="stitch-card" style="margin-bottom: 12px; padding: 1.25rem;">
    <div style="display: flex; justify-content: space-between; align-items: center; margin-bottom: 8px;">
        <div style="display: flex; align-items: center; gap: 10px;">
            <div style="width: 32px; height: 32px; border-radius: 8px; background: #EDEEF0; color: #2F3A42; display: flex; align-items: center; justify-content: center;">
                <span class="material-symbols-outlined" style="font-size: 18px;">{icon}</span>
            </div>
            <span style="font-weight: 700; font-size: 0.95rem; color: #191C1E;">{agent_name}</span>
        </div>
        <span class="stitch-pill {pill_class}">{status}</span>
    </div>
    <div style="height: 4px; background: #EDEEF0; border-radius: 2px; overflow: hidden; margin: 8px 0 10px 0;">
        <div style="width: {progress}%; height: 100%; background: #1A242C; border-radius: 2px;"></div>
    </div>
    <div style="display: flex; justify-content: space-between; font-size: 0.78rem; color: #64748B; margin-bottom: 8px;">
        <span>Latency: <b style="color: #191C1E;">{exec_time:.2f}s</b></span>
        <span>Quality Confidence: <b style="color: #10B981;">{int(confidence*100)}%</b></span>
        <span>Completion: <b style="color: #191C1E;">{progress}%</b></span>
    </div>
    <div style="background: #F8F9FB; border: 1px solid #E5E7EB; border-radius: 6px; padding: 10px 12px; font-size: 0.82rem; color: #43474B; line-height: 1.45;">
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
        pts_color = "#10B981" if pts > 0 else "#EF4444"
        icon_name = "check_circle" if pts > 0 else "warning"
        items_html.append(f"""
<div style="display: flex; justify-content: space-between; align-items: center; padding: 8px 0; border-bottom: 1px solid #F2F4F6;">
    <div style="display: flex; align-items: flex-start; gap: 8px;">
        <span class="material-symbols-outlined" style="font-size: 16px; color: {pts_color}; margin-top: 1px;">{icon_name}</span>
        <div>
            <span style="font-weight: 600; font-size: 0.86rem; color: #191C1E;">{item.get('name', '')}</span>
            <div style="font-size: 0.76rem; color: #64748B;">{item.get('explanation', '')}</div>
        </div>
    </div>
    <span class="font-mono" style="font-weight: 700; font-size: 0.84rem; color: {pts_color};">{pts_str}</span>
</div>
""")

    html = f"""
<div class="stitch-card" style="padding: 1.25rem;">
    <div style="display: flex; justify-content: space-between; align-items: center; margin-bottom: 12px;">
        <div>
            <span style="font-size: 0.72rem; text-transform: uppercase; color: #64748B; font-weight: 700; letter-spacing: 0.05em;">Dispute Classification</span>
            <div style="font-size: 1.05rem; font-weight: 700; color: #191C1E;">{dispute_type}</div>
        </div>
        <div style="text-align: right;">
            <span style="font-size: 0.72rem; text-transform: uppercase; color: #64748B; font-weight: 700; letter-spacing: 0.05em;">Win Probability</span>
            <div style="font-size: 1.15rem; font-weight: 800; color: #10B981;">{int(win_prob*100)}%</div>
        </div>
    </div>
    <div style="display: flex; align-items: center; justify-content: space-between; background: #F8F9FB; border: 1px solid #E5E7EB; padding: 8px 12px; border-radius: 8px; margin-bottom: 12px;">
        <span style="font-size: 0.85rem; color: #191C1E; font-weight: 600;">Overall Score: <b style="color: #10B981;">{score}/100</b></span>
        <span class="stitch-pill stitch-pill-success">{label}</span>
    </div>
    <div style="font-size: 0.78rem; font-weight: 700; color: #64748B; text-transform: uppercase; letter-spacing: 0.05em; margin: 12px 0 6px 0;">Evidence Score Factors:</div>
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
<div style="background: #ECFDF5; border: 1px solid #A7F3D0; border-radius: 10px; padding: 14px 16px; margin-top: 10px; display: flex; justify-content: space-between; align-items: center; gap: 12px;">
    <div>
        <div style="font-size: 0.72rem; text-transform: uppercase; letter-spacing: 0.06em; color: #065F46; font-weight: 700;">🚀 Recommended Next Evidence</div>
        <div style="font-size: 0.98rem; font-weight: 700; color: #065F46; margin: 2px 0;">{doc}</div>
        <div style="font-size: 0.78rem; color: #047857;">{reason} &bull; <span style="font-weight: 500;">Alt: {alt}</span></div>
    </div>
    <div style="text-align: right; shrink-0;">
        <div class="stitch-pill stitch-pill-success" style="font-size: 0.86rem; padding: 4px 10px;">+{uplift}%</div>
        <div style="font-size: 0.68rem; color: #065F46; font-weight: 600; margin-top: 2px;">Win Uplift</div>
    </div>
</div>
"""
    render_html(html)


def render_traceable_claim(claim_title: str, entity_type: str, source_doc: str, page_num: int, ocr_conf: float, ent_conf: float):
    html = f"""
<div style="background: #FFFFFF; border: 1px solid #E5E7EB; border-radius: 8px; padding: 10px 14px; margin-bottom: 8px; display: flex; justify-content: space-between; align-items: center;">
    <div>
        <span style="font-weight: 600; color: #191C1E; font-size: 0.88rem;">{claim_title}</span>
        <div style="font-size: 0.76rem; color: #64748B; margin-top: 2px;">
            Field: <code>{entity_type}</code> &bull; OCR Clarity: <b style="color: #10B981;">{int(ocr_conf*100)}%</b> &bull; NLP Confidence: <b style="color: #10B981;">{int(ent_conf*100)}%</b>
        </div>
    </div>
    <span class="stitch-pill stitch-pill-neutral">📄 {source_doc} (p.{page_num})</span>
</div>
"""
    render_html(html)


def render_score_radial(score: int, win_prob: float):
    """
    Renders clean Plotly gauge styled with Stitch neutral palette and emerald highlights.
    """
    fig = go.Figure(go.Indicator(
        mode="gauge+number",
        value=score,
        domain={'x': [0, 1], 'y': [0, 1]},
        title={'text': "CASE READINESS SCORE", 'font': {'size': 12, 'color': '#64748B', 'family': 'Inter'}},
        number={'font': {'size': 38, 'color': '#191C1E', 'family': 'Inter'}, 'suffix': "%"},
        gauge={
            'axis': {'range': [0, 100], 'tickwidth': 1, 'tickcolor': "#CBD5E1"},
            'bar': {'color': "#1A242C"},
            'bgcolor': "#F2F4F6",
            'borderwidth': 1,
            'bordercolor': "#E5E7EB",
            'steps': [
                {'range': [0, 50], 'color': '#FEE2E2'},
                {'range': [50, 80], 'color': '#FEF3C7'},
                {'range': [80, 100], 'color': '#ECFDF5'}
            ],
            'threshold': {
                'line': {'color': "#10B981", 'width': 3},
                'thickness': 0.8,
                'value': score
            }
        }
    ))
    fig.update_layout(
        paper_bgcolor='rgba(0,0,0,0)',
        plot_bgcolor='rgba(0,0,0,0)',
        font={'color': "#191C1E", 'family': "Inter"},
        height=190,
        margin=dict(l=15, r=15, t=25, b=10)
    )
    st.plotly_chart(fig, use_container_width=True)
