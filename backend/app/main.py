from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from contextlib import asynccontextmanager

from app.database import engine, Base
from app.routes.products import router as products_router

# === Création des tables au démarrage ===
# Base.metadata.create_all(bind=engine)   # Déplacé dans le lifespan

# === Gestion du cycle de vie de l'application ===
@asynccontextmanager
async def lifespan(app: FastAPI):
    """
    Exécute du code au démarrage et à l'arrêt de l'application.
    - Au démarrage : crée les tables si elles n'existent pas
    - À l'arrêt : ferme les connexions (optionnel)
    """
    # === Démarrage ===
    print("🚀 Création des tables en base de données...")
    Base.metadata.create_all(bind=engine)
    print("✅ Tables prêtes")
    
    yield  # L'application tourne ici
    
    # === Arrêt ===
    print("🛑 Arrêt de l'application...")
    # Ajoutez ici le nettoyage si nécessaire (ex: fermeture de connexions)

# === Création de l'application FastAPI ===
app = FastAPI(
    title="AI Customer Support API",
    description="API de gestion des produits pour le support client",
    version="1.0.0",
    lifespan=lifespan  # Utilisation du gestionnaire de cycle de vie
)

# === Configuration CORS (sécurité) ===
# Permet aux applications frontend de communiquer avec l'API
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],        # À restreindre en production
    allow_credentials=True,
    allow_methods=["*"],        # Autorise toutes les méthodes HTTP
    allow_headers=["*"],        # Autorise tous les en-têtes
)

# === Inclusion des routeurs ===
# Tous les endpoints de produits sont accessibles via /routes/products (défini dans le routeur)
app.include_router(products_router)

# === Endpoint racine ===
@app.get("/")
def home():
    """
    Endpoint de bienvenue.
    Retourne un message indiquant que l'API est en ligne.
    """
    return {
        "message": "AI Customer Support API",
        "version": "1.0.0",
        "status": "running"
    }

# === Endpoint de santé (health check) ===
@app.get("/health")
def health_check():
    """
    Endpoint utilisé par les services de monitoring.
    Retourne le statut de l'API.
    """
    return {
        "status": "healthy",
        "database": "connected"  # Idéalement, vérifier la connexion DB
    }