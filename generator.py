"""
generator.py — Generate SEO-optimized blog posts using Google Gemini.
"""

import warnings
warnings.simplefilter('ignore')

import google.generativeai as genai
from config import GEMINI_API_KEY, BLOG_LANGUAGE, INTERNAL_LINKS

# Configure Gemini with the API Key
genai.configure(api_key=GEMINI_API_KEY)


def generate_blog(title: str, link: str) -> str:
    """
    Uses Google Gemini to generate a 1000+ word SEO blog post for a given AKTU notice.

    Args:
        title: The notice/circular title.
        link:  The direct PDF/notice link.

    Returns:
        The generated blog content as an HTML-ready string.
    """
    
    # Optional: we can specify the model ('gemini-2.5-pro' or 'gemini-2.5-flash' are good choices)
    # Using flash for faster & cheaper generation, or pro for better reasoning
    model = genai.GenerativeModel('gemini-2.5-flash')

    internal_links_text = "\n".join(
        [f"- {url}" for url in INTERNAL_LINKS]
    )

    prompt = f"""
You are an expert education blogger writing for Indian engineering students (AKTU University).

Write a 1000+ word SEO-optimized blog post in {BLOG_LANGUAGE} (mix of Hindi and English).

Title: {title}

Structure the post with proper HTML tags (use <h2>, <h3>, <p>, <ul>, <li>, <strong>, <a>). Do not include the ```html markdown wrapper around your answer. 

Include ALL of the following sections:
1. **Introduction** — engaging hook, what this notice is about
2. **Key Highlights** — bullet points of the main points
3. **Important Dates** — table or list (if dates are mentioned or likely)
4. **Who is Affected** — which students, branches, semesters
5. **How to Check / Download the Notice** — numbered step-by-step guide
6. **Official Link** — mention the direct link: <a href="{link}" target="_blank" rel="noopener">{link}</a>
7. **Internal Links** — embed these naturally within the content:
{internal_links_text}
8. **Student Advice / Pro Tips** — 3-5 practical tips
9. **FAQs** — 5 frequently asked questions with answers

SEO Requirements:
- Include the main keyword (from the title) in the first paragraph
- Use the keyword naturally 4–6 times throughout
- Add LSI/related keywords
- Write meta-friendly, human-like sentences
- Make it engaging and Ezoic ad-friendly (good content depth)

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
