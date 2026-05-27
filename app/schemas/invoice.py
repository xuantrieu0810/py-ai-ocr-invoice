from pydantic import BaseModel, Field
from typing import List, Optional


class InvoiceResponse(BaseModel):
    merchant: str = Field(..., description="Merchant or vendor name")
    invoice_number: str = Field(..., description="Invoice identifier")
    invoice_date: str = Field(..., description="Invoice date in YYYY-MM-DD format")
    subtotal: Optional[float] = Field(None, description="Subtotal amount")
    tax: Optional[float] = Field(None, description="Tax amount")
    total: Optional[float] = Field(None, description="Total amount")
    currency: str = Field("USD", description="Currency code")
    warnings: List[str] = Field(default_factory=list, description="Validation warnings")
    status: str = Field(..., description="Invoice validation status")
