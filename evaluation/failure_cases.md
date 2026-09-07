# Failure Case Analysis & Test Cases

This document details 6 benchmark failure and edge cases evaluated on the **Clinical Note Clarification Assistant**.

---

## Test Case 1: Missing Follow-up Time

* **Input Clinical Note**: `"Review the patient later."`
* **Expected Result**: Ambiguity detected (`FOLLOWUP_TIME_MISSING`).
* **Actual System Result**: Ambiguity detected (`FOLLOWUP_TIME_MISSING`).
* **System Confidence**: `High`
* **Evidence**: `"Vague time phrase: 'later'"`
* **Suggested Clarification**: `"What exact date or number of days should be used for follow-up?"`
* **Human Action**: `CONFIRMED`
* **Escalation Occurred**: No (`ROUTINE_CLINICIAN`)
* **Lessons Learned**: Keyword matching for "later" is effective, but requiring explicit day counts prevents premature patient departure.

---

## Test Case 2: Contradictory Follow-up Instructions

* **Input Clinical Note**: `"Review tomorrow. Follow-up after two weeks."`
* **Expected Result**: Contradictory timing detected (`CONTRADICTORY_TIMING`).
* **Actual System Result**: Contradictory timing detected (`CONTRADICTORY_TIMING`).
* **System Confidence**: `High`
* **Evidence**: `"Conflicting milestones: 'tomorrow' vs 'two weeks'"`
* **Suggested Clarification**: `"Which timing milestone should be scheduled for the patient (short-term review vs long-term)?"`
* **Human Action**: `CONFIRMED` (Clinician clarified 24-hour review needed).
* **Escalation Occurred**: No (`ROUTINE_CLINICIAN`)
* **Lessons Learned**: Flagging dual timelines prevents clinic staff from scheduling conflicting appointment dates.

---

## Test Case 3: Empty Clinical Note

* **Input Clinical Note**: `""` (Empty string)
* **Expected Result**: Manual review required (`MISSING_NOTE`).
* **Actual System Result**: Manual review required (`MISSING_NOTE`).
* **System Confidence**: `High`
* **Evidence**: `"[Empty input]"`
* **Suggested Clarification**: `"Clinical note is missing. Manual review required."`
* **Human Action**: `REJECTED` / `ESCALATED` (Held departure until clinician documented note).
* **Escalation Occurred**: Yes (`MANUAL_REVIEW`)
* **Lessons Learned**: System must fail safely when input is missing to prevent patient discharge without written care instructions.

---

## Test Case 4: Noisy / Low-Quality Clinical Note

* **Input Clinical Note**: `"follw up aftr 3 dys if condtion worsn"`
* **Expected Result**: Low-confidence interpretation (`NOISY_NOTE`).
* **Actual System Result**: Low-confidence interpretation (`NOISY_NOTE`).
* **System Confidence**: `Low`
* **Evidence**: `"Noisy tokens detected: follw up, dys, worsn"`
* **Uncertainty Warning**: `"Low-confidence interpretation. The note may contain transcription or spelling errors. Human confirmation is required."`
* **Human Action**: `MODIFIED` (Clinician confirmed: "Follow-up in 3 days if condition worsens").
* **Escalation Occurred**: No (`ROUTINE_CLINICIAN`)
* **Lessons Learned**: System should flag uncertainty rather than hallucinating or assuming text intent.

---

## Test Case 5: Potential Urgent Case

* **Input Clinical Note**: `"Patient has worsening breathing difficulty. Review later."`
* **Expected Result**: Potential urgency conflict detected (`URGENCY_AMBIGUITY`).
* **Actual System Result**: Potential urgency conflict detected (`URGENCY_AMBIGUITY`).
* **System Confidence**: `High`
* **Evidence**: `"Urgent symptom: 'worsening breathing difficulty' | Routine follow-up phrase: 'later'"`
* **Suggested Clarification**: `"Is immediate emergency triage required rather than routine outpatient follow-up?"`
* **Human Action**: `ESCALATED` (Transferred to emergency oxygen triage).
* **Escalation Occurred**: Yes (`IMMEDIATE_URGENT_REVIEW`)
* **Lessons Learned**: Catching urgency conflicts before patient departure prevents fatal delays in emergency care.

---

## Test Case 6: Ambiguous Instruction with Insufficient Context

* **Input Clinical Note**: `"Patient needs follow-up soon if pain continues."`
* **Expected Result**: Dual Ambiguity Flag (`FOLLOWUP_TIME_MISSING` / `VAGUE_SYMPTOM_CONDITION`).
* **Actual System Result**: Ambiguity flagged (`FOLLOWUP_TIME_MISSING`).
* **System Confidence**: `High`
* **Evidence**: `"Vague time phrase: 'soon'"`
* **Suggested Clarification**: `"What specific date and pain scale threshold warrant return?"`
* **Human Action**: `MODIFIED`
* **Escalation Occurred**: No (`ROUTINE_CLINICIAN`)
* **Lessons Learned**: Multi-label ambiguity triggers should be surfaced in heirarchical priority order.
