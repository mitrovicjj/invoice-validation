# Invoice Extraction and Validation Pipeline

## Project Description

Focus of the project is on automated extraction and validation of data from invoices. The goal is to create a controlled pipeline that can process PDF invoices (text-based and scanned), validate key fields and prepare structured outputs (JSON / Excel) for further processing.

Main workflow:  Input(PDF) - Extraction - Validation - Retry (if errors) - Formatting / Export

---

## Problem Statement

Invoices come in various formats, so direct parsing can be challenging. Most common difficulties include:

- **Imprecise OCR**: Text from scanned invoices may be misrecognized - requiring retry logic or LLM prompts for correction.
- **Format variations**: Dates and amounts may come in multiple formats.  
- **Incomplete or incorrect data**: Some fields may be missing/misinterpreted.  
- **Different invoice layouts**: Invoices from different vendors may have fields in different positions or with different labels.

---

## Potential Solutions

1. **Extraction (OCR + Mock Data)**  
   - Extract text from PDFs using libraries such as `pdfplumber` and `pytesseract`.  
   - In the R&D phase, mock data is used to isolate validation and retry logic.

2. **Validation**  
   - Check for the presence of all required fields, verify data types, handle edge cases (incorrect formats or missing values).

3. **Retry / Prompt Generation**  
   - Simulate LLM prompts to correct misparsed or missing fields.  
   - Enable development of AI evaluation loops.

4. **Data Normalization & Export**  
   - Normalize dates, currencies and decimal formats.  
   - Save data in structured formats (JSON / Excel / DataFrame) for further analytics or integration.
