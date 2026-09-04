"""
Chargeback Evidence AI - Agent REST Endpoints
Individual microservice-ready REST endpoints for every agent:
1. OCR Agent (PyMuPDF + Tesseract)
2. NLP Agent (spaCy + Regex)
3. Verification Engine (Cross-document consistency)
4. ML Scoring Agent (XGBoost Evidence Strength)
5. RAG Agent (pgvector Precedent Retrieval)
6. Gemini Report Agent (Structured synthesis)
Strictly conforms to Page 8, Page 11, and Page 21.
"""

from pathlib import Path
from typing import Dict, Any, List
from fastapi import APIRouter, HTTPException, Body
from pydantic import BaseModel

from agents.ocr_agent import OCRAgent
from agents.nlp_agent import NLPAgent
from agents.verification_engine import EvidenceConsistencyEngine
from agents.ml_scoring_agent import MLScoringAgent
from agents.rag_agent import RAGAgent
from agents.report_agent import GeminiReportAgent
from app.db.repository import Repository

router = APIRouter(prefix="/api/agents", tags=["AI Agents"])

ml_agent = MLScoringAgent()

# -------------------------------------------------------------
# 1. OCR Agent Endpoint
# -------------------------------------------------------------
class OCRRequest(BaseModel):
    document_id: str
    file_path: str

@router.post("/ocr")
def run_ocr_agent(req: OCRRequest):
    p = Path(req.file_path)
    if not p.exists():
        raise HTTPException(status_code=404, detail=f"File not found at path: {req.file_path}")
    result = OCRAgent.process_document(req.document_id, p)
    # Persist in DB
    doc = Repository.get_document_by_id(req.document_id)
    if doc:
        conn = Repository.get_or_create_default_merchant() # ensure initialized
    return result

# -------------------------------------------------------------
# 2. NLP Agent Endpoint
# -------------------------------------------------------------
class NLPRequest(BaseModel):
    ocr_result: Dict[str, Any]
    known_customer_name: str = ""
    known_order_id: str = ""

@router.post("/nlp")
def run_nlp_agent(req: NLPRequest):
    result = NLPAgent.extract_entities(
        req.ocr_result,
        known_customer_name=req.known_customer_name,
        known_order_id=req.known_order_id
    )
    # Save entities if document_id present
    doc_id = req.ocr_result.get("document_id")
    if doc_id and result.get("entities"):
        Repository.save_extracted_entities(doc_id, result["entities"])
    return result

# -------------------------------------------------------------
# 3. Verification Engine Endpoint
# -------------------------------------------------------------
class VerifyRequest(BaseModel):
    case_data: Dict[str, Any]
    documents: List[Dict[str, Any]]
    entities: List[Dict[str, Any]]

@router.post("/verify")
def run_verification_agent(req: VerifyRequest):
    return EvidenceConsistencyEngine.verify_case(req.case_data, req.documents, req.entities)

# -------------------------------------------------------------
# 4. ML Scoring Agent Endpoint
# -------------------------------------------------------------
class MLScoreRequest(BaseModel):
    case_data: Dict[str, Any]
    verification_report: Dict[str, Any]
    doc_count: int = 2

@router.post("/ml-score")
def run_ml_scoring_agent(req: MLScoreRequest):
    res = ml_agent.score_case(req.case_data, req.verification_report, req.doc_count)
    # Persist score
    case_id = req.case_data.get("id")
    if case_id:
        Repository.save_evidence_score({
            "case_id": case_id,
            "score": res["evidence_strength_score"],
            "win_probability": res["win_probability"],
            "model_version": res.get("model_version", "xgb_v1.0.0"),
            "features": res.get("feature_contributions", {}),
            "breakdown": res.get("breakdown", {})
        })
    return res

# -------------------------------------------------------------
# 5. RAG Retrieval Endpoint
# -------------------------------------------------------------
class RAGRequest(BaseModel):
    case_data: Dict[str, Any]
    documents: List[Dict[str, Any]]
    verification_report: Dict[str, Any]
    top_k: int = 5

@router.post("/rag")
def run_rag_agent(req: RAGRequest):
    return RAGAgent.retrieve_similar_cases(
        req.case_data, req.documents, req.verification_report, top_k=req.top_k
    )

# -------------------------------------------------------------
# 6. Gemini Report Agent Endpoint
# -------------------------------------------------------------
class GeminiReportRequest(BaseModel):
    case_data: Dict[str, Any]
    documents: List[Dict[str, Any]]
    entities: List[Dict[str, Any]]
    verification_report: Dict[str, Any]
    ml_score: Dict[str, Any]
    similar_cases: List[Dict[str, Any]]

@router.post("/gemini-report")
def run_gemini_report_agent(req: GeminiReportRequest):
    return GeminiReportAgent.generate_report(
        req.case_data, req.documents, req.entities,
        req.verification_report, req.ml_score, req.similar_cases
    )
