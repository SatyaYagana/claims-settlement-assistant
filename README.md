# 💬 Claims Processing & Settlement Automation Assistant

This is a **conversational chatbot** for automating claims processing and settlement guidance. It combines **OpenAI GPT-4** with a **manual claim validation engine** to guide users step-by-step, highlight missing or suspicious information, and provide settlement recommendations.

---

## **Features**

- Conversational interface via **Streamlit**.
- Step-by-step guidance for claim submission.
- Manual validation of:
  - Policy number format
  - Claim type
  - Incident date
  - Claim amount
  - Supporting documents
- Risk flagging for high-value or suspicious claims.
- Summarizes errors, warnings, and next steps.
- Stores conversation history for a single session.
- Easy to extend for:
  - Automatic claim field extraction
  - Fraud detection
  - Settlement calculation
  - Document verification

---

## **Project Structure**

```text
claimsbot/
│
├── app.py                  # Chatbot logic + claim validation
├── streamlit_interface.py  # Streamlit conversational UI
├── .env                    # Environment variables (API key)
├── requirements.txt        # Python dependencies
└── README.md               # This file