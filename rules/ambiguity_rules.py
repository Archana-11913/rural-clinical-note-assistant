"""
Ambiguity Detection Rules Engine & NLP Pipeline
Includes both Baseline System (Regex/Keyword) and Proposed System (Explainable Engine).
"""

import re
import math
from typing import Dict, Any, Union

class BaselineAmbiguityDetector:
    """
    Baseline Rule-Based Ambiguity Detector.
    Uses basic keyword matching and standard regexes to flag potential ambiguity.
    """
    def __init__(self):
        self.vague_time_keywords = [
            "later", "soon", "after some time", "few days", "some time", "convenient time"
        ]
        self.vague_condition_keywords = [
            "if necessary", "if needed", "when appropriate", "if worse", "if feels unwell"
        ]
        self.time_regex = re.compile(
            r'\b(\d+\s*(days?|weeks?|months?|hours?)|tomorrow|next week|next month)\b',
            re.IGNORECASE
        )

    def analyze(self, clinical_note: Any) -> Dict[str, Any]:
        if clinical_note is None or (isinstance(clinical_note, float) and (math.isnan(clinical_note) or clinical_note != clinical_note)):
            clinical_note = ""
        else:
            clinical_note = str(clinical_note)
            
        if not clinical_note or not clinical_note.strip():
            return {
                "is_ambiguous": True,
                "ambiguity_type": "MISSING_NOTE",
                "confidence": "High"
            }
            
        note_lower = clinical_note.lower()
        
        # 1. Contradiction check: multiple time expressions
        matches = self.time_regex.findall(note_lower)
        if len(matches) >= 2:
            return {
                "is_ambiguous": True,
                "ambiguity_type": "CONTRADICTORY_TIMING",
                "confidence": "Medium"
            }
            
        # 2. Vague time check
        for kw in self.vague_time_keywords:
            if kw in note_lower:
                return {
                    "is_ambiguous": True,
                    "ambiguity_type": "FOLLOWUP_TIME_MISSING",
                    "confidence": "Medium"
                }
                
        # 3. Unclear condition / referral
        for kw in self.vague_condition_keywords:
            if kw in note_lower:
                return {
                    "is_ambiguous": True,
                    "ambiguity_type": "UNCLEAR_SPECIALIST_REFERRAL" if "specialist" in note_lower or "refer" in note_lower else "VAGUE_SYMPTOM_CONDITION",
                    "confidence": "Medium"
                }
                
        return {
            "is_ambiguous": False,
            "ambiguity_type": "NONE",
            "confidence": "High"
        }


class ProposedAmbiguityAssistant:
    """
    Proposed Explainable Clinical Note Clarification Assistant.
    Provides structured, transparent decision support with confidence & evidence.
    """
    def __init__(self):
        # Urgent symptom indicators
        self.urgent_symptoms = [
            "worsening breathing difficulty", "breathing difficulty", "dyspnea",
            "chest pressure", "chest pain", "radiation to left arm",
            "high fever", "neck stiffness", "lethargy",
            "abdominal rigidity", "tachycardia", "severe bleeding"
        ]
        # Delayed / routine follow-up indicators
        self.routine_delays = [
            "review later", "return if convenient", "re-examine after some time",
            "check tomorrow if worsens", "follow-up next week", "review after a few days",
            "later", "next week", "after some time"
        ]
        
        # Contradiction patterns
        self.contradiction_pairs = [
            (r'tomorrow', r'two weeks|2 weeks|next month'),
            (r'3 days', r'next month|30 days'),
            (r'24 hours|24h', r'6 weeks'),
            (r'5 days', r'3 months')
        ]
        
        # Vague duration patterns
        self.vague_durations = [
            "some time", "couple of days", "a while", "as long as needed", "for a bit"
        ]
        
        # Vague condition patterns
        self.vague_conditions = [
            "get worse", "condition deteriorates", "feels unwell", "eyes look bad", "pain persist"
        ]

    def analyze(self, clinical_note: Any, planned_action: Any = "") -> Dict[str, Any]:
        if clinical_note is None or (isinstance(clinical_note, float) and (math.isnan(clinical_note) or clinical_note != clinical_note)):
            clinical_note = ""
        else:
            clinical_note = str(clinical_note)

        if planned_action is None or (isinstance(planned_action, float) and (math.isnan(planned_action) or planned_action != planned_action)):
            planned_action = ""
        else:
            planned_action = str(planned_action)

        # Handle empty/missing clinical note
        if not clinical_note or not clinical_note.strip():
            return {
                "is_ambiguous": True,
                "ambiguity_category": "MISSING_NOTE",
                "issue_description": "Clinical note is completely empty or missing.",
                "confidence": "High",
                "evidence": "[Empty input]",
                "triggered_rule": "Empty note detection rule",
                "suggested_clarification": "Manual clinical review required. Please document the patient consultation note before departure.",
                "recommended_next_step": "Hold departure and obtain full clinical documentation from attending provider.",
                "escalation_level": "MANUAL_REVIEW",
                "human_confirmation_required": "Human confirmation required",
                "uncertainty_warning": "Unable to safely assess the case because the clinical note is missing. Manual review is required."
            }

        note_lower = clinical_note.lower()

        # Check 1: Urgent Escalation Conflict (Category H)
        for surg in self.urgent_symptoms:
            if surg in note_lower:
                for rdelay in self.routine_delays:
                    if rdelay in note_lower or "later" in note_lower or "next week" in note_lower:
                        return {
                            "is_ambiguous": True,
                            "ambiguity_category": "URGENCY_AMBIGUITY",
                            "issue_description": "Potential urgent clinical wording conflicts with a routine or delayed follow-up instruction.",
                            "confidence": "High",
                            "evidence": f"Urgent symptom: '{surg}' | Routine follow-up phrase: '{rdelay}'",
                            "triggered_rule": "Urgent Symptom vs Routine Delay Conflict Rule",
                            "suggested_clarification": "Is immediate emergency triage required rather than routine outpatient follow-up?",
                            "recommended_next_step": "Initiate immediate human clinical review and transfer to urgent care pathway if confirmed.",
                            "escalation_level": "IMMEDIATE_URGENT_REVIEW",
                            "human_confirmation_required": "Human confirmation required",
                            "uncertainty_warning": "Potential urgency conflict detected. Immediate human clinical review required!"
                        }

        # Check 2: Contradictory Timing (Category E)
        for p1, p2 in self.contradiction_pairs:
            if re.search(p1, note_lower) and re.search(p2, note_lower):
                m1 = re.search(p1, note_lower).group(0)
                m2 = re.search(p2, note_lower).group(0)
                return {
                    "is_ambiguous": True,
                    "ambiguity_category": "CONTRADICTORY_TIMING",
                    "issue_description": "Two conflicting follow-up timing milestones detected in clinical note.",
                    "confidence": "High",
                    "evidence": f"Conflicting milestones: '{m1}' vs '{m2}'",
                    "triggered_rule": "Multiple Conflicting Temporal Milestones Rule",
                    "suggested_clarification": "Which timing milestone should be scheduled for the patient (short-term review vs long-term)?",
                    "recommended_next_step": "Confirm correct follow-up timeframe with responsible clinician prior to discharge.",
                    "escalation_level": "ROUTINE_CLINICIAN",
                    "human_confirmation_required": "Human confirmation required",
                    "uncertainty_warning": None
                }

        # Check 3: Low-Quality / Noisy Note (Category J)
        noisy_indicators = ["follw up", "aftr", "dys", "worsn", "pt revw", "dyas", "chk bp", "latr", "refr specist", "syncp"]
        noisy_matches = [kw for kw in noisy_indicators if kw in note_lower]
        if len(noisy_matches) >= 2 or (len(noisy_matches) >= 1 and len(clinical_note) < 45):
            return {
                "is_ambiguous": True,
                "ambiguity_category": "NOISY_NOTE",
                "issue_description": "Clinical note contains severe spelling noise or transcription shorthand.",
                "confidence": "Low",
                "evidence": f"Noisy tokens detected: {', '.join(noisy_matches)}",
                "triggered_rule": "Noisy / Non-standard Clinical Text Rule",
                "suggested_clarification": "Can the clinician verify the exact follow-up interval and conditions intended?",
                "recommended_next_step": "Human clinician confirmation required to verify intended words.",
                "escalation_level": "ROUTINE_CLINICIAN",
                "human_confirmation_required": "Human confirmation required",
                "uncertainty_warning": "Low-confidence interpretation. The note may contain transcription or spelling errors. Human confirmation is required."
            }

        # Check 4: Unclear Specialist Referral (Category F)
        if any(term in note_lower for term in ["refer to specialist", "consult specialist", "refer to expert", "refr specist"]):
            if any(qual in note_lower for qual in ["if necessary", "when appropriate", "if needed"]):
                return {
                    "is_ambiguous": True,
                    "ambiguity_category": "UNCLEAR_SPECIALIST_REFERRAL",
                    "issue_description": "Specialist referral indicated but referral criteria and specialty are ambiguous.",
                    "confidence": "High",
                    "evidence": "Phrases detected: 'refer to specialist if necessary' / 'when appropriate'",
                    "triggered_rule": "Conditional Specialist Referral Ambiguity Rule",
                    "suggested_clarification": "Which specific specialist clinic is required and what specific clinical triggers warrant referral?",
                    "recommended_next_step": "Specify referral specialty and trigger criteria in discharge paper.",
                    "escalation_level": "SENIOR_CLINICIAN",
                    "human_confirmation_required": "Human confirmation required",
                    "uncertainty_warning": None
                }

        # Check 5: Unclear Responsibility (Category G)
        if any(term in note_lower for term in ["someone should review", "needs to be checked", "health worker ought to"]):
            return {
                "is_ambiguous": True,
                "ambiguity_category": "UNCLEAR_RESPONSIBILITY",
                "issue_description": "Follow-up responsibility assigned to an unspecified or vague party.",
                "confidence": "High",
                "evidence": "Impersonal phrase detected: 'someone should review' / 'needs to be checked'",
                "triggered_rule": "Unclear Care Provider Responsibility Rule",
                "suggested_clarification": "Which specific health worker or clinician is designated responsible for follow-up?",
                "recommended_next_step": "Assign named provider or role to the follow-up instruction.",
                "escalation_level": "ROUTINE_CLINICIAN",
                "human_confirmation_required": "Human confirmation required",
                "uncertainty_warning": None
            }

        # Check 6: Vague Duration (Category B)
        for vdur in self.vague_durations:
            if vdur in note_lower:
                return {
                    "is_ambiguous": True,
                    "ambiguity_category": "VAGUE_DURATION",
                    "issue_description": "Treatment or medication duration is vaguely defined.",
                    "confidence": "High",
                    "evidence": f"Vague duration phrase: '{vdur}'",
                    "triggered_rule": "Unspecified Treatment Duration Rule",
                    "suggested_clarification": "What is the exact number of days/weeks the treatment should continue?",
                    "recommended_next_step": "Specify clear end date or exact day count for medication.",
                    "escalation_level": "ROUTINE_CLINICIAN",
                    "human_confirmation_required": "Human confirmation required",
                    "uncertainty_warning": None
                }

        # Check 7: Vague Symptom Condition (Category C)
        for vcond in self.vague_conditions:
            if vcond in note_lower:
                return {
                    "is_ambiguous": True,
                    "ambiguity_category": "VAGUE_SYMPTOM_CONDITION",
                    "issue_description": "Return condition depends on vague symptom worsening without defined red flags.",
                    "confidence": "High",
                    "evidence": f"Vague condition phrase: '{vcond}'",
                    "triggered_rule": "Vague Symptom Aggravation Trigger Rule",
                    "suggested_clarification": "What specific measurable signs or red-flag symptoms define 'worse'?",
                    "recommended_next_step": "Provide patient with specific written red-flag symptoms for return.",
                    "escalation_level": "ROUTINE_CLINICIAN",
                    "human_confirmation_required": "Human confirmation required",
                    "uncertainty_warning": None
                }

        # Check 8: Missing Follow-up Time (Category A)
        vague_time_phrases = ["review later", "after some time", "come back soon", "in a few days", "convenient time", "review the patient later"]
        for vtime in vague_time_phrases:
            if vtime in note_lower or ("later" in note_lower and "follow" not in note_lower and "scheduled" not in note_lower):
                return {
                    "is_ambiguous": True,
                    "ambiguity_category": "FOLLOWUP_TIME_MISSING",
                    "issue_description": "Follow-up timeframe is missing or vaguely specified.",
                    "confidence": "High",
                    "evidence": f"Vague time phrase: '{vtime if vtime in note_lower else 'later'}'",
                    "triggered_rule": "Unspecified Follow-up Timeframe Rule",
                    "suggested_clarification": "What exact calendar date or number of days should be set for follow-up?",
                    "recommended_next_step": "Confirm specific follow-up interval with clinician before discharge.",
                    "escalation_level": "ROUTINE_CLINICIAN",
                    "human_confirmation_required": "Human confirmation required",
                    "uncertainty_warning": None
                }

        # Check 9: Missing Action (Category D)
        if any(term in note_lower for term in ["follow-up in one week", "clinic visit in 3 days", "see nurse next monday", "review scheduled"]):
            if not any(act in note_lower for act in ["bp", "lab", "wound", "dressing", "suture", "medication", "blood"]):
                return {
                    "is_ambiguous": True,
                    "ambiguity_category": "MISSING_ACTION",
                    "issue_description": "Follow-up time is mentioned but specific clinical action is omitted.",
                    "confidence": "High",
                    "evidence": "Follow-up timing present without clinical action details.",
                    "triggered_rule": "Missing Follow-up Action Rule",
                    "suggested_clarification": "What specific action or procedure is scheduled during the follow-up visit?",
                    "recommended_next_step": "Record specific objective of follow-up visit.",
                    "escalation_level": "ROUTINE_CLINICIAN",
                    "human_confirmation_required": "Human confirmation required",
                    "uncertainty_warning": None
                }

        # Default: Clear Note
        return {
            "is_ambiguous": False,
            "ambiguity_category": "NONE",
            "issue_description": "Clinical note contains clear, unambiguous follow-up instructions.",
            "confidence": "High",
            "evidence": "Specific date, duration, or procedure explicitly stated.",
            "triggered_rule": "Unambiguous Clinical Instruction Rule",
            "suggested_clarification": "None required.",
            "recommended_next_step": "Proceed with standard patient discharge workflow.",
            "escalation_level": "NONE",
            "human_confirmation_required": "Optional",
            "uncertainty_warning": None
        }
