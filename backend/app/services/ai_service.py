"""
Service IA.

Ce fichier gère :
- connexion DeepSeek API
- envoi prompts
- récupération réponses IA
"""

from openai import OpenAI

from app.config.settings import (
    DEEPSEEK_API_KEY
)

# Initialisation client DeepSeek
client = OpenAI(
    api_key=DEEPSEEK_API_KEY,
    base_url="https://api.deepseek.com"
)

def generate_ai_response(prompt: str) -> str:
    """
    Envoie un prompt à DeepSeek
    et retourne la réponse IA.

    Args:
        prompt (str): Prompt envoyé au modèle

    Returns:
        str: Réponse générée par l'IA
    """

    response = client.chat.completions.create(
        model="deepseek-chat",

        messages=[
            {
                "role": "system",
                "content": (
                    "Tu es un assistant vendeur professionnel "
                    "pour une boutique en ligne."
                )
            },
            {
                "role": "user",
                "content": prompt
            }
        ],

        # Contrôle créativité
        temperature=0.7,

        # Taille maximale réponse
        max_tokens=300
    )

    return response.choices[0].message.content