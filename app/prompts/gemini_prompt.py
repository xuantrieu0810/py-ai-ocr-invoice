from typing import Dict

PROMPT_TEMPLATE = """
You are an invoice analysis assistant.

OCR Text:
{ocr_text}

Candidate Fields:
{candidate_fields}

Validation Results:
{rule_results}

Return only strict JSON with the following structure:
{
  "validated_fields": {
    "merchant": "...",
    "invoice_number": "...",
    "invoice_date": "...",
    "subtotal": 0.0,
    "tax": 0.0,
    "total": 0.0,
    "currency": "..."
  },
  "warnings": [],
  "status": "valid"
}
"""


def build_prompt(ocr_text: str, candidate_fields: Dict[str, object], rule_results: Dict[str, object]) -> str:
    return PROMPT_TEMPLATE.format(
        ocr_text=ocr_text,
        candidate_fields=candidate_fields,
        rule_results=rule_results,
    )
