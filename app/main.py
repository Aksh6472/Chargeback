"""
Chargeback Evidence AI - FastAPI Gateway
Phase 0: Architecture & Service Skeletons (PDF Reference: Page 8, Page 11, Page 24).
"""

import json
from pathlib import Path
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles

from app.config import settings
from app.routes import auth_router, case_router, agent_router, fraud_router, pipeline_router
from app.db.repository import Repository

app = FastAPI(
    title=settings.APP_NAME,
    version=settings.APP_VERSION,
    description="Multi-agent dispute intelligence backend with OCR, NLP, verification, XGBoost scoring, RAG, and Gemini report generation.",
    docs_url="/docs",
    redoc_url="/redoc"
)

# Enable CORS for Streamlit and external webhooks (n8n)
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Mount Routers
app.include_router(auth_router)
app.include_router(case_router)
app.include_router(agent_router)
app.include_router(fraud_router)
app.include_router(pipeline_router)

@app.on_event("startup")
def startup_event():
    """Seed initial records and verify directory health."""
    settings.DATA_DIR.mkdir(parents=True, exist_ok=True)
    settings.UPLOADS_DIR.mkdir(parents=True, exist_ok=True)
    settings.REPORTS_DIR.mkdir(parents=True, exist_ok=True)
    settings.MODELS_DIR.mkdir(parents=True, exist_ok=True)

    print(f"[*] Initializing {settings.APP_NAME} v{settings.APP_VERSION}...")
    merchant = Repository.get_or_create_default_merchant()
    print(f"[*] Verified default merchant: {merchant['name']} ({merchant['id']})")

    # Check if historical cases need to be seeded
    seed_file = settings.DATA_DIR / "historical_disputes.json"
    if seed_file.exists():
        with open(seed_file, "r", encoding="utf-8") as f:
            cases = json.load(f)
            Repository.seed_historical_cases(cases)
            print(f"[*] Verified historical cases database: {len(cases)} disputes available.")

    # Seed initial demo dispute case if none exists
    existing_cases = Repository.list_cases_for_merchant(merchant["id"])
    if not existing_cases:
        seed_case = {
            "merchant_id": merchant["id"],
            "order_id": "ORD-2024-9842",
            "amount": 4299.00,
            "currency": "INR",
            "dispute_reason": "Product Not Received",
            "customer_name": "Aarav Sharma",
            "customer_email": "aarav.sharma@example.com",
            "customer_phone": "+91 9811223344",
            "shipping_address": "Flat 402, Green Glen Layout, Bellandur, Bengaluru, Karnataka 560103",
            "tracking_id": "BLUEDART-88392104",
            "status": "investigating"
        }
        created = Repository.create_case(seed_case)

        # Seed realistic dispute documents
        docs_to_seed = [
            ("invoice", "tax_invoice_ord9842.pdf", 4299.00),
            ("delivery_proof", "signed_pod_bluedart.pdf", 4299.00),
            ("receipt", "razorpay_payment_receipt.pdf", 4299.00),
            ("chat_log", "support_chat_transcript.pdf", 0.0)
        ]
        for dtype, fname, amt in docs_to_seed:
            file_p = settings.UPLOADS_DIR / fname
            if not file_p.exists():
                # Write placeholder text content
                file_p.write_text(f"Document {fname} for Order {created['order_id']}, Amount INR {amt}\nCustomer: {created['customer_name']}\nCarrier Tracking: BLUEDART-88392104\nAddress: {created['shipping_address']}")

            Repository.add_document({
                "case_id": created["id"],
                "doc_type": dtype,
                "file_name": fname,
                "file_path": str(file_p),
                "file_size_bytes": 1024 * 45,
                "ocr_confidence": 0.97,
                "ocr_text": f"Invoice and Delivery Proof for Order {created['order_id']}, Amount: INR {amt:,.2f}, Consignee: {created['customer_name']}, Address: {created['shipping_address']}"
            })
        print(f"[*] Seeded initial demo case: {created['order_id']} with 4 evidence documents.")

@app.get("/health", tags=["Health"])
def health_check():
    """Health check route for orchestration and deployment monitoring."""
    return {
        "status": "healthy",
        "app": settings.APP_NAME,
        "version": settings.APP_VERSION,
        "environment": settings.ENVIRONMENT,
        "models_loaded": {
            "xgboost": settings.XGB_MODEL_PATH.exists(),
            "gemini_api": settings.GEMINI_API_KEY != "demo_key_placeholder"
        }
    }
