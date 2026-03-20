"""
generator.py — Generate SEO-optimized blog posts using Google Gemini.
"""

import warnings
warnings.simplefilter('ignore')

import google.generativeai as genai
from config import GEMINI_API_KEY, BLOG_LANGUAGE, INTERNAL_LINKS

# Configure Gemini with the API Key
genai.configure(api_key=GEMINI_API_KEY)


def generate_ctr_title(original_title: str) -> str:
    """
    Uses Google Gemini to generate a high CTR, click-baity (but accurate) title for the AKTU notice.
    """
    model = genai.GenerativeModel('gemini-2.5-flash')
    
    prompt = f"""
You are an expert copywriter for an Indian engineering student blog.
Rewrite the following AKTU official notice title into a highly engaging, high-CTR (Click-Through Rate) blog post title.
Make it urgent, exciting, and clear for students (e.g., use words like "Big Update", "Urgent", "Must Check", "Good News", "Alert").
Keep it under 70 characters. Do not use quotes around the title.

Original Notice Title: {original_title}

Return ONLY the new title text, nothing else.
"""
    try:
        response = model.generate_content(
            prompt,
            generation_config=genai.types.GenerationConfig(temperature=0.9)
        )
        new_title = response.text.strip().replace('"', '').replace("'", "")
        print(f"[INFO] Generated CTR Title: {new_title}")
        return new_title
    except Exception as e:
        print(f"[ERROR] CTR Title generation failed: {e}")
        return original_title


def generate_blog(title: str, link: str, pdf_text: str = "", image_url: str = "") -> str:
    """
    Uses Google Gemini to generate a 1000+ word SEO blog post for a given AKTU notice.

    Args:
        title: The notice/circular title.
        link:  The direct PDF/notice link.
        pdf_text: Output text extracted from the actual PDF.
        image_url: URL to the webp image of the PDF page to embed.

    Returns:
        The generated blog content as an HTML-ready string.
    """
    
    # Optional: we can specify the model ('gemini-2.5-pro' or 'gemini-2.5-flash' are good choices)
    # Using flash for faster & cheaper generation, or pro for better reasoning
    model = genai.GenerativeModel('gemini-2.5-flash')

    internal_links_text = "\n".join(
        [f"- {url}" for url in INTERNAL_LINKS]
    )

    image_instruction = ""
    if image_url:
        image_instruction = f"""
    - **CRITICAL**: You MUST embed the following image inside the blog post where it is most required (e.g., after the introduction or in the key highlights).
      Use this exact HTML code: <img src="{image_url}" alt="{title}" style="max-width:100%; height:auto;" />
"""

    prompt = f"""
You are an expert education blogger writing for Indian engineering students (AKTU University).

Write a 1000+ word complete SEO-optimized blog post in {BLOG_LANGUAGE} (mix of Hindi and English) that is highly engaging and designed to keep users reading (high CTR/retention).
Read the actual PDF text below carefully to make the blog post 100% accurate according to the inside PDF content.

Title: {title}

--- ACTUAL PDF CONTENT ENCLOSED BELOW ---
{pdf_text[:10000]} # taking first 10k chars to avoid token limits
--- END OF PDF CONTENT ---

Structure the post with proper HTML tags (use <h2>, <h3>, <p>, <ul>, <li>, <strong>, <a>). Do not include the ```html markdown wrapper around your answer. 

CRITICAL HEADING RULE: Do NOT use generic section names like "Introduction", "Key Highlights", "Important Dates", or "Who is Affected" as your actual H2/H3 headings. Instead, create UNIQUE, content-specific, and catchy headings for every single blog post (e.g., instead of "Important Dates", use "AKTU B.Tech Exam Form Last Date 2024").

Ensure the blog covers ALL of the following topics (using your unique headings):
1. **Introduction** — start with a high-CTR, click-worthy hook! Tell the students exactly why this notice is crucial today.
2. **Key Highlights (Urgent)** — bullet points of the main updates.
3. **Important Dates** — table or list (if dates are mentioned or likely)
4. **Who is Affected** — which students, branches, semesters
5. **How to Check / Download the Notice** — numbered step-by-step guide
6. **Official Link** — mention the direct link: <a href="{link}" target="_blank" rel="noopener">{link}</a>
7. **Internal Links** — embed these naturally within the content:
{internal_links_text}
8. **Student Advice / Pro Tips** — 3-5 practical tips
9. **FAQs** — 5 frequently asked questions with answers

SEO & CTR Requirements:
- Write an incredibly engaging, scroll-stopping first paragraph to reduce bounce rate.
- Create unique, content-specific H2 and H3 subheadings for every post.
- Include the main keyword (from the title) in the first paragraph.
- Use the keyword naturally 4–6 times throughout.
- Add LSI/related keywords.
- Write meta-friendly, human-like sentences with an exciting tone.
- Write good content depth with short paragraphs format, making it Ezoic ad-friendly and ensuring complete SEO optimization.
- STRICT RULE: Do NOT use any emojis anywhere in the text.
- STRICT RULE: Do NOT use any divider lines (e.g., <hr>, ---, or any horizontal rules).
{image_instruction}
Do NOT add a meta description tag — just return the full blog HTML body content.
"""

    try:
        response = model.generate_content(
            prompt,
            generation_config=genai.types.GenerationConfig(
                temperature=0.8,
                max_output_tokens=3000,
            )
        )
        content = response.text
        
        # Strip potential markdown formatting from the response
        if content.startswith("```html"):
            content = content[7:]
        if content.endswith("```"):
            content = content[:-3]
            
        print(f"[INFO] Blog generated via Gemini ({len(content)} characters).")
        return content.strip()

    except Exception as e:
        print(f"[ERROR] Gemini API call failed: {e}")
        return ""


if __name__ == "__main__":
    # Quick test
    sample_title = "AKTU Result 2024 — B.Tech Odd Semester Declared"
    sample_link  = "https://aktu.ac.in/pdf/sample-circular.pdf"
    blog = generate_blog(sample_title, sample_link)
    print(blog[:500], "...")
