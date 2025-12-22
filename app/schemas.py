from pydantic import BaseModel, Field
from typing import List
from datetime import datetime

# ---------------- PRODUCT SCHEMAS ----------------

class CreateProduct(BaseModel):
    name: str
    price: float
    stock: int = 0
    image_url: str | None = None

class ProductResponse(BaseModel):
    id: int
    name: str
    price: float
    stock: int
    image_url: str | None

    class Config:
        from_attributes = True


# ---------------- USER SCHEMAS ----------------

class UserCreate(BaseModel):
    username: str
    password: str

class UserLogin(BaseModel):
    username: str
    password: str

class Token(BaseModel):
    access_token: str
    token_type: str = "bearer"

class UserResponse(BaseModel):
    id: int
    username: str
    is_admin: bool

    class Config:
        from_attributes = True


# ---------------- CART SCHEMAS ----------------

class CartProduct(BaseModel):
    id: int
    name: str
    price: float

    class Config:
        from_attributes = True

class CartItemResponse(BaseModel):
    product: CartProduct
    quantity: int
    subtotal: float

    class Config:
        from_attributes = True

class CartResponse(BaseModel):
    items: List[CartItemResponse]
    total: float

    class Config:
        from_attributes = True

class AddToCart(BaseModel):
    id: int
    quantity: int = Field(ge=1)

class UpdateQuantity(BaseModel):
    quantity: int = Field(ge=1)

class OrderItemResponse(BaseModel):
    product_name: str
    product_price: float
    quantity: int

    class Config:
        from_attributes = True

class OrderResponse(BaseModel):
    id: int
    total: float
    created_at: datetime
    items: list[OrderItemResponse]

    class Config:
        from_attributes = True
