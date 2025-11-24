import sys
import os
import json
from pprint import pprint

sys.path.append(os.path.abspath("app/services"))
from app.services.extractor import extract_invoice_from_file
from app.services.validator import validate_invoice_data

file_path = r"C:\Users\Korisnik\py\invoice-validation\sample-invoice.pdf"

extracted_data = extract_invoice_from_file(file_path)
print("=== Extracted Data ===")
pprint(extracted_data)

validated_data = validate_invoice_data(extracted_data)
print("\n=== Validated Data ===")
pprint(validated_data)