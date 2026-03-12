import json
from research.schemas import ResearchRequest, ResearchResponse, RiskSignal
from research.pipeline_logger import PipelineLogger
from research.search_service import generate_queries, search_serper
from research.scraper import extract_article
from research.analyzer import analyze_article, extract_risk_signals, MODEL
from research.prompts import get_summary_prompt
from common.aipipe_client import get_aipipe_client


async def perform_research(request: ResearchRequest) -> ResearchResponse:
    """Orchestrate the full research pipeline with logging at every stage."""
    logger = PipelineLogger()
    client = get_aipipe_client()

    # ── Stage 1: Query Generation ──────────────────────────────────────
    anomalies = []
    if request.financial_data:
        anomalies = [a.model_dump() for a in request.financial_data.anomalies_detected]

    queries = generate_queries(
        request.company_name, 
        request.sector, 
        request.promoters, 
        anomalies
    )
    logger.log("query_generation", {"queries": queries})

    # ── Stage 2: Search Retrieval ──────────────────────────────────────
    all_search_results = []
    for query in queries:
        results = await search_serper(query)
        all_search_results.extend(results)

    # Deduplicate by link
    seen_links: set[str] = set()
    unique_results = []
    for r in all_search_results:
        if r.link not in seen_links:
            seen_links.add(r.link)
            unique_results.append(r)

    logger.log("search_results", {
        "total_results": len(unique_results),
        "results": [r.model_dump() for r in unique_results[:20]],
    })

    # ── Stage 3: Article Extraction ────────────────────────────────────
    articles = []
    extraction_log = []
    target_article_count = 3
    
    for result in unique_results:
        # Stop fetching once we have enough successful articles
        if len(articles) >= target_article_count:
            break
            
        article = await extract_article(result.link)
        if article:
            articles.append(article)
            extraction_log.append({
                "url": article.url,
                "text_length": article.text_length,
                "preview": article.text[:200] + "..." if len(article.text) > 200 else article.text,
            })
        else:
            # Log the failure for transparency
            extraction_log.append({
                "url": result.link,
                "error": "Failed to extract content (404, timeout, or anti-bot block)"
            })

    logger.log("article_extraction", {
        "articles_extracted": len(articles),
        "details": extraction_log,
    })

    # ── Stage 4: LLM Analysis ─────────────────────────────────────────
    analysis_results = []
    analysis_texts = []
    for article in articles:
        result = await analyze_article(article, request.company_name, request.sector, client)
        analysis_results.append(result)
        analysis_texts.append(result["response"])

    logger.log("llm_analysis", {
        "articles_analyzed": len(analysis_results),
        "details": analysis_results,
    })

    # ── Stage 5: Risk Signal Extraction ────────────────────────────────
    risk_signals: list[RiskSignal] = []
    if analysis_texts:
        risk_signals = await extract_risk_signals(analysis_texts, request.company_name, client)

    logger.log("risk_signal_extraction", {
        "signals_found": len(risk_signals),
        "signals": [s.model_dump() for s in risk_signals],
    })

    # ── Stage 6: Produce Structured Insights ───────────────────────────
    research_summary = ""
    company_news: list[str] = []
    promoter_risks: list[str] = []
    sector_trends: list[str] = []

    if analysis_texts:
        combined = "\n\n---\n\n".join(analysis_texts)
        summary_prompt = get_summary_prompt(combined, request.company_name, request.sector)

        try:
            summary_response = await client.chat.completions.create(
                model=MODEL,
                messages=[{"role": "user", "content": summary_prompt}],
                response_format={"type": "json_object"}
            )
            raw = summary_response.choices[0].message.content.strip()

            # Strip markdown fences if present
            if raw.startswith("```"):
                raw = raw.split("\n", 1)[1] if "\n" in raw else raw[3:]
            if raw.endswith("```"):
                raw = raw[:-3].strip()

            summary_data = json.loads(raw)
            research_summary = summary_data.get("research_summary", "")
            company_news = summary_data.get("company_news", [])
            promoter_risks = summary_data.get("promoter_risks", [])
            sector_trends = summary_data.get("sector_trends", [])
        except Exception as e:
            research_summary = f"Summary generation failed: {e}"
    else:
        research_summary = "No articles were extracted for analysis."

    return ResearchResponse(
        research_summary=research_summary,
        company_news=company_news,
        promoter_risks=promoter_risks,
        sector_trends=sector_trends,
        risk_signals=risk_signals,
        pipeline_logs=logger.get_logs(),
        financial_data=request.financial_data,
    )
