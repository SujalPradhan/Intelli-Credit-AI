from fastapi import APIRouter
from ingestion.schemas import DocumentIngestRequest, DocumentIngestResponse
from ingestion.service import process_document

router = APIRouter(prefix="/ingest", tags=["Ingestion"])

@router.post("/document", response_model=DocumentIngestResponse)
async def ingest_document(request: DocumentIngestRequest):
    """
    Endpoint to handle document parsing and financial data extraction.
    """
    # TODO: Handle document parsing and extraction via service
    return await process_document(request)
