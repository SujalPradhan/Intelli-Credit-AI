from pydantic import BaseModel
from typing import Any, Optional

# ingestion pipeline outputs
class FinancialSummary(BaseModel):
    revenue: Optional[float] = None
    profit: Optional[float] = None
    total_assets: Optional[float] = None
    total_liabilities: Optional[float] = None
    net_worth: Optional[float] = None

class FinancialRatios(BaseModel):
    debt_to_equity: Optional[float] = None
    current_ratio: Optional[float] = None
    profit_margin: Optional[float] = None
    dscr: Optional[float] = None

class CashflowAnalysis(BaseModel):
    monthly_avg_inflow: Optional[float] = None
    monthly_avg_outflow: Optional[float] = None
    cashflow_volatility: Optional[str] = None

class Anomaly(BaseModel):
    type: str
    period: str
    severity: str
    description: str

class ParsedDocument(BaseModel):
    document_type: str
    key_findings: list[str]

class IngestionOutput(BaseModel):
    """ what ingestion pipeline returns """
    company_name: str
    financial_summary: FinancialSummary = FinancialSummary()
    financial_ratios: FinancialRatios = FinancialRatios()
    cashflow_analysis: CashflowAnalysis = CashflowAnalysis()
    anomalies_detected: list[Anomaly] = []
    parsed_documents: list[ParsedDocument] = []


class ResearchRequest(BaseModel):
    company_name: str
    sector: str
    promoters: list[str] = []
    financial_data: Optional[IngestionOutput] = None


class SearchResult(BaseModel):
    title: str
    link: str
    snippet: str
    source: str


class ExtractedArticle(BaseModel):
    url: str
    text: str
    text_length: int


class RiskSignal(BaseModel):
    risk_type: str
    entity: str
    severity: str
    source: str
    evidence: str
    confidence: str = ""
    reasoning: dict = {}

class PipelineLog(BaseModel):
    stage: str
    timestamp: str
    data: Any


class ResearchResponse(BaseModel):
    research_summary: str
    company_news: list[str]
    promoter_risks: list[str]
    sector_trends: list[str]
    risk_signals: list[RiskSignal]
    pipeline_logs: list[PipelineLog]
    financial_data: Optional[IngestionOutput] = None
