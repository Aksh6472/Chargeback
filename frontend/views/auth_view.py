"""
Chargeback Evidence AI - Premium Fintech Authentication & Portal Selection
Stripe/Ramp/Brex/Linear inspired landing & authentication experience:
1. Split-Screen Hero + Value Matrix (Left) & Glassmorphism Card (Right)
2. Step 1: Portal Selection (Large interactive cards for Merchant and Customer)
3. Step 2: Phone Login (Country code + Phone Number, no OTP visible yet)
4. Step 3: 6-Digit OTP Verification (Centered monospace digits, resend code)
5. Step 4: Automatic session authorization & role-based routing
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
    # TWO-COLUMN SPLIT SCREEN: LEFT BRAND HERO / RIGHT AUTH CARD
    # -----------------------------------------------------------------
    col_left, col_right = st.columns([1.15, 1.0], gap="large")

    # =================================================================
    # LEFT COLUMN: BRANDING, HEADLINE, VALUE GRID, PARTNERS
    # =================================================================
    with col_left:
        render_html("""
<div style="padding: 10px 10px 20px 0;">
    <!-- Top Brand Header -->
    <div class="landing-brand-header">
        <div class="landing-brand-logo">
            <div class="landing-logo-icon">
                <svg width="20" height="20" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2.5" stroke-linecap="round" stroke-linejoin="round">
                    <polygon points="12 2 2 7 12 12 22 7 12 2"></polygon>
                    <polyline points="2 17 12 22 22 17"></polyline>
                    <polyline points="2 12 12 17 22 12"></polyline>
                </svg>
            </div>
            <span class="landing-brand-name">Chargeback Evidence AI</span>
        </div>
        <span class="landing-tagline">Disputes. Resolved.</span>
    </div>

    <!-- Small Badge -->
    <div class="landing-badge">
        <span>✦</span>
        <span>AI-POWERED DISPUTE INTELLIGENCE</span>
    </div>

    <!-- Main Headline -->
    <h1 class="landing-headline">
        Turn chargeback<br>
        evidence into<br>
        <span class="gradient-text">winning cases.</span>
    </h1>

    <!-- Supporting Text -->
    <p class="landing-subtitle">
        Investigate disputes, verify documents, uncover contradictions, and generate submission-ready evidence packets with AI.
    </p>

    <!-- 4 Subtle Trust/Value Indicators (2x2 Grid) -->
    <div class="trust-grid">
        <div class="trust-item">
            <div class="trust-icon investigation">✦</div>
            <div>
                <div class="trust-item-title">AI Investigation</div>
                <div class="trust-item-desc">Analyze and extract key evidence</div>
            </div>
        </div>
        <div class="trust-item">
            <div class="trust-icon verification">🛡️</div>
            <div>
                <div class="trust-item-title">Evidence Verification</div>
                <div class="trust-item-desc">Cross-check and detect inconsistencies</div>
            </div>
        </div>
        <div class="trust-item">
            <div class="trust-icon traceability">📄</div>
            <div>
                <div class="trust-item-title">Source Traceability</div>
                <div class="trust-item-desc">Every claim backed by source</div>
            </div>
        </div>
        <div class="trust-item">
            <div class="trust-icon vault">🔒</div>
            <div>
                <div class="trust-item-title">Secure Evidence Vault</div>
                <div class="trust-item-desc">Your data, always protected</div>
            </div>
        </div>
    </div>

    <!-- Partners Section -->
    <div class="partners-section">
        <div class="partners-label">Trusted by modern businesses</div>
        <div class="partners-row">
            <span class="partner-logo">stripe</span>
            <span class="partner-logo">shopify</span>
            <span class="partner-logo">Razorpay</span>
            <span class="partner-logo">Paytm</span>
        </div>
    </div>
</div>
""")

    # =================================================================
    # RIGHT COLUMN: GLASSMORPHISM AUTHENTICATION CARD
    # =================================================================
    with col_right:
        st.write("")
        with st.container(key="auth_card_container"):
            # -------------------------------------------------------------
            # STEP 1: PORTAL SELECTION (MERCHANT VS CUSTOMER)
            # -------------------------------------------------------------
            if step == "portal_select":
                render_html("""
<div>
    <div class="auth-card-heading">Welcome back</div>
    <div class="auth-card-subheading">Choose how you'd like to access your workspace.</div>

    <!-- Merchant Portal Card Visual -->
    <div class="portal-card-box merchant-card">
        <div class="portal-card-left">
            <div class="portal-card-icon merchant">
                <svg width="24" height="24" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round">
                    <rect x="4" y="2" width="16" height="20" rx="2" ry="2"></rect>
                    <path d="M9 22v-4h6v4"></path>
                    <path d="M8 6h.01"></path>
                    <path d="M16 6h.01"></path>
                    <path d="M8 10h.01"></path>
                    <path d="M16 10h.01"></path>
                    <path d="M8 14h.01"></path>
                    <path d="M16 14h.01"></path>
                </svg>
            </div>
            <div>
                <div class="portal-card-title">Merchant Portal</div>
                <div class="portal-card-desc">
                    Manage chargebacks, investigate evidence, and create AI-powered submission-ready evidence packets.
                </div>
            </div>
        </div>
        <div class="portal-card-arrow">→</div>
    </div>
</div>
""")
                # Clickable overlay button for Merchant Portal
                if st.button("Select Merchant Portal", key="btn_portal_merchant", use_container_width=True):
                    st.session_state["auth_role"] = "merchant"
                    st.session_state["auth_step"] = "phone_entry"
                    st.rerun()

                # Customer Portal Card Visual
                render_html("""
<div>
    <div class="portal-card-box customer-card">
        <div class="portal-card-left">
            <div class="portal-card-icon customer">
                <svg width="24" height="24" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round">
                    <path d="M19 21v-2a4 4 0 0 0-4-4H9a4 4 0 0 0-4 4v2"></path>
                    <circle cx="12" cy="7" r="4"></circle>
                </svg>
            </div>
            <div>
                <div class="portal-card-title">Customer Portal</div>
                <div class="portal-card-desc">
                    Upload requested documents, manage your proof vault, and track your dispute case.
                </div>
            </div>
        </div>
        <div class="portal-card-arrow">→</div>
    </div>

    <!-- Security Footer -->
    <div class="auth-card-footer">
        <div class="auth-card-footer-item">
            <svg width="14" height="14" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round">
                <rect x="3" y="11" width="18" height="11" rx="2" ry="2"></rect>
                <path d="M7 11V7a5 5 0 0 1 10 0v4"></path>
            </svg>
            <span>Secure login powered by Supabase</span>
        </div>
        <div class="auth-card-footer-sub">Your data is encrypted and always protected.</div>
    </div>
</div>
""")
                # Clickable overlay button for Customer Portal
                if st.button("Select Customer Portal", key="btn_portal_customer", use_container_width=True):
                    st.session_state["auth_role"] = "customer"
                    st.session_state["auth_step"] = "phone_entry"
                    st.rerun()

            # -------------------------------------------------------------
            # STEP 2: PHONE LOGIN (REPLACES CONTENT IN SAME CARD)
            # -------------------------------------------------------------
            elif step == "phone_entry":
                title_role = "Merchant" if role == "merchant" else "Customer"
                default_phone = "9876543210" if role == "merchant" else "9123456780"

                if st.button("← Back to portal selection", key="btn_back_to_portals"):
                    st.session_state["auth_step"] = "portal_select"
                    st.rerun()

                render_html(f"""
<div style="margin-top: 10px;">
    <div style="margin-bottom: 12px;">
        <span class="sub-tag" style="background: rgba(59, 130, 246, 0.15); color: #93C5FD; border-color: rgba(59, 130, 246, 0.3);">
            {title_role.upper()} PORTAL
        </span>
    </div>
    <div class="auth-card-heading">Sign in as {title_role}</div>
    <div class="auth-card-subheading">
        Enter your mobile number and we'll send you a secure verification code.
    </div>
</div>
""")

                col_cc, col_num = st.columns([1.1, 2.5])
                with col_cc:
                    country_code = st.selectbox("Country", ["🇮🇳 +91", "🇺🇸 +1", "🇬🇧 +44", "🇦🇪 +971", "🇸🇬 +65"], index=0)
                with col_num:
                    ph_digits = st.text_input("Mobile Number", value=default_phone, placeholder="9876543210")

                full_phone = f"{country_code.split(' ')[1]} {ph_digits}".strip()

                st.write("")
                if st.button("Continue →", type="primary", use_container_width=True, key="btn_send_otp"):
                    with st.spinner("Dispatching secure verification code..."):
                        res = service.send_otp(full_phone, user_type=role)
                        st.session_state["phone_number"] = full_phone
                        st.session_state["session_id"] = res.get("session_id", "sess_demo")
                        st.session_state["demo_otp"] = res.get("test_otp", "123456")
                        st.session_state["auth_step"] = "otp_verify"
                        st.rerun()

                render_html("""
<div style="text-align: center; margin-top: 16px; font-size: 0.76rem; color: #64748B; line-height: 1.4;">
    By continuing, you agree to securely verify your account using a one-time code.
</div>
""")

            # -------------------------------------------------------------
            # STEP 3: OTP VERIFICATION (REPLACES CONTENT IN SAME CARD)
            # -------------------------------------------------------------
            elif step == "otp_verify":
                ph = st.session_state.get("phone_number", "+91 98765 43210")
                demo_code = st.session_state.get("demo_otp", "123456")

                if st.button("← Change number", key="btn_change_num"):
                    st.session_state["auth_step"] = "phone_entry"
                    st.rerun()

                render_html(f"""
<div style="margin-top: 10px;">
    <div style="margin-bottom: 12px;">
        <span class="sub-tag" style="background: rgba(59, 130, 246, 0.15); color: #93C5FD; border-color: rgba(59, 130, 246, 0.3);">
            SECURITY CHECK
        </span>
    </div>
    <div class="auth-card-heading">Verify your number</div>
    <div class="auth-card-subheading">
        We've sent a 6-digit verification code to: <br>
        <b style="color: #F8FAFC; font-size: 1.05rem;">{ph}</b>
    </div>
</div>
""")

                otp_input = st.text_input(
                    "6-Digit Verification Code",
                    value=demo_code,
                    max_chars=6,
                    placeholder="123456",
                    help="Enter the 6-digit verification code sent to your phone"
                )

                st.write("")
                if st.button("Verify & Continue →", type="primary", use_container_width=True, key="btn_verify_otp"):
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

                # Resend code
                st.write("")
                c_resend, _ = st.columns([2, 1])
                with c_resend:
                    if st.button("Didn't receive a code? Resend code", key="btn_resend_otp"):
                        res = service.send_otp(ph, user_type=role)
                        st.session_state["demo_otp"] = res.get("test_otp", "123456")
                        st.info("New verification code dispatched!")
                        st.rerun()

                render_html(f"""
<div style="background: rgba(16, 185, 129, 0.08); border: 1px solid rgba(16, 185, 129, 0.25); border-radius: 10px; padding: 10px 14px; margin-top: 16px; font-size: 0.8rem; color: #34D399; text-align: center;">
    ✓ Active evaluation OTP code: <b>{demo_code}</b>
</div>
""")
