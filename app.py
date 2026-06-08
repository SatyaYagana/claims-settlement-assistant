# app.py
import os
import re
from datetime import datetime
from dotenv import load_dotenv
from openai import OpenAI

# -----------------------------
# Load environment variables
# -----------------------------
load_dotenv()
client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

# -----------------------------
# System prompt for GPT
# -----------------------------
SYSTEM_PROMPT = """
You are ClaimsBot, a professional Claims Processing & Settlement Automation Assistant.

Your responsibilities:
- Guide users step-by-step to submit claims.
- Validate claim information and documents.
- Assess risk and highlight missing information.
- Explain settlements empathetically.
- Recommend human review if necessary.

Always provide responses in this format:
Summary:
<brief summary of claim>

Assessment:
<risk evaluation or comments>

Next Steps:
<actions the user should take>
"""

# -----------------------------
# Allowed values
# -----------------------------
ALLOWED_CLAIM_TYPES = ["AUTO", "HEALTH", "PROPERTY"]

# -----------------------------
# Manual Claim Validation
# -----------------------------
def validate_claim_data(claim: dict):
    """
    Manual validation engine for claim parameters.
    Returns: dict with is_valid, errors, warnings, risk_flags
    """
    errors = []
    warnings = []
    risk_flags = []

    # Policy number
    policy_number = claim.get("policy_number")
    if not policy_number:
        errors.append("Policy number is required.")
    elif not re.match(r"^[A-Z0-9]{5,15}$", policy_number):
        errors.append("Invalid policy number format (expected A-Z, 0-9, 5–15 chars).")

    # Claim type
    claim_type = claim.get("claim_type")
    if not claim_type:
        errors.append("Claim type is required.")
    elif claim_type not in ALLOWED_CLAIM_TYPES:
        errors.append(f"Invalid claim type. Allowed: {ALLOWED_CLAIM_TYPES}")

    # Incident date
    incident_date = claim.get("incident_date")
    if not incident_date:
        errors.append("Incident date is required.")
    else:
        try:
            if isinstance(incident_date, str):
                incident_date = datetime.strptime(incident_date, "%Y-%m-%d")
            if incident_date > datetime.now():
                errors.append("Incident date cannot be in the future.")
            days_diff = (datetime.now() - incident_date).days
            if days_diff > 365:
                warnings.append("Claim reported more than 1 year after incident.")
        except Exception:
            errors.append("Invalid incident date format. Use YYYY-MM-DD.")

    # Claim amount
    claim_amount = claim.get("claim_amount")
    if claim_amount is not None:
        try:
            claim_amount = float(claim_amount)
            if claim_amount <= 0:
                errors.append("Claim amount must be greater than 0.")
            if claim_amount > 1000000:
                risk_flags.append("High value claim (>10L)")
        except:
            errors.append("Claim amount must be a number.")
    else:
        warnings.append("Claim amount not provided.")

    # Documents
    documents = claim.get("documents", [])
    if not isinstance(documents, list):
        errors.append("Documents must be a list.")
    elif len(documents) == 0:
        warnings.append("No supporting documents uploaded.")
    elif len(documents) < 2:
        risk_flags.append("Low documentation support")

    # Fraud heuristics
    description = claim.get("description", "").lower()
    suspicious_keywords = ["urgent cash", "fake", "backdated", "no proof"]
    if any(word in description for word in suspicious_keywords):
        risk_flags.append("Suspicious language detected in description")

    is_valid = len(errors) == 0
    return {
        "is_valid": is_valid,
        "errors": errors,
        "warnings": warnings,
        "risk_flags": risk_flags
    }

# -----------------------------
# OpenAI GPT Chat Function
# -----------------------------
def ask_claimsbot(user_message: str, chat_history: list):
    """
    Sends user message and chat history to OpenAI GPT and returns assistant response.
    """
    if not chat_history:
        chat_history = [{"role": "system", "content": SYSTEM_PROMPT}]

    chat_history.append({"role": "user", "content": user_message})

    try:
        response = client.chat.completions.create(
            model="gpt-4.1-mini",
            messages=chat_history,
            temperature=0.5
        )
        assistant_message = response.choices[0].message.content
    except Exception as e:
        assistant_message = f"Error communicating with OpenAI: {e}"

    chat_history.append({"role": "assistant", "content": assistant_message})
    return assistant_message, chat_history