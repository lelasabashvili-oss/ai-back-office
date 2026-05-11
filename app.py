import os
import json
import asyncio
from fastapi import FastAPI, Request
from fastapi.responses import StreamingResponse, HTMLResponse, FileResponse
from fastapi.staticfiles import StaticFiles
from fastapi.middleware.cors import CORSMiddleware
from pathlib import Path
import anthropic
from dotenv import load_dotenv
from mock_data import PATIENTS, APPOINTMENTS, CLAIMS, PAYER_DENIAL_PATTERNS, get_context_for_claude

load_dotenv()

app = FastAPI(title="AI Back Office")
app.add_middleware(CORSMiddleware, allow_origins=["*"], allow_methods=["*"], allow_headers=["*"])

client = anthropic.AsyncAnthropic(api_key=os.getenv("ANTHROPIC_API_KEY"))

SYSTEM_PROMPT = """You are ARIA — AI Revenue & Intake Assistant — the AI back-office admin for a solo wellness practice. You work for a nutritionist/integrative health provider who sees patients and bills insurance.

Your job is to act exactly like an expert human admin who knows the practice inside-out. You handle scheduling questions, claim status, patient communications, SOAP notes, appeal letters, prior auth, CPT/ICD coding, and denial risk analysis.

CRITICAL RULES:
- Be concise and direct. Providers are busy. No fluff.
- When asked about schedule, claims, or patients — use the real data below.
- When you see a high-denial-risk claim, proactively warn about it.
- When drafting letters (appeals, patient messages) — write the full letter, ready to send/submit.
- Always suggest the next action (e.g., "Want me to draft the appeal letter?")
- You can generate SOAP notes from brief visit descriptions. Use standard clinical format.
- For CPT/ICD suggestions, be specific and accurate for nutrition/wellness/GLP-1 billing.
- Never say "I don't have access to" — you DO have access to the practice data below.

SOAP NOTE FORMAT:
S (Subjective): What patient reports
O (Objective): Measurable findings, vitals, labs
A (Assessment): Clinical assessment, diagnoses
P (Plan): Treatment plan, follow-up, prescriptions

CPT CODES YOU COMMONLY USE:
- 97802: Medical nutrition therapy, initial assessment, 15 min
- 97803: Medical nutrition therapy, re-assessment, 15 min
- 97804: Medical nutrition therapy, group, 30 min
- 99213/99214: Office visit, established patient (moderate complexity)
- S9470: Nutritional counseling for obesity
- J3490: Unclassified drug (GLP-1 medications)
- G0270: MNT for obesity when referred by physician

ICD-10 CODES YOU COMMONLY USE:
- E11.9: Type 2 diabetes mellitus without complications
- E66.01: Morbid obesity due to excess calories
- E66.9: Obesity, unspecified
- E28.2: PCOS
- R73.09: Prediabetes
- O24.419: Gestational diabetes
- K90.0: Celiac disease
- N18.3: CKD Stage 3

PRACTICE DATA:
""" + get_context_for_claude() + """

BEHAVIOR:
- If provider asks "what's my schedule" or "what do I have today" → list today's appointments
- If provider asks about a specific patient → pull their info and any pending claims
- If provider asks about a claim → give full status + denial risk + recommended action
- If provider asks to "appeal" a claim → draft a complete, payer-specific appeal letter
- If provider asks to "write a SOAP note" → ask for brief visit summary then generate it
- If provider asks about denial risk → explain the risk factors and how to fix before filing
- If provider says "what needs attention" → highlight critical-risk claims and urgent items
"""

@app.get("/", response_class=HTMLResponse)
async def serve_app():
    html_path = Path("static/index.html")
    return HTMLResponse(html_path.read_text())

@app.get("/api/data")
async def get_data():
    return {
        "patients": PATIENTS,
        "appointments": APPOINTMENTS,
        "claims": CLAIMS,
        "payer_patterns": PAYER_DENIAL_PATTERNS,
    }

@app.post("/api/chat")
async def chat(request: Request):
    body = await request.json()
    messages = body.get("messages", [])

    async def stream_response():
        async with client.messages.stream(
            model="claude-sonnet-4-6",
            max_tokens=1500,
            system=SYSTEM_PROMPT,
            messages=messages,
        ) as stream:
            async for text in stream.text_stream:
                yield f"data: {json.dumps({'text': text})}\n\n"
        yield "data: [DONE]\n\n"

    return StreamingResponse(
        stream_response(),
        media_type="text/event-stream",
        headers={
            "Cache-Control": "no-cache",
            "X-Accel-Buffering": "no",
        }
    )

@app.post("/api/denial-check")
async def denial_check(request: Request):
    body = await request.json()
    claim_id = body.get("claim_id")
    claim = next((c for c in CLAIMS if c["id"] == claim_id), None)
    if not claim:
        return {"error": "Claim not found"}

    payer_data = PAYER_DENIAL_PATTERNS.get(claim["payer"], {})

    prompt = f"""Analyze this insurance claim for denial risk and provide specific corrections:

CLAIM: {json.dumps(claim, indent=2)}
PAYER PATTERNS: {json.dumps(payer_data, indent=2)}

Provide:
1. Risk assessment (why this claim is at {claim['denial_risk']}% denial risk)
2. Specific items to fix before filing
3. Required documentation to attach
4. Exact steps to reduce denial risk to under 10%

Be specific and actionable. Format as a brief checklist."""

    response = await client.messages.create(
        model="claude-sonnet-4-6",
        max_tokens=600,
        messages=[{"role": "user", "content": prompt}]
    )
    return {"analysis": response.content[0].text, "claim": claim}

if __name__ == "__main__":
    import uvicorn
    port = int(os.environ.get("PORT", 8000))
    uvicorn.run(app, host="0.0.0.0", port=port)
