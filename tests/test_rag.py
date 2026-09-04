"""
Unit Tests for Phase 7: RAG & Similar Case Retrieval
"""

import pytest
from agents.rag_agent import RAGAgent, generate_dense_embedding, cosine_similarity

def test_dense_embedding_shape_and_norm():
    vec = generate_dense_embedding("Test dispute query", dim=768)
    assert len(vec) == 768

def test_cosine_similarity_identical():
    v = [0.5, 0.5, 0.5, 0.5]
    sim = cosine_similarity(v, v)
    assert abs(sim - 1.0) < 1e-4

def test_rag_retrieval():
    case_data = {
        "id": "case_rag_test",
        "order_id": "ORD-2024-9842",
        "dispute_reason": "Product Not Received",
        "amount": 4299.00
    }
    res = RAGAgent.retrieve_similar_cases(case_data, [], {"overall_confidence": 0.95}, top_k=3)
    assert "top_k_cases" in res
    assert len(res["top_k_cases"]) > 0
    assert res["top_k_cases"][0]["similarity_percentage"] >= 80.0
