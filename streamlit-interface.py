import streamlit as st
from app import ask_claimsbot, validate_claim_data

st.set_page_config(page_title="ClaimsBot Chat", page_icon="💬", layout="wide")
st.title("💬 Claims Processing & Settlement Automation Assistant")
st.caption("Chat with ClaimsBot to submit claims, validate information, and get settlement guidance.")

# -----------------------------
# Session state
# -----------------------------
if "messages" not in st.session_state:
    st.session_state.messages = []

# -----------------------------
# Show chat history
# -----------------------------
for msg in st.session_state.messages:
    with st.chat_message(msg["role"]):
        st.markdown(msg["content"])

# -----------------------------
# User input
# -----------------------------
if user_input := st.chat_input("Type your message here..."):

    # Show user message
    st.chat_message("user").markdown(user_input)

    # -----------------------------
    # Simulated claim extraction (replace later with GPT extraction)
    # -----------------------------
    simulated_claim_data = {
        "policy_number": "AUTO12345",
        "claim_type": "AUTO",
        "incident_date": "2026-06-01",
        "claim_amount": 75000,
        "documents": ["photo1.jpg", "report.pdf"],
        "description": user_input
    }

    # -----------------------------
    # Validate claim
    # -----------------------------
    validation_result = validate_claim_data(simulated_claim_data)

    if not validation_result["is_valid"]:

        # Precompute safe strings (IMPORTANT FIX)
        errors = validation_result["errors"]
        warnings = validation_result["warnings"]
        risk_flags = validation_result["risk_flags"]

        errors_text = "\n- ".join(errors) if errors else "None"
        warnings_text = "\n- ".join(warnings) if warnings else "None"
        risk_text = "\n- ".join(risk_flags) if risk_flags else "None"

        response_text = f"""
❌ Claim validation failed.

Errors:
- {errors_text}

Warnings:
- {warnings_text}

Risk Flags:
- {risk_text}

Next Steps:
- Please correct missing or invalid information before proceeding.
"""

    else:
        # Valid claim → send to GPT chatbot
        response_text, st.session_state.messages = ask_claimsbot(
            user_input,
            st.session_state.messages
        )

    # -----------------------------
    # Show assistant response
    # -----------------------------
    st.chat_message("assistant").markdown(response_text)

    # Save assistant message in history
    st.session_state.messages.append(
        {"role": "assistant", "content": response_text}
    )

# -----------------------------
# Sidebar
# -----------------------------
with st.sidebar:
    st.title("📋 ClaimsBot Options")

    if st.button("🗑️ New Conversation"):
        st.session_state.messages = []
        st.rerun()