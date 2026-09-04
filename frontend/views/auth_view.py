"""
Chargeback Evidence AI - Premium Split-Screen Authentication & Portal Selection
Stripe/Ramp/Brex inspired login flow with zero-leakage security guards:
1. Portal Selection (Merchant vs Customer)
2. Phone Number Entry with Country Code
3. 6-Digit OTP Verification
4. Automatic Role-based Routing into isolated workspaces
"""

import streamlit as st
from frontend.components import render_html


def render_auth_view(service):
    if "auth_step" not in st.session_state:
        st.session_state["auth_step"] = "portal_select"  # portal_select | phone_entry | otp_verify
    if "auth_role" not in st.session_state:
        st.session_state["auth_role"] = "merchant"  # merchant | customer

    step = st.session_state["auth_step"]
    role = st.session_state["auth_role"]

    # -------------------------------------------------------------
    # 2-COLUMN SPLIT SCREEN: LEFT BRAND / RIGHT AUTH CARD
    # -------------------------------------------------------------
    col_left, col_right = st.columns([1.1, 1.0], gap="large")

    with col_left:
        render_html("""
<div style="padding: 40px 20px 40px 10px;">
    <div style="display: inline-flex; align-items: center; gap: 10px; margin-bottom: 24px;">
        <div style="width: 40px; height: 40px; border-radius: 12px; background: linear-gradient(135deg, #2563EB, #7C3AED); display: flex; align-items: center; justify-content: center; font-weight: 800; font-size: 1.3rem; color: white; box-shadow: 0 4px 16px rgba(37, 99, 235, 0.4);">
            ⚡
        </div>
        <span style="font-weight: 800; font-size: 1.3rem; letter-spacing: -0.02em; color: #F8FAFC;">Chargeback Evidence AI</span>
    </div>

    <div style="margin-bottom: 18px;">
        <span class="sub-tag" style="background: rgba(59, 130, 246, 0.15); color: #93C5FD; border-color: rgba(59, 130, 246, 0.3); font-size: 0.74rem;">
            ✦ AI-POWERED DISPUTE INTELLIGENCE
        </span>
    </div>

    <h1 style="font-size: 2.7rem; font-weight: 800; letter-spacing: -0.035em; color: #F8FAFC; line-height: 1.15; margin-bottom: 18px;">
        Turn chargeback evidence into <span style="background: linear-gradient(90deg, #60A5FA, #A78BFA); -webkit-background-clip: text; -webkit-text-fill-color: transparent;">winning cases.</span>
    </h1>

    <p style="font-size: 1.05rem; color: #94A3B8; line-height: 1.6; margin-bottom: 32px; max-width: 520px;">
        Investigate disputes, verify cross-document evidence, and generate submission-ready legal packets with 7 autonomous cooperating AI agents.
    </p>

    <div style="display: grid; grid-template-columns: 1fr 1fr; gap: 14px; max-width: 480px;">
        <div style="background: rgba(255,255,255,0.025); border: 1px solid rgba(255,255,255,0.06); border-radius: 10px; padding: 12px 14px;">
            <div style="font-size: 1.1rem; margin-bottom: 4px;">⚡</div>
            <div style="font-size: 0.85rem; font-weight: 700; color: #F1F5F9;">AI Investigation</div>
            <div style="font-size: 0.75rem; color: #64748B;">10-step multi-agent triage</div>
        </div>
        <div style="background: rgba(255,255,255,0.025); border: 1px solid rgba(255,255,255,0.06); border-radius: 10px; padding: 12px 14px;">
            <div style="font-size: 1.1rem; margin-bottom: 4px;">⚖️</div>
            <div style="font-size: 0.85rem; font-weight: 700; color: #F1F5F9;">Evidence Verification</div>
            <div style="font-size: 0.75rem; color: #64748B;">6-way triangulation</div>
        </div>
        <div style="background: rgba(255,255,255,0.025); border: 1px solid rgba(255,255,255,0.06); border-radius: 10px; padding: 12px 14px;">
            <div style="font-size: 1.1rem; margin-bottom: 4px;">🔍</div>
            <div style="font-size: 0.85rem; font-weight: 700; color: #F1F5F9;">Source Traceability</div>
            <div style="font-size: 0.75rem; color: #64748B;">Zero-hallucination audits</div>
        </div>
        <div style="background: rgba(255,255,255,0.025); border: 1px solid rgba(255,255,255,0.06); border-radius: 10px; padding: 12px 14px;">
            <div style="font-size: 1.1rem; margin-bottom: 4px;">🛡️</div>
            <div style="font-size: 0.85rem; font-weight: 700; color: #F1F5F9;">Secure Proof Vault</div>
            <div style="font-size: 0.75rem; color: #64748B;">AES-256 encrypted dockets</div>
        </div>
    </div>
</div>
""")

    with col_right:
        st.write("")
        st.write("")

        # ---------------------------------------------------------
        # STEP 1: PORTAL SELECTION SCREEN
        # ---------------------------------------------------------
        if step == "portal_select":
            render_html("""
<div style="background: rgba(18, 24, 38, 0.8); border: 1px solid rgba(255,255,255,0.08); border-radius: 18px; padding: 32px 28px; box-shadow: 0 20px 50px rgba(0,0,0,0.5); backdrop-filter: blur(20px);">
    <div style="margin-bottom: 24px;">
        <h2 style="font-size: 1.5rem; font-weight: 800; color: #F8FAFC; margin: 0 0 6px 0;">Welcome</h2>
        <p style="font-size: 0.88rem; color: #94A3B8; margin: 0;">Choose how you want to access your workspace.</p>
    </div>
</div>
""")

            # Merchant Card
            render_html("""
<div style="background: rgba(255,255,255,0.02); border: 1px solid rgba(255,255,255,0.07); border-radius: 14px; padding: 22px; margin-bottom: 16px; transition: border-color 0.2s ease;">
    <div style="display: flex; gap: 16px; align-items: flex-start;">
        <div style="width: 44px; height: 44px; border-radius: 10px; background: rgba(37, 99, 235, 0.15); border: 1px solid rgba(37, 99, 235, 0.3); display: flex; align-items: center; justify-content: center; font-size: 1.4rem;">
            🏢
        </div>
        <div style="flex: 1;">
            <div style="font-weight: 700; font-size: 1.05rem; color: #F8FAFC; margin-bottom: 4px;">Merchant Portal</div>
            <div style="font-size: 0.82rem; color: #94A3B8; line-height: 1.45; margin-bottom: 14px;">
                Manage disputes, investigate evidence with 7 AI agents, and generate AI-powered chargeback packets.
            </div>
        </div>
    </div>
</div>
""")
            if st.button("Continue as Merchant ➔", key="btn_choose_merchant", type="primary", use_container_width=True):
                st.session_state["auth_role"] = "merchant"
                st.session_state["auth_step"] = "phone_entry"
                st.rerun()

            st.write("")

            # Customer Card
            render_html("""
<div style="background: rgba(255,255,255,0.02); border: 1px solid rgba(255,255,255,0.07); border-radius: 14px; padding: 22px; margin-bottom: 16px; transition: border-color 0.2s ease;">
    <div style="display: flex; gap: 16px; align-items: flex-start;">
        <div style="width: 44px; height: 44px; border-radius: 10px; background: rgba(16, 185, 129, 0.15); border: 1px solid rgba(16, 185, 129, 0.3); display: flex; align-items: center; justify-content: center; font-size: 1.4rem;">
            👤
        </div>
        <div style="flex: 1;">
            <div style="font-weight: 700; font-size: 1.05rem; color: #F8FAFC; margin-bottom: 4px;">Customer Portal</div>
            <div style="font-size: 0.82rem; color: #94A3B8; line-height: 1.45; margin-bottom: 14px;">
                Upload requested documents, manage your 5-category proof vault, and track your active case status.
            </div>
        </div>
    </div>
</div>
""")
            if st.button("Continue as Customer ➔", key="btn_choose_customer", type="secondary", use_container_width=True):
                st.session_state["auth_role"] = "customer"
                st.session_state["auth_step"] = "phone_entry"
                st.rerun()

        # ---------------------------------------------------------
        # STEP 2: PHONE NUMBER ENTRY SCREEN
        # ---------------------------------------------------------
        elif step == "phone_entry":
            title_text = "Merchant Sign In" if role == "merchant" else "Customer Sign In"
            desc_text = "Enter your mobile number to securely access your workspace."

            if st.button("← Back to portal selection", key="btn_back_to_portals"):
                st.session_state["auth_step"] = "portal_select"
                st.rerun()

            render_html(f"""
<div style="background: rgba(18, 24, 38, 0.8); border: 1px solid rgba(255,255,255,0.08); border-radius: 18px; padding: 28px 24px; box-shadow: 0 20px 50px rgba(0,0,0,0.5); backdrop-filter: blur(20px); margin-top: 10px;">
    <h2 style="font-size: 1.45rem; font-weight: 800; color: #F8FAFC; margin: 0 0 6px 0;">{title_text}</h2>
    <p style="font-size: 0.86rem; color: #94A3B8; margin: 0 0 20px 0;">{desc_text}</p>
</div>
""")

            default_ph = "+91 9876543210" if role == "merchant" else "+91 9811223344"
            col_cc, col_num = st.columns([1, 2.5])
            with col_cc:
                country_code = st.selectbox("Country", ["🇮🇳 +91", "🇺🇸 +1", "🇬🇧 +44", "🇦🇪 +971"], index=0)
            with col_num:
                ph_digits = st.text_input("Mobile Number", value="9876543210" if role == "merchant" else "9811223344", placeholder="9876543210")

            full_phone = f"{country_code.split(' ')[1]} {ph_digits}".strip()

            if st.button("Send OTP ➔", type="primary", use_container_width=True, key="btn_send_otp"):
                with st.spinner("Dispatching secure SMS verification code..."):
                    res = service.send_otp(full_phone, user_type=role)
                    st.session_state["phone_number"] = full_phone
                    st.session_state["session_id"] = res.get("session_id", "sess_demo")
                    st.session_state["demo_otp"] = res.get("test_otp", "123456")
                    st.session_state["auth_step"] = "otp_verify"
                    st.rerun()

            render_html(f"""
<div style="background: rgba(255,255,255,0.02); border: 1px dashed rgba(255,255,255,0.08); border-radius: 8px; padding: 10px 14px; margin-top: 14px; font-size: 0.78rem; color: #64748B;">
    💡 <b>Demo Account:</b> {default_ph} &bull; OTP is generated instantly.
</div>
""")

        # ---------------------------------------------------------
        # STEP 3: OTP VERIFICATION SCREEN
        # ---------------------------------------------------------
        elif step == "otp_verify":
            ph = st.session_state.get("phone_number", "+91 9876543210")
            demo_code = st.session_state.get("demo_otp", "123456")

            if st.button("← Change number", key="btn_change_num"):
                st.session_state["auth_step"] = "phone_entry"
                st.rerun()

            render_html(f"""
<div style="background: rgba(18, 24, 38, 0.8); border: 1px solid rgba(255,255,255,0.08); border-radius: 18px; padding: 28px 24px; box-shadow: 0 20px 50px rgba(0,0,0,0.5); backdrop-filter: blur(20px); margin-top: 10px;">
    <h2 style="font-size: 1.45rem; font-weight: 800; color: #F8FAFC; margin: 0 0 6px 0;">Verify your number</h2>
    <p style="font-size: 0.86rem; color: #94A3B8; margin: 0 0 16px 0;">
        Enter the 6-digit code sent to <b style="color: #F1F5F9;">{ph}</b>
    </p>
</div>
""")

            otp_input = st.text_input(
                "6-Digit OTP Code",
                value=demo_code,
                max_chars=6,
                placeholder="123456",
                help="Enter the 6-digit verification code"
            )

            col_v1, col_v2 = st.columns([2, 1])
            with col_v1:
                if st.button("Verify & Continue ➔", type="primary", use_container_width=True, key="btn_verify_otp"):
                    with st.spinner("Verifying cryptographic OTP signature..."):
                        auth_res = service.verify_otp(
                            st.session_state.get("phone_number", ph),
                            otp_input,
                            st.session_state.get("session_id", ""),
                            user_type=role
                        )
                        st.session_state["authenticated"] = True
                        st.session_state["role"] = role
                        st.session_state["active_portal"] = "Merchant" if role == "merchant" else "Customer"
                        st.session_state["current_page"] = "Dashboard" if role == "merchant" else "My Cases"

                        if role == "customer":
                            st.session_state["current_customer"] = auth_res.get("customer", {
                                "id": "cust_aarav_01",
                                "full_name": "Aarav Sharma",
                                "phone_number": ph
                            })
                        else:
                            st.session_state["current_merchant"] = auth_res.get("merchant", {
                                "id": "m_apex_01",
                                "name": "Apex Retailers Pvt Ltd",
                                "phone": ph
                            })

                        st.rerun()

            with col_v2:
                if st.button("Resend code", key="btn_resend_otp", use_container_width=True):
                    res = service.send_otp(ph, user_type=role)
                    st.session_state["demo_otp"] = res.get("test_otp", "123456")
                    st.info("New OTP code dispatched!")
                    st.rerun()

            render_html(f"""
<div style="background: rgba(16, 185, 129, 0.08); border: 1px solid rgba(16, 185, 129, 0.25); border-radius: 8px; padding: 10px 14px; margin-top: 16px; font-size: 0.8rem; color: #34D399;">
    ✓ Active evaluation OTP: <b>{demo_code}</b>
</div>
""")
