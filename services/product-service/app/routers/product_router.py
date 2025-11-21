from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from app.schemas.product import ProductCreate, ProductBase, ProductRead, ProductUpdate 
from app.services.product_service import ProductNotFoundError, get_product, get_products, update_product, delete_product, create_product
from app.database import get_db

router = APIRouter()

# Get a product
@router.get("/products/{product_id}", response_model=ProductRead)
def api_get_product(product_id: int, db: Session = Depends(get_db)):
    try:
        product = get_product(db, product_id)
        return product
    
    except ProductNotFoundError:
        raise HTTPException(status_code=404, detail="Product Not found")
    
# Create a product
@router.post("/products", response_model=ProductRead)
def api_create_product(product_data: ProductCreate, db: Session = Depends(get_db)):
    try:
        product = create_product(db, product_data)
        return product
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

