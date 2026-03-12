from recommendation.schemas import RecommendationRequest, FiveCsScore, CreditDecision

# (min_score, loan_pct_of_requested, rate_pct_pa, tenor_months)
_SCORE_BANDS = [
    (75, 1.00, 10.0, 60),
    (60, 0.80, 12.0, 48),
    (50, 0.60, 14.0, 36),
    (40, 0.40, 16.0, 24),
]

_REJECTION_THRESHOLD = 40


def _weakest_c(score: FiveCsScore) -> tuple[str, int]:
    scores_map = {
        "Character": score.character,
        "Capacity": score.capacity,
        "Capital": score.capital,
        "Collateral": score.collateral,
        "Conditions": score.conditions,
    }
    name = min(scores_map, key=scores_map.get)
    return name, scores_map[name]


def derive_decision(request: RecommendationRequest, score: FiveCsScore) -> CreditDecision:
    # Hard rejection: any severity-5 (critical) risk signal
    critical = [s for s in request.risk_signals if str(s.severity) == "5"]

    if critical:
        reason = (
            f"Rejected due to critical risk signal ({critical[0].risk_type}) involving "
            f"{critical[0].entity} despite a score of {score.total}/100. "
            f"Evidence: {critical[0].evidence[:200]}"
        )
        return CreditDecision(
            status="rejected",
            primary_reason=reason,
            detailed_reasoning=reason,
        )

    if score.total < _REJECTION_THRESHOLD:
        weak_name, weak_val = _weakest_c(score)
        reason = (
            f"Rejected — credit score {score.total}/100 is below the minimum threshold of "
            f"{_REJECTION_THRESHOLD}. Primary weakness: {weak_name} ({weak_val} pts)."
        )
        return CreditDecision(
            status="rejected",
            primary_reason=reason,
            detailed_reasoning=reason,
        )

    # Find the applicable score band (ordered high → low)
    for min_score, loan_pct, rate, tenor in _SCORE_BANDS:
        if score.total >= min_score:
            loan_amount = round(request.loan_requested * loan_pct, -3)  # nearest ₹1,000
            status = "approved" if score.total >= 50 else "conditional"

            scores_map = {
                "Character": score.character,
                "Capacity": score.capacity,
                "Capital": score.capital,
                "Collateral": score.collateral,
                "Conditions": score.conditions,
            }
            strongest = max(scores_map, key=scores_map.get)
            weak_name, weak_val = _weakest_c(score)

            reason = (
                f"{status.capitalize()} with credit score {score.total}/100. "
                f"Recommended: ₹{loan_amount:,.0f} at {rate}% p.a. for {tenor} months. "
                f"Strongest factor: {strongest} ({scores_map[strongest]} pts). "
                f"Key constraint: {weak_name} ({weak_val} pts)."
            )
            return CreditDecision(
                status=status,
                loan_amount_recommended=loan_amount,
                interest_rate=rate,
                tenor_months=tenor,
                primary_reason=reason,
                detailed_reasoning=reason,
            )

    # Should never reach here, but safe fallback
    reason = f"Score {score.total}/100 — below all approval thresholds."
    return CreditDecision(
        status="rejected",
        primary_reason=reason,
        detailed_reasoning=reason,
    )
