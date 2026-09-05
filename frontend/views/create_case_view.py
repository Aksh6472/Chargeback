"""
Chargeback Evidence AI - Create Chargeback Case
Dispute metadata, automated classification, customer linking, and direct launch into Investigation.
"""

import random
import streamlit as st
from frontend.components import render_html

def render_create_case_view(service):
    render_html("""
    <div style="margin-bottom: 24px;">
        <div style="display: flex; align-items: center; gap: 8px; margin-bottom: 6px;">
            <span class="material-symbols-outlined" style="color: #2D3948; font-size: 22px;">add_circle</span>
            <h2 style="margin: 0; color: #1A242C; font-weight: 700; font-size: 1.4rem; letter-spacing: -0.02em;">Create Chargeback Dispute</h2>
        </div>
        <p style="color: #64748B; font-size: 0.88rem; margin: 0;">Upload transaction dockets, invoice records, courier delivery receipts, and dynamically link customer proof vaults.</p>
    </div>
    """)

    customers = service.list_all_customers()

    # Dynamic Customer Profile Selector
    render_html("""
    <div class="stitch-card" style="margin-bottom: 18px;">
        <div class="stitch-card-header">
            <div style="display: flex; align-items: center; gap: 8px;">
                <span class="material-symbols-outlined" style="color: #2D3948; font-size: 20px;">account_circle</span>
                <span class="stitch-card-title">Customer Profile &amp; Proof Vault Link</span>
            </div>
            <span class="stitch-pill stitch-pill-draft">Dynamic Selection</span>
        </div>
        <p style="color: #64748B; font-size: 0.84rem; margin: 0 0 12px 0;">Select an existing customer to auto-fill their verified identity, contact details, and encrypted proof vault, or add a new customer.</p>
    </div>
    """)

    cust_labels = [f"👤 {c['full_name']} — {c['phone_number']} ({c.get('email', '')})" for c in customers]
    cust_labels.append("➕ Add New / Custom Customer")

    if "create_case_cust_choice" not in st.session_state or st.session_state["create_case_cust_choice"] not in cust_labels:
        st.session_state["create_case_cust_choice"] = cust_labels[0] if cust_labels else "➕ Add New / Custom Customer"

    selected_cust_choice = st.selectbox(
        "Select Customer Account",
        cust_labels,
        key="create_case_cust_choice",
        help="Switching customer dynamically populates their verified name, phone, email, and shipping address below."
    )

    is_new = selected_cust_choice.startswith("➕")
    if not is_new:
        idx = cust_labels.index(selected_cust_choice)
        sel_c = customers[idx]
        default_cust_id = sel_c.get("id")
        default_name = sel_c.get("full_name", "")
        default_phone = sel_c.get("phone_number", "")
        default_email = sel_c.get("email", "")
        default_addr = sel_c.get("address") or "Flat 402, Green Glen Layout, Bellandur, Bengaluru, Karnataka 560103"
        vault_docs = service.get_customer_vault_docs(default_cust_id)
        doc_count = len(vault_docs)
    else:
        default_cust_id = None
        default_name = ""
        default_phone = "+91 "
        default_email = ""
        default_addr = ""
        doc_count = 0

    if not is_new:
        render_html(f"""
        <div style="background: #EFF6FF; border: 1px solid #BFDBFE; border-radius: 8px; padding: 10px 14px; margin-bottom: 18px; display: flex; align-items: center; justify-content: space-between; font-size: 0.84rem;">
            <div style="color: #1E40AF; display: flex; align-items: center; gap: 6px;">
                <span class="material-symbols-outlined" style="font-size: 18px; color: #2563EB;">verified</span>
                <span><b>{default_name}</b> active &bull; Customer ID: <code style="color: #1E3A8A; background: #DBEAFE; padding: 2px 6px; border-radius: 4px; font-size: 0.78rem;">{default_cust_id}</code></span>
            </div>
            <div style="color: #065F46; font-weight: 600; display: flex; align-items: center; gap: 4px;">
                <span class="material-symbols-outlined" style="font-size: 18px; color: #059669;">inventory_2</span>
                <span>{doc_count} Vault Documents Available</span>
            </div>
        </div>
        """)
    else:
        render_html("""
        <div style="background: #FFFBEB; border: 1px solid #FDE68A; border-radius: 8px; padding: 10px 14px; margin-bottom: 18px; font-size: 0.84rem; color: #92400E; display: flex; align-items: center; gap: 6px;">
            <span class="material-symbols-outlined" style="font-size: 18px; color: #D97706;">person_add</span>
            <span><b>New Customer Mode</b>: Details entered below will be automatically saved to customer records upon case submission.</span>
        </div>
        """)

    # Transaction and Case Details Form
    with st.form("create_case_form"):
        render_html("""
        <div class="stitch-card-header" style="margin-bottom: 12px;">
            <div style="display: flex; align-items: center; gap: 8px;">
                <span class="material-symbols-outlined" style="color: #2D3948; font-size: 20px;">receipt_long</span>
                <span class="stitch-card-title">1. Disputed Transaction Details</span>
            </div>
            <span class="stitch-pill stitch-pill-review">Required Metadata</span>
        </div>
        """)

        rand_order = f"ORD-2026-{random.randint(1000, 9999)}"
        c1, c2, c3 = st.columns(3)
        with c1:
            order_id = st.text_input("Order ID / Transaction Ref", value=rand_order)
            dispute_type = st.selectbox("Dispute Classification", [
                "Product Not Received",
                "Fraudulent / Unauthorized Transaction",
                "Not as Described or Defective",
                "Duplicate Processing",
                "Subscription Canceled",
                "Credit Not Processed"
            ])
            dispute_reason = st.text_input("Reason Summary", value="Customer claims product was never delivered to their doorstep.")
        with c2:
            amount = st.number_input("Dispute Amount (INR)", min_value=1.0, value=14999.00, step=100.0)
            customer_name = st.text_input("Customer Full Name", value=default_name, placeholder="e.g. Aarav Sharma")
            customer_phone = st.text_input("Customer Phone", value=default_phone, placeholder="+91 9876543210")
        with c3:
            customer_email = st.text_input("Customer Email", value=default_email, placeholder="customer@example.com")
            tracking_id = st.text_input("Carrier Tracking AWB", value=f"BLUEDART-{random.randint(80000000, 89999999)}")
            st.caption(f"Linked Customer: **{default_name if default_name else 'New Customer'}**")

        shipping_address = st.text_area("Customer Shipping Address", value=default_addr, placeholder="Door No, Street, Landmark, City, State, Pincode")

        render_html("""
        <div style="margin-top: 18px; margin-bottom: 12px;" class="stitch-card-header">
            <div style="display: flex; align-items: center; gap: 8px;">
                <span class="material-symbols-outlined" style="color: #2D3948; font-size: 20px;">cloud_upload</span>
                <span class="stitch-card-title">2. Supporting Evidence Documents (Drag &amp; Drop)</span>
            </div>
            <span class="stitch-pill stitch-pill-draft">PDFs &amp; Images</span>
        </div>
        <p style="color: #64748B; font-size: 0.84rem; margin: 0 0 12px 0;">Upload multiple files: Tax invoices, signed PODs, courier logs, customer support chats, or gateway receipts.</p>
        """)

        uploaded_files = st.file_uploader(
            "Drop documents here or browse files",
            type=["pdf", "png", "jpg", "jpeg"],
            accept_multiple_files=True
        )

        submit_btn = st.form_submit_button("Create Case & Launch Investigation", use_container_width=True, type="primary")

    if submit_btn:
        with st.spinner("Registering dispute case and initializing investigation cluster..."):
            case_data = {
                "order_id": order_id,
                "amount": float(amount),
                "currency": "INR",
                "dispute_reason": dispute_reason,
                "dispute_type": dispute_type,
                "customer_name": customer_name,
                "customer_email": customer_email,
                "customer_phone": customer_phone,
                "customer_id": default_cust_id,
                "shipping_address": shipping_address,
                "tracking_id": tracking_id,
                "status": "new",
                "case_status": "new"
            }
            new_case = service.create_case(case_data)
            st.session_state["active_case_id"] = new_case["id"]

            # Save uploaded documents
            if uploaded_files:
                for uf in uploaded_files:
                    fname = uf.name.lower()
                    dtype = "invoice" if "inv" in fname else ("delivery_proof" if "pod" in fname or "deliver" in fname else ("receipt" if "rec" in fname else "chat_log"))
                    service.upload_case_document(new_case["id"], dtype, uf.name, uf.getvalue())
            else:
                demo_docs = [
                    ("invoice", f"tax_invoice_{order_id.lower()}.pdf"),
                    ("delivery_proof", "signed_pod_bluedart.pdf"),
                    ("receipt", "razorpay_payment_receipt.pdf")
                ]
                for dtype, fname in demo_docs:
                    service.upload_case_document(new_case["id"], dtype, fname, b"Demo Evidence Content for testing")

            st.success(f"Dispute Case #{order_id} created for {customer_name}! Auto-navigating to Investigation...")
            st.session_state["current_page"] = "Live Investigation"
            st.rerun()

