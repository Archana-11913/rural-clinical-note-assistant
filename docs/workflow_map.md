# Field Workflow Map: Rural Clinic Pre-Departure Clarification

```
+-------------------------------------------------------+
|                 Patient Consultation                 |
+-------------------------------------------------------+
                           |
                           v
+-------------------------------------------------------+
|                Clinical Note Created                  |
+-------------------------------------------------------+
                           |
                           v
+-------------------------------------------------------+
|         Note Clarification Assistant Execution        |
+-------------------------------------------------------+
                           |
                           v
            +--------------+--------------+
            |  Check for Ambiguity & Risk |
            +--------------+--------------+
                           |
             +-------------+-------------+
             |                           |
             v                           v
     [ Status: CLEAR ]           [ Status: AMBIGUOUS / URGENT ]
             |                           |
             v                           v
+------------------------+   +------------------------------------+
| Continue Normal        |   | Show Structured Explanation        |
| Discharge Workflow     |   | - Ambiguity Category & Confidence  |
+------------------------+   | - Extracted Evidence & Trigger Rule|
             |               | - Suggested Clarification Question |
             |               | - Recommended Next Step            |
             |               +------------------------------------+
             |                           |
             |                           v
             |               +------------------------------------+
             |               | Human Clinician Review             |
             |               | (Must Review Before Departure)     |
             |               +------------------------------------+
             |                           |
             |         +-----------------+-----------------+
             |         |                 |                 |
             |         v                 v                 v
             |    [ Confirm ]      [ Modify/Reject ]  [ Escalate ]
             |         |                 |                 |
             |         |                 v                 v
             |         |           Record Override    Urgent Care
             |         |               Reason           Pathway
             |         |                 |                 |
             |         +-----------------+-----------------+
             |                           |
             |                           v
             |               +------------------------------------+
             |               | Record Decision in Audit Log       |
             |               +------------------------------------+
             |                           |
             +---------------------------+
                           |
                           v
+-------------------------------------------------------+
|                   Patient Departure                   |
+-------------------------------------------------------+
```

## Key Clinical Timing Requirement:
The system is explicitly designed to execute **BEFORE** the patient departs the clinic. Identifying ambiguity at the point of care empowers clinical staff to clarify instructions directly with the prescribing healthcare provider, reducing post-consultation errors, readmissions, and patient confusion.
