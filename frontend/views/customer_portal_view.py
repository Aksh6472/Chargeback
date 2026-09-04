"""
Chargeback Evidence AI - Dedicated Customer Workspace & Proof Vault
Enables customers to view active chargeback disputes, manage encrypted proof vault,
and directly attach / share verified documents to bank defense dockets.
"""

import streamlit as st
from frontend.components import render_case_status_tracker

def render_customer_portal_view(service):
    cust = st.session_state.get("current_customer")
    if not cust:
        # Fallback to demo customer
        customers = service.list_all_customers()
        cust = customers[0] if customers else {
            "id": "cust_demo_01",
            "full_name": "Aarav Sharma",
            "phone_number": "+91 9811223344",
            "email": "aarav.sharma@example.com"
        }
        st.session_state["current_customer"] = cust

    st.markdown(f"""
    <div style="margin-bottom: 20px;">
        <div style="display: flex; justify-content: space-between; align-items: center;">
            <div>
                <h2 style="margin: 0; color: #F8FAFC; font-weight: 700; letter-spacing: -0.02em;">👤 Customer Dispute & Proof Workspace</h2>
                <p style="color: #94A3B8; font-size: 0.88rem; margin-top: 4px;">Manage identity proofs, view active dispute resolutions, and share evidence with banks.</p>
            </div>
            <div style="text-align: right; background: rgba(16, 185, 129, 0.1); border: 1px solid rgba(16, 185, 129, 0.3); padding: 6px 14px; border-radius: 8px;">
                <div style="font-size: 0.72rem; color: #34D399; font-weight: 700; text-transform: uppercase;">Authenticated Customer</div>
                <div style="font-size: 0.92rem; font-weight: 700; color: #F8FAFC;">{cust.get('full_name', 'Aarav Sharma')} ({cust.get('phone_number', '+91 9811223344')})</div>
            </div>
        </div>
    </div>
    """, unsafe_allow_html=True)

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
            # Also fetch cases matching customer's phone or name
            all_cases = service.list_cases()
            cases = [c for c in all_cases if c.get("customer_name") == cust.get("full_name") or c.get("customer_id") == cust.get("id")]
            if not cases:
                cases = all_cases[:2]  # Show current active cases

        st.markdown(f"#### Active Disputes Assigned to {cust.get('full_name', 'Customer')}")
        if cases:
            for c in cases:
                st.markdown('<div class="fintech-card">', unsafe_allow_html=True)
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
                    current_status = c.get("case_status") or c.get("status", "investigating")
                    st.markdown(f"**Current Status:**")
                    st.markdown(f'<span class="sub-tag" style="background: rgba(59,130,246,0.2);">{current_status.upper()}</span>', unsafe_allow_html=True)

                st.write("")
                render_case_status_tracker(c.get("case_status") or c.get("status", "new"))
                st.markdown('</div>', unsafe_allow_html=True)
        else:
            st.info("No active dispute cases found for your account.")

    # -------------------------------------------------------------
    # TAB 2: Customer Proof Vault
    # -------------------------------------------------------------
    with tab_vault:
        st.markdown("""
        <div class="fintech-card">
            <div class="card-title">
                <span>Secure Cardholder Proof Vault</span>
                <span class="sub-tag">AES-256 Encrypted</span>
            </div>
            <p class="card-subtitle">Maintain verified customer credentials: Identity Proof, Billing Address, Delivery Proof, Purchase Receipt, and Warranty Invoice.</p>
        </div>
        """, unsafe_allow_html=True)

        col_left, col_right = st.columns([1, 2])

        with col_left:
            st.markdown("##### ➕ Add Proof to Vault")
            vault_categories = [
                "Identity Proof (Aadhaar / Passport)",
                "Billing Address Proof",
                "Delivery Proof / Signature",
                "Purchase Receipt",
                "Warranty Invoice"
            ]
            selected_cat = st.selectbox("Document Category", vault_categories)
            up_file = st.file_uploader("Upload Document (PDF / Image)", type=["pdf", "png", "jpg", "jpeg"], key="cust_vault_up")
            if up_file and st.button("Save to My Vault", type="primary", use_container_width=True):
                service.upload_customer_vault_doc(cust["id"], selected_cat, up_file.name, up_file.getvalue())
                st.success(f"Added '{up_file.name}' to your encrypted Proof Vault!")
                st.rerun()

        with col_right:
            st.markdown("##### 📁 Stored Vault Documents")
            vault_docs = service.get_customer_vault_docs(cust["id"])
            if vault_docs:
                for doc in vault_docs:
                    st.markdown(f"""
                    <div style="background: rgba(15, 23, 42, 0.8); border: 1px solid rgba(255,255,255,0.08); border-radius: 8px; padding: 12px 16px; margin-bottom: 10px;">
                        <div style="display: flex; justify-content: space-between; align-items: center;">
                            <div>
                                <div style="font-weight: 700; color: #F8FAFC; font-size: 0.92rem;">📄 {doc['file_name']}</div>
                                <div style="font-size: 0.78rem; color: #94A3B8; margin-top: 2px;">Category: <b>{doc['doc_type']}</b> &bull; Added: {doc.get('uploaded_at', '')[:10]}</div>
                            </div>
                            <span class="status-pill complete">✓ {doc.get('verification_status', 'VERIFIED')}</span>
                        </div>
                    </div>
                    """, unsafe_allow_html=True)

                    c_act1, c_act2, c_act3 = st.columns([2, 1, 1])
                    with c_act1:
                        # Share to case selector
                        all_c = service.list_cases()
                        case_options = {f"{c['order_id']} (₹{c['amount']})": c['id'] for c in all_c}
                        if case_options:
                            target_c = st.selectbox("Share to Case", list(case_options.keys()), key=f"share_sel_{doc['id']}")
                            if st.button("🔗 Share to Case", key=f"btn_share_{doc['id']}"):
                                target_id = case_options[target_c]
                                service.share_vault_doc_to_case(doc["id"], target_id)
                                st.success(f"Shared '{doc['file_name']}' with dispute docket {target_c}!")
                    with c_act2:
                        replace_file = st.file_uploader("Replace", key=f"rep_{doc['id']}", type=["pdf", "png", "jpg"], label_visibility="collapsed")
                        if replace_file and st.button("🔄 Replace", key=f"btn_rep_{doc['id']}"):
                            service.replace_customer_vault_doc(doc["id"], replace_file.name, replace_file.getvalue())
                            st.success("Document replaced!")
                            st.rerun()
                    with c_act3:
                        if st.button("🗑️ Delete", key=f"del_cust_vault_{doc['id']}"):
                            service.delete_customer_vault_doc(doc["id"])
                            st.rerun()
                    st.write("---")
            else:
                st.info("Your Proof Vault is currently empty. Upload your identity or delivery documents above.")

    # -------------------------------------------------------------
    # TAB 3: Upload Requested Evidence
    # -------------------------------------------------------------
    with tab_upload:
        st.markdown('<div class="fintech-card">', unsafe_allow_html=True)
        st.markdown('<div class="card-title"><span>Upload Requested Evidence for Dispute</span></div>', unsafe_allow_html=True)
        st.markdown('<p class="card-subtitle">Submit dispute-specific counter-evidence requested by the acquiring bank or merchant.</p>', unsafe_allow_html=True)

        all_c = service.list_cases()
        if all_c:
            selected_case = st.selectbox(
                "Select Target Dispute Case",
                [f"{c['order_id']} &bull; {c['dispute_reason']} (₹{c['amount']})" for c in all_c],
                key="cust_target_case_sel"
            )
            case_idx = [f"{c['order_id']} &bull; {c['dispute_reason']} (₹{c['amount']})" for c in all_c].index(selected_case)
            target_case_id = all_c[case_idx]["id"]

            doc_type_choice = st.selectbox("Evidence Type", [
                "customer_delivery_receipt",
                "customer_damage_photo",
                "customer_chat_transcript",
                "customer_affidavit",
                "bank_statement_snippet"
            ])

            cust_file = st.file_uploader("Choose Evidence File", type=["pdf", "png", "jpg", "jpeg"], key="cust_direct_evidence_up")
            if cust_file and st.button("Submit Evidence to Dispute Docket", type="primary", use_container_width=True):
                service.upload_case_document(
                    case_id=target_case_id,
                    doc_type=doc_type_choice,
                    file_name=cust_file.name,
                    file_bytes=cust_file.getvalue(),
                    owner_type="customer",
                    document_category="customer_evidence"
                )
                st.balloons()
                st.success(f"Evidence '{cust_file.name}' attached to Case {all_c[case_idx]['order_id']}. AI Multi-Agent re-analysis ready.")
        else:
            st.info("No active cases available to attach documents to.")

        st.markdown('</div>', unsafe_allow_html=True)
