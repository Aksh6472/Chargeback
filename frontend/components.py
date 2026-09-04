"""
Chargeback Evidence AI - Reusable UI Components
Stripe & Linear inspired HTML/CSS components with rich fintech aesthetic.
"""

import streamlit as st
import plotly.graph_objects as go
from typing import Dict, Any, List

def render_app_header(current_merchant: Dict[str, Any], active_order_id: str = ""):
    st.markdown(f"""
    <div class="app-header-container">
        <div style="display: flex; align-items: center; gap: 14px;">
            <div style="width: 38px; height: 38px; border-radius: 10px; background: linear-gradient(135deg, #3B82F6, #6366F1); display: flex; align-items: center; justify-content: center; font-weight: 800; font-size: 1.2rem; color: white;">
                ⚡
            </div>
            <div>
                <div class="brand-badge">CHARGEBACK EVIDENCE AI</div>
                <div style="font-size: 0.76rem; color: #94A3B8;">Razorpay AI Builder Intern Challenge &bull; Multi-Agent Dispute Intelligence</div>
            </div>
        </div>
        <div style="display: flex; align-items: center; gap: 12px;">
            <span class="sub-tag">LIVE ARBITRATION</span>
            <div style="background: rgba(255,255,255,0.06); padding: 5px 12px; border-radius: 8px; border: 1px solid rgba(255,255,255,0.08); font-size: 0.78rem; color: #E2E8F0;">
                🏢 <b>{current_merchant.get('name', 'Apex Retailers')}</b>
            </div>
        </div>
    </div>
    """, unsafe_allow_html=True)

def render_kpi_card(title: str, value: str, trend: str, is_up: bool = True):
    trend_class = "trend-up" if is_up else "trend-neutral"
    arrow = "↑" if is_up else "→"
    st.markdown(f"""
    <div class="metric-container">
        <div class="metric-label">{title}</div>
        <div class="metric-value">{value}</div>
        <div class="metric-trend {trend_class}">
            <span>{arrow} {trend}</span>
        </div>
    </div>
    """, unsafe_allow_html=True)

def render_agent_card(agent_name: str, status: str, progress: int, exec_time: float, confidence: float, preview: str):
    icon_map = {
        "OCR Agent": "📄",
        "NLP Agent": "🧠",
        "Verification Agent": "⚖️",
        "ML Scoring Agent": "🎯",
        "RAG Agent": "📚",
        "Gemini Report Agent": "✨"
    }
    icon = icon_map.get(agent_name, "🤖")
    pill_class = "complete" if status.lower() == "complete" else ("running" if status.lower() == "running" else "queued")

    st.markdown(f"""
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
    """, unsafe_allow_html=True)

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
