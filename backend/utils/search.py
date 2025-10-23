import requests
from bs4 import BeautifulSoup
import urllib.parse
import logging
import random
import time
import random

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# List of eco-friendly e-commerce sites
ECO_SITES = [
    "foaclothing.com",
    "rei.com",
    "everlane.com",
    "cotopaxi.com",
    "ethicalsuperstore.com"
]

# Rotate user agents to avoid blocks
USER_AGENTS = [
    "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36",
    "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.114 Safari/537.36",
    "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.101 Safari/537.36"
]

async def search_product_url(product_name: str) -> str | None:  # Made async (though no await inside; allows future expansion)
    headers = {
        "User-Agent": random.choice(USER_AGENTS),
        "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8",
        "Accept-Language": "en-US,en;q=0.5",
        "Accept-Encoding": "gzip, deflate",
        "Connection": "keep-alive"
    }

    # Try each eco-friendly site with specific product search
    for site in ECO_SITES:
        logger.info(f"Searching for {product_name} on {site}")
        query = f"site:{site} eco-friendly {product_name} buy product"  # Added "eco-friendly" for relevance
        encoded_query = urllib.parse.quote(query)
        search_url = f"https://www.google.com/search?q={encoded_query}&num=10"  # Increased num for more results
        try:
            response = requests.get(search_url, headers=headers, timeout=10)
            response.raise_for_status()
            soup = BeautifulSoup(response.text, "html.parser")
            
            for link in soup.find_all("a"):
                href = link.get("href")
                if href and href.startswith("/url?q="):
                    actual_url = href.split("/url?q=")[1].split("&")[0]
                    actual_url = urllib.parse.unquote(actual_url)
                    # Relaxed condition: Accept if on site and looks product-like (added more patterns like .html, /p/)
                    if site in actual_url and not any(domain in actual_url for domain in ["google", "youtube", "wikipedia", "facebook", "twitter"]):
                        if any(ind in actual_url.lower() for ind in ["/product/", "/item/", "/p/", ".html", "/shop/"]):
                            logger.info(f"Found product URL for {product_name} on {site}: {actual_url}")
                            return actual_url
            time.sleep(2)  # Avoid rate limits
        except Exception as e:
            logger.error(f"Search failed for {site}: {str(e)}")
            continue

    # Fallback: Check category pages for product links
    for site in ECO_SITES:
        query = f"site:{site} eco-friendly {product_name}"  # Added "eco-friendly"
        encoded_query = urllib.parse.quote(query)
        search_url = f"https://www.google.com/search?q={encoded_query}&num=10"
        try:
            response = requests.get(search_url, headers=headers, timeout=10)
            response.raise_for_status()
            soup = BeautifulSoup(response.text, "html.parser")
            
            for link in soup.find_all("a"):
                href = link.get("href")
                if href and href.startswith("/url?q="):
                    actual_url = href.split("/url?q=")[1].split("&")[0]
                    actual_url = urllib.parse.unquote(actual_url)
                    if site in actual_url and any(ind in actual_url.lower() for ind in ["/c/", "/shop/", "/collections/", "/category/"]):
                        # Scrape category page for product link
                        product_url = extract_product_from_category(actual_url, headers)
                        if product_url:
                            logger.info(f"Found product URL from category page {actual_url}: {product_url}")
                            return product_url
            time.sleep(2)
        except Exception as e:
            logger.error(f"Category search failed for {site}: {str(e)}")
            continue

    fallback_urls = [
    "https://www.foaclothing.com/collections/all",     # FOA Clothing (local)
    "https://www.kaymu.lk/",                           # Kaymu / Daraz local fashion
    "https://www.coolplanet.lk/collections/all",       # Cool Planet
    "https://www.gflock.com/collections/all",          # Gflock
    "https://www.nolimit.lk/collections/all", 
    ]

    fallback_url = random.choice(fallback_urls)
    logger.info(f"No specific URL found for {product_name}; using fallback: {fallback_url}")
    return fallback_url


def extract_product_from_category(category_url: str, headers: dict) -> str | None:
    try:
        response = requests.get(category_url, headers=headers, timeout=10)
        response.raise_for_status()
        soup = BeautifulSoup(response.text, "html.parser")
        
        # Improved: Look for product links with more class-based or pattern matching (e.g., for Patagonia: class="product-tile__link")
        product_links = soup.find_all("a", class_=lambda x: x and ("product" in x.lower() or "item" in x.lower() or "tile" in x.lower()))
        if not product_links:
            # Fallback to any a with /product/ or .html
            product_links = soup.find_all("a", href=lambda h: h and ("/product/" in h.lower() or "/item/" in h.lower() or h.endswith(".html")))
        
        for link in product_links:
            href = link.get("href")
            if href:
                # Ensure full URL
                if href.startswith("http"):
                    return href
                elif href.startswith("/"):
                    from urllib.parse import urljoin
                    return urljoin(category_url, href)
        return None
    except Exception as e:
        logger.error(f"Failed to extract product from category {category_url}: {str(e)}")
        return None