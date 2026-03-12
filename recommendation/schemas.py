from pydantic import BaseModel
from typing import Optional
from research.schemas import RiskSignal, IngestionOutput


class FiveCsScore(BaseModel):
    character: int    # 0–25
    capacity: int     # 0–25
    capital: int      # 0–20
    collateral: int   # 0–15
    conditions: int   # 0–15
    total: int        # 0–100


class ScoreExplanation(BaseModel):
    character_reasons: list[str]
    capacity_reasons: list[str]
    capital_reasons: list[str]
    collateral_reasons: list[str]
    conditions_reasons: list[str]


class CreditDecision(BaseModel):
    status: str                              # "approved" | "conditional" | "rejected"
    loan_amount_recommended: Optional[float] = None   # INR
    interest_rate: Optional[float] = None             # % per annum
    tenor_months: Optional[int] = None
    primary_reason: str
    detailed_reasoning: str


class RecommendationRequest(BaseModel):
    company_name: str
    sector: str
    loan_requested: float                            # INR
    collateral_value: Optional[float] = None        # INR
    collateral_description: Optional[str] = "Unsecured"
    promoters: list[str] = []

    # Passed directly from /research/analyze response
    research_summary: str = ""
    company_news: list[str] = []
    promoter_risks: list[str] = []
    sector_trends: list[str] = []
    risk_signals: list[RiskSignal] = []
    financial_data: Optional[IngestionOutput] = None


class RecommendationResponse(BaseModel):
    company_name: str
    score_breakdown: FiveCsScore
    score_explanation: ScoreExplanation
    decision: CreditDecision
    cam_report_url: str
    cam_pdf_url: Optional[str] = None
