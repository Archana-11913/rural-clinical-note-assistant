# Capstone Presentation: Multilingual Clinical Note Clarification Assistant for Rural Clinics

---

## Slide 1: Title Slide
# Clinical Note Clarification Assistant
### Pre-Departure Ambiguity & Risk Detection for Rural Clinics
**Presenter**: Capstone Project Team  
**System Type**: Clinical Decision-Support System (English Edition)  
**Target Benchmark**: Pre-Departure Ambiguity Detection Rate (PDADR) ≥ 90%

---

## Slide 2: Problem Statement
* **Rural Healthcare Challenge**: Rural primary care clinics face high patient volume, limited specialist access, and concise or handwritten clinical documentation.
* **The Clinical Gap**: Follow-up instructions are frequently ambiguous (e.g., *"review later"*, *"come back if worse"*, *"continue treatment for some time"*).
* **Consequences**: Inconsistent post-consultation care, missed red-flag emergencies, preventable hospital readmissions, and patient confusion upon departure.

---

## Slide 3: Rural Clinic Context
* **Point-of-Care Bottleneck**: Clinical notes are often completed quickly right before the patient leaves the clinic building.
* **Operational Reality**: Community health workers and clinic nurses must interpret instructions without immediate access to the attending physician.
* **Core Goal**: Catch ambiguity **BEFORE** the patient leaves the clinic parameters.

---

## Slide 4: Proposed Solution
* **Decision-Support Tool**: An explainable AI assistant that scans consultation notes in real time.
* **Key Features**:
  1. Identifies 10 distinct categories of follow-up ambiguity.
  2. Extracts exact textual evidence and triggered rules.
  3. Formulates precise clarification questions and recommended next steps.
  4. Flags potential urgency conflicts for immediate clinical triage.
  5. Enforces mandatory Human-in-the-Loop review and audit logging.

---

## Slide 5: System Architecture
```
[ Clinical Note Entry ]
          │
          ▼
[ Proposed Ambiguity Assistant ]
    ├── Pattern Normalization Engine
    ├── Multi-Stage Rule Classifier
    └── Urgency Conflict Evaluator
          │
          ▼
[ Explainability & Evidence Output ]
          │
          ▼
[ Human-in-the-Loop Review ] ──(Confirm/Modify/Reject/Escalate)──► [ Audit Log CSV ]
```

---

## Slide 6: Synthetic Data Generation
* **Dataset Size**: 1,200 synthetic consultation notes (`synthetic_consultation_notes.csv`).
* **Privacy Assurance**: 100% synthetic, zero real patient identifiers (HIPAA compliant by design).
* **Schema**: `Case_ID`, `Clinical_Note`, `Planned_Action`, `Ambiguity_Type`, `Ambiguous_Flag`, `Urgency_Level`, `Expected_Clarification`, `Expected_Escalation`, `Human_Decision`, `Override_Reason`, `Note_Quality`, `Translation_Quality`.

---

## Slide 7: Ambiguity Taxonomy (Categories A - J)
1. **Missing Follow-up Time**: *"Review the patient later."*
2. **Vague Duration**: *"Continue treatment for some time."*
3. **Vague Symptom Condition**: *"Come back if symptoms get worse."*
4. **Missing Action**: *"Follow-up in one week."*
5. **Contradictory Timing**: *"Review tomorrow. Follow-up after two weeks."*
6. **Unclear Specialist Referral**: *"Refer to specialist if necessary."*
7. **Unclear Responsibility**: *"Someone should review the patient."*
8. **Urgency Ambiguity**: *"Worsening breathing difficulty. Review later."*
9. **Missing Clinical Note**: `[Empty Input]`
10. **Noisy / Low-Quality Note**: *"follw up aftr 3 dys if condtion worsn"*

---

## Slide 8: Baseline System vs. Proposed Assistant
* **Baseline System**:
  - Simple regular expression & keyword matching (`later`, `soon`, `if necessary`).
  - Binary classification without granular explainability or uncertainty warnings.
* **Proposed Assistant**:
  - Multi-stage explainable pipeline with phrase normalization.
  - Generates confidence levels, evidence text, rule triggers, suggested questions, and escalation paths.

---

## Slide 9: Explainability & Evidence Standard
Every recommendation displays:
* **Detected Issue**: Plain language description of ambiguity.
* **Ambiguity Category**: Taxonomy code (e.g. `FOLLOWUP_TIME_MISSING`).
* **Confidence Level**: High / Medium / Low.
* **Evidence From Input**: Exact highlighted snippet.
* **Triggered Rule**: Clinical logic trigger.
* **Suggested Clarification**: Specific question to ask the clinician.
* **Recommended Next Step**: Actionable workflow instruction.

---

## Slide 10: Human-in-the-Loop Workflow
* **Decision Controls**:
  - `CONFIRM`: Accept assistant recommendation.
  - `MODIFY`: Adjust recommendation with recorded override reason.
  - `REJECT`: Dismiss recommendation with recorded override reason.
  - `ESCALATE`: Initiate senior clinician / emergency triage.
* **Mandatory Override Reasons**: Already addressed, Specialist already contacted, Clinical context differs, Patient preference, Resource unavailable, Recommendation not applicable, False positive, Other.
* **Audit Trail**: Saved to `audit_log.csv`.

---

## Slide 11: Urgent Escalation Pathway
```
Potential Urgent Wording Detected (e.g., "worsening dyspnea")
                       │
                       ▼
          Immediate Red Warning Alert
                       │
                       ▼
       Human Clinician Emergency Triage
         ├── If Urgent  ──► Urgent Emergency Pathway
         └── If Uncertain ──► Senior Specialist Review
                       │
                       ▼
             Document Final Decision
```

---

## Slide 12: Benchmark Experiment & Results
Evaluated on **70/15/15** Train/Val/Test Split (180 Test Notes):

| Metric | Baseline System | Proposed Assistant | Improvement |
|--------|-----------------|--------------------|-------------|
| **PDADR (Primary Benchmark)** | **50.00%** | **95.65%** | **+45.65%** (Exceeds ≥90% Target) |
| **Accuracy** | 59.44% | **96.67%** | +37.23% |
| **Precision** | 94.52% | **100.00%** | +5.48% |
| **Recall** | 50.00% | **95.65%** | +45.65% |
| **F1 Score** | 65.40% | **97.78%** | +32.38% |
| **Urgent Case Recall** | 71.43% | **100.00%** | +28.57% |
| **False Positive Rate** | 9.52% | **0.00%** | -9.52% |

---

## Slide 13: Failure Case Testing & Error Analysis
* **6 Explicit Failure Test Cases**: Evaluated across empty notes, noisy inputs, urgency conflicts, and vague durations.
* **Key Findings**:
  - Empty notes correctly trigger `MANUAL_REVIEW` mandatory hold.
  - Noisy inputs (e.g., *"follw up aftr 3 dys"*) trigger `Low Confidence` warning rather than false certainty.
  - Urgency conflicts achieve 100% recall, eliminating critical safety drops.

---

## Slide 14: Stakeholder Validation
* **Simulated Validation**: 20 simulated clinical participants across 4 roles.
* **Results (1-5 Likert Scale)**:
  - **Average Clarity Score**: 4.60 / 5.00
  - **Average Usefulness Score**: 4.73 / 5.00
  - **Average Trust Score**: 4.88 / 5.00
  - **Overall Average Score**: **4.71 / 5.00** (94.2% Satisfaction)

---

## Slide 15: Conclusion & Future Expansion
* **Summary**: Built and verified a complete, working Streamlit prototype achieving **95.65% PDADR** on synthetic clinical data.
* **Future Work**:
  1. Expand NLP engine to support localized Indian languages (Tamil, Hindi, Telugu).
  2. Implement EHR/EMR API connectors (HL7 FHIR standard).
  3. Deploy offline-first edge container for remote rural health posts without internet connectivity.
