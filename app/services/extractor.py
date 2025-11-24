import re
from typing import Dict, List
import pytesseract
import pdfplumber
from PIL import Image

pytesseract.pytesseract.tesseract_cmd = r"C:\Program Files\Tesseract-OCR\tesseract.exe"

def ocr_from_image(image_path: str) -> str:
    """Učitaj sliku i vrati tekst koristeći pytesseract."""
    img = Image.open(image_path)
    text = pytesseract.image_to_string(img)
    return text

def ocr_from_pdf(pdf_path: str) -> str:
    """Učitaj PDF i vrati sve tekstove u jedan string."""
    text = ""
    with pdfplumber.open(pdf_path) as pdf:
        for page in pdf.pages:
            text += page.extract_text() + "\n"
    return text


def extract_invoice_fields(text: str) -> Dict:
    regex_map = {
        "invoice_number": [
            (r"(?i)invoice\s*[#:\s]*([\w\-]+)", 0.95),
            (r"(?i)inv(?:oice)?\s*([\w\-]+)", 0.75),
            (r"([\w]{3,}-\d{3,})", 0.45)
        ],
        "invoice_date": [
            r"Date[:\s]*([0-9]{4}[/\-\.][0-9]{2}[/\-\.][0-9]{2})",
            r"([0-9]{2}[/\-\.][0-9]{2}[/\-\.][0-9]{4})"
        ],
        "vendor_name": [
            r"^([A-Z][A-Za-z0-9 &,-]{2,})"
        ],
        "total_amount": [
            r"Total\s*[:\-]?\s*\$?\s*([0-9,]+\.?[0-9]{0,2})"
        ]
    }

    results = {}

    for field, patterns in regex_map.items():
        value = None
        confidence = 0.0

        #invoice_number ima regex + confidence logiku
        if field == "invoice_number":
            for pattern, conf in patterns:
                match = re.search(pattern, text, flags=re.MULTILINE)
                if match:
                    value = match.group(1).strip()
                    confidence = conf
                    break
        else:
            # ostala polja, confidence 1.0 ako postoji
            for pattern in patterns:
                match = re.search(pattern, text, flags=re.MULTILINE|re.IGNORECASE)
                if match:
                    value = match.group(1).strip()
                    confidence = 1.0
                    break

        results[field] = {"value": value, "confidence": confidence}

    # izdvajam linije koje sadrze cijenu
    lines = text.splitlines()
    line_items = []
    for line in lines:
        line = line.strip()
        if any(word in line.lower() for word in ["phone", "iban", "vat", "no", "de"]):
            continue

        price_matches = re.findall(r"\b\d{1,5}[.,]\d{2}\b", line)
        if price_matches:
            price = price_matches[-1].replace(",", ".")  # zadnji broj kao total_price
            desc = line[:line.rfind(price_matches[-1])].strip()  # sve prije zadnjeg broja
            line_items.append({
                "description": desc,
                "total_price": price
            })

    results["line_items"] = {
        "value": line_items,
        "confidence": 1.0 if line_items else 0.0
    }

    return results


def extract_invoice_from_file(file_path: str) -> Dict:
    # iz fajla u raw text
    if file_path.lower().endswith(".pdf"):
        text = ocr_from_pdf(file_path)
    elif file_path.lower().endswith((".png", ".jpg", ".jpeg", ".tiff")):
        text = ocr_from_image(file_path)
    else:
        raise ValueError("Unsupported file format")
    
    return extract_invoice_fields(text)