from io import BytesIO
from typing import Dict, List

import numpy as np
from paddleocr import PaddleOCR
from PIL import Image

try:
    import pytesseract
    PYTESSERACT_AVAILABLE = True
except ImportError:
    PYTESSERACT_AVAILABLE = False


class OCRService:
    def __init__(self):
        self._ocr = None
        self._use_pytesseract = False
        
        # Try PaddleOCR first (heavy but accurate)
        try:
            self._ocr = PaddleOCR(use_angle_cls=True, lang="en")
        except Exception:
            pass
        
        # Fall back to pytesseract if available
        if self._ocr is None and PYTESSERACT_AVAILABLE:
            self._use_pytesseract = True

    def extract_text(self, file_bytes: bytes) -> Dict[str, object]:
        image = Image.open(BytesIO(file_bytes)).convert("RGB")
        image_array = np.array(image)
        
        if self._use_pytesseract:
            # Use pytesseract (lightweight)
            return self._extract_with_pytesseract(Image.fromarray(image_array))
        elif self._ocr is not None:
            # Use PaddleOCR
            return self._extract_with_paddleocr(image_array)
        else:
            # No OCR available
            return {"lines": [], "full_text": ""}

    def _extract_with_pytesseract(self, image: Image.Image) -> Dict[str, object]:
        """Extract text using pytesseract."""
        text = pytesseract.image_to_string(image)
        lines = [{"text": line, "bbox": [], "confidence": 0.9} for line in text.split('\n') if line.strip()]
        return {"lines": lines, "full_text": text}

    def _extract_with_paddleocr(self, image_array: np.ndarray) -> Dict[str, object]:
        """Extract text using PaddleOCR."""
        raw_result = self._ocr.ocr(image_array, cls=True)
        lines: List[Dict[str, object]] = []
        text_lines: List[str] = []

        for item in raw_result:
            if len(item) < 2:
                continue
            box, text_info = item[0], item[1]
            if not isinstance(text_info, (list, tuple)) or len(text_info) < 2:
                continue

            text = text_info[0]
            confidence = float(text_info[1])
            bbox = [[int(coord[0]), int(coord[1])] for coord in box]

            lines.append({"text": text, "bbox": bbox, "confidence": confidence})
            text_lines.append(text)

        return {
            "lines": lines,
            "full_text": "\n".join(text_lines),
        }
