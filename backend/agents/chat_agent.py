import json
import re
from models.schemas import ProductQuery
from utils.gemini_client import GeminiClient
from utils.search import search_product_url
from agents.product_info_agent import get_product_info
from agents.eco_score_agent import get_eco_score
from agents.recycling_agent import get_recycling_options
from agents.recommendation_agent import get_recommendation


# ✅ Sensitive keywords (expand this list as needed)
SENSITIVE_KEYWORDS = [
    "bomb", "gun", "kill", "murder", "drugs", "sex", "nude",
    "nudity", "porn", "profanity", "abuse", "terrorist", "blood",
    "violence", "suicide", "weapon", "explosive", "assault"
]


def contains_sensitive_content(message: str) -> bool:
    """Return True if message contains sensitive/inappropriate words."""
    pattern = re.compile(r'\b(' + '|'.join(SENSITIVE_KEYWORDS) + r')\b', re.IGNORECASE)
    return bool(pattern.search(message))


async def get_chat_response(message: str) -> dict:
    # ✅ Step 1: Sensitive content check FIRST
    if contains_sensitive_content(message):
        # 🚫 Stop processing immediately
        return {
            "type": "warning",
            "message": "⚠️ This is sensitive content. Please avoid such topics."
        }

    # ✅ Step 2: Continue only if message is safe
    gemini = GeminiClient()
    prompt = f"""
    Analyze the user message: "{message}"
    
    - If it's a casual greeting or conversation (e.g., "hi", "hello", "how are you"), classify as "casual" and generate a friendly, engaging response as an eco-conscious shopping assistant (e.g., "Hi there! I'm here to help with sustainable shopping tips. What can I assist you with?").
    - If it's a product query (e.g., "tell me about eco-friendly bags" or "check this: eco-friendly bags https://example.com"), classify as "product", extract the product_name, and extract url if mentioned (null if not).
    
    Output ONLY valid JSON:
    {{
        "type": "casual" or "product",
        "response": "friendly reply if casual" (str or null),
        "product_name": "extracted name if product" (str or null),
        "url": "extracted url if provided" (str or null)
    }}
    """

    response_text = await gemini.generate_content(prompt)

    try:
        data = json.loads(response_text)
    except json.JSONDecodeError:
        return {"error": "Failed to parse message. Please try again."}

    # ✅ Step 3: Casual messages
    if data.get("type") == "casual":
        return {"message": data.get("response", "Hello! How can I help today?")}

    # ✅ Step 4: Product queries
    elif data.get("type") == "product":
        product_name = data.get("product_name")
        url = data.get("url")

        if not product_name:
            return {"error": "No product name detected in query."}

        if not url:
            searched_url = await search_product_url(product_name)
            if not searched_url:
                return {"error": "Unable to find a URL for the product. Please provide one."}
            url = searched_url

        query = ProductQuery(product_name=product_name, url=url)
        product_info = await get_product_info(query)
        eco_score = await get_eco_score(product_info)
        recycling_options = await get_recycling_options(product_info)
        recommendation = await get_recommendation(product_info, eco_score, recycling_options)

        return {
            "type": "product",
            "product_info": product_info.dict(),
            "eco_score": eco_score.dict(),
            "recycling_options": recycling_options.dict(),
            "recommendation": recommendation.dict()
        }

    # ✅ Step 5: Unknown message type
    return {"error": "Unknown message type. Please clarify."}
