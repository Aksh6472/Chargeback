"""
Chargeback Evidence AI - Dedicated Customer Workspace & Proof Vault
Matches Stitch UI: Clean cards, status pills, proof vault manager, and 1-click document attachment.
"""

from typing import Optional, Any
import streamlit as st
from frontend.components import render_case_status_tracker, render_html


NAV_PAGES = [
    "My Cases",
    "Proof Vault",
    "Requested Documents",
    "Upload Evidence",
    "Case Status"
]


def render_customer_portal_view(service, active_page: Optional[str] = None):
    # Customer Authentication & Profile Resolution
    all_customers = service.list_all_customers()
    cust = st.session_state.get("current_customer")
    if not cust or not any(c.get("id") == cust.get("id") for c in all_customers):
        cust = all_customers[0] if all_customers else {
            "id": "cust_aarav_01",
            "full_name": "Aarav Sharma",
            "phone_number": "+91 9811223344",
            "email": "aarav.sharma@example.com"
        }
        st.session_state["current_customer"] = cust

    cust_id = cust.get("id", "")
    cust_name = cust.get("full_name", "Cardholder")
    cust_phone = cust.get("phone_number", "+91 9811223344")
    cust_email = cust.get("email", f"{cust_name.split()[0].lower()}@example.com")

    # Fetch this customer's disputes and vault items
    customer_cases = service.list_cases_for_customer(cust_id)
    vault_docs = service.get_customer_vault_docs(cust_id)

    # Resolve active selected case
    if customer_cases:
        selected_case_id = st.session_state.get("customer_active_case_id")
        active_case = next((c for c in customer_cases if c.get("id") == selected_case_id), customer_cases[0])
        st.session_state["customer_active_case_id"] = active_case.get("id")
    else:
        active_case = None
        st.session_state["customer_active_case_id"] = None

    # Synchronize Navigation
    curr_nav = active_page or st.session_state.get("current_page", "My Cases")
    if curr_nav not in NAV_PAGES:
        curr_nav = "My Cases"
    st.session_state["current_page"] = curr_nav

    # Header & Quick Stat Banner
    render_html(f"""
    <div class="stitch-card" style="margin-bottom: 20px;">
        <div style="display: flex; justify-content: space-between; align-items: center; flex-wrap: wrap; gap: 16px;">
            <div>
                <div style="display: flex; align-items: center; gap: 8px; margin-bottom: 4px;">
                    <span class="material-symbols-outlined" style="color: #2D3948; font-size: 24px;">shield</span>
                    <h2 style="margin: 0; color: #1A242C; font-weight: 700; font-size: 1.35rem; letter-spacing: -0.02em;">
                        Cardholder Proof &amp; Dispute Workspace
                    </h2>
                </div>
                <p style="color: #64748B; font-size: 0.86rem; margin: 0;">
                    Manage verified credentials, respond to merchant requests, and monitor dispute resolutions.
                </p>
            </div>
            <div style="display: flex; align-items: center; gap: 10px;">
                <div style="background: #ECFDF5; border: 1px solid #A7F3D0; padding: 8px 14px; border-radius: 8px; text-align: right;">
                    <div style="font-size: 0.70rem; color: #059669; font-weight: 700; text-transform: uppercase; letter-spacing: 0.05em; display: flex; align-items: center; justify-content: flex-end; gap: 4px;">
                        <span class="material-symbols-outlined" style="font-size: 14px;">verified</span>
                        <span>VERIFIED CARDHOLDER</span>
                    </div>
                    <div style="font-size: 0.92rem; font-weight: 700; color: #1A242C;">
                        {cust_name}
                    </div>
                    <div style="font-size: 0.74rem; color: #64748B;">
                        {cust_phone} &bull; {cust_email}
                    </div>
                </div>
            </div>
        </div>
    </div>
    """)

    # Action-Oriented Guide Banner
    if active_case:
        status_raw = active_case.get("case_status") or active_case.get("status", "investigating")
        order_num = active_case.get("order_id", "ORD")
        amount_fmt = f"₹{float(active_case.get('amount', 0)):,.2f}"

        if status_raw in ["new", "investigating"]:
            render_html(f"""
            <div style="background: #FFFBEB; border: 1px solid #FDE68A; border-radius: 8px; padding: 14px 18px; margin-bottom: 20px;">
                <div style="display: flex; align-items: center; gap: 8px; margin-bottom: 4px;">
                    <span class="material-symbols-outlined" style="color: #D97706; font-size: 20px;">bolt</span>
                    <span style="font-weight: 700; color: #92400E; font-size: 0.88rem; text-transform: uppercase;">Action Required</span>
                </div>
                <div style="font-size: 0.88rem; color: #1A242C; font-weight: 600;">
                    Upload supporting evidence for Order #{order_num} ({amount_fmt})
                </div>
                <div style="font-size: 0.80rem; color: #78350F; margin-top: 2px;">
                    The acquiring bank requires signed Proof of Delivery or billing confirmation to validate your claim.
                </div>
            </div>
            """)
        elif status_raw in ["evidence_ready", "rebuttal_drafted"]:
            render_html(f"""
            <div style="background: #EFF6FF; border: 1px solid #BFDBFE; border-radius: 8px; padding: 14px 18px; margin-bottom: 20px;">
                <div style="display: flex; align-items: center; gap: 8px; margin-bottom: 4px;">
                    <span class="material-symbols-outlined" style="color: #2563EB; font-size: 20px;">hourglass_top</span>
                    <span style="font-weight: 700; color: #1E40AF; font-size: 0.88rem; text-transform: uppercase;">Under Final Review</span>
                </div>
                <div style="font-size: 0.88rem; color: #1A242C; font-weight: 600;">
                    Rebuttal packet compiled for Order #{order_num}
                </div>
                <div style="font-size: 0.80rem; color: #1E3A8A; margin-top: 2px;">
                    All required documents have been cross-verified with 100% data consistency. Awaiting final submission.
                </div>
            </div>
            """)
        elif status_raw == "submitted":
            render_html(f"""
            <div style="background: #ECFDF5; border: 1px solid #A7F3D0; border-radius: 8px; padding: 14px 18px; margin-bottom: 20px;">
                <div style="display: flex; align-items: center; gap: 8px; margin-bottom: 4px;">
                    <span class="material-symbols-outlined" style="color: #059669; font-size: 20px;">check_circle</span>
                    <span style="font-weight: 700; color: #065F46; font-size: 0.88rem; text-transform: uppercase;">Docket Formally Submitted</span>
                </div>
                <div style="font-size: 0.88rem; color: #1A242C; font-weight: 600;">
                    Order #{order_num} is under bank arbitration
                </div>
                <div style="font-size: 0.80rem; color: #047857; margin-top: 2px;">
                    No further action is required. The dispute packet has been dispatched to payment network arbitration.
                </div>
            </div>
            """)

    # -------------------------------------------------------------
    # SECTION 1: 📋 My Cases
    # -------------------------------------------------------------
    if curr_nav == "My Cases":
        render_html("""
        <div class="stitch-card-header" style="margin-bottom: 8px;">
            <div style="display: flex; align-items: center; gap: 8px;">
                <span class="material-symbols-outlined" style="color: #2D3948; font-size: 20px;">folder_open</span>
                <span class="stitch-card-title">Active Chargeback Disputes</span>
            </div>
        </div>
        """)

        if customer_cases:
            for idx, c in enumerate(customer_cases):
                status_key = c.get("case_status") or c.get("status", "investigating")
                current_status = status_key.upper().replace("_", " ")
                amount_val = float(c.get("amount", 0))
                opened_date = str(c.get("opened_at", ""))[:10]
                ev_score = c.get("evidence_score", 85)
                is_won_status = status_key in ["submitted", "won"]

                render_html(f"""
                <div class="stitch-card" style="margin-bottom: 14px;">
                    <div class="stitch-card-header">
                        <div style="display: flex; align-items: center; gap: 10px;">
                            <span style="font-size: 1.05rem; font-weight: 700; color: #1A242C;">Order Reference: <code>{c.get('order_id', 'ORD')}</code></span>
                        </div>
                        <span class="stitch-pill {'stitch-pill-won' if is_won_status else 'stitch-pill-review'}">
                            {current_status}
                        </span>
                    </div>
                """)

                c1, c2, c3 = st.columns(3)
                with c1:
                    st.markdown(f"**Disputed Amount:** ₹{amount_val:,.2f} {c.get('currency', 'INR')}")
                    st.markdown(f"**Dispute Reason:** `{c.get('dispute_reason', 'Product Not Received')}`")
                with c2:
                    st.markdown(f"**Filing Date:** {opened_date or 'Recent'}")
                    st.markdown(f"**Carrier Tracking:** `{c.get('tracking_id', 'N/A')}`")
                with c3:
                    st.markdown(f"**Evidence Integrity:** `{ev_score}/100`")
                    docs_count = c.get("document_count", 0)
                    st.markdown(f"**Attached Docs:** `{docs_count} files`")

                st.write("")
                render_case_status_tracker(c.get("case_status") or c.get("status", "new"))

                btn_col1, btn_col2, btn_col3 = st.columns(3)
                with btn_col1:
                    if st.button("Upload Evidence for Case", key=f"case_up_btn_{c.get('id')}", use_container_width=True):
                        st.session_state["customer_active_case_id"] = c.get("id")
                        st.session_state["current_page"] = "Upload Evidence"
                        st.rerun()
                with btn_col2:
                    if st.button("Attach Proof from Vault", key=f"case_vault_btn_{c.get('id')}", use_container_width=True):
                        st.session_state["customer_active_case_id"] = c.get("id")
                        st.session_state["current_page"] = "Proof Vault"
                        st.rerun()
                with btn_col3:
                    if st.button("View Full Timeline", key=f"case_status_btn_{c.get('id')}", use_container_width=True):
                        st.session_state["customer_active_case_id"] = c.get("id")
                        st.session_state["current_page"] = "Case Status"
                        st.rerun()

                render_html("</div>")
        else:
            render_html("""
            <div class="stitch-card">
                <p style="color: #64748B; margin: 0;">No active dispute cases are currently recorded for this customer account.</p>
            </div>
            """)

    # -------------------------------------------------------------
    # SECTION 2: 🛡️ Proof Vault
    # -------------------------------------------------------------
    elif curr_nav == "Proof Vault":
        render_html("""
        <div class="stitch-card-header" style="margin-bottom: 8px;">
            <div style="display: flex; align-items: center; gap: 8px;">
                <span class="material-symbols-outlined" style="color: #2D3948; font-size: 20px;">inventory_2</span>
                <span class="stitch-card-title">Secure Cardholder Proof Vault</span>
            </div>
        </div>
        <p style="color: #64748B; font-size: 0.84rem; margin: 0 0 16px 0;">Store once, reuse across disputes. All credentials are encrypted with AES-256 and pre-verified for bank submission.</p>
        """)

        col_left, col_right = st.columns([1, 2])

        with col_left:
            render_html("""
            <div class="stitch-card">
                <div class="stitch-card-header" style="margin-bottom: 8px;">
                    <span class="stitch-card-title">+ Add Document to Vault</span>
                </div>
            """)
            vault_categories = [
                "Identity Proof (Aadhaar / Passport / DL)",
                "Billing Address Proof (Utility / Bank)",
                "Delivery Proof / Signed POD",
                "Purchase Receipt & Invoice",
                "Warranty & Terms Agreement"
            ]
            sel_cat = st.selectbox("Document Category", vault_categories, key="cust_vault_category_sel")
            up_doc = st.file_uploader(
                "Select PDF or Image",
                type=["pdf", "png", "jpg", "jpeg"],
                key="cust_vault_file_uploader"
            )

            if up_doc:
                st.caption(f"📁 **{up_doc.name}** ({len(up_doc.getvalue()) / 1024:.1f} KB)")
                if st.button("Save to Proof Vault", type="primary", use_container_width=True, key="save_to_vault_action_btn"):
                    service.add_customer_vault_doc(
                        customer_id=cust_id,
                        category=sel_cat,
                        file_name=up_doc.name,
                        file_bytes=up_doc.getvalue()
                    )
                    st.success(f"✓ '{up_doc.name}' stored in Proof Vault!")
                    st.rerun()

            render_html("</div>")

        with col_right:
            render_html("""
            <div class="stitch-card">
                <div class="stitch-card-header">
                    <span class="stitch-card-title">Stored Credentials &amp; Evidence</span>
                </div>
            """)
            if vault_docs:
                target_case_id = None
                if customer_cases:
                    case_choices = {f"Order #{c.get('order_id')} (₹{float(c.get('amount', 0)):,.2f})": c.get("id") for c in customer_cases}
                    default_label = next((k for k, v in case_choices.items() if v == (active_case.get("id") if active_case else None)), list(case_choices.keys())[0])
                    sel_target_label = st.selectbox("Target Case for Attachments:", list(case_choices.keys()), index=list(case_choices.keys()).index(default_label), key="vault_target_case_sel")
                    target_case_id = case_choices[sel_target_label]

                st.divider()

                for vd in vault_docs:
                    vd_id = vd.get("id")
                    v_name = vd.get("file_name", "document.pdf")
                    v_type = vd.get("doc_type", vd.get("category", "General Proof"))
                    v_date = str(vd.get("uploaded_at", ""))[:10] or "Active"
                    v_status = vd.get("verification_status", "VERIFIED")

                    render_html(f"""
                    <div style="background: #F8F9FB; border: 1px solid #E5E7EB; border-radius: 8px; padding: 10px 14px; margin-bottom: 8px; display: flex; justify-content: space-between; align-items: center; flex-wrap: wrap; gap: 8px;">
                        <div>
                            <div style="font-weight: 600; color: #1A242C; font-size: 0.88rem;">
                                📄 {v_name}
                            </div>
                            <div style="font-size: 0.74rem; color: #64748B; margin-top: 2px;">
                                Category: <b>{v_type}</b> &bull; Added: {v_date}
                            </div>
                        </div>
                        <div>
                            <span class="stitch-pill stitch-pill-won">
                                ✓ {v_status}
                            </span>
                        </div>
                    </div>
                    """)
                    act_col1, act_col2 = st.columns([2, 1])
                    with act_col1:
                        if target_case_id:
                            if st.button(f"Attach to Selected Case", key=f"v_attach_{vd_id}", use_container_width=True):
                                res = service.share_vault_doc_to_case(vault_doc_id=vd_id, case_id=target_case_id)
                                if res:
                                    st.success(f"Attached '{v_name}' to dispute docket!")
                                else:
                                    st.warning("Document is already linked or verified.")
                    with act_col2:
                        if st.button(f"Delete", key=f"v_del_{vd_id}", use_container_width=True):
                            service.delete_customer_vault_doc(doc_id=vd_id, customer_id=cust_id)
                            st.success("Document removed from vault.")
                            st.rerun()

                    st.write("")
            else:
                st.info("Your Proof Vault is currently empty. Upload your documents using the form on the left.")

            render_html("</div>")

    # -------------------------------------------------------------
    # SECTION 3: 📥 Requested Documents
    # -------------------------------------------------------------
    elif curr_nav == "Requested Documents":
        render_html("""
        <div class="stitch-card-header" style="margin-bottom: 8px;">
            <div style="display: flex; align-items: center; gap: 8px;">
                <span class="material-symbols-outlined" style="color: #2D3948; font-size: 20px;">mark_email_unread</span>
                <span class="stitch-card-title">Bank &amp; Merchant Evidence Requests</span>
            </div>
        </div>
        <p style="color: #64748B; font-size: 0.84rem; margin: 0 0 16px 0;">Respond to open evidence requests required by acquiring banks to resolve dispute claims.</p>
        """)

        if not active_case:
            render_html("""
            <div class="stitch-card">
                <p style="color: #64748B; margin: 0;">No active dispute case selected. You do not have any pending evidence requests at this time.</p>
            </div>
            """)
        else:
            render_html(f"""
            <div class="stitch-card" style="margin-bottom: 14px;">
                <div class="stitch-card-header">
                    <span class="stitch-card-title">Active Case: {active_case.get('order_id')}</span>
                    <span class="stitch-pill stitch-pill-pending">Due in 5 Days</span>
                </div>
                <div style="font-size: 0.84rem; color: #64748B;">
                    Dispute: <b>{active_case.get('dispute_reason')}</b> &bull; Value: <b>₹{float(active_case.get('amount', 0)):,.2f}</b>
                </div>
            </div>
            """)

            d_reason = active_case.get("dispute_reason", "Product Not Received").lower()
            if "not received" in d_reason:
                required_items = [
                    ("Delivery Proof / Signed POD", "Proof that shipment was not received or courier note", "Delivery Proof"),
                    ("Written Statement / Explanation", "Clarify circumstances around delivery or carrier attempt", "Statement"),
                    ("Customer Identity Verification", "Government-issued ID to verify cardholder identity", "Identity Proof")
                ]
            else:
                required_items = [
                    ("Cardholder Identity Verification", "Aadhaar / Passport confirming rightful cardholder", "Identity Proof"),
                    ("Bank Statement Snippet", "Statement snippet showing duplicate or unauthorized debit", "Bank Statement"),
                    ("Customer Explanation Statement", "Written statement explaining the disputed charge", "Statement")
                ]

            for req_title, req_desc, req_type in required_items:
                render_html(f"""
                <div class="stitch-card" style="margin-bottom: 10px;">
                    <div style="font-weight: 600; color: #1A242C; font-size: 0.9rem; margin-bottom: 2px;">📄 {req_title}</div>
                    <div style="font-size: 0.78rem; color: #64748B; margin-bottom: 8px;">{req_desc}</div>
                """)
                matching_vault_docs = [
                    vd for vd in vault_docs
                    if req_type.lower() in vd.get("doc_type", "").lower() or req_type.lower() in vd.get("file_name", "").lower()
                ]
                if matching_vault_docs:
                    m_doc = matching_vault_docs[0]
                    st.caption(f"✓ Found in Vault: `{m_doc.get('file_name')}`")
                    if st.button("1-Click Attach from Vault", key=f"fulfill_req_{m_doc.get('id')}_{req_type}", use_container_width=True, type="primary"):
                        service.share_vault_doc_to_case(vault_doc_id=m_doc.get("id"), case_id=active_case.get("id"))
                        st.success(f"Attached '{m_doc.get('file_name')}' to Case {active_case.get('order_id')}!")
                else:
                    f_up = st.file_uploader(f"Upload {req_type}", type=["pdf", "png", "jpg"], key=f"up_req_{req_type}")
                    if f_up and st.button(f"Upload & Link to Case", key=f"btn_up_req_{req_type}", use_container_width=True):
                        service.upload_case_document(
                            case_id=active_case.get("id"),
                            doc_type=req_type.lower().replace(" ", "_"),
                            file_name=f_up.name,
                            file_bytes=f_up.getvalue(),
                            owner_type="customer",
                            document_category="customer_proof"
                        )
                        st.success(f"Uploaded and linked '{f_up.name}'!")
                        st.rerun()

                render_html("</div>")

    # -------------------------------------------------------------
    # SECTION 4: 📤 Upload Evidence
    # -------------------------------------------------------------
    elif curr_nav == "Upload Evidence":
        render_html("""
        <div class="stitch-card-header" style="margin-bottom: 8px;">
            <div style="display: flex; align-items: center; gap: 8px;">
                <span class="material-symbols-outlined" style="color: #2D3948; font-size: 20px;">cloud_upload</span>
                <span class="stitch-card-title">Upload Dispute Evidence</span>
            </div>
        </div>
        <p style="color: #64748B; font-size: 0.84rem; margin: 0 0 16px 0;">Submit supporting documents directly to the active dispute packet or attach from your saved vault.</p>
        """)

        if not active_case:
            render_html("""
            <div class="stitch-card">
                <p style="color: #64748B; margin: 0;">No active dispute case found to attach evidence.</p>
            </div>
            """)
        else:
            render_html(f"""
            <div class="stitch-card" style="margin-bottom: 14px;">
                <div class="stitch-card-header">
                    <span class="stitch-card-title">Fulfilling Evidence for Order: #{active_case.get('order_id')}</span>
                </div>
                <div style="font-size: 0.84rem; color: #64748B;">
                    Reason: <b>{active_case.get('dispute_reason')}</b> &bull; Value: <b>₹{float(active_case.get('amount', 0)):,.2f} INR</b>
                </div>
            </div>
            """)

            upload_mode = st.radio(
                "Evidence Source:",
                ["Choose from My Proof Vault", "Upload Fresh Document"],
                horizontal=True,
                key="cust_evidence_source_mode"
            )

            if "Vault" in upload_mode:
                if vault_docs:
                    v_choices = {f"{vd.get('file_name')} ({vd.get('doc_type', vd.get('category'))})": vd.get("id") for vd in vault_docs}
                    sel_vault_doc_label = st.selectbox("Select Document from Vault", list(v_choices.keys()), key="cust_sel_vault_for_upload")
                    if st.button("1-Click Link to Dispute Docket", type="primary", use_container_width=True, key="btn_link_vault_to_case_direct"):
                        v_id = v_choices[sel_vault_doc_label]
                        service.share_vault_doc_to_case(vault_doc_id=v_id, case_id=active_case.get("id"))
                        st.success("Selected document from vault linked to case evidence docket!")
                        st.rerun()
                else:
                    st.info("No documents found in your Proof Vault.")
                    if st.button("Go to Proof Vault to Add Documents →"):
                        st.session_state["current_page"] = "Proof Vault"
                        st.rerun()
            else:
                up_c1, up_c2 = st.columns(2)
                with up_c1:
                    fresh_category = st.selectbox(
                        "Document Classification",
                        [
                            "Customer Explanation Statement",
                            "Delivery Slip / Courier POD",
                            "Bank / Card Debit Statement",
                            "Damage / Defect Photography",
                            "Communication & Chat Log",
                            "Other Supporting Document"
                        ],
                        key="fresh_evidence_doc_type"
                    )
                with up_c2:
                    fresh_file = st.file_uploader("Select Evidence File", type=["pdf", "png", "jpg", "jpeg"], key="fresh_evidence_file")

                if fresh_file:
                    st.caption(f"File selected: `{fresh_file.name}` ({len(fresh_file.getvalue()) / 1024:.1f} KB)")
                    if st.button("Submit Evidence to Dispute Docket", type="primary", use_container_width=True, key="btn_submit_fresh_evidence"):
                        service.upload_case_document(
                            case_id=active_case.get("id"),
                            doc_type=fresh_category.lower().replace(" ", "_"),
                            file_name=fresh_file.name,
                            file_bytes=fresh_file.getvalue(),
                            owner_type="customer",
                            document_category="customer_proof"
                        )
                        st.success(f"'{fresh_file.name}' submitted and attached to case!")
                        st.rerun()

            st.write("")
            render_html("""
            <div class="stitch-card-header" style="margin-bottom: 8px;">
                <span class="stitch-card-title">Documents Attached to this Dispute</span>
            </div>
            """)
            case_docs = service.get_case_documents(active_case.get("id"))
            if case_docs:
                for cd in case_docs:
                    owner_badge = "CUSTOMER SUBMISSION" if cd.get("owner_type") == "customer" else "MERCHANT SUBMISSION"
                    render_html(f"""
                    <div style="background: #F8F9FB; border: 1px solid #E5E7EB; border-radius: 8px; padding: 10px 14px; margin-bottom: 6px; display: flex; justify-content: space-between; align-items: center; flex-wrap: wrap; gap: 8px;">
                        <div>
                            <div style="font-weight: 600; color: #1A242C; font-size: 0.88rem;">📄 {cd.get('file_name')}</div>
                            <div style="font-size: 0.74rem; color: #64748B; margin-top: 2px;">
                                Type: <b>{cd.get('doc_type')}</b> &bull; Size: {int(cd.get('file_size_bytes', 0)) // 1024} KB &bull; Confidence: {int(float(cd.get('ocr_confidence', 0.95)) * 100)}%
                            </div>
                        </div>
                        <div style="display: flex; align-items: center; gap: 6px;">
                            <span class="stitch-pill stitch-pill-draft">
                                {owner_badge}
                            </span>
                            <span class="stitch-pill stitch-pill-won">
                                ✓ VERIFIED
                            </span>
                        </div>
                    </div>
                    """)
            else:
                st.info("No documents are currently linked to this dispute docket.")

    # -------------------------------------------------------------
    # SECTION 5: ⏱️ Case Status
    # -------------------------------------------------------------
    elif curr_nav == "Case Status":
        render_html("""
        <div class="stitch-card-header" style="margin-bottom: 8px;">
            <div style="display: flex; align-items: center; gap: 8px;">
                <span class="material-symbols-outlined" style="color: #2D3948; font-size: 20px;">timer</span>
                <span class="stitch-card-title">Dispute Milestone &amp; Status Tracker</span>
            </div>
        </div>
        <p style="color: #64748B; font-size: 0.84rem; margin: 0 0 16px 0;">Live timeline and resolution status for your active cardholder dispute claims.</p>
        """)

        if not active_case:
            render_html("""
            <div class="stitch-card">
                <p style="color: #64748B; margin: 0;">No active dispute case to track.</p>
            </div>
            """)
        else:
            render_html(f"""
            <div class="stitch-card" style="margin-bottom: 14px;">
                <div class="stitch-card-header">
                    <span class="stitch-card-title">Case #{active_case.get('order_id')}</span>
                    <span class="stitch-pill stitch-pill-won">₹{float(active_case.get('amount', 0)):,.2f}</span>
                </div>
                <div style="font-size: 0.84rem; color: #64748B; margin-bottom: 12px;">
                    Dispute Reason: <b>{active_case.get('dispute_reason')}</b> &bull; Filing Date: <b>{str(active_case.get('opened_at', ''))[:10]}</b>
                </div>
            """)

            render_case_status_tracker(active_case.get("case_status") or active_case.get("status", "new"))
            render_html("</div>")

            col_t1, col_t2 = st.columns([1, 1])

            with col_t1:
                carrier_name = "BlueDart Express" if "BLUE" in active_case.get("tracking_id", "") else "Delhivery Logistics"
                render_html(f"""
                <div class="stitch-card">
                    <div class="stitch-card-header">
                        <span class="stitch-card-title">Carrier Delivery &amp; Tracking</span>
                    </div>
                    <div style="font-size: 0.82rem; color: #334155; display: flex; flex-direction: column; gap: 4px;">
                        <div><b>Carrier:</b> {carrier_name}</div>
                        <div><b>Waybill / AWB:</b> <code style="font-family: 'JetBrains Mono', monospace;">{active_case.get('tracking_id', 'N/A')}</code></div>
                        <div><b>Delivery Address:</b> {active_case.get('shipping_address', 'Registered Address')}</div>
                        <div style="color: #059669; font-weight: 700; margin-top: 4px;">DELIVERED - SIGNED POD ON FILE</div>
                    </div>
                </div>
                """)

            with col_t2:
                render_html("""
                <div class="stitch-card">
                    <div class="stitch-card-header">
                        <span class="stitch-card-title">Resolution Milestones</span>
                    </div>
                    <div style="font-size: 0.82rem; color: #334155; display: flex; flex-direction: column; gap: 4px;">
                        <div>&bull; <b>Cardholder Filing:</b> Recorded</div>
                        <div>&bull; <b>Evidence Window:</b> Open (5 Days remaining)</div>
                        <div>&bull; <b>Bank Packet Generation:</b> Automated by AI</div>
                        <div>&bull; <b>Card Issuer Ruling:</b> Expected in 7-14 business days</div>
                    </div>
                </div>
                """)

