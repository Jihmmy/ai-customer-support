"""
Schémas Pydantic pour le système de chat IA.
"""

from pydantic import BaseModel

class ChatRequest(BaseModel):
    """
    Message envoyé par le client.
    """

    message: str


class ChatResponse(BaseModel):
    """
    Réponse retournée par l'IA.
    """

    response: str