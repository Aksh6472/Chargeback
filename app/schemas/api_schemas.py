"""
Chargeback Evidence AI - Pydantic API Schemas & Data Contracts
Complete data contracts for FastAPI endpoints, agents, and Streamlit UI.
"""

from typing import List, Dict, Any, Optional
from datetime import datetime
from pydantic import BaseModel, Field


# -------------------------------------------------------------
# Auth & KYC Vault Schemas
# -------------------------------------------------------------
class PhoneOtpSendRequest(BaseModel):
    phone: str = Field(..., example="+91 9876543210")

class PhoneOtpSendResponse(BaseModel):
    success: bool
    message: str
    session_id: str
    test_otp: Optional[str] = "742918"  # Convenient demo OTP for test evaluation

class PhoneOtpVerifyRequest(BaseModel):
    phone: str
    otp: str
    session_id: str

class MerchantProfileCreateRequest(BaseModel):
    name: str = Field(..., example="Apex Retailers Pvt Ltd")
    email: str = Field(..., example="finance@apexretail.in")
    phone: str = Field(..., example="+91 9876543210")
    gst_number: str = Field(..., example="29AAAAA0000A1Z5")
    pan_number: str = Field(..., example="ABCDE1234F")
    business_type: str = "E-Commerce / D2C"
    address: str = Field(..., example="42, Indiranagar 100ft Rd, Bengaluru, KA 560038")

class MerchantVaultDocumentResponse(BaseModel):
    id: str
    merchant_id: str
    doc_type: str  # GST, PAN, REGISTRATION, ADDRESS_PROOF
    file_name: str
    verification_status: str  # VERIFIED, PENDING, REJECTED
    uploaded_at: str

class MerchantProfileResponse(BaseModel):
    id: str
    name: str
    email: str
    phone: str
    gst_number: str
    pan_number: str
    business_type: str
    address: str
    vault_documents: List[MerchantVaultDocumentResponse] = []


# -------------------------------------------------------------
# Case Management Schemas
# -------------------------------------------------------------
class CaseCreateRequest(BaseModel):
    merchant_id: Optional[str] = None
    order_id: str = Field(..., example="ORD-2024-9842")
    amount: float = Field(..., example=4299.00)
    currency: str = "INR"
    dispute_reason: str = Field(..., example="Product Not Received")
    customer_name: str = Field(..., example="Aarav Sharma")
    customer_email: Optional[str] = "aarav.sharma@example.com"
    customer_phone: Optional[str] = "+91 9811223344"
    shipping_address: Optional[str] = "Flat 402, Green Glen Layout, Bellandur, Bengaluru, Karnataka 560103"
    tracking_id: Optional[str] = "BLUEDART-88392104"

class DocumentInfo(BaseModel):
    id: str
    case_id: str
    doc_type: str
    file_name: str
    file_path: str
    file_size_bytes: int
    ocr_confidence: float
    page_count: int
    extraction_method: str
    uploaded_at: str

class CaseSummaryResponse(BaseModel):
    id: str
    merchant_id: str
    order_id: str
    status: str
    amount: float
    currency: str
    dispute_reason: str
    customer_name: str
    customer_email: Optional[str]
    opened_at: str
    deadline_at: str
    evidence_score: Optional[float] = None
    win_probability: Optional[float] = None
    document_count: int = 0


# -------------------------------------------------------------
# Agent 1: OCR Agent Schemas (Page 15)
# -------------------------------------------------------------
class OCRPreprocessMeta(BaseModel):
    deskewed: bool = True
    denoised: bool = True
    binarized: bool = True

class OCRAgentOutput(BaseModel):
    document_id: str
    source_file: str
    page_count: int
    raw_text: str
    confidence: float
    preprocessing: OCRPreprocessMeta
    extraction_method: str  # "pymupdf_text_layer" | "tesseract_fallback"
    needs_manual_review: bool = False


# -------------------------------------------------------------
# Agent 2: NLP Agent Schemas (Page 16)
# -------------------------------------------------------------
class ExtractedEntityRecord(BaseModel):
    entity_type: str  # customer_name, order_id, address, date, amount, tracking_id
    raw_value: str
    normalized_value: Any
    confidence: float
    source_doc_type: str

class NLPAgentOutput(BaseModel):
    case_id: str
    document_id: str
    entities: List[ExtractedEntityRecord]
    normalized_dates: List[str] = []
    normalized_amounts: List[float] = []
    normalized_order_id: Optional[str] = None
    normalized_customer_name: Optional[str] = None
    normalized_tracking_id: Optional[str] = None
    normalized_address: Optional[Dict[str, str]] = None


# -------------------------------------------------------------
# Agent 3: Verification Engine Schemas (Page 17)
# -------------------------------------------------------------
class FieldConsistencyDetail(BaseModel):
    field_name: str  # Name, Address, Amount, Dates, Tracking, Invoice
    match_percentage: float  # 0 to 100
    status: str  # MATCH, MINOR_VARIANCE, MISMATCH, MISSING
    explanation: str
    supporting_documents: List[str]
    contradictions: List[str] = []

class VerificationReportOutput(BaseModel):
    case_id: str
    overall_confidence: float  # 0.0 to 1.0
    field_details: Dict[str, FieldConsistencyDetail]
    contradictions_detected: List[str]
    missing_fields: List[str]


# -------------------------------------------------------------
# Agent 4: ML Scoring Agent Schemas (Page 18)
# -------------------------------------------------------------
class MLScoreOutput(BaseModel):
    case_id: str
    evidence_strength_score: int  # 0 - 100
    win_probability: float  # 0.0 to 1.0
    model_version: str = "xgb_v1.0.0"
    metrics_summary: Dict[str, Any] = {
        "precision": 89.6,
        "recall": 89.4,
        "f1_score": 89.5,
        "test_cases": 660
    }
    feature_contributions: Dict[str, float]
    risk_level: str  # "Low Risk", "Moderate", "High Risk"


# -------------------------------------------------------------
# Agent 5: RAG & Similar Case Retrieval Schemas (Page 19)
# -------------------------------------------------------------
class SimilarCaseItem(BaseModel):
    historical_id: str
    order_id: str
    dispute_reason: str
    amount: float
    similarity_percentage: float
    outcome: str  # "WIN" | "LOSE"
    evidence_quality: str
    summary: str
    closed_at: str

class RAGAgentOutput(BaseModel):
    case_id: str
    query_summary: str
    top_k_cases: List[SimilarCaseItem]


# -------------------------------------------------------------
# Agent 6: Fraud Intelligence (NetworkX) Schemas (Page 7)
# -------------------------------------------------------------
class GraphNode(BaseModel):
    id: str
    label: str
    node_type: str  # customer, merchant, address, device, order, ip
    is_suspicious: bool = False

class GraphEdge(BaseModel):
    source: str
    target: str
    relation: str
    weight: float = 1.0

class FraudIntelligenceOutput(BaseModel):
    case_id: str
    fraud_risk_score: int  # 0 - 100
    risk_level: str  # "None", "Low", "Medium", "High"
    suspicious_patterns: List[str]
    nodes: List[GraphNode]
    edges: List[GraphEdge]


# -------------------------------------------------------------
# Agent 7: Gemini Report Agent & Final Evidence Packet (Page 20)
# -------------------------------------------------------------
class TimelineEvent(BaseModel):
    stage: str  # Ordered, Paid, Shipped, Delivered, Customer Contact, Chargeback Filed
    timestamp: str
    document_ref: str
    description: str
    status: str = "completed"

class FinalEvidencePacketOutput(BaseModel):
    case_id: str
    order_id: str
    evidence_strength_score: int
    win_probability: float
    executive_summary: str
    timeline: List[TimelineEvent]
    evidence_list: List[Dict[str, Any]]
    contradictions: List[str]
    missing_evidence: List[str]
    recommendation: str
    pdf_download_url: Optional[str] = None
    created_at: str


# -------------------------------------------------------------
# Full Pipeline Execution Schemas
# -------------------------------------------------------------
class PipelineStepStatus(BaseModel):
    agent_name: str
    status: str  # "queued", "running", "complete", "error"
    progress: int  # 0 - 100
    execution_time_sec: float
    confidence: float
    output_preview: str

class PipelineRunResponse(BaseModel):
    case_id: str
    status: str
    steps: List[PipelineStepStatus]
    evidence_score: int
    win_probability: float
    final_report: Optional[FinalEvidencePacketOutput] = None
