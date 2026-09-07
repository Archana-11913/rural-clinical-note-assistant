# Technical Documentation: Clinical Note Clarification Assistant

## 1. System Overview
The **Clinical Note Clarification Assistant** is an explainable decision-support tool built for rural health centers. It detects vague, missing, contradictory, or urgent follow-up instructions in clinical consultation notes before patient departure.

---

## 2. Technical Stack
* **Language & Runtime**: Python 3.10+
* **User Interface**: Streamlit 1.25+
* **Data Processing & ML Pipeline**: Pandas, NumPy, Scikit-learn
* **Visualization**: Matplotlib, Seaborn
* **Language Support**: English-Only core interface (designed with modular dictionary abstraction for future Tamil/Hindi expansion).

---

## 3. Core Architecture & Modules

```
rural_clinical_note_assistant/
├── app.py                      # Main Streamlit 5-page web application
├── rules/
│   └── ambiguity_rules.py      # Baseline & Proposed Rule Engines
├── data/
│   ├── generate_synthetic_data.py # Synthetic dataset generator (1,200 records)
│   ├── synthetic_consultation_notes.csv # Primary benchmark dataset
│   └── audit_log.csv           # Persisted audit log file
├── evaluation/
│   ├── run_experiment.py       # Benchmark evaluation script
│   ├── metrics.csv             # Evaluated performance metrics
│   ├── error_analysis.md       # Qualitative error analysis
│   └── failure_cases.md        # 6 explicit failure test cases
├── docs/
│   ├── workflow_map.md         # Field workflow diagram
│   ├── technical_documentation.md # Technical documentation (this file)
│   └── user_feedback_summary.md # Simulated stakeholder validation results
├── presentation/
│   └── presentation_content.md # 15-slide capstone presentation deck
└── README.md                   # Project setup & usage guide
```

---

## 4. Rule Engine Specification

### Baseline Engine (`BaselineAmbiguityDetector`)
* **Mechanism**: Direct regex substring searching and basic temporal regex matching.
* **Target Categories**: `FOLLOWUP_TIME_MISSING`, `CONTRADICTORY_TIMING`, `UNCLEAR_SPECIALIST_REFERRAL`.

### Proposed Engine (`ProposedAmbiguityAssistant`)
* **Mechanism**: Multi-stage pattern parsing, phrase normalization, confidence scoring, evidence extraction, and risk escalation mapping.
* **Outputs**:
  - `is_ambiguous` (bool)
  - `ambiguity_category` (str)
  - `confidence` (High / Medium / Low)
  - `evidence` (str)
  - `triggered_rule` (str)
  - `suggested_clarification` (str)
  - `recommended_next_step` (str)
  - `escalation_level` (str)
  - `human_confirmation_required` (str)
  - `uncertainty_warning` (str or None)

---

## 5. Ambiguity Categories Classification Taxonomy
1. `NONE`: Clear note.
2. `FOLLOWUP_TIME_MISSING`: Vague relative time (e.g., "later", "soon").
3. `VAGUE_DURATION`: Unclear treatment duration (e.g., "for some time").
4. `VAGUE_SYMPTOM_CONDITION`: Unclear return threshold (e.g., "if symptoms get worse").
5. `MISSING_ACTION`: Return date stated without clinical procedure.
6. `CONTRADICTORY_TIMING`: Conflicting milestones (e.g., "tomorrow" and "two weeks").
7. `UNCLEAR_SPECIALIST_REFERRAL`: Unspecified specialty or trigger criteria.
8. `UNCLEAR_RESPONSIBILITY`: Unassigned care provider role.
9. `URGENCY_AMBIGUITY`: Urgent symptom combined with routine/delayed review.
10. `MISSING_NOTE`: Empty or whitespace note.
11. `NOISY_NOTE`: Severe transcription / spelling noise.

---

## 6. Audit Logging & Persistence
Decisions made in the Human-in-the-Loop interface are written to `data/audit_log.csv` with fields:
`Case_ID`, `Original_Note`, `Detected_Ambiguity`, `Recommendation`, `Human_Decision`, `Override_Reason`, `Timestamp`.

---

## 7. Multilingual Extensibility Architecture
While the current prototype strictly uses English, the rule engine isolates dictionary keys into modular string mappings (`CATEGORIES`, `urgent_symptoms`, `routine_delays`), allowing localized translations (e.g. Tamil or Hindi) to be plugged into the NLP pre-processor without altering core evaluation logic.
