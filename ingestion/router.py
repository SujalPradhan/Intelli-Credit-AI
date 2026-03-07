from fastapi import APIRouter, UploadFile, File, Form
from typing import Annotated, List
from ingestion.schemas import DocumentIngestResponse, StructuredFinancialOutput
from ingestion.service import process_company_documents
import json

router = APIRouter(prefix="/ingest", tags=["Ingestion"])

@router.post("/document")
async def ingest_company(
    file: UploadFile = File(...),
    metadata: str = Form(...) # JSON string: {company_name, sector, location, documents:[{doc_type, file_name}]}
):
    """
    Upload multiple financial documents for a company.
    Returns structured financial JSON ready for the research agent.
    """
    meta = json.loads(metadata)
    return await process_company_documents([file], meta)
