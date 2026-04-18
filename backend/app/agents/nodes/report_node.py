from backend.app.core.llm_client import LLMClient
from backend.app.services.report_service import ReportService
from backend.app.services.report_data_service import ReportDataService
import json


async def report_node(state):

    db = state["db"]
    question = state["rewritten_query"]

    extract_prompt = f"""
Extract the community name from the user query.

Return ONLY JSON.

Example:
{{ "community": "Highlands" }}
{{ "community": "Banksia" }}

User query:
{question}
"""

    response = await LLMClient.generate_answer(extract_prompt)

    try:
        data = json.loads(response)
        community_name = data.get("community")
    except:
        community_name = None


    if not community_name:

        return {"context": [{"type": "error", "title": "Report Error", "summary": "Please specify the community you want the report for."}]}

    community_data = await ReportDataService.get_full_community_data(
        db,
        community_name
    )

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


    pdf_path = ReportService.generate_pdf(report_text)

    pdf_url = f"http://127.0.0.1:8000/{pdf_path}"
    
    return {"context": [{"type": "report", "title": "Community Report", "summary": f"Your report for {community_name} is ready. [Download Community Report]({pdf_url})"}]}