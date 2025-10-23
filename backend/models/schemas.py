from pydantic import BaseModel, HttpUrl, Field
from typing import List, Optional

class ProductQuery(BaseModel):
    product_name: str = Field(..., min_length=1, max_length=100)
    url: Optional[HttpUrl] = None  # Made optional

class ProductInfo(BaseModel):
    name: str
    brand: str
    materials: List[str]
    price: float
    description: str
    url: HttpUrl

class EcoScore(BaseModel):
    score: int = Field(..., ge=0, le=100)
    reason: str

class RecyclingOptions(BaseModel):
    options: List[str]

class Recommendation(BaseModel):
    recommended_product: str
    reason: str
    url: Optional[HttpUrl] = None

class ChatMessage(BaseModel):  # New for /chat
    message: str = Field(..., min_length=1)