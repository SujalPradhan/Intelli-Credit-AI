import requests
import trafilatura
from research.schemas import ExtractedArticle


def extract_article(url: str) -> ExtractedArticle | None:
    """Fetch a URL and extract clean article text using trafilatura."""
    try:
        response = requests.get(url, timeout=10, headers={
            "User-Agent": "Mozilla/5.0 (compatible; IntelliCredit/1.0)"
        })
        response.raise_for_status()
    except requests.RequestException as e:
        print(f"[scraper] Failed to fetch {url}: {e}")
        return None

    text = trafilatura.extract(response.text)

    if not text or len(text.strip()) < 50:
        print(f"[scraper] No meaningful content extracted from {url}")
        return None

    return ExtractedArticle(
        url=url,
        text=text.strip(),
        text_length=len(text.strip()),
    )
