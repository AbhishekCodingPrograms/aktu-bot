"""
publisher.py — Publish blog posts to WordPress via REST API.
"""

import requests
from config import WP_URL, WP_USERNAME, WP_PASSWORD, WP_CATEGORY_IDS, WP_TAG_IDS


def publish_post(title: str, content: str, media_id: int = 0) -> dict:
    """
    Publishes a post to WordPress using the REST API.

    Args:
        title:   The blog post title.
        content: The HTML blog content body.
        media_id: Document ID for the featured media image (optional).

    Returns:
        The JSON response from WordPress (contains post ID, URL, etc.)
    """

    post_data = {
        "title":      title,
        "content":    content,
        "status":     "publish",          # Change to "draft" to review before publishing
        "categories": WP_CATEGORY_IDS,
        "tags":       WP_TAG_IDS,
        "format":     "standard",
    }
    
    # Attach featured image if generated successfully
    if media_id > 0:
        post_data["featured_media"] = media_id

    try:
        response = requests.post(
            WP_URL,
            json=post_data,
            auth=(WP_USERNAME, WP_PASSWORD),
            timeout=30,
        )
        response.raise_for_status()
        result = response.json()

        post_id  = result.get("id", "?")
        post_url = result.get("link", "?")
        print(f"[SUCCESS] Published! ID: {post_id} | URL: {post_url}")
        return result

    except requests.exceptions.HTTPError as e:
        print(f"[ERROR] HTTP error while publishing: {e}")
        print(f"        Response: {response.text[:300]}")
        return {}
    except requests.RequestException as e:
        print(f"[ERROR] Network error: {e}")
        return {}


if __name__ == "__main__":
    # Quick connection test
    result = publish_post(
        "Test Post — AKTU Auto Blog",
        "<p>This is a test post from the automation script.</p>"
    )
    print(result)
