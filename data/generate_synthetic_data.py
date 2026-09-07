"""
Synthetic Dataset Generator for Rural Clinical Note Clarification Assistant
Generates realistic, synthetic consultation notes in English covering 10 ambiguity categories.
"""

import os
import random
import pandas as pd
import numpy as np

# Set seed for reproducibility
random.seed(42)
np.random.seed(42)

# Ambiguity Categories Definition
CATEGORIES = {
    "NONE": "Clear Note - No Ambiguity",
    "FOLLOWUP_TIME_MISSING": "Missing Follow-up Time",
    "VAGUE_DURATION": "Vague Duration",
    "VAGUE_SYMPTOM_CONDITION": "Vague Symptom Condition",
    "MISSING_ACTION": "Missing Action",
    "CONTRADICTORY_TIMING": "Contradictory Timing",
    "UNCLEAR_SPECIALIST_REFERRAL": "Unclear Specialist Referral",
    "UNCLEAR_RESPONSIBILITY": "Unclear Responsibility",
    "URGENCY_AMBIGUITY": "Urgency Ambiguity / Worsening Symptoms",
    "MISSING_NOTE": "Missing Clinical Note",
    "NOISY_NOTE": "Low-Quality / Noisy Note"
}

# Template definitions for synthetic generation

# Clear Notes (NONE)
CLEAR_TEMPLATES = [
    ("Patient diagnosed with acute pharyngitis. Amoxicillin 500mg prescribed for 7 days. Return to clinic in 5 days for review.", "Review in 5 days", "ROUTINE", "None required", "NONE", "CONFIRMED", "HIGH"),
    ("Hypertension consultation. BP recorded at 135/85 mmHg. Continue daily Amlodipine 5mg. Schedule follow-up visit on 15 September.", "Follow-up on 15 September", "ROUTINE", "None required", "NONE", "CONFIRMED", "HIGH"),
    ("Patient presenting with mild eczema. Hydrocortisone cream applied. Return to rural health center in 2 weeks for reassessment.", "Reassessment in 2 weeks", "ROUTINE", "None required", "NONE", "CONFIRMED", "HIGH"),
    ("Post-op wound check day 7. Wound healing cleanly with no signs of infection. Sutures removed. Next checkup in 10 days.", "Checkup in 10 days", "ROUTINE", "None required", "NONE", "CONFIRMED", "HIGH"),
    ("Type 2 diabetes routine check. HbA1c 7.2%. Continue Metformin 500mg BD. Re-check blood fasting sugar on Monday morning.", "Fasting sugar recheck Monday", "ROUTINE", "None required", "NONE", "CONFIRMED", "HIGH"),
    ("Mild osteoarthritis of right knee. Paracetamol 1g TDS prescribed as needed for pain. Follow up in 3 weeks at clinic.", "Follow up in 3 weeks", "ROUTINE", "None required", "NONE", "CONFIRMED", "HIGH"),
    ("Upper respiratory tract infection. Advised bed rest and oral fluids. Return to clinic on Friday if not completely resolved.", "Return on Friday if unresolved", "ROUTINE", "None required", "NONE", "CONFIRMED", "HIGH"),
]

# Ambiguity Category A: Missing Follow-up Time
CAT_A_TEMPLATES = [
    ("Patient treated for gastroenteritis with oral rehydration salts. Review the patient later.", "Review later", "ROUTINE", "When exactly should the patient return for follow-up?", "ROUTINE_CLINICIAN", "CONFIRMED", "HIGH"),
    ("Minor head injury evaluated, CT normal. Patient advised to return for follow-up after some time.", "Follow-up after some time", "ROUTINE", "What exact date or number of days should be used for follow-up?", "ROUTINE_CLINICIAN", "CONFIRMED", "HIGH"),
    ("Asthma exacerbation resolved after nebulization. Continue inhaler and come back soon.", "Come back soon", "ROUTINE", "Specify the exact follow-up interval in days or weeks.", "ROUTINE_CLINICIAN", "CONFIRMED", "MEDIUM"),
    ("Patient completed course of antibiotics for urinary tract infection. Re-assess in a few days.", "Re-assess in a few days", "ROUTINE", "Clarify the precise number of days before re-assessment.", "ROUTINE_CLINICIAN", "CONFIRMED", "HIGH"),
    ("Allergic dermatitis treated with antihistamines. Return to clinic at a convenient time.", "Return at convenient time", "ROUTINE", "Define a specific follow-up target date for clinic visit.", "ROUTINE_CLINICIAN", "MODIFIED", "HIGH"),
]

# Ambiguity Category B: Vague Duration
CAT_B_TEMPLATES = [
    ("Patient presenting with lumbar muscle strain. Continue treatment for some time.", "Continue treatment for some time", "ROUTINE", "How many days or weeks should treatment be continued?", "ROUTINE_CLINICIAN", "CONFIRMED", "HIGH"),
    ("Fungal skin infection on forearm. Apply anti-fungal ointment for a couple of days.", "Apply ointment for a couple of days", "ROUTINE", "Specify exact duration of ointment application (e.g., 7 or 14 days).", "ROUTINE_CLINICIAN", "CONFIRMED", "HIGH"),
    ("Iron deficiency anemia. Take ferrous sulfate tablets for a while then review.", "Take tablets for a while", "ROUTINE", "What is the intended treatment duration before rechecking blood count?", "ROUTINE_CLINICIAN", "CONFIRMED", "MEDIUM"),
    ("Mild gastritis symptoms. Continue PPI medication as long as needed.", "Continue PPI as long as needed", "ROUTINE", "Define maximum treatment duration and clear review threshold.", "ROUTINE_CLINICIAN", "CONFIRMED", "HIGH"),
]

# Ambiguity Category C: Vague Symptom Condition
CAT_C_TEMPLATES = [
    ("Patient started on antihypertensive therapy. Come back if symptoms get worse.", "Come back if symptoms get worse", "ROUTINE", "What specific red-flag symptoms or BP thresholds define 'worse'?", "ROUTINE_CLINICIAN", "CONFIRMED", "HIGH"),
    ("Mild bronchitis. Take cough syrup. Return to clinic if condition deteriorates.", "Return if condition deteriorates", "MODERATE", "Which specific signs (fever >38.5C, severe shortness of breath) constitute deterioration?", "ROUTINE_CLINICIAN", "CONFIRMED", "HIGH"),
    ("Post-vaccination fever and arm pain. Re-consult if patient feels unwell.", "Re-consult if feels unwell", "ROUTINE", "Clarify parameters for re-consultation (e.g., persistent fever >48 hours).", "ROUTINE_CLINICIAN", "CONFIRMED", "HIGH"),
    ("Conjunctivitis treated with antibiotic drops. Return if eyes look bad.", "Return if eyes look bad", "ROUTINE", "Define clinical indicators (increased discharge, vision change, severe pain).", "ROUTINE_CLINICIAN", "CONFIRMED", "HIGH"),
]

# Ambiguity Category D: Missing Action
CAT_D_TEMPLATES = [
    ("Patient consultation for chronic back pain. Follow-up in one week.", "Follow-up in one week", "ROUTINE", "What specific action (BP check, lab test, medication review) is required at follow-up?", "ROUTINE_CLINICIAN", "CONFIRMED", "HIGH"),
    ("Diabetic ulcer dressing changed. Clinic visit in 3 days.", "Clinic visit in 3 days", "ROUTINE", "Clarify whether visit is for dressing change, debridement, or physician review.", "ROUTINE_CLINICIAN", "CONFIRMED", "HIGH"),
    ("Pediatric fever settled. See nurse next Monday.", "See nurse next Monday", "ROUTINE", "Specify the action needed (growth monitoring, repeat temperature check, vaccination).", "ROUTINE_CLINICIAN", "CONFIRMED", "HIGH"),
    ("Elevated blood pressure observed. Review scheduled for 10th August.", "Review scheduled 10th August", "ROUTINE", "Identify required clinical procedure or test prior to review.", "ROUTINE_CLINICIAN", "CONFIRMED", "HIGH"),
]

# Ambiguity Category E: Contradictory Timing
CAT_E_TEMPLATES = [
    ("Patient with chest congestion. Review tomorrow. Follow-up after two weeks.", "Review tomorrow and after 2 weeks", "MODERATE", "Resolve conflict: Is immediate review needed tomorrow or routine follow-up in 2 weeks?", "ROUTINE_CLINICIAN", "CONFIRMED", "HIGH"),
    ("Post-operative suture care. Come back in 3 days. Return to clinic next month.", "Come back in 3 days and next month", "ROUTINE", "Confirm whether suture removal is at day 3 or 30 days.", "ROUTINE_CLINICIAN", "CONFIRMED", "HIGH"),
    ("Hypertension follow-up. Repeat BP check in 24 hours. Schedule follow-up in 6 weeks.", "Repeat BP in 24h and 6 weeks", "ROUTINE", "Clarify if 24-hour ambulatory check or 6-week routine visit is intended.", "ROUTINE_CLINICIAN", "CONFIRMED", "HIGH"),
    ("Patient started on thyroid supplement. Review in 5 days. Return after 3 months for blood test.", "Review in 5 days and 3 months", "ROUTINE", "Reconcile short-term review with 3-month blood test schedule.", "ROUTINE_CLINICIAN", "CONFIRMED", "HIGH"),
]

# Ambiguity Category F: Unclear Specialist Referral
CAT_F_TEMPLATES = [
    ("Suspected glaucoma with elevated intraocular pressure. Refer to specialist if necessary.", "Refer to specialist if necessary", "MODERATE", "Which specialist department (Ophthalmology) and under what exact criteria?", "SENIOR_CLINICIAN", "CONFIRMED", "HIGH"),
    ("Persistent abdominal pain suspicious for gallstones. Consult specialist when appropriate.", "Consult specialist when appropriate", "MODERATE", "Define referral criteria, target department (General Surgery/GI), and urgency timeline.", "SENIOR_CLINICIAN", "CONFIRMED", "HIGH"),
    ("Skin lesion showing irregular borders. Refer to expert if needed.", "Refer to expert if needed", "MODERATE", "Specify Dermatology referral trigger (biopsy result, size increase) and referral priority.", "SENIOR_CLINICIAN", "CONFIRMED", "HIGH"),
]

# Ambiguity Category G: Unclear Responsibility
CAT_G_TEMPLATES = [
    ("Patient with fluctuating blood glucose levels. Someone should review the patient.", "Someone should review the patient", "ROUTINE", "Who (duty doctor, community health nurse, endocrinologist) is responsible for review?", "ROUTINE_CLINICIAN", "CONFIRMED", "HIGH"),
    ("Post-discharge stroke rehabilitation. Patient needs to be checked regularly.", "Patient needs to be checked regularly", "ROUTINE", "Assign explicit staff role responsible for regular checks.", "ROUTINE_CLINICIAN", "CONFIRMED", "HIGH"),
    ("Complex wound dressing. The health worker ought to monitor wound site.", "Health worker ought to monitor", "ROUTINE", "Designate named healthcare provider or specific clinic role for monitoring.", "ROUTINE_CLINICIAN", "CONFIRMED", "HIGH"),
]

# Ambiguity Category H: Urgency Ambiguity
CAT_H_TEMPLATES = [
    ("Patient has worsening breathing difficulty. Review later.", "Review later despite worsening dyspnea", "HIGH", "Urgency Conflict: Severe respiratory symptom combined with delayed review. Immediate clinical evaluation required!", "IMMEDIATE_URGENT_REVIEW", "ESCALATED", "HIGH"),
    ("Acute chest pressure with radiation to left arm noted. Return if convenient.", "Return if convenient despite acute chest pain", "HIGH", "Urgency Conflict: Potential cardiac event with vague follow-up. Immediate emergency assessment required!", "IMMEDIATE_URGENT_REVIEW", "ESCALATED", "HIGH"),
    ("Severe high fever 40C with neck stiffness. Re-examine after some time.", "Re-examine after some time despite high fever and stiff neck", "HIGH", "Urgency Conflict: Meningeal signs require emergency escalation to hospital care immediately!", "IMMEDIATE_URGENT_REVIEW", "ESCALATED", "HIGH"),
    ("Child presenting with lethargy, high grade fever and vomiting. Check tomorrow if worsens.", "Check tomorrow despite severe pediatric lethargy", "HIGH", "Urgency Conflict: Pediatric red-flag symptoms require urgent emergency triage!", "IMMEDIATE_URGENT_REVIEW", "ESCALATED", "HIGH"),
    ("Post-traumatic abdominal rigidity and tachycardia. Follow-up next week.", "Follow-up next week despite acute abdomen", "HIGH", "Urgency Conflict: Suspected internal bleeding requiring immediate surgical evaluation!", "IMMEDIATE_URGENT_REVIEW", "ESCALATED", "HIGH"),
]

# Ambiguity Category I: Missing Clinical Note
CAT_I_TEMPLATES = [
    ("", "", "ROUTINE", "Clinical note is completely empty. Manual clinical review required before patient departure.", "MANUAL_REVIEW", "REJECTED", "EMPTY"),
    ("   ", "N/A", "ROUTINE", "Clinical note contains only whitespace. Manual clinical review required.", "MANUAL_REVIEW", "REJECTED", "EMPTY"),
]

# Ambiguity Category J: Low-Quality / Noisy Note
CAT_J_TEMPLATES = [
    ("follw up aftr 3 dys if condtion worsn", "follw up 3 dys", "ROUTINE", "Low-confidence transcription. Verify if 'follow up after 3 days if condition worsens' was intended.", "ROUTINE_CLINICIAN", "MODIFIED", "NOISY"),
    ("pt revw in few dyas or wks if pain persist", "pt revw few dyas", "ROUTINE", "Low-confidence text. Confirm exact follow-up interval and pain management plan.", "ROUTINE_CLINICIAN", "MODIFIED", "NOISY"),
    ("chk BP agin latr nxt wk if high", "chk BP latr", "ROUTINE", "Noisy input detected. Clarify exact target day and target blood pressure threshold.", "ROUTINE_CLINICIAN", "MODIFIED", "NOISY"),
    ("refr specist if syncp recr", "refr specist", "MODERATE", "Noisy text. Clarify referral criteria for recurrent syncope and target specialist.", "SENIOR_CLINICIAN", "MODIFIED", "NOISY"),
]

ALL_CAT_MAP = {
    "NONE": CLEAR_TEMPLATES,
    "FOLLOWUP_TIME_MISSING": CAT_A_TEMPLATES,
    "VAGUE_DURATION": CAT_B_TEMPLATES,
    "VAGUE_SYMPTOM_CONDITION": CAT_C_TEMPLATES,
    "MISSING_ACTION": CAT_D_TEMPLATES,
    "CONTRADICTORY_TIMING": CAT_E_TEMPLATES,
    "UNCLEAR_SPECIALIST_REFERRAL": CAT_F_TEMPLATES,
    "UNCLEAR_RESPONSIBILITY": CAT_G_TEMPLATES,
    "URGENCY_AMBIGUITY": CAT_H_TEMPLATES,
    "MISSING_NOTE": CAT_I_TEMPLATES,
    "NOISY_NOTE": CAT_J_TEMPLATES,
}

OVERRIDE_REASONS = [
    "NONE",
    "Already addressed",
    "Specialist already contacted",
    "Clinical context differs",
    "Patient preference",
    "Resource unavailable",
    "Recommendation not applicable",
    "False positive",
    "Other"
]

TRANSLATION_QUALITIES = [
    "STANDARD_ENGLISH",
    "ENGLISH_NATIVE",
    "DIALECT_ENGLISH",
    "TRANSLATED_ENGLISH"
]

def generate_dataset(num_records=1200):
    records = []
    
    # Calculate balance: ~20% Clear, ~80% across ambiguity categories
    cat_keys = list(ALL_CAT_MAP.keys())
    
    for i in range(1, num_records + 1):
        case_id = f"CASE-{i:04d}"
        
        # Pick category
        # Weight NONE to be ~20-25% of dataset, others distributed evenly
        if random.random() < 0.22:
            cat_code = "NONE"
        else:
            cat_code = random.choice([k for k in cat_keys if k != "NONE"])
            
        templates = ALL_CAT_MAP[cat_code]
        tmpl = random.choice(templates)
        
        clinical_note = tmpl[0]
        planned_action = tmpl[1]
        urgency_level = tmpl[2]
        expected_clarification = tmpl[3]
        expected_escalation = tmpl[4]
        human_decision = tmpl[5]
        note_quality = tmpl[6]
        
        ambiguous_flag = 0 if cat_code == "NONE" else 1
        
        # Slight realistic variations in phrasing
        if cat_code != "MISSING_NOTE" and random.random() < 0.3:
            prefix_variations = [
                "Rural Clinic Visit Note: ",
                "Consultation Summary: ",
                "Outpatient Record: ",
                "Nurse Triage Note: ",
                ""
            ]
            clinical_note = random.choice(prefix_variations) + clinical_note
            
        # Determine override reason based on decision
        if human_decision in ["MODIFIED", "REJECTED"]:
            override_reason = random.choice(OVERRIDE_REASONS[1:])
        else:
            override_reason = "NONE"
            
        clarification_outcome = "Resolved" if ambiguous_flag == 1 else "Not Required"
        translation_quality = random.choice(TRANSLATION_QUALITIES)
        
        records.append({
            "Case_ID": case_id,
            "Clinical_Note": clinical_note,
            "Planned_Action": planned_action,
            "Ambiguity_Type": cat_code,
            "Ambiguous_Flag": ambiguous_flag,
            "Urgency_Level": urgency_level,
            "Expected_Clarification": expected_clarification,
            "Expected_Escalation": expected_escalation,
            "Clarification_Outcome": clarification_outcome,
            "Human_Decision": human_decision,
            "Override_Reason": override_reason,
            "Note_Quality": note_quality,
            "Translation_Quality": translation_quality
        })
        
    df = pd.DataFrame(records)
    return df

if __name__ == "__main__":
    out_dir = os.path.dirname(os.path.abspath(__file__))
    os.makedirs(out_dir, exist_ok=True)
    csv_path = os.path.join(out_dir, "synthetic_consultation_notes.csv")
    
    print(f"Generating 1,200 synthetic consultation notes...")
    df = generate_dataset(1200)
    df.to_csv(csv_path, index=False)
    print(f"Dataset successfully saved to: {csv_path}")
    print(f"Total Records: {len(df)}")
    print(f"Ambiguity Distribution:\n{df['Ambiguity_Type'].value_counts()}")
