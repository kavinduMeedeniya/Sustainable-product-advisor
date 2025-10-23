import json
import logging
from models.schemas import ProductInfo, RecyclingOptions
from utils.gemini_client import GeminiClient

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

async def get_recycling_options(product_info: ProductInfo) -> RecyclingOptions:
    logger.info(f"Fetching recycling options for product: {product_info.name}")
    # Load mock recycling database
    with open("data/recycling_db.json", "r") as f:
        recycling_db = json.load(f)
    
    gemini = GeminiClient()
    prompt = f"""
    Based on the product materials and recycling database, provide recycling or return options.
    Product: {product_info.name}
    Materials: {', '.join(product_info.materials)}
    Recycling DB: {json.dumps(recycling_db)}
    
    Output format: JSON with fields options (list of str)
    """
    try:
        response = await gemini.generate_content(prompt)
        logger.info(f"Gemini response: {response}")
        data = json.loads(response)
    except json.JSONDecodeError as e:
        logger.error(f"Failed to parse Gemini response: {response}, error: {str(e)}")
        data = {"options": ["No recycling options available"]}
    
    return RecyclingOptions(
        options=data.get("options", ["No recycling options available"])
    )