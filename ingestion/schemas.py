from pydantic import BaseModel
from typing import Any, Optional

class DocumentIngestResponse(BaseModel):
    status: str
    document_id: str
    filename: str
    data: Optional[dict[str, Any]] = None

class DocumentMeta(BaseModel):
    document_type: str # "annual_report" | "bank_stataement" | "gst_return"
    file_name : str

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
    cashflow_volatility: Optional[str] = None  # "low" | "moderate" | "high"

class Anomaly(BaseModel):
    type: str
    period: str
    severity: str # "low" | "medium" | "high"
    description: str

class ParsedDocument(BaseModel):
    document_type: str
    key_findings: list[str]

class StructuredFinancialOutput(BaseModel):
    company_name: str
    financial_summary: FinancialSummary
    financial_ratios: FinancialRatios
    cashflow_analysis: CashflowAnalysis
    anomalies_detected: list[Anomaly]
    parsed_documents: list[ParsedDocument]
