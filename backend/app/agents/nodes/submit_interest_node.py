import json
import re
from backend.app.services.interest_service import InterestService
from backend.app.core.llm_client import LLMClient


async def submit_interest_node(state):
    db = state["db"]
    question = state["question"]
    lead = state.get("lead", {})

    prompt = f"""
    Extract the following real estate lead information from the user message:
    - name
    - phone
    - email
    - community (the name of the project or area)

    Return ONLY a valid JSON object. Do not include any conversational text.
    If a value is missing, use null.

    User message: {question}
    
    JSON Template:
    {{
      "name": null,
      "phone": null,
      "email": null,
      "community": null
    }}
    """

    response = await LLMClient.generate_answer(prompt)

    try:
        clean_response = re.sub(r"```json|```", "", response).strip()
        
        start_idx = clean_response.find('{')
        end_idx = clean_response.rfind('}')
        
        if start_idx != -1 and end_idx != -1:
            json_str = clean_response[start_idx:end_idx+1]
            data = json.loads(json_str)

            for key in ["name", "phone", "email", "community"]:
                val = data.get(key)
                if val and val != "null":
                    lead[key] = str(val).strip()
        
    except Exception as e:
        print(f"Extraction Error Logic: {str(e)} | Raw Response: {response}")

    required_fields = ["name", "phone", "email"]
    missing = [f for f in required_fields if f not in lead or not lead[f]]

    if missing:
        state["lead"] = lead
        missing_str = ", ".join(missing)
        return {"context": [{"type": "info", "title": "Information Needed", "summary": f"To record your interest, please provide your **{missing_str}**."}]}

    try:
        await InterestService.save_interest(db, lead)
        state["lead"] = {} 
        return {"context": [{"type": "success", "title": "Success!", "summary": "Thank you! Your interest has been recorded in our system. One of our property consultants will reach out to you shortly."}]}
    except Exception as e:
        return {"context": [{"type": "error", "title": "Error", "summary": f"I'm sorry, I encountered an error saving your details. Please try again or contact us directly. (Error: {str(e)})"}]}

    return state
