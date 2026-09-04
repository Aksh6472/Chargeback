"""
Chargeback Evidence AI - Fraud Intelligence Routes
Provides NetworkX graph relationship analysis across customer, merchant, address, devices, and orders.
"""

from fastapi import APIRouter, HTTPException
from app.db.repository import Repository
from agents.fraud_intelligence import FraudIntelligenceAgent

router = APIRouter(prefix="/api/fraud", tags=["Fraud Intelligence"])

@router.get("/graph/{case_id}")
def get_fraud_graph_for_case(case_id: str):
    c = Repository.get_case_by_id(case_id)
    if not c:
        raise HTTPException(status_code=404, detail="Case not found")

    graph_data = FraudIntelligenceAgent.build_fraud_graph(c)
    return graph_data
