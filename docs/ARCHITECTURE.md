# Intelli-Credit AI — Full Architectural Documentation

> **Version:** 1.0  |  **Date:** March 12, 2026  |  **Status:** Production

---

## 1. System Overview

**Intelli-Credit AI** is an end-to-end AI-powered credit decisioning platform that automates the complete loan appraisal cycle — from raw financial document intake through external intelligence gathering to final credit scoring and professional memo generation. The system replaces weeks of manual analyst work with a deterministic, explainable, and auditable AI pipeline that returns a credit decision in seconds.

### Why It Exists

Traditional credit appraisal involves:
- Manually reading 50–200 page annual reports
- Googling company news, promoter backgrounds, and sector risks
- Hand-computing financial ratios and DSCR
- Writing a Credit Appraisal Memo (CAM) from scratch
- Committee review based on subjective interpretation

**Intelli-Credit AI** automates all of this — with verifiable evidence at every step.

---

## 2. High-Level Architecture

```
┌─────────────────────────────────────────────────────────────────────┐
│                        INTELLI-CREDIT AI                            │
│                     FastAPI  ·  Python 3.11+                        │
│                     http://localhost:8000                           │
└────────────────────────────┬────────────────────────────────────────┘
                             │
        ┌────────────────────┼────────────────────┐
        ▼                    ▼                    ▼
┌───────────────┐   ┌────────────────┐   ┌───────────────────┐
│   INGESTION   │   │   RESEARCH     │   │  RECOMMENDATION   │
│   PIPELINE    │──▶│   PIPELINE     │──▶│    PIPELINE       │
│               │   │                │   │                   │
│ POST          │   │ POST           │   │ POST              │
│ /ingest/      │   │ /research/     │   │ /recommend/       │
│ document      │   │ analyze        │   │                   │
└───────────────┘   └────────────────┘   └───────────────────┘
        │                    │                    │
        ▼                    ▼                    ▼
 Gemini 2.5 Flash     GPT-5-nano (AIPipe)   Gemini 2.5 Flash
 PyMuPDF / Pandas     Serper API             python-docx
                       trafilatura            docx2pdf
```

---

## 3. Pipeline Architecture — Stage by Stage

### Stage 1: Document Ingestion

**Entry Point:** `POST /ingest/document`

**Purpose:** Parse raw financial documents uploaded by loan officers and extract structured, machine-readable financial data.

```
Client uploads PDF / CSV
          │
          ▼
  Save to storage/documents/
          │
          ▼
  ┌───────────────────┐
  │   Dispatcher      │──── .pdf ──▶ PDF Parser (PyMuPDF)
  │  (dispatcher.py)  │                    │
  └───────────────────┘                    ├─ Page text extraction
                       ──── .csv ──▶       ├─ Financial keyword scoring
                            CSV Parser     ├─ Noise page filtering
                            (pandas)       ├─ Table extraction (≤10 tables)
                                           └─ 60K char text budget
          │
          ▼
  Gemini 2.5 Flash
  (summarizer.py)
  → StructuredFinancialOutput (JSON)
          │
          ▼
  Auto-POST → /research/analyze
```

**PDF Parser Intelligence:**
- Loads each page and scores it by financial keyword density
- Discards noise sections: Chairman's Message, CSR reports, Board profiles
- Prioritises high-value sections: P&L, Balance Sheet, Cash Flow, Notes
- Caps output at 60,000 characters + 10 tables to fit within LLM context window

**Supported Document Types:**

| Type | Key Data Extracted |
|------|--------------------|
| `annual_report` | Revenue, profit, assets, liabilities, net worth, ratios |
| `bank_statement` | Monthly inflows/outflows, volatility, transaction anomalies |
| `gst_return` | Declared turnover, GST consistency, filing regularity |

---

### Stage 2: Research Pipeline

**Entry Point:** `POST /research/analyze`

**Purpose:** Gather external intelligence on the company, its promoters, and sector from the public internet, then use an LLM to extract structured risk signals.

```
ResearchRequest (company_name, sector, promoters, financial_data)
          │
          ▼
  ┌──────────────────────────────────────────────────────────────┐
  │  STAGE 1: Query Generation (search_service.py)              │
  │  ─────────────────────────────────────────────────────────   │
  │  Company queries:  "[name] fraud", "[name] litigation",      │
  │                    "[name] RBI action", "[name] latest news" │
  │  Promoter queries: "[promoter] background check"            │
  │  Sector queries:   "[sector] India 2026 outlook"            │
  │  Anomaly queries:  driven by detected financial anomalies   │
  └──────────────────────────────────────────────────────────────┘
          │
          ▼
  ┌──────────────────────────────────────────────────────────────┐
  │  STAGE 2: Search Retrieval (Serper API)                     │
  │  ─────────────────────────────────────────────────────────   │
  │  Google Search results (deduplicated by URL)                 │
  └──────────────────────────────────────────────────────────────┘
          │
          ▼
  ┌──────────────────────────────────────────────────────────────┐
  │  STAGE 3: Article Extraction (trafilatura)                  │
  │  ─────────────────────────────────────────────────────────   │
  │  Clean article text from top 3 extractable URLs             │
  │  Logs failures (404, timeout, anti-bot blocks)              │
  └──────────────────────────────────────────────────────────────┘
          │
          ▼
  ┌──────────────────────────────────────────────────────────────┐
  │  STAGE 4: LLM Analysis (GPT-5-nano via AIPipe)             │
  │  ─────────────────────────────────────────────────────────   │
  │  Chain-of-thought per article:                              │
  │    1. Entity Identification                                 │
  │    2. Event Extraction                                      │
  │    3. Risk Interpretation                                   │
  │    4. Severity Rating (1–5)                                 │
  │    5. Evidence Extraction                                   │
  └──────────────────────────────────────────────────────────────┘
          │
          ▼
  ┌──────────────────────────────────────────────────────────────┐
  │  STAGE 5: Risk Signal Consolidation (GPT-5-nano)           │
  │  ─────────────────────────────────────────────────────────   │
  │  Deduplicated JSON risk signals                             │
  │  Each: risk_type, entity, severity (1–5), evidence, source  │
  └──────────────────────────────────────────────────────────────┘
          │
          ▼
  ┌──────────────────────────────────────────────────────────────┐
  │  STAGE 6: Structured Summary (GPT-5-nano)                  │
  │  ─────────────────────────────────────────────────────────   │
  │  research_summary, company_news[], promoter_risks[],        │
  │  sector_trends[]                                            │
  └──────────────────────────────────────────────────────────────┘
```

**Risk Signal Types & Severity:**

| Type | Examples | Severity 5 Triggers Rejection? |
|------|----------|--------------------------------|
| `fraud` | Fraud FIR, ED investigation | Yes |
| `regulatory` | RBI penalty, SEBI action | Yes |
| `litigation` | Major court case | Yes |
| `industry` | Sector collapse | Rarely |
| `reputational` | Negative press | No |

---

### Stage 3: Recommendation Pipeline

**Entry Point:** `POST /recommend/`

**Purpose:** Score the applicant on the Five Cs of Credit, derive a loan decision, and generate a professional Credit Appraisal Memo (CAM).

```
RecommendationRequest (research output + loan specifics)
          │
          ├──▶ scorer.py ──▶ FiveCsScore (0–100)
          │         │
          │         ├─ Character (0–25):  risk_signals + promoter_risks
          │         ├─ Capacity  (0–25):  DSCR + profit margin + volatility
          │         ├─ Capital   (0–20):  D/E ratio + net worth coverage
          │         ├─ Collateral(0–15):  LTV ratio
          │         └─ Conditions(0–15):  sector trends sentiment
          │
          ├──▶ decision.py ──▶ CreditDecision
          │         │
          │         ├─ Hard reject if any severity-5 signal
          │         ├─ Reject if score < 40
          │         ├─ Score 40–49: Conditional, 40% loan, 16%, 24m
          │         ├─ Score 50–59: Approved, 60% loan, 14%, 36m
          │         ├─ Score 60–74: Approved, 80% loan, 12%, 48m
          │         └─ Score 75–100: Approved, 100% loan, 10%, 60m
          │
          └──▶ cam_generator.py ──▶ CAM (.docx + .pdf)
                    │
                    ├─ Gemini 2.5 Flash → narrative sections (JSON)
                    ├─ python-docx → structured Word document
                    └─ docx2pdf → PDF export
```

---

## 4. Five Cs Scoring Engine (Detailed)

### CHARACTER (max 25 pts)
Measures trustworthiness and past behaviour.

| Condition | Deduction |
|-----------|-----------|
| Risk signal severity 5 | −11 pts |
| Risk signal severity 4 | −8 pts |
| Risk signal severity 3 | −5 pts |
| Risk signal severity 2 | −3 pts |
| Risk signal severity 1 | −1 pt |
| Type = fraud | +2 extra pts deducted |
| Type = regulatory | +1 extra pt deducted |
| Type = litigation | +1 extra pt deducted |
| Per promoter risk (first 3) | −3 pts |
| No adverse signals | Full 25 pts awarded |

Maximum per signal deduction capped at 13 pts.

### CAPACITY (max 25 pts)
Measures ability to repay from business operations.

| Metric | Condition | Points |
|--------|-----------|--------|
| DSCR | ≥ 1.5 | 10/10 |
| DSCR | 1.25–1.5 | 8/10 |
| DSCR | 1.0–1.25 | 5/10 |
| DSCR | < 1.0 | 2/10 |
| Profit Margin | ≥ 15% | 8/8 |
| Profit Margin | 8–15% | 6/8 |
| Profit Margin | 0–8% | 4/8 |
| Profit Margin | Negative | 0/8 |
| Cashflow Volatility | Low | 7/7 |
| Cashflow Volatility | Moderate | 4/7 |
| Cashflow Volatility | High | 1/7 |

### CAPITAL (max 20 pts)
Measures financial strength and leverage.

| Metric | Condition | Points |
|--------|-----------|--------|
| D/E Ratio | < 1.0 | 10/10 |
| D/E Ratio | 1.0–2.0 | 7/10 |
| D/E Ratio | 2.0–3.0 | 4/10 |
| D/E Ratio | ≥ 3.0 | 1/10 |
| Net Worth Coverage | ≥ 3× loan | 10/10 |
| Net Worth Coverage | 2–3× loan | 7/10 |
| Net Worth Coverage | 1–2× loan | 4/10 |
| Net Worth Coverage | < 1× loan | 1/10 |

### COLLATERAL (max 15 pts)
Measures security coverage.

| LTV Ratio | Points |
|-----------|--------|
| ≤ 50% | 15 |
| 51–70% | 11 |
| 71–80% | 7 |
| > 80% | 3 |
| Unsecured | 5 |

### CONDITIONS (max 15 pts)
Measures external environment risk.

- Baseline: 10 pts
- Sector trend keywords: positive news → +5 pts; negative/downturn → −5 pts
- Industry-type risk signals trigger further deductions

---

## 5. CAM Document Structure

The generated Credit Appraisal Memo (Word + PDF) contains 7 sections:

| # | Section | Content |
|---|---------|---------|
| 1 | Executive Summary | AI-generated overview of the credit proposal (Gemini) |
| 2 | Applicant Profile | Company background, sector, promoter details |
| 3 | Five Cs Analysis | Each C with narrative + scoring breakdown |
| 4 | Financial Analysis | Metrics table: revenue, profit, ratios |
| 5 | Risk Matrix | All identified risks with evidence and severity |
| 6 | Credit Score Summary | Tabulated Five Cs scorecard |
| 7 | Recommendation & Decision | Final verdict with full reasoning |

---

## 6. Data Flow — End to End

```
INPUT: Annual Report PDF + Metadata
                    │
                    ▼
         ┌─────────────────────┐
         │  Ingestion Pipeline │
         │  Gemini 2.5 Flash   │
         └─────────┬───────────┘
                   │
         StructuredFinancialOutput:
         {
           revenue: ₹45Cr
           profit: ₹6.75Cr
           net_worth: ₹22Cr
           D/E: 0.8
           DSCR: 1.6
           profit_margin: 15%
           cashflow_volatility: "low"
           anomalies: []
         }
                   │
                   ▼
         ┌─────────────────────┐
         │  Research Pipeline  │
         │  GPT-5-nano + Serper│
         └─────────┬───────────┘
                   │
         ResearchOutput:
         {
           research_summary: "Rajesh Industries..."
           company_news: ["Company expanded..."]
           promoter_risks: []
           sector_trends: ["Manufacturing sector..."]
           risk_signals: [
             { risk_type: "litigation",
               severity: "2",
               evidence: "Minor tax dispute..." }
           ]
         }
                   │
                   ▼
         ┌─────────────────────┐
         │  Recommendation     │
         │  Five Cs Scorer     │
         └─────────┬───────────┘
                   │
         FiveCsScore:
         {
           character:  22  (sev-2 litigation −3)
           capacity:   25  (DSCR 1.6 + PM 15% + low vol)
           capital:    17  (D/E 0.8 + NW 4.4x loan)
           collateral: 15  (LTV = 5M/8M = 62.5% → 11 pts... wait LTV≤70% = 11)
           conditions: 13  (positive sector keywords)
           total:      92
         }

         Wait — let's recalculate for the example:
         Loan = ₹50L, Collateral = ₹80L → LTV = 62.5% → 11 pts collateral

         Revised:
         character:  22, capacity: 25, capital: 17,
         collateral: 11, conditions: 13 → TOTAL: 88/100
                   │
                   ▼
         CreditDecision:
         {
           status: "approved"
           loan_amount: ₹50,00,000 (100%)
           rate: 10% p.a.
           tenor: 60 months
         }
                   │
                   ▼
         CAM Document:
         Rajesh_Industries_a1b2c3_CAM.docx
         Rajesh_Industries_a1b2c3_CAM.pdf
```

---

## 7. API Contract

### POST /ingest/document
**Request:** `multipart/form-data`
- `files`: One or more PDF/CSV files
- `metadata`: JSON string with company info

**Response:** Full research pipeline output (ResearchResponse)

---

### POST /research/analyze
**Request:**
```json
{
  "company_name": "Rajesh Industries Pvt Ltd",
  "sector": "manufacturing",
  "promoters": ["Rajesh Kumar"],
  "financial_data": { ... StructuredFinancialOutput ... }
}
```

**Response:**
```json
{
  "research_summary": "Rajesh Industries Pvt Ltd is a mid-sized...",
  "company_news": ["Rajesh Industries wins ₹12Cr export order..."],
  "promoter_risks": [],
  "sector_trends": ["Indian manufacturing outperforms global peers in Q4 2025..."],
  "risk_signals": [
    {
      "risk_type": "litigation",
      "entity": "Rajesh Industries Pvt Ltd",
      "severity": "2",
      "source": "https://...",
      "evidence": "Minor income tax dispute filed in 2024...",
      "confidence": "medium",
      "reasoning": {}
    }
  ],
  "pipeline_logs": [ ... ],
  "financial_data": { ... }
}
```

---

### POST /recommend/
**Request:** Research output + loan specifics
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
  "promoter_risks": [],
  "sector_trends": ["..."],
  "risk_signals": [ ... ],
  "financial_data": { ... }
}
```

**Response:**
```json
{
  "company_name": "Rajesh Industries Pvt Ltd",
  "score_breakdown": {
    "character": 22,
    "capacity": 25,
    "capital": 17,
    "collateral": 11,
    "conditions": 13,
    "total": 88
  },
  "score_explanation": {
    "character_reasons": [
      "Risk signal: litigation on Rajesh Industries Pvt Ltd — severity 2. Deducted 4 pts."
    ],
    "capacity_reasons": [
      "DSCR = 1.60 (≥1.5) — excellent debt service capacity (10/10).",
      "Profit margin = 15.0% (≥15%) — strong profitability (8/8).",
      "Cashflow volatility: low — stable and predictable cash inflows (7/7)."
    ],
    "capital_reasons": [
      "D/E = 0.80 (<1.0) — low leverage, strong capital base (10/10).",
      "Net worth = 4.4x loan requested — strong capital coverage (10/10)."
    ],
    "collateral_reasons": [
      "LTV = 62.5% (≤70%) — adequate security cover (11/15)."
    ],
    "conditions_reasons": [
      "Sector trends positive (manufacturing growth) — Conditions awarded 13/15."
    ]
  },
  "decision": {
    "status": "approved",
    "loan_amount_recommended": 5000000,
    "interest_rate": 10.0,
    "tenor_months": 60,
    "primary_reason": "Approved with credit score 88/100. ...",
    "detailed_reasoning": "..."
  },
  "cam_report_url": "/recommend/cam/Rajesh_Industries_a1b2c3_CAM.docx",
  "cam_pdf_url": "/recommend/pdf/Rajesh_Industries_a1b2c3_CAM.pdf"
}
```

---

## 8. Technology Stack

| Layer | Technology | Purpose |
|-------|-----------|---------|
| API Framework | FastAPI + Uvicorn | REST API server, async endpoints |
| LLM (Primary) | Google Gemini 2.5 Flash | Document summarization, CAM narrative |
| LLM (Research) | GPT-5-nano via AIPipe | Risk analysis, signal extraction, summary |
| Web Search | Serper API (Google) | External search queries |
| Web Scraping | trafilatura | Article text extraction |
| Document Parsing | PyMuPDF (fitz) | PDF text and table extraction |
| Data Processing | pandas | CSV document parsing |
| Data Validation | Pydantic v2 | Request/response schema enforcement |
| Document Generation | python-docx | CAM Word document builder |
| PDF Export | docx2pdf | Word to PDF conversion (requires MS Word) |
| Environment | python-dotenv | API key management |

---

## 9. Security Architecture

- **API keys** are loaded exclusively from `.env` via `python-dotenv` — never hardcoded
- **File uploads** are saved with UUID-prefixed names to prevent path traversal
- **External HTTP calls** use `httpx.AsyncClient` with explicit timeouts (300s) to prevent hanging
- **Pydantic v2** validates all inputs at API boundaries — type-safe throughout
- **Storage isolation:** Uploaded docs go to `storage/documents/`, CAMs go to `storage/cam/`
- **No user-controlled filenames** reach the filesystem directly (UUID rename on upload)

---

## 10. Deployment Notes

- **OS requirement:** Windows (for `docx2pdf` — requires Microsoft Word installed)
- **Python:** 3.11+
- **Package manager:** `uv` recommended, `pip` supported
- **Port:** 8000 (configurable via `uvicorn`)
- **Swagger UI:** Available at `http://localhost:8000/docs`
- **Async throughout:** All pipelines are `async`/`await` — single Uvicorn worker handles concurrent requests

---

## 11. File & Module Reference

| File | Module | Responsibility |
|------|--------|---------------|
| `main.py` | App entrypoint | FastAPI init, router registration |
| `common/config.py` | Settings | Env var loading (GEMINI, SERPER, AIPIPE keys) |
| `common/gemini_client.py` | Gemini factory | Google Gemini SDK client |
| `common/aipipe_client.py` | AIPipe factory | OpenAI-compatible GPT-5-nano client |
| `ingestion/router.py` | POST /ingest/document | Request handling, multipart form |
| `ingestion/service.py` | Ingestion orchestrator | Save, parse, summarize, trigger research |
| `ingestion/summarizer.py` | Gemini summarizer | Structured JSON extraction from parsed text |
| `ingestion/parser/dispatcher.py` | Parser router | Route to PDF or CSV parser by extension |
| `ingestion/parser/pdf_parser.py` | PDF parser | PyMuPDF page filtering, table extraction |
| `ingestion/parser/csv_parser.py` | CSV parser | Pandas read, text serialization |
| `ingestion/parser/constants.py` | Keywords | Financial/noise keyword lists |
| `research/router.py` | POST /research/analyze | Request handling |
| `research/service.py` | Research orchestrator | 6-stage pipeline execution |
| `research/search_service.py` | Search | Query generation, Serper API calls |
| `research/scraper.py` | Scraper | trafilatura article extraction |
| `research/analyzer.py` | LLM analyzer | GPT-5-nano risk analysis per article |
| `research/pipeline_logger.py` | Logger | Structured stage-by-stage transparency logs |
| `recommendation/router.py` | POST /recommend/ | Request + download endpoints |
| `recommendation/service.py` | Recommendation orchestrator | Score, decide, generate CAM |
| `recommendation/scorer.py` | Five Cs engine | Rule-based deterministic scoring |
| `recommendation/decision.py` | Decision logic | Band-based loan terms derivation |
| `recommendation/cam_generator.py` | CAM generator | Gemini narrative + docx + PDF |
| `recommendation/prompts.py` | CAM prompt | Gemini prompt for narrative generation |
