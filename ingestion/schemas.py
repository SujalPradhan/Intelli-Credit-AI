from pydantic import BaseModel

class DocumentIngestRequest(BaseModel):
    document_url: str
    document_type: str

class DocumentIngestResponse(BaseModel):
    status: str
    document_id: str
