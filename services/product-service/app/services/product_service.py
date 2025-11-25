from sqlalchemy.orm import Session
from app.models.product import Product
from app.schemas.product import ProductCreate, ProductUpdate

# Possible Errors Classes
class ProductNotFoundError(Exception):
    pass


def get_product(db:Session, product_id: int):
    product = db.query(Product).filter(Product.id == product_id).first()

    if not product:
        raise ProductNotFoundError(f"Product Not Found")
    
    return product


def get_products(db: Session, skip: int = 0, limit: int = 100):
    products = db.query(Product).offset(skip).limit(limit).all()

    if not products:
        raise ProductNotFoundError(f"Product Not Found")
    
    return products


def create_product(db: Session, product: ProductCreate):
    db_product = Product(**product.model_dump())
    db.add(db_product)
    db.commit()
    db.refresh(db_product)
    return db_product


def update_product(db:Session, product_id: int, product: ProductUpdate):
    db_product = get_product(db, product_id)

    for key, value in product.model_dump(exclude_unset=True).items():
        setattr(db_product, key, value)
    
    db.commit()
    db.refresh(db_product)
    return db_product


def delete_product(db: Session, product_id: int):
    db_product = get_product(db, product_id)
    db.delete(db_product)
    db.commit()
    return {"message": "Product deleted"}