from typing import Dict
from datetime import datetime
from dateutil.parser import parse as parse_date

def validate_invoice_data(results: Dict) -> Dict:
   
    schema = {
        "invoice_number": {"required": True, "type": str},
        "invoice_date": {"required": True, "type": str}, #parse later
        "vendor_name": {"required": True, "type": str},
        "total_amount": {"required": True, "type": float},
        "line_items": {"required": True, "type": list}
    }

    validated = {}

    for field, info in schema.items():
        field_data = results.get(field, {})
        value = field_data.get("value")
        confidence = field_data.get("confidence", 0.0)
        valid = True

        if field == "invoice_number":
            # vec imam value i confidence iz extractora
            valid = bool(value)

        elif field == "invoice_date":
            if value:
                try:
                    _ = parse_date(value, dayfirst=False, yearfirst=True)
                    valid = True
                except ValueError:
                    valid = False
            else:
                valid = False

        elif field == "total_amount":
            if value is not None:
                try:
                    float(value)
                    valid = True
                except ValueError:
                    valid = False
            else:
                valid = False

        elif field == "line_items":
            if not isinstance(value, list) or len(value) == 0:
                valid = False
            else:
                total_sum = 0.0
                for item in value:
                    desc = item.get("description")
                    price = item.get("total_price")
                    if not desc or price is None:
                        valid = False
                        break
                    try:
                        price_float = float(price.replace(",", ""))
                    except ValueError:
                        valid = False
                        break

                # provjera total_amount
                total_amount = results.get("total_amount", {}).get("value")
                try:
                    if total_amount is not None and abs(float(total_amount.replace(",", "")) - total_sum) > 0.01:
                        valid = False
                except Exception:
                    pass

        # required check
        if info["required"] and (value is None or value == ""):
            valid = False
            confidence = 0.0

        validated[field] = {
            "value": value,
            "confidence": confidence,
            "required": info["required"],
            "valid": valid
        }

    return validated