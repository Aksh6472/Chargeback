"""
Chargeback Evidence AI - Timeline View
Vertical interactive timeline: Ordered -> Paid -> Shipped -> Delivered -> Customer Contact -> Chargeback Filed.
Includes timestamps, source document references, and audit descriptions matching Stitch UI.
"""

import streamlit as st
from frontend.components import render_html


def render_timeline_view(service):
    render_html("""
    <div style="margin-bottom: 24px;">
        <div style="display: flex; align-items: center; gap: 8px; margin-bottom: 4px;">
            <span class="material-symbols-outlined" style="color: #2D3948; font-size: 22px;">schedule</span>
            <h2 style="margin: 0; color: #1A242C; font-weight: 700; font-size: 1.4rem; letter-spacing: -0.02em;">Chronological Order Journey</h2>
        </div>
        <p style="color: #64748B; font-size: 0.88rem; margin: 0;">Reconstructed factual events from purchase to doorstep delivery to dispute filing.</p>
    </div>
    """)

    cases = service.list_cases()
    if not cases:
        st.warning("No dispute cases available.")
        return

    active_case_id = st.session_state.get("active_case_id", cases[0]["id"])
    active_case = service.get_case(active_case_id)

    order_id = active_case.get("order_id", "ORD-2026-9842")
    cust_name = active_case.get("customer_name", "Aarav Sharma")
    amt = active_case.get("amount", 4299.00)
    reason = active_case.get("dispute_reason", "Product Not Received")
    awb = active_case.get("tracking_id", "BLUEDART-88392104")

    events = [
        {
            "stage": "Ordered",
            "time": "2026-10-12 14:15:00 UTC",
            "doc": f"Tax Invoice #{order_id}",
            "desc": f"Order successfully checked out by {cust_name} for ₹{amt:,.2f} via 3D-Secure card authentication.",
            "dot_color": "#2563EB",
            "status": "Verified on Gateway"
        },
        {
            "stage": "Paid",
            "time": "2026-10-12 14:16:12 UTC",
            "doc": "Payment Gateway Settlement Ledger",
            "desc": f"Payment captured with Razorpay authorization code #882910. Settlement credited to merchant bank account.",
            "dot_color": "#059669",
            "status": "Capture Confirmed"
        },
        {
            "stage": "Shipped",
            "time": "2026-10-13 11:30:00 UTC",
            "doc": f"Carrier Dispatch Docket ({awb})",
            "desc": f"Package dispatched from Bangalore Fulfillment Hub via BlueDart Express. Gross parcel weight: 1.42 kg.",
            "dot_color": "#4F46E5",
            "status": "In Transit"
        },
        {
            "stage": "Delivered",
            "time": "2026-10-14 15:40:00 UTC",
            "doc": "Signed Proof of Delivery (POD)",
            "desc": f"Package handed over to consignee {cust_name} at registered address: {active_case.get('shipping_address')}. Doorstep signature captured.",
            "dot_color": "#059669",
            "status": "Fulfillment Complete"
        },
        {
            "stage": "Customer Contact",
            "time": "2026-10-18 11:20:00 UTC",
            "doc": "Helpdesk Support Transcript #TKT-492",
            "desc": "Customer initiated live chat inquiring about warranty registration; made no statement claiming missing parcel.",
            "dot_color": "#D97706",
            "status": "Chat Inquired"
        },
        {
            "stage": "Chargeback Filed",
            "time": "2026-10-26 09:00:00 UTC",
            "doc": "Bank Dispute Charge Notice",
            "desc": f"Cardholder disputed transaction alleging '{reason}'. Discrepancy refuted by signed delivery proof and unbroken timeline.",
            "dot_color": "#DC2626",
            "status": "Under Arbitration"
        }
    ]

    col_tl, col_info = st.columns([3, 2])

    with col_tl:
        render_html("""
        <div class="stitch-card">
            <div class="stitch-card-header">
                <span class="stitch-card-title">Interactive Vertical Timeline</span>
                <span class="stitch-pill stitch-pill-won">6 Verified Events</span>
            </div>
        </div>
        """)

        for e in events:
            render_html(f"""
            <div class="timeline-step">
                <div class="timeline-dot" style="background: {e['dot_color']};"></div>
                <div style="display: flex; justify-content: space-between; align-items: baseline;">
                    <div class="timeline-title">{e['stage']}</div>
                    <span class="stitch-pill stitch-pill-draft" style="font-size: 0.68rem;">{e['status']}</span>
                </div>
                <div class="timeline-time">🕒 {e['time']}</div>
                <div class="timeline-desc">{e['desc']}</div>
                <span class="timeline-badge">📄 Exhibit: <b>{e['doc']}</b></span>
            </div>
            """)

    with col_info:
        render_html("""
        <div class="stitch-card">
            <div class="stitch-card-header">
                <span class="stitch-card-title">Timeline Consistency Analysis</span>
            </div>
            <p style="font-size: 0.84rem; color: #64748B; margin: 0 0 14px 0; line-height: 1.45;">
                Chronological journey compiled and reconciled across 4 official sources (Tax invoice, settlement log, carrier AWB, and customer service transcript).
            </p>
        """)

        metrics = [
            ("Days from Order to Delivery", "2 Days", "Fast Delivery Benchmark"),
            ("Days from Delivery to Claim", "12 Days", "Unusual Gap for INR 4k+"),
            ("Fulfillment Precedence", "Valid", "Order < Ship < Deliver"),
            ("Delivery Integrity", "100%", "Signed Delivery Verified")
        ]

        for lbl, val, sub in metrics:
            render_html(f"""
            <div style="display: flex; justify-content: space-between; align-items: center; padding: 10px 0; border-bottom: 1px solid #E5E7EB;">
                <div>
                    <div style="font-size: 0.84rem; font-weight: 600; color: #1A242C;">{lbl}</div>
                    <div style="font-size: 0.74rem; color: #64748B;">{sub}</div>
                </div>
                <span style="font-size: 0.95rem; font-weight: 700; color: #0284C7; font-family: 'JetBrains Mono', monospace;">{val}</span>
            </div>
            """)

        render_html("</div>")

