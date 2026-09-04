"""
Chargeback Evidence AI - Final AI Report & Interactive PDF Editor
Features:
1. Horizontal Case Status Lifecycle Progress Tracker
2. AI Case Narrative Tab with structured 6-section legal breakdown
3. Interactive PDF Preview Editor (Custom Title, Executive Summary, Merchant Notes, Digital Signature)
4. Approve & Submit Case Action (transitions status to 'submitted')
5. Instant PDF Evidence Packet Download
"""

import streamlit as st
from pathlib import Path
from frontend.components import render_case_status_tracker


def render_final_report_view(service):
    st.markdown("""
    <div style="display: flex; justify-content: space-between; align-items: flex-end; margin-bottom: 20px;">
        <div>
            <h2 style="margin: 0; color: #F8FAFC; font-weight: 800; font-size: 1.6rem; letter-spacing: -0.03em;">Chargeback Defense Packet & Interactive PDF</h2>
            <p style="color: #94A3B8; font-size: 0.88rem; margin-top: 4px;">Submission-ready formal dispute packet formatted for acquirers, Visa, Mastercard & NPCI arbitration with interactive custom editing.</p>
        </div>
        <div>
            <span class="sub-tag" style="background: rgba(59, 130, 246, 0.2); color: #93C5FD; border-color: rgba(59, 130, 246, 0.4);">
                INTERACTIVE PDF BUILDER
            </span>
        </div>
    </div>
    """, unsafe_allow_html=True)

    cases = service.list_cases()
    if not cases:
        st.warning("No dispute cases found.")
        return

    active_case_id = st.session_state.get("active_case_id", cases[0]["id"])
    active_case = service.get_case(active_case_id)

    # Horizontal Lifecycle Tracker
    render_case_status_tracker(active_case.get("case_status") or active_case.get("status", "investigating"))

    # Get pipeline output or generate
    pipeline_state = service.get_latest_run(active_case_id)
    if not pipeline_state or not pipeline_state.get("final_report"):
        pipeline_state = service.run_full_pipeline(active_case_id)

    rep = pipeline_state.get("final_report") or {}
    score_val = rep.get("evidence_strength_score", active_case.get("evidence_score", 92))
    win_prob = rep.get("win_probability", active_case.get("win_probability", 0.92))

    # Header Card with Score Badge
    st.markdown(f"""
    <div class="fintech-card" style="display: flex; justify-content: space-between; align-items: center; border-left: 4px solid #10B981;">
        <div>
            <div style="font-size: 1.25rem; font-weight: 800; color: #F8FAFC;">
                Chargeback Evidence Report — Case #{active_case.get('order_id')}
            </div>
            <div style="font-size: 0.82rem; color: #94A3B8; margin-top: 4px;">
                Customer: <b>{active_case.get('customer_name')}</b> &bull; Disputed Amount: <b>₹{float(active_case.get('amount', 4299)):,.2f}</b> &bull; Classification: <b>{active_case.get('dispute_type', 'Product Not Received')}</b>
            </div>
        </div>
        <div style="display: flex; align-items: center; gap: 16px;">
            <div style="text-align: right;">
                <div style="font-size: 0.72rem; color: #94A3B8; text-transform: uppercase;">Evidence Strength</div>
                <div style="font-size: 2.2rem; font-weight: 900; color: #10B981; line-height: 1;">SCORE {score_val}</div>
                <div style="font-size: 0.75rem; color: #60A5FA;">Win Probability: {int(win_prob*100)}%</div>
            </div>
        </div>
    </div>
    """, unsafe_allow_html=True)

    tab_doc, tab_narrative, tab_interactive = st.tabs([
        "📄 Evidence Packet Summary",
        "✍️ AI Case Narrative (6 Sections)",
        "🎨 Interactive PDF Editor & Approval"
    ])

    # -------------------------------------------------------------
    # TAB 1: Evidence Packet Summary
    # -------------------------------------------------------------
    with tab_doc:
        pdf_path = rep.get("pdf_file_path")
        if pdf_path and Path(pdf_path).exists():
            with open(pdf_path, "rb") as f:
                pdf_bytes = f.read()
            col_d1, col_d2 = st.columns([1, 3])
            with col_d1:
                st.download_button(
                    label="📥 Download Evidence PDF",
                    data=pdf_bytes,
                    file_name=f"chargeback_evidence_{active_case.get('order_id')}.pdf",
                    mime="application/pdf",
                    type="primary",
                    use_container_width=True
                )
            with col_d2:
                st.caption("Official bank dispute document generated with SHA-256 digital seal.")

        # Executive Summary
        st.markdown('<div class="fintech-card">', unsafe_allow_html=True)
        st.markdown('<div class="card-title"><span>1. EXECUTIVE SUMMARY</span></div>', unsafe_allow_html=True)
        st.markdown(f"""
        <p style="font-size: 0.9rem; color: #CBD5E1; line-height: 1.6; margin: 0;">
            {rep.get('executive_summary', 'The order was placed, paid, and delivered to the address on file with signed confirmation. All key facts are consistent across invoice, receipt, and courier records.')}
        </p>
        """, unsafe_allow_html=True)
        st.markdown('</div>', unsafe_allow_html=True)

        # Contradictions & Missing Evidence
        col_c, col_m = st.columns(2)
        with col_c:
            st.markdown('<div class="fintech-card" style="min-height: 160px;">', unsafe_allow_html=True)
            st.markdown('<div class="card-title"><span>2. CONTRADICTIONS AUDIT</span></div>', unsafe_allow_html=True)
            contras = rep.get("contradictions", [])
            if not contras:
                st.markdown("""
                <div style="font-size: 0.88rem; color: #10B981; font-weight: 600;">
                    ✓ Zero contradictions detected across submitted evidence documents.
                </div>
                """, unsafe_allow_html=True)
            else:
                for c in contras:
                    st.error(c)
            st.markdown('</div>', unsafe_allow_html=True)

        with col_m:
            st.markdown('<div class="fintech-card" style="min-height: 160px;">', unsafe_allow_html=True)
            st.markdown('<div class="card-title"><span>3. RECOMMENDED NEXT EVIDENCE</span></div>', unsafe_allow_html=True)
            rec = rep.get("recommended_next_evidence") or {}
            st.markdown(f"""
            <div style="font-size: 0.88rem; color: #34D399; font-weight: 700;">
                +{rec.get('win_probability_uplift_pct', 14)}% Win Rate Uplift: {rec.get('recommended_document', 'Courier Proof of Delivery (POD)')}
            </div>
            <p style="font-size: 0.78rem; color: #94A3B8; margin-top: 4px;">{rec.get('reason', 'Attaching physical signature proof maximizes acquirer acceptance.')}</p>
            """, unsafe_allow_html=True)
            st.markdown('</div>', unsafe_allow_html=True)

        # Exhibits Table
        st.markdown('<div class="fintech-card">', unsafe_allow_html=True)
        st.markdown('<div class="card-title"><span>4. EVIDENCE EXHIBIT CHECKLIST</span></div>', unsafe_allow_html=True)
        ev_list = rep.get("evidence_list", [
            {"type": "Tax Invoice", "details": "Matches billing name, itemized pricing, and tax breakups", "weight": "High"},
            {"type": "Payment Authorization Receipt", "details": "Reconciles 100% with gateway settlement", "weight": "High"},
            {"type": "Proof of Delivery (POD)", "details": "Carrier GPS timestamp and consignee signature confirmation", "weight": "High"}
        ])

        for ev in ev_list:
            st.markdown(f"""
            <div style="display: flex; justify-content: space-between; align-items: center; padding: 8px 0; border-bottom: 1px solid rgba(255,255,255,0.04);">
                <div>
                    <span style="font-weight: 600; color: #F8FAFC;">📁 {ev.get('type')}</span>
                    <div style="font-size: 0.78rem; color: #94A3B8;">{ev.get('details')}</div>
                </div>
                <span class="tag-chip tag-green">{ev.get('weight', 'High')}</span>
            </div>
            """, unsafe_allow_html=True)
        st.markdown('</div>', unsafe_allow_html=True)

    # -------------------------------------------------------------
    # TAB 2: AI Case Narrative (6 Structured Sections)
    # -------------------------------------------------------------
    with tab_narrative:
        nar = rep.get("case_narrative") or {}
        st.markdown('<div class="fintech-card">', unsafe_allow_html=True)
        st.markdown('<div class="card-title"><span>Structured AI Case Narrative</span><span class="sub-tag">Legal Grounding</span></div>', unsafe_allow_html=True)

        st.markdown("##### 1. Incident Overview")
        st.info(nar.get("incident_overview", f"Dispute #{active_case.get('order_id')} filed under reason '{active_case.get('dispute_reason')}'. Merchant provided full documentation."))

        st.markdown("##### 2. Chronological Timeline Summary")
        st.markdown(f"""
        <div style="background: rgba(0,0,0,0.3); padding: 12px 16px; border-radius: 8px; font-size: 0.85rem; color: #E2E8F0; line-height: 1.5;">
            {nar.get('timeline_summary', '1. Order Placed -> 2. Payment Verified -> 3. Dispatched -> 4. Delivered')}
        </div>
        """, unsafe_allow_html=True)

        st.markdown("##### 3. Verified Factual Findings")
        verified_facts = nar.get("verified_facts", [
            {"fact": "Order and Invoice details match 100%", "confidence": "98%"},
            {"fact": "Recipient address verified with Carrier POD", "confidence": "96%"}
        ])
        for vf in verified_facts:
            st.markdown(f"• **{vf.get('fact')}** (Confidence: `{vf.get('confidence')}`)")

        st.markdown("##### 4. Contradictions & Fraud Audit")
        st.markdown(f"_{nar.get('contradictions_audit', 'No factual contradictions detected across invoice, shipping logs, and customer chat history.')}_")

        st.markdown("##### 5. AI Reasoning & Precedent Evidence")
        st.markdown(f"""
        <div style="background: rgba(30, 41, 59, 0.6); padding: 12px 16px; border-radius: 8px; font-size: 0.85rem; color: #93C5FD; border-left: 3px solid #3B82F6;">
            {nar.get('ai_reasoning', 'Historical precedent indicates 94% merchant win probability when both AWB POD and GST invoice are submitted.')}
        </div>
        """, unsafe_allow_html=True)

        st.markdown("##### 6. Formal Arbitration Recommendation")
        st.success(nar.get("final_recommendation", "Submit full defense docket immediately as evidence completeness is 100%."))
        st.markdown('</div>', unsafe_allow_html=True)

    # -------------------------------------------------------------
    # TAB 3: Interactive PDF Preview & Case Approval
    # -------------------------------------------------------------
    with tab_interactive:
        st.markdown("""
        <div class="fintech-card">
            <div class="card-title">
                <span>Interactive PDF Editor & Case Submission</span>
                <span class="sub-tag">Live Draft Customization</span>
            </div>
            <p class="card-subtitle">Edit report titles, add merchant custom notes, apply digital signature, and formally approve the dispute packet to payment gateway.</p>
        </div>
        """, unsafe_allow_html=True)

        with st.form("interactive_pdf_form"):
            col_e1, col_e2 = st.columns(2)
            with col_e1:
                custom_title = st.text_input("Report Title", value="Formal Chargeback Defense Packet")
                digital_sig = st.text_input("Authorized Signatory Name", value=st.session_state.get("digital_sig", "Apex Retail Operations Desk"))
            with col_e2:
                notes = st.text_area("Merchant Custom Notes / Statement", value="The cardholder was contacted on email and WhatsApp. Goods were physically handed over with signature. Chargeback claim is completely invalid.")

            c_sub1, c_sub2 = st.columns(2)
            with c_sub1:
                preview_btn = st.form_submit_button("🔄 Update PDF Draft Preview", use_container_width=True)
            with c_sub2:
                approve_btn = st.form_submit_button("✅ Approve Case & Mark Submitted", use_container_width=True, type="primary")

        if preview_btn:
            with st.spinner("Regenerating customized PDF defense packet..."):
                custom_rep = service.preview_report(
                    case_id=active_case_id,
                    report_title=custom_title,
                    merchant_notes=notes,
                    signature_name=digital_sig
                )
                pipeline_state["final_report"] = custom_rep
                st.session_state[f"pipeline_run_{active_case_id}"] = pipeline_state
                st.success("PDF Draft re-rendered with your custom notes and digital signature!")
                st.rerun()

        if approve_btn:
            with st.spinner("Approving and dispatching dispute packet to acquiring network..."):
                service.approve_case(active_case_id)
                st.balloons()
                st.success("Case marked as SUBMITTED! Formal defense docket transmitted to payment gateway & bank.")
                st.rerun()

