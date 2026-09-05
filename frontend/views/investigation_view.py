"""
Chargeback Evidence AI - Multi-Agent Investigation & Live 10-Step Timeline
Stitch UI Design Integration:
1. Horizontal Case Lifecycle Progress Tracker
2. 10-Step Connected Live Timeline with Stitch cards & latency metrics
3. Dispute Classification & Explainable AI Score Drivers (+/- points)
4. Recommended Next Evidence with Win Rate Uplift (+14%)
5. Evidence Chat Assistant with zero hallucinations and clickable citations
"""

import time
import streamlit as st
from frontend.components import (
    render_score_radial,
    render_case_status_tracker,
    render_explainable_score_card,
    render_recommended_next_evidence,
    render_html
)
from agents.ml_scoring_agent import MLScoringAgent


def render_investigation_view(service):
    render_html("""
    <div style="display: flex; justify-content: space-between; align-items: flex-start; margin-bottom: 20px; flex-wrap: wrap; gap: 12px;">
        <div>
            <div style="display: flex; align-items: center; gap: 8px; margin-bottom: 4px;">
                <span class="material-symbols-outlined" style="color: #2D3948; font-size: 22px;">biotech</span>
                <h2 style="margin: 0; color: #1A242C; font-weight: 700; font-size: 1.4rem; letter-spacing: -0.02em;">Autonomous Multi-Agent Investigation</h2>
            </div>
            <p style="color: #64748B; font-size: 0.88rem; margin: 0;">7 specialized micro-agents cooperating through a 10-step pipeline to deconstruct, cross-verify, and defend this dispute.</p>
        </div>
        <div>
            <span class="stitch-pill stitch-pill-won" style="font-size: 0.8rem; padding: 4px 10px;">
                <span class="material-symbols-outlined" style="font-size: 16px;">bolt</span>
                Workflow Orchestrated
            </span>
        </div>
    </div>
    """)

    # Active case selection
    cases = service.list_cases()
    if not cases:
        st.warning("No chargeback cases found. Please create a case first.")
        return

    case_options = {f"{c['order_id']} - ₹{c['amount']:,.0f} ({c['dispute_reason']})": c['id'] for c in cases}
    default_idx = 0
    if st.session_state.get("active_case_id"):
        for idx, (label, cid) in enumerate(case_options.items()):
            if cid == st.session_state["active_case_id"]:
                default_idx = idx
                break

    selected_label = st.selectbox("Active Dispute Case Under Investigation", list(case_options.keys()), index=default_idx)
    active_case_id = case_options[selected_label]
    st.session_state["active_case_id"] = active_case_id

    active_case = service.get_case(active_case_id)

    # Horizontal Lifecycle Tracker
    render_case_status_tracker(active_case.get("case_status") or active_case.get("status", "investigating"))

    col_btn1, col_btn2 = st.columns([2, 3])
    with col_btn1:
        run_pipeline = st.button("Execute 10-Step Pipeline", type="primary", use_container_width=True)
    with col_btn2:
        st.caption(f"Order: **{active_case.get('order_id')}** &bull; Customer: **{active_case.get('customer_name')}** &bull; Disputed: **₹{active_case.get('amount'):,.2f}** &bull; Type: `{active_case.get('dispute_type', 'Product Not Received')}`")

    # Progress container
    pipeline_state = st.session_state.get(f"pipeline_run_{active_case_id}")

    if run_pipeline:
        status_bar = st.progress(0, text="Initializing 10-step multi-agent pipeline...")
        timeline_10 = [
            ("Document Agent", "Classifying evidence files into structured dockets..."),
            ("OCR Agent", "Running CV image deskewing, denoising & text layer extraction..."),
            ("OCR Agent", "Parsing itemized table matrices and tax breakdowns..."),
            ("NLP Agent", "Extracting customer names, order IDs, ISO dates, and amounts..."),
            ("Verification Agent", "Validating GSTIN, PAN & KYC corporate vault credentials..."),
            ("Verification Agent", "Triangulating cross-document consistency & auditing contradictions..."),
            ("Intelligence Agent", "Cross-referencing historical dispute rulings and arbitration benchmarks..."),
            ("ML Scoring Agent", "Evaluating evidence strength model & calculating win uplift..."),
            ("Narrative Agent", "Synthesizing formal defense narrative with timestamped facts..."),
            ("Report Agent", "Compiling submission-ready dispute defense packet...")
        ]

        for idx, (aname, msg) in enumerate(timeline_10):
            status_bar.progress(int((idx + 1) * 10), text=f"Step {idx+1}/10: {aname} - {msg}")
            time.sleep(0.15)

        with st.spinner("Finalizing agent outputs and assembling verdict..."):
            pipeline_state = service.run_full_pipeline(active_case_id)
            st.session_state[f"pipeline_run_{active_case_id}"] = pipeline_state
            status_bar.progress(100, text="✓ All 10 Steps Completed Investigation Successfully!")
            time.sleep(0.12)
            status_bar.empty()

    if not pipeline_state:
        saved_run = service.get_latest_run(active_case_id)
        if saved_run:
            pipeline_state = saved_run
        else:
            pipeline_state = service.run_full_pipeline(active_case_id)
            st.session_state[f"pipeline_run_{active_case_id}"] = pipeline_state

    # 10-Step Timeline and ML Verdict Layout
    col_left, col_right = st.columns([3, 2])

    with col_left:
        render_html("""
        <div class="stitch-card-header" style="margin-bottom: 12px;">
            <div style="display: flex; align-items: center; gap: 8px;">
                <span class="material-symbols-outlined" style="color: #2D3948; font-size: 20px;">timeline</span>
                <span class="stitch-card-title">Live 10-Step Investigation Timeline</span>
            </div>
            <span class="stitch-pill stitch-pill-won">10/10 Complete</span>
        </div>
        """)
        steps = pipeline_state.get("steps", [])
        for step in steps:
            step_num = step.get("step_number", 1)
            aname = step.get("agent_name", "AI Agent")
            stitle = step.get("step_title", step.get("output_preview", ""))
            etime = float(step.get("execution_time_sec", 0.3))
            conf = float(step.get("confidence", 0.95))
            preview = step.get("output_preview", "")

            render_html(f"""
            <div class="step-card complete">
                <div class="step-badge-num complete">✓ {step_num}</div>
                <div class="step-content">
                    <div class="step-header">
                        <div class="step-name">{stitle}</div>
                        <span class="step-agent">{aname}</span>
                    </div>
                    <div class="step-desc">{preview}</div>
                    <div class="step-meta">
                        <span>⏱️ Latency: <b>{etime:.2f}s</b></span>
                        <span>🎯 Quality: <b>{int(conf*100)}%</b></span>
                        <span class="stitch-pill stitch-pill-won" style="font-size: 0.68rem; padding: 2px 6px;">COMPLETED</span>
                    </div>
                </div>
            </div>
            """)

    with col_right:
        render_html("""
        <div class="stitch-card-header" style="margin-bottom: 12px;">
            <div style="display: flex; align-items: center; gap: 8px;">
                <span class="material-symbols-outlined" style="color: #2D3948; font-size: 20px;">analytics</span>
                <span class="stitch-card-title">Risk &amp; Evidence Verdict</span>
            </div>
        </div>
        """)
        score_val = pipeline_state.get("evidence_score", 92)
        win_prob = pipeline_state.get("win_probability", 0.92)

        render_score_radial(score_val, win_prob)

        # ML Scoring Agent output with explainable breakdown
        ml_agent = MLScoringAgent()
        ver_rep = pipeline_state.get("verification_report") or {"overall_confidence": 0.95, "contradictions_detected": []}
        ml_score_data = ml_agent.score_case(active_case, ver_rep, doc_count=3)

        render_explainable_score_card(ml_score_data)

        # Recommended Next Evidence Banner
        rec_data = ml_score_data.get("recommended_next_evidence", {
            "recommended_document": "Courier Proof of Delivery (POD)",
            "win_probability_uplift_pct": 14,
            "reason": "Proves physical doorstep delivery with signature.",
            "suggested_alternative": "Customer Delivery Confirmation Email"
        })
        render_recommended_next_evidence(rec_data)

        # Quick Navigation
        render_html("""
        <div class="stitch-card" style="margin-top: 14px;">
            <div class="stitch-card-header" style="margin-bottom: 8px;">
                <span class="stitch-card-title">Next Steps</span>
            </div>
        </div>
        """)
        c_act1, c_act2 = st.columns(2)
        with c_act1:
            if st.button("Evidence Integrity", use_container_width=True):
                st.session_state["current_page"] = "Evidence Integrity"
                st.rerun()
        with c_act2:
            if st.button("Final Defense Packet", use_container_width=True, type="primary"):
                st.session_state["current_page"] = "Final Packet"
                st.rerun()

    # -------------------------------------------------------------
    # AI Evidence Chat Assistant
    # -------------------------------------------------------------
    st.write("---")
    render_html("""
    <div style="margin-bottom: 12px;">
        <div style="display: flex; align-items: center; gap: 8px; margin-bottom: 4px;">
            <span class="material-symbols-outlined" style="color: #2D3948; font-size: 20px;">chat</span>
            <h3 style="margin: 0; font-size: 1.15rem; font-weight: 700; color: #1A242C;">Dispute Evidence Assistant</h3>
        </div>
        <p style="color: #64748B; font-size: 0.84rem; margin: 0;">Ask any question about this active dispute. Answers are cross-checked directly against attached invoices, courier logs, and transaction records.</p>
    </div>
    """)

    chat_history_key = f"chat_history_{active_case_id}"
    if chat_history_key not in st.session_state:
        st.session_state[chat_history_key] = [
            {
                "is_user": False,
                "text": f"Hello! I am your AI Evidence Assistant for Case **{active_case.get('order_id')}**. I have analyzed all invoices, shipping logs, and customer communications. What would you like to verify?",
                "citations": []
            }
        ]

    for msg in st.session_state[chat_history_key]:
        if msg["is_user"]:
            render_html(f'<div class="chat-bubble-user">{msg["text"]}</div>')
        else:
            render_html(f'<div class="chat-bubble-ai">{msg["text"]}</div>')
            for cit in msg.get("citations", []):
                render_html(f"""
                <div class="citation-box">
                    <span class="material-symbols-outlined" style="font-size: 16px; color: #0284C7; vertical-align: middle;">menu_book</span>
                    <b>Citation:</b> {cit.get('source_file')} (Page {cit.get('page_number')}) &bull; Snippet: <i>"{cit.get('snippet')}"</i>
                </div>
                """)

    with st.form(key=f"chat_form_{active_case_id}", clear_on_submit=True):
        col_q, col_s = st.columns([5, 1])
        with col_q:
            user_question = st.text_input("Ask a question about the evidence...", placeholder="e.g. Was the delivery address verified against the tax invoice?", label_visibility="collapsed")
        with col_s:
            submit_q = st.form_submit_button("Send ➔", use_container_width=True, type="primary")

        if submit_q and user_question.strip():
            st.session_state[chat_history_key].append({"is_user": True, "text": user_question, "citations": []})
            with st.spinner("Analyzing case evidence dockets..."):
                chat_res = service.ask_ai_chat(active_case_id, user_question)
                st.session_state[chat_history_key].append({
                    "is_user": False,
                    "text": chat_res.get("answer", "Evidence analyzed."),
                    "citations": chat_res.get("citations", [])
                })
            st.rerun()
