"""
image_generator.py — Generate and upload Featured Images via DALL-E 3 and WordPress REST API.
"""

import math
import requests
from google import genai
from config import GEMINI_API_KEY, WP_URL, WP_USERNAME, WP_PASSWORD, GENERATE_IMAGES

# We'll use the new google-genai package
gemini_client = genai.Client(api_key=GEMINI_API_KEY)


from typing import Tuple

def upload_image_bytes(title: str, img_data: bytes, file_ext: str = "webp", content_type: str = "image/webp") -> Tuple[int, str]:
    """
    Uploads raw image bytes to WordPress Media Library.
    Returns: (media_id, source_url)
    """
    media_url = WP_URL.replace("/posts", "/media")
    headers = {
        "Content-Disposition": f"attachment; filename=aktu-notice-{hash(title)}.{file_ext}",
        "Content-Type": content_type
    }

    try:
        print("   ☁️ Uploading featured image to WordPress Media Library...")
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
    Generates an image using Google Gemini (Imagen), and uploads it to WordPress.

    Args:
        title: The title of the AKTU Notice to generate an image for.

    Returns:
        Tuple of (media_id, source_url). (0, "") if failed or disabled.
    """
    if not GENERATE_IMAGES:
        return (0, "")

    print(f"\n🖼️ Generating Featured Image via Gemini for: '{title[:40]}...'")

    prompt = f"Design a modern, professional YouTube thumbnail style image for a university announcement titled: '{title}'. Keep it clean, minimal, using a mix of dark blue and yellow colors. Premium aesthetic, no messy text."

    try:
        response = gemini_client.models.generate_images(
            model='imagen-4.0-generate-001',
            prompt=prompt,
            config={
                "number_of_images": 1,
                "aspect_ratio": "16:9",
                "person_generation": "DONT_ALLOW"
            }
        )
        
        generated_image = response.generated_images[0]
        img_data = generated_image.image.image_bytes
        
        try:
            import io
            from PIL import Image, ImageOps
            
            with Image.open(io.BytesIO(img_data)) as img:
                # Resize and crop cleanly to exact 1200x628
                img_resized = ImageOps.fit(img, (1200, 628), Image.Resampling.LANCZOS)
                output_io = io.BytesIO()
                img_resized.save(output_io, format="WEBP", quality=90)
                img_data = output_io.getvalue()
        except Exception as resize_err:
            print(f"   [WARNING] Failed to resize image to 1200x628: {resize_err}")
            
        print(f"   [SUCCESS] Image generated via Gemini and scaled to 1200x628 ({len(img_data)} bytes).")
        
        # 2. Upload to WordPress Media Library using our helper function
        return upload_image_bytes(title, img_data, file_ext="webp", content_type="image/webp")
        
    except Exception as e:
        print(f"   [ERROR] Gemini Image generation failed: {e}")
        return (0, "")

if __name__ == "__main__":
    # Test
    test_title = "AKTU B.Tech Even Semester Results Declared"
    media_id, img_url = generate_and_upload_image(test_title)
    print(f"Returned Media ID: {media_id} | URL: {img_url}")
