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
from datetime import datetime

# Fix for printing emojis in Windows cmd/PowerShell
if hasattr(sys.stdout, 'reconfigure') and sys.stdout.encoding != 'utf-8':
    sys.stdout.reconfigure(encoding='utf-8')  # type: ignore

from scraper   import fetch_notices
from generator import generate_blog, generate_ctr_title
from publisher import publish_post
from image_generator import generate_and_upload_image, upload_image_bytes
from pdf_handler import process_pdf

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
            
        date_text = notice.get("date_text", "")
        if date_text:
            try:
                # AKTU format is usually '19-Mar-2026'
                notice_date = datetime.strptime(date_text, "%d-%b-%Y")
                if (datetime.now() - notice_date).days > 3:
                    print(f"[SKIP] Old notice ({date_text}): {title[:60]}...")
                    posted.append(title)
                    save_database(posted)
                    continue
            except ValueError:
                pass # Unparseable date format, proceed normally

        print(f"\n📄 Processing ({date_text}): {title[:70]}...")

        # 1. Process PDF (Extract text & page image)
        pdf_text, webp_bytes = process_pdf(link)

        # 2. Generate CTR title
        ctr_title = generate_ctr_title(title)

        # 3. Upload Extracted PDF Image (WEBP) to embed in the post body
        embedded_image_url = ""
        pdf_media_id = 0
        if webp_bytes:
            upload_result = upload_image_bytes(ctr_title, webp_bytes)
            if isinstance(upload_result, tuple) and len(upload_result) == 2:
                pdf_media_id, embedded_image_url = upload_result

        # 4. Generate & Upload Featured Image via Google Gemini AI
        media_id = 0
        gemini_img_result = generate_and_upload_image(ctr_title)
        if isinstance(gemini_img_result, tuple) and len(gemini_img_result) == 2:
            media_id, _ = gemini_img_result
        elif isinstance(gemini_img_result, int):
            media_id = gemini_img_result
            
        # 4b. Fallback to PDF preview as Featured Image if Gemini failed
        if not media_id and pdf_media_id:
            print("   [INFO] Using PDF preview as Featured Image since Gemini generation was unavailable.")
            media_id = pdf_media_id

        # 5. Generate blog content using PDF text and embedded image url
        blog_content = generate_blog(ctr_title, link, pdf_text, embedded_image_url)

        if not blog_content:
            print(f"[ERROR] Blog generation failed for: {title}. Skipping.")
            continue

        # Publish to WordPress
        result = publish_post(ctr_title, blog_content, media_id=media_id)

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
