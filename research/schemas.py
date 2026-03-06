from pydantic import BaseModel
from typing import Any


class ResearchRequest(BaseModel):
    company_name: str
    sector: str
    promoters: list[str] = []


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
