# Invoice AI Backend

## Setup

```bash
deactivate
python3 -m venv .venv
source .venv/bin/activate
pip install --upgrade pip
pip install -r requirements.txt
```

## Run server

```bash
cd /Users/trieulx/Developer/Learning/AI/poc_ocr/backend
source .venv/bin/activate
uvicorn app.main:app --reload --host 0.0.0.0 --port 8000
```

## API

- `POST /invoice/analyze`
  - Accepts PNG, JPG, TIFF, or PDF file upload
  - Returns extracted invoice fields, warnings, and status

## Notes

- The backend uses `PaddleOCR` for text extraction.
- The current structure is organized as a package under `backend/`.
- Keep `backend/.venv` inside `backend/` to separate the runtime environment from project docs and top-level files.
