import os
from dotenv import load_dotenv
from google import genai

load_dotenv()
client = genai.Client()

def test_image():
    try:
        result = client.models.generate_images(
            model='imagen-4.0-generate-001',
            prompt='A futuristic glowing blue tree, neon cyberpunk style, 8k resolution',
            config=dict(
                number_of_images=1,
                aspect_ratio="16:9",
                person_generation="DONT_ALLOW"
            )
        )
        for g in result.generated_images:
            if g.image:
                print("Image generated! size:", len(g.image.image_bytes))
                return
        print("Failed to get image bytes")
    except Exception as e:
        print("Error:", e)

test_image()
