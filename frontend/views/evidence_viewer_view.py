"""
Chargeback Evidence AI - Page 4: Evidence Viewer
Split layout showing:
- Original document viewer / simulated document docket
- OCR machine-extracted text
- Extracted entities chips & table with confidence scores
- Visual highlighting of detected entities (Customer, Order ID, Date, Amount, AWB)
"""

import streamlit as st
import pandas as pd


def render_evidence_viewer_view(service):
    st.markdown("""
    <div style="margin-bottom: 20px;">
        <h2 style="margin: 0; color: #F8FAFC; font-weight: 800; font-size: 1.6rem; letter-spacing: -0.03em;">Evidence Document & Entity Viewer</h2>
        <p style="color: #94A3B8; font-size: 0.88rem; margin-top: 4px;">Split layout inspection of original artifacts, PyMuPDF OCR layers, and normalized NER extractions.</p>
    </div>
    """, unsafe_allow_html=True)

    cases = service.list_cases()
    if not cases:
        st.warning("No dispute cases found.")
        return

    active_case_id = st.session_state.get("active_case_id", cases[0]["id"])
    active_case = service.get_case(active_case_id)
    documents = active_case.get("documents", [])

    if not documents:
        st.info("No documents attached to this case.")
        return

    # Document Selector tabs/dropdown
    doc_map = {f"{d['doc_type'].upper()} - {d['file_name']}": d for d in documents}
    selected_doc_label = st.selectbox("Select Evidence Artifact to Inspect", list(doc_map.keys()))
    current_doc = doc_map[selected_doc_label]

    # Split Layout
    col_left, col_right = st.columns([1, 1])

    with col_left:
        st.markdown('<div class="fintech-card">', unsafe_allow_html=True)
        st.markdown(f'<div class="card-title"><span>Original Document Exhibit</span><span class="sub-tag">{current_doc["doc_type"].upper()}</span></div>', unsafe_allow_html=True)

        # Render document preview box
        st.markdown(f"""
        <div style="background: #FFFFFF; color: #0F172A; border-radius: 8px; padding: 24px; font-family: 'Inter', sans-serif; box-shadow: 0 4px 15px rgba(0,0,0,0.2); min-height: 420px;">
            <div style="border-bottom: 2px solid #E2E8F0; padding-bottom: 12px; margin-bottom: 16px; display: flex; justify-content: space-between;">
                <div>
                    <h3 style="margin: 0; color: #1E293B; font-size: 1.2rem;">TAX INVOICE & DISPATCH MEMO</h3>
                    <div style="font-size: 0.75rem; color: #64748B;">Apex Retailers Private Limited &bull; GSTIN: 29AAAAA0000A1Z5</div>
                </div>
                <div style="text-align: right;">
                    <div style="font-weight: 700; color: #2563EB;">{active_case['order_id']}</div>
                    <div style="font-size: 0.75rem; color: #64748B;">Date: 2024-08-02</div>
                </div>
            </div>
            <div style="display: flex; justify-content: space-between; font-size: 0.8rem; margin-bottom: 16px; line-height: 1.5;">
                <div>
                    <b>Billed & Shipped To:</b><br/>
                    <mark style="background: #FEF08A; padding: 2px 4px; border-radius: 3px;">{active_case.get('customer_name', 'Aarav Sharma')}</mark><br/>
                    <mark style="background: #BBF7D0; padding: 2px 4px; border-radius: 3px;">{active_case.get('shipping_address', 'Bellandur, Bengaluru')}</mark>
                </div>
                <div style="text-align: right;">
                    <b>Logistics Dispatch:</b><br/>
                    Carrier: BlueDart Express<br/>
                    AWB: <mark style="background: #BFDBFE; padding: 2px 4px; border-radius: 3px;">{active_case.get('tracking_id', 'BLUEDART-88392104')}</mark><br/>
                    Status: <span style="color: #059669; font-weight: 600;">Delivered with Signature</span>
                </div>
            </div>
            <div style="border-top: 1px solid #E2E8F0; padding-top: 12px; margin-top: 18px;">
                <table style="width: 100%; font-size: 0.78rem; text-align: left; border-collapse: collapse;">
                    <tr style="border-bottom: 1px solid #CBD5E1;">
                        <th style="padding: 6px 0;">Item Description</th>
                        <th style="text-align: right; padding: 6px 0;">Qty</th>
                        <th style="text-align: right; padding: 6px 0;">Amount</th>
                    </tr>
                    <tr>
                        <td style="padding: 8px 0;">Premium Wireless Headphones & Audio Kit</td>
                        <td style="text-align: right; padding: 8px 0;">1</td>
                        <td style="text-align: right; padding: 8px 0;">₹3,643.22</td>
                    </tr>
                    <tr>
                        <td style="padding: 8px 0;">GST (18% Integrated Goods Tax)</td>
                        <td style="text-align: right; padding: 8px 0;">-</td>
                        <td style="text-align: right; padding: 8px 0;">₹655.78</td>
                    </tr>
                    <tr style="border-top: 2px solid #0F172A; font-weight: 700; font-size: 0.88rem;">
                        <td style="padding: 10px 0;">Total Payable</td>
                        <td style="text-align: right; padding: 10px 0;">-</td>
                        <td style="text-align: right; padding: 10px 0;"><mark style="background: #FECDD3; padding: 2px 6px; border-radius: 3px;">₹{float(active_case.get('amount', 4299)):,.2f}</mark></td>
                    </tr>
                </table>
            </div>
            <div style="margin-top: 30px; font-size: 0.7rem; color: #64748B; border-top: 1px dashed #CBD5E1; padding-top: 8px; display: flex; justify-content: space-between;">
                <span>Authorized Signatory: Apex Retail Operations</span>
                <span>SHA-256 Digest: e89a20...verified</span>
            </div>
        </div>
        """, unsafe_allow_html=True)
        st.markdown('</div>', unsafe_allow_html=True)

    with col_right:
        st.markdown('<div class="fintech-card">', unsafe_allow_html=True)
        st.markdown('<div class="card-title"><span>Extracted Entities & OCR Stream</span><span class="sub-tag">97% OCR Confidence</span></div>', unsafe_allow_html=True)

        # Color-coded entity chips legend
        st.markdown("""
        <div style="margin-bottom: 14px;">
            <span class="tag-chip tag-amber">👤 Customer Name</span>
            <span class="tag-chip tag-green">📍 Delivery Address</span>
            <span class="tag-chip tag-blue">📦 Tracking AWB</span>
            <span class="tag-chip tag-rose">💵 Reconciled Amount</span>
            <span class="tag-chip tag-purple">📅 ISO Timestamp</span>
        </div>
        """, unsafe_allow_html=True)

        # Tabbed View: Entities Table vs Raw OCR text
        view_tab1, view_tab2 = st.tabs(["Structured NER Entities", "Cleaned OCR Text Layer"])

        with view_tab1:
            entities_data = [
                {"Entity": "Customer Name", "Extracted Value": active_case.get("customer_name", "Aarav Sharma"), "Normalized": active_case.get("customer_name", "Aarav Sharma"), "Confidence": "99.2%", "Status": "VERIFIED"},
                {"Entity": "Order Reference", "Extracted Value": active_case.get("order_id", "ORD-2024-9842"), "Normalized": active_case.get("order_id", "ORD-2024-9842"), "Confidence": "98.5%", "Status": "VERIFIED"},
                {"Entity": "Transaction Amount", "Extracted Value": f"INR {active_case.get('amount', 4299):,.2f}", "Normalized": f"{active_case.get('amount', 4299):.2f}", "Confidence": "99.8%", "Status": "VERIFIED"},
                {"Entity": "Delivery Address", "Extracted Value": active_case.get("shipping_address", "Bellandur, Bengaluru"), "Normalized": "IND, KA, BLR 560103", "Confidence": "96.4%", "Status": "VERIFIED"},
                {"Entity": "Carrier Tracking", "Extracted Value": active_case.get("tracking_id", "BLUEDART-88392104"), "Normalized": "AWB-88392104", "Confidence": "97.1%", "Status": "VERIFIED"},
                {"Entity": "Fulfillment Date", "Extracted Value": "06 Aug 2024", "Normalized": "2024-08-06", "Confidence": "98.0%", "Status": "VERIFIED"}
            ]
            df_ent = pd.DataFrame(entities_data)
            st.dataframe(df_ent, use_container_width=True, hide_index=True)

        with view_tab2:
            st.markdown(f"""
            <div class="agent-output-box" style="height: 320px; overflow-y: auto;">
TAX INVOICE & DISPATCH MEMO
Apex Retailers Private Limited | Indiranagar, Bengaluru
GSTIN: 29AAAAA0000A1Z5 | CIN: U52100KA2021PTC148810

Invoice Number: INV-2024-9842
Order Reference: {active_case.get('order_id')}
Payment Capture ID: pay_RZP8829104
Date of Invoice: 2024-08-02T14:15:00+05:30

Bill To / Ship To:
Consignee: {active_case.get('customer_name')}
Address: {active_case.get('shipping_address')}
Contact: {active_case.get('customer_phone', '+91 9811223344')}

Logistics Details:
Carrier: BlueDart Express Surface & Air
AWB Tracking No: {active_case.get('tracking_id')}
Dispatch Hub: Bangalore Sort Facility (BLR-NORTH)
Delivery Status: DELIVERED (Signee: {active_case.get('customer_name')})
Delivery Timestamp: 2024-08-06T15:40:00+05:30

Items:
1. Premium Wireless Noise-Cancelling Headphones x 1 | ₹3,643.22
CGST 9%: ₹327.89
SGST 9%: ₹327.89
Total Gross Amount Reconciled: INR {float(active_case.get('amount', 4299)):,.2f}
Payment Status: CAPTURED & SETTLED (Razorpay)
            </div>
            """, unsafe_allow_html=True)

        st.markdown('</div>', unsafe_allow_html=True)
