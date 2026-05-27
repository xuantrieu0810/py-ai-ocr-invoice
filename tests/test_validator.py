from app.core.validation.validator import InvoiceValidator


def test_validator_valid_case():
    fields = {
        "merchant": "ACME Corporation",
        "invoice_number": "INV-2026-001",
        "invoice_date": "2026-05-20",
        "subtotal": 100.0,
        "tax": 10.0,
        "total": 110.0,
        "currency": "USD",
    }

    v = InvoiceValidator()
    res = v.validate(fields)
    assert res["status"] == "valid"
    assert res["warnings"] == []


def test_validator_mismatch_total():
    fields = {
        "merchant": "ACME",
        "invoice_number": "INV-2",
        "invoice_date": "2026-05-20",
        "subtotal": 90.0,
        "tax": 5.0,
        "total": 110.0,
        "currency": "USD",
    }

    v = InvoiceValidator()
    res = v.validate(fields)
    assert res["status"] == "invalid"
    assert any("does not match total" in w.lower() for w in res["warnings"]) 
