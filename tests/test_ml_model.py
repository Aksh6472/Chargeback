"""
Unit Tests for Phase 6: ML Scoring Agent (XGBoost)
"""

import pytest
from agents.ml_scoring_agent import MLScoringAgent

def test_ml_scoring():
    agent = MLScoringAgent()
    case_data = {
        "id": "case_test_ml",
        "order_id": "ORD-2024-9842",
        "amount": 4299.00,
        "dispute_reason": "Product Not Received"
    }
    verification_report = {
        "overall_confidence": 0.96,
        "field_details": {
            "Name": {"match_percentage": 98.0},
            "Address": {"match_percentage": 95.0},
            "Amount": {"match_percentage": 100.0},
            "Dates": {"match_percentage": 96.0}
        },
        "contradictions_detected": []
    }

    res = agent.score_case(case_data, verification_report, doc_count=3)
    assert 0 <= res["evidence_strength_score"] <= 100
    assert 0.0 <= res["win_probability"] <= 1.0
    assert res["evidence_strength_score"] >= 80
    assert "precision" in res["metrics_summary"]
    assert res["metrics_summary"]["precision"] == 89.6
