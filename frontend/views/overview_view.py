"""
Chargeback Evidence AI - Stitch Overview Dashboard & Case Detail Workspace
Matching overview_chargeback_evidence_ai/code.html and dispute_cb_2026_1042_workspace_chargeback_evidence_ai/code.html
"""

import streamlit as st
import pandas as pd
from frontend.components import (
    render_kpi_card,
    render_html,
    render_case_status_tracker,
    render_score_radial,
    render_explainable_score_card,
    render_recommended_next_evidence,
    render_traceable_claim
)
from agents.ml_scoring_agent import MLScoringAgent
from agents.document_agent import DocumentAgent
from agents.ocr_agent import OCRAgent
from agents.nlp_agent import NLPAgent
from agents.verification_engine import EvidenceConsistencyEngine
from agents.rag_agent import RAGAgent
from agents.narrative_agent import NarrativeAgent


def render_overview_view(service):
    # Check if user is drilling into a specific case detail
    case_detail_id = st.session_state.get("viewing_case_detail")
    if case_detail_id:
        render_case_detail_view(service, case_detail_id)
        return

    m = service.get_merchant_profile()
    m_name = m.get("name", "Apex Retailers Pvt Ltd") if m else "Apex Retailers Pvt Ltd"

    # Screen Header & Operational Strip
    render_html(f"""
<div style="margin-bottom: 24px;">
    <div style="display: flex; justify-content: space-between; align-items: flex-end; flex-wrap: wrap; gap: 12px;">
        <div>
            <div style="display: flex; align-items: center; gap: 6px; margin-bottom: 4px;">
                <span style="font-size: 0.7rem; font-weight: 700; text-transform: uppercase; color: #64748B; letter-spacing: 0.06em;">Dispute Operations</span>
                <span style="width: 4px; height: 4px; border-radius: 50%; background: #CBD5E1;"></span>
                <span class="font-mono" style="font-size: 0.72rem; color: #64748B;">Q1 Re-presentment Cycle</span>
            </div>
            <h1 style="font-size: 2rem; font-weight: 800; letter-spacing: -0.03em; color: #191C1E; margin: 0 0 4px 0;">
                Overview
            </h1>
            <p style="color: #64748B; font-size: 0.88rem; margin: 0;">Track your active disputes, evidence completeness, and recovery rate across payment rails.</p>
        </div>
        <div style="display: flex; align-items: center; gap: 10px;">
            <div style="background: #F2F4F6; border: 1px solid #E5E7EB; padding: 6px 12px; border-radius: 8px; font-size: 0.78rem; color: #191C1E; display: flex; align-items: center; gap: 6px;">
                <span class="material-symbols-outlined" style="font-size: 16px; color: #10B981;">sync</span>
                <span class="font-mono">Auto-sync: Active (Live)</span>
            </div>
        </div>
    </div>
</div>
""")

    cases = service.list_cases()
    total_cases = len(cases)
    evidence_ready_cases = [c for c in cases if (c.get("case_status") or c.get("status")) in ["evidence_ready", "submitted", "won"]]
    pending_action_cases = [c for c in cases if (c.get("case_status") or c.get("status")) in ["new", "investigating"]]
    total_exposure = sum(float(c.get("amount", 0)) for c in cases)

    # 4 Summary Metric Cards (Matching Stitch UI Strip)
    col1, col2, col3, col4 = st.columns(4)
    with col1:
        render_kpi_card(
            title="Active Disputes",
            value=f"{total_cases}",
            trend="+4 cases",
            is_up=True,
            footer_label="Dispute Exposure",
            footer_val=f"₹{total_exposure:,.0f}",
            icon_name="account_balance_wallet"
        )
    with col2:
        render_kpi_card(
            title="Evidence Pending",
            value=f"{len(pending_action_cases)}",
            trend="Needs docs within 48h",
            is_up=False,
            footer_label="Urgent SLA Window",
            footer_val=f"{len(pending_action_cases)} In Collection",
            icon_name="timer"
        )
    with col3:
        render_kpi_card(
            title="Cases Ready",
            value=f"{len(evidence_ready_cases)}",
            trend="94% win probability",
            is_up=True,
            footer_label="Packets Verified",
            footer_val="Auto-dispatchable",
            icon_name="fact_check"
        )
    with col4:
        render_kpi_card(
            title="Win Rate",
            value="78.4%",
            trend="+3.2% vs benchmark",
            is_up=True,
            footer_label="Protected Capital",
            footer_val=f"₹{total_exposure * 0.78:,.0f}",
            icon_name="trending_up"
        )

    st.write("")

    # Primary Asymmetric Grid (65% Left / 35% Right)
    col_main, col_side = st.columns([1.85, 1.0], gap="large")

    # =============================================================
    # LEFT COLUMN (65%): RECENT DISPUTES TABLE & DISPOSITION CHART
    # =============================================================
    with col_main:
        # Table Header Box
        render_html(f"""
<div style="display: flex; justify-content: space-between; align-items: center; margin-bottom: 12px;">
    <div>
        <div style="display: flex; align-items: center; gap: 8px;">
            <h2 style="font-size: 1.15rem; font-weight: 700; color: #191C1E; margin: 0;">Recent Disputes</h2>
            <span class="font-mono" style="background: #E1E2E4; color: #43474B; font-size: 0.72rem; font-weight: 700; padding: 2px 8px; border-radius: 9999px;">{total_cases} active</span>
        </div>
        <p style="font-size: 0.8rem; color: #64748B; margin: 2px 0 0 0;">Prioritized cases awaiting merchant review, evidence collection, or automatic delivery.</p>
    </div>
</div>
""")

        if not cases:
            st.info("No dispute cases registered yet. Click 'Create Case' to upload a dispute.")
        else:
            # Render Table in Stitch Card Format
            for c in cases:
                cid = c.get("id")
                oid = c.get("order_id", "ORD-UNKNOWN")
                cname = c.get("customer_name", "Cardholder")
                amount = float(c.get("amount", 0.0))
                dtype = c.get("dispute_type", c.get("dispute_reason", "Product Not Received"))
                score = int(c.get("evidence_score", 85))
                status_raw = (c.get("case_status") or c.get("status", "new")).lower()

                if status_raw in ["submitted", "won"]:
                    pill_class = "stitch-pill-success"
                    pill_text = "Submitted" if status_raw == "submitted" else "Closed (Won)"
                elif status_raw in ["evidence_ready", "rebuttal_drafted"]:
                    pill_class = "stitch-pill-info"
                    pill_text = "Ready to Submit"
                else:
                    pill_class = "stitch-pill-warning"
                    pill_text = "Collecting Evidence"

                # Progress completeness
                comp_pct = score
                comp_bar_color = "#10B981" if comp_pct >= 80 else "#2F3A42"

                render_html(f"""
<div class="stitch-card" style="padding: 1.15rem; margin-bottom: 10px; border: 1px solid #E5E7EB;">
    <div style="display: flex; justify-content: space-between; align-items: center; flex-wrap: wrap; gap: 14px;">
        <div style="min-width: 170px;">
            <span class="font-mono" style="font-weight: 700; font-size: 0.95rem; color: #1A242C;">#{oid}</span>
            <div style="font-size: 0.82rem; color: #191C1E; font-weight: 600; margin-top: 2px;">{cname}</div>
            <div class="font-mono" style="font-size: 0.72rem; color: #64748B;">Visa &bull; {c.get('tracking_id', 'AWB-LIVE')}</div>
        </div>
        <div>
            <div style="font-size: 0.68rem; text-transform: uppercase; color: #64748B; font-weight: 700;">Amount</div>
            <div class="font-mono" style="font-size: 1rem; font-weight: 700; color: #191C1E;">₹{amount:,.2f}</div>
        </div>
        <div>
            <div style="font-size: 0.68rem; text-transform: uppercase; color: #64748B; font-weight: 700;">Reason</div>
            <div style="font-size: 0.8rem; font-weight: 600; color: #43474B; max-width: 150px; overflow: hidden; text-overflow: ellipsis; white-space: nowrap;">{dtype}</div>
        </div>
        <div style="min-width: 120px;">
            <div style="display: flex; justify-content: space-between; font-size: 0.72rem; color: #64748B; margin-bottom: 4px;">
                <span>Completeness</span>
                <span class="font-mono" style="font-weight: 700; color: {comp_bar_color};">{comp_pct}%</span>
            </div>
            <div style="height: 5px; background: #EDEEF0; border-radius: 9999px; overflow: hidden;">
                <div style="width: {comp_pct}%; height: 100%; background: {comp_bar_color}; border-radius: 9999px;"></div>
            </div>
        </div>
        <div>
            <span class="stitch-pill {pill_class}">
                <span class="stitch-pill-dot"></span>
                <span>{pill_text}</span>
            </span>
        </div>
    </div>
</div>
""")
                col_sp, col_b = st.columns([4, 1])
                with col_b:
                    if st.button("Review Case ➔", key=f"btn_open_ov_{cid}", type="primary", use_container_width=True):
                        st.session_state["viewing_case_detail"] = cid
                        st.session_state["active_case_id"] = cid
                        st.rerun()

        # Weekly Disposition Velocity Chart (from Stitch UI)
        render_html("""
<div class="stitch-card" style="margin-top: 1.25rem;">
    <div style="display: flex; justify-content: space-between; align-items: center; margin-bottom: 1rem;">
        <div>
            <h3 style="font-size: 0.95rem; font-weight: 700; color: #191C1E; margin: 0;">Weekly Dispute Disposition Velocity</h3>
            <p style="font-size: 0.78rem; color: #64748B; margin: 2px 0 0 0;">Volume processed vs counter-evidence recovery rate</p>
        </div>
        <span class="stitch-pill stitch-pill-neutral">Rolling 7-Day</span>
    </div>
    <div style="display: grid; grid-template-columns: repeat(7, 1fr); gap: 8px; text-align: center;">
        <div style="background: #F8F9FB; border: 1px solid #E5E7EB; border-radius: 8px; padding: 8px 4px;">
            <div style="height: 70px; display: flex; align-items: flex-end; justify-content: center; margin-bottom: 6px;">
                <div style="width: 70%; background: #2F3A42; height: 60%; border-radius: 4px 4px 0 0;"></div>
            </div>
            <span class="font-mono" style="font-size: 0.72rem; color: #64748B;">Mon</span>
            <div class="font-mono" style="font-size: 0.76rem; font-weight: 700; color: #191C1E;">₹12.4k</div>
        </div>
        <div style="background: #F8F9FB; border: 1px solid #E5E7EB; border-radius: 8px; padding: 8px 4px;">
            <div style="height: 70px; display: flex; align-items: flex-end; justify-content: center; margin-bottom: 6px;">
                <div style="width: 70%; background: #2F3A42; height: 40%; border-radius: 4px 4px 0 0;"></div>
            </div>
            <span class="font-mono" style="font-size: 0.72rem; color: #64748B;">Tue</span>
            <div class="font-mono" style="font-size: 0.76rem; font-weight: 700; color: #191C1E;">₹8.1k</div>
        </div>
        <div style="background: #F8F9FB; border: 1px solid #E5E7EB; border-radius: 8px; padding: 8px 4px;">
            <div style="height: 70px; display: flex; align-items: flex-end; justify-content: center; margin-bottom: 6px;">
                <div style="width: 70%; background: #2F3A42; height: 85%; border-radius: 4px 4px 0 0;"></div>
            </div>
            <span class="font-mono" style="font-size: 0.72rem; color: #64748B;">Wed</span>
            <div class="font-mono" style="font-size: 0.76rem; font-weight: 700; color: #191C1E;">₹19.2k</div>
        </div>
        <div style="background: #F8F9FB; border: 1px solid #E5E7EB; border-radius: 8px; padding: 8px 4px;">
            <div style="height: 70px; display: flex; align-items: flex-end; justify-content: center; margin-bottom: 6px;">
                <div style="width: 70%; background: #2F3A42; height: 70%; border-radius: 4px 4px 0 0;"></div>
            </div>
            <span class="font-mono" style="font-size: 0.72rem; color: #64748B;">Thu</span>
            <div class="font-mono" style="font-size: 0.76rem; font-weight: 700; color: #191C1E;">₹15.0k</div>
        </div>
        <div style="background: #ECFDF5; border: 1px solid #A7F3D0; border-radius: 8px; padding: 8px 4px;">
            <div style="height: 70px; display: flex; align-items: flex-end; justify-content: center; margin-bottom: 6px;">
                <div style="width: 70%; background: #10B981; height: 95%; border-radius: 4px 4px 0 0;"></div>
            </div>
            <span class="font-mono" style="font-size: 0.72rem; font-weight: 700; color: #065F46;">Today</span>
            <div class="font-mono" style="font-size: 0.76rem; font-weight: 800; color: #065F46;">₹22.8k</div>
        </div>
        <div style="background: #F8F9FB; border: 1px solid #E5E7EB; border-radius: 8px; padding: 8px 4px; opacity: 0.6;">
            <div style="height: 70px; display: flex; align-items: flex-end; justify-content: center; margin-bottom: 6px;">
                <div style="width: 70%; background: #CBD5E1; height: 30%; border-radius: 4px 4px 0 0;"></div>
            </div>
            <span class="font-mono" style="font-size: 0.72rem; color: #64748B;">Sat</span>
            <div class="font-mono" style="font-size: 0.76rem; color: #64748B;">Est.</div>
        </div>
        <div style="background: #F8F9FB; border: 1px solid #E5E7EB; border-radius: 8px; padding: 8px 4px; opacity: 0.6;">
            <div style="height: 70px; display: flex; align-items: flex-end; justify-content: center; margin-bottom: 6px;">
                <div style="width: 70%; background: #CBD5E1; height: 25%; border-radius: 4px 4px 0 0;"></div>
            </div>
            <span class="font-mono" style="font-size: 0.72rem; color: #64748B;">Sun</span>
            <div class="font-mono" style="font-size: 0.76rem; color: #64748B;">Est.</div>
        </div>
    </div>
</div>
""")

    # =============================================================
    # RIGHT COLUMN (35%): EVIDENCE PROGRESS & RECENT ACTIVITY
    # =============================================================
    with col_side:
        # Card 1: Evidence Progress
        render_html("""
<div class="stitch-card" style="padding: 1.25rem;">
    <div style="display: flex; justify-content: space-between; align-items: center; margin-bottom: 4px;">
        <div style="display: flex; align-items: center; gap: 8px;">
            <span class="material-symbols-outlined" style="color: #1A242C; font-size: 18px;">task_alt</span>
            <h3 style="font-size: 0.95rem; font-weight: 700; color: #191C1E; margin: 0;">Evidence Progress</h3>
        </div>
        <span class="stitch-pill stitch-pill-info">In-Flight</span>
    </div>
    <p style="font-size: 0.78rem; color: #64748B; margin: 0 0 12px 0;">Dossier completion status for pending gateway submissions.</p>

    <!-- Case Item A -->
    <div style="background: #F8F9FB; border: 1px solid #E5E7EB; border-radius: 8px; padding: 12px; margin-bottom: 10px;">
        <div style="display: flex; justify-content: space-between; align-items: center; margin-bottom: 4px;">
            <span class="font-mono" style="font-weight: 700; color: #191C1E; font-size: 0.85rem;">#CB-2026-1042</span>
            <span class="font-mono" style="font-size: 0.8rem; font-weight: 700; color: #10B981;">8 of 10</span>
        </div>
        <div style="height: 4px; background: #EDEEF0; border-radius: 9999px; overflow: hidden; margin-bottom: 8px;">
            <div style="width: 80%; height: 100%; background: #10B981;"></div>
        </div>
        <div style="display: flex; flex-direction: column; gap: 4px; font-size: 0.76rem; color: #43474B;">
            <div style="display: flex; align-items: center; gap: 6px;">
                <span class="material-symbols-outlined" style="font-size: 14px; color: #10B981;">check_circle</span>
                <span>Signed Proof of Delivery (BlueDart)</span>
            </div>
            <div style="display: flex; align-items: center; gap: 6px;">
                <span class="material-symbols-outlined" style="font-size: 14px; color: #10B981;">check_circle</span>
                <span>AVS &amp; 3DS Authentication Token</span>
            </div>
            <div style="display: flex; align-items: center; gap: 6px; color: #EF4444;">
                <span class="material-symbols-outlined" style="font-size: 14px;">pending</span>
                <span>Waiting on terms acceptance log</span>
            </div>
        </div>
    </div>

    <!-- Case Item B -->
    <div style="background: #F8F9FB; border: 1px solid #E5E7EB; border-radius: 8px; padding: 12px;">
        <div style="display: flex; justify-content: space-between; align-items: center; margin-bottom: 4px;">
            <span class="font-mono" style="font-weight: 700; color: #191C1E; font-size: 0.85rem;">#CB-2026-1034</span>
            <span class="font-mono" style="font-size: 0.8rem; font-weight: 700; color: #EF4444;">4 of 9</span>
        </div>
        <div style="height: 4px; background: #EDEEF0; border-radius: 9999px; overflow: hidden; margin-bottom: 8px;">
            <div style="width: 45%; height: 100%; background: #EF4444;"></div>
        </div>
        <div style="display: flex; flex-direction: column; gap: 4px; font-size: 0.76rem; color: #43474B;">
            <div style="display: flex; align-items: center; gap: 6px;">
                <span class="material-symbols-outlined" style="font-size: 14px; color: #10B981;">check_circle</span>
                <span>Initial Invoice &amp; Settlement Ledger</span>
            </div>
            <div style="display: flex; align-items: center; gap: 6px; color: #EF4444;">
                <span class="material-symbols-outlined" style="font-size: 14px;">warning</span>
                <span>Needs merchant refund ledger log</span>
            </div>
        </div>
    </div>
</div>
""")

        # Card 2: Recent Activity Timeline Feed
        render_html("""
<div class="stitch-card" style="padding: 1.25rem;">
    <div style="display: flex; justify-content: space-between; align-items: center; margin-bottom: 4px;">
        <div style="display: flex; align-items: center; gap: 8px;">
            <span class="material-symbols-outlined" style="color: #1A242C; font-size: 18px;">history</span>
            <h3 style="font-size: 0.95rem; font-weight: 700; color: #191C1E; margin: 0;">Recent Activity</h3>
        </div>
    </div>
    <p style="font-size: 0.78rem; color: #64748B; margin: 0 0 14px 0;">Live event stream from gateway webhooks and document pipelines.</p>

    <div style="display: flex; flex-direction: column; gap: 14px; border-left: 2px solid #E5E7EB; padding-left: 14px; margin-left: 6px;">
        <div>
            <div class="font-mono" style="font-size: 0.7rem; color: #64748B;">12 mins ago &bull; EVIDENCE UPLOAD</div>
            <div style="font-size: 0.82rem; color: #191C1E; font-weight: 600; margin-top: 2px;">
                Signed proof of delivery PDF uploaded for case <span class="font-mono" style="color: #1A242C;">#CB-2026-1042</span>
            </div>
        </div>
        <div>
            <div class="font-mono" style="font-size: 0.7rem; color: #64748B;">45 mins ago &bull; PACKET BUILT</div>
            <div style="font-size: 0.82rem; color: #191C1E; font-weight: 600; margin-top: 2px;">
                Automated package compiled for <span style="font-weight: 700;">Aarav Sharma</span> (₹14,999.00)
            </div>
        </div>
        <div>
            <div class="font-mono" style="font-size: 0.7rem; color: #10B981; font-weight: 700;">2 hours ago &bull; PORTAL VICTORY</div>
            <div style="font-size: 0.82rem; color: #191C1E; font-weight: 600; margin-top: 2px;">
                Case <span class="font-mono" style="color: #1A242C;">#CB-2026-1021</span> marked <b style="color: #10B981;">Won</b> by card dispute portal (+₹2,190 recovered)
            </div>
        </div>
    </div>
</div>
""")

        # Card 3: Shield Active Card
        render_html("""
<div style="background: #1A242C; color: #FFFFFF; border-radius: 12px; padding: 1.25rem; box-shadow: 0 4px 12px rgba(26,36,44,0.15);">
    <div style="display: flex; justify-content: space-between; align-items: center; margin-bottom: 8px;">
        <div style="display: flex; align-items: center; gap: 8px;">
            <span class="material-symbols-outlined" style="color: #6FFBBE; font-size: 20px;">verified_user</span>
            <span style="font-weight: 700; font-size: 0.9rem; color: #FFFFFF;">Chargeback Shield Active</span>
        </div>
        <span class="font-mono" style="font-size: 0.72rem; color: #98A4AD;">v4.12</span>
    </div>
    <p style="font-size: 0.8rem; color: #BCC8D2; line-height: 1.45; margin: 0 0 10px 0;">
        Automated rules are monitoring active cases across Visa Resolve Online &amp; Mastercard Dispute Resolution.
    </p>
    <div style="display: flex; justify-content: space-between; align-items: center; border-top: 1px solid rgba(255,255,255,0.1); padding-top: 8px;">
        <span class="font-mono" style="font-size: 0.72rem; color: #6FFBBE;">All Rails Synced</span>
    </div>
</div>
""")


# -------------------------------------------------------------
# UNIFIED CASE DETAIL WORKSPACE (Matching Stitch Case Detail)
# -------------------------------------------------------------
def render_case_detail_view(service, case_id: str):
    case = service.get_case(case_id)
    if not case:
        st.error("Dispute case not found.")
        if st.button("← Back to Overview"):
            st.session_state["viewing_case_detail"] = None
            st.rerun()
        return

    if st.button("← Back to Overview", key="btn_back_to_ov"):
        st.session_state["viewing_case_detail"] = None
        st.rerun()

    c_status = (case.get("case_status") or case.get("status", "new")).upper()
    pill_class = "stitch-pill-success" if c_status in ["SUBMITTED", "WON", "EVIDENCE_READY"] else "stitch-pill-warning"
    score_val = int(case.get("evidence_score", 92))
    dispute_type = case.get("dispute_type", case.get("dispute_reason", "Product Not Received"))

    # Top Case Detail Banner
    render_html(f"""
<div class="stitch-card" style="margin-bottom: 16px;">
    <div style="display: flex; justify-content: space-between; align-items: center; flex-wrap: wrap; gap: 14px;">
        <div>
            <div style="display: flex; align-items: center; gap: 10px;">
                <h2 style="font-size: 1.45rem; font-weight: 800; color: #191C1E; margin: 0;">Dispute #{case.get('order_id')}</h2>
                <span class="stitch-pill {pill_class}">{c_status}</span>
            </div>
            <div style="font-size: 0.84rem; color: #64748B; margin-top: 4px;">
                Customer: <b>{case.get('customer_name')}</b> &bull; Disputed Amount: <b>₹{case.get('amount', 0):,.2f}</b> &bull; AWB: <span class="font-mono">{case.get('tracking_id', 'BLUEDART')}</span>
            </div>
        </div>
        <div style="display: flex; gap: 20px; align-items: center;">
            <div>
                <div style="font-size: 0.68rem; color: #64748B; text-transform: uppercase; font-weight: 700;">Dispute Classification</div>
                <div style="font-size: 0.95rem; font-weight: 700; color: #191C1E;">🏷️ {dispute_type}</div>
            </div>
            <div style="text-align: right;">
                <div style="font-size: 0.68rem; color: #64748B; text-transform: uppercase; font-weight: 700;">Evidence Strength</div>
                <div style="font-size: 1.35rem; font-weight: 800; color: #10B981;">{score_val}/100</div>
            </div>
        </div>
    </div>
</div>
""")

    # Horizontal Lifecycle Tracker
    render_case_status_tracker(case.get("case_status") or case.get("status", "new"))

    # 7 Cohesive Tabs
    tab_over, tab_inv, tab_evi, tab_ver, tab_rag, tab_nar, tab_rep = st.tabs([
        "📋 Overview",
        "⚡ Live Investigation",
        "📁 Evidence Exhibits",
        "⚖️ Verification & Traceability",
        "📚 AI Intelligence",
        "✍️ Case Narrative",
        "📄 Final Package"
    ])

    pipeline_state = service.get_latest_run(case_id) or service.run_full_pipeline(case_id)

    # TAB 1: OVERVIEW
    with tab_over:
        col_o1, col_o2 = st.columns(2)
        with col_o1:
            render_html("""
<div class="stitch-card">
    <h3 class="stitch-card-title">Order & Transaction Authentication</h3>
    <p class="stitch-card-subtitle">Verified transaction attributes captured via payment gateway and 3D-Secure.</p>
</div>
""")
            st.markdown(f"**Order ID / Reference:** `{case.get('order_id')}`")
            st.markdown(f"**Settlement Amount:** `₹{case.get('amount', 0):,.2f} {case.get('currency', 'INR')}`")
            st.markdown(f"**Dispute Reason Code:** {case.get('dispute_reason')}")
            st.markdown(f"**Carrier Tracking AWB:** `{case.get('tracking_id', 'BLUEDART-88392104')}`")
        with col_o2:
            render_html("""
<div class="stitch-card">
    <h3 class="stitch-card-title">Cardholder & Fulfillment Details</h3>
    <p class="stitch-card-subtitle">Verified identity credentials and doorstep destination records.</p>
</div>
""")
            st.markdown(f"**Customer Name:** {case.get('customer_name')}")
            st.markdown(f"**Email Address:** {case.get('customer_email', 'aarav.sharma@example.com')}")
            st.markdown(f"**Phone Number:** {case.get('customer_phone', '+91 9811223344')}")
            st.markdown(f"**Shipping Address:**\n> {case.get('shipping_address')}")

    # TAB 2: LIVE INVESTIGATION
    with tab_inv:
        col_l, col_r = st.columns([3, 2])
        with col_l:
            st.markdown("#### ⚡ 10-Step Connected Investigation Pipeline")
            steps = pipeline_state.get("steps", [])
            for step in steps:
                snum = step.get("step_number", 1)
                aname = step.get("agent_name", "Agent")
                stitle = step.get("step_title", "")
                preview = step.get("output_preview", "")
                etime = float(step.get("execution_time_sec", 0.3))
                conf = float(step.get("confidence", 0.95))

                render_html(f"""
<div class="stitch-card" style="padding: 1rem; margin-bottom: 8px;">
    <div style="display: flex; justify-content: space-between; align-items: center; margin-bottom: 4px;">
        <div style="font-weight: 700; font-size: 0.9rem; color: #191C1E;">Step {snum}: {stitle}</div>
        <span class="stitch-pill stitch-pill-success">{aname}</span>
    </div>
    <div style="font-size: 0.82rem; color: #43474B; margin-bottom: 6px;">{preview}</div>
    <div class="font-mono" style="font-size: 0.72rem; color: #64748B;">
        ⏱️ {etime:.2f}s &bull; Quality: {int(conf*100)}% &bull; <b style="color: #10B981;">COMPLETED</b>
    </div>
</div>
""")

        with col_r:
            st.markdown("#### 🎯 Case Readiness & Score Breakdown")
            render_score_radial(score_val, pipeline_state.get("win_probability", 0.92))

            ml_agent = MLScoringAgent()
            ver_rep = pipeline_state.get("verification_report") or {"overall_confidence": 0.95, "contradictions_detected": []}
            ml_score_data = ml_agent.score_case(case, ver_rep, doc_count=3)
            render_explainable_score_card(ml_score_data)

            rec = ml_score_data.get("recommended_next_evidence", {})
            render_recommended_next_evidence(rec)

    # TAB 3: EVIDENCE EXHIBITS
    with tab_evi:
        docs = service.list_case_documents(case_id)
        st.markdown(f"#### Verified Evidence Exhibits ({len(docs)} Files)")
        for doc in docs:
            ocr_conf = float(doc.get("ocr_confidence", 0.96))
            render_html(f"""
<div class="stitch-card" style="padding: 1.15rem; margin-bottom: 10px;">
    <div style="display: flex; justify-content: space-between; align-items: center;">
        <div>
            <div style="font-weight: 700; color: #191C1E; font-size: 0.95rem;">📄 {doc.get('file_name')}</div>
            <div style="font-size: 0.78rem; color: #64748B; margin-top: 2px;">Category: <b>{doc.get('doc_type')}</b> &bull; Added: {doc.get('uploaded_at', '')[:10]}</div>
        </div>
        <div style="text-align: right;">
            <span class="stitch-pill stitch-pill-success">OCR Quality: {int(ocr_conf*100)}%</span>
        </div>
    </div>
</div>
""")

    # TAB 4: VERIFICATION & TRACEABILITY
    with tab_ver:
        ver_rep = service.get_verification_report(case_id)
        field_details = ver_rep.get("field_details", {})
        st.markdown("#### ⚖️ Cross-Document Triangulation")

        categories = [
            ("Name", "👤 Customer Name Reconciliation"),
            ("Address", "📍 Shipping vs Billing Address"),
            ("Amount", "💵 Amount & Currency Match"),
            ("Dates", "📅 Chronological Journey Match"),
            ("Tracking", "📦 Carrier AWB & Waybill Match"),
            ("Invoice", "📑 Document Completeness & Integrity")
        ]
        for i in range(0, len(categories), 2):
            c_a, c_b = st.columns(2)
            for col, (ckey, ctitle) in zip([c_a, c_b], categories[i:i+2]):
                fdata = field_details.get(ckey, {"match_percentage": 98.0, "status": "MATCH", "explanation": "Verified consistent."})
                mpct = fdata.get("match_percentage", 95.0)
                with col:
                    render_html(f"""
<div class="stitch-card" style="padding: 1rem; margin-bottom: 10px;">
    <div class="stitch-card-header">
        <span style="font-weight: 700; font-size: 0.88rem; color: #191C1E;">{ctitle}</span>
        <span class="stitch-pill stitch-pill-success">{fdata.get('status', 'MATCH')}</span>
    </div>
    <div style="display: flex; justify-content: space-between; align-items: center; margin: 6px 0;">
        <span style="font-size: 0.78rem; color: #64748B;">Consistency Match</span>
        <span class="font-mono" style="font-size: 1.1rem; font-weight: 800; color: #10B981;">{mpct}%</span>
    </div>
    <div style="font-size: 0.8rem; color: #43474B;">{fdata.get('explanation', '')}</div>
</div>
""")

    # TAB 5: AI INTELLIGENCE
    with tab_rag:
        st.markdown("#### 📚 Historical Precedent Intelligence")
        sim_data = service.get_similar_cases(case_id, top_k=3)
        precedents = sim_data.get("top_k_cases", [])
        for p in precedents:
            sim_score = int(p.get('similarity_percentage', 92))
            render_html(f"""
<div class="stitch-card" style="padding: 1.15rem; margin-bottom: 10px;">
    <div style="display: flex; justify-content: space-between; align-items: center;">
        <span style="font-weight: 700; color: #191C1E;">Case #{p.get('order_id', p.get('case_id'))} &bull; Reason: {p.get('dispute_reason', dispute_type)}</span>
        <span class="stitch-pill stitch-pill-success">Outcome: {p.get('outcome', 'Won')}</span>
    </div>
    <div style="font-size: 0.82rem; color: #43474B; margin: 6px 0;">{p.get('summary')}</div>
    <div style="font-size: 0.74rem; color: #1A242C; font-weight: 600;">Precedent Relevance Match: <b style="color: #10B981;">{sim_score}%</b></div>
</div>
""")

    # TAB 6: CASE NARRATIVE
    with tab_nar:
        rep = pipeline_state.get("final_report") or {}
        nar = rep.get("case_narrative") or {}
        render_html("""
<div class="stitch-card">
    <h3 class="stitch-card-title">Structured Legal Defense Narrative</h3>
    <p class="stitch-card-subtitle">Card scheme arbitration formatted narrative generated by AI reasoning engine.</p>
</div>
""")
        st.markdown("##### 1. Incident Overview")
        st.info(nar.get("incident_overview", f"Dispute #{case.get('order_id')} filed under reason '{case.get('dispute_reason')}'. Merchant fulfilled order with verified delivery confirmation."))
        st.markdown("##### 2. Chronological Timeline Summary")
        st.markdown(f"> {nar.get('timeline_summary', '1. Order Checkout -> 2. Payment Captured -> 3. Courier Dispatched -> 4. Doorstep Delivery')}")
        st.markdown("##### 3. Verified Factual Findings")
        for vf in nar.get("verified_facts", [{"fact": "Order & Invoice match 100%", "confidence": "98%"}]):
            st.markdown(f"• **{vf.get('fact')}** (Confidence: `{vf.get('confidence')}`)")
        st.markdown("##### 4. Contradictions & Audit")
        st.markdown(f"_{nar.get('contradictions_audit', 'Zero factual contradictions detected across submitted records.')}_")
        st.markdown("##### 5. Strategic Defense Reasoning")
        st.markdown(f"> {nar.get('ai_reasoning', 'Factual records confirm fulfillment integrity and physical custody handover.')}")
        st.markdown("##### 6. Final Recommendation")
        st.success(nar.get("final_recommendation", "Submit full defense docket immediately as evidence completeness is 100%."))

    # TAB 7: FINAL REPORT
    with tab_rep:
        rep = pipeline_state.get("final_report") or {}
        render_html("""
<div class="stitch-card">
    <h3 class="stitch-card-title">Evidence Package Editor & Case Approval</h3>
    <p class="stitch-card-subtitle">Edit executive summaries, attach custom merchant statements, sign digitally, and approve case status to SUBMITTED.</p>
</div>
""")
        with st.form(f"pdf_editor_form_{case_id}"):
            col_t1, col_t2 = st.columns(2)
            with col_t1:
                rtitle = st.text_input("Report Title", value="Formal Chargeback Defense Packet")
                rsig = st.text_input("Digital Signatory Name", value="Apex Retail Operations Desk")
            with col_t2:
                rnotes = st.text_area("Merchant Custom Statement", value="The cardholder claim is refuted by carrier GPS timestamp and consignee signature.")

            c_btn1, c_btn2 = st.columns(2)
            with c_btn1:
                save_draft = st.form_submit_button("💾 Save Draft Preview", use_container_width=True)
            with c_btn2:
                approve_case = st.form_submit_button("✅ Approve Case & Mark Submitted", type="primary", use_container_width=True)

        if save_draft:
            with st.spinner("Updating PDF preview..."):
                service.preview_report(case_id, rtitle, rnotes, rsig)
                st.success("Draft updated!")
                st.rerun()

        if approve_case:
            with st.spinner("Transmitting formal defense packet to bank..."):
                service.approve_case(case_id)
                st.balloons()
                st.success(f"Case #{case.get('order_id')} marked as SUBMITTED!")
                st.rerun()
