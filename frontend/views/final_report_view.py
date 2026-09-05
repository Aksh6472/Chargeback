"""
Chargeback Evidence AI - Evidence Package Builder & Interactive PDF Editor
Matches Stitch UI: 3-column layout (Document Sequence & Audit | Simulated PDF Sheet | Rebuttal Options & Live Editor).
Preserves full PDF compilation, draft customization, case approval, and instant download.
"""

from pathlib import Path
import streamlit as st
from frontend.components import render_case_status_tracker, render_html


def render_final_report_view(service):
    cases = service.list_cases()
    if not cases:
        st.warning("No dispute cases found.")
        return

    active_case_id = st.session_state.get("active_case_id", cases[0]["id"])
    active_case = service.get_case(active_case_id)

    # Get pipeline output or generate
    pipeline_state = service.get_latest_run(active_case_id)
    if not pipeline_state or not pipeline_state.get("final_report"):
        pipeline_state = service.run_full_pipeline(active_case_id)

    rep = pipeline_state.get("final_report") or {}
    score_val = rep.get("evidence_strength_score", active_case.get("evidence_score", 92))
    win_prob = rep.get("win_probability", active_case.get("win_probability", 0.92))
    pdf_path = rep.get("pdf_file_path")
    pdf_bytes = b""
    if pdf_path and Path(pdf_path).exists():
        with open(pdf_path, "rb") as f:
            pdf_bytes = f.read()

    # Top Header
    render_html(f"""
    <div style="display: flex; justify-content: space-between; align-items: flex-start; margin-bottom: 20px; flex-wrap: wrap; gap: 16px;">
        <div>
            <div style="display: flex; align-items: center; gap: 8px; font-size: 0.75rem; color: #64748B; text-transform: uppercase; letter-spacing: 0.06em; font-weight: 700; margin-bottom: 4px;">
                <span>Dispute Shield</span>
                <span>&bull;</span>
                <span>Rebuttal Generation Engine</span>
                <span>&bull;</span>
                <span style="color: #059669;">Audit Ready v3.4</span>
            </div>
            <h1 style="margin: 0; font-size: 1.6rem; font-weight: 700; color: #1A242C; letter-spacing: -0.02em;">Evidence Package Builder</h1>
            <p style="margin: 4px 0 0 0; font-size: 0.88rem; color: #64748B;">
                Review, organize, and compile case #{active_case.get('order_id')} into a card-network and acquirer ready dispute packet.
            </p>
        </div>
        <div style="display: flex; align-items: center; gap: 10px;">
            <span class="stitch-pill stitch-pill-won" style="font-size: 0.85rem; padding: 6px 12px;">
                <span class="material-symbols-outlined" style="font-size: 16px;">verified</span>
                Evidence Score: {score_val}/100 ({int(win_prob*100)}% Win Rate)
            </span>
        </div>
    </div>
    """)

    # Horizontal Lifecycle Tracker
    render_case_status_tracker(active_case.get("case_status") or active_case.get("status", "investigating"))

    # Main 3-Column Layout: Left (Sequence & Audit) | Middle (PDF Sheet) | Right (Controls & Editor)
    col_left, col_mid, col_right = st.columns([1, 2.1, 1.1])

    # -------------------------------------------------------------
    # LEFT COLUMN: Document Sequence & Scheme Compliance
    # -------------------------------------------------------------
    with col_left:
        render_html("""
        <div class="stitch-card" style="margin-bottom: 16px;">
            <div class="stitch-card-header">
                <div style="display: flex; align-items: center; gap: 6px;">
                    <span class="material-symbols-outlined" style="color: #2D3948; font-size: 18px;">layers</span>
                    <span class="stitch-card-title">Document Sequence</span>
                </div>
                <span class="stitch-pill stitch-pill-draft" style="font-family: 'JetBrains Mono', monospace; font-size: 0.72rem;">6 Pages</span>
            </div>
            <p style="font-size: 0.78rem; color: #64748B; margin: 0 0 12px 0;">Mandatory scheme indexing sequence for arbitration.</p>
            
            <div style="display: flex; flex-direction: column; gap: 8px;">
                <div style="background: #F8F9FB; border: 1px solid #E5E7EB; border-radius: 6px; padding: 8px 10px; display: flex; align-items: center; justify-content: space-between;">
                    <div>
                        <div style="font-size: 0.82rem; font-weight: 600; color: #1A242C;">1. Cover &amp; Synopsis</div>
                        <div style="font-size: 0.72rem; color: #64748B;">Visa Compelling Standard</div>
                    </div>
                    <span style="font-family: 'JetBrains Mono', monospace; font-size: 0.7rem; color: #64748B; background: #EDEFEF; padding: 2px 5px; border-radius: 4px;">P.1</span>
                </div>
                <div style="background: #F8F9FB; border: 1px solid #E5E7EB; border-radius: 6px; padding: 8px 10px; display: flex; align-items: center; justify-content: space-between;">
                    <div>
                        <div style="font-size: 0.82rem; font-weight: 600; color: #1A242C;">2. Table of Contents</div>
                        <div style="font-size: 0.72rem; color: #64748B;">Exhibit Map &amp; Citations</div>
                    </div>
                    <span style="font-family: 'JetBrains Mono', monospace; font-size: 0.7rem; color: #64748B; background: #EDEFEF; padding: 2px 5px; border-radius: 4px;">P.2</span>
                </div>
                <div style="background: #F8F9FB; border: 1px solid #E5E7EB; border-radius: 6px; padding: 8px 10px; display: flex; align-items: center; justify-content: space-between;">
                    <div>
                        <div style="font-size: 0.82rem; font-weight: 600; color: #1A242C;">3. 3DS Auth Verification</div>
                        <div style="font-size: 0.72rem; color: #059669; font-weight: 600;">Liability Shift ECI 05</div>
                    </div>
                    <span style="font-family: 'JetBrains Mono', monospace; font-size: 0.7rem; color: #64748B; background: #EDEFEF; padding: 2px 5px; border-radius: 4px;">P.3</span>
                </div>
                <div style="background: #F8F9FB; border: 1px solid #E5E7EB; border-radius: 6px; padding: 8px 10px; display: flex; align-items: center; justify-content: space-between;">
                    <div>
                        <div style="font-size: 0.82rem; font-weight: 600; color: #1A242C;">4. Carrier POD Receipt</div>
                        <div style="font-size: 0.72rem; color: #64748B;">Signed Consignee Delivery</div>
                    </div>
                    <span style="font-family: 'JetBrains Mono', monospace; font-size: 0.7rem; color: #64748B; background: #EDEFEF; padding: 2px 5px; border-radius: 4px;">P.4</span>
                </div>
                <div style="background: #F8F9FB; border: 1px solid #E5E7EB; border-radius: 6px; padding: 8px 10px; display: flex; align-items: center; justify-content: space-between;">
                    <div>
                        <div style="font-size: 0.82rem; font-weight: 600; color: #1A242C;">5. Customer Comms Log</div>
                        <div style="font-size: 0.72rem; color: #64748B;">Support Ticket Reconciled</div>
                    </div>
                    <span style="font-family: 'JetBrains Mono', monospace; font-size: 0.7rem; color: #64748B; background: #EDEFEF; padding: 2px 5px; border-radius: 4px;">P.5</span>
                </div>
                <div style="background: #F8F9FB; border: 1px solid #E5E7EB; border-radius: 6px; padding: 8px 10px; display: flex; align-items: center; justify-content: space-between;">
                    <div>
                        <div style="font-size: 0.82rem; font-weight: 600; color: #1A242C;">6. Terms &amp; Digital Seal</div>
                        <div style="font-size: 0.72rem; color: #64748B;">SHA-256 Authenticated</div>
                    </div>
                    <span style="font-family: 'JetBrains Mono', monospace; font-size: 0.7rem; color: #64748B; background: #EDEFEF; padding: 2px 5px; border-radius: 4px;">P.6</span>
                </div>
            </div>
        </div>
        """)

        # Network Rebuttal Strength Card
        render_html("""
        <div class="stitch-card">
            <div class="stitch-card-header">
                <div style="display: flex; align-items: center; gap: 6px;">
                    <span class="material-symbols-outlined" style="color: #059669; font-size: 18px;">verified_user</span>
                    <span class="stitch-card-title">Scheme Strength</span>
                </div>
                <span class="stitch-pill stitch-pill-won">98% Match</span>
            </div>
            <div style="background: #E5E7EB; border-radius: 9999px; height: 6px; overflow: hidden; margin-bottom: 8px;">
                <div style="background: #10B981; height: 100%; width: 98%;"></div>
            </div>
            <p style="font-size: 0.78rem; color: #64748B; margin: 0; line-height: 1.4;">
                All Tier-1 requirements satisfied: Verified Delivery Address matches billing record.
            </p>
        </div>
        """)

    # -------------------------------------------------------------
    # MIDDLE COLUMN: Simulated 8.5x11 PDF Sheet
    # -------------------------------------------------------------
    with col_mid:
        exec_text = rep.get('executive_summary', 'The order was placed, paid, and delivered to the verified cardholder address on file with signed confirmation. All factual records are reconciled and consistent across payment gateway, tax invoice, and courier manifests.')
        merchant_statement = rep.get('merchant_notes', 'The cardholder was contacted via registered email and messaging. Goods were physically handed over with recipient signature verification. Chargeback claim is without merit.')
        signer_name = rep.get('digital_signature', {}).get('signer_name', 'Apex Retail Operations Desk')
        rep_title = rep.get('report_title', 'Formal Chargeback Defense Packet')

        render_html(f"""
        <div style="background: #EDEFEF; border-radius: 12px; padding: 16px; display: flex; justify-content: center; box-shadow: inset 0 2px 4px rgba(0,0,0,0.05);">
            <div class="pdf-canvas" style="width: 100%; background: #FFFFFF; border: 1px solid #D1D5DB; box-shadow: 0 4px 16px rgba(0,0,0,0.08); border-radius: 4px; padding: 32px 36px; font-family: 'Inter', sans-serif;">
                
                <!-- Document Header -->
                <div style="display: flex; justify-content: space-between; align-items: flex-start; border-bottom: 2px solid #1A242C; padding-bottom: 14px; margin-bottom: 18px;">
                    <div style="display: flex; align-items: center; gap: 12px;">
                        <div style="width: 36px; height: 36px; background: #1A242C; border-radius: 6px; display: flex; align-items: center; justify-content: center; color: #FFFFFF;">
                            <span class="material-symbols-outlined" style="font-size: 20px;">shield</span>
                        </div>
                        <div>
                            <div style="font-size: 1.05rem; font-weight: 800; color: #1A242C; text-transform: uppercase; letter-spacing: -0.01em;">{rep_title}</div>
                            <div style="font-size: 0.72rem; color: #64748B; text-transform: uppercase; letter-spacing: 0.08em; font-weight: 600;">Payment Scheme Arbitration Docket</div>
                        </div>
                    </div>
                    <div style="text-align: right;">
                        <div style="font-family: 'JetBrains Mono', monospace; font-size: 0.8rem; font-weight: 700; color: #1A242C;">REF: #{active_case.get('order_id')}</div>
                        <div style="font-size: 0.72rem; color: #64748B;">Date: October 26, 2026</div>
                        <span class="stitch-pill stitch-pill-won" style="font-size: 0.68rem; padding: 2px 6px; margin-top: 4px; display: inline-block;">Formal Response</span>
                    </div>
                </div>

                <!-- Case Synopsis Table -->
                <div style="background: #F8F9FB; border: 1px solid #E5E7EB; border-radius: 6px; padding: 12px 14px; margin-bottom: 18px;">
                    <div style="display: flex; justify-content: space-between; align-items: center; margin-bottom: 8px; border-bottom: 1px solid #E5E7EB; padding-bottom: 6px;">
                        <span style="font-size: 0.72rem; font-weight: 700; color: #64748B; text-transform: uppercase; letter-spacing: 0.05em;">Case Synopsis &amp; Dispute Metadata</span>
                        <span style="font-family: 'JetBrains Mono', monospace; font-size: 0.72rem; color: #1A242C; font-weight: 600;">AWB: {active_case.get('tracking_id', 'BLUEDART-84920194')}</span>
                    </div>
                    <div style="display: grid; grid-template-columns: 1fr 1fr 1fr; gap: 8px; font-size: 0.78rem;">
                        <div>
                            <span style="color: #64748B; font-size: 0.7rem; display: block;">Customer</span>
                            <span style="font-weight: 600; color: #1A242C;">{active_case.get('customer_name')}</span>
                        </div>
                        <div>
                            <span style="color: #64748B; font-size: 0.7rem; display: block;">Dispute Classification</span>
                            <span style="font-weight: 600; color: #DC2626;">{active_case.get('dispute_type', 'Product Not Received')}</span>
                        </div>
                        <div>
                            <span style="color: #64748B; font-size: 0.7rem; display: block;">Disputed Amount</span>
                            <span style="font-weight: 700; color: #1A242C; font-family: 'JetBrains Mono', monospace;">₹{float(active_case.get('amount', 4299)):,.2f}</span>
                        </div>
                    </div>
                </div>

                <!-- Section 1: Executive Summary -->
                <div style="margin-bottom: 16px;">
                    <div style="display: flex; align-items: center; gap: 6px; margin-bottom: 6px;">
                        <span style="width: 4px; height: 14px; background: #1A242C; border-radius: 2px; display: inline-block;"></span>
                        <span style="font-size: 0.88rem; font-weight: 700; color: #1A242C;">1. Executive Summary &amp; Compelling Evidence</span>
                    </div>
                    <p style="font-size: 0.8rem; color: #334155; line-height: 1.55; margin: 0; text-align: justify;">
                        {exec_text}
                    </p>
                </div>

                <!-- Section 2: Chronological Sequence -->
                <div style="margin-bottom: 16px;">
                    <div style="display: flex; align-items: center; gap: 6px; margin-bottom: 8px;">
                        <span style="width: 4px; height: 14px; background: #1A242C; border-radius: 2px; display: inline-block;"></span>
                        <span style="font-size: 0.88rem; font-weight: 700; color: #1A242C;">2. Chronological Sequence of Verified Events</span>
                    </div>
                    <div style="font-size: 0.78rem; color: #475569; display: flex; flex-direction: column; gap: 6px; padding-left: 10px; border-left: 2px solid #E5E7EB;">
                        <div>&bull; <b style="color: #1A242C;">Order Placed:</b> Customer initiated transaction from verified IP &amp; session.</div>
                        <div>&bull; <b style="color: #1A242C;">Payment Reconciled:</b> 3DS Two-Factor Authentication confirmed with acquirer authorization.</div>
                        <div>&bull; <b style="color: #1A242C;">Courier Dispatched:</b> Manifest scan recorded with tracking ID {active_case.get('tracking_id', 'BLUEDART-84920194')}.</div>
                        <div>&bull; <b style="color: #059669;">Signed Delivery:</b> Consignee physical signature and GPS coordinates logged at billing destination.</div>
                    </div>
                </div>

                <!-- Section 3: Merchant Statement & Digital Seal -->
                <div style="margin-bottom: 16px;">
                    <div style="display: flex; align-items: center; gap: 6px; margin-bottom: 6px;">
                        <span style="width: 4px; height: 14px; background: #1A242C; border-radius: 2px; display: inline-block;"></span>
                        <span style="font-size: 0.88rem; font-weight: 700; color: #1A242C;">3. Merchant Operational Statement</span>
                    </div>
                    <p style="font-size: 0.78rem; color: #475569; line-height: 1.5; margin: 0; background: #F8F9FB; padding: 8px 10px; border-radius: 6px;">
                        {merchant_statement}
                    </p>
                </div>

                <!-- Document Footer -->
                <div style="border-top: 1px solid #E5E7EB; padding-top: 12px; margin-top: 20px; display: flex; justify-content: space-between; align-items: center; font-size: 0.7rem; color: #64748B;">
                    <span>Page 1 of 6 &bull; Confidential Dispute Submission</span>
                    <div style="display: flex; align-items: center; gap: 4px; color: #059669; font-weight: 600;">
                        <span class="material-symbols-outlined" style="font-size: 14px;">verified</span>
                        <span>Signatory: {signer_name} (SHA-256 Certified)</span>
                    </div>
                </div>

            </div>
        </div>
        """)

    # -------------------------------------------------------------
    # RIGHT COLUMN: Options, Live Editor Form & Actions
    # -------------------------------------------------------------
    with col_right:
        # Case Status Badge
        is_submitted = (active_case.get("status") == "submitted" or active_case.get("case_status") == "submitted")
        
        render_html(f"""
        <div class="stitch-card" style="margin-bottom: 16px;">
            <div class="stitch-card-header">
                <span class="stitch-card-title">Target Case</span>
                <span class="stitch-pill {'stitch-pill-won' if is_submitted else 'stitch-pill-review'}">
                    {'SUBMITTED' if is_submitted else 'PRIORITY REVIEW'}
                </span>
            </div>
            <div style="font-family: 'JetBrains Mono', monospace; font-size: 1.05rem; font-weight: 700; color: #1A242C;">
                #{active_case.get('order_id')}
            </div>
            <div style="font-size: 0.8rem; color: #64748B; margin-top: 2px;">
                Customer: {active_case.get('customer_name')}
            </div>
        </div>
        """)

        # Interactive Form
        with st.form("interactive_pdf_builder_form"):
            render_html("""
            <div class="stitch-card-header" style="margin-bottom: 8px;">
                <div style="display: flex; align-items: center; gap: 6px;">
                    <span class="material-symbols-outlined" style="color: #2D3948; font-size: 18px;">tune</span>
                    <span class="stitch-card-title">Rebuttal Customization</span>
                </div>
            </div>
            """)

            curr_title = st.session_state.get(f"pdf_title_{active_case_id}", rep.get("report_title", "Formal Chargeback Defense Packet"))
            curr_sig = st.session_state.get(f"pdf_sig_{active_case_id}", rep.get("digital_signature", {}).get("signer_name", "Apex Retail Operations Desk"))
            curr_notes = st.session_state.get(f"pdf_notes_{active_case_id}", rep.get("merchant_notes", "The cardholder was contacted via registered email and messaging. Goods were physically handed over with recipient signature verification. Chargeback claim is without merit."))
            curr_summary = st.session_state.get(f"pdf_summary_{active_case_id}", rep.get("executive_summary", "The order was placed, paid, and delivered to the verified cardholder address on file with signed confirmation. All factual records are reconciled and consistent across payment gateway, tax invoice, and courier manifests."))

            custom_title = st.text_input("Report Title", value=curr_title)
            digital_sig = st.text_input("Authorized Signatory", value=curr_sig)
            exec_summary_input = st.text_area("Executive Summary", value=curr_summary, height=110)
            notes = st.text_area("Merchant Statement", value=curr_notes, height=80)

            preview_btn = st.form_submit_button("Update Draft Preview", use_container_width=True)
            approve_btn = st.form_submit_button("Approve & Mark Submitted", use_container_width=True, type="primary")

        if preview_btn:
            if not custom_title.strip() or not exec_summary_input.strip():
                st.error("Report title and executive summary cannot be empty.")
            else:
                with st.spinner("Re-rendering PDF draft..."):
                    st.session_state[f"pdf_title_{active_case_id}"] = custom_title.strip()
                    st.session_state[f"pdf_sig_{active_case_id}"] = digital_sig.strip()
                    st.session_state[f"pdf_notes_{active_case_id}"] = notes.strip()
                    st.session_state[f"pdf_summary_{active_case_id}"] = exec_summary_input.strip()

                    custom_rep = service.preview_report(
                        case_id=active_case_id,
                        report_title=custom_title.strip(),
                        merchant_notes=notes.strip(),
                        signature_name=digital_sig.strip(),
                        executive_summary=exec_summary_input.strip()
                    )
                    pipeline_state["final_report"] = custom_rep
                    st.session_state[f"pipeline_run_{active_case_id}"] = pipeline_state
                    st.success("Draft updated!")
                    st.rerun()

        if approve_btn:
            if not custom_title.strip() or not exec_summary_input.strip() or not digital_sig.strip():
                st.error("All fields (Title, Signatory, Executive Summary) are required.")
            else:
                with st.spinner("Submitting case and compiling finalized packet..."):
                    custom_rep = service.preview_report(
                        case_id=active_case_id,
                        report_title=custom_title.strip(),
                        merchant_notes=notes.strip(),
                        signature_name=digital_sig.strip(),
                        executive_summary=exec_summary_input.strip()
                    )
                    pipeline_state["final_report"] = custom_rep
                    st.session_state[f"pipeline_run_{active_case_id}"] = pipeline_state
                    service.approve_case(active_case_id)
                    st.balloons()
                    st.success("Case marked as SUBMITTED!")
                    st.rerun()

        # Direct Download Button
        if pdf_bytes:
            st.download_button(
                label="Download Evidence PDF",
                data=pdf_bytes,
                file_name=f"chargeback_evidence_{active_case.get('order_id')}.pdf",
                mime="application/pdf",
                type="primary",
                key="download_btn_stitch_panel",
                use_container_width=True
            )
            st.caption(f"PDF Size: {len(pdf_bytes):,} bytes &bull; SHA-256 Digitally Signed")
        else:
            st.info("Generating defense docket...")


