import json
import logging
from models.schemas import ProductInfo, EcoScore
from utils.gemini_client import GeminiClient

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

async def get_eco_score(product_info: ProductInfo) -> EcoScore:
    logger.info(f"Evaluating eco-score for product: {product_info.name}")
    gemini = GeminiClient()
    prompt = f"""
    Evaluate the eco-friendliness of this product based on its materials and description.
    Product: {product_info.name}
    Materials: {', '.join(product_info.materials)}
    Description: {product_info.description}
    
    Provide a score (0-100) and a brief reason.
    Output format: JSON with fields score (int), reason (str)
    """
    try:
        response = await gemini.generate_content(prompt)
        logger.info(f"Cleaned Gemini response: {response}")
        data = json.loads(response)
    except json.JSONDecodeError as e:
        logger.error(f"Failed to parse Gemini response: {response}, error: {str(e)}")
        data = {"score": 50, "reason": "Failed to parse eco-score response or missing materials"}
    
    return EcoScore(
        score=data.get("score", 50),
        reason=data.get("reason", "No reason provided")
    )