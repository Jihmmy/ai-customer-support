import google.generativeai as genai

from google.api_core.exceptions import GoogleAPIError, DeadlineExceeded
from app.config.settings import GEMINI_API_KEY

import logging

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

genai.configure(api_key=GEMINI_API_KEY)

model = genai.GenerativeModel("gemini-1.5-flash")


def generate_ai_response(prompt: str) -> str:
    """
    Génère réponse IA avec Gemini + gestion erreurs.
    """

    try:
        if not prompt.strip():
            return "Prompt vide"

        response = model.generate_content(prompt)

        if not response.text:
            return "Réponse vide IA"

        return response.text


    except DeadlineExceeded:
        logger.error("Timeout Gemini API")
        return "IA trop lente, réessayez."


    except GoogleAPIError as e:
        logger.error(f"Gemini API error: {e}")
        return "Erreur API IA."


    except Exception as e:
        logger.error(f"Unknown error: {e}")
        return "Erreur interne IA."