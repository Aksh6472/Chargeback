"""
Tests for upgraded AI Chargeback Operating System Agents and Vault features.
"""

import pytest
from agents.document_agent import DocumentAgent
from agents.narrative_agent import NarrativeAgent
from agents.chat_agent import AIEvidenceChatAgent, ChatAgent
from agents.ml_scoring_agent import MLScoringAgent
from app.db.repository import Repository
from app.db.database import get_db_connection


def test_document_agent_classification():
    docs = [
        {"id": "doc-1", "file_name": "tax_invoice_ord9842.pdf", "ocr_text": "TAX INVOICE GSTIN TOTAL INR 4299"},
        {"id": "doc-2", "file_name": "bluedart_pod.pdf", "ocr_text": "DELIVERY RUN SHEET SIGNED BY RECIPIENT AARAV SHARMA"},
        {"id": "doc-3", "file_name": "support_chat.pdf", "ocr_text": "Customer Support Ticket Conversation Log"}
    ]
    organized = DocumentAgent.organize_docket("CASE-TEST-001", docs)
    assert organized["case_id"] == "CASE-TEST-001"
    assert len(organized["classified_documents"]) == 3
    doc_types = [d["detected_type"] for d in organized["classified_documents"]]
    assert "Tax Invoice" in doc_types
    assert "Carrier Proof of Delivery (POD)" in doc_types
    assert "Customer Chat Transcript" in doc_types


def test_ml_scoring_breakdown_and_uplift():
    agent = MLScoringAgent()
    case_data = {
        "order_id": "ORD-2024-9842",
        "customer_name": "Aarav Sharma",
        "amount": 4299.00,
        "dispute_reason": "Product Not Received"
    }
    verification_report = {
        "overall_confidence": 0.94,
        "field_details": {
            "Name": {"match_percentage": 95},
            "Address": {"match_percentage": 90},
            "Amount": {"match_percentage": 100},
            "Dates": {"match_percentage": 92}
        },
        "contradictions_detected": []
    }
    result = agent.score_case(case_data, verification_report, doc_count=3)
    assert "evidence_score" in result
    assert result["evidence_score"] >= 80
    assert "score_breakdown" in result
    assert "recommended_evidence" in result
    assert result["recommended_evidence"]["win_probability_uplift_pct"] >= 5


def test_narrative_agent_generation():
    case_data = {
        "order_id": "ORD-TEST-001",
        "customer_name": "John Doe",
        "amount": 5000.0,
        "currency": "INR",
        "dispute_reason": "Product Not Received",
        "evidence_score": 90,
        "tracking_id": "BLUEDART-12345",
        "created_at": "2024-08-01T10:00:00"
    }
    docs = [{"file_name": "invoice.pdf", "doc_type": "Tax Invoice", "ocr_text": "Invoice ORD-TEST-001"}]
    verification_report = {"overall_confidence": 0.95, "contradictions_detected": []}
    ml_score = {"evidence_score": 92, "win_probability": 0.92}

    narrative = NarrativeAgent.generate_narrative(case_data, docs, verification_report, ml_score)
    assert "incident_overview" in narrative
    assert "timeline_summary" in narrative
    assert "verified_facts" in narrative
    assert "contradictions_audit" in narrative
    assert "ai_reasoning" in narrative
    assert "final_recommendation" in narrative


def test_ai_chat_agent():
    # Insert or query with mock case
    res = AIEvidenceChatAgent.answer_query("CASE-2024-001", "What is the order amount?")
    assert "case_id" in res
    assert "answer" in res
    assert "4,299.00" in res["answer"] or "INR" in res["answer"] or "amount" in res["answer"].lower()


def test_customer_vault_repository():
    # Test customer creation & vault persistence
    customer_data = {
        "id": "CUST-TEST-999",
        "full_name": "Priya Patel",
        "email": "priya.test@example.com",
        "phone_number": "+91 9988776655"
    }
    Repository.upsert_customer(customer_data)
    customer = Repository.get_customer_by_phone("+91 9988776655")
    assert customer is not None
    assert customer["full_name"] == "Priya Patel"

    # Add vault doc
    doc_data = {
        "customer_id": "CUST-TEST-999",
        "category": "Customer ID Proof",
        "file_name": "aadhaar_mask.pdf",
        "file_path": "/uploads/aadhaar_mask.pdf",
        "file_size": 204800,
        "mime_type": "application/pdf"
    }
    new_doc = Repository.add_customer_vault_doc(doc_data)
    assert new_doc is not None
    assert new_doc["doc_type"] == "Customer ID Proof"

    # List vault docs
    vault_docs = Repository.get_customer_vault_docs("CUST-TEST-999")
    assert len(vault_docs) >= 1

    # Cleanup
    Repository.delete_customer_vault_doc(new_doc["id"], "CUST-TEST-999")
