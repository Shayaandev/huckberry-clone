from fastapi import APIRouter, Depends, HTTPException
from database import Products, User, get_current_user, get_db
from sqlalchemy.orm import Session

from schemas import (
    CreateProduct,
    ProductResponse,
    Token,
    UserCreate,
    UserLogin,
)

router = APIRouter()

@router.get("/")
def read_root():
    return{"message": "Hello, world!"}

@router.get("/products/")
def get_products(db: Session = Depends(get_db)):
    return db.query(Products).all()

@router.get("/products/{product_id}")
def get_product(product_id: int, db: Session = Depends(get_db)):
    product = db.query(Products).filter(Products.id == product_id).first()

    if not product:
        raise HTTPException(status_code=404, detail="Product not found")

    return product
    
@router.post("/products/", response_model=ProductResponse, dependencies=[Depends(get_current_user)])
def create_product(product: CreateProduct, db: Session = Depends(get_db)):
    db_product = Products(
        name = product.name,
        price= product.price,
    )
    db.add(db_product)
    db.commit()
    db.refresh(db_product)
    return db_product

@router.put("/products/{product_id}", response_model=ProductResponse)
def update_product(product_id: int, updated: CreateProduct, db: Session = Depends(get_db)):
    product = db.query(Products).filter(Products.id == product_id).first()

    if not product:
        raise HTTPException(status_code=404, detail="Product not found")
    
    # update only the provided fields
    update_data = updated.model_dump(exclude_unset=True)
    for key, value in update_data.items():
        setattr(product, key, value)
    
    db.commit()
    db.refresh(product)
    return product
    

@router.delete("/products/{product_id}")
def delete_product(product_id: int, db: Session = Depends(get_db)):
    product = db.query(Products).filter(Products.id == product_id).first()

    if not product:
        raise HTTPException(status_code=404, detail="Product not found")
    
    db.delete(product)
    db.commit()
    return {"message": "Product deleted successfully"}

@router.post("/user", response_model=Token)
def register(user: UserCreate, db: Session = Depends(get_db)):
    if db.query(User).filter(User.username == user.username).first():
        raise HTTPException(status_code=400, detail="Username already exists")
    
    db_user = User(
        username=user.username,
        hashed_password=hash_password(user.password)
    )

    db.add(db_user)
    db.commit()
    db.refresh(db_user)

    access_token = create_access_token({"sub": db_user.username})
    return{"access_token": access_token, "token_type": "bearer"}

@router.post("/login", response_model=Token)
def login(user: UserLogin, db: Session = Depends(get_db)):
    db_user = db.query(User).filter(User.username == user.username).first()
    if not db_user or not verify_password(user.password, db_user.hashed_password):
        raise HTTPException(status_code=401, detail="Invalid credentials")
    
    access_token = create_access_token({"sub": db_user.username})
    return {"access_token": access_token, "token_type": "bearer" }