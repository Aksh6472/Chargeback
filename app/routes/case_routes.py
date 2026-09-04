"""
Chargeback Evidence AI - Dispute Case Management Routes
Endpoints for creating cases, listing disputes, retrieving case details, and uploading documents.
"""

import uuid
import shutil
from pathlib import Path
from typing import List, Optional
from fastapi import APIRouter, UploadFile, File, Form, HTTPException, Body
from app.schemas.api_schemas import (
    CaseCreateRequest,
    CaseSummaryResponse,
    CaseStatusUpdateRequest,
    DocumentInfo,
    EvidenceTraceabilityResponse,
    ShareVaultDocRequest
)
from app.db.repository import Repository
from app.config import settings

router = APIRouter(prefix="/api/cases", tags=["Dispute Cases"])

@router.get("", response_model=List[CaseSummaryResponse])
def list_cases():
    merchant = Repository.get_or_create_default_merchant()
    cases = Repository.list_cases_for_merchant(merchant["id"])
    return [
        CaseSummaryResponse(
            id=c["id"],
            merchant_id=c["merchant_id"],
            customer_id=c.get("customer_id"),
            order_id=c["order_id"],
            status=c.get("case_status") or c.get("status", "investigating"),
            case_status=c.get("case_status") or c.get("status", "new"),
            amount=float(c["amount"]),
            currency=c.get("currency", "INR"),
            dispute_reason=c["dispute_reason"],
            dispute_type=c.get("dispute_type", "Product Not Received"),
            customer_name=c.get("customer_name", "N/A"),
            customer_email=c.get("customer_email"),
            opened_at=c.get("opened_at", ""),
            deadline_at=c.get("deadline_at", ""),
            evidence_score=c.get("evidence_score"),
            win_probability=c.get("win_probability"),
            document_count=c.get("document_count", 0)
        )
        for c in cases
    ]

@router.get("/customer/{customer_id}", response_model=List[CaseSummaryResponse])
def list_cases_for_customer(customer_id: str):
    cases = Repository.list_cases_for_customer(customer_id)
    return [
        CaseSummaryResponse(
            id=c["id"],
            merchant_id=c["merchant_id"],
            customer_id=c.get("customer_id"),
            order_id=c["order_id"],
            status=c.get("case_status") or c.get("status", "investigating"),
            case_status=c.get("case_status") or c.get("status", "new"),
            amount=float(c["amount"]),
            currency=c.get("currency", "INR"),
            dispute_reason=c["dispute_reason"],
            dispute_type=c.get("dispute_type", "Product Not Received"),
            customer_name=c.get("customer_name", "N/A"),
            customer_email=c.get("customer_email"),
            opened_at=c.get("opened_at", ""),
            deadline_at=c.get("deadline_at", ""),
            evidence_score=c.get("evidence_score"),
            win_probability=c.get("win_probability"),
            document_count=c.get("document_count", 0)
        )
        for c in cases
    ]

@router.post("", response_model=CaseSummaryResponse)
def create_case(req: CaseCreateRequest):
    merchant = Repository.get_or_create_default_merchant()
    case_data = {
        "id": str(uuid.uuid4()),
        "merchant_id": req.merchant_id or merchant["id"],
        "customer_id": req.customer_id,
        "order_id": req.order_id,
        "amount": req.amount,
        "currency": req.currency,
        "dispute_reason": req.dispute_reason,
        "dispute_type": req.dispute_type or "Product Not Received",
        "customer_name": req.customer_name,
        "customer_email": req.customer_email,
        "customer_phone": req.customer_phone,
        "shipping_address": req.shipping_address,
        "tracking_id": req.tracking_id,
        "status": "new",
        "case_status": "new"
    }
    created = Repository.create_case(case_data)
    return CaseSummaryResponse(
        id=created["id"],
        merchant_id=created["merchant_id"],
        customer_id=created.get("customer_id"),
        order_id=created["order_id"],
        status=created["status"],
        case_status=created.get("case_status", "new"),
        amount=float(created["amount"]),
        currency=created["currency"],
        dispute_reason=created["dispute_reason"],
        dispute_type=created.get("dispute_type", "Product Not Received"),
        customer_name=created["customer_name"],
        customer_email=created.get("customer_email"),
        opened_at=created.get("opened_at", ""),
        deadline_at=created.get("deadline_at", ""),
        evidence_score=None,
        win_probability=None,
        document_count=0
    )

@router.get("/{case_id}")
def get_case(case_id: str):
    c = Repository.get_case_by_id(case_id)
    if not c:
        raise HTTPException(status_code=404, detail="Case not found")
    docs = Repository.list_documents_for_case(case_id)
    c["documents"] = docs
    return c

@router.patch("/{case_id}/status")
def update_case_status(case_id: str, req: CaseStatusUpdateRequest):
    valid_statuses = ["new", "investigating", "evidence_ready", "submitted", "won", "lost"]
    if req.status.lower() not in valid_statuses:
        raise HTTPException(status_code=400, detail=f"Invalid status. Must be one of {valid_statuses}")
    
    updated = Repository.update_case_status(case_id, req.status.lower())
    if not updated:
        raise HTTPException(status_code=404, detail="Case not found")
    return {"success": True, "case_id": case_id, "status": req.status.lower()}

@router.get("/{case_id}/traceability/{entity_type}")
def get_entity_traceability(case_id: str, entity_type: str):
    trace = Repository.get_entity_traceability(case_id, entity_type)
    if not trace:
        raise HTTPException(status_code=404, detail=f"No traceability metadata for entity '{entity_type}'")
    return trace

@router.post("/{case_id}/share-vault-doc")
def share_vault_doc(case_id: str, req: ShareVaultDocRequest):
    case = Repository.get_case_by_id(case_id)
    if not case:
        raise HTTPException(status_code=404, detail="Case not found")
    
    doc = Repository.share_customer_vault_doc_to_case(req.vault_doc_id, case_id)
    if not doc:
        raise HTTPException(status_code=404, detail="Vault document not found")
    return {"success": True, "document": doc}

@router.post("/{case_id}/upload")
async def upload_document_to_case(
    case_id: str,
    doc_type: str = Form(..., description="invoice, receipt, delivery_proof, tracking_slip, chat_log"),
    owner_type: str = Form("merchant"),
    document_category: str = Form("evidence"),
    file: UploadFile = File(...)
):
    c = Repository.get_case_by_id(case_id)
    if not c:
        raise HTTPException(status_code=404, detail="Case not found")

    file_id = str(uuid.uuid4())[:8]
    safe_name = f"{case_id[:6]}_{doc_type}_{file_id}_{file.filename}"
    save_path = settings.UPLOADS_DIR / safe_name

    with open(save_path, "wb") as f:
        shutil.copyfileobj(file.file, f)

    doc_record = Repository.add_document({
        "case_id": case_id,
        "owner_type": owner_type,
        "document_category": document_category,
        "doc_type": doc_type,
        "file_name": file.filename,
        "file_path": str(save_path),
        "file_size_bytes": save_path.stat().st_size,
        "mime_type": file.content_type or "application/pdf"
    })

    return doc_record

@router.get("/{case_id}/documents")
def list_case_documents(case_id: str):
    return Repository.list_documents_for_case(case_id)
