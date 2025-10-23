from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import ValidationError
from agents.product_info_agent import get_product_info
from agents.eco_score_agent import get_eco_score
from agents.recycling_agent import get_recycling_options
from agents.recommendation_agent import get_recommendation
from agents.chat_agent import get_chat_response  # New import
from models.schemas import ProductQuery, ProductInfo, EcoScore, RecyclingOptions, Recommendation, ChatMessage
from utils.search import search_product_url  # New import for auto-search

app = FastAPI(title="Eco-Conscious Shopping Assistant")

# CORS for frontend (even though frontend is not implemented)
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.post("/product-info", response_model=ProductInfo)
async def product_info_endpoint(query: ProductQuery):
    try:
        if not query.url:  # Auto-search if no URL
            query.url = search_product_url(query.product_name)
            if not query.url:
                raise HTTPException(status_code=400, detail="No URL provided and search failed")
        return await get_product_info(query)
    except ValidationError as e:
        raise HTTPException(status_code=422, detail=str(e))
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.post("/eco-score", response_model=EcoScore)
async def eco_score_endpoint(product_info: ProductInfo):
    try:
        return await get_eco_score(product_info)
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.post("/recycling-options", response_model=RecyclingOptions)
async def recycling_options_endpoint(product_info: ProductInfo):
    try:
        return await get_recycling_options(product_info)
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.post("/recommendation", response_model=Recommendation)
async def recommendation_endpoint(product_info: ProductInfo, eco_score: EcoScore, recycling_options: RecyclingOptions):
    try:
        return await get_recommendation(product_info, eco_score, recycling_options)
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

# New conversational endpoint
@app.post("/chat", response_model=dict)
async def chat_endpoint(chat: ChatMessage):
    try:
        return await get_chat_response(chat.message)
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))