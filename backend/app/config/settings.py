"""
Configuration globale du projet.

Ce fichier charge :
- variables d'environnement
- configuration base de données
- clés API
"""

from dotenv import load_dotenv
import os

# Charge les variables du fichier .env
load_dotenv()

# URL PostgreSQL
DATABASE_URL = os.getenv("DATABASE_URL")

# Clé API DeepSeek
GEMINI_API_KEY = os.getenv("GEMINI_API_KEY")