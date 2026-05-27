from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from app.api.invoice import router as invoice_router

app = FastAPI(
    title="Invoice AI POC",
    description="Lightweight invoice OCR, extraction, and validation proof of concept.",
    version="0.1.0",
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(invoice_router)


@app.get("/")
def root():
    return {"status": "ok", "message": "Invoice AI POC backend is running."}
