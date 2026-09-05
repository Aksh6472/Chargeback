"""
Chargeback Evidence AI - Stitch Minimalist Authentication & Portal Selection
Matching sign_in_chargeback_evidence_ai/code.html with:
1. Left Pane: Institutional Brand Dossier & Network Canvas (SOC-2 Type II Certified, Audit Trail, Network Shield)
2. Right Pane: Clean Workspace Authentication Card with:
   - Step 1: Portal Choice (Merchant Portal vs Customer Portal)
   - Step 2: Phone Login (Country Code + Phone Number + Send OTP)
   - Step 3: 6-Digit OTP Verification (Centered Monospace Input + Resend Code)
"""

import streamlit as st
from frontend.components import render_html


def render_auth_view(service):
    # Initialize authentication step & role in session state
    if "auth_step" not in st.session_state:
        st.session_state["auth_step"] = "portal_select"  # portal_select | phone_entry | otp_verify
    if "auth_role" not in st.session_state:
        st.session_state["auth_role"] = "merchant"  # merchant | customer

    step = st.session_state["auth_step"]
    role = st.session_state["auth_role"]

    # -----------------------------------------------------------------
    # TWO-COLUMN SPLIT SCREEN: LEFT BRAND DOSSIER / RIGHT AUTH CARD
    # -----------------------------------------------------------------
    col_left, col_right = st.columns([1.1, 1.0], gap="large")

    # =================================================================
    # LEFT COLUMN: BRAND DOSSIER & ENTERPRISE METADATA
    # =================================================================
    with col_left:
        render_html("""
<div style="background: #1A242C; color: #FFFFFF; border-radius: 16px; padding: 2.75rem 2.25rem; display: flex; flex-direction: column; justify-content: space-between; min-height: 580px; position: relative; overflow: hidden; box-shadow: 0 10px 25px -5px rgba(26,36,44,0.2);">
    <!-- Header Brand Line -->
    <div>
        <div style="display: flex; align-items: center; gap: 12px; margin-bottom: 2rem;">
            <div style="width: 38px; height: 38px; border-radius: 10px; background: rgba(255,255,255,0.1); border: 1px solid rgba(255,255,255,0.15); display: flex; align-items: center; justify-content: center; font-size: 1.1rem; color: #FFFFFF;">
                <span class="material-symbols-outlined" style="font-size: 22px;">shield</span>
            </div>
            <div>
                <div style="font-weight: 800; font-size: 1.15rem; color: #FFFFFF; letter-spacing: -0.02em;">Chargeback Evidence AI</div>
                <div style="font-size: 0.68rem; color: #98A4AD; letter-spacing: 0.08em; text-transform: uppercase; font-weight: 700;">DISPUTE ARBITRATION PLATFORM</div>
            </div>
        </div>

        <!-- Compliance Pill -->
        <div style="display: inline-flex; align-items: center; gap: 8px; background: rgba(255,255,255,0.08); border: 1px solid rgba(255,255,255,0.12); padding: 5px 12px; border-radius: 9999px; margin-bottom: 1.5rem;">
            <span style="width: 6px; height: 6px; border-radius: 50%; background: #4EDEA3;"></span>
            <span class="font-mono" style="font-size: 0.7rem; color: #6FFBBE; font-weight: 600; letter-spacing: 0.04em;">SOC-2 TYPE II AUDITED &bull; REGULATION COMPLIANT</span>
        </div>

        <!-- Headline & Subtitle -->
        <h1 style="font-size: 2.35rem; font-weight: 800; color: #FFFFFF; letter-spacing: -0.03em; line-height: 1.15; margin: 0 0 1rem 0;">
            Evidence. Clarity.<br>Confidence.
        </h1>
        <p style="font-size: 0.95rem; color: #BCC8D2; line-height: 1.55; margin: 0 0 2rem 0; max-width: 480px;">
            The enterprise platform for dispute defense, intelligent documentation, and automated chargeback recovery.
        </p>

        <!-- Feature Bullets -->
        <div style="display: flex; flex-direction: column; gap: 14px;">
            <div style="display: flex; align-items: flex-start; gap: 10px;">
                <div style="width: 22px; height: 22px; border-radius: 50%; background: #00422B; color: #10B981; display: flex; align-items: center; justify-content: center; flex-shrink: 0; margin-top: 1px;">
                    <span class="material-symbols-outlined" style="font-size: 14px;">check</span>
                </div>
                <span style="font-size: 0.88rem; color: #F2F4F6;">Organize dispute evidence with complete audit trails</span>
            </div>
            <div style="display: flex; align-items: flex-start; gap: 10px;">
                <div style="width: 22px; height: 22px; border-radius: 50%; background: #00422B; color: #10B981; display: flex; align-items: center; justify-content: center; flex-shrink: 0; margin-top: 1px;">
                    <span class="material-symbols-outlined" style="font-size: 14px;">check</span>
                </div>
                <span style="font-size: 0.88rem; color: #F2F4F6;">Build stronger, card-network compliant case files</span>
            </div>
            <div style="display: flex; align-items: flex-start; gap: 10px;">
                <div style="width: 22px; height: 22px; border-radius: 50%; background: #00422B; color: #10B981; display: flex; align-items: center; justify-content: center; flex-shrink: 0; margin-top: 1px;">
                    <span class="material-symbols-outlined" style="font-size: 14px;">check</span>
                </div>
                <span style="font-size: 0.88rem; color: #F2F4F6;">Keep your transaction and customer data enterprise-secure</span>
            </div>
        </div>
    </div>

    <!-- Footer Metadata -->
    <div style="border-top: 1px solid rgba(255,255,255,0.1); padding-top: 1.25rem; margin-top: 2rem; display: flex; justify-content: space-between; align-items: center; font-size: 0.74rem; color: #98A4AD;">
        <span>&copy; 2026 Chargeback Evidence AI Inc.</span>
        <div style="display: flex; align-items: center; gap: 6px;">
            <span class="material-symbols-outlined" style="font-size: 15px; color: #4EDEA3;">verified_user</span>
            <span>TLS 1.3 Encrypted</span>
        </div>
    </div>
</div>
""")

    # =================================================================
    # RIGHT COLUMN: WORKSPACE AUTHENTICATION CARD
    # =================================================================
    with col_right:
        st.write("")
        with st.container():
            # -------------------------------------------------------------
            # STEP 1: PORTAL SELECTION (MERCHANT VS CUSTOMER)
            # -------------------------------------------------------------
            if step == "portal_select":
                render_html("""
<div style="margin-bottom: 1.5rem;">
    <h2 style="font-size: 1.6rem; font-weight: 800; color: #191C1E; letter-spacing: -0.025em; margin: 0 0 4px 0;">
        Sign in to your account
    </h2>
    <p style="font-size: 0.88rem; color: #64748B; margin: 0;">
        Choose how you would like to access your chargeback workspace.
    </p>
</div>
""")

                # Merchant Choice Card
                render_html("""
<div class="stitch-card" style="padding: 1.25rem; margin-bottom: 0.75rem; border: 1px solid #E5E7EB;">
    <div style="display: flex; align-items: center; justify-content: space-between;">
        <div style="display: flex; align-items: center; gap: 12px;">
            <div style="width: 40px; height: 40px; border-radius: 10px; background: #2F3A42; color: #FFFFFF; display: flex; align-items: center; justify-content: center;">
                <span class="material-symbols-outlined" style="font-size: 20px;">storefront</span>
            </div>
            <div>
                <div style="font-weight: 700; font-size: 0.98rem; color: #191C1E;">Merchant Portal</div>
                <div style="font-size: 0.8rem; color: #64748B; margin-top: 1px;">Manage disputes, review evidence, and generate rebuttal packets.</div>
            </div>
        </div>
    </div>
</div>
""")
                if st.button("Continue as Merchant ➔", key="btn_choose_merch", use_container_width=True, type="primary"):
                    st.session_state["auth_role"] = "merchant"
                    st.session_state["auth_step"] = "phone_entry"
                    st.rerun()

                st.write("")

                # Customer Choice Card
                render_html("""
<div class="stitch-card" style="padding: 1.25rem; margin-bottom: 0.75rem; border: 1px solid #E5E7EB;">
    <div style="display: flex; align-items: center; justify-content: space-between;">
        <div style="display: flex; align-items: center; gap: 12px;">
            <div style="width: 40px; height: 40px; border-radius: 10px; background: #ECFDF5; color: #065F46; border: 1px solid #A7F3D0; display: flex; align-items: center; justify-content: center;">
                <span class="material-symbols-outlined" style="font-size: 20px;">person</span>
            </div>
            <div>
                <div style="font-weight: 700; font-size: 0.98rem; color: #191C1E;">Customer Portal</div>
                <div style="font-size: 0.8rem; color: #64748B; margin-top: 1px;">Provide documents, manage proof vault, and track case progress.</div>
            </div>
        </div>
    </div>
</div>
""")
                if st.button("Continue as Customer ➔", key="btn_choose_cust", use_container_width=True):
                    st.session_state["auth_role"] = "customer"
                    st.session_state["auth_step"] = "phone_entry"
                    st.rerun()

                # Quick One-Click Demo Access
                st.write("---")
                render_html("""
<div style="text-align: center; margin-bottom: 8px;">
    <span style="font-size: 0.7rem; font-weight: 700; text-transform: uppercase; color: #64748B; letter-spacing: 0.06em;">
        Instant One-Click Evaluation Demo
    </span>
</div>
""")
                col_demo1, col_demo2 = st.columns(2)
                with col_demo1:
                    if st.button("🏢 Instant Merchant", key="btn_instant_m", use_container_width=True):
                        st.session_state["authenticated"] = True
                        st.session_state["role"] = "merchant"
                        st.session_state["active_portal"] = "Merchant"
                        st.session_state["current_page"] = "Dashboard"
                        st.session_state["current_merchant"] = service.get_merchant_profile()
                        st.rerun()
                with col_demo2:
                    if st.button("👤 Instant Customer", key="btn_instant_c", use_container_width=True):
                        st.session_state["authenticated"] = True
                        st.session_state["role"] = "customer"
                        st.session_state["active_portal"] = "Customer"
                        st.session_state["current_page"] = "My Cases"
                        all_c = service.list_all_customers()
                        st.session_state["current_customer"] = all_c[0] if all_c else {
                            "id": "cust_aarav_01",
                            "full_name": "Aarav Sharma",
                            "phone_number": "+91 9811223344",
                            "email": "aarav.sharma@example.com"
                        }
                        st.rerun()

            # -------------------------------------------------------------
            # STEP 2: PHONE & PROFILE SELECTION
            # -------------------------------------------------------------
            elif step == "phone_entry":
                title_role = "Merchant" if role == "merchant" else "Customer"
                default_phone = "9876543210" if role == "merchant" else "9811223344"

                if st.button("← Back to portal selection", key="btn_back_to_portals"):
                    st.session_state["auth_step"] = "portal_select"
                    st.rerun()

                render_html(f"""
<div style="margin: 1rem 0 1.25rem 0;">
    <span class="stitch-pill stitch-pill-info" style="margin-bottom: 6px;">
        <span class="stitch-pill-dot"></span>
        <span>{title_role.upper()} AUTHENTICATION</span>
    </span>
    <h2 style="font-size: 1.5rem; font-weight: 800; color: #191C1E; letter-spacing: -0.02em; margin: 4px 0 2px 0;">
        Sign in as {title_role}
    </h2>
    <p style="font-size: 0.85rem; color: #64748B; margin: 0;">
        Enter your mobile number to receive a secure verification code.
    </p>
</div>
""")

                if role == "customer":
                    demo_custs = service.list_all_customers()
                    cust_opts = {f"👤 {dc['full_name']} ({dc['phone_number']})": dc for dc in demo_custs}
                    cust_opts["Custom / Other Mobile Number"] = None

                    sel_account = st.selectbox(
                        "Customer Account",
                        list(cust_opts.keys()),
                        index=0,
                        help="Select an existing customer from the database or enter any custom mobile number."
                    )
                    chosen_obj = cust_opts.get(sel_account)
                    if chosen_obj:
                        raw_ph = chosen_obj.get("phone_number", "")
                        digits = "".join(ch for ch in raw_ph if ch.isdigit())
                        if len(digits) >= 10:
                            default_phone = digits[-10:]

                col_cc, col_num = st.columns([1.1, 2.5])
                with col_cc:
                    country_code = st.selectbox("Country", ["🇮🇳 +91", "🇺🇸 +1", "🇬🇧 +44", "🇦🇪 +971", "🇸🇬 +65"], index=0)
                with col_num:
                    ph_digits = st.text_input("Mobile Number", value=default_phone, placeholder="9876543210")

                full_phone = f"{country_code.split(' ')[1]} {ph_digits}".strip()

                st.write("")
                if st.button("Send Verification Code ➔", type="primary", use_container_width=True, key="btn_send_otp"):
                    with st.spinner("Dispatching secure verification code..."):
                        res = service.send_otp(full_phone, user_type=role)
                        st.session_state["phone_number"] = full_phone
                        st.session_state["session_id"] = res.get("session_id", "sess_demo")
                        st.session_state["demo_otp"] = res.get("test_otp", "123456")
                        st.session_state["auth_step"] = "otp_verify"
                        st.rerun()

            # -------------------------------------------------------------
            # STEP 3: OTP VERIFICATION
            # -------------------------------------------------------------
            elif step == "otp_verify":
                ph = st.session_state.get("phone_number", "+91 98765 43210")
                demo_code = st.session_state.get("demo_otp", "123456")

                if st.button("← Change number", key="btn_change_num"):
                    st.session_state["auth_step"] = "phone_entry"
                    st.rerun()

                render_html(f"""
<div style="margin: 1rem 0 1.25rem 0;">
    <span class="stitch-pill stitch-pill-success" style="margin-bottom: 6px;">
        <span class="stitch-pill-dot"></span>
        <span>SECURITY VERIFICATION</span>
    </span>
    <h2 style="font-size: 1.5rem; font-weight: 800; color: #191C1E; letter-spacing: -0.02em; margin: 4px 0 2px 0;">
        Enter verification code
    </h2>
    <p style="font-size: 0.85rem; color: #64748B; margin: 0;">
        We've dispatched a 6-digit code to <b style="color: #191C1E;">{ph}</b>
    </p>
</div>
""")

                otp_input = st.text_input(
                    "6-Digit Verification Code",
                    value=demo_code,
                    max_chars=6,
                    placeholder="123456",
                    help="Enter the 6-digit code sent to your registered number"
                )

                st.write("")
                if st.button("Verify & Sign In ➔", type="primary", use_container_width=True, key="btn_verify_otp"):
                    with st.spinner("Authorizing secure workspace session..."):
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
                                "name": "Acme Global Merchants",
                                "phone": ph
                            })

                        st.rerun()

                # Resend Option & Demo Code Notice
                st.write("")
                col_res, _ = st.columns([2, 1])
                with col_res:
                    if st.button("Resend code", key="btn_resend_otp"):
                        res = service.send_otp(ph, user_type=role)
                        st.session_state["demo_otp"] = res.get("test_otp", "123456")
                        st.info("New verification code dispatched!")
                        st.rerun()

                render_html(f"""
<div style="background: #ECFDF5; border: 1px solid #A7F3D0; border-radius: 8px; padding: 8px 12px; margin-top: 14px; font-size: 0.78rem; color: #065F46; text-align: center;">
    ✓ Active evaluation test code: <b class="font-mono">{demo_code}</b>
</div>
""")
