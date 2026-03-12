# Intelli-Credit AI — Presentation Slide Deck Content

> Copy-paste ready content for PowerPoint / Google Slides / Canva
> Suggested theme: Dark navy background, gold/amber accents, clean sans-serif (Inter or Montserrat)
> Total slides: 18

---

## SLIDE 1 — Title Slide

**HEADLINE:**
# Intelli-Credit AI
### AI-Powered Credit Decisioning System

**SUBTEXT:**
> From document upload to CAM generation — fully automated, explainable, and auditable.

**VISUAL:** System diagram thumbnail or abstract AI/banking imagery

---

## SLIDE 2 — The Problem We Solve

**TITLE:** The Challenge with Traditional Credit Appraisal

**3-COLUMN LAYOUT:**

| ⏱ Slow | 👁 Subjective | 📄 Manual |
|--------|--------------|----------|
| 5–15 days per appraisal | Different analysts, different conclusions | 50–200 page reports read manually |
| Committee scheduling delays | No standardized scoring | Hand-written CAM documents |
| Backlogs during peak periods | Promoter research is hit-or-miss | No audit trail |

**BOTTOM CALLOUT:**
> "Banks spend thousands of analyst-hours each year on appraisals that could be automated."

---

## SLIDE 3 — The Solution

**TITLE:** Intelli-Credit AI: End-to-End Automation

**VISUAL (4-step horizontal flow):**
```
[📄 Upload Docs]  →  [🔍 Research Company]  →  [🏦 Score & Decide]  →  [📋 Download CAM]
   seconds              15–30 seconds            < 1 second             < 2 seconds
```

**BULLET POINTS:**
- Processes PDF/CSV financial documents instantly
- Scours the web for risk signals, litigation, and sector data
- Scores on the internationally-recognised Five Cs framework
- Generates a professional Credit Appraisal Memo (Word + PDF)

**CALLOUT BOX:**
> **Full loan appraisal in under 60 seconds**

---

## SLIDE 4 — System Architecture Overview

**TITLE:** Three-Stage Pipeline Architecture

**VISUAL:** (Use the Mermaid flowchart from WIREFRAMES.md, Wireframe 1)

```
STAGE 1          STAGE 2          STAGE 3
────────         ────────         ────────
INGESTION    →   RESEARCH     →   RECOMMENDATION
                
POST             POST             POST
/ingest/         /research/       /recommend/
document         analyze
                
Gemini           GPT-5-nano       Gemini
2.5 Flash        + Serper API     2.5 Flash
PyMuPDF          trafilatura      python-docx
```

---

## SLIDE 5 — Stage 1: Document Ingestion

**TITLE:** Stage 1 — Smart Financial Document Parsing

**LEFT COLUMN (What it does):**
- Accepts: Annual Reports (PDF), Bank Statements (CSV/PDF), GST Returns (CSV)
- PyMuPDF extracts text from relevant pages only
- Keyword scoring filters out noise (CSR, Chairman's letter, awards)
- Up to 10 tables + 60,000 characters extracted
- Gemini 2.5 Flash converts raw text → structured JSON

**RIGHT COLUMN (Output — StructuredFinancialOutput):**
```
Revenue:       ₹45 Cr
Net Profit:    ₹6.75 Cr
Net Worth:     ₹22 Cr
DSCR:          1.62
D/E Ratio:     0.73
Profit Margin: 15%
Volatility:    Low
Anomalies:     None detected
```

**BOTTOM:** Auto-triggers Stage 2 (Research) immediately after

---

## SLIDE 6 — Stage 2: Research Intelligence

**TITLE:** Stage 2 — 6-Stage External Intelligence Pipeline

**NUMBERED LIST (vertical):**

1. **Query Generation** — Targeted searches for fraud, litigation, regulatory actions, promoter checks, sector trends
2. **Google Search** — Serper API retrieves 20+ unique results
3. **Article Extraction** — trafilatura cleans article text (top 3 successful)
4. **LLM Risk Analysis** — GPT-5-nano performs chain-of-thought analysis per article
5. **Signal Consolidation** — Deduplicated JSON risk signals with severity scores
6. **Structured Summary** — Research summary, news, promoter risks, sector trends

**CALLOUT:**
> Every stage is logged → full pipeline transparency for audit

---

## SLIDE 7 — Risk Signal Framework

**TITLE:** Risk Signal Classification

**TABLE:**

| Risk Type | Examples | Max Severity |
|-----------|----------|-------------|
| Fraud | ED investigation, fraud FIR | ⚠️ Critical (5) |
| Regulatory | RBI penalty, SEBI order | ⚠️ Critical (5) |
| Litigation | Major court case | 🔴 High (4) |
| Industry | Sector collapse, macro risk | 🟡 Moderate (3) |
| Reputational | Negative press coverage | 🟢 Low (1–2) |

**CALLOUT BOX (RED):**
> **Any Severity-5 signal = Automatic Hard Rejection**
> Regardless of credit score

---

## SLIDE 8 — Stage 3: Five Cs Scoring Engine

**TITLE:** Stage 3 — Transparent Five Cs Credit Scoring

**5-CARD LAYOUT:**

```
┌─────────────────┐  ┌─────────────────┐  ┌─────────────────┐
│   CHARACTER     │  │    CAPACITY     │  │     CAPITAL     │
│    max 25       │  │    max 25       │  │    max 20       │
│                 │  │                 │  │                 │
│ Risk signals    │  │ DSCR (10 pts)   │  │ D/E ratio       │
│ + promoter      │  │ Profit margin   │  │ (10 pts)        │
│   risks         │  │ (8 pts)         │  │                 │
│                 │  │ Cashflow        │  │ Net worth       │
│                 │  │ volatility      │  │ vs loan         │
│                 │  │ (7 pts)         │  │ (10 pts)        │
└─────────────────┘  └─────────────────┘  └─────────────────┘

┌─────────────────┐  ┌─────────────────┐
│   COLLATERAL    │  │   CONDITIONS    │
│    max 15       │  │    max 15       │
│                 │  │                 │
│ Loan-to-Value   │  │ Sector trends   │
│ ratio           │  │ keyword         │
│                 │  │ sentiment       │
│ LTV ≤50%: 15   │  │ Baseline: 10   │
│ LTV ≤70%: 11   │  │ Positive: +5   │
│ LTV ≤80%: 7    │  │ Negative: −5   │
│ LTV >80%: 3    │  │                 │
└─────────────────┘  └─────────────────┘

                 TOTAL: 0 – 100
```

---

## SLIDE 9 — Decision Bands

**TITLE:** Credit Decision Logic

**TABLE (large, bold, colour-coded):**

| Score Range | Status | Loan Amount | Interest Rate | Tenor |
|-------------|--------|-------------|---------------|-------|
| 🟢 75 – 100 | **APPROVED** | 100% of requested | 10% p.a. | 60 months |
| 🟡 60 – 74 | **APPROVED** | 80% of requested | 12% p.a. | 48 months |
| 🟠 50 – 59 | **APPROVED** | 60% of requested | 14% p.a. | 36 months |
| 🔴 40 – 49 | **CONDITIONAL** | 40% of requested | 16% p.a. | 24 months |
| ⛔ < 40 | **REJECTED** | — | — | — |
| ⛔ Severity-5 signal | **HARD REJECT** | — | — | — |

---

## SLIDE 10 — Worked Example: Rajesh Industries

**TITLE:** Example: Rajesh Industries Pvt Ltd

**TWO-COLUMN LAYOUT:**

**LEFT — Input:**
```
Company:      Rajesh Industries Pvt Ltd
Sector:       Manufacturing
Promoter:     Rajesh Kumar
Document:     Annual Report 2025 (PDF, 120 pages)

Loan Request: ₹ 50,00,000
Collateral:   ₹ 80,00,000 (residential property)
```

**RIGHT — Key Financials Extracted:**
```
Revenue:       ₹ 45 Cr
Net Profit:    ₹  6.75 Cr  (15% margin)
Net Worth:     ₹ 22 Cr
DSCR:          1.62  ✓
D/E Ratio:     0.73  ✓
Volatility:    Low   ✓
Anomalies:     None
```

---

## SLIDE 11 — Worked Example: Scoring Breakdown

**TITLE:** Example: Five Cs Scoring Result

**SCORECARD TABLE + BAR CHART:**

```
CHARACTER   ████████████████████░░░░  21 / 25  (84%)
             ↳ Minor tax dispute — −4 pts

CAPACITY    ████████████████████████  25 / 25  (100%)
             ↳ DSCR 1.62 + 15% margin + Low volatility

CAPITAL     ████████████████████████  20 / 20  (100%)
             ↳ D/E 0.73, Net worth 4.4× loan

COLLATERAL  █████████████████░░░░░░░  11 / 15  (73%)
             ↳ LTV = 62.5% → adequate cover

CONDITIONS  ████████████████████░░░░  13 / 15  (87%)
             ↳ Manufacturing PMI at 14-month high

TOTAL       ████████████████████████  90 / 100
```

---

## SLIDE 12 — Worked Example: Decision + CAM

**TITLE:** Example: Decision & Output

**LEFT — Decision (GREEN BOX):**
```
✅  STATUS:    APPROVED

    Loan Amount:   ₹ 50,00,000
    Interest Rate: 10.0% per annum
    Tenor:         60 months (5 years)

    Score:  90/100  (Band: 75–100)
    Reason: Approved — strong capacity,
            clean promoter profile,
            positive sector outlook.
```

**RIGHT — Output Files:**
```
📄  Rajesh_Industries_a1b2c3_CAM.docx
    ↳ 7-section Word document

📋  Rajesh_Industries_a1b2c3_CAM.pdf
    ↳ PDF export (ready to share)

🔗  Available at:
    GET /recommend/cam/{filename}
    GET /recommend/pdf/{filename}
```

---

## SLIDE 13 — CAM Document Structure

**TITLE:** Generated Credit Appraisal Memo (CAM)

**7-SECTION VISUAL (vertical numbered list with icons):**

```
1. 📋  Executive Summary        → AI-generated credit proposal overview
2. 🏢  Applicant Profile        → Company, sector, promoters, loan request
3. 📊  Five Cs Analysis         → Each C: narrative + score table
4. 💰  Financial Analysis       → Key metrics table (revenue, ratios, etc.)
5. ⚠️  Risk Matrix              → All risk signals with evidence + severity
6. 🎯  Credit Score Summary     → Tabulated Five Cs scorecard
7. ✅  Recommendation           → Final decision with full reasoning
```

**CALLOUT:** Narratives generated by Gemini 2.5 Flash | Formatted by python-docx | Exported as PDF

---

## SLIDE 14 — Technology Stack

**TITLE:** Built On Modern, Production-Grade Stack

**4-QUADRANT LAYOUT:**

```
┌──────────────────────────────┬──────────────────────────────┐
│  🤖  AI / LLMs               │  🌐  API & Web               │
│                              │                              │
│  Google Gemini 2.5 Flash     │  FastAPI + Uvicorn           │
│  GPT-5-nano (AIPipe)         │  Serper API (Google Search)  │
│  OpenAI-compatible API       │  trafilatura (scraping)      │
│  Pydantic v2                 │  httpx (async HTTP)          │
├──────────────────────────────┼──────────────────────────────┤
│  📄  Document Processing     │  📁  Storage & Output        │
│                              │                              │
│  PyMuPDF (fitz)              │  Local filesystem            │
│  pandas                      │  python-docx (Word)          │
│  python-dotenv               │  docx2pdf (PDF)              │
│  Pydantic v2                 │  storage/documents/          │
│                              │  storage/cam/                │
└──────────────────────────────┴──────────────────────────────┘
```

---

## SLIDE 15 — Pipeline Transparency & Auditability

**TITLE:** Explainability at Every Step

**3-COLUMN LAYOUT:**

| 📊 Transparent Scoring | 🔍 Research Logs | 📋 Documented Decisions |
|------------------------|-----------------|------------------------|
| Every point awarded or deducted has a written reason | Every stage logged: queries, results, extracted text, analysis | CAM documents decision with full narrative reasoning |
| Rules are fixed and inspectable in code | Pipeline logs returned in API response | Score explanation per parameter |
| No black-box AI scoring | Article sources cited with evidence quotes | Weakest C identified and named |

**CALLOUT:**
> Explainable AI is not optional in regulated banking — it is mandatory.

---

## SLIDE 16 — Security Architecture

**TITLE:** Security by Design

**BULLET LIST:**
- 🔑 **API keys** stored in `.env`, never in code or version control
- 🏷️ **File uploads** renamed to UUID — no user-controlled paths reach filesystem
- ✅ **Pydantic v2** validates and sanitises all API inputs at boundaries
- ⏱️ **Request timeouts** on all external HTTP calls (300s for research pipeline)
- 🗂️ **Storage isolation** — uploads and generated files in separate directories
- 🔒 **No SQL** — no databases, eliminating SQL injection risk
- 📝 **Audit trail** — every research decision and score reason is persisted in CAM

---

## SLIDE 17 — Setup & Usage

**TITLE:** Getting Started in 3 Steps

**STEP 1 — Install:**
```bash
git clone https://github.com/your-org/Intelli-Credit-AI
cd Intelli-Credit-AI
uv venv
uv pip install -r requirements.txt
```

**STEP 2 — Configure `.env`:**
```env
GEMINI_API_KEY=your_gemini_key
SERPER_API_KEY=your_serper_key
AIPIPE_API_KEY=your_aipipe_key
```

**STEP 3 — Run:**
```bash
python main.py
# → http://localhost:8000/docs
```

**System Requirements:**
- Python 3.11+
- Windows (for docx2pdf — requires Microsoft Word)
- uv (recommended) or pip

---

## SLIDE 18 — Summary & Roadmap

**TITLE:** What Intelli-Credit AI Delivers Today

**LEFT — Delivered:**
- ✅ Full PDF/CSV document parsing (Gemini-powered)
- ✅ 6-stage external research pipeline
- ✅ Deterministic, rule-based Five Cs scoring (0–100)
- ✅ Band-based decision logic with hard-rejection rules
- ✅ Professional CAM generation (.docx + .pdf)
- ✅ Full pipeline transparency logs
- ✅ Swagger UI for interactive testing

**RIGHT — Potential Roadmap:**
- 🔲 Web dashboard / front-end UI
- 🔲 Multi-language document support
- 🔲 Database persistence (PostgreSQL)
- 🔲 Role-based access (maker-checker)
- 🔲 Bureau data integration (CIBIL / CRIF)
- 🔲 Portfolio-level risk dashboards
- 🔲 Cloud deployment (AWS / Azure)

---

## SPEAKER NOTES (Key Talking Points)

### On the Problem (Slide 2):
> "A typical bank's credit team processes 50–200 applications per month. Each one involves manual reading of dense financial documents, ad-hoc internet searches, and writing a memo from scratch. This is a process ripe for automation."

### On Stage 1 (Slide 5):
> "The PDF parser doesn't just dump the whole document into the AI. It scores every page by financial keyword density and discards noise pages like the Chairman's message or CSR section. This keeps the AI focused and reduces cost."

### On Stage 2 (Slide 6):
> "The research pipeline doesn't trust the applicant's own documents alone. It goes out to the public internet and looks for litigation records, regulatory actions, promoter fraud cases, and sector trends. This is what a good analyst would do manually."

### On Transparency (Slide 15):
> "Every single point added or deducted in the Five Cs score has a written explanation. You can see exactly why a company scored 21 on Character instead of 25. This is critical for RBI compliance and for loan officers to defend decisions in committee."

### On Security (Slide 16):
> "No user-controlled filename ever reaches the filesystem. Every upload is renamed to a UUID. We use Pydantic for strict input validation. API keys are environment variables only. We've thought about OWASP Top 10 throughout."

### On the Worked Example (Slides 10–12):
> "Rajesh Industries scored 90 out of 100. The only deduction was 4 points on Character due to a minor ITAT tax dispute — which is a routine income tax assessment, not a fraud. The system correctly distinguished that and approved the full loan at the best rate."
