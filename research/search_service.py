import requests
from common.config import settings
from research.schemas import SearchResult


def generate_queries(
        company_name: str, 
        sector: str, 
        promoters: list[str],
        anomalies: list = []
    ) -> list[str]:
    """Generate diverse search queries for comprehensive research coverage."""
    queries = [
        f"{company_name} India news",
        f"{company_name} fraud investigation",
        f"{company_name} litigation India",
        f"{company_name} regulatory action",
        f"{company_name} financial trouble",
        f"{sector} industry outlook India",
        f"{sector} sector risks India",
    ]

    for promoter in promoters:
        queries.append(f"{promoter} fraud OR investigation OR litigation")

    for anomaly in anomalies:
        if anomaly.get("severity") in ("medium", "high"):
            queries.append(f"{company_name} {anomaly.get('type', '')} {anomaly.get('period', '')}")

    return queries


def search_serper(query: str, num_results: int = 5) -> list[SearchResult]:
    """Call Serper API to retrieve search results for a single query."""
    url = "https://google.serper.dev/search"
    headers = {
        "X-API-KEY": settings.SERPER_API_KEY,
        "Content-Type": "application/json",
    }
    payload = {"q": query, "num": num_results}

    try:
        response = requests.post(url, json=payload, headers=headers, timeout=10)
        response.raise_for_status()
        data = response.json()
    except requests.RequestException as e:
        print(f"[search_service] Serper API error for query '{query}': {e}")
        return []

    results = []
    for item in data.get("organic", []):
        results.append(
            SearchResult(
                title=item.get("title", ""),
                link=item.get("link", ""),
                snippet=item.get("snippet", ""),
                source=item.get("source", item.get("link", "")),
            )
        )

    return results
