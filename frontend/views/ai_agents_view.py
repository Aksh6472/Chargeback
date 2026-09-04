"""
Chargeback Evidence AI - Dedicated 7 AI Agent Center
Interactive dashboard to inspect, test, and monitor all 7 autonomous AI agents:
1. Document Agent (Categorization & Folder Routing)
2. OCR Agent (CV Deskewing & Layer Extraction)
3. NLP Agent (Named Entity Extraction & Normalization)
4. Verification Agent (Triangulation & Contradictions)
5. ML Scoring Agent (XGBoost Win Probability & Next Evidence Recommender)
6. RAG Agent (pgvector Precedent Retrieval)
7. Narrative Agent (Legal Defense Narrative Synthesis)
"""

import streamlit as st
import time
from pathlib import Path
from agents.document_agent import DocumentAgent
from agents.ocr_agent import OCRAgent
from agents.nlp_agent import NLPAgent
from agents.verification_engine import EvidenceConsistencyEngine
from agents.ml_scoring_agent import MLScoringAgent
from agents.rag_agent import RAGAgent
from agents.narrative_agent import NarrativeAgent
from frontend.components import render_agent_card

def render_ai_agents_view(service):
    st.markdown("""
    <div style="margin-bottom: 24px;">
        <h2 style="margin: 0; color: #F8FAFC; font-weight: 700; letter-spacing: -0.02em;">🤖 Autonomous 7 AI Agent Center</h2>
        <p style="color: #94A3B8; font-size: 0.88rem; margin-top: 4px;">Inspect, monitor, and execute individual microservice agents independently with full transparency.</p>
    </div>
    """, unsafe_allow_html=True)

    # Agent selection tabs
    tabs = st.tabs([
        "🗂️ 1. Document Agent",
        "📄 2. OCR Agent",
        "🧠 3. NLP Agent",
        "⚖️ 4. Verification Agent",
        "🎯 5. ML Scoring Agent",
        "📚 6. RAG Agent",
        "✍️ 7. Narrative Agent"
    ])

    cases = service.list_cases()
    selected_case = cases[0] if cases else {
        "id": "case_demo",
        "order_id": "ORD-884920",
        "amount": 14999.0,
        "currency": "INR",
        "customer_name": "Aarav Sharma",
        "dispute_reason": "Product Not Received"
    }

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
        st.markdown('<div class="fintech-card">', unsafe_allow_html=True)
        st.markdown("#### Test Document Categorization & Folder Layout")
        sample_docs = [
            {"id": "doc1", "file_name": "tax_invoice_ord884920.pdf", "doc_type": "invoice"},
            {"id": "doc2", "file_name": "bluedart_pod_receipt.jpg", "doc_type": "delivery_proof"},
            {"id": "doc3", "file_name": "whatsapp_customer_support_chat.png", "doc_type": "chat_log"}
        ]
        if st.button("▶️ Execute Document Agent Test", key="btn_test_doc_agent", type="primary"):
            t0 = time.time()
            out = DocumentAgent.classify_and_organize(selected_case["id"], sample_docs)
            st.success(f"Classification completed in {time.time()-t0:.2f}s!")
            st.json(out)
        st.markdown('</div>', unsafe_allow_html=True)

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
        st.markdown('<div class="fintech-card">', unsafe_allow_html=True)
        st.markdown("#### Test OCR Preprocessing & Extraction")
        uploaded_test_file = st.file_uploader("Upload sample document to extract", type=["pdf", "png", "jpg"], key="ocr_test_up")
        if uploaded_test_file and st.button("▶️ Run OCR Agent", key="btn_run_ocr_test", type="primary"):
            st.info("Executing PyMuPDF text stream & computer vision preprocessing...")
            tmp_path = Path(f"/tmp/test_ocr_{uploaded_test_file.name}")
            with open(tmp_path, "wb") as f:
                f.write(uploaded_test_file.getvalue())
            t0 = time.time()
            res = OCRAgent.process_document("test_doc_01", tmp_path)
            st.success(f"OCR extracted in {time.time()-t0:.2f}s with {int(res['confidence']*100)}% quality!")
            st.json(res)
        st.markdown('</div>', unsafe_allow_html=True)

    # -------------------------------------------------------------
    # AGENT 3: NLP Agent
    # -------------------------------------------------------------
    with tabs[2]:
        render_agent_card(
            agent_name="NLP Agent",
            status="Complete",
            progress=100,
            exec_time=0.35,
            confidence=0.94,
            preview="spaCy NER + Regex pipelines to extract Customer Name, Order ID, ISO Dates, Currencies, Tracking Numbers, and GPS Addresses."
        )
        st.markdown('<div class="fintech-card">', unsafe_allow_html=True)
        st.markdown("#### Test Named Entity Extraction & ISO Normalization")
        sample_text = st.text_area(
            "Input Raw Document Text",
            value=f"TAX INVOICE INV-2024-9981 Billed To: {selected_case['customer_name']} Date: 14/10/2024 Total: INR {selected_case['amount']} Tracking: BLUEDART-88392104"
        )
        if st.button("▶️ Run NLP Entity Extraction", key="btn_run_nlp_test", type="primary"):
            t0 = time.time()
            out = NLPAgent.extract_entities(
                {"raw_text": sample_text, "document_id": "test_nlp_doc", "source_file": "invoice.pdf"},
                known_customer_name=selected_case.get("customer_name"),
                known_order_id=selected_case.get("order_id")
            )
            st.success(f"Extracted {len(out['entities'])} normalized entities in {time.time()-t0:.2f}s!")
            st.json(out)
        st.markdown('</div>', unsafe_allow_html=True)

    # -------------------------------------------------------------
    # AGENT 4: Verification Agent
    # -------------------------------------------------------------
    with tabs[3]:
        render_agent_card(
            agent_name="Verification Agent",
            status="Complete",
            progress=100,
            exec_time=0.28,
            confidence=0.95,
            preview="Cross-document consistency engine that audits Customer Name, Delivery Address, Transaction Amount, Dates, and flags contradictions."
        )
        st.markdown('<div class="fintech-card">', unsafe_allow_html=True)
        st.markdown("#### Cross-Document Consistency & Contradiction Audit")
        if st.button("▶️ Run Verification Engine", key="btn_run_verify_test", type="primary"):
            t0 = time.time()
            docs = service.get_case(selected_case["id"]).get("documents", []) if cases else []
            out = EvidenceConsistencyEngine.verify_case(selected_case, docs, [])
            st.success(f"Audit completed in {time.time()-t0:.2f}s! Overall Consistency: {int(out['overall_confidence']*100)}%")
            st.json(out)
        st.markdown('</div>', unsafe_allow_html=True)

    # -------------------------------------------------------------
    # AGENT 5: ML Scoring Agent
    # -------------------------------------------------------------
    with tabs[4]:
        render_agent_card(
            agent_name="ML Scoring Agent",
            status="Complete",
            progress=100,
            exec_time=0.19,
            confidence=0.92,
            preview="XGBoost model predicting win rate (0-100%), explainable score drivers (+/- points), and Recommended Next Evidence with uplift."
        )
        st.markdown('<div class="fintech-card">', unsafe_allow_html=True)
        st.markdown("#### ML Strength Scoring & Uplift Calculation")
        ml_agent = MLScoringAgent()
        if st.button("▶️ Run ML Risk & Scoring Agent", key="btn_run_ml_test", type="primary"):
            t0 = time.time()
            dummy_ver = {"overall_confidence": 0.95, "contradictions_detected": []}
            out = ml_agent.score_case(selected_case, dummy_ver, doc_count=3)
            st.success(f"Scored in {time.time()-t0:.2f}s! Strength: {out['evidence_strength_score']}/100 | Win Rate: {int(out['win_probability']*100)}%")
            st.json(out)
        st.markdown('</div>', unsafe_allow_html=True)

    # -------------------------------------------------------------
    # AGENT 6: RAG Agent
    # -------------------------------------------------------------
    with tabs[5]:
        render_agent_card(
            agent_name="RAG Agent",
            status="Complete",
            progress=100,
            exec_time=0.30,
            confidence=0.95,
            preview="pgvector 768-dimensional semantic search retrieving winning bank dispute precedents and strategy templates."
        )
        st.markdown('<div class="fintech-card">', unsafe_allow_html=True)
        st.markdown("#### Precedent Retrieval & Semantic Vector Match")
        if st.button("▶️ Run RAG Vector Search", key="btn_run_rag_test", type="primary"):
            t0 = time.time()
            out = RAGAgent.retrieve_similar_cases(selected_case, [], {"overall_confidence": 0.95}, top_k=5)
            st.success(f"Retrieved {len(out['top_k_cases'])} similar winning precedents in {time.time()-t0:.2f}s!")
            st.json(out)
        st.markdown('</div>', unsafe_allow_html=True)

    # -------------------------------------------------------------
    # AGENT 7: Narrative Agent
    # -------------------------------------------------------------
    with tabs[6]:
        render_agent_card(
            agent_name="Narrative Agent",
            status="Complete",
            progress=100,
            exec_time=0.40,
            confidence=0.97,
            preview="LLM legal synthesizer compiling 6-section chronological defense narratives with structured factual grounding."
        )
        st.markdown('<div class="fintech-card">', unsafe_allow_html=True)
        st.markdown("#### Legal Defense Narrative Synthesis")
        if st.button("▶️ Run Legal Narrative Agent", key="btn_run_nar_test", type="primary"):
            t0 = time.time()
            dummy_ver = {"overall_confidence": 0.95, "contradictions_detected": []}
            dummy_score = {"evidence_strength_score": 88, "win_probability": 0.91}
            out = NarrativeAgent.generate_narrative(selected_case, [], [], dummy_ver, dummy_score)
            st.success(f"Narrative synthesized in {time.time()-t0:.2f}s!")
            st.markdown(f"**Executive Overview:** {out['incident_overview']}")
            st.markdown(f"**Chronological Timeline:** {out['timeline_summary']}")
            st.markdown(f"**AI Reasoning:** {out['ai_reasoning']}")
            st.markdown(f"**Recommendation:** {out['final_recommendation']}")
        st.markdown('</div>', unsafe_allow_html=True)
