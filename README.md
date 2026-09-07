# Multilingual Clinical Note Clarification Assistant for Rural Clinics (English Edition)

[![Streamlit App](https://img.shields.io/badge/Streamlit-App-FF4B4B.svg)](https://streamlit.io)
[![Python Version](https://img.shields.io/badge/Python-3.10%2B-blue.svg)](https://python.org)
[![PDADR Benchmark](https://img.shields.io/badge/PDADR-95.65%25-brightgreen.svg)]()

> [!IMPORTANT]
> **SAFETY DISCLAIMER**: This prototype is a clinical decision-support demonstration using synthetic data. It does NOT diagnose diseases, prescribe medications, or replace professional clinical judgment. All recommendations require human clinician verification before patient departure.

---

## 1. Project Overview & Problem Statement
Rural primary care health centers frequently operate under high patient volume with limited access to clinical specialists. Consultation notes created in these environments may contain vague, incomplete, contradictory, or ambiguous follow-up instructions (e.g., *"review later"*, *"continue treatment for some time"*, *"come back if condition worsens"*). 

This ambiguity leads to inconsistent post-consultation care, missed red-flag emergency symptoms, and preventable patient deterioration after departure. 

The **Clinical Note Clarification Assistant** is an explainable decision-support tool engineered to identify ambiguity in clinical consultation notes **BEFORE** the patient leaves the clinic building.

---

## 2. Objectives & Benchmark Target
* **Primary Benchmark**: **Pre-Departure Ambiguity Detection Rate (PDADR)**
  $$\text{PDADR} = \frac{\text{Correctly Identified Ambiguous Instructions}}{\text{Total Ambiguous Instructions}} \times 100$$
* **Target Rate**: $\ge 90\%$ (Empirically Achieved: **95.65%**).
* **Language Specification**: **English only** (UI, datasets, rules, recommendations, documentation, and presentation), architected for future multilingual extensibility.

---

## 3. System Architecture & Workflow Map

```
Patient Consultation ──► Clinical Note Entry ──► Note Clarification Assistant
                                                              │
                                                              ▼
                                                 Check Ambiguity & Risk
                                                              │
                                            ┌─────────────────┴─────────────────┐
                                            ▼                                   ▼
                                     [ Status: CLEAR ]             [ Status: AMBIGUOUS / URGENT ]
                                            │                                   │
                                            ▼                                   ▼
                                   Standard Discharge               Structured Explanation &
                                        Workflow                    Clarification Question
                                            │                                   │
                                            │                                   ▼
                                            │                       Human Clinician Review
                                            │                       (Confirm / Modify / Reject / Escalate)
                                            │                                   │
                                            │                                   ▼
                                            └───────────────────────► Audit Log Recorded
                                                                                │
                                                                                ▼
                                                                        Patient Departure
```

---

## 4. Ambiguity Taxonomy (Categories A – J)
1. **Category A: Missing Follow-up Time** (`FOLLOWUP_TIME_MISSING`): *"Review the patient later."*
2. **Category B: Vague Duration** (`VAGUE_DURATION`): *"Continue treatment for some time."*
3. **Category C: Vague Symptom Condition** (`VAGUE_SYMPTOM_CONDITION`): *"Come back if symptoms get worse."*
4. **Category D: Missing Action** (`MISSING_ACTION`): *"Follow-up in one week."*
5. **Category E: Contradictory Timing** (`CONTRADICTORY_TIMING`): *"Review tomorrow. Follow-up after two weeks."*
6. **Category F: Unclear Specialist Referral** (`UNCLEAR_SPECIALIST_REFERRAL`): *"Refer to specialist if necessary."*
7. **Category G: Unclear Responsibility** (`UNCLEAR_RESPONSIBILITY`): *"Someone should review the patient."*
8. **Category H: Urgency Ambiguity** (`URGENCY_AMBIGUITY`): *"Patient has worsening breathing difficulty. Review later."*
9. **Category I: Missing Clinical Note** (`MISSING_NOTE`): Empty or whitespace-only input.
10. **Category J: Low-Quality / Noisy Note** (`NOISY_NOTE`): *"follw up aftr 3 dys if condtion worsn"*.

---

## 5. Dataset Generation & Schema
A synthetic dataset of **1,200 records** was created via `data/generate_synthetic_data.py` into `data/synthetic_consultation_notes.csv`. No real patient data is used.

**Required Schema**: `Case_ID`, `Clinical_Note`, `Planned_Action`, `Ambiguity_Type`, `Ambiguous_Flag`, `Urgency_Level`, `Expected_Clarification`, `Expected_Escalation`, `Clarification_Outcome`, `Human_Decision`, `Override_Reason`, `Note_Quality`, `Translation_Quality`.

---

## 6. Baseline vs. Proposed System
* **Baseline System**: Regular expression and keyword matching model.
* **Proposed System**: Explainable decision-support engine featuring pattern normalization, confidence scoring, evidence extraction, triggered rule reporting, suggested clarification formulation, escalation routing, and uncertainty warnings.

---

## 7. Explainability & Human-in-the-Loop
For every evaluated note, the assistant displays:
* **Detected Issue & Category**
* **Confidence Level** (High / Medium / Low)
* **Evidence Extracted from Input**
* **Triggered Clinical Rule**
* **Suggested Clarification Question**
* **Recommended Next Step & Escalation Level**

Staff can interactively choose: **Confirm**, **Modify**, **Reject**, or **Escalate**. Modifying or rejecting requires selecting a mandatory override reason (e.g., *Already addressed*, *Specialist already contacted*, *Clinical context differs*, *False positive*). All decisions are saved to `data/audit_log.csv`.

---

## 8. Benchmark Evaluation & Results

Evaluated on **70/15/15** Train/Val/Test Split (180 Test Notes):

| Metric | Baseline System | Proposed Assistant | Delta |
|--------|-----------------|--------------------|-------|
| **PDADR (Primary Benchmark)** | **50.00%** | **95.65%** | **+45.65%** |
| **Accuracy** | 59.44% | **96.67%** | +37.23% |
| **Precision** | 94.52% | **100.00%** | +5.48% |
| **Recall** | 50.00% | **95.65%** | +45.65% |
| **F1 Score** | 65.40% | **97.78%** | +32.38% |
| **Urgent Case Recall** | 71.43% | **100.00%** | +28.57% |
| **False Positive Rate (FPR)** | 9.52% | **0.00%** | -9.52% |
| **False Negative Rate (FNR)** | 50.00% | **4.35%** | -45.65% |
| **Clarification Success Rate** | 42.50% | **100.00%** | +57.50% |

---

## 9. Installation & Execution Instructions

### Prerequisites
* Python 3.10 or higher installed.

### Setup Environment
```bash
cd rural_clinical_note_assistant
pip install -r requirements.txt
```

### 1. Regenerate Synthetic Dataset (Optional)
```bash
python data/generate_synthetic_data.py
```

### 2. Run Benchmark Experiment
```bash
python evaluation/run_experiment.py
```

### 3. Launch Streamlit Web Application
```bash
streamlit run app.py
```

---

## 10. Repository Structure

```
rural_clinical_note_assistant/
├── app.py                      # Streamlit 5-page application
├── requirements.txt            # Project dependencies
├── README.md                   # System documentation
├── data/
│   ├── generate_synthetic_data.py # Dataset generation script
│   ├── synthetic_consultation_notes.csv # 1,200 synthetic records
│   └── audit_log.csv           # Persisted clinical decisions
├── rules/
│   └── ambiguity_rules.py      # Baseline and Proposed Rule Engines
├── notebooks/
│   └── experiment.ipynb        # Jupyter evaluation notebook
├── evaluation/
│   ├── run_experiment.py       # Benchmark evaluation script
│   ├── metrics.csv             # Evaluated metrics CSV
│   ├── error_analysis.md       # Error analysis report
│   └── failure_cases.md        # 6 explicit failure test cases
├── docs/
│   ├── workflow_map.md         # Field workflow diagram
│   ├── technical_documentation.md # Technical documentation
│   └── user_feedback_summary.md # Simulated stakeholder validation results
└── presentation/
    └── presentation_content.md # 15-slide presentation deck
```

---

## 11. Limitations & Future Work
* **Language Support**: Currently configured for English; dictionary pre-processors will be extended for Tamil, Hindi, and Telugu.
* **EHR Integration**: Future work includes FHIR API endpoints for direct integration with rural electronic health record systems.
