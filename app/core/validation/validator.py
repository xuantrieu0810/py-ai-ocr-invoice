from datetime import datetime
from typing import Dict, List, Optional


class InvoiceValidator:
    def validate(self, fields: Dict[str, Optional[object]]) -> Dict[str, object]:
        warnings: List[str] = []

        subtotal = fields.get("subtotal")
        tax = fields.get("tax")
        total = fields.get("total")
        invoice_date = fields.get("invoice_date")

        if subtotal is None:
            warnings.append("Missing subtotal.")
        if tax is None:
            warnings.append("Missing tax amount.")
        if total is None:
            warnings.append("Missing total amount.")

        if subtotal is not None and tax is not None and total is not None:
            if abs((subtotal + tax) - total) > 0.99:
                warnings.append("Subtotal plus tax does not match total.")

        if total is not None and total <= 0:
            warnings.append("Total amount must be positive.")

        if invoice_date:
            try:
                parsed_date = datetime.strptime(invoice_date, "%Y-%m-%d")
                if parsed_date.date() > datetime.utcnow().date():
                    warnings.append("Invoice date is in the future.")
            except ValueError:
                warnings.append("Invoice date format could not be validated.")

        status = "valid" if not warnings else "invalid"
        return {"warnings": warnings, "status": status}
