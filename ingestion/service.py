from ingestion.schemas import DocumentIngestResponse, StructuredFinancialOutput
from ingestion.parser.dispatcher import parse_document
from ingestion.summarizer import summarize
import os
import uuid
from fastapi import UploadFile 
from ingestion.parser.pdf_parser import parse_financial_pdf
from typing import List

STORAGE_DIR = "storage/documents"

async def process_company_documents(
    files: List[UploadFile], 
    meta: dict
) -> StructuredFinancialOutput:
    
    company_name = meta["company_name"]
    sector = meta.get("metadata", {}).get("sector", "unknown")
    location = meta.get("metadata", {}).get("location", "India")
    doc_types = {d["file_name"]: d["document_type"] for d in meta.get("documents", [])}

    os.makedirs(STORAGE_DIR, exist_ok=True)
    parsed_docs = []

    for file in files:
        # Save file
        doc_id = f"doc_{uuid.uuid4().hex}"
        ext = file.filename.split(".")[-1]
        saved_name = f"{doc_id}.{ext}"
        file_path = os.path.join(STORAGE_DIR, saved_name)
        
        with open(file_path, "wb") as f:
            f.write(await file.read())
        
        # Determine document type from metadata
        doc_type = doc_types.get(file.filename, "unknown")
        
        # Parse
        parsed = parse_document(file_path, doc_type)
        parsed_docs.append(parsed)

    # debug prints
    for doc in parsed_docs:
        print(f"\n=== {doc['document_type']} ===")
        print(f"Pages: {doc['relevant_pages']}/{doc['total_pages']}")
        print(f"Text preview: {doc['raw_text'][:500]}")
        print(f"Tables found: {doc['tables_found']}")

    # Summarize all docs together with Gemini
    result = summarize(company_name, sector, location, parsed_docs)
    return result