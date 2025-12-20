from pydantic import BaseModel, Field
from typing import List, Optional

# Product Models

class CreateProduct(BaseModel):
    name: str
    price: int
    description: str

class ProductResponse(BaseModel):
    id: int
    name: str
    price: int

    class Config:
        orm_mode = True

# User Models

class UserCreate(BaseModel):
    username: str
    password: str

class UserLogin(BaseModel):
    username: str
    password: str

class Token(BaseModel):
    access_token: str
    token_type: str = "bearer"
