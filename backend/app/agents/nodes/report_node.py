from backend.app.core.llm_client import LLMClient
from backend.app.services.report_service import ReportService
from backend.app.services.report_data_service import ReportDataService
import json


async def report_node(state):

    db = state["db"]
    question = state["question"]

    # Step 1 — Extract community using LLM
    extract_prompt = f"""
Extract the community name from the user query.

Return ONLY JSON.

Example:
{{ "community": "Highlands" }}

User query:
{question}
"""

    response = await LLMClient.generate_answer(extract_prompt)

    try:
        data = json.loads(response)
        community_name = data.get("community")
    except:
        community_name = None

    # Step 2 — Validate community
    if not community_name:

        state["answer"] = "Please specify the community you want the report for."

        return state

    # Step 3 — Fetch data from database
    community_data = await ReportDataService.get_full_community_data(
        db,
        community_name
    )

    # Step 4 — Generate report text
    report_prompt = f"""
You are a professional real estate analyst.

Create a structured report for the following community.

Sections:
1. Community Overview
2. Amenities
3. Nearby Schools
4. Parks
5. Shopping Centres
6. Available Homes
7. Market Insights

Community Data:
{community_data}
"""

    report_text = await LLMClient.generate_answer(report_prompt)

    # Step 5 — Generate PDF
    pdf_path = ReportService.generate_pdf(report_text)

    pdf_url = f"http://127.0.0.1:8000/{pdf_path}"
    
    state["answer"] = f"### ✅ Your Report is Ready\n\nYou can download the structured report here: **[Download Community Report]({pdf_url})**"

    return state