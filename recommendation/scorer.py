from recommendation.schemas import RecommendationRequest, FiveCsScore, ScoreExplanation


# ── Character (max 25) ────────────────────────────────────────────────────────

def _score_character(req: RecommendationRequest) -> tuple[int, list[str]]:
    score = 25
    reasons: list[str] = []

    severity_deductions = {"5": 11, "4": 8, "3": 5, "2": 3, "1": 1}
    type_extras = {"fraud": 2, "regulatory": 1, "litigation": 1}

    for signal in req.risk_signals:
        base = severity_deductions.get(str(signal.severity), 3)
        extra = type_extras.get(signal.risk_type, 0)
        deduction = min(base + extra, 13)
        score -= deduction
        reasons.append(
            f"Risk signal: {signal.risk_type} on {signal.entity} — severity {signal.severity}. "
            f"Deducted {deduction} pts. Evidence: {signal.evidence[:120]}"
        )

    for risk in req.promoter_risks[:3]:
        score -= 3
        reasons.append(f"Promoter risk identified — Deducted 3 pts: {risk[:120]}")

    if not req.risk_signals and not req.promoter_risks:
        reasons.append("No adverse risk signals or promoter issues found — full character score awarded.")

    return max(0, score), reasons


# ── Capacity (max 25) ─────────────────────────────────────────────────────────

def _score_capacity(req: RecommendationRequest) -> tuple[int, list[str]]:
    score = 0
    reasons: list[str] = []

    ratios = req.financial_data.financial_ratios if req.financial_data else None
    cashflow = req.financial_data.cashflow_analysis if req.financial_data else None

    # DSCR — 10 pts
    dscr = ratios.dscr if ratios else None
    if dscr is None:
        score += 5
        reasons.append("DSCR not available — partial score awarded (5/10).")
    elif dscr >= 1.5:
        score += 10
        reasons.append(f"DSCR = {dscr:.2f} (≥1.5) — excellent debt service capacity (10/10).")
    elif dscr >= 1.25:
        score += 8
        reasons.append(f"DSCR = {dscr:.2f} (1.25–1.5) — adequate debt service (8/10).")
    elif dscr >= 1.0:
        score += 5
        reasons.append(f"DSCR = {dscr:.2f} (1.0–1.25) — borderline debt service capacity (5/10).")
    else:
        score += 2
        reasons.append(f"DSCR = {dscr:.2f} (<1.0) — insufficient debt service capacity (2/10).")

    # Profit margin — 8 pts
    pm = ratios.profit_margin if ratios else None
    if pm is None:
        score += 4
        reasons.append("Profit margin not available — partial score awarded (4/8).")
    elif pm >= 0.15:
        score += 8
        reasons.append(f"Profit margin = {pm*100:.1f}% (≥15%) — strong profitability (8/8).")
    elif pm >= 0.08:
        score += 6
        reasons.append(f"Profit margin = {pm*100:.1f}% (8–15%) — adequate profitability (6/8).")
    elif pm >= 0:
        score += 4
        reasons.append(f"Profit margin = {pm*100:.1f}% (0–8%) — thin profitability (4/8).")
    else:
        score += 0
        reasons.append(f"Profit margin = {pm*100:.1f}% — company is loss-making (0/8).")

    # Cashflow volatility — 7 pts
    vol = cashflow.cashflow_volatility if cashflow else None
    if vol is None:
        score += 3
        reasons.append("Cashflow volatility not available — partial score awarded (3/7).")
    elif vol == "low":
        score += 7
        reasons.append("Cashflow volatility: low — stable and predictable cash inflows (7/7).")
    elif vol == "moderate":
        score += 4
        reasons.append("Cashflow volatility: moderate — some variability in cash flows (4/7).")
    else:
        score += 1
        reasons.append("Cashflow volatility: high — unpredictable cash flows (1/7).")

    return min(score, 25), reasons


# ── Capital (max 20) ──────────────────────────────────────────────────────────

def _score_capital(req: RecommendationRequest) -> tuple[int, list[str]]:
    score = 0
    reasons: list[str] = []

    summary = req.financial_data.financial_summary if req.financial_data else None
    ratios = req.financial_data.financial_ratios if req.financial_data else None

    # Debt-to-equity — 10 pts
    de = ratios.debt_to_equity if ratios else None
    if de is None:
        score += 5
        reasons.append("Debt-to-equity not available — partial score awarded (5/10).")
    elif de < 1.0:
        score += 10
        reasons.append(f"D/E = {de:.2f} (<1.0) — low leverage, strong capital base (10/10).")
    elif de < 2.0:
        score += 7
        reasons.append(f"D/E = {de:.2f} (1.0–2.0) — moderate leverage (7/10).")
    elif de < 3.0:
        score += 4
        reasons.append(f"D/E = {de:.2f} (2.0–3.0) — high leverage (4/10).")
    else:
        score += 1
        reasons.append(f"D/E = {de:.2f} (>3.0) — over-leveraged balance sheet (1/10).")

    # Net worth vs loan requested — 10 pts
    nw = summary.net_worth if summary else None
    if nw is None or req.loan_requested <= 0:
        score += 5
        reasons.append("Net worth not available — partial score awarded (5/10).")
    else:
        coverage = nw / req.loan_requested
        if coverage >= 3.0:
            score += 10
            reasons.append(f"Net worth = {coverage:.1f}x loan requested — strong capital coverage (10/10).")
        elif coverage >= 2.0:
            score += 7
            reasons.append(f"Net worth = {coverage:.1f}x loan requested — adequate capital coverage (7/10).")
        elif coverage >= 1.0:
            score += 4
            reasons.append(f"Net worth = {coverage:.1f}x loan requested — thin capital coverage (4/10).")
        else:
            score += 1
            reasons.append(f"Net worth covers only {coverage:.1f}x of loan requested — insufficient (1/10).")

    return min(score, 20), reasons


# ── Collateral (max 15) ───────────────────────────────────────────────────────

def _score_collateral(req: RecommendationRequest) -> tuple[int, list[str]]:
    reasons: list[str] = []

    if not req.collateral_value or req.collateral_value <= 0:
        reasons.append("No collateral provided — unsecured loan, partial base score (5/15).")
        return 5, reasons

    ltv = req.loan_requested / req.collateral_value
    if ltv <= 0.50:
        score = 15
        reasons.append(f"LTV = {ltv*100:.0f}% (≤50%) — well-secured collateral (15/15).")
    elif ltv <= 0.70:
        score = 11
        reasons.append(f"LTV = {ltv*100:.0f}% (50–70%) — adequately secured (11/15).")
    elif ltv <= 0.80:
        score = 7
        reasons.append(f"LTV = {ltv*100:.0f}% (70–80%) — marginally secured (7/15).")
    else:
        score = 3
        reasons.append(f"LTV = {ltv*100:.0f}% (>80%) — under-secured collateral (3/15).")

    if req.collateral_description:
        reasons.append(f"Collateral type: {req.collateral_description}")

    return score, reasons


# ── Conditions (max 15) ───────────────────────────────────────────────────────

_POSITIVE_KEYWORDS = [
    "growth", "expanding", "favorable", "tailwind", "strong demand",
    "upturn", "recovery", "boom", "opportunity",
]
_NEGATIVE_KEYWORDS = [
    "downturn", "recession", "headwind", "decline", "slowdown",
    "risk", "pressure", "stress", "contraction", "overcapacity",
]


def _score_conditions(req: RecommendationRequest) -> tuple[int, list[str]]:
    score = 10  # neutral baseline
    reasons: list[str] = []

    positive_count = sum(
        1 for trend in req.sector_trends
        if any(kw in trend.lower() for kw in _POSITIVE_KEYWORDS)
    )
    negative_count = sum(
        1 for trend in req.sector_trends
        if any(kw in trend.lower() for kw in _NEGATIVE_KEYWORDS)
    )

    if positive_count > negative_count:
        score += 5
        reasons.append(f"Sector outlook positive ({positive_count} favourable trend signals) — +5 pts.")
    elif negative_count > positive_count:
        score -= 5
        reasons.append(f"Sector outlook negative ({negative_count} adverse trend signals) — -5 pts.")
    else:
        reasons.append("Sector outlook neutral — no adjustment to conditions score.")

    industry_signals = [s for s in req.risk_signals if s.risk_type == "industry"]
    for signal in industry_signals:
        deduction = int(signal.severity) if str(signal.severity).isdigit() else 2
        score -= deduction
        reasons.append(
            f"Industry risk signal (severity {signal.severity}): {signal.evidence[:80]} — -{deduction} pts."
        )

    if not req.sector_trends and not industry_signals:
        reasons.append("No sector trend data available — baseline conditions score maintained (10/15).")

    return max(0, min(score, 15)), reasons


# ── Aggregator ────────────────────────────────────────────────────────────────

def compute_five_cs(request: RecommendationRequest) -> tuple[FiveCsScore, ScoreExplanation]:
    char_score, char_reasons = _score_character(request)
    cap_score, cap_reasons = _score_capacity(request)
    capital_score, capital_reasons = _score_capital(request)
    coll_score, coll_reasons = _score_collateral(request)
    cond_score, cond_reasons = _score_conditions(request)

    total = char_score + cap_score + capital_score + coll_score + cond_score

    return (
        FiveCsScore(
            character=char_score,
            capacity=cap_score,
            capital=capital_score,
            collateral=coll_score,
            conditions=cond_score,
            total=total,
        ),
        ScoreExplanation(
            character_reasons=char_reasons,
            capacity_reasons=cap_reasons,
            capital_reasons=capital_reasons,
            collateral_reasons=coll_reasons,
            conditions_reasons=cond_reasons,
        ),
    )
