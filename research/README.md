# Research Pipeline

Performs external intelligence gathering on a company using web search, article scraping, and LLM-based risk analysis. Produces structured risk signals and categorized insights with full pipeline transparency logs.

## Endpoint

```
POST /research/analyze
```

### Request Body

```json
{
  "company_name": "Rajesh Industries Pvt Ltd",
  "sector": "manufacturing",
  "promoters": ["Rajesh Kumar"],
  "financial_data": { ... }
}
```

`financial_data` is the `StructuredFinancialOutput` from the ingestion pipeline (optional but recommended — anomalies drive targeted search queries).

## 6-Stage Pipeline

```
Stage 1: Query Generation
   ├── Company-specific queries (news, fraud, litigation, regulatory)
   ├── Promoter background checks
   ├── Sector outlook queries
   └── Anomaly-driven queries (from ingestion)

Stage 2: Search Retrieval
   └── Serper API (Google search) → deduplicated results

Stage 3: Article Extraction
   └── trafilatura → clean article text (top 3 successful extractions)

Stage 4: LLM Analysis
   └── GPT-5-nano (AIPipe) → chain-of-thought risk analysis per article
       (Entities → Event → Risk Interpretation → Severity → Evidence)

Stage 5: Risk Signal Extraction
   └── GPT-5-nano → consolidated JSON risk signals with deduplication

Stage 6: Structured Summary
   └── GPT-5-nano → research_summary, company_news, promoter_risks, sector_trends
```

## Response

```json
{
  "research_summary": "Executive summary of findings",
  "company_news": ["..."],
  "promoter_risks": ["..."],
  "sector_trends": ["..."],
  "risk_signals": [
    {
      "risk_type": "litigation",
      "entity": "Company X",
      "severity": "4",
      "source": "article URL",
      "evidence": "supporting quote",
      "confidence": "high",
      "reasoning": {}
    }
  ],
  "pipeline_logs": [
    {
      "stage": "query_generation",
      "timestamp": "2026-03-12T10:00:00Z",
      "data": { ... }
    }
  ],
  "financial_data": { ... }
}
```

## Pipeline Transparency

Every stage emits a structured log entry via `PipelineLogger`. The `pipeline_logs` array in the response provides full visibility into what queries were generated, how many results came back, which articles were extracted (and which failed), what the LLM analyzed, and what signals were produced. This supports explainability requirements for credit decisions downstream.

## Risk Signal Types

| Type | Description |
|------|-------------|
| `litigation` | Lawsuits, court cases, legal disputes |
| `regulatory` | RBI actions, SEBI orders, compliance violations |
| `fraud` | Fraud investigations, scam allegations |
| `industry` | Sector-wide risks, market downturns |
| `reputational` | Negative press, public controversies |

Severity scale: `1` (minimal) to `5` (critical). A severity-5 signal triggers automatic rejection in the recommendation stage.
