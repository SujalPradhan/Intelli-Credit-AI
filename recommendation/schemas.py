from pydantic import BaseModel

class RecommendationRequest(BaseModel):
    document_id: str
    company_name: str

class RecommendationResponse(BaseModel):
    score: int
    cam_report: str
