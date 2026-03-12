# Ingestion Pipeline

Parses uploaded financial documents (PDF / CSV) and extracts structured financial data using Google Gemini 2.5 Flash. Automatically triggers the research pipeline after processing.

## Endpoint

```
POST /ingest/document
```

**Content-Type:** `multipart/form-data`

| Field | Type | Description |
|-------|------|-------------|
| `file` | File | PDF or CSV financial document |
| `metadata` | string (JSON) | Company info and document type mapping |

### Metadata Schema

```json
{
  "company_name": "Rajesh Industries Pvt Ltd",
  "documents": [
    {
      "document_type": "annual_report",
      "file_name": "rajesh_ar_2025.pdf"
    }
  ],
  "metadata": {
    "sector": "manufacturing",
    "location": "India"
  },
  "promoters": ["Rajesh Kumar"]
}
```

Supported `document_type` values: `annual_report`, `bank_statement`, `gst_return`

## Internal Flow

```
Upload → Save to storage/documents/
       → Dispatch to PDF or CSV parser
       → Gemini 2.5 Flash → StructuredFinancialOutput (JSON)
       → Auto-POST to /research/analyze
       → Return research response
```

## Parsers

### PDF Parser (`parser/pdf_parser.py`)
- Uses PyMuPDF (`fitz`) for text and table extraction
- For annual reports: smart page filtering using financial keyword scoring and number-density heuristics (skips noise pages like Chairman's Message, CSR, etc.)
- Extracts up to 10 tables and 60K chars of text from relevant pages

### CSV Parser (`parser/csv_parser.py`)
- Reads via pandas
- Returns full text representation for Gemini processing

## Output Schema

`StructuredFinancialOutput` contains:
- `financial_summary` — revenue, profit, assets, liabilities, net worth
- `financial_ratios` — D/E, current ratio, profit margin, DSCR
- `cashflow_analysis` — avg inflow/outflow, volatility
- `anomalies_detected` — revenue drops, unusual transactions, GST mismatches
- `parsed_documents` — per-document key findings

