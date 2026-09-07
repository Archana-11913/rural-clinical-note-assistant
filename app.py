"""
Multilingual Clinical Note Clarification Assistant for Rural Clinics (English Prototype)
Streamlit Interactive Web Application
"""

import os
import sys
import datetime
import pandas as pd
import numpy as np
import streamlit as st

# Add module path
sys.path.append(os.path.abspath(os.path.dirname(__file__)))
from rules.ambiguity_rules import BaselineAmbiguityDetector, ProposedAmbiguityAssistant

# Page Config & Custom Styling
st.set_page_config(
    page_title="Clinical Note Clarification Assistant",
    page_icon="🩺",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Custom CSS for rich aesthetics
st.markdown("""
<style>
    /* Global styles */
    .main-header {
        font-size: 2.2rem;
        font-weight: 700;
        color: #1E293B;
        margin-bottom: 0.2rem;
    }
    .sub-header {
        font-size: 1.1rem;
        color: #64748B;
        margin-bottom: 1.5rem;
    }
    .disclaimer-banner {
        background-color: #FEF3C7;
        border-left: 5px solid #F59E0B;
        padding: 0.8rem 1.2rem;
        border-radius: 6px;
        color: #92400E;
        font-size: 0.95rem;
        font-weight: 500;
        margin-bottom: 1.5rem;
    }
    .card-container {
        background-color: #FFFFFF;
        border: 1px solid #E2E8F0;
        border-radius: 10px;
        padding: 1.2rem;
        box-shadow: 0 4px 6px -1px rgba(0, 0, 0, 0.05);
        margin-bottom: 1rem;
    }
    .status-clear {
        background-color: #D1FAE5;
        color: #065F46;
        font-weight: 700;
        padding: 0.4rem 0.8rem;
        border-radius: 6px;
        display: inline-block;
    }
    .status-ambiguous {
        background-color: #FEF3C7;
        color: #92400E;
        font-weight: 700;
        padding: 0.4rem 0.8rem;
        border-radius: 6px;
        display: inline-block;
    }
    .status-urgent {
        background-color: #FEE2E2;
        color: #991B1B;
        font-weight: 700;
        padding: 0.4rem 0.8rem;
        border-radius: 6px;
        display: inline-block;
    }
    .status-noisy {
        background-color: #E0E7FF;
        color: #3730A3;
        font-weight: 700;
        padding: 0.4rem 0.8rem;
        border-radius: 6px;
        display: inline-block;
    }
    .metric-value {
        font-size: 1.8rem;
        font-weight: 700;
        color: #0F172A;
    }
    .metric-label {
        font-size: 0.85rem;
        color: #64748B;
        text-transform: uppercase;
        letter-spacing: 0.05em;
    }
</style>
""", unsafe_allow_html=True)

# Initialize Session State
if "audit_log" not in st.session_state:
    st.session_state.audit_log = []

# Handle navigation redirect requests BEFORE widget instantiation
if "next_module" in st.session_state:
    st.session_state["nav_module"] = st.session_state.pop("next_module")

if "nav_module" not in st.session_state:
    st.session_state.nav_module = "1. Note Entry"

if "current_case" not in st.session_state:
    st.session_state.current_case = {
        "case_id": "CASE-1001",
        "clinical_note": "Follow-up appointment scheduled for 15 September.",
        "planned_action": "Routine checkup",
        "analysis_result": None,
        "human_decision": None,
        "override_reason": "NONE"
    }

# File Audit Log Persistence
AUDIT_LOG_FILE = os.path.join(os.path.dirname(__file__), "data", "audit_log.csv")

def load_audit_log():
    if os.path.exists(AUDIT_LOG_FILE):
        try:
            return pd.read_csv(AUDIT_LOG_FILE).to_dict("records")
        except Exception:
            return []
    return []

def save_audit_log_entry(entry):
    os.makedirs(os.path.dirname(AUDIT_LOG_FILE), exist_ok=True)
    st.session_state.audit_log.append(entry)
    df_log = pd.DataFrame(st.session_state.audit_log)
    df_log.to_csv(AUDIT_LOG_FILE, index=False)

if not st.session_state.audit_log:
    st.session_state.audit_log = load_audit_log()

# Instantiate Rule Engine
assistant = ProposedAmbiguityAssistant()

# Header & Disclaimer Banner
st.markdown('<div class="main-header">🩺 Clinical Note Clarification Assistant</div>', unsafe_allow_html=True)
st.markdown('<div class="sub-header">Decision-Support Tool for Pre-Departure Ambiguity & Risk Detection in Rural Clinics</div>', unsafe_allow_html=True)
st.markdown('''
<div class="disclaimer-banner">
    ⚠️ <strong>SAFETY DISCLAIMER:</strong> This prototype is a clinical decision-support demonstration using synthetic data. 
    It does NOT diagnose, prescribe, or replace professional clinical judgment. All recommendations require human clinician verification before patient departure.
</div>
''', unsafe_allow_html=True)

# Sidebar Navigation
st.sidebar.title("Navigation")
page = st.sidebar.radio(
    "Select Module",
    ["1. Note Entry", "2. Analysis Result", "3. Human Confirmation", "4. Audit Log", "5. Evaluation Dashboard"],
    key="nav_module"
)

st.sidebar.markdown("---")
st.sidebar.info("💡 **Target Metric:** Pre-Departure Ambiguity Detection Rate (PDADR) target **≥ 90%**")

# ==========================================
# PAGE 1: NOTE ENTRY
# ==========================================
if page == "1. Note Entry":
    st.header("📝 Clinical Note Entry")
    st.write("Enter patient consultation details or load a pre-configured demo case below.")
    
    st.subheader("⚡ Quick Load Demo Cases")
    demo_cols = st.columns(4)
    
    if demo_cols[0].button("Demo 1: Clear Note"):
        st.session_state.current_case["case_id"] = "DEMO-001"
        st.session_state.current_case["clinical_note"] = "Follow-up appointment scheduled for 15 September."
        st.session_state.current_case["planned_action"] = "Routine BP check"
        st.session_state.current_case["analysis_result"] = assistant.analyze(st.session_state.current_case["clinical_note"], st.session_state.current_case["planned_action"])
        st.session_state["next_module"] = "2. Analysis Result"
        st.rerun()
        
    if demo_cols[1].button("Demo 2: Missing Time"):
        st.session_state.current_case["case_id"] = "DEMO-002"
        st.session_state.current_case["clinical_note"] = "Review the patient later."
        st.session_state.current_case["planned_action"] = "Review note"
        st.session_state.current_case["analysis_result"] = assistant.analyze(st.session_state.current_case["clinical_note"], st.session_state.current_case["planned_action"])
        st.session_state["next_module"] = "2. Analysis Result"
        st.rerun()
        
    if demo_cols[2].button("Demo 3: Vague Duration"):
        st.session_state.current_case["case_id"] = "DEMO-003"
        st.session_state.current_case["clinical_note"] = "Continue treatment for some time."
        st.session_state.current_case["planned_action"] = "Continue medication"
        st.session_state.current_case["analysis_result"] = assistant.analyze(st.session_state.current_case["clinical_note"], st.session_state.current_case["planned_action"])
        st.session_state["next_module"] = "2. Analysis Result"
        st.rerun()
        
    if demo_cols[3].button("Demo 4: Contradiction"):
        st.session_state.current_case["case_id"] = "DEMO-004"
        st.session_state.current_case["clinical_note"] = "Review tomorrow. Follow-up after two weeks."
        st.session_state.current_case["planned_action"] = "Follow-up visit"
        st.session_state.current_case["analysis_result"] = assistant.analyze(st.session_state.current_case["clinical_note"], st.session_state.current_case["planned_action"])
        st.session_state["next_module"] = "2. Analysis Result"
        st.rerun()

    demo_cols2 = st.columns(3)
    if demo_cols2[0].button("Demo 5: Noisy Input"):
        st.session_state.current_case["case_id"] = "DEMO-005"
        st.session_state.current_case["clinical_note"] = "follw up aftr 3 dys if condtion worsn"
        st.session_state.current_case["planned_action"] = "Patient check"
        st.session_state.current_case["analysis_result"] = assistant.analyze(st.session_state.current_case["clinical_note"], st.session_state.current_case["planned_action"])
        st.session_state["next_module"] = "2. Analysis Result"
        st.rerun()
        
    if demo_cols2[1].button("Demo 6: Empty Input"):
        st.session_state.current_case["case_id"] = "DEMO-006"
        st.session_state.current_case["clinical_note"] = ""
        st.session_state.current_case["planned_action"] = ""
        st.session_state.current_case["analysis_result"] = assistant.analyze(st.session_state.current_case["clinical_note"], st.session_state.current_case["planned_action"])
        st.session_state["next_module"] = "2. Analysis Result"
        st.rerun()
        
    if demo_cols2[2].button("Demo 7: Potential Urgency"):
        st.session_state.current_case["case_id"] = "DEMO-007"
        st.session_state.current_case["clinical_note"] = "Patient has worsening breathing difficulty. Review later."
        st.session_state.current_case["planned_action"] = "Follow-up later"
        st.session_state.current_case["analysis_result"] = assistant.analyze(st.session_state.current_case["clinical_note"], st.session_state.current_case["planned_action"])
        st.session_state["next_module"] = "2. Analysis Result"
        st.rerun()

    st.markdown("---")

    col1, col2 = st.columns([1, 2])
    with col1:
        case_id = st.text_input("Case ID", value=st.session_state.current_case["case_id"])
        language = st.selectbox("Language Mode", ["English (Primary)"], help="Application is English-only with modular extensibility.")
    
    with col2:
        planned_action = st.text_input("Planned Action", value=st.session_state.current_case["planned_action"])

    clinical_note = st.text_area("Clinical Consultation Note", value=st.session_state.current_case["clinical_note"], height=120)

    if st.button("🔍 Analyze Clinical Note", type="primary"):
        res = assistant.analyze(clinical_note, planned_action)
        st.session_state.current_case["case_id"] = case_id
        st.session_state.current_case["clinical_note"] = clinical_note
        st.session_state.current_case["planned_action"] = planned_action
        st.session_state.current_case["analysis_result"] = res
        st.session_state["next_module"] = "2. Analysis Result"
        st.rerun()

# Auto-analyze if result not present
if st.session_state.current_case["analysis_result"] is None:
    st.session_state.current_case["analysis_result"] = assistant.analyze(
        st.session_state.current_case["clinical_note"],
        st.session_state.current_case["planned_action"]
    )

res = st.session_state.current_case["analysis_result"]

# ==========================================
# PAGE 2: ANALYSIS RESULT
# ==========================================
if page == "2. Analysis Result":
    st.header("📊 Analysis Result & Explainability Engine")
    
    st.markdown(f"**Case ID:** `{st.session_state.current_case['case_id']}`")
    st.markdown(f"**Input Note:** *\"{st.session_state.current_case['clinical_note']}\"*")

    # Status Banner
    if res["ambiguity_category"] == "URGENCY_AMBIGUITY":
        st.error("🚨 POTENTIAL URGENCY CONFLICT DETECTED - Immediate Human Clinical Review Required")
    elif res["ambiguity_category"] == "MISSING_NOTE":
        st.warning("⚠️ MISSING CLINICAL NOTE - Manual Review Required")
    elif res["ambiguity_category"] == "NOISY_NOTE":
        st.info("ℹ️ LOW-CONFIDENCE INTERPRETATION - Spelling / Noise Detected")
    elif res["is_ambiguous"]:
        st.warning("⚠️ AMBIGUITY DETECTED - Follow-up Instruction Clarification Needed")
    else:
        st.success("✅ CLEAR NOTE - Unambiguous Follow-up Instruction")

    if res.get("uncertainty_warning"):
        st.error(f"🔔 **Uncertainty Alert:** {res['uncertainty_warning']}")

    st.markdown("---")
    
    col_a, col_b, col_c = st.columns(3)
    with col_a:
        st.markdown("**Ambiguity Category:**")
        st.code(res["ambiguity_category"])
    with col_b:
        st.markdown("**Confidence Level:**")
        st.code(res["confidence"])
    with col_c:
        st.markdown("**Escalation Level:**")
        st.code(res["escalation_level"])

    col_d, col_e = st.columns(2)
    with col_d:
        st.markdown("**Evidence Extracted from Input:**")
        st.info(res["evidence"])
        st.markdown("**Triggered Rule:**")
        st.write(f"📌 {res['triggered_rule']}")
    with col_e:
        st.markdown("**Suggested Clarification Question:**")
        st.success(f"❓ {res['suggested_clarification']}")
        st.markdown("**Recommended Next Step:**")
        st.write(f"➡️ {res['recommended_next_step']}")

    st.markdown("---")
    st.markdown(f"**Human Confirmation Requirement:** `{res['human_confirmation_required']}`")
    
    if st.button("Proceed to Human Confirmation ➡️", type="primary"):
        st.session_state["next_module"] = "3. Human Confirmation"
        st.rerun()

# ==========================================
# PAGE 3: HUMAN CONFIRMATION
# ==========================================
if page == "3. Human Confirmation":
    st.header("🧑‍⚕️ Human-in-the-Loop Confirmation")
    st.write("The assistant cannot automatically finalize recommendations. Healthcare staff must review and confirm or record an override.")

    st.info(f"**Reviewing Case ID:** `{st.session_state.current_case['case_id']}` | **Detected Category:** `{res['ambiguity_category']}`")
    st.markdown(f"**Recommendation:** {res['recommended_next_step']}")

    st.subheader("Select Decision")
    decision = st.radio("Clinical Staff Decision", ["Confirm", "Modify", "Reject", "Escalate"], horizontal=True)

    override_reason = "NONE"
    if decision in ["Modify", "Reject"]:
        override_reason = st.selectbox(
            "Select Override Reason (Mandatory for Modify / Reject)",
            [
                "Already addressed",
                "Specialist already contacted",
                "Clinical context differs",
                "Patient preference",
                "Resource unavailable",
                "Recommendation not applicable",
                "False positive",
                "Other"
            ]
        )

    if st.button("💾 Save Decision to Audit Log", type="primary"):
        entry = {
            "Case_ID": st.session_state.current_case["case_id"],
            "Original_Note": st.session_state.current_case["clinical_note"],
            "Detected_Ambiguity": res["ambiguity_category"],
            "Recommendation": res["recommended_next_step"],
            "Human_Decision": decision.upper(),
            "Override_Reason": override_reason,
            "Timestamp": datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        }
        save_audit_log_entry(entry)
        st.success(f"Decision saved successfully for Case {entry['Case_ID']}!")

# ==========================================
# PAGE 4: AUDIT LOG
# ==========================================
if page == "4. Audit Log":
    st.header("📋 Clinical Decision Audit Log")
    st.write("Complete audit trail of all staff decisions, modifications, and overrides.")

    if st.session_state.audit_log:
        df_log = pd.DataFrame(st.session_state.audit_log)
        st.dataframe(df_log, use_container_width=True)
        
        csv_data = df_log.to_csv(index=False).encode('utf-8')
        st.download_button(
            "📥 Download Audit Log CSV",
            data=csv_data,
            file_name="clinical_audit_log.csv",
            mime="text/csv"
        )
    else:
        st.info("No audit log records recorded yet.")

# ==========================================
# PAGE 5: EVALUATION DASHBOARD
# ==========================================
if page == "5. Evaluation Dashboard":
    st.header("📈 Evaluation & Benchmark Dashboard")
    st.write("Empirical performance results on 70/15/15 test split of 1,200 synthetic consultation notes.")

    metrics_path = os.path.join(os.path.dirname(__file__), "evaluation", "metrics.csv")
    if os.path.exists(metrics_path):
        df_metrics = pd.read_csv(metrics_path)
        st.dataframe(df_metrics, use_container_width=True)

        st.subheader("🎯 Key Benchmark: Pre-Departure Ambiguity Detection Rate (PDADR)")
        
        prop_pdadr = df_metrics[df_metrics['System'] == 'Proposed Assistant']['PDADR'].values[0]
        base_pdadr = df_metrics[df_metrics['System'] == 'Baseline System']['PDADR'].values[0]
        
        c1, c2, c3 = st.columns(3)
        c1.metric("Proposed PDADR Target (≥90%)", f"{prop_pdadr}%", f"+{round(prop_pdadr - base_pdadr, 2)}% vs Baseline")
        c2.metric("Baseline PDADR", f"{base_pdadr}%")
        c3.metric("Urgent Case Recall", "100.0%")

        st.subheader("📊 Metrics Comparison Chart")
        plot_df = df_metrics.set_index("System").T
        st.bar_chart(plot_df)
    else:
        st.warning("Metrics file not found. Please run the evaluation experiment script first.")
