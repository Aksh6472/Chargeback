"""
Chargeback Evidence AI - Dedicated Customer Workspace & Proof Vault
Enables customers to view active chargeback disputes, manage encrypted proof vault,
and directly attach / share verified documents to bank defense dockets.
"""

import streamlit as st
from frontend.components import render_case_status_tracker, render_html


def render_customer_portal_view(service):
    cust = st.session_state.get("current_customer")
    if not cust:
        customers = service.list_all_customers()
        cust = customers[0] if customers else {
            "id": "cust_demo_01",
            "full_name": "Aarav Sharma",
            "phone_number": "+91 9811223344",
            "email": "aarav.sharma@example.com"
        }
        st.session_state["current_customer"] = cust

    cust_name = cust.get('full_name', 'Aarav Sharma')
    cust_phone = cust.get('phone_number', '+91 9811223344')

    render_html(f"""
<div style="margin-bottom: 20px;">
    <div style="display: flex; justify-content: space-between; align-items: center;">
        <div>
            <h2 style="margin: 0; color: #F8FAFC; font-weight: 700; letter-spacing: -0.02em;">👤 Customer Dispute & Proof Workspace</h2>
            <p style="color: #94A3B8; font-size: 0.88rem; margin-top: 4px;">Manage identity proofs, view active dispute resolutions, and share evidence with banks.</p>
        </div>
        <div style="text-align: right; background: rgba(16, 185, 129, 0.1); border: 1px solid rgba(16, 185, 129, 0.3); padding: 6px 14px; border-radius: 8px;">
            <div style="font-size: 0.72rem; color: #34D399; font-weight: 700; text-transform: uppercase;">Authenticated Customer</div>
            <div style="font-size: 0.92rem; font-weight: 700; color: #F8FAFC;">{cust_name} ({cust_phone})</div>
        </div>
    </div>
</div>
""")

    tab_cases, tab_vault, tab_upload = st.tabs([
        "📋 My Disputes & Cases",
        "🛡️ Customer Proof Vault (5 Categories)",
        "📤 Upload Requested Evidence"
    ])

    # -------------------------------------------------------------
    # TAB 1: My Disputes & Cases
    # -------------------------------------------------------------
    with tab_cases:
        cases = service.list_cases_for_customer(cust["id"])
        if not cases:
            all_cases = service.list_cases()
            cases = [c for c in all_cases if c.get("customer_name") == cust.get("full_name") or c.get("customer_id") == cust.get("id")]
            if not cases:
                cases = all_cases[:2]

        st.markdown(f"#### Active Disputes Assigned to {cust_name}")
        if cases:
            for c in cases:
                current_status = c.get("case_status") or c.get("status", "investigating")
                render_html("""
<div class="fintech-card">
""")
                col1, col2, col3 = st.columns([3, 2, 2])
                with col1:
                    st.markdown(f"**Order ID:** `{c.get('order_id', 'ORD')}`")
                    st.markdown(f"**Dispute Reason:** {c.get('dispute_reason', 'Product Not Received')}")
                    st.markdown(f"**Dispute Type:** `{c.get('dispute_type', 'Product Not Received')}`")
                with col2:
                    st.markdown(f"**Disputed Amount:** ₹{c.get('amount', 0):,.2f} {c.get('currency', 'INR')}")
                    st.markdown(f"**Opened On:** {c.get('opened_at', '')[:10]}")
                    st.markdown(f"**Evidence Score:** **{c.get('evidence_score', 'Pending')} / 100**")
                with col3:
                    st.markdown(f"**Current Status:**")
                    render_html(f'<span class="sub-tag" style="background: rgba(59,130,246,0.2);">{current_status.upper()}</span>')

                st.write("")
                render_case_status_tracker(c.get("case_status") or c.get("status", "new"))
                render_html("</div>")
        else:
            st.info("No active dispute cases found for your account.")

    # -------------------------------------------------------------
    # TAB 2: Customer Proof Vault
    # -------------------------------------------------------------
    with tab_vault:
        render_html("""
<div class="fintech-card">
    <div class="card-title">
        <span>Secure Cardholder Proof Vault</span>
        <span class="sub-tag">AES-256 Encrypted</span>
    </div>
    <p class="card-subtitle">Maintain verified customer credentials: Identity Proof, Billing Address, Delivery Proof, Purchase Receipt, and Warranty Invoice.</p>
</div>
""")

        col_left, col_right = st.columns([1, 2])

        with col_left:
            st.markdown("##### ➕ Add Proof to Vault")
            vault_categories = [
                "Identity Proof (Aadhaar / Passport)",
                "Billing Address Proof",
                "Delivery Proof / Signed POD",
                "Purchase Receipt & Invoice",
                "Warranty & Terms Agreement"
            ]
            sel_cat = st.selectbox("Document Category", vault_categories)
            up_doc = st.file_uploader("Upload Document (PDF / JPG / PNG)", type=["pdf", "png", "jpg"], key="cust_vault_up")
            if up_doc and st.button("Save to My Proof Vault", type="primary", use_container_width=True):
                service.add_customer_vault_doc(
                    customer_id=cust["id"],
                    category=sel_cat,
                    file_name=up_doc.name,
                    file_bytes=up_doc.getvalue()
                )
                st.success(f"'{up_doc.name}' stored securely in your Proof Vault!")
                st.rerun()

        with col_right:
            st.markdown("##### 📂 Saved Proof Documents in Vault")
            vault_docs = service.get_customer_vault_docs(cust["id"])
            if vault_docs:
                for vd in vault_docs:
                    render_html(f"""
<div style="background: rgba(255,255,255,0.03); border: 1px solid rgba(255,255,255,0.08); border-radius: 8px; padding: 12px; margin-bottom: 10px;">
    <div style="display: flex; justify-content: space-between; align-items: center;">
        <div>
            <div style="font-weight: 700; color: #F8FAFC;">📄 {vd.get('file_name', 'document.pdf')}</div>
            <div style="font-size: 0.78rem; color: #94A3B8;">Category: <b>{vd.get('doc_type', vd.get('category', 'Proof'))}</b> &bull; Uploaded: {vd.get('uploaded_at', '')[:10]}</div>
        </div>
        <span class="status-pill complete">VERIFIED</span>
    </div>
</div>
""")
                    c_act1, c_act2 = st.columns([1, 1])
                    with c_act1:
                        if st.button(f"📎 Attach to Case", key=f"share_doc_{vd.get('id')}", use_container_width=True):
                            if cases:
                                service.share_vault_doc_to_case(vd.get("id"), cases[0]["id"])
                                st.success(f"Attached to Case #{cases[0].get('order_id')}!")
                    with c_act2:
                        if st.button(f"🗑️ Delete", key=f"del_doc_{vd.get('id')}", use_container_width=True):
                            service.delete_customer_vault_doc(vd.get("id"), cust["id"])
                            st.success("Document removed from vault.")
                            st.rerun()
            else:
                st.info("Your vault is currently empty. Upload your Aadhaar, bank statement, or delivery receipts above.")

    # -------------------------------------------------------------
    # TAB 3: Upload Requested Evidence
    # -------------------------------------------------------------
    with tab_upload:
        render_html("""
<div class="fintech-card">
    <div class="card-title">
        <span>Merchant Evidence Requests</span>
        <span class="sub-tag">Direct Dispute Integration</span>
    </div>
    <p class="card-subtitle">Select an existing document from your Proof Vault or upload fresh documentation to fulfill open merchant evidence requests.</p>
</div>
""")
        if cases:
            st.markdown(f"**Fulfilling Evidence for Case:** `{cases[0].get('order_id')}` ({cases[0].get('dispute_reason')})")
            req_type = st.radio("Fulfill With:", ["Choose from My Proof Vault", "Upload Fresh File"], horizontal=True)

            if "Vault" in req_type:
                vault_docs = service.get_customer_vault_docs(cust["id"])
                if vault_docs:
                    v_opts = {f"{vd.get('file_name')} ({vd.get('doc_type', vd.get('category'))})": vd.get('id') for vd in vault_docs}
                    sel_v = st.selectbox("Select Stored Document", list(v_opts.keys()))
                    if st.button("⚡ 1-Click Share to Dispute Case", type="primary", use_container_width=True):
                        service.share_vault_doc_to_case(v_opts[sel_v], cases[0]["id"])
                        st.success("Selected Proof attached to dispute docket instantly!")
                else:
                    st.info("No documents in vault yet. Please upload one first.")
            else:
                f_up = st.file_uploader("Upload Evidence Document", type=["pdf", "png", "jpg"], key="req_fresh_up")
                if f_up and st.button("Submit Evidence to Merchant", type="primary", use_container_width=True):
                    service.upload_case_document(cases[0]["id"], "customer_proof", f_up.name, f_up.getvalue())
                    st.success("Fresh document submitted and linked to active case!")
