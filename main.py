"""
main.py — AKTU Auto Blog: Orchestrator Script
=============================================
Flow:
  1. Fetch latest AKTU PDF notices
  2. Skip already-posted ones (via database.json)
  3. Generate a 1000+ word SEO blog with AI
  4. Publish to WordPress
  5. Save to database to avoid re-posting
"""

import json
import sys
from pathlib import Path

# Fix for printing emojis in Windows cmd/PowerShell
if sys.stdout.encoding != 'utf-8':
    sys.stdout.reconfigure(encoding='utf-8')

from scraper   import fetch_notices
from generator import generate_blog
from publisher import publish_post
from image_generator import generate_and_upload_image

DATABASE_FILE = Path(__file__).parent / "database.json"


def load_database() -> list:
    """Load the list of already-posted notice titles."""
    try:
        with open(DATABASE_FILE, "r", encoding="utf-8") as f:
            return json.load(f)
    except (FileNotFoundError, json.JSONDecodeError):
        return []


def save_database(posted: list) -> None:
    """Save the updated list of posted notice titles."""
    with open(DATABASE_FILE, "w", encoding="utf-8") as f:
        json.dump(posted, f, indent=2, ensure_ascii=False)


def main():
    print("=" * 60)
    print("🤖 AKTU Auto Blog — Starting Run")
    print("=" * 60)

    # Step 1 — Load what we've already posted
    posted = load_database()
    print(f"[INFO] {len(posted)} notices already in database.")

    # Step 2 — Fetch latest notices from AKTU
    notices = fetch_notices()

    if not notices:
        print("[WARNING] No notices fetched. Exiting.")
        sys.exit(0)

    # Step 3 — Process each new notice
    new_posts_count = 0

    for notice in notices:
        title = notice["title"]
        link  = notice["link"]

        if title in posted:
            print(f"[SKIP] Already posted: {title[:60]}...")
            continue

        print(f"\n📄 Processing: {title[:70]}...")

        # Generate blog content
        blog_content = generate_blog(title, link)

        if not blog_content:
            print(f"[ERROR] Blog generation failed for: {title}. Skipping.")
            continue
            
        # Optional: Generate Featured Image
        media_id = generate_and_upload_image(title)

        # Publish to WordPress
        result = publish_post(title, blog_content, media_id=media_id)

        if result:
            posted.append(title)
            save_database(posted)   # Save after each post to avoid data loss on crash
            new_posts_count += 1
        else:
            print(f"[ERROR] Publishing failed for: {title}.")

    # Summary
    print("\n" + "=" * 60)
    print(f"✅ Done! {new_posts_count} new post(s) published.")
    print("=" * 60)


if __name__ == "__main__":
    main()
