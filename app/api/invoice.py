from fastapi import APIRouter, UploadFile, File, HTTPException
from fastapi.responses import JSONResponse
from app.core.ocr.ocr_service import OCRService
from app.core.extraction.extractor import InvoiceExtractor
from app.core.validation.validator import InvoiceValidator
from app.schemas.invoice import InvoiceResponse

router = APIRouter(prefix="/invoice", tags=["invoice"])


@router.post("/analyze", response_model=InvoiceResponse)
async def analyze_invoice(file: UploadFile = File(...)):
    if file.content_type not in {"image/png", "image/jpeg", "image/jpg", "image/tiff", "application/pdf"}:
        raise HTTPException(status_code=400, detail="Unsupported file type. Upload PNG, JPG, TIFF, or PDF.")

    body = await file.read()
    ocr_result = OCRService().extract_text(body)
    invoice_fields = InvoiceExtractor().extract_fields(ocr_result["full_text"])
    validation = InvoiceValidator().validate(invoice_fields)

    response = {
        **invoice_fields,
        "warnings": validation["warnings"],
        "status": validation["status"],
    }

    return JSONResponse(content=response)
