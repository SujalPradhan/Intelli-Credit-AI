from google import genai
import json
import os
from dotenv import load_dotenv
from ingestion.schemas import StructuredFinancialOutput
from ingestion.prompts import SYSTEM_PROMPT

load_dotenv()

client = genai.Client(api_key=os.getenv("GEMINI_API_KEY"))
aio_client = genai.Client(api_key=os.getenv("GEMINI_API_KEY"))

def build_user_prompt(company_name: str, sector: str, location: str, parsed_docs: list[dict]) -> str:
    docs_text = ""
    for doc in parsed_docs:
        docs_text += f"\n\n--- {doc['document_type'].upper()} ---\n"
        docs_text += doc.get("raw_text", "")

        if doc.get("table_text"):
            docs_text += f"\n\nTABLES:\n{doc['table_text']}"

    return f"""
Company: {company_name}
Sector: {sector}
Location: {location}

DOCUMENT CONTENTS:
{docs_text}

Extract all financial data and return the JSON.
"""

async def summarize(
        company_name: str,
        sector: str,
        location: str,
        parsed_docs: list[dict]
) -> StructuredFinancialOutput:
    
    prompt = build_user_prompt(company_name, sector, location, parsed_docs)

    response = await aio_client.aio.models.generate_content(
        model="gemini-2.5-flash",
        contents=SYSTEM_PROMPT + "\n\n" + prompt,
        config = {
            "temperature": 0.1,
            "response_mime_type": "application/json"
        }
    )

    raw = response.text.strip()

    # Safety: strip markdown fences if present
    if raw.startswith("```"):
        raw = raw.split("```")[1]
        if raw.startswith("json"):
            raw = raw[4:]

    data = json.loads(raw)
    data["company_name"] = company_name

    return StructuredFinancialOutput(**data)