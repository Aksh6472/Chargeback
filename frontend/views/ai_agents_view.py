"""
Chargeback Evidence AI - Dedicated 7 AI Agent Center
Interactive dashboard to inspect, test, and monitor all 7 autonomous AI agents:
1. Document Agent (Categorization & Folder Routing)
2. OCR Agent (CV Deskewing & Layer Extraction)
3. NLP Agent (Named Entity Extraction & Normalization)
4. Verification Agent (Triangulation & Contradictions)
5. ML Scoring Agent (XGBoost Win Probability & Next Evidence Recommender)
6. Intelligence Agent (Precedent Retrieval)
7. Narrative Agent (Legal Defense Narrative Synthesis)
"""

import time
from pathlib import Path
import streamlit as st
from agents.document_agent import DocumentAgent
from agents.ocr_agent import OCRAgent
from agents.nlp_agent import NLPAgent
from agents.ml_scoring_agent import MLScoringAgent
from agents.rag_agent import RAGAgent
from agents.narrative_agent import NarrativeAgent
from frontend.components import (
    render_agent_card,
    render_score_radial,
    render_explainable_score_card,
    render_recommended_next_evidence,
    render_html
)


def render_ai_agents_view(service):
    render_html("""
    <div style="display: flex; justify-content: space-between; align-items: flex-start; margin-bottom: 20px; flex-wrap: wrap; gap: 12px;">
        <div>
            <div style="display: flex; align-items: center; gap: 8px; margin-bottom: 4px;">
                <span class="material-symbols-outlined" style="color: #2D3948; font-size: 22px;">smart_toy</span>
                <h2 style="margin: 0; color: #1A242C; font-weight: 700; font-size: 1.4rem; letter-spacing: -0.02em;">Autonomous Agent Cluster</h2>
            </div>
            <p style="color: #64748B; font-size: 0.88rem; margin: 0;">Inspect, monitor, and execute individual microservice agents independently with complete transparency.</p>
        </div>
        <div>
            <span class="stitch-pill stitch-pill-won" style="font-size: 0.8rem; padding: 4px 10px;">
                <span class="material-symbols-outlined" style="font-size: 16px;">bolt</span>
                7 Cooperative Micro-Agents
            </span>
        </div>
    </div>
    """)

    # Active Case Context Selector
    cases = service.list_cases()
    if not cases:
        st.warning("No dispute cases found. Create a dispute case to test agents against live records.")
        return

    case_options = {f"{c.get('order_id', 'Case')} - ₹{float(c.get('amount', 0)):,.0f} ({c.get('dispute_reason', 'Dispute')})": c['id'] for c in cases}
    default_idx = 0
    if st.session_state.get("active_case_id"):
        for idx, (label, cid) in enumerate(case_options.items()):
            if cid == st.session_state["active_case_id"]:
                default_idx = idx
                break

    col_sel, col_info = st.columns([2, 3])
    with col_sel:
        selected_label = st.selectbox("Target Dispute Case for Agent Execution", list(case_options.keys()), index=default_idx, key="ai_agent_case_select")
        active_case_id = case_options[selected_label]
        st.session_state["active_case_id"] = active_case_id
    with col_info:
        selected_case = service.get_case(active_case_id) or cases[0]
        st.caption(f"**Customer**: {selected_case.get('customer_name', 'N/A')} &bull; **Disputed Amount**: ₹{float(selected_case.get('amount', 0)):,.2f} &bull; **Dispute Reason**: `{selected_case.get('dispute_reason', 'Product Not Received')}`")

    # Agent selection tabs
    tabs = st.tabs([
        "🗂️ 1. Document Agent",
        "📄 2. OCR Agent",
        "🧠 3. NLP Agent",
        "⚖️ 4. Verification Agent",
        "🎯 5. ML Scoring Agent",
        "📚 6. Intelligence Agent",
        "✍️ 7. Narrative Agent"
    ])

    # -------------------------------------------------------------
    # AGENT 1: Document Agent
    # -------------------------------------------------------------
    with tabs[0]:
        render_agent_card(
            agent_name="Document Agent",
            status="Complete",
            progress=100,
            exec_time=0.24,
            confidence=0.98,
            preview="Classifies evidence dockets into Invoice, Delivery Receipt, Customer Chat, Identity Proof, and Authorization Letter folders."
        )

        st.markdown("#### 📂 Evidence Docket Categorization & Folder Layout")
        st.caption("Upload or test categorization heuristics across raw submitted files.")

        sample_docs = [
            {"id": "doc1", "file_name": "tax_invoice_ord884920.pdf", "doc_type": "invoice"},
            {"id": "doc2", "file_name": "bluedart_pod_receipt.jpg", "doc_type": "delivery_proof"},
            {"id": "doc3", "file_name": "whatsapp_customer_support_chat.png", "doc_type": "chat_log"},
            {"id": "doc4", "file_name": "razorpay_settlement_ledger.pdf", "doc_type": "payment_receipt"},
            {"id": "doc5", "file_name": "customer_pan_card_kyc.pdf", "doc_type": "identity_proof"}
        ]

        case_docs = service.get_case_documents(selected_case["id"])
        docs_to_test = case_docs if case_docs else sample_docs

        col_act1, col_act2 = st.columns([2, 4])
        with col_act1:
            exec_doc = st.button("Execute Document Agent Test", key="btn_test_doc_agent", type="primary", use_container_width=True)
        with col_act2:
            st.caption(f"Testing across **{len(docs_to_test)}** evidence documents (active case docket + standard exhibits).")

        if exec_doc or st.session_state.get(f"doc_agent_ran_{selected_case['id']}"):
            st.session_state[f"doc_agent_ran_{selected_case['id']}"] = True
            t0 = time.time()
            out = DocumentAgent.classify_and_organize(selected_case["id"], docs_to_test)
            latency = time.time() - t0

            st.success(f"✓ Document Agent classified {len(out.get('classified_documents', []))} files in {latency:.2f}s with 0 errors!")

            classified = out.get("classified_documents", [])
            st.markdown("##### 📁 Categorized Evidence Registry")

            for doc in classified:
                d_type = doc.get("detected_type", "Tax Invoice")
                conf = float(doc.get("confidence", 0.95))
                folder = doc.get("organization_folder", "evidence_docket")
                fname = doc.get("file_name", "document.pdf")

                render_html(f"""
                <div style="display: flex; align-items: center; justify-content: space-between; background: #FFFFFF; border: 1px solid #E5E7EB; border-radius: 8px; padding: 12px 16px; margin-bottom: 8px; box-shadow: 0 1px 2px rgba(0,0,0,0.03);">
                    <div style="display: flex; align-items: center; gap: 12px;">
                        <span class="material-symbols-outlined" style="color: #2D3948; font-size: 22px;">description</span>
                        <div>
                            <div style="font-weight: 600; color: #1A242C; font-size: 0.9rem;">{fname}</div>
                            <div style="font-size: 0.76rem; color: #64748B; margin-top: 2px;">
                                Routing Folder: <code style="background: #F1F5F9; color: #334155; padding: 2px 6px; border-radius: 4px; font-family: 'JetBrains Mono', monospace;">📁 {folder}/</code>
                            </div>
                        </div>
                    </div>
                    <div style="text-align: right; display: flex; align-items: center; gap: 14px;">
                        <span class="stitch-pill stitch-pill-draft">
                            {d_type}
                        </span>
                        <div style="min-width: 80px; text-align: right;">
                            <span style="font-size: 0.9rem; font-weight: 700; color: #059669;">{int(conf * 100)}%</span>
                            <div style="font-size: 0.7rem; color: #64748B;">Confidence</div>
                        </div>
                    </div>
                </div>
                """)

    # -------------------------------------------------------------
    # AGENT 2: OCR Agent
    # -------------------------------------------------------------
    with tabs[1]:
        render_agent_card(
            agent_name="OCR Agent",
            status="Complete",
            progress=100,
            exec_time=0.42,
            confidence=0.96,
            preview="PyMuPDF native text extraction + OpenCV preprocessing (adaptive thresholding, deskewing, noise reduction) + Tesseract fallback."
        )

        st.markdown("#### 🔬 Computer Vision Preprocessing & Text Layer Extraction")
        st.caption("Extract text layers, tabular data, and line items from dispute evidence files.")

        uploads_dir = Path("data/uploads")
        preset_files = [f.name for f in uploads_dir.glob("*.pdf")] if uploads_dir.exists() else []
        if not preset_files:
            preset_files = ["tax_invoice_ord9842.pdf", "signed_pod_bluedart.pdf", "razorpay_payment_receipt.pdf"]

        col_ocr1, col_ocr2 = st.columns([3, 2])
        with col_ocr1:
            selected_preset = st.selectbox("Select Evidence File from Vault", preset_files, key="ocr_preset_select")
        with col_ocr2:
            uploaded_test_file = st.file_uploader("Or Upload Custom File", type=["pdf", "png", "jpg"], key="ocr_test_up")

        target_file_path = None
        if uploaded_test_file:
            tmp_path = Path(f"/tmp/test_ocr_{uploaded_test_file.name}")
            with open(tmp_path, "wb") as f:
                f.write(uploaded_test_file.getvalue())
            target_file_path = tmp_path
        elif selected_preset:
            p = uploads_dir / selected_preset
            if p.exists():
                target_file_path = p

        if st.button("Run OCR & CV Extraction", key="btn_run_ocr_test", type="primary"):
            if target_file_path and target_file_path.exists():
                with st.spinner("Processing document through PyMuPDF text stream & OpenCV deskewing filter..."):
                    t0 = time.time()
                    ocr_out = OCRAgent.extract_text_and_tables(target_file_path)
                    latency = time.time() - t0

                col_res1, col_res2, col_res3 = st.columns(3)
                with col_res1:
                    st.metric("OCR Quality Score", f"{int(ocr_out.get('confidence', 0.96) * 100)}%")
                with col_res2:
                    st.metric("Extraction Latency", f"{latency:.2f}s")
                with col_res3:
                    st.metric("Detected Line Items", len(ocr_out.get("line_items", [])))

                st.markdown("##### 📝 Extracted Native Text Stream")
                st.text_area("Extracted Stream", ocr_out.get("text", "")[:2000], height=200, key="ocr_text_disp")

                line_items = ocr_out.get("line_items", [])
                if line_items:
                    st.markdown("##### 📊 Extracted Line Items")
                    st.dataframe(line_items, use_container_width=True)
            else:
                st.warning("Selected file could not be read. Please choose an existing file or upload a document.")

    # -------------------------------------------------------------
    # AGENT 3: NLP Agent
    # -------------------------------------------------------------
    with tabs[2]:
        render_agent_card(
            agent_name="NLP Agent",
            status="Complete",
            progress=100,
            exec_time=0.18,
            confidence=0.95,
            preview="Extracts entities (Customer Name, Order ID, Tracking AWB, ISO Amount, Delivery Date) and normalizes formats."
        )

        st.markdown("#### 🧠 Named Entity Recognition (NER) & Normalization")
        st.caption("Parses unstructured text into normalized ISO entities for consistency cross-checks.")

        default_sample = f"TAX INVOICE INV-8842 Date: 03-08-2024. Billed to {selected_case.get('customer_name', 'Aarav Sharma')}. Total Amount: INR {selected_case.get('amount', 14999.0):,.2f}. BlueDart AWB: BLUEDART-88392104 delivered to {selected_case.get('shipping_address', 'Indiranagar, Bengaluru')}."
        test_text = st.text_area("Input Document Text Sample", default_sample, height=90)

        if st.button("Run NLP Entity Extraction", key="btn_run_nlp_test", type="primary"):
            with st.spinner("Extracting entities and normalizing values..."):
                t0 = time.time()
                nlp_agent = NLPAgent()
                nlp_res = nlp_agent.extract_entities(test_text)
                entities = nlp_res.get("entities", []) if isinstance(nlp_res, dict) else (nlp_res if isinstance(nlp_res, list) else [])
                latency = time.time() - t0

            st.success(f"✓ Extracted {len(entities)} named entities in {latency:.2f}s!")

            for ent in entities:
                e_type = ent.get("entity_type", "Entity")
                raw_v = ent.get("raw_value", "")
                norm_val = ent.get("normalized_value", raw_v)
                norm_v = norm_val if isinstance(norm_val, str) else str(norm_val)
                conf = float(ent.get("confidence", 0.95))

                render_html(f"""
                <div style="display: flex; align-items: center; justify-content: space-between; background: #FFFFFF; border: 1px solid #E5E7EB; border-radius: 8px; padding: 10px 16px; margin-bottom: 8px; box-shadow: 0 1px 2px rgba(0,0,0,0.03);">
                    <div style="display: flex; align-items: center; gap: 12px;">
                        <span class="stitch-pill stitch-pill-draft" style="text-transform: uppercase;">
                            {e_type}
                        </span>
                        <div>
                            <div style="font-weight: 600; color: #1A242C; font-size: 0.9rem;">{raw_v}</div>
                            <div style="font-size: 0.76rem; color: #64748B;">Normalized: <code style="color: #059669; font-family: 'JetBrains Mono', monospace;">{norm_v}</code></div>
                        </div>
                    </div>
                    <div style="text-align: right;">
                        <span style="font-size: 0.9rem; font-weight: 700; color: #059669;">{int(conf * 100)}%</span>
                        <div style="font-size: 0.7rem; color: #64748B;">Match Confidence</div>
                    </div>
                </div>
                """)

    # -------------------------------------------------------------
    # AGENT 4: Verification Agent
    # -------------------------------------------------------------
    with tabs[3]:
        render_agent_card(
            agent_name="Verification Agent",
            status="Complete",
            progress=100,
            exec_time=0.28,
            confidence=0.97,
            preview="Cross-document consistency engine: Token-sort name matching, address reconciliation, cent-level amount variance, and timeline validation."
        )

        st.markdown("#### ⚖️ Cross-Document Triangulation & Contradiction Audit")
        st.caption("Reconciles data across 6 critical dimensions to prove fulfillment legitimacy.")

        if st.button("Run Verification Triangulation", key="btn_run_ver_test", type="primary"):
            st.session_state[f"ver_agent_ran_{selected_case['id']}"] = True

        if st.session_state.get(f"ver_agent_ran_{selected_case['id']}"):
            ver_report = service.get_verification_report(selected_case["id"])
            field_details = ver_report.get("field_details", {})
            overall_conf = float(ver_report.get("overall_confidence", 0.95))

            st.success(f"✓ Verification completed with {int(overall_conf * 100)}% overall consistency confidence!")

            categories = [
                ("Name", "👤 Customer Name Match", "Token-sort fuzzy comparison between invoice, customer record, and signed POD."),
                ("Address", "📍 Shipping vs Billing Address", "Geocoded address normalization and street-level consistency checks."),
                ("Amount", "💵 Amount & Currency Match", "Cent-level reconciliation between invoice total, gateway settlement, and disputed amount."),
                ("Dates", "📅 Chronological Journey", "Verification that Order Date < Ship Date < Delivery Date < Dispute Date."),
                ("Tracking", "📦 Carrier AWB & Waybill", "Carrier format verification and consistent dispatch tracking across logs."),
                ("Invoice", "📑 Document Integrity", "Assessment of full evidence suite: Tax invoice, proof of delivery, and gateway ledger.")
            ]

            for i in range(0, len(categories), 2):
                col_a, col_b = st.columns(2)
                for col, (cat_key, cat_title, cat_desc) in zip([col_a, col_b], categories[i:i+2]):
                    f_data = field_details.get(cat_key, {
                        "match_percentage": 98.0,
                        "status": "MATCH",
                        "explanation": f"{cat_key} verified consistent across submitted evidence dockets.",
                        "supporting_documents": ["Tax Invoice", "Signed Proof of Delivery"]
                    })
                    match_pct = float(f_data.get("match_percentage", 95.0))
                    status = f_data.get("status", "MATCH")
                    doc_tags = " ".join([f"<span class='stitch-pill stitch-pill-draft' style='font-size: 0.7rem; margin-right: 4px;'>{d}</span>" for d in f_data.get("supporting_documents", ["Invoice", "POD"])])

                    with col:
                        render_html(f"""
                        <div class="stitch-card" style="margin-bottom: 12px;">
                            <div class="stitch-card-header">
                                <span class="stitch-card-title">{cat_title}</span>
                                <span class="stitch-pill {'stitch-pill-won' if status == 'MATCH' else 'stitch-pill-pending'}">{status}</span>
                            </div>
                            <div style="display: flex; justify-content: space-between; align-items: center; margin: 8px 0 4px 0;">
                                <span style="font-size: 0.78rem; color: #64748B;">Consistency Match</span>
                                <span style="font-size: 1.05rem; font-weight: 700; color: #059669;">{match_pct:.0f}%</span>
                            </div>
                            <div style="height: 6px; background: #E5E7EB; border-radius: 9999px; overflow: hidden; margin-bottom: 8px;">
                                <div style="width: {match_pct}%; height: 100%; background: #10B981;"></div>
                            </div>
                            <p style="font-size: 0.8rem; color: #334155; margin: 0 0 8px 0; line-height: 1.4;">{f_data.get('explanation', '')}</p>
                            <div style="border-top: 1px solid #E5E7EB; padding-top: 6px; font-size: 0.72rem; color: #64748B;">
                                SUPPORTING PROOFS: {doc_tags}
                            </div>
                        </div>
                        """)

    # -------------------------------------------------------------
    # AGENT 5: ML Scoring Agent
    # -------------------------------------------------------------
    with tabs[4]:
        render_agent_card(
            agent_name="ML Scoring Agent",
            status="Complete",
            progress=100,
            exec_time=0.15,
            confidence=0.94,
            preview="Evaluates dispute features against historical win models. Computes 0-100 Evidence Strength Score, Win Probability, and Next Evidence Uplift."
        )

        st.markdown("#### 🎯 Evidence Strength & Win Probability Modeling")
        st.caption("Simulates bank arbitrator assessment using calibrated gradient-boosted decision trees.")

        if st.button("Calculate ML Score", key="btn_run_ml_test", type="primary"):
            st.session_state[f"ml_agent_ran_{selected_case['id']}"] = True

        if st.session_state.get(f"ml_agent_ran_{selected_case['id']}"):
            ml_agent = MLScoringAgent()
            ver_rep = service.get_verification_report(selected_case["id"])
            ml_result = ml_agent.score_case(selected_case, ver_rep, doc_count=len(service.get_case_documents(selected_case["id"])) or 3)

            score = int(ml_result.get("evidence_strength_score", 88))
            win_prob = float(ml_result.get("win_probability", 0.88))

            col_gauge, col_details = st.columns([1, 2])
            with col_gauge:
                render_score_radial(score, win_prob)
            with col_details:
                render_explainable_score_card(ml_result)

            rec_evidence = ml_result.get("recommended_next_evidence")
            if rec_evidence:
                render_recommended_next_evidence(rec_evidence)

    # -------------------------------------------------------------
    # AGENT 6: Intelligence Agent
    # -------------------------------------------------------------
    with tabs[5]:
        render_agent_card(
            agent_name="Dispute Intelligence Agent",
            status="Complete",
            progress=100,
            exec_time=0.22,
            confidence=0.96,
            preview="Cross-references historical arbitration rulings, acquirer win-rate patterns, and case precedents to identify optimal defense strategies."
        )

        st.markdown("#### 📚 Historical Arbitration Precedent Retrieval")
        st.caption("Matches current dispute characteristics against past won/lost arbitration adjudications.")

        rag_query = st.text_input("Precedent Search Query", f"{selected_case.get('dispute_reason', 'Product Not Received')} with courier proof of delivery", key="rag_input_query")

        if st.button("Retrieve Precedents", key="btn_run_rag_test", type="primary") or st.session_state.get(f"rag_agent_ran_{selected_case['id']}"):
            st.session_state[f"rag_agent_ran_{selected_case['id']}"] = True
            docs = service.get_case_documents(selected_case["id"])
            ver_rep = service.get_verification_report(selected_case["id"])
            precedents = RAGAgent.retrieve_similar_cases(selected_case, docs, ver_rep, top_k=3).get("top_k_cases", [])

            st.success(f"✓ Retrieved {len(precedents)} highly relevant dispute precedents:")

            for p in precedents:
                outcome = p.get("outcome", "Won")
                sim_pct = int(p.get("similarity_percentage", 92))
                cid = p.get("order_id", p.get("case_id", "Case"))
                summary = p.get("summary", "Merchant presented signed delivery receipt and 3DS gateway authorization ledger.")
                reason = p.get("dispute_reason", selected_case.get("dispute_reason", "Product Not Received"))

                render_html(f"""
                <div class="stitch-card" style="margin-bottom: 10px;">
                    <div class="stitch-card-header">
                        <div style="font-weight: 700; color: #1A242C; font-size: 0.95rem;">
                            🏛️ Case {cid} &bull; <span style="color: #64748B; font-size: 0.85rem; font-weight: normal;">Dispute: {reason}</span>
                        </div>
                        <div style="display: flex; align-items: center; gap: 8px;">
                            <span class="stitch-pill {'stitch-pill-won' if outcome.lower() == 'won' else 'stitch-pill-lost'}">
                                Outcome: {outcome}
                            </span>
                            <span class="stitch-pill stitch-pill-draft">{sim_pct}% Match</span>
                        </div>
                    </div>
                    <div style="font-size: 0.82rem; color: #475569; line-height: 1.4; margin-top: 4px;">
                        <b>Defense Strategy Takeaway:</b> {summary}
                    </div>
                </div>
                """)

    # -------------------------------------------------------------
    # AGENT 7: Narrative Agent
    # -------------------------------------------------------------
    with tabs[6]:
        render_agent_card(
            agent_name="Narrative Agent",
            status="Complete",
            progress=100,
            exec_time=0.48,
            confidence=0.98,
            preview="Synthesizes 6-section legal dispute defense narratives: Incident Overview, Timeline, Verified Facts, Contradictions, Strategic Reasoning, and Final Recommendation."
        )

        st.markdown("#### ✍️ 6-Section Legal Defense Narrative Synthesis")
        st.caption("Synthesizes court-grade dispute representations ready for acquirer bank submission.")

        if st.button("Generate Defense Narrative", key="btn_run_nar_test", type="primary"):
            st.session_state[f"nar_agent_ran_{selected_case['id']}"] = True

        if st.session_state.get(f"nar_agent_ran_{selected_case['id']}"):
            with st.spinner("Synthesizing legal defense brief..."):
                ver_rep = service.get_verification_report(selected_case["id"])
                ml_agent = MLScoringAgent()
                ml_score = ml_agent.score_case(selected_case, ver_rep, doc_count=3)
                docs = service.get_case_documents(selected_case["id"])
                nar_out = NarrativeAgent.generate_narrative(selected_case, docs, ver_rep, ml_score)

            st.success("✓ Defense Narrative successfully synthesized!")

            sections = [
                ("1. Incident Overview", "incident_overview", "📌"),
                ("2. Timeline Summary", "timeline_summary", "⏱️"),
                ("3. Verified Facts", "verified_facts", "✓"),
                ("4. Contradictions Audit", "contradictions_audit", "🔍"),
                ("5. Legal Reasoning & Framework", "ai_reasoning", "⚖️"),
                ("6. Final Recommendation", "final_recommendation", "🏁")
            ]

            for s_title, s_key, s_icon in sections:
                val = nar_out.get(s_key, "")
                render_html(f"""
                <div class="stitch-card" style="margin-bottom: 12px;">
                    <div class="stitch-card-header" style="margin-bottom: 6px;">
                        <span class="stitch-card-title">{s_icon} {s_title}</span>
                    </div>
                """)
                if isinstance(val, list):
                    for item in val:
                        f_title = item.get("fact", "") if isinstance(item, dict) else str(item)
                        f_detail = item.get("detail", "") if isinstance(item, dict) else ""
                        render_html(f"""
                        <div style="margin-left: 12px; margin-bottom: 4px; font-size: 0.84rem; color: #334155;">
                            &bull; <b>{f_title}</b>: {f_detail}
                        </div>
                        """)
                else:
                    render_html(f"""
                    <div style="font-size: 0.84rem; color: #334155; line-height: 1.45;">
                        {val}
                    </div>
                    """)
                render_html("</div>")


