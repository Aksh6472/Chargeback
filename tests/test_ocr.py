"""
Unit Tests for Phase 3: OCR Agent
"""

import pytest
from pathlib import Path
from agents.ocr_agent import OCRAgent

def test_ocr_clean_text():
    raw = "Invoice  #2043\r\nTotal:  INR   4,29O.OO\n\n\nTax: INR 650.00"
    cleaned = OCRAgent.clean_text(raw)
    assert "4,290.00" in cleaned
    assert "\r" not in cleaned

def test_ocr_process_non_existent():
    # OCR on dummy file
    temp_file = Path("data/uploads/test_invoice.txt")
    temp_file.parent.mkdir(parents=True, exist_ok=True)
    temp_file.write_text("Tax Invoice #INV-9842 Total Amount: INR 4299.00 Customer: Aarav Sharma")

    result = OCRAgent.process_document("doc_test_1", temp_file)
    assert result["document_id"] == "doc_test_1"
    assert "confidence" in result
    assert result["preprocessing"]["binarized"] is True
