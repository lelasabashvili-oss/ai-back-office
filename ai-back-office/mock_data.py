from datetime import date, timedelta
import random

TODAY = date.today().isoformat()

PATIENTS = [
    {"id": "P001", "name": "Maria Gonzalez", "dob": "1985-03-12", "insurance": "Aetna", "member_id": "AET8823110", "phone": "917-555-0142", "condition": "Type 2 Diabetes, Obesity", "provider_notes": "GLP-1 candidate; started Zepbound 2.5mg in Jan 2026"},
    {"id": "P002", "name": "Sarah Chen", "dob": "1991-07-28", "insurance": "Blue Cross Blue Shield", "member_id": "BCBS449201", "phone": "212-555-0387", "condition": "Obesity, PCOS", "provider_notes": "On Wegovy 0.5mg; needs nutrition follow-up monthly"},
    {"id": "P003", "name": "James Okafor", "dob": "1978-11-05", "insurance": "UnitedHealthcare", "member_id": "UHC2290045", "phone": "646-555-0219", "condition": "Prediabetes, Hypertension", "provider_notes": "Referred by PCP; insurance nutrition benefit active"},
    {"id": "P004", "name": "Linda Park", "dob": "1967-04-19", "insurance": "Cigna", "member_id": "CIG5501872", "phone": "718-555-0491", "condition": "Celiac Disease, Malnutrition", "provider_notes": "Medical nutrition therapy; 3 sessions approved"},
    {"id": "P005", "name": "David Ruiz", "dob": "1995-09-03", "insurance": "Aetna", "member_id": "AET6641093", "phone": "347-555-0728", "condition": "Eating Disorder, Anxiety", "provider_notes": "Collaborative care with therapist Dr. Kim"},
    {"id": "P006", "name": "Angela Torres", "dob": "1982-02-14", "insurance": "Humana", "member_id": "HUM3310567", "phone": "929-555-0055", "condition": "Obesity, Sleep Apnea", "provider_notes": "GLP-1 interest; prior auth pending for Wegovy"},
    {"id": "P007", "name": "Michael Flynn", "dob": "1959-12-30", "insurance": "Medicare", "member_id": "MCR1A2B3C4D", "phone": "516-555-0811", "condition": "CKD Stage 3, Diabetes", "provider_notes": "MNT covered under Medicare; 3 hours/year"},
    {"id": "P008", "name": "Priya Patel", "dob": "1988-06-22", "insurance": "Blue Cross Blue Shield", "member_id": "BCBS772910", "phone": "201-555-0334", "condition": "Gestational Diabetes", "provider_notes": "Third trimester; weekly check-ins"},
]

APPOINTMENTS = [
    {"id": "A001", "patient_id": "P002", "patient_name": "Sarah Chen", "time": "09:00 AM", "duration": 45, "type": "GLP-1 Follow-up", "status": "confirmed", "notes": "Monthly Wegovy check-in; review side effects and nutrition adherence"},
    {"id": "A002", "patient_id": "P008", "patient_name": "Priya Patel", "time": "10:00 AM", "duration": 30, "type": "Nutrition Counseling", "status": "confirmed", "notes": "Week 34 gestational diabetes management"},
    {"id": "A003", "patient_id": "P003", "patient_name": "James Okafor", "time": "11:30 AM", "duration": 60, "type": "Initial Assessment", "status": "confirmed", "notes": "New patient intake; full dietary assessment"},
    {"id": "A004", "patient_id": "P006", "patient_name": "Angela Torres", "time": "01:00 PM", "duration": 45, "type": "GLP-1 Consultation", "status": "confirmed", "notes": "Prior auth review; discuss Wegovy candidacy"},
    {"id": "A005", "patient_id": "P001", "patient_name": "Maria Gonzalez", "time": "02:30 PM", "duration": 30, "type": "GLP-1 Follow-up", "status": "confirmed", "notes": "Zepbound dose titration check; review labs"},
    {"id": "A006", "patient_id": "P007", "patient_name": "Michael Flynn", "time": "04:00 PM", "duration": 45, "type": "Medical Nutrition Therapy", "status": "confirmed", "notes": "CKD diet compliance review; phosphorus & potassium tracking"},
]

CLAIMS = [
    {
        "id": "CLM-2026-0441",
        "patient_id": "P001",
        "patient_name": "Maria Gonzalez",
        "payer": "Aetna",
        "cpt_codes": ["97802", "97803"],
        "icd_codes": ["E11.9", "E66.9"],
        "service_date": "2026-04-28",
        "amount": 285.00,
        "status": "denied",
        "denial_reason": "Missing prior authorization for medical nutrition therapy",
        "denial_date": "2026-05-02",
        "denial_risk": 88,
        "appeal_deadline": "2026-06-02",
        "notes": "Appeal needed — prior auth was approved but not attached to claim"
    },
    {
        "id": "CLM-2026-0439",
        "patient_id": "P002",
        "patient_name": "Sarah Chen",
        "payer": "Blue Cross Blue Shield",
        "cpt_codes": ["99213", "S9470"],
        "icd_codes": ["E66.01", "E28.2"],
        "service_date": "2026-04-22",
        "amount": 195.00,
        "status": "pending",
        "denial_risk": 62,
        "notes": "High denial risk — BCBS frequently denies S9470 without nutritional assessment documentation"
    },
    {
        "id": "CLM-2026-0435",
        "patient_id": "P003",
        "patient_name": "James Okafor",
        "payer": "UnitedHealthcare",
        "cpt_codes": ["97802"],
        "icd_codes": ["R73.09", "I10"],
        "service_date": "2026-04-15",
        "amount": 155.00,
        "status": "paid",
        "paid_amount": 124.00,
        "paid_date": "2026-05-01",
        "denial_risk": 12,
        "notes": "Paid at contracted rate; $31 patient responsibility"
    },
    {
        "id": "CLM-2026-0448",
        "patient_id": "P004",
        "patient_name": "Linda Park",
        "payer": "Cigna",
        "cpt_codes": ["97802", "97803", "97804"],
        "icd_codes": ["K90.0", "E46"],
        "service_date": "2026-05-06",
        "amount": 420.00,
        "status": "pre-flight",
        "denial_risk": 34,
        "notes": "Ready to file — low risk, Cigna covers MNT for Celiac with active approval"
    },
    {
        "id": "CLM-2026-0446",
        "patient_id": "P006",
        "patient_name": "Angela Torres",
        "payer": "Humana",
        "cpt_codes": ["J3490"],
        "icd_codes": ["E66.01", "G47.33"],
        "service_date": "2026-05-01",
        "amount": 890.00,
        "status": "pre-flight",
        "denial_risk": 91,
        "notes": "CRITICAL — Humana prior auth not confirmed for Wegovy. File will be denied. Needs PA documentation."
    },
    {
        "id": "CLM-2026-0431",
        "patient_id": "P007",
        "patient_name": "Michael Flynn",
        "payer": "Medicare",
        "cpt_codes": ["97802"],
        "icd_codes": ["N18.3", "E11.9"],
        "service_date": "2026-04-10",
        "amount": 145.00,
        "status": "paid",
        "paid_amount": 116.00,
        "paid_date": "2026-04-28",
        "denial_risk": 8,
        "notes": "Clean Medicare MNT claim; paid at 80% of allowed amount"
    },
    {
        "id": "CLM-2026-0450",
        "patient_id": "P008",
        "patient_name": "Priya Patel",
        "payer": "Blue Cross Blue Shield",
        "cpt_codes": ["97802", "97803"],
        "icd_codes": ["O24.419"],
        "service_date": "2026-05-07",
        "amount": 265.00,
        "status": "pre-flight",
        "denial_risk": 18,
        "notes": "Gestational diabetes MNT — BCBS covers; attach OB referral to avoid denial"
    },
]

PAYER_DENIAL_PATTERNS = {
    "Aetna": {
        "avg_denial_rate": 0.22,
        "common_denials": ["Missing prior auth", "Non-covered CPT", "Insufficient documentation"],
        "glp1_denial_rate": 0.55,
        "tips": "Always attach prior auth number in Box 23. Aetna requires dietitian NPI in Box 24J."
    },
    "Blue Cross Blue Shield": {
        "avg_denial_rate": 0.18,
        "common_denials": ["Medical necessity not established", "Duplicate claim", "Missing referral"],
        "glp1_denial_rate": 0.48,
        "tips": "BCBS requires nutritional assessment (MNA or SGA) attached for MNT claims. S9470 needs supporting documentation."
    },
    "UnitedHealthcare": {
        "avg_denial_rate": 0.15,
        "common_denials": ["Out-of-network", "Authorization required", "Timely filing exceeded"],
        "glp1_denial_rate": 0.42,
        "tips": "UHC processes fastest. File within 90 days. Always verify in-network status before visit."
    },
    "Cigna": {
        "avg_denial_rate": 0.14,
        "common_denials": ["Non-covered benefit", "Coordination of benefits"],
        "glp1_denial_rate": 0.38,
        "tips": "Cigna is most provider-friendly. Attach diagnosis letter for specialty nutrition diagnoses."
    },
    "Humana": {
        "avg_denial_rate": 0.26,
        "common_denials": ["Prior auth required", "Investigational treatment", "Formulary exclusion"],
        "glp1_denial_rate": 0.72,
        "tips": "Humana has highest GLP-1 prior auth denial rate. Always confirm PA before filing. Require step therapy documentation."
    },
    "Medicare": {
        "avg_denial_rate": 0.09,
        "common_denials": ["Frequency limit exceeded", "Not medically necessary"],
        "glp1_denial_rate": 0.35,
        "tips": "Medicare MNT: 3 hours first year, 2 hours subsequent years for diabetes/CKD. Track hours carefully."
    }
}

def get_context_for_claude():
    """Returns a structured context string for the Claude system prompt."""
    claims_summary = []
    for c in CLAIMS:
        risk_label = "CRITICAL" if c["denial_risk"] >= 80 else "HIGH" if c["denial_risk"] >= 60 else "MEDIUM" if c["denial_risk"] >= 30 else "LOW"
        claims_summary.append(
            f"- {c['id']}: {c['patient_name']} | {c['payer']} | ${c['amount']} | Status: {c['status'].upper()} | Denial Risk: {c['denial_risk']}% ({risk_label}) | CPT: {', '.join(c['cpt_codes'])} | Notes: {c['notes']}"
        )

    schedule_summary = [
        f"- {a['time']}: {a['patient_name']} ({a['type']}, {a['duration']}min) — {a['notes']}"
        for a in APPOINTMENTS
    ]

    patient_summary = [
        f"- {p['name']} (ID: {p['id']}): {p['insurance']} #{p['member_id']} | {p['condition']}"
        for p in PATIENTS
    ]

    return f"""TODAY'S DATE: {TODAY}

TODAY'S SCHEDULE ({len(APPOINTMENTS)} appointments):
{chr(10).join(schedule_summary)}

CLAIMS DASHBOARD ({len(CLAIMS)} claims):
{chr(10).join(claims_summary)}

PATIENT ROSTER:
{chr(10).join(patient_summary)}

PAYER INTELLIGENCE:
- Aetna avg denial rate: 22% | GLP-1 denial rate: 55%
- BCBS avg denial rate: 18% | GLP-1 denial rate: 48%
- UnitedHealthcare avg denial rate: 15% | GLP-1 denial rate: 42%
- Humana avg denial rate: 26% | GLP-1 denial rate: 72% (HIGHEST)
- Medicare avg denial rate: 9%"""
