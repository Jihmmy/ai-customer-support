"""
Schémas Pydantic pour le système de chat IA.
"""

from pydantic import BaseModel, Field

class ChatRequest(BaseModel):
    """
    Message envoyé par le client.
    """

    message: str = Field(..., min_length=1, max_length=1000)


class ChatResponse(BaseModel):
    """
    Réponse retournée par l'IA.
    """

    response: str