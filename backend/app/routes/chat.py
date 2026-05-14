from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

# Import de la session SQLAlchemy
from app.database import SessionLocal

# Import du modèle Product
from app.models.product import Product

# Import des schémas Pydantic
from app.schemas.chat_schema import ChatRequest, ChatResponse

# Import du service IA
from app.services.ai_service import generate_ai_response


# Création du router FastAPI
router = APIRouter(
    prefix="/chat",
    tags=["AI Chat"]
)


# =========================
# DATABASE DEPENDENCY
# =========================
def get_db():
    """
    Crée une session de base de données
    puis la ferme automatiquement
    après la requête.
    """

    db = SessionLocal()

    try:
        yield db

    finally:
        db.close()


# =========================
# CHAT ENDPOINT
# =========================
@router.post(
    "/",
    response_model=ChatResponse
)
def chat(
    request: ChatRequest,
    db: Session = Depends(get_db)
):
    """
    Chatbot IA vendeur.

    Cette route :
    - récupère les produits
    - construit un contexte IA
    - envoie le prompt au modèle IA
    - retourne la réponse générée
    """

    # -------------------------
    # Validation du message
    # -------------------------
    if not request.message.strip():

        raise HTTPException(
            status_code=400,
            detail="Message invalide"
        )

    # -------------------------
    # Récupération des produits
    # -------------------------
    products = db.query(Product).all()

    if not products:

        raise HTTPException(
            status_code=404,
            detail="Aucun produit disponible"
        )

    # -------------------------
    # Construction du contexte
    # -------------------------
    products_context = "\n".join([

        f"""
        Produit: {product.name}
        Description: {product.description}
        Prix: {product.price} Ar
        Stock: {product.stock}
        """

        for product in products
    ])

    # -------------------------
    # Création du prompt IA
    # -------------------------
    prompt = f"""
    Tu es un assistant vendeur professionnel.

    Voici les produits disponibles :

    {products_context}

    Question du client :
    {request.message}

    Réponds de manière claire, professionnelle et utile.
    """

    # -------------------------
    # Génération réponse IA
    # -------------------------
    try:

        ai_response = generate_ai_response(prompt)

    except Exception as e:

        raise HTTPException(
            status_code=500,
            detail=f"Erreur IA : {str(e)}"
        )

    # -------------------------
    # Retour de la réponse
    # -------------------------
    return ChatResponse(
        response=ai_response
    )