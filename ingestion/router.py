from fastapi import APIRouter, UploadFile, File
from ingestion.schemas import DocumentIngestRequest, DocumentIngestResponse
from ingestion.service import process_document

router = APIRouter(prefix="/ingest", tags=["Ingestion"])

@router.post("/document", response_model=DocumentIngestResponse)
async def ingest_document(file: UploadFile = File(...)):
    """
    Endpoint to handle document parsing and financial data extraction.
    """
    
    # upload a document for ingetion
    return await process_document(file)
