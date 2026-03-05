from pydantic import BaseModel

class ResearchRequest(BaseModel):
    company_name: str
    sector: str

class ResearchResponse(BaseModel):
    status: str
    insights: dict
