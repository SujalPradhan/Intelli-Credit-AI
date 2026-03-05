from ingestion.schemas import DocumentIngestRequest, DocumentIngestResponse

async def process_document(request: DocumentIngestRequest) -> DocumentIngestResponse:
    # TODO: Orchestrate document parsing and extraction
    return DocumentIngestResponse(status="success", document_id="placeholder-123")
