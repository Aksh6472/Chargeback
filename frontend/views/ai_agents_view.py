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
from frontend.components import render_agent_card, render_html


def render_ai_agents_view(service):
    render_html("""
<div style="margin-bottom: 24px;">
    <h2 style="margin: 0; color: #F8FAFC; font-weight: 700; letter-spacing: -0.02em;">🤖 Autonomous 7 AI Agent Center</h2>
    <p style="color: #94A3B8; font-size: 0.88rem; margin-top: 4px;">Inspect, monitor, and execute individual microservice agents independently with full transparency.</p>
</div>
""")

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
        render_html("""
<div class="fintech-card">
    <div class="card-title"><span>Test Document Categorization & Folder Layout</span></div>
</div>
""")
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
        render_html("""
<div class="fintech-card">
    <div class="card-title"><span>Test OCR Preprocessing & Extraction</span></div>
</div>
""")
        uploaded_test_file = st.file_uploader("Upload sample document to extract", type=["pdf", "png", "jpg"], key="ocr_test_up")
        if uploaded_test_file and st.button("▶️ Run OCR Agent", key="btn_run_ocr_test", type="primary"):
            st.info("Executing PyMuPDF text stream & computer vision preprocessing...")
            tmp_path = Path(f"/tmp/test_ocr_{uploaded_test_file.name}")
            with open(tmp_path, "wb") as f:
                f.write(uploaded_test_file.getvalue())
            t0 = time.time()
            ocr_out = OCRAgent.extract_text_and_tables(tmp_path)
            st.success(f"OCR completed in {time.time()-t0:.2f}s with confidence {int(ocr_out.get('confidence', 0.95)*100)}%!")
            st.text_area("Extracted Text Stream", ocr_out.get("text", "")[:1000], height=200)

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
        render_html("""
<div class="fintech-card">
    <div class="card-title"><span>Test NLP Entity Extraction & Normalization</span></div>
</div>
""")
        test_text = st.text_area(
            "Input Document Text Sample",
            "TAX INVOICE INV-8842 Date: 03-08-2024. Billed to Aarav Sharma. Total Amount: INR 14,999.00. BlueDart AWB: BLUEDART-88392104 delivered to Indiranagar, Bengaluru."
        )
        if st.button("▶️ Run NLP Entity Extraction", key="btn_run_nlp_test", type="primary"):
            nlp_agent = NLPAgent()
            entities = nlp_agent.extract_entities(test_text)
            st.success(f"Extracted {len(entities)} named entities successfully!")
            st.dataframe(entities, use_container_width=True)

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
            preview="Cross-document consistency engine: Token-sort name matching, Levenshtein address reconciliation, cent-level amount variance, and timeline sequence validation."
        )
        render_html("""
<div class="fintech-card">
    <div class="card-title"><span>Triangulate Active Case Entities</span></div>
</div>
""")
        if st.button("▶️ Run Verification Triangulation", key="btn_run_ver_test", type="primary"):
            ver_engine = EvidenceConsistencyEngine()
            ver_report = service.get_verification_report(selected_case["id"])
            st.success("Verification Triangulation complete!")
            st.json(ver_report)

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
            preview="XGBoost classifier inference on 9 dispute features. Computes 0-100 Evidence Strength Score, Win Probability, and Next Evidence Uplift."
        )
        render_html("""
<div class="fintech-card">
    <div class="card-title"><span>Evaluate Case Evidence Strength & Uplift</span></div>
</div>
""")
        if st.button("▶️ Calculate ML Score", key="btn_run_ml_test", type="primary"):
            ml_agent = MLScoringAgent()
            ver_rep = service.get_verification_report(selected_case["id"])
            ml_result = ml_agent.score_case(selected_case, ver_rep, doc_count=3)
            st.success(f"Score: {ml_result['evidence_strength_score']}/100 &bull; Win Probability: {int(ml_result['win_probability']*100)}%")
            st.json(ml_result)

    # -------------------------------------------------------------
    # AGENT 6: RAG Agent
    # -------------------------------------------------------------
    with tabs[5]:
        render_agent_card(
            agent_name="RAG Agent",
            status="Complete",
            progress=100,
            exec_time=0.22,
            confidence=0.96,
            preview="Dense semantic search over 768-dimensional pgvector dispute embeddings. Identifies precedent rulings and arbitration win probabilities."
        )
        render_html("""
<div class="fintech-card">
    <div class="card-title"><span>Semantic Precedent Retrieval</span></div>
</div>
""")
        rag_query = st.text_input("Precedent Query", "Product Not Received with carrier proof of delivery")
        if st.button("▶️ Retrieve Precedents", key="btn_run_rag_test", type="primary"):
            rag_agent = RAGAgent()
            precedents = rag_agent.retrieve_similar_cases(rag_query, top_k=3)
            st.success("Found matching historical precedents:")
            for p in precedents:
                render_html(f"""
<div style="background: rgba(255,255,255,0.03); padding: 10px; border-radius: 6px; margin-bottom: 8px;">
    <b>{p.get('case_id', 'Case')}</b> &bull; Outcome: <span style="color: #34D399;">{p.get('outcome', 'Won')}</span> (Similarity: <b>{int(p.get('similarity_score', 0.9)*100)}%</b>)
    <div style="font-size: 0.8rem; color: #94A3B8;">{p.get('summary', '')}</div>
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
            preview="Synthesizes 6-section legal dispute defense narratives: Incident Overview, Timeline, Verified Facts, Contradictions, AI Reasoning, and Final Recommendation."
        )
        render_html("""
<div class="fintech-card">
    <div class="card-title"><span>Synthesize 6-Section Case Narrative</span></div>
</div>
""")
        if st.button("▶️ Generate Defense Narrative", key="btn_run_nar_test", type="primary"):
            ver_rep = service.get_verification_report(selected_case["id"])
            ml_agent = MLScoringAgent()
            ml_score = ml_agent.score_case(selected_case, ver_rep, doc_count=3)
            docs = service.list_case_documents(selected_case["id"])
            nar_out = NarrativeAgent.generate_narrative(selected_case, docs, ver_rep, ml_score)
            st.success("Narrative Synthesized!")
            st.json(nar_out)
