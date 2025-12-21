from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session, joinedload
from sqlalchemy.exc import SQLAlchemyError

from database import get_db
from models import Products, User, Cart, CartItem, Order, OrderItem
from schemas import (
    CreateProduct, ProductResponse,
    Token, UserCreate, UserLogin, UserResponse,
    AddToCart, UpdateQuantity, CartItemResponse, CartResponse, CartProduct,
    OrderResponse,OrderItemResponse
)
from auth import hash_password, verify_password, create_access_token, get_current_user, admin_required
from fastapi import UploadFile, File
from fastapi.staticfiles import StaticFiles
# app.mount("/static", StaticFiles(directory="static"), name="static")

router = APIRouter()

# ---------------------- HELPER FUNCTIONS ----------------------

def get_or_create_cart(db: Session, user_id: int):
    cart = db.query(Cart).filter(Cart.user_id == user_id).first()
    if not cart:
        cart = Cart(user_id=user_id)
        db.add(cart)
        db.commit()
        db.refresh(cart)
    return cart

# ---------------------- PRODUCT ROUTES -----------------------

@router.get("/", tags=["General"])
def read_root():
    return {"message": "Hello, world!"}

@router.get("/products/", response_model=list[ProductResponse], tags=["Products"])
def get_products(db: Session = Depends(get_db)):
    return db.query(Products).all()

@router.get("/products/{product_id}", response_model=ProductResponse, tags=["Products"])
def get_product(product_id: int, db: Session = Depends(get_db)):
    product = db.query(Products).filter(Products.id == product_id).first()
    if not product:
        raise HTTPException(status_code=404, detail="Product not found")
    return product

@router.post("/products/", response_model=ProductResponse, dependencies=[Depends(admin_required)], tags=["Products"])
def create_product(
    name: str,
    price: float,
    stock: int = 0,
    image: UploadFile | None = File(None),
    db: Session = Depends(get_db),
):
    image_url = None
    if image:
        file_location = f"static/images/{image.filename}"
        with open(file_location, "wb+") as f:
            f.write(image.file.read())
        image_url = f"/static/images/{image.filename}"

    product = Products(name=name, price=price, stock=stock, image_url=image_url)
    db.add(product)
    db.commit()
    db.refresh(product)
    return product

@router.put("/products/{product_id}", response_model=ProductResponse, dependencies=[Depends(admin_required)], tags=["Products"])
def update_product(product_id: int, updated: CreateProduct, db: Session = Depends(get_db)):
    product = db.query(Products).filter(Products.id == product_id).first()
    if not product:
        raise HTTPException(status_code=404, detail="Product not found")
    update_data = updated.model_dump(exclude_unset=True)
    for key, value in update_data.items():
        setattr(product, key, value)
    db.commit()
    db.refresh(product)
    return product

@router.delete("/products/{product_id}", dependencies=[Depends(admin_required)], tags=["Products"])
def delete_product(product_id: int, db: Session = Depends(get_db)):
    product = db.query(Products).filter(Products.id == product_id).first()
    if not product:
        raise HTTPException(status_code=404, detail="Product not found")
    db.delete(product)
    db.commit()
    return {"message": "Product deleted successfully"}

# ---------------------- USER ROUTES --------------------------

@router.post("/auth/register", response_model=Token, tags=["Auth"])
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
    return {"access_token": access_token, "token_type": "bearer"}

@router.post("/auth/login", response_model=Token, tags=["Auth"])
def login(form_data: UserLogin, db: Session = Depends(get_db)):
    user = db.query(User).filter(User.username == form_data.username).first()
    if not user or not verify_password(form_data.password, user.hashed_password):
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid credentials")
    access_token = create_access_token({"sub": user.username})
    return {"access_token": access_token, "token_type": "bearer"}

@router.get("/users", response_model=list[UserResponse], dependencies=[Depends(admin_required)], tags=["Admin"])
def get_all_users(db: Session = Depends(get_db)):
    return db.query(User).all()

@router.delete("/users/{user_id}", dependencies=[Depends(admin_required)], tags=["Admin"])
def delete_user(user_id: int, db: Session = Depends(get_db)):
    user = db.query(User).filter(User.id == user_id).first()
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    db.delete(user)
    db.commit()
    return {"message": "User deleted successfully"}

# ---------------------- CART ROUTES --------------------------

@router.post("/cart/add", tags=["Cart"])
def add_to_cart(data: AddToCart, db: Session = Depends(get_db), user: User = Depends(get_current_user)):
    cart = get_or_create_cart(db, user.id)
    item = db.query(CartItem).filter(
        CartItem.cart_id == cart.id,
        CartItem.product_id == data.id
    ).first()
    if item:
        item.quantity += data.quantity
    else:
        item = CartItem(cart_id=cart.id, product_id=data.id, quantity=data.quantity)
        db.add(item)
    db.commit()
    return {"message": "Item added to cart"}

@router.delete("/cart/remove/{product_id}", tags=["Cart"])
def remove_from_cart(product_id: int, db: Session = Depends(get_db), user: User = Depends(get_current_user)):
    cart = get_or_create_cart(db, user.id)
    item = db.query(CartItem).filter(
        CartItem.cart_id == cart.id,
        CartItem.product_id == product_id
    ).first()
    if not item:
        raise HTTPException(status_code=404, detail="Item not in cart")
    db.delete(item)
    db.commit()
    return {"message": "Item removed from cart"}

@router.patch("/cart/{product_id}", tags=["Cart"])
def change_quantity(product_id: int, data: UpdateQuantity, db: Session = Depends(get_db), user: User = Depends(get_current_user)):
    cart = get_or_create_cart(db, user.id)
    item = db.query(CartItem).filter(
        CartItem.cart_id == cart.id,
        CartItem.product_id == product_id
    ).first()
    if not item:
        raise HTTPException(status_code=404, detail="Item not in cart")
    item.quantity = data.quantity
    db.commit()
    return {"message": "Quantity updated"}

@router.get("/cart", response_model=CartResponse, tags=["Cart"])
def get_cart(db: Session = Depends(get_db), user: User = Depends(get_current_user)):
    cart = get_or_create_cart(db, user.id)
    items = db.query(CartItem).options(joinedload(CartItem.product)).filter(CartItem.cart_id == cart.id).all()
    cart_items = []
    total = 0
    for item in items:
        subtotal = item.quantity * item.product.price
        total += subtotal
        cart_items.append(CartItemResponse(product=item.product, quantity=item.quantity, subtotal=subtotal))
    return {"items": cart_items, "total": total}

# ---------------------- CHECKOUT --------------------------

@router.post("/checkout", tags=["Cart"])
def checkout(db: Session = Depends(get_db), user: User = Depends(get_current_user)):
    cart = get_or_create_cart(db, user.id)
    if not cart.items:
        raise HTTPException(status_code=400, detail="Cart is empty")

    for item in cart.items:
        if item.quantity > item.product.stock:
            raise HTTPException(status_code=400, detail=f"Not enough stock for {item.product.name}")

    try:
        # Deduct stock and clear cart
        for item in cart.items:
            item.product.stock -= item.quantity
            db.delete(item)

        db.commit()
    except SQLAlchemyError:
        db.rollback()
        raise HTTPException(status_code=500, detail="Checkout failed")

    return {"detail": "Purchase successful"}

@router.get("/orders/history", response_model=list[OrderResponse], tags=["Orders"])
def get_purchase_history(
    db: Session = Depends(get_db),
    user: User = Depends(get_current_user),
):
    orders = db.query(Order).filter(Order.user_id == user.id).options(joinedload(Order.items)).all()
    return orders
