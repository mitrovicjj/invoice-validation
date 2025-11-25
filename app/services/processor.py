import tempfile
from app.services.extractor import extract_invoice_from_file
from app.services.validator import validate_invoice_data

async def process_invoice_upload(upload_file):
    # citanje bajtova iz streama
    file_bytes = await upload_file.read()

    # cuvam tmp file
    suffix = ".pdf" if upload_file.filename.endswith(".pdf") else ".png"
    with tempfile.NamedTemporaryFile(delete=False, suffix=suffix) as tmp:
        tmp.write(file_bytes)
        temp_path = tmp.name

    extracted = extract_invoice_from_file(temp_path)
    validated = validate_invoice_data(extracted)

    # helper da izvuce value iz dict strukture
    def get_value(field, default=""):
        if isinstance(field, dict):
            val = field.get("value", default)
            # ao je val None, vrati prazan string
            return val if val is not None else default
        return default
    
    def get_float_value(field, default=0.0):
        if isinstance(field, dict):
            val = field.get("value", default)
            try:
                return float(val) if val is not None else default
            except (ValueError, TypeError):
                return default
        return default

    line_items_raw = validated.get("line_items", [])
    if isinstance(line_items_raw, dict):
        line_items = line_items_raw.get("value", [])
    else:
        line_items = line_items_raw if isinstance(line_items_raw, list) else []

    return {
        "invoice_number": get_value(validated.get("invoice_number"), ""),
        "invoice_date": get_value(validated.get("invoice_date"), ""),
        "vendor_name": get_value(validated.get("vendor_name"), ""),
        "total_amount": get_float_value(validated.get("total_amount"), 0.0),
        "line_items": line_items,
        "overall_confidence": validated.get("overall_confidence", 0.0),
        "overall_valid": validated.get("overall_valid", False),
    }


def _safe_field(field):
    """
    Omogućava rad i kad je field dict, BaseModel, None, ili ima drugačije ključeve.
    Vraća first-available u ovom prioritetu: parsed → value → None
    """
    if field is None:
        return None

    if isinstance(field, dict):
        return field.get("parsed") or field.get("value")

    if hasattr(field, "parsed") or hasattr(field, "value"):
        return getattr(field, "parsed", None) or getattr(field, "value", None)

    return None


def _safe_line_items(raw_items):
    """
    Raw line_items može biti:
    - lista line itema
    - dict sa "value"
    - None
    - nešto treće
    Ovo vraća uvek LISTU.
    """
    if raw_items is None:
        return []

    if isinstance(raw_items, list):
        return raw_items

    if isinstance(raw_items, dict):
        value = raw_items.get("value")
        return value if isinstance(value, list) else []

    return []


def flatten_validated_result(raw):
    """
    Transformiše raw output u clean strukturu, bez bacanja errora.
    """
    clean = {}

    clean["invoice_number"] = _safe_field(raw.get("invoice_number"))
    clean["invoice_date"] = _safe_field(raw.get("invoice_date"))
    clean["vendor_name"] = _safe_field(raw.get("vendor_name"))
    clean["total_amount"]  = _safe_field(raw.get("total_amount"))

    clean["line_items"] = _safe_line_items(raw.get("line_items"))

    clean["is_consistent"] = raw.get("overall_valid")
    clean["overall_confidence"] = raw.get("overall_confidence")
    clean["overall_valid"] = raw.get("overall_valid")

    # Missing fields detection
    missing = []
    for key in ["invoice_number", "invoice_date", "vendor_name", "total_amount"]:
        if clean.get(key) in [None, ""]:
            missing.append(key)

    clean["missing_fields"] = missing

    return clean