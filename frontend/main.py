import sys
from pathlib import Path

# Add project root to sys.path so modules resolve seamlessly
ROOT_DIR = Path(__file__).resolve().parent.parent
if str(ROOT_DIR) not in sys.path:
    sys.path.insert(0, str(ROOT_DIR))

import streamlit as st
from frontend.styles import FINTECH_CSS
from frontend.components import render_html
from frontend.api_client import DisputeService
from frontend.views import (
    render_auth_view,
    render_overview_view,
    render_create_case_view,
    render_customer_portal_view,
    render_ai_agents_view,
    render_investigation_view,
    render_verification_view,
    render_timeline_view,
    render_similar_cases_view,
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

# -------------------------------------------------------------
# AUTHENTICATION GUARD (PRIMARY REQUIREMENT)
# -------------------------------------------------------------
is_auth = st.session_state.get("authenticated", False)

if not is_auth:
    # Unauthenticated users see ONLY the premium landing & login screen
    # Hide sidebar completely via CSS
    st.markdown("""
    <style>
        [data-testid="stSidebar"], [data-testid="collapsedControl"] { display: none !important; }
        .main .block-container { max-width: 1240px !important; padding-top: 2rem !important; }
    </style>
    """, unsafe_allow_html=True)
    render_auth_view(service=DisputeService)
    st.stop()

# -------------------------------------------------------------
# AUTHENTICATED SESSION ROUTING
# -------------------------------------------------------------
role = st.session_state.get("role", "merchant")
user_profile = st.session_state.get("current_merchant", {}) if role == "merchant" else st.session_state.get("current_customer", {})
user_display_name = user_profile.get("name") or user_profile.get("full_name") or ("Apex Retailers" if role == "merchant" else "Aarav Sharma")

cases = DisputeService.list_cases()
if "active_case_id" not in st.session_state and cases:
    st.session_state["active_case_id"] = cases[0]["id"]

# Set default page per role
if "current_page" not in st.session_state:
    st.session_state["current_page"] = "Dashboard" if role == "merchant" else "My Cases"

# -------------------------------------------------------------
# SIDEBAR NAVIGATION (RENDERS ONLY AFTER AUTHENTICATION)
# -------------------------------------------------------------
with st.sidebar:
    # Brand Top
    render_html(f"""
<div style="padding: 10px 0 16px 0; border-bottom: 1px solid rgba(255,255,255,0.08); margin-bottom: 16px;">
    <div style="display: flex; align-items: center; gap: 10px;">
        <div style="width: 32px; height: 32px; border-radius: 8px; background: linear-gradient(135deg, #2563EB, #7C3AED); display: flex; align-items: center; justify-content: center; font-weight: 800; font-size: 1rem; color: white;">
            ⚡
        </div>
        <div>
            <div style="font-weight: 800; font-size: 1rem; letter-spacing: -0.02em; color: #F8FAFC;">Chargeback AI OS</div>
            <div style="font-size: 0.7rem; color: #64748B;">{role.upper()} WORKSPACE</div>
        </div>
    </div>
</div>
""")

    curr_page = st.session_state.get("current_page", "Dashboard")

    # ---------------------------------------------------------
    # MERCHANT SIDEBAR
    # ---------------------------------------------------------
    if role == "merchant":
        st.caption("OVERVIEW")
        if st.button("📊 Dashboard", key="nav_m_dash", use_container_width=True, type="primary" if curr_page in ["Dashboard", "My Cases"] else "secondary"):
            st.session_state["viewing_case_detail"] = None
            st.session_state["current_page"] = "Dashboard"
            st.rerun()

        st.caption("CASE MANAGEMENT")
        col_c1, col_c2 = st.columns(2)
        with col_c1:
            if st.button("➕ Create Case", key="nav_m_create", use_container_width=True, type="primary" if curr_page == "Create Case" else "secondary"):
                st.session_state["viewing_case_detail"] = None
                st.session_state["current_page"] = "Create Case"
                st.rerun()
        with col_c2:
            if st.button("⏱️ Timeline", key="nav_m_time", use_container_width=True, type="primary" if curr_page == "Timeline" else "secondary"):
                st.session_state["current_page"] = "Timeline"
                st.rerun()

        st.caption("AI INVESTIGATION")
        if st.button("⚡ Live Investigation", key="nav_m_inv", use_container_width=True, type="primary" if curr_page == "Live Investigation" else "secondary"):
            st.session_state["current_page"] = "Live Investigation"
            st.rerun()
        if st.button("🤖 AI Agents", key="nav_m_agents", use_container_width=True, type="primary" if curr_page == "AI Agents" else "secondary"):
            st.session_state["current_page"] = "AI Agents"
            st.rerun()
        if st.button("⚖️ Evidence Integrity", key="nav_m_ver", use_container_width=True, type="primary" if curr_page == "Evidence Integrity" else "secondary"):
            st.session_state["current_page"] = "Evidence Integrity"
            st.rerun()
        if st.button("📚 Case Intelligence", key="nav_m_rag", use_container_width=True, type="primary" if curr_page == "Case Intelligence" else "secondary"):
            st.session_state["current_page"] = "Case Intelligence"
            st.rerun()

        st.caption("REPORTS")
        if st.button("📄 Final Packet", key="nav_m_rep", use_container_width=True, type="primary" if curr_page == "Final Packet" else "secondary"):
            st.session_state["current_page"] = "Final Packet"
            st.rerun()

        st.caption("WORKSPACE")
        if st.button("🛡️ Merchant Vault", key="nav_m_vault", use_container_width=True, type="primary" if curr_page == "Merchant Vault" else "secondary"):
            st.session_state["current_page"] = "Merchant Vault"
            st.rerun()
        if st.button("⚙️ Settings", key="nav_m_settings", use_container_width=True, type="primary" if curr_page == "Settings" else "secondary"):
            st.session_state["current_page"] = "Settings"
            st.rerun()

    # ---------------------------------------------------------
    # CUSTOMER SIDEBAR
    # ---------------------------------------------------------
    else:
        st.caption("OVERVIEW")
        if st.button("📋 My Cases", key="nav_c_cases", use_container_width=True, type="primary" if curr_page == "My Cases" else "secondary"):
            st.session_state["current_page"] = "My Cases"
            st.rerun()

        st.caption("EVIDENCE")
        if st.button("🛡️ Proof Vault", key="nav_c_vault", use_container_width=True, type="primary" if curr_page == "Proof Vault" else "secondary"):
            st.session_state["current_page"] = "Proof Vault"
            st.rerun()
        if st.button("📥 Requested Documents", key="nav_c_req", use_container_width=True, type="primary" if curr_page == "Requested Documents" else "secondary"):
            st.session_state["current_page"] = "Requested Documents"
            st.rerun()
        if st.button("📤 Upload Evidence", key="nav_c_up", use_container_width=True, type="primary" if curr_page == "Upload Evidence" else "secondary"):
            st.session_state["current_page"] = "Upload Evidence"
            st.rerun()

        st.caption("CASE TRACKING")
        if st.button("⏱️ Case Status", key="nav_c_status", use_container_width=True, type="primary" if curr_page == "Case Status" else "secondary"):
            st.session_state["current_page"] = "Case Status"
            st.rerun()

    st.write("---")

    # Bottom User Card & Logout
    verified_label = "● KYC Level 2 Verified" if role == "merchant" else "● Verified Cardholder"
    render_html(f"""
<div style="padding: 12px; background: rgba(255,255,255,0.03); border: 1px solid rgba(255,255,255,0.06); border-radius: 10px; margin-bottom: 12px;">
    <div style="display: flex; align-items: center; gap: 10px;">
        <div style="width: 32px; height: 32px; border-radius: 50%; background: rgba(59, 130, 246, 0.2); border: 1px solid rgba(59, 130, 246, 0.4); display: flex; align-items: center; justify-content: center; font-size: 0.9rem;">
            {'🏢' if role == 'merchant' else '👤'}
        </div>
        <div style="flex: 1; overflow: hidden;">
            <div style="font-weight: 700; font-size: 0.85rem; color: #F8FAFC; white-space: nowrap; text-overflow: ellipsis; overflow: hidden;">
                {user_display_name}
            </div>
            <div style="font-size: 0.7rem; color: #34D399;">{verified_label}</div>
        </div>
    </div>
</div>
""")

    if st.button("🚪 Logout", key="btn_logout", use_container_width=True):
        st.session_state["authenticated"] = False
        st.session_state["role"] = None
        st.session_state["auth_step"] = "portal_select"
        st.session_state["viewing_case_detail"] = None
        st.rerun()

# -------------------------------------------------------------
# MAIN APP BODY (AUTHENTICATED ONLY)
# -------------------------------------------------------------
# Top Minimalist Banner
render_html(f"""
<div class="app-header-container">
    <div style="display: flex; align-items: center; gap: 12px;">
        <div style="width: 34px; height: 34px; border-radius: 8px; background: linear-gradient(135deg, #2563EB, #7C3AED); display: flex; align-items: center; justify-content: center; font-weight: 800; font-size: 1.1rem; color: white;">
            ⚡
        </div>
        <div>
            <div class="brand-badge">CHARGEBACK EVIDENCE AI</div>
            <div style="font-size: 0.75rem; color: #94A3B8;">Autonomous Dispute Operating System</div>
        </div>
    </div>
    <div style="display: flex; align-items: center; gap: 10px;">
        <span class="sub-tag" style="background: rgba(37, 99, 235, 0.15); border-color: rgba(37, 99, 235, 0.3); color: #93C5FD;">{role.upper()} PORTAL</span>
        <div style="background: rgba(255,255,255,0.05); padding: 5px 12px; border-radius: 8px; border: 1px solid rgba(255,255,255,0.08); font-size: 0.78rem; color: #E2E8F0;">
            {'🏢' if role == 'merchant' else '👤'} <b>{user_display_name}</b>
        </div>
    </div>
</div>
""")

page = st.session_state.get("current_page", "Dashboard")

# -------------------------------------------------------------
# MERCHANT ROUTING
# -------------------------------------------------------------
if role == "merchant":
    if page in ["Dashboard", "My Cases"]:
        render_overview_view(service=DisputeService)
    elif page == "Create Case":
        render_create_case_view(service=DisputeService)
    elif page == "Timeline":
        render_timeline_view(service=DisputeService)
    elif page == "Live Investigation":
        render_investigation_view(service=DisputeService)
    elif page == "AI Agents":
        render_ai_agents_view(service=DisputeService)
    elif page == "Evidence Integrity":
        render_verification_view(service=DisputeService)
    elif page == "Case Intelligence":
        render_similar_cases_view(service=DisputeService)
    elif page == "Final Packet":
        render_final_report_view(service=DisputeService)
    elif page in ["Merchant Vault", "Settings"]:
        # Merchant Document Vault
        render_html("""
<div class="fintech-card">
    <div class="card-title"><span>Merchant Document Vault & Corporate Credentials</span><span class="sub-tag">Supabase Storage</span></div>
    <p class="card-subtitle">Maintain business registration, GST certificates, and authorization letters used in arbitration representment filings.</p>
</div>
""")
        m_prof = DisputeService.get_merchant_profile()
        c_v1, c_v2 = st.columns([1, 2])
        with c_v1:
            doc_choice = st.selectbox("Document Category", [
                "GST Certificate",
                "Business PAN Card",
                "Registration Certificate",
                "Business Address Proof",
                "Authorization Letter"
            ])
            up_file = st.file_uploader("Select Certificate", type=["pdf", "png", "jpg"])
            if up_file and st.button("Upload to Merchant Vault", type="primary", use_container_width=True):
                DisputeService.upload_vault_doc(doc_choice, up_file.name, up_file.getvalue())
                st.success("Uploaded & Verified!")
                st.rerun()
        with c_v2:
            st.markdown("#### Vault Inventory & Verification Status")
            v_docs = m_prof.get("vault_documents", [])
            if v_docs:
                for vd in v_docs:
                    render_html(f"""
<div style="padding: 10px 14px; background: rgba(0,0,0,0.3); border: 1px solid rgba(255,255,255,0.06); border-radius: 8px; margin-bottom: 8px; display: flex; justify-content: space-between; align-items: center;">
    <div>
        <div style="font-weight: 600; font-size: 0.88rem; color: #F1F5F9;">📁 {vd['file_name']}</div>
        <div style="font-size: 0.74rem; color: #94A3B8;">Type: <b>{vd['doc_type']}</b> &bull; Uploaded: {vd.get('uploaded_at', '')[:10]} &bull; <span style="color: #34D399;">✓ VERIFIED</span></div>
    </div>
</div>
""")
            else:
                st.info("No documents uploaded yet.")

# -------------------------------------------------------------
# CUSTOMER ROUTING
# -------------------------------------------------------------
else:
    # Customer pages
    render_customer_portal_view(service=DisputeService)
