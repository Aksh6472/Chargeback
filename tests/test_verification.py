"""
Unit Tests for Phase 5: Verification Engine
Includes test fixtures with known deliberate contradictions.
"""

import pytest
from agents.verification_engine import EvidenceConsistencyEngine

def test_name_matching_fuzzy():
    ratio = EvidenceConsistencyEngine.fuzzy_token_sort_ratio("Aarav Sharma", "Sharma Aarav")
    assert ratio >= 0.95

def test_verification_engine_clean_case():
    case_data = {
        "id": "c1",
        "order_id": "ORD-2024-9842",
        "customer_name": "Aarav Sharma",
        "amount": 4299.00,
        "shipping_address": "Bellandur, Bengaluru",
        "tracking_id": "BLUEDART-88392104"
    }
    docs = [{"id": "d1", "file_name": "invoice.pdf", "doc_type": "invoice"}]
    entities = [
        {"entity_type": "customer_name", "raw_value": "Aarav Sharma", "file_name": "invoice.pdf"},
        {"entity_type": "amount", "normalized_value": {"amount": 4299.00}, "file_name": "invoice.pdf"},
        {"entity_type": "date", "normalized_value": {"iso_date": "2024-08-02"}, "file_name": "invoice.pdf"}
    ]

    res = EvidenceConsistencyEngine.verify_case(case_data, docs, entities)
    assert res["overall_confidence"] >= 0.85
    assert len(res["contradictions_detected"]) == 0

def test_verification_engine_deliberate_contradiction():
    # Deliberate amount mismatch fixture
    case_data = {
        "id": "c2",
        "order_id": "ORD-2024-9999",
        "customer_name": "Rohan Verma",
        "amount": 10000.00,
        "shipping_address": "Indiranagar, Bengaluru",
        "tracking_id": "BD-1111"
    }
    docs = [{"id": "d2", "file_name": "receipt.pdf", "doc_type": "receipt"}]
    entities = [
        {"entity_type": "amount", "normalized_value": {"amount": 2500.00}, "file_name": "receipt.pdf"}, # Mismatch: 2500 vs 10000
        {"entity_type": "customer_name", "raw_value": "Different Person", "file_name": "receipt.pdf"}
    ]

    res = EvidenceConsistencyEngine.verify_case(case_data, docs, entities)
    assert len(res["contradictions_detected"]) > 0
    assert res["field_details"]["Amount"]["status"] == "MISMATCH"
