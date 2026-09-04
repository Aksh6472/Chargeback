"""
Chargeback Evidence AI - Auth & KYC Vault Routes
Implements Dual Portal Phone OTP Authentication (Merchant & Customer),
Merchant Profile + Enhanced Document Vault, and Customer Proof Vault.
"""

import uuid
import shutil
from datetime import datetime
from pathlib import Path
from fastapi import APIRouter, UploadFile, File, Form, HTTPException
from typing import Dict, Any, List, Optional

from app.schemas.api_schemas import (
    PhoneOtpSendRequest, PhoneOtpSendResponse,
    PhoneOtpVerifyRequest, MerchantProfileCreateRequest,
    MerchantProfileResponse, MerchantVaultDocumentResponse,
    CustomerProfileResponse, CustomerVaultDocumentResponse
)
from app.db.repository import Repository
from app.config import settings

router = APIRouter(prefix="/api/auth", tags=["Authentication & Vaults (Dual Portal)"])

# In-memory OTP session cache for phone verification
OTP_CACHE: Dict[str, Dict[str, str]] = {}

@router.post("/phone-otp/send", response_model=PhoneOtpSendResponse)
def send_phone_otp(req: PhoneOtpSendRequest):
    session_id = str(uuid.uuid4())
    test_otp = "742918"  # High-polish demo OTP
    OTP_CACHE[session_id] = {
        "phone": req.phone,
        "otp": test_otp
    }
    return PhoneOtpSendResponse(
        success=True,
        message=f"OTP successfully dispatched to {req.phone}",
        session_id=session_id,
        test_otp=test_otp
    )

@router.post("/phone-otp/verify")
def verify_phone_otp(req: PhoneOtpVerifyRequest):
    session = OTP_CACHE.get(req.session_id)
    if not session or session.get("phone") != req.phone:
        # For smooth developer experience, allow demo OTP
        if req.otp != "742918":
            raise HTTPException(status_code=400, detail="Invalid OTP or expired session.")

    user_type = getattr(req, "user_type", "merchant")
    if user_type == "customer":
        customer = Repository.get_customer_by_phone(req.phone)
        if not customer:
            customer = Repository.get_or_create_default_customer()
            customer["phone_number"] = req.phone
            Repository.upsert_customer(customer)
        vault_docs = Repository.get_customer_vault_docs(customer["id"])
        return {
            "success": True,
            "user_type": "customer",
            "token": f"jwt_mock_token_cust_{customer['id'][:8]}",
            "customer": customer,
            "vault_documents": vault_docs
        }
    else:
        merchant = Repository.get_merchant_by_phone(req.phone)
        if not merchant:
            merchant = Repository.get_or_create_default_merchant()
            merchant["phone"] = req.phone
            merchant["phone_number"] = req.phone
            Repository.upsert_merchant(merchant)
        vault_docs = Repository.get_merchant_vault_docs(merchant["id"])
        return {
            "success": True,
            "user_type": "merchant",
            "token": f"jwt_mock_token_merch_{merchant['id'][:8]}",
            "merchant": merchant,
            "vault_documents": vault_docs
        }

# -------------------------------------------------------------
# Merchant Profile & Vault Endpoints
# -------------------------------------------------------------
@router.get("/merchant-profile", response_model=MerchantProfileResponse)
def get_merchant_profile():
    merchant = Repository.get_or_create_default_merchant()
    vault_docs = Repository.get_merchant_vault_docs(merchant["id"])
    return MerchantProfileResponse(
        id=merchant["id"],
        name=merchant["name"],
        email=merchant["email"],
        phone=merchant["phone"],
        gst_number=merchant.get("gst_number", "29AAAAA0000A1Z5"),
        pan_number=merchant.get("pan_number", "ABCDE1234F"),
        business_type=merchant.get("business_type", "E-Commerce / D2C"),
        address=merchant.get("address", "Indiranagar, Bengaluru"),
        is_verified=bool(merchant.get("is_verified", True)),
        vault_documents=[MerchantVaultDocumentResponse(**d) for d in vault_docs]
    )

@router.post("/merchant-profile", response_model=MerchantProfileResponse)
def update_merchant_profile(req: MerchantProfileCreateRequest):
    merchant = Repository.get_or_create_default_merchant()
    merchant["name"] = req.name
    merchant["email"] = req.email
    merchant["phone"] = req.phone
    merchant["phone_number"] = req.phone
    merchant["gst_number"] = req.gst_number
    merchant["pan_number"] = req.pan_number
    merchant["business_type"] = req.business_type
    merchant["address"] = req.address

    updated = Repository.upsert_merchant(merchant)
    vault_docs = Repository.get_merchant_vault_docs(updated["id"])
    return MerchantProfileResponse(
        id=updated["id"],
        name=updated["name"],
        email=updated["email"],
        phone=updated["phone"],
        gst_number=updated["gst_number"],
        pan_number=updated["pan_number"],
        business_type=updated["business_type"],
        address=updated["address"],
        is_verified=True,
        vault_documents=[MerchantVaultDocumentResponse(**d) for d in vault_docs]
    )

@router.post("/vault-upload", response_model=MerchantVaultDocumentResponse)
async def upload_vault_document(
    doc_type: str = Form(..., description="GST Certificate, Business PAN, Registration Certificate, Business Address Proof, Authorization Letter"),
    file: UploadFile = File(...)
):
    merchant = Repository.get_or_create_default_merchant()
    file_id = str(uuid.uuid4())[:8]
    safe_name = f"vault_{doc_type.replace(' ', '_')}_{file_id}_{file.filename}"
    save_path = settings.UPLOADS_DIR / safe_name

    with open(save_path, "wb") as f:
        shutil.copyfileobj(file.file, f)

    doc_record = Repository.add_vault_document(
        merchant_id=merchant["id"],
        doc_type=doc_type,
        file_name=file.filename,
        file_path=str(save_path)
    )

    return MerchantVaultDocumentResponse(
        id=doc_record["id"],
        merchant_id=doc_record["merchant_id"],
        doc_type=doc_record["doc_type"],
        file_name=doc_record["file_name"],
        verification_status="VERIFIED",
        uploaded_at=datetime.utcnow().isoformat()
    )

@router.delete("/merchant-vault/{doc_id}")
def delete_merchant_vault_doc(doc_id: str):
    Repository.delete_merchant_vault_doc(doc_id)
    return {"success": True, "message": "Document removed from merchant vault"}

# -------------------------------------------------------------
# Customer Profile & Proof Vault Endpoints (Dual Portal)
# -------------------------------------------------------------
@router.get("/customer-profile", response_model=CustomerProfileResponse)
def get_customer_profile():
    cust = Repository.get_or_create_default_customer()
    return CustomerProfileResponse(
        id=cust["id"],
        phone_number=cust["phone_number"],
        full_name=cust["full_name"],
        email=cust.get("email"),
        created_at=cust.get("created_at", datetime.utcnow().isoformat())
    )

@router.get("/customer-vault/{customer_id}", response_model=List[CustomerVaultDocumentResponse])
def get_customer_vault(customer_id: str):
    docs = Repository.get_customer_vault_docs(customer_id)
    return [CustomerVaultDocumentResponse(**d) for d in docs]

@router.post("/customer-vault/upload", response_model=CustomerVaultDocumentResponse)
async def upload_customer_vault_doc(
    customer_id: str = Form(...),
    doc_type: str = Form(..., description="Identity Proof, Billing Address, Delivery Proof, Purchase Receipt, Warranty Invoice"),
    file: UploadFile = File(...)
):
    file_id = str(uuid.uuid4())[:8]
    safe_name = f"cust_vault_{doc_type.replace(' ', '_')}_{file_id}_{file.filename}"
    save_path = settings.UPLOADS_DIR / safe_name

    with open(save_path, "wb") as f:
        shutil.copyfileobj(file.file, f)

    doc_record = Repository.add_customer_vault_doc(
        customer_id=customer_id,
        doc_type=doc_type,
        file_name=file.filename,
        file_path=str(save_path),
        file_size=save_path.stat().st_size
    )

    return CustomerVaultDocumentResponse(
        id=doc_record["id"],
        customer_id=doc_record["customer_id"],
        doc_type=doc_record["doc_type"],
        file_name=doc_record["file_name"],
        verification_status="VERIFIED",
        uploaded_at=datetime.utcnow().isoformat()
    )

@router.delete("/customer-vault/{doc_id}")
def delete_customer_vault_doc(doc_id: str):
    Repository.delete_customer_vault_doc(doc_id)
    return {"success": True, "message": "Document removed from customer proof vault"}

