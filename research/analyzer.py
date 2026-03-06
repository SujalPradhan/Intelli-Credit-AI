import json
from research.schemas import ExtractedArticle, RiskSignal
from research.prompts import get_analysis_prompt, get_risk_extraction_prompt

# The gemini_client is a google.genai.Client instance.
# Usage: client.models.generate_content(model=MODEL, contents=PROMPT)

MODEL = "gemini-2.0-flash"


def analyze_article(
    article: ExtractedArticle,
    company_name: str,
    sector: str,
    gemini_client,
) -> dict:
    """Send article text to Gemini for risk analysis. Returns prompt and response."""
    prompt = get_analysis_prompt(article.text, company_name, sector)

    try:
        response = gemini_client.models.generate_content(
            model=MODEL,
            contents=prompt,
        )
        analysis_text = response.text
    except Exception as e:
        analysis_text = f"[analyzer] Gemini error: {e}"

    return {
        "url": article.url,
        "prompt": prompt[:500] + "..." if len(prompt) > 500 else prompt,
        "response": analysis_text,
    }


def extract_risk_signals(
    analysis_texts: list[str],
    company_name: str,
    gemini_client,
) -> list[RiskSignal]:
    """Convert combined LLM analyses into structured risk signals via Gemini."""
    combined = "\n\n---\n\n".join(analysis_texts)
    prompt = get_risk_extraction_prompt(combined, company_name)

    try:
        response = gemini_client.models.generate_content(
            model=MODEL,
            contents=prompt,
        )
        raw = response.text.strip()

        # Strip markdown code fences if present
        if raw.startswith("```"):
            raw = raw.split("\n", 1)[1] if "\n" in raw else raw[3:]
        if raw.endswith("```"):
            raw = raw[:-3].strip()

        signals_data = json.loads(raw)
    except (json.JSONDecodeError, Exception) as e:
        print(f"[analyzer] Failed to parse risk signals: {e}")
        return []

    signals = []
    for item in signals_data:
        try:
            signals.append(RiskSignal(**item))
        except Exception:
            continue

    return signals
