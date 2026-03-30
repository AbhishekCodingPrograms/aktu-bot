import os
from dotenv import load_dotenv

load_dotenv()  # Load variables from .env file

# ============================================================
# AKTU AUTO BLOG — Configuration
# ============================================================

# 🔑 API Keys (Loaded from environment variables or set manually)
GEMINI_API_KEY = os.environ.get("GEMINI_API_KEY")
GROQ_API_KEY = os.environ.get("GROQ_API_KEY")
OPENROUTER_API_KEY = os.environ.get("OPENROUTER_API_KEY")
OPENAI_API_KEY = os.environ.get("OPENAI_API_KEY") # (Only needed if GENERATE_IMAGES is True)

# 🌐 WordPress Site Settings
WP_URL = os.environ.get("WP_URL")
WP_USERNAME = os.environ.get("WP_USERNAME")
WP_PASSWORD = os.environ.get("WP_PASSWORD")   # Use App Password from WP settings

# 📚 WordPress Category & Tag IDs (update to match your site)
WP_CATEGORY_IDS = []         # e.g., "AKTU" category ID, leave empty [] to skip
WP_TAG_IDS = []              # e.g., "AKTU", "Results" tag IDs, leave empty [] to skip

# 🔗 AKTU Source URL
AKTU_URL = "https://erp.aktu.ac.in/Webpages/Public/Circular/frmCircularForWebsite.aspx"

# 🖊️ Blog Settings
MAX_NOTICES = 15             # How many latest notices to process per run
BLOG_LANGUAGE = "English"    # Language style for AI-generated content
GENERATE_IMAGES = os.environ.get("GENERATE_IMAGES", "false").lower() == "true"  # Set to "true" to enable DALL-E images

# 🔗 Internal links to embed in posts (for SEO)
INTERNAL_LINKS = [
    "https://notesgallery.com/aktu-notes",
    "https://notesgallery.com/aktu-syllabus",
]
