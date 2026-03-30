"""
scraper.py — Scrape latest notices/circulars from AKTU website.
"""

import urllib3
import requests
from bs4 import BeautifulSoup
from config import AKTU_URL, MAX_NOTICES

# Suppress insecure request warnings for AKTU's self-signed certs
urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)

def fetch_notices() -> list[dict]:
    """
    Fetches the latest notices from the AKTU circulars page.

    Returns:
        List of dicts with 'title' and 'link' keys.
    """
    headers = {
        "User-Agent": (
            "Mozilla/5.0 (Windows NT 10.0; Win64; x64) "
            "AppleWebKit/537.36 (KHTML, like Gecko) "
            "Chrome/122.0.0.0 Safari/537.36"
        )
    }

    from network_router import robust_get
    
    import time
    uncached_url = f"{AKTU_URL}?_={int(time.time())}"
    
    try:
        response = robust_get(uncached_url, headers=headers)
    except Exception as e:
        print(f"[ERROR] Failed to fetch AKTU page: {e}")
        return []

    soup = BeautifulSoup(response.text, "html.parser")

    notices = []

    for link in soup.select("a"):
        href = link.get("href", "")

        # Only pick links that look like PDF notices
        if href and "pdf" in href.lower():
            # Get the parent row (tr)
            row = link.find_parent("tr")
            if not row:
                continue
                
            # Extract text from columns, avoiding the 'Download' or 'देखे' text
            columns = row.find_all("td")
            date_text = ""
            if len(columns) >= 3:
                # Typically, col 0 is SNo, col 1 is Dept, col 2 is Title, col 3 is Date
                title = columns[2].text.strip()
                if len(columns) >= 4:
                    date_text = columns[3].text.strip()
            else:
                title = row.get_text(separator=' ', strip=True)

            # Skip empty titles or titles that just say 'view'
            if not title or title == "देखें":
                continue

            full_url = (
                href if href.startswith("http")
                else f"https://aktu.ac.in/{href.lstrip('/')}"
            )
            notices.append({
                "title": title,
                "link": full_url,
                "date_text": date_text
            })

    if not notices:
        print("[WARNING] No PDF notices found. The page structure may have changed.")

    print(f"[INFO] Found {len(notices)} notices. Taking top {MAX_NOTICES}.")
    return notices[:MAX_NOTICES]


if __name__ == "__main__":
    results = fetch_notices()
    for n in results:
        print(f"→ {n['title']}\n  {n['link']}\n")
