"""
Test suite validating recent repair and polish features:
1. NarrativeAgent compatibility (no 'list' object has no attribute 'get')
2. ReportAgent custom fields in PDF generation
3. DisputeService.preview_report & approve_case
4. Merchant & Customer profile persistence
"""

import os
from pathlib import Path
from frontend.api_client import DisputeService
from app.db.repository import Repository
from agents.narrative_agent import NarrativeAgent
from agents.report_agent import GeminiReportAgent


def test_narrative_agent_call_compatibility():
    """Verify NarrativeAgent handles both 4-argument and 5-argument calls safely."""
    cases = DisputeService.list_cases()
    assert len(cases) > 0
    case = cases[0]
    docs = Repository.list_documents_for_case(case["id"])
    ents = Repository.get_entities_for_case(case["id"])
    ver = {"overall_confidence": 0.95, "contradictions_detected": []}
    score = {"evidence_strength_score": 92, "win_probability": 0.92}

    # 5-argument call: (case, docs, ents, ver, score)
    nar5 = NarrativeAgent.generate_narrative(case, docs, ents, ver, score)
    assert isinstance(nar5, dict)
    assert "incident_overview" in nar5

    # 4-argument call: (case, docs, ver, score)
    nar4 = NarrativeAgent.generate_narrative(case, docs, ver, score)
    assert isinstance(nar4, dict)
    assert "incident_overview" in nar4


def test_preview_report_custom_fields_and_approval():
    """Verify preview_report compiles PDF with custom fields, and approve_case updates status."""
    cases = DisputeService.list_cases()
    assert len(cases) > 0
    case_id = cases[0]["id"]

    custom_title = "FORMAL MERCHANT ARBITRATION REBUTTAL"
    notes = "Custom merchant verification statement: physical POD attached."
    sig = "Test Signatory Officer"
    summary = "Cardholder placed order and accepted delivery with signature."

    rep = DisputeService.preview_report(
        case_id=case_id,
        report_title=custom_title,
        merchant_notes=notes,
        signature_name=sig,
        executive_summary=summary
    )

    assert rep["report_title"] == custom_title
    assert rep["merchant_notes"] == notes
    assert rep["digital_signature"]["signer_name"] == sig
    assert rep["executive_summary"] == summary

    pdf_path = rep.get("pdf_file_path")
    assert pdf_path is not None
    assert os.path.exists(pdf_path)
    assert os.path.getsize(pdf_path) > 1000

    # Test approve_case
    res = DisputeService.approve_case(case_id)
    assert res["success"] is True
    assert res["status"] == "submitted"

    # Verify in DB
    updated_case = Repository.get_case_by_id(case_id)
    assert updated_case["status"] == "submitted"
    assert updated_case["case_status"] == "submitted"


def test_merchant_and_customer_settings_persistence():
    """Verify settings update persists to database and returns updated records."""
    # Merchant
    m = DisputeService.get_merchant_profile()
    original_name = m.get("name", "Apex Retailers")
    new_name = "Apex Global Retail Enterprises"
    m_update = dict(m)
    m_update["name"] = new_name
    m_update["gst_number"] = "07AAAAA1234A1Z9"

    saved_m = DisputeService.update_merchant_profile(m_update)
    assert saved_m["name"] == new_name
    assert saved_m["gst_number"] == "07AAAAA1234A1Z9"

    # Restore
    m_update["name"] = original_name
    DisputeService.update_merchant_profile(m_update)

    # Customer
    customers = DisputeService.list_all_customers()
    if customers:
        cust = customers[0]
        c_update = dict(cust)
        c_update["full_name"] = "Aarav K. Sharma"
        c_update["address"] = "DLF Phase 5, Gurugram, India"

        saved_c = DisputeService.update_customer_profile(c_update)
        assert saved_c["full_name"] == "Aarav K. Sharma"
        assert saved_c["address"] == "DLF Phase 5, Gurugram, India"
