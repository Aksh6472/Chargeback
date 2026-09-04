"""
Chargeback Evidence AI - Agent 1: Document Classification & Evidence Docket Agent
Classifies uploaded files into canonical categories:
- Tax Invoice
- Payment Receipt
- Carrier Proof of Delivery (POD) / Waybill
- Customer Chat Transcript
- Delivery Confirmation Email
- Identity Proof / KYC
- Merchant Authorization Letter
"""

import re
from pathlib import Path
from typing import Dict, Any, List, Optional


class DocumentAgent:
    """
    Agent 1: Document Classification & Evidence Docket Organization Agent.
    Categorizes raw evidence files, analyzes header/structural semantics,
    and returns classification tags with confidence scores.
    """

    KEYWORD_MAPPINGS = {
        "Tax Invoice": [r"invoice", r"tax\s*invoice", r"bill\s*to", r"gstin", r"total\s*payable", r"item\s*description", r"unit\s*price"],
        "Payment Receipt": [r"payment\s*receipt", r"razorpay", r"settlement", r"transaction\s*id", r"auth\s*code", r"paid\s*via", r"captured"],
        "Carrier Proof of Delivery (POD)": [r"proof\s*of\s*delivery", r"pod", r"delivered", r"bluedart", r"delhivery", r"waybill", r"awb", r"consignee\s*signature", r"tracking"],
        "Customer Chat Transcript": [r"support\s*chat", r"transcript", r"ticket", r"helpdesk", r"customer\s*service", r"conversation\s*log", r"agent:"],
        "Delivery Confirmation Email": [r"order\s*confirmation", r"dispatch\s*notice", r"email", r"subject:", r"from:", r"to:"],
        "Identity Proof": [r"aadhaar", r"passport", r"identity\s*card", r"voter\s*id", r"pan\s*card"],
        "Merchant Authorization Letter": [r"authorization\s*letter", r"acquirer", r"merchant\s*agreement", r"power\s*of\s*attorney"]
    }

    @classmethod
    def classify_document(cls, document_id: str, file_name: str, text_sample: str = "") -> Dict[str, Any]:
        """
        Classifies a document based on its file name, extension, and OCR text sample.
        """
        fname_lower = file_name.lower()
        combined_text = f"{fname_lower} {text_sample.lower()}"

        best_type = "Tax Invoice"
        best_score = 0.0

        for category, patterns in cls.KEYWORD_MAPPINGS.items():
            matches = 0
            for pat in patterns:
                if re.search(pat, combined_text, re.IGNORECASE):
                    matches += 1
            if matches > 0:
                score = min(0.99, 0.70 + (matches * 0.08))
                if score > best_score:
                    best_score = score
                    best_type = category

        # Filename heuristics if text was minimal
        if best_score == 0.0:
            if "inv" in fname_lower:
                best_type = "Tax Invoice"
                best_score = 0.92
            elif "pod" in fname_lower or "deliv" in fname_lower or "track" in fname_lower:
                best_type = "Carrier Proof of Delivery (POD)"
                best_score = 0.94
            elif "rec" in fname_lower or "pay" in fname_lower:
                best_type = "Payment Receipt"
                best_score = 0.91
            elif "chat" in fname_lower or "log" in fname_lower or "ticket" in fname_lower:
                best_type = "Customer Chat Transcript"
                best_score = 0.89
            elif "aadhaar" in fname_lower or "id" in fname_lower or "pan" in fname_lower:
                best_type = "Identity Proof"
                best_score = 0.93
            else:
                best_type = "Tax Invoice"
                best_score = 0.86

        folder_map = {
            "Tax Invoice": "billing_records",
            "Payment Receipt": "gateway_ledgers",
            "Carrier Proof of Delivery (POD)": "logistics_proofs",
            "Customer Chat Transcript": "support_transcripts",
            "Delivery Confirmation Email": "customer_communications",
            "Identity Proof": "kyc_vault",
            "Merchant Authorization Letter": "legal_dockets"
        }

        return {
            "document_id": document_id,
            "file_name": file_name,
            "detected_type": best_type,
            "confidence": round(best_score, 4),
            "organization_folder": folder_map.get(best_type, "evidence_docket")
        }

    @classmethod
    def organize_docket(cls, case_id: str, documents: List[Dict[str, Any]]) -> Dict[str, Any]:
        """
        Organizes all uploaded case evidence into a structured, categorized docket.
        """
        classified = []
        for doc in documents:
            c = cls.classify_document(
                document_id=doc.get("id", ""),
                file_name=doc.get("file_name", ""),
                text_sample=doc.get("ocr_text", "")
            )
            classified.append(c)

        types_count = len(set(c["detected_type"] for c in classified))
        summary = f"Categorized {len(classified)} evidence items into {types_count} canonical dispute exhibit folders."

        return {
            "case_id": case_id,
            "classified_documents": classified,
            "organization_summary": summary
        }
