import re
from datetime import datetime
from typing import Dict, Optional


class InvoiceExtractor:
    AMOUNT_PATTERN = re.compile(r"(?P<label>subtotal|tax|total|amount|invoice total|grand total)[^0-9\n]*?(?P<value>[\d,.]+)")
    DATE_PATTERN = re.compile(r"(?P<date>\d{4}[-/.]\d{1,2}[-/.]\d{1,2}|\d{1,2}[-/.]\d{1,2}[-/.]\d{2,4})")
    INVOICE_NUMBER_PATTERN = re.compile(r"(?:invoice\s*(?:number|no|#)|inv(?:ice)?\s*#?)\s*[:\-\s]*([A-Za-z0-9\-\_]+)", re.IGNORECASE)
    CURRENCY_PATTERN = re.compile(r"\b(USD|EUR|GBP|JPY|AUD|CAD|CHF|CNY|HKD)\b", re.IGNORECASE)

    def extract_fields(self, ocr_text: str) -> Dict[str, Optional[object]]:
        lines = [line.strip() for line in ocr_text.splitlines() if line.strip()]
        flat_text = " ".join(lines)

        merchant = self._extract_merchant(lines)
        invoice_number = self._extract_invoice_number(flat_text)
        invoice_date = self._extract_date(flat_text)
        currency = self._extract_currency(flat_text) or "USD"

        amounts = self._extract_amounts(flat_text)
        subtotal = amounts.get("subtotal")
        tax = amounts.get("tax")
        total = amounts.get("total")

        return {
            "merchant": merchant or "",
            "invoice_number": invoice_number or "",
            "invoice_date": invoice_date or "",
            "subtotal": subtotal,
            "tax": tax,
            "total": total,
            "currency": currency,
        }

    def _extract_merchant(self, lines):
        for line in lines[:5]:
            if not re.search(r"invoice|bill|date|total|amount|due", line, re.IGNORECASE):
                return line
        return lines[0] if lines else ""

    def _extract_invoice_number(self, text):
        match = self.INVOICE_NUMBER_PATTERN.search(text)
        return match.group(1).strip() if match else None

    def _extract_date(self, text):
        match = self.DATE_PATTERN.search(text)
        if not match:
            return None

        raw_date = match.group("date")
        for fmt in ("%Y-%m-%d", "%Y/%m/%d", "%d-%m-%Y", "%d/%m/%Y", "%m/%d/%Y", "%Y.%m.%d"):
            try:
                parsed = datetime.strptime(raw_date, fmt)
                return parsed.strftime("%Y-%m-%d")
            except ValueError:
                continue
        return raw_date

    def _extract_currency(self, text):
        match = self.CURRENCY_PATTERN.search(text)
        return match.group(1).upper() if match else None

    def _extract_amounts(self, text):
        amounts = {}
        for match in self.AMOUNT_PATTERN.finditer(text.lower()):
            label = match.group("label").lower()
            value = self._parse_number(match.group("value"))
            if value is None:
                continue

            if "subtotal" in label and "tax" not in label:
                amounts["subtotal"] = value
            elif "tax" in label:
                amounts["tax"] = value
            elif "total" in label or "amount" in label:
                amounts["total"] = value

        return amounts

    def _parse_number(self, raw):
        cleaned = raw.replace(",", "").replace(" ", "")
        try:
            return float(cleaned)
        except ValueError:
            return None
