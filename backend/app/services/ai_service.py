from google import genai
import logging
from app.config.settings import GEMINI_API_KEY

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Client Gemini (nouveau SDK)
client = genai.Client(api_key=GEMINI_API_KEY)


def generate_ai_response(prompt: str) -> str:
    """
    Génère une réponse IA avec Gemini (nouveau SDK google-genai)
    """

    try:
        if not prompt.strip():
            return "Prompt vide"

        response = client.models.generate_content(
            model="gemini-2.0-flash",
            contents=prompt
        )

        if not response.text:
            return "Réponse vide IA"

        return response.text

    except Exception as e:
        logger.error(f"Gemini API error: {e}")
        return "Erreur API IA."