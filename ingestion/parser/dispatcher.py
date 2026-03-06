from ingestion.parser.pdf_parser import parse_financial_pdf
from ingestion.parser.csv_parser import parse_get_csv

def parse_document(file_path: str, document_type: str) -> dict:
    """
    Route to the right parser based on document type
    """

    ext = file_path.split(".")[-1].lower()

    if ext == "csv":
        return parse_get_csv(file_path, document_type)
    elif ext == "pdf":
        return parse_financial_pdf(file_path, document_type)
    else:
        raise ValueError(f"Unsupported file type: {ext}")