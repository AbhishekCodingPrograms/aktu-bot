"""
image_generator.py — Generate and upload Featured Images via DALL-E 3 and WordPress REST API.
"""

import math
import requests
from openai import OpenAI
from config import OPENAI_API_KEY, WP_URL, WP_USERNAME, WP_PASSWORD, GENERATE_IMAGES

client = OpenAI(api_key=OPENAI_API_KEY)


def generate_and_upload_image(title: str) -> int:
    """
    Generates an image using DALL-E 3, downloads it, and uploads it to WordPress.

    Args:
        title: The title of the AKTU Notice to generate an image for.

    Returns:
        The WordPress media ID (int), or 0 if failed or disabled.
    """
    if not GENERATE_IMAGES:
        return 0

    print(f"\n🖼️ Generating Featured Image for: '{title[:40]}...'")

    # 1. Generate Image with DALL-E 3
    prompt = f"Design a modern, professional YouTube thumbnail style image for a university announcement titled: '{title}'. Keep it clean, minimal, using a mix of dark blue and yellow colors. Premium aesthetic, no messy text."

    try:
        response = client.images.generate(
            model="dall-e-3",
            prompt=prompt,
            size="1024x1024",
            quality="standard",
            n=1,
        )
        image_url = response.data[0].url
        print(f"   [SUCCESS] Image generated via DALL-E: {image_url[:60]}...")
    except Exception as e:
        print(f"   [ERROR] DALL-E API call failed: {e}")
        return 0

    # 2. Download Image Temporarily
    try:
        img_response = requests.get(image_url, timeout=20)
        img_response.raise_for_status()
        img_data = img_response.content
    except requests.RequestException as e:
        print(f"   [ERROR] Failed to download generated image: {e}")
        return 0

    # 3. Upload to WordPress Media Library
    media_url = WP_URL.replace("/posts", "/media")
    headers = {
        "Content-Disposition": f"attachment; filename=aktu-notice-{hash(title)}.png",
        "Content-Type": "image/png"
    }

    try:
        print("   ☁️ Uploading image to WordPress Media Library...")
        wp_res = requests.post(
            media_url,
            headers=headers,
            data=img_data,
            auth=(WP_USERNAME, WP_PASSWORD),
            timeout=40
        )
        wp_res.raise_for_status()
        media_id = wp_res.json().get("id", 0)
        
        if media_id:
            print(f"   [SUCCESS] Image uploaded! Media ID: {media_id}")
            return media_id
        else:
            print("   [ERROR] No media ID returned from WordPress.")
            return 0
    except requests.exceptions.HTTPError as e:
        print(f"   [ERROR] WordPress Media Upload failed: {e}")
        print(f"           Response: {wp_res.text[:200]}")
        return 0
    except Exception as e:
        print(f"   [ERROR] Unexpected error uploading image: {e}")
        return 0


if __name__ == "__main__":
    # Test
    test_title = "AKTU B.Tech Even Semester Results Declared"
    media_id = generate_and_upload_image(test_title)
    print(f"Returned Media ID: {media_id}")
