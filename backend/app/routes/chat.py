"""
Routes API du chatbot IA.
"""

from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from app.database import SessionLocal
from app.models.product import Product

from app.schemas.chat_schema import (
    ChatRequest,
    ChatResponse
)

from app.services.ai_service import (
    generate_ai_response
)

# Création router FastAPI
router = APIRouter()

def get_db():
    """
    Ouvre une session PostgreSQL
    puis la ferme automatiquement.
    """

    db = SessionLocal()

    try:
        yield db

    finally:
        db.close()


@router.post(
    "/chat",
    response_model=ChatResponse,
    tags=["AI Chat"]
)
def chat(
    request: ChatRequest,
    db: Session = Depends(get_db)
):
    """
    Endpoint principal du chatbot IA.

    Processus :
    1. Lire produits PostgreSQL
    2. Construire contexte vendeur
    3. Envoyer prompt à DeepSeek
    4. Retourner réponse IA
    """

    # Récupération produits
    products = db.query(Product).all()

    # Construction contexte produits
    products_context = ""

    for product in products:

        products_context += f"""
        Produit : {product.name}
        Description : {product.description}
        Prix : {product.price} Ariary
        Stock : {product.stock}
        """

    # Prompt envoyé à l'IA
    prompt = f"""
    Tu travailles comme assistant vendeur IA.

    Voici les produits disponibles :

    {products_context}

    Instructions :
    - Réponds en français
    - Sois professionnel
    - Réponds clairement
    - Utilise les informations produits
    - Ne crée pas de faux prix

    Message client :
    {request.message}
    """

    # Génération réponse IA
    ai_response = generate_ai_response(prompt)

    return {
        "response": ai_response
    }