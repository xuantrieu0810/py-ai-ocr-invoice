from io import BytesIO
from typing import Dict, List

import numpy as np
from paddleocr import PaddleOCR
from PIL import Image


class OCRService:
    def __init__(self):
        self._ocr = None

        try:
            self._ocr = PaddleOCR(lang="en")
            print("PaddleOCR initialized successfully")
        except Exception as e:
            print(f"PaddleOCR init failed: {e}")

    def extract_text(self, file_bytes: bytes) -> Dict[str, object]:
        if self._ocr is None:
            return {
                "lines": [],
                "full_text": "",
            }

        try:
            image = Image.open(BytesIO(file_bytes)).convert("RGB")
            image_array = np.array(image)

            return self._extract_with_paddleocr(image_array)

        except Exception as e:
            print(f"OCR extract failed: {e}")

            return {
                "lines": [],
                "full_text": "",
            }

    def _extract_with_paddleocr(
        self,
        image_array: np.ndarray,
    ) -> Dict[str, object]:
        raw_result = self._ocr.predict(image_array)

        lines: List[Dict[str, object]] = []
        text_lines: List[str] = []

        if not raw_result:
            return {
                "lines": [],
                "full_text": "",
            }

        for result in raw_result:
            texts = result.get("rec_texts", [])
            scores = result.get("rec_scores", [])
            boxes = result.get("dt_polys", [])

            for text, confidence, box in zip(
                texts,
                scores,
                boxes,
            ):
                bbox = [[int(coord[0]), int(coord[1])] for coord in box]

                lines.append(
                    {
                        "text": text,
                        "bbox": bbox,
                        "confidence": float(confidence),
                    }
                )

                text_lines.append(text)

        return {
            "lines": lines,
            "full_text": "\n".join(text_lines),
        }
