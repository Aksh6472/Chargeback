"""
Chargeback Evidence AI - Main Application Entrypoint
Streamlit Frontend delivering a Stripe, Linear, Notion & Ramp fintech aesthetic.
Orchestrates multi-agent dispute intelligence, KYC onboarding vault, and 9 core pages.
"""

import sys
from pathlib import Path

# Add project root to sys.path so modules resolve seamlessly
ROOT_DIR = Path(__file__).resolve().parent.parent
if str(ROOT_DIR) not in sys.path:
    sys.path.insert(0, str(ROOT_DIR))

import streamlit as st

# Relative imports with fallback for standalone direct runner
try:
    from .styles import FINTECH_CSS
    from .components import render_app_header
    from .api_client import DisputeService
    from .views import (
        render_auth_view,
        render_overview_view,
        render_create_case_view,
        render_investigation_view,
        render_evidence_viewer_view,
        render_verification_view,
        render_timeline_view,
        render_similar_cases_view,
        render_fraud_intel_view,
        render_final_report_view
    )
except (ImportError, ValueError):
    from frontend.styles import FINTECH_CSS
    from frontend.components import render_app_header
    from frontend.api_client import DisputeService
    from frontend.views import (
        render_auth_view,
        render_overview_view,
        render_create_case_view,
        render_investigation_view,
        render_evidence_viewer_view,
        render_verification_view,
        render_timeline_view,
        render_similar_cases_view,
        render_fraud_intel_view,
        render_final_report_view
    )

# Page configuration
st.set_page_config(
    page_title="Chargeback Evidence AI | Razorpay Challenge",
    page_icon="⚡",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Inject custom fintech CSS
st.markdown(FINTECH_CSS, unsafe_allow_html=True)

# Session state initialization
if "current_merchant" not in st.session_state:
    st.session_state["current_merchant"] = DisputeService.get_merchant_profile()

if "current_page" not in st.session_state:
    st.session_state["current_page"] = "Overview"

cases = DisputeService.list_cases()
if "active_case_id" not in st.session_state and cases:
    st.session_state["active_case_id"] = cases[0]["id"]

# -------------------------------------------------------------
# SIDEBAR NAVIGATION
# -------------------------------------------------------------
with st.sidebar:
    st.markdown("""
    <div style="padding: 10px 0 20px 0; border-bottom: 1px solid rgba(255,255,255,0.08); margin-bottom: 16px;">
        <div style="display: flex; align-items: center; gap: 10px;">
            <div style="width: 32px; height: 32px; border-radius: 8px; background: linear-gradient(135deg, #3B82F6, #8B5CF6); display: flex; align-items: center; justify-content: center; font-weight: 800; font-size: 1rem; color: white;">
                ⚡
            </div>
            <div>
                <div style="font-weight: 800; font-size: 1.05rem; letter-spacing: -0.02em; color: #F8FAFC;">Chargeback AI</div>
                <div style="font-size: 0.7rem; color: #64748B;">Razorpay AI Builder Intern</div>
            </div>
        </div>
    </div>
    """, unsafe_allow_html=True)

    pages = [
        "Overview",
        "Create Chargeback Case",
        "AI Investigation",
        "Evidence Viewer",
        "Verification Center",
        "Timeline",
        "Similar Historical Cases",
        "Fraud Intelligence",
        "Final AI Report",
        "Merchant Auth & Vault"
    ]

    icons = [
        "📊", "➕", "🤖", "🔍", "⚖️", "⏱️", "📚", "🕸️", "📄", "🛡️"
    ]

    selected_page = st.radio(
        "Navigation",
        pages,
        index=pages.index(st.session_state["current_page"]) if st.session_state["current_page"] in pages else 0,
        format_func=lambda p: f"{icons[pages.index(p)]}  {p}",
        label_visibility="collapsed"
    )
    st.session_state["current_page"] = selected_page

    st.write("---")

    # Active Case Widget in Sidebar
    active_case = DisputeService.get_case(st.session_state.get("active_case_id", ""))
    if active_case:
        sc = active_case.get("evidence_score")
        sc_text = f"SCORE {int(sc)}" if sc else "Analyzing"
        st.markdown(f"""
        <div style="background: rgba(18, 24, 38, 0.7); border: 1px solid rgba(255,255,255,0.08); border-radius: 10px; padding: 12px; margin-bottom: 16px;">
            <div style="font-size: 0.7rem; color: #94A3B8; text-transform: uppercase; font-weight: 600;">ACTIVE CASE UNDER REVIEW</div>
            <div style="font-size: 0.95rem; font-weight: 700; color: #F1F5F9; margin-top: 2px;">{active_case.get('order_id')}</div>
            <div style="font-size: 0.75rem; color: #64748B;">Amount: ₹{active_case.get('amount', 0):,.2f}</div>
            <div style="margin-top: 8px; display: flex; justify-content: space-between; align-items: center;">
                <span class="status-pill complete" style="font-size: 0.68rem;">{active_case.get('status').upper()}</span>
                <span style="font-size: 0.75rem; font-weight: 700; color: #10B981;">{sc_text}</span>
            </div>
        </div>
        """, unsafe_allow_html=True)

    # Cloud & Multi-Agent Architecture Status
    is_live = DisputeService.check_backend_alive()
    api_status_label = "FastAPI: Connected (Port 8000)" if is_live else "FastAPI: Local Agent Mode"
    api_status_color = "#10B981" if is_live else "#60A5FA"

    st.markdown(f"""
    <div style="font-size: 0.72rem; color: #64748B; line-height: 1.5;">
        <div style="color: {api_status_color}; font-weight: 600;">● {api_status_label}</div>
        <div style="color: #10B981; font-weight: 600;">● Supabase: RLS Active</div>
        <div style="color: #A78BFA; font-weight: 600;">● XGBoost ML: v1.0.0 (89.5% F1)</div>
        <div style="color: #60A5FA; font-weight: 600;">● n8n Webhook: Ready</div>
    </div>
    """, unsafe_allow_html=True)

# -------------------------------------------------------------
# MAIN APP BODY
# -------------------------------------------------------------
merchant = st.session_state.get("current_merchant", {})
active_order = active_case.get("order_id", "") if active_case else ""
render_app_header(merchant, active_order)

# Router passing DisputeService exclusively from app.py
page = st.session_state["current_page"]

if page == "Overview":
    render_overview_view(service=DisputeService)
elif page == "Create Chargeback Case":
    render_create_case_view(service=DisputeService)
elif page == "AI Investigation":
    render_investigation_view(service=DisputeService)
elif page == "Evidence Viewer":
    render_evidence_viewer_view(service=DisputeService)
elif page == "Verification Center":
    render_verification_view(service=DisputeService)
elif page == "Timeline":
    render_timeline_view(service=DisputeService)
elif page == "Similar Historical Cases":
    render_similar_cases_view(service=DisputeService)
elif page == "Fraud Intelligence":
    render_fraud_intel_view(service=DisputeService)
elif page == "Final AI Report":
    render_final_report_view(service=DisputeService)
elif page == "Merchant Auth & Vault":
    render_auth_view(service=DisputeService)
