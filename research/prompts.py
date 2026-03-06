def get_analysis_prompt(article_text: str, company_name: str, sector: str) -> str:
    """Step-by-step reasoning prompt for analyzing a single article."""
    return f"""You are a financial research analyst evaluating news about companies.

Your task is to identify credit risk signals from the article.

Think step-by-step and return your reasoning.

Follow this structure:

Step 1: Entities Mentioned
List all companies, promoters, and institutions mentioned.

Step 2: Key Event
Describe the main event in the article.

Step 3: Risk Interpretation
Explain why this event could affect financial risk.

Step 4: Severity Assessment
Assign a severity score from 1 to 5.

Step 5: Evidence
Quote the sentence from the article that supports the risk.

Step 6: Final Risk Signal
Return the signal in JSON format.

Output format:

{{
  "reasoning": {{
    "entities": [],
    "event": "",
    "risk_interpretation": "",
    "severity": "",
    "evidence": ""
  }},
  "risk_signal": {{
    "type": "",
    "entity": "",
    "severity": "",
    "confidence": ""
  }}
}}

ARTICLE:
{article_text[:4000]}

Do not skip reasoning steps.
Explain your thought process clearly before producing the final answer."""


def get_risk_extraction_prompt(combined_analysis: str, company_name: str) -> str:
    """Prompt to convert free-text analyses into structured JSON risk signals."""
    return f"""You are a financial risk analyst. Based on the following step-by-step \
analyses about "{company_name}", extract a consolidated JSON array of risk signals.

For each risk signal identified in the analyses, produce an object with these fields:
- "risk_type": one of "litigation", "regulatory", "fraud", "industry", "reputational"
- "entity": the company, person, or sector the risk relates to
- "severity": one of "1", "2", "3", "4", "5"
- "source": the origin of the information (article URL or description)
- "evidence": a concise quote or summary supporting the signal
- "confidence": confidence level of the signal
- "reasoning": the dictionary of reasoning steps

Think step-by-step:
1. Read each analysis JSON object and identify distinct risk signals.
2. Deduplicate overlapping signals.
3. Assign severity based on the reasoning provided.
4. Format as JSON.

Analyses:
\"\"\"
{combined_analysis[:8000]}
\"\"\"

Return ONLY a valid JSON array. No markdown, no commentary."""


def get_summary_prompt(combined_analysis: str, company_name: str, sector: str) -> str:
    """Prompt to produce a concise research summary and categorized insights."""
    return f"""You are a credit research analyst. Based on the following step-by-step \
analyses about "{company_name}" in the "{sector}" sector, produce a structured summary.

Think step-by-step:
1. Identify the most important findings across all analyses.
2. Categorize them into company-specific news, promoter risks, and sector trends.
3. Write a concise executive summary.

Return a JSON object with these keys:
- "research_summary": a 2-3 sentence executive summary of the findings
- "company_news": array of short bullet strings about company-specific news
- "promoter_risks": array of short bullet strings about risks tied to promoters/directors
- "sector_trends": array of short bullet strings about sector-level trends or risks

Analyses:
\"\"\"
{combined_analysis[:6000]}
\"\"\"

Return ONLY valid JSON. No markdown, no commentary."""
