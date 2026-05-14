"""
Point d'entrée principal FastAPI.
"""

from fastapi import FastAPI

from app.database import engine, Base

# Import modèles
from app.models.product import Product

# Import routes
from app.routes.products import (
    router as products_router
)

from app.routes.chat import (
    router as chat_router
)

# Création automatique tables PostgreSQL
Base.metadata.create_all(bind=engine)

# Initialisation application FastAPI
app = FastAPI(
    title="AI Customer Support API",
    description="Backend IA pour support client",
    version="1.0.0"
)

# Enregistrement routes
app.include_router(products_router)

app.include_router(chat_router)

@app.get("/")
def home():
    """
    Endpoint racine API.
    """

    return {
        "message": "AI Customer Support API"
    }