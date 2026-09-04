"""
Chargeback Evidence AI - Create Chargeback Case
Dispute metadata, ML dispute classification, customer linking, and automated navigation to Live Investigation.
"""

import streamlit as st

def render_create_case_view(service):
    st.markdown("""
    <div style="margin-bottom: 20px;">
        <h2 style="margin: 0; color: #F8FAFC; font-weight: 800; font-size: 1.6rem; letter-spacing: -0.03em;">Create Chargeback Case</h2>
        <p style="color: #94A3B8; font-size: 0.88rem; margin-top: 4px;">Upload disputed transaction dockets, invoice records, delivery receipts, and customer proof vault links.</p>
    </div>
    """, unsafe_allow_html=True)

    customers = service.list_all_customers()
    cust_options = {f"{c['full_name']} ({c['phone_number']})": c['id'] for c in customers}

    with st.form("create_case_form"):
        st.markdown('<div class="fintech-card">', unsafe_allow_html=True)
        st.markdown('<div class="card-title"><span>1. Disputed Transaction Details</span><span class="sub-tag">Required Metadata</span></div>', unsafe_allow_html=True)

        c1, c2, c3 = st.columns(3)
        with c1:
            order_id = st.text_input("Order ID / Transaction Ref", value="ORD-2024-9842")
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
            customer_name = st.text_input("Customer Full Name", value="Aarav Sharma")
            customer_phone = st.text_input("Customer Phone", value="+91 9811223344")
        with c3:
            customer_email = st.text_input("Customer Email", value="aarav.sharma@example.com")
            tracking_id = st.text_input("Carrier Tracking AWB", value="BLUEDART-88392104")
            selected_cust_link = st.selectbox("Link to Customer Profile", list(cust_options.keys()) if cust_options else ["Aarav Sharma (+91 9811223344)"])

        shipping_address = st.text_area("Customer Shipping Address", value="Flat 402, Green Glen Layout, Bellandur, Bengaluru, Karnataka 560103")

        st.markdown('</div>', unsafe_allow_html=True)

        st.markdown('<div class="fintech-card">', unsafe_allow_html=True)
        st.markdown('<div class="card-title"><span>2. Supporting Evidence Documents (Drag & Drop)</span><span class="sub-tag">PDFs & Scans</span></div>', unsafe_allow_html=True)
        st.markdown('<p class="card-subtitle">Upload multiple files: Tax invoices, signed PODs, courier logs, customer support chats, or gateway receipts.</p>', unsafe_allow_html=True)

        uploaded_files = st.file_uploader(
            "Drop documents here or browse files",
            type=["pdf", "png", "jpg", "jpeg"],
            accept_multiple_files=True
        )

        st.markdown('</div>', unsafe_allow_html=True)

        submit_btn = st.form_submit_button("⚡ Create Case & Auto-Launch AI Investigation", use_container_width=True, type="primary")

    if submit_btn:
        with st.spinner("Registering dispute case and initializing AI agent cluster..."):
            linked_cust_id = cust_options.get(selected_cust_link) if cust_options else None
            case_data = {
                "order_id": order_id,
                "amount": float(amount),
                "currency": "INR",
                "dispute_reason": dispute_reason,
                "dispute_type": dispute_type,
                "customer_name": customer_name,
                "customer_email": customer_email,
                "customer_phone": customer_phone,
                "customer_id": linked_cust_id,
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

            st.success(f"Dispute Case #{order_id} created! Auto-navigating to 10-Step AI Investigation...")
            st.session_state["current_page"] = "AI Investigation"
            st.rerun()
