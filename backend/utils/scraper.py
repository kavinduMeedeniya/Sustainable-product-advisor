import requests
from bs4 import BeautifulSoup
import logging
import random
import time

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

USER_AGENTS = [
    "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36",
    "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.114 Safari/537.36",
    "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.101 Safari/537.36"
]

def scrape_product_page(url: str) -> dict:
    headers = {
        "User-Agent": random.choice(USER_AGENTS),
        "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8",
        "Accept-Language": "en-US,en;q=0.5",
        "Accept-Encoding": "gzip, deflate",
        "Connection": "keep-alive"
    }
    
    try:
        time.sleep(2)  # Avoid rate limits
        response = requests.get(url, headers=headers, timeout=10)
        response.raise_for_status()
        soup = BeautifulSoup(response.text, "html.parser")
        
        data = {}
        
        # Try JSON-LD (common in e-commerce)
        json_ld = soup.find("script", type="application/ld+json")
        if json_ld:
            import json
            try:
                json_data = json.loads(json_ld.string)
                if isinstance(json_data, dict):
                    data["name"] = json_data.get("name")
                    data["brand"] = json_data.get("brand", {}).get("name")
                    data["price"] = float(json_data.get("offers", {}).get("price", 0.0))
                    data["description"] = json_data.get("description")
            except json.JSONDecodeError:
                pass
        
        # Fallback to HTML scraping
        if not data.get("name"):
            data["name"] = soup.find("h1") or soup.find("h2") or ""
            data["name"] = data["name"].text.strip() if data["name"] else "Unknown"
        
        if not data.get("brand"):
            meta_brand = soup.find("meta", property="og:brand") or soup.find("meta", name="brand")
            data["brand"] = meta_brand["content"] if meta_brand else "Unknown"
        
        if not data.get("price"):
            price_tag = soup.find("span", class_=lambda x: x and ("price" in x.lower() or "amount" in x.lower()))
            data["price"] = float(price_tag.text.strip("$").replace(",", "")) if price_tag else 0.0
        
        if not data.get("description"):
            desc_tag = soup.find("meta", property="og:description") or soup.find("meta", name="description") or soup.find("p", class_=lambda x: x and "description" in x.lower())
            data["description"] = desc_tag["content"] if desc_tag and "content" in desc_tag.attrs else (desc_tag.text.strip() if desc_tag else "No description available")
        
        # Materials (often in product details or description)
        details = soup.find("div", class_=lambda x: x and ("details" in x.lower() or "material" in x.lower()))
        data["materials"] = []
        if details:
            text = details.text.lower()
            if "recycled polyester" in text:
                data["materials"].append("recycled polyester")
            if "organic cotton" in text:
                data["materials"].append("organic cotton")
            if "recycled nylon" in text:
                data["materials"].append("recycled nylon")
            if not data["materials"]:
                data["materials"] = ["unknown"]
        else:
            data["materials"] = ["unknown"]
        
        return data
    
    except Exception as e:
        logger.error(f"Scraping failed for {url}: {str(e)}")
        return {
            "name": "Unknown",
            "brand": "Unknown",
            "materials": ["unknown"],
            "price": 0.0,
            "description": "No description available"
        }
    