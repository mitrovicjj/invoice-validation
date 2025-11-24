# Invoice extraction and validation pipeline

## Project description

This project focuses on automated extraction and validation of data from invoices, supporting both PDF and scanned image formats. The pipeline includes:

- OCR-based extraction (`pdfplumber` for PDFs, `pytesseract` for images)  
- Validation of key invoice fields  
- Structured output via Pydantic models, ready for API responses/further processing  

Main workflow (current state):  

Input(PDF); Extraction; Validation; Flatten; FastAPI Response (Clean + Raw JSON)


---

## Problem statement

Invoices come in various formats, so direct parsing can be challenging. Most common difficulties include:

- Imprecise OCR: Text from scanned invoices may be misrecognized - requiring retry logic or LLM prompts for correction.
- Format variations: Dates and amounts may come in multiple formats.  
- Incomplete or incorrect data: Some fields may be missing/misinterpreted.  
- Different invoice layouts: Invoices from different vendors may have fields in different positions or with different labels.

---

## Current solutions

1. **Extraction (OCR + Regex)**  
   - Text extraction from PDFs and images.  
   - Multi-strategy regex for key fields with confidence scores.  

2. **Validation**  
   - Checks field presence, types, line item consistency, and total amount sums.  
   - Produces validated dictionaries with confidence and validity metadata.  

3. **Flattening / Pydantic models**  
   - Converts nested raw extraction results into a flat structure (`CleanInvoiceResult`) for easy API consumption.  
   - `InvoiceResponse` combines `clean` + `raw` for structured FastAPI responses.  

4. **API integration (FastAPI)**  
   - Upload invoices via `/api/extract-invoice`.  
   - Returns structured JSON:  
     - `clean`: ready for UI / downstream processing  
     - `raw`: full extraction details for debugging  

5. **Future / next steps**  
   - Implement retry/LLM correction for low-confidence fields.  
   - Extend line item parsing to support quantity/unit_price.  
   - Add more example invoices and automated tests.  
   - Prepare pipeline for production-ready deployment with robust error handling.  

---
