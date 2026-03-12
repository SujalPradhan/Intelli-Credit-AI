def get_cam_narrative_prompt(
    request_data: dict,
    score_data: dict,
    decision_data: dict,
) -> str:
    fin = request_data.get("financial_data", {})
    fs = fin.get("financial_summary", {}) if fin else {}
    fr = fin.get("financial_ratios", {}) if fin else {}
    ca = fin.get("cashflow_analysis", {}) if fin else {}
    anomalies = fin.get("anomalies_detected", []) if fin else []

    loan_amt = decision_data.get("loan_amount_recommended")
    rate = decision_data.get("interest_rate")
    tenor = decision_data.get("tenor_months")

    return f"""You are a senior credit analyst at an Indian bank. Write a professional Credit Appraisal Memo (CAM).

COMPANY: {request_data["company_name"]}
SECTOR: {request_data["sector"]}
LOAN REQUESTED: ₹{request_data["loan_requested"]:,.0f}
COLLATERAL: {request_data.get("collateral_description", "Unsecured")} (₹{request_data.get("collateral_value") or 0:,.0f})
PROMOTERS: {", ".join(request_data.get("promoters", [])) or "Not specified"}

FIVE CS CREDIT SCORE:
  Character:  {score_data["character"]}/25
  Capacity:   {score_data["capacity"]}/25
  Capital:    {score_data["capital"]}/20
  Collateral: {score_data["collateral"]}/15
  Conditions: {score_data["conditions"]}/15
  TOTAL:      {score_data["total"]}/100

DECISION: {decision_data["status"].upper()}
{f"Recommended Loan: ₹{loan_amt:,.0f}" if loan_amt else ""}
{f"Interest Rate: {rate}% p.a." if rate else ""}
{f"Tenor: {tenor} months" if tenor else ""}
Decision Rationale: {decision_data["primary_reason"]}

RESEARCH SUMMARY:
{request_data.get("research_summary", "Not available")}

RISK SIGNALS:
{chr(10).join(f'  - [{s.get("risk_type","?")} / severity {s.get("severity","?")}] {s.get("entity","?")}: {s.get("evidence","")[:150]}' for s in request_data.get("risk_signals", [])[:6]) or "  None identified"}

SECTOR TRENDS:
{chr(10).join(f'  - {t}' for t in request_data.get("sector_trends", [])[:5]) or "  Not available"}

KEY FINANCIAL METRICS:
  Revenue:           ₹{fs.get("revenue") if fs.get("revenue") is not None else "N/A"}
  Net Profit:        ₹{fs.get("profit") if fs.get("profit") is not None else "N/A"}
  Total Assets:      ₹{fs.get("total_assets") if fs.get("total_assets") is not None else "N/A"}
  Total Liabilities: ₹{fs.get("total_liabilities") if fs.get("total_liabilities") is not None else "N/A"}
  Net Worth:         ₹{fs.get("net_worth") if fs.get("net_worth") is not None else "N/A"}
  Debt-to-Equity:    {fr.get("debt_to_equity") if fr.get("debt_to_equity") is not None else "N/A"}
  Current Ratio:     {fr.get("current_ratio") if fr.get("current_ratio") is not None else "N/A"}
  Profit Margin:     {f'{fr["profit_margin"]*100:.1f}%' if fr.get("profit_margin") is not None else "N/A"}
  DSCR:              {fr.get("dscr") if fr.get("dscr") is not None else "N/A"}
  Avg Monthly Inflow:  ₹{ca.get("monthly_avg_inflow") if ca.get("monthly_avg_inflow") is not None else "N/A"}
  Avg Monthly Outflow: ₹{ca.get("monthly_avg_outflow") if ca.get("monthly_avg_outflow") is not None else "N/A"}
  Cashflow Volatility: {ca.get("cashflow_volatility") if ca.get("cashflow_volatility") is not None else "N/A"}

ANOMALIES DETECTED:
{chr(10).join(f'  - [{a.get("severity","?")}] {a.get("type","?")}: {a.get("description","")[:120]}' for a in anomalies[:4]) or "  None detected"}

Generate a CAM as a JSON object with exactly these keys:
{{
  "executive_summary": "2–3 paragraph professional summary of the credit proposal and decision",
  "applicant_profile": "Description of the company, its business, sector position, and promoter background",
  "character_analysis": "Analysis of the borrower's integrity, track record, and any risk signals found. Reference specific risk signals.",
  "capacity_analysis": "Analysis of DSCR, cash flows, profitability, and ability to service debt. Reference specific ratios.",
  "capital_analysis": "Analysis of net worth, leverage (D/E), and overall financial strength relative to the loan.",
  "collateral_analysis": "Analysis of the security offered, LTV ratio, and asset quality.",
  "conditions_analysis": "Analysis of industry and sector conditions, macroeconomic outlook for the borrower's sector.",
  "risk_matrix": "Key risks (as numbered bullet points) and corresponding mitigation measures.",
  "recommendation": "Final credit recommendation — state the loan terms, any conditions precedent, and a clear explanation of why the decision was made (or why it was rejected)."
}}

Use formal Indian banking language. Cite specific numbers. The recommendation section MUST explain the decision using the Five Cs scores and any critical risk signals.
Return ONLY valid JSON. No markdown fences, no commentary outside the JSON."""

