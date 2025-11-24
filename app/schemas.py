from pydantic import BaseModel
from typing import Optional, List, Any


class FieldResult(BaseModel):
    parsed: Optional[str] = None
    value: Optional[str] = None
    confidence: Optional[float] = None
    valid: Optional[bool] = None


class LineItem(BaseModel):
    description: str
    price: float


class RawInvoiceResult(BaseModel):
    invoice_number: FieldResult
    invoice_date: FieldResult
    vendor_name: FieldResult
    total_amount: FieldResult
    line_items: Optional[List[Any]] = []
    overall_confidence: Optional[float] = None
    overall_valid: Optional[bool] = None


class CleanInvoiceResult(BaseModel):
    invoice_number: Optional[str] = None
    invoice_date: Optional[str] = None
    vendor_name: Optional[str] = None
    total_amount: Optional[str] = None
    line_items: List[Any] = []
    is_consistent: Optional[bool] = None
    missing_fields: List[str] = []
    overall_confidence: Optional[float] = None
    overall_valid: Optional[bool] = None


class InvoiceResponse(BaseModel):
    clean: CleanInvoiceResult
    raw: RawInvoiceResult