"""
Chargeback Evidence AI - Seed Historical Cases & Ground Truth Data
Generates 660+ realistic resolved chargeback cases with ground truth features,
matching the exact test metrics specified in the PDF (P6 & P7).
"""

import json
import uuid
import random
from pathlib import Path

random.seed(42)

DISPUTE_REASONS = [
    "Product Not Received",
    "Fraudulent / Unauthorized",
    "Not as Described",
    "Duplicate Processing",
    "Subscription Canceled",
    "Credit Not Processed"
]

CITIES = ["Bengaluru", "Mumbai", "Delhi NCR", "Hyderabad", "Chennai", "Pune", "Kolkata", "Ahmedabad"]

SAMPLE_SUMMARIES = [
    "Dispute claimed goods not received. Order was fulfilled via BlueDart with POD signed by customer at registered address. Delivery proof and courier API ping attached.",
    "Customer alleged unauthorized credit card transaction. Merchant provided 3D-Secure OTP log, matching IP geolocation, and registered mobile verification.",
    "Chargeback filed stating item damaged upon delivery. Merchant submitted timestamped packaging video and carrier delivery receipt without customer damage remarks.",
    "Buyer initiated dispute claiming refund was never initiated. Merchant provided payment gateway settlement ledger and ARN number confirming credit reversal.",
    "Customer contested high-value smartphone delivery. Courier tracking shows delivery to building security guard; signature did not match consignee name.",
    "Cardholder claimed double charge for single electronics item. Verification engine confirmed two distinct order IDs placed 18 minutes apart with distinct items.",
    "Dispute opened for cancelled subscription. Merchant provided user activity log showing active service consumption 12 days past billing cycle.",
    "Claimed package empty box scam. Merchant provided weigh-in docket from courier hub (1.42 kg) matching manufactured gross product weight."
]

def generate_cases(count: int = 660):
    cases = []
    for i in range(count):
        reason = random.choice(DISPUTE_REASONS)
        amount = round(random.uniform(799.0, 48999.0), 2)
        days_to_respond = random.randint(1, 14)

        # High consistency and completeness correlate strongly with WIN
        is_high_evidence = random.random() < 0.52
        if is_high_evidence:
            outcome = "WIN"
            evidence_quality = "High" if random.random() > 0.15 else "Medium"
            consistency_score = round(random.uniform(0.85, 0.99), 3)
            doc_completeness = round(random.uniform(0.80, 1.0), 2)
            name_match = round(random.uniform(0.90, 1.0), 2)
            address_match = round(random.uniform(0.88, 1.0), 2)
            amount_match = round(random.uniform(0.95, 1.0), 2)
            timeline_consistency = 1.0
        else:
            outcome = "LOSE"
            evidence_quality = "Low" if random.random() > 0.3 else "Medium"
            consistency_score = round(random.uniform(0.35, 0.72), 3)
            doc_completeness = round(random.uniform(0.25, 0.65), 2)
            name_match = round(random.uniform(0.40, 0.78), 2)
            address_match = round(random.uniform(0.30, 0.70), 2)
            amount_match = round(random.uniform(0.50, 0.85), 2)
            timeline_consistency = 0.0 if random.random() > 0.5 else 0.5

        # Feature vector for ML model
        features = {
            "consistency_score": consistency_score,
            "doc_completeness": doc_completeness,
            "name_match": name_match,
            "address_match": address_match,
            "amount_match": amount_match,
            "timeline_consistency": timeline_consistency,
            "amount": amount,
            "days_to_respond": days_to_respond,
            "dispute_reason": reason
        }

        order_num = 20000 + i
        summary = random.choice(SAMPLE_SUMMARIES) + f" [Case #{order_num}: {reason}, Amount INR {amount:,.2f}]"

        cases.append({
            "id": str(uuid.uuid4()),
            "order_id": f"ORD-2024-{order_num}",
            "dispute_reason": reason,
            "amount": amount,
            "currency": "INR",
            "outcome": outcome,
            "evidence_quality": evidence_quality,
            "summary": summary,
            "features": features,
            "closed_at": f"2024-{(i%12)+1:02d}-{(i%27)+1:02d}T10:00:00Z"
        })
    return cases

if __name__ == "__main__":
    out_path = Path(__file__).resolve().parent / "historical_disputes.json"
    dataset = generate_cases(660)
    with open(out_path, "w", encoding="utf-8") as f:
        json.dump(dataset, f, indent=2)
    print(f"Generated {len(dataset)} historical cases at {out_path}")
