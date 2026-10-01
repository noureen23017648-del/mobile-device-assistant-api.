from typing import Dict, List, Literal

from pydantic import BaseModel, Field


class Device(BaseModel):
    brand: str
    model: str
    specs: Dict[str, str]
    release_year: int
    price_tier: Literal["budget", "mid-range", "flagship"]


class ExtractRequest(BaseModel):
    text: str


class ExtractResponse(BaseModel):
    device: Device


class SearchRequest(BaseModel):
    q: str = Field(..., max_length=500)


class SearchResult(BaseModel):
    document: str
    score: float


class SearchResponse(BaseModel):
    results: List[SearchResult]