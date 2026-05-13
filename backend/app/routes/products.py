from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from app.database import SessionLocal
from app.models.product import Product
from app.schemas.product_schema import ProductCreate, ProductResponse

# Création d'un routeur avec un tag pour la documentation automatique
router = APIRouter(tags=["Produits"])

# Dépendance : fournit une session DB et la ferme automatiquement
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

# Endpoint : Créer un produit
@router.post("/products", response_model=ProductResponse, status_code=201)
def create_product(
    product: ProductCreate,        # Données validées via Pydantic
    db: Session = Depends(get_db)  # Injection de la session DB
):
    """
    Crée un nouveau produit en base de données.
    - **product** : objet JSON contenant name, description, price, stock
    """
    # Vérification métier : le prix et le stock doivent être positifs
    if product.price <= 0:
        raise HTTPException(status_code=400, detail="Le prix doit être supérieur à 0")
    if product.stock < 0:
        raise HTTPException(status_code=400, detail="Le stock ne peut pas être négatif")

    # Création de l'objet Product à partir des données validées
    new_product = Product(
        name=product.name,
        description=product.description,
        price=product.price,
        stock=product.stock
    )

    try:
        # Ajout et commit en base
        db.add(new_product)
        db.commit()
        # Rafraîchit l'objet pour récupérer l'ID généré automatiquement
        db.refresh(new_product)
    except Exception as e:
        # Rollback en cas d'erreur (ex: contrainte unique)
        db.rollback()
        raise HTTPException(status_code=500, detail=f"Erreur lors de la création : {str(e)}")

    return new_product

# Endpoint : Lister les produits avec pagination
@router.get("/products", response_model=list[ProductResponse])
def get_products(
    skip: int = 0,                # Nombre d'éléments à sauter (défaut 0)
    limit: int = 50,              # Nombre maximum d'éléments (défaut 50)
    db: Session = Depends(get_db)
):
    """
    Retourne la liste des produits avec pagination.
    - **skip** : index de départ
    - **limit** : nombre maximum de produits retournés
    """
    try:
        # Requête avec offset et limit pour éviter de charger trop de données
        products = db.query(Product).offset(skip).limit(limit).all()
        return products
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Erreur lors de la récupération : {str(e)}")