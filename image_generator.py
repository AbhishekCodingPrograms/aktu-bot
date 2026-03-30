"""
image_generator.py — Generate and upload Featured Images via Free AI and WordPress REST API.
"""

import math
import urllib.parse
import requests
from config import WP_URL, WP_USERNAME, WP_PASSWORD, GENERATE_IMAGES
from typing import Tuple

def upload_image_bytes(title: str, img_data: bytes, file_ext: str = "jpg", content_type: str = "image/jpeg") -> Tuple[int, str]:
    """
    Uploads raw image bytes to WordPress Media Library.
    Returns: (media_id, source_url)
    """
    if not WP_URL:
        print("   [ERROR] WP_URL is not configured. Cannot upload image.")
        return (0, "")
        
    media_url = WP_URL.replace("/posts", "/media")
    headers = {
        "Content-Disposition": f"attachment; filename=aktu-notice-{hash(title)}.{file_ext}",
        "Content-Type": content_type
    }

    try:
        print("   [INFO] Uploading featured image to WordPress Media Library...")
        wp_res = requests.post(
            media_url,
            headers=headers,
            data=img_data, # the raw bytes
            auth=(WP_USERNAME, WP_PASSWORD),
            timeout=40,
            verify=False
        )
        wp_res.raise_for_status()
        media_id = wp_res.json().get("id", 0)
        source_url = wp_res.json().get("source_url", "")
        
        if media_id:
            print(f"   [SUCCESS] Image uploaded! Media ID: {media_id}")
            return (media_id, source_url)
        else:
            print("   [ERROR] No media ID returned from WordPress.")
            return (0, "")
    except requests.exceptions.HTTPError as e:
        print(f"   [ERROR] WordPress Media Upload failed: {e}")
        print(f"           Response: {wp_res.text[:200]}")
        return (0, "")
    except Exception as e:
        print(f"   [ERROR] Unexpected error uploading image: {e}")
        return (0, "")


def generate_and_upload_image(title: str) -> Tuple[int, str]:
    """
    Generates an image using a free AI API (Pollinations) at 1200x628, and uploads it to WordPress.

    Args:
        title: The title of the AKTU Notice to generate an image for.

    Returns:
        Tuple of (media_id, source_url). (0, "") if failed or disabled.
    """
    if not GENERATE_IMAGES:
        return (0, "")

    # Simplifying prompt to avoid API errors
    safe_title = ''.join(e for e in title if e.isalnum() or e.isspace())
    prompt = f"abstract modern university announcement thumbnail blue yellow {safe_title}"
    encoded_prompt = urllib.parse.quote(prompt)
    
    # Using Pollinations API for free image generation (default size to avoid 500 errors)
    image_url = f"https://image.pollinations.ai/prompt/{encoded_prompt}"

    try:
        response = requests.get(image_url, timeout=10)
        response.raise_for_status()
        img_data = response.content
    except requests.exceptions.RequestException as e:
        # If Pollinations API fails (e.g. timeout or 500), fallback to a high-quality free placeholder
        print(f"   [WARNING] Free AI tool failed ({e}). Using fallback high-quality placeholder.")
        try:
            fallback_seed = safe_title.replace(" ", "") if safe_title else "aktu"
            image_url = f"https://picsum.photos/seed/{fallback_seed}/1200/628"
            response = requests.get(image_url, timeout=15)
            response.raise_for_status()
            img_data = response.content
        except requests.exceptions.RequestException as fallback_e:
            print(f"   [ERROR] Fallback image retrieval failed: {fallback_e}")
            return (0, "")
        
    # Resize/crop locally using Pillow
    try:
        import io
        from PIL import Image, ImageOps
        
        with Image.open(io.BytesIO(img_data)) as img:
            # Resize and crop cleanly to exact 1200x628
            img_resized = ImageOps.fit(img, (1200, 628), Image.Resampling.LANCZOS)
            output_io = io.BytesIO()
            # Save as JPEG
            img_resized.convert("RGB").save(output_io, format="JPEG", quality=90)
            img_data = output_io.getvalue()
            
        print(f"   [SUCCESS] Image retrieved and scaled to exactly 1200x628 ({len(img_data)} bytes).")
        
    except Exception as resize_err:
        print(f"   [WARNING] Failed to resize image locally: {resize_err}")
        print(f"   [SUCCESS] Image generated via Free AI but kept original size.")
    
    # Upload to WordPress Media Library using our helper function
    return upload_image_bytes(title, img_data, file_ext="jpg", content_type="image/jpeg")

if __name__ == "__main__":
    # Test
    # Enable image generation just for the test
    GENERATE_IMAGES = True
    test_title = "AKTU B.Tech Even Semester Results Declared"
    media_id, img_url = generate_and_upload_image(test_title)
    print(f"Returned Media ID: {media_id} | URL: {img_url}")
