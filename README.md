# Intelli-Credit AI

AI-powered credit decisioning system that automates the entire loan appraisal pipeline — from document ingestion to research intelligence to credit scoring and CAM (Credit Appraisal Memo) generation.

## Architecture

```
POST /ingest/document        →  Parse financial documents (PDF/CSV)
         │                        Gemini 2.5 Flash → Structured JSON
         ▼
POST /research/analyze       →  External intelligence gathering
         │                        Serper API → Web scraping → GPT-5-nano risk analysis
         ▼
POST /recommend/             →  Five Cs credit scoring + decision logic
         │                        Gemini 2.5 Flash → CAM (.docx + .pdf)
         ▼
GET  /recommend/cam/{file}   →  Download CAM Word document
GET  /recommend/pdf/{file}   →  Download CAM PDF
```

## Project Structure

```
Intelli-Credit-AI/
├── main.py                          # FastAPI app entrypoint
├── requirements.txt
│
├── common/                          # Shared utilities
│   ├── config.py                    # Environment variables (API keys)
│   ├── gemini_client.py             # Google Gemini client factory
│   ├── aipipe_client.py             # AIPipe (OpenAI-compatible) client
│   └── utils.py
│
├── ingestion/                       # Stage 1: Document parsing
│   ├── router.py                    # POST /ingest/document
│   ├── service.py                   # Orchestration: parse → summarize → research
│   ├── summarizer.py                # Gemini-based financial data extraction
│   ├── prompts.py                   # System prompt for JSON extraction
│   ├── schemas.py                   # StructuredFinancialOutput models
│   └── parser/
│       ├── dispatcher.py            # Route to PDF or CSV parser
│       ├── pdf_parser.py            # PyMuPDF: page filtering + table extraction
│       ├── csv_parser.py            # Pandas CSV parser
│       └── constants.py             # Financial keyword lists
│
├── research/                        # Stage 2: External intelligence
│   ├── router.py                    # POST /research/analyze
│   ├── service.py                   # 6-stage research pipeline
│   ├── search_service.py            # Serper API query generation + search
│   ├── scraper.py                   # Web article extraction (trafilatura)
│   ├── analyzer.py                  # LLM-based risk analysis (AIPipe)
│   ├── prompts.py                   # Chain-of-thought analysis prompts
│   ├── pipeline_logger.py           # Structured pipeline transparency logs
│   └── schemas.py                   # Request/Response + RiskSignal models
│
├── recommendation/                  # Stage 3: Credit scoring + CAM
│   ├── router.py                    # POST /recommend/ + GET download endpoints
│   ├── service.py                   # Orchestration: score → decide → generate CAM
│   ├── scorer.py                    # Five Cs rule-based scoring engine (0–100)
│   ├── decision.py                  # Loan amount, rate, tenor, approve/reject logic
│   ├── cam_generator.py             # Gemini narrative + python-docx + PDF
│   ├── prompts.py                   # CAM generation prompt
│   └── schemas.py                   # Five Cs, CreditDecision, Request/Response
│
└── storage/
    ├── documents/                   # Uploaded financial documents
    └── cam/                         # Generated CAM reports (.docx + .pdf)
```

## Setup

### Prerequisites

- Python 3.11+
- [uv](https://docs.astral.sh/uv/) (recommended) or pip
- Microsoft Word (Windows — required for PDF conversion via `docx2pdf`)

### Installation

```bash
git clone https://github.com/your-username/Intelli-Credit-AI.git
cd Intelli-Credit-AI

# Using uv
uv venv
uv pip install -r requirements.txt

# Or using pip
python -m venv .venv
.venv\Scripts\activate
pip install -r requirements.txt
```

### Environment Variables

Create a `.env` file in the project root:

```env
GEMINI_API_KEY=your_google_gemini_api_key
SERPER_API_KEY=your_serper_dev_api_key
AIPIPE_API_KEY=your_aipipe_api_key
```

| Key | Used for |
|-----|----------|
| `GEMINI_API_KEY` | Document summarization (ingestion) + CAM narrative generation |
| `SERPER_API_KEY` | Web search queries in the research pipeline |
| `AIPIPE_API_KEY` | GPT-5-nano via AIPipe for risk analysis |

### Running

```bash
uv run frontend_server.py
# or
python frontend_server.py
```

Server starts at `http://localhost:8000/`.
Go to `http://localhost:8000/ui` for dedicated UI
Open `http://localhost:8000/docs` for the Swagger UI.

## API Endpoints

| Method | Endpoint | Description |
|--------|----------|-------------|
| `GET` | `/` | Health check |
| `GET` | `/docs` | Swagger UI |
| `POST` | `/ingest/document` | Upload financial docs → structured JSON |
| `POST` | `/research/analyze` | Run external research pipeline |
| `POST` | `/recommend/` | Credit scoring + CAM generation |
| `GET` | `/recommend/cam/{filename}` | Download CAM (.docx) |
| `GET` | `/recommend/pdf/{filename}` | Download CAM (.pdf) |

## Usage Flow

**Step 1 — Ingest:** Upload a PDF/CSV financial document with metadata via `/ingest/document`. The pipeline parses, extracts financial data, and auto-triggers the research stage.

**Step 2 — Research (or call directly):** `POST /research/analyze` with company details. Returns risk signals, company news, promoter risks, and sector trends with full pipeline logs.

**Step 3 — Recommend:** `POST /recommend/` with the research output + loan details:

```json
{
  "company_name": "Rajesh Industries Pvt Ltd",
  "sector": "manufacturing",
  "loan_requested": 5000000,
  "collateral_value": 8000000,
  "collateral_description": "Residential property, registered mortgage",
  "promoters": ["Rajesh Kumar"],
  "research_summary": "...",
  "company_news": ["..."],
  "promoter_risks": ["..."],
  "sector_trends": ["..."],
  "risk_signals": [...],
  "financial_data": {...}
}
```

**Step 4 — Download:** Use `cam_report_url` and `cam_pdf_url` from the response to download the generated CAM document.

## Credit Scoring Model

Transparent, rule-based Five Cs scorecard (0–100):

| Parameter | Max Score | Source Data |
|-----------|-----------|-------------|
| Character | 25 | Risk signals, promoter risks |
| Capacity | 25 | DSCR, profit margin, cashflow volatility |
| Capital | 20 | D/E ratio, net worth vs loan amount |
| Collateral | 15 | Loan-to-value ratio |
| Conditions | 15 | Sector trends, industry risk signals |

### Decision Bands

| Score | Status | Loan % | Rate | Tenor |
|-------|--------|--------|------|-------|
| 75–100 | Approved | 100% | 10% p.a. | 60 months |
| 60–74 | Approved | 80% | 12% p.a. | 48 months |
| 50–59 | Approved | 60% | 14% p.a. | 36 months |
| 40–49 | Conditional | 40% | 16% p.a. | 24 months |
| < 40 | Rejected | — | — | — |

Any severity-5 risk signal triggers automatic rejection regardless of score.

## Tech Stack

- **Framework:** FastAPI + Uvicorn
- **LLMs:** Google Gemini 2.5 Flash, GPT-5-nano (via AIPipe)
- **Document Parsing:** PyMuPDF, pandas
- **Web Research:** Serper API, trafilatura
- **Document Generation:** python-docx, docx2pdf
- **Data Validation:** Pydantic v2

## License

This project is licensed under the MIT License — see the [LICENSE](LICENSE) file.
