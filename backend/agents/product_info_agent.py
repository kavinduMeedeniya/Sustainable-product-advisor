import json
import logging
from models.schemas import ProductQuery, ProductInfo
from utils.scraper import scrape_product_page
from utils.gemini_client import GeminiClient
from utils.search import search_product_url

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

async def get_product_info(query: ProductQuery) -> ProductInfo:
    gemini = GeminiClient()
    
    # Use search if no URL provided
    url = query.url
    if not url:
        url = await search_product_url(query.product_name)  # Made async; see below
        if not url:
            logger.error(f"No URL found for {query.product_name}")
            raise ValueError("Unable to find a product URL")
    
    # Scrape the page
    scraped_data = scrape_product_page(str(url))  # Convert HttpUrl to string
    logger.info(f"Scraped data: {scraped_data}")
    
    # Validate scraped data
    infer_mode = False
    if scraped_data.get("name") == "Unknown" and scraped_data.get("materials") == ["unknown"]:
        logger.warning(f"Scraped data is generic for {url}; instructing Gemini to infer product")
        scraped_data["context"] = f"Category page for {query.product_name}. Infer a specific product."
        infer_mode = True
    
    # Handle search/category pages - Fix: Use str(url).lower()
    is_search_page = any(indicator in str(url).lower() for indicator in ["/s?k=", "/search", "/collections", "/shop/all"])
    context = (
        f"This is a search or category page for {query.product_name}. "
        "Infer the first or most relevant eco-friendly product from the data."
    ) if is_search_page else "This is a product page. Extract details directly."
    
    # Prepare prompt for Gemini
    prompt = f"""
    {context}
    Given the scraped data from {url}:
    {json.dumps(scraped_data)}
    
    Extract and format the product information as valid JSON:
    {{
        "name": "specific product name",
        "brand": "brand name",
        "materials": ["material1", "material2", ...],
        "price": float,
        "description": "product description",
        "url": "specific product URL (infer a real one if this is a category page)"
    }}
    
    If the data is from a category page (e.g., contains 'shop' or 'collections'), infer a specific product based on the query "{query.product_name}".
    Example: For "eco-friendly jackets" on a category page, infer a product like "Men's Nano Puff Jacket" with recycled polyester, and provide its specific URL like "https://www.patagonia.com/product/mens-nano-puff-jacket/84212.html".
    Ensure materials reflect eco-friendly attributes (e.g., recycled polyester, organic cotton).
    If data is missing, provide reasonable values based on the website and query.
    If inferring, provide a specific, valid product URL from the same website (do not make up invalid URLs; use known structures like /product/...).
    Output valid JSON with no extra text or markdown.
    """
    response_text = await gemini.generate_content(prompt)
    try:
        data = json.loads(response_text)
        # Update URL if Gemini inferred a new one
        inferred_url = data.get("url", str(url))
        
        # If inferred a new URL and we're in infer mode, re-scrape for real data
        if infer_mode and inferred_url != str(url):
            logger.info(f"Gemini inferred new URL: {inferred_url}; re-scraping for accuracy")
            new_scraped_data = scrape_product_page(inferred_url)
            if new_scraped_data.get("name") != "Unknown":  # Re-scrape succeeded
                scraped_data = new_scraped_data
                data.update(new_scraped_data)  # Override with real scraped data
                data["url"] = inferred_url
            else:
                logger.warning(f"Re-scrape of {inferred_url} failed; keeping Gemini inference")
        
        # Validate materials
        if not data.get("materials") or data.get("materials") == ["unknown"]:
            logger.warning("Gemini returned no materials; using scraped materials")
            data["materials"] = scraped_data.get("materials", ["unknown"])
        
        return ProductInfo(
            name=data.get("name", query.product_name),
            brand=data.get("brand", scraped_data.get("brand", "Unknown")),
            materials=data.get("materials", ["unknown"]),
            price=float(data.get("price", scraped_data.get("price", 0.0))),
            description=data.get("description", scraped_data.get("description", "No description available")),
            url=inferred_url  # Use potentially updated URL
        )
    except json.JSONDecodeError:
        logger.error(f"Failed to parse Gemini response for {url}: {response_text}")
        return ProductInfo(
            name=query.product_name,
            brand=scraped_data.get("brand", "Unknown"),
            materials=scraped_data.get("materials", ["unknown"]),
            price=scraped_data.get("price", 0.0),
            description=scraped_data.get("description", "No description available"),
            url=url
        )