"""
Chargeback Evidence AI - Authentication & Onboarding View
Implements 3-Screen Onboarding:
Screen 1: Phone OTP Authentication (Supabase Auth / Demo engine)
Screen 2: Merchant Business Profile (GST, PAN, Address, Category)
Screen 3: Secure Document Vault (Upload GST cert, PAN, Reg cert, Address proof with verification status)
"""

import streamlit as st


def render_auth_view(service):
    st.markdown("""
    <div style="margin-bottom: 24px;">
        <h2 style="margin: 0; color: #F8FAFC; font-weight: 700; letter-spacing: -0.02em;">Merchant Access & Verification Vault</h2>
        <p style="color: #94A3B8; font-size: 0.88rem; margin-top: 4px;">Secure biometric & SMS OTP gateway backed by Supabase Auth and RLS document encryption.</p>
    </div>
    """, unsafe_allow_html=True)

    tab1, tab2, tab3 = st.tabs([
        "📱 Screen 1: Phone OTP Login",
        "🏢 Screen 2: Merchant Profile",
        "🛡️ Screen 3: Secure Document Vault"
    ])

    # -------------------------------------------------------------
    # SCREEN 1: Phone OTP Login
    # -------------------------------------------------------------
    with tab1:
        st.markdown('<div class="fintech-card">', unsafe_allow_html=True)
        st.markdown('<div class="card-title"><span>Phone OTP Authentication</span><span class="sub-tag">Supabase Auth</span></div>', unsafe_allow_html=True)
        st.markdown('<p class="card-subtitle">Zero-password passwordless merchant authentication. Enter registered business mobile number.</p>', unsafe_allow_html=True)

        col1, col2 = st.columns([2, 1])
        with col1:
            phone_input = st.text_input("Registered Phone Number", value=st.session_state.get("merchant_phone", "+91 9876543210"))
        with col2:
            st.write("")
            st.write("")
            if st.button("Send Verification Code", use_container_width=True, type="primary"):
                res = service.send_otp(phone_input)
                st.session_state["otp_sent"] = True
                st.session_state["session_id"] = res["session_id"]
                st.session_state["demo_otp"] = res["test_otp"]
                st.success(f"OTP sent! (Demo evaluation code: **{res['test_otp']}**)")

        if st.session_state.get("otp_sent", True):
            st.write("---")
            otp_val = st.text_input("Enter 6-Digit OTP Code", value=st.session_state.get("demo_otp", "742918"))
            if st.button("Verify OTP & Authorize Session", use_container_width=True):
                auth_res = service.verify_otp(phone_input, otp_val, st.session_state.get("session_id", ""))
                st.session_state["authenticated"] = True
                st.session_state["current_merchant"] = auth_res["merchant"]
                st.balloons()
                st.success(f"Welcome, {auth_res['merchant']['name']}! Merchant session authorized with Supabase RLS.")

        st.markdown('</div>', unsafe_allow_html=True)

    # -------------------------------------------------------------
    # SCREEN 2: Merchant Profile
    # -------------------------------------------------------------
    with tab2:
        st.markdown('<div class="fintech-card">', unsafe_allow_html=True)
        st.markdown('<div class="card-title"><span>Business Information Profile</span><span class="sub-tag">KYC Level 2</span></div>', unsafe_allow_html=True)
        st.markdown('<p class="card-subtitle">Business credentials used in dispute representment filings and arbitration dockets.</p>', unsafe_allow_html=True)

        m = service.get_merchant_profile()
        with st.form("merchant_profile_form"):
            col_a, col_b = st.columns(2)
            with col_a:
                name = st.text_input("Legal Business Name", value=m.get("name", "Apex Retailers Pvt Ltd"))
                email = st.text_input("Authorized Dispute Email", value=m.get("email", "finance@apexretail.in"))
                btype = st.selectbox("Industry / Business Model", ["E-Commerce / D2C", "SaaS / Digital Goods", "Travel / Hospitality", "Logistics"], index=0)
            with col_b:
                gst = st.text_input("Goods & Services Tax (GSTIN)", value=m.get("gst_number", "29AAAAA0000A1Z5"))
                pan = st.text_input("Business PAN", value=m.get("pan_number", "ABCDE1234F"))
                phone = st.text_input("Contact Phone", value=m.get("phone", "+91 9876543210"))

            address = st.text_area("Registered Corporate Address", value=m.get("address", "42, Indiranagar 100ft Rd, Bengaluru, Karnataka 560038"))

            submitted = st.form_submit_button("Update Merchant Profile", use_container_width=True)
            if submitted:
                service.update_merchant_profile({
                    "id": m["id"],
                    "name": name,
                    "email": email,
                    "phone": phone,
                    "gst_number": gst,
                    "pan_number": pan,
                    "business_type": btype,
                    "address": address
                })
                st.session_state["current_merchant"] = service.get_merchant_profile()
                st.success("Merchant profile updated successfully!")

        st.markdown('</div>', unsafe_allow_html=True)

    # -------------------------------------------------------------
    # SCREEN 3: Secure Document Vault
    # -------------------------------------------------------------
    with tab3:
        st.markdown('<div class="fintech-card">', unsafe_allow_html=True)
        st.markdown('<div class="card-title"><span>Merchant Secure Document Vault</span><span class="sub-tag">Supabase Storage</span></div>', unsafe_allow_html=True)
        st.markdown('<p class="card-subtitle">Upload corporate identity certificates. Once verified, these proofs auto-attach to bank dispute filings.</p>', unsafe_allow_html=True)

        col_up1, col_up2 = st.columns([1, 2])
        with col_up1:
            doc_choice = st.selectbox("Document Category", [
                "GST Certificate",
                "Business PAN Card",
                "Company Incorporation / Registration",
                "Corporate Address Proof"
            ])
            uploaded_file = st.file_uploader("Select Certificate (PDF or Image)", type=["pdf", "png", "jpg", "jpeg"])
            if uploaded_file and st.button("Upload to Secure Vault", type="primary"):
                dtype_code = doc_choice.split()[0].upper()
                service.upload_vault_doc(dtype_code, uploaded_file.name, uploaded_file.getvalue())
                st.success(f"Uploaded {uploaded_file.name} to Supabase Storage with instant SHA-256 verification!")

        with col_up2:
            st.markdown("#### Vault Inventory & Verification Status")
            m = service.get_merchant_profile()
            vault_items = m.get("vault_documents", [])
            if vault_items:
                for v in vault_items:
                    st.markdown(f"""
                    <div style="display: flex; justify-content: space-between; align-items: center; padding: 10px 14px; background: rgba(0,0,0,0.3); border: 1px solid rgba(255,255,255,0.06); border-radius: 8px; margin-bottom: 8px;">
                        <div>
                            <div style="font-weight: 600; font-size: 0.88rem; color: #F1F5F9;">📁 {v['file_name']}</div>
                            <div style="font-size: 0.74rem; color: #94A3B8;">Type: <b>{v['doc_type']}</b> &bull; Uploaded: {v.get('uploaded_at', '')[:10]}</div>
                        </div>
                        <span class="status-pill complete">✓ {v.get('verification_status', 'VERIFIED')}</span>
                    </div>
                    """, unsafe_allow_html=True)
            else:
                st.info("No documents in vault yet. Upload your business certificates above.")

        st.markdown('</div>', unsafe_allow_html=True)
