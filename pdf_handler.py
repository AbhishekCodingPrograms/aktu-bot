"""
pdf_handler.py — Downloads and processes AKTU Notice PDFs.
"""

import requests
import urllib3
import fitz  # PyMuPDF

# Suppress insecure request warnings for AKTU's self-signed certs
urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)

def process_pdf(pdf_url: str):
    """
    Downloads PDF from AKTU, extracts text, and converts the first page to WEBP.
    
    Returns:
        tuple: (extracted_text: str, webp_image_bytes: bytes | None)
    """
    print(f"   [INFO] Downloading and parsing PDF: {pdf_url}")
    try:
        headers = {
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64)"
        }
        response = requests.get(pdf_url, headers=headers, timeout=30, verify=False)
        response.raise_for_status()
        pdf_bytes = response.content
        
        doc = fitz.open(stream=pdf_bytes, filetype="pdf")
        text = ""
        for page in doc:
            text += page.get_text() + "\n"
            
        # Convert first page to WEBP image correctly using PyMuPDF Pillow/Pil or fitz
        try:
            page = doc[0]
            pix = page.get_pixmap(dpi=150)
            
            # Use Pillow to convert to webp (PyMuPDF sometimes lacks webp support natively)
            from PIL import Image
            import io
            
            mode = "RGBA" if pix.alpha else "RGB"
            img = Image.frombytes(mode, [pix.width, pix.height], pix.samples)
            
            img_byte_arr = io.BytesIO()
            img.save(img_byte_arr, format='WEBP', quality=85)
            webp_bytes = img_byte_arr.getvalue()
        except Exception as img_err:
            print(f"   [ERROR] Failed to convert PDF page to image: {img_err}")
            webp_bytes = None
            
        doc.close()
        return text.strip(), webp_bytes
        
    except Exception as e:
        print(f"   [ERROR] Failed to process PDF {pdf_url}: {e}")
        return "", None
