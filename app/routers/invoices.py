from fastapi import APIRouter, UploadFile, File
from app.services.processor import process_invoice_upload, flatten_validated_result
from app.schemas import InvoiceResponse, CleanInvoiceResult, RawInvoiceResult

router = APIRouter()


@router.post("/extract-invoice", response_model=InvoiceResponse)
async def extract_invoice(file: UploadFile = File(...)):
    try:
        raw_result = await process_invoice_upload(file)
        clean_dict = flatten_validated_result(raw_result)
        
        return InvoiceResponse(
            clean=CleanInvoiceResult(**clean_dict),
            raw=RawInvoiceResult(**raw_result)
        )
    except Exception as e:
        print(f"Error: {e}")
        raise