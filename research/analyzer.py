import json
from openai import OpenAI
from research.schemas import ExtractedArticle, RiskSignal
from research.prompts import get_analysis_prompt, get_risk_extraction_prompt

# Using the requested model from the AIPipe curl example
MODEL = "gpt-5-nano"


def analyze_article(
    article: ExtractedArticle,
    company_name: str,
    sector: str,
    aipipe_client: OpenAI,
) -> dict:
    """Send article text to AIPipe for risk analysis. Returns prompt and response."""
    prompt = get_analysis_prompt(article.text, company_name, sector)

    try:
        response = aipipe_client.chat.completions.create(
            model=MODEL,
            messages=[
                {"role": "user", "content": prompt}
            ],
        )
        analysis_text = response.choices[0].message.content
    except Exception as e:
        analysis_text = f"[analyzer] AIPipe error: {e}"

    return {
        "url": article.url,
        "prompt": prompt[:500] + "..." if len(prompt) > 500 else prompt,
        "response": analysis_text,
    }


def extract_risk_signals(
    analysis_texts: list[str],
    company_name: str,
    aipipe_client: OpenAI,
) -> list[RiskSignal]:
    """Convert combined LLM analyses into structured risk signals via AIPipe."""
    combined = "\n\n---\n\n".join(analysis_texts)
    prompt = get_risk_extraction_prompt(combined, company_name)

    try:
        response = aipipe_client.chat.completions.create(
            model=MODEL,
            messages=[{"role": "user", "content": prompt}],
            response_format={"type": "json_object"} # Force JSON if the model supports it, else prompt-level parsing applies
        )
        raw = response.choices[0].message.content.strip()

        # Handle potential markdown code fences just in case
        if raw.startswith("```"):
            raw = raw.split("\n", 1)[1] if "\n" in raw else raw[3:]
        if raw.endswith("```"):
            raw = raw[:-3].strip()

        # Depending on how the prompt is interpreted, the JSON might be exactly an array
        # or an object wrapping an array. We try parsing exactly what came back.
        signals_data = json.loads(raw)
        
        # If the API returned `{"risk_signals": [...]}` instead of `[...]` unpack it:
        if isinstance(signals_data, dict):
            # Try to grab the first list value it finds, or default to empty
            signals_data = next((v for v in signals_data.values() if isinstance(v, list)), [])

    except (json.JSONDecodeError, Exception) as e:
        print(f"[analyzer] Failed to parse risk signals from AIPipe: {e}")
        return []

    signals = []
    for item in signals_data:
        try:
            signals.append(RiskSignal(**item))
        except Exception:
            continue

    return signals
