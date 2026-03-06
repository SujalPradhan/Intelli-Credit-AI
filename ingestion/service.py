from ingestion.schemas import DocumentIngestRequest, DocumentIngestResponse
import os
import uuid
from fastapi import UploadFile 

STORAGE_DIR = "storage/documents"

async def process_document(file: UploadFile) -> DocumentIngestResponse:
    """
    Save uploaded document and generate document ID
    """

    # Generate doc id
    document_id = f"doc_{uuid.uuid4().hex}"

    file_extension = file.filename.split(".")[-1]

    filename = f"{document_id}.{file_extension}"

    file_path = os.path.join(STORAGE_DIR, filename)

    os.makedirs(STORAGE_DIR, exist_ok=True)

    # save file
    with open(file_path, "wb") as f:
        contents = await file.read()
        f.write(contents)

    return DocumentIngestResponse(
        status="uploaded", 
        document_id=document_id, 
        filename=filename
    )
