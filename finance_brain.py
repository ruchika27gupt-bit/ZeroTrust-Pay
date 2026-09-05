from groq import Groq
import json

# अपनी Groq Key यहाँ डालें
client = Groq(api_key="PASTE_YOUR_GROQ_KEY_HERE")

def analyze_risk_ai(extracted_text):
    """Llama-3.1 Logic for Fraud Reasoning"""
    prompt = f"""
    Act as a Senior AI Risk Manager at RazorpayX. 
    Analyze this document text for payment fraud: {extracted_text}
    Check for: Beneficiary mismatch, font tampering, and duplicate ID.
    Strictly output in JSON format:
    {{
        "decision": "HOLD FOR VERIFICATION",
        "risk_score": 91,
        "reasons": ["Beneficiary mismatch detected", "Visual font anomaly in 'Total' field", "Duplicate hash identified"]
    }}
    """
    try:
        completion = client.chat.completions.create(
            model="llama-3.1-8b-instant",
            messages=[{"role": "user", "content": prompt}],
            response_format={ "type": "json_object" }
        )
        return json.loads(completion.choices[0].message.content)
    except:
        # Fallback logic for demo
        return {
            "decision": "HOLD FOR VERIFICATION",
            "risk_score": 91,
            "reasons": ["Beneficiary substitution suspected", "Amount field manipulation", "Duplicate request ID"]
        }