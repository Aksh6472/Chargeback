import sys
from pathlib import Path

# Add project root to sys.path so modules resolve seamlessly
ROOT_DIR = Path(__file__).resolve().parent.parent
if str(ROOT_DIR) not in sys.path:
    sys.path.insert(0, str(ROOT_DIR))

import streamlit as st
import textwrap

from frontend.styles import FINTECH_CSS
from frontend.components import render_app_header, render_html
from frontend.api_client import DisputeService
from frontend.views import (
    render_auth_view,
    render_overview_view,
    render_create_case_view,
    render_customer_portal_view,
    render_ai_agents_view,
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
    page_title="Chargeback Evidence AI | Autonomous Dispute OS",
    page_icon="⚡",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Inject custom fintech CSS
st.markdown(FINTECH_CSS, unsafe_allow_html=True)

# Session state initialization
if "current_merchant" not in st.session_state:
    st.session_state["current_merchant"] = DisputeService.get_merchant_profile()

if "active_portal" not in st.session_state:
    st.session_state["active_portal"] = "Merchant"

if "current_page" not in st.session_state:
    st.session_state["current_page"] = "Overview"

cases = DisputeService.list_cases()
if "active_case_id" not in st.session_state and cases:
    st.session_state["active_case_id"] = cases[0]["id"]


# -------------------------------------------------------------
# LANDING SCREEN (When in Landing / Auth mode)
# -------------------------------------------------------------
def render_landing_screen():
    render_html("""
<div style="text-align: center; max-width: 800px; margin: 0 auto 36px auto; padding-top: 20px;">
    <div style="display: inline-flex; align-items: center; justify-content: center; width: 64px; height: 64px; border-radius: 16px; background: linear-gradient(135deg, #3B82F6, #8B5CF6); font-size: 2rem; margin-bottom: 16px; box-shadow: 0 0 30px rgba(59, 130, 246, 0.4);">
        ⚡
    </div>
    <h1 style="font-size: 2.4rem; font-weight: 800; letter-spacing: -0.03em; color: #F8FAFC; margin-bottom: 10px;">
        Chargeback Evidence AI Operating System
    </h1>
    <p style="font-size: 1.05rem; color: #94A3B8; line-height: 1.6;">
        Autonomous multi-agent dispute intelligence, customer proof vault, and instant arbitration packet synthesis.
    </p>
</div>
""")

    col1, col2 = st.columns(2)

    with col1:
        render_html("""
<div class="portal-card" style="border-top: 4px solid #3B82F6; height: 100%;">
    <div class="portal-icon">🏢</div>
    <div class="portal-title">Merchant Portal</div>
    <div class="portal-desc">
        Full operations control center: 7 AI Agent Center, 10-Step Investigation Timeline, KYC Document Vault, and Interactive PDF Defense Builder.
    </div>
</div>
""")
        if st.button("Enter Merchant Portal ➔", type="primary", use_container_width=True, key="landing_btn_merchant"):
            st.session_state["active_portal"] = "Merchant"
            st.session_state["current_page"] = "Overview"
            st.rerun()

    with col2:
        render_html("""
<div class="portal-card" style="border-top: 4px solid #10B981; height: 100%;">
    <div class="portal-icon">👤</div>
    <div class="portal-title">Customer Portal</div>
    <div class="portal-desc">
        Dedicated cardholder workspace: 5-Category Proof Vault, active dispute status tracker, and 1-click evidence sharing directly to defense dockets.
    </div>
</div>
""")
        if st.button("Enter Customer Portal ➔", type="secondary", use_container_width=True, key="landing_btn_customer"):
            st.session_state["active_portal"] = "Customer"
            st.session_state["current_page"] = "Customer Proof Workspace"
            st.rerun()

    st.write("---")
    st.markdown("### 🔑 Phone OTP Authentication & Credentials")
    render_auth_view(service=DisputeService)


# -------------------------------------------------------------
# SIDEBAR NAVIGATION
# -------------------------------------------------------------
with st.sidebar:
    render_html("""
<div style="padding: 10px 0 16px 0; border-bottom: 1px solid rgba(255,255,255,0.08); margin-bottom: 12px;">
    <div style="display: flex; align-items: center; gap: 10px;">
        <div style="width: 32px; height: 32px; border-radius: 8px; background: linear-gradient(135deg, #3B82F6, #8B5CF6); display: flex; align-items: center; justify-content: center; font-weight: 800; font-size: 1rem; color: white;">
            ⚡
        </div>
        <div>
            <div style="font-weight: 800; font-size: 1.05rem; letter-spacing: -0.02em; color: #F8FAFC;">Chargeback AI OS</div>
            <div style="font-size: 0.7rem; color: #64748B;">Multi-Agent Dispute Intelligence</div>
        </div>
    </div>
</div>
""")

    # Portal Switcher Radio
    portal_roles = ["🏢 Merchant Portal", "👤 Customer Portal", "🔑 Landing & Login"]
    current_role_idx = 0 if st.session_state["active_portal"] == "Merchant" else (1 if st.session_state["active_portal"] == "Customer" else 2)
    
    portal_choice = st.radio(
        "Active Portal Role",
        portal_roles,
        index=current_role_idx,
        label_visibility="collapsed"
    )
    if "Merchant" in portal_choice:
        st.session_state["active_portal"] = "Merchant"
    elif "Customer" in portal_choice:
        st.session_state["active_portal"] = "Customer"
    else:
        st.session_state["active_portal"] = "Landing"

    st.write("---")

    if st.session_state["active_portal"] == "Merchant":
        st.caption("📊 DASHBOARD")
        btn_overview = st.button("📊 Overview", use_container_width=True, type="primary" if st.session_state["current_page"] == "Overview" else "secondary")
        if btn_overview:
            st.session_state["current_page"] = "Overview"
            st.rerun()

        st.caption("📁 CASE MANAGEMENT")
        col_c1, col_c2 = st.columns(2)
        with col_c1:
            if st.button("➕ Create Case", use_container_width=True, type="primary" if st.session_state["current_page"] == "Create Chargeback Case" else "secondary"):
                st.session_state["current_page"] = "Create Chargeback Case"
                st.rerun()
        with col_c2:
            if st.button("⏱️ Timeline", use_container_width=True, type="primary" if st.session_state["current_page"] == "Timeline" else "secondary"):
                st.session_state["current_page"] = "Timeline"
                st.rerun()

        st.caption("🤖 AI INVESTIGATION")
        if st.button("⚡ Live Investigation", use_container_width=True, type="primary" if st.session_state["current_page"] == "AI Investigation" else "secondary"):
            st.session_state["current_page"] = "AI Investigation"
            st.rerun()
        if st.button("🤖 7 AI Agent Center", use_container_width=True, type="primary" if st.session_state["current_page"] == "7 AI Agent Center" else "secondary"):
            st.session_state["current_page"] = "7 AI Agent Center"
            st.rerun()
        if st.button("⚖️ Verification & Traceability", use_container_width=True, type="primary" if st.session_state["current_page"] == "Verification Center" else "secondary"):
            st.session_state["current_page"] = "Verification Center"
            st.rerun()
        if st.button("🔍 Evidence Viewer", use_container_width=True, type="primary" if st.session_state["current_page"] == "Evidence Viewer" else "secondary"):
            st.session_state["current_page"] = "Evidence Viewer"
            st.rerun()
        if st.button("📚 Case Intelligence (RAG)", use_container_width=True, type="primary" if st.session_state["current_page"] == "Similar Historical Cases" else "secondary"):
            st.session_state["current_page"] = "Similar Historical Cases"
            st.rerun()
        if st.button("🕸️ Fraud Intelligence", use_container_width=True, type="primary" if st.session_state["current_page"] == "Fraud Intelligence" else "secondary"):
            st.session_state["current_page"] = "Fraud Intelligence"
            st.rerun()

        st.caption("📄 REPORTS")
        if st.button("📄 Final Defense Packet", use_container_width=True, type="primary" if st.session_state["current_page"] == "Final AI Report" else "secondary"):
            st.session_state["current_page"] = "Final AI Report"
            st.rerun()

        st.caption("🛡️ WORKSPACE")
        if st.button("🏢 Merchant Document Vault", use_container_width=True, type="primary" if st.session_state["current_page"] == "Merchant Vault" else "secondary"):
            st.session_state["current_page"] = "Merchant Vault"
            st.rerun()
        if st.button("👤 Customer Proof Vault", use_container_width=True, type="primary" if st.session_state["current_page"] == "Customer Proof Workspace" else "secondary"):
            st.session_state["current_page"] = "Customer Proof Workspace"
            st.rerun()

    elif st.session_state["active_portal"] == "Customer":
        st.caption("👤 CUSTOMER WORKSPACE")
        if st.button("📋 My Disputes & Cases", use_container_width=True, type="primary" if st.session_state["current_page"] == "Customer Proof Workspace" else "secondary"):
            st.session_state["current_page"] = "Customer Proof Workspace"
            st.rerun()
        if st.button("⚡ Case Investigation Status", use_container_width=True, type="primary" if st.session_state["current_page"] == "AI Investigation" else "secondary"):
            st.session_state["current_page"] = "AI Investigation"
            st.rerun()
        if st.button("⚖️ Verification Summary", use_container_width=True, type="primary" if st.session_state["current_page"] == "Verification Center" else "secondary"):
            st.session_state["current_page"] = "Verification Center"
            st.rerun()
        if st.button("📄 Dispute Defense Report", use_container_width=True, type="primary" if st.session_state["current_page"] == "Final AI Report" else "secondary"):
            st.session_state["current_page"] = "Final AI Report"
            st.rerun()
        if st.button("🛡️ Customer Auth & Vault", use_container_width=True, type="primary" if st.session_state["current_page"] == "Customer Vault" else "secondary"):
            st.session_state["current_page"] = "Customer Vault"
            st.rerun()

    st.write("---")

    # Active Case Widget in Sidebar
    active_case = DisputeService.get_case(st.session_state.get("active_case_id", ""))
    if active_case:
        sc = active_case.get("evidence_score")
        sc_text = f"SCORE {int(sc)}" if sc else "Analyzing"
        c_status = active_case.get("case_status") or active_case.get("status", "new")
        render_html(f"""
<div style="background: rgba(18, 24, 38, 0.7); border: 1px solid rgba(255,255,255,0.08); border-radius: 10px; padding: 12px; margin-bottom: 16px;">
    <div style="font-size: 0.7rem; color: #94A3B8; text-transform: uppercase; font-weight: 600;">ACTIVE DISPUTE CASE</div>
    <div style="font-size: 0.95rem; font-weight: 700; color: #F1F5F9; margin-top: 2px;">{active_case.get('order_id')}</div>
    <div style="font-size: 0.75rem; color: #64748B;">Amount: ₹{active_case.get('amount', 0):,.2f} &bull; {active_case.get('dispute_type', 'Dispute')}</div>
    <div style="margin-top: 8px; display: flex; justify-content: space-between; align-items: center;">
        <span class="status-pill complete" style="font-size: 0.68rem;">{c_status.upper()}</span>
        <span style="font-size: 0.75rem; font-weight: 700; color: #10B981;">{sc_text}</span>
    </div>
</div>
""")

    # Multi-Agent Architecture Status
    is_live = DisputeService.check_backend_alive()
    api_status_label = "FastAPI: Connected (Port 8000)" if is_live else "FastAPI: Local 7-Agent Engine"
    api_status_color = "#10B981" if is_live else "#60A5FA"

    render_html(f"""
<div style="font-size: 0.72rem; color: #64748B; line-height: 1.5;">
    <div style="color: {api_status_color}; font-weight: 600;">● {api_status_label}</div>
    <div style="color: #10B981; font-weight: 600;">● Supabase: Dual RLS Active</div>
    <div style="color: #A78BFA; font-weight: 600;">● 7 AI Agents: Synchronized</div>
    <div style="color: #60A5FA; font-weight: 600;">● n8n Webhook: Ready</div>
</div>
""")

# -------------------------------------------------------------
# MAIN APP BODY
# -------------------------------------------------------------
if st.session_state["active_portal"] == "Landing":
    render_landing_screen()
else:
    merchant = st.session_state.get("current_merchant", {})
    active_order = active_case.get("order_id", "") if active_case else ""
    render_app_header(merchant, active_order, active_portal=st.session_state["active_portal"])

    page = st.session_state["current_page"]

    if page == "Overview":
        render_overview_view(service=DisputeService)
    elif page == "Customer Proof Workspace":
        render_customer_portal_view(service=DisputeService)
    elif page == "7 AI Agent Center":
        render_ai_agents_view(service=DisputeService)
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
    elif page in ["Merchant Vault", "Customer Vault"]:
        render_auth_view(service=DisputeService)
    else:
        render_overview_view(service=DisputeService)
