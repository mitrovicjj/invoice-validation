from fastapi import APIRouter, UploadFile, File
from app.services.processor import process_invoice_upload, flatten_validated_result
from app.schemas import InvoiceResponse, CleanInvoiceResult, RawInvoiceResult

router = APIRouter()


@router.post("/extract-invoice", response_model=InvoiceResponse)
async def extract_invoice(file: UploadFile = File(...)):

    # 1. Run processor (extract + validate)
    raw_result = await process_invoice_upload(file)

    # 2. Flatten into clean structure
    clean_dict = flatten_validated_result(raw_result)

    # 3. Pydantic response
    return InvoiceResponse(
        clean=CleanInvoiceResult(**clean_dict),
        raw=RawInvoiceResult(**raw_result)
    )