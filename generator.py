"""
generator.py — Generate SEO-optimized blog posts using OpenRouter.
"""

import warnings
warnings.simplefilter('ignore')

from openai import OpenAI
from config import GROQ_API_KEY, BLOG_LANGUAGE, INTERNAL_LINKS

# Configure Groq Client (OpenAI compatible)
client = OpenAI(
    base_url="https://api.groq.com/openai/v1",
    api_key=GROQ_API_KEY,
)

# Use the top free model on Groq
MODEL_NAME = "llama-3.3-70b-versatile"

def generate_ctr_title(original_title: str) -> str:
    """
    Uses AI to generate a high CTR, click-baity (but accurate) title for the AKTU notice.
    """
    prompt = f"""
You are an expert copywriter for an Indian engineering student blog.
Rewrite the following AKTU official notice title into a highly engaging, high-CTR (Click-Through Rate) blog post title.
Make it urgent, exciting, and clear for students (e.g., use words like "Big Update", "Urgent", "Must Check", "Good News", "Alert").
Keep it strictly under 120 characters maximum. Do not use quotes around the title.

Original Notice Title: {original_title}

Return ONLY the new title text, nothing else.
"""
    try:
        response = client.chat.completions.create(
            model=MODEL_NAME,
            messages=[{"role": "user", "content": prompt}],
            temperature=0.9
        )
        new_title = response.choices[0].message.content.strip().replace('"', '').replace("'", "")
        print(f"[INFO] Generated CTR Title: {new_title}")
        return new_title
    except Exception as e:
        print(f"[ERROR] CTR Title generation failed: {e}")
        return original_title


def generate_blog(title: str, link: str, pdf_text: str = "", image_url: str = "") -> str:
    """
    Uses AI to generate a 1000+ word SEO blog post for a given AKTU notice.

    Args:
        title: The notice/circular title.
        link:  The direct PDF/notice link.
        pdf_text: Output text extracted from the actual PDF.
        image_url: URL to the webp image of the PDF page to embed.

    Returns:
        The generated blog content as an HTML-ready string.
    """
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

Write a HIGHLY DETAILED, 1000+ word complete SEO-optimized blog post in {BLOG_LANGUAGE} (mix of Hindi and English) that is highly engaging and designed to keep users reading (high CTR/retention).
Read the actual PDF text below carefully to make the blog post 100% accurate according to the inside PDF content. If the PDF text is short, expand on the context naturally and comprehensively to meet the strict 1000+ word requirement.

Title: {title}

--- ACTUAL PDF CONTENT ENCLOSED BELOW ---
{pdf_text[:10000]} # taking first 10k chars to avoid token limits
--- END OF PDF CONTENT ---

Structure the post with proper HTML tags (use <h2>, <h3>, <p>, <ul>, <li>, <strong>, <a>). Do not include the ```html markdown wrapper around your answer. 

CRITICAL HEADING RULE: Do NOT use generic section names like "Introduction", "Key Highlights", "Important Dates", or "Who is Affected" as your actual H2/H3 headings. Instead, create UNIQUE, content-specific, and catchy headings for every single blog post (e.g., instead of "Important Dates", use "AKTU B.Tech Exam Form Last Date 2024").

Ensure the blog covers ALL of the following topics (using your unique headings) in GREAT DETAIL:
1. **Introduction** — start with a high-CTR, click-worthy hook! Tell the students exactly why this notice is crucial today in 2-3 paragraphs.
2. **Key Highlights (Urgent)** — detailed bullet points of the main updates. Explain each point.
3. **Important Dates** — table or detailed list (if dates are mentioned or likely).
4. **Who is Affected** — deeply explain which students, branches, and semesters this applies to.
5. **How to Check / Download the Notice** — detailed numbered step-by-step guide.
6. **Official Link** — mention the direct link: <a href="{link}" target="_blank" rel="noopener">{link}</a>
7. **Internal Links** — embed these naturally within the content:
{internal_links_text}
8. **Student Advice / Pro Tips** — 3-5 highly practical, actionable tips for students.
9. **FAQs** — 5-7 frequently asked questions with highly detailed answers.

SEO, EZOIC & QUALITY REQUIREMENTS (STRICT):
- LENGTH REQUIREMENT: You MUST generate at least 1000 words. Expand heavily on context, implications, rules, and student advice to reach this length.
- HUMAN-WRITTEN TONE: Write in a highly conversational, natural, and relatable tone. Avoid robotic structures, AI clichés (like "delve into", "in conclusion"), and repetitive phrasing.
- EZOIC AD OPTIMIZATION: Write almost EXCLUSIVELY in short paragraphs (1-3 sentences maximum). Break up text constantly with bullet points, numbered lists, bold text, and H2/H3 headings. This creates "white space" for automatic Ezoic ad placeholders.
- Create unique, content-specific H2 and H3 subheadings for every post (aim for at least 7-10 subheadings).
- Include the main keyword (from the title) in the first paragraph. Use the keyword naturally 4–6 times throughout, along with LSI/related keywords.
- STRICT RULE: Do NOT use any emojis anywhere in the text.
- STRICT RULE: Do NOT use any divider lines (e.g., <hr>, ---, or any horizontal rules).
{image_instruction}
Do NOT add a meta description tag — just return the full blog HTML body content.
"""

    try:
        response = client.chat.completions.create(
            model=MODEL_NAME,
            messages=[{"role": "user", "content": prompt}],
            temperature=0.8,
            max_tokens=3000
        )
        content = response.choices[0].message.content.strip()
        
        # Strip potential markdown formatting from the response
        if content.startswith("```html"):
            content = content[7:]
        elif content.startswith("```"):
            content = content[3:]
            
        content = content.strip()
        if content.endswith("```"):
            content = content[:-3]
            
        print(f"[INFO] Blog generated via AI ({len(content)} characters).")
        return content.strip()

    except Exception as e:
        print(f"[ERROR] API call failed: {e}")
        return ""


if __name__ == "__main__":
    # Quick test
    sample_title = "AKTU Result 2024 — B.Tech Odd Semester Declared"
    sample_link  = "https://aktu.ac.in/pdf/sample-circular.pdf"
    blog = generate_blog(sample_title, sample_link)
    print(blog[:500], "...")
