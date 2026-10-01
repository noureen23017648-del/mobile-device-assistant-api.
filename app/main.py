from fastapi import FastAPI

from app.schemas.device import (
    ExtractRequest,
    ExtractResponse,
    SearchRequest,
    SearchResponse,
)

from app.services.extraction import extract_device
from app.services.search import hybrid_search


app = FastAPI(
    title="Mobile Device Assistant API",
    description="AI-powered Mobile Device Assistant",
    version="1.0.0"
)


@app.get("/")
def root():
    return {
        "message": "Mobile Device Assistant API is running"
    }


@app.post("/extract", response_model=ExtractResponse)
def extract(request: ExtractRequest):
    device = extract_device(request.text)

    return {
        "device": device
    }


@app.post("/search", response_model=SearchResponse)
def search(request: SearchRequest):
    results = hybrid_search(request.q, k=3)

    return {
        "results": [
            {
                "document": document,
                "score": score
            }
            for document, score in results
        ]
    }