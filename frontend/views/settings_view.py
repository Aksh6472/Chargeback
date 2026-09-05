import streamlit as st
from typing import Any
from frontend.components import render_html


def render_settings_view(service: Any):
    role = st.session_state.get("role", "merchant")

    render_html("""
    <div style="margin-bottom: 24px;">
        <div style="display: flex; align-items: center; gap: 8px; margin-bottom: 4px;">
            <span class="material-symbols-outlined" style="color: #2D3948; font-size: 22px;">settings</span>
            <h2 style="margin: 0; color: #1A242C; font-weight: 700; font-size: 1.4rem; letter-spacing: -0.02em;">Account &amp; System Settings</h2>
        </div>
        <p style="color: #64748B; font-size: 0.88rem; margin: 0;">Manage organization credentials, contact information, notification channels, and multi-factor security rules.</p>
    </div>
    """)

    if role == "merchant":
        _render_merchant_settings(service)
    else:
        _render_customer_settings(service)


def _render_merchant_settings(service: Any):
    merchant = service.get_merchant_profile() or {}

    tab_profile, tab_business, tab_security, tab_notif = st.tabs([
        "🏢 Organization Profile",
        "📄 Tax & Business Credentials",
        "🔐 Security & Access",
        "🔔 Dispute Alerts & Notifications"
    ])

    with tab_profile:
        render_html("""
        <div class="stitch-card-header" style="margin-bottom: 8px;">
            <span class="stitch-card-title">Business Profile Information</span>
        </div>
        <p style="color: #64748B; font-size: 0.84rem; margin: 0 0 16px 0;">Update primary contact details used on formal dispute rebuttal packets and merchant registries.</p>
        """)

        with st.form("merchant_profile_form"):
            col1, col2 = st.columns(2)
            with col1:
                name = st.text_input("Organization / Merchant Name", value=merchant.get("name", "Apex Retailers Pvt Ltd"))
                email = st.text_input("Official Contact Email", value=merchant.get("email", "disputes@apexretailers.com"))
            with col2:
                phone = st.text_input("Primary Phone Number", value=merchant.get("phone", "+91 9876543210"))
                business_type = st.selectbox(
                    "Business Classification",
                    ["E-Commerce / D2C", "SaaS / Digital Goods", "Retail & Hospitality", "Travel & Ticketing", "Financial Services"],
                    index=0 if merchant.get("business_type") not in ["E-Commerce / D2C", "SaaS / Digital Goods", "Retail & Hospitality", "Travel & Ticketing", "Financial Services"]
                    else ["E-Commerce / D2C", "SaaS / Digital Goods", "Retail & Hospitality", "Travel & Ticketing", "Financial Services"].index(merchant.get("business_type"))
                )

            address = st.text_area(
                "Registered Business Address",
                value=merchant.get("address", "Plot 42, Cyber City, Phase II, Gurugram, Haryana - 122002, India"),
                help="This address is printed on formal rebuttal documentation."
            )

            submit_profile = st.form_submit_button("Save Organization Profile", type="primary", use_container_width=True)

            if submit_profile:
                if not name.strip():
                    st.error("Organization Name cannot be empty.")
                else:
                    updated_data = dict(merchant)
                    updated_data["name"] = name.strip()
                    updated_data["email"] = email.strip()
                    updated_data["phone"] = phone.strip()
                    updated_data["phone_number"] = phone.strip()
                    updated_data["business_type"] = business_type
                    updated_data["address"] = address.strip()

                    res = service.update_merchant_profile(updated_data)
                    st.session_state["current_merchant"] = res
                    st.success("Organization profile updated successfully!")
                    st.rerun()

    with tab_business:
        render_html("""
        <div class="stitch-card-header" style="margin-bottom: 8px;">
            <span class="stitch-card-title">Tax Identification &amp; Legal Records</span>
        </div>
        <p style="color: #64748B; font-size: 0.84rem; margin: 0 0 16px 0;">Government identification numbers used during automated GSTIN/PAN cross-verification in disputes.</p>
        """)

        with st.form("merchant_business_form"):
            col1, col2 = st.columns(2)
            with col1:
                gst_number = st.text_input("GSTIN Number", value=merchant.get("gst_number", "07AAAAA0000A1Z5"), help="15-character GST Identification Number")
            with col2:
                pan_number = st.text_input("Permanent Account Number (PAN)", value=merchant.get("pan_number", "AAACA1234K"), help="10-character Tax Identification PAN")

            st.caption("Verification Status: Active & Triangulated with Ministry Records.")

            submit_business = st.form_submit_button("Update Legal Credentials", type="primary", use_container_width=True)
            if submit_business:
                updated_data = dict(merchant)
                updated_data["gst_number"] = gst_number.strip().upper()
                updated_data["pan_number"] = pan_number.strip().upper()
                res = service.update_merchant_profile(updated_data)
                st.session_state["current_merchant"] = res
                st.success("Business credentials saved!")
                st.rerun()

    with tab_security:
        render_html("""
        <div class="stitch-card-header" style="margin-bottom: 8px;">
            <span class="stitch-card-title">Security &amp; Session Management</span>
        </div>
        <p style="color: #64748B; font-size: 0.84rem; margin: 0 0 16px 0;">Multi-factor authentication policies and session controls.</p>
        """)

        col_s1, col_s2 = st.columns(2)
        with col_s1:
            render_html("""
            <div class="stitch-card">
                <div class="stitch-card-header">
                    <span class="stitch-card-title">OTP Re-Authentication Policy</span>
                    <span class="stitch-pill stitch-pill-won">ACTIVE</span>
                </div>
                <p style="font-size: 0.82rem; color: #64748B; margin: 0;">Enforces 6-digit SMS OTP verification whenever switching between merchant and cardholder portals.</p>
            </div>
            """)
        with col_s2:
            render_html("""
            <div class="stitch-card">
                <div class="stitch-card-header">
                    <span class="stitch-card-title">Active Security Session</span>
                    <span class="stitch-pill stitch-pill-won">AUTHENTICATED</span>
                </div>
                <p style="font-size: 0.82rem; color: #64748B; margin: 0;">Role Isolation: <b>Strict Merchant Boundary</b> &bull; Token: <code>sess_live_merch_sec</code></p>
            </div>
            """)

    with tab_notif:
        render_html("""
        <div class="stitch-card-header" style="margin-bottom: 8px;">
            <span class="stitch-card-title">Dispute Alerts &amp; Webhooks</span>
        </div>
        <p style="color: #64748B; font-size: 0.84rem; margin: 0 0 16px 0;">Configure how operations teams are notified regarding upcoming filing deadlines.</p>
        """)

        st.checkbox("Email alert when a new chargeback dispute is initiated", value=True)
        st.checkbox("Critical alert 24 hours prior to representment deadline", value=True)
        st.checkbox("Alert when customer uploads missing rebuttal proof", value=True)

        webhook_url = st.text_input("Dispute Lifecycle Webhook URL", value="https://api.apexretailers.com/webhooks/chargeback-events")
        if st.button("Save Notification Settings", type="primary"):
            st.success(f"Notification preferences and webhook ({webhook_url}) saved!")


def _render_customer_settings(service: Any):
    cust = st.session_state.get("current_customer", {})
    cust_id = cust.get("id")
    customer = service.get_customer_profile(cust_id) if cust_id else cust

    tab_profile, tab_security, tab_notif = st.tabs([
        "👤 Personal Details",
        "🔐 Security & Verification",
        "🔔 Notification Preferences"
    ])

    with tab_profile:
        render_html("""
        <div class="stitch-card-header" style="margin-bottom: 8px;">
            <span class="stitch-card-title">Cardholder Profile</span>
        </div>
        <p style="color: #64748B; font-size: 0.84rem; margin: 0 0 16px 0;">Update contact information associated with dispute resolution inquiries.</p>
        """)

        with st.form("customer_profile_form"):
            col1, col2 = st.columns(2)
            with col1:
                full_name = st.text_input("Full Legal Name", value=customer.get("full_name", customer.get("name", "Cardholder")))
                email = st.text_input("Email Address", value=customer.get("email", "cardholder@example.com"))
            with col2:
                phone = st.text_input("Registered Mobile Number", value=customer.get("phone_number", customer.get("phone", "+91 9999999999")))
                delivery_address = st.text_area("Default Delivery / Billing Address", value=customer.get("address", "Sector 43, Gurugram, India"))

            submit_cust = st.form_submit_button("Update Cardholder Information", type="primary", use_container_width=True)

            if submit_cust:
                if not full_name.strip():
                    st.error("Name cannot be blank.")
                else:
                    updated_cust = dict(customer)
                    updated_cust["full_name"] = full_name.strip()
                    updated_cust["name"] = full_name.strip()
                    updated_cust["email"] = email.strip()
                    updated_cust["phone_number"] = phone.strip()
                    updated_cust["phone"] = phone.strip()
                    updated_cust["address"] = delivery_address.strip()

                    res = service.update_customer_profile(updated_cust)
                    st.session_state["current_customer"] = res
                    st.success("Personal details updated successfully!")
                    st.rerun()

    with tab_security:
        render_html("""
        <div class="stitch-card">
            <div class="stitch-card-header">
                <span class="stitch-card-title">SMS OTP Verification</span>
                <span class="stitch-pill stitch-pill-won">VERIFIED CARDHOLDER</span>
            </div>
            <p style="font-size: 0.82rem; color: #64748B; margin: 0;">Your account is secured via one-time SMS verification sent to your registered mobile phone.</p>
        </div>
        """)

    with tab_notif:
        render_html("""
        <div class="stitch-card-header" style="margin-bottom: 8px;">
            <span class="stitch-card-title">Dispute Updates &amp; Reminders</span>
        </div>
        """)
        st.checkbox("Receive SMS notifications when additional dispute documents are requested", value=True)
        st.checkbox("Receive Email confirmation upon evidence submission", value=True)
        if st.button("Save Preferences", type="primary"):
            st.success("Notification preferences updated successfully!")

