from sqlalchemy import create_engine, Column, Integer, String, Float
from sqlalchemy.orm import sessionmaker, Session, declarative_base

from fastapi import FastAPI, HTTPException, Depends
from pydantic import BaseModel
from typing import List

from fastapi.middleware.cors import CORSMiddleware

app = FastAPI()
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

DATABASE_URL = "sqlite:///test.db"

engine = create_engine(DATABASE_URL, connect_args={"check_same_thread": False})

SessionLocal = sessionmaker(autocommit = False, autoflush= False, bind= engine)
Base = declarative_base()

class Products(Base):
    __tablename__ = "products"
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, index=True, nullable=False) 
    price = Column(Integer, nullable=False)

Base.metadata.create_all(bind=engine)

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

class CreateProduct(BaseModel):
    name: str
    price: int

class ProductResponse(BaseModel):
    id: int
    name: str
    price: int

    class Config:
        orm_mode = True


# below endpoint doesnt work for some reason

@app.get("/products/")
def get_products(db: Session = Depends(get_db)):
    return db.query(Products).all()

@app.get("/")
    
@app.post("/products/", response_model=ProductResponse)
def create_product(product: CreateProduct, db: Session = Depends(get_db)):
    db_product = Products(
        name = product.name,
        price= product.price,
    )
    db.add(db_product)
    db.commit()
    db.refresh(db_product)
    return db_product

@app.put("/products/{product_id}", response_model=ProductResponse)
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
    

@app.delete("/products/{product_id}")
def delete_product(product_id: int, db: Session = Depends(get_db)):
    product = db.query(Products).filter(Products.id == product_id).first()

    if not product:
        raise HTTPException(status_code=404, detail="Product not found")
    
    db.delete(product)
    db.commit()
    return {"message": "Product deleted successfully"}