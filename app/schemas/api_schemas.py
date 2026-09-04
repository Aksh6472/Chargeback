"""
Chargeback Evidence AI - Pydantic API Schemas & Data Contracts
Complete data contracts for FastAPI endpoints, agents, dual portal, and Streamlit UI.
"""

from typing import List, Dict, Any, Optional
from datetime import datetime
from pydantic import BaseModel, Field


# -------------------------------------------------------------
# Auth & KYC Vault Schemas (Merchant & Customer Dual Portal)
# -------------------------------------------------------------
class PhoneOtpSendRequest(BaseModel):
    phone: str = Field(...)

class PhoneOtpSendResponse(BaseModel):
    success: bool
    message: str
    session_id: str
    test_otp: Optional[str] = "742918"  # Convenient demo OTP for instant evaluation

class PhoneOtpVerifyRequest(BaseModel):
    phone: str
    otp: str
    session_id: str
    user_type: str = "merchant"  # "merchant" or "customer"

class MerchantProfileCreateRequest(BaseModel):
    name: str = Field(...)
    email: str = Field(...)
    phone: str = Field(...)
    gst_number: str = "29AAAAA0000A1Z5"
    pan_number: str = "ABCDE1234F"
    business_type: str = "E-Commerce / D2C"
    address: str = "42, Indiranagar 100ft Rd, Bengaluru, KA 560038"

class MerchantVaultDocumentResponse(BaseModel):
    id: str
    merchant_id: str
    doc_type: str  # GST Certificate, Business PAN, Registration Certificate, Business Address Proof, Authorization Letter
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
    is_verified: bool = True
    vault_documents: List[MerchantVaultDocumentResponse] = []

class CustomerProfileResponse(BaseModel):
    id: str
    phone_number: str
    full_name: str
    email: Optional[str] = None
    created_at: str

class CustomerVaultDocumentResponse(BaseModel):
    id: str
    customer_id: str
    doc_type: str  # Identity Proof, Billing Address, Delivery Proof, Purchase Receipt, Warranty Invoice
    file_name: str
    verification_status: str = "VERIFIED"
    uploaded_at: str

class ShareVaultDocRequest(BaseModel):
    case_id: str
    vault_doc_id: str


# -------------------------------------------------------------
# Case Management & Lifecycle Schemas
# -------------------------------------------------------------
class CaseCreateRequest(BaseModel):
    merchant_id: Optional[str] = None
    customer_id: Optional[str] = None
    order_id: str = Field(...)
    amount: float = Field(...)
    currency: str = "INR"
    dispute_reason: str = Field(...)
    dispute_type: Optional[str] = "Product Not Received"
    customer_name: str = Field(...)
    customer_email: Optional[str] = "aarav.sharma@example.com"
    customer_phone: Optional[str] = "+91 9811223344"
    shipping_address: Optional[str] = "Flat 402, Green Glen Layout, Bellandur, Bengaluru, Karnataka 560103"
    tracking_id: Optional[str] = "BLUEDART-88392104"

class DocumentInfo(BaseModel):
    id: str
    case_id: str
    owner_type: str = "merchant"
    document_category: str = "evidence"
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
    customer_id: Optional[str] = None
    order_id: str
    status: str  # new, investigating, evidence_ready, submitted, won, lost
    case_status: str = "new"
    amount: float
    currency: str
    dispute_reason: str
    dispute_type: str = "Product Not Received"
    customer_name: str
    customer_email: Optional[str] = None
    opened_at: str
    deadline_at: str
    evidence_score: Optional[float] = None
    win_probability: Optional[float] = None
    document_count: int = 0

class CaseStatusUpdateRequest(BaseModel):
    case_id: str
    status: str  # new, investigating, evidence_ready, submitted, won, lost


# -------------------------------------------------------------
# Agent 1: Document Agent Schemas
# -------------------------------------------------------------
class DocumentClassificationResult(BaseModel):
    document_id: str
    file_name: str
    detected_type: str  # Invoice, Receipt, Chat, Courier, Email, Identity Proof, Authorization Letter
    confidence: float
    organization_folder: str

class DocumentAgentOutput(BaseModel):
    case_id: str
    classified_documents: List[DocumentClassificationResult]
    organization_summary: str


# -------------------------------------------------------------
# Agent 2: OCR Agent Schemas
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
    has_tables: bool = False
    preprocessing: OCRPreprocessMeta
    extraction_method: str  # "pymupdf_text_layer" | "tesseract_fallback"
    needs_manual_review: bool = False


# -------------------------------------------------------------
# Agent 3: NLP Agent Schemas
# -------------------------------------------------------------
class ExtractedEntityRecord(BaseModel):
    entity_type: str  # customer_name, merchant_name, order_id, address, date, amount, tracking_id
    raw_value: str
    normalized_value: Any
    confidence: float
    source_page: int = 1
    source_doc_type: str

class NLPAgentOutput(BaseModel):
    case_id: str
    document_id: str
    entities: List[ExtractedEntityRecord]
    entity_confidences: Dict[str, float] = {}
    normalized_dates: List[str] = []
    normalized_amounts: List[float] = []
    normalized_order_id: Optional[str] = None
    normalized_customer_name: Optional[str] = None
    normalized_merchant_name: Optional[str] = None
    normalized_tracking_id: Optional[str] = None
    normalized_address: Optional[Dict[str, str]] = None


# -------------------------------------------------------------
# Agent 4: Verification Agent Schemas
# -------------------------------------------------------------
class FieldConsistencyDetail(BaseModel):
    field_name: str  # Name, Address, Amount, Dates, Tracking, Order ID, Invoice
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
# Agent 5: ML Risk Agent & Next Evidence Recommendation Schemas
# -------------------------------------------------------------
class ScoreComponent(BaseModel):
    name: str
    points: int
    is_positive: bool
    explanation: str

class RecommendedNextEvidence(BaseModel):
    recommended_document: str  # e.g. "Courier Proof of Delivery (POD)"
    win_probability_uplift_pct: int  # e.g. 14 (+14%)
    reason: str
    suggested_alternative: str  # e.g. "Customer Delivery Confirmation Email"

class MLScoreOutput(BaseModel):
    case_id: str
    evidence_strength_score: int  # 0 - 100
    score_label: str = "Moderate Strength"  # Strong, Moderate Strength, Weak
    win_probability: float  # 0.0 to 1.0
    dispute_classification: str  # Product Not Received, Fraudulent Transaction, Duplicate Transaction, Unauthorized Payment, Service Not Delivered, Product Defective
    model_version: str = "xgb_v1.0.0"
    score_breakdown: List[ScoreComponent] = []
    recommended_next_evidence: RecommendedNextEvidence
    risk_level: str  # "Low Risk", "Moderate", "High Risk"
    how_to_improve: List[str] = []
    feature_contributions: Dict[str, float] = {}


# -------------------------------------------------------------
# Agent 6: RAG Intelligence Agent Schemas
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
    supporting_evidence: List[str] = []
    closed_at: str

class RAGAgentOutput(BaseModel):
    case_id: str
    query_summary: str
    top_k_cases: List[SimilarCaseItem]


# -------------------------------------------------------------
# Agent 7: Narrative Agent & Case Narrative Schemas
# -------------------------------------------------------------
class AICaseNarrativeOutput(BaseModel):
    case_id: str
    order_id: str
    incident_overview: str
    timeline_summary: str
    verified_facts: List[Dict[str, str]]
    contradictions_audit: str
    ai_reasoning: str
    final_recommendation: str


# -------------------------------------------------------------
# Evidence Source Traceability Schemas
# -------------------------------------------------------------
class EvidenceTraceabilityResponse(BaseModel):
    source_file: str
    page_number: int = 1
    extracted_text: str
    ocr_confidence: float
    entity_confidence: float
    verified: bool = True


# -------------------------------------------------------------
# AI Evidence Chat Schemas
# -------------------------------------------------------------
class EvidenceCitation(BaseModel):
    source_file: str
    page_number: int
    snippet: str
    confidence: float

class AIChatRequest(BaseModel):
    case_id: str
    question: str

class AIChatResponse(BaseModel):
    case_id: str
    question: str
    answer: str
    citations: List[EvidenceCitation] = []


# -------------------------------------------------------------
# Interactive PDF Preview & Report Schemas
# -------------------------------------------------------------
class PDFReportEditRequest(BaseModel):
    case_id: str
    report_title: Optional[str] = "Chargeback Defense Packet"
    executive_summary: Optional[str] = None
    merchant_notes: Optional[str] = None
    digital_signature_name: Optional[str] = "Apex Retail Operations"
    include_narrative: bool = True

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
    dispute_classification: str = "Product Not Received"
    executive_summary: str
    case_narrative: Optional[AICaseNarrativeOutput] = None
    timeline: List[TimelineEvent]
    evidence_list: List[Dict[str, Any]]
    contradictions: List[str]
    missing_evidence: List[str]
    recommended_next_evidence: Optional[RecommendedNextEvidence] = None
    recommendation: str
    pdf_file_path: Optional[str] = None
    pdf_download_url: Optional[str] = None
    created_at: str


# -------------------------------------------------------------
# Pipeline Step & Full Run Schemas (10-Step Investigation Timeline)
# -------------------------------------------------------------
class PipelineStepStatus(BaseModel):
    step_number: int
    agent_name: str
    step_title: str
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
    dispute_classification: str = "Product Not Received"
    final_report: Optional[FinalEvidencePacketOutput] = None

