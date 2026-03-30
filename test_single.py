"""
test_single.py — Scrape the single latest notice and create a blog post locally to verify.
"""
import sys
from scraper import fetch_notices
from pdf_handler import process_pdf
from generator import generate_ctr_title, generate_blog

def test_single_scrape_and_generate():
    print("[INFO] Fetching latest notice from AKTU...")
    notices = fetch_notices()
    
    if not notices:
        print("[ERROR] No notices found.")
        return

    latest_notice = notices[0]
    title = latest_notice["title"]
    link = latest_notice["link"]
    
    print(f"\n[INFO] Notice found: {title}")
    print(f"[INFO] Link: {link}\n")
    
    print("[INFO] Downloading and Extracting PDF Text...")
    pdf_text, img_bytes = process_pdf(link)
    print(f"[SUCCESS] Extracted {len(pdf_text)} characters from PDF.")
    
    print("\n[INFO] Generating CTR Title using Groq AI...")
    ctr_title = generate_ctr_title(title)
    print(f"[SUCCESS] Optimized Title: {ctr_title}\n")
    
    print("[INFO] Generating 1000+ Word Blog Post using Groq AI...")
    blog_content = generate_blog(ctr_title, link, pdf_text, image_url="")
    
    if not blog_content:
        print("[ERROR] Blog generation failed!")
        return

    print(f"[SUCCESS] Blog Post Generated! ({len(blog_content)} characters)")
    
    filename = "latest_post_preview.html"
    with open(filename, "w", encoding="utf-8") as f:
        f.write(f"<!DOCTYPE html>\n<html>\n<head>\n<title>{ctr_title}</title>\n</head>\n<body>\n")
        f.write(f"<h1>{ctr_title}</h1>\n")
        f.write(blog_content)
        f.write("\n</body>\n</html>")
        
    print(f"[SUCCESS] The generated blog post has been saved locally as: {filename}")

if __name__ == "__main__":
    test_single_scrape_and_generate()
