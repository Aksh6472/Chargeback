import sys
from pathlib import Path

# Add project root to sys.path so modules resolve seamlessly
ROOT_DIR = Path(__file__).resolve().parent.parent
if str(ROOT_DIR) not in sys.path:
    sys.path.insert(0, str(ROOT_DIR))

import streamlit as st
from frontend.styles import FINTECH_CSS
from frontend.components import render_html, render_app_header
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
    render_final_report_view,
    render_settings_view
)

# Page configuration
st.set_page_config(
    page_title="Chargeback Evidence AI | Enterprise Dispute Platform",
    page_icon="🛡️",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Inject custom Stitch corporate fintech CSS
st.markdown(FINTECH_CSS, unsafe_allow_html=True)


# -------------------------------------------------------------
# SECURE ROLE & PROFILE SWITCH DIALOG (RE-AUTHENTICATION)
# -------------------------------------------------------------
@st.dialog("🔐 Security Verification (Re-Authentication)")
def confirm_portal_or_profile_switch(target_role: str, target_customer_id: str = None):
    st.write("You are transitioning across security boundaries. Enter the 6-digit verification code sent to your registered device to authenticate this session.")
    st.info("Evaluation OTP Code: **742918**")
    otp_val = st.text_input("Enter 6-Digit OTP", max_chars=6, key="dialog_otp_box", placeholder="742918")
    col_v1, col_v2 = st.columns(2)
    with col_v1:
        if st.button("Cancel", use_container_width=True):
            st.rerun()
    with col_v2:
        if st.button("Verify & Switch", type="primary", use_container_width=True):
            if otp_val.strip() in ["742918", "123456"]:
                if target_role == "customer":
                    st.session_state["role"] = "customer"
                    st.session_state["active_portal"] = "Customer"
                    if target_customer_id:
                        cust = DisputeService.get_customer_profile(target_customer_id)
                        if cust:
                            st.session_state["current_customer"] = cust
                    else:
                        custs = DisputeService.list_all_customers()
                        if custs:
                            st.session_state["current_customer"] = custs[0]
                    st.session_state["current_page"] = "My Cases"
                else:
                    st.session_state["role"] = "merchant"
                    st.session_state["active_portal"] = "Merchant"
                    st.session_state["current_page"] = "Dashboard"
                st.session_state["viewing_case_detail"] = None
                st.success("Identity verified successfully!")
                st.rerun()
            else:
                st.error("Invalid verification code. Please enter 742918.")


# -------------------------------------------------------------
# AUTHENTICATION GUARD (PRIMARY REQUIREMENT: FIRST SCREEN IS LOGIN)
# -------------------------------------------------------------
is_auth = st.session_state.get("authenticated", False)

if not is_auth:
    # Unauthenticated users see ONLY the Stitch landing & login screen
    # Hide sidebar completely via CSS
    st.markdown("""
    <style>
        [data-testid="stSidebar"], [data-testid="collapsedControl"] { display: none !important; }
        .main .block-container { max-width: 1200px !important; padding-top: 2rem !important; }
    </style>
    """, unsafe_allow_html=True)
    render_auth_view(service=DisputeService)
    st.stop()

# -------------------------------------------------------------
# AUTHENTICATED SESSION ROUTING & ROLE GUARD
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

# Strict Role-Based Route Isolation
merchant_pages = {"Dashboard", "Create Case", "Disputes", "Timeline", "Live Investigation", "AI Agents", "Evidence Integrity", "Case Intelligence", "Final Packet", "Merchant Vault", "Settings"}
customer_pages = {"My Cases", "Proof Vault", "Requested Documents", "Upload Evidence", "Case Status", "Settings"}

curr_page = st.session_state.get("current_page", "Dashboard")
if role == "merchant" and curr_page in customer_pages and curr_page != "Settings":
    st.session_state["current_page"] = "Dashboard"
    curr_page = "Dashboard"
elif role == "customer" and curr_page in merchant_pages and curr_page != "Settings":
    st.session_state["current_page"] = "My Cases"
    curr_page = "My Cases"

# -------------------------------------------------------------
# SIDEBAR NAVIGATION (STITCH UI SHELL)
# -------------------------------------------------------------
with st.sidebar:
    # Brand Top
    render_html(f"""
<div style="padding: 6px 0 16px 0; border-bottom: 1px solid rgba(255,255,255,0.1); margin-bottom: 14px;">
    <div style="display: flex; align-items: center; justify-content: space-between;">
        <div style="display: flex; align-items: center; gap: 10px;">
            <div style="width: 32px; height: 32px; border-radius: 8px; background: #FFFFFF; color: #1A242C; display: flex; align-items: center; justify-content: center;">
                <span class="material-symbols-outlined" style="font-size: 20px;">shield</span>
            </div>
            <div>
                <div style="font-weight: 800; font-size: 0.98rem; letter-spacing: -0.02em; color: #FFFFFF;">Evidence AI</div>
                <div style="font-size: 0.66rem; color: #98A4AD; letter-spacing: 0.08em; text-transform: uppercase; font-weight: 700;">DISPUTE SHIELD</div>
            </div>
        </div>
        <span style="font-size: 0.65rem; font-weight: 700; text-transform: uppercase; padding: 2px 6px; border-radius: 4px; background: rgba(255,255,255,0.1); color: #FFFFFF;">
            Enterprise
        </span>
    </div>
</div>
""")

    curr_page = st.session_state.get("current_page", "Dashboard")

    # ---------------------------------------------------------
    # MERCHANT SIDEBAR
    # ---------------------------------------------------------
    if role == "merchant":
        st.caption("OVERVIEW")
        if st.button("📊 Overview & Dashboard", key="nav_m_dash", use_container_width=True, type="primary" if curr_page in ["Dashboard", "My Cases"] else "secondary"):
            st.session_state["viewing_case_detail"] = None
            st.session_state["current_page"] = "Dashboard"
            st.rerun()

        st.caption("CASE MANAGEMENT")
        if st.button("➕ Create Dispute Case", key="nav_m_create", use_container_width=True, type="primary" if curr_page == "Create Case" else "secondary"):
            st.session_state["viewing_case_detail"] = None
            st.session_state["current_page"] = "Create Case"
            st.rerun()
        if st.button("⏱️ Chronological Timeline", key="nav_m_time", use_container_width=True, type="primary" if curr_page == "Timeline" else "secondary"):
            st.session_state["current_page"] = "Timeline"
            st.rerun()

        st.caption("AI INVESTIGATION")
        if st.button("⚡ Live Investigation", key="nav_m_inv", use_container_width=True, type="primary" if curr_page == "Live Investigation" else "secondary"):
            st.session_state["current_page"] = "Live Investigation"
            st.rerun()
        if st.button("🤖 7 AI Agents Center", key="nav_m_agents", use_container_width=True, type="primary" if curr_page == "AI Agents" else "secondary"):
            st.session_state["current_page"] = "AI Agents"
            st.rerun()
        if st.button("⚖️ Evidence Integrity", key="nav_m_ver", use_container_width=True, type="primary" if curr_page == "Evidence Integrity" else "secondary"):
            st.session_state["current_page"] = "Evidence Integrity"
            st.rerun()
        if st.button("📚 Case Intelligence", key="nav_m_rag", use_container_width=True, type="primary" if curr_page == "Case Intelligence" else "secondary"):
            st.session_state["current_page"] = "Case Intelligence"
            st.rerun()

        st.caption("EVIDENCE & REPORTS")
        if st.button("📄 Final Package Builder", key="nav_m_rep", use_container_width=True, type="primary" if curr_page == "Final Packet" else "secondary"):
            st.session_state["current_page"] = "Final Packet"
            st.rerun()
        if st.button("🛡️ Merchant Vault", key="nav_m_vault", use_container_width=True, type="primary" if curr_page == "Merchant Vault" else "secondary"):
            st.session_state["current_page"] = "Merchant Vault"
            st.rerun()

        st.caption("WORKSPACE & SECURITY")
        if st.button("⚙️ Settings", key="nav_m_settings", use_container_width=True, type="primary" if curr_page == "Settings" else "secondary"):
            st.session_state["current_page"] = "Settings"
            st.rerun()
        if st.button("🔄 Switch to Customer Portal", key="btn_switch_to_cust", use_container_width=True):
            confirm_portal_or_profile_switch(target_role="customer")

    # ---------------------------------------------------------
    # CUSTOMER SIDEBAR
    # ---------------------------------------------------------
    else:
        st.caption("SWITCH CARDHOLDER PROFILE")
        all_customers = DisputeService.list_all_customers()
        cust_map = {
            f"👤 {c.get('full_name', 'Customer')} ({c.get('phone_number', '')[-4:] if len(c.get('phone_number', '')) >= 4 else 'XXXX'})": c
            for c in all_customers
        }
        curr_cust = st.session_state.get("current_customer", {})
        curr_id = curr_cust.get("id")
        current_selection_label = next((k for k, v in cust_map.items() if v.get("id") == curr_id), list(cust_map.keys())[0] if cust_map else "Customer")
        sel_cust_option = st.selectbox(
            "Active Customer Profile",
            list(cust_map.keys()),
            index=list(cust_map.keys()).index(current_selection_label) if current_selection_label in cust_map else 0,
            label_visibility="collapsed",
            key="customer_sidebar_switcher"
        )
        if sel_cust_option and cust_map[sel_cust_option].get("id") != curr_id:
            target_id = cust_map[sel_cust_option].get("id")
            confirm_portal_or_profile_switch(target_role="customer", target_customer_id=target_id)

        st.caption("OVERVIEW")
        if st.button("📋 My Disputes", key="nav_c_cases", use_container_width=True, type="primary" if curr_page == "My Cases" else "secondary"):
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

        st.caption("WORKSPACE & ACCESS")
        if st.button("⚙️ Settings", key="nav_c_settings", use_container_width=True, type="primary" if curr_page == "Settings" else "secondary"):
            st.session_state["current_page"] = "Settings"
            st.rerun()
        if st.button("🔄 Switch to Merchant Portal", key="btn_switch_to_merch", use_container_width=True):
            confirm_portal_or_profile_switch(target_role="merchant")

    st.write("---")

    # Bottom User Card & Logout
    verified_label = "KYC Level 2 Verified" if role == "merchant" else "Verified Cardholder"
    user_title = "Director of Risk & Fraud" if role == "merchant" else "Customer Account"
    render_html(f"""
<div style="padding: 10px; background: rgba(255,255,255,0.05); border: 1px solid rgba(255,255,255,0.1); border-radius: 10px; margin-bottom: 10px;">
    <div style="display: flex; align-items: center; gap: 10px;">
        <div style="width: 32px; height: 32px; border-radius: 50%; background: #1A242C; border: 1px solid rgba(255,255,255,0.2); display: flex; align-items: center; justify-content: center; font-size: 0.9rem; color: #FFFFFF;">
            <span class="material-symbols-outlined" style="font-size: 18px;">{'account_balance' if role == 'merchant' else 'person'}</span>
        </div>
        <div style="flex: 1; overflow: hidden;">
            <div style="font-weight: 700; font-size: 0.82rem; color: #FFFFFF; white-space: nowrap; text-overflow: ellipsis; overflow: hidden;">
                {user_display_name}
            </div>
            <div style="font-size: 0.68rem; color: #98A4AD;">{user_title}</div>
            <div style="font-size: 0.66rem; color: #4EDEA3;">&bull; {verified_label}</div>
        </div>
    </div>
</div>
""")

    if st.button("🚪 Sign Out", key="btn_logout", use_container_width=True):
        st.session_state["authenticated"] = False
        st.session_state["role"] = None
        st.session_state["auth_step"] = "portal_select"
        st.session_state["viewing_case_detail"] = None
        st.rerun()

# -------------------------------------------------------------
# MAIN WORKSPACE (AUTHENTICATED)
# -------------------------------------------------------------
# Render Stitch Top Navigation Bar
render_app_header(
    current_merchant=st.session_state.get("current_merchant") if role == "merchant" else None,
    active_order_id=st.session_state.get("active_case_id", ""),
    active_portal="Merchant" if role == "merchant" else "Customer"
)

page = st.session_state.get("current_page", "Dashboard")

# -------------------------------------------------------------
# MERCHANT ROUTING
# -------------------------------------------------------------
if role == "merchant":
    if page in ["Dashboard", "My Cases", "Disputes"]:
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
    elif page == "Merchant Vault":
        render_html("""
<div class="stitch-card">
    <div class="stitch-card-header">
        <h3 class="stitch-card-title">Merchant Document Vault & Corporate Credentials</h3>
        <span class="stitch-pill stitch-pill-info">Secure Storage</span>
    </div>
    <p class="stitch-card-subtitle">Maintain business registration, GST certificates, and authorization letters used in arbitration representment filings.</p>
</div>
""")
        m_prof = DisputeService.get_merchant_profile()
        c_v1, c_v2 = st.columns([1, 2])
        with c_v1:
            with st.container():
                st.markdown("#### Upload Vault Credential")
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
                    st.success("Uploaded & Verified in Vault!")
                    st.rerun()
        with c_v2:
            st.markdown("#### Vault Inventory & Verification Status")
            v_docs = m_prof.get("vault_documents", [])
            if v_docs:
                for vd in v_docs:
                    render_html(f"""
<div style="padding: 12px 16px; background: #FFFFFF; border: 1px solid #E5E7EB; border-radius: 8px; margin-bottom: 8px; display: flex; justify-content: space-between; align-items: center; box-shadow: 0 1px 2px rgba(0,0,0,0.04);">
    <div>
        <div style="font-weight: 600; font-size: 0.9rem; color: #191C1E;">📁 {vd['file_name']}</div>
        <div style="font-size: 0.76rem; color: #64748B;">Category: <b>{vd['doc_type']}</b> &bull; Added: {vd.get('uploaded_at', '')[:10]}</div>
    </div>
    <span class="stitch-pill stitch-pill-success">✓ VERIFIED</span>
</div>
""")
            else:
                st.info("No documents uploaded to vault yet.")
    elif page == "Settings":
        render_settings_view(service=DisputeService)

# -------------------------------------------------------------
# CUSTOMER ROUTING
# -------------------------------------------------------------
else:
    if page == "Settings":
        render_settings_view(service=DisputeService)
    else:
        render_customer_portal_view(service=DisputeService, active_page=curr_page)
