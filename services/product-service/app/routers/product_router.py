from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from app.schemas.product import ProductCreate, ProductBase, ProductRead, ProductUpdate 
from app.services.product_service import ProductNotFoundError, get_product, get_products, update_product, delete_product, create_product
from app.database import get_db
from typing import List

router = APIRouter()

# Get a product
@router.get("/products/{product_id}", response_model=ProductRead)
def api_get_product(product_id: int, db: Session = Depends(get_db)):
    try:
        product = get_product(db, product_id)
        return product
    
    except ProductNotFoundError:
        raise HTTPException(status_code=404, detail="Product Not found")
    
    
# Get all products
@router.get("/products", response_model=List[ProductRead])
def api_get_all_products(db: Session = Depends(get_db)):
    try:
        products = get_products(db)
        return products
    except ProductNotFoundError:
        raise HTTPException(status_code=404, detail="Products Not found")
    

# Create a product
@router.post("/products", response_model=ProductRead)
def api_create_product(product_data: ProductCreate, db: Session = Depends(get_db)):
    try:
        product = create_product(db, product_data)
        return product
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
    

# Update a product
@router.put("/products/{product_id}", response_model=ProductRead)
def api_update_product(product_id: int, product_data: ProductUpdate, db: Session = Depends(get_db)):
    try:
        product = update_product(db, product_id, product_data)
        return product
    except ProductNotFoundError:
        raise HTTPException(status_code=404, detail="Product Not found")
    except Exception as e:
        raise HTTPException(status_code=500, detail = str(e))
    

# Delete a product
@router.delete("/products/{product_id}")
def api_delete_product(product_id: int, db: Session = Depends(get_db)):
    try:
        product = delete_product(db, product_id)
        return product
    except ProductNotFoundError:
        raise HTTPException(status_code=404, detail="Product Not found")
    except Exception as e:
        raise HTTPException(status_code=500, detail = str(e))


