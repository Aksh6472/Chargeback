"""
Chargeback Evidence AI - Dispute Case Management Routes
Endpoints for creating cases, listing disputes, retrieving case details, and uploading documents.
"""

import uuid
import shutil
from pathlib import Path
from typing import List, Optional
from fastapi import APIRouter, UploadFile, File, Form, HTTPException
from app.schemas.api_schemas import CaseCreateRequest, CaseSummaryResponse, DocumentInfo
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
            order_id=c["order_id"],
            status=c.get("status", "investigating"),
            amount=float(c["amount"]),
            currency=c.get("currency", "INR"),
            dispute_reason=c["dispute_reason"],
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
        "merchant_id": merchant["id"],
        "order_id": req.order_id,
        "amount": req.amount,
        "currency": req.currency,
        "dispute_reason": req.dispute_reason,
        "customer_name": req.customer_name,
        "customer_email": req.customer_email,
        "customer_phone": req.customer_phone,
        "shipping_address": req.shipping_address,
        "tracking_id": req.tracking_id,
        "status": "pending"
    }
    created = Repository.create_case(case_data)
    return CaseSummaryResponse(
        id=created["id"],
        merchant_id=created["merchant_id"],
        order_id=created["order_id"],
        status=created["status"],
        amount=float(created["amount"]),
        currency=created["currency"],
        dispute_reason=created["dispute_reason"],
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

@router.post("/{case_id}/upload")
async def upload_document_to_case(
    case_id: str,
    doc_type: str = Form(..., description="invoice, receipt, delivery_proof, tracking_slip, chat_log"),
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
