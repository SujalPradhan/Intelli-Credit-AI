import fitz  # PyMuPDF
import pandas as pd
import re
from ingestion.parser.constants import FINANCIAL_KEYWORDS, NOISE_SECTIONS, HIGH_VALUE_SECTIONS

# extracting text --> returning pages
def extract_text_from_pdf(pdf_path: str) -> list:
    """
    Extract text from each page of a PDF 
    Returns as list of (pages_number, text)
    """

    doc = fitz.open(pdf_path)

    pages = []

    for page_num in range(len(doc)):
        page = doc.load_page(page_num)
        text = page.get_text()

        pages.append((page_num + 1, text))
    
    return pages


# filtering financial pages
def filter_financial_pages(pages):
    """
    Filter pages that contain financial keywords
    """

    relevant_pages = []

    for page_num, text in pages:
        lower_text = text.lower()

        if any(keyword in lower_text for keyword in FINANCIAL_KEYWORDS):
            relevant_pages.append((page_num, text))
    
    return relevant_pages

# extracting tables
def extract_tables_from_pdf(pdf_path: str):

    doc = fitz.open(pdf_path)

    tables = []

    for page in doc:

        tabs = page.find_tables()

        for tab in tabs:
            df = tab.to_pandas()
            tables.append(df)
    
    return tables


# extracting metrics
def extract_financial_metrics(text):
    metrics = {}

    revenue_match = re.search(r"revenue.*?(\d[\d,]*)", text, re.IGNORECASE)
    profit_match = re.search(r"profit.*?(\d[\d,]*)", text, re.IGNORECASE)

    if revenue_match:
        metrics["revenue"] = revenue_match.group(1)

    if profit_match:
        metrics["profit"] = profit_match.group(1)

    return metrics

# financial page or not
def is_financial_page(text: str) -> bool:
    lower = text.lower()
    
    # if noise header --> return (EARLY EXIT)
    if any(noise in lower for noise in NOISE_SECTIONS):
        return False
    
    has_keywords = any(kw in lower for kw in HIGH_VALUE_SECTIONS)
    
    # if lots of digits --> accept it
    number_pattern = re.findall(r'\b\d{4,}\b', text)  # numbers >= 4 digits
    is_number_dense = len(number_pattern) > 15  # more than 15 large numbers
    
    return has_keywords or is_number_dense


def extract_financial_sections(pages: list) -> list:
    """
    Smarter extraction: find anchor pages + grab surrounding context
    """
    selected_indices = set()
    
    for i, (page_num, text) in enumerate(pages):
        if is_financial_page(text):
            # this + next 3 pages
            for j in range(i, min(i + 4, len(pages))):
                selected_indices.add(j)
    
    return [(pages[i][0], pages[i][1]) for i in sorted(selected_indices)]

def parse_financial_pdf(pdf_path: str, document_type: str = "unknown") -> dict:
    pages = extract_text_from_pdf(pdf_path)

    if document_type == "annual_report":
        relevant_pages = extract_financial_sections(pages)
    else:
        relevant_pages = pages

    full_text = "\n\n".join([f"[Page {pn}]\n{text}" for pn, text in relevant_pages])

    tables = extract_tables_from_pdf(pdf_path)
    table_text = "\n\n".join([df.to_string(index=False) for df in tables[:10]])

    return {
        "document_type": document_type,
        "total_pages": len(pages),
        "relevant_pages": len(relevant_pages),  # assuming to be 20-40 out of 200
        "tables_found": len(tables),
        "raw_text": full_text[:60_000],
        "table_text": table_text[:30_000],
    }