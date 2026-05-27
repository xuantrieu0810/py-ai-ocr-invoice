from app.core.extraction.extractor import InvoiceExtractor
from pathlib import Path


def test_extract_fields_from_sample():
    root = Path(__file__).resolve().parents[2]
    sample_path = root / "samples" / "invoices" / "sample_invoice.txt"
    ocr_text = sample_path.read_text()

    extractor = InvoiceExtractor()
    fields = extractor.extract_fields(ocr_text)

    assert fields["merchant"] in ("ACME Corporation", "" )
    assert fields["invoice_number"] == "INV-2026-001"
    assert fields["invoice_date"] == "2026-05-20"
    assert fields["subtotal"] == 100.0
    assert fields["tax"] == 10.0
    assert fields["total"] == 110.0
    assert fields["currency"] == "USD"
