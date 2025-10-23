import os
import google.generativeai as genai
from dotenv import load_dotenv
from fastapi import HTTPException
import logging
import re

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

load_dotenv()

class GeminiClient:
    def __init__(self):
        try:
            genai.configure(api_key=os.getenv("GEMINI_API_KEY"))
            self.model_name = "gemini-2.5-flash"  # Updated to current stable model
            self.model = genai.GenerativeModel(self.model_name)
            logger.info(f"Initialized GeminiClient with model: {self.model_name}")
        except Exception as e:
            logger.error(f"Failed to initialize GeminiClient: {str(e)}")
            raise HTTPException(status_code=500, detail=f"GeminiClient initialization error: {str(e)}")
    
    async def generate_content(self, prompt: str) -> str:
        try:
            response = await self.model.generate_content_async(
                prompt,
            )
            # Log raw response
            raw_text = response.text or ""
            logger.info(f"Raw Gemini response: {raw_text}")
            
            # Clean response: strip markdown and extra whitespace
            cleaned_text = re.sub(r'^```json\s*|\s*```$', '', raw_text, flags=re.MULTILINE).strip()
            if not cleaned_text:
                logger.error("Gemini response is empty after cleaning")
                raise ValueError("Empty response from Gemini API")
            
            return cleaned_text
        except Exception as e:
            logger.error(f"Gemini API error: {str(e)}")
            raise HTTPException(status_code=500, detail=f"Gemini API error: {str(e)}")