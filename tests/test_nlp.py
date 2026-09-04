"""
Unit Tests for Phase 4: NLP Agent
"""

import pytest
from agents.nlp_agent import NLPAgent

def test_date_normalization():
    assert NLPAgent.normalize_date("02/08/2024") == "2024-08-02"
    assert NLPAgent.normalize_date("2024-08-02") == "2024-08-02"
    assert NLPAgent.normalize_date("02 Aug 2024") == "2024-08-02"

def test_amount_normalization():
    assert NLPAgent.normalize_amount("INR 4,299.00") == 4299.00
    assert NLPAgent.normalize_amount("₹ 12,500.50") == 12500.50
    assert NLPAgent.normalize_amount("4299") == 4299.00

def test_nlp_entity_extraction():
    ocr_sample = {
        "document_id": "doc_test_10",
        "raw_text": (
            "TAX INVOICE\n"
            "Order ID: ORD-2024-9842\n"
            "Customer: Aarav Sharma\n"
            "Deliver to: Flat 402, Green Glen Layout, Bengaluru 560103\n"
            "Date: 02 Aug 2024\n"
            "Total Amount: INR 4,299.00\n"
            "Tracking: BLUEDART-88392104"
        ),
        "source_file": "tax_invoice.pdf"
    }

    res = NLPAgent.extract_entities(ocr_sample, known_customer_name="Aarav Sharma", known_order_id="ORD-2024-9842")
    assert res["normalized_order_id"] == "ORD-2024-9842"
    assert res["normalized_customer_name"] == "Aarav Sharma"
    assert 4299.00 in res["normalized_amounts"]
    assert "2024-08-02" in res["normalized_dates"]
    assert res["normalized_tracking_id"] == "88392104"
    assert res["normalized_address"]["postal_code"] == "560103"
