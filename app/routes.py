from fastapi import APIRouter, Depends, HTTPException, status
from database import get_db
from models import Products, User
from sqlalchemy.orm import Session

from schemas import (
    CreateProduct,
    ProductResponse,
    Token,
    UserCreate,
    UserLogin,
    UserResponse,
)

from auth import hash_password, verify_password, create_access_token, get_current_user, admin_required
from fastapi.security import OAuth2PasswordRequestForm

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
    
@router.post("/products/", response_model=ProductResponse, dependencies=[Depends(admin_required)])
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

# USER ROUTES

@router.post("/auth/register", response_model=Token)
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

@router.post("/auth/login", response_model=Token)
def login(
    form_data: OAuth2PasswordRequestForm = Depends(),
    db: Session = Depends(get_db)
):
    user = db.query(User).filter(
        User.username == form_data.username
    ).first()

    if not user or not verify_password(
        form_data.password,
        user.hashed_password
    ):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid credentials"
        )

    access_token = create_access_token(
        data={"sub": user.username}
    )

    return {
        "access_token": access_token,
        "token_type": "bearer"
    }

@router.get("/users", response_model=list[UserResponse])
def get_all_users(
    db: Session = Depends(get_db),
    # _: User = Depends(admin_required)  uncomment when you get the swagger auth thing working
):
    return db.query(User).all()
