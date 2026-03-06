import requests
import trafilatura
from research.schemas import ExtractedArticle


def extract_article(url: str) -> ExtractedArticle | None:
    """Fetch a URL and extract clean article text using trafilatura."""
    try:
        response = requests.get(url, timeout=15, headers={
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36",
            "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8",
            "Accept-Language": "en-US,en;q=0.5",
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
