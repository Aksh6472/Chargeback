"""
Generates realistic sample PDF documents for testing:
1. sample_tax_invoice.pdf
2. sample_proof_of_delivery.pdf
3. sample_razorpay_receipt.pdf
"""

from pathlib import Path
from reportlab.lib import colors
from reportlab.lib.pagesizes import letter
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, Table, TableStyle, HRFlowable
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle

OUT_DIR = Path(__file__).resolve().parent / "sample_documents"
OUT_DIR.mkdir(parents=True, exist_ok=True)

styles = getSampleStyleSheet()
title_s = ParagraphStyle('Title', parent=styles['Heading1'], fontName='Helvetica-Bold', fontSize=16, leading=20, textColor=colors.HexColor('#0F172A'))
body_s = ParagraphStyle('Body', parent=styles['Normal'], fontName='Helvetica', fontSize=9, leading=13, textColor=colors.HexColor('#334155'))
bold_s = ParagraphStyle('Bold', parent=styles['Normal'], fontName='Helvetica-Bold', fontSize=9, leading=13, textColor=colors.HexColor('#0F172A'))

# 1. Tax Invoice
doc1 = SimpleDocTemplate(str(OUT_DIR / "sample_tax_invoice.pdf"), pagesize=letter, rightMargin=36, leftMargin=36, topMargin=36, bottomMargin=36)
story1 = [
    Paragraph("TAX INVOICE & RETAIL RECEIPT", title_s),
    Paragraph("Apex Retailers Pvt Ltd &bull; GSTIN: 29AAAAA0000A1Z5 &bull; Bengaluru, Karnataka", body_s),
    HRFlowable(width="100%", thickness=1, color=colors.HexColor('#CBD5E1'), spaceBefore=6, spaceAfter=12),
    Table([
        [Paragraph("<b>Invoice No:</b> INV-2024-9842", body_s), Paragraph("<b>Order ID:</b> ORD-2024-9842", body_s)],
        [Paragraph("<b>Date:</b> 2024-08-02", body_s), Paragraph("<b>Payment:</b> Razorpay Settled", body_s)],
        [Paragraph("<b>Customer Name:</b> Aarav Sharma", body_s), Paragraph("<b>Tracking ID:</b> BLUEDART-88392104", body_s)],
        [Paragraph("<b>Shipping Address:</b> Flat 402, Green Glen Layout, Bellandur, Bengaluru 560103", body_s), Paragraph("<b>Gross Total:</b> INR 4,299.00", bold_s)]
    ], colWidths=[270, 270]),
    Spacer(1, 15),
    Table([
        [Paragraph("<b>Item Description</b>", bold_s), Paragraph("<b>Qty</b>", bold_s), Paragraph("<b>Amount</b>", bold_s)],
        [Paragraph("High-Fidelity Studio Headphones (Model X)", body_s), Paragraph("1", body_s), Paragraph("INR 3,643.22", body_s)],
        [Paragraph("Integrated GST (18%)", body_s), Paragraph("1", body_s), Paragraph("INR 655.78", body_s)],
        [Paragraph("<b>Total Reconciled Amount</b>", bold_s), Paragraph("-", body_s), Paragraph("<b>INR 4,299.00</b>", bold_s)]
    ], colWidths=[340, 60, 140])
]
doc1.build(story1)

# 2. Proof of Delivery
doc2 = SimpleDocTemplate(str(OUT_DIR / "sample_proof_of_delivery.pdf"), pagesize=letter, rightMargin=36, leftMargin=36, topMargin=36, bottomMargin=36)
story2 = [
    Paragraph("BLUEDART EXPRESS - PROOF OF DELIVERY (POD)", title_s),
    Paragraph("Carrier Waybill Docket: BLUEDART-88392104 &bull; Service: Doorstep Priority Air", body_s),
    HRFlowable(width="100%", thickness=1, color=colors.HexColor('#CBD5E1'), spaceBefore=6, spaceAfter=12),
    Table([
        [Paragraph("<b>Consignee:</b> Aarav Sharma", body_s), Paragraph("<b>Dispatch Date:</b> 2024-08-03", body_s)],
        [Paragraph("<b>Delivery Address:</b> Flat 402, Green Glen Layout, Bengaluru 560103", body_s), Paragraph("<b>Delivery Date:</b> 2024-08-06 15:40:00", body_s)],
        [Paragraph("<b>Order Ref:</b> ORD-2024-9842", body_s), Paragraph("<b>Status:</b> DELIVERED - SIGNED", bold_s)],
        [Paragraph("<b>Signee Confirmation:</b> Doorstep Recipient Signature Captured", body_s), Paragraph("<b>Parcel Gross Weight:</b> 1.42 kg", body_s)]
    ], colWidths=[270, 270])
]
doc2.build(story2)

# 3. Razorpay Settlement Receipt
doc3 = SimpleDocTemplate(str(OUT_DIR / "sample_razorpay_receipt.pdf"), pagesize=letter, rightMargin=36, leftMargin=36, topMargin=36, bottomMargin=36)
story3 = [
    Paragraph("RAZORPAY PAYMENT SETTLEMENT RECEIPT", title_s),
    Paragraph("Transaction Capture Authorization &bull; Razorpay ID: pay_RZP8829104", body_s),
    HRFlowable(width="100%", thickness=1, color=colors.HexColor('#CBD5E1'), spaceBefore=6, spaceAfter=12),
    Table([
        [Paragraph("<b>Merchant:</b> Apex Retailers Pvt Ltd", body_s), Paragraph("<b>Order ID:</b> ORD-2024-9842", body_s)],
        [Paragraph("<b>Customer:</b> Aarav Sharma", body_s), Paragraph("<b>Payment Date:</b> 2024-08-02 14:16:12", body_s)],
        [Paragraph("<b>Card Auth:</b> 3D-Secure Authenticated (OTP Verified)", body_s), Paragraph("<b>Amount Settled:</b> INR 4,299.00", bold_s)],
        [Paragraph("<b>Settlement Account:</b> HDFC Bank Acct ending in 4091", body_s), Paragraph("<b>Bank ARN:</b> 882910401928", body_s)]
    ], colWidths=[270, 270])
]
doc3.build(story3)

print("Generated sample PDFs in data/sample_documents/")
