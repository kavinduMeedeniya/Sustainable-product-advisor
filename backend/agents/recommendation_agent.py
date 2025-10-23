from models.schemas import ProductInfo, EcoScore, RecyclingOptions, Recommendation
from utils.gemini_client import GeminiClient
from utils.search import search_product_url
from utils.scraper import scrape_product_page
import random
import logging
import json

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

ECO_SITES = [
    "patagonia.com",
    "rei.com",
    "everlane.com",
    "cotopaxi.com",
    "ethicalsuperstore.com"
]

async def get_recommendation(product_info: ProductInfo, eco_score: EcoScore, recycling_options: RecyclingOptions) -> Recommendation:
    gemini = GeminiClient()
    product_category = product_info.name.lower().split()[0]  # E.g., "jacket" from "Men's Nano Puff Jacket"
    
    # Find alternative product from a different eco-friendly site
    current_site = str(product_info.url).split("/")[2]  # Convert HttpUrl to string, e.g., "patagonia.com"
    alternative_sites = [site for site in ECO_SITES if site != current_site]
    if not alternative_sites:
        alternative_sites = ECO_SITES  # Fallback to any site if needed
    
    alternative_url = None
    for site in alternative_sites:
        query = f"{product_category} eco-friendly"
        url = await search_product_url(query)  # Added await
        if url and isinstance(url, str) and site in url:  # Ensure url is a string
            alternative_url = url
            break
    
    if not alternative_url:
        alternative_url = f"https://www.amazon.com/s?k={product_category}+eco-friendly" 
    
    # Handle search/category pages
    is_search_page = any(indicator in str(alternative_url).lower() for indicator in ["/s?k=", "/search", "/collections"])
    context = (
        f"This is a search or category page for {product_category}. "
        "Infer the first or most relevant eco-friendly product from the data."
    ) if is_search_page else "This is a product page. Extract details directly."
    
    # Use Gemini to generate recommendation based on real alternative
    prompt = f"""
    {context}
    Given a product: {product_info.name} from {product_info.url} with eco-score {eco_score.score} ({eco_score.reason}) and recycling options {recycling_options.options},
    recommend a specific alternative eco-friendly product from {alternative_url}.
    Ensure the recommendation is a real, specific product (not generic) from a different website.
    Provide the product name, a reason for the recommendation, and the product URL, considering sustainability.
    Output valid JSON:
    {{
        "recommended_product": "specific product name",
        "reason": "why this is a good alternative",
        "url": "specific product URL"
    }}
    Output valid JSON with no extra text or markdown.
    """
    response_text = await gemini.generate_content(prompt)
    try:
        data = json.loads(response_text)
        return Recommendation(
            recommended_product=data.get("recommended_product", "Alternative Eco-Friendly Product"),
            reason=data.get("reason", "This product is a sustainable alternative with similar eco-friendly materials."),
            url=data.get("url", alternative_url)  # Include URL in Recommendation
        )
    except json.JSONDecodeError:
        logger.error("Failed to parse Gemini response for recommendation")
        return Recommendation(
            recommended_product="Alternative Eco-Friendly Product",
            reason="This product from another eco-friendly retailer offers similar sustainability benefits.",
            url=alternative_url
        )